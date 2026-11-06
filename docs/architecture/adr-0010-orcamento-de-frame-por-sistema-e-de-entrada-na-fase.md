# ADR-0010: Orçamento de frame: tabela de alocação por sistema em milissegundos, sonda de medição fora da engine, regra do tick de recuperação, `LoadLevel` por taxa de frames perdidos, orçamento de entrada na fase e livro de memória

## Status
Proposed

## Date
2026-11-06

## Last Verified
2026-11-06 (contra o ADR-0001 com as Emendas 1 a 18, o ADR-0007, o ADR-0008, o ADR-0009, `docs/registry/architecture.yaml` (`performance_budgets: []`), os GDDs #2 (P1 a P7, L586 a L598), #3 (P1, L625), #6 (`orcamento_combate_ms`, L527) e #7 (`orcamento_horda_ms`, L579), `docs/architecture/requirements-traceability.md` (TR-combate-012, TR-horda-013, TR-simulacao-018, TR-fluxo-008), `.claude/docs/technical-preferences.md` (Performance Budgets) e `docs/engine-reference/unity/` em disco; Unity 6.3 LTS, pin 6000.3.x). **O spike de performance ainda não foi rodado e o aparelho de referência não está verificado** (`VERSION.md`; `technical-preferences.md` com draw calls e memória "TO BE CONFIGURED"). **Todo número deste ADR é provisório.**

## Decision Makers
Rodrigo Reis (escolheu este ADR em 2026-11-06 e confirmou a premissa "fixar a estrutura agora, com números provisórios marcados 'a reavaliar', e deixar o spike só calibrar"; o resto é decisão técnica por recomendação, **provisória, a reavaliar com o spike e o jogo jogável**), Claude Code (autoria), `unity-specialist` (validação, 5.5; um bloqueante, "R medido pelo frame inteiro", corrigido) e `technical-director` (gate TD-ADR, 5.6; veredito CONCERNS com 2 bloqueantes e 6 preocupações, tratados nesta revisão por escolha do autor).

## Summary
Os GDDs #6 e #7 pedem 2,0 ms e 0,3 ms por tick, o #2 pede um custo X1 para o `Tick` inteiro, e a referência de preferências técnicas fala em ~12 ms por frame, mas nenhum documento soma esses pedidos contra o frame, nem diz quem mede, o que acontece quando passa do limite e o que cabe na entrada da fase. Decidido: uma **tabela de alocação** de 12,0 ms por frame com tick, repartida em linhas com dono (o `Tick` da simulação soma 3,0 ms e o resto do frame, 6,5 ms, mais 2,5 ms de reserva térmica); uma **sonda de tempo** (`ITickProbe`) que a simulação chama sem referenciar a engine e cuja implementação mede com `Stopwatch` em histogramas de tamanho fixo (funciona em Release/IL2CPP, sem Profiler); a **desigualdade do tick de recuperação** que valida o `MaxTicksPerFrame`; um **`LoadLevel` dinâmico** (`Normal`/`High`) calculado pela taxa de frames perdidos com histerese e lido só pela apresentação; um **orçamento de entrada na fase** (tela de carregamento) com a regra de que toda alocação e toda carga acontecem antes do primeiro tick; e um **livro de memória** cujo teto fica `NOT ASSESSED` até o aparelho de referência existir. A simulação nunca é cortada por desempenho: o jogo desacelera pelo `MaxTicksPerFrame`, e só a apresentação corta.

## Engine Compatibility

| Field | Value |
|-------|-------|
| **Engine** | Unity 6.3 LTS (6000.3.x; editor instalado 6000.3.27f1) |
| **Domain** | Core (desempenho: orçamento de frame, medição, carga e memória) |
| **Layer** | Foundation (a lista de Required ADRs de `architecture-review-2026-11-06-2.md`, linha 216, classifica como Foundation; não existe `docs/architecture/architecture.md` nem mapa de camadas, então a camada é **provisória, a reavaliar**) |
| **Knowledge Risk** | HIGH (a linha do engine é HIGH em `VERSION.md`; **não existe `modules/core.md`**, e nenhum arquivo de `docs/engine-reference/unity/` cobre medição de tempo de frame, `Stopwatch`, `Application.targetFrameRate`, `FrameTimingManager`, `ProfilerMarker`, GC, estrangulamento térmico nem memória em Android) |
| **References Consulted** | `docs/engine-reference/unity/VERSION.md`, `breaking-changes.md` (Addressables passa a lançar exceção na falha, 6.2+), `deprecated-apis.md` (`Resources.Load`, carga síncrona), `current-best-practices.md` (Asset Management, Performance), `plugins/addressables.md` (carga assíncrona, `Release`); ADR-0001 (`Simulation.Create`, `ISimSystem.Step`, `MaxTicksPerFrame` L406, "orçamento não reivindicado" L451), ADR-0007 (`TickPacer.Plan`, `IFrameClock`, `DroppedTicks`, Decisão 7), ADR-0008 (`ICounterSource`, Seção 7 e Performance), ADR-0009 (`VfxBudget`, `LoadLevel` L102, `PREWARM_MAX_WAIT_MS`, Seção 8); GDD #2 (P1 a P6 e o protocolo L598), GDD #3 (P1), GDD #6 (L527), GDD #7 (L579). **Nenhum módulo de referência cobre o domínio Core.** |
| **Post-Cutoff APIs Used** | Nenhuma API nova de Unity 6 é essencial. Usa `System.Diagnostics.Stopwatch` (BCL), `Time.unscaledDeltaTime` (já usado pelo ADR-0007) e o Addressables como a referência local descreve. O comportamento de cada um no 6000.3.27f1 em Android é **`NOT SOURCEABLE`** (Verification Required 1 a 9). O código novo fica em **C# 9**. |
| **Verification Required** | (1) `NOT SOURCEABLE`: resolução e custo de `Stopwatch.GetTimestamp` em IL2CPP ARM64; **a sonda ligada não pode custar mais que 0,05 ms no p95 do `Tick`** (medir com `NullTickProbe` contra `StopwatchTickProbe`). (2) `NOT SOURCEABLE`: `Application.targetFrameRate = 60` é respeitado no aparelho de referência; `QualitySettings.vSyncCount`; aparelho com tela de 90 ou 120 Hz. (3) `NOT SOURCEABLE`: se `Time.unscaledDeltaTime` é suavizado pela Unity e se ele aponta um frame perdido de verdade (provocar um engasgo de 100 ms e uma queda sustentada para 30 fps e ver o detector acusar). **Gatilho: se não acusar, trocar o sinal por `FrameTimingManager` (item 5) sem mudar o `LoadGovernor`.** (4) `NOT SOURCEABLE`: GC no aparelho: zero alocação gerenciada por frame depois do primeiro tick, e nenhuma coleta durante a fase (o modo de GC do projeto é decisão pendente). (5) `NOT SOURCEABLE`: `FrameTimingManager`: fonte **provável** do tempo ativo da CPU principal e da render thread (R) em build de aceite e plano B do sinal de carga; disponibilidade no aparelho, em quais APIs gráficas (GLES e Vulkan variam), quais campos existem no 6000.3, e o atraso de alguns frames dos resultados. **Gatilho: se não houver tempo ativo, R só é medido em build de desenvolvimento com o Profiler, e o aceite de R vira "medido em Dev Build, não em Release" registrado na Emenda de calibração.** (6) Estrangulamento térmico: tudo medido no **minuto 20** de sessão contínua, com a temperatura inicial e o modo de energia registrados. (7) Addressables no 6000.3.27f1: a falha lança exceção (`breaking-changes.md`); todos os handles da fase liberados no `Discard`; nenhuma carga depois do primeiro tick. (8) `NOT SOURCEABLE`: a ferramenta e a métrica de memória residente no Android (PSS) e o teto do aparelho de referência. (9) O custo de cada linha da Tabela é medido no cenário `BENCH-HEAVY` (Decisão 1) em Release/IL2CPP (definição na Decisão 1), nunca no Editor; **R é tempo ativo da thread principal, nunca frame − Tick** (Decisão 1). (10) Registrar no protocolo o modo bateria/economia de energia e, se o spike quiser, o status térmico do Android lido pela API nativa (`NOT SOURCEABLE`, opcional, sem dependência nova). |

## ADR Dependencies

| Field | Value |
|-------|-------|
| **Depends On** | ADR-0001 (`Proposed`; `Simulation.Create`, `ISimSystem.Step`, zero alocação, `MaxTicksPerFrame` inicial 4), ADR-0007 (`Proposed`; `TickPacer.Plan`, `IFrameClock`, `PhaseHost`, `LateUpdate`, `DroppedTicks`), ADR-0008 (`Proposed`; `ICounterSource`, `NoteKind`) e ADR-0009 (`Proposed`; `VfxBudget`, `LoadLevel`, pré-aquecimento). Este ADR só pode ser aceito depois dos quatro. |
| **Enables** | O GDD #12 (dono do consumo do `LoadLevel`), os critérios de aceite de desempenho do `docs/acceptance/mvp.md` (X1, X3, X6, N), as stories de aceite do #2, #3, #6 e #7, o spike de performance (protocolo e cenário), a entrada `performance_budgets` do registro. |
| **Blocks** | As stories de aceite de desempenho dos GDDs #2 (P1 a P6), #3 (P1), #6 (AC-P1) e #7 (AC-P1); TR-combate-012, TR-horda-013, TR-simulacao-018 e TR-fluxo-008 (hoje "❌ GAP" ou "⚠️ Partial"). |
| **Ordering Note** | **Emendas pedidas, a escrever junto com a aceitação deste:** (A) **ADR-0001**, Key Interfaces: `ISimSystem` ganha `int BudgetLine { get; }` (1, 2, 3 ou 5); `Simulation.Create` ganha o parâmetro `ITickProbe probe` (nulo vira `NullTickProbe`) e **lança** se um sistema declarar uma linha inválida; o `Tick` chama `Begin`/`End` do slot total e de cada sistema (Decisões 2 e 3). (B) **ADR-0007**, Decisão 4: o `Plan` devolve também o `dt` saneado efetivamente usado (`DtUsed`; 0 quando pausado ou descartado) e o `PhaseHost` o entrega ao `LoadGovernor` (Decisão 5). (C) **ADR-0008**: a apresentação/orçamento implementa `ICounterSource` com ids próprios, e o enum `NoteKind` ganha `LoadLevelChanged = 9` (o próximo livre depois de `PrewarmIncomplete = 8`). (D) **ADR-0009**, Decisão 6 (L102): o `LoadLevel` real e o significado de `High` passam a ser os da Decisão 5 deste ADR; sai o "NOT ASSESSED"; e o texto `Alto = 1` vira `High = 1`, o nome do enum que o próprio ADR-0009 declara (L164). **O tipo `LoadLevel` é o do ADR-0009 (`Forja.Gameplay.Sim.View`); este ADR não declara outro.** (E) **ADR-0009, Seção 8 (e L137, L198, L211)**: "a carga continua em segundo plano depois do teto" passa a valer só para o aquecimento (shader, desenho fora da tela, áudio); a residência dos assets é obrigatória antes do primeiro tick (Decisão 6 deste ADR). (F) **GDDs**: ver GDD Sync. O tempo do commit do `BeginStage` é uma linha da entrada na fase (Decisão 6) e pertence ao ADR-0003. |

## Context

### Problem Statement
Quatro documentos pedem tempo de CPU sem que ninguém o some: o GDD #6 quer um `Tick` de combate com p95 ≤ 2,0 ms e p99 ≤ 4,0 ms com 300+ vivos e 3 avisos; o #7 quer p95 0,3 ms e p99 0,5 ms para o passo da horda; o #2 exige um X1 para o `Tick` inteiro (P1), um X3 de memória (P3), um X6 para o hash do fim (P6) e um N de vivos (P4), todos "SPEC INCOMPLETO"; e o #3 depende do X1 para o passo de XP. A preferência técnica fixa ~12 ms por frame a 60 fps, sem repartir. O ADR-0001 (L451) deliberadamente não reivindica orçamento, o ADR-0007 (Decisão 7) e o ADR-0009 (Decisão 6 e 8) empurram para "o ADR de orçamento de frame" o `LoadLevel` dinâmico, o teto de memória, o Addressables e o `MaxTicksPerFrame` medido, e o registro tem `performance_budgets: []`. Sem este ADR, cada sistema se mede no cenário que lhe convém, a soma pode passar do frame sem que nada acuse, e o corte por carga do ADR-0009 nunca liga. A revisão de 2026-11-06 pôs este ADR "depois do spike"; a estrutura, porém, não depende do número, e os ADRs 0007 e 0009 só aceitam com ela.

### Constraints
- ADR-0001: `Forja.Simulation` e os sistemas chamados por `ISimSystem.Step` não referenciam `UnityEngine` ("No Engine References"); zero alocação gerenciada por `Tick`; a simulação é determinística no mesmo build; `MaxTicksPerFrame` 1 a 16, inicial 4, a medir.
- GDD #2, Regra 11: o jogo desacelera e **nunca pula nem muda o conteúdo da fase por desempenho**; o protocolo de medição (L598): aparelho verificado, "fase mais pesada" por ID, ≥ 20 execuções com aquecimento descartado, temperatura e modo de energia registrados, máximo, mediana e p95, orçamento commitado **antes** do build de aceite.
- Preferência técnica: 60 fps de alvo, piso de 30 fps, ~12 ms por frame (folga térmica sob os 16,6 ms), medido no minuto 20 num Android intermediário.
- Art bible 8: ≤ 150 draws, ≤ 300 mil triângulos, overdraw médio ≤ 2,5×, texturas da horda ≤ 2 MB e de VFX ≤ 4 MB (todos provisórios).
- Dev solo, uma pessoa valida: poucas classes, nenhuma ferramenta nova, sem pacote de terceiros.
- Aparelho de referência não verificado: nenhum número deste ADR é medido.

### Requirements
- Cumprir TR-combate-012, TR-horda-013, TR-simulacao-018 e TR-fluxo-008 sem mudar a decisão dos GDDs além do registrado em GDD Sync.
- Que a **soma** das linhas seja verificável por teste e por `/architecture-review`.
- Medir em Release/IL2CPP no aparelho, sem depender do Profiler, e sem a medição entrar na simulação, no hash ou no log como estado.
- Que o corte por carga nunca altere a simulação.
- Que a entrada na fase tenha dono, teto e regra de alocação e de carga.
- Que cada premissa não coberta pela referência seja medida, tenha plano B e gatilho.

## Decision

### 1. Moeda, total e cenário de medição
- **Moeda:** milissegundos de **tempo ATIVO** da CPU da thread principal (sem as esperas de vsync, de pacing e da thread de render), **no frame que roda ao menos um `Tick`** ("frame com tick", o mais pesado dos frames regulares), em **p95**, com p99 e máximo ao lado. A 60 fps o tick de 30 Hz cai num frame sim, noutro não; o frame sem tick é mais leve e não é o que limita.
- **O tempo de parede do frame NÃO é a moeda.** Com vsync e frame pacing o frame dura ~16,6 ms mesmo que a thread principal trabalhe 8 ms, porque ela espera a thread de render; "R = frame − Tick" daria sempre o mesmo número e nunca fecharia. De onde sai cada medida:
  - **Tick e trechos nossos** (L1 a L5, e os pedaços de L6 que o nosso código delimita): `Stopwatch` pela sonda (Decisão 3), que mede só dentro do trecho e portanto não inclui espera. É tempo de parede do trecho: preempção ou migração big.LITTLE o infla, e o p99 e o pior tick absorvem isso.
  - **R (L6 a L9) em build de desenvolvimento:** o Profiler (CPU da thread principal excluindo as esperas).
  - **R em build de aceite (Release):** o `FrameTimingManager` (campos de tempo ativo da CPU principal e da render thread; `NOT SOURCEABLE`, Verification Required 5). Por isso ele deixa de ser só plano B do sinal de carga e passa a ser a fonte **provável** de R no aparelho.
- **Total `T = 12,0 ms`** *(provisório; vem das preferências técnicas)*, sob o frame de 16,6 ms a 60 fps. O piso de 30 fps (frame de 33,3 ms) **não relaxa a tabela**: a 30 fps o frame não tem folga a mais para gastar, tem um tick por frame; o piso é alcançado pelos cortes da Decisão 5, não por orçamento maior.
- **Fora da moeda:** o tempo da GPU e o da thread de render. Ele é limitado pelos tetos estruturais do art bible (draws, triângulos, overdraw) e visto pelo sinal de frames perdidos (Decisão 5). Um frame limitado pela GPU aparece como frame perdido e aciona `High`, que é o efeito certo pelo motivo certo. Como medi-lo no aparelho é `NOT SOURCEABLE` (Verification Required 5 e 9).
- **Taxa do frame (decisão):** o bootstrap fixa `Application.targetFrameRate = 60` e `QualitySettings.vSyncCount = 0`, e o Android liga o "Optimized Frame Pacing" nos Player Settings. Sem isso o padrão do Android pode cair em 30 fps, todo frame viraria "perdido" e o `LoadGovernor` ficaria em `High` para sempre. `NOT SOURCEABLE`: o comportamento exato no 6000.3.27f1 e no aparelho é o Verification Required 2. Em tela de 90 Hz, 60 não é múltiplo e pode gerar alternância de 11 e 22 ms (judder); a taxa para esse caso (45 ou 90) é decisão pendente, medida no aparelho.
- **"Release" quer dizer:** IL2CPP com *C++ Compiler Configuration* em Release (ou Master) e **Development Build desligado** para o aceite. Para ver o Profiler no aparelho, Development Build + IL2CPP + Release; os números do Profiler não valem como aceite, só apontam onde olhar.
- **Cenário único `BENCH-HEAVY`** (o ID que o `docs/acceptance/mvp.md` nomeia como a "fase mais pesada"): 300 vivos de horda e 200 pendentes, 3 avisos simultâneos, elite e chefe presentes, 150 cartões aliados, e as três situações de pico do GDD #7 (AC-P1) **cada uma como um trecho medido à parte**: o tick do rugido (300 mortes), a escolta e **20 nascimentos por tick sustentados**. **Todo número da tabela, o X1, o X3, o X6 e o N são medidos neste mesmo cenário**, no protocolo do #2 (L598), com soak de 5 minutos e leituras no **minuto 20** de sessão contínua. Um sistema não escolhe o cenário em que se mede. O p95 e o p99 de cada linha valem **em cada trecho**, não só na média da fase.
- **Critério do frame inteiro** (o que verifica o total `T`): seja `A_f` o tempo ativo da thread principal do frame `f` (que **inclui** o `Tick`). Nos frames com tick, `R_f = A_f − (soma dos totais de Tick medidos pela sonda nesse frame)`, e `R_p95` é o p95 de `R_f`. **Aceite do frame: p95 de `A_f` nos frames com tick ≤ `T − L10` = 9,5 ms, e p99 ≤ `T` = 12,0 ms.** A reserva L10 **não é gasta**: ela é a folga que o p99 pode consumir. Passar de 9,5 no p95 consome a reserva e dispara a escada de gatilhos da Decisão 2. O casamento entre os tempos do `FrameTimingManager`, que chegam com alguns frames de atraso, e o `Tick` do mesmo frame usa o número de frame que o próprio `FrameTimingManager` devolver; se ele não devolver (`NOT SOURCEABLE`), `R_p95` é calculado por janela de 2 s e o aceite registra a perda de precisão.

### 2. A tabela de alocação (`FrameLedger`)
Cada linha tem um dono. Valores em ms, **todos provisórios**; a coluna "Origem" separa o que vem de GDD do que é palpite deste ADR.

| # | Linha | Dono | p95 | p99 | Pior tick | Origem |
|---|---|---|---|---|---|---|
| L1 | `Tick`: Combate | GDD #6 | 2,0 | 4,0 | 5,0 | #6 (p95, p99); pior tick novo (fecha `orcamento_combate_pior_tick_ms`) |
| L2 | `Tick`: Horda | GDD #7 | 0,3 | 0,5 | 1,0 | #7 (p95 e p99, **também** no tick do rugido, na escolta e com 20 nascimentos por tick: o pior tick de 1,0 é só o teto do máximo, o GDD não o define, e **não relaxa** o p95 e o p99) |
| L3 | `Tick`: Fluxo e XP | GDD #3 | 0,3 | 0,6 | 1,0 | palpite (passo O(1) + O(mortes), 300 mortes no pior) |
| L4 | `Tick`: Núcleo (resíduo: `Tick` total − soma dos slots) | ADR-0001 | 0,2 | 0,4 | 0,5 | palpite |
| L5 | `Tick`: reserva da simulação (sistemas sem GDD ainda) | `technical-director` | 0,2 | 0,5 | 0,5 | palpite |
| | **X1 = soma do `Tick`** | | **3,0** | **6,0** | **8,0** | |
| L6 | Apresentação na CPU (`OnTick`, `RenderFrameBuilder`, upload da textura de instância) | ADR-0009 / GDD #12 | 2,0 | 3,0 | | palpite |
| L7 | Motor, URP e envio de draws (o "resto" que não é código nosso) | medido, não alocado | 3,0 | 4,0 | | palpite |
| L8 | UI e HUD | GDD #12, #13 | 1,0 | 1,5 | | palpite |
| L9 | Entrada, áudio, log e outros | vários | 0,5 | 1,0 | | palpite |
| L10 | Reserva térmica e de variância | `technical-director` | 2,5 | | | palpite |
| | **Soma dos p95 (L1 a L10)** | | **12,0** | | | `= T` |

**Regras da tabela:**
- A soma dos p95 **deve ser ≤ T**. `FrameLedger` é uma tabela imutável em código (`Forja.Gameplay.Sim.Budget`, C# puro) e um teste de EditMode afirma `Σ p95 ≤ T`, que cada linha tem dono e que `X1` é a soma de L1 a L5.
- **A soma dos p95 é um limite conservador, não o p95 da soma.** O **aceite** é sobre o X1 e o frame **medidos** no `BENCH-HEAVY`, não sobre as parcelas. Cada parcela medida também deve caber na sua linha, para apontar quem estourou.
- **Sistema sem linha não tem tempo, e isso é imposto na criação.** Cada `ISimSystem` declara o id da sua linha (`int BudgetLine`, de L1, L2, L3 ou L5; L4 é o resíduo e nenhum sistema a declara). `Simulation.Create` **lança** se algum sistema declarar um id inválido ou ausente. A linha não depende da posição em `systemsInExecutionOrder`, então reordenar a lista não troca linhas. Um sistema novo pede a sua linha tirando de L5 (simulação) ou de L10 (resto), por Emenda a este ADR; tirar de L10 exige o `technical-director`.
- **R = L6 + L7 + L8 + L9 = 6,5 ms (p95)** é o "resto do frame fora do `Tick`", com `R_f` definido na Decisão 1. A definição do #2 (P1) de X1 como "orçamento do frame menos o p95 do resto do frame" vale com a reserva: **X1 final = (T − L10) − R_p95 medido = 9,5 − R_p95**. Se o R medido for maior que 6,5, o X1 encolhe e a escada de gatilhos abaixo roda.
- **Eventos únicos fora da soma** (custo que acontece uma vez, num frame sem tick): **X6, o hash do fim da fase, ≤ 2,0 ms** (o hash não roda por tick no jogo; ADR-0008); a entrada na fase tem orçamento próprio (Decisão 6).
- **N** do #2 (P4) = `teto_vivos_horda` do #7 (300 vivos) mais os 200 pendentes do cenário; a fase sustenta 30 ticks por segundo com **zero ticks descartados**.
- **Alocação gerenciada: 0 B por frame** a partir do primeiro tick (ADR-0001, ADR-0007, ADR-0009); é uma linha da tabela com limite 0, não um ms.
- **Escada de gatilhos quando a soma medida passa de T** (nesta ordem, sem pular): (1) reduzir a apresentação pelos botões do ADR-0009 (`ALLY_CARD_MAX`, alfa, `GHOST_POOL_MAX`); (2) reduzir `teto_vivos_horda` com o autor; (3) reabrir a taxa de 30 Hz do ADR-0001 (alternativa de 20 Hz); (4) reabrir o alvo de 60 fps com o autor. **Nunca** se resolve estourando o total.

### 3. Medição: `ITickProbe` e histogramas
- A simulação não pode referenciar a engine (ADR-0001), então ela não usa `ProfilerMarker`. Ela chama uma interface **escrita só no sentido de saída**:
  - `ITickProbe { void Begin(int slot); void End(int slot); }`, com `TotalSlot = 0` e **o slot de cada sistema = o `BudgetLine` que ele declara** (1, 2, 3 ou 5), não o índice na lista. `Simulation.Tick` chama `Begin(TotalSlot)` no começo e `End(TotalSlot)` no fim, e o par de cada `ISimSystem.Step`. Vários sistemas na mesma linha **somam** dentro do tick: a sonda acumula a duração por slot e, no `End(TotalSlot)`, joga o acumulado de cada slot no seu histograma (uma amostra por slot por tick). L4 é o total menos a soma dos slots. O **marcador `Horda.Tick`** que o GDD #7 pede é o slot da linha L2; não há `ProfilerMarker` na simulação.
  - **A sonda nunca lança exceção dentro do `Tick`:** um `Begin`/`End` desbalanceado é ignorado e conta em `ProbeFaults`.
  - `NullTickProbe` (o padrão, para testes e headless): não faz nada. `StopwatchTickProbe` (em `Forja.Gameplay.Sim.Budget`, sem `UnityEngine`): lê `ITimestampSource.Now()` (a implementação do jogo devolve `Stopwatch.GetTimestamp()`; o teste usa uma fonte falsa, como o `FakeRelogio` do ADR-0007), e acumula a duração em um `LatencyHistogram` por slot.
- `LatencyHistogram`: contagens em **bins de tamanho fixo de 0,01 ms até 20 ms** (2000 `int`, ≈ 8 KB), mais um bin de excedente e o máximo exato; `Add` é O(1); `Percentile(p)` varre os bins; criado na tela de carregamento; **zero alocação** depois. Não há ordenação nem lista de amostras. A conversão de `Stopwatch` ticks para ms usa `long`/`double`, nunca `float`. Bins de 0,1 ms seriam grossos demais para L2 (p95 de 0,3 ms, erro de ±33%).
- **Exceção declarada a uma postura do registro.** `api_decisions: real_time_source` (ADR-0007) proíbe "qualquer relógio de parede dentro do `Tick` ou de um `ISimSystem`". A sonda lê o relógio (por `ITimestampSource`, fora do assembly da simulação) enquanto o `Tick` roda. Isto **não supersede** aquela postura: é uma exceção estreita, de **medição só de saída**. O relógio nunca devolve valor à simulação, nenhum sistema lê a sonda, e o hash é idêntico com a sonda ligada ou desligada (teste de contrato). Qualquer outro uso de relógio de parede dentro do `Tick` continua proibido.
- **A sonda nunca é lida pela simulação.** O que ela mede sai apenas por `ICounterSource` (ADR-0008) e pelo relatório do spike. Com a sonda ligada ou desligada, **o hash da simulação é idêntico** (teste de contrato).
- **Contadores no log (#5)**, ids próprios num enum de valores explícitos que só cresce: `TickP95Us = 1`, `TickP99Us = 2`, `TickMaxUs = 3`, `CombateP95Us = 4`, `HordaP95Us = 5`, `FluxoP95Us = 6`, `FramesMissed = 7`, `FramesTotal = 8`, `LoadHighSeconds = 9`, `FloorBreachedWindows = 10`, `EntryMs = 11`, `HashEndUs = 12`, `ProbeFaults = 14`, `GcCollections = 13` (a diferença de `GC.CollectionCount(0)+(1)+(2)` entre o primeiro tick e o fim da fase; a invariante barata de "nenhuma coleta durante a fase" em Release, sem Profiler; deve ser 0). Servem ao aceite e ao spike; não influenciam nada.
- O `ProfilerMarker` e o Profiler do Unity são **ferramentas de spike** em build de desenvolvimento, para olhar o motor e a thread de render (L7); o jogo não depende deles.

### 4. O tick de recuperação e o `MaxTicksPerFrame`
- Depois de um engasgo, o frame executa até `k = MaxTicksPerFrame` ticks de uma vez (ADR-0007, FS1). Esse frame é ruim por definição, mas **não pode ele mesmo virar um novo engasgo**:
  `k × X1_p99 + R_p95 ≤ 33,3 ms`
- Com a Tabela provisória: `4 × 6,0 + 6,5 = 30,5 ≤ 33,3` (folga de 2,8 ms). **O `MaxTicksPerFrame = 4` do ADR-0001 e do ADR-0007 fica como está, condicionado a esta desigualdade com os números medidos** (GDD #2, P5, mede com engasgos de 100 e 300 ms).
- Se a desigualdade falhar com os números medidos, **baixa-se o `k`** (o jogo fica mais lento depois do engasgo), **nunca se sobe o X1**.
- **Pior tick** isolado (o tick do rugido, 300 mortes e 3 avisos): `WORST_TICK_MS = 8,0` *(provisório)*, derivado de `16,6 − R_p95 (6,5) − 2,0 de folga`, de modo que um tick pesado sozinho caiba num frame de 16,6 ms. A coluna "Pior tick" da Tabela reparte esse 8,0; L1 = 5,0 fecha o valor que o GDD #6 deixou indefinido (`orcamento_combate_pior_tick_ms`).

### 5. `LoadLevel` dinâmico: `LoadGovernor`
- **Sinal:** o `dt` saneado do frame (`DtUsed`, Emenda B do ADR-0007: o `dt` depois do tratamento de NaN, negativo, infinito e do descarte do 1º `dt`, **antes** do corte `dt_ef = min(dt, (Max+1) × TickSeconds)` da FS1, para que um engasgo de 250 ms apareça inteiro), já lido pelo `PhaseHost` pelo `IFrameClock`. É o intervalo do frame anterior, então o `LoadGovernor` tem 1 frame de atraso (aceito). Frames com `dt ≤ 0` (pausa, 1º `dt` descartado, volta do segundo plano) **não contam**.
- **Frame perdido:** `dt > MISS_FACTOR × FRAME_TARGET_S`, com `FRAME_TARGET_S = 1/60` e `MISS_FACTOR = 1,5` (25 ms) *(provisório)*. Um aparelho que só segura 30 fps perde todos, e isso está certo: é o aparelho para o qual `High` existe.
- **Janela** `WINDOW_S = 2,0` de `dt` acumulado. No fim de cada janela: `frac = perdidos / total`.
  - `Normal → High` quando `frac ≥ 0,10` em **2 janelas seguidas**.
  - `High → Normal` quando `frac ≤ 0,02` em **5 janelas seguidas** (10 s).
  - A cada troca o `LoadGovernor` não troca de novo antes de uma janela completa. *(Todos provisórios.)*
- **Piso:** em `High`, se mais de 5% dos frames de uma janela passarem de `36,7 ms` (1,1 × 33,3), a janela conta em `FloorBreachedWindows`. Não há terceiro nível: não resta o que cortar. **`FloorBreachedWindows > 0` no `BENCH-HEAVY` reprova o aparelho no spike.**
- **O que `High` corta** (a apresentação só; todos os cortes são do ADR-0009 ou do art bible, aqui só se liga o gatilho): (a) a sombra do herói e do chefe vira blob (art bible: "a sombra é o primeiro corte no piso de 30 fps"; dono: GDD #12); (b) a horda perde flash e dissolve e vira fade (ADR-0009, Decisão 6, corte 1); (c) os cartões aliados caem para metade de `ALLY_CARD_MAX` (corte 2, escalado). **Telegraph e herói nunca são cortados.**
- **Quem lê:** só a apresentação, uma vez por frame, no `LateUpdate`, e entrega ao `VfxBudget.Grant(request, caps, level)` do ADR-0009. `LoadGovernor` é C# puro, não referencia a engine, roda em EditMode com sequências de `dt`, e **não aloca** (só contadores).
- **Nunca entra na simulação.** O `LoadLevel` depende do relógio real e é não determinístico; **nenhum sistema de tick, nenhum comando e nenhuma regra de jogo o lê**. Ele não entra no hash nem no log como estado (só os contadores e uma `HostNote LoadLevelChanged`, Emenda C).
- **Sinal alternativo (plano B):** se o Verification Required 3 mostrar que o `dt` não acusa a perda, o `LoadGovernor` recebe os tempos do `FrameTimingManager` (Verification Required 5; exige "Frame Timing Stats" ligado e chamada a `CaptureFrameTimings` todo frame, `NOT SOURCEABLE`) no lugar do `dt`, sem mudar a regra. Os resultados chegam com alguns frames de atraso, o que não importa para uma janela de 2 s.

### 6. Entrada na fase: orçamento de carregamento
- **Janela:** do toque em Entrar (estado *Entrando* do #3) até o **primeiro `Tick`**. Dentro dela, em ordem: o `BeginStage` (commit do #28; ADR-0003) **em paralelo** com o `PrewarmPlan` (ADR-0009, Seção 8; espera máxima `PREWARM_MAX_WAIT_MS` = 3000); depois `Simulation.Create`, `Preparar` e a alocação de todos os arrays e histogramas da fase.
- **Orçamento:** `ENTRY_P95_MS = 4000` e `ENTRY_MAX_MS = 6000` *(provisórios)*: carga dos assets e pré-aquecimento até 3000, `Create` + `Preparar` + alocação até 500, folga 500. O `EntryMs` vai ao log; `p95 > ENTRY_P95_MS` reprova o aceite.
- **Duas coisas distintas no pré-aquecimento do ADR-0009, que esta Decisão separa:** (i) a **residência dos assets** do plano (passos 1 e 3 do `PrewarmPlan`: modelo, materiais, texturas e perfil de Volume do chefe), que é **obrigatória**; (ii) o **aquecimento** (compilar variantes de shader, desenhar o chefe fora da tela, decodificar o áudio do rugido; passos 2, 4 e 5), que é **melhor-esforço**.
  - O teto `PREWARM_MAX_WAIT_MS` (3000) do ADR-0009 **vale só para (ii)**: passado o teto, a fase começa e o aquecimento continua em segundo plano, com `PrewarmIncomplete` no log, como o ADR-0009 manda. **(i) nunca continua depois do primeiro `Tick`.**
  - A janela termina quando (i) terminou **e** ((ii) terminou **ou** passou o teto). Se (i) não terminar até `ENTRY_MAX_MS` (6000), a entrada **falha**: a `TentativaDeFase` recebe a falha de carga e a fase não começa (o que o #3 faz com ela é a pergunta aberta do GDD Sync). A fase nunca começa com um asset obrigatório ainda carregando.
  - Isso exige uma **Emenda ao ADR-0009, Seção 8** (Ordering Note E): "a carga continua em segundo plano" passa a valer só para o aquecimento, não para a residência dos assets.
- **Regra de alocação:** **toda** alocação de fase (arrays do `SimWorld`, textura de instância, pools, histogramas, buffers do log) **acontece dentro da janela**; **nenhuma depois do primeiro `Tick`**. O `PrewarmRunner` pode alocar (ADR-0009), mas só enquanto roda (i) e o aquecimento (ii) em segundo plano **não pode alocar no caminho quente do frame**; a alocação de máquina de estado do aquecimento tardio é a única exceção, e fica contada em `GcCollections` (deve ser 0 em regime).
- **Residente não é pronto para desenhar.** O upload de textura pode ser assíncrono e o primeiro desenho compila shader e estado de pipeline (`NOT SOURCEABLE`). Por isso (ii) existe e por isso a janela espera por ele até o teto. Nunca se usa espera síncrona (`WaitForCompletion`) em carga.
- **Escopo desta Decisão:** só o orçamento e as regras de carga e alocação. O layout de grupos do Addressables e a carga remota não são tratados aqui.
- **Regra de carga:** todo asset obrigatório da fase fica **residente antes do primeiro `Tick`**. Carga **assíncrona** (Addressables), nunca síncrona; `Resources.Load` **proibido** (`deprecated-apis.md`). A falha de carga lança no 6.2+ (`breaking-changes.md`): o carregador captura e entrega o resultado à `TentativaDeFase` (o que fazer é do #3; **pergunta aberta**). Os `AsyncOperationHandle` são guardados por quem carrega e liberados no `Discard` da fase; `Addressables.Release` em todos.
- **Fora do escopo:** o layout dos grupos do Addressables (a referência local o descreve para conteúdo remoto, e o jogo é offline) é do ADR de pipeline de assets, quando existirem assets. Se a falha de carga lança no 6.2+, o carregador a captura (acima); o que a `TentativaDeFase` faz é do #3.

### 7. Livro de memória
- **Dono:** este ADR mantém a tabela; cada ADR e GDD declara a sua linha. Hoje só há linhas **sourceadas**: texturas da horda ≤ 2 MB e de VFX ≤ 4 MB (art bible 8.4); buffers do log 2 × 1 MiB + 64 KiB (ADR-0008, Seção 7); textura de instância e arrays de render, "poucos KB" (ADR-0009). Faltam: `SimWorld` e o buffer de eventos (X3 do #2), o snapshot da fase (ADR-0002), o herói e o chefe, o áudio, os atlas de UI.
- **Teto `MEM_CEILING_MB`: `NOT ASSESSED`.** Depende do aparelho de referência e da métrica de memória residente no Android (Verification Required 8), nenhum dos dois conhecido. **Enquanto não existir, o veredito de memória é `NOT ASSESSED`, nunca `PASS`**: `/architecture-review` e `/gate-check` devem dizer "memória: NOT ASSESSED — sem teto, sem aparelho de referência" e não contar a soma parcial como aprovação. O X3 do #2 (P3) segue "SPEC INCOMPLETO" até lá.
- O livro de memória **não tem código** hoje (a soma parcial seria um número que parece um orçamento); vira tabela em código quando o teto existir.

### Architecture Diagram
```
 Frame (60 fps, T = 12,0 ms, p95, frame com tick)
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ Tick (X1 = 3,0)                       │ resto R = 6,5                      │ reserva 2,5 │
 │ L1 Combate 2,0 | L2 Horda 0,3         │ L6 Apres. 2,0 | L7 Motor 3,0       │ L10         │
 │ L3 Fluxo 0,3 | L4 Núcleo 0,2 | L5 0,2 │ L8 UI 1,0 | L9 Outros 0,5          │             │
 └───────────────────────────────────────────────────────────────────────────┘
 Simulation.Tick ──Begin/End(slot)──▶ ITickProbe ──▶ LatencyHistogram ──▶ ICounterSource (log #5)   (só saída)
 PhaseHost ──DtUsed──▶ LoadGovernor ──Level (Normal|High)──▶ PresentationDriver ──▶ VfxBudget.Grant   (a simulação não lê)
 Entrada: [tap Entrar] ─(BeginStage ∥ PrewarmPlan)─▶ Create ─▶ Preparar ─▶ alocar tudo ─▶ 1º Tick  (ENTRY_P95 4000 ms)
```

### Key Interfaces
```csharp
namespace Forja.Simulation {                       // sem UnityEngine
    public interface ITickProbe { void Begin(int slot); void End(int slot); }   // TotalSlot = 0; sistema = o BudgetLine que ele declara
    public static class ProbeSlots { public const int Total = 0; }
    public sealed class NullTickProbe : ITickProbe { /* não faz nada */ }
}
namespace Forja.Gameplay.Sim.Budget {              // C# puro, sem UnityEngine
    public interface ITimestampSource { long Now(); long Frequency { get; } }
    public sealed class StopwatchTickProbe : ITickProbe { public StopwatchTickProbe(ITimestampSource src, int slotCount); /* ... */ }
    public sealed class LatencyHistogram {
        public LatencyHistogram(int binCount /*2000*/, double binWidthMs /*0.01*/);
        public void Add(double ms); public double Percentile(double p); public double Max { get; } public void Reset();
    }
    public readonly struct BudgetLine { public readonly int Id; public readonly string Owner; public readonly float P95, P99, WorstTick; }
    public static class FrameLedger { public const float TotalMs = 12.0f; public static int LineCount { get; } public static BudgetLine Line(int i); public static float TickP95Sum(); }
    // LoadLevel NÃO é declarado aqui: é o enum do ADR-0009 em Forja.Gameplay.Sim.View ({ Normal = 0, High = 1 })
    public sealed class LoadGovernor {
        public Forja.Gameplay.Sim.View.LoadLevel Level { get; } public int FloorBreachedWindows { get; }
        public void Add(float dtSeconds);   // dt <= 0 é ignorado
    }
}
```

### Implementation Guidelines
- Nenhum sistema de tick **must** referenciar `Stopwatch`, `Time`, `ProfilerMarker` ou `LoadGovernor`; **must never** ler `ITickProbe`, `LatencyHistogram`, `LoadGovernor.Level` nem qualquer medida de tempo real. A sonda é escrita só no sentido de saída.
- Todo `ISimSystem` **must** declarar o seu `BudgetLine`; `Simulation.Create` **must** lançar para linha inválida; um sistema sem linha **must never** entrar no `systemsInExecutionOrder`. A sonda **must never** lançar exceção dentro do `Tick`.
- `FrameLedger` **must** ter `Σ p95 ≤ T`; mudar um número **must** passar por Emenda a este ADR, atualizar o registro (`revised`) e rodar o teste da soma.
- O aceite de desempenho **must** usar o cenário `BENCH-HEAVY` em Release/IL2CPP no aparelho de referência, com o protocolo do #2 (L598), com leituras no minuto 20; **must never** usar o Editor.
- Alocação e carga **must** acontecer dentro da janela de entrada; **must never** acontecer depois do primeiro `Tick`. Carga **must** ser assíncrona e **must never** usar `Resources.Load`.
- O `LoadLevel` **must** ser lido uma vez por frame, só pela apresentação, e **must never** alterar quantos ticks rodam, o conteúdo da fase, o hash ou um comando.
- O desempenho **must never** degradar a simulação: nem pular tick, nem trocar a taxa, nem reduzir inimigos em execução. O jogo desacelera só pelo `MaxTicksPerFrame`.
- Histogramas, o `LoadGovernor` e a sonda **must** ser criados na tela de carregamento e **must never** alocar por frame; nenhum campo `static` mutável (domain reload desligado hoje; ADR-0007 e ADR-0009).
- Testes em `Assets/Tests/EditMode/Budget/` (`FrameLedger`, `LatencyHistogram`, `LoadGovernor`, `StopwatchTickProbe` com fonte falsa) e `Assets/Tests/PlayMode/` só para o spike de aparelho. C# 9 apenas.

## Alternatives Considered

### Alternative 1: só o total de 12 ms, cada sistema se mede sozinho
- **Description**: fixar T e deixar cada GDD manter o seu número sem uma tabela de soma.
- **Pros**: menos documento; nenhum palpite por linha.
- **Cons**: é o estado de hoje: a soma pode passar de T sem que nada acuse; o X1 do #2 continua sem dono; o #3 depende de um número que ninguém reivindica; cada sistema escolhe o cenário em que se mede.
- **Rejection Reason**: não fecha TR-simulacao-018 nem TR-fluxo-008, e é a causa do "GAP" dos requisitos. A tabela custa pouco e o aceite ainda é sobre o X1 medido.

### Alternative 2: esperar o spike e só então escrever, com números medidos
- **Description**: manter este ADR para depois do spike de performance, como a revisão de 2026-11-06 listou.
- **Pros**: nenhum número chutado.
- **Cons**: os ADRs 0007 e 0009 dependem dele para aceitar (`LoadLevel`, `MaxTicksPerFrame`); as stories de render e de aceite ficam paradas; o spike precisa de um protocolo e de um cenário comuns, que são justamente o que este ADR define.
- **Rejection Reason**: a estrutura (linhas, regras, sonda, desigualdades, `LoadGovernor`, entrada) não depende do número. Escolha do autor (2026-11-06): fixar agora com números provisórios e calibrar no spike por Emenda.

### Alternative 3: orçamento em percentual do frame
- **Description**: cada sistema recebe uma fatia (por exemplo 25%) em vez de ms.
- **Pros**: escala com o aparelho.
- **Cons**: um aparelho lento muda todos os custos em ms, não a fatia; os GDDs #6 e #7 já falam em ms; o piso de 30 fps tornaria a fatia o dobro sem o custo mudar.
- **Rejection Reason**: ms medidos no aparelho de referência são verificáveis; percentuais escondem o que falhou.

### Alternative 4: Adaptive Performance ou `FrameTimingManager` como sinal primário do `LoadLevel`
- **Description**: usar o pacote de desempenho adaptativo da Unity, ou o `FrameTimingManager`, como **a fonte do sinal do `LoadGovernor`** no lugar do `dt`.
- **Pros**: vê CPU e GPU de verdade, não só o frame perdido.
- **Cons**: nenhum dos dois está em `docs/engine-reference/unity/` (`NOT SOURCEABLE`). O pacote é **dependência nova** e pode ser específico de fabricante. O `FrameTimingManager` é **API do próprio motor, não dependência**, mas a disponibilidade e os campos no aparelho de referência são desconhecidos, exige ligar "Frame Timing Stats" e entrega os resultados com atraso.
- **Rejection Reason**: o `dt` já é lido pelo ADR-0007 e não custa nada. A rejeição vale **só para o sinal primário do `LoadGovernor`**. O `FrameTimingManager` continua sendo (a) o **plano B** desse sinal (Decisão 5, gatilho no Verification Required 3) e (b) a fonte **provável** do tempo ativo `A_f` em build de aceite (Decisão 1, gatilho no Verification Required 5). O pacote de desempenho adaptativo fica rejeitado.

### Alternative 5: degradar a simulação sob carga
- **Description**: reduzir inimigos vivos, baixar a taxa de tick ou pular sistemas quando o frame passa do limite.
- **Pros**: alivia a CPU na hora.
- **Cons**: contradiz o GDD #2 (Regra 11: o jogo desacelera, nunca pula nem muda o conteúdo da fase por desempenho), quebra a reprodutibilidade por seed e o hash, e faria o desempenho do aparelho decidir o resultado do jogo.
- **Rejection Reason**: só a apresentação corta. A escada de gatilhos reabre os GDDs com o autor, não degrada em silêncio.

### Alternative 6: `ProfilerMarker` dentro da simulação
- **Description**: marcar cada sistema com `ProfilerMarker` e medir pelo Profiler.
- **Pros**: integra-se às ferramentas da Unity.
- **Cons**: `Forja.Simulation` não pode referenciar a engine (critério A1 do #2); o Profiler exige build de desenvolvimento, e o aceite do #2 é em Release/IL2CPP; o resultado não sai para o log (#5).
- **Rejection Reason**: a interface `ITickProbe` mantém a simulação limpa e mede em Release; o `ProfilerMarker` fica como ferramenta de spike para o resto do frame.

### Alternative 7: `LoadLevel` contínuo ou com mais níveis
- **Description**: vários níveis de qualidade, ou um fator de 0 a 1.
- **Pros**: degradação mais suave.
- **Cons**: o ADR-0009 definiu dois níveis e a política de corte por prioridade para dois; mais níveis exigem mais tabelas de tetos e mais testes para um dev solo; o sinal (frames perdidos) não distingue graus.
- **Rejection Reason**: YAGNI. Reabrir só se o spike mostrar que dois níveis oscilam ou cortam demais.

### Alternative 8: jogo fixo em 30 fps
- **Description**: alvo único de 30 fps, frame de 33,3 ms.
- **Pros**: dobra o orçamento por frame; menos cortes.
- **Cons**: a preferência técnica e o game concept pedem 60 fps; o piso de 30 já existe; um alvo de 30 fps escolhido agora é decisão de sensação de jogo, do autor.
- **Rejection Reason**: é o último degrau da escada de gatilhos (Decisão 2), não o ponto de partida.

## Consequences

### Positive
- O X1, o X6, o N e o `orcamento_combate_pior_tick_ms` ganham valor e dono; TR-combate-012, TR-horda-013, TR-simulacao-018 e TR-fluxo-008 passam a ter ADR.
- A soma é verificável por teste e por `/architecture-review`; o `performance_budgets` do registro sai do vazio.
- A medição funciona em Release/IL2CPP sem Profiler e sem tocar a simulação nem o hash.
- Os ADRs 0007 e 0009 perdem o "NOT ASSESSED"; o `LoadLevel` tem regra, histerese e piso.
- A entrada na fase tem teto, e a regra "tudo alocado antes do 1º tick" protege o zero alocação.
- O spike ganha protocolo e cenário únicos; sua saída é uma Emenda de calibração, não um novo ADR.

### Negative
- A maior parte dos números da Tabela (L3 a L10, o pior tick, `T`) é palpite deste ADR: pode ser trocada por inteiro no spike.
- Uma soma de p95 não é o p95 da soma; a tabela é conservadora e o aceite é sobre o medido, o que exige manter os dois.
- O sinal de frames perdidos só acusa quando já houve engasgo visível; não vê a folga se esgotando.
- Cinco tipos novos (`ITickProbe`, `StopwatchTickProbe`, `LatencyHistogram`, `FrameLedger`, `LoadGovernor`) e um parâmetro novo em `Simulation.Create` para um dev solo manter.
- A memória fica sem veredito até existir um aparelho de referência.

## Risks
- **R mais alto que 6,5 ms (URP mobile pesado):** então o X1 encolhe e o #6 e o #7 não cabem. Mitigação: a escada de gatilhos da Decisão 2; o L7 é medido como resto, não alocado.
- **`dt` suavizado ou travado em vsync não acusa a perda:** o `LoadLevel` ficaria sempre `Normal`. Mitigação: Verification Required 3 (provocar a perda) e o plano B `FrameTimingManager`.
- **Tela de 90 ou 120 Hz:** sem `targetFrameRate`, o `dt` seria 8 a 11 ms e a regra de "perdido" (25 ms) ficaria frouxa; em 90 Hz, 60 fps não é múltiplo e alterna 11 e 22 ms. Mitigação: a Decisão 1 fixa `targetFrameRate = 60` e `vSyncCount = 0`; a taxa para telas de 90 Hz fica pendente e medida (Verification Required 2).
- **Custo da sonda:** 2 leituras de relógio por slot por tick (≈ 12 por tick) mais um `Add`. Estimativa, não medida: Verification Required 1 exige ≤ 0,05 ms no p95, senão a sonda sai do jogo e fica só no spike.
- **Estrangulamento térmico:** o número do minuto 0 não vale. Mitigação: leituras no minuto 20 e a reserva L10.
- **Oscilação `Normal`/`High`:** a histerese (2 janelas para subir, 5 para descer) e a janela mínima evitam; os números são chute e o contador `LoadHighSeconds` expõe o problema.
- **GC durante a fase:** uma coleta no meio da fase estoura o frame. O GC incremental não evita o estouro (marcação e coleta ainda rodam na thread principal), e as alocações que escapam costumam vir da engine (UI, Input, Addressables, logs, strings). Mitigação: zero alocação a partir do primeiro tick, e o contador `GcCollections` = 0 como invariante em Release (Verification Required 4). Desligar o GC durante a fase (`GarbageCollector.GCMode`) e coletar no fim da janela de entrada é uma defesa possível, com risco de falta de memória se algo vazar; é **decisão pendente** do dono do modo de GC, fora deste ADR.
- **Tempo ativo de R indisponível em Release:** sem o `FrameTimingManager`, R só se mede em build de desenvolvimento. Mitigação: o gatilho do Verification Required 5; o X1 continua medido por `Stopwatch` em Release.
- **Falha de carga na entrada** (um asset obrigatório não fica residente até `ENTRY_MAX_MS`, ou o Addressables lança): a fase não começa e a `TentativaDeFase` recebe a falha; o que o jogador vê e se há nova tentativa é do #3 (pergunta aberta, GDD Sync).

## GDD Requirements Addressed

| GDD System | Requirement | How This ADR Addresses It |
|------------|-------------|--------------------------|
| combate-e-dano.md (#6) | `orcamento_combate_ms` (L527, AC-P1): p95 ≤ 2,0 ms e p99 ≤ 4,0 ms com 300+ vivos e 3 avisos; pior tick (300 mortes + 3 avisos) ≤ `orcamento_combate_pior_tick_ms` (indefinido) (TR-combate-012) | L1 da Tabela (2,0 / 4,0 / pior tick 5,0 ms, provisório); cenário `BENCH-HEAVY`; medido pela sonda |
| horda-waves-e-inimigos.md (#7) | `orcamento_horda_ms` (L579, AC-P1): p95 0,3 ms e p99 0,5 ms com 300 vivos e 200 pendentes (TR-horda-013) | L2 da Tabela (0,3 / 0,5 / pior tick 1,0 ms); mesmo cenário |
| simulacao-deterministica.md (#2) | P1 (X1), P3 (X3), P4 (N e zero ticks descartados), P5 (`MaxTicksPerFrame`), P6 (pior tick e X6), zero alocação (TR-simulacao-018) | X1 = 3,0 ms (soma L1 a L5); X6 = 2,0 ms; N = 300 + 200; desigualdade do tick de recuperação para o P5; zero alocação como linha da Tabela; **X3 fica `NOT ASSESSED`** (livro de memória) |
| fluxo-de-fase.md (#3) | P1: p95 do passo do #3 dentro do orçamento do #3 (X1 do #2) (TR-fluxo-008) | L3 da Tabela (0,3 / 0,6 / 1,0 ms) dentro do X1; orçamento de entrada na fase |
| ADR-0009 (dependência) | `LoadLevel` dinâmico e o teto de memória "do ADR de orçamento de frame" | Decisão 5 (`LoadGovernor`, o que `High` corta) e Decisão 7 (livro de memória, teto `NOT ASSESSED`) |

## Performance Implications
- **CPU**: por tick, ≈ 12 leituras de relógio e 6 `Add` nos histogramas (estimativa, não medida; Verification Required 1); por frame, O(1) no `LoadGovernor`; sem alocação. A Tabela é o orçamento, não custo extra.
- **Memory**: 6 histogramas de 2000 `int` (≈ 48 KB), criados na entrada; o livro de memória não aloca nada.
- **Load Time**: a janela de entrada é limitada a `ENTRY_P95_MS` 4000 e `ENTRY_MAX_MS` 6000 (provisórios).
- **Network**: não se aplica.

## Migration Plan
Não há código de jogo hoje (`Assets/` só contém o modelo inicial do Unity). Ordem: (1) `LatencyHistogram`, `FrameLedger`, `LoadGovernor`, `NullTickProbe` e `StopwatchTickProbe` com fonte falsa, em EditMode; (2) as Emendas A e B (o parâmetro `probe` em `Simulation.Create` e `DtUsed` no `Plan`) junto das primeiras stories de #2 e do host; (3) os contadores no log (Emenda C) e o enum de ids; (4) a ligação do `LoadGovernor` ao `PresentationDriver` e ao `VfxBudget`; (5) **o spike**: `BENCH-HEAVY` no aparelho, calibração da Tabela, de `WINDOW_S` e dos limiares, e o teto de memória; sai uma **Emenda de calibração** a este ADR e a entrada `performance_budgets` do registro com `revised`.

## Validation Criteria
- `FrameLedger`: `Σ p95 ≤ T` (12,0); X1 = soma de L1 a L5; toda linha com dono; mudar um valor sem atualizar o teste falha.
- `LatencyHistogram`: percentis corretos em entradas conhecidas, `Max`, bin de excedente, zero alocação.
- `LoadGovernor`: 60 fps estáveis ficam em `Normal`; ≥ 10% de frames perdidos em 2 janelas seguidas sobem para `High`; ≤ 2% em 5 janelas descem; `dt ≤ 0` não conta; não troca duas vezes numa janela; `FloorBreachedWindows` conta só em `High`; zero alocação.
- **Determinismo**: mesma seed e mesmos comandos dão o **mesmo hash** com `NullTickProbe` e com `StopwatchTickProbe`.
- `StopwatchTickProbe`: pares `Begin`/`End` balanceados, duração correta com fonte falsa, slots independentes.
- `Simulation.Create`: lança para um sistema com `BudgetLine` inválido ou ausente; reordenar `systemsInExecutionOrder` não troca a linha medida; dois sistemas na mesma linha somam na mesma amostra por tick. `StopwatchTickProbe`: `Begin`/`End` desbalanceado não lança e conta em `ProbeFaults`.
- **No aparelho**, em Release/IL2CPP (Development Build desligado), `BENCH-HEAVY` (incluindo os trechos do rugido, da escolta e dos 20 nascimentos por tick), ≥ 20 execuções, minuto 20:
  - **frame inteiro:** p95 de `A_f` nos frames com tick ≤ 9,5 ms e p99 ≤ 12,0 ms (Decisão 1); `R_p95` calculado como na Decisão 1;
  - p95 de X1 ≤ 3,0 ms e cada linha dentro da sua, **em cada trecho** (a horda ≤ 0,3 p95 e ≤ 0,5 p99 também no rugido, na escolta e nos 20 nascimentos); pior tick ≤ 8,0 ms;
  - `k × X1_p99 + R_p95 ≤ 33,3 ms` com o `MaxTicksPerFrame` escolhido; `FloorBreachedWindows = 0`; zero ticks descartados em regime;
  - **buffer de eventos:** a capacidade cobre o pior tick medido, com `DroppedEvents` = 0 (P6 do #2; o valor de `event_capacity` segue dos ADRs 0001 e 0005);
  - **alocação:** 0 B de GC por frame depois do primeiro tick medido pelo Profiler **em Development Build** (o P2 do #2 pede o Profiler, que exige esse build) e `GcCollections` = 0 **em Release**;
  - `EntryMs` p95 ≤ 4000 e a residência dos assets completa antes do primeiro tick; a sonda custa ≤ 0,05 ms no p95.
- **Se o `FrameTimingManager` não der o tempo ativo** (Verification Required 5): `A_f` e `R` só passam no aceite medidos em Development Build com o Profiler, e isso fica registrado na Emenda de calibração; o X1 continua medido em Release pela sonda.
- **Memória: `NOT ASSESSED`** até haver aparelho e teto; nunca `PASS`.
- **A story de aceite de desempenho não fecha sem a evidência do spike** (Test Evidence de integração), mesmo que o ADR seja aceito antes.

## Related
- Depende de ADR-0001, ADR-0007, ADR-0008 e ADR-0009 (todos `Proposed`). Pede emendas ao ADR-0001 (`ITickProbe` em `Simulation.Create`), ao ADR-0007 (`DtUsed` no `Plan`), ao ADR-0008 (ids de contador, `NoteKind.LoadLevelChanged = 9`) e ao ADR-0009 (Decisão 6: `LoadLevel` real); ver Ordering Note.
- Abre uma exceção estreita (medição só de saída) a `api_decisions: real_time_source` do ADR-0007; ver a Decisão 3.
- ADR-0003 (o `BeginStage` é uma linha da entrada na fase) e ADR-0002 (o snapshot é uma linha do livro de memória): sem dependência de aceite.
- Candidatas de registro a apresentar depois de gravar: `performance_budgets` (o total e as linhas L1 a L10); interfaces `tick_probe` (`ITickProbe`) e `load_governor`; `state_ownership` do `LoadLevel`; `api_decisions` de fonte do sinal de carga e de medição em Release; `forbidden_patterns` (`sim_reads_realtime_measure`, `perf_degrades_simulation`, `system_without_ledger_line`, `alloc_after_first_tick`, `sync_load_in_phase`).
- GDDs: `design/gdd/simulacao-deterministica.md` (#2), `fluxo-de-fase.md` (#3), `combate-e-dano.md` (#6), `horda-waves-e-inimigos.md` (#7); `design/art/art-bible.md` (Seção 8.4 e a sombra no piso de 30 fps).
- `docs/architecture/architecture-review-2026-11-06-2.md` (Required ADRs, item 2); `docs/architecture/requirements-traceability.md` (TR-combate-012, TR-horda-013, TR-simulacao-018, TR-fluxo-008).

## GDD Sync (pendente; nenhum arquivo foi editado)
- **GDD #6 (L527):** `orcamento_combate_pior_tick_ms` indefinido; este ADR o fixa em 5,0 ms (provisório). O texto "≤ 12% de 33,3 ms" continua válido como faixa segura.
- **GDD #2 (P1, P3, P4, P6):** X1 = 3,0 ms, X6 = 2,0 ms e N = 300 vivos + 200 pendentes são os valores provisórios deste ADR; **X3 continua indefinido** (memória `NOT ASSESSED`). O `docs/acceptance/mvp.md` deve gravar X1, X6 e N **antes** do build de aceite (protocolo L598).
- **GDD #3 (P1, L625):** o orçamento do passo do #3 é a linha L3 (0,3 / 0,6 / 1,0 ms), dentro do X1.
- **GDD #7 (L579, AC-P1, TR-horda-013):** o p95 0,3 e o p99 0,5 valem também no tick do rugido, na escolta e com 20 nascimentos por tick; a linha L2 e o `BENCH-HEAVY` os cobrem como trechos medidos à parte. O "pior tick" de 1,0 ms é só um teto de máximo que o GDD não define. O **marcador `Horda.Tick`** que o AC-P1 pede passa a ser o **slot da sonda da linha L2** (sem `ProfilerMarker` na simulação); o texto do GDD deve dizer "slot `Horda` da sonda".
- **GDD #2 (P2, L591):** manda medir a alocação com o Profiler em Release; o Profiler exige Development Build. Este ADR mede com o Profiler em Development Build **e** com o contador `GcCollections` em Release; o P2 deve registrar a troca.
- **GDD #2 (P6, L595):** a capacidade do buffer de eventos cobrir o pior tick passa a ser critério do `BENCH-HEAVY` (Validation Criteria); o valor de `event_capacity` continua dos ADRs 0001 e 0005.
- **ADR-0009 (Emendas D e E):** `Alto` → `High` em L102; a carga que continua depois do teto passa a valer só para o aquecimento (Seção 8, L137, L198, L211).
- **GDD #12 (a escrever):** passa a consumir o `LoadLevel` e a ser dono do corte "sombra vira blob" e da linha L8.
- **Preferências técnicas (`technical-preferences.md`):** o "Frame Budget ~12 ms" passa a ser o `T` deste ADR; "Draw Calls" e "Memory Ceiling" continuam "TO BE CONFIGURED" até o spike.
- **Pergunta aberta (para o #3 e o autor):** o que a `TentativaDeFase` faz se uma carga de asset falhar na entrada (Decisão 6).

## Decisões provisórias (a reavaliar com o spike e o jogo jogável)
1. `T` = 12,0 ms e todas as linhas L3 a L10, o pior tick (8,0 ms) e o X6 (2,0 ms) (Decisões 1, 2 e 4).
2. `MaxTicksPerFrame` = 4 condicionado à desigualdade do tick de recuperação (Decisão 4).
3. `FRAME_TARGET_S` = 1/60, `MISS_FACTOR` = 1,5, `WINDOW_S` = 2, limiares 0,10 / 0,02 e janelas 2 / 5, piso de 36,7 ms (Decisão 5).
4. O que `High` corta e a ordem (sombra, horda, aliados) (Decisão 5).
5. `ENTRY_P95_MS` = 4000 e `ENTRY_MAX_MS` = 6000 (Decisão 6).
6. A camada **Foundation** (sem `architecture.md`).
7. O sinal do `LoadGovernor` por `dt`, com `FrameTimingManager` como plano B.
8. `targetFrameRate = 60`, `vSyncCount = 0` e o Optimized Frame Pacing; a taxa para telas de 90 Hz.
9. R como tempo ativo medido pelo `FrameTimingManager` em Release e pelo Profiler em Dev Build; o modo de GC durante a fase é decisão pendente, fora deste ADR.
