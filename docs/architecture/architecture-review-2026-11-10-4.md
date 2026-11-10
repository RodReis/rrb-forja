## Architecture Review Report
Date: 2026-11-10 (noite, 8ª passada)
Mode: full
Workflow: full
Engine: Unity 6.3 LTS (6000.3.27f1)
GDDs Reviewed: 6 (de 8 arquivos em design/gdd/; game-concept.md e systems-index.md não são GDDs de sistema)
ADRs Reviewed: 10

Reviewed-Content-Hash: docs/architecture/adr-0001-simulacao-deterministica-float32-tick-30hz.md 5092ee66c3c720dbe5b0bfcb594f247753262311
Reviewed-Content-Hash: docs/architecture/adr-0002-dados-e-balanceamento-snapshot-imutavel-gerado-no-build.md 7fa77e010e33680b85a9c26f911d62715fc21b8e
Reviewed-Content-Hash: docs/architecture/adr-0003-save-local-envelope-tlv-commit-atomico-gravador-unico.md 8a6f5963c397449e2e27d1c6b1b5df6a94efb9cf
Reviewed-Content-Hash: docs/architecture/adr-0004-colunas-do-simworld-combate-e-horda.md e0efedc0fffb3f64733e853268e6d56ceddce45e
Reviewed-Content-Hash: docs/architecture/adr-0005-pipeline-de-dano-e-eventos-de-combate.md 946dee1b9ed20d7cb0e24fce8ade1b6d9a916b87
Reviewed-Content-Hash: docs/architecture/adr-0006-vetor-geometria-e-consulta-espacial-deterministicos.md d6343e06a0b98b683f647d544872d742fb8f5a22
Reviewed-Content-Hash: docs/architecture/adr-0007-ponte-de-entrada-tempo-e-ciclo-de-vida-do-app.md 56e75534b22065cbbd6335b89a061864ce2dc2a4
Reviewed-Content-Hash: docs/architecture/adr-0008-log-de-eventos-e-instrumentacao-do-5.md 8b200b6ddb80d8746b9060dc78627465cb3a625f
Reviewed-Content-Hash: docs/architecture/adr-0009-render-de-multidao-e-vfx-em-mobile.md 0b0c2266cc728c66b7f206de81a1b3a78702395c
Reviewed-Content-Hash: docs/architecture/adr-0010-orcamento-de-frame-por-sistema-e-de-entrada-na-fase.md ae1a6f7ed1673b49b631097cf44b15aac5baa3ca
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

Esta é a 8ª passada, feita depois das rodadas 4, 5 e 6 de emendas (rodada 4: ADRs 0008, 0001, 0007, 0009 e 0010; rodada 5: 0003, 0005 e 0006; rodada 6: 0001, 0002 e 0007), que responderam ao relatório `architecture-review-2026-11-10-3.md` (CONCERNS). O ADR-0004, os GDDs e o `tr-registry.yaml` não mudaram, então a Fase 2 não reextraiu requisitos.

### Traceability Summary
Total requirements: 128 ativos (+1 superseded)
✅ Covered: 0 (nenhum ADR está `Accepted`)
🟡 Covered (Proposed): 97
⚠️ Partial: 27
❌ Gaps: 4

Comparação com a 7ª passada (128 / 92 / 32 / 4): cinco linhas passaram de ⚠️ para 🟡, e nenhuma piorou.
- TR-save-010 (ADR-0003 Emenda 3 item 1: `OnMarkFound`, `MarkFound`, `MarkAnswer`, tabela `MarkState`; `CommitKind.MarkConsume = 6`; a marca restaurada nasce `Answered`).
- TR-save-011 (ADR-0003 Emenda 3 itens 2 e 3: `enum FailureCause : byte` de 0 a 7, `ReadOnlyRejected = 5`, selo idempotente).
- TR-fluxo-013 (ADR-0003 Emenda 3 item 1 e ADR-0007 Decisão 6: `BeginStage` com marca `Found` falha com `MarkUnanswered`, e a ponte trata como erro de fluxo).
- TR-dados-004 (`IDataResolver` declarado no ADR-0003 e implementado por `DataResolver` em `Forja.Gameplay.Sim.Resolve` sobre a `DefIdTable` do ADR-0002).
- TR-save-018 (ADR-0002: `TryGetRevisionHistory` e a seção `RevisionHistory`; o save guarda o ID).

