# Forja das Hordas — Arquitetura Mestra

## Document Status
- Version: 2
- Last Updated: 2026-11-10
- Engine: Unity 6.3 LTS (6000.3.27f1), URP, Android (GLES3 e Vulkan), IL2CPP
- GDDs Covered (6 de 40 sistemas): #1 Dados e balanceamento, #2 Simulação determinística, #3 Fluxo de fase, #6 Combate e dano, #7 Horda, waves e inimigos, #28 Save local. Os outros 34 sistemas do `systems-index` não têm GDD: entram como "contrato pendente".
- ADRs Referenced (10, todos `Proposed`): ADR-0001 Simulação determinística float32 a 30 Hz · ADR-0002 Dados e snapshot imutável · ADR-0003 Save local · ADR-0004 Colunas do `SimWorld` · ADR-0005 Pipeline de dano e eventos · ADR-0006 Vetor, geometria e consulta espacial · ADR-0007 Ponte de entrada, tempo e ciclo de vida · ADR-0008 Log de eventos · ADR-0009 Render de multidão e VFX · ADR-0010 Orçamento de frame e de entrada.
- Linha de base de requisitos: os 129 TR do `docs/architecture/tr-registry.yaml` (128 ativos, 1 superseded), todos registrados; nenhum provisório.
- TD-ARCHITECTURE: 2026-11-10 — REVISED after CONCERNS (a v1 deu CONCERNS sem bloqueante; a v2 corrige a regra de camadas, a raiz de composição, a tabela de asmdefs e os tipos de motor)
- LP-FEASIBILITY: 2026-11-10 — REVISED after CONCERNS (a v1 deu CONCERNS sem bloqueante; a v2 acrescenta threads, o orçamento do laço de ticks e os contratos que bloqueiam a primeira story)

> Este documento é o mapa das decisões que os ADRs já tomam, não uma fonte nova de decisão. Onde o texto e um ADR divergirem, vale o ADR. Os fatos de motor, de Android e de IL2CPP que não estão em `docs/engine-reference/unity/` aparecem como `NOT SOURCEABLE`.

## Engine Knowledge Gap Summary
Motor: Unity 6.3 LTS. O conhecimento do modelo cobre até ~2022 LTS; as docs locais são de 2026-02-13.

| Domínio | Risco | O que mudou do Unity 2022 | Onde o projeto toca |
|---|---|---|---|
| Render (URP, RenderGraph, GPU Resident Drawer) | **HIGH** | Passes customizados usam `RecordRenderGraph`; o Resident Drawer é novo | ADR-0009 (multidão instanciada); o Resident Drawer está desligado no projeto |
| Input | **HIGH** | `Input` legado depreciado; vale o Input System package | #4 Input e câmera (sem GDD) |
| DOTS/ECS | **HIGH** | `ISystem`, `IJobEntity`, API refeita | **Não usado**: o `SimWorld` é escrito à mão (ADR-0001 e 0004) |
| Addressables | MEDIUM | Desde o 6.2, falha de carga lança exceção | Fora do `manifest.json`; é a decisão M4 em aberto |
| Física | MEDIUM | Iterações do solver mudaram | **Não usada**: geometria própria (ADR-0006) |
| UI | LOW | UI Toolkit é o recomendado | #30 UI de meta-jogo (sem GDD) |
| Áudio | LOW | Poucas mudanças | #31 Áudio (sem GDD) |

**Divergências deliberadas das práticas recomendadas pela referência:**
- A referência recomenda ECS/Jobs/Burst. O projeto escolheu uma simulação própria, determinística, em `float32` a 30 Hz, sem `UnityEngine` (ADR-0001, 0004, 0006).
- A referência recomenda Addressables e marca `Resources.Load` como depreciado. O projeto proíbe Addressables para o snapshot embarcado, lido como `TextAsset` síncrono (desvio declarado no ADR-0002 §8); o carregador dos assets do chefe é a decisão M4.

**Fatos sem fonte local (`NOT SOURCEABLE`):** Android (JNI, vsync ignorado, Optimized Frame Pacing, StreamingAssets no APK), GLES e Vulkan (limite de lote, PSO), IL2CPP (stripping, `BinaryPrimitives`), `RenderParams.matProps`, `ShaderVariantCollection.WarmUpProgressively`, AssetBundle e cena aditiva, `OnApplicationPause`. Também não estão em `docs/engine-reference/unity/`: `MonoBehaviour`, `DontDestroyOnLoad`, `Application.persistentDataPath`, `Application.targetFrameRate`, `RuntimeInitializeOnLoadMethod`, `TextAsset`, `MaterialPropertyBlock` e `ShaderVariantCollection`; são APIs estáveis anteriores ao cutoff, mas não verificadas contra a referência. Só `Graphics.RenderMeshInstanced` e `RenderParams(material)` estão em `modules/rendering.md`.

