# ADR-0005: Pipeline de dano e eventos de combate (#6, #7, #8, #3): fila de pedidos tipada dona do #6, cura só por `curaPendente`, eventos emitidos por quem decide e evento agregado da horda

## Status
Proposed

## Date
2026-11-06

## Last Verified
2026-11-10 (rodada 7, ver "Rodada 7" na Emenda abaixo: só texto, sem mudança de contrato; rodada 5, ver "Emenda de 2026-11-10 (rodada 5)"; conferido contra o ADR-0001 com as Emendas 1 a 20 e a Emenda 18 já aplicada, o ADR-0004 (`Proposed`, com a nota de sincronia de 2026-11-06 aplicada), o ADR-0002 §4, `docs/registry/architecture.yaml` e os GDDs #6, #7 e #2 em disco; Unity 6.3 LTS, pin 6000.3.x). Escrito em 2026-11-06, contra o ADR-0001 com as Emendas 1 a 16.

## Decision Makers
Rodrigo Reis (escopo e alternativa A confirmados em 2026-11-06; o resto é decisão técnica por recomendação, **provisória, a reavaliar com o jogo jogável**), Claude Code (autoria), `unity-specialist` (validação, 5.5) e `technical-director` (gate TD-ADR, 5.6). Os resultados das duas revisões entram na seção Risks antes de gravar.

## Summary
O GDD #6 manda #7, #8 e #3 pedirem dano e cura por `Combate.Aplicar`/`Curar` e resolve tudo em dois tempos, mas o ADR-0001 diz que a comunicação interna do tick passa pelo `SimWorld` e que `Kill` emite um `Death` por morte, o que não cabe em 300 mortes por tick. Decidido: uma fila de pedidos tipada, dona do #6 e entregue por referência pelo compositor, com ordem contratual, fora do hash e vazia ao fim de cada `Step`; `Curar` sempre acumula em `curaPendente`; o pedido `Rugido` é um único sinal tipado que o #6 expande; `Kill` e `Spawn` do Core deixam de emitir evento, e quem decide emite (o #6 emite `Death`, `HeroDeath` e o evento agregado da horda); `SimEvent` ganha dois inteiros. Isso exigiu a Emenda 18 ao ADR-0001 (já aplicada lá).

## Engine Compatibility

| Field | Value |
|-------|-------|
| **Engine** | Unity 6.3 LTS (6000.3.x; editor instalado 6000.3.27f1) |
| **Domain** | Core |
| **Layer** | Core (igual ao ADR-0001 e ao ADR-0004; não existe `docs/architecture/architecture.md` nem mapa de camadas, então a camada foi confirmada pelo autor em 2026-11-06) |
| **Knowledge Risk** | MEDIUM (a superfície de API é LOW: nenhuma API da Unity, nada em `deprecated-apis.md` ou `breaking-changes.md`; o comportamento em runtime IL2CPP, isto é, contração de `float`, exceção e stack trace em Release, não é coberto por `docs/engine-reference`); a linha do engine é HIGH em `VERSION.md:34`; não existe `modules/core.md` |
| **References Consulted** | `docs/engine-reference/unity/VERSION.md`, `breaking-changes.md`, `deprecated-apis.md`, `current-best-practices.md`; ADR-0001 (Decision, Key Interfaces, Emendas 2, 4, 6, 9, 10, 15, 18), ADR-0004, ADR-0002 (§4: `IPhaseSnapshot`, `QueueCapacity`, `EventCapacity`); GDDs #6 (Regras 1 a 3, 11, 14, 15, F1, F2, Edge Cases), #7 (Regra 10) e #2 (Regra 6). **Não existe `modules/core.md`**: nada do domínio Core foi checado contra um módulo de referência (`NOT SOURCEABLE`) |
| **Post-Cutoff APIs Used** | Nenhuma. Só `struct`, `readonly struct`, enums, arrays e parâmetros `in` de C# 9. |
| **Verification Required** | (1) AC-P2 do #6: zero alocação gerenciada em 600 ticks com a fila a 80% e 300 mortes no mesmo tick (`ProfilerRecorder` "GC.Alloc"). (2) Hash igual quando o mesmo conjunto de pedidos chega pela mesma ordem de sistemas, e hash diferente quando a ordem de enfileiramento muda (a ordem é contratual). (3) Soma de dano em `float` na ordem fixa da fila: hash repetível em duas execuções do mesmo build IL2CPP Release no aparelho (não igual ao do Editor; ADR-0001, Verification Required 2). A contração implícita de `a*b+c` pelo compilador é `NOT SOURCEABLE` e é risco já aceito no ADR-0001. (4) `NOT SOURCEABLE`: parâmetro `in` de `readonly struct` e `ref SimContext` em método de interface sob IL2CPP com stripping de Release; vira um item do spike Release IL2CPP do ADR-0001. (5) O buffer de eventos cobre o pior tick (rugido com 300 mortes agregadas, mais os individuais) sem `DroppedEvents` (AC-P6 do #2, R14 do #6). (6) `NOT SOURCEABLE`: o stack trace da `SimInvariantException` em Release IL2CPP; por isso a exceção grava tick, `cap_fila` e `FilaPico` antes de lançar. |

## ADR Dependencies

| Field | Value |
|-------|-------|
| **Depends On** | ADR-0001 (`Proposed`; precisa estar `Accepted`; a Emenda 18, abaixo, já está aplicada nele, e o `SimContext.InStep` da rodada 5 também: ADR-0001 Emenda 22), ADR-0004 (`Proposed`; `curaPendente`, `iframes`, `hpMax`, `HpAndPosForWrite`, `DeathsThisTick` por id) e ADR-0002 (`Proposed`; §4: `QueueCapacity` e `EventCapacity` vêm do `PhaseSnapshot`). Este ADR só pode ser aceito depois deles. |
| **Enables** | GDD #8 Skills (contrato de `Aplicar` e de `ICombatModifiers`), ADR do log de eventos do #5 (tabela de `SimEventKind` e payloads), GDD #12 (eventos de combate), ADR-0006 (que depende deste: a direção de knockback e a geometria dos golpes usam os campos da fila, e a regra do `KbDir`/`DirExplicita` do `Aplicar` é daqui) |
| **Blocks** | Épicos de #6 e #7; stories do #8 que enfileiram dano; R3, R14, R15, R22, E1, I2, D1, P2 do #6 e TR-horda-010 e 022 (hoje "BLOQ: ADR") |
| **Ordering Note** | Este ADR não usa nada do ADR-0006 (vetor e geometria): só carrega números e direções já calculados; é o ADR-0006 que depende deste (a dependência inversa fica em Enables). O GDD #8 não existe; este ADR fixa só o que o #6 exige do #8 (ordem, `modDano` em `[1, MODDANO_MAX]`, `modCadencia` na faixa, dano 0 só para empurrão, sem bônus negativo). |

## Context

### Problem Statement
O GDD #6 define `Combate.Aplicar(golpe)` e `Combate.Curar(alvo, valor)` como pontos únicos de dano e cura, usados pelo #6, pelo #8 e (a cura) pelo #3, e o pedido `Rugido` do #7. Todos só enfileiram; o HP muda só no passo 7b, em dois tempos, para que herói e chefe possam morrer no mesmo tick e a soma em `float` tenha ordem contratual. O ADR-0001 não define esse canal e, ao contrário, diz que a comunicação interna do tick passa pelo `SimWorld` e que eventos nunca são canal. Além disso, o `Kill` do ADR-0001 emite um `Death` por morte e o `Spawn` emite `Spawn`, enquanto o GDD #6 exige que 300 mortes de horda no mesmo tick virem **um** evento agregado `{mortes, acertos, danoTotal}`, e o GDD #7 que não haja evento por corpo nascido. Sem este ADR não há tipo de pedido, dono da fila, regra de capacidade, nem tabela de eventos, e a revisão de 2026-11-05 aponta isso como bloqueio de `/create-epics` do #6 e do #7.

### Constraints
- ADR-0001: eventos são só saída; `DroppedEvents` nunca em silêncio; descartar evento nunca altera o estado; reserva `EventosReservados` para tipos críticos; sem alocação por `Tick`; sem `static` mutável; iteração por id crescente; `Kill` é o único caminho de morte e a primeira causa vence.
- ADR-0004: o #6 é o único escritor de HP e posição (`HpAndPosForWrite`); `curaPendente` e `iframes` são colunas privadas do #6; scratch fora do hash e vazio ao fim de todo `Step`.
- GDD #6: Aplicar e Curar só enfileiram; a ordem da fila é contratual (`Rugido`, #8 em ordem de enfileiramento, impactos por id do atacante, contatos, auto-ataque); estouro da fila deixa a simulação `Broken`, porque descartar mudaria o HP.
- Dev solo: poucos tipos, sem reflexão, sem genérico em runtime (IL2CPP).

### Requirements
- Um canal de pedidos de dano e cura com ordem determinística e documentada.
- Resolução em dois tempos: soma por alvo em 7a (na ordem da fila), HP e `Kill` em 7b (por id crescente).
- O pedido `Rugido` tipado, sem valor de dano, na frente da fila, com causa `Rugido`.
- Eventos individuais só para herói, elite e chefe; a horda agregada por tick; capacidade do buffer que cobre o pior tick.
- `modDano` e `modCadencia` do #8 lidos pelo #6 sem acoplar os dois sistemas por dados dentro do #6.

## Decision

### 1. A fila de pedidos
- **Dono:** o #6. O objeto `CombatRequests` (em `Forja.Gameplay.Sim`) implementa `ICombatRequests` e é entregue **por referência direta, pelo compositor**, ao #7, ao #8 e ao #3 (e ao próprio #6). Sem `static`, sem localizador, sem reflexão.
- **Por que isso não viola o ADR-0001:** o princípio do ADR-0001 (L84) é que a **ordem de assinatura nunca vire regra**. Esta fila não tem assinantes nem ordem de assinatura: é um buffer preenchido pela ordem fixa dos sistemas do compositor. A Emenda 18 (abaixo) registra a exceção de forma estreita, em três formas: a fila de pedidos do consumidor (esta Decisão), o acumulador hasheado do dono, escrito só pelo código do dono (`curaPendente`, Decisão 4), e a vista só de leitura do estado de outro sistema (`ICombatModifiers`, Decisão 6, e o `ICombatReadView` do ADR-0004). Eventos continuam sem poder ser canal (`event_as_inter_system_channel`).
- **Capacidade:** um array de `HitRequest` pré-alocado, de comprimento `cap_fila`, que é o `QueueCapacity` do `PhaseSnapshot` (ADR-0002 §4: a **fórmula é do GDD #6**, `cap_fila ≥ vivos_máx × fontes_de_área_por_tick + 8`, sem o termo do rugido, Decisão 3; o baker a calcula e o `DataValidator` a valida contra o teto do #1); dimensionado ou redimensionado no `Preparar` do #6, como as tabelas do ADR-0004. Fila cheia: `Aplicar` lança `SimInvariantException` (derivada de `InvalidOperationException`, lançada de um helper, para o host distinguir fila cheia de outro bug) **nos dois modos**, depois de gravar tick, `cap_fila` e `FilaPico`; um `Step` que lança leva a `Broken` (Emenda 2). Descartar mudaria o HP, que está no hash.
- **Quem pode enfileirar e quando:** os três métodos recebem `ref SimContext ctx`, que o Core monta para o `Step` de um sistema: o `Tick`, o `CombatActive` e o `Strict` vêm dele. `SimContext` é `ref struct`, então o `CombatRequests` **nunca** o guarda em campo. **Guarda do contexto (rodada 5):** `default(SimContext)` compila em qualquer lugar (um teste, um `Update`, um construtor), então "fora do `Tick`" **não** é inexpressável: `Aplicar` e `PedirRugido` lançariam só porque `CombatActive` vem falso em `default`, mas `Curar` vale sem `CombatActive` e gravaria `curaPendente`, que está no hash. Por isso o `SimContext` ganha a propriedade somente leitura `bool InStep`, que **só o Core preenche** (`true` no contexto que o `Simulation.Tick` monta para cada `Step`; construtor `internal` do assembly do Core; `default` = `false`), e os três métodos checam `ctx.InStep` **antes de qualquer outra coisa** e **lançam `InvalidOperationException` se for falso, nos dois modos, independentemente do `Strict`**, sem tocar na fila, em `curaPendente` nem em contador. Depois da guarda: `Aplicar` e `PedirRugido` lançam nos dois modos se `!ctx.CombatActive` (o #7 e o #8 já só agem com ele); `Curar` vale mesmo sem `CombatActive`, porque só acumula. O pedido guarda os números **crus**: a validação (NaN, infinito, negativo, `modDano` fora da faixa) e os contadores ficam na resolução 7a, onde a F1 do #6 os trata.
- **Ordem contratual** (a do GDD #6, Edge Cases): (1) o `Rugido`; (2) os pedidos do #8, na ordem em que foram enfileirados; (3) os impactos de telegraph, por id do atacante; (4) os contatos, por id; (5) o auto-ataque do herói. O #8 roda antes do #6 e enfileira durante o próprio `Step`; o #6 acrescenta os dele no passo 6. A fila é **append-only dentro do tick**; ninguém reordena.
- **Scratch:** a fila e o `acc` (dano acumulado por alvo) são scratch do #6, fora do hash, e **vazios ao fim de toda saída do `Step`**, inclusive o retorno antecipado sem `CombatActive` (ADR-0004, Decisão 3.4).

### 2. O pedido de golpe
`HitRequest` é uma `readonly struct` passada por `in`. Os campos exatos e seus domínios são do GDD #6 (F1 e F3); acrescentar um campo sem mudar a ordem, o dono nem a capacidade **não exige novo ADR** (o mesmo critério da `PhaseSheet` e do bloco do herói). Campos mínimos:

| Campo | Tipo | Uso |
|---|---|---|
| `SourceId` | `int` (−1 = sem entidade; exige `DirExplicita` quando há knockback) | atacante, para a direção do knockback, a causa e o `Esquiva` |
| `TargetId` | `int` | alvo; alvo morto no início do passe é descartado |
| `Kind` | `HitKind : byte` (`None = 0` inválido, `Contato = 1`, `Golpe = 2`) | escolhe `mit_contato` ou `mit_golpe` (F1) |
| `Flags` | `HitFlags : byte` (`Pesado = 1`, `Telegraph = 2`, `DirExplicita = 4`, `Suprema = 8`) | punição do `pesado` (F1), `Esquiva` só para telegraph, direção da `linha`, motivo 2 do `HitStop` |
| `Base` | `float` | dano base |
| `KbDistancia` | `float` | `D` do knockback (0 = nenhum) |
| `KbDirX`, `KbDirY` | `float` | só com `DirExplicita` (a investida `linha` empurra na direção da linha) |

`Rugido` **não** é um `HitRequest`. **`modDano` não viaja no pedido:** o #6 lê `ICombatModifiers.ModDano` uma vez no começo do `Step` e o aplica a todo golpe cuja `SourceId` é o herói (`Phase.HeroId`), inclusive os do #8; golpe de inimigo vale 1. Assim existe uma só fonte do número (F1). A `HitRequest` é construída só por fábricas nomeadas (`HitRequest.Contato(...)`, `HitRequest.Golpe(...)`), porque quatro `float` seguidos trocados de posição não dão erro de compilação; sem `init` nem `record`; 28 B com a ordem declarada.

### 3. O pedido `Rugido`
`ICombatRequests.PedirRugido(ref ctx)`, chamado só pelo #7, uma vez por fase, no tick de entrada do chefe, depois do `Spawn` do chefe; lança nos dois modos se `!ctx.InStep` (guarda da Decisão 1) ou `!ctx.CombatActive`. É **um sinal tipado, sem valor de dano**, e não N entradas na fila *(simplificação em relação ao texto do GDD #6, equivalente no efeito; provisória)*. Na resolução, o #6 o trata **antes de qualquer outro pedido**: todo alvo vivo no início do passe, **hostil** (facção do inimigo), de classe `Horda` ou `Elite` e não `Essencial`, em ordem crescente de id, é marcado (inclui o corpo que o #7 ou o #8 fez nascer antes do #6 no mesmo tick, que "pode ser alvo e morrer"; o rugido ignora i-frames, que só o herói tem, e o herói nunca é alvo); em 7b o HP vira 0 e o `Kill(id, DeathCause.Rugido)` sai com `dano_aplicado` = HP. Pula a F1 e a mitigação, não gera `Damage`, knockback nem `HitStop`. **A causa é a do primeiro pedido que zera o HP**: como o `Rugido` vem primeiro, todo alvo dele sai com causa `Rugido`, inclusive o corpo que o auto-ataque mataria no mesmo passe. Os demais pedidos do mesmo passe contra um alvo marcado **não somam em `acc`**: contam só 1 em `acertos` do `HordeTick` quando o alvo é da horda, e **não geram `Damage`, `Knockback` nem `HitStop`**, nem para o elite *(provisória)*. Por não ocupar entradas, o termo `teto_vivos_horda + 1` **sai** da fórmula de `cap_fila` (a pendência (f) do GDD #7 e a Edge Case do #6 mudam; ver GDD Sync). Chamar de novo no mesmo tick não muda nada (basta um `bool` `rugidoPendente`, scratch, limpo na saída do `Step` e no `Preparar`; não há campo de tick). "Uma vez por fase" é invariante do #7, testada no #7; o #6 não guarda estado entre ticks para isso (um segundo pedido em outro tick seria só um segundo rugido).

### 4. Cura
`ICombatRequests.Curar(ref SimContext ctx, int targetId, float amount)`, aceita de qualquer sistema dentro do seu `Step`, e **sempre acumula na coluna `curaPendente`** (ADR-0004), nunca entra na fila:
- Fora de um `Step` (`!ctx.InStep`, Decisão 1): lança `InvalidOperationException` nos dois modos, antes de validar o valor e sem gravar nada; é a guarda que impede `curaPendente` (no hash) de ser escrita por um `default(SimContext)`.
- `amount` NaN, infinito ou negativo: descarta, soma em `CurasDescartadas` (fora do hash) e lança se `ctx.Strict`. Alvo morto: descarta **sem contar** (é o caso legítimo do herói que morre no tick do level-up). `targetId` fora de `[0, IdCount)`: bug, conta em `CurasDescartadas` e lança se `ctx.Strict`. `amount` = 0 é válido e não faz nada.
- `curaPendente[alvo] = Min(curaPendente[alvo] + amount, hpMax[alvo])`. O clamp a `hpMax` não muda o resultado (a cura aplicada é `Min(hpMax, HP + cura)`) e mantém o `float` limitado. A soma segue a ordem: o pendente anterior e depois as curas na ordem de chamada; um `Curar` chamado pelo próprio #6 depois do 7b vale no próximo tick.
- O #6 consome a coluna em **7b**, no primeiro passe com `CombatActive`: `base = Min(hpMax, HP + curaPendente)`, `curaPendente = 0`, e só então subtrai o `acc` (a cura soma antes do dano e nunca reanima: vale só para quem estava vivo no início do passe). Um `Curar` do #3 (que roda depois do #6) entra no próximo tick com combate; um `Curar` do #8 (que roda antes) entra no mesmo tick. Com `CombatHold ≠ 0` a coluna espera, no hash. Esta decisão **elimina o scratch `curaAcc`** do GDD #6 *(provisória; sincronizar o F2)*.

### 5. Resolução em dois tempos
Dono: o #6; os passos 7a e 7b são os do GDD #6, e este ADR só fixa os invariantes:
- **7a:** (i) tira a foto `vivoNoInicio` e lê `iframes` uma vez; (ii) marca os alvos do `Rugido`; (iii) percorre a fila **em ordem**: descarta alvo morto no início do passe, valida (F1: descarte e `GolpesDescartados` ou clamp e `GolpesLimitados`), descarta com `iframes > 0` (e guarda um `Esquiva` por herói se o descartado era `Telegraph`), senão `acc[alvo] += dano_final`, anota a primeira entrada que leva a vida a zero (a causa) e acumula para o evento (um `Damage` por alvo individual por tick, a soma; `acertos` e `danoTotal` da horda). A soma em `float32` na ordem da fila, **sem FMA**.
- **7b:** por id crescente, para quem estava vivo no início: aplica a cura (Decisão 4), `HP' = (base − acc < HP_RESIDUO) ? 0 : base − acc`, grava por `HpAndPosForWrite` e, se zerou, chama `Kill(id, causa)` na mesma escrita. Herói e chefe podem morrer no mesmo tick (Regra 13 do #3).
- Valor inválido que chega a 7b (`mit` NaN, HP ≤ 0 em vivo): exceção nos dois modos (GDD #6). Os contadores de diagnóstico (`GolpesDescartados`, `GolpesLimitados`, `ModForaDeFaixa`, `CurasDescartadas`) seguem a regra única de modo do ADR-0001 (item 9): lançam no primeiro caso no estrito e só contam no não estrito (`CurasDescartadas` conta só valor inválido e id fora de faixa, nunca o alvo morto); ficam em uma `readonly struct CombatCounters` lida pelo host e pelo log (#5), **fora do hash**, junto com o pico de uso da fila (para ajustar `cap_fila`).
- O `Strict` do modo chega aos sistemas por **`SimContext.Strict`** (somente leitura, Emenda 18 d).

### 6. `modDano` e `modCadencia`
Estado **escrito pelo #8**: mora no #8 e chega ao #6 por `ICombatModifiers` (`float ModDano`, `float ModCadencia`), entregue por referência pelo compositor, com uma implementação padrão `NullCombatModifiers` (1, 1) quando não há #8 (testes, `FakeSistema8`). O #6 lê as duas **uma vez no começo do `Step`**; o `Hash` delas é do #8. A faixa é validada pelo #6 (F1 e Edge Cases do GDD #6): `modDano` fora de `[1, MODDANO_MAX]` descarta os golpes do herói do tick (cada um conta em `GolpesDescartados`); `modCadencia` fora de `[MOD_CAD_MIN, MOD_CAD_MAX]` mantém o último valor válido (inicial 1) e conta `ModForaDeFaixa`. O **último valor válido** de `modCadencia` é um campo do bloco do herói do #6 (hasheado; acréscimo pela regra de extensão do ADR-0004, sem novo ADR). Este ADR não define o conteúdo do #8: ele fixa só o contrato.

### 7. Eventos
**Princípio (Emenda 18 b):** evento de regra é emitido **por quem decide**, nunca pelo Core. `SimWorld.Kill` marca a morte e anota em `DeathsThisTick`, **sem emitir evento**; `SimWorld.Spawn` também não emite. O #6 emite os de combate e o #7 emite `Spawn` (só de elite e chefe; o #8, o das invocações individuais) e `Rugido`. **`Kill` só pelo #6** (e pelo Core no caminho do NaN), senão uma morte ficaria sem evento. Assim a uma morte corresponde no máximo um evento individual e a horda sai agregada, e a ordem de emissão é a ordem dos sistemas.

**`SimEvent`** ganha `int ArgA, ArgB` (Emenda 18 c). **Tabela de tipos** (valores explícitos; só cresce no final; os tipos de #3, #16 e #5 entram depois):

| Kind | Valor | Emissor | Payload |
|---|---|---|---|
| `None` | 0 | nunca | inválido |
| `Damage` | 1 | #6 | só alvo individual (herói, elite, chefe) e só com ao menos 1 golpe aceito; `TargetId`, `ActorId` = fonte do 1º golpe aceito, `Value` = soma de `dano_final` dos golpes aceitos (o `acc`, antes da cura e do limite pelo HP; a mitigação já está dentro), `ArgA` = bits do que ocorreu em algum golpe aceito (1 `Pesado`, 2 em Recuperação, 4 `Aberto`), `ArgB` = número de golpes aceitos (os descartados por i-frames, NaN ou alvo morto não entram) *(provisória)* |
| `Death` | 2 | #6 | elite e chefe; `TargetId`, `ArgA` = `DeathCause` *(resolve o "a rever" da Emenda 15)* |
| `Spawn` | 3 | quem faz nascer (o #7; o #8 nas invocações individuais) | só elite, chefe e invocação individual; nenhum evento por corpo de horda (a apresentação deriva de `tickNascimento`) |
| `SkillCast` | 4 | #8 | do #8 |
| `Esquiva` | 5 | #6 | `ActorId` = atacante, `TargetId` = herói; só quando a esquiva nega telegraph; uma vez por tick e por herói |
| `Knockback` | 6 | #6 | `TargetId`, `Value` = deslocamento total |
| `HitStop` | 7 | #6 | `Value` = ticks (3), `ArgA` = motivo (1 sofrido, 2 suprema, 3 pesado) |
| `Rugido` | 8 | #7 | sempre emitido, mesmo com 0 corpos; `ArgA` = alvos esperados (informativo) |
| `HordeTick` | 9 | #6 | agregado da horda no tick, só se algum valor for > 0: `ArgA` = mortes (inclui as do `Rugido`), `ArgB` = acertos, `Value` = `danoTotal`; acertos e dano só contam pedidos com valor, nunca o rugido |
| `TelegraphStart` | 10 | #6 | emitido no passo 4, quando o Aviso começa, antes dos eventos do passo 8; início do Aviso de elite e chefe; `ActorId` = atacante, `ArgA` = índice do golpe, `Value` = `A` em ticks |
| `HeroDeath` | 11 | #6 | morte do herói; `TargetId` |

**Reserva por tipo, nunca por conteúdo:** `EventosReservados` (ADR-0001) vale para `HeroDeath`, `TelegraphStart`, o fim de fase e a oferta (do #3 e do #16). **Ordem de emissão do #6:** `TelegraphStart` no passo 4, quando o Aviso começa; depois, no passo 8: `Esquiva`; depois, por id crescente de alvo individual, `Damage`, `Knockback`, `Death` ou `HeroDeath`; depois `HitStop`; por último `HordeTick`. **Capacidade do buffer** (o GDD #6 dá `EventosReservados + 5 + 3 × individuais_máx + 4` sem decompor, e aqui os termos têm nome; o `EventCapacity` do `PhaseSnapshot` é a **capacidade final** usada no `Simulation.Create`, ADR-0002 §4): `EventCapacity ≥ R + 3 × individuais_máx + 4 + S_max + K + E_3_16`, em que `R` = `EventosReservados` (cobre `HeroDeath`, `TelegraphStart` ≤ 3, fim de fase e oferta), **constante de código do Core** (de 8 a 16, ADR-0001 Emenda 10), validada pelo **teste do Core** e **não** pelo #1: `R` não é dado do snapshot, e o #1 só valida os termos que vêm de dados; o `Simulation.Create` confere a desigualdade **completa, com `R`** (ADR-0001 Emenda 22; ADR-0002 §4), no mesmo caminho de falha da conferência de ids (ADR-0001, item 6), e não o baker nem o compositor; o `EventCapacityDataTerms` (só os termos de dados, sem `R`) é o que o baker calcula e o `DataValidator` valida (ADR-0001 Emenda 22); `3 × individuais_máx` = `Damage`, `Knockback` e `Death` de cada alvo individual; `4` = `Rugido`, `HordeTick`, `Esquiva` e `HitStop`; `S_max` = `Spawn` individuais por tick (elite, chefe, invocação); `K` = `SkillCast` por tick (**knob pendente do #8**); `E_3_16` = eventos do #3 e do #16 fora de `R` (**pendente dos ADRs ou GDDs deles**). O pior tick é o da entrada do chefe (`Spawn` do chefe, `Rugido`, `HordeTick` e `Death` do elite, mais os eventos do herói naquele tick), e a capacidade não depende do número de corpos da horda. Enquanto `K` e `E_3_16` estão pendentes (seguem `NOT ASSESSED`), o #1 valida com `K = 0` e `E_3_16 = 0` **e registra a pendência como `NOT ASSESSED` para o #8, o #3 e o #16**; a Verification Required 5 só é conclusiva depois deles. **O "5" do GDD #6 (rodada 8):** o `EventosReservados + 5 + 3 × individuais_máx + 4` do GDD #6 traz um "5" que é um **piso provisório** para `S_max + K + E_3_16`. Este ADR declara: `S_max + K + E_3_16` **substitui** o 5 do GDD, e o baker **EXIGE** `S_max + K + E_3_16 ≥ 5` (piso do GDD #6; erro de build se menor), enquanto `K` e `E_3_16` estão `NOT ASSESSED` (= 0 no cálculo). A fórmula do `EventCapacityDataTerms` do ADR-0001 **não muda**; a validação do piso e o teste `EventCapacity_PisoDoGdd6_Recusa` ficam no `DataValidator` do ADR-0002.

### 8. Emenda 18 ao ADR-0001 (aprovada pelo autor e aplicada no ADR-0001; o texto abaixo é o que este ADR pediu)
(a) exceção estreita ao L84, com **três formas** de canal direto, todas entregues pelo compositor por referência, sem `static`, sem reflexão e nunca por evento: (i) uma fila de pedidos tipada, dona do consumidor, preenchida na ordem do compositor, scratch fora do hash e vazia ao fim do `Step` do dono (`ICombatRequests`); (ii) um acumulador hasheado do dono, escrito só pelo código do dono (`curaPendente`, via `Curar`); (iii) uma vista só de leitura do estado de outro sistema (`ICombatReadView` do #6, `ICombatModifiers` do #8); (b) `Kill` e `Spawn` do Core não emitem evento; o item 6 da Emenda 6 perde "emite `Death` uma vez"; `Kill` só pode ser chamado pelo #6 (e pelo Core no caminho do NaN), e quem faz nascer elite, chefe ou invocação individual emite o `Spawn`; (c) `SimEvent` ganha `ArgA` e `ArgB` e entra a tabela de tipos acima; a Emenda 15 passa a dizer que `Death` carrega a causa em `ArgA`; (d) `SimContext.Strict`; (e) a reserva `EventosReservados` é por tipo (`HeroDeath`, `TelegraphStart`, fim de fase, oferta); (f) a caminho do NaN do Core (HP ou posição não finitos), a morte entra em `DeathsThisTick` com causa `InvalidValue` e **não emite evento** (a apresentação lê a lista); (g) o registro (feito: `sim_events` ganhou este ADR e a assinatura nova; entraram os contratos `combat_requests` e `combat_modifiers`; foram revistas as descrições de `event_as_inter_system_channel` (as três formas), `sim_death_cause` (`Death` carrega a causa em `ArgA`), `combat_columns` e `scratch_surviving_tick` (sai `curaAcc`; entra o sinal do `Rugido`)); (h) o ADR-0004 recebeu uma nota de sincronia (feito, 2026-11-06: sai `curaAcc` do catálogo de scratch e da Decisão 3.4; o Ordering Note deixou de dizer que o ADR-0005 não o toca).

### Architecture Diagram
```
 ordem do compositor:   #7 Horda ──▶ #8 Skills ──▶ #6 Combate ──▶ #3 Fluxo ──▶ #16 Oferta
                          │            │             ▲  ▲             │
        PedirRugido()─────┘            │             │  │ Curar()─────┘ (próximo tick com combate)
        Spawn event (elite/chefe)      │             │  └ curaPendente (coluna do #6, no hash)
                                       └Aplicar()────┘
                        ICombatRequests (fila append-only, dona do #6, fora do hash)
 #6, passo 7a: foto vivoNoInicio + iframes ▶ Rugido ▶ fila em ordem ▶ acc[alvo]   (soma float32, sem FMA)
 #6, passo 7b: por id: cura ▶ HP' ▶ HpAndPosForWrite ▶ Kill(id, causa)            (DeathsThisTick)
 #6, passo 8:  Esquiva ▶ por alvo individual: Damage, Knockback, Death/HeroDeath ▶ HitStop ▶ HordeTick
 #8 ──ICombatModifiers(ModDano, ModCadencia)──▶ #6 lê uma vez no começo do Step
```

### Key Interfaces
```csharp
namespace Forja.Simulation   // acrescenta ao ADR-0001 (Emenda 18)
{
    public enum SimEventKind : byte { None = 0, Damage = 1, Death = 2, Spawn = 3, SkillCast = 4, Esquiva = 5, Knockback = 6,
                                      HitStop = 7, Rugido = 8, HordeTick = 9, TelegraphStart = 10, HeroDeath = 11 }   // explícitos; só cresce no final

    public readonly struct SimEvent
    {
        public readonly int Tick;
        public readonly SimEventKind Kind;
        public readonly int ActorId, TargetId;
        public readonly float Value;
        public readonly int ArgA, ArgB;     // significado por tipo, na tabela da Decisão 7
    }

    public ref struct SimContext
    {
        public bool Strict { get; }
        public bool InStep { get; }     // rodada 5: só o Core preenche (true no contexto de cada Step; construtor internal); default(SimContext) = false
        /* ...resto no ADR-0001 */
    }
    // SimWorld.Kill e SimWorld.Spawn deixam de emitir evento.

    /// <summary>Invariante da simulação violado (fila cheia, por exemplo). O host a distingue de outro bug; o Step que a lança leva a Broken.</summary>
    public sealed class SimInvariantException : System.InvalidOperationException { public SimInvariantException(string message) : base(message) { } }
}

namespace Forja.Gameplay.Sim   // sem engine
{
    public enum HitKind : byte { None = 0, Contato = 1, Golpe = 2 }
    [System.Flags] public enum HitFlags : byte { None = 0, Pesado = 1, Telegraph = 2, DirExplicita = 4, Suprema = 8 }

    public readonly struct HitRequest { /* campos mínimos da Decisão 2; os exatos são do GDD #6 (F1, F3) */ }

    // CombatRequests: sealed, dono #6, entregue por referência pelo compositor. Os métodos recebem o ctx do Step do chamador
    // (ref struct: nunca vira campo), de onde vêm Tick, CombatActive e Strict. Fora de um Step (default(SimContext)) os três lançam
    // InvalidOperationException, nos dois modos, pela guarda ctx.InStep (primeira checagem de cada método).
    public interface ICombatRequests
    {
        void Aplicar(ref SimContext ctx, in HitRequest hit);        // lança se !ctx.InStep ou !ctx.CombatActive; só enfileira; fila cheia lança SimInvariantException (nos dois modos)
        void PedirRugido(ref SimContext ctx);                       // só o #7; lança se !ctx.InStep ou !ctx.CombatActive; idempotente no tick; "uma vez por fase" é invariante do #7
        void Curar(ref SimContext ctx, int targetId, float amount); // qualquer sistema; lança se !ctx.InStep; acumula em curaPendente (ADR-0004), nunca na fila; lança se ctx.Strict e o valor é inválido
    }

    public interface ICombatModifiers           // implementada pelo #8; NullCombatModifiers = (1, 1)
    {
        float ModDano { get; }
        float ModCadencia { get; }
    }

    public readonly struct CombatCounters       // fora do hash; lida pelo host e pelo log (#5)
    {
        public readonly int GolpesDescartados, GolpesLimitados, ModForaDeFaixa, CurasDescartadas, FilaPico;
    }
}
```

### Implementation Guidelines
- A fila **must** ser um array pré-alocado de `HitRequest`, dimensionado no `Preparar` do #6 com `cap_fila` (o `QueueCapacity` do `PhaseSnapshot`, fórmula do GDD #6), e **must never** crescer, ser realocada no `Tick` nem usar `List<T>`; fila cheia **must** lançar nos dois modos.
- `Aplicar`, `PedirRugido` e `Curar` **must** receber `ref SimContext ctx` (o contexto do `Step` do chamador) e **must never** guardá-lo; os três **must** checar `ctx.InStep` primeiro e lançar `InvalidOperationException` nos dois modos (independentemente do `Strict`) se for falso, sem gravar nada; só o Core **must** preencher `InStep` (construtor `internal`); `Aplicar` e `PedirRugido` **must** lançar nos dois modos se `!ctx.CombatActive`; `Aplicar` e `PedirRugido` **must** só enfileirar/marcar e **must never** alterar HP, `curaPendente` nem coluna alguma.
- Só o #7 **must** chamar `PedirRugido`, no máximo uma vez por fase; só o #6 **must** chamar `HpAndPosForWrite`, e o #6 **must** gravar HP só em 7b.
- `Aplicar` **must** lançar nos dois modos se `SourceId == −1`, `KbDistancia > 0` e o pedido não tem `DirExplicita` (uma área sem entidade, do #8, não tem como derivar a direção do knockback; ADR-0006).
- A fila **must** ser percorrida na ordem de inserção por um laço sequencial, e a soma de `float32` **must** seguir essa ordem, com o produto e a soma em instruções separadas; **must never** usar `MathF.FusedMultiplyAdd`, ordenar, deduplicar nem somar fora da ordem. A contração implícita de `a*b+c` pelo compilador do IL2CPP não é controlável pelo projeto e é o risco já aceito no ADR-0001.
- O #6 **must** esvaziar a fila, o `acc` e o sinal do `Rugido` em toda saída do `Step`, inclusive o retorno antecipado sem `CombatActive`.
- `Curar` **must** acumular só em `curaPendente`, limitada a `hpMax`; **must never** entrar na fila nem curar na hora. O #6 **must** consumir `curaPendente` em 7b antes de subtrair o dano, só para quem estava vivo no início do passe.
- `Kill` e `Spawn` do Core **must never** emitir evento; `Kill` **must** ser chamado só pelo #6 (e pelo Core no caminho do NaN); `HitRequest` **must never** carregar `modDano`; cada evento **must** ser emitido pelo sistema que decide (tabela da Decisão 7) e **must never** ser lido por outro sistema do tick como canal.
- `Death` e `HeroDeath` **must** ser individuais só para herói, elite e chefe; a horda **must** sair agregada em `HordeTick`, e **must never** haver evento por corpo de horda nascido, acertado ou morto.
- Um `switch` sobre `SimEventKind`, `HitKind` ou `DeathCause` **must** ter `default` que lança; valores **must** ser explícitos e só crescer no final.
- A reserva de `EventosReservados` **must** ser por `Kind`, nunca por conteúdo do payload.
- `ICombatModifiers` **must** ser lida uma vez por `Step`; o #6 **must never** ler outro dado do #8 por esse canal.
- Todo contador de diagnóstico do #6 **must** seguir a regra única de modo (lança no primeiro no estrito; conta no não estrito) por `ctx.Strict`, e **must never** entrar no hash.
- Sobre `HitFlags`, **must** usar `(f & HitFlags.X) != 0` e **must never** usar `HasFlag`; `Enum.ToString` e `Enum.IsDefined` **must never** rodar no `Tick` (o log usa tabela de nomes).
- Enfileirar **must** ser `fila[n++] = hit`, percorrer **must** ser por `ref readonly` e esvaziar **must** ser `n = 0`; `HitRequest` **must** ser criada só pelas fábricas nomeadas, e `CombatRequests` **must** ser `sealed`.
- Fila cheia **must** lançar `SimInvariantException` de um helper, depois de gravar tick, `cap_fila` e `FilaPico`; o AC-P2 **must never** forçar o lançamento.

## Alternatives Considered

### Alternative 1 (B): cada produtor tem o seu buffer e o #6 lê por vistas
- **Description**: o #7 guarda o sinal do rugido, o #8 guarda a sua lista de golpes e o #3 guarda o seu pedido de cura; o #6 lê tudo por vistas, na ordem fixa.
- **Pros**: nenhum canal compartilhado, então nada a emendar no L84 do ADR-0001; cada dono tem o seu estado.
- **Cons**: cada produtor define o seu tipo de buffer, a sua vista e a sua capacidade; o GDD #6 e o futuro GDD #8 precisariam ser reescritos sobre um `Aplicar` que deixa de existir; a ordem contratual vira "ordem das vistas" e mais difícil de testar; o #8 não tem GDD ainda.
- **Rejection Reason**: mais código e mais contratos para o dev solo, sem ganho de determinismo: a ordem da fila já é a ordem fixa do compositor.

### Alternative 2 (C): a fila no `SimWorld` (Core)
- **Description**: o Core guarda o buffer de pedidos de dano.
- **Pros**: um só lugar; o L84 do ADR-0001 fica intacto.
- **Cons**: o Core passa a conhecer o vocabulário de combate (dano, mitigação, knockback), que o ADR-0001 quis fora dele; o hash e as Key Interfaces do Core crescem com cada campo do GDD #6.
- **Rejection Reason**: acopla o Core a um sistema de regra.

### Alternative 3 (D): aplicar o dano na hora (sem fila)
- **Description**: `Aplicar` muda o HP imediatamente.
- **Pros**: nenhum buffer.
- **Cons**: o resultado dependeria da ordem de chamada; herói e chefe não poderiam morrer no mesmo tick; i-frames seriam lidos em momentos diferentes.
- **Rejection Reason**: contradiz a Regra 3 e a resolução em dois tempos do GDD #6.

### Alternative 4 (E): eventos como canal entre sistemas
- **Rejection Reason**: banida por `event_as_inter_system_channel` (ADR-0001).

### Alternative 5 (F): o `Rugido` como N entradas na fila
- **Description**: o #7 enfileira um pedido por alvo vivo de horda e elite (o texto atual do GDD #6/#7).
- **Pros**: o pedido é um dado como os outros.
- **Cons**: a fila precisa de `teto_vivos_horda + 1` posições a mais só para um tick por fase; o #7 teria de conhecer os alvos.
- **Rejection Reason**: o sinal único dá o mesmo efeito (mesmos alvos, mesma ordem, mesma causa) sem inflar a capacidade. Provisória: se o GDD #6 preferir N entradas, só a fórmula de `cap_fila` volta a ter o termo.

### Alternative 6 (G): `Kill` e `Spawn` continuam emitindo evento no Core
- **Description**: o Core emite `Death` e `Spawn` como no ADR-0001, e o #6 só soma o agregado.
- **Cons**: 300 mortes no rugido viram 300 `Death`, o que exige `EventCapacity ≥ pico_vivos + reserva` e polui o log; o Core precisaria saber que a horda é agregada.
- **Rejection Reason**: evento de regra tem que sair de quem decide.

## Consequences

### Positive
- Um único canal de dano e cura, com ordem contratual e testável (R3, R14, R22, E1, D1 do #6).
- O buffer de eventos não cresce com o número de corpos (o pior tick deixa de ser 300 `Death`).
- O Core fica sem vocabulário de combate, e o #8 pode ser escrito contra `ICombatRequests` e `ICombatModifiers` sem esperar o #6.
- `curaPendente` único tira o scratch `curaAcc` e resolve a cura do level-up sob `CombatHold` sem fila extra.
- `Death` passa a carregar a causa, o que atende ao log (#5) sem dedução.

### Negative
- A Emenda 18 muda o ADR-0001 em eventos (`Kill`, `Spawn`, `SimEvent`, reserva por tipo): os GDDs #2 (Regras 5 e 6 e os Edge Cases de capacidade e de valores inválidos) e #7 também mudam (ver GDD Sync).
- O #6 passa a ser o emissor dos eventos de combate; um teste do #2 sozinho (sem #6) não vê `Death`.
- O log (#5) perde o evento por corpo de horda; ele vê `HordeTick` e `DeathsThisTick`.
- Uma fila de pedidos entre sistemas é um canal a mais para disciplinar (revisão de código e analisador).
- O `Rugido` por sinal diverge do texto do GDD #6/#7.

## Risks
- **`cap_fila` subdimensionado** derruba a simulação (`Broken`). Mitigação: a fórmula do GDD #6 (validada pelo #1) sem o termo do rugido, o pico de uso (`FilaPico`) no log e o AC-P2.
- **Ordem de enfileiramento mal entendida pelo #8** (sem GDD). Mitigação: o contrato está aqui; o teste D1/I2 com um `FakeSistema8` embaralhado.
- **`HitRequest` incompleto** quando o GDD #8 existir. Mitigação: a regra de extensão (campo novo sem mudar ordem, dono nem capacidade não exige ADR).
- **Dois emissores do mesmo evento** por engano. Mitigação: a tabela da Decisão 7 e o analisador (`SimWorld` não emite).
- **Soma de `float32` por ordem** diverge entre runtimes. Já é o risco aceito do ADR-0001 (mesmo build), não novo.
- **Resultado do `unity-specialist` (5.5, 2026-11-06): dois bloqueios, ambos revistos e confirmados pelo autor.** B1: `CombatRequests` não tinha de onde ler `Tick`, `CombatActive` e `Strict` (`SimContext` é `ref struct`); agora cada método recebe `ref SimContext ctx`. B2: "sem FMA" não é garantível em C# 9 e IL2CPP; agora é ordem fixa da soma, proibição de `FusedMultiplyAdd` e o risco de contração aceito no ADR-0001. Notas aplicadas: `SimInvariantException`, fábricas nomeadas, sem `HasFlag`, `CombatRequests` `sealed`, Knowledge Risk com um único valor. `NOT SOURCEABLE`: IL2CPP, contração de `float`, stack trace em Release, custo de interface call.
- **Resultado do `technical-director` (TD-ADR, 5.6, 2026-11-06): CONCERNS, 1 bloqueante e 9 importantes, todos de especificação; revisão escolhida pelo autor e aplicada:** exceção do L84 em três formas; `Kill` só pelo #6; seção GDD Sync; alvos do `Rugido` (facção hostil, nascidos no tick, sem i-frames) e o que os outros pedidos fazem com eles; `PedirRugido` lança sem `CombatActive`; `CurasDescartadas` sem alvo morto; `modDano` só no #6; bit `Suprema`; payload de `Damage`; capacidade de eventos decomposta, com `K` e `E_3_16` pendentes como `NOT ASSESSED`; Risks e Migration Plan corrigidos.
- **Pendências abertas, não deste ADR:** `K` (`SkillCast` por tick) do #8 e `E_3_16` do #3 e do #16 para fechar a capacidade de eventos. (A nota de sincronia no ADR-0004 e a revisão das quatro entradas do registro já foram feitas em 2026-11-06.)

## GDD Requirements Addressed

| GDD System | Requirement | How This ADR Addresses It |
|------------|-------------|--------------------------|
| combate-e-dano.md (TR-combate-005) | Ponto único `Combate.Aplicar`/`Curar` com fila entre sistemas, `Rugido` tipado na frente, resolução 7a/7b, scratch fora do hash, estouro vira `Broken` | Decisões 1 a 5 |
| combate-e-dano.md (TR-combate-007) | Eventos individuais só para herói, elite e chefe; horda agregada `{mortes, acertos, danoTotal}` | Decisão 7 (`HordeTick`, `Death`, `HeroDeath`) |
| combate-e-dano.md (TR-combate-021) | Capacidade de eventos e `DeathsThisTick` sem descarte | Decisão 7 (capacidade) e Decisão 5 (`Kill` anota sempre) |
| combate-e-dano.md (TR-combate-001, parte) | Escalares `modDano` e `modCadencia` do #8 | Decisão 6 (`ICombatModifiers`) |
| combate-e-dano.md (Regra 15, R22) | Cura soma antes do dano, nunca reanima, sobrevive ao `CombatHold` | Decisão 4 |
| combate-e-dano.md (Regras 3, 14; R3, R14, E1) | Descartes contados, `Esquiva` 1× por tick, fila cheia quebra a simulação | Decisões 1, 5 e 7 |
| horda-waves-e-inimigos.md (TR-horda-010) | `Rugido` tipado, sem dano, na frente da fila, causa `Rugido` | Decisão 3 (sinal único; o termo `teto_vivos_horda + 1` sai de `cap_fila`) |
| horda-waves-e-inimigos.md (TR-horda-016, 022) | Evento `Rugido` mesmo com 0 corpos; nenhum evento por corpo nascido; o tick do rugido sem `DroppedEvents` | Decisão 7 (`Rugido`, `Spawn` só de elite e chefe, `HordeTick`) |
| simulacao-deterministica.md (Regra 6, Edge Cases) | `EventBuffer` só de saída; `DroppedEvents` nunca em silêncio; até 300 `Death` no rugido | Decisão 7 e Emenda 18: o agregado substitui os 300 `Death` |
| fluxo-de-fase.md (Regra 6, `Curar`) | O #3 pede a cura do level-up | Decisão 4 |

## Performance Implications
- **CPU**: enfileirar é uma escrita em array; a resolução é O(fila + alvos); a soma em `float32` por alvo. Sem alocação por `Tick`. O custo do `Tick` do #6 é medido no spike (OQ-14 do #6).
- **Memory**: a fila ocupa `cap_fila × ~28 B` (por exemplo ~310 entradas ≈ 10 KB); o evento ganha 8 B; scratch do #6 no ADR-0004.
- **Load Time**: alocação da fila no `Preparar`, na tela de carregamento.
- **Network**: não se aplica.

## Migration Plan
Nenhum código existe. Ordem: (1) feito: a Emenda 18 e a Emenda 17 (pedida pelo ADR-0004) estão aplicadas no ADR-0001 e a nota de sincronia está no ADR-0004; o `SimContext.InStep` já está no ADR-0001 (Emenda 22); falta a aceitação dos três; (2) o #6 implementa `CombatRequests` e o compositor entrega a referência; (3) o #7 troca o rugido por `PedirRugido()` e emite `Spawn` (elite e chefe) e `Rugido`; (4) o #3 usa `Curar`; (5) o GDD #8 nasce contra `ICombatRequests` e `ICombatModifiers`; (6) os testes R3, R14, R22, E1, D1 e I2 do #6 deixam de estar "BLOQ".

## Validation Criteria
- R3, R14, R22, E1 do #6 com `FakeSistema8`: descartes contados, 1 `Esquiva` por tick, fila cheia leva a `Broken`, `curaPendente` no hash e aplicada no primeiro passe com combate.
- R14: 300 mortes de horda e 1 do elite no mesmo tick geram 1 `HordeTick` e 1 `Death`, sem `DroppedEvents`.
- D1: duas execuções com a mesma seed e comandos, hash igual em todos os ticks; e hash diferente quando a ordem de enfileiramento muda.
- TR-horda-010/016/022: o rugido sai com causa `Rugido`, o evento `Rugido` sai mesmo com 0 corpos, e nenhum evento por corpo nascido.
- Teste: `SimWorld.Kill` e `SimWorld.Spawn` não emitem evento (um teste do #2 sozinho).
- **Teste de contrato da guarda do contexto** (`CombatRequests_CtxForaDoStep_Lanca`): com `default(SimContext)`, `Aplicar` (pedido válido), `PedirRugido` e `Curar` (alvo vivo, valor válido) lançam `InvalidOperationException`, com o modo estrito e com o não estrito; depois de cada chamada a fila está vazia, `curaPendente[alvo]` segue 0, `CurasDescartadas` e `FilaPico` não mudaram e o `Hash` do #6 é o mesmo de antes; dentro de um `Step` real (com `CombatActive`) as mesmas três chamadas funcionam. O teste não depende do `CombatActive`: o caso `Curar` com `default` é o que prova que a guarda é `InStep` e não `CombatActive`.
- Reavaliar com o jogo jogável: o sinal único do `Rugido`, `Curar` só por `curaPendente`, a reserva por tipo e o payload dos eventos.

## GDD Sync (pendente; os GDDs não foram editados)
- **combate-e-dano.md:** Regra 3 (o `Rugido` deixa de passar por `Aplicar`: é `PedirRugido`); Regra 15 e F2 (`Curar` só acumula em `curaPendente`, sai o scratch `curaAcc`; a cura do #8 sob `CombatHold` deixa de se perder, o que é melhor que o texto); Edge Case de `capFila` (L353) e o knob `cap_fila` (L525): sai o termo `teto_vivos_horda + 1`; `modDano` não viaja no pedido; `CurasDescartadas` não conta alvo morto; nomes de evento: "Morte" vira `Death` ou `HeroDeath`, a morte agregada vira `HordeTick`, e o payload de `Damage` da Decisão 7.
- **horda-waves-e-inimigos.md:** Regra 10.2 (o rugido sai por `PedirRugido`, sem N entradas) e a exigência (f) do #6 (L177); o #7 emite `Spawn` só de elite e chefe, e `Rugido`; TR-horda-010 e 022.
- **simulacao-deterministica.md:** Regra 5 ("só pelo `SimWorld`"), Regra 6 (a reserva de "`Death` do herói" vira `HeroDeath`; `Kill` e `Spawn` do Core não emitem), o Edge Case do caminho do NaN (o `Death` com motivo inválido não sai mais) e o de capacidade de eventos ("até 300 `Death`" vira o agregado). As linhas exatas vêm do relatório do TD-ADR e precisam ser conferidas.
- **ADR-0004 e registro:** já sincronizados em 2026-11-06 (Emenda 18 (g) e (h)); não são pendência deste ADR.

## Related
- Depende de `docs/architecture/adr-0001-simulacao-deterministica-float32-tick-30hz.md` (Emenda 18 aplicada), `docs/architecture/adr-0004-colunas-do-simworld-combate-e-horda.md` e `docs/architecture/adr-0002-dados-e-balanceamento-snapshot-imutavel-gerado-no-build.md`.
- ADR vizinho: `docs/architecture/adr-0006-vetor-geometria-e-consulta-espacial-deterministicos.md` (`Proposed`), que depende deste ADR (ver Enables).
- GDDs: `design/gdd/combate-e-dano.md`, `design/gdd/horda-waves-e-inimigos.md`, `design/gdd/simulacao-deterministica.md`, `design/gdd/fluxo-de-fase.md`.
- `docs/architecture/architecture-review-2026-11-05.md` (Required ADRs, item 3).

## Decisões provisórias (a reavaliar com o jogo jogável)
Fila dona do #6 com exceção estreita ao L84; `Rugido` como sinal único (sai o termo `teto_vivos_horda + 1` de `cap_fila`); `Curar` só por `curaPendente` (sai o `curaAcc`); `Kill` e `Spawn` sem evento no Core; `SimEvent` com `ArgA`/`ArgB`; `Death` com a causa em `ArgA`; reserva de eventos por tipo; `HeroDeath` como tipo próprio; ordem de emissão do #6; `ICombatModifiers` com `NullCombatModifiers`; `SimContext.InStep` como guarda dos três métodos (rodada 5).

## Emenda de 2026-11-10 (rodada 5)
Origem: `architecture-review-2026-11-10-3.md` (3ª passada, itens 6 e 7 do ADR-0005; seções "Cross-ADR Conflicts" e "Blocking Issues") e a lista de texto desatualizado do `architecture-review-2026-11-06.md`; autorização do usuário ("emendar antes o ADR-0003 e os ADRs 0005 e 0006"). Status segue `Proposed`. Esta rodada não muda a fila, a ordem contratual, o `HitRequest`, o `Rugido`, a cura, a tabela de eventos nem a fórmula de `EventCapacity` (só a quem pertence cada termo).

| Item | Mudança de contrato | Onde |
|------|--------------------|------|
| 3ª passada nº 6 e nº 7 (`QueueCapacity`, `EventCapacity`) | O `cap_fila` é o `QueueCapacity` do `PhaseSnapshot` (ADR-0002 §4): a **fórmula é do GDD #6**, o baker a calcula e o `DataValidator` a valida contra o teto do #1 (antes: "fórmula e validação do #1"). O `EventCapacity` do snapshot é a **capacidade final** do `Create`. O termo `R` (`EventosReservados`) é **constante de código do Core** (ADR-0001 Emenda 10, de 8 a 16), validada pelo teste do Core e não pelo #1; o #1 valida só os termos de dados; o `Simulation.Create` confere a desigualdade completa, com `R` (corrigido na rodada 7: não é o compositor; ADR-0001 Emenda 22). `K` e `E_3_16` seguem `NOT ASSESSED`. | Decisão 1 (Capacidade), Decisão 7 (capacidade), Implementation Guidelines, Risks |
| `Curar` sem guarda (MEDIUM) | "Fora do `Tick` é inexpressável" era falso (`default(SimContext)` compila em qualquer lugar; `Curar` vale sem `CombatActive` e gravaria `curaPendente`, que está no hash). Novo campo **`SimContext.InStep`** (`bool`, somente leitura, só o Core preenche, `default` = `false`): `Aplicar`, `PedirRugido` e `Curar` o checam primeiro e **lançam `InvalidOperationException` nos dois modos**, independentemente do `Strict`, sem gravar nada. Frase reescrita; teste de contrato `CombatRequests_CtxForaDoStep_Lanca` nos Validation Criteria. | Decisões 1, 3 e 4, Key Interfaces, Implementation Guidelines, Validation Criteria |
| Texto desatualizado (3ª passada, lista do ADR-0005) | Last Verified (Emendas 1 a 20, ADR-0004 `Proposed` com a nota de sincronia aplicada); Summary e Depends On ("exige/precisa receber" a Emenda 18 virou "aplicada"); Ordering Note (o ADR-0006 deixou de ser "independente": depende deste, e a dependência inversa está em Enables); título da Decisão 8 ("pendente" virou aplicada, itens (g) e (h) feitos); Pendências abertas e Migration Plan sem a nota de sincronia e o registro (já feitos); GDD Sync sem o ADR-0004 e o registro como pendentes; Related (ADR-0006 escrito); `HitFlags.Suprema = 8` na declaração de Key Interfaces (a tabela da Decisão 2 já o tinha). Conferido contra o texto atual; nenhuma outra frase "pendente/precisa receber" ficou além das do GDD Sync (os GDDs seguem sem edição: `PedirRugido` e `HordeTick` ainda não aparecem em `design/gdd/`). | Last Verified, Summary, ADR Dependencies, Decisão 8, Key Interfaces, Risks, Migration Plan, GDD Sync, Related |

**Nomes novos que os outros ADRs precisam citar:** `SimContext.InStep` (ADR-0001, Key Interfaces); `QueueCapacity` e `EventCapacity` do `PhaseSnapshot` como capacidades finais (ADR-0002 já os tem em §4); nenhum nome novo no ADR-0006.

**Pendências para outros ADRs:** ~~ADR-0001 deve declarar `InStep` em `SimContext`~~ (feito no ADR-0001, Emenda 22a: campo em Key Interfaces, `Tick` monta `true`, construtor `internal`; conferido na rodada 7). Nenhuma pendência para o ADR-0002 (§4 já diz o que esta rodada cita), 0004 (já sincronizado) ou 0006.

**Pendências para os GDDs (itens que esta rodada NÃO trata):** GDD #6 deve alinhar `CurasDescartadas` sem contar alvo morto (Edge Case do #6 × Decisão 5 deste ADR) e `curaAcc` (L69 e F2: a cura só acumula em `curaPendente`); o resto do GDD Sync segue como está.

### Rodada 7 (2026-11-10, noite)
Origem: `architecture-review-2026-11-10-4.md` (8ª passada, conflito [18] e pendências conhecidas do ADR-0005); autorização do usuário ("emendar agora esses itens no mesmo fluxo"). Status segue `Proposed`. Só texto: nenhum contrato muda (fila, ordem, `HitRequest`, `Rugido`, cura, tabela de eventos, fórmula do `EventCapacity`).

| Item | Mudança | Onde |
|------|---------|------|
| [18] quem confere a desigualdade com `R` | "O compositor confere a desigualdade completa, com `R`, ao montar o `Create`" passa a "o `Simulation.Create` confere (ADR-0001 Emenda 22)"; a Decisão 7 também cita o `EventCapacityDataTerms` (só termos de dados, sem `R`), que o baker calcula e o `DataValidator` valida (ADR-0001 Emenda 22; ADR-0002 §4). A linha da rodada 5 acima ganhou o mesmo ajuste. | Decisão 7 (capacidade), tabela da rodada 5 |
| [18] `InStep` "falta" no ADR-0001 | O `SimContext.InStep` JÁ está no ADR-0001 (Emenda 22a: Key Interfaces, `Tick` monta `true`, construtor `internal`, `default` = `false`; conferido em disco). Depends On, Migration Plan e a pendência da rodada 5 deixam de dizer "falta/ainda não". | Depends On, Migration Plan, "Pendências para outros ADRs" |

A linha `Depends On` segue com ADR-0001, ADR-0004 e ADR-0002 (nenhuma menção ao ADR-0006; a dependência inversa fica em Enables).

**Nomes novos que os outros ADRs precisam citar:** nenhum.

**Pendências para outros ADRs:** nenhuma.

### Rodada 8 (2026-11-10, noite)
Origem: `architecture-review-2026-11-10-5.md` (9ª passada, conflito [20]); autorização do usuário ("emendar agora o [19], o [20], o A3 e os ⚪"). Status segue `Proposed`. Só texto e uma exigência de validação: nenhum contrato de fila, ordem, `HitRequest`, `Rugido`, cura ou tabela de eventos muda.

| Item | Mudança | Onde |
|------|---------|------|
| [20] o "+5" do GDD #6 | O "5" de `EventosReservados + 5 + 3 × individuais_máx + 4` (GDD #6, Edge Cases e Tuning Knobs: `event_capacity`) é um piso PROVISÓRIO para `S_max + K + E_3_16`. `S_max + K + E_3_16` substitui o 5 do GDD; o baker EXIGE `S_max + K + E_3_16 ≥ 5` (erro de build se menor) enquanto `K` e `E_3_16` estão `NOT ASSESSED` (= 0). A fórmula do `EventCapacityDataTerms` (ADR-0001) não muda. O ADR-0002 acrescenta a validação ao `DataValidator` e o teste `EventCapacity_PisoDoGdd6_Recusa`. | Decisão 7 (capacidade) |

A linha `Depends On` segue com ADR-0001, ADR-0004 e ADR-0002 (nenhuma menção ao ADR-0006).

**Nomes novos que os outros ADRs precisam citar:** nenhum (o ADR-0002 já recebe o critério `EventCapacity_PisoDoGdd6_Recusa`).

**Pendências para outros ADRs:** ADR-0002: validação `S_max + K + E_3_16 ≥ 5` no `DataValidator` e o teste `EventCapacity_PisoDoGdd6_Recusa` (dono: ADR-0002, na mesma rodada).

**Pendências para os GDDs:** GDD #6 (Edge Cases, "buffer de eventos precisa de espaço", e Tuning Knobs, `event_capacity`) deve sincronizar a redação: "o 5 é `S_max + K + E_3_16`, com piso 5". Não editado aqui.