Por GDD (🟡 / ⚠️ / ❌): #2 15/6/1 · #3 18/3/0 · #1 15/6/1 · #28 17/1/1 · #6 12/9/1 · #7 20/2/0.

Notas atualizadas sem mudar o status: fluxo-010 (o ADR-0008 já implementa `IPhaseEndObserver`; resta só `CommitStatus` × `CommitOutcome`), simulacao-016 e fluxo-014 (o literal "nunca `Focus`" foi corrigido) e fluxo-011 (a marca fantasma do `CancelStage` foi corrigida).

Os ⚠️ que continuam, com o que falta: simulacao-008 (GDD #2 L86), simulacao-009 (`IPhaseSnapshot` sem `SpawnsDeDados` nem `CapacityMarginPct`), simulacao-013 e combate-008 (o `GolpesLimitados` lança no estrito no ADR-0005, e o GDD diz que só conta), simulacao-017 (campos de tag e ABI), simulacao-018 e dados-011 (memória X3 e snapshot sem número), simulacao-019 (analisador e CI), fluxo-002 (`MotivoFim` fora da `PhaseSheet`), fluxo-015 (`ISeedSource`), fluxo-020 (OQ-6), dados-008, dados-013, dados-018, dados-019, dados-020 e save-019 (delegados ao #29, ao #17 ou ao save), combate-001, combate-005 (`PedirRugido` fora da fila e `curaAcc`), combate-006, combate-010, combate-018 (`UltimoDanoTick`), combate-020, combate-021 e horda-022 (capacidade de `DeathsThisTick`), combate-022, horda-010.

**Limite desta passada:** as ~85 linhas 🟡 antigas foram conferidas só por palavra-chave. As seções das rodadas 4 e 6 dos ADRs 0006, 0009 e 0010 e a rodada 4 do ADR-0007 foram conferidas só por grep.

### Coverage Gaps (no ADR exists)
- ❌ TR-simulacao-020 (Alpha em ponto fixo): "ADR de simulação em ponto fixo".
- ❌ TR-dados-016 (análise estática e CI): "ADR de análise estática e CI".
- ❌ TR-save-017 (avisos do save para a UI): "ADR de avisos do save para a UI".
- ❌ TR-combate-019 (háptico): "ADR de feedback de plataforma"; a API do motor é `NOT SOURCEABLE` em `docs/engine-reference/`.

### Cross-ADR Conflicts
**Da 7ª passada:** resolvidos: conflito 3 (o `PhaseLog` implementa `IPhaseEndObserver`, ADR-0008 L112-116, e "o `PhaseHost` NÃO é fonte", L192 e L236), [9] (a residência roda em paralelo com o `BeginStage`, ADR-0009 L117 = ADR-0010 L138), [10] (`ENTRY_TAIL_MS` e a fórmula nova, ADR-0010 L139 e L148), [11] (`warmMaxMs` ≤ `PREWARM_MAX_MS`, calculado pelo host), [12] (texto velho do `DtUsedSeconds`), [13] ("mais quatro interfaces", ADR-0007 L370), o `DroppedTicks` × `DroppedTicksTotal` (ADR-0008 L115) e os antigos 3ª nº 3 (`Depends On` do ADR-0006) e nº 9 (ADR-0006 L89). Seguem: 3ª nº 7 **parcial** (o `R` já é constante do Core, mas o ADR-0005 L122 e L330 ainda dizem "o compositor confere"; pendência declarada no ADR-0001 L563) e 3ª nº 8 **aberto de propósito** (`MEM_CEILING_MB`, NOT ASSESSED, ADR-0010 L176).

**Verificado sem conflito:** os nomes cruzados batem entre dono e citador (`IsDiscarded`, `EndObserversCalled`, `PrewarmStep`/`PrewarmStepKind`, `ReleasePending()`, `ENTRY_TAIL_MS`, `PREWARM_STEP_MAX_MS`, o construtor da `BudgetLine`, `SimContext.InStep`, `FailureCause` de 0 a 7, `MarkState`, `MarkAnswer`, `MarkConsume = 6`, `MarkUnanswered`, `DefIdKind` = `DefKind`). Os asmdefs não formam ciclo: `Forja.Gameplay.Sim` → `Forja.Data` e `Forja.Save`; `Forja.Save` → `Forja.Data`; `Forja.Data` nunca → `Forja.Save`. A sequência de fim de fase (hash → observador → `Concluir` → `Discard` → commit) bate entre o ADR-0007 e o ADR-0008, com o rodapé no passo 5, depois do commit. O `CommitStatusMap` continua correto (só mapeia `CommitOutcome`; o ADR-0008 não lê `CommitKind`). O ADR-0004 não contradiz nada novo.

**Conflitos novos (nenhum 🔴):**
- 🟠 **[14] ADR-0001 × ADR-0002, `EventCapacityDataTerms`.** O 0001 (L114, L263) o define como `3 × individuais_máx + 4 + S_max + K + E_3_16`, e o 0002 (L87, L132) só como `S_max + K + E_3_16`. Um baker que siga o 0002 grava uma soma menor, e o `Create` aceita uma `EventCapacity` abaixo do limite: a reserva fica sem garantia. Origem: a mensagem enviada ao agente do ADR-0002 na rodada 6 não trazia a fórmula. Resolução: o 0002 adota a lista do 0001 (todos os termos menos `R`).
- 🟠 **[15] ADR-0002 × ADR-0007, o que o `StartupFailed` cobre.** O 0002 (L112) diz que um catálogo inválido dá `StartupFailed` e que o save nunca é lido; o 0007 (L67, L146d) diz que o `StartupFailed` é só de `MaxTicksPerFrame` e bloqueia só o `BeginStage`, não a abertura do save. Resolução: o 0007 acrescenta o motivo `CatalogInvalid` e bloqueia a abertura do #28 (cabe na mesma emenda da pendência do resolvedor).
- 🟠/⚪ **[16] ADR-0003 × ADR-0010, o `BeginStage` sem prazo na janela de entrada.** O 0010 (L37) diz que o commit do `BeginStage` "é uma linha da entrada (Decisão 6)", mas a tabela (L140-146) não tem essa linha, e o `Create` espera o `BeginStage` (L138) sem tempo esgotado (ADR-0003 L155). A promessa de caber em `ENTRY_MAX_MS` (L148) só vale se o commit terminar antes. Resolução: o 0010 acrescenta a linha do `BeginStage` (medida, sem corte) ou exclui a espera do commit da promessa.
- ⚪ **[17] ADR-0003 × ADR-0008, a causa da falha sem lugar no log.** O 0003 (L142) diz que os valores de `FailureCause` "vão ao log", e o 0008 não define onde (o `Code` da `HostNote CommitFailed`, L89, não tem semântica). Resolução: `CommitFailed.Code = (int)FailureCause`.
- ⚪ **[18] Texto velho.** O ADR-0005 (L34, L299 e L336) ainda diz que o `InStep` falta no ADR-0001, que já o tem (Emenda 22); o ADR-0003 (L188 e L462) ainda diz que a implementação do `DataResolver` é "pendência para o ADR-0002", que já a tem (L209-216).
- **Pendências conhecidas, declaradas:** o "o compositor confere" no ADR-0005; a lista de tipos de `Forja.Save` na Emenda 19 do ADR-0001 sem `IDataResolver`, `DefKind` e `DefRef` (declarada no ADR-0002 L397); a ordem do resolvedor no ADR-0007 (montado antes de o #28 abrir o save); a `HostNote` fora de fase (ADR-0007 L507); e o `NoteKind` que a nota do `MarkUnanswered` usa.

### ADR Dependency Order
Sem ciclos pelo script (ADR-0001, 0002, 0003, 0004, 0005, 0006, 0007, 0008, 0009, 0010). O ADR-0006 depende do 0001, 0002, 0004 e 0005. Todos os 10 ADRs estão `Proposed`.

### GDD Revision Flags (Architecture → Design Feedback)
- GDD #3 (`fluxo-de-fase.md`): definir o destino de uma fase já `Ended` quando o app vai para segundo plano antes do commit de fim (depende do N3 do motor, abaixo), o caminho hub e retry do `BeginStage`, e que a ponte espera o `ConsumeMark`.
- Seguem abertos: o pré-aquecimento "no `Preparar`" no GDD #7 (L182, L530, L796), o hit-stop do #6, o `CurasDescartadas` e o `curaAcc` do #6, e o fato de nenhum GDD citar `PedirRugido` nem `HordeTick`.

### Engine Compatibility Issues
Engine: Unity 6.3 LTS (6000.3.27f1). Nenhuma API depreciada em uso.

### Engine Specialist Findings (`unity-specialist`, delta das rodadas 4 a 6)
- **Da 7ª passada:** o `Warm` não preemptivo está FECHADO no contrato (ADR-0009 L144, L224-225 e L346; ADR-0010 L148 e L313); o `Destroy` adiado está FECHADO (ADR-0009 L158, L206 e L239; ADR-0007 L125 e L284; ler um campo gerenciado depois do `Destroy` é válido; a ordem `AppLifecycle(-200)`/`PhaseHost(-100)` cobre o `OnMarkFound` entre frames); a E/S sem cancelamento está **PARCIAL**: `ReleasePending()` está certo no formato (ADR-0009 L219-223 e L347; ADR-0010 L341), mas o "liberar" depende do carregador, que segue sem escolha (M4).
- **MEDIUM novos:**
  - **N1, orçamento do aquecimento (ADR-0010 L148, ADR-0009 L225).** A fórmula do `warmMaxMs` desconta só um estouro de `PREWARM_STEP_MAX_MS`. Com um passo por frame, cada passo ocupa no mínimo um intervalo de frame, e a compilação de shader e o primeiro desenho (`WarmupDraw`) caem na render thread ou no driver do GLES/Vulkan, um frame depois da medição na thread principal. Correção: descontar `PREWARM_STEP_MAX_MS` mais um intervalo de frame; medir o passo na VR7 como tempo de frame (`Stopwatch` entre frames), não como a duração da chamada C#; usar um relógio real, nunca `Time.time`.
  - **N2, `ReleasePending` (ADR-0009 L219-223 e L382).** Com AssetBundle cru, um asset isolado só pode ser liberado com `Resources.UnloadAsset`, que não serve para prefab nem GameObject; sobram `bundle.Unload(true)` ou `UnloadUnusedAssets`. Há uma corrida entre a segunda tentativa e a liberação: se a carga concluir, for liberada e a segunda tentativa reusar o handle, o asset já está destruído (o teste cobre só "2ª tentativa antes de concluir"); o retry precisa desmarcar a liberação pendente, ou recarregar se ela já ocorreu. Uma cena aditiva com `allowSceneActivation = false` trava a fila de `AsyncOperation`. Os três mecanismos são NOT SOURCEABLE (AssetBundle, cena e `UnloadAsset` não estão em `docs/engine-reference/unity/`).
  - **N3, `EndPending` com o app em segundo plano (ADR-0007 L121-141 e L271).** "Roda com o app pausado" vale para o `PauseGate`, não para o SO. No Android o `Update` não roda em segundo plano (o próprio ADR diz isso em L84). Se o `Ended` cair no último frame antes do `OnApplicationPause(true)`, o passo 4 fica para depois da volta, e a gravação da pausa é "só fora de fase"; se o processo for morto, uma fase já vencida se perde. Correção: no `OnApplicationPause(true)` com `EndPending`, executar o passo 4 de forma síncrona antes da gravação, ou aceitar e documentar a perda.
- **LOW novos:** (a) ADR-0003 L443: a regra do detach JNI deve dizer "só na thread que fez o attach, nunca na principal" (se o IL2CPP anexa threads gerenciadas sozinho: NOT SOURCEABLE); (b) ADR-0002 L112 e L209: as seções `IdTable` e `RevisionHistory` devem ser lidas com `BinaryPrimitives` (endianness explícita, sem leitura desalinhada), `Forja.Data` e `Forja.Save` têm de ser asmdefs sem engine, e não há reflexão, então não é preciso `link.xml` (o stripping do IL2CPP é NOT SOURCEABLE, como já está em L325).
- **Não verificado pelo especialista:** a seção "Engine Specialist Findings" da 7ª passada não foi relida (o status foi dado contra o texto atual dos ADRs); `ShaderVariantCollection`/`GraphicsStateCollection` para o `ShaderVariantSlice` no Vulkan (NOT SOURCEABLE); o valor de 200 ms do `PREWARM_STEP_MAX_MS`.

### Architecture Document Coverage
**NOT ASSESSED:** não existe `docs/architecture/architecture.md`. A Fase 6 não rodou.

---

### Verdict: CONCERNS

Mesmo veredito das passadas anteriores. Não há 🔴. O teto é CONCERNS porque os 10 ADRs estão `Proposed` (🟡 não é aprovação), a Fase 6 está NOT ASSESSED (impede PASS no modo `full`), e restam três conflitos 🟠 novos ([14] a [16]) e três MEDIUM de motor (N1 a N3). As rodadas 4 a 6 fecharam 5 requisitos e todos os conflitos da 7ª passada, e abriram 3 conflitos 🟠, dos quais o [14] nasceu de uma instrução minha incompleta ao agente do ADR-0002.

### Blocking Issues (must resolve before PASS)
Nenhum conflito bloqueante. Antes do aceite do ADR-0001, em ordem:
1. Alinhar os conflitos 🟠 [14] (a fórmula do `EventCapacityDataTerms` no 0002), [15] (`CatalogInvalid` no 0007) e [16] (a linha do `BeginStage` no 0010), e os ⚪ [17] e [18].
2. Tratar os MEDIUM de motor: o orçamento do aquecimento (N1), a corrida do `ReleasePending` (N2) e o `EndPending` em segundo plano (N3, com a flag para o GDD #3).
3. Decisões do usuário: M4 (Addressables, AssetBundle cru ou cena aditiva por fase) e `UltimoDanoTick`.
4. Textos do ADR-0005 ("o compositor confere", `InStep` "falta"), lista de tipos da Emenda 19 do ADR-0001, resolvedor no boot do ADR-0007 e `HostNote` fora de fase no ADR-0008.
5. `/create-architecture` (para a Fase 6 deixar de ser NOT ASSESSED) e a revisão independente dos GDDs #2 e #3, depois `/architecture-decision accept ADR-0001`.

### Required ADRs
1. Emendas aos ADRs 0002 ([14]), 0007 ([15], N3, resolvedor, `HostNote` fora de fase), 0010 ([16], N1), 0009 (N2), 0008 ([17]), 0001 (Emenda 19), 0005 ([18], "o compositor confere") e 0003 ([18], LOW do detach).
2. ADRs futuros: ponto fixo (Alpha), análise estática e CI, avisos do save para a UI, feedback de plataforma.

### Pré-gate (todos ❌)
- ❌ Raiz de testes Unity (`Assets/Tests/EditMode/` e `Assets/Tests/PlayMode/`): `/test-setup`
- ❌ `.github/workflows/tests.yml`: `/test-setup`
- ❌ `design/accessibility-requirements.md`: `/ux-design`
- ❌ `design/ux/interaction-patterns.md`: `/ux-design`

### Limites desta passada
- A rastreabilidade conferiu as linhas ⚠️ e ❌ e as notas citadas; as ~85 linhas 🟡 antigas só por palavra-chave, e as rodadas 4 e 6 dos ADRs 0006, 0009 e 0010 e a rodada 4 do ADR-0007 só por grep.
- O agente de conflitos não verificou se `individuais_máx` é termo de dados no GDD #6 (o [14] supõe que sim, como diz o ADR-0001), nem a thread da leitura do save no boot contra a regra "só thread principal" do `IDataResolver`, nem a VR2 do UBO e os itens de motor da rodada 4, nem GDDs e registries.
- O especialista não releu a seção da 7ª passada e não verificou os fatos NOT SOURCEABLE.
- As correções das rodadas 4 a 6 foram feitas por agentes e só foram verificadas por esta revisão e pelo script de dependências.
- Os arquivos `tr-registry.yaml` e `consistency-failures.md` não mudaram (sem IDs novos e sem conflito 🔴).