## System Layer Map
Cinco camadas de código, como no `systems-index`, sobre a camada Platform (o motor e o SO, sem nenhum sistema). A camada é uma classificação de responsabilidade, para planejar e revisar; o que o compilador impõe é o grafo de asmdefs (tabela em Module Ownership), e dentro de `Forja.Gameplay.Sim` a separação é só por namespace, então precisa de um teste de dependência por namespace (QQ-14).

```
┌─ POLISH ─ depende de tudo, inclui o online ───────────────────────────┐
│  #29 Serviços online · #32 Onboarding · #33 Acessibilidade            │
│  #34 Analytics · #35 Coop PvE · #36 PvP · #39 Consentimento            │
├─ PRESENTATION ────────────────────────────────────────────────────────┤
│  #12 Feedback/VFX/HUD · #4 Input e câmera · #30 UI de meta · #31 Áudio │
│  módulo: Forja.Gameplay.Sim.View (ADR-0009)                            │
├─ FEATURE ─────────────────────────────────────────────────────────────┤
│  #7 Horda · #8 Skills · #9 Oferta · #10 Funções · #11 Raças · #13 IA   │
│  #14 Dungeons · #15 Varredura · #16 Grimório · #17 Selamento           │
│  #18 Reforja · #19 Herói · #20 Campanha · #21 Poder · #22 Ranking      │
│  #23 Runas · #24 Inventário · #25 Forja · #26 Economia · #27 Loja      │
│  #38 Cosméticos · #40 Auto-battle                                      │
├─ CORE ────────────────────────────────────────────────────────────────┤
│  #2 Simulação determinística · #6 Combate e dano · #3 Fluxo de fase    │
│  #5 Log de eventos                                                     │
│  módulos: Forja.Simulation (ADR-0001, 0004, 0005, 0006), Sim.Log      │
├─ FOUNDATION ──────────────────────────────────────────────────────────┤
│  #1 Dados e balanceamento · #28 Save local · #37 Entitlements          │
│  módulos: Forja.Data (ADR-0002), Forja.Save (ADR-0003)                 │
├─ PLATFORM (motor e SO, sem sistemas) ─────────────────────────────────┤
│  Unity 6.3 · URP · Android (GLES3/Vulkan) · IL2CPP                     │
└───────────────────────────────────────────────────────────────────────┘

┌─ RAIZ DE COMPOSIÇÃO (fora da pilha) ──────────────────────────────────┐
│  Forja.Gameplay (MonoBehaviours) · Sim.Host (ADR-0007, ponte e ganchos)│
│  Sim.Budget (ADR-0010) · Sim.Resolve (DataResolver, ADR-0002)          │
└───────────────────────────────────────────────────────────────────────┘
```

**A raiz de composição** é o conjunto de módulos que liga as camadas: o único autorizado a referenciar todas. (Decisão do usuário, 2026-11-10: o host chama `Simulation.Tick` e o `Sim.Budget` usa tipos de Presentation e Core, então um lugar em Foundation inverteria o sentido das dependências.) Duas regras, com as exceções que os ADRs impõem:

- **R1, camadas:** cada camada depende só das de baixo, com **uma exceção declarada**: `Forja.Data → Forja.Simulation`, porque o `PhaseSnapshot` implementa o `IPhaseSnapshot` que o Core declara (ADR-0002 §9). A inversão é de contrato, não de implementação.
- **R2, raiz de composição:** nenhuma camada referencia a **implementação** da raiz. Há **duas exceções conhecidas**: (a) as interfaces dos ganchos moram no `Sim.Host` (a raiz), e o Log (Core) e a View (Presentation) as implementam; (b) a View lê `PhaseHost.IsDiscarded` e `Alpha` da classe concreta. A resolução recomendada é uma emenda ao ADR-0007 que publique as interfaces e os DTOs dos ganchos num namespace de contratos (`Forja.Gameplay.Sim.Contracts`, sem implementação) e exponha `Alpha` e `IsDiscarded` por interface. Até lá as duas exceções ficam registradas (QQ-10).

**O laço da simulação cruza as camadas.** #7, #8, #6, #3 e #16 rodam dentro do `Simulation.Tick` como `ISimSystem`, na ordem #7 → #8 → #6 → #3 → #16 (ADR-0001, Emenda 19(f)), embora o #7, #8 e #16 estejam em Feature pelo grafo de dependências. O #3 depende do #7 por uma interface que o #3 define e o #7 cumpre, sem ciclo.

**Consciência do motor por camada.** Foundation e Core só tocam o motor na borda: a simulação não referencia `UnityEngine`, e `Forja.Data` e `Forja.Save` são asmdefs sem engine. O que usa API do motor é a raiz de composição (`MonoBehaviour`, `RuntimeInitializeOnLoadMethod`, `OnApplicationPause`, `Application.targetFrameRate`), o plano JNI do save e o `TextAsset` do snapshot. Os domínios HIGH que o jogo usa (URP/RenderGraph e Input System) ficam só na Presentation; o DOTS também é HIGH, mas não é usado.

## Module Ownership

