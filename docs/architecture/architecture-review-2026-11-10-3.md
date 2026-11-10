## Architecture Review Report
Date: 2026-11-10 (noite, 7ª passada)
Mode: full
Workflow: full
Engine: Unity 6.3 LTS (6000.3.27f1)
GDDs Reviewed: 6 (de 8 arquivos em design/gdd/; game-concept.md e systems-index.md não são GDDs de sistema)
ADRs Reviewed: 10

Reviewed-Content-Hash: docs/architecture/adr-0001-simulacao-deterministica-float32-tick-30hz.md f5f733ab812b3734cd6f881450ba5489226f9258
Reviewed-Content-Hash: docs/architecture/adr-0002-dados-e-balanceamento-snapshot-imutavel-gerado-no-build.md e119e953e1ca263f7342d3c1cbe2bbfcce88f84b
Reviewed-Content-Hash: docs/architecture/adr-0003-save-local-envelope-tlv-commit-atomico-gravador-unico.md 523c5e36ad3082556a5b8f099142fbb4a17505af
Reviewed-Content-Hash: docs/architecture/adr-0004-colunas-do-simworld-combate-e-horda.md e0efedc0fffb3f64733e853268e6d56ceddce45e
Reviewed-Content-Hash: docs/architecture/adr-0005-pipeline-de-dano-e-eventos-de-combate.md 25c3b5d7348f5006c1581e8e6184189d8bd3ad64
Reviewed-Content-Hash: docs/architecture/adr-0006-vetor-geometria-e-consulta-espacial-deterministicos.md e9bdc151c4cc6e2c0e204fd2311394eddaa06a00
Reviewed-Content-Hash: docs/architecture/adr-0007-ponte-de-entrada-tempo-e-ciclo-de-vida-do-app.md aaa607d611c0a21cd96597315ff6d40b4576d3aa
Reviewed-Content-Hash: docs/architecture/adr-0008-log-de-eventos-e-instrumentacao-do-5.md 20c15ecdba7d492f1a5f163798601b62422ab57d
Reviewed-Content-Hash: docs/architecture/adr-0009-render-de-multidao-e-vfx-em-mobile.md f2c697b6dc7687489c1d6ffa24923c76564a6725
Reviewed-Content-Hash: docs/architecture/adr-0010-orcamento-de-frame-por-sistema-e-de-entrada-na-fase.md 0fd81b904b7fe16c098a10ac0d57d0a89e0be48d
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

Esta é a 7ª passada, feita depois da "rodada 3" de emendas (ADRs 0007, 0009 e 0010), que respondeu ao relatório `architecture-review-2026-11-10-2.md` (CONCERNS). Os outros ADRs, os GDDs e o `tr-registry.yaml` não mudaram, então a Fase 2 não reextraiu requisitos.

### Traceability Summary
Total requirements: 128 ativos (+1 superseded)
✅ Covered: 0 (nenhum ADR está `Accepted`)
🟡 Covered (Proposed): 92
⚠️ Partial: 32
❌ Gaps: 4

Nenhum status mudou em relação à 6ª passada. Das 12 linhas que citam os ADRs 0007, 0009 ou 0010 (simulacao-015, 016 e 018; fluxo-008 e 014; combate-012 e 018; horda-013, 014, 015 e 017), nenhuma piorou. Por GDD (🟡 / ⚠️ / ❌): #2 15/6/1 · #3 17/4/0 · #1 14/7/1 · #28 14/4/1 · #6 12/9/1 · #7 20/2/0.

A rodada 3 não resolve três ⚠️: simulacao-018 (o X3, memória, segue `NOT ASSESSED`, ADR-0010 L175), combate-018 (`UltimoDanoTick` não aplicado no ADR-0004; a rodada 3 só deu uma forma de medir o limite de lote) e combate-022 (nomes e tipos das vistas somente leitura).

Foram atualizadas as Notas de 8 linhas, sem mudar o status: horda-015, fluxo-010, combate-012, horda-013, simulacao-016, fluxo-014, simulacao-017 e horda-017.

**Limite desta passada:** só foram conferidas as 12 linhas que citam os ADRs emendados. As outras linhas 🟡 não foram reconferidas, e não foi verificado se a Emenda 19 está mesmo gravada no ADR-0001 nem se o ADR-0004 tem a Emenda A (`UltimoDanoTick`).

