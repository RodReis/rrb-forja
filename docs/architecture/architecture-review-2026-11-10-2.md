## Architecture Review Report
Date: 2026-11-10 (tarde, 6ª passada)
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
Reviewed-Content-Hash: docs/architecture/adr-0007-ponte-de-entrada-tempo-e-ciclo-de-vida-do-app.md 7c996e4158e89773213ec80b81908f381b6b2819
Reviewed-Content-Hash: docs/architecture/adr-0008-log-de-eventos-e-instrumentacao-do-5.md 20c15ecdba7d492f1a5f163798601b62422ab57d
Reviewed-Content-Hash: docs/architecture/adr-0009-render-de-multidao-e-vfx-em-mobile.md 980a011e13d811b9eadbf276e04f3fd761ddde22
Reviewed-Content-Hash: docs/architecture/adr-0010-orcamento-de-frame-por-sistema-e-de-entrada-na-fase.md 79a515f3bf46444667dcc546f4fa60c2af5c09d0
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

Esta é a 6ª passada, feita depois da "rodada 2" de emendas (ADRs 0001, 0002, 0003, 0007, 0008, 0009 e 0010) que respondeu ao relatório `architecture-review-2026-11-10.md` (FAIL). Os GDDs e o `tr-registry.yaml` não mudaram, então a Fase 2 não reextraiu requisitos.

### Traceability Summary
Total requirements: 128 ativos (+1 superseded)
✅ Covered: 0 (nenhum ADR está `Accepted`)
🟡 Covered (Proposed): 92
⚠️ Partial: 32
❌ Gaps: 4

Comparação com a 5ª passada (128 / 89 / 35 / 4): três linhas passaram de ⚠️ para 🟡 e nenhuma piorou.
- TR-dados-005 (categoria "instante": ADR-0002 §3 e ADR-0001 Emenda 20(g)).
- TR-dados-022 (`ValidationResult.Warnings` e `AuthoringReport`: ADR-0002 §2 e Key Interfaces).
- TR-horda-018 (waves por (`inicio`, `w`): ADR-0002 §4 e §3).

Por GDD (🟡 / ⚠️ / ❌): #2 15/6/1 · #3 17/4/0 · #1 14/7/1 · #28 14/4/1 · #6 12/9/1 · #7 20/2/0.

**Limite desta passada:** foram conferidas as 35 ⚠️ e as 4 ❌ da passada anterior e as 10 linhas que mudaram na 5ª. As outras 117 linhas 🟡 não foram reconferidas contra a rodada 2 (só se procurou por pontos que as afetassem).

### Coverage Gaps (no ADR exists)
- ❌ TR-simulacao-020 (Alpha em ponto fixo): "ADR de simulação em ponto fixo".
- ❌ TR-dados-016 (análise estática e CI): "ADR de análise estática e CI".
- ❌ TR-save-017 (avisos do save para a UI): "ADR de avisos do save para a UI".
- ❌ TR-combate-019 (háptico): "ADR de feedback de plataforma"; a API do motor é `NOT SOURCEABLE` em `docs/engine-reference/`.

### Cross-ADR Conflicts
**Antigos.** N1 a N13 da 5ª passada: 12 resolvidos e 1 parcial (N1). Das passadas 3 e 4, ficam: 3ª nº 7 (parcial: ADR-0005 L121 ainda diz que o termo `R` é "validado pelo #1"), 3ª nº 8 (parcial: as linhas do livro de memória estão no ADR-0010, mas `MEM_CEILING_MB` segue NOT ASSESSED), 3ª nº 3 (aberto: o `Depends On` do ADR-0006 não lista 0002 nem 0005) e 3ª nº 9 (aberto: o ADR-0006 não foi editado e a L89 não foi relida).

**N1 (parcial).** A residência obrigatória está resolvida (ADR-0009 L112-113, ADR-0010 L138-140). Sobra o ADR-0009 L116 ("o aquecimento pode continuar em segundo plano", "o rugido pode pagar parte da carga"), que contradiz o ADR-0010 L139 e L142.