### Foundation
| Módulo | Dono de (exclusivo) | Expõe | Consome | APIs de motor |
|---|---|---|---|---|
| **#1 Dados** (`Forja.Data`, ADR-0002) | Snapshot imutável gerado no build: `PhaseSnapshot`, catálogo, `DefIdTable`, `IdTable`, `RevisionHistory`, `ContentHash`; `DataValidator`, baker, `AuthoringReport`; `Fnv1a64` | `IPhaseSnapshot` (para o Core), `PhaseSnapshot` concreto (compositor e `Arena`), `ValidationResult` | nada em runtime | `TextAsset` síncrono (desvio declarado); menu e pré-build só no editor; asmdef sem engine |
| **#28 Save** (`Forja.Save`, ADR-0003) | Envelope TLV, commit atômico, gravador único, `MarkState`, `AttemptId`, `FailureCause` | `ISaveService`, `ISaveStorage`, `ISaveClock`, `ISaveEventSink`, `IDataResolver` (declara) | `Fnv1a64` | `System.IO` e `persistentDataPath`; JNI no plano C (`NOT SOURCEABLE`); asmdef sem engine |
| **#37 Entitlements** | (sem GDD) leitura das posses de cosméticos comprados | — | — | — |

### Core
| Módulo | Dono de | Expõe | Consome | APIs de motor |
|---|---|---|---|---|
| **#2 Simulação** (`Forja.Simulation`, ADR-0001, 0004, 0006) | `SimWorld` (colunas), `Simulation`, RNG PCG32 em streams, fila de eventos, `SimMath`, `SimQuery`, `Arena` | `Simulation`, `ISimSystem`, spans `Alive`/`XpValues`/`Essentials`, `ICombatReadView`, `ITickProbe` | `IPhaseSnapshot` | **nenhuma** |
| **#6 Combate** (ADR-0005) | Pipeline de dano, fila `Aplicar`/`Curar`/`PedirRugido`, `CombatCounters`, eventos de golpe | `ICombatRequests` (só dentro de um `Step`, guarda `InStep`) | `SimWorld`, snapshot | nenhuma |
| **#3 Fluxo de fase** | `PhaseSheet`, XP e nível, `PhaseResult`, `IPreparaFase`/`IConcluiFase` | `PhaseResult` | `SimWorld`, `ISaveService` | nenhuma |
| **#5 Log** (`Sim.Log`, ADR-0008) | `PhaseLog`, `LogHost`, `LogWriter`, formato `.fjlog`, `ICounterSource` | implementa `ITickObserver`, `IPhaseEndObserver`, `IAppLifecycleObserver`, `ISessionNoteSink` | `Fnv1a64`, tipos de `Forja.Save` | só `System.IO` (escrita em `ThreadPool`) |

### Presentation
| Módulo | Dono de | Expõe | Consome | APIs de motor |
|---|---|---|---|---|
| **Sim.View** (ADR-0009) | `PresentationDriver`, `GhostPool`, `CardPool`, textura de dados por instância, `PrewarmRunner`, `LoadLevel` | `ILoadLevelSource` (declara) | `ITickObserver`, vistas do `SimWorld`, `PhaseHost.IsDiscarded`/`Alpha` | **HIGH:** URP, `Graphics.RenderMeshInstanced` + `MaterialPropertyBlock` em pedaços, textura `RGBA32F` com `.Load()`, `ShaderVariantCollection`; `RenderParams.matProps` é `NOT SOURCEABLE` |
| **#4 Input e câmera** | (sem GDD) `InputSample` | alimenta o host | — | **HIGH:** Input System package |
| **#12 HUD/VFX, #30 UI, #31 Áudio** | (sem GDD) | — | — | UI Toolkit (#30), `AudioMixer` (#31) |

### Raiz de composição
| Módulo | Dono de | Expõe | Consome | APIs de motor |
|---|---|---|---|---|
| **Ponte e host** (`Sim.Host` + `Forja.Gameplay`, ADR-0007) | `AppLifecycle` (persistente), `PhaseHost` (por fase), `TickPacer`, `PauseGate`, `BootState`, ganchos neutros | `ITickObserver`, `IAppLifecycleObserver`, `IFrameObserver`, `IPhaseEndObserver`, `ISessionNoteSink`, `FrameRate.Target`, `PhaseHost.Alpha`/`IsDiscarded` | `Simulation`, `ISaveService`, snapshot validado | `MonoBehaviour`, `RuntimeInitializeOnLoadMethod(BeforeSceneLoad)`, `DontDestroyOnLoad`, `OnApplicationPause`, `Application.targetFrameRate` |
| **Orçamento** (`Sim.Budget`, ADR-0010) | `FrameLedger`, `LoadGovernor`, implementação da sonda, contadores `Source = Budget` | implementa `ILoadLevelSource` | `IFrameObserver`, `ITickProbe`, `IPhaseLog.WriteNote` | `Stopwatch`; a medição de frame fica para o spike |
| **Resolvedor** (`Sim.Resolve`, ADR-0002) | `DataResolver` | implementa `IDataResolver` | `DefIdTable`, ADR-0003 | nenhuma |