### Coverage Gaps (no ADR exists)
- ❌ TR-simulacao-020 (Alpha em ponto fixo): "ADR de simulação em ponto fixo".
- ❌ TR-dados-016 (análise estática e CI): "ADR de análise estática e CI".
- ❌ TR-save-017 (avisos do save para a UI): "ADR de avisos do save para a UI".
- ❌ TR-combate-019 (háptico): "ADR de feedback de plataforma"; a API do motor é `NOT SOURCEABLE` em `docs/engine-reference/`.

### Cross-ADR Conflicts
**Da 6ª passada:** N1 resolvido (ADR-0009 L116-117: "nunca continua depois do 1º `Tick`"). Conflito 1 (taxa de quadros) resolvido: `Sim.Host.FrameRate.Target` no ADR-0007 L74 e L242-243, e o ADR-0010 só lê o valor. Conflito 2 (nível de carga) resolvido: `ILoadLevelSource` no ADR-0009, e `LoadGovernor : ILoadLevelSource` no ADR-0010. Conflito 4 (residência × aquecimento) resolvido: ADR-0009 L113-117, ADR-0010 L139-151. Conflito 5 (linha de orçamento) resolvido: o #8 e o #16 declaram `ISimSystem.BudgetLine = 5` (ADR-0010 L84, L96 e L224, de acordo com o ADR-0001: 1, 2, 3 ou 5).
Conflito 3 (hash, contadores e rodapé no fim de fase): **PARCIAL, pendência declarada.** O lado do ADR-0007 está correto (L121-127, L158, L160). O ADR-0008 L110-111 ainda diz que o "`PhaseHost` é fonte" do `ICounterSource`, que mora em `Sim.Log`, mas o 0007 proíbe o `PhaseHost` de referenciar `Sim.Log` (L301). A ordem das duas sequências não se contradiz; o que falta é o ADR-0008 implementar `IPhaseEndObserver`, declarado em 0007 L468 e 0010 L406 e L414.
Itens de texto ⚪: o 6 (`ProbeSlots.Total` corrigido; falta o construtor da struct `BudgetLine` no ADR-0001, declarado no 0010) e o 7 (o 0007 está correto; o 0010 tem texto velho, ver nº 12) estão parciais, e o 8 está resolvido (sobra a linha histórica do ADR-0001 L520, já declarada).
**Antigos ainda abertos:** 3ª nº 3 (`Depends On` do ADR-0006), nº 7 (ADR-0005 L121, termo `R`), nº 8 (`MEM_CEILING_MB` NOT ASSESSED) e nº 9 (ADR-0006 L89). Os ADRs 0005 e 0006 não foram tocados.

**Nomes cruzados:** todos batem entre dono e citador: `FrameRate.Target`, `IPhaseEndObserver` e os 6 campos de `PhaseEndInfo` (os tipos batem com o ADR-0001: `ulong StateHash()`, `SimStatus`), `ILoadLevelSource` e `NullLoadLevelSource`, `EnsureResident(plan, ct)` e `Warm(plan, warmMaxMs, ct)`, `ENTRY_MAX_MS`, `PREWARM_MAX_MS` e `ISimSystem.BudgetLine = 5`. O `IPhaseLog.WriteNote(in HostNote)` existe no ADR-0008 (L195), então a dependência `Sim.Budget` → `Sim.Log` é permitida e não forma ciclo.

**Conflitos novos (nenhum 🔴):**
- 🟠 **[9] ADR-0009 × ADR-0010, ordem da residência.** O 0009 L117 diz que `EnsureResident` → `Warm` rodam "depois da confirmação do `BeginStage`", e o 0009 L115, L355 e L395 e o 0010 L138 e L189 dizem "em paralelo com o `BeginStage`". Em sequência, o `t_residência` da fórmula não inclui o tempo do commit e a janela passa de `ENTRY_MAX_MS`. Resolução: no 0009 L117, "em paralelo com o `BeginStage`; o `Create` espera os dois".
- ⚪/🟠 **[10] ADR-0010, a fórmula contradiz a promessa.** O L148 diz que a janela inteira nunca passa de `ENTRY_MAX_MS`, mas o teto da residência é o próprio `ENTRY_MAX_MS` (L143, L151; 0009 L113): uma residência de 5,9 s, com `Warm` = 0 e mais ~500 ms de `Create`, `Preparar` e alocação, dá ~6,4 s. Resolução: prazo da residência = `ENTRY_MAX_MS − 500`, ou dizer que o teto cobre só residência mais aquecimento.
- ⚪ **[11]** O 0009 L215 diz que o `PREWARM_MAX_MS` é "passado em `warmMaxMs`"; o 0010 L148 passa o valor efetivo (≤ `PREWARM_MAX_MS`). Resolução: o 0009 diz "`warmMaxMs` ≤ `PREWARM_MAX_MS`, calculado pelo host".
- ⚪ **[12]** Texto velho no ADR-0010: a Ordering Note B (L37) ainda dá a `FrameStats` 3 campos e "pede" o `DtUsedSeconds`; a L122 fala em "pedido B"; a L124 mantém o plano de um `IFrameClock` próprio "se o ADR-0007 não acrescentar". O 0007 L157 e L246 já têm o campo, e o próprio 0010 L405 o marca "feito".
- ⚪ **[13]** O ADR-0007 L366 diz "mais três interfaces", e agora são quatro (com o `IPhaseEndObserver`).
- ⚪ possível, não confirmado: `DroppedTicks` (id de contador, 0008 L87) × `DroppedTicksTotal` (propriedade, 0007).

