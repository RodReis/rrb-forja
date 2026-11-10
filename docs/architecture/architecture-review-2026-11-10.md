## Architecture Review Report
Date: 2026-11-10
Mode: full
Workflow: full
Engine: Unity 6.3 LTS (6000.3.27f1)
GDDs Reviewed: 6 (de 8 arquivos em design/gdd/; game-concept.md e systems-index.md não são GDDs de sistema)
ADRs Reviewed: 10

Reviewed-Content-Hash: docs/architecture/adr-0001-simulacao-deterministica-float32-tick-30hz.md 251a4ed3f455af63544b9c9fe6febec4680b51d3
Reviewed-Content-Hash: docs/architecture/adr-0002-dados-e-balanceamento-snapshot-imutavel-gerado-no-build.md 0048dce6b94da35a3b8f5a212334a7dd937e6d2b
Reviewed-Content-Hash: docs/architecture/adr-0003-save-local-envelope-tlv-commit-atomico-gravador-unico.md 880c09bf1099b9e134b5396cf2283930139bc7b5
Reviewed-Content-Hash: docs/architecture/adr-0004-colunas-do-simworld-combate-e-horda.md e0efedc0fffb3f64733e853268e6d56ceddce45e
Reviewed-Content-Hash: docs/architecture/adr-0005-pipeline-de-dano-e-eventos-de-combate.md 25c3b5d7348f5006c1581e8e6184189d8bd3ad64
Reviewed-Content-Hash: docs/architecture/adr-0006-vetor-geometria-e-consulta-espacial-deterministicos.md e9bdc151c4cc6e2c0e204fd2311394eddaa06a00
Reviewed-Content-Hash: docs/architecture/adr-0007-ponte-de-entrada-tempo-e-ciclo-de-vida-do-app.md 8c9d1d4f3e7cb37c23c3116192a5afc0c6201cda
Reviewed-Content-Hash: docs/architecture/adr-0008-log-de-eventos-e-instrumentacao-do-5.md 8b3ee26d14a6e75dafb23ddff1d81ed5ad0b4cc9
Reviewed-Content-Hash: docs/architecture/adr-0009-render-de-multidao-e-vfx-em-mobile.md ac582034f2bec36f614d7586a983d84622dc4b0e
Reviewed-Content-Hash: docs/architecture/adr-0010-orcamento-de-frame-por-sistema-e-de-entrada-na-fase.md 0f21175ba438e961dd96cb20394709813ce0d2b1
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

### Traceability Summary
Total requirements: 128 ativos (+1 superseded)
✅ Covered: 0 (nenhum ADR está `Accepted`)
🟡 Covered (Proposed): 89
⚠️ Partial: 35
❌ Gaps: 4

Comparação com a 4ª passada (125 / 79 / 40 / 6): +3 IDs novos (TR-fluxo-021, TR-dados-021, TR-dados-022).
- ⚠️ → 🟡: simulacao-012, fluxo-005, fluxo-008, combate-003, horda-001, horda-015, horda-017.
- ❌ → 🟡: combate-012 e horda-013 (cobertos pelo ADR-0010).
- 🟡 → ⚠️: dados-005 (instante de 0 tick).
- Revisados (`revised: 2026-11-10`): TR-fluxo-008, TR-dados-005, TR-dados-006.

**Limite desta passada:** foram conferidas as linhas novas e as 46 ⚠️/❌ da matriz anterior. As outras 117 linhas 🟡 não foram reconferidas contra as emendas de 2026-11-10.

### Coverage Gaps (no ADR exists)
- ❌ TR-simulacao-020 (Alpha em ponto fixo): sugerido "ADR de simulação em ponto fixo".
- ❌ TR-dados-016 (análise estática e CI): sugerido "ADR de análise estática e CI".
- ❌ TR-save-017 (avisos do save para a UI): sugerido "ADR de avisos do save para a UI".
- ❌ TR-combate-019 (háptico): sugerido "ADR de feedback de plataforma". A API do motor é `NOT SOURCEABLE` em `docs/engine-reference/`.

Emenda ao ADR-0002 (não é ADR novo) fecha dados-005, dados-022 e horda-018: categoria "instante" no conversor, ordem das waves por (`inicio`, `w`), relatório de autoria com canal de avisos, e citar o #7 em GDD Requirements Addressed.