### Feature e Polish
Donos e dependências estão no `systems-index`, mas nenhum desses sistemas tem GDD nem contrato: ficam como "contrato pendente". #7, #8 e #16 vão herdar o contrato do `Step` do ADR-0001.

### Grafo real de asmdefs
Conferido nos ADRs 0001 (Emenda 19), 0002 (§9) e 0003 (§9). Não existe código ainda (`Assets/Scripts` não existe), então o grafo vem só do texto dos ADRs.

| asmdef | Engine | Referencia | Abriga |
|---|---|---|---|
| `Forja.Simulation` | não | — | `SimWorld`, `Simulation`, RNG, `SimMath`, `ISimSystem`, `IPhaseSnapshot`, `ITickProbe` |
| `Forja.Data` | não | `Forja.Simulation` | `PhaseSnapshot`, `DataValidator`, baker, `Fnv1a64`, `DefIdTable` |
| `Forja.Data.Editor` | só editor | `Forja.Data` | menu manual de validar e gerar, e o passo de pré-build |
| `Forja.Save` | não | `Forja.Data` | `ISaveService`, `FailureCause`, `IDataResolver` (declara) |
| `Forja.Gameplay.Sim` | não | `Forja.Simulation`, `Forja.Data`, `Forja.Save` | #3, #6, #7, #8, #16, compositor; namespaces `Sim.Host`, `Sim.Log`, `Sim.View` (lógica), `Sim.Budget`, `Sim.Resolve` |
| `Forja.Gameplay` | **sim** | `Forja.Gameplay.Sim` | `AppLifecycle`, `PhaseHost`, o desenho do `PresentationDriver`, `AndroidStorage`, o carregador do `TextAsset` |
| asmdefs de teste | editor | por módulo | EditMode e PlayMode |

```
Forja.Gameplay ─► Forja.Gameplay.Sim ─► Forja.Save ─► Forja.Data ─► Forja.Simulation
                          │                              ▲  (exceção R1: IPhaseSnapshot)
                          ├───────────────────────────────┘
                          └─► Forja.Simulation, Forja.Data
```
`A ─► B` = A referencia B. A `Forja.Data` nunca referencia a `Forja.Save`. O `DataResolver` usa a `Forja.Save`, e o `TextAsset` do snapshot é lido pelo carregador que mora em `Forja.Gameplay` (ADR-0002 §9). O grafo é acíclico.

## Data Flow

### 1. Caminho do frame
```
Input System (#4) ─► InputSample ─────────────────────────────┐ (estado compartilhado, buffer)
                                                              ▼
frame N, thread principal
  AppLifecycle.Update (ordem -200)   esvazia a fila do save: OnMarkFound, Emit
  PhaseHost.Update   (ordem -100)    TickPacer: dt saneado → n ticks (teto MaxTicksPerFrame)
    para cada tick:
      Simulation.Tick(input)         Step: #7 → #8 → #6 → #3 → #16
      DrainEvents()  (UMA vez)       → ITickObserver.OnTickDrained(CurrentTick, eventos, status)
                                          ├─ PhaseLog           (grava o lote no buffer)
                                          └─ PresentationDriver (copia para GhostPool/CardPool)
    fim do frame: IFrameObserver.OnFrameEnd(FrameStats) ─► LoadGovernor (nível de carga)
  LateUpdate  PresentationDriver     lê Alpha (só leitura), sai se IsDiscarded,
                                     desenha em pedaços de N (RenderMeshInstanced)
```
Chamada síncrona na thread principal; o laço de ticks é o único lugar onde o estado do jogo muda. Nada neste caminho cruza thread.

**Orçamento do laço (provisório, sem medição).** O ADR-0010 afirma `4 × 6,0 + 6,5 = 30,5 ms ≤ 33,3 ms` (4 ticks no pior caso, `MaxTicksPerFrame`, mais o resto do frame). Isso cabe no frame de 30 Hz, mas um frame de recuperação de 30,5 ms **estoura o frame de 16,7 ms do alvo de 60 fps** (`FrameRate.Target = 60`, provisório). Alternativas: `MaxTicksPerFrame = 2` com descarte, ou 30 fps na fase. O documento não decide: a escolha fica para o spike (QQ-12), e `X3` e `MEM_CEILING_MB` seguem `NOT ASSESSED`.

### 2. Caminho de eventos
- **Eventos de simulação** (`SimEvent`): produzidos no `Step`, num buffer por tick no Core, e saem por um único `DrainEvents` (a 2ª chamada devolve vazio, ADR-0001 Emenda 19). Log e apresentação consomem sem se conhecerem.
- **Pedidos entre sistemas** (dano, cura, rugido): `Combate.Aplicar`/`Curar`/`PedirRugido` só enfileiram, e só dentro de um `Step` (`SimContext.InStep` lança fora dele). A ordem da fila é contratual.
- **Resultados do save:** o gravador deixa os eventos na fila, e só o `AppLifecycle` os emite, na thread principal e entre frames.
- **Acoplamento:** quatro ganchos neutros em `Sim.Host` e uma saída (`ISessionNoteSink`). O host não referencia log, apresentação nem orçamento.