### ADR Dependency Order
Sem ciclos pelo script (ADR-0001, 0002, 0003, 0004, 0005, 0006, 0007, 0008, 0009, 0010). Todos os 10 ADRs estão `Proposed`.

### GDD Revision Flags (Architecture → Design Feedback)
Nenhum novo. Segue aberta a pendência do GDD #7 (L182, L530, L796: pré-aquecimento "no `Preparar`") e a pergunta de jogo do hit-stop (#6).

### Engine Compatibility Issues
Engine: Unity 6.3 LTS (6000.3.27f1). Nenhuma API depreciada em uso.

### Engine Specialist Findings (`unity-specialist`, delta da rodada 3)
- **Fechados (da 6ª passada, nos ADRs 0007, 0009 e 0010):** aquecimento com o mesmo URP Renderer, nível de qualidade e luz com sombra (ADR-0009 L114 e VR7 L28; `GraphicsStateCollection` marcado NOT SOURCEABLE); forma de medir o limite real de lote (VR1, duas candidatas NOT SOURCEABLE); M4 com exatamente as três opções sem escolher (ADR-0010 L396-402 e ADR-0009 L119; `streamingMipmapsActive: 0` conferido em `QualitySettings.asset` L39 e L93); `Stopwatch` (ADR-0010 L108, L228 e L337); janelas do `LoadGovernor` zeradas no 1º `Tick` e `DtUsedSeconds` = 0 no `dt` descartado (ADR-0010 L216 e L228; ADR-0007 L466); linhas de residência e aquecimento separadas (ADR-0010 L141-148). O `targetFrameRate` no `BeforeSceneLoad` está certo, com `vSyncCount: 0` em `QualitySettings.asset` L32 e L86. A fórmula do `warmMaxMs` está correta, e nenhuma das três opções de carregador depende de `Resources.Load`.
- **MEDIUM novos:**
  - **O corte do `Warm` não é preemptivo (ADR-0009 L114-117, ADR-0010 L148).** `ShaderVariantCollection.WarmUp` e o primeiro desenho com compilação do driver são chamadas síncronas, e o teto só se confere entre elas; a frase "a janela nunca passa de `ENTRY_MAX_MS`" é falsa pela duração do maior passo, e um frame bloqueado por segundos no GLES arrisca ANR. Correção: aquecer em lotes, uma fatia por frame, conferindo o teto a cada fatia (`WarmUpProgressively`: NOT SOURCEABLE, não está em `docs/engine-reference/unity/`). Medir o maior passo no spike VR7.
  - **Estourar `ENTRY_MAX_MS` não cancela a E/S (ADR-0009 L117).** O `AsyncOperation` de AssetBundle e de cena não aceita cancelamento. Correção: guardar o handle e liberar o asset quando a carga terminar depois da falha, senão vaza memória e uma segunda tentativa pode achar uma carga duplicada. NOT SOURCEABLE.
  - **`Destroy` adiado (ADR-0007 L125-126).** O `PhaseHost` só morre no fim do frame, e o `LateUpdate` da apresentação, no mesmo frame, roda depois do `Discard` e lê as vistas de uma `Simulation` já descartada. Correção: um sinal de "descartado" que a apresentação confere, ou desligar a apresentação antes do `Discard`.
