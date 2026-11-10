# ADR-0006: Vetor, geometria e consulta espacial determinísticos (#6, #7, #8): `SimVec2`, testes de acerto por distância ao quadrado e varredura linear em ordem de id

## Status
Proposed

## Date
2026-11-06

## Last Verified
2026-11-06 (contra o ADR-0001 com as Emendas 1 a 18, o ADR-0004, o ADR-0005, `docs/registry/architecture.yaml` e os GDDs #6 e #7 em disco; Unity 6.3 LTS, pin 6000.3.x)

## Decision Makers
Rodrigo Reis (escopo e alternativa A confirmados em 2026-11-06; o resto é decisão técnica por recomendação, **provisória, a reavaliar com o jogo jogável**), Claude Code (autoria), `unity-specialist` (validação, 5.5) e `technical-director` (gate TD-ADR, 5.6). Os resultados das duas revisões entram na seção Risks antes de gravar.

## Summary
O ADR-0001 proíbe `Vector3`, `Mathf` e `Unity.Mathematics` na simulação e adiou o tipo de vetor "para o ADR do #6", que nunca existiu; sem ele o #6 e o #7 não têm como escrever movimento, empurrão, hit de círculo, cone e linha, limite da arena nem busca de alvo de forma determinística. Decidido: um `SimVec2` (struct só de leitura, `X` e `Y` em `float`), funções estáticas puras em `SimGeometry` (distância ao quadrado, círculo, cone por `cos²` sem raiz, cápsula da linha, `Dir`, `EIXOS8`, arena retangular), e uma consulta `SimQuery` por varredura linear da lista de vivos em ordem de id, escrevendo num buffer do chamador. Sem grade espacial no MVP.

## Engine Compatibility

| Field | Value |
|-------|-------|
| **Engine** | Unity 6.3 LTS (6000.3.x; editor instalado 6000.3.27f1) |
| **Domain** | Core |
| **Layer** | Core (igual aos ADRs 0001, 0004 e 0005; não existe `docs/architecture/architecture.md` nem mapa de camadas, então a camada foi confirmada pelo autor em 2026-11-06) |
| **Knowledge Risk** | MEDIUM (a superfície de API é LOW: nenhuma API da Unity, só `float`, `struct` e `MathF.Sqrt`; o comportamento em runtime IL2CPP, isto é, inlining de operadores de struct e `sqrt` entre runtimes, não é coberto por `docs/engine-reference`); a linha do engine é HIGH em `VERSION.md:34`; não existe `modules/core.md` |
| **References Consulted** | `docs/engine-reference/unity/VERSION.md`, `breaking-changes.md`, `deprecated-apis.md`, `current-best-practices.md`; ADR-0001 (Numérico, Emendas 6 e 12, Key Interfaces), ADR-0004 (colunas de posição em `X`/`Y`), ADR-0005 (`HitRequest` com direção de knockback); GDDs #6 (Regras 2.5, 4, 5, 6; F3, F5, F8, F10) e #7 (Regras 2, 7; F4, F5). **Não existe `modules/core.md`**: nada do domínio Core foi checado contra um módulo de referência (`NOT SOURCEABLE`) |
| **Post-Cutoff APIs Used** | Nenhuma. Só `readonly struct`, operadores, `static` puros e `MathF.Sqrt` (BCL anterior ao cutoff; a disponibilidade no perfil de API do projeto é `NOT SOURCEABLE`, já a Verification Required 4 e 6 do ADR-0001). |
| **Verification Required** | (1) Testes de fronteira de cada função (círculo inclusivo, ápice do cone, segmento degenerado, clamp deslizando na parede, `EIXOS8` unitários), rodando no Editor e em IL2CPP. (2) Zero alocação gerenciada por `Tick` com 300 vivos e as consultas do tick (AC-P2 do #6). (3) Custo das consultas de varredura com 300 vivos no aparelho de referência, contra `orcamento_combate_ms` (OQ-14 do #6). (4) `NOT SOURCEABLE`: `MathF.Sqrt` dar o mesmo bit em Mono x64 e IL2CPP ARM64 (a raiz quadrada de IEEE 754 é arredondada corretamente por padrão, mas nenhum doc do projeto a cobre); fica no spike de hash do ADR-0001. (5) `NOT SOURCEABLE`: inlining dos operadores de `SimVec2` sob IL2CPP em Release; medir antes de reescrever à mão. (6) **`NOT ASSESSED`**: a abertura do cone não está definida em nenhum GDD (Decisão 6). |

## ADR Dependencies

| Field | Value |
|-------|-------|
| **Depends On** | ADR-0001 (`Proposed`; `float32`, `SimMath`, listas de vivos em ordem de id, Emendas 17 e 18; a ordem do `Step` e a do `Preparar`, Emenda 19(a)(f)), ADR-0002 (`Proposed`; o `cos2Meia` calculado em `decimal` no build e a `Arena` como seção do snapshot, lida pelo compositor no tipo concreto), ADR-0004 (`Proposed`; posição em colunas `X`/`Y`, `IsAlive`, `Factions`) e ADR-0005 (`Proposed`; a regra do `KbDir`/`DirExplicita` do `Aplicar`: `HitRequest` com `SourceId`, `KbDistancia`, `KbDirX`/`KbDirY` e `HitFlags.DirExplicita`, e o `Aplicar` que recusa `SourceId = −1` com knockback sem `DirExplicita`). Este ADR só pode ser aceito depois dos quatro. |
| **Enables** | Épicos de #6 e #7; GDD #8 (as áreas da suprema usam `SimQuery`); ADR do log (#5) não depende |
| **Blocks** | Stories de movimento, empurrão, telegraph, contato e auto-ataque do #6; posição de nascimento do #7; TR-combate-010, TR-horda-004 e TR-horda-005 (hoje "BLOQ: ADR"). A story de golpe de forma `Cone` fica bloqueada até os GDDs #6 e #7 definirem a abertura do cone (`NOT ASSESSED`). |
| **Ordering Note** | Ordem de aceite: ADR-0001, ADR-0002, ADR-0004, ADR-0005 e depois este ADR (emenda da rodada 5: a dependência do ADR-0005 passou a ser real, pela regra do `KbDir`/`DirExplicita`). O ADR-0005 não depende deste ADR: ele só carrega a direção do knockback com `DirExplicita`, e a dependência inversa fica em Enables do ADR-0005; este ADR fornece `KbDir`, `Dir` e `Axis8` (Decisão 5). Se um dia houver separação entre corpos (OQ-7 e OQ-9 dos GDDs), entra um ADR novo com a grade uniforme por trás da mesma API de `SimQuery`. |

## Context

### Problem Statement
O GDD #6 mede tudo em metros e em `float32`: o passo de cada inimigo até o herói com parada em `dist_parada_m` (Regra 2.5), o knockback com decaimento linear e vetor nulo (F3), o contato por distância ao quadrado (Regra 5), o teste de acerto do telegraph em círculo, cone ou segmento da linha, travado no início do Aviso (Regra 6), o `clampArena` por eixo (F3), a supressão do hit-stop por distância (F8) e a escolha do alvo do auto-ataque (Regra 4). O GDD #7 acrescenta a posição de nascimento como função pura de direções literais, com espelho por eixo (Regra 7), e a arena retangular (Regra 2). O ADR-0001 diz que o vetor é "`SimVec2` ou equivalente, definido pelo ADR de #6" e que tudo além de `+ - * /` passa por `SimMath`. Sem este ADR cada sistema reinventaria o vetor e a geometria, e um detalhe (ordem das contas, `==` em `float`, raiz quadrada desnecessária) mudaria o resultado entre sistemas.

### Constraints
- ADR-0001: só `float`; `SimMath` para `Sqrt`, `Abs`, `Min`, `Max`, `Clamp`, `Lerp`; sem trigonometria, sem `Vector3`, `Mathf`, `Unity.Mathematics`; iteração por id crescente; nenhuma alocação por `Tick`; sem `static` mutável.
- ADR-0004: a posição mora em colunas `X`/`Y` separadas; o `SimVec2` não pode virar outro armazenamento.
- Dev solo: poucas funções, todas pequenas, com testes de fronteira.
- Aparelho móvel: 300+ vivos e poucos ms por tick.

### Requirements
- Um tipo de vetor e funções de geometria que todos os sistemas compartilhem, determinísticas e sem alocação.
- Testes de acerto que não dependam de `Sqrt` nem de trigonometria.
- A mesma geometria da arena no #6 (`clampArena`) e no #7 (espelho do nascimento).
- Uma consulta espacial para o auto-ataque e as áreas do #8, com ordem determinística, que não exija reescrever os chamadores quando a grade vier.

## Decision

### 1. `SimVec2` e `Arena`
Em `Forja.Simulation` (Core):
- **`SimVec2`**: `readonly struct` com `float X, Y`, construtor, `+`, `-`, multiplicação por escalar, `Dot` e `LenSq`. **Não tem propriedade `Length`**: o comprimento exige `SimMath.Sqrt(LenSq)` escrito à mão, para que cada raiz quadrada seja uma decisão visível. Unidade: metros. Sem `==` nem `Equals` em `float` (Decisão 4).
- **`SimVec2` é só uma vista por valor.** O armazenamento continua nas colunas `X`/`Y` do ADR-0004 (`PosX[id]`, `PosY[id]`); `new SimVec2(PosX[id], PosY[id])` monta o vetor e nenhum sistema guarda `SimVec2` em tabela própria no lugar da coluna.
- **`Arena`**: `readonly struct` do retângulo alinhado aos eixos `[0, Largura] × [0, Altura]` (GDD #7, Regra 2; confirma a OQ-10 do #6). **Quem constrói:** o compositor (`Forja.Gameplay.Sim`), uma vez por fase, a partir do snapshot concreto (o Core só enxerga `IPhaseSnapshot`, que não tem a largura), e a entrega por valor ao #6 e ao #7. `MaxBodyRadius` é o maior raio entre o herói e os arquétipos da fase (um `max` é exato em `float`). O construtor lança nos dois modos se `Largura`, `Altura` ou `maxBodyRadius` não for finito, se `maxBodyRadius` for negativo ou se `Largura` ou `Altura` não passar de `2 × maxBodyRadius` (guarda contra bug; a validação de verdade é a F5 do #7, com o fator 2,02, feita pelo #1 no build). A `Arena` guarda `MaxBodyRadius`, e `default(Arena)` (largura 0) é inválido: `IsValid` é falso e o compositor o confere ao construir e antes de entregá-la ao #7 e ao #6, portanto antes do `Create` e do `Preparar` (o `Preparar(SimWorld)` do ADR-0001 não recebe a `Arena`; o `Preparar` não confere `IsValid`). É estado derivado dos dados, fora do hash, e o mesmo valor serve ao `clampArena` do #6 e ao espelho do nascimento do #7 (TR-horda-005).

### 2. `SimGeometry`: funções estáticas puras
Em `Forja.Simulation`, sem estado e sem alocação; **nenhuma função de `SimGeometry` lança por valor** (a precondição é do chamador): só o construtor de `Arena` e `Arena.Clamp` com raio acima de `MaxBodyRadius` (bug interno, nos dois modos) lançam; `SimQuery` lança numa precondição de buffer ou de filtro inválido. Todas as comparações são **inclusivas** (`≤`) salvo onde dito. Todo literal numérico leva o sufixo `f` (um literal sem `f` compara ou multiplica em `double` sem erro de compilação).

| Função | Contrato |
|---|---|
| `DistSq(a, b)` | `(a−b)·(a−b)`, sem raiz |
| `Dir(d)` | `len = SimMath.Sqrt(LenSq(d))` e **cada componente dividida por `len`** (nunca multiplicada por `1f / len`, que arredonda diferente), ou **`(1, 0)` se `LenSq(d) < DirEpsSq`** (a regra `dir` da F3: Aviso, investida e mira nunca têm vetor nulo nem NaN com entrada finita) |
| `KbDir(d, id)` | como `Dir`, mas com vetor nulo devolve `Axis8(id & 7)` (a regra `dir_kb` da F3, para a horda sobreposta não ir toda para +x) |
| `Axis8(i)` | as 8 direções de `EIXOS8` por switch expression sobre `i & 7` (função total, sem `throw`) que devolve `SimVec2` de literais (`1f`, `0f` e, nas diagonais, `InvSqrt2 = 0.70710678f` com os sinais); **sem tabela `static`**; as diagonais têm módulo² `1 ± 1 ulp` |
| `InCircle(centro, r2, p)` | `DistSq(centro, p) ≤ r2` |
| `InCone(ápice, dir, alcance2, cos2Meia, p)` | com `d = p − ápice`: `LenSq(d) ≤ alcance2` **e** `Dot(dir, d) ≥ 0` **e** `Dot² ≥ cos2Meia × LenSq(d)`. Sem raiz e sem trigonometria. **Precondições do chamador:** `dir` é unitário (só vem de `Dir()` ou `Axis8`; sem isso o cone muda de abertura em silêncio, e `dir = (0,0)` com `cos2Meia = 0` vira o disco inteiro) e `alcance2 ≥ 0`. Vale para meia-abertura em **(0°, 90°]**, isto é, `cos2Meia ∈ [0, 1)`: `cos2Meia = 0` é o semicírculo (a cláusula `Dot ≥ 0` carrega a semântica) e `1` seria só a linha colinear, vazia em `float`. O alvo exatamente no ápice está dentro |
| `DistSqToSegment(p, a, b)` | `ab = b − a`; se `LenSq(ab) < DirEpsSq`, `DistSq(p, a)` (o círculo em `a`, como o GDD #6 manda para a linha colada na parede); senão `t = Clamp(Dot(p − a, ab) / LenSq(ab), 0, 1)` e `DistSq(p, a + ab × t)` |
| `InCapsule(p, a, b, r2)` | `DistSqToSegment(p, a, b) ≤ r2` (a `linha` do GDD #6: `raio_golpe` é a meia largura) |
| `Arena.Clamp(p, raio)` | por eixo: `x = SimMath.Clamp(x, raio, Largura − raio)`, `y` igual; **precondição `raio ≤ MaxBodyRadius`**, impossível de violar por construção (o `MaxBodyRadius` é o maior raio da fase), então a violação é bug interno e **lança nos dois modos**; o excedente se perde e o movimento desliza ao longo da parede (F3) |
| `Arena.OutsideX(x)` e `OutsideY(y)` | `x < 0f ∥ x > Largura` e `y < 0f ∥ y > Altura`; **por eixo**, porque o espelho da F4 do #7 reflete cada eixo separadamente e a Regra 7.4 precisa saber qual eixo espelhou |

**`SimMath` é a classe estática do ADR-0001 (`Forja.Simulation`), que só lista os nomes; este ADR fixa os corpos de `Clamp`, `Min` (`a < b ? a : b`) e `Max` (`a > b ? a : b`) no mesmo molde, e o ADR-0001 recebe uma nota de sincronia (ver GDD Sync).** `SimMath.Clamp(x, lo, hi)` é `x < lo ? lo : (x > hi ? hi : x)`: não lança, o NaN atravessa (as duas comparações dão `false` e devolve `x`) e `lo > hi` dá um resultado determinístico, ainda que sem sentido. **Não** se implementa com `Math.Clamp` nem com `MathF.Min/Max`, porque o lançamento em `min > max` e a propagação de NaN deles por runtime são `NOT SOURCEABLE`.

`DirEpsSq = 1e-6f` é uma **constante numérica de compilação** (um limiar contra vetor nulo, não um valor de gameplay), única para o #6 e o #7. Nenhuma função devolve ou aceita ângulo.

### 3. `SimQuery`: varredura linear em ordem de id
Em `Forja.Simulation`, estática e sem alocação:
- `CollectInCircle(SimWorld world, SimVec2 centro, float r2, FactionFilter alvo, Span<int> resultado)` devolve a contagem. Percorre `world.Alive` **em ordem crescente de id**, filtra por facção (`FactionFilter`: `HostileToHero ⇔ Factions[id] != Factions[Phase.HeroId]`; `AlliedToHero ⇔` mesma facção do herói e `id != Phase.HeroId`, isto é, **sem o próprio herói** *(provisória)*; `None` não casa nada e um valor fora da tabela lança; o "hostil" é o mesmo do `Rugido` do ADR-0005) e por `IsAlive`, testa `InCircle` e escreve os ids em ordem crescente. `CollectInCone` e `CollectInCapsule` são iguais, com os testes da Decisão 2.
- `NearestInCircle(world, centro, r2, alvo, out int id, out float d2)` devolve o de **menor `DistSq`**, e no empate o de **menor id** (a varredura é crescente e só troca com `<` estrito). Sem candidato devolve `false`, com `id = -1` e `distSq = 0f`. É a regra de base do auto-ataque (Regra 4 do #6); a prioridade "elite ou chefe em Recuperação primeiro" é do #6 e não entra aqui.
- **Precondição:** `resultado.Length ≥ world.Alive.Length`, conferida na entrada (lança `SimInvariantException` nos dois modos). Quem chama aloca o buffer **uma vez** no `Preparar`, com `EntityCapacity` posições (cerca de 4,5 KB com 1124 linhas; `AliveCapacity` não existe no `SimWorld`, só no snapshot), e o reusa, então a consulta nunca estoura nem aloca. O buffer é **scratch do chamador**: fora do hash e válido só até a próxima consulta. A consulta vê os ids que estão em `Alive` no instante da chamada, **inclusive os nascidos antes no mesmo tick** (o `Spawn` acrescenta o id ao fim de `Alive` na hora; o ADR-0001 recebe a frase, ver GDD Sync).
- **Quem pode usar:** qualquer sistema dentro do seu `Step`. As consultas só leem; o filtro por `IsAlive` vale no instante da chamada (as mortes acontecem no passo 7b do #6, no passo 6 do Core e depois do 7b, pelo #3 e pelo #16, que rodam depois do #6 na ordem do `Step` #7 → #8 → #6 → #3 → #16, ADR-0001 Emenda 19(f); ver ADR-0005, Decisão 5; o `SimQuery` filtra por `IsAlive`, então não há efeito prático).
- **Custo:** O(vivos) por consulta, na ordem de ~300 distâncias ao quadrado. Com uma consulta do auto-ataque e as `fontes_de_area_por_tick` do #8, são poucos milhares de contas por tick. **Não há grade espacial no MVP** (TR-horda-012; OQ-7 e OQ-9 dos GDDs). Se o spike de performance ou a separação entre corpos pedirem a grade, um ADR novo a põe por trás desta mesma API. **Custo escondido:** o #6 grava posições no passo 5 e consulta no passo 6, então uma grade teria de morar no Core e ser reconstruída (ou invalidada a cada escrita de posição) depois do passo 5, e teria de devolver os ids em ordem crescente.

### 4. Regras de determinismo
- **Nenhuma comparação `==` ou `Equals` entre `float` ou `SimVec2`.** Dois vetores "iguais" se decidem por inteiro: a classe de vetor da Regra 7.4 do #7 é um id inteiro pré-calculado em `decimal` no build (TR-horda-021), e o espelho do nascimento compara esses ids.
- **Sem raiz quadrada nos testes.** `Sqrt` só aparece em `Dir`/`KbDir`, em `Length` escrito à mão e no passo de parada do #6 (Regra 2.5). Testes de alcance, contato, supressão, círculo, cone e cápsula comparam distâncias ao quadrado.
- **Ordem das contas fixa**, produto e soma em instruções separadas, sem `MathF.FusedMultiplyAdd`; a contração implícita do compilador do IL2CPP não é controlável e é o risco já aceito no ADR-0001.
- **Entrada não finita:** as funções não validam (caminho quente); uma comparação com NaN dá `false`, e o Core já encerra a fase ou mata a entidade quando posição ou HP de um vivo não é finito (ADR-0001, Emendas 6 e 8). Nenhuma função de `SimGeometry` lança por valor (só o construtor de `Arena` e `Arena.Clamp` com raio acima de `MaxBodyRadius`); `SimMath.Clamp` não lança e deixa o NaN atravessar. `Dir` devolve `(1,0)` para vetor nulo e nunca NaN **com entrada finita**; com entrada NaN devolve NaN.
- **Posição de nascimento e movimento do herói** usam a posição do início do tick, lida antes de qualquer escrita, como os GDDs mandam; isso é do #6 e do #7, não desta API.

### 5. Onde cada função é usada

| Regra do GDD | Função |
|---|---|
| #6 Regra 2.5: passo até o herói, parada em `FATOR_PARADA × dist_parada_m`, alvo de mira da `Horda` | `SimVec2`, `DistSq`, `Sqrt` explícito, `Dir`, tabela de mira (dado do #7, 32 entradas) |
| #6 F3: knockback `dir_kb`, `clampArena`, regra "vence" (`v0_novo² > LenSq(v_atual)`, sem raiz) | `KbDir`, `Axis8`, `LenSq`, `Arena.Clamp` |
| #6 Regra 5: contato `dist² ≤ alcance_contato²` | `DistSq`, `InCircle` |
| #6 Regra 6: acerto do Impacto em círculo, cone e `linha` | `InCircle`, `InCone`, `InCapsule`, `DistSqToSegment` |
| #6 Regra 4: alvo do auto-ataque | `NearestInCircle` (mais a prioridade do #6) |
| #6 F8: supressão do hit-stop (a `linha` mede até o segmento travado) | `DistSq`, `DistSqToSegment` |
| #6 F10: Impactos "que alcançam o herói" | **interpretação provisória:** os testes de forma da Regra 6, com a posição do herói no início do tick do Aviso novo e sem margem; o GDD #6 não define o predicado (pendência `NOT ASSESSED`; não conta como requisito coberto) |
| #7 Regra 7 / F4: posição de nascimento (herói + `d × R_spawn`, espelho por eixo) | `Arena.OutsideX`, `Arena.OutsideY`, `SimVec2`; a função de nascimento é do #7 |
| #8 (GDD futuro): áreas da suprema | `CollectInCircle`, `CollectInCone`, `CollectInCapsule` |

**Direção do knockback (junto com o ADR-0005).** Sem `DirExplicita`, o #6 chama `KbDir(pos[alvo] − pos[fonte], alvo)` com as posições depois do passo 5. Com `DirExplicita`, `KbDirX`/`KbDirY` vêm de `Dir` ou `Axis8` e o #6 não renormaliza. `SourceId = −1` (área sem entidade, do #8) exige `DirExplicita`, e o `Aplicar` recusa o pedido sem ela (nota de sincronia no ADR-0005).

### 6. O cone: representação, e o que falta
O cone é descrito por `alcance` (já em metros), a direção travada e **`cos2Meia`**, o quadrado do cosseno da meia-abertura, calculado **em `decimal` no build** (ADR-0002) e guardado como `float`. Isso evita trigonometria na simulação. **Nenhum GDD define a abertura do cone** (nem o #6 nem o #7, que descrevem a forma só como "cone" com `raio_golpe` = alcance), então o valor, a faixa válida (aqui, `cos2Meia ∈ [0, 1)`) e a validação pelo #1 são `NOT ASSESSED` e ficam como pendência dos GDDs #6, #7 e #1. Enquanto isso o #1 **recusa** um golpe de forma `Cone` sem `cos2Meia` (o contrato exige o campo; não há valor padrão). Nenhum golpe do elenco do MVP do #7 usa cone (o Campeão usa linha e círculo, o Arremessador usa círculo), então o risco imediato é baixo; a story de golpe `Cone` fica bloqueada até a abertura ser definida.

### Architecture Diagram
```
 Forja.Simulation (Core)
 ┌───────────────────────────────────────────────────────────────────────────────┐
 │ SimVec2 (readonly struct, vista por valor)   Arena (AABB [0,L]x[0,A], raio)    │
 │ SimGeometry: DistSq · Dir · KbDir · Axis8 · InCircle · InCone · DistSqToSegment│
 │              InCapsule · Arena.Clamp · OutsideX/Y           (puras, sem alocação)│
 │ SimQuery:    CollectInCircle/Cone/Capsule · NearestInCircle (varredura em id ↑) │
 └───────────────▲───────────────────────────▲───────────────────────────▲────────┘
        colunas X/Y (ADR-0004)           #6 Combate                    #7 Horda / #8
        World.Alive, IsAlive, Factions   (movimento, hits, alvo)       (nascimento, áreas)
```

### Key Interfaces
```csharp
namespace Forja.Simulation
{
    public readonly struct SimVec2
    {
        public readonly float X, Y;
        public SimVec2(float x, float y) { X = x; Y = y; }
        public static SimVec2 operator +(SimVec2 a, SimVec2 b) => new SimVec2(a.X + b.X, a.Y + b.Y);
        public static SimVec2 operator -(SimVec2 a, SimVec2 b) => new SimVec2(a.X - b.X, a.Y - b.Y);
        public static SimVec2 operator *(SimVec2 a, float s) => new SimVec2(a.X * s, a.Y * s);
        public static SimVec2 operator /(SimVec2 a, float s) => new SimVec2(a.X / s, a.Y / s);   // usado por Dir; nunca multiplicar por 1f / s
        public static float Dot(SimVec2 a, SimVec2 b) { float px = a.X * b.X; float py = a.Y * b.Y; return px + py; }   // produto e soma separados
        public static float LenSq(SimVec2 a) => Dot(a, a);
        // sem Length, sem ==, sem Equals(float)
    }

    public readonly struct Arena
    {
        public Arena(float width, float height, float maxBodyRadius);   // construída pelo compositor; lança nos dois modos se não finito, maxBodyRadius < 0 ou width/height <= 2 * maxBodyRadius
        public float Width { get; }  public float Height { get; }  public float MaxBodyRadius { get; }
        public bool IsValid { get; }                       // false em default(Arena); o compositor confere ao construir (Decisão 1), não o Preparar
        public SimVec2 Clamp(SimVec2 p, float radius);     // por eixo; desliza na parede; precondição radius <= MaxBodyRadius (violar é bug interno: lança nos dois modos)
        public bool OutsideX(float x);                     // por eixo, para o espelho do nascimento (#7)
        public bool OutsideY(float y);
    }

    public static class SimGeometry
    {
        public const float DirEpsSq = 1e-6f;     // limiar contra vetor nulo (numérico, não gameplay)
        public static float DistSq(SimVec2 a, SimVec2 b);
        public static SimVec2 Dir(SimVec2 d);                    // (1,0) se LenSq < DirEpsSq
        public static SimVec2 KbDir(SimVec2 d, int targetId);    // Axis8(targetId & 7) se LenSq < DirEpsSq
        public static SimVec2 Axis8(int i);                      // switch expression sobre i & 7, total, sem tabela static e sem throw
        public static bool InCircle(SimVec2 center, float r2, SimVec2 p);
        public static bool InCone(SimVec2 apex, SimVec2 dir, float range2, float cos2Half, SimVec2 p);   // dir unitário (de Dir/Axis8); range2 >= 0; meia-abertura em (0, 90] graus, cos2Half em [0, 1)
        public static float DistSqToSegment(SimVec2 p, SimVec2 a, SimVec2 b);
        public static bool InCapsule(SimVec2 p, SimVec2 a, SimVec2 b, float r2);
    }

    public enum FactionFilter : byte { None = 0, HostileToHero = 1, AlliedToHero = 2 }   // None não casa nada (resultado vazio); valor fora da tabela lança (default do switch); explícito, só cresce no final

    public static class SimQuery
    {
        // Em ordem crescente de id; result.Length >= world.Alive.Length (senão lança SimInvariantException; o chamador aloca uma vez, por EntityCapacity); devolve a contagem.
        public static int CollectInCircle(SimWorld world, SimVec2 center, float r2, FactionFilter filter, Span<int> result);
        public static int CollectInCone(SimWorld world, SimVec2 apex, SimVec2 dir, float range2, float cos2Half, FactionFilter filter, Span<int> result);
        public static int CollectInCapsule(SimWorld world, SimVec2 a, SimVec2 b, float r2, FactionFilter filter, Span<int> result);
        public static bool NearestInCircle(SimWorld world, SimVec2 center, float r2, FactionFilter filter, out int id, out float distSq);   // menor DistSq; empate: menor id; sem candidato: false, id = -1, distSq = 0f
    }
}
```
`Alive`, `IsAlive`, `Factions` e `Phase.HeroId` vêm do `SimWorld` (ADR-0001 e ADR-0004).

### Implementation Guidelines
- O vetor da simulação **must** ser o `SimVec2`; **must never** usar `Vector2`, `Vector3`, `Mathf`, `Unity.Mathematics` nem tipo de vetor próprio de outro sistema.
- `SimVec2` **must** ser `readonly struct`, **must never** ter `Length`, `==` nem `Equals` sobre `float`, e **must never** ser guardado em tabela de entidade no lugar das colunas `X`/`Y` do ADR-0004.
- Os testes de alcance, contato, supressão, círculo, cone e cápsula **must** comparar distâncias ao quadrado; **must never** chamar `Sqrt` para decidir um acerto.
- Nenhuma função da geometria **must** usar trigonometria, ângulo, `Atan2`, `Pow` ou `Exp`; o cone **must** usar `cos2Meia` calculado no build.
- `EIXOS8` **must** ser `SimGeometry.Axis8` (um `switch` de literais); **must never** ser um array `static` (um array `static readonly` tem elementos mutáveis).
- `DirEpsSq` **must** ser a única constante de vetor nulo, para `Dir`, `KbDir` e `DistSqToSegment`; **must never** haver outro limiar no #6 ou no #7.
- O produto e a soma de `Dot` **must** ficar em instruções separadas, e **must never** haver `MathF.FusedMultiplyAdd`; isso ajuda, mas não garante que o compilador do IL2CPP não contraia `a*b + c*d` (risco aceito do ADR-0001).
- `Dir` **must** dividir cada componente por `len` e **must never** multiplicar pelo inverso; todo literal numérico da geometria **must** levar o sufixo `f`.
- `SimMath.Clamp`, `Min` e `Max` **must** ser `x < lo ? lo : (x > hi ? hi : x)`, `a < b ? a : b` e `a > b ? a : b`; **must never** ser implementados com `Math.Clamp`, `Math.Min/Max` nem `MathF.Min/Max`.
- A regra "vence" do knockback **must** comparar `v0_novo²` com `LenSq(v_atual)`; **must never** usar `Sqrt` para decidir.
- A `Arena` **must** ser construída pelo compositor uma vez por fase, com o maior raio de corpo da fase (o herói e os arquétipos), e entregue por valor ao #6 e ao #7, que **must** usar a mesma; **must never** ser hasheada, e `default(Arena)` **must never** ser usado (`IsValid`).
- As consultas **must** varrer `World.Alive` em ordem crescente de id, **must** escrever num buffer do chamador (scratch dele, fora do hash) de comprimento ≥ `World.Alive.Length`, dimensionado por `EntityCapacity` e alocado uma vez, e **must never** alocar, usar `List<T>`, delegate, LINQ nem `Dictionary`.
- `NearestInCircle` **must** trocar o candidato só com `<` estrito, para o empate cair no menor id.
- Quem precisar de uma estrutura espacial (grade, quadtree) **must** pôr um ADR novo e **must** manter a API de `SimQuery`.
- O golpe de forma `Cone` **must** trazer `cos2Meia` calculado no build, e o #1 **must** recusá-lo sem esse campo; o chamador de `InCone` **must** passar `dir` unitário, vindo de `Dir` ou `Axis8`.

## Alternatives Considered

### Alternative 1 (B): grade uniforme já no MVP
- **Description**: dividir a arena em células e indexar os vivos por célula a cada tick, para as consultas e a separação entre corpos.
- **Pros**: consultas O(vizinhos); abre a porta para separação e bloqueio de corpo.
- **Cons**: estado novo por tick (reconstruir ou atualizar a grade) que precisa ser limpo e testado; nenhuma regra do MVP precisa de separação (a horda se sobrepõe, Regra 5 do #6); com 300 vivos a varredura custa poucos milhares de contas.
- **Rejection Reason**: custo sem requisito. O TR-horda-012 e as OQ-7 e OQ-9 dos GDDs já adiam a grade ao spike de performance; a API de `SimQuery` foi escolhida para a trocar sem mudar os chamadores.

### Alternative 2 (C): sem tipo de vetor, só pares de `float`
- **Description**: cada sistema trabalha com `x` e `y` soltos.
- **Pros**: nenhum tipo novo; casa direto com as colunas do ADR-0004.
- **Cons**: verboso; fácil trocar `x` e `y` ou esquecer um eixo; cada sistema reescreve `DistSq` e `Dir`, com limiares que divergem.
- **Rejection Reason**: o ADR-0001 já prevê o tipo; a duplicação é o risco real.

### Alternative 3 (D): `Unity.Mathematics.float2`
- **Rejection Reason**: banida pelo ADR-0001 (`unityengine_in_simulation`): o determinismo do pacote é `NOT SOURCEABLE`.

### Alternative 4 (E): testes com `Sqrt` (distância real)
- **Description**: comparar `Length(d) ≤ raio`.
- **Cons**: uma raiz quadrada a mais por teste, com arredondamento extra, e custo sem ganho.
- **Rejection Reason**: a distância ao quadrado dá o mesmo resultado lógico sem a raiz.

### Alternative 5 (F): cone por ângulo (`Atan2`/`Acos`)
- **Rejection Reason**: banida (funções transcendentais fora do estado, ADR-0001); o `cos²` calculado no build resolve sem trigonometria.

### Alternative 6 (G): ponto fixo só para a geometria
- **Rejection Reason**: contradiz o ADR-0001 (um só tipo numérico); a troca para ponto fixo é um ADR de substituição inteiro (#22, #40).

## Consequences

### Positive
- Um só vocabulário de geometria para #6, #7 e #8, com contratos de fronteira testáveis.
- Sem raiz e sem trigonometria nos testes: menos arredondamentos e menos risco entre runtimes.
- A consulta espacial é estável: a grade, se vier, não muda os chamadores.
- `Arena` e `DirEpsSq` únicos eliminam divergência entre o #6 e o #7.

### Negative
- A varredura linear custa O(vivos) por consulta; se as áreas do #8 crescerem, o spike pode pedir a grade.
- A meia-abertura do cone fica limitada a 90° (um cone mais largo exige outra fórmula).
- O `SimVec2` sem `Length`, `==` e `Equals` é incômodo para quem vem do Unity.
- A abertura do cone continua sem definição nos GDDs (`NOT ASSESSED`).

## Risks
- **Contração de `float` no IL2CPP** muda o resultado entre runtimes: já aceita no ADR-0001 (mesmo build).
- **`MathF.Sqrt` entre Mono e IL2CPP** (Verification Required 4): a raiz de IEEE 754 é determinística por padrão, mas nenhum doc do projeto a cobre; só entra em `Dir`/`KbDir` e no passo de parada.
- **Cone sem abertura nos GDDs:** o #6 e o #7 não podem fechar o golpe `Cone` sem o dado. Mitigação: o contrato exige `cos2Meia` e o #1 recusa o golpe sem ele; pendência registrada.
- **Estouro da varredura** com muitas fontes de área: mitigação é o AC-P1 do #6 e a Alternativa 1.
- **Limiar `DirEpsSq` único** pode esconder um caso de vetor quase nulo legítimo: aceito, porque o valor 1e-6 vem do GDD #6.
- **Grade futura não é troca gratuita:** o #6 grava posições no passo 5 e consulta no passo 6, então uma grade precisaria morar no Core e ser reconstruída depois do passo 5, devolvendo ids em ordem crescente (Decisão 3). A assinatura estática que recebe `SimWorld` a aguenta.
- **Predicado da F10 ("alcança o herói") e abertura do cone sem definição nos GDDs:** pendências `NOT ASSESSED`, marcadas como parcial no rastreio e bloqueando a story de golpe `Cone`.
- **Resultado do `unity-specialist` (5.5, 2026-11-06): dois bloqueios de contrato, ambos revistos e confirmados pelo autor.** B1: `Arena.Clamp` podia inverter os limites e o contrato de `SimMath.Clamp` não existia; agora `SimMath.Clamp` é por comparação (não lança, NaN atravessa) e a `Arena` guarda `MaxBodyRadius`. B2: o cone não tinha precondição de `dir` unitário e a faixa de `cos2Meia` contradizia "0° a 90°"; agora é (0°, 90°] com `cos2Meia ∈ [0, 1)`. A conta do cone e da cápsula foi conferida e está correta. Notas aplicadas: `Axis8` total por `i & 7`, `Dir` divide por componente, literais com `f`, semântica de `FactionFilter.None`, retorno de `NearestInCircle` sem candidato, `default(Arena)` inválido, testes de fronteira exatos. `NOT SOURCEABLE`: `MathF.Sqrt` entre runtimes, inlining, contração do clang.
- **Resultado do `technical-director` (TD-ADR, 5.6, 2026-11-06): CONCERNS, 0 bloqueantes, 8 importantes e 6 menores, todos de especificação; revisão escolhida pelo autor (itens 1 a 14) e aplicada:** `Arena` construída pelo compositor, com `MaxBodyRadius` e `Clamp` que lança nos dois modos; `OutsideX`/`OutsideY`; `FactionFilter` sobre a facção do herói; buffer por `Alive.Length` e dimensionado por `EntityCapacity`; direção do knockback sem `DirExplicita`; corpos de `SimMath.Clamp`/`Min`/`Max`; F10 provisória; cone parcial no rastreio; F8 da `linha`; regra "vence" sem raiz; frase de lançamento restrita a `SimGeometry`; validação de `passo_min_tick` e `dist_parada_m` pelo #1; buffer como scratch; custo da grade futura.

## GDD Requirements Addressed

| GDD System | Requirement | How This ADR Addresses It |
|------------|-------------|--------------------------|
| combate-e-dano.md (TR-combate-010) | Tipo vetorial próprio e geometria determinística: círculo, cone, segmento da linha, `clampArena`, `EIXOS8`, `dir` (1,0), sem trigonometria | **Parcial:** coberto pelas Decisões 1 e 2, **exceto a abertura do cone (`NOT ASSESSED`, Decisão 6)** |
| combate-e-dano.md (Regra 2.5, F3) | Passo até o herói com parada, mira da `Horda`, knockback e vetor nulo | `SimVec2`, `Dir`, `KbDir`, `Axis8`, `Arena.Clamp` |
| combate-e-dano.md (Regras 5, 6, F8) | Contato, hit do telegraph e supressão por distância ao quadrado | `DistSq`, `InCircle`, `InCone`, `InCapsule`, `DistSqToSegment` |
| combate-e-dano.md (F10) | Impactos em área "que alcançam o herói" | **Provisório:** interpretação da Decisão 5; o predicado é pendência do GDD #6 |
| combate-e-dano.md (Regra 4) | Alvo do auto-ataque: o mais próximo, empate no menor id | `SimQuery.NearestInCircle` |
| horda-waves-e-inimigos.md (TR-horda-004) | Posição de nascimento como função pura: direções `SimVec2`, espelho por eixo, `dist²`, sem `sin`/`cos` | `SimVec2`, `Arena.OutsideX` e `Arena.OutsideY`; a função é do #7 |
| horda-waves-e-inimigos.md (TR-horda-005) | Arena AABB e tipo vetorial compartilhados com o `clampArena` do #6 | `Arena` única |
| horda-waves-e-inimigos.md (TR-horda-012) | Separação e bloqueio de corpo (grade uniforme) adiados ao spike | Decisão 3 e Alternativa 1 |
| horda-waves-e-inimigos.md (TR-horda-021) | Classe de vetor como inteiro, nunca igualdade de `float` | Decisão 4 |
| simulacao-deterministica.md (#2) | `float32` com `SimMath`, sem transcendentais | Decisão 4 |

## Performance Implications
- **CPU**: testes por distância ao quadrado (duas multiplicações e uma soma); uma consulta de varredura ≈ 300 testes; sem alocação por `Tick`. O custo total é medido no spike (OQ-14 do #6).
- **Memory**: o buffer de resultado do chamador, `EntityCapacity × 4 B` (~4,5 KB com 1124 linhas), alocado uma vez; o resto é pilha.
- **Load Time**: a `Arena` e os buffers no `Preparar`, desprezível.
- **Network**: não se aplica.

## Migration Plan
Nenhum código existe. Ordem: (1) aprovar este ADR; (2) criar `SimVec2`, `Arena`, `SimGeometry` e `SimQuery` em `Forja.Simulation` com os testes de fronteira; (3) o #6 e o #7 usam só essa geometria; (4) o #1 passa a exigir `cos2Meia` no golpe de forma `Cone`; (5) os GDDs #6, #7 e #1 definem a abertura do cone.

## Validation Criteria
- Fronteiras: ponto exatamente no raio está dentro (círculo), no alcance e no limite angular (cone), no extremo do segmento (cápsula); alvo no ápice do cone está dentro; segmento com `LenSq < DirEpsSq` vira círculo. Os testes de fronteira usam valores exatamente representáveis (por exemplo `dir = (1,0)` e `cos2Meia = 0.5f` para o limite de 45° com `p = (1,1)`, e `b` de componentes inteiras no extremo do segmento), porque `a + ab × 1f` pode diferir de `b` em 1 ulp e as diagonais de `Axis8` têm módulo² `1 ± 1 ulp`.
- `Dir` de vetor nulo dá (1, 0); `KbDir` dá `Axis8(id & 7)`; as 8 direções de `Axis8` têm módulo² 1 dentro de 1e-6.
- `Arena.Clamp` desliza ao longo da parede e o construtor lança com dimensão ≤ `2 × raio` ou não finita.
- `CollectInCircle` devolve ids crescentes, ignora mortos e facção errada, e `NearestInCircle` resolve o empate no menor id.
- AC-P2 do #6: zero alocação em 600 ticks com 300 vivos e as consultas do tick.
- O #1 recusa um golpe `Cone` sem `cos2Meia` e valida `passo_min_tick ≥ 0,001 m` e `dist_parada_m ≥ 0,001 m` (abaixo disso `Dir` trataria um vetor legítimo como nulo e o movimento iria para +x).
- Reavaliar com o jogo jogável: a varredura linear contra a grade, a meia-abertura máxima de 90° e `DirEpsSq`.

## GDD Sync (as notas de sincronia dos ADRs 0001 e 0005 foram aplicadas; as dos GDDs #6, #7 e #1 seguem pendentes, nenhum GDD foi editado)
- **ADR-0001 (aplicada em 2026-11-06):** (a) o `Spawn` acrescenta o id ao fim de `Alive` na hora, para a consulta ver quem nasceu antes no mesmo tick; (b) os corpos de `SimMath.Clamp`, `Min` e `Max` (Decisão 2).
- **ADR-0005 (aplicada em 2026-11-06):** `SourceId = −1` exige `DirExplicita`, e o `Aplicar` recusa o pedido sem ela (Decisão 5).
- **GDD #6:** a abertura do cone (`NOT ASSESSED`); o predicado da F10 ("alcança o herói") e a margem; a regra "vence" do knockback sem raiz (`v0_novo² > LenSq(v_atual)`); `passo_min_tick` mínimo.
- **GDD #7:** a F4 limita o nascimento a `[0, L]` com raio 0, enquanto o #6 limita a `[r, L − r]`; o fator 2,02 da F5 é validação do #1 no build; a abertura do cone no dado do golpe.
- **GDD #1:** recusar `Cone` sem `cos2Meia`; validar `passo_min_tick ≥ 0,001 m` e `dist_parada_m ≥ 0,001 m`; calcular `cos2Meia` em `decimal` no build.

## Emenda de 2026-11-10 (rodada 5)
Autorizada pelo usuário (pendências do ADR-0006 vindas do `architecture-review-2026-11-10-3.md`). Nenhum contrato de tipo ou função mudou; mudou a linha `Depends On` e três trechos de texto.
1. **`Depends On` (3ª passada nº 3).** Passa a listar ADR-0001, ADR-0002, ADR-0004 e ADR-0005, cada um com o que este ADR usa; "só pode ser aceito depois deles" vale para os quatro. Ordering Note atualizada (ordem 0001, 0002, 0004, 0005, depois este); Related alinhado. O ADR-0005 não cita este ADR na linha `Depends On` dele (conferido).
2. **Decisão 3, "Quem pode usar" (3ª passada nº 9).** "As mortes ocorrem depois de todos os `Step`" era falso: o #3 e o #16 rodam depois do passo 7b do #6 (ADR-0001 Emenda 19(f); ADR-0005, Decisão 5). Reescrito; o `SimQuery` filtra por `IsAlive`, então não há efeito prático.
3. **`Arena.IsValid`.** O texto dizia "o compositor confere" (Decisão 1) e "o `Preparar` confere" (Key Interfaces). **Escolha: o compositor**, ao construir a `Arena` e antes de entregá-la ao #7 e ao #6, portanto antes do `Create` (ADR-0001 Emenda 19(a): `Created` → `Preparar` → `BeginRun`; ordem do `Preparar` #3, #7, #6). Razões: a `Arena` sai do snapshot concreto, que só o compositor enxerga, e o `Preparar(SimWorld)` não a recebe; falhar antes do `Create` não deixa simulação para `Discard`. Key Interfaces alinhado.
4. **GDD Sync:** o título dizia "pendente; nenhum arquivo foi editado" e contradizia as linhas abaixo; ajustado.

## Related
- Depende de `docs/architecture/adr-0001-simulacao-deterministica-float32-tick-30hz.md`, `docs/architecture/adr-0002-dados-e-balanceamento-snapshot-imutavel-gerado-no-build.md` (`cos2Meia` calculado no build; `Arena` do snapshot), `docs/architecture/adr-0004-colunas-do-simworld-combate-e-horda.md` e `docs/architecture/adr-0005-pipeline-de-dano-e-eventos-de-combate.md` (`HitRequest`, `DirExplicita`).
- GDDs: `design/gdd/combate-e-dano.md`, `design/gdd/horda-waves-e-inimigos.md`, `design/gdd/simulacao-deterministica.md`.
- `docs/architecture/architecture-review-2026-11-05.md` (Required ADRs, item 4).

## Decisões provisórias (a reavaliar com o jogo jogável)
`SimVec2` sem `Length`; varredura linear sem grade; cone limitado a meia-abertura de 90° com `cos²` do build; `DirEpsSq = 1e-6f` único; `Axis8` por `switch`; `Arena` com raio máximo e construtor que lança; `NearestInCircle` com desempate no menor id; consultas escrevendo em buffer do chamador.