### 3. Caminho de save e carga
```
BOOT   BeforeSceneLoad → AppLifecycle(DontDestroyOnLoad)
         valida MaxTicksPerFrame → lê o snapshot (TextAsset, síncrono) → DataValidator
         → monta o DataResolver → BootState = Ready → só então o #28 abre o save
         → OnMarkFound → #3 responde MarkAnswer → ConsumeMark (efeito gravado no MESMO commit)
FASE   tela de carregamento: registra observadores
         BeginStage (commit da marca)  ∥  PrewarmRunner.EnsureResident → Warm (passos, 1/frame)
         Create espera os dois → confere ids e R → Preparar (#3, #7, #6) → BeginRun → ticks
FIM    Ended → EndPending → no Update seguinte (ou síncrono em OnApplicationPause(true)):
         hash → OnPhaseEnding (log) → Concluir → Discard → pedido do commit de fim
         → rodapé do log só DEPOIS da resposta do commit → FlushPending
PAUSA  OnApplicationPause(true): Add(AppPaused); RunEndPending se pendente;
         em fase espera o commit de fim já na fila (teto 150–250 ms), nunca cria substituto;
         fora de fase pede um commit e espera (até dois); o log faz FlushSession/FlushPending
```
O #28 só serializa o estado; cada sistema é dono da sua fatia. O save guarda o ID, nunca o índice; um ID desconhecido preserva o registro e deixa o slot indisponível.

**Cruza thread:** gravador do save (thread dedicada, com attach JNI uma vez no plano C e detach num `finally`), `LogWriter` (job do `ThreadPool`, só `System.IO`) e I/O assíncrona de assets (a conclusão volta à thread principal). Todo o resto é a thread principal.

**Bifurcação do `LogWriter`:** ele roda no `ThreadPool` por padrão, mas passa a **thread dedicada** se o `ISaveStorage` cair no plano C (JNI), porque o attach JNI vale por thread (ADR-0008). O `ISaveStorage` precisa ser **seguro para dois chamadores** (save e log): sem estado entre chamadas e com injeção de falha por chamador (ADR-0003, Emenda 1).

### 4. Ordem de inicialização
```
Platform (Unity, URP, Android)
  1. AppLifecycle            BeforeSceneLoad, ordem -200, guarda de duplicata
  2. validação do snapshot   BootState: Pending → Ready | Failed (CatalogInvalid, MaxTicksPerFrameInvalid)
  3. DataResolver            montado do snapshot validado
  4. #28 Save                só com BootState == Ready
  5. LogHost                 existe fora de fase (FlushSession, notas de sessão)
  6. PhaseHost + observadores + PrewarmPlan   por fase, na tela de carregamento
  7. Simulation.Create → Preparar → BeginRun
```
Ordem do `Preparar`: #3, #7, #6 e depois os demais. A do `Step` é #7 → #8 → #6 → #3 → #16. As duas são independentes (ADR-0001, Emenda 19(f)).

## API Boundaries
As assinaturas são as dos ADRs, conferidas no texto atual deles.

### A. Dados → Simulação
```csharp
public interface IPhaseSnapshot { int EntityCapacity, AliveCapacity, EventCapacity, QueueCapacity,
                                  EventCapacityDataTerms; ulong ContentHash; }
public sealed class Simulation {
  static Simulation Create(IPhaseSnapshot s, ulong logHeaderDataHash, ulong masterSeed,
                           ISimSystem[] systemsInExecutionOrder, bool strict, ITickProbe probe);
  void BeginRun();                         // Created → Running, só o compositor, depois do Preparar
  void Tick(ReadOnlySpan<Command> cmds);   // lança em Created, Ended, Broken, Destroyed
  ReadOnlySpan<SimEvent> DrainEvents();    // 1ª chamada após o Tick devolve o lote; as seguintes, vazio
  ulong StateHash();                       // lança em Broken e Destroyed
  void Discard();
  int CurrentTick, CombatTick; SimStatus Status;   // Created, Running, Ended, Broken, Destroyed
}
```
- **O chamador respeita:** `Create` lança se o hash do snapshot difere do `logHeaderDataHash`, se um sistema declara `BudgetLine` fora de {1, 2, 3, 5}, ou se `EventCapacity < R + EventCapacityDataTerms`. O host drena uma vez por tick. Nenhum sistema lê o relógio real.
- **O módulo garante:** o hash é idêntico com a sonda ligada ou desligada; `float32` a 30 Hz; PCG32 em streams; nenhuma referência a `UnityEngine`.

### B. Sistemas de tick
```csharp
public interface ISimSystem { int BudgetLine { get; }      // 1, 2, 3 ou 5
                              void Step(ref SimContext ctx); void Hash(ref StateHasher h); }
// SimContext.InStep: só o Core preenche (construtor internal); default(SimContext).InStep == false
ICombatRequests: Aplicar(ref SimContext, in HitRequest) · Curar(ref SimContext, int alvo, float v)
                 · PedirRugido(ref SimContext, ...)   // só enfileiram; lançam se !ctx.InStep
```
- **O chamador respeita:** o `Step` roda na ordem #7 → #8 → #6 → #3 → #16; os pedidos só valem dentro de um `Step`; a ordem da fila é contratual.
- **O módulo garante:** estouro da fila nunca é silencioso (contador e, no modo estrito, falha); o escritor único de cada coluna é o sistema dono (a exceção é HP = 0 do Core no caminho do NaN).