**Novos, todos 🟠 ou ⚪:**
1. **ADR-0007 × ADR-0010, taxa de quadros.** O 0007 (L74, L245) diz que o `AppLifecycle` aplica a constante do 0010 e que o 0007 "não referencia tipos do 0010" (L281). No 0010 a constante é `FrameLedger.TargetFrameRate`, em `Sim.Budget` (L70, L194). O `AppLifecycle` mora em `Forja.Gameplay`, que referencia os dois, então a implementação não trava, mas o texto cria um ciclo lógico entre ADRs que o script de dependências não vê. O agente de revisão o classificou como 🔴; foi reclassificado como 🟠 depois de conferir as linhas. Resolução: nome e posição da constante em `Sim.Host` (o 0007 é dono do nome e o 0010 do valor), ou um campo serializado conferido por teste contra o `FrameLedger`.
2. **ADR-0009 × ADR-0010, nível de carga.** O 0010 (L131, L176) diz que a `PresentationDriver` lê `LoadGovernor.Level`, mas o 0009 não tem essa entrada nas Key Interfaces (L146-205) e não lista o 0010 em `Depends On` (L34): dependência oculta no sentido contrário. Resolução: interface neutra em `Sim.View` que o `LoadGovernor` implemente, ou injeção pelo compositor.
3. **ADR-0007 × ADR-0008, fim de fase.** O 0008 (L108-110) exige `StateHash` e `WriteCounters` no `Update` do `EndPending`, antes do `Concluir`. O passo 4 do 0007 (L121-125) lista só Concluir → Discard → commit, o `PhaseHost` não pode referenciar `Sim.Log` (0007 L281) e nenhum gancho cobre "fase terminando". Além disso, o 0007 L157 diz que o log lê `DroppedTicksTotal` "ao fechar o rodapé", que é o passo 5, quando o `PhaseHost` já foi destruído. Resolução: o 0007 nomeia quem chama o hash e os contadores no passo 4.
4. **ADR-0009 × ADR-0010, residência.** O 0009 L116 aguarda a residência "sem teto de tempo"; o 0010 L140 faz a entrada falhar em `ENTRY_MAX_MS` = 6000. `PrewarmRunner.RunAsync(plan, maxWaitMs, ct)` (0009 L203) tem um teto só, sem separar residência de aquecimento.
5. **ADR-0001/ADR-0010 × sistemas #8 e #16.** `Simulation.Create` lança se um sistema declarar linha inválida (0001 L113). A tabela do 0010 (L80-84) só dá linha ao #6, #7 e #3, e o #8 e a oferta do #16 também são `ISimSystem`. Resolução: atribuir L5. Os ADRs 0004, 0005 e 0006 não contradizem isso (não declaram implementações de `ISimSystem` nas Key Interfaces).
6. ⚪ A struct `BudgetLine` tem campos `readonly` e nenhum construtor (0001 L254), mas o `FrameLedger.Line(i)` do 0010 precisa construí-la; o nome repete o da propriedade `int ISimSystem.BudgetLine`; e "TotalSlot" aparece onde o nome é `ProbeSlots.Total`.
7. ⚪ `FramePlan` não tem o campo `DtUsedSeconds` (0007 L227), mas 0007 L137 usa `plan.DtUsedSeconds`; 0007 L417 lista só 3 campos de `FrameStats`; o ADR-0010 ainda trata o campo como pendência, com plano B (L37, L123, L366).
8. ⚪ Textos velhos: 0007 L28 ("ponto ainda aberto no ADR-0003"), 0007 L396 (diz que o 0009 implementa `IAppLifecycleObserver`), 0009 L35 (o ADR de orçamento "recebe" o `LoadLevel`, quando o produz), 0010 L156 ("tamanho a fixar no 0005", mas o `HitRequest` tem 28 B), 0001 L520 (linha histórica do `Create` com 5 parâmetros), e ninguém foi designado para gravar a `HostNote LoadLevelChanged` (0010 L131-132).

**Sem conflito:** os nomes cruzados (`FrameStats`, `EndPending`, `CounterSource.Budget = 4`, `NoteKind` 8 e 9, `LoadLevel`, `ValidationResult`, `AuthoringReport`) batem entre dono e citador, e a sequência de fim de fase é a mesma no 0001, 0007, 0008 e 0009, exceto pelo item 3. O 0010 não chama mais o `LoadGovernor` a partir do `PhaseHost`.

