## Architecture Review Report
Date: 2026-11-10 (noite, 9ª passada)
Mode: full
Workflow: full
Engine: Unity 6.3 LTS (6000.3.27f1)
GDDs Reviewed: 6 (de 8 arquivos em design/gdd/; game-concept.md e systems-index.md não são GDDs de sistema)
ADRs Reviewed: 10

Reviewed-Content-Hash: docs/architecture/adr-0001-simulacao-deterministica-float32-tick-30hz.md a7f0fb0677136f23d2b7c3c0cbf294dc4c48921f
Reviewed-Content-Hash: docs/architecture/adr-0002-dados-e-balanceamento-snapshot-imutavel-gerado-no-build.md 28e211724824a2b809b17497bd01b5410a8f1bdc
Reviewed-Content-Hash: docs/architecture/adr-0003-save-local-envelope-tlv-commit-atomico-gravador-unico.md 471bb9d86012e5d76611440ce10ea645fbabe027
Reviewed-Content-Hash: docs/architecture/adr-0004-colunas-do-simworld-combate-e-horda.md e0efedc0fffb3f64733e853268e6d56ceddce45e
Reviewed-Content-Hash: docs/architecture/adr-0005-pipeline-de-dano-e-eventos-de-combate.md 1ecdb207c0ae6aa29efdefefdd2a1d23a7d795ef
Reviewed-Content-Hash: docs/architecture/adr-0006-vetor-geometria-e-consulta-espacial-deterministicos.md d6343e06a0b98b683f647d544872d742fb8f5a22
Reviewed-Content-Hash: docs/architecture/adr-0007-ponte-de-entrada-tempo-e-ciclo-de-vida-do-app.md 329d092bf989d02047770964ba5dacba880c4c9a
Reviewed-Content-Hash: docs/architecture/adr-0008-log-de-eventos-e-instrumentacao-do-5.md ec394559d37e132813bb4aca33aa37181d88705d
Reviewed-Content-Hash: docs/architecture/adr-0009-render-de-multidao-e-vfx-em-mobile.md 135601fec5e5755b428fac2118dc13f639055fbd
Reviewed-Content-Hash: docs/architecture/adr-0010-orcamento-de-frame-por-sistema-e-de-entrada-na-fase.md 3ae594d0e4757e5fe59672e6e57b1f13278568c6
Reviewed-Content-Hash: design/gdd/combate-e-dano.md 2751177b88876d0831e4faa7eed4d91543e52f61
Reviewed-Content-Hash: design/gdd/dados-e-balanceamento.md 58edadb5e87f2ed4939cc7fbc8c7698fd5f07bb2
Reviewed-Content-Hash: design/gdd/fluxo-de-fase.md 30c6d1297741842bbac51b42b9ad14a1deb746cc
Reviewed-Content-Hash: design/gdd/game-concept.md 3a61558d87c0374c253396d6a268ac932ac062f3
Reviewed-Content-Hash: design/gdd/horda-waves-e-inimigos.md c4b40ed39de60bc67735ce70b72e1f9b5e50589e
Reviewed-Content-Hash: design/gdd/save-local.md 05117224694ea7bdbe211af4a2400b9225010b53
Reviewed-Content-Hash: design/gdd/simulacao-deterministica.md 7baf9d4fc684ff6d36c3c8464cfbfb0db1a2f782
Reviewed-Content-Hash: design/gdd/systems-index.md a592f42638761936179ee0842d8e4c46b612093b
Reviewed-Content-Hash: docs/architecture/tr-registry.yaml 1a4757db267c6d6320dac422c79d8bdc85984d95
Reviewed-Content-Hash: docs/engine-reference/unity/breaking-changes.md fb4b916b76b87bf474a4152ce8c64f7c02e7b747
Reviewed-Content-Hash: docs/engine-reference/unity/current-best-practices.md 764d12ee314452d4d814380074ea157d0984ec37
Reviewed-Content-Hash: docs/engine-reference/unity/deprecated-apis.md a8216efd06ba1b7f2ae3bb16ec8b6d3afe902eb8
Reviewed-Content-Hash: docs/engine-reference/unity/PLUGINS.md 8d99063a63269d629be11e9e00e9f460188b689a
Reviewed-Content-Hash: docs/engine-reference/unity/VERSION.md f1dce5ea4147e039928bdbd2be6df2e9a0336a43
Reviewed-Content-Hash: docs/engine-reference/unity/modules/animation.md e0601eeba72565d71e1dd2a8bb267eb966d10a5f
Reviewed-Content-Hash: docs/engine-reference/unity/modules/audio.md 56c04c15cb9a356b87a27df5d0fcf67f18db9302
Reviewed-Content-Hash: docs/engine-reference/unity/modules/input.md 1b64a2381167d17c1b796d4d5f93a7e1fcc651e6
Reviewed-Content-Hash: docs/engine-reference/unity/modules/navigation.md 484a867a2fe1acf86b2071f7950b10afaab8ffab
Reviewed-Content-Hash: docs/engine-reference/unity/modules/networking.md ab0ada43362406731784044326eed68fd25aa3b1
Reviewed-Content-Hash: docs/engine-reference/unity/modules/physics.md 191e8d8d502363a99e80670942d251ef819a3976
Reviewed-Content-Hash: docs/engine-reference/unity/modules/rendering.md 292081320361b18c12715f7ed11dae2a38ba5f2d
Reviewed-Content-Hash: docs/engine-reference/unity/modules/ui.md 87de2ff30ce1c8d9499b6bcf084947201852e6ab
Reviewed-Content-Hash: project.yaml f2cb79bb9dc42984c9d25ae1fc1c4b3d93c89c7c
Reviewed-Content-Hash: .claude/docs/technical-preferences.md 8e13739d97e37ff3c1ad91e6a1be132864ae6138
Reviewed-Content-Hash: docs/consistency-failures.md 29625fb5256996e5d1bec3fd6d93d2f0053dba0e
Reviewed-Content-Hash: .claude/skills/architecture-review/SKILL.md 1a9d28aadbcbd26b5fc6b8ed1c64d73ae82b7b73
Reviewed-Content-Hash: .claude/skills/architecture-review/references/1-load.md 9a65759ebdbb2cb1f9744775bfed18cb25e76347
Reviewed-Content-Hash: .claude/skills/architecture-review/references/2-extract-requirements.md d08ea0b0e9ab9760b0d8bfe0cd9115f0bc40f8e2
Reviewed-Content-Hash: .claude/skills/architecture-review/references/3-traceability.md bb7b6b65c5e5e5b8869fa692413aa831615dede7
Reviewed-Content-Hash: .claude/skills/architecture-review/references/4-conflicts.md 0d30f8173b23248a32523a365b606dd1ce9642ab
Reviewed-Content-Hash: .claude/skills/architecture-review/references/5-engine.md 318ecbc1361d430badaf5dd8ce4cfc6ab0dff0ca
Reviewed-Content-Hash: .claude/skills/architecture-review/references/6-document-coverage.md dcce78482ec2ce60048989b6f9d1f797dd0a9a0e
Reviewed-Content-Hash: .claude/skills/architecture-review/references/7-report.md a007fd66bdac87812dc272e4b14cd231174e979d
Reviewed-Content-Hash: .claude/skills/architecture-review/references/8-write.md bf6d8946fc7b9e19eda7f65503a5c8f593a0d2b1
Reviewed-Content-Hash: .claude/skills/architecture-review/references/9-handoff.md fd5f681f4c3517c6a2e388c6d78075d82dded22e