### C. Ganchos do host (`Sim.Host`)
```csharp
ITickObserver         { void OnTickDrained(int tick, ReadOnlySpan<SimEvent> events, SimStatus status); }
IAppLifecycleObserver { void OnAppPaused(PauseReason r); void OnAppResumed(); void OnAppQuitting(); }
IFrameObserver        { void OnFrameEnd(in FrameStats s); }   // TicksRun, DtUsedTicks, DroppedTicks, DtUsedSeconds
IPhaseEndObserver     { void OnPhaseEnding(in PhaseEndInfo i); }  // 1x por fase, antes de Concluir/Discard/commit
ISessionNoteSink      { void WriteSessionNote(byte noteKind, int code); }  // saída; nula = descarta
static class FrameRate { const int Target = 60; }   // nome do ADR-0007, valor do ADR-0010
enum BootState : byte { Pending = 0, Ready = 1, Failed = 2 }
```
- **O chamador respeita:** os observadores rodam na thread principal, sem alocação, sem lançar (o host envolve cada um em `try/catch`) e sem receber referência com a qual dirigir o laço. O `PhaseHost` expõe só `Alpha` e `IsDiscarded`, somente leitura.
- **O módulo garante:** o `tick` é o `CurrentTick`, monotônico mesmo no `CombatHold`; o tick do `Ended` também é entregue uma vez; uma exceção nunca repete o passo nem impede `Concluir`, `Discard` e o commit.

### D. Save e resolução de IDs
```csharp
public interface ISaveService {            // thread principal, um gravador único atrás
  void RequestCommit(int requestId, CommitKind kind, in SaveSnapshot s);
  void BeginStage(int requestId, in StageMark m);   // falha com MarkUnanswered se Mark == Found
  void CancelStage(int requestId); void ConsumeMark(in MarkAnswer a);
  void RegisterOnMarkFound(MarkFoundHandler h);
  bool TryDequeueResult(out CommitResult r);        // lido entre frames
  MarkState Mark { get; } SaveState State { get; } long EffectiveUtcMs { get; } }
enum CommitOutcome { Pending, Confirmed, Failed }   // nunca "tempo esgotado"
enum FailureCause : byte { None, DiskFull, WriteError, VerifyFailed, StorageUnavailable,
                           ReadOnlyRejected, MarkUnanswered, Unexpected }
public interface IDataResolver { bool TryResolve(DefKind k, string id, out DefRef d);
                                 bool TryGetRevisionHistory(string skillId, out ReadOnlySpan<RevisionStep> h); }
```
- **O chamador respeita:** o save nunca é aberto com `BootState != Ready`; o `requestId` vem de uma fonte única injetada; o `IDataResolver` roda fora do `Step`.
- **O módulo garante:** o save guarda o ID e nunca o índice; um ID desconhecido preserva o registro e deixa o slot indisponível; o `Confirmed` só vem depois do `FsyncDirectory`; em só leitura, os pedidos falham na hora com `ReadOnlyRejected`, sem tocar o armazenamento; o gravador nunca chama o resolvedor.

### E. Orçamento e apresentação
```csharp
public interface ILoadLevelSource { LoadLevel Level { get; } }   // declarada em Sim.View; padrão NullLoadLevelSource
enum LoadLevel { Normal = 0, High = 1 }                           // dono: ADR-0009
PrewarmRunner: EnsureResident(plan, ct)   // termina ou falha; teto ENTRY_MAX_MS − ENTRY_TAIL_MS
               Warm(plan, warmMaxMs, ct)  // melhor-esforço, um PrewarmStep por frame
               ReleasePending()           // marcador ReleaseRequested; o retry desmarca ou recarrega
```
- **O chamador respeita:** a apresentação nunca escreve na simulação nem entra no hash; lê só enquanto `!IsDiscarded`; o aquecimento nunca continua depois do 1º `Tick`.
- **O módulo garante:** o corte do `Warm` é entre passos (passa no máximo a duração do maior passo, `PREWARM_STEP_MAX_MS`).

### Verificação de tipos de motor
- **Sem tipo de motor** nas fronteiras A, B e D: simulação e save usam só `System.*` (`ReadOnlySpan`, `Span`).
- **Com tipo de motor** apenas no host e na apresentação. **Só `Graphics.RenderMeshInstanced` e `RenderParams(material)` estão em `docs/engine-reference/unity/modules/rendering.md`.** `MonoBehaviour`, `DontDestroyOnLoad`, `Application.persistentDataPath`, `Application.targetFrameRate`, `RuntimeInitializeOnLoadMethod`, `TextAsset`, `MaterialPropertyBlock` e `ShaderVariantCollection` são APIs estáveis anteriores ao cutoff, mas não estão na referência local: ficam **`NOT SOURCEABLE`** (não verificadas). `RenderParams.matProps` e `ShaderVariantCollection.WarmUpProgressively` também.