### ADR Dependency Order
Sem ciclos pelo script. Ordem: ADR-0001, 0002, 0003, 0004, 0005, 0006, 0007, 0008, 0009, 0010. Os 10 ADRs estão `Proposed`. O conflito novo 1 é um ciclo lógico (0007 lê um valor que o 0010 possui, e o 0010 depende do 0007) que o script não detecta; o conflito 2 é uma dependência oculta do 0009 para o 0010.

### GDD Revision Flags (Architecture → Design Feedback)
Nenhum novo. Segue aberta a pendência do GDD #7 (L182, L530, L796: pré-aquecimento "no `Preparar`"), registrada no ADR-0009 L369, e a pergunta de jogo do hit-stop (#6).

### Engine Compatibility Issues
Engine: Unity 6.3 LTS (6000.3.27f1). `Engine Compatibility` em 10 / 10 ADRs. Nenhuma API depreciada em uso.

### Engine Specialist Findings (`unity-specialist`, delta da rodada 2)
- **Fechados:** as 3 ressalvas do HIGH do ADR-0009 (assert de que N ≤ lote real; `_ForjaChunkBase` uniforme por draw; mesmo alvo, MSAA e depth no aquecimento), o VR9 (Shuriken × quads), M1 (frustum), M3 (sem fade), M4 (como pergunta aberta, sem decisão), L1 (domain reload ligado, conferido em `EditorSettings.asset` L27-28) e L2 (`gcIncremental: 1`, `androidUseSwappy: 0`, `enableFrameTimingStats: 0`, conferidos nos `ProjectSettings`).
- **PARCIAL:** o HIGH da §7 do ADR-0003. O `.androidlib` está correto e marcado NOT SOURCEABLE (ADR-0003 L375); falta dizer onde ficam os atributos `android:fullBackupContent` e `android:dataExtractionRules` do `<application>` (Custom Main Manifest ou fusão do manifest da biblioteca). Vira item do spike.
- **MEDIUM novos:**
  - **M4, Addressables (ADR-0010 L147, ADR-0009 L113):** "outro carregador" quase não existe no 6.3. Sem `Resources.Load`, as opções assíncronas reais com liberação no `Discard` são Addressables, AssetBundle cru ou cena aditiva por fase (`LoadSceneAsync`/`UnloadSceneAsync`). Uma referência serializada direta garante a residência, mas fica carregada para sempre. Correção: listar as três opções na pergunta. NÃO SOURCEÁVEL. O mipmap streaming está desligado (`QualitySettings.asset` L39 e L93) e deve continuar assim para os assets do chefe.
  - **JNI (ADR-0003 L374):** o attach uma vez por thread está correto, mas falta obrigar `AndroidJNI.DetachCurrentThread()` num `finally` antes de a thread dedicada terminar (no ART, uma thread que sai anexada aborta o processo); e numa thread de worker o `FindClass` só enxerga classes do sistema (`android.system.Os` funciona; uma classe do `.androidlib`, não), então a classe é resolvida na thread principal e guardada como referência global. NÃO SOURCEÁVEL.
- **LOW novos:**
  - ADR-0010 L136-140: o orçamento ainda soma "carga dos assets e pré-aquecimento até 3000", mas a residência não tem teto próprio (só `ENTRY_MAX_MS`). Separar a linha da residência da do aquecimento.
  - ADR-0007 L221: `DtUsedSeconds` precisa valer 0 no `dt` descartado depois de voltar do segundo plano, e o `LoadGovernor` precisa zerar as janelas no 1º `Tick`. O `targetFrameRate` no `BeforeSceneLoad` vale no Android, e `vSyncCount: 0` já está em `QualitySettings.asset` L32 e L86.
  - ADR-0010 L186-187 e ADR-0001 L248 (`Stopwatch`): no Mono/IL2CPP, `Stopwatch.Frequency` vale 10⁷; no editor CoreCLR, 10⁹. Converter sempre por `ITimestampSource.Frequency`. NÃO SOURCEÁVEL.
  - ADR-0009 L114: o desenho de aquecimento também precisa usar o mesmo URP Renderer, nível de qualidade e luz com sombra, senão os passes `ShadowCaster` e `DepthOnly` só compilam no primeiro frame de jogo. NÃO SOURCEÁVEL.
  - ADR-0009 L211: o "limite real de lote" precisa de uma forma de medir (`SystemInfo.maxConstantBufferSize` ÷ bytes por instância, ou o `ProfilerRecorder` "Draw Calls Count" no aparelho). NÃO SOURCEÁVEL.
