# ADR-0004: Colunas do SimWorld para combate e horda (#6 e #7): quatro colunas compartilhadas preenchidas pelo `Spawn`, o resto do #6 em tabelas próprias indexadas pelo id e uma vista só de leitura

## Status
Proposed

## Date
2026-11-06

## Last Verified
2026-11-06 (contra o ADR-0001 com as Emendas 1 a 16, o ADR-0002, `docs/registry/architecture.yaml` e os GDDs #6 e #7 em disco; Unity 6.3 LTS, pin 6000.3.x)

## Decision Makers
Rodrigo Reis (escopo e alternativa A confirmados em 2026-11-06; o resto é decisão técnica por recomendação, **provisória, a reavaliar com o jogo jogável**), Claude Code (autoria), `unity-specialist` (validação, 5.5) e `technical-director` (gate TD-ADR, 5.6). Os resultados das duas revisões entram na seção Risks antes de gravar.

## Summary
O ADR-0001 permite que o #6 e o #7 acrescentem colunas ao `SimWorld`, mas só por um ADR de colunas, que ainda não existe. Decidido: o `SimWorld` ganha só quatro colunas que vários sistemas leem (`classe`, `arquetipoId`, `tickNascimento`, `hpMax`), preenchidas pelo `Spawn` e imutáveis depois; todo o resto do estado do #6 fica em tabelas do próprio #6, indexadas pelo id e dimensionadas por `EntityCapacity`, hasheadas pelo `Hash` do #6 e expostas aos outros sistemas por uma vista só de leitura.

## Engine Compatibility

| Field | Value |
|-------|-------|
| **Engine** | Unity 6.3 LTS (6000.3.x; editor instalado 6000.3.27f1) |
| **Domain** | Core |
| **Layer** | Core (igual ao ADR-0001; não existe `docs/architecture/architecture.md` nem mapa de camadas, então a camada foi confirmada pelo autor em 2026-11-06) |
| **Knowledge Risk** | **LOW** para a superfície de API (nenhuma API da Unity; nada em `deprecated-apis.md` ou `breaking-changes.md`); **MEDIUM** para o comportamento em runtime (`Span<T>` sob IL2CPP com stripping) até a Verification Required 5 passar num build Android IL2CPP; a linha do engine é HIGH em `VERSION.md:34`; não existe `modules/core.md`. A referência de API é a do 6.3 (o 6000.5.5f1 também está instalado e não é o pin) |
| **References Consulted** | `docs/engine-reference/unity/VERSION.md`, `breaking-changes.md`, `deprecated-apis.md`, `current-best-practices.md`; ADR-0001 (Decision, Key Interfaces, Emendas 6, 12, 14, 15, 16), ADR-0002 (`IPhaseSnapshot`, capacidades), `docs/registry/architecture.yaml`; GDDs #6 e #7. **Não existe `docs/engine-reference/unity/modules/core.md`**: nada do domínio Core foi checado contra um módulo de referência (`NOT SOURCEABLE`) |
| **Post-Cutoff APIs Used** | Nenhuma. Só `float`, `int`, `byte`, arrays e `Span<T>`/`ReadOnlySpan<T>`, como no ADR-0001. A disponibilidade de `Span<T>` no perfil de API do projeto e o comportamento sob IL2CPP são `NOT SOURCEABLE` e já são a Verification Required 4 e 6 do ADR-0001 |
| **Verification Required** | (1) Hash igual com tabelas novas e com tabelas reusadas de uma fase anterior (a limpeza no `Preparar`, Decisão 6), inclusive reusando o #6 numa fase com `EntityCapacity` maior e noutra com menor, no Editor (com e sem domain reload: o projeto tem Enter Play Mode Options ligado e o 6.6 passa a pular o domain reload por padrão, `VERSION.md:47`) e em IL2CPP. (2) Zero alocação gerenciada por `Tick` com 300+ vivos (`ProfilerRecorder` "GC.Alloc"), já o AC-P2 do #6. (3) Custo do `Hash` do #6 com 300 vivos, medido no aparelho (nunca dentro do `Tick`). (4) Tempo do `Tick` do #6 contra `orcamento_combate_ms` (OQ-14 do #6) com a disposição em colunas separadas (SoA); se estourar, reavaliar a Alternativa F. (5) `NOT SOURCEABLE`: propriedades que devolvem `ReadOnlySpan<T>` numa interface entre asmdefs, sob IL2CPP com stripping de Release, num build Android IL2CPP (o suporte Android está instalado; iOS não). (6) `NOT SOURCEABLE`: `BannedApiAnalyzers` rodar no pipeline de compilação da Unity 6.3; se não rodar, a guarda de `HpAndPosForWrite` fica só por revisão de código (já é o caso de `PhaseSheet` no ADR-0001). (7) `apiCompatibilityLevel` do projeto expõe `Span<T>` (`ProjectSettings.asset`, valor 6, `NOT SOURCEABLE` quanto ao significado). |

## ADR Dependencies

| Field | Value |
|-------|-------|
| **Depends On** | ADR-0001 (`Proposed`; precisa estar `Accepted` e receber a Emenda 17, abaixo) e ADR-0002 (`Proposed`; `IPhaseSnapshot.EntityCapacity`). Este ADR só pode ser aceito depois deles. |
| **Enables** | ADR-0005 (pipeline de dano: `Combate.Curar` acumula na coluna `curaPendente` definida aqui; `Aplicar` não a toca), ADR-0006 (geometria: as colunas de posição e de área são pares de `float`, sem `SimVec2`), GDD #12 (vista de leitura do telegraph) |
| **Blocks** | Épicos de #6 Combate e dano e #7 Horda; as stories que escrevem ou leem as colunas listadas na Decisão 2; I2, I12, D1, D3 e R22 do #6 e I12 do #7 (hoje "BLOQ: ADR das colunas") |
| **Ordering Note** | ADR-0005 e ADR-0006 podem ser escritos em paralelo, mas nenhum fixa nome de coluna: se o ADR-0006 escolher um tipo `SimVec2`, ele entra como vista sobre os pares `X`/`Y` daqui, sem mudar o armazenamento. `modDano` e `modCadencia` (TR-combate-001) são **estado escrito pelo #8**: moram no #8 e chegam ao #6 por uma vista do #8 definida no ADR-0005; não são colunas deste ADR, então o ADR-0005 não precisa emendar o ADR-0004 por causa delas. **Nota de sincronia (2026-11-06, ADR-0005):** o ADR-0005 tocou este ADR em dois pontos, já aplicados aqui: o `curaAcc` saiu do scratch (a cura só acumula em `curaPendente`) e entrou o sinal do `Rugido`. As três formas de canal direto da Emenda 18 do ADR-0001 cobrem o `ICombatReadView` (vista só de leitura) e o `curaPendente` (acumulador hasheado do dono). |

## Context

### Problem Statement
O #6 precisa guardar, por entidade, o estado do golpe com aviso (fase, contagem, área travada), o empurrão, as recargas e a cura pendente; o #7 e o #3 precisam ler `classe`, `arquetipoId`, `tickNascimento` e `hpMax`; o #12 precisa desenhar o telegraph lendo colunas, não eventos (um evento descartado nunca pode esconder o aviso). O ADR-0001 deixou o `SimWorld` com a forma mínima (id, posição atual e anterior, facção, HP, vivo, `Essencial`, `xpValue`) e diz que "colunas extras só por ADR de #6/#7". Sem este ADR não há nome, tipo, dono nem regra de hash para essas colunas, e a revisão de 2026-11-05 aponta isso como bloqueio de `/create-epics` do #6 e do #7.

### Constraints
- ADR-0001: uma só tabela de entidades; ids monotônicos e nunca reutilizados; o id é o índice da linha; `float` em C# puro; sem `UnityEngine`; sem `static` mutável; nenhuma alocação por `Tick`; hash por byte, campo a campo, fora do `Tick`; toda iteração por id crescente.
- O #6 é o **único escritor de posição e de HP** (GDD #6, Regra 1); o #7 só faz nascer; o #3 só pede cura.
- Dev solo, MVP de 13 a 20 meses: a solução precisa ser simples de escrever e de depurar.
- Capacidades vêm do snapshot (ADR-0002): `EntityCapacity` cobre o total de spawns da fase com margem (exemplo do GDD #7 F7: 514 spawns → capacidade ≥ 644; ADR-0002: 1124).

### Requirements
- Nome, tipo, dono (único escritor), leitores e pertencimento ao hash de cada coluna que o #6 e o #7 nomeiam.
- `classe`, `arquetipoId` e `tickNascimento` corretos em cada `Spawn` (TR-combate-023, TR-horda-007; I12 do #7).
- O #12 e o #7 leem o estado de ataque sem poder escrever nele.
- Estado de scratch (fila, dano acumulado) claramente fora do hash e sem poder vazar de um tick para o outro.
- Hash igual com buffers novos ou reusados (ADR-0001, Verification Required 9).

## Decision

### 1. Três tipos de coluna e onde cada um mora
1. **Colunas-base** (já existem no ADR-0001): posição atual e do tick anterior, facção, HP, vivo, `Essencial`, `xpValue`. Moram no `SimWorld` (Core), no hash do Core.
2. **Colunas compartilhadas novas** (este ADR): `classe`, `arquetipoId`, `tickNascimento`, `hpMax`. Moram no `SimWorld` (Core), são escritas **só pelo `Spawn`**, nunca mudam depois e entram no hash do Core.
3. **Colunas privadas do #6** (este ADR): estado de combate por entidade. Moram em tabelas do próprio #6 em `Forja.Gameplay.Sim`, indexadas pelo id, com comprimento ≥ `EntityCapacity`; só o #6 escreve; entram no `Hash` do #6; os outros sistemas leem por uma vista só de leitura (Decisão 5).
4. **Bloco do herói** (este ADR): escalares do #6 que só existem para o herói (esquiva, dash, cadência, hit-stop). Moram numa struct do #6, no `Hash` do #6.
5. **Scratch do #6**: fila de golpes (ADR-0005), dano e cura acumulados por alvo, `vivoNoInicio`, intenção de velocidade do herói, contadores. Moram no #6, **fora do hash**, e valem só dentro do `Tick` (Decisão 4).

O #7 **não acrescenta colunas** (confirma a OQ-13 do #7): ele escreve as quatro compartilhadas por meio do `Spawn` e mantém seus cursores no próprio `Hash`.

### 2. Catálogo

**Colunas compartilhadas do `SimWorld`** (Core; comprimento `EntityCapacity`; escritas pelo `Spawn`):

| Coluna | Tipo | Valor | Hash do Core |
|---|---|---|---|
| `classe` | `EntityClass : byte` (`None = 0` inválido, `Heroi = 1`, `Horda = 2`, `Elite = 3`, `Chefe = 4`; valores explícitos, só cresce no final) | passada ao `Spawn`; `None` é bug e o `Spawn` lança nos dois modos | sim |
| `arquetipoId` | `int` ≥ 0 | o espaço de índices depende de `classe`: com `Heroi` é o índice na tabela de heróis do snapshot; com `Horda`, `Elite` e `Chefe` é o índice na tabela de arquétipos de inimigo; as duas em ordem de IDs do snapshot (ADR-0002). A chave é o par (`classe`, `arquetipoId`); o mapeamento índice → definição é do #1 *(provisória)* | sim |
| `tickNascimento` | `int` | o `CombatTick` do `Spawn` (0 no `Preparar`), carimbado pelo `SimWorld`, não passado pelo chamador | sim |
| `hpMax` | `float` > 0 | o `hp` passado ao `Spawn` (toda entidade nasce com a vida cheia) *(provisória)* | sim |

**Colunas privadas do #6** (uma por entidade; comprimento ≥ `EntityCapacity`; escritas só pelo #6; todas no `Hash` do #6; **o valor zero é o estado inicial válido**). Os significados e as transições são do GDD #6; este ADR fixa só nome, tipo e dono:

| Coluna | Tipo | Leitura pela vista |
|---|---|---|
| `estadoCombate` | `byte` (enum do #6, valores explícitos, 0 = estado inicial) | sim (#7, #12) |
| `timerTicks` | `int` (ticks restantes do estado; `ticks_ate_dano` do #12 vem daqui) | sim |
| `forma` | `byte` (`Nenhuma = 0`, `Circulo`, `Cone`, `Linha`) | sim |
| `raio` | `float` | sim |
| `origemX`, `origemY`, `dirX`, `dirY` | `float` | sim |
| `destinoX`, `destinoY` | `float` (só na `Linha`) | sim |
| `aberto`, `punidoPesado` | `byte` (0 ou 1) | `aberto` sim |
| `iframes` | `int` | sim (apresentação da esquiva) |
| `cicloIdx` | `int` (índice do golpe em curso na lista de golpes do arquétipo; do Aviso ao fim da Recuperação identifica o golpe travado, e (`arquetipoId`, `cicloIdx`) acha no snapshot o dado por golpe, como a abertura do cone) *(semântica a confirmar no GDD #6)* | sim |
| `contactCd`, `poise`, `kbRefrat`, `prontoDesde`, `kbRestante` | `int` | não |
| `kbVelX`, `kbVelY` | `float` | não |
| `curaPendente` | `float` ≥ 0 (escrita só pelo código do #6, quando `Combate.Curar` do ADR-0005 acumula; `Aplicar` não a toca; o #3 chama `Curar` e nunca toca a coluna) | não |

**Bloco do herói** (um por fase; `struct HeroCombat` no #6; no `Hash` do #6): recarga da esquiva, `esquivaBuf`, dash restante e direção, `ultimaDirecao` (inicial (0, 1), gravada pelo `Preparar`), cadência do auto-ataque, `ultimoContatoTick`, `proximoHitStopTick` e o contador do orçamento de hit-stop. A lista exata de campos é do GDD #6; acrescentar um campo ao bloco ou uma coluna privada ao catálogo **não exige novo ADR** quando ele obedece às regras 1 a 5 da Decisão 3 (mesmo critério que o ADR-0001 deu à `PhaseSheet`). Já uma coluna **compartilhada** nova, ou uma coluna escrita por outro sistema, exige emenda a este ADR. **Exceção declarada:** estado escrito por outro sistema para o #6 ler (`modDano` e `modCadencia`, do #8) não é coluna deste ADR: mora no sistema que o escreve e chega ao #6 por uma vista desse sistema (ADR-0005). O `iframes` está por entidade (e não no bloco do herói) porque o GDD #6 o trata como coluna e a vista o expõe; os demais campos do herói são um só *(provisória)*.

**Scratch (fora do hash):** `acc` (dano acumulado por alvo), o sinal do `Rugido` (ADR-0005), `vivoNoInicio`, `intentVel` do herói (derivada do comando do próprio tick; comandos valem só no tick em que chegam, então não persiste: sem `Move` no tick a intenção é zero, e a ponte reenvia `Move` em todo tick com o stick inclinado, Emenda 4 do ADR-0001; o GDD #6 a lista como coluna hasheada, a sincronizar), a fila de golpes e os contadores de diagnóstico (`CurasDescartadas`, `GolpesLimitados` e afins).

### 3. Regras de dono, acesso e escrita
1. **Único escritor.** Cada coluna privada e o bloco do herói têm o #6 como único escritor. "Único escritor" significa o **código do #6**: `Combate.Aplicar` e `Combate.Curar` são as únicas portas de entrada dos outros sistemas, e como essa chamada direta se concilia com "a comunicação interna do tick passa pelo `SimWorld`" (ADR-0001, L84) é decisão do ADR-0005. As colunas compartilhadas não têm escritor depois do `Spawn`. Posição e HP continuam sendo do #6 (Regra 1 do #6).
2. **Acesso às colunas-base e compartilhadas** (Key Interfaces): leitura por `ReadOnlySpan<T>` de comprimento `IdCount`; escrita de HP e posição por **uma chamada guardada** por `Tick`, `HpAndPosForWrite(out hp, out posX, out posY)`, aceita só dentro do `Tick` e que lança nos demais estados (o mesmo molde de `PhaseForWrite`). A guarda não impede um sistema de chamá-la: o que impede é a regra de revisão e a análise estática (`BannedApiAnalyzers`, AC-D4 do #6), como já é a regra de `PhaseSheet` e `CombatHold`.
3. **Comprimento e estabilidade.** As colunas do `SimWorld` têm comprimento `IPhaseSnapshot.EntityCapacity` (criadas pelo `Create`). As tabelas do #6 têm comprimento **≥ `EntityCapacity` da fase em curso** e são dimensionadas no `Preparar` (Decisão 6), porque `EntityCapacity` muda de fase para fase e um #6 pode ser reusado. Spans e `Hash` fatiam sempre por `IdCount`, nunca por `Length`. Dentro de uma fase **nenhum array é realocado**, e os spans obtidos no começo do `Step` continuam válidos no tick inteiro. Um id nascido mais tarde no mesmo tick fica fora do span já obtido; isso é coerente com "ids novos só agem a partir do sistema seguinte" (Emenda 6).
4. **Scratch.** Todo scratch **deve** estar vazio ao fim de cada `Tick` (o #6 zera `acc` e o sinal do `Rugido` no passo 8; a cura não tem scratch: o `Curar` acumula direto em `curaPendente`, ADR-0005) e **deve** ser reescrito antes de ser lido no tick seguinte. É isso que permite deixá-lo fora do hash: um scratch que sobrevive ao tick é estado oculto e é bug. Um `Tick` que lança leva a `Broken` (Emenda 2), então um scratch sujo nunca alcança o tick seguinte. **Quem garante o invariante é o #6, em toda saída do `Step`**, inclusive o retorno antecipado sem `CombatActive` (GDD #6, passo 2.1), onde ele esvazia a fila e o `acc` antes de retornar. O #7 e o #8 só enfileiram com `CombatActive` (GDD #7, Regra 1), então a fila já chega vazia nesse caso; a regra vale mesmo assim, e o contrato de `Aplicar` com `!CombatActive` é do ADR-0005.
5. **Linha de entidade morta.** A linha de uma entidade morta **não é reciclada** e fica legível até o fim da fase (os ids nunca se repetem). É por isso que o `DeathRecord` continua `{Id, Cause}` e o #3, o #12 e o #24 leem posição, `arquetipoId` e `tickNascimento` da morte pelo id (GDD #6, Regra 14; isto substitui a ideia de estender o `DeathRecord`, citada na revisão de 2026-11-05). O #6 zera as colunas de telegraph de um atacante morto no passo 8 (GDD #6, Edge Cases).

### 4. Hash
- **Core** (Emenda 17 b): na ordem do item 12 da Emenda do ADR-0001, os campos por id passam a ser vivo, facção, `Essencial`, HP, x, y, **`xpValue`, `classe`, `arquetipoId`, `tickNascimento`, `hpMax`** (o `xpValue` é imutável desde o `Spawn`, como as quatro novas, e o item 12 do ADR-0001 não o hasheava). O hash do Core percorre **todo id < `IdCount`, vivo ou morto**. Quem é dono da coluna a hasheia.
- **#6**: o `Hash` do #6 percorre primeiro o bloco do herói, depois `World.Alive` em ordem crescente de id, e para cada vivo todas as colunas privadas na ordem da tabela da Decisão 2, campo a campo, com `-0` normalizado para `+0` (o `StateHasher` do Core). Linhas de mortos não entram. Scratch nunca entra.
- Mudar só uma coluna privada ou o scratch de uma entidade morta nunca muda o hash do Core. Mudar qualquer coluna privada de uma entidade viva muda o `StateHash` (AC-D3 do #6).
- O hash nunca é calculado dentro do `Tick` (ADR-0001).

### 5. Vista de leitura
O #6 expõe `ICombatReadView` (em `Forja.Gameplay.Sim`) com `ReadOnlySpan<T>` das colunas marcadas "sim" no catálogo, o `ticks_ate_dano` derivado (`timerTicks` quando `estadoCombate` é Aviso) e uma cópia só de leitura do bloco do herói que o #12 precisa (dash restante e direção, cadência; `iframes` é coluna e se lê em `Iframes[Phase.HeroId]`). Regras:
- O compositor entrega a vista **por referência direta** ao #7 e ao #12; sem reflexão, sem `static`, sem localizador.
- O #7 roda **antes** do #6 e portanto lê o estado de ataque gravado **no fim do tick anterior** (a defasagem de 1 tick já é aceita na Regra 11 do GDD #7).
- A vista só tem propriedades de leitura; nenhuma delas devolve `Span<T>` gravável.
- Os spans incluem as linhas de entidades mortas: todo consumidor **filtra por `IsAlive`** antes de usar `aberto`, `iframes` ou outra coluna privada (o #6 só zera as colunas de telegraph de quem morre), e o #6 nunca lê coluna privada de um morto para decidir efeito.
- O #6 não depende do #7: ele lê `classe`, `arquetipoId` e `tickNascimento` do `SimWorld`, nunca do #7 (sem ciclo).

### 6. Ciclo de vida e capacidade
- Os arrays do #6 são alocados na construção do sistema (tela de carregamento). O #6 implementa `IPreparaFase` (`IdsDePreparacao = 0`) e, no `Preparar`, **realoca cada tabela se `Length < world.EntityCapacity`** (ainda é a tela de carregamento) e **zera todas as suas tabelas** (`Array.Clear(a, 0, a.Length)` ou `span.Clear()`, nunca a sobrecarga de um argumento, que não é garantida no perfil de API do projeto) e grava só as constantes não nulas (`ultimaDirecao`). Assim um #6 reusado entre fases dá o mesmo hash que um novo. O `Preparar` do #6 limpa só as próprias tabelas e nunca lê linhas de `Spawn`, então a ordem entre ele e o #3 não importa.
- As colunas compartilhadas não precisam de limpeza: o `Spawn` inicia a linha inteira, e linhas com id ≥ `IdCount` nunca são lidas nem hasheadas.
- **Sem id reservado para o chefe** *(resolve a OQ-3 do #7; provisória)*: a conferência de capacidade do compositor (ADR-0001, item 6, com a margem de `CapacityMarginPct`) e o `total_spawns_7` máximo (F7 do #7) já garantem que o chefe cabe; se mesmo assim um `Spawn` `essential` for rejeitado, vale o caminho já decidido (`InternalFailure`, `EssentialSpawnRejected`). Reservar um id só complicaria o contador.
- Capacidade da fila de golpes e do buffer de eventos: ADR-0005 (a fórmula de `cap_fila` é do GDD #6).

### 7. Emenda 17 ao ADR-0001 (pendente; só com aprovação do autor)
(a) `Spawn(faction, essential, xpValue, hp, x, y)` vira `Spawn(faction, essential, xpValue, hp, x, y, EntityClass entityClass, int archetypeId)`; o `SimWorld` carimba `tickNascimento` e `hpMax`; (b) o item 12 (hash) acrescenta `xpValue` e as quatro colunas, na ordem acima, e fixa que o percurso é por todo id < `IdCount`; (c) as Key Interfaces ganham as propriedades de leitura e `HpAndPosForWrite`; (d) o enum `EntityClass`; (e) o registro: `entity_table` ganha este ADR em `referenced_by` e tem o `write_access` revisto (HP e posição passam a ser só do #6; hoje "isimsystem-within-tick"); entram uma entrada em `state_ownership` para as colunas de combate (dono: #6) e um contrato `combat_read_view` em `interfaces` (Passo 6 da skill, só com aprovação). Nenhum hash gravado existe ainda, então a mudança de ordem do hash não invalida nada.

### Architecture Diagram
```
 Forja.Simulation (Core)                        Forja.Gameplay.Sim (sem engine)
 ┌──────────────────────────────────┐           ┌──────────────────────────────────────┐
 │ SimWorld (EntityCapacity linhas) │           │ #6 Combate (ISimSystem + IPreparaFase)│
 │  base:  pos, prev, facção, HP,   │◀─escreve──│  HpAndPosForWrite (só dentro do Tick) │
 │         vivo, Essencial, xpValue │   HP/pos  │  privadas: estadoCombate, timerTicks, │
 │  nova:  classe, arquetipoId,     │           │   forma, raio, origem, dir, destino,  │
 │         tickNascimento, hpMax    │           │   iframes, kb*, poise, curaPendente…  │
 │         (só o Spawn escreve)     │           │  bloco do herói · scratch (sem hash)  │
 └───────────▲──────────────────────┘           └───────┬──────────────────────────────┘
             │ Spawn(..., classe, arquetipoId)          │ ICombatReadView (só leitura)
         #7 Horda (cursores no próprio Hash) ◀──────────┤ (estado de ataque do tick anterior)
         #3 (lê hpMax, tickNascimento) · #12 (telegraph) ◀┘
```

### Key Interfaces
```csharp
namespace Forja.Simulation
{
    public enum EntityClass : byte { None = 0, Heroi = 1, Horda = 2, Elite = 3, Chefe = 4 }   // valores explícitos (vão para o hash e o log); só cresce no final

    public sealed class SimWorld   // acrescenta ao SimWorld do ADR-0001 (a Emenda 17 edita a classe existente, sem partial)
    {
        // Spawn passa a receber classe e arquetipoId; lança nos dois modos em None, archetypeId < 0, ou hp não finito ou ≤ 0. tickNascimento e hpMax são carimbados pelo SimWorld.
        public int Spawn(int faction, bool essential, int xpValue, float hp, float x, float y, EntityClass entityClass, int archetypeId);

        public int EntityCapacity { get; }
        // Leitura: comprimento IdCount, arrays fixos (nunca realocados), válidos no tick inteiro.
        public ReadOnlySpan<EntityClass> Classes { get; }
        public ReadOnlySpan<int> ArchetypeIds { get; }
        public ReadOnlySpan<int> BirthCombatTicks { get; }
        public ReadOnlySpan<float> HpMaxes { get; }
        public ReadOnlySpan<float> Hp { get; }
        public ReadOnlySpan<float> PosX { get; }  public ReadOnlySpan<float> PosY { get; }
        public ReadOnlySpan<float> PrevPosX { get; }  public ReadOnlySpan<float> PrevPosY { get; }
        public ReadOnlySpan<int> Factions { get; }
        // Escrita: uma chamada por Tick; só dentro do Tick; lança nos demais estados; só o #6 chama (revisão + analisador).
        // Os três spans têm comprimento IdCount no instante da chamada; um id nascido depois, no mesmo tick, fica fora deles.
        public void HpAndPosForWrite(out Span<float> hp, out Span<float> posX, out Span<float> posY);
    }
}

namespace Forja.Gameplay.Sim   // sem engine
{
    // Enums do #6, explícitos, 0 = estado inicial; só crescem no final. Os valores e as transições são do GDD #6.
    public enum CombatState : byte { /* Perseguindo = 0, Aviso, Impacto, Recuperacao, Golpe, Recarga, ... (GDD #6) */ }
    public enum TelegraphShape : byte { Nenhuma = 0, Circulo = 1, Cone = 2, Linha = 3 }

    public interface ICombatReadView   // implementada pelo #6; entregue ao #7 e ao #12 pelo compositor, por referência direta
    {
        // Todo span abaixo tem comprimento IdCount no instante da chamada. Quem lê pega cada span UMA vez por tick (ou por frame)
        // numa variável local; não chama a propriedade dentro do laço por entidade, não guarda span em campo,
        // lambda, coroutine ou async (um span não pode escapar para o heap).
        ReadOnlySpan<CombatState> EstadoCombate { get; }
        ReadOnlySpan<int> TimerTicks { get; }
        ReadOnlySpan<int> CicloIdx { get; }
        ReadOnlySpan<TelegraphShape> Forma { get; }
        ReadOnlySpan<float> Raio { get; }
        ReadOnlySpan<float> OrigemX { get; }  ReadOnlySpan<float> OrigemY { get; }
        ReadOnlySpan<float> DirX { get; }     ReadOnlySpan<float> DirY { get; }
        ReadOnlySpan<float> DestinoX { get; } ReadOnlySpan<float> DestinoY { get; }
        ReadOnlySpan<byte> Aberto { get; }
        ReadOnlySpan<int> Iframes { get; }
        int TicksAteDano(int id);          // TimerTicks[id] quando EstadoCombate[id] é Aviso; senão -1
        HeroCombatView Hero { get; }       // readonly struct devolvida por valor (nunca boxed): dash restante e direção, cadência (sem iframes: use Iframes[Phase.HeroId])
    }
    // O #6 implementa IPreparaFase com IdsDePreparacao = 0: zera as tabelas e grava as constantes não nulas.
}
```

### Implementation Guidelines
- As quatro colunas compartilhadas **must** ser escritas só pelo `Spawn` e **must never** ter setter público; `Spawn` com `EntityClass.None`, `archetypeId < 0` ou `hp` não finito ou ≤ 0 **must** lançar nos dois modos.
- As colunas privadas e o bloco do herói **must** ter o #6 como único escritor; nenhum outro sistema **must** receber `Span<T>` gravável delas.
- Todo array de coluna do #6 **must** ter comprimento ≥ `EntityCapacity` da fase, ser alocado na construção ou realocado no `Preparar` quando menor, e **must never** ser realocado, redimensionado nem trocado depois do `Preparar`; spans e `Hash` **must** fatiar por `IdCount`; **must never** haver `List<T>` nem alocação no `Tick`.
- O valor zero de toda coluna privada **must** ser um estado inicial válido (enum com 0 = estado inicial); a única constante não nula (`ultimaDirecao`) **must** ser gravada pelo `Preparar`.
- O #6 **must** implementar `IPreparaFase` e **must** zerar todas as tabelas no `Preparar`; um teste **must** conferir hash igual com tabelas novas e com tabelas reusadas de uma fase com 300 vivos.
- Scratch **must** estar vazio ao fim do `Tick` e **must** ser reescrito antes de ser lido; **must never** haver estado que sobreviva ao tick fora do hash.
- O `Hash` do #6 **must** percorrer o bloco do herói e depois `World.Alive` por id crescente, campo a campo, `-0` normalizado, e **must never** incluir scratch nem linhas de mortos; **must never** hashear memória bruta de struct nem usar `GetHashCode`.
- A vista **must** ser entregue por referência direta pelo compositor e **must** ter só propriedades de leitura; **must never** haver `static`, localizador ou reflexão. O consumidor **must** pegar cada span uma vez por tick (ou frame) numa variável local e **must never** guardá-lo em campo, lambda, coroutine ou `async`. Os limites de índice **must never** ser desligados: a checagem também protege o determinismo.
- O #7 **must** ler o estado de ataque da vista como o do fim do tick anterior e **must never** escrever nele.
- Posição e HP **must** ser gravados só pelo #6, por `HpAndPosForWrite`, uma chamada por `Tick`; `PrevPos` **must never** ser gravável fora do Core.
- Um enum de coluna (`EntityClass`, `estadoCombate`, `forma`) **must** ter valores explícitos, só crescer no final, e todo `switch` sobre ele **must** ter um `default` que lança.
- Acrescentar uma coluna **compartilhada**, ou uma coluna escrita por outro sistema, **must** passar por emenda a este ADR; estado de outro sistema que o #6 lê **must** morar nesse sistema, com vista própria (ADR-0005).
- O #6 **must** esvaziar a fila de golpes e o `acc` em toda saída do `Step`, também no retorno antecipado sem `CombatActive`.
- Todo consumidor da vista **must** filtrar por `IsAlive` antes de usar uma coluna privada, e o #6 **must never** ler coluna privada de uma entidade morta para decidir efeito.

## Alternatives Considered

### Alternative 1 (B): tudo no `SimWorld`, hasheado pelo Core
- **Description**: as ~25 colunas do #6 (telegraph, empurrão, recargas) viram colunas do `SimWorld`, escritas pelo #6 por spans e hasheadas pelo Core.
- **Pros**: um só objeto para ler; um só hash; a vista de leitura desaparece.
- **Cons**: o Core passa a conhecer o vocabulário do #6 (telegraph, knockback, poise); cada campo novo do GDD #6 vira emenda do ADR-0001 e muda o contrato do hash do Core; o Core cresce sem o #2 precisar disso.
- **Rejection Reason**: acopla o Core à evolução de um sistema de regra, que é o que o ADR-0001 quis evitar ao manter o `SimWorld` mínimo.

### Alternative 2 (C): nada novo no `SimWorld`, tudo dentro do #6
- **Description**: `classe`, `arquetipoId`, `tickNascimento` e `hpMax` também ficam no #6.
- **Pros**: nenhuma mudança no Core nem no `Spawn`.
- **Cons**: o `Spawn` deixa de iniciar a linha inteira de uma vez (o #7 teria de escrever no #6 depois, quebrando o escritor único, ou o #6 teria de inferir a classe); o #3 e o #12 passam a depender do #6 por fatos de identidade; o teste do #2 sem o #6 não vê a classe.
- **Rejection Reason**: identidade da entidade é fato do Core, não do combate.

### Alternative 3 (D): tabela compacta de atacantes (slots) só para elite e chefe
- **Description**: fase, timer, forma, raio, origem, direção e destino ficam numa tabela de N slots (3 avisos), com um mapa id → slot.
- **Pros**: economiza cerca de 40 KB com 1124 linhas e combina com o "no máximo 3 avisos".
- **Cons**: indireção e um mapa id → slot a manter no hash; o limite de 1 elite vivo + chefe é regra do MVP (OQ-10, OQ-12 do #7), não invariante; mais código de ciclo de vida.
- **Rejection Reason**: a economia é irrelevante na capacidade atual e o custo em código é real. Reavaliar só se o teto de `EntityCapacity` (pendência P3 do ADR-0002) subir ordens de grandeza.

### Alternative 4 (E): Entities/DOTS para guardar as colunas
- **Description**: componentes do Entities.
- **Rejection Reason**: já rejeitada no ADR-0001 (Alternative 2): determinismo de float sob Burst é `NOT SOURCEABLE` e o pacote muda entre as versões 6.x (`docs/engine-reference/unity/plugins/dots-entities.md`).

### Alternative 5 (F): uma struct por linha (array de structs) no lugar de colunas separadas
- **Description**: `struct CombatRow` com todos os campos do #6, num `CombatRow[]`.
- **Pros**: melhor localidade de cache quando o #6 toca muitos campos de uma entidade; uma só indexação.
- **Cons**: foge do SoA do ADR-0001; a vista de leitura teria de copiar campos ou expor `ref readonly` de struct larga; passes que tocam um campo só (posição) leem linhas inteiras.
- **Rejection Reason**: provisória. SoA é o padrão do ADR-0001 e dá spans simples para o #12; se o spike de performance (AC-P1 do #6) mostrar que o `Tick` do #6 estoura por cache, esta alternativa volta (Verification Required 4).

## Consequences

### Positive
- O Core cresce só em quatro colunas de identidade; o vocabulário de combate fica no #6.
- O #12 lê o telegraph por colunas, como o GDD exige, sem depender de evento (um descarte nunca esconde o aviso).
- Escritor único, hash e scratch têm regra explícita e testável (AC-D3 e D4 do #6, I12 do #7).
- Acrescentar campo do #6 não exige novo ADR; só a coluna compartilhada exige.
- Resolve a OQ-3 e a OQ-13 do #7 e a OQ-1 do #6 (a parte de colunas).

### Negative
- O hash do Core muda de ordem (Emenda 17): nenhum hash gravado existe ainda.
- O `Spawn` ganha dois parâmetros; todo chamador (#3 no `Preparar`, #7) muda de assinatura.
- Duas famílias de coluna (Core e #6) e uma vista: mais um conceito para o dev solo, em troca de um Core pequeno.
- ~100 B por linha, ~110 KB com 1124 linhas, mesmo para a horda que não usa os campos de telegraph.
- O #7 passa a depender de uma interface de leitura do #6 (sem ciclo, e já prevista no GDD #7).

## Risks
- **Capacidade cresce.** `EntityCapacity` sem teto (P3 do ADR-0002) multiplicaria a memória. Mitigação: ~100 B por linha torna 10 mil linhas ≈ 1 MB; o teto da P3 deve ser fixado e a Alternativa 3 revisitada se passar disso.
- **Esquecer a limpeza do `Preparar`** deixa lixo de fase anterior nas tabelas e quebra o replay sem erro. Mitigação: o teste de hash com tabelas novas e reusadas (Verification Required 1) e a regra "zero é estado válido".
- **Scratch que sobrevive ao tick** vira estado oculto fora do hash. Mitigação: a regra 4 da Decisão 3 e um teste que compara dois ticks seguidos após `Reset` manual do scratch.
- **Nomes do GDD #6 diferem do ADR**: `iframes`, `esquivaBuf`, `curaPendente`, `ultimoContatoTick`, `ultimaDirecao` e `intentVel` aparecem como "colunas" no GDD e aqui são coluna, bloco do herói ou scratch. Mitigação: a lista de sincronização do GDD (5.7). `intentVel` como scratch exige confirmar que o GDD #6 não a usa entre ticks.
- **Um só herói.** O bloco do herói supõe um herói controlável; um segundo (aliado, co-op) exige emenda. Ver OQ-11/OQ-12 do #7 e #40.
- **Defasagem de 1 tick** do #7 ao ler o estado do chefe: já aceita no GDD #7 (Regra 11), mas é regra de ordem e não de tipo; mudar a ordem do compositor a muda.
- **Reuso do #6 com capacidade diferente** (achado do TD-ADR): coberto pela realocação no `Preparar` e pelo teste da Verification Required 1.
- **Resultado do `unity-specialist` (5.5, 2026-11-06):** sem bloqueio de API. Ajustes aplicados: Knowledge Risk em dois eixos, comprimento dos spans fixado em cada ponto, `SimWorld` sem `partial`, `Array.Clear` com três argumentos, enums na vista, spans pegos uma vez por tick, teste de hash também sem domain reload. Itens `NOT SOURCEABLE` nas Verification Required 5 a 7.
- **Resultado do `technical-director` (TD-ADR, 5.6, 2026-11-06): CONCERNS, 13 itens, todos de especificação, nenhum exigindo refazer o desenho. Revisão escolhida pelo autor e aplicada:** capacidade ao reusar o #6; scratch no retorno antecipado; `xpValue` e percurso por todo id no hash do Core; exceção do estado do #8; `curaPendente` com "único escritor" = código do #6; espaço de `arquetipoId` por classe; registro mais amplo na Emenda 17 (e); linhas de mortos na vista; `iframes` fora do `HeroCombatView`; invariante de `intentVel`; `cicloIdx` na vista; validação de `hp` no `Spawn`.

## GDD Requirements Addressed

| GDD System | Requirement | How This ADR Addresses It |
|------------|-------------|--------------------------|
| combate-e-dano.md (TR-combate-001) | Colunas hasheadas do #6 e sua lista; "Vira ADR (colunas do SimWorld)" | Decisão 2: catálogo com nome, tipo, dono e hash; `modDano` e `modCadencia` ficam no ADR-0005 |
| combate-e-dano.md (TR-combate-023) | `Spawn` grava `classe`, `arquetipoId` e `tickNascimento` | Decisão 2 e Emenda 17 (a): `Spawn` com classe e arquétipo; `tickNascimento` carimbado pelo `SimWorld` |
| combate-e-dano.md (Regra 1, 11) | O #6 é o único escritor de posição e HP; morte só por `Kill` | Decisão 3.1 e 3.2: `HpAndPosForWrite` guardado e só do #6 |
| combate-e-dano.md (Regra 14, TR-combate-017) | O #12 lê o telegraph por colunas, não por eventos | Decisão 5: `ICombatReadView` |
| combate-e-dano.md (Regra 15, R22) | `curaPendente` no hash, somada em 7b com `CombatActive` | Decisão 2: coluna privada no `Hash` do #6; a API é do ADR-0005 |
| combate-e-dano.md (AC-D3, D4, I2, I12, D1) | Hash por coluna; scratch fora do hash; laço por id crescente | Decisão 4 e Decisão 3.4 |
| horda-waves-e-inimigos.md (TR-horda-007, I12) | `classe`, `arquetipoId` e `tickNascimento` corretos em cada spawn; a escolta lê o estado de ataque do tick anterior | Decisão 2, 5 e Emenda 17 |
| horda-waves-e-inimigos.md (OQ-3, OQ-13) | Reservar um id para o chefe? O #7 não acrescenta colunas | Decisão 6 (sem id reservado) e Decisão 1 |
| simulacao-deterministica.md (FS8, hash) | O hash do Core cobre a tabela de entidades | Decisão 4 e Emenda 17 (b) |
| fluxo-de-fase.md (Regra 6, 7) | O #3 lê `xpValue`, `hpMax` e `tickNascimento` | Decisão 2 (colunas compartilhadas) |

## Performance Implications
- **CPU**: nenhuma alocação por `Tick`; acesso por índice sobre spans; o `Hash` (fora do `Tick`) percorre ~300 vivos × ~90 B ≈ 27 KB por chamada. O custo do `Tick` do #6 é medido no spike (OQ-14 do #6).
- **Memory**: ~13 B/linha (compartilhadas) + ~76 B/linha (privadas) + ~9 B/linha (scratch) ≈ 98 B/linha; com `EntityCapacity` = 1124, ≈ 110 KB. Cálculo do autor, a confirmar no Profiler.
- **Load Time**: alocação e `Array.Clear` de ~110 KB no `Preparar`/construção, na tela de carregamento; desprezível frente ao `Create` (ADR-0001, Verification Required 9).
- **Network**: não se aplica.

## Migration Plan
Nenhum código existe. Ordem: (1) aprovar e aplicar a Emenda 17 no ADR-0001; (2) o #3 e o #7 usam o novo `Spawn`; (3) o #6 cria as tabelas e a vista; (4) o #12 lê a vista; (5) os testes I12, D1, D3, D4 dos GDDs deixam de estar "BLOQ".

## Validation Criteria
- I12 do #7: `classe`, `arquetipoId`, `tickNascimento` corretos em cada spawn (inclusive o herói no `Preparar`, com `tickNascimento` = 0).
- D3 do #6: mudar qualquer coluna privada de uma entidade viva muda o `StateHash`; mudar scratch ou linha de morto não muda.
- Hash igual com tabelas novas e reusadas (Verification Required 1).
- AC-P2 do #6: zero alocação em 600 ticks com 300 vivos.
- Teste: nenhum outro sistema chama `HpAndPosForWrite` (analisador) e nenhum recebe `Span<T>` gravável das colunas privadas.
- Reavaliar (com o jogo jogável): Alternativas 3 e 5; `hpMax` = HP inicial; o bloco do herói único; `iframes` por entidade.

## Related
- Depende de `docs/architecture/adr-0001-simulacao-deterministica-float32-tick-30hz.md` (Emenda 17 pendente) e `docs/architecture/adr-0002-dados-e-balanceamento-snapshot-imutavel-gerado-no-build.md`.
- ADRs vizinhos ainda não escritos: ADR-0005 (pipeline de dano e eventos), ADR-0006 (vetor, geometria e consulta espacial).
- GDDs: `design/gdd/combate-e-dano.md`, `design/gdd/horda-waves-e-inimigos.md`, `design/gdd/simulacao-deterministica.md`, `design/gdd/fluxo-de-fase.md`.
- `docs/architecture/architecture-review-2026-11-05.md` (Required ADRs, item 2).

## Decisões provisórias (a reavaliar com o jogo jogável)
`hpMax` = HP inicial; sem id reservado para o chefe; `iframes` por entidade e o resto do herói em um bloco único; SoA em vez de array de structs; Core faz o hash das quatro colunas compartilhadas; `DeathRecord` sem extensão (linhas de mortos legíveis até o fim da fase); `intentVel` como scratch; vista de leitura com defasagem de 1 tick para o #7; `arquetipoId` com espaço por classe; `cicloIdx` exposto na vista; `xpValue` no hash do Core.