### Contratos que bloqueiam a primeira story
Hoje o documento só diz "a definir na story do dono", mas estes precisam existir **antes da primeira story do #2 ou do #4** (QQ-11):
- **`Command` e o mapeamento `InputSample → Command`** (entrada de `Tick`, base da reprodutibilidade).
- **`IPreparaFase` e `IConcluiFase`.**
- **A sequência do compositor:** `Create → Preparar (#3, #7, #6, demais) → BeginRun → Tick`.
- **`SaveSnapshot`, `StageMark` e `SaveEvent`** (ADR-0003), e o layout dos bytes do cabeçalho.

Não existe `control-manifest.md` ainda; ele nasce com o `/create-control-manifest`, depois que os ADRs forem aceitos.

## ADR Audit

| ADR | Engine Compat | Versão | Post-cutoff sinalizado | Ligação aos GDDs | Conflito com o mapa |
|---|---|---|---|---|---|
| 0001 Simulação | ✅ | ✅ | ✅ | ✅ | nenhum |
| 0002 Dados | ✅ | ✅ | ✅ | ✅ | exceção R1: `Forja.Data → Forja.Simulation` |
| 0003 Save | ✅ | ✅ | ✅ | ✅ | nenhum |
| 0004 Colunas | ✅ | ✅ | ✅ | ✅ | nenhum |
| 0005 Dano | ✅ | ✅ | ✅ | ✅ | nenhum |
| 0006 Geometria | ✅ | ✅ | ✅ | ✅ | nenhum |
| 0007 Ponte e host | ✅ | ✅ | ✅ | ✅ | exceção R2: as interfaces dos ganchos moram na raiz (QQ-10) |
| 0008 Log | ✅ | ✅ | ✅ | ✅ | exceção R2: o `PhaseLog` implementa interfaces da raiz |
| 0009 Render | ✅ | ✅ | ✅ | ✅ | exceção R2: a View implementa `ITickObserver` e lê `PhaseHost.IsDiscarded` |
| 0010 Orçamento | ✅ | ✅ | ✅ | ✅ | o `Sim.Budget` é raiz de composição; o texto "camada: Foundation" do ADR precisa de emenda de redação (QQ-08) |

Todos os 10 estão `Proposed`: nenhum conta como cobertura `✅`. A última revisão de consistência é `docs/architecture/architecture-review-2026-11-10-5.md` (veredito CONCERNS, sem 🔴). **A rodada 8 de emendas veio depois dela e não foi revisada**, então o `/architecture-review` deve rodar de novo antes de aceitar qualquer ADR.

### Ordem de aceite
Vale a ordem do script de dependências (`adr-dep-graph.sh`): **0001 → 0002 → 0003 → 0004 → 0005 → 0006 → 0007 → 0008 → 0009 → 0010**. O ADR-0002 exige o ADR-0001 `Accepted` antes dele, e o ADR-0010 exige o 0007 a 0009 antes. (O technical-director sugeriu 0002 e 0003 antes do 0001; isso contradiz a dependência declarada.)

### Rastreabilidade (linha de base de 128 requisitos ativos)
- **✅ cobertos por ADR `Accepted`:** 0
- **🟡 cobertos por ADR `Proposed`:** 98
- **⚠️ parciais:** 26 (quase todos pontas de GDD ou decisões do usuário; por exemplo `combate-018` e `simulacao-018`)
- **❌ sem ADR:** 4 (`simulacao-020`, `dados-016`, `save-017`, `combate-019`)

A matriz completa, requisito a requisito, está em `docs/architecture/requirements-traceability.md`.

## Required ADRs

**Antes de codar (Foundation e Core):**
- Carregamento de assets e cenas por fase (resolve o M4: Addressables, AssetBundle cru ou cena aditiva). Cobre `horda-015` e destrava a residência do ADR-0010.
- Análise estática e CI (`dados-016`): o `/test-setup` e o gate de pré-produção dependem dele.