- **Não verificado pelo especialista:** M2 e L3 do ADR-0010; as Seções 1 a 5 e o diagrama do ADR-0010 só em parte; se o `.androidlib` exige `build.gradle` no 6.3; se o Addressables lança no 6.2+; o `FrameTimingManager` em Release no GLES; se `Forja.Gameplay.Sim.Budget` divide o asmdef com os sistemas de tick (se dividir, a proibição de `Stopwatch` no ADR-0010 L206 é só convenção).

### Architecture Document Coverage
**NOT ASSESSED:** não existe `docs/architecture/architecture.md`. A Fase 6 não rodou.

---

### Verdict: CONCERNS

Subiu de FAIL (5ª passada). O 🔴 N1 está resolvido no que importa (a residência obrigatória está em ambos os ADRs; sobra uma frase no ADR-0009 L116) e esta passada não achou nenhum 🔴 novo. O teto é CONCERNS por três motivos: os 10 ADRs estão `Proposed` (🟡 não é aprovação), a Fase 6 está NOT ASSESSED (impede PASS no modo `full`) e há conflitos 🟠 abertos. **O veredito depende de o conflito novo 1 ter sido classificado como 🟠:** o agente de revisão o tratou como 🔴, e com essa classificação seria FAIL de novo.

### Blocking Issues (must resolve before PASS)
Nenhum conflito bloqueante. Antes do aceite do ADR-0001, em ordem:
1. Conflitos 🟠 novos 1 a 5 e a sobra do N1 (ADR-0009 L116).
2. Decisões do usuário: Addressables (M4, agora com as três opções) e `UltimoDanoTick` (muda o golden hash do #6).
3. Pendências nos ADRs 0005 e 0006 (`Depends On` do 0006, `QueueCapacity`/`R` no 0005).
4. `/create-architecture` (para a Fase 6 deixar de ser NOT ASSESSED) e a revisão independente dos GDDs #2 e #3, depois `/architecture-decision accept ADR-0001`.

### Required ADRs
1. Emenda aos ADRs 0007, 0009 e 0010 para os conflitos 🟠 novos 1 a 5 (a constante da taxa em `Sim.Host`, a interface neutra do nível de carga, o dono do hash e dos contadores no passo 4, os dois tetos da residência e do aquecimento, a linha L5 do #8 e do #16).
2. Emenda ao ADR-0003 (JNI com detach e classe global, atributos do manifest, e os itens pendentes: `MarkAnswer`, enum de causas, `ReadOnlyRejected`, `IDataResolver`, marca fantasma do `CancelStage`).
3. ADRs futuros: ponto fixo (Alpha), análise estática e CI, avisos do save para a UI, feedback de plataforma.

### Pré-gate (todos ❌)
- ❌ Raiz de testes Unity (`Assets/Tests/EditMode/` e `Assets/Tests/PlayMode/`): `/test-setup`
- ❌ `.github/workflows/tests.yml`: `/test-setup`
- ❌ `design/accessibility-requirements.md`: `/ux-design`
- ❌ `design/ux/interaction-patterns.md`: `/ux-design`

### Limites desta passada
- A rastreabilidade conferiu as 35 ⚠️ e as 4 ❌ antigas e as 10 linhas que mudaram na 5ª passada; as outras 117 linhas 🟡 não foram reconferidas.
- O agente de conflitos não leu o ADR-0006 por inteiro (incluindo a L89), nem os ADRs 0004 e 0005 além de grep, nem os GDDs, nem fatos de motor.
- O especialista leu o ADR-0010 em parte e não verificou M2/L3.
- O conflito novo 1 foi reclassificado de 🔴 para 🟠 por mim, depois de conferir as linhas citadas.
- Esta passada mede o estado depois da rodada 2; as correções foram feitas por agentes e só foram verificadas por esta revisão e pelo script de dependências.
- Os arquivos `tr-registry.yaml` e `consistency-failures.md` não mudaram (sem IDs novos e sem conflito 🔴).