- **LOW novos:** (a) se o observador de `OnPhaseEnding` lançar, a Unity só registra o erro e o `EndPending` repete no frame seguinte, então o gancho roda de novo e o `Concluir` nunca chega (ADR-0007 L123): usar `try/catch` ou marcar "chamado" antes da chamada; (b) o ADR-0009 L117 contradiz L115 sobre a ordem em relação ao `BeginStage` (é o mesmo defeito do conflito [9]); (c) o ADR-0009 L28 (VR2): "UBO de 64 KB no GLES 3.0" é valor típico de aparelho, e o mínimo da especificação é 16 KB; a VR1 deve medir também como `maxcount` e `forcemaxcount` se comportam no GLES (NOT SOURCEABLE).
- **Não verificado pelo especialista:** a Decisão 4 do ADR-0007 por inteiro; se ir para segundo plano entre o `Ended` e o `Update` seguinte perde o commit de fim; se o `ProfilerRecorder` "Draw Calls Count" funciona em build Release; não abriu `breaking-changes.md` nem `deprecated-apis.md` por orçamento de chamadas.

### Architecture Document Coverage
**NOT ASSESSED:** não existe `docs/architecture/architecture.md`. A Fase 6 não rodou.

---

### Verdict: CONCERNS

Mesmo veredito da 6ª passada. Nenhum 🔴 foi encontrado. O teto é CONCERNS porque os 10 ADRs estão `Proposed` (🟡 não é aprovação), a Fase 6 está NOT ASSESSED (impede PASS no modo `full`), e restam um conflito 🟠 novo ([9]), o conflito 3 parcial (pendência declarada no ADR-0008) e três MEDIUM de motor. A rodada 3 fechou os 5 conflitos da 6ª passada e abriu 1 conflito 🟠 e 3 MEDIUM, a maioria de suposições sobre carga assíncrona que só o spike confirma.

### Blocking Issues (must resolve before PASS)
Nenhum conflito bloqueante. Antes do aceite do ADR-0001, em ordem:
1. Emendar o ADR-0008 (`IPhaseEndObserver`, `IPhaseLog.WriteNote` pelo `LoadGovernor`, L110-111) e o ADR-0001 (construtor da `BudgetLine`, linha L520).
2. Alinhar o conflito [9] e os ⚪ [10] a [13], e tratar os três MEDIUM de motor (aquecimento em fatias, E/S sem cancelamento, `Destroy` adiado).
3. Decisões do usuário: M4 (Addressables, AssetBundle cru ou cena aditiva por fase) e `UltimoDanoTick`.
4. Pendências dos ADRs 0003, 0005 e 0006.
5. `/create-architecture` (para a Fase 6 deixar de ser NOT ASSESSED) e a revisão independente dos GDDs #2 e #3, depois `/architecture-decision accept ADR-0001`.

### Required ADRs
1. Emendas aos ADRs 0008 e 0001 (item 1 acima) e aos ADRs 0007, 0009 e 0010 (itens [9] a [13] e os MEDIUM de motor).
2. Emenda ao ADR-0003 (JNI com `DetachCurrentThread` em `finally` e classe resolvida na thread principal, atributos do manifest do `.androidlib`, e `MarkAnswer`, enum de causas, `ReadOnlyRejected`, `IDataResolver`, marca fantasma do `CancelStage`) e aos ADRs 0005 e 0006.
3. ADRs futuros: ponto fixo (Alpha), análise estática e CI, avisos do save para a UI, feedback de plataforma.

### Pré-gate (todos ❌)
- ❌ Raiz de testes Unity (`Assets/Tests/EditMode/` e `Assets/Tests/PlayMode/`): `/test-setup`
- ❌ `.github/workflows/tests.yml`: `/test-setup`
- ❌ `design/accessibility-requirements.md`: `/ux-design`
- ❌ `design/ux/interaction-patterns.md`: `/ux-design`

### Limites desta passada
- A rastreabilidade conferiu só as 12 linhas que citam os ADRs 0007, 0009 e 0010.
- O agente de conflitos não leu os ADRs 0001 a 0006 fora das linhas citadas, nem o `Validation Criteria` e os `Risks` dos três ADRs emendados, e não releu o ADR-0005 L121 nem o ADR-0006 L89.
- O especialista não leu a Decisão 4 do ADR-0007 por inteiro e não abriu `breaking-changes.md` nem `deprecated-apis.md`.
- As correções da rodada 3 foram feitas por agentes e só foram verificadas por esta revisão e pelo script de dependências.
- Os arquivos `tr-registry.yaml` e `consistency-failures.md` não mudaram (sem IDs novos e sem conflito 🔴).