### Cross-ADR Conflicts
**Antigos:** dos 14 da 4ª passada, 12 resolvidos e 2 parciais (nº 8 e nº 13). Dos 9 da 3ª, 5 resolvidos, 2 parciais (nº 7 e nº 8) e 2 abertos (nº 3: `Depends On` do ADR-0006 sem 0002 e 0005; nº 9: texto do ADR-0006 L89, ⚪).

**Novos:**
- 🔴 **N1, ADR-0009 × ADR-0010 (carga depois do teto).** O 0009 (L113, L210) deixa a carga do pré-aquecimento continuar em segundo plano depois do teto e exige o desenho do chefe dentro do frustum. O 0010 (L138, L144, L194) proíbe os assets obrigatórios depois do 1º `Tick` e (L137) trata como melhor-esforço "desenhar o chefe fora da tela". Resolução: Emenda E ao 0009 (residência obrigatória separada do aquecimento) e corrigir o L137 do 0010.
- 🟠 N2, ADR-0007 × ADR-0008/0009: o `tick` de `OnTickDrained` não é definido. O 0009 passa `combatTick`, que congela no `CombatHold`; o 0008 exige `Tick` crescente (AC I5). Resolução: `tick = CurrentTick`; o 0009 lê o `CombatTick` do `SimWorld`.
- 🟠 N3, ADR-0007 (interno) × ADR-0008: o passo 4 sai se `Status != Running` e vem antes do passo 9, então o `Discard` do frame seguinte nunca roda no caso `Ended`; o momento do `Concluir` é ambíguo no 0008 (L106-108).
- 🟠 N4, ADR-0002 × ADR-0003/0008: o 0002 (L92) diz que o `StateHasher` é a única cópia permitida do FNV-1a; a Emenda 1.7 do 0003 e o 0008 (L82) dizem que a variante do Core não é a mesma função.
- 🟠 N5, ADR-0010 × ADR-0001/0007: `ITickProbe` e `BudgetLine` no Core sem emenda ao 0001; o `DtUsed` do `PhaseHost` para o `LoadGovernor` contraria a D1 e o 0007 L256.
- 🟠 N6, ADR-0010 × ADR-0008/0009: os contadores 1 a 14 do 0010 não têm `Source` e colidem com `View` (1 a 8). Resolução: `Source = Budget = 4`.
- 🟠 N7, ADR-0010 × ADR-0009: o corte do nível `High` "vira fade"; o 0009 (L101) não tem fade.
- 🟠 N8, ADR-0010 × ADR-0003/0007/0008/0009: domain reload "desligado hoje" (0010 L197); está ligado (`EditorSettings.asset:27-28`). O 0003 (L116, L283) também ainda o supõe desligado.
- 🟠 N9, ADR-0010 × ADR-0007: quem fixa `targetFrameRate`; o 0007 aboliu a cena de bootstrap e trata 30 fps como padrão.
- 🟠 N10, ADR-0010 × ADR-0002/0004/0005/0006: livro de memória sem os ~110 KB do 0004, a fila do 0005 e os ~4,5 KB por chamador do 0006.
- 🟠 N11, ADR-0001 × GDD #1: o 0001 (L69, L288) recusa qualquer valor abaixo de 1 tick; o GDD #1 (Regra 4) aceita instante 0. Resolução: restringir o texto a "durações".
- 🟠 N12, ADR-0007 × ADR-0009/0010: o 0007 (L145) diz que nenhum observador tem referência de volta ao `PhaseHost`, mas o 0009 lê `Alpha` dele.
- 🟠 N13, ADR-0009 L37: cita o gancho na "Decisão 6" do 0007; ele está na Decisão 8.
- ⚪ 11 itens de texto desatualizado (por exemplo 0007 L10 "ainda a gravar", 0002 L118/L328 "QueueCapacity a acrescentar", 0007 com dois itens "10.", 0009 L348 sobre `IAppLifecycleObserver`).