**Antes do sistema que os usa:**
- Input e câmera de combate (Input System, joystick de um dedo, `InputSample`), antes do #4.
- Avisos do save para a UI (`save-017`), antes do #30.
- UI de meta-jogo em UI Toolkit, antes do #30.
- Feedback de plataforma/háptico (`combate-019`), antes do #12; a API é `NOT SOURCEABLE`.
- Backend e compras (#29), antes do GDD #26.

**Emendas e artefatos que fecham este documento:**
- Emenda ao ADR-0007: namespace de contratos dos ganchos e `Alpha`/`IsDiscarded` por interface (QQ-10).
- Contratos que bloqueiam a primeira story (`Command`, `InputSample → Command`, `IPreparaFase`, a sequência do compositor, `SaveSnapshot`, `StageMark`, `SaveEvent`) (QQ-11).
- `/create-control-manifest`, depois que os ADRs forem aceitos.

**Pode esperar:** simulação em ponto fixo (`simulacao-020`), áudio (#31), analytics (#34), rede do coop e PvP (#35 e #36), consentimento (#39), e o ADR do #37 Entitlements (Alpha).

## Architecture Principles
1. **A simulação é determinística e não conhece o motor.** `float32`, 30 Hz, PCG32 em streams, sem `UnityEngine` (ADR-0001). É o gargalo do grafo e o maior risco técnico.
2. **Todo valor de gameplay é dado.** Snapshot imutável gerado no build, nunca constante no código (ADR-0002); o save guarda o ID, nunca o índice.
3. **Acoplamento por contratos, não por implementações.** Cada camada só aponta para baixo (com a exceção R1 declarada); só a raiz de composição conhece todas; log, apresentação e orçamento implementam interfaces do `Sim.Host`, e as exceções R2 que sobram estão registradas (QQ-10).
4. **Orçamento medido, nunca suposto.** O que não foi medido fica `NOT ASSESSED` (por exemplo `MEM_CEILING_MB`); o que não tem fonte local fica `NOT SOURCEABLE`; os valores provisórios dos ADRs saem do spike, não de palpite.
5. **Nada falha em silêncio.** Contadores de diagnóstico, causa tipada (`FailureCause`), resultado de commit que nunca é "tempo esgotado", e erro de build para dado inválido (sem clamp).

## Open Questions

| ID | Resumo | Prioridade | Caminho de resolução |
|---|---|---|---|
| QQ-01 | **M4, o carregador dos assets do chefe:** Addressables (pacote fora do `manifest.json`; o ADR-0002 o proíbe para o conjunto embarcado), AssetBundle cru ou cena aditiva por fase | Alta | Decisão do usuário, depois o ADR "Carregamento de assets e cenas por fase" |
| QQ-02 | **`UltimoDanoTick`:** o flash por corpo da horda fica desligado sem ele; a coluna muda o golden hash do #6 | Alta | Decisão do usuário, depois emenda ao ADR-0004 |
| QQ-03 | **Piso do "+5":** `S_max + K + E_3_16 ≥ 5` pode recusar uma fase com poucos spawns especiais enquanto `K` e `E_3_16` valem 0 | Média | Confirmar com o #7 e o #8; sincronizar a redação do GDD #6 |
| QQ-04 | **Fase `Ended` cujo commit de fim não terminou** (o app morre antes do gravador) | Alta | GDD #3 (também o caminho hub e retry do `BeginStage` e a espera do `ConsumeMark`) |
| QQ-05 | **Valores medidos que viram contrato:** `PREWARM_STEP_MAX_MS`, `Step4SyncMs`, `BEGINSTAGE_P95_MS`, `ENTRY_MAX_MS` | Alta | Spikes VR7 e VR11 no aparelho de referência (ainda não verificado) |
| QQ-06 | **Memória da fase:** `MEM_CEILING_MB` segue `NOT ASSESSED` | Média | Spike de memória e a seção de memória do ADR-0010 |
| QQ-07 | **Aparelho de referência e iOS:** o build de iOS não está instalado e o aparelho de teste não foi verificado | Média | `/setup-engine` e o spike de performance |
| QQ-08 | **Texto "camada: Foundation" do ADR-0010** (agora raiz de composição) | Baixa | Emenda de redação ao ADR-0010 |
| QQ-09 | **GDDs ainda ausentes:** 34 de 40 sistemas sem GDD; contratos de Feature, Presentation e Polish pendentes | Média | `/design-system` por sistema, na ordem do `systems-index` |
| QQ-10 | **Namespace de contratos dos ganchos:** publicar as interfaces e os DTOs (`ITickObserver`, `IPhaseEndObserver`, `FrameStats`, ...) sem implementação, e expor `Alpha`/`IsDiscarded` por interface, para a regra R2 valer sem exceção | Média | Emenda ao ADR-0007 |
| QQ-11 | **Contratos da primeira story:** `Command`, `InputSample → Command`, `IPreparaFase`/`IConcluiFase`, sequência do compositor, `SaveSnapshot`, `StageMark`, `SaveEvent` | Alta | Definir antes da primeira story do #2 ou do #4 |
| QQ-12 | **Frame de recuperação de 30,5 ms contra os 16,7 ms de 60 fps:** `MaxTicksPerFrame = 2` com descarte, ou 30 fps na fase | Alta | Spike no aparelho de referência, depois emenda ao ADR-0010 |
| QQ-13 | **Escopo dos ganchos no MVP:** entregar só `ITickObserver` e `IPhaseEndObserver` e adiar `IFrameObserver`, `IAppLifecycleObserver`, `ISessionNoteSink` e `ILoadLevelSource`; `BudgetLine ∈ {1, 2, 3, 5}` é número mágico a nomear | Média | Decisão do technical-director |
| QQ-14 | **Teste de dependência por namespace** dentro de `Forja.Gameplay.Sim`, para impor R1 e R2 onde o compilador não impõe | Média | `/test-setup` |
