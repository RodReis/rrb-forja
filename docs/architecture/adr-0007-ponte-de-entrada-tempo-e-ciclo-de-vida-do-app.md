# ADR-0007: Ponte de entrada, tempo e ciclo de vida do app: `AppLifecycle` persistente, `PhaseHost` por fase, `TickPacer` e conjunto de motivos de pausa

## Status
Proposed

## Date
2026-11-06

## Last Verified
2026-11-06 (contra o ADR-0001 com as Emendas 1 a 18, o ADR-0003, `docs/registry/architecture.yaml` e os GDDs #2 (Regras 4, 11, 15 e 16, FS1, FS2), #3 (Regras 11 e 12, bordas e estados) e #28 em disco; Unity 6.3 LTS, pin 6000.3.x)

## Decision Makers
Rodrigo Reis (escolheu este ADR, confirmou as premissas e mandou revisar os pontos do gate em 2026-11-06; o resto é decisão técnica por recomendação, **provisória, a reavaliar com o jogo jogável e depois do spike no aparelho**), Claude Code (autoria), `unity-specialist` (validação, 5.5) e `technical-director` (gate TD-ADR, 5.6; veredito CONCERNS, tratado nesta revisão).

## Summary
O GDD #2 manda a "ponte" decidir quantos `Tick` chamar por frame, entregar `Mover` e as ações discretas, e tratar pausa, segundo plano e foco, mas nenhum ADR diz onde a ponte mora, de onde vem o tempo real, nem como os sinais do app viram "zero ticks" (TR-simulacao-015 sem ADR; TR-simulacao-016 e TR-fluxo-014 parciais). Decidido: um `AppLifecycle` persistente (um por app) que recebe os callbacks do app, é dono do conjunto de motivos de pausa e esvazia a fila do #28; um `PhaseHost` por fase que só roda o laço de ticks; e classes C# puras (`TickPacer`, `PauseGate`) em `Forja.Gameplay.Sim.Host`, testáveis em EditMode, com a FS1 e a FS2, a entrega de `Mover` em todo tick e das ações discretas uma vez, o 1º `dt` descartado, o portão do joystick e a tentativa que nasce Pausada. O foco perdido é um motivo de pausa e não grava.

## Engine Compatibility

| Field | Value |
|-------|-------|
| **Engine** | Unity 6.3 LTS (6000.3.x; editor instalado 6000.3.27f1) |
| **Domain** | Input + Core (laço de frame, tempo e ciclo de vida do app) |
| **Layer** | Core (recomendação do `technical-director` no gate TD-ADR: laço de frame e ciclo de vida do app dependem do Core do ADR-0001 e não de outra feature; a lista de Required ADRs de `architecture-review-2026-11-06.md`, linha 227, dizia Feature; não existe `docs/architecture/architecture.md` nem mapa de camadas, então a camada é **provisória, a reavaliar**) |
| **Knowledge Risk** | HIGH (a linha do engine é HIGH em `VERSION.md`; a superfície do Input System é coberta por `modules/input.md`, mas **`Time.*`, `OnApplicationPause`, `OnApplicationFocus`, `Application.isFocused` e o ciclo de vida do Android não são cobertos por nenhum arquivo de `docs/engine-reference/unity/`**) |
| **References Consulted** | `docs/engine-reference/unity/VERSION.md`, `breaking-changes.md`, `deprecated-apis.md`, `modules/input.md`; ADR-0001 (Emendas 2, 3, 4, 5, 14, Key Interfaces, `L307`), ADR-0003 (Seções 5 e 6, `L186`); GDD #2 (Regras 4, 11, 15, 16; FS1; FS2; bordas "Ponte, dt e pausa"), GDD #3 (Regras 11 e 12; bordas de tempo e pausa; estados), GDD #28. **Não existe `modules/core.md`**: nada do domínio Core foi checado contra um módulo de referência (`NOT SOURCEABLE`) |
| **Post-Cutoff APIs Used** | O pacote Input System (`com.unity.inputsystem`, `EnhancedTouch`) aparece só na fronteira do #4: este ADR consome uma `InputSample` já montada. `Time.unscaledDeltaTime`, `MonoBehaviour.OnApplicationPause`, `OnApplicationFocus`, `Application.isFocused` e `[DefaultExecutionOrder]` são anteriores ao cutoff, mas o **comportamento no 6000.3.27f1 e no Android é `NOT SOURCEABLE`** (Verification Required 1 a 5). O código novo fica em **C# 9** (`VERSION.md`): sem `record struct`, sem namespace com escopo de arquivo, sem `required`. |
| **Verification Required** | (1) `NOT SOURCEABLE`: `OnApplicationPause` e `OnApplicationFocus` chegam na thread principal, entre frames e nunca dentro do laço de ticks (pressuposto (e) do ADR-0001, Verification Required 8). **Gatilho: se falhar, este ADR e o pressuposto (e) do ADR-0001 reabrem** (a Decisão 6 depende dele; não há plano B). (2) `NOT SOURCEABLE`: a ordem e a cobertura dos dois callbacks ao ir para segundo plano e ao voltar no Android, e se ligação, aba de notificação, multi-janela e picture-in-picture disparam um deles ou os dois; o desenho tolera qualquer ordem, e nenhum teste presume uma. (3) `NOT SOURCEABLE`: `Time.unscaledDeltaTime` no 1º frame depois de voltar do segundo plano (embute o tempo ausente? é limitado por `maximumDeltaTime`?); medir também com `Stopwatch.GetTimestamp`; o plano B é trocar a fonte atrás do `IFrameClock` (pressuposto (f) do ADR-0001). (4) `NOT SOURCEABLE`: `Application.isFocused` correto no 1º frame e a cada frame; o `AppLifecycle` reconcilia o `FocusLost` com ele em todo frame, então o valor inicial errado se corrige sozinho (Decisão 3). (5) `NOT SOURCEABLE`: os dois casos do toque na volta: (a) o Android **não** cancela os toques (o dedo apoiado segue apoiado) e (b) o Android **cancela** e o dedo que continua apoiado gera um novo início de toque **depois** do frame que guarda `geracaoDoPortao`, o que abriria o portão sozinho; incluir o `backgroundBehavior` do Input System (que pode resetar o dispositivo ao perder o foco). (6) Zero alocação gerenciada por frame no `Plan` e no `BuildCommands` em IL2CPP. (7) Em tela a 60 Hz e simulação a 30 Hz, a alternância de frames com 0, 1 e 2 ticks não faz a interpolação tremer; avaliar `Application.targetFrameRate` fixo e o Optimized Frame Pacing do Android. (8) `Time.timeScale == 1` o tempo todo (assert em desenvolvimento; os testes restauram o valor no SetUp e no TearDown, porque ele persiste entre execuções com domain reload desligado); o Input System em "Dynamic Update". |

## ADR Dependencies

| Field | Value |
|-------|-------|
| **Depends On** | ADR-0001 (`Proposed`; `Tick(ReadOnlySpan<Command>)`, `DrainEvents`, `SimStatus`, `CombatHold` por leitura, `PhaseSheet.IdDoHeroi`, thread única) e ADR-0003 (`Proposed`; a pausa grava só por `OnApplicationPause`, nunca durante a fase, e a fila de respostas do #28 é esvaziada pela ponte entre frames). **Contrato pendente:** o GDD #4 Input e câmera ainda não existe; a `InputSample` e o `TouchGeneration` (Decisão 4) são o que esta ADR exige dele (ver GDD Sync). Este ADR só pode ser aceito depois do ADR-0001 e do ADR-0003. ADR-0002, ADR-0004, ADR-0005 e ADR-0006: **nenhuma dependência** (o `max_ticks_per_frame` não é remoto e não passa pelo #1). |
| **Enables** | Épico da ponte e do host de fase; GDD #4 Input e câmera (ganha o contrato `InputSample`); GDD #12 (pausa e aviso "toque para continuar" via `PauseGate`); ADR do log (#5) (lê `DroppedTicks`) |
| **Blocks** | Stories da ponte (FS1, FS2, entrega de comandos, portão do joystick, motivos de pausa); TR-simulacao-015 (hoje "BLOQ: ADR"), TR-simulacao-016 e TR-fluxo-014 (hoje "Partial"). |
| **Ordering Note** | Escreva a **Emenda ao ADR-0003** (item 3 da lista de Required ADRs) junto com a aceitação deste: "nunca `Focus`" vale **como gatilho de gravação**, não como motivo de pausa (Decisão 5); e a fila do #28 passa a ser esvaziada pelo `AppLifecycle` (Decisão 3). A medição de `MaxTicksPerFrame` e o orçamento de frame ficam no ADR de orçamento (depois do spike de performance). |

## Context

### Problem Statement
O determinismo do ADR-0001 só vale se o `Tick` receber os comandos certos, no número certo de vezes, e nunca durante uma pausa. Quem faz isso é a ponte, que o ADR-0001 cita (acumulador de tempo, drenagem de eventos, interpolação) mas não especifica. O GDD #2 especifica o comportamento (Regra 4: `Mover` em todos os ticks do frame, ações discretas uma vez no 1º tick, ação segurada em frame de 0 ticks; Regra 11: câmera lenta, pausa, 1º `dt` descartado, portão do joystick só com `CombatHold = 0`; Regra 15: `Mover` zerado até um toque novo depois do `PickOffer`; FS1 e FS2), e o GDD #3 acrescenta o conjunto de motivos de pausa e a tentativa que nasce Pausada. Faltam as decisões de engenharia: onde o código mora, **quem recebe os callbacks do app quando não há fase** (o commit do `BeginStage`, a pausa fora de fase e a fila do #28 acontecem antes de existir simulação), qual propriedade da Unity alimenta o acumulador, em que ordem o frame roda e como tudo é testado sem tela. Há também uma tensão a resolver: o GDD #2 diz que perda de foco vale como pausa, e o ADR-0003 diz "nunca `Focus`".

### Constraints
- ADR-0001: a simulação não tem relógio; o `Tick` nunca lê relógio nem frame; `Simulation` é confinada à thread principal; nenhuma alocação gerenciada por `Tick`; sem `static` mutável; `Simulation.Create` e o `Preparar` rodam na tela de carregamento.
- `api_decisions: sim_time` do registro: `not: Time.deltaTime, Time.time, wall clock` **para a simulação**. A ponte é o único lugar com relógio real.
- ADR-0003: a pausa grava só por `OnApplicationPause`, nunca por `Focus`, e nunca durante a fase; as respostas do #28 voltam numa fila que a ponte esvazia entre frames, na thread principal, **em qualquer momento**, não só na fase.
- GDD #3: `TentativaDeFase` fica no mesmo assembly dos sistemas de tick, em **outro namespace**; ela decide o diálogo de abandono (`PedirAbandono`, `ConfirmarAbandono`) e nasce Pausada se há motivo ativo.
- GDD #2 Regra 11: `MaxTicksPerFrame` inicial 4 (a medir), faixa 1 a 16, não remoto, não passa pelo #1; o jogo desacelera e nunca pula nem muda o conteúdo da fase por desempenho.
- GDD #2 Regra 4: "a lógica de entrega é função pura, como a FS1 e a FS2, para rodar em EditMode". A amostragem do toque é do #4 (Presentation).
- Dev solo, uma pessoa valida: poucas classes, todas pequenas, com teste de EditMode.
- Aparelho móvel: zero alocação por frame na ponte.

### Requirements
- Cumprir TR-simulacao-015 e 016 e TR-fluxo-014 sem mudar o GDD #2 nem o #3.
- A FS1, a FS2, a entrega de comandos e a máquina de pausa testáveis em EditMode, com um relógio falso (o `FakeRelogio` do AC-R11 do #3).
- Uma só fonte de verdade para "o jogo está pausado", com dono que existe também fora da fase.
- O jogo desacelera sem pular e sem usar `Time.timeScale`.
- Nenhum callback do app muda estado da simulação, e nenhum roda dentro do laço de ticks.

## Decision

### 1. Três peças: `AppLifecycle`, `PhaseHost` e a lógica pura
- **`AppLifecycle`** (`Forja.Gameplay`, com Unity): um `MonoBehaviour` **persistente, um por app**, criado na cena de bootstrap antes de qualquer tela. É o **único** receptor de `OnApplicationPause` e `OnApplicationFocus`, o dono do `PauseGate` do app, quem esvazia a fila de respostas do #28 e quem aciona o fluxo de gravação da pausa do ADR-0003. Existe antes, durante e depois de qualquer fase.
- **`PhaseHost`** (`Forja.Gameplay`, com Unity): um `MonoBehaviour` **por fase**, criado depois do `Simulation.Create` e do `Preparar`, destruído no `Discard`. Só roda o laço de ticks: lê `IFrameClock`, pede a `InputSample` ao #4, chama o `TickPacer` e a `Simulation` e expõe o `Alpha` à apresentação. Não recebe callback do app.
- **Lógica pura** em `Forja.Gameplay.Sim.Host` (C# sem `UnityEngine`; o mesmo asmdef da `TentativaDeFase` mas **outro namespace** que o dos sistemas chamados por `ISimSystem.Step`, GDD #3): `PauseGate`, `PauseState`, `TickPacer`, `InputSample`, `IFrameClock`, `IPauseView`. É onde estão a FS1, a FS2, o portão do joystick, os latches das ações e a montagem dos `Command`. Tudo roda em EditMode.
- `MaxTicksPerFrame` é um campo serializado do `AppLifecycle`, validado de 1 a 16 **no início do app**, antes de qualquer `BeginStage` (a validação só no `Awake` do host por fase aconteceria depois do commit do `BeginStage`, com a marca já gravada): em `OnValidate` no Editor, numa checagem de build, e no `Awake` do `AppLifecycle`, que falha o início do app; o construtor do `TickPacer` lança como última barreira e o `Awake` do `PhaseHost` só assere (a Unity só loga a exceção de um `Awake` e o `Update` segue rodando, então ele nunca é a barreira). Não passa pelo #1, não é remoto.

### 2. Tempo real: `IFrameClock`, `Update`, sem `timeScale`
- O laço roda no **`Update`** (uma vez por frame de tela), não no `FixedUpdate` e não no `PlayerLoop` próprio (Alternatives 1 e 2). O acumulador e a FS1 são nossos; a Unity não acumula nada por nós.
- O `dt` vem de `IFrameClock.RealDeltaSeconds`. A implementação padrão devolve **`Time.unscaledDeltaTime`** *(provisória; NOT SOURCEABLE, Verification Required 3)*. A interface existe para que o spike troque a fonte (por exemplo `Stopwatch.GetTimestamp`) sem tocar na FS1, e para o teste usar o `FakeRelogio`.
- **A pausa e a câmera lenta nunca usam `Time.timeScale`** (Alternative 3): a pausa é "zero chamadas de `Tick`"; a câmera lenta é o descarte do excedente da FS1. `Time.timeScale` fica em 1, com assert em desenvolvimento.
- A FS1 e a FS2 valem como estão no GDD #2 (`dt_ef`, `n_devido`, `n`, `acum_novo`, `alfa`); o ADR não as redefine. `dt` NaN, negativo ou infinito vira 0.
- Ordem entre os dois hosts: `AppLifecycle` com `[DefaultExecutionOrder(-200)]` e `PhaseHost` com `[DefaultExecutionOrder(-100)]`, para o app reconciliar a pausa e esvaziar a fila antes do laço de ticks. A apresentação lê no `LateUpdate`.

### 3. Conjunto de motivos de pausa: `PauseGate`, `PauseState` e `IPauseView`
- `PauseReason` é um `[Flags] enum : uint` com valores explícitos (só cresce no final): `None = 0`, `AppPaused = 1`, `FocusLost = 2`, `PauseMenu = 4`, `Dialog = 8`. **Conjunto de motivos, não booleano** (Alternative 5): a retomada só acontece quando a máscara esvazia.
- **Um `PauseGate` por app**, criado pelo `AppLifecycle`. Quem escreve **cada motivo** (e só remove o que adicionou; convenção e **regra de revisão de código**, porque `Add` e `Remove` são públicos):
  - `AppPaused` e `FocusLost`: só o `AppLifecycle`.
  - `PauseMenu`: a UI do #12.
  - `Dialog`: **só a `TentativaDeFase`**, que o adiciona em `PedirAbandono` e o remove ao cancelar ou confirmar (GDD #3, Regra 12). A UI não escreve `Dialog`, para não haver duas fontes de verdade que um evento perdido dessincronize.
  - Ao `Discard` da fase, quem adicionou remove `PauseMenu` e `Dialog` (a `TentativaDeFase` e a UI do #12 limpam os seus).
- **Época de pausa.** O `PauseGate` mantém `Epoch` (`int`), que sobe a cada transição da máscara de vazia para não vazia. O `PauseState` (`Active` + `Epoch`) é o que a ponte lê. A volta da pausa é detectada por `Epoch != ultimaEpocaVista`, **não** por um estado que só o `Plan` vê: no Android o `Update` não roda em segundo plano e os callbacks de pausa e retomada chegam os dois entre frames, então no 1º `Update` depois da volta a máscara já está vazia e só a época mostra que houve pausa. Isso também cobre pausa e retomada no mesmo intervalo entre frames.
- `PauseGate` não dispara eventos nem delegates (sem alocação, sem ordem de assinatura): o `AppLifecycle` lê a máscara no começo do frame e chama `TentativaDeFase.SetPaused(bool)` na borda de `IsPaused`. A `TentativaDeFase` ignora a pausa em *Concluindo* e *Resolvida* (GDD #3, bordas).
- **Foco sem ficar preso.** O `AppLifecycle` reconcilia o bit `FocusLost` com `!Application.isFocused` **no começo de todo `Update`** e ao receber `OnApplicationPause(false)`. Assim o valor inicial errado ou um `OnApplicationFocus(true)` que nunca vem se corrigem sozinhos, e a ordem entre os callbacks (Verification Required 2) deixa de importar para esse motivo. A máscara inicial também vem de `Application.isFocused` (`FocusLost` se falso; Verification Required 4). No Editor, a Game view sem foco dispara `FocusLost`: o `AppLifecycle` tem a opção serializada `ignoreFocusInEditor`.
- **Ligação e segundo plano não têm motivo próprio:** a Unity não distingue a ligação (`NOT SOURCEABLE`, Verification Required 2); ela chega como `AppPaused` e/ou `FocusLost`, que já cobrem o que o GDD #3 chama de "foco, segundo plano, ligação". Multi-janela e picture-in-picture entregam `Focus` sem `Pause`, e a ligação pode vir só como `Pause`: o conjunto de motivos cobre os dois casos.
- A tentativa **nasce Pausada** quando a máscara não é vazia no instante em que o #28 confirma a marca (GDD #3, Regra 11): o `AppLifecycle` já existe nesse momento e mantém a máscara, então a `TentativaDeFase` lê `IsPaused` antes do 1º frame de jogo.
- O fim da simulação é tratado **no frame em que ocorre** (Decisão 6, passo 8): o `PhaseHost` leva a tentativa a *Concluindo* assim que o laço vê `Ended`, antes de qualquer `SetPaused` do frame seguinte; por isso a pausa que chega depois já é ignorada pela `TentativaDeFase`.

### 4. `TickPacer`: o que a ponte decide por frame
`TickPacer` é uma classe C# pura, uma por fase, sem `static`, com estado: `acum`, `descartarProximoDt`, `ultimaEpocaVista`, `portaoFechado` e `geracaoDoPortao`, os latches `dodge`, `ultimate` e `pick` (com serial e índice), `moveSuprimido` e `geracaoSuprimida`, e o último `alfa`. Em cada frame o host chama `Plan(...)` e depois, para cada tick do frame, `BuildCommands(k, ...)`.

Ordem dentro de `Plan` (a ordem importa):
1. **Pausado** (`pause.Active != None`): `acum = 0`, apaga os latches e devolve `Ticks = 0` com o último `Alpha` congelado (a tela não pula). O tempo ausente não vira ticks nem é recuperado (GDD #2, Regra 11). Não consome a época.
2. **Voltou da pausa** (`pause.Active == None` e `pause.Epoch != ultimaEpocaVista`): `ultimaEpocaVista = pause.Epoch`, `descartarProximoDt = true`, `acum = 0`, apaga os latches, e o **portão do joystick fecha** se `combatHold == 0` **e** a fase já rodou ao menos um tick (sem portão no tick 0: não há horda; GDD #3, bordas). Guarda `geracaoDoPortao = input.TouchGeneration`. Com `combatHold != 0` não há portão (o combate já está congelado pela simulação e o `PickOffer` só age dentro de um `Tick`). O `TickPacer` nasce com `ultimaEpocaVista` igual à época do gate: a tentativa que nasce Pausada não fecha portão na volta (tick 0) e é coberta pelo descarte do 1º `dt` armado no carregamento.
3. **`dt`:** saneado; se `descartarProximoDt`, vira 0 e a bandeira cai. A bandeira também é armada por `ArmFirstDtDiscard()` ao sair do carregamento da fase (GDD #3, Regra 11: "ou depois do carregamento").
4. **Portão fechado:** devolve `Ticks = 0`, `acum = 0`, `Alpha` congelado, e descarta `Dodge`, `Ultimate` e `PickOffer` tocados. O portão **abre** quando `input.TouchGeneration != geracaoDoPortao`, isto é, num novo início de toque no joystick; no frame em que abre, as ações discretas daquele frame ainda são descartadas *(provisória)*, e o resto do frame segue pelo passo 5.
5. **FS1:** calcula `n`, `acum_novo` e `DroppedTicks = n_devido − n`. Mescla as ações do frame nos latches (dois toques viram um; para `PickOffer`, o último vale).
6. **Frame de 0 ticks:** os latches ficam segurados até o próximo `Tick` executado.

`BuildCommands(k, heroId, buffer)` monta os comandos do tick `k` do frame, **em ordem crescente de `CommandKind`** (a ordem que o ADR-0001, Emenda 4, exige no modo estrito):
- `Move` em **todos** os ticks do frame, com o `ActorId` do herói (`Phase.HeroId`). Cada eixo não finito vira 0 e é limitado a `±EixoMax` (Emenda 4), para que a rejeição do `Tick` só acuse bug de verdade. O `Move` de módulo zero **não é enviado** (sem comando, o joystick está solto; GDD #2, Regra 4).
- `Dodge`, `Ultimate` e `PickOffer` **só em `k == 0`**, a partir dos latches, que são zerados depois de entregues.
- **Supressão do `Move` depois do `PickOffer`** (GDD #2, Regra 15): no frame em que o `PickOffer` é entregue, a ponte liga `moveSuprimido` com `geracaoSuprimida = input.TouchGeneration` **antes** de montar o `Move` do `k == 0`, e o `Move` sai zerado (isto é, omitido) até `input.TouchGeneration != geracaoSuprimida`. O dedo que já estava no joystick não retoma o combate; só um novo início de toque.

**Contrato exigido do #4:** `TouchGeneration` é um inteiro que sobe **só num início de toque real** (dedo apoiado), **nunca** num reset, cancelamento ou reinício do dispositivo; depois de uma volta do segundo plano o estado do joystick é "sem toque". A ponte nunca interpreta a posição do dedo. O toque que confirma "continuar" no #12 conta como novo início no joystick? É pergunta aberta para o #4 e o #12 (GDD Sync).

### 5. Foco perdido é motivo de pausa; gravar continua só no `OnApplicationPause`
O GDD #2 (Regra 11) manda tratar a perda de foco sem pausa como pausa; o ADR-0003 (Seção 6 e `L186`) proíbe `Focus`. **Não há contradição de fundo**: o ADR-0003 proíbe o `Focus` **como gatilho de gravação** (ele dispara também por notificação e janela flutuante, o que gravaria à toa), e o GDD fala de **parar os ticks**. Decidido: o `AppLifecycle` trata `OnApplicationFocus(false)` adicionando `FocusLost` ao `PauseGate` e **não pede commit**; só `OnApplicationPause(true)` aciona o fluxo de gravação do ADR-0003, e só fora de fase. A ordem dentro do callback é fixa: primeiro `PauseGate.Add(AppPaused)`, depois o fluxo de gravação num `try/catch` que registra a exceção e segue (uma falha no save nunca deixa de pausar). "Durante a fase" é, como no ADR-0003, do pedido de `BeginStage` até o commit de fim, informado ao `AppLifecycle` pela `TentativaDeFase`. A nota do ADR-0003 vira uma Emenda (Ordering Note).

### 6. Ordem do frame e fronteira com a apresentação
```
AppLifecycle.Update  ([DefaultExecutionOrder(-200)], um por app, sempre presente)
  1. reconcilia FocusLost com !Application.isFocused (e a máscara inicial no 1º frame)
  2. esvazia a fila de respostas do #28 -> TentativaDeFase (se existir); thread principal
  3. se IsPaused mudou: TentativaDeFase.SetPaused(bool)   (ela ignora em Concluindo/Resolvida)
PhaseHost.Update     ([DefaultExecutionOrder(-100)], um por fase, só com a simulação criada)
  4. se Simulation.Status != Running: sai
  5. dt = IFrameClock; input = #4.Sample()
  6. plan = TickPacer.Plan(dt, gate.State, World.CombatHold, faseJaRodou, input)
  7. para k em 0..plan.Ticks-1:
       n = TickPacer.BuildCommands(k, Phase.HeroId, buffer)
       Simulation.Tick(new ReadOnlySpan<Command>(buffer, 0, n))   // nunca fatiar o array: cria cópia
       events = DrainEvents() -> apresentação e log (#5)
       se Status == Ended: pára o laço e DESCARTA os ticks que sobram (sem acumulá-los)
  8. se Ended: TentativaDeFase.OnSimulationEnded()  (-> Concluindo); expõe plan.Alpha e DroppedTicks
LateUpdate (apresentação: #4, #12, #13...): lê as vistas somente leitura e o Alpha; desenha
```
- A **máscara de pausa é conferida só entre frames**: nada no laço do passo 7 a relê. Se o spike mostrar que um callback pode chegar dentro do laço, o pressuposto (e) do ADR-0001 falhou: **este ADR e esse pressuposto reabrem** (Verification Required 1).
- `DrainEvents()` é chamado **depois de cada** `Tick` (o buffer não drenado faz o `Tick` seguinte lançar; ADR-0001, Emenda 2).
- A apresentação nunca chama `Tick`, `Create` nem escreve `AppPaused`, `FocusLost` ou `Dialog`; a UI do #12 escreve só `PauseMenu`.
- O `AppLifecycle` guarda o id da thread principal no `Awake`; em desenvolvimento, um callback de pausa fora dela lança (acusa o pressuposto (e)); em release, registra e segue.
- O Input System fica em "Dynamic Update" (o padrão): em `FixedUpdate` o toque amostrado no `Update` ficaria velho.

### 7. Orçamento e alocação
Custo por frame: O(1) para `Plan` e O(comandos) para `BuildCommands` (no máximo 4 comandos por tick, um por `CommandKind`). Buffers (`Command[4]`) e latches são campos do `TickPacer`, criados na tela de carregamento; sem LINQ, sem lambda e sem boxing por frame. `Span<Command>` aparece só como parâmetro e variável local (como campo de classe não compila). O custo do `Tick` em si pertence ao ADR de orçamento de frame.

### Architecture Diagram
```
 Unity (thread principal, entre frames)
 OnApplicationPause ─┐
 OnApplicationFocus ─┴─▶ AppLifecycle (1 por app, persistente)
                           │  dono do PauseGate: AppPaused, FocusLost (reconcilia com Application.isFocused)
                           │  esvazia a fila do #28 ─▶ TentativaDeFase (#3)
                           │  OnApplicationPause(true) fora de fase ─▶ gravação (ADR-0003)
 UI #12 ── PauseMenu ──────┤
 TentativaDeFase ── Dialog ┘
                  PauseGate (mascara + Epoch) ── PauseState ──┐
                                                              ▼
 #4 (Presentation) ── InputSample ──▶ PhaseHost (1 por fase) ─▶ TickPacer.Plan ─▶ n ticks, Alpha, DroppedTicks
 IFrameClock (Time.unscaledDeltaTime…) ──┘          │
 World.CombatHold (leitura) ───────────────────────┘
                              para k em 0..n-1: BuildCommands(k) ─▶ Simulation.Tick ─▶ DrainEvents ─▶ apresentação / log (#5)
                              Ended ─▶ TentativaDeFase.OnSimulationEnded()
 Forja.Gameplay.Sim.Host (C# puro, EditMode): TickPacer, PauseGate, PauseState, InputSample, IFrameClock, IPauseView
 Forja.Gameplay (Unity):                      AppLifecycle, PhaseHost
```

### Key Interfaces
```csharp
namespace Forja.Gameplay.Sim.Host   // C# 9 puro, sem UnityEngine; outro namespace que o dos ISimSystem; testavel em EditMode
{
    [System.Flags] public enum PauseReason : uint { None = 0, AppPaused = 1, FocusLost = 2, PauseMenu = 4, Dialog = 8 /* valores explicitos; so cresce no final */ }

    public readonly struct PauseState { public readonly PauseReason Active; public readonly int Epoch; }   // Epoch sobe a cada transicao vazio -> nao vazio

    public interface IFrameClock { float RealDeltaSeconds { get; } }          // segundos reais do frame, sem timeScale; NaN/negativo/infinito vira 0 na FS1
    public interface IPauseView  { bool IsPaused { get; } PauseState State { get; } }

    public sealed class PauseGate : IPauseView {                              // thread principal; sem eventos, sem delegates; Add/Remove idempotentes e nunca lancam
        public void Add(PauseReason reason);                                  // so quem e dono do motivo (regra de revisao)
        public void Remove(PauseReason reason);
        public bool IsPaused { get; }
        public PauseState State { get; }
    }

    public struct InputSample {                                               // montada pelo #4 uma vez por frame
        public float MoveX, MoveY;          // eixos do joystick, ja com zona morta (do #4); a ponte limita a +-EixoMax
        public int   TouchGeneration;       // sobe so em inicio de toque real; nunca em reset/cancelamento
        public bool  Dodge, Ultimate;       // tocados neste frame (borda de subida)
        public bool  HasPick; public int PickSerial, PickIndex;   // ArgA = serial da oferta, ArgB = indice da carta (ADR-0001, Emenda 4)
    }

    public readonly struct FramePlan { public readonly int Ticks; public readonly float Alpha; public readonly int DroppedTicks; }

    public sealed class TickPacer {                                           // uma por fase; sem static
        public TickPacer(int maxTicksPerFrame, int gateEpochAtCreation);      // lanca fora de 1..16
        public void ArmFirstDtDiscard();                                      // ao sair do carregamento da fase
        public FramePlan Plan(float rawDt, in PauseState pause, int combatHold, bool phaseHasTicked, in InputSample input);
        public int BuildCommands(int tickIndexInFrame, int heroId, System.Span<Command> buffer);   // devolve quantos comandos escreveu
    }
}

namespace Forja.Gameplay          // com Unity
{
    [UnityEngine.DefaultExecutionOrder(-200)]
    public sealed class AppLifecycle : UnityEngine.MonoBehaviour              // 1 por app, cena de bootstrap
    {
        [UnityEngine.SerializeField] int maxTicksPerFrame = 4;                // 1..16; validado no Awake, OnValidate e checagem de build
        [UnityEngine.SerializeField] bool ignoreFocusInEditor;
        public PauseGate Gate { get; }
        void Update();                                                        // Decisao 6, passos 1 a 3
        void OnApplicationPause(bool paused);                                 // AppPaused primeiro; depois a gravacao do ADR-0003 (try/catch), so fora de fase
        void OnApplicationFocus(bool hasFocus);                               // FocusLost; nunca grava
    }

    [UnityEngine.DefaultExecutionOrder(-100)]
    public sealed class PhaseHost : UnityEngine.MonoBehaviour                 // 1 por fase; so le Gate; nao recebe callback do app
    {
        void Update();                                                        // Decisao 6, passos 4 a 8
        public float Alpha { get; }                                           // FS2, lido pela apresentacao
        public int DroppedTicksTotal { get; }                                 // lido pelo log (#5)
    }
}
```

### Implementation Guidelines
- O `TickPacer`, o `PauseGate`, o `InputSample` e as interfaces **must** viver em `Forja.Gameplay.Sim.Host` e **must never** referenciar `UnityEngine`; só o `AppLifecycle` e o `PhaseHost` tocam a Unity. Nenhum sistema chamado por `ISimSystem.Step` **must** referenciar `IFrameClock`, `TickPacer` ou `PauseGate` (separa o código com relógio real do código de tick dentro do mesmo asmdef).
- O `AppLifecycle` **must** ser o único receptor de `OnApplicationPause` e `OnApplicationFocus`; o `PhaseHost` **must never** declarar esses callbacks.
- A ponte **must** chamar `Tick` somente a partir do `Update` do `PhaseHost`, na thread principal, com `Status == Running`; **must never** chamar `Tick` a partir de um callback do app, de `FixedUpdate`, de `LateUpdate` ou de uma corrotina.
- A pausa **must** ser "zero chamadas de `Tick`"; **must never** usar `Time.timeScale` (nem para pausa nem para câmera lenta). A câmera lenta **must** ser o descarte do excedente da FS1.
- O conjunto de motivos **must** ser um `[Flags] enum` com valores explícitos; **must never** virar um `bool`. Cada escritor **must** remover só os motivos que ele adicionou (regra de revisão de código); só a `TentativaDeFase` escreve `Dialog`.
- A volta da pausa **must** ser detectada por `PauseState.Epoch`, **must never** por um estado que só o `Plan` observa.
- `OnApplicationFocus` **must never** acionar gravação; só `OnApplicationPause` aciona o fluxo do ADR-0003, e só fora de fase; uma exceção do save **must never** impedir o `PauseGate.Add`.
- O `Move` **must** ser entregue em todos os ticks do frame; `Dodge`, `Ultimate` e `PickOffer` **must** ser entregues uma vez, em `k == 0`, e **must** ser segurados em frame de 0 ticks.
- Os comandos **must** sair em ordem crescente de `CommandKind` e com eixos finitos e limitados a `±EixoMax`. `Tick` **must** receber `new ReadOnlySpan<Command>(buffer, 0, n)`, nunca uma fatia que copie.
- O `DrainEvents()` **must** ser chamado depois de cada `Tick`; ao `Ended`, o laço **must** parar e descartar os ticks restantes, e o `PhaseHost` **must** chamar `TentativaDeFase.OnSimulationEnded()`.
- A ponte **must never** ler `CombatHold` por outro caminho que não a leitura do `SimWorld`, e **must never** escrevê-lo.
- Nenhum teste de EditMode da ponte **must** depender de relógio real: todos usam `FakeRelogio` (`IFrameClock`) e `PauseGate` direto; testes que tocam `Time.timeScale` **must** restaurá-lo no SetUp e no TearDown.
- Testes ficam em `Assets/Tests/EditMode/Gameplay/` (pacer, gate, comandos) e `Assets/Tests/PlayMode/` só para o `AppLifecycle` e o `PhaseHost` (callbacks, ordem do frame).

## Alternatives Considered

### Alternative 1: ticks no `FixedUpdate`
- **Description**: `Time.fixedDeltaTime = 1/30` e a simulação roda no `FixedUpdate`; a Unity acumula o tempo e chama quantas vezes precisar.
- **Pros**: menos código nosso; o acumulador é da engine.
- **Cons**: a Unity decide sozinha quantos `FixedUpdate` rodar por frame e tem o próprio teto (`maximumDeltaTime`), então `MaxTicksPerFrame` e o descarte da FS1 deixam de ser nossos e de ser testáveis; o 1º `dt` depois da pausa não é descartável de fora; `Time.fixedDeltaTime` é global e mexe na física que o projeto não usa; o `FakeRelogio` deixa de existir; a FS2 (`acum_novo`) não sai do motor.
- **Rejection Reason**: tira da ponte o controle que a Regra 11 do #2 e o AC-R11 do #3 exigem testar.

### Alternative 2: ponte injetada no `PlayerLoop`
- **Description**: um `PlayerLoopSystem` próprio roda a ponte antes do `Update`.
- **Pros**: controle total da posição no frame, sem depender de `DefaultExecutionOrder`.
- **Cons**: mais código de engine que muda entre versões; risco com domain reload desligado; o ganho sobre `[DefaultExecutionOrder]` não é medido.
- **Rejection Reason**: YAGNI. Reabrir só se o spike mostrar que a ordem entre `AppLifecycle` e `PhaseHost` não basta.

### Alternative 3: pausa e câmera lenta por `Time.timeScale`
- **Description**: `timeScale = 0` para pausar e `timeScale < 1` para a câmera lenta.
- **Pros**: uma linha; pausa também as animações da engine.
- **Cons**: a FS1 usa tempo real e não escalado, então o efeito é inconsistente; congela animações e áudio da apresentação (o menu de pausa e o aviso "toque para continuar" do #12 precisam animar); a câmera lenta por escala **pularia** a promessa "o jogo desacelera e nunca pula"; mistura o relógio da engine com o da ponte.
- **Rejection Reason**: contradiz a Regra 11 do #2 (zero ticks, descarte do excedente) e a promessa da Player Fantasy.

### Alternative 4: relógio por `Stopwatch` já como padrão
- **Description**: `IFrameClock` padrão lê `Stopwatch.GetTimestamp` em vez de `Time.unscaledDeltaTime`.
- **Pros**: independe do que a Unity faz com o `dt` ao voltar do segundo plano.
- **Cons**: duplica o que a engine já mede; não há evidência local de que `unscaledDeltaTime` falhe; o ganho só aparece se o spike mostrar saltos.
- **Rejection Reason**: não é preciso decidir já. A interface `IFrameClock` guarda a troca, e a Verification Required 3 decide.

### Alternative 5: pausa com um `bool`
- **Description**: `isPaused` ligado e desligado por cada fonte.
- **Pros**: o mais simples.
- **Cons**: foco e `OnApplicationPause` vêm juntos e em ordens diferentes; o diálogo de abandono precisa continuar pausando depois que o foco volta (GDD #3, Regra 12); um `bool` retoma cedo demais.
- **Rejection Reason**: o GDD #3 (Regra 11) pede o conjunto, e a tentativa que nasce Pausada exige saber *quem* pausa.

### Alternative 6: tratar só `OnApplicationPause`, ignorar o foco
- **Description**: seguir à risca o "nunca `Focus`" do ADR-0003 também para a pausa.
- **Pros**: um sinal só; nenhuma tensão com o ADR-0003.
- **Cons**: aba de notificação, janela flutuante e multi-janela deixariam a simulação rodando com o jogador sem ver ou sem controlar; contradiz a Regra 11 do #2 e a Regra 11 do #3.
- **Rejection Reason**: o ADR-0003 proíbe o `Focus` como gatilho de gravação, não como motivo de pausa (Decisão 5).

### Alternative 7: callbacks do app dentro do `PhaseHost` (rascunho inicial)
- **Description**: o host por fase recebe `OnApplicationPause`/`Focus`, guarda a máscara e aciona o save.
- **Pros**: um só objeto novo; a máscara nasce e morre com a fase.
- **Cons**: fora da fase não há host, mas o commit do `BeginStage`, a pausa fora de fase e a fila do #28 acontecem antes de existir simulação; a tentativa não conseguiria nascer Pausada; callbacks entre o `Discard` de uma fase e o `Create` da seguinte se perderiam.
- **Rejection Reason**: apontada pelo `technical-director` (lacuna 1) e pelo `unity-specialist` (B2); substituída pelo `AppLifecycle` persistente.

## Consequences

### Positive
- A FS1, a FS2, a entrega de comandos, o portão do joystick e a máquina de pausa ficam inteiras em C# puro, testáveis em EditMode com `FakeRelogio`, sem aparelho.
- Uma só fonte de pausa (`IPauseView`), com dono que existe também fora da fase, para a ponte, a `TentativaDeFase` e a UI.
- A escolha da fonte do tempo e do conjunto de callbacks, que são os pontos `NOT SOURCEABLE`, fica atrás de `IFrameClock` e do `PauseGate`: se o spike discordar, muda uma implementação e não o contrato. O `FocusLost` e a época de pausa se corrigem sozinhos.
- Fecha o GAP TR-simulacao-015 e a parte aberta de 016 e fluxo-014 sem alterar os GDDs.

### Negative
- Dois `MonoBehaviour` (um por app, um por fase) e uma cena de bootstrap que precisa criar o `AppLifecycle` antes de qualquer tela.
- A fração de tick (até 33 ms) se perde a cada pausa; a tela pode "dar um passo atrás" de até 1 tick na retomada (aceito pelo GDD #2).
- A retomada depende de um **novo início de toque** (não basta o dedo já apoiado), o que é mais estrito do que "tocar" e precisa de playtest.
- O ADR-0003 precisa de uma Emenda curta (Ordering Note), e o GDD #4 precisa nascer com o contrato `InputSample`/`TouchGeneration`.

## Risks
- **Callback fora da thread principal ou dentro do laço (pressuposto (e)):** quebraria a garantia de "zero `Tick` em pausa". Mitigação: o assert de thread em desenvolvimento e a Verification Required 1; **gatilho de reabertura** escrito (Decisão 6); a conferência da máscara só entre frames limita o dano aos ticks daquele frame.
- **Ordem e cobertura dos sinais no Android (ligação, aba de notificação, multi-janela, picture-in-picture):** `NOT SOURCEABLE`. Mitigação: o conjunto de motivos tolera os dois callbacks em qualquer ordem e a reconciliação por `Application.isFocused` corrige o foco preso.
- **1º `dt` depois do segundo plano:** a FS1 sozinha ainda rodaria `Max` ticks; o descarte do 1º `dt` e o `acum = 0` cobrem. Mitigação: o spike mede com `unscaledDeltaTime` e com `Stopwatch`.
- **Volta da pausa invisível ao `Plan`:** corrigida pela `Epoch`; exige teste de EditMode com `Add` e `Remove` sem nenhum `Plan` no meio.
- **Portão do joystick por `TouchGeneration`:** se o Android não cancela os toques, o dedo apoiado na volta não abre o portão e o jogador precisa soltar e tocar de novo; se cancela e o dedo continua apoiado, um novo início de toque depois do frame do portão o abre sozinho (Verification Required 5, os dois casos). Mitigação: contrato do #4 (`TouchGeneration` só em início real); o aviso "toque para continuar" é do #12; a regra fica na lista de provisórias.
- **Passo atrás de até 1 tick na retomada:** pequeno, único e já aceito pelo GDD; mitigação: o `Alpha` fica congelado durante a pausa.
- **Escritor removendo motivo alheio:** `Remove` é público; só a revisão de código impede. Mitigação: a lista de donos por motivo na Decisão 3 e uma regra no manifesto de controle.
- **Estado do `PhaseHost` por fase:** esquecer de destruí-lo no `Discard` deixaria um segundo host chamando `Tick` numa simulação `Destroyed`. Mitigação: o `Tick` em `Destroyed` já lança (ADR-0001, Emenda 2), e o `Discard` do #3 destrói o host.
- **Frame pacing a 60 Hz com sim a 30 Hz:** o jitter do `dt` alterna 0, 1 e 2 ticks por frame. Mitigação: Verification Required 7.
- **Revisões 5.5 e 5.6 (resultado):** `unity-specialist`: abordagem aprovada; bloqueantes B1 (volta da pausa invisível ao `Plan`) e B2 (callbacks fora de fase) **resolvidos** nesta revisão; notas 1 a 11 incorporadas (reconciliação do foco, `ReadOnlySpan` no `Tick`, validação do `MaxTicksPerFrame`, contrato do `TouchGeneration`, `timeScale` nos testes, frame pacing, multi-janela, C# 9). `technical-director`: CONCERNS; lacunas 1 a 3 (ciclo de vida do dono dos callbacks, `FocusLost` preso, duas fontes para o `Dialog`) e concerns 4 a 9 (namespace, ordem do frame, validação do `MaxTicksPerFrame`, caso inverso do toque, entradas de registro, camada Core) **resolvidos** no texto; o gatilho da Verification Required 1 foi escrito. Um novo parecer do diretor sobre este texto revisado **não foi pedido**; o veredito vigente continua sendo o CONCERNS acima, tratado, e não um APPROVE.

## GDD Requirements Addressed

| GDD System | Requirement | How This ADR Addresses It |
|------------|-------------|--------------------------|
| simulacao-deterministica.md (#2) | Regra 4 / TR-simulacao-015: `Mover` em todo tick do frame, ações discretas 1x no 1º tick, ação segurada em frame de 0 ticks | Decisão 4: `BuildCommands(k)` e os latches do `TickPacer`; ordem por `CommandKind` |
| simulacao-deterministica.md (#2) | Regra 11 e FS1 / FS2: acumulador, `MaxTicksPerFrame`, descarte do excedente, `alfa` | Decisões 1, 2 e 4: `Plan`, `IFrameClock`, campo serializado validado de 1 a 16 no início do app, `DroppedTicks`, `Alpha` congelado na pausa |
| simulacao-deterministica.md (#2) | Regra 11 / TR-simulacao-016: zero `Tick` em pausa, acumulador zerado, 1º `dt` descartado, portão do joystick só com `CombatHold = 0` | Decisão 4 (passos 1 a 4) com detecção por `Epoch`; `CombatHold` lido do `SimWorld`, nunca escrito |
| simulacao-deterministica.md (#2) | Regra 15: `Mover` zerado do `PickOffer` até um toque novo | Decisão 4: `moveSuprimido` e `geracaoSuprimida` por `TouchGeneration` |
| simulacao-deterministica.md (#2) | Regra 16 (e), (f): callbacks na thread principal, entre frames; fonte do `dt` | Decisões 2, 3 e 6; Verification Required 1 a 3 (marcadas `NOT SOURCEABLE`, com gatilho de reabertura) |
| fluxo-de-fase.md (#3) | Regra 11 / TR-fluxo-014: conjunto de motivos, 1º `dt` descartado também depois da carga, nasce Pausada, pausa não grava | Decisão 3 (`PauseGate`, `AppLifecycle` persistente, máscara inicial, `SetPaused`), Decisão 4 passo 3 (`ArmFirstDtDiscard`), Decisão 5 |
| fluxo-de-fase.md (#3) | Regra 12: diálogo de abandono conta como motivo de pausa | Decisão 3: só a `TentativaDeFase` escreve `Dialog` |
| fluxo-de-fase.md (#3) | Bordas: pausa com a simulação `Ended`; laço para ao `Ended` e descarta o resto | Decisões 3 e 6 (passos 7 e 8): `OnSimulationEnded` leva a Concluindo no mesmo frame |
| save-local.md (#28) / ADR-0003 | A pausa grava só por `OnApplicationPause`, nunca durante a fase; fila de respostas esvaziada entre frames | Decisões 3, 5 e 6 (passos 2 e 3): o `AppLifecycle` esvazia a fila e aciona o save, também fora de fase |

## Performance Implications
- **CPU**: O(1) por frame no `Plan` e no máximo 4 comandos por tick; desprezível frente ao `Tick`. O custo do `Tick` é do ADR de orçamento de frame.
- **Memory**: um `AppLifecycle` e um `PauseGate` por app; um `TickPacer`, `Command[4]` e campos escalares por fase; sem alocação por frame.
- **Load Time**: criação do `PhaseHost`, do `TickPacer` e dos buffers na tela de carregamento, depois do `Preparar`; o `AppLifecycle` nasce na cena de bootstrap.
- **Network**: não se aplica.

## Migration Plan
Não há código da ponte nem do host hoje (`Assets/` ainda sem esses tipos). A ordem é: (1) `PauseReason`, `PauseGate` com `Epoch`, `InputSample`, `IFrameClock` e o `TickPacer` com a FS1 e a FS2, testados em EditMode com `FakeRelogio`; (2) a entrega de comandos, os latches, o portão e a supressão do `Move`; (3) o `AppLifecycle` na cena de bootstrap e o `PhaseHost`, com os callbacks e a ordem do frame; (4) o spike no aparelho (Verification Required 1 a 8).

## Validation Criteria
- AC-T do GDD #2 (tempo e ponte) e AC-R11 do GDD #3 passam em EditMode: com `FakeRelogio` que avança 600 s durante a pausa, 0 `Tick` e o mesmo `StateHash`; 2 motivos de pausa e 1 encerrado seguem Pausada; a tentativa pronta com motivo ativo nasce Pausada; a pausa não grava.
- Testes do `TickPacer`: os exemplos (a), (b), (c) da FS1; `Max` fora de 1 a 16 lança; `dt` NaN, negativo e infinito viram 0; frame de 0 ticks segura `Dodge`; dois toques viram um; `PickOffer` zera o `Move` até `TouchGeneration` mudar; portão fechado com `combatHold == 0` e aberto com `combatHold != 0` e no tick 0; ação tocada com o portão fechado é descartada; **`Add` e `Remove` sem nenhum `Plan` no meio ainda descarta o 1º `dt` e fecha o portão**.
- Testes do `AppLifecycle` (PlayMode): `FocusLost` preso se corrige com `Application.isFocused`; `OnApplicationFocus` nunca chama o save; `OnApplicationPause(true)` fora de fase chama o save uma vez e, dentro de fase, não chama.
- Zero alocação gerenciada por frame no `Plan` e no `BuildCommands` (IL2CPP, no aparelho).
- No aparelho: Verification Required 1 a 8. **A story da ponte não fecha sem a evidência do spike nos itens 1 a 5** (Test Evidence de integração), mesmo que o ADR seja aceito antes.

## Related
- Depende de ADR-0001 (`Proposed`) e ADR-0003 (`Proposed`). Pede uma **Emenda ao ADR-0003** (L186: "nunca `Focus`" como gatilho de gravação; fila do #28 esvaziada pelo `AppLifecycle`) e anota nos GDDs #2 e #3 que "ligação" e "segundo plano" não são motivos separados na implementação (GDD Sync).
- GDDs: `design/gdd/simulacao-deterministica.md` (#2), `design/gdd/fluxo-de-fase.md` (#3), `design/gdd/save-local.md` (#28), `design/gdd/systems-index.md` (#4 Input e câmera, #12 UI de pausa, sem GDD ainda).
- `docs/architecture/architecture-review-2026-11-06.md` (Required ADRs, item 1); `docs/architecture/requirements-traceability.md` (TR-simulacao-015, 016, TR-fluxo-014).

## GDD Sync (pendente; nenhum arquivo foi editado)
- GDD #2 (Regra 11) e GDD #3 (Regra 11, estados): citam "ligação" como causa de pausa. Aqui "ligação" chega como `AppPaused` e/ou `FocusLost` (a Unity não a distingue). Sugestão: manter o texto do GDD e anotar que "ligação" é coberta pelos motivos de app e de foco.
- GDD #2 (Regra 4) fala em "toque" do joystick sem definir "novo início de toque"; aqui é o `TouchGeneration` do #4. O GDD #4 deve defini-lo (só em início real) quando for escrito; o ADR o lista como contrato pendente.
- GDD #4 e #12: definir se o toque que confirma "continuar" conta como novo início no joystick.
- GDD #3 (Regra 12): diz que o diálogo de abandono conta como motivo de pausa; este ADR atribui a escrita de `Dialog` só à `TentativaDeFase`. Consistente; sem mudança no GDD.

## Decisões provisórias (a reavaliar com o jogo jogável e depois do spike no aparelho)
1. `Time.unscaledDeltaTime` como fonte padrão do `dt` (Decisão 2; `Stopwatch` atrás do `IFrameClock` se o spike pedir).
2. Hosts no `Update` com `[DefaultExecutionOrder]` -200 e -100 (Decisão 2; `PlayerLoop` só se a ordem não bastar).
3. O `AppLifecycle` persistente como único receptor dos callbacks do app (Decisão 1) e a reconciliação do `FocusLost` com `Application.isFocused` a cada frame (Decisão 3).
4. Os quatro motivos `AppPaused`, `FocusLost`, `PauseMenu` e `Dialog`, "ligação" sem motivo próprio, e a `Epoch` do `PauseGate` (Decisão 3).
5. O portão do joystick abre por **novo início de toque** (`TouchGeneration`), e as ações discretas do frame em que ele abre são descartadas (Decisão 4, passo 4).
6. `PickOffer` segurado: o último vale (Decisão 4, passo 5).
7. `Move` de módulo zero não é enviado; eixos limitados a `±EixoMax` pela ponte (Decisão 4).
8. A camada **Core** (recomendação do gate TD-ADR, sem `architecture.md`).
9. O `Alpha` congelado durante a pausa e na espera do portão (Decisão 4).
10. O `MaxTicksPerFrame` como campo do `AppLifecycle`, validado no início do app (Decisão 1).