**Declarados e não aplicados:** `UltimoDanoTick` (ADR-0004 L310 e L316; sem ele o flash da horda fica desligado e o golden hash do #6 não muda), `PrewarmIncomplete = 8` e `LoadLevelChanged = 9` (ausentes do ADR-0008).

**Origem:** N2, N3, N4, N12 e N13 vêm das emendas de 2026-11-10 (as assinaturas dos ganchos e a prosa do `Discard` não foram checadas contra o resto do ADR-0007). N5 a N10 vêm do ADR-0010, que nunca tinha sido revisado.

**Correção aplicada durante a passada:** o script de dependências achou um ciclo ADR-0001 ↔ ADR-0002, criado pela emenda ao ADR-0001 (a linha `Depends On` citava o ADR-0002). A linha foi reescrita e o grafo ficou sem ciclos. Também foi acrescentado `QueueCapacity` ao `IPhaseSnapshot` do ADR-0001 (L246).

### ADR Dependency Order
Sem ciclos. Ordem emitida pelo script: ADR-0001, 0002, 0003, 0004, 0005, 0006, 0007, 0008, 0009, 0010. Todos os 10 ADRs estão `Proposed`, então nenhum pode ser implementado até o aceite em ordem. O ADR-0010 é Foundation mas depende de 0007 a 0009 (camada invertida). O `Depends On` do ADR-0006 não lista 0002 nem 0005 (3ª passada, nº 3).

### GDD Revision Flags (Architecture → Design Feedback)
Nenhum novo. Seguem abertas as perguntas de jogo de passadas anteriores: o pré-aquecimento "no `Preparar`" no GDD #7 (L182, L530, L796; AC-P4) contra "antes do `Create`" no ADR-0009, e o cancelar contra congelar o hit-stop no GDD #6 (L412, L440). Não verificado: grep de `SV_InstanceID`, "lote" e `baseInstance` em `design/gdd/*.md` (nenhum GDD conhecido supõe `SV_InstanceID`). Não foi proposta alteração no `systems-index.md`.

### Engine Compatibility Issues
Engine: Unity 6.3 LTS (6000.3.27f1). ADRs com `Engine Compatibility`: 10 / 10, todos com a mesma versão do `VERSION.md`. APIs do `deprecated-apis.md`: nenhuma em uso (`Resources.Load` só como proibição; o ADR-0002 L98 lê um `TextAsset` de forma síncrona, desvio declarado). Nenhum ADR afirma API nova de Unity 6 em "Post-Cutoff APIs Used".

### Engine Specialist Findings (`unity-specialist`, parcial)
- **HIGH do ADR-0009 (`SV_InstanceID`): fechado no texto (L84, L86, L28 VR1), com ressalvas.** `unity_InstanceID` inclui `unity_BaseInstanceID` quando a API tem baseInstance, e num draw de ≤ N instâncias vai de 0 a N-1, em GLES3 e em Vulkan [conhecimento do especialista; NÃO SOURCEABLE em `docs/engine-reference/`]. `RenderParams.matProps` também é `NOT SOURCEABLE` localmente (`modules/rendering.md:185` só mostra `new RenderParams(material)`). Ressalvas: (1) o N do C# tem de ser ≤ o limite real de lote da Unity no aparelho (depende do UBO e dos dados por instância), senão a Unity divide de novo e o bug volta, então falta um assert do N medido; (2) `_ForjaChunkBase` precisa ser uniforme por draw, não `UNITY_DEFINE_INSTANCED_PROP`; (3) o pré-aquecimento deve usar o mesmo alvo de render, MSAA e depth da câmera de jogo.
- Fechados: domain reload (0007, 0008, 0009), `SubsystemRegistration`, `RGBA32F` e precisão, B1 exige Vulkan, GPU Resident Drawer, `AppLifecycle` persistente, `StartupFailed`, 30 fps padrão, `DrainEvents` uma vez por tick, `Application.quitting`.
- Abertos: HIGH da Seção 7 do ADR-0003 (XMLs de backup em `Assets/Plugins/Android/res/xml/`; a Unity 6 só empacota `res` dentro de um `.androidlib` [conhecimento, NÃO SOURCEABLE]); ADR-0009 L66 asmdef único "decisão pendente"; VFX Graph exige compute e não roda em GLES 3.0 (a comparação útil do VR9 é Shuriken contra quads).
- Novos: **M1** ADR-0010 L137 "fora da tela" (= N1); **M2** plano C do `FsyncDirectory`/`Replace` com JNI e attach por chamada (ADR-0003 L153) quebra "o log só usa `System.IO`" (0008 L137, L160); **M3** ADR-0010 L129(b) "horda vira fade" (= N7); **M4** ADR-0010 L144 exige Addressables, mas `Packages/manifest.json` não tem `com.unity.addressables` e o ADR-0002 (L98, L181) proíbe Addressables para o conjunto embarcado; **L1** domain reload (= N8); **L2** `gcIncremental: 1` já está configurado (não é "decisão pendente"), e `androidUseSwappy: 0` e `enableFrameTimingStats: 0` precisam ser ligados e registrados como tarefa; **L3** ADR-0003 item 4(d) "attach em cada gravador".
- **Não verificado pelo especialista:** ADR-0010 do §8 em diante; ADR-0007 e ADR-0008 só por grep dirigido; ADRs 0001, 0002, 0004, 0005, 0006 só nos campos de Engine Compatibility; o `LoadLevel` (`Alto` contra `High`) no ADR-0009 L102 e L164. O ADR-0003 (L116, L283) ainda supõe domain reload desligado.

### Architecture Document Coverage
**NOT ASSESSED:** não existe `docs/architecture/architecture.md`. A Fase 6 não rodou.

---

### Verdict: FAIL

Motivo: 1 conflito 🔴 (N1) entre o ADR-0009 e o ADR-0010, que não podem ser implementados como estão escritos. A correção é de texto (a Emenda E ao 0009 e o L137 do 0010). Sem o N1, o veredito seria CONCERNS: os 10 ADRs estão `Proposed` (🟡 limita a CONCERNS) e a Fase 6 está NOT ASSESSED (impede PASS no modo `full`).

### Blocking Issues (must resolve before PASS)
1. **N1** (🔴): alinhar o ADR-0009 e o ADR-0010 sobre residência obrigatória (antes do 1º `Tick`) e aquecimento (melhor-esforço).
2. Aceitar os ADRs em ordem (`/architecture-decision accept ADR-0001` primeiro), depois da revisão independente dos GDDs #2 e #3.
3. Criar `docs/architecture/architecture.md` (`/create-architecture`), para a Fase 6 deixar de ser NOT ASSESSED.

Antes de aceitar o ADR-0001: N2, N3, N4, N11, a emenda ao ADR-0002 (instantes, relatório, citar o #7) e o texto "metade do XP" da Emenda 15.

### Required ADRs
1. Emenda ao ADR-0002 (instantes, ordem das waves, relatório de autoria, #7 em GDD Requirements Addressed).
2. Emenda E ao ADR-0009 e correções do ADR-0010 (N1, N5 a N10).
3. Emenda ao ADR-0003 (marca encontrada, enum de causas, `ReadOnlyRejected`, `IDataResolver`, marca fantasma do `CancelStage`, HIGH da Seção 7, domain reload, `StateHasher`).
4. ADRs futuros: ponto fixo (Alpha), análise estática e CI, avisos do save para a UI, feedback de plataforma.

### Pré-gate (todos ❌)
- ❌ Raiz de testes Unity (`Assets/Tests/EditMode/` e `Assets/Tests/PlayMode/`): `/test-setup`
- ❌ `.github/workflows/tests.yml`: `/test-setup`
- ❌ `design/accessibility-requirements.md`: `/ux-design`
- ❌ `design/ux/interaction-patterns.md`: `/ux-design`

### Limites desta passada
- A Fase 2 foi feita só sobre as mudanças dos GDDs; a base de requisitos é a do `tr-registry.yaml`.
- A rastreabilidade conferiu as linhas novas e as 46 ⚠️/❌ antigas. Não reconferiu 117 linhas 🟡, nem releu os ADRs 0005 e 0006 (não mudaram), e não leu o diff do ADR-0007 linha a linha.
- Os três agentes de revisão bateram o limite de turnos e entregaram relatórios parciais depois de um pedido de hand-back. As lacunas de cada um estão nos itens acima.
- A Regra 9 do GDD #3 não foi relida.
