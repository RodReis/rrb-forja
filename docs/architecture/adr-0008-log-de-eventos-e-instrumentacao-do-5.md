# ADR-0008: Log de eventos e instrumentação do #5: contrato técnico do arquivo de log por tentativa (`PhaseLog`), cabeçalho, registros, ordem de fim de fase, falha que se anuncia e comparador

## Status
Proposed

## Date
2026-11-06

## Last Verified
2026-11-06 (contra o ADR-0001 com as Emendas 1 a 18, o ADR-0002, o ADR-0003, o ADR-0005, o ADR-0007, `docs/registry/architecture.yaml` e os GDDs #1, #2, #3, #6, #7 e #28 em disco; Unity 6.3 LTS, pin 6000.3.x). **O GDD #5 não existe** (`systems-index.md`: Not Started).

## Decision Makers
Rodrigo Reis (escolheu este ADR e confirmou em 2026-11-06 o escopo "só o contrato técnico, sem o GDD #5" e mandou revisar os pontos do gate; o resto é decisão técnica por recomendação, **provisória, a reavaliar quando o GDD #5 e o jogo jogável existirem**), Claude Code (autoria), `unity-specialist` (validação, 5.5) e `technical-director` (gate TD-ADR, 5.6; veredito CONCERNS, tratado nesta revisão).

## Summary
Os GDDs #1, #2, #3, #7 e #28 mandam vários dados para "o log do #5" (seed antes do tick 0, hash dos dados, tag do build, ABI, ordem dos sistemas, eventos por tick, hash final, resultado, contadores de diagnóstico, eventos do save) e dizem que o #5 é dono do formato, mas o GDD #5 não existe e nenhum ADR fixa como esse log é montado, ordenado, gravado, lido e comparado. Decidido: um **arquivo binário por tentativa** (e um por execução headless, e um por sessão do app para o que acontece fora de fase), montado **em memória** durante a fase pela classe `PhaseLog` (C# puro, thread principal, sem alocação por tick), fechado **depois da resposta do commit de fim** e gravado fora da thread principal por troca atômica sobre o `ISaveStorage`, com checksum FNV-1a de 64 bits no rodapé. O log nunca derruba nem trava o jogo, toda perda é contada e marcada no arquivo, e o comparador devolve **"não comparável"** (nunca "divergência") quando a identidade, o formato, a completude ou o hash final não permitem afirmar nada; o log de uma tentativa no aparelho e o de uma execução headless **são comparáveis entre si** de propósito. O que o aceite mede é do futuro GDD #5.

## Engine Compatibility

| Field | Value |
|-------|-------|
| **Engine** | Unity 6.3 LTS (6000.3.x; editor instalado 6000.3.27f1) |
| **Domain** | Core (serialização binária, gravação em arquivo fora da thread principal, identidade do build) |
| **Layer** | Core (a lista de Required ADRs de `architecture-review-2026-11-06.md`, linha 228, classifica como Core; não existe `docs/architecture/architecture.md` nem mapa de camadas, então a camada é **provisória, a reavaliar**) |
| **Knowledge Risk** | MEDIUM (a superfície de API é BCL do .NET Standard 2.1: `System.IO` via `ISaveStorage`, `ThreadPool`, `Span<byte>`, `BinaryPrimitives`; o risco está no comportamento em runtime no Android e no IL2CPP, que **não é coberto por nenhum arquivo de `docs/engine-reference/unity/`**; a linha do engine é HIGH em `VERSION.md`; não existe `modules/core.md`) |
| **References Consulted** | `docs/engine-reference/unity/VERSION.md`, `breaking-changes.md`, `deprecated-apis.md`; ADR-0001 (Emendas 1, 2, 3, 15 e 18, Key Interfaces, `SimEvent`, `DeathCause`, `EndKind`, Verification Required 7), ADR-0002 (`IDataVersion`, seção 6), ADR-0003 (`ISaveStorage`, `ISaveClock`, `ISaveEventSink`, `CommitResult`, Seções 5 e 6), ADR-0005 (Seção 7, tabela de `SimEventKind`), ADR-0007 (`AppLifecycle`, ordem do frame, Decisão 5); GDDs #1 (Regra 3, `IDataVersion`, AC-I2), #2 (Regras 1, 6, 12, 13; bordas L379, L389, L405 a L408; AC I5), #3 (Regra 9, Regra 14, TR-fluxo-016, X11), #6, #7 (contadores de diagnóstico), #28 (Regra 3: "o log de eventos é telemetria separada", eventos ao #5). **Não existe `modules/core.md`**: nada do domínio Core foi checado contra um módulo de referência (`NOT SOURCEABLE`) |
| **Post-Cutoff APIs Used** | Nenhuma API nova da Unity. `System.Buffers.Binary.BinaryPrimitives`, `System.Threading.ThreadPool` e `System.Span<T>` são BCL anterior ao cutoff; a disponibilidade no perfil de API do projeto (.NET Standard 2.1, `apiCompatibilityLevel: 6`) e o comportamento sob IL2CPP ARM64 são `NOT SOURCEABLE` (Verification Required 1 e 6). O código novo fica em **C# 9**: sem `record struct`, sem namespace com escopo de arquivo, sem `required`. |
| **Verification Required** | (1) `NOT SOURCEABLE`: gravar o arquivo por `ThreadPool` no Android e no IL2CPP sem travar o frame nem gerar lixo relevante que dispare GC na thread principal; a falha de um item de fila não pode derrubar o app; e o **`ISaveStorage` ser seguro para dois chamadores ao mesmo tempo (a thread do save e o `ThreadPool` do log)**, com a implementação Android anexando a thread ao JNI (`AttachCurrentThread`/`DetachCurrentThread`) em cada chamada que o usa. (2) `NOT SOURCEABLE`: a troca atômica do arquivo temporário pelo definitivo (`ISaveStorage.Replace`) e o `FsyncDirectory(log/)` valem para a pasta `log/` como valem para o save (Verification Required do ADR-0003); a visibilidade do arquivo inteiro vem do `Replace`, a durabilidade depois de queda de energia é melhor-esforço (o log é telemetria); sem o `Replace` atômico, o arquivo pode sobrar pela metade e o leitor o reconhece pela ausência de rodapé válido. (3) `NOT SOURCEABLE`: **de onde vêm a tag do build e a ABI** (ADR-0001, Verification Required 7: quais campos a tag deve levar é do spike); enquanto não houver fonte, o campo `Abi` vai vazio, marcado desconhecido, e o comparador devolve "não comparável" (Decisão 6), nunca "comparável". (4) `ISaveEventSink.Emit` é chamado na **thread principal**: o ADR-0003 não diz; este ADR exige (Ordering Note). (5) Ler os contadores de diagnóstico e o `StateHash` com a `Simulation` em `Ended` e em `Broken` não lança onde se espera `indisponível` (o `StateHash` lança em `Broken`, ADR-0001 Emenda 2; os contadores, a confirmar). (6) Zero alocação gerenciada por tick em `WriteBatch` e `WriteHashCheckpoint` em IL2CPP (testado com 300 vivos e o pior tick). (7) Tamanho real do log por fase e o tempo de `Replace` no aparelho de referência, para calibrar `LOG_BUFFER_KB` (estimativa na Seção Performance); **gatilho: se o spike mostrar fase acima de 1 MiB, a Decisão 7 reabre para buffer segmentado em vez de truncar** (truncar perde justamente o fim da fase, o chefe). (8) O arquivo gravado é legível por `adb` em build de desenvolvimento; o método de exportação em release é `NOT ASSESSED` (Decisão 8). (9) A visibilidade entre threads na ARM64 (o retorno "buffer livre" do worker para a principal com `Volatile`/`Interlocked`) e o `LogWriter` esvaziar a fila no `Application.quitting` sem travar o app (Decisão 7). |

## ADR Dependencies

| Field | Value |
|-------|-------|
| **Depends On** | ADR-0001 (`Proposed`; `SimEvent`, `DrainEvents`, `Simulation.Create` com `logHeaderDataHash`, `StateHash`, `EndKind`, `DeathCause`, enums com valores explícitos), ADR-0002 (`Proposed`; `IDataVersion`), ADR-0003 (`Proposed`; `ISaveStorage`, `ISaveClock`, `ISaveEventSink`, `CommitResult`), ADR-0005 (`Proposed`; tabela de `SimEventKind` e payloads), ADR-0007 (`Proposed`; a ordem do frame e o `AppLifecycle`). **Contrato pendente:** o GDD #5 não existe; este ADR decide o contrato técnico e deixa para o GDD o que o aceite mede. Este ADR só pode ser aceito depois dos cinco acima. ADR-0004 e ADR-0006: nenhuma dependência. |
| **Enables** | GDD #5 (nasce com o contrato técnico pronto); o documento de aceite do MVP (`docs/acceptance/mvp.md`, sinais X11 e S1 a S5 do #7); a ferramenta de comparação de logs; o corredor headless e a varredura de balanceamento (#15, que precisam do mesmo cabeçalho) |
| **Blocks** | Stories de log do #5, do `LogSaveEventSink` e da ferramenta de comparação; TR-simulacao-017 e TR-fluxo-010/016 (hoje "Partial"). I5 do #2, R3a, R9 e I6 do #3 e AC-I2 do #1 passam de "BLOQ: #5" a testáveis com o `PhaseLog` real. |
| **Ordering Note** | **Emendas pedidas, a escrever junto com a aceitação deste:** (A) **ADR-0003** (a Emenda já prevista, item 3 da lista de Required ADRs): (i) `ISaveEventSink.Emit` só na thread principal; (ii) `ISaveStorage` **seguro para dois chamadores ao mesmo tempo** (a thread do save e o `ThreadPool` do log), com `PersistentRoot` resolvido uma vez e imutável, a implementação Android anexando a thread ao JNI em cada chamada que o usa, e o contador de falha injetada do `InMemorySaveStorage` seguro para threads; (iii) "nunca `Focus`" só como gatilho de gravação (já previsto no ADR-0007). (B) **ADR-0007**, Decisão 5, duas frases: (i) o `AppLifecycle`, no mesmo ponto fora de fase em que aciona a gravação da pausa, chama `PhaseLog.FlushSession()`; (ii) em `OnApplicationPause(true)` com a tentativa em *Concluindo* (fase terminada, resposta do commit pendente), chama `PhaseLog.FlushPending()`. Nenhuma é feita agora. O ADR de orçamento de frame (depois do spike) decide o custo do `StateHash` por checkpoint. Entradas de registro candidatas: ver Related. |

## Context

### Problem Statement
O aceite do MVP e toda a calibração de balanceamento dependem de observar o que a simulação fez: quantas mortes por causa, tempo até o chefe, picos da horda, escolhas de carta, falhas do save. Os GDDs mandam esses dados para "o log (#5)" e deixam o formato para o #5, mas o #5 não tem GDD, e três ADRs (0001, 0003, 0005) já expõem entradas para ele (`DrainEvents`, `StateHash`, `ISaveEventSink`, `DroppedEvents`) sem dizer para onde vão. Sem um contrato único, cada host gravaria o que quisesse, o arquivo de uma execução headless não seria comparável ao do aparelho, e uma perda silenciosa de evento passaria por log completo. Também faltam decisões que só a engenharia toma: onde o log mora, em que ordem as peças entram quando a fase acaba (o evento ao #5 só sai depois da resposta do commit), como o arquivo falha, e como se compara.

### Constraints
- ADR-0001: eventos são só saída; `DrainEvents()` depois de cada `Tick`; `DroppedEvents` nunca em silêncio; o `Tick` nunca calcula hash e nunca lê relógio; `Simulation` na thread principal; zero alocação gerenciada por `Tick`; sem `static` mutável; `Simulation.Create` confere o hash do snapshot contra o `logHeaderDataHash`, então o cabeçalho existe **antes** do `Create`; `StateHash` lança em `Broken`.
- ADR-0003: a thread principal nunca bloqueia no disco; o armazenamento é `ISaveStorage` injetável, com versão em memória e injeção de falha; os resultados voltam por fila esvaziada entre frames; o gravador do save liga o `Dispose` ao `Application.quitting`.
- GDD #28 (Regra 3): o log de eventos **não** vai para o save. É telemetria separada.
- GDD #3 (Regra 9): ordem de fim de fase: drenar, `StateHash`, `IConcluiFase`, descartar, commit de fim, e só então o evento ao #5, que sai mesmo se o commit falhar, marcado "commit falhou". O abandono segue a mesma ordem.
- GDD #1: o cabeçalho de cada partida e de cada execução headless leva hash, rótulo, tag do build e o pacote remoto aplicado; sobrescritas rejeitadas entram no log.
- Dev solo, uma pessoa valida: poucas classes, formato simples, ferramenta de leitura pequena.
- Aparelho móvel: zero alocação por tick; um arquivo por fase de poucas centenas de KB.

### Requirements
- Cabeçalho completo antes do tick 0 (TR-simulacao-017) e rodapé com resultado, hash final e status do commit (TR-fluxo-010, TR-fluxo-016).
- Todos os eventos de saída entregues ao log sem perda silenciosa (AC I5 do #2).
- Contadores de diagnóstico dos sistemas coletados sem acoplar o log aos sistemas.
- Um comparador que distingue "idêntico", "divergência no tick T" e "não comparável", e que compara o aparelho com o headless.
- O log falha sem derrubar o jogo e sem enganar o leitor.
- O mesmo código roda no jogo e no corredor headless.

## Decision

### 1. Escopo e donos
- **Deste ADR:** o contêiner do arquivo, o cabeçalho, os tipos de registro, a ordem em que as peças entram, a gravação e a retenção, a falha, o comparador, a interface de entrada (`IPhaseLog`) e a de contadores (`ICounterSource`).
- **Do futuro GDD #5:** o que o aceite mede, as contas derivadas (contagem de mortes de fase por causa por `Resultado.ContaComoMorteDeFase`, `OfertasNoRugido` pelos `NiveisGanhos` do #3, dano de contato somado a partir dos eventos do #6), o relatório e o método de exportação em release. Nada disso é decidido aqui (`NOT ASSESSED`, lista em GDD Sync). **Os valores de retenção, de buffer e de cadência de checkpoint abaixo são padrões provisórios que o GDD #5 pode sobrescrever.**
- O log é **somente saída**: nenhum sistema da simulação o lê (Alternative 7).

### 2. Três peças e uma fronteira
- **Lógica pura** em `Forja.Gameplay.Sim.Log` (C# 9 sem `UnityEngine`; mesmo asmdef do `TentativaDeFase`, namespace à parte dos sistemas de tick): `PhaseLog`, `LogWriter` (empacota, calcula o checksum e grava), `LogReader`, `LogComparer`, `ICounterSource`, as structs de registro e os enums. Roda em EditMode.
- **Host** em `Forja.Gameplay` (com Unity): o `LogHost` cria no boot os buffers persistentes, o `PhaseLog` de cada fase, fornece o `BuildIdentity` e a implementação de `ISaveStorage` (a do ADR-0003), despacha o `LogWriter` para o `ThreadPool` e faz o desligamento (Decisão 7). Não tem regra de jogo.
- **`LogSaveEventSink`**: implementa `ISaveEventSink` do ADR-0003 e escreve no log de sessão (ou no da fase, se houver). Inscreve-se no boot; recebe o buffer de eventos do boot.
- **Fronteira:** `Forja.Simulation` e os sistemas chamados por `ISimSystem.Step` **nunca** referenciam o namespace `Forja.Gameplay.Sim.Log`; no mesmo asmdef do `TentativaDeFase` isso é regra de revisão de código **registrada em `forbidden_patterns`**. Quem alimenta o log é o host, com o que `DrainEvents()` devolve.

### 3. Três tipos de arquivo, um contêiner
`LogKind`: `Phase = 1` (uma tentativa no jogo), `Headless = 2` (uma execução sem tela) e `Session = 3` (eventos fora de fase de uma sessão do app: eventos do save no boot, `AppFechado`, "fase desconhecida", rejeições de pacote remoto, "relógio atrás"). Contêiner comum, **little-endian**, só `Span<byte>` (como variável local) e `BinaryPrimitives`, campo a campo:
```
magic "FJLG" (4)  | FormatVersion u16 | LogKind u8 | HeaderLength u16 | Header ... | Record* | Footer
Record = Type u8 | Length u16 | Payload[Length]     (Type desconhecido: o leitor pula pelo Length)
Footer = Type 0xFF | Length u16 | campos | Checksum u64   (FNV-1a de 64 bits, por byte, de todos os bytes anteriores)
```
- **Tipos de registro** (valores explícitos; só crescem no final): `EventBatch = 1`, `HashCheckpoint = 2`, `Counters = 3`, `HostNote = 4`, `External = 5`.
- `EventBatch`: `Tick i32`, `Count u16`, depois `Count` eventos de 21 bytes: `Kind u8, ActorId i32, TargetId i32, Value f32 (bits por BitConverter.SingleToInt32Bits), ArgA i32, ArgB i32`. O `Tick` do lote é o de todos os eventos (assert em desenvolvimento). **Só se escreve lote em tick com pelo menos um evento**; o rodapé leva o último tick, e o leitor reconstrói "lotes com `Tick` crescente" (AC I5 do #2). Nunca se grava `SimEvent` por cópia de memória (`MemoryMarshal`): campo a campo, para o layout não depender do compilador.
- `HashCheckpoint`: `Tick i32`, `Hash u64`. Escrito pelo host a cada `LOG_HASH_EVERY_TICKS` ticks (padrão 0 no jogo = só o hash final do rodapé; 30 no corredor headless) *(provisória; o GDD #5 pode sobrescrever)*; o `StateHash` é calculado pelo host **fora do `Tick`**, entre ticks.
- `Counters`: lista de pares `(CounterId u16, Value i64, Available u8)`. Cada sistema dono declara os seus ids num enum de valores explícitos que só cresce (por exemplo os do #7: `HordaEsperouTicks`, `EliteEsperouTicks`, `HordaCancelada`, `ElitesCancelados`, `TicksNoTeto`, `VivosHordaNoElite`, `TicksNoCanto`; e os do Core: `CommandsRejected`, `SpawnsRejected`, `NonFiniteCount`, `DroppedEvents`). `Available = 0` quando o valor não pôde ser lido (`indisponível`, nunca 0).
- `HostNote`: `NoteKind u8` (`SeedDrawn = 1`, `Abandoned = 2`, `Exception = 3`, `CommitFailed = 4`, `PhaseRejected = 5`, `LogDegraded = 6`, `DataOverrideRejected = 7`), `Tick i32` (-1 se fora de tick), `Code i32`, `Text` (UTF-8 de até 256 bytes, só nas exceções; o corte cai **em fronteira de caractere**, nunca no meio de um byte multibyte).
- `External`: `Source u8` (`Save = 1`, `Data = 2`), `Code i32`, `A i64`, `B i64`: o `SaveEvent` do #28 e as rejeições de pacote do #1 caem aqui. O significado de `Code` por fonte é definido junto com o `SaveEvent` na 1ª story do #28 (ADR-0003 L170).

### 4. Cabeçalho (antes do tick 0 e antes do `Create`)
Montado a partir de fontes injetadas e escrito **antes** de `Simulation.Create`, porque o `Create` compara o hash do snapshot com o `logHeaderDataHash` (Emenda 1):
`LogKind`; `AttemptId` (128 bits, do #3); `MasterSeed u64` (a seed sorteada pelo `ISeedSource`, **gravada antes do tick 0**, GDD #2 Regra 1.2); `DataHash u64` e `DataLabel` (de `IDataVersion`, ADR-0002); `AppliedPackHash u64` (0 = nenhum) e `CandidatePackHash u64` (corredor headless com candidato; nunca persistido); `BuildTag` (string) e `Abi` (string; **vazia = desconhecida**); `Strict u8`; `TicksPerSecond u8` (30); `SystemsOrder` (lista de ids de sistema na ordem do compositor) e `PreparerOrder` (lista dos `IPreparaFase` na ordem em que o compositor os chama, GDD #3 TR-fluxo-016); `PhaseId` e `HeroId` (IDs de texto do #1); `StartUtcMs i64` (informativo, de `ISaveClock`, **fora do comparador**). A tag do build e a ABI vêm de um `BuildIdentity` fornecido pelo host; **de onde vêm é `NOT SOURCEABLE`** (Verification Required 3) e o ADR não inventa campos. As strings do cabeçalho são codificadas **uma vez por fase**, na tela de carregamento (alocação ali é aceitável).

### 5. `IPhaseLog`: a interface de entrada e a ordem
```
host, no boot                  : LogHost cria os buffers persistentes (2 de fase + 1 de sessao)
host, na tela de carregamento  : PhaseLog = LogHost.Open(kind)                  // pega um buffer de fase livre; sem alocacao por tick
host, apos seed e antes do Create : BeginPhase(in LogHeader)                    // HostNote SeedDrawn
por tick executado             : events = Simulation.DrainEvents(); WriteBatch(tick, events)   // so se events.Length > 0
a cada N ticks (opcional)      : WriteHashCheckpoint(tick, hash)
no fim (ordem do GDD #3, Regra 9), igual para vitoria, derrota, abandono, excecao e falha interna:
  1. DrainEvents final -> WriteBatch (no abandono nao ha Tick: so a nota Abandoned)
  2. StateHash -> guarda no EndInfo (em Broken: indisponivel, sem lancar para fora do log)
  3. ICounterSource.Collect -> WriteCounters (cada fonte; erro de uma = Available 0 so dela)
  4. IConcluiFase, Discard, pedido do commit de fim
  5. quando a resposta do commit chega pela fila da ponte (entre frames): EndPhase(in EndInfo, commitStatus)
     -> escreve o rodape, entrega o buffer ao LogWriter
```
- **O rodapé só é escrito no passo 5**, depois da resposta do commit (GDD #3, Regra 9 passo 4), **também no abandono** (o abandono não é um atalho que pula a espera do commit). Se o commit falha, `CommitStatus = Falhou` e o rodapé sai **mesmo assim** (o aceite não perde a contagem).
- **`Pending`.** Se o app vai para segundo plano com a tentativa em *Concluindo* (a resposta do commit ainda não veio), o `AppLifecycle` chama `PhaseLog.FlushPending()` (Ordering Note B): o `PhaseLog` **copia a parte usada** do buffer (uma alocação, rara, fora do tick), escreve nela um rodapé provisório com `CommitStatus = Pending` e a entrega ao `LogWriter`; o buffer original continua com o `PhaseLog`. Se a resposta chega depois (o app voltou), o passo 5 roda normalmente e **regrava o mesmo nome por `Replace`** com o status final (`Confirmado` ou `Falhou`). Se o app é morto antes, fica o arquivo com `Pending`, que o comparador trata como não conclusivo (Decisão 6). Em *Em andamento* ou *Pausada* **não há flush**: a fase não é retomável e o log dela se perde se o app morre (o `AppFechado` entra pelo log de sessão do boot seguinte).
- **Exceção na simulação** (`Quebrada`): `HostNote Exception` com o texto; `StateHash` indisponível; os contadores que o Core permitir ler; rodapé normal (GDD #3, Regra 14).
- **Vitória e derrota no mesmo tick:** os dois eventos já estão no lote; o rodapé leva `MorteSimultanea` (GDD #2 L390).
- Tudo na **thread principal**; o `PhaseLog` guarda o id da thread no construtor e lança em desenvolvimento se for chamado de outra (o `LogWriter`, em segundo plano, só recebe o buffer já fechado).

### 6. Rodapé e o comparador
**Rodapé:** `EndKind u8`, `FailureDetail u8`, `ResultCause u8` (o enum de causas do #3, valores explícitos), `MotivoFim u8`, `FinalLevel i32` (-1 = indisponível), `ChefeVisto u8`, `MorteSimultanea u8`, `CombatTickFinal i32` (-1), `FinalTick i32`, `FinalHashAvailable u8` e `FinalHash u64`, `CommitStatus u8` (`NaoPedido = 0`, `Confirmado = 1`, `Falhou = 2`, `Pendente = 3`), `Flags u16` (`Truncated = 1`, `Degraded = 2`), `RecordsWritten i32`, `RecordsDropped i32`, `LogFaults i32` e o checksum.

**`LogComparer.Compare(a, b)`** devolve `Identical`, `Divergence(tick, primeiroDiferente)` ou `NotComparable(motivo)`, nesta ordem de precedência:
1. **`NotComparable(motivo)`**, se qualquer uma destas vale:
   - **Tipo:** qualquer lado é `Session`, ou o `FormatVersion` é ilegível. **`Phase` e `Headless` comparam entre si de propósito** (é o objetivo do comparador: aparelho contra corredor headless); o `LogKind` não entra na identidade entre os dois.
   - **Completude:** arquivo **incompleto** (sem rodapé válido, ou checksum que não bate), `Truncated` ou `Degraded` em qualquer lado.
   - **Identidade:** `Abi` ou `BuildTag` **vazios ou diferentes**; `DataHash`, `AppliedPackHash`, `CandidatePackHash`, `SystemsOrder`, `PreparerOrder`, `MasterSeed`, `Strict`, `TicksPerSecond`, `PhaseId` ou `HeroId` diferentes.
2. **`Divergence(tick, kind)`:** comparáveis, e o primeiro lote que difere, ou o primeiro `HashCheckpoint` que difere **em um tick onde os dois lados têm checkpoint**. Um checkpoint que existe só de um lado é **ignorado** (a cadência pode diferir: 0 no jogo, 30 no headless); a divergência então aparece nos lotes ou no hash final.
3. **`NotComparable(HashFinalIndisponivel | CommitPendente)`:** nenhuma divergência achada, mas `FinalHashAvailable = 0` (estado `Broken`, abandono) ou `CommitStatus = Pendente` em qualquer lado: não dá para afirmar "idêntico". Uma divergência achada antes **vale** (um problema conhecido não é rebaixado a "não conclusivo").
4. **`Identical`:** comparáveis, todos os lotes iguais, os checkpoints comuns iguais, o hash final igual e `EndKind`, `ResultCause` e `FinalTick` iguais.

**Ficam fora do veredito, de propósito:** `StartUtcMs`, `Text`, os registros `External` e `HostNote` (os eventos do save diferem entre aparelho e headless) e os `Counters` (são informativos; o relatório do GDD #5 pode compará-los à parte). **"Não comparável" nunca vira "divergência"** (GDD #2 L405) e **valor ausente nunca vira permissivo**: `Abi` vazia é "não comparável", não "igual".

### 7. Memória, gravação, desligamento e falha
- **Buffers persistentes.** O `LogHost` cria **no boot**, uma vez, três `byte[]`: dois de fase de `LOG_BUFFER_KB` (padrão provisório 1024) e um de sessão de `LOG_SESSION_KB` (padrão 64); nenhum é criado por fase (evita fragmentar o heap com objetos grandes). O fim de cada buffer reserva `LOG_RESERVE_BYTES` (padrão 512) para o rodapé, o último lote e as notas críticas. Cheio o buffer, o `PhaseLog` **para de gravar lotes e checkpoints**, soma em `RecordsDropped`, liga `Truncated` e continua a contar; o rodapé sempre cabe. Nada é descartado em silêncio: o contador e a flag vão no arquivo. O buffer volta a ficar livre pelo worker com `Volatile.Write`/`Interlocked` (a ARM64 tem modelo de memória fraco; um `bool` simples não basta). `PhaseLog` e o job de gravação guardam `byte[]` e `int` (comprimento usado); o `Span` só existe como variável local, dentro de cada método e do worker. `CounterWriter` é `ref struct`.
- **Gravação.** O fim fecha o buffer e o `LogWriter` o grava no `ThreadPool`: `QueueUserWorkItem` com um `WaitCallback` em cache (campo `static readonly`, sem estado mutável) e um objeto `WriteJob` reutilizável (`buffer`, `length`, tipo, nome) como estado, para não criar closure. O **worker** calcula o FNV-1a e escreve o rodapé final (a thread principal só preenche o corpo), grava `log/<nome>.tmp` por `ISaveStorage.WriteAll(ReadOnlySpan<byte>)` com **só os bytes usados** (`length`, centenas de KB), `Replace` para `log/<nome>.fjlog` e `FsyncDirectory(log/)`. A visibilidade do arquivo inteiro vem do `Replace`; a durabilidade depois de queda de energia é melhor-esforço. Se os dois buffers de fase estão ocupados, o log novo é descartado e conta `LogFaults`, nunca bloqueia. **O log de sessão tem o buffer próprio** e nunca disputa os de fase.
- **Nome e numeração.** `fase-<seq6>.fjlog`, `headless-<seq6>.fjlog`, `sessao-<seq6>.fjlog`, com `seq` único: lido pelo **primeiro job do pool no boot** (`TryList` da pasta, fora da thread principal) e depois incrementado com `Interlocked`; os jobs seguintes esperam o fim desse primeiro com um `ManualResetEventSlim` (no worker, nunca na thread principal). O nome é escolhido no worker. Sem relógio no nome. O log de sessão usa o **mesmo `seq` em todas as reescritas** da sessão e é **reescrito inteiro** por `Replace`.
- **Quando grava.** Fase: depois do `EndPhase` (ou do `FlushPending`). Sessão: no fim de cada fase e no `OnApplicationPause(true)` fora de fase (Ordering Note B). Um app morto no meio de uma fase **perde o log daquela fase** (aceito, Decisão 5).
- **Retenção.** O mesmo primeiro job do boot, antes da primeira fase, apaga os mais antigos de cada tipo: `Phase` até `LOG_MAX_FILES` (50) arquivos e `LOG_MAX_TOTAL_KB` (20000); `Headless` até 50 e 20000; `Session` até 10 e 1024. Falha de `Delete` é contada e ignorada. *(provisória; o GDD #5 pode sobrescrever.)*
- **Desligamento.** O `LogWriter` mantém um contador de itens pendentes (`Interlocked`) e um `ManualResetEventSlim`. O `LogHost` se desliga em `Application.quitting` e na saída do Play Mode: não aceita itens novos, espera os pendentes por até `LOG_SHUTDOWN_WAIT_MS` (padrão 200) e **abandona** o que sobrar (o `.tmp` não vira definitivo sem o `Replace`). `LogHost` e `LogWriter` não têm estado `static` mutável (com domain reload desligado, um item de um Play Mode anterior continua rodando durante o seguinte), e o item de fila é idempotente. O `try/catch` é o mais externo do callback do worker (uma exceção não tratada num item do pool derruba o processo). Nenhuma API de `UnityEngine` é chamada no worker: a raiz de `ISaveStorage` é resolvida uma vez no boot.
- **Falha nunca sobe.** Todo método público do `PhaseLog` e do `LogWriter` captura exceções, soma `LogFaults`, liga `Degraded` e escreve uma `HostNote LogDegraded` enquanto couber. Nenhuma exceção do log chega ao laço de ticks nem ao fluxo de fase. Em modo estrito (testes), `DroppedEvents != 0` continua falhando o teste como manda o ADR-0001, e o log só registra.

### 8. Local, formato dos dados e exportação
- Os arquivos moram em `ISaveStorage.PersistentRoot + "/log/"` (a raiz do save, no armazenamento privado do app). **Não vão para o save** (GDD #28) e não entram no Auto Backup do `save.dat`. Sem rede, sem identificador do aparelho, sem dado pessoal: o `AttemptId` é aleatório.
- O arquivo é autocontido e copiável. O método de **exportação em release** (botão de compartilhar, `adb` com `run-as` só em build de desenvolvimento) é do GDD #5 e do #12: **`NOT ASSESSED`** aqui.
- A ferramenta `LogReader` com `Dump` em texto (uma linha por registro) vive em `Forja.Gameplay.Sim.Log` e é testada em EditMode; é o que o GDD #5 usa para tirar relatório. O `LogComparer` é a ferramenta de comparação.

### Architecture Diagram
```
 DrainEvents() / StateHash / Counters / Resultado (#3)       ISaveEventSink.Emit (#28, thread principal)      IDataVersion (#1)   BuildIdentity (host)
        │                                                              │                                       │                  │
        └──────────────▶  host (PhaseHost / TentativaDeFase / LogHost) ┴──▶ PhaseLog  <───── LogHeader ────────┴──────────────────┘
                                                                           │  (thread principal; buffers persistentes; sem alocacao por tick)
                          EndPhase (apos resposta do commit)  /  FlushPending (em Concluindo)  /  FlushSession (fora de fase)  [AppLifecycle]
                                                                           ▼
                                                    LogWriter (ThreadPool, 1 job por arquivo; checksum e rodape no worker)
                                                                           ▼
                           ISaveStorage.WriteAll(log/x.tmp) ─▶ Replace(log/x.fjlog) ─▶ FsyncDirectory(log/)      [seq e retencao: 1º job do boot]
                                                                           ▼
                           LogReader / Dump (EditMode)     LogComparer ─▶ Identical | Divergence(tick) | NotComparable(motivo)   (Phase x Headless comparam)
 Forja.Gameplay.Sim.Log (C# puro, EditMode):  PhaseLog, LogWriter, LogReader, LogComparer, ICounterSource, registros
 Forja.Gameplay (Unity):                      LogHost, LogSaveEventSink
```

### Key Interfaces
```csharp
namespace Forja.Gameplay.Sim.Log   // C# 9 puro, sem UnityEngine; outro namespace que o dos ISimSystem; EditMode
{
    public enum LogKind : byte { Phase = 1, Headless = 2, Session = 3 }                       // valores explicitos; so cresce no final
    public enum RecordType : byte { EventBatch = 1, HashCheckpoint = 2, Counters = 3, HostNote = 4, External = 5, Footer = 0xFF }
    public enum CommitStatus : byte { NotRequested = 0, Confirmed = 1, Failed = 2, Pending = 3 }
    [System.Flags] public enum LogFlags : ushort { None = 0, Truncated = 1, Degraded = 2 }

    public readonly struct BuildIdentity { public readonly string BuildTag; public readonly string Abi; }   // Abi vazia = desconhecida (NOT SOURCEABLE)

    public interface ICounterSource { void Collect(ref CounterWriter w); }                    // CounterWriter e ref struct; ids em enum proprio, explicito, so cresce

    public interface IPhaseLog                                                                // thread principal; nunca lanca para o chamador
    {
        void BeginPhase(in LogHeader header);                                                 // antes do Simulation.Create
        void WriteBatch(int tick, System.ReadOnlySpan<SimEvent> events);                      // so se events.Length > 0
        void WriteHashCheckpoint(int tick, ulong stateHash);
        void WriteCounters(ICounterSource source);
        void WriteNote(in HostNote note);
        void WriteExternal(in ExternalEvent e);
        void EndPhase(in EndInfo end, CommitStatus commit);                                   // depois da resposta do commit; tambem no abandono; regrava apos FlushPending
        void FlushPending();                                                                  // em Concluindo, ao ir para segundo plano: copia o usado, rodape Pending, entrega
        void FlushSession();                                                                  // fora de fase; nao bloqueia
        LogFlags Flags { get; }  int RecordsDropped { get; }  int LogFaults { get; }
    }

    public enum CompareOutcome : byte { Identical = 0, Divergence = 1, NotComparable = 2 }
    public static class LogComparer { public static CompareResult Compare(LogReader a, LogReader b); }   // NotComparable tem motivo; nunca vira Divergence; Phase x Headless comparam
}
```

### Implementation Guidelines
- O `PhaseLog` **must** usar buffers criados no boot e **must never** alocar memória gerenciada por tick (`WriteBatch`, `WriteHashCheckpoint`); strings entram só no cabeçalho, nas notas de exceção e no rodapé.
- `Forja.Simulation` e qualquer sistema chamado por `ISimSystem.Step` **must never** referenciar `Forja.Gameplay.Sim.Log`, e nenhum sistema **must** ler o log (nem para decidir regra).
- O host **must** escrever o cabeçalho antes do `Simulation.Create` e **must** gravar o rodapé final só depois da resposta do commit de fim, inclusive no abandono; o evento ao #5 **must never** sair antes da resposta do commit. Ao ir para segundo plano em *Concluindo*, **must** entregar com `Pending` e regravar depois.
- Todo valor de enum que vai para o arquivo **must** ser explícito e só crescer no final; um `switch` sobre eles **must** ter `default` que lança no leitor de testes e que **registra e pula** no leitor de produção (tipo de registro desconhecido é pulado pelo `Length`).
- Toda perda de registro **must** somar em `RecordsDropped` e ligar `Truncated`; toda falha do próprio log **must** somar em `LogFaults` e ligar `Degraded`. Nenhum caminho **must** descartar em silêncio.
- O comparador **must** devolver `NotComparable` quando `Abi`, `BuildTag` ou qualquer campo de identidade estiver vazio, diferente ou desconhecido, quando o hash final estiver indisponível ou o commit pendente sem divergência achada, e **must never** devolver `Divergence` para um par que não é comparável.
- Nenhuma exceção do log **must** chegar ao laço de ticks, ao `TentativaDeFase` ou à UI; o `try/catch` **must** ser o mais externo do callback do worker.
- `ISaveEventSink.Emit` **must** ser chamado na thread principal, e `ISaveStorage` **must** ser seguro para dois chamadores ao mesmo tempo (Emenda ao ADR-0003).
- Os contadores **must** ser lidos pelo host **antes** do `Discard` e cada fonte **must** poder marcar `Available = 0` sem derrubar as outras.
- O `StateHash` **must** ser calculado pelo host fora do `Tick` e, em `Broken`, marcado `indisponível` sem lançar para fora do log.
- `LogHost` e `LogWriter` **must never** ter estado `static` mutável; o item de fila **must** ser idempotente; nenhuma API de `UnityEngine` **must** ser chamada no worker.
- O retorno de um buffer livre do worker para a thread principal **must** usar `Volatile` ou `Interlocked`; `Span<T>` **must never** ser campo de classe nem ser capturado.
- Testes em `Assets/Tests/EditMode/Log/` (formato, leitor, comparador, falhas, buffer cheio, ordem de fim, `Pending`) com `InMemorySaveStorage` (injeção de falha) e relógio falso; `Assets/Tests/PlayMode/` só para o `LogHost`, o `ThreadPool` e o desligamento.

## Alternatives Considered

### Alternative 1: texto linha a linha (JSON Lines), gravado em segundo plano durante a fase
- **Description**: cada lote vira uma linha de texto escrita por uma thread de segundo plano à medida que a fase corre.
- **Pros**: legível sem ferramenta; um app morto no meio deixa o que já foi escrito.
- **Cons**: formatar texto aloca (strings, `StringBuilder`) e o lixo de uma thread dispara coleta de lixo que pausa a thread principal (o ADR-0003 já evitou isso no gravador do save); `float` em texto precisa de cultura invariante e ida e volta exata para o comparador; escrever durante a fase mantém disco em uso no caminho quente; o comparador precisa de bits exatos.
- **Rejection Reason**: a política do projeto é zero alocação e bits exatos. O `Dump` em texto no leitor dá a legibilidade sem pagar o custo no jogo.

### Alternative 2: só memória, sem arquivo
- **Description**: o log vive na sessão e é lido por uma tela de depuração.
- **Pros**: nada de disco, nada de retenção.
- **Cons**: o aceite do MVP precisa de dados entre sessões e entre aparelhos; a execução headless e o aparelho precisam do mesmo artefato para comparar.
- **Rejection Reason**: o aceite e o comparador exigem artefato persistente.

### Alternative 3: gravar por lote com `fsync` (arquivo único que cresce)
- **Description**: abrir o arquivo da fase e dar `append` e `fsync` a cada lote.
- **Pros**: sobrevive à morte do app; nada se perde.
- **Cons**: disco e `fsync` no caminho quente de cada tick; o ADR-0003 proíbe bloquear a thread principal no disco; uma fase não retomável não ganha com o log parcial.
- **Rejection Reason**: o custo supera o ganho; o `AppFechado` já entra pela marca do save.

### Alternative 4: reusar o arquivo do save
- **Description**: gravar o log junto do `save.dat`.
- **Pros**: um arquivo só, um commit.
- **Cons**: o GDD #28 (Regra 3) proíbe: o log é telemetria separada; misturar o tamanho variável do log com o envelope atômico do save arrisca o save.
- **Rejection Reason**: contradiz o GDD #28.

### Alternative 5: uma thread própria para o log (espelho do gravador do save)
- **Description**: `Thread` dedicada com parada cooperativa, como no ADR-0003.
- **Pros**: controle da vida da thread; mesma disciplina do save; sem depender do pool.
- **Cons**: mais código de ciclo de vida para um arquivo por fase; o log é melhor-esforço.
- **Rejection Reason**: YAGNI. Um job de `ThreadPool` por arquivo basta, com o desligamento da Decisão 7; trocar por thread própria é um ajuste interno do `LogWriter` se o spike pedir (Verification Required 1).

### Alternative 6: serviço de analytics de terceiros
- **Description**: enviar os eventos a um SDK externo.
- **Pros**: painéis prontos.
- **Cons**: o MVP é offline; dados pessoais e identificadores entram; dependência nova; o #34 (Analytics e live ops) é pós-lançamento e pode ser reduzido a este log.
- **Rejection Reason**: fora do escopo do MVP.

### Alternative 7: o log como canal para outros sistemas (o #3 lê o log para contar)
- **Description**: sistemas consultam o log para decidir regra.
- **Pros**: nenhuma duplicação de contadores.
- **Cons**: viola "eventos são só saída" e a ordem de assinatura vira regra (ADR-0001).
- **Rejection Reason**: proibido pelo registro (`forbidden_patterns`, eventos são só saída).

### Alternative 8: o comparador recusa `Phase` × `Headless` (rascunho inicial)
- **Description**: `LogKind` na identidade do comparador.
- **Pros**: regra mais simples.
- **Cons**: o aparelho contra o corredor headless, que é o propósito do comparador, ficaria sempre "não comparável".
- **Rejection Reason**: apontada pelo `technical-director` (contradição 1); só `Session` é recusado.

## Consequences

### Positive
- Um contrato único para o que entra no log, em que ordem e com que garantia, fechando TR-simulacao-017 e TR-fluxo-010/016 sem esperar o GDD #5.
- Nenhuma perda silenciosa: buffer cheio, falha de disco, arquivo incompleto, commit pendente e hash final ausente aparecem no próprio arquivo e no comparador.
- O corredor headless e o jogo produzem o mesmo artefato e se comparam entre si; "não comparável" deixa de ser confundido com "divergência".
- Zero alocação por tick; a gravação gera pouco lixo, fora do tick e uma vez por arquivo.

### Negative
- Um app morto no meio de uma fase perde o log daquela fase (o `AppFechado` entra pelo log de sessão).
- Um formato binário próprio exige leitor e `Dump`; o GDD #5 depende deles para qualquer relatório.
- Duas emendas a ADRs ainda `Proposed` (ADR-0003 com três itens, ADR-0007 com duas frases).
- **Até a Verification Required 3 fechar (fonte da tag do build e da ABI), a comparação aparelho × headless, que é o propósito do comparador, fica indisponível: todo par sai `NotComparable`.** O comparador só serve para dois logs do mesmo build até lá.
- Memória fixa de cerca de 2 MiB + 64 KiB para buffers persistentes.
- Os valores de `LOG_BUFFER_KB`, `LOG_SESSION_KB`, `LOG_MAX_FILES`, `LOG_MAX_TOTAL_KB` e `LOG_SHUTDOWN_WAIT_MS` são palpites até o spike.

## Risks
- **Fonte da tag do build e da ABI (`NOT SOURCEABLE`):** sem ela, todo log sai "não comparável". Mitigação: o comparador trata o campo vazio como não comparável (nunca como igual), e a Verification Required 3 é do spike do ADR-0001.
- **`ThreadPool` no Android/IL2CPP (`NOT SOURCEABLE`):** pode atrasar ou gerar lixo; o GC do Unity para todas as threads. Mitigação: um job por arquivo, buffers persistentes entregues sem cópia, pouco lixo fora do tick, e plano B de thread própria (Alternative 5).
- **`ISaveStorage` chamado por duas threads:** corrida no fake e, no Android, falha do plano C do `Replace` por JNI sem attach. Mitigação: a Emenda ao ADR-0003 (seguro para dois chamadores, attach por chamada) e a Verification Required 1.
- **Item do pool vivo depois do fim do app ou do Play Mode:** com domain reload desligado, reaproveitaria estado. Mitigação: sem `static` mutável, item idempotente, desligamento com espera curta (Decisão 7).
- **Escrita parcial por morte do app durante o `Replace`:** o arquivo temporário sobra; o definitivo ou existe inteiro ou não existe. O leitor também reconhece arquivo sem rodapé válido como incompleto.
- **Buffer cheio perde o fim da fase (o chefe):** a truncagem para os lotes e marca `Truncated`, e o par vira `NotComparable`. Mitigação: o gatilho da Verification Required 7 (buffer segmentado se o spike mostrar fase acima de 1 MiB).
- **Estados de `Simulation` em que ler contadores ou hash lança:** cada fonte marca `Available = 0`; o `StateHash` em `Broken` é `indisponível`. Mitigação: Verification Required 5.
- **`ISaveEventSink.Emit` em outra thread:** corromperia o buffer do log. Mitigação: o assert de thread do `PhaseLog` em desenvolvimento e a Emenda ao ADR-0003.
- **Sem GDD #5, o que o aceite mede pode exigir novo tipo de registro:** os tipos são extensíveis (`Type` + `Length`, valores só crescem), então um GDD novo acrescenta, não quebra.
- **Perda do log de sessão numa morte do app antes do flush:** aceito (melhor esforço).
- **Revisões 5.5 e 5.6 (resultado):** `unity-specialist`: abordagem idiomática, sem API depreciada; bloqueantes B1 (`ISaveStorage` sem contrato de thread) e B2 (sem desligamento do `LogWriter`) **resolvidos** nesta revisão; notas N1 a N7 incorporadas (job reutilizável sem closure, `Span` só local, `Volatile`, checksum no worker, `SingleToInt32Bits` campo a campo e corte de UTF-8 em fronteira, "pouco lixo" em vez de "sem lixo", buffers persistentes e buffer de sessão próprio, `TryList` e retenção fora da thread principal). `technical-director`: CONCERNS; contradições 1 a 3 (`Phase` × `Headless`, hash final ausente, gatilho do `Pending`) e lacunas 4 a 7 (emenda ao ADR-0003, abandono, buffers e retenção, registro) **resolvidas** no texto. Um novo parecer do diretor sobre este texto revisado **não foi pedido**; o veredito vigente continua sendo o CONCERNS acima, tratado, e não um APPROVE.

## GDD Requirements Addressed

| GDD System | Requirement | How This ADR Addresses It |
|------------|-------------|--------------------------|
| simulacao-deterministica.md (#2) | Regra 1.2 / TR-simulacao-017: seed no log antes do tick 0; cabeçalho com hash dos dados, tag do build, ABI e ordem dos sistemas | Decisão 4: cabeçalho escrito antes do `Create`, com `MasterSeed`, `DataHash`, `BuildTag`, `Abi`, `SystemsOrder` |
| simulacao-deterministica.md (#2) | Bordas L405 e L406: logs com ABI, tag ou hash dos dados diferentes são "não comparável"; mudar a ordem dos sistemas muda o hash | Decisão 6: `LogComparer` e `SystemsOrder` no cabeçalho |
| simulacao-deterministica.md (#2) | AC I5, Regra 6 e L379: eventos drenados após cada tick sem perda; `DroppedEvents` nunca silencioso | Decisão 3 (`EventBatch`), Decisão 7 (`RecordsDropped`, `Truncated`), contador `DroppedEvents` |
| simulacao-deterministica.md (#2) | Regra 13 e L389/L390: hash final no log; abandono grava o `StateHash` marcado "abandonada"; vitória e derrota no mesmo tick | Decisão 5 (abandono pelo passo 5, `MorteSimultanea`) e Decisão 6 (rodapé) |
| fluxo-de-fase.md (#3) | Regra 9 / TR-fluxo-010: drenar, `StateHash` (indisponível em `Broken`), Concluir, Discard, commit de fim, evento ao #5 após a resposta | Decisão 5: ordem de fim e rodapé só depois da resposta do commit, com `Falhou`, `Pendente` e regravação |
| fluxo-de-fase.md (#3) | TR-fluxo-016, Regra 14, X11: seed, hash final, causa, `MorteSimultanea`, abandonada, exceção, commit falhou, ordem dos `Preparar` | Decisões 3 a 6: `HostNote`, rodapé, `PreparerOrder` |
| dados-e-balanceamento.md (#1) | Regra 3, AC-I2: cabeçalho com hash, rótulo, tag, pacote aplicado; rejeições no log | Decisão 4 (`DataLabel`, `AppliedPackHash`, `CandidatePackHash`) e `External` (rejeições) |
| horda-waves-e-inimigos.md (#7) | Contadores de diagnóstico e o evento `Rugido` para o #5 | Decisão 3: `Counters` por `ICounterSource`; os eventos entram nos lotes |
| combate-e-dano.md (#6) | Mortes e danos para as métricas de aceite | Os eventos do ADR-0005 entram sem alteração em `EventBatch`; as contas são do GDD #5 |
| save-local.md (#28) | Regra 3: o log não vai para o save; interface de eventos com sink nulo e buffer no boot; eventos do save ao #5 | Decisões 2, 3 e 8: `LogSaveEventSink`, `External(Save)`, arquivos fora do save |

## Performance Implications
- **CPU**: por tick, copiar no máximo `EventCapacity` eventos de 21 bytes para o buffer (sem alocação); o `StateHash` por checkpoint tem custo de passada pelo estado e é do ADR de orçamento de frame (padrão 0 no jogo). O FNV-1a de 64 bits por byte sobre algumas centenas de KB a 1 MiB custa da ordem de 1 a 3 ms em IL2CPP (**estimativa, não medida**) e roda no worker, nunca na thread principal.
- **Memory**: dois buffers persistentes de fase de `LOG_BUFFER_KB` (1 MiB provisório cada) e um de sessão de 64 KiB, criados no boot. **Tamanho estimado do arquivo** (calculado do layout, não medido): 1 evento = 21 bytes; um lote tem 7 bytes de cabeçalho. A horda sai agregada (1 `HordeTick` por tick no máximo), então um tick típico custa cerca de 28 a 50 bytes; 9000 ticks (5 minutos a 30 Hz) dão da ordem de 250 a 450 KB. O teto absoluto de 16 eventos por tick em 9000 ticks seria cerca de 3 MB e estouraria o buffer; nesse caso o log trunca e marca. Calibrar no spike.
- **Load Time**: alocação dos buffers uma vez no boot; `TryList` e retenção no primeiro job do pool (fora da thread principal).
- **Network**: não se aplica (offline).

## Migration Plan
Não há código de log hoje. Ordem: (1) contêiner, `LogReader`, `Dump`, `LogComparer` e as structs de registro em EditMode, com `InMemorySaveStorage` e fixtures; (2) o `PhaseLog` com buffer, rodapé, `Truncated` e `Degraded`; (3) a ordem de fim de fase ligada ao `TentativaDeFase` e ao `PhaseHost`, com `Pending` e regravação; (4) `LogHost`, `LogWriter` no `ThreadPool`, desligamento e o `LogSaveEventSink`; (5) retenção e numeração; (6) o spike no aparelho (Verification Required 1 a 9).

## Validation Criteria
- AC I5 do #2 (3 ticks, 3 lotes com `Tick` crescente, sem perda) e I6 do #3 (seed, hash final, causa, `MorteSimultanea`, abandonada e exceção chegam ao log) passam com o `PhaseLog` real; AC-I2 do #1 (cabeçalho com hash, rótulo e tag; rejeição gera entrada).
- Testes do formato: ida e volta de cada tipo de registro com valores nos extremos (incluindo `float` por bits, NaN e `-0`); tipo desconhecido é pulado; arquivo sem rodapé válido e com 1 byte alterado é "incompleto"; `Text` cortado em fronteira de caractere.
- Testes de falha: buffer cheio (`Truncated`, `RecordsDropped`, rodapé presente); `ISaveStorage` com injeção de falha em `WriteAll`, `Replace` e `FsyncDirectory` (`Degraded`, jogo segue); os dois buffers de fase ocupados (descarta e conta, sem bloquear; o de sessão segue livre); exceção dentro de `ICounterSource` (só aquela fonte `Available = 0`); desligamento com job pendente (espera curta, abandona).
- Testes do comparador: mesmos logs = `Identical`; **`Phase` contra `Headless` do mesmo build e seed = `Identical`**; um bit diferente num `HashCheckpoint` comum = `Divergence(tick)`; checkpoint só de um lado é ignorado; `Abi` vazia, `BuildTag`, `DataHash`, `AppliedPackHash`, `SystemsOrder`, `MasterSeed`, `Strict`, `TicksPerSecond` ou `FormatVersion` diferentes, `Session`, arquivo incompleto, `Truncated` ou `Degraded` = `NotComparable(motivo)`, nunca `Divergence`; hash final indisponível ou `Pendente` sem divergência = `NotComparable`; divergência achada antes vale.
- Teste da ordem de fim: com portão manual no commit, o rodapé e o evento ao #5 não saem antes de `Confirmado`; com `Falhou`, saem marcados; **no abandono, também esperam a resposta**; ao ir para segundo plano em *Concluindo*, `FlushPending` entrega `Pending` e a resposta tardia regrava o mesmo nome com o status final; em *Em andamento* não há flush.
- Zero alocação gerenciada por tick em `WriteBatch` (IL2CPP, 300 vivos, pior tick).
- **Pré-condição do aceite:** a comparação aparelho × headless só conta como instrumento de aceite depois que a Verification Required 3 fechar (fonte da tag do build e da ABI); antes disso todo par é `NotComparable`.
- No aparelho: Verification Required 1 a 9. **A story do log do #5 não fecha sem a evidência do spike nos itens 1, 2, 3 e 6.**

## Related
- Depende de ADR-0001, ADR-0002, ADR-0003, ADR-0005 e ADR-0007 (todos `Proposed`). Pede emendas ao ADR-0003 (três itens) e ao ADR-0007 (duas frases); ver Ordering Note.
- Candidatas de registro a apresentar depois de gravar: `state_ownership` do arquivo de log (dono: `PhaseLog`), interfaces `phase_log` (`IPhaseLog`) e `counter_source` (`ICounterSource`), `api_decisions` de formato e de gravação (`log_format`, `log_storage`), `forbidden_patterns` (`log_read_by_system`, `sim_references_log`, `log_throws_into_game`, `silent_log_loss`, `comparer_diverges_when_not_comparable`).
- GDDs: `design/gdd/simulacao-deterministica.md` (#2), `design/gdd/fluxo-de-fase.md` (#3), `design/gdd/dados-e-balanceamento.md` (#1), `design/gdd/horda-waves-e-inimigos.md` (#7), `design/gdd/combate-e-dano.md` (#6), `design/gdd/save-local.md` (#28), `design/gdd/systems-index.md` (#5, Not Started).
- `docs/architecture/architecture-review-2026-11-06.md` (Required ADRs, item 2); `docs/architecture/requirements-traceability.md` (TR-simulacao-017, TR-fluxo-010, TR-fluxo-016).

## GDD Sync (pendente; nenhum arquivo foi editado)
- **GDD #5 (a escrever)** nasce com este contrato e deve decidir: quais sinais de aceite o log carrega além dos aqui descritos, as contas derivadas, o relatório, o método de exportação em release, e a política de retenção, de buffer e de checkpoint definitiva (os padrões deste ADR são provisórios). Até lá, `NOT ASSESSED`.
- GDD #2 (L145, L428) e #3 (L193, L416) dizem "o #5 é dono do formato do log". Consistente: este ADR fixa o contêiner e os tipos de registro; o GDD #5 acrescenta tipos.
- GDD #7: os contadores de diagnóstico precisam de ids estáveis num enum de valores explícitos (hoje só nomes); o ADR os trata como `CounterId` a definir na 1ª story do log.
- GDD #28: o significado de `Code` dos `SaveEvent` por fonte é da 1ª story do #28 (ADR-0003 L170).

## Decisões provisórias (a reavaliar quando o GDD #5 e o jogo jogável existirem)
1. O formato binário próprio com rodapé FNV-1a de 64 bits (Decisão 3), contra texto.
2. Um arquivo por tentativa, um por execução headless e um por sessão (Decisão 3), e a sessão reescrita inteira.
3. O buffer em memória por fase, gravado só no fim (Decisão 7); a fase não retomável perde o log se o app morrer.
4. `LOG_HASH_EVERY_TICKS` = 0 no jogo e 30 no headless; `LOG_BUFFER_KB` = 1024; `LOG_SESSION_KB` = 64; `LOG_RESERVE_BYTES` = 512; `LOG_MAX_FILES` = 50; `LOG_MAX_TOTAL_KB` = 20000; `LOG_SHUTDOWN_WAIT_MS` = 200. O GDD #5 pode sobrescrever.
5. O `ThreadPool` com um job por arquivo (Decisão 7).
6. A precedência do comparador (Decisão 6), `Phase` e `Headless` comparáveis, `Counters` fora do veredito, e `MasterSeed`, `Strict`, `Truncated` e `Degraded` como motivos de "não comparável".
7. Os tipos `HostNote` e `External` genéricos até o GDD #5 e a 1ª story do #28.
8. O `FlushPending` só em *Concluindo* e a regravação do mesmo nome.
9. A camada **Core** (sem `architecture.md`).