---

Esta é a 9ª passada, feita depois da rodada 7 de emendas (ADRs 0001 Emenda 23, 0002, 0003 Emenda 4, 0005, 0007, 0008, 0009 e 0010), que respondeu ao relatório `architecture-review-2026-11-10-4.md` (CONCERNS). Os ADRs 0004 e 0006, os GDDs e o `tr-registry.yaml` não mudaram, então a Fase 2 não reextraiu requisitos.

### Traceability Summary
Total requirements: 128 ativos (+1 superseded)
✅ Covered: 0 (nenhum ADR está `Accepted`)
🟡 Covered (Proposed): 98
⚠️ Partial: 26
❌ Gaps: 4

Comparação com a 8ª passada (128 / 97 / 27 / 4): uma linha passou de ⚠️ para 🟡, e nenhuma piorou. TR-horda-022: a capacidade de eventos no tick do rugido está declarada do mesmo jeito nos três ADRs (o termo 4 inclui o `Rugido`, as mortes da horda saem agregadas em `HordeTick`, e o `Simulation.Create` confere `EventCapacity ≥ R + EventCapacityDataTerms`; ADR-0001 Emendas 22b e 23, ADR-0005 Decisão 7, ADR-0002 §4). `K` e `E_3_16` seguem NOT ASSESSED, e a VR5 só fecha depois deles.

