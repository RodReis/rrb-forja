# ADR-0001: Simulação de combate determinística (#2): float32 em C# puro, tick fixo de 30 Hz, PCG32 com streams e interface por Tick + buffer de eventos

## Status
Proposed

## Date
2026-11-03 (emendado em 2026-11-05, em duas levas, e em 2026-11-06, Emendas 17 e 18; ver a seção Emendas)

## Last Verified
2026-11-06 (contra Unity 6.3 LTS, pin 6000.3.x, `design/gdd/game-concept.md` congelado, os GDDs #1, #2, #3, #6, #7 e #28 em disco e os ADRs 0004 e 0005)

## Decision Makers
Rodrigo Reis (decisão de projeto, as quatro escolhas abaixo confirmadas em 2026-11-03), Claude Code (autoria), `unity-specialist` (validação de API, 5.5) e `technical-director` (gate TD-ADR, 5.6). Os resultados das duas revisões entram na seção Risks e no log deste ADR antes de gravar. **Emendas de 2026-11-05:** Rodrigo Reis (decisões dos GDDs #2 e #3), Claude Code (autoria), `unity-specialist` (5.5) e `technical-director` (5.6); os resultados das revisões das emendas entram na seção Risks.

## Summary
A simulação de combate (#2) precisa de um tipo numérico, de uma taxa de tick e de um gerador aleatório decididos antes dos GDDs #6 Combate, #7 Horda e #8 Skills, porque cada fórmula desses GDDs herda a escolha. Decidido: simulação em `float` (32 bits) em C# puro, sem referência à engine, com tick fixo de 30 Hz, PRNG próprio PCG32 com streams independentes, e uma interface em que a apresentação chama `Tick(comandos)` e lê um buffer de eventos; a reprodutibilidade garantida é a do mesmo build, e o ponto fixo fica como substituição futura registrada. **Emendas de 2026-11-05:** os GDDs #2 e #3 fixaram o que a interface precisa carregar além disso: criação da instância por fábrica com snapshot e modo estrito, estados da simulação, pedido de fim com motivo, combate retido (`CombatHold` e `CombatTick`), a marca `Essencial`, a ficha de fase do #3 e as interfaces de início e de fim de fase chamadas pelo compositor fora do tick. A seção Emendas lista cada item e o GDD de origem. A segunda leva de emendas de 2026-11-05 (15 e 16) acrescenta a causa de morte `Rugido` e o gerador da wave disponível no `Preparar`, pedidos pelos GDDs #6 e #7. **A terceira leva, de 2026-11-06 (17 e 18),** vem dos ADRs 0004 e 0005: `Spawn` com classe e arquétipo, hash do Core com as colunas novas, três formas de canal direto entre sistemas e um contrato de eventos em que `Kill` e `Spawn` do Core não emitem e quem decide emite.

## Engine Compatibility

| Field | Value |
|-------|-------|
| **Engine** | Unity 6.3 LTS (6000.3.x; editor instalado 6000.3.27f1) |
| **Domain** | Core |
| **Layer** | Core |
| **Knowledge Risk** | HIGH (`docs/engine-reference/unity/VERSION.md`) |
| **References Consulted** | `docs/engine-reference/unity/VERSION.md`, `current-best-practices.md`, `deprecated-apis.md`, `breaking-changes.md`; `design/gdd/game-concept.md` (L246, L323, L326, L349, L400); `design/gdd/systems-index.md`; `design/gdd/simulacao-deterministica.md`, `fluxo-de-fase.md`, `dados-e-balanceamento.md` e `save-local.md`. **Não existe `docs/engine-reference/unity/modules/core.md`**: nada do domínio Core foi checado contra um módulo de referência (`NOT SOURCEABLE`) |
| **Post-Cutoff APIs Used** | Nenhuma API da Unity dentro da simulação. As APIs de BCL (`Span<T>`, `ref struct`, `BitConverter`, `MathF`) são anteriores ao cutoff, mas a disponibilidade delas no perfil de API do projeto é `NOT SOURCEABLE` e fica para o spike. O código da simulação usa só C# 9 (`System`, `System.Runtime.CompilerServices`, `Span<T>`) e a opção de asmdef "No Engine References". Nenhuma API Unity 6 é necessária dentro da simulação; a ponte com a apresentação (MonoBehaviour que acumula tempo e chama `Tick`) usa APIs antigas e estáveis. |
| **Verification Required** | (1) Spike de hash entre runtimes: mesma seed e mesmo fluxo de comandos gravado, hash do estado a cada N ticks, rodando no Editor (Mono, x64), em build Windows IL2CPP e em Android IL2CPP ARM64; comparar. Hoje `NOT SOURCEABLE`: determinismo de float entre Mono, IL2CPP e ARM64 não está coberto por `docs/engine-reference/unity/`. (2) Confirmar no aparelho que o IL2CPP ARM64 não funde `a*b+c` em FMA de modo que mude o resultado entre execuções do mesmo build (esperado estável no mesmo build; o spike (1) mostra). (3) Profiler: zero alocação gerenciada por `Tick` em regime. (4) Confirmar no 6000.3.27f1 que a opção "No Engine References" do asmdef existe e falha a compilação ao usar `UnityEngine` (`NOT SOURCEABLE`: `docs/engine-reference/unity/` não a cobre), e que `ref struct` + `ReadOnlySpan<T>` + interface compilam e rodam no asmdef sem engine, no Editor (Mono) e em IL2CPP. (5) O spike (1) roda em build **Release** (IL2CPP, stripping ligado), não só Debug. (6) `BitConverter.SingleToInt32Bits` existe e dá os mesmos bits no Mono e no IL2CPP (senão o plano B é uma struct com `FieldOffset`); `NOT SOURCEABLE`. (7) A configuração do IL2CPP (modo Release ou Debug, nível de stripping, compilador) entra na tag do build gravada no log; quais campos a tag deve levar é `NOT SOURCEABLE` e fica para o spike. (8) Os callbacks de pausa e foco da engine chegam na thread principal, entre frames, nunca no meio de um `Tick`; `NOT SOURCEABLE` (hipótese (e) do #2 e OQ-9 A do #3). (9) O custo de `Simulation.Create` e do `Preparar` (inclusive a composição inteira das waves do #7) no aparelho de referência (tempo e bytes alocados) e a igualdade do hash com buffers novos ou reusados. |

## ADR Dependencies

| Field | Value |
|-------|-------|
| **Depends On** | None (varredura conclusiva: não existe outro ADR em `docs/architecture/` e `docs/registry/architecture.yaml` está vazio) |
| **Enables** | GDDs #6 Combate e dano, #7 Horda/waves/inimigos e #8 Skills e evoluções (unidades de tempo em ticks, fórmulas em float32, ordem de sistemas). ADR futuro de replay e validação de ranking (#22) e de auto-battle (#40), que podem substituir este ADR pelo ponto fixo. GDD #3 Fluxo de fase e GDD #16 Grimório (contrato de ciclo de vida da fase: `IPreparaFase`, `IConcluiFase` e a ficha de fase). |
| **Blocks** | Épicos de #2 Simulação, #3 Fluxo de fase e #5 Log de eventos e instrumentação; qualquer story de #6, #7 e #8 que escreva fórmula com unidade de tempo. Nenhuma story existe ainda, então nenhuma está `Blocked` hoje. |
| **Ordering Note** | Deve ser Accepted antes de `/design-system` de #6. A tabela de ordem de implementação do índice põe #2 logo depois de #28 Save local. O spike de hash entre runtimes (Verification Required 1) roda junto do spike de performance já previsto antes do vertical slice; ele não condiciona a aceitação, mas um resultado de divergência no mesmo build reabre este ADR. As emendas de 2026-11-05 fecham os itens da OQ-5 do #2 e a OQ-2 do #3; a aceitação (`accept ADR-0001`) ainda depende da revisão independente dos GDDs #2 e #3 e continua não condicionada ao spike de hash. |

## Context

### Problem Statement
O conceito exige tick fixo, RNG com seed e lógica de combate sem MonoBehaviour (L326), e uma simulação headless que chama o mesmo código do jogo para medir oferta, registro e substituição do Grimório (L400). Ele também deixa a escolha entre float e inteiro ou ponto fixo para este ADR, porque só o inteiro ou o ponto fixo viabilizaria replay validado por servidor, ranking por replay e autoridade de host no futuro (L326). Os GDDs #6, #7 e #8 vão definir fórmulas, durações, cooldowns e taxas de spawn; se o tipo numérico e a unidade de tempo mudarem depois deles, toda fórmula é reescrita. A decisão precisa vir agora.

### Constraints
- Dev solo, MVP dentro de 13 a 20 meses; custo de código e de depuração pesa mais que o ganho teórico de determinismo que o MVP não usa.
- Android primeiro, aparelho de referência ainda não verificado; horda grande em CPU móvel: sem alocação por tick e custo do tick na ordem de poucos milissegundos.
- C# 9 no Unity 6.3; Burst só aceita tipos blittable; determinismo de `Unity.Mathematics` e semântica de float sob Burst são `NOT SOURCEABLE`.
- No MVP basta reprodutibilidade no mesmo build. Replay, validação cross-device e ranking por replay são pós-lançamento (#22 Alpha, #40 Full Vision).
- Valores de gameplay vêm de dados externos, nunca fixos no código (`.claude/docs/coding-standards.md`); isto vale para o tick: a taxa é a única constante de simulação.
- Rules de `Assets/**/Core/**`: zero alocação nos caminhos quentes.

### Requirements
- Mesma `seed` e mesmo fluxo de comandos por tick produzem o mesmo estado, tick a tick, no mesmo build.
- RNG com streams independentes (spawn, oferta, loot): consumir um sorteio num stream nunca desloca outro.
- Lógica sem MonoBehaviour e sem `UnityEngine`; a simulação roda headless em teste EditMode chamando o mesmo código do jogo.
- O auto-battle (#40, Full Vision) e o teste headless rodam a mesma simulação, com comandos vindos de uma política em vez do jogador. A Varredura (#15) credita a recompensa sem simular a fase (`systems-index.md`) e não usa este ADR.
- Apresentação nunca escreve no estado da simulação; a simulação nunca chama a apresentação.

## Decision

### Numérico
A simulação usa **`float` (System.Single)** como único tipo fracionário. `double` e `decimal` ficam fora do estado da simulação. Os tipos de vetor da simulação são próprios (`SimVec2` ou equivalente, definido pelo ADR de #6 conforme os eixos do combate), e **toda operação além de `+ - * /` e comparação passa por `SimMath`**: `Sqrt`, `Abs`, `Min`, `Max`, `Clamp`, `Lerp`. Os corpos de `Clamp`, `Min` e `Max` são por comparação (`Clamp(x, lo, hi) = x < lo ? lo : (x > hi ? hi : x)`, `Min = a < b ? a : b`, `Max = a > b ? a : b`): não lançam e deixam o NaN atravessar; `Math.Clamp`, `Math.Min/Max` e `MathF.Min/Max` não entram na simulação (ADR-0006). Funções transcendentais (`Sin`, `Cos`, `Atan2`, `Pow`, `Exp`, `Log`) **não entram** no estado da simulação; quando uma fórmula as pedir, usar tabela pré-computada e versionada, ou trocar a fórmula. `Unity.Mathematics`, `UnityEngine.Mathf` e `Vector3` ficam fora do código da simulação (determinismo de `Unity.Mathematics` é `NOT SOURCEABLE`; `Mathf` e `Vector3` exigem `UnityEngine`).

**"Mesmo build" neste ADR significa mesmo binário e mesma ABI** (mesmo código IL2CPP gerado para a mesma arquitetura). Um APK com `armeabi-v7a` e `arm64-v8a` tem dois caminhos de código e não se compara entre eles. Consequência: o resultado de um auto-battle (#40) é calculado e creditado de uma vez, e **nunca é derivado de novo da seed depois de um update do app**, porque um build novo pode mudar o resultado.

Escolha e custo: o float dá reprodutibilidade no mesmo build (o que o MVP exige) pelo menor custo de código nos GDDs #6, #7 e #8, mas não garante o mesmo resultado entre runtimes diferentes (Editor Mono x64, IL2CPP ARM64). `SimMath` e o vetor próprio são o ponto único por onde uma troca futura para ponto fixo passa, mas a troca ainda toca toda fórmula; ela não é gratuita.

### Tempo
`SimClock.TicksPerSecond = 30` e `SimClock.TickSeconds = 1f / 30f` são constantes de compilação. A simulação nunca lê `Time`, relógio de parede nem frame. **Os GDDs e os dados escrevem tempo em segundos; a simulação trabalha em ticks inteiros.** **No build** (ADR-0002, `Forja.Data`, uma única vez; a simulação nunca converte): durações e cooldowns viram ticks por **arredondamento ao inteiro mais próximo (`floor(s × 30 + 0,5)`), e o que der menos de 1 tick é recusado** (não `ceil`, que é frágil em float: `0,1 × 30` pode dar `3,0000x` e virar 4 ticks); taxas por segundo (velocidade, DPS, regeneração) viram taxas por tick **dividindo em `decimal` (r ÷ 30) e convertendo uma só vez para `float`** no build (ADR-0002), em vez de multiplicar por `SimClock.TickSeconds` (dois arredondamentos). Janelas curtas (i-frames, telegraph) podem ser escritas direto em ticks nos dados. Um valor de dado que resulte em menos de 1 tick é recusado na validação dos dados. A apresentação acumula tempo real e executa `N` ticks por frame, limitada por `MaxTicksPerFrame` (valor inicial 4, botão de ajuste a medir no aparelho): se o atraso passar do limite, o excedente é descartado e a simulação roda em câmera lenta, o que é determinístico porque o resultado depende só da sequência de ticks e de comandos, nunca do tempo de parede. A renderização interpola entre o estado anterior e o atual; **quem guarda o estado anterior é a simulação** (o `SimWorld` mantém a posição do tick anterior), a apresentação só lê. A ponte e o log (#5) **drenam os eventos depois de cada `Tick`**, não uma vez por frame, porque com até `MaxTicksPerFrame` ticks por frame o buffer só vale até o próximo `Tick`.

### Aleatoriedade
O PRNG é **PCG32** (estado de 64 bits, saída de 32 bits) implementado em C# puro, na simulação. `UnityEngine.Random` e `System.Random` são proibidos em todo código chamado pela simulação ou pelo código de oferta do Grimório. Cada stream é uma instância `Pcg32` inicializada com a seed `SplitMix64(seedMestre ^ idDoStream)` e com o id como sequência (incremento) do PCG32: o incremento sozinho deixaria streams de mesma seed correlacionados. Streams iniciais: `Spawn`, `Offer`, `Loot`. Criar um stream novo exige um novo id fixo e uma entrada no registro. **Regra para o GDD #7:** o `Spawn` sorteia por índice de wave (subsequência derivada de `(seedMestre, índiceDaWave)` ou número fixo de sorteios por wave), nunca por tick; senão o ritmo de abate desloca a sequência e a comparação Tank × DPS na mesma seed (systems-index #2) deixa de ver a mesma composição de waves. Sorteios limitados usam o método de rejeição (sem viés de módulo) e o float em `[0,1)` é `(saída >> 8) * (1f / 16777216f)`, que é exato em float32. Nenhuma estrutura de iteração não ordenada (`Dictionary`, `HashSet`) pode ser percorrida para decidir ordem de efeito; a iteração é sempre por índice crescente.

### Interface
A simulação é uma classe de C# puro. **Três asmdefs**, para que o teste headless e o jogo montem exatamente a mesma lista de sistemas (L400):
- `Forja.Simulation` (Core, "No Engine References", `Assets/Scripts/Core/Simulation/`): relógio de ticks, streams, `SimWorld`, buffers de comandos e de eventos, `ISimSystem`.
- `Forja.Gameplay.Sim` (sem engine, `Assets/Scripts/Gameplay/Sim/`): os sistemas de regra (#3 Fluxo de fase, #6 Combate, #7 Horda, #8 Skills, a oferta do Grimório #16, …) e o **compositor**, que fixa a ordem dos sistemas. O jogo e o teste headless chamam o mesmo compositor.
- `Forja.Gameplay` (com Unity, `Assets/Scripts/Gameplay/`): o carregador do snapshot de dados gerado no build (ADR-0002; a conversão de segundos para ticks e a validação não acontecem aqui), a ponte (acumulador de tempo, drenagem de eventos, interpolação) e a apresentação.

A dependência vai sempre de Gameplay para Core. A ordem de execução dos sistemas dentro do tick é a ordem de registro no compositor, fixa e documentada.

**Estado compartilhado: `SimWorld` mínimo em Core.** Tabela de entidades com arrays pré-alocados (SoA): id, posição atual e posição do tick anterior, facção, HP e flag de vivo, com capacidade fixada no início da fase a partir dos dados da fase. **IDs são monotônicos por fase e nunca reutilizados**, de modo que um `ActorId` num evento lido pela apresentação nunca aponta para outra entidade depois de uma morte (handle com geração só entra se o pool exigir, e isso é uma mudança de ADR). Os sistemas leem e escrevem esses campos pelo mesmo contrato; dado extra de um sistema (cooldowns, estados de skill) fica no sistema, indexado pelo índice da entidade. O ADR do #6 e do #7 pode acrescentar colunas ao `SimWorld`, nunca outra tabela de entidades (o ADR-0004 acrescenta `classe`, `arquetipoId`, `tickNascimento` e `hpMax` e põe o estado de combate em tabelas do #6; Emenda 17).

**Eventos são só saída.** O `EventBuffer` serve à apresentação e ao log (#5); **não é barramento entre sistemas**. A comunicação interna do tick passa pelo `SimWorld`, para que ordem de assinatura nunca vire regra, com a exceção estreita da Emenda 18: três formas de canal direto (fila de pedidos do consumidor, acumulador hasheado do dono e vista só de leitura), entregues pelo compositor por referência, sem `static`, sem reflexão e nunca por evento. A capacidade do buffer vem dos dados da fase; se encher, a simulação incrementa `DroppedEvents` e **nunca descarta em silêncio**: em desenvolvimento o teste e o host falham quando o contador é diferente de zero, em release o contador vai para o log (#5).

**#3 e a oferta do Grimório (#16) são `ISimSystem`.** Eles rodam dentro do `Step`, na ordem do compositor, e sorteiam do stream `Offer` pelo contexto; o teste headless chama o mesmo código de oferta, registro e substituição do jogo. O #3 tem **duas metades**: o `SistemaFluxoDeFase` é um `ISimSystem` (fim da fase, XP, nível, entrada do chefe), e a `TentativaDeFase` (entrar na fase, seed, criação da simulação, pausa, abandono, encerramento e retry) é C# puro em `Forja.Gameplay.Sim` que **não** é `ISimSystem`: ela roda entre frames, chamada pelo host, e fica fora do hash (GDD #3, Regra 2).

Fluxo de um tick: a apresentação (ou a política de auto-battle, ou o teste headless) chama `Tick(comandos)`; a simulação limpa o buffer de eventos, executa cada sistema em ordem, que lê comandos e o `SimWorld`, sorteia dos streams e escreve eventos; a ponte e o log drenam os eventos e a apresentação lê as visões somente leitura. O `Hash` de cada sistema e o do `SimWorld` compõem o hash global usado em testes. A política do auto-battle (#40) obedece às mesmas regras da simulação (float, sem `System.Random`, sem `UnityEngine`).

### Emendas de 2026-11-05 ao contrato

Estas decisões vêm dos GDDs #2 (OQ-5) e #3 (OQ-2). Onde o GDD marca a regra como *(provisória)*, ela fica provisória aqui e entra na reavaliação (OQ-13 do #2 e OQ-10 do #3).

1. **Criação por fábrica.** `Simulation.Create(snapshot, logHeaderDataHash, masterSeed, systems, strict)` substitui o construtor. O `Create` confere o snapshot e compara o hash dele com o do cabeçalho do log; se divergir, lança exceção e a simulação não existe. O `SimWorld` e o `EventBuffer` são dimensionados pelas capacidades do snapshot. Cada stream nasce de `SplitMix64(seedMestre ^ idDoStream)`, com o id como sequência do PCG32. O `Create` é fábrica estática **sem campo estático**, e `strict` é opção da instância, nunca `#if` nem `static`. O tipo do snapshot é do ADR-0002: o Core só lê as capacidades e o hash (`IPhaseSnapshot`).
2. **Estados.** `Created`, `Running`, `Ended`, `Broken` e `Destroyed`. `Tick` depois de `Ended`, `Tick` reentrante, `Tick` com o buffer de eventos não drenado (o buffer conta como drenado depois que o host chama `DrainEvents()`; a propriedade `Events` é só leitura, sem efeito) e leitura de `Events` ou `StateHash` durante o `Tick` são **erros do host** e lançam nos dois modos; `StateHash` lança também em `Broken` e `Destroyed`. Qualquer exceção lançada depois que o `Tick` começou a mudar estado leva a `Broken`; uma exceção antes (argumento inválido, snapshot recusado) deixa a simulação intacta. O host descarta a instância com `Discard()` (abandono pelo menu, ou depois do fim): estado `Destroyed`.
3. **Ordem do tick.** (1) valida os comandos; (2) `CurrentTick += 1`, tira a foto `CombatActive = (CombatHold == 0)` e, se ativa, `CombatTick += 1`; (3) limpa o `EventBuffer` e a lista de mortos do tick; (4) copia a posição atual para a anterior; (5) roda cada sistema na ordem do compositor; (6) confere se posição e HP das entidades vivas são finitos; (7) verifica o pedido de fim; depois compacta a lista de vivos. O `Tick` nunca calcula hash, nunca lê relógio nem frame e não aloca memória gerenciada.
4. **Comandos.** `Command` leva `ActorId`, `Kind`, `X`, `Y`, `ArgA` e `ArgB` (os dois inteiros só valem no tipo que os usa). `CommandKind` ganha `PickOffer` (`ArgA` = serial da oferta, `ArgB` = índice da carta; **quem valida o serial é o #16**). Comando para ator nunca emitido, duplicado do mesmo ator e tipo no tick, ou com eixo não finito ou acima de `EixoMax` é descartado e contado em `CommandsRejected` no modo não estrito e **lança no estrito**. Comando **fora da ordem** (`ActorId` crescente e depois tipo) lança no estrito e, no não estrito, é processado como veio, **sem contador** (a ordem recebida faz parte da entrada reproduzível; Regra 3 do #2). `PickOffer` com serial errado nunca lança. Comando para ator já morto é descartado e contado, sem falha. Comandos valem só no tick em que chegam.
5. **Combate retido e relógio.** O `SimWorld` tem o escalar `CombatHold` (0 livre, 1 oferta pendente, 2 aguardando retomada), **escrito só pelo #16** e incluído no hash. `ctx.CombatActive` é a foto do tick inteiro, e os sistemas de combate não fazem nada quando é falsa. `ctx.CombatTick` só avança nos ticks com `CombatActive`: waves, recargas e duração da fase usam o `CombatTick`, e o `CurrentTick` serve ao log, ao número do evento e ao hash.
6. **Entidades.** O id é o índice na tabela, nunca reutilizado, e a capacidade da tabela cobre o **total de spawns da fase** (soma de `ids_de_preparacao`, das waves e das invocações). O `SimWorld` mantém a lista dos vivos em ordem de id. `Spawn(faction, essential, xpValue, hp, x, y, entityClass, archetypeId)` inicia a linha inteira de uma vez (posição anterior igual à atual, para não interpolar a partir de (0,0); `tickNascimento` e `hpMax` são carimbados pelo `SimWorld`, e `entityClass` `None`, `archetypeId` negativo ou `hp` não finito ou ≤ 0 lançam nos dois modos, Emenda 17) e devolve −1 e incrementa `SpawnsRejected` quando a tabela enche (lança no estrito). Em `Created` (no `Preparar`), um `Spawn` `essential` rejeitado **lança** nos dois modos; dentro do tick, todo `Spawn` `essential` rejeitado é inimigo (o herói só nasce no `Preparar`) e a simulação encerra com `InternalFailure` (detalhe `EssentialSpawnRejected`) no mesmo tick, que o #3 traduz em `ChefeAusente` no resultado *(provisória: escolha deste ADR, Alternative 9; o GDD #3 pediu o motivo `ChefeAusente` ao #2)*. `ids_de_preparacao` é a soma do que cada `IPreparaFase` declara em `IdsDePreparacao` (o #3 declara 1, constante de código), calculada pelo compositor **antes** do `Create`. Nesse mesmo ponto o compositor confere que a tabela cobre o total: `(ids_de_preparacao + SpawnsDeDados) × (100 + CapacityMarginPct) ≤ EntityCapacity × 100`, em inteiro de 64 bits, com `SpawnsDeDados` e `CapacityMarginPct` lidos do snapshot (ADR-0002). Se não cobrir, a simulação não é criada e o #3 monta `FalhaInterna(DadosInvalidos)` com hash "indisponível" (o mesmo caminho da falha do `Preparar`; não é do Core). O `DataValidator` do build confere só a parte de dados (GDD #1, F3); este passo cobre o termo de código *(provisória, a reavaliar: a conferência fica no compositor para o Core continuar sem conhecer o #3)*. A coluna `Essencial` (1 bit, no hash) é escrita por quem cria a entidade. Uma morte só marca a flag de vivo; ids novos só agem a partir do sistema seguinte; a lista de vivos é compactada no fim do tick. O `Spawn` acrescenta o id ao fim de `Alive` na hora (a lista segue em ordem de id), então uma consulta de outro sistema, no mesmo tick, vê quem nasceu antes dele (ADR-0006). Toda morte passa por `SimWorld.Kill(id, causa)`, chamado só pelo #6 (e pelo Core no caminho do NaN), que marca e anota o id e a causa na **lista de mortos do tick**, **sem emitir evento** (quem decide emite, Emenda 18) (ordem crescente de id, limpa em todo tick) e **mantém a primeira causa**: `Kill` sobre entidade já morta no mesmo tick é ignorado e não muda a causa; o `xpValue` inteiro é escrito pelo #7 no `Spawn`. *(provisória; `Kill` só pelo #6 e `xpValue` no `Spawn` e no hash, Emendas 17 e 18.)*
7. **Fim da fase.** Um sistema pede o fim com `ctx.RequestEnd(kind, detail)`, em que `kind` é `Victory`, `Defeat` ou `InternalFailure`; a simulação vira `Ended` ao fim desse tick e o log recebe o hash final. Prioridade no mesmo tick: `InternalFailure` > `Victory` > `Defeat`. Valor não finito num `Essencial` (passo 6) encerra com `InternalFailure` e **ignora** o pedido de fim do tick; o `InternalFailure` que o #3 pede (`MissingBoss`) segue a mesma prioridade. **Dado inválido não é do tick**: o #3 valida os knobs no `Preparar`, por exceção (GDD #3, Regra 14). Os sistemas leem o pedido pendente por `ctx.PendingEnd` e `ctx.PendingEndDetail` (somente leitura: o #3 pula XP e o #16 não abre oferta quando há pedido), e o host lê `Simulation.End` e `Simulation.EndDetail` depois de `Ended`. O abandono pelo menu não passa por tick: o host chama `Discard()`.
8. **Valores inválidos.** NaN ou infinito: o modo estrito lança com tick e entidade; o modo não estrito conta em `NonFiniteCount`, a entidade morre sem XP nem loot e a posição é regravada com a anterior (NaN nunca entra no hash). Conversão de `float` para inteiro só por `SimMath.RoundToInt` (o meio arredonda para longe de zero) e `SimMath.FloorToInt`, com checagem de faixa (fora da faixa do `int`, NaN ou infinito é bug interno e lança).
9. **Regra única de modo.** Todo contador de diagnóstico (`CommandsRejected`, `SpawnsRejected`, `NonFiniteCount`, `DroppedEvents`) lança no primeiro caso em modo estrito e só conta em modo não estrito. Um script sem erro dá o mesmo hash nos dois modos.
10. **Eventos reservados.** `EventosReservados` (de 8 a 16 posições, constante) é reservada a eventos críticos, **por tipo e nunca por conteúdo** (`HeroDeath`, fim de fase, oferta, `TelegraphStart`; Emenda 18): não são descartados enquanto houver reserva. Descartar evento nunca altera o estado.
11. **Aleatoriedade por wave.** `SimWorld.RngWave(w)` (Emenda 16) devolve o gerador da wave, derivado como na FS6 do #2: `base = Mix(seedMestre XOR 0)` (a semente do stream `Spawn`, guardada como `waveBase`), `seed_w = Mix(base XOR (ulong)w)` e `Pcg32(seed_w, seq = w)` *(provisória)*; `ctx.RngWave(w)` só delega. O stream `Spawn` vira só a raiz da derivação, `w` negativo é bug interno e lança, e se os sorteios cruzam ticks o gerador fica no estado do sistema e no `Hash` dele (o `RngWave` devolve uma struct por valor: guardar em variável local). O #7 não precisa disso, porque sorteia tudo no `Preparar` (Emenda 16).
12. **Hash.** FNV-1a de 64 bits, por byte (não por palavra), com `-0` normalizado para `+0`. Entram `CurrentTick`, `CombatTick`, `CombatHold`, o contador de ids, os três streams, por todo id < `IdCount`, vivo ou morto (vivo, facção, `Essencial`, HP, x, y, `xpValue`, `classe`, `arquetipoId`, `tickNascimento`, `hpMax`; Emenda 17) e o `Hash` de cada sistema na ordem do compositor. Não entram a posição anterior, o `EventBuffer`, os contadores de diagnóstico, o snapshot, as capacidades, a `waveBase` guardada, a lista de mortos do tick (com a causa) nem a tabela de composição do #7. O hash nunca é calculado dentro do `Tick`.
13. **Ficha de fase do #3.** Um bloco de escalares no `SimWorld` (`PhaseSheet`), **escrito só pelo #3 e lido por qualquer sistema**, como o `CombatHold`: estado dentro do tick (`EmCombate` ou `FimPedido`), nível, XP, `NiveisGanhos` (só cresce), `ChefeVisto`, `TickDeEntradaDoChefe`, `ChefeVencido`, `MorteSimultanea`, `IdDoHeroi`, `ProximoIdAVer`, `IdDoChefe`, `EssenciaisInimigosVivos` e o pedido de fim com motivo e tick. Ela entra no hash **pelo `Hash` do próprio sistema #3**, que já entra na ordem do compositor, então a ordem do item 12 não muda. Os campos exatos e o domínio de cada um pertencem ao GDD #3; mudar um campo atualiza o struct `PhaseSheet` deste ADR, sem novo gate quando a mudança não altera o contrato (quem escreve, quem lê, onde entra no hash).
14. **Ciclo de vida da fase pelo compositor.** Duas interfaces **opcionais** em `Forja.Gameplay.Sim`. `IPreparaFase.Preparar(world)` é chamada pelo compositor logo depois do `Create` e **antes do 1º `Tick`**, na ordem do compositor com o #3 primeiro: ele cria o herói por `Spawn`, escreve `Essencial` e declara `ids_de_preparacao` = 1. `IConcluiFase.Concluir(resultado)` é chamada pelo compositor **depois do último `Tick` (ou do abandono, da falha do `Preparar` ou de `Broken`) e antes do `Discard` e do commit de fim**, em toda causa e com a causa no resultado (cada implementador filtra o que lhe interessa). Durante `Preparar` (estado `Created`) o #3 cria o herói por `Spawn` (HP e posição do snapshot) e grava `IdDoHeroi` na ficha: essas duas escritas são as **únicas permitidas fora do `Tick`** (mais a leitura pura de `RngWave`, que o #7 usa no `Preparar`, Emenda 16), e o `Spawn` de `Preparar` **não emite evento**. `Spawn`, `PhaseForWrite` e `RngWave` aceitam só o estado `Created` ou o `Tick`; `Kill` e o `set` de `CombatHold` aceitam só o `Tick`; todos lançam nos demais estados. Se o `Preparar` lançar, a simulação **não** passa a `Running`: o host chama `Discard()` e o resultado é `FalhaInterna(DadosInvalidos)` com hash "indisponível", montado pelo #3 no `PhaseResult` (não é do Core). O compositor só chama quem implementa a interface, então o teste sem tela monta o mesmo caminho do jogo.
15. **Causa de morte `Rugido`.** `DeathCause` ganha `Rugido = 2` (valores explícitos, só cresce no final; o valor vai para o log). Quem chama `Kill(id, DeathCause.Rugido)` é o #6, ao resolver o pedido tipado `Rugido` do #7 (GDD #6, Regras 3 e 11; GDD #7, Regra 10.2). **A primeira causa vence** (Emenda 6): no nível do Core é o "primeiro pedido que zera o HP" da F2 do #6. A causa fica só na lista de mortos do tick (`DeathsThisTick`, limpa em todo tick) e **fora do hash do Core**: mudar só a causa de uma morte não muda o `SimWorld` nem o seu hash. **Condição:** todo sistema que age pela causa (#3: metade do XP e limite de um nível; #8: sem efeito de abate; #24: sem loot) **deve refletir o efeito no próprio `Hash`**, e todo `switch` sobre `DeathCause` num consumidor **deve** ter um `default` que lança. O evento `Death` carrega a causa em `ArgA` (Emenda 18): o `Death` individual é do #6 (elite e chefe), o `HeroDeath` é do herói e a horda sai agregada em `HordeTick`; o log (#5) lê a causa do evento. *(provisória)*
16. **Gerador da wave também no `Preparar`.** `RngWave(int waveIndex)` passa a existir em `SimWorld` e é a **única dona da derivação** (Emenda 11); `SimContext.RngWave(w)` só delega a ele. É leitura pura: aceito só em `Created` (dentro do `Preparar`) ou no `Tick`, e lança nos demais estados (`Running` fora do `Tick`, `Ended`, `Broken` e `Destroyed`); a guarda não protege estado, limita o sorteio às fases da simulação (o host e a apresentação nunca sorteiam). `w < 0` lança nos dois modos. **Sem estado:** o `SimWorld` guarda só `waveBase = Mix(seedMestre XOR 0)` (a seed do stream `Spawn`, FS6), `readonly`, gravada pelo `Create` (pelo construtor) antes de qualquer `Preparar` e **fora do hash** (os três streams já entram no hash e refletem a seed); com esse campo não dá para derivar `Offer` nem `Loot`. Cada chamada devolve um gerador novo, sem cache, sem tabela estática e sem campo memoizado, e não consome nem altera nenhum stream. O `Create` e o `RngWave` chamam **a mesma função `Mix`**, para a raiz do `Spawn` e a derivação nunca divergirem. **Só o #7 chama `RngWave` no `Preparar`** (convenção e revisão de código, como `PhaseSheet` e `CombatHold`). O #7 sorteia aí toda a composição das waves (GDD #7, Regra 6): nenhum gerador de wave atravessa ticks, a tabela de composição é derivada da seed e dos dados e **não entra no hash**, e o `Hash` do #7 leva só os cursores. `IdsDePreparacao` do #7 é 0. *(provisória)*
17. **Colunas de combate e horda (ADR-0004).** (a) `Spawn(faction, essential, xpValue, hp, x, y, EntityClass entityClass, int archetypeId)`; o `SimWorld` carimba `tickNascimento` (o `CombatTick` do `Spawn`, 0 no `Preparar`) e `hpMax` (= `hp`); `EntityClass` é `None = 0` (inválido), `Heroi = 1`, `Horda = 2`, `Elite = 3`, `Chefe = 4`, valores explícitos, só cresce no final; (b) o hash (item 12) passa a incluir `xpValue`, `classe`, `arquetipoId`, `tickNascimento` e `hpMax` por id e percorre todo id < `IdCount`; (c) o `SimWorld` expõe `ReadOnlySpan` de comprimento `IdCount` para as colunas-base e as quatro novas, e `HpAndPosForWrite(out hp, out posX, out posY)`, uma chamada por `Tick`, aceita só dentro do `Tick` e só do #6; (d) o `DeathRecord` continua `{Id, Cause}` e a linha de uma entidade morta não é reciclada, ficando legível até o fim da fase; (e) o estado de combate do #6 mora em tabelas do #6 indexadas pelo id, no `Hash` do #6, com uma vista só de leitura (ADR-0004); (f) o registro revê o `write_access` de `entity_table`. *(provisória)*
18. **Pedidos, vistas e eventos de combate (ADR-0005).** (a) exceção estreita ao princípio "a comunicação interna passa pelo `SimWorld`": três formas de canal direto, todas entregues pelo compositor por referência, sem `static`, sem reflexão e nunca por evento: uma fila de pedidos tipada, dona do consumidor, preenchida na ordem do compositor, scratch fora do hash e vazia ao fim do `Step` do dono (`ICombatRequests`); um acumulador hasheado do dono, escrito só pelo código do dono (`curaPendente`, via `Curar`); uma vista só de leitura do estado de outro sistema (`ICombatReadView`, `ICombatModifiers`); (b) `SimWorld.Kill` e `SimWorld.Spawn` não emitem evento; `Kill` só é chamado pelo #6 e pelo Core no caminho do NaN, e quem faz nascer elite, chefe ou invocação individual emite o `Spawn`; (c) `SimEvent` ganha `int ArgA, ArgB`, e `SimEventKind` ganha valores explícitos (`None = 0`, `Damage = 1`, `Death = 2`, `Spawn = 3`, `SkillCast = 4`, `Esquiva = 5`, `Knockback = 6`, `HitStop = 7`, `Rugido = 8`, `HordeTick = 9`, `TelegraphStart = 10`, `HeroDeath = 11`; só cresce no final), com o payload por tipo no ADR-0005; o `Death` carrega a causa em `ArgA` (resolve o "a rever" da Emenda 15); (d) `SimContext` ganha `bool Strict` somente leitura; (e) a reserva `EventosReservados` é por tipo (`HeroDeath`, `TelegraphStart`, fim de fase, oferta); (f) no caminho do NaN do Core a morte entra em `DeathsThisTick` com causa `InvalidValue` e não emite evento; (g) `SimInvariantException : InvalidOperationException` é o tipo lançado por violação de invariante (fila cheia, por exemplo); (h) a horda sai agregada em `HordeTick` (mortes, acertos, dano), nunca um evento por corpo. *(provisória)*

### Architecture Diagram
```
 Forja.Gameplay (Unity)                        Core: Forja.Simulation (sem UnityEngine)
 ┌────────────────────────────────┐             ┌──────────────────────────────────────┐
 │ input → Command[]              │  Tick(cmds) │ Simulation                            │
 │ acumula tempo → N ticks (≤cap) │───────────▶│  ├ SimClock (30 Hz)                   │
 │ drena eventos após CADA Tick   │             │  ├ RngStreams: Spawn / Offer / Loot   │
 │ interpola prev/curr no render  │◀───────────│  ├ SimWorld (entidades, ids, prev pos)│
 │ lê eventos, anima, toca SFX    │ eventos +   │  ├ EventBuffer (só saída)             │
 └────────────────────────────────┘ visões RO   │  └ ISimSystem[] em ordem fixa         │
 Auto-battle (#40) / teste headless              └────────┼───────────────────────────────┘
 = outra fonte de Command[]                                │ registrados pelo compositor
                                                  Forja.Gameplay.Sim (sem engine):
                                                  #3 Fluxo, #6 Combate, #7 Horda, #8 Skills,
                                                  #16 Oferta (dependem de Core; estado e hash próprios)
```

### Key Interfaces
```csharp
namespace Forja.Simulation
{
    /// <summary>Unidade de tempo de toda a simulação e dos GDDs: o tick.</summary>
    public static class SimClock
    {
        public const int TicksPerSecond = 30;
        public const float TickSeconds = 1f / TicksPerSecond;
    }

    public enum CommandKind { Move = 0, Dodge = 1, Ultimate = 2, PickOffer = 3 /* valores explícitos (vão para o log e o hash); só cresce no final; o #9 acrescenta reroll e favorecer */ }

    /// <summary>Entrada de um ator num tick; a simulação só vê comandos, nunca o dispositivo.</summary>
    public readonly struct Command
    {
        public readonly int ActorId;
        public readonly CommandKind Kind;
        public readonly float X, Y;       // eixo do joystick; só vale em Move
        public readonly int ArgA, ArgB;   // PickOffer: serial da oferta e índice da carta; ignorados nos outros tipos
    }

    public enum EntityClass : byte { None = 0, Heroi = 1, Horda = 2, Elite = 3, Chefe = 4 }   // Emenda 17; valores explícitos (hash e log); só cresce no final

    public enum SimEventKind : byte { None = 0, Damage = 1, Death = 2, Spawn = 3, SkillCast = 4, Esquiva = 5, Knockback = 6,
                                      HitStop = 7, Rugido = 8, HordeTick = 9, TelegraphStart = 10, HeroDeath = 11 }   // Emenda 18; payload por tipo no ADR-0005; só cresce no final

    /// <summary>Evento de saída, escrito pela simulação e lido pela apresentação e pelo log (#5).</summary>
    public readonly struct SimEvent
    {
        public readonly int Tick;
        public readonly SimEventKind Kind;  // tabela explícita acima (Emenda 18); só cresce no final
        public readonly int ActorId, TargetId;
        public readonly float Value;
        public readonly int ArgA, ArgB;     // significado por tipo (ADR-0005; Emenda 18)
    }

    /// <summary>PCG32 em C# puro; estado de 64 bits, uma sequência por stream.</summary>
    public struct Pcg32
    {
        public Pcg32(ulong seed, ulong stream);
        public uint NextUInt();
        public int NextInt(int exclusiveMax);   // sem viés de módulo
        public float NextFloat01();             // [0,1), exato em float32
    }

    public enum RngStream { Spawn = 0, Offer = 1, Loot = 2 }

    public enum DeathCause { Normal = 0, InvalidValue = 1, Rugido = 2 /* valores explícitos (vão para o log); só cresce no final; fora do hash */ }
    public readonly struct DeathRecord { public readonly int Id; public readonly DeathCause Cause; }

    public enum EndKind { None = 0, Victory = 1, Defeat = 2, InternalFailure = 3 }
    public enum FailureDetail { None = 0, NonFiniteEssential = 1, EssentialSpawnRejected = 2, MissingBoss = 3 }   // dado inválido não é do tick: o #3 valida no Preparar, por exceção

    public enum PhaseState { InCombat = 0, EndRequested = 1 }   // dentro do tick só estes dois; os demais estados da tentativa vivem fora do tick

    /// <summary>Ficha de fase: escalares escritos só pelo #3 e lidos por qualquer sistema. Campos exatos: GDD #3.</summary>
    public struct PhaseSheet
    {
        public PhaseState State;
        public int Level, Xp, LevelsGained;          // LevelsGained só cresce
        public bool BossSeen, BossBeaten, SimultaneousDeath;
        public int BossEntryCombatTick;              // -1 até o chefe ser visto
        public int HeroId, NextIdToSee, BossId, EnemyEssentialsAlive;
        public EndKind EndRequested; public FailureDetail EndDetail; public int EndTick;
    }

    /// <summary>Tabela de entidades compartilhada (SoA, pré-alocada). Ids monotônicos, nunca reutilizados.</summary>
    public sealed class SimWorld
    {
        public int Spawn(int faction, bool essential, int xpValue, float hp, float x, float y, EntityClass entityClass, int archetypeId); // Emenda 17: carimba tickNascimento e hpMax; não emite evento; inicia a linha inteira (posição anterior = atual); devolve o id novo, ou -1 se cheia (SpawnsRejected++; lança no estrito); aceito só em Created (Preparar) ou dentro do Tick; lança nos demais estados
        public void Kill(int id, DeathCause cause);                     // único caminho de morte, só do #6 (e do Core no caminho do NaN): marca e anota na lista de mortos, sem emitir evento; a primeira causa vence (Kill em entidade já morta no mesmo tick é ignorado); só dentro do Tick, lança nos demais estados
        public Pcg32 RngWave(int waveIndex);   // única dona da derivação (Emenda 11); função pura de waveBase (readonly, gravada pelo Create, fora do hash) e do índice; sem cache nem estado; aceito só em Created (Preparar) ou dentro do Tick; w < 0 lança nos dois modos; lança nos demais estados; não consome nem altera nenhum stream
        public bool IsAlive(int id);
        public bool IsEssential(int id);
        public int CombatHold { get; set; }          // 0 livre, 1 oferta pendente, 2 aguardando retomada; escrito só pelo #16; o set só vale dentro do Tick e lança nos demais estados
        public ref readonly PhaseSheet Phase => ref _phase;   // leitura para todos os sistemas
        public ref PhaseSheet PhaseForWrite();       // só o #3; aceito só em Created (Preparar) ou dentro do Tick; lança nos demais estados
        public int IdCount { get; }                  // ids já emitidos
        public ReadOnlySpan<int> Alive { get; }      // vivos em ordem de id
        public ReadOnlySpan<DeathRecord> DeathsThisTick { get; }   // ordem crescente de id, limpa em todo tick
        // posição atual e do tick anterior, facção, HP, xpValue, classe, arquetipoId, tickNascimento e hpMax por id (Emenda 17); colunas extras só por ADR de #6/#7
        public int EntityCapacity { get; }
        public ReadOnlySpan<float> Hp { get; }   // idem PosX, PosY, PrevPosX, PrevPosY, HpMaxes, Factions, Classes, ArchetypeIds, BirthCombatTicks: comprimento IdCount, ver o ADR-0004
        public void HpAndPosForWrite(out Span<float> hp, out Span<float> posX, out Span<float> posY);   // uma chamada por Tick; só dentro do Tick; só o #6
    }

    /// <summary>Contexto passado a cada sistema durante um tick.</summary>
    public ref struct SimContext
    {
        public int Tick { get; }            // CurrentTick em execução
        public int CombatTick { get; }      // só avança nos ticks com CombatActive
        public bool CombatActive { get; }   // foto do tick inteiro (CombatHold == 0 no início do tick)
        public bool Strict { get; }         // modo estrito da instância (Emenda 18)
        public SimWorld World { get; }
        public ReadOnlySpan<Command> Commands { get; }
        public ref Pcg32 Rng(RngStream stream);
        public Pcg32 RngWave(int waveIndex);                    // delega a World.RngWave(waveIndex)
        public void Emit(in SimEvent e);
        public void RequestEnd(EndKind kind, FailureDetail detail = FailureDetail.None);
        public EndKind PendingEnd { get; }                      // pedido de fim já feito neste tick (somente leitura)
        public FailureDetail PendingEndDetail { get; }
        public void RejectCommand(in Command c);                // #16: PickOffer com serial errado (CommandsRejected, sem falha)
    }

    /// <summary>Uma regra da simulação (combate, horda, skills). Estado próprio, sem UnityEngine.</summary>
    public interface ISimSystem
    {
        void Step(ref SimContext ctx);
        void Hash(ref StateHasher hasher);  // para testes de reprodutibilidade
    }

    /// <summary>Lido pelo Create: só as capacidades e o hash. O tipo do snapshot é do ADR-0002.</summary>
    public interface IPhaseSnapshot { int EntityCapacity { get; } int AliveCapacity { get; } int EventCapacity { get; } ulong ContentHash { get; } }

    public enum SimStatus { Created = 0, Running = 1, Ended = 2, Broken = 3, Destroyed = 4 }

    public sealed class Simulation
    {
        public static Simulation Create(IPhaseSnapshot snapshot, ulong logHeaderDataHash, ulong masterSeed,
                                        ISimSystem[] systemsInExecutionOrder, bool strict);  // lança se o hash do snapshot != logHeaderDataHash
        public SimStatus Status { get; }
        public EndKind End { get; }                      // valor quando Ended
        public FailureDetail EndDetail { get; }          // detalhe da falha, para o #3 traduzir (ex.: EssentialSpawnRejected em ChefeAusente)
        public int CurrentTick { get; }
        public int CombatTick { get; }
        public SimWorld World { get; }
        public int DroppedEvents { get; }                // contadores de diagnóstico: nunca em silêncio
        public int CommandsRejected { get; }
        public int SpawnsRejected { get; }
        public int NonFiniteCount { get; }
        public ReadOnlySpan<SimEvent> Events { get; }    // só leitura, sem efeito colateral; válido até o próximo Tick
        public ReadOnlySpan<SimEvent> DrainEvents();     // devolve os eventos do último Tick e marca o buffer como drenado; chamar após cada Tick
        public void Tick(ReadOnlySpan<Command> commands);
        public ulong StateHash();
        public void Discard();                           // abandono ou depois do fim: Destroyed
    }

    /// <summary>Invariante da simulação violado (fila de pedidos cheia, por exemplo); o Step que a lança leva a Broken (Emenda 18 g).</summary>
    public sealed class SimInvariantException : System.InvalidOperationException { public SimInvariantException(string message) : base(message) { } }
}

namespace Forja.Gameplay.Sim   // sem engine; o compositor só chama quem implementa
{
    public interface IPreparaFase { int IdsDePreparacao { get; } void Preparar(SimWorld world); }   // IdsDePreparacao: constante de código, lida antes do Create; Preparar depois do Create, antes do 1º Tick; Spawn sem evento
    public interface IConcluiFase { void Concluir(in PhaseResult result); }   // depois do último Tick (ou do abandono, da falha do Preparar ou de Broken), antes do Discard; em toda causa
    // PhaseResult (readonly struct: causa, nível final, ChefeVisto, MorteSimultanea, CombatTick final, StateHash final, `attemptId` de 128 bits, ADR-0003): GDD #3
}
```
Os nomes e as assinaturas são o contrato do ADR; campos e enums completos pertencem aos ADRs e GDDs de #3 (`PhaseSheet`, `PhaseResult`), #6, #7 e #8.

### Implementation Guidelines
- O compositor que fixa a ordem dos sistemas **must** viver em `Forja.Gameplay.Sim` (sem engine) e ser o único lugar que monta a lista; o teste headless e o jogo **must never** montar listas próprias. **Must** drenar `Events` depois de cada `Tick` e **must never** ler um `Events` de um tick anterior. Eventos **must never** ser usados como canal entre sistemas dentro do tick (usar o `SimWorld`).
- IDs de entidade **must never** ser reutilizados na mesma fase.
- Dados de tempo **must** vir em segundos (ou em ticks, nas janelas curtas) e ser convertidos **no build** (ADR-0002) com arredondamento ao mais próximo, recusando o que der menos de 1 tick; **must never** usar `ceil` sobre float para isso.
- O código da simulação e de qualquer sistema chamado por `ISimSystem.Step` **must** estar em asmdef com "No Engine References"; **must never** referenciar `UnityEngine`, `MonoBehaviour`, `ScriptableObject` (carregar dados e converter em structs antes da fase), `Time`, `Mathf`, `Vector3` nem `Unity.Mathematics`.
- **Must** usar só `float`; **must never** usar `double` ou `decimal` no estado; **must never** chamar funções transcendentais no estado; **must** passar `Sqrt`, `Abs`, `Min`, `Max`, `Clamp` e `Lerp` por `SimMath`.
- **Must never** usar `UnityEngine.Random` nem `System.Random`; todo sorteio vem de um `RngStream` do contexto; **must never** fazer um sistema compartilhar sorteios de outro stream.
- Sistemas `ISimSystem` **must** ser `class` (nunca `struct`: seriam boxed ao entrar em `ISimSystem[]`); o buffer interno de eventos **must** ser `SimEvent[]` com contador, e `Events` só o expõe como `ReadOnlySpan` em propriedade (span não pode ser campo de classe).
- `Forja.Simulation`, `Forja.Gameplay.Sim` (compositor e sistemas, inclusive o #3) e a ponte **must never** ter estado `static` mutável (tabelas de streams, `SimMath` e tabelas de lookup são imutáveis; vale também para eventos e caches estáticos; `Simulation.Create` é fábrica estática **sem campo estático**): com "Enter Play Mode Options" sem domain reload, estado estático sobreviveria entre execuções. **Must never** registrar sistemas por reflexão (stripping do IL2CPP); registrar por referência direta no compositor.
- Os dados de fase **must** chegar à simulação como o snapshot gerado no build (ADR-0002, `Forja.Data`); o carregador com Unity **must** ficar fora do asmdef da simulação; **must never** haver `ScriptableObject`, parse de texto ou conversão de segundos dentro dele.
- **Must** pré-alocar arrays no início da fase; **must never** alocar memória gerenciada dentro de `Tick` (sem LINQ, sem `new` de classe, sem lambda capturante, sem boxing).
- **Must** iterar por índice crescente; **must never** decidir ordem de efeito iterando `Dictionary` ou `HashSet`.
- **Must** escrever tempo em ticks inteiros dentro da simulação; **must never** acumular tempo em float entre ticks (contagem regressiva em ticks inteiros).
- A apresentação **must** só ler eventos e visões somente leitura; **must never** escrever no estado dos sistemas.
- Todo sistema novo **must** implementar `Hash` e entrar no teste de reprodutibilidade (mesma seed, mesmos comandos, duas execuções, mesmo hash).
- Testes ficam em `Assets/Tests/EditMode/Simulation/` e usam `Assets/Tests/PlayMode/` só para a ponte com a apresentação.
- `Simulation` **must** ser criada só por `Simulation.Create` (construtor não público); o host **must** conferir `Status` e **must never** chamar `Tick` em `Ended`, reentrar no `Tick` nem ler `Events` ou `StateHash` durante o `Tick`.
- O compositor **must** chamar `IPreparaFase.Preparar` antes do 1º `Tick` e `IConcluiFase.Concluir` depois do fim, só em quem implementa a interface; o `Spawn` de `Preparar` **must never** emitir evento; **must never** haver `Spawn` fora do estado `Created` e fora do `Tick`.
- `PhaseSheet` **must** ser escrita só pelo #3 e `CombatHold` só pelo #16; nenhum outro sistema **must** escrever neles (revisão de código e o critério R17 do #3).
- Toda morte **must** passar por `SimWorld.Kill`, e a primeira causa vence; o #3 **must never** conhecer o #16 (a ficha e o `CombatHold` são o único canal). Todo sistema que age pela causa **must** refletir o efeito no próprio `Hash`, e todo `switch` sobre `DeathCause` **must** ter um `default` que lança.
- `SimWorld.Kill` **must** ser chamado só pelo #6 (e pelo Core no caminho do NaN), e `SimWorld.Kill` e `SimWorld.Spawn` **must never** emitir evento; cada evento de regra **must** ser emitido pelo sistema que decide (ADR-0005, Emenda 18).
- As colunas de combate e horda **must** seguir o ADR-0004 (Emenda 17): as quatro compartilhadas só pelo `Spawn`; HP e posição só pelo #6, por `HpAndPosForWrite`; o estado do #6 em tabelas próprias, no `Hash` do #6.
- Os canais diretos entre sistemas **must** ser só as três formas da Emenda 18, entregues pelo compositor por referência; **must never** haver outro, nem por evento, nem por `static`, nem por localizador.
- Todo contador de diagnóstico **must** lançar no primeiro caso em modo estrito e só contar em modo não estrito; **must never** usar `#if` para isso.
- Conversão de `float` para inteiro **must** passar por `SimMath.RoundToInt` ou `SimMath.FloorToInt`, com checagem de faixa; **must never** usar cast direto.
- O hash **must** ser por byte, em ordem little-endian explícita, campo a campo; **must never** hashear memória bruta de struct nem `GetHashCode` de objeto.
- `Simulation` e seus sistemas são **confinados à thread principal** (não são thread-safe; a guarda de reentrada é um `bool` simples); os callbacks de pausa e foco **must** chegar à ponte na thread principal, entre frames (`NOT SOURCEABLE`, Verification Required 8).
- Os streams `Pcg32` **must** viver em array e o retorno de `RngWave` **must** ser guardado em variável local (struct mutável: copiar para campo `readonly` ou para `List<Pcg32>` faz `NextUInt` agir numa cópia, e a sequência repete sem erro). A aritmética de PCG32, SplitMix64 e FNV-1a **must** estar em `unchecked { }` explícito. `RngWave` **must** ser sem estado (**must never** haver cache de gerador por wave, tabela estática ou campo memoizado: seria estado que atravessa ticks fora do hash) e derivar sempre da `waveBase` imutável, nunca do estado corrente de um stream; `Pcg32` **must** ser inicializado só pelo construtor (`default(Pcg32)` tem sequência zero e é degenerado).
- O compositor **must** conferir, antes do `Create`, que `EntityCapacity` cobre `ids_de_preparacao + SpawnsDeDados` com a margem (inteiro de 64 bits) e **must never** criar a simulação se não cobrir; `IdsDePreparacao` **must** ser constante de código, nunca derivada de dado da fase.
- O compositor **must** montar listas tipadas `IPreparaFase[]` e `IConcluiFase[]` por referência direta e **must never** descobrir implementadores por `is`, `as` ou reflexão em runtime; um teste confere que `Preparar` e `Concluir` rodaram para cada implementador. **Must never** haver reflexão, método virtual genérico sobre struct nem genérico criado em runtime (AOT do IL2CPP).
- `Spawn` e `PhaseForWrite` **must** ser guardados por `Status == Created` ou dentro do `Tick`; `Kill` e o `set` de `CombatHold` **must** ser guardados por dentro do `Tick`; todos **must** lançar nos demais estados, e a `Preparar` **must never** receber mais poder do que isso exige. `RngWave` **must** ser guardado por `Created` ou `Tick`, **must** lançar nos demais estados e para `w < 0`, e só o #7 **must** chamá-lo no `Preparar`.
- `PhaseResult` **must** ser `readonly struct`, e `IConcluiFase.Concluir` o recebe por `in`.
- Os asmdefs da simulação **must** ter "Auto Referenced" desligado e **must never** exigir `unsafe`; **must never** usar `static event` nem `[RuntimeInitializeOnLoadMethod]` em `Forja.Simulation`, no compositor ou no #3.
- `Simulation.Create` e o `Preparar` (inclusive a composição inteira das waves do #7) **must** rodar na tela de carregamento (nunca no meio do jogo, para o GC não engasgar) e zerar os buffers reusados, para o hash ser igual; a ponte **must** montar a visão do herói lendo `World` e `Phase.HeroId`, não eventos (o `Spawn` de `Preparar` não emite evento).

## Alternatives Considered

### Alternative 1: Ponto fixo (inteiros, Q-format, intermediários em 64 bits)
- **Description**: Posições, velocidades, dano e tempo em inteiros com formato Q (por exemplo Q16.16), multiplicação com intermediário em `long`, divisão e raiz por rotinas próprias.
- **Pros**: Mesmo resultado em qualquer runtime e arquitetura por construção; viabiliza replay validado por servidor, ranking por replay e auto-battle verificável sem trabalho extra (L326).
- **Cons**: Cada fórmula dos GDDs #6, #7 e #8 vira aritmética manual com risco de overflow e perda de precisão; mais código e mais bug para um dev solo; multiplica o custo dos testes de balanceamento; o ganho só é usado após o lançamento.
- **Rejection Reason**: O MVP só exige reprodutibilidade no mesmo build, e o custo recai antes de qualquer retorno. Fica como substituição registrada, disparada quando #22 ou #40 exigirem verificação entre dispositivos ou servidor.

### Alternative 2: DOTS com Burst e float
- **Description**: Simulação em Entities/Burst/Jobs, componentes blittable, sistemas paralelizados.
- **Pros**: Throughput alto para hordas muito grandes; ECS como modelo.
- **Cons**: Burst só aceita tipos blittable e restringe o C# da lógica; semântica de float sob Burst e determinismo de `Unity.Mathematics` são `NOT SOURCEABLE`; exige o modelo de ECS inteiro na equipe de um; os testes headless precisam do mundo ECS; o risco do Unity 6.3 (HIGH) cresce.
- **Rejection Reason**: Complexidade e risco desproporcionais para um dev solo antes de existir um aparelho de referência medido. Se o spike de performance mostrar que a horda não cabe em C# puro, este ADR é revisto com dado.

### Alternative 3: Tipo escalar próprio (`SimReal`) desde já, como hedge para o ponto fixo
- **Description**: Todo o código da simulação e as fórmulas usam um tipo `SimReal` (struct fino sobre `float` ou alias por arquivo) em vez de `float`; trocar o ponto fixo depois seria trocar a definição do tipo.
- **Pros**: A troca futura para ponto fixo fica quase mecânica no texto das fórmulas; responde de antemão à pergunta de quem lê "a troca ainda toca toda fórmula".
- **Cons**: C# 9 não tem `global using` (alias vale por arquivo); um struct fino adiciona ruído a cada operação e depende de otimização do IL2CPP/Mono para não custar em horda; paga-se o custo de legibilidade de todas as fórmulas por um gatilho (#22, #40) que pode nunca vir; o tipo não resolve overflow, precisão nem a ausência de funções transcendentais, que continuam sendo o trabalho real da troca.
- **Rejection Reason**: O custo é imediato e certo, o benefício é hipotético e parcial. `SimMath` e o vetor próprio já concentram as operações além de `+ - * /`; se o gatilho vier, o ADR de substituição decide se introduz o tipo então.

### Alternative 4: Outras taxas de tick (20 Hz e 60 Hz)
- **Description**: Manter a mesma arquitetura com `TicksPerSecond` de 20 ou 60.
- **Pros**: 20 Hz custa ainda menos CPU em Android; 60 Hz casa com o frame alvo, dispensa interpolação e dá precisão de esquiva e telegraph para o "Massacre com peso".
- **Cons**: 20 Hz põe hit e telegraph em granularidade de 50 ms e arrisca a sensação de combate; 60 Hz dobra o custo da horda no aparelho de referência, que ainda não foi verificado.
- **Rejection Reason**: 30 Hz é o meio-termo que cabe no orçamento móvel provável com interpolação; a taxa é uma constante e o ADR é reaberto se o spike de performance ou o playtest mostrarem que 30 Hz não serve. Nenhum GDD pode fixar valor "por tick": os dados usam segundos, o que mantém a troca barata.

### Alternative 5: Eventos por delegate ou função pura `Step(estado, comandos)`
- **Description**: (a) sistemas notificam por `event`/delegate direto; (b) a simulação como função pura que devolve novo estado e eventos.
- **Pros**: (a) liga fácil à UI; (b) fácil de testar e de repetir.
- **Cons**: (a) a ordem dos efeitos depende de quem assinou e dificulta teste headless; (b) copiar ou alocar o estado a cada tick pesa na horda em Android (GC) e exigiria pooling pesado.
- **Rejection Reason**: Buffer de eventos limpo por tick dá ordem determinística, zero alocação e leitura simples pela apresentação.

### Alternative 6: Onde criar o herói (emenda de 2026-11-05)
- **Description**: (a) o host cria o herói antes do `Create`; (b) o #3 cria o herói no 1º `Tick`, como `ISimSystem`; (c) o compositor chama `IPreparaFase.Preparar` depois do `Create` e antes do 1º `Tick`, com o #3 primeiro.
- **Pros**: (a) simples; (b) não exige interface nova; (c) o herói existe no tick 0, no hash e nos comandos do tick 1, e o teste sem tela monta o mesmo caminho do jogo.
- **Cons**: (a) mistura regra de jogo no host e deixa o `Create` sem o estado inicial; (b) o passo 1 do tick valida comandos antes de qualquer sistema, então o `Mover` do tick 1 seria para um ator "nunca emitido" (falha em modo estrito), e #7, #8 e #6 rodariam o tick 1 sem herói; (c) cria uma exceção ao "só dentro do Tick" na `entity_table`.
- **Rejection Reason**: Escolhida a (c), por recomendação (GDD #3, Regra 3.4, provisória). A exceção é estreita: só o `Spawn` de `Preparar`, sem evento, no estado `Created`.

### Alternative 7: Como o #3 avisa o #16 (emenda de 2026-11-05)
- **Description**: (a) eventos no `EventBuffer`; (b) callbacks ou delegates; (c) uma lista de ganchos registrados no compositor; (d) uma ficha de escalares no `SimWorld`, lida pelo #16 no passo dele, mais interfaces opcionais fora do tick; (e) a ficha como estado do próprio #3 em `Forja.Gameplay.Sim`, entregue pelo compositor ao #16 como visão somente leitura.
- **Pros**: (d) não perde nada se o #16 não rodou (contador que só cresce), não aloca, entra no hash e dispensa que um sistema conheça o outro.
- **Cons**: (a) evento é só saída e pode ser descartado (`event_as_inter_system_channel`); (b) a ordem de assinatura vira regra e aloca; (c) é um barramento escondido entre sistemas; (d) o Core passa a conhecer o formato da ficha.
- **Rejection Reason**: Escolhida a (d) (GDD #3, Regra 15, provisória). A (e) tiraria do Core o formato do #3 (que o Core nunca lê nem hasheia) e a exceção do `IdDoHeroi`, e enxugaria o `FailureDetail`, mas exigiria emendar os GDDs #2 e #3 ("no `SimWorld`"); rejeitada **por ora, por decisão do autor (2026-11-05)**, e entra na reavaliação (OQ-13 do #2 e OQ-10 do #3).

### Alternative 8: Onde hashear a ficha de fase (emenda de 2026-11-05)
- **Description**: (a) pelo `SimWorld`, como o `CombatHold`; (b) pelo `Hash` do próprio sistema #3.
- **Pros**: (b) a ordem de entrada do hash do item 12 não muda, e nada muda no registro `hash_estado`.
- **Cons**: (a) exigiria emendar a ordem do hash e a nota do registro.
- **Rejection Reason**: Escolhida a (b), achada no `/consistency-check` de 2026-11-04 (GDD #3, Regras 4 e 16).

### Alternative 9: Como o #2 avisa que o chefe não nasceu (emenda de 2026-11-05)
- **Description**: (a) o Core emite `ChefeAusente`, como pede o texto do GDD #3; (b) o Core emite `EssentialSpawnRejected` e o #3 traduz em `ChefeAusente`.
- **Pros**: (b) o Core continua sem saber o que é um "chefe" (só sabe de entidade `Essencial`).
- **Cons**: (a) o Core passa a conhecer um conceito do #7 e do #3; (b) exige `EndDetail` legível pelo #3 e a regra "dentro do tick, todo `Essencial` rejeitado é inimigo" (porque o herói só nasce no `Preparar`).
- **Rejection Reason**: Escolhida a (b), por recomendação (provisória; o GDD #3, Regra 7, pediu o motivo `ChefeAusente`).

### Alternative 10: Como o #7 alcança o gerador da wave no `Preparar` (emenda de 2026-11-05)
- **Description**: (a) `RngWave(w)` em `SimWorld`, função pura de uma `waveBase` guardada; (b) mudar a assinatura para `Preparar(SimWorld, PrepContext)` com o `RngWave` no contexto; (c) o compositor entrega a seed mestre ao #7.
- **Pros**: (a) não muda `IPreparaFase` (o #3 e a Emenda 14 ficam intactos), segue o padrão das guardas de `Spawn` e `PhaseForWrite` e esconde a seed; (b) é explícita.
- **Cons**: (b) é mais invasiva: reescreve cada implementador de `IPreparaFase`; (c) expõe a seed mestre a um sistema, duplica a derivação e pode divergir da FS6; (a) deixa a regra "só o #7 chama" como convenção e revisão.
- **Rejection Reason**: Escolhida a (a), pelo autor em 2026-11-05 (provisória). O TD-ADR recomendou guardar só a `waveBase`, e não a seed mestre.

## Consequences

### Positive
- Fórmulas dos GDDs em float, sem aritmética manual: menor custo de design e de teste.
- Um único tick, uma única conversão de segundos para ticks e um único contrato de estado (`SimWorld`) para #3, #6, #7, #8 e o auto-battle (#40, futuro); o headless e o jogo montam a mesma lista de sistemas pelo mesmo compositor.
- Streams independentes: mudar a regra de loot não altera spawns nem ofertas da mesma seed, o que preserva as métricas de oferta do aceite.
- Teste headless chama o mesmo código do jogo, com hash para detectar divergência.
- Simulação sem engine roda em EditMode e é fácil de reaproveitar.
- O ciclo de vida da fase é uniforme: o jogo, o teste sem tela e o auto-battle montam a mesma sequência (`Create`, `Preparar`, `Tick`..., `Concluir`, `Discard`).
- A ficha de fase e o `CombatHold` são escalares no `SimWorld`: nenhum sistema precisa conhecer outro, e o #3 nunca conhece o #16.

### Negative
- **Sem garantia cross-runtime.** Não há replay validado por servidor, nem ranking por replay, nem autoridade de host com este ADR. Se #22 ou #40 pedirem isso, é preciso um ADR de substituição (ponto fixo) que reescreve as fórmulas; `SimMath` e o vetor próprio reduzem, não eliminam, esse custo.
- **O teste headless no Editor (Mono, x64) não é o mesmo runtime do jogo (IL2CPP, ARM64).** As métricas de aceite da oferta são estatísticas e não dependem de igualdade bit a bit, mas um resultado do Editor não prova o resultado do aparelho até o spike de hash.
- Proibir funções transcendentais e `Unity.Mathematics` limita fórmulas (curvas, ângulos) e obriga tabelas.
- 30 Hz coloca o hit e o telegraph numa granularidade de 33 ms e exige interpolação na apresentação.
- Dois estados (anterior e atual) por entidade visível custam memória e cópia por tick.
- O `SimWorld` fixa em Core a forma mínima de uma entidade (id, posição, facção, HP, vivo): o ADR-0004 acrescenta as quatro colunas de identidade e os demais ADRs só podem acrescentar colunas, e uma mudança de modelo (por exemplo handle com geração) é um novo ADR.
- Um APK com mais de uma ABI tem determinismo separado por ABI; o resultado de um auto-battle não pode ser rederivado da seed depois de um update.
- O Core passa a conhecer o formato da ficha de fase do #3 (`PhaseSheet`): mudar um campo atualiza o struct deste ADR e o GDD #3 (a Alternative 7(e) fica como saída).
- O `Spawn` de `Preparar` e a escrita de `IdDoHeroi` na ficha são uma exceção à regra "só dentro do Tick" (o registro de arquitetura precisa refletir isso na `entity_table`).
- Mais superfície de contrato (estados, contadores, modo estrito): mais testes. No modo estrito, um script com erro só roda inteiro em modo não estrito.
- O ADR cresce e o custo recai sobre um dev solo: as regras marcadas *(provisória)* nos GDDs #2 e #3 entram na reavaliação (OQ-13 do #2 e OQ-10 do #3).

## Risks
- **Float divergente no mesmo build** (fusão FMA, otimizações do IL2CPP): mitigação é o spike de hash no aparelho antes do vertical slice; se divergir, este ADR é reaberto com a alternativa de ponto fixo.
- **Valor de tempo em segundos que arredonda para 0 tick** (cooldown ou duração menor que ~17 ms): mitigação é a conversão ao inteiro mais próximo com mínimo de 1 tick e a validação de dados que recusa o valor.
- **Eventos perdidos numa horda grande:** `DroppedEvents` nunca descarta em silêncio; a capacidade do buffer vem dos dados da fase e é medida no spike de performance.
- **`MaxTicksPerFrame` baixo demais** deixa o jogo em câmera lenta em aparelho fraco; alto demais causa espiral: o valor inicial 4 é provisório e deve ser medido no aparelho de referência (ainda não verificado).
- **Sistema de gameplay referencia `UnityEngine` por descuido:** mitigação é o asmdef "No Engine References" e a revisão de `code-reviewer`.
- **Novo stream de RNG criado sem registro:** mitigação é a regra de registro e um teste que lista os ids.
- **Divergência por desenho entre Editor x64 e ARM64 IL2CPP.** O hash do Editor pode diferir do hash do aparelho sem que isso seja bug: este ADR só promete determinismo no mesmo build e no mesmo runtime. O spike registra o resultado e a divergência entre runtimes é aceita (não reabre o ADR) enquanto #22 e #40 não exigirem o contrário; divergência dentro do mesmo build reabre o ADR.
- **Validação do `unity-specialist` (5.5, 2026-11-03):** sem achado bloqueante. Notas incorporadas: regra de classe para sistemas, buffer `SimEvent[]`, zero estado `static` mutável, sem reflexão, spike em Release, e verificação de compilação de `ref struct` + `ReadOnlySpan`. As afirmações sobre asmdef sem engine, `ref struct` em interface e `Span` em Mono/IL2CPP são `NOT SOURCEABLE` em `docs/engine-reference/` e ficam como verificação, não como fato.
- **Revisão TD-ADR (5.6, 2026-11-03): CONCERNS na 1ª passada, sem REJECT.** Itens 1 a 10 e os menores foram revisados neste texto: Varredura fora da simulação (#15), "mesmo build" = mesmo binário e ABI, `SimWorld` com ids monotônicos, eventos só saída com `DroppedEvents`, drenagem após cada tick, #3 e #16 como `ISimSystem`, três asmdefs com compositor sem engine, segundos nos dados e ticks na simulação com arredondamento ao mais próximo, alternativas de taxa e de tipo escalar próprio, seed de stream por SplitMix64, `Spawn` por índice de wave, política de auto-battle sob as mesmas regras e estado anterior guardado pela simulação. As escolhas confirmadas pelo usuário (float32, 30 Hz, PCG32, `Tick` + buffer de eventos) não mudaram. A revisão do TD sobre o texto revisado não foi refeita.

- **`Spawn` rejeitado do chefe sem detecção (emenda de 2026-11-05):** o `SpawnsRejected` é só diagnóstico e não distingue o chefe de um inimigo comum; mitigação é o parâmetro `essential` no `Spawn`, que encerra a fase com `InternalFailure` (`EssentialSpawnRejected`) no mesmo tick. Sem isso o #3 só pegaria o caso pelo teto de tempo.
- **Escrita fora do tick (emenda de 2026-11-05):** o `Preparar` é a única exceção (`Spawn` e a ficha); mitigação é a guarda por estado em cada escritor (só `Spawn` e `PhaseForWrite` aceitam `Created`) e um teste que confirma que cada um falha fora do que lhe cabe.
- **Dois escritores da ficha ou do `CombatHold`:** a regra é só convenção e revisão (o Core não impõe); mitigação é a revisão de código e o critério R17 do #3.
- **Interface opcional não chamada:** um sistema que implementa `IPreparaFase` ou `IConcluiFase` e que o compositor não chama falharia em silêncio; mitigação é o compositor único e um teste que confere que `Preparar` e `Concluir` rodam para cada implementador registrado.
- **Conflito entre GDDs (emenda de 2026-11-05):** a Regra 13 do #2 põe `DadosInvalidos` no pedido de fim dentro do tick, e o #3 (Regra 14) valida no `Preparar`, por exceção. Este ADR segue o #3; falta corrigir a Regra 13 do #2 (pendência registrada, a aprovar).
- **Rotatividade de emendas:** cada campo *(provisório)* da ficha que o GDD #3 mudar atualiza o struct deste ADR; mitigação: só uma mudança que altera o contrato (quem escreve, quem lê, onde entra no hash) exige novo gate, e a Alternative 7(e) fica como saída na reavaliação.
- **Prazo do MVP:** o tamanho do contrato pesa para um dev solo (13 a 20 meses); mitigação: os testes de Validation Criteria entram como aceite da 1ª story do #2.
- **Linha do herói fora do tick:** resolvida por `Spawn(faction, essential, xpValue, hp, x, y, entityClass, archetypeId)`, que inicia a linha inteira com a posição anterior igual à atual (sem interpolar a partir de (0,0)).
- **Validação das emendas pelo `unity-specialist` (5.5, 2026-11-05):** sem achado bloqueante. Incorporado: `ref readonly` para ler a ficha e escrita só por `PhaseForWrite` (uma auto-propriedade não devolve `ref`: o corpo é `=> ref _phase`); valores explícitos nos enums que vão para log e hash; campo "Post-Cutoff APIs Used" reescrito (BCL pré-cutoff, disponibilidade `NOT SOURCEABLE`); listas tipadas no compositor, sem reflexão nem genérico em runtime (AOT); guarda de escrita fora do `Tick` e exceção do `Preparar` ampliada à ficha; `Pcg32` em array, `RngWave` em variável local e `unchecked` explícito; `static event` e `[RuntimeInitializeOnLoadMethod]` proibidos; asmdef com Auto Referenced desligado e sem `unsafe`; `PhaseResult` como `readonly struct`; golden de hash por runtime; confinamento à thread principal. Segue `NOT SOURCEABLE` em `docs/engine-reference/unity/`: a opção "No Engine References", o perfil de API, `Span<T>`, `ref struct` e retorno por `ref` em Mono e IL2CPP ARM64, `BitConverter.SingleToInt32Bits`, FMA e float entre runtimes, stripping com interfaces, GC e custo do `Create`, e a thread dos callbacks do Android. Se o pin subir para o 6.5 ou o 6.6 (Editor CoreCLR), o item 1 de Verification Required precisa ser refeito.
- **Revisão TD-ADR das emendas (5.6, 2026-11-05):** CONCERNS na 1ª passada, sem REJECT. Revisados neste texto: (C1) guarda de escrita só em `Created` e no `Tick` (`Kill` e o `set` de `CombatHold` só no `Tick`; `Spawn` e `PhaseForWrite` também em `Created`) e `Spawn` que inicia a linha inteira (`hp`, `x`, `y`); (C2) `Simulation.EndDetail` e `ctx.PendingEnd`; (C3) comando fora de ordem processado como veio, sem contador; (C4) falha do `Preparar` por exceção, `InvalidData` fora do Core, `EssentialSpawnRejected` dentro do tick e Alternative 9; (C5) `DrainEvents()`; (C6) derivação do `RngWave` na emenda 11 e, na gravação, as posições do registro (`combat_hold`, `phase_sheet`, `phase_lifecycle`, `sim_create`; `sim_random` com o `RngWave`; `entity_table` delimitada); menores (`PhaseSheet` com `State` e `SimultaneousDeath`, momento do `Concluir`, `StateHash` lança em `Broken` e `Destroyed`, origem de `ids_de_preparacao`); Alternative 7(e) e os riscos de rotatividade, conflito entre GDDs e prazo. O autor confirmou em 2026-11-05 a ficha no `SimWorld`, com a (e) registrada. Pendente: corrigir a Regra 13 do #2 (`DadosInvalidos` no `Preparar`). A revisão do TD sobre o texto revisado não foi refeita.
- **`RngWave` com estado ou chamado fora do #7 (emenda de 2026-11-05):** um cache de gerador por wave, uma tabela estática ou um campo memoizado seriam estado fora do hash que atravessa ticks e quebrariam o replay sem erro; `default(Pcg32)` é degenerado. Mitigação: `RngWave` sem estado, `Pcg32` só por construtor, teste de que nunca devolve `default`, vetor de referência por runtime e revisão de código (convenção, como o risco dos dois escritores).
- **Causa de morte fora do hash (emenda de 2026-11-05):** hash igual com causas diferentes só ocorre se nenhum consumidor mudar estado; mitigação: todo sistema que age pela causa reflete o efeito no próprio `Hash`, `switch` com `default` que lança, e o teste do Core roda com sistemas falsos.
- **Capacidade de eventos no tick do rugido (emenda de 2026-11-05):** **revista na Emenda 18:** com a horda agregada em `HordeTick`, o tick do rugido não precisa mais de cerca de 300 `Death`; a fórmula de `EventCapacity` com termos nomeados está no ADR-0005 (Decisão 7), com `K` (`SkillCast`) e `E_3_16` (#3 e #16) pendentes como `NOT ASSESSED`.
- **Validação das Emendas 15 e 16 pelo `unity-specialist` (5.5, 2026-11-05):** sem bloqueio; notas menores incorporadas (sem estado, seed gravada no `Create` antes do `Preparar`, uma só função de derivação, `w < 0`, `default(Pcg32)`, critério da causa só no Core, `default` que lança nos `switch`, valores de referência por runtime). Nada foi confirmado contra `docs/engine-reference/unity/`, que não cobre C#, IL2CPP, struct por valor nem enum (`NOT SOURCEABLE`); as respostas vêm da semântica do C# 9 e do comportamento geral do IL2CPP.
- **Revisão TD-ADR das Emendas 15 e 16 (5.6, 2026-11-05):** CONCERNS na 1ª passada, sem REJECT. Revisados neste texto: `RngWave` na Emenda 14, na guideline de guardas e no teste de guarda; a causa fora do hash vale só no Core e o consumidor reflete o efeito; a primeira causa vence em `Kill` repetido; os critérios de validação; a Alternative 10; `waveBase` no lugar da seed mestre; a Emenda 11 como fonte única; a lista "Não entram" da Emenda 12; o `Preparar` na tela de carregamento e no Verification Required 9. A revisão do TD sobre o texto revisado não foi refeita.

## GDD Requirements Addressed

Os GDDs #1, #2, #3, #6, #7 e #28 já existem em disco (as últimas linhas da tabela os citam). Os demais (#5, #8, #16, #22) continuam pendentes: as linhas deles citam o conceito congelado e o índice, o requisito é o esperado e deve ser conferido quando o GDD existir.

| GDD System | Requirement | How This ADR Addresses It |
|------------|-------------|--------------------------|
| `design/gdd/game-concept.md` L326 | Separar simulação de apresentação: tick fixo, RNG com seed, lógica sem MonoBehaviour | Asmdef sem engine, `Tick(comandos)`, 30 Hz, PCG32 com seed mestre |
| `design/gdd/game-concept.md` L400 | Seeds determinísticas para spawn e oferta; simulação headless chama o mesmo código do jogo | Streams `Spawn` e `Offer`; teste EditMode chama `Simulation.Tick` |
| `design/gdd/game-concept.md` L323 | Composição das waves por seed | Stream `Spawn` independente de `Loot` e `Offer` |
| `design/gdd/game-concept.md` L246 | O auto-battle é simulação determinística por seed e pode falhar (a Varredura não simula: #15) | Mesma simulação, comandos vindos de uma política em vez do jogador (#40, futuro); determinismo do mesmo binário e da mesma ABI; o resultado se calcula e se credita de uma vez, nunca se rederiva da seed depois de um update |
| #16 Grimório (GDD pendente) | Oferta, registro e substituição são o mesmo código no headless; o #16 lê os level-ups pela ficha do #3 | `ISimSystem` no compositor; oferta sorteia do stream `Offer`; `CombatHold` escrito só pelo #16; `IPreparaFase` e `IConcluiFase` |
| `design/gdd/combate-e-dano.md` (#6) | Fórmulas de dano, cooldowns e telegraphs; morte pelo rugido do #7 com causa própria | Float32; segundos nos dados convertidos para ticks; `SimWorld` para HP e posição; `DeathCause.Rugido` e a primeira causa vence (Emenda 15) |
| `design/gdd/horda-waves-e-inimigos.md` (#7) | Composição das waves sorteada por seed e por índice de wave, antes do tick 1; hordas grandes em Android | `RngWave(w)` em `SimWorld`, pura e fora do hash, usada no `Preparar` (Emenda 16); arrays pré-alocados, zero alocação por tick; `SimWorld` para as entidades |
| #8 Skills e evoluções (GDD pendente) | Efeitos de skill em ordem previsível | `ISimSystem` em ordem de registro fixa; comunicação pelo `SimWorld`, não por eventos |
| #5 Log de eventos e instrumentação (GDD pendente) | Registro dos eventos de combate para o aceite | Buffer de eventos limpo por tick, lido pelo log |
| #22 Ranking (GDD pendente) | Replay validado por servidor | **Não atendido**: exige ADR de substituição por ponto fixo (ver Negative) |
| `design/gdd/simulacao-deterministica.md` (#2) | Contrato de `Simulation` (`Create` com snapshot, estados, modo estrito), `CombatHold` e `CombatTick`, `Essencial` e `InternalFailure`, `PickOffer`, contadores, hash por byte | Emendas 1 a 12 e Key Interfaces |
| `design/gdd/fluxo-de-fase.md` (#3) | Ficha de fase, `IPreparaFase` e `IConcluiFase`, `Essencial` escrito no `Preparar`, `xpValue` e lista de mortos, `InternalFailure` no pedido de fim | Emendas 6, 7, 13 e 14 |
| `design/gdd/dados-e-balanceamento.md` (#1) | Snapshot da fase imutável, em ticks, com capacidades e hash | `IPhaseSnapshot` e `Create` (emenda 1); o tipo do snapshot é do ADR-0002 |
| `design/gdd/save-local.md` (#28) | Nada de estado de fase em andamento no save; abandono e app fechado não passam por tick | Estados `Broken` e `Destroyed` e `Discard()`; a simulação não serializa nem restaura fase |

## Performance Implications
- **CPU**: tick de 30 Hz, metade do custo de um tick a 60 Hz; o orçamento em ms por tick **não é reivindicado aqui** (aparelho de referência não verificado), então nenhum orçamento é registrado; cada sistema recebe o seu na medição do spike de performance.
- **Memory**: arrays por fase pré-alocados com capacidade máxima vinda dos dados da fase; dois estados por entidade visível para interpolação.
- **Load Time**: nenhum impacto relevante; conversão de dados para structs no início da fase.
- **Network**: não se aplica.

## Migration Plan
Não se aplica: o projeto não tem código de jogo (`Assets/` só contém o modelo inicial do Unity). A estrutura de pastas e os asmdefs nascem com a primeira story de #2.

## Validation Criteria
- Teste de reprodutibilidade em EditMode: mesma seed e mesmos comandos, duas execuções, mesmo hash a cada 100 ticks, por pelo menos uma fase completa.
- Teste de independência dos streams: consumir N sorteios extras em `Loot` não altera a sequência de `Spawn` nem de `Offer`.
- Spike de hash entre Editor, Windows IL2CPP e Android IL2CPP ARM64: resultado registrado (iguais ou divergentes) neste ADR.
- Profiler: 0 B de alocação gerenciada por `Tick` em regime, no aparelho de referência.
- Compilação falha ao usar `UnityEngine` dentro do asmdef da simulação.
- Teste de ciclo de vida: `Create` com hash de snapshot diferente do cabeçalho do log lança e não cria; a sequência `Create`, `Preparar`, `Tick`..., `Concluir` roda na ordem; o `Spawn` de `Preparar` não emite evento; `Spawn` fora do estado `Created` e fora do `Tick` lança.
- Teste dos dois modos: um script sem erro dá o mesmo hash em modo estrito e não estrito; um script com erro só roda inteiro em modo não estrito.
- Teste do fim: com `InternalFailure` e `Victory` pedidas no mesmo tick vale `InternalFailure`; `Tick` depois de `Ended` lança.
- O hash de referência (golden) é **por runtime** (Editor Mono x64, IL2CPP Windows, IL2CPP ARM64): um golden do Editor não prova o resultado do aparelho.
- Teste de guarda: `Spawn` e `PhaseForWrite` lançam fora de `Created` e fora do `Tick`; `Kill` e o `set` de `CombatHold` lançam fora do `Tick` (inclusive em `Created`); `RngWave` lança em `Running` fora do `Tick`, em `Ended`, `Broken` e `Destroyed`, e para `w < 0` nos dois modos. Esses testes, o de ciclo de vida e o dos dois modos entram como aceite da 1ª story do #2.
- Capacidade de ids: com `SpawnsDeDados` 899, `IdsDePreparacao` 1 e margem 25, `EntityCapacity` 1124 é recusada pelo compositor (nenhuma simulação é criada, o #3 recebe `DadosInvalidos`) e 1125 cria a simulação; um `IPreparaFase` que declara mais ids que o snapshot comporta é recusado do mesmo modo.
- `RngWave(w)` devolve o mesmo estado inicial no `Preparar` e no `Tick`, nunca devolve `default(Pcg32)`, e chamá-lo K vezes a mais no `Preparar` não altera nenhum dos três streams nem o `StateHash`.
- Vetor de referência: para uma seed fixa, as N primeiras saídas de `RngWave(0)`, `RngWave(1)` e `RngWave(3)` batem com a FS6 calculada à parte, e o golden é por runtime (junto do golden do hash).
- Causa de morte, só no Core e com sistemas falsos: `DeathCause.Rugido == 2`; mudar só a causa de um `Kill` não muda o hash do `SimWorld`; `Kill` duas vezes no mesmo id e no mesmo tick gera 1 `Death` e mantém a 1ª causa. O hash da simulação montada pode mudar pelo efeito da causa nos consumidores (#3, #8, #24), que o refletem no próprio `Hash`.

## Reavaliação prevista
O usuário aceitou as escolhas deste ADR por recomendação (float32, 30 Hz, PCG32, `Tick` + buffer de eventos, `SimWorld`, #3 e #16 como `ISimSystem`, segundos nos dados) sem dominar todos os conceitos, e pediu para reavaliá-las com o jogo avançado. Momento natural: depois do spike de performance e do spike de hash entre runtimes, com o vertical slice jogável. Até lá o ADR segue `Proposed`. As emendas de 2026-11-05 marcadas *(provisória)* nos GDDs #2 e #3 entram na mesma reavaliação (OQ-13 do #2 e OQ-10 do #3).

## Related
- `design/gdd/game-concept.md` (L246, L323, L326, L349, L400) e `design/gdd/systems-index.md` (#2, #3, #5, #6, #7, #8, #22, #40).
- `design/gdd/simulacao-deterministica.md` (#2, OQ-5), `design/gdd/fluxo-de-fase.md` (#3, OQ-2), `design/gdd/dados-e-balanceamento.md` (#1) e `design/gdd/save-local.md` (#28).
- `docs/consistency-failures.md` (hash da ficha de fase e total de spawns, 2026-11-04).
- `docs/registry/architecture.yaml`, posições novas ou revisadas por estas emendas: novas `combat_hold` (dono #16), `phase_sheet` (dono #3), `phase_lifecycle` (`IPreparaFase` e `IConcluiFase`, chamada direta pelo compositor) e `sim_create` (criação por `Simulation.Create`); estendidas `sim_random` (inclui o `RngWave`), `sim_events` (assinatura com `DrainEvents()`) e `mutable_static_in_simulation` (compositor, #3 e ponte); revisada `entity_table` (`write_access`: o `Spawn` de `Preparar`, com a linha inteira e sem evento, e a ficha, só em `Created`).
- ADR-0002 (`Proposed`, 2026-11-05): dados e balanceamento do #1; emenda a conversão de tempo e de taxas, os dados de fase e o carregador. Sem outros ADRs além dele. Candidatos de substituição deste ADR: ADR futuro de replay e validação de ranking (#22) e de auto-battle (#40).
- ADR-0004 (colunas do `SimWorld` para combate e horda, `Proposed`, 2026-11-06) e ADR-0005 (pipeline de dano e eventos de combate, `Proposed`, 2026-11-06): pedem as Emendas 17 e 18 deste ADR.
- `design/business-model.md` não depende deste ADR.


## Emendas

### 2026-11-05: ADR ainda `Proposed`, emendado no lugar

O ADR não foi aceito, então as emendas entram neste arquivo (não há ADR novo nem supersessão). Cada linha liga um item pedido pelos GDDs ao ponto deste ADR que o resolve.

| # | Item | Origem | Onde neste ADR |
|---|------|--------|----------------|
| 1 | Pedido de fim em `SimContext`, com motivo | OQ-5 do #2; OQ-2 do #3 | Emenda 7 e `RequestEnd` |
| 2 | Contadores `CommandsRejected`, `SpawnsRejected` e `NonFiniteCount` (o `DroppedEvents` já existia) | OQ-5 do #2 | Emendas 6, 8 e 9; `Simulation` |
| 3 | `Create` estático sem campo `static` mutável | OQ-5 do #2 | Emenda 1; Implementation Guidelines |
| 4 | Configuração do IL2CPP na tag do build | OQ-5 do #2 | Verification Required 7 |
| 5 | `Simulation.Create(snapshot, cabeçalho, seed, sistemas, estrito)` no lugar do construtor | OQ-5 do #2; OQ-2 do #3 | Emenda 1; Key Interfaces |
| 6 | `Command` com `ArgA` e `ArgB`; `PickOffer` em `CommandKind` | OQ-5 do #2 | Emenda 4 |
| 7 | `CombatHold` no `SimWorld`, `ctx.CombatActive` e `CombatTick` | OQ-5 do #2 | Emenda 5 |
| 8 | Coluna `Essencial` e motivo de fim `FalhaInterna` | OQ-5 do #2 | Emendas 6 e 7 |
| 9 | `RngWave(w)` no `SimContext` | OQ-5 do #2 | Emenda 11 |
| 10 | `Spawn` devolvendo −1 quando cheio, id = índice com capacidade igual ao total de spawns, lista de vivos | OQ-5 do #2 | Emenda 6 |
| 11 | `EventosReservados` como constante | OQ-5 do #2 | Emenda 10 |
| 12 | Estados *Quebrada* e *Destruída* | OQ-5 do #2 | Emenda 2 |
| 13 | `SimMath.RoundToInt` (meio para longe de zero) e `FloorToInt` com checagem de faixa | OQ-5 do #2 | Emenda 8 |
| 14 | Hash por byte | OQ-5 do #2 | Emenda 12 |
| 15 | Asmdef do compositor também com "No Engine References" | OQ-5 do #2 | Interface (três asmdefs) e Verification Required 4 |
| 16 | Ficha de fase no `SimWorld`, hasheada pelo `Hash` do #3 | OQ-2 do #3; consistência de 2026-11-04 | Emenda 13; Alternativa 8 |
| 17 | `IPreparaFase` e `IConcluiFase` | OQ-2 do #3 | Emenda 14; Alternativas 6 e 7 |
| 18 | Escrita da marca `Essencial` no `Preparar`, fora do tick, com `Spawn` sem evento | OQ-2 do #3 | Emendas 6 e 14 |
| 19 | Coluna `xpValue` e lista de mortos do tick | OQ-2 do #3 | Emenda 6; `SimWorld.Kill` |
| 20 | Motivo `FalhaInterna` (`ChefeAusente`) no pedido de fim; o `Spawn` rejeitado do chefe é pedido pelo #2; `DadosInvalidos` é por exceção no `Preparar` (não é do Core) | OQ-2 do #3 | Emendas 6, 7 e 14; Alternativa 9; no Core o detalhe é `EssentialSpawnRejected`, e o #3 o traduz em `ChefeAusente` |
| 21 | Detectar "buffer não drenado" | TD-ADR (C5) | Emenda 2; `DrainEvents()` |
| 22 | Detalhe da falha legível pelo #3 | TD-ADR (C2) | Emenda 7; `Simulation.EndDetail` e `ctx.PendingEnd` |
| 23 | Conversão de tempo e de taxas feita no build; dados de fase como snapshot gerado, sem `ScriptableObject` na simulação | ADR-0002 (dados do #1) | Tempo, Interface e Implementation Guidelines |
| 24 | Conferência da capacidade da tabela de ids no compositor, antes do `Create`: `ids_de_preparacao` (código) + `SpawnsDeDados` (snapshot), com a margem; `IPreparaFase.IdsDePreparacao` | `/propagate-design-change` (GDD #1, pendência P2); ADR-0002 | Entidades (item 6), Interface e Implementation Guidelines |
| 25 | Causa de morte `Rugido` em `DeathCause`; a primeira causa vence em `Kill` repetido | `/consistency-check` de 2026-11-05; GDDs #6 (Regras 3 e 11, F2) e #7 (Regra 10.2) | Emendas 6 e 15; Key Interfaces |
| 26 | `RngWave(w)` disponível no `Preparar`, em `SimWorld`, função pura de `waveBase`, fora do hash | GDD #7 (Regra 6); GDD #2 (FS6, nota de 2026-11-05) | Emendas 11, 14 e 16; Alternative 10; Key Interfaces |
| 27 | `Spawn` com `EntityClass` e `archetypeId`; colunas `classe`, `arquetipoId`, `tickNascimento` e `hpMax` no `SimWorld` e no hash do Core (com `xpValue`); `HpAndPosForWrite`; `DeathRecord` sem extensão (2026-11-06) | ADR-0004; GDDs #6 e #7 | Emenda 17; Key Interfaces |
| 28 | Exceção ao "comunicação pelo `SimWorld`" em três formas de canal direto; `Kill` e `Spawn` do Core sem evento; `Kill` só pelo #6 (2026-11-06) | ADR-0005; GDD #6 (Regra 3) | Emenda 18 |
| 29 | `SimEvent` com `ArgA`/`ArgB`, `SimEventKind` com valores explícitos, `Death` com a causa, reserva por tipo, `SimContext.Strict`, `SimInvariantException` (2026-11-06) | ADR-0005; GDDs #6 e #7 | Emenda 18; Key Interfaces |
| 30 | `Spawn` acrescenta o id a `Alive` na hora; corpos de `SimMath.Clamp`, `Min` e `Max` por comparação (2026-11-06) | ADR-0006 | Emenda 6; Numérico |

**Itens que o ADR deixa para outros donos:** o tipo do snapshot (ADR-0002); (resolvido em 2026-11-06: `Kill` só pelo #6, Emenda 18; o `xpValue` entra no `Spawn` e no hash, Emenda 17); os campos exatos de `PhaseSheet` e de `PhaseResult` (GDD #3); a validação do serial de `PickOffer` (#16).