Por GDD (🟡 / ⚠️ / ❌): #2 15/6/1 · #3 18/3/0 · #1 15/6/1 · #28 17/1/1 · #6 12/9/1 · #7 21/1/0.

Notas atualizadas sem mudar o status:
- **combate-021:** a parte de eventos fechou; continua aberta a capacidade de `DeathsThisTick` (GDD #6 L435; o ADR-0001 não a fixa).
- **simulacao-013 e combate-008:** a nota estava velha, porque `SimContext.Strict` (Emenda 18d) e `CombatCounters` (ADR-0005 Decisão 5) já existem. A falha que sobra é o `GolpesLimitados` lançar no modo estrito (ADR-0005 L96), enquanto o GDD #2 L110 diz que só conta nos dois modos, e o ADR-0001 item 9 não lista os quatro contadores do #6.
- **fluxo-010, save-011, fluxo-011, fluxo-016 e horda-015:** acrescentados os nomes da rodada 7 (`CommitFailed.Code`, `NoteKind.BeginStageFailed`, `ISessionNoteSink`, `EntryBeginStageMs`, `FRAME_INTERVAL_MS` e `ReleaseRequested`).

Os ⚠️ que continuam, sem mudança: simulacao-008, 009 (conflito do snapshot concreto, ADR-0001 L99), 017, 018 e 019; fluxo-002, 015 e 020; dados-008, 011, 013, 018, 019 e 020; save-019; combate-001, 005, 006, 010, 018, 020, 021 e 022; horda-010. Gaps sem ADR: os mesmos 4 (ponto fixo, análise estática e CI, avisos do save para a UI, háptico).

**Limite desta passada:** o corpo inteiro das emendas da rodada 7 nos ADRs 0003, 0007 e 0008 foi conferido por palavra-chave e pelas linhas citadas, e as ~90 linhas 🟡 restantes só pelas palavras-chave da rodada 7.

### Coverage Gaps (no ADR exists)
- ❌ TR-simulacao-020 (Alpha em ponto fixo): "ADR de simulação em ponto fixo".
- ❌ TR-dados-016 (análise estática e CI): "ADR de análise estática e CI".
- ❌ TR-save-017 (avisos do save para a UI): "ADR de avisos do save para a UI".
- ❌ TR-combate-019 (háptico): "ADR de feedback de plataforma"; a API do motor é `NOT SOURCEABLE` em `docs/engine-reference/`.

### Cross-ADR Conflicts
**Herdados da 8ª passada, todos resolvidos:** [14] `EventCapacityDataTerms` (lista idêntica em ADR-0001 L114-115, ADR-0002 L87, L132 e L381, ADR-0005 L122); [15] `CatalogInvalid` (ADR-0007 L68, L250 e L281, ADR-0002 L112); [16] `BeginStage` na entrada (ADR-0010 L111, L147 e L149; o ADR-0008 ficou com texto velho, ver [21]); [17] causa da falha no log (ADR-0008 L90, L123 e L188, ADR-0003 L142 e L471); [18] textos velhos dos ADRs 0005 e 0003; "o compositor confere" o `R` (ADR-0005 L122: "e não o baker nem o compositor"); o resolvedor montado antes de o #28 abrir o save (ADR-0007 L68 e L324, ADR-0002 L112 e L398); a `HostNote` fora de fase (ADR-0007 L150, ADR-0008 L74, L149 e L218); e a 3ª nº 7 (o termo `R` é constante do Core, conferida no `Create`, ADR-0001 L333 e ADR-0002 L87). A lista de tipos da Emenda 19 está **parcial** (ver [22]). A 3ª nº 8 (`MEM_CEILING_MB`) segue **aberta de propósito**, NOT ASSESSED (ADR-0010 L179).

**Verificado sem conflito:** a fórmula do `warmMaxMs` e o `FRAME_INTERVAL_MS` são idênticas no ADR-0010 L151 e no ADR-0009 L114 e L227; `NoteKind.BeginStageFailed = 10` e `CommitFailed.Code` estão alinhados entre o 0008, o 0003 e o 0007; `StartupFailReason` e `ReportStartupFailure` só existem no 0007, e o 0002 cita só `CatalogInvalid`, o que basta; os ADRs 0004 e 0006 não contradizem nada. Os padrões velhos buscados (`WriteSessionNote(in HostNote)`, "HostNote tipo 4", "pendência para o ADR-0002") só aparecem em linhas de histórico de emenda.

**Conflitos novos (nenhum 🔴):**
- 🟠 **[19] ADR-0007 × ADR-0003, passo 4 síncrono no `OnApplicationPause(true)`.** O 0007 (L115 e L541) roda o passo 4 e o pedido do commit de fim antes do fluxo de pausa, e diz que esse fluxo "não pede um segundo commit" e que o `FlushPending` "cobre o fim". O 0003 (L117 e L227) define "durante a fase" como "do pedido de `BeginStage` até o commit de fim"; fora de fase, a pausa pede um commit e espera de forma síncrona, com teto, e espera **dois** commits se houver um em andamento. Nas duas leituras o texto quebra: se a fase acaba no pedido do commit, o 0003 cria um commit substituto, contra o 0007; se acaba na conclusão, ninguém espera o commit de fim com teto. O `FlushPending` do 0008 (L41 e L125) grava só o log, não o save. O teto de 150 a 250 ms do 0003 (L28) também não conta o hash nem o `Discard`, que agora rodam no mesmo callback. O próprio 0007 (L547) deixou isso pendente para o 0003, e a Emenda 4 do 0003 não trata. Resolução: o 0003 decide o que conta como "fim da fase" para a pausa (pedido ou conclusão), se a pausa espera o commit de fim já na fila sem criar substituto, e se o teto inclui o passo 4. Origem: a decisão N3 que tomei na spec da rodada 7.
- 🟠 **[20] GDD #6 × ADR-0005 e ADR-0001, o "+5".** O GDD (`combate-e-dano.md` L420 e L526) diz `EventosReservados + 5 + 3 × individuais_máx + 4`. O 0005 (L122) admite que o GDD dá a fórmula "sem decompor" e troca o 5 por `S_max + K + E_3_16`, mas não afirma que essa soma vale 5. O 0001 (L115) cita o "+5" do GDD e define a soma sem ele. Com `K` = `E_3_16` = 0 enquanto pendentes, o limite dos ADRs fica abaixo do limite do GDD sempre que `S_max` < 5. Resolução: o 0005 declara que `S_max + K + E_3_16` substitui o 5, ou exige que seja ≥ 5, e o GDD #6 é sincronizado.
- ⚪ **[21]** O ADR-0008 (L89 e L380) ainda diz "ids 1 a 14 com `Source = Budget`", e o 0010 (L111 e L448) vai até 15 (`EntryBeginStageMs`; pendência registrada no 0010 L451).
- ⚪ **[22]** As listas de tipos de `Forja.Save` divergem: o ADR-0001 (L77) tem 8 tipos, com `IDataResolver`, `DefKind` e `DefRef`, mas não `CommitOutcome`; o 0008 (L38 e L177) tem `CommitOutcome` e não os três novos; o 0007 (L24) tem só os 5 originais; e nenhuma cita `FailureCause`, que o `PhaseLog` lê para gravar `CommitFailed.Code` (ADR-0003 L155). Resolução: o 0001 publica a lista única e os outros a citam.
- ⚪ **[23]** O ADR-0008 (L41 e L90) atribui o `ISessionNoteSink` à "Decisão 2" do 0007, e ele está na Decisão 6 (0007 L10 e L150).
- ⚪ **[24]** O ADR-0009 (L71 e L434) e o 0008 (L356 e L378) descrevem `Concluir` → `Discard` → commit só "no `Update` do frame seguinte", e ignoram o caminho síncrono da pausa; o ADR-0010 (L155, L315 e L344) diz que o retry "reusa o handle" sem o caso "já liberada, recarrega" (`ReleaseRequested`, dono ADR-0009 L120).
- ⚪ **[25]** O ADR-0003 não registra a pré-condição "com `CatalogInvalid` o #28 não abre o save"; hoje ela só está implícita nas flags do `IDataResolver` (0003 L163).

### ADR Dependency Order
Sem ciclos pelo script (ADR-0001, 0002, 0003, 0004, 0005, 0007, 0006, 0008, 0009, 0010). O ADR-0007 passou a vir antes do 0006 porque a frase "nenhuma dependência" saiu da linha `Depends On` do 0007, que o script lia como aresta. Todos os 10 ADRs estão `Proposed`.

### GDD Revision Flags (Architecture → Design Feedback)
- GDD #6: sincronizar o "+5" da fórmula de `EventCapacity` com a decomposição dos ADRs ([20]) e fixar a capacidade de `DeathsThisTick`; o `CurasDescartadas` e o `curaAcc` seguem abertos.
- GDD #3: definir o destino de uma fase já `Ended` cujo commit de fim não concluiu (`RunEndPending`), o caminho hub e retry do `BeginStage` e que a ponte espera o `ConsumeMark`.
- Seguem abertos: o pré-aquecimento "no `Preparar`" no GDD #7 (L182, L530, L796) e o hit-stop do #6.

### Engine Compatibility Issues
Engine: Unity 6.3 LTS (6000.3.27f1). Nenhuma API depreciada em uso.

### Engine Specialist Findings (`unity-specialist`, delta da rodada 7)
A busca em `docs/engine-reference/unity/` estourou o tempo, e o próprio ADR-0010 (L25) diz que ali não há nada sobre tempo de frame; por isso todo fato de motor abaixo está marcado **NOT SOURCEABLE**.
- **Fechados (da 8ª passada):** N1, orçamento do aquecimento (a fórmula do ADR-0010 L151 está correta e é conservadora); N2, `ReleasePending` (ADR-0009 L221-225, L350 e L467-469: `ReleaseRequested`, retry que desmarca ou recarrega, liberar só ao concluir, `allowSceneActivation = false` proibido); N3, `EndPending` em segundo plano (ADR-0007 L115, L287, L295, L323 e L404; não há reentrância, porque o `OnApplicationPause` não é chamado de dentro de um `Update`); LOW do detach JNI (ADR-0003 L183, L253 e L469); LOW do `BinaryPrimitives` (ADR-0002 L87, L93, L381 e L399).
- **MEDIUM novo, A3 (ADR-0007 L68 e L280).** O `BeforeSceneLoad` não consegue ler o snapshot de forma síncrona se ele estiver em StreamingAssets no Android, que fica dentro do APK e exige `UnityWebRequest`; o mesmo vale para Addressables, cuja inicialização é assíncrona, e para um campo serializado de cena, que ainda não existe nesse momento. Com validação assíncrona, `StartupReason == None` durante a carga parece sucesso, e o `BeginStage` ou o #28 poderiam passar antes de a validação terminar. Correção: um estado de boot `Pending/Ready` (ou `BootComplete`) que bloqueie o `BeginStage` e a abertura do save até a validação terminar, e fixar o carregador do `.bytes` como `TextAsset` num ScriptableObject de bootstrap carregado no `Start`, ou documentar a espera. Origem: a decisão Q2 da rodada 7, de montar o resolvedor no bootstrap.
- **LOW novos:** A1 (ADR-0010 L151): o `FRAME_INTERVAL_MS` usa o valor nominal 1000/60, mas no Android o `vSyncCount` é ignorado e o Optimized Frame Pacing pode enfileirar 2 ou mais frames; um `glLinkProgram` ou a criação de um PSO no Vulkan pode custar mais que 16,7 ms na render thread e cair no frame seguinte; correção: definir na VR11 que o `PREWARM_STEP_MAX_MS` é o maior valor de `dt(N) + dt(N+1)`, conferido pelo relógio real. A2 (ADR-0007 L65 e L115): um `Destroy` pedido dentro do `OnApplicationPause(true)` pode só executar depois da volta do app; correção: o `Discard` faz `enabled = false` de forma síncrona, e a primeira linha do `PhaseHost.Update` sai se `IsDiscarded`; medir a duração do passo 4 síncrono (hash do mundo mais flush do log), pelo risco de ANR.
- **Não verificado pelo especialista:** se o ADR-0009 trata a cena aditiva por `UnloadSceneAsync` e o `AssetBundleCreateRequest` como handle; o texto da regra de `IsDiscarded` na Decisão 6 do ADR-0007; qual carregador o ADR-0002 usa para o snapshot; e os arquivos de `docs/engine-reference/unity/`, que não puderam ser listados.

### Architecture Document Coverage
**NOT ASSESSED:** não existe `docs/architecture/architecture.md`. A Fase 6 não rodou.

---

### Verdict: CONCERNS

Mesmo veredito das passadas anteriores. Não há 🔴. O teto é CONCERNS porque os 10 ADRs estão `Proposed` (🟡 não é aprovação), a Fase 6 está NOT ASSESSED (impede PASS no modo `full`), e restam dois conflitos 🟠 ([19] e [20]) e um MEDIUM de motor (A3). A rodada 7 fechou todos os itens herdados e abriu bem menos que as anteriores: duas pontas soltas de contrato e uma de motor. As maiores nasceram de decisões minhas na própria rodada (o passo 4 síncrono, [19], e o resolvedor no bootstrap, A3), e o [20] é uma divergência antiga entre o GDD #6 e os ADRs, que a unificação do `EventCapacityDataTerms` tornou visível.

### Blocking Issues (must resolve before PASS)
Nenhum conflito bloqueante. Antes do aceite do ADR-0001, em ordem:
1. Alinhar os conflitos 🟠 [19] (o ADR-0003 decide o fim da fase na pausa) e [20] (o "+5" entre o GDD #6 e o ADR-0005), e os ⚪ [21] a [25].
2. Tratar o MEDIUM A3 (estado de boot `Pending/Ready` no ADR-0007) e os LOW A1 e A2.
3. Decisões do usuário: M4 (Addressables, AssetBundle cru ou cena aditiva por fase) e `UltimoDanoTick`.
4. Sincronizar os GDDs #3 e #6 com as flags acima.
5. `/create-architecture` (para a Fase 6 deixar de ser NOT ASSESSED) e a revisão independente dos GDDs #2 e #3, depois `/architecture-decision accept ADR-0001`.

### Required ADRs
1. Emendas aos ADRs 0003 ([19], [25]), 0005 ([20]), 0007 (A3, A2, [23]), 0010 (A1, [24]), 0008 ([21], [22], [24]), 0001 ([22]) e 0009 ([24]).
2. ADRs futuros: ponto fixo (Alpha), análise estática e CI, avisos do save para a UI, feedback de plataforma.

### Pré-gate (todos ❌)
- ❌ Raiz de testes Unity (`Assets/Tests/EditMode/` e `Assets/Tests/PlayMode/`): `/test-setup`
- ❌ `.github/workflows/tests.yml`: `/test-setup`
- ❌ `design/accessibility-requirements.md`: `/ux-design`
- ❌ `design/ux/interaction-patterns.md`: `/ux-design`

### Limites desta passada
- Os ADRs foram lidos por grep dirigido e trechos; as ~90 linhas 🟡 restantes só por palavra-chave.
- O agente de conflitos não verificou os detalhes de motor da Q7 no ADR-0009, em que ponto do frame a Unity chama o `OnApplicationPause` (sem fonte em `docs/engine-reference/`), se o `PhaseLog` já está aberto quando o `EntryBeginStageMs` é medido, nem os registries e o `tr-registry`.
- Todo fato de motor é `NOT SOURCEABLE` porque a busca na referência estourou o tempo.
- As correções da rodada 7 foram feitas por agentes e só foram verificadas por esta revisão e pelo script de dependências.
- Os arquivos `tr-registry.yaml` e `consistency-failures.md` não mudaram (sem IDs novos e sem conflito 🔴).
