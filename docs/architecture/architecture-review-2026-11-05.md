## Architecture Review Report
Date: 2026-11-05
Mode: full
Workflow: full
Engine: Unity 6.3 LTS (6000.3.27f1)
GDDs Reviewed: 6 (de 8 arquivos em design/gdd/; game-concept.md e systems-index.md não são GDDs de sistema)
ADRs Reviewed: 3

Reviewed-Content-Hash: docs/architecture/adr-0001-simulacao-deterministica-float32-tick-30hz.md 3b95bbc32565a5527425c703a27dd1c11d6509be
Reviewed-Content-Hash: docs/architecture/adr-0002-dados-e-balanceamento-snapshot-imutavel-gerado-no-build.md 9f40c08f9c59a92d0cebc7a8570192582f48066f
Reviewed-Content-Hash: docs/architecture/adr-0003-save-local-envelope-tlv-commit-atomico-gravador-unico.md b2b8e643afcb53e743598ece049e82c46d85c010
Reviewed-Content-Hash: design/gdd/combate-e-dano.md 3fe998f96ba1c65be5ad71bee8bd7b91c9965729
Reviewed-Content-Hash: design/gdd/dados-e-balanceamento.md 36e6d1886f91d8c766b2e4a9a6b43fe91834a9d7
Reviewed-Content-Hash: design/gdd/fluxo-de-fase.md 022ecda6c354b3fda492fca85492943bc3ebff62
Reviewed-Content-Hash: design/gdd/game-concept.md 3a61558d87c0374c253396d6a268ac932ac062f3
Reviewed-Content-Hash: design/gdd/horda-waves-e-inimigos.md c4b40ed39de60bc67735ce70b72e1f9b5e50589e
Reviewed-Content-Hash: design/gdd/save-local.md 05117224694ea7bdbe211af4a2400b9225010b53
Reviewed-Content-Hash: design/gdd/simulacao-deterministica.md b10ca52446075ff31c758cda1c56a4cdb31098a9
Reviewed-Content-Hash: design/gdd/systems-index.md a592f42638761936179ee0842d8e4c46b612093b
Reviewed-Content-Hash: docs/architecture/tr-registry.yaml c7d31793f3f1bd6494bf2ac53bc341447f68ce82
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
Reviewed-Content-Hash: docs/consistency-failures.md 422b7285b01888f60d0315ad6e38e7f6c0c4ce32
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

> **2ª passada de 2026-11-05.** Substitui a 1ª passada do mesmo dia (FAIL; 119 requisitos: 60 🟡, 39 ⚠️, 20 ❌). Motivo da nova passada: o ADR-0001 ganhou as emendas 15 e 16, os GDDs #2, #6 e #7 foram revisados, e o índice de sistemas e o log de consistência mudaram. Os GDDs #1, #3 e #28 e os ADR-0002 e ADR-0003 não mudaram; para eles só se conferiu se as emendas novas do ADR-0001 alteram alguma linha (não alteram).
>
> **Atualização da 2ª passada (mesmo dia, depois da `/consistency-check`).** Mudaram só dois insumos: o #7 (saída do knob `atraso_oferta_rugido_ticks`, 7 trechos) e o `docs/consistency-failures.md` (1 entrada nova, entre GDDs). Foi verificado que essas foram as únicas mudanças: desfeitas numa cópia, os dois arquivos reproduzem exatamente o hash do recibo anterior (`5e50308a` e `df5c6a6d`). Nenhum requisito do #7 cita o knob, então matriz, contagens, flags e veredito não mudam; a lista de divergências e a nota da Phase 4 foram atualizadas e o recibo abaixo foi tirado de novo. Por decisão do autor, não se rodou de novo a revisão completa com agentes.

### Traceability Summary
Total requirements: 125 ativos (mais 1 superseded)
✅ Covered (ADR Accepted): 0
🟡 Covered (ADR Proposed): 64
⚠️ Partial: 44
❌ Gaps: 17

As 3 ADRs estão `Proposed`; a cobertura é, portanto, 🟡 e limita o veredito a CONCERNS no máximo. A rota é `/architecture-decision accept ADR-NNNN`.

| GDD | Ativos | 🟡 | ⚠️ | ❌ | Mudança desde a 1ª passada |
|---|---|---|---|---|---|
| #2 Simulação | 22 | 13 | 7 | 2 | +2 requisitos (021, 022). O 009 caiu de 🟡 para ⚠️ |
| #3 Fluxo de fase | 20 | 11 | 8 | 1 | Nenhuma |
| #1 Dados | 20 | 12 | 7 | 1 | Nenhuma |
| #28 Save | 19 | 14 | 4 | 1 | Nenhuma |
| #6 Combate | 22 | 6 | 9 | **7** | TR-016 (`AvisoPerto`) superseded; +3 requisitos (021 a 023), todos ⚠️ |
| #7 Horda | 22 | 8 | 9 | **5** | 002 e 020 subiram para 🟡; 006 e 010 foram de ❌ para ⚠️; +2 requisitos (021 🟡, 022 ⚠️) |

O #6 não ganhou nenhum 🟡: as emendas 15 e 16 do ADR-0001 não tocam colunas, canais, geometria nem orçamento.

Registro de TRs (`tr-registry.yaml`, versão 3): +7 IDs novos (simulacao-021 e 022, combate-021 a 023, horda-021 e 022), 21 textos reescritos com a mesma intenção (campo `revised`), e `TR-combate-016` marcado `superseded-by: TR-combate-004`. Nenhum ID foi renumerado.

### Coverage Gaps (no ADR exists)
Ver "Known Gaps" em `requirements-traceability.md` para a lista dos 17 e as ADRs sugeridas. Os de camada Core, que bloqueiam `/create-epics` de #6 e #7:
- colunas do `SimWorld` (as hasheadas do #6; `classe`, `arquetipoId` e `tickNascimento`, que o `Spawn` não recebe);
- fila de dano `Combate.Aplicar`/`Curar`, `curaPendente`, `modDano` e `modCadencia`, mais o pedido tipado de `Rugido`;
- `SimVec2` e geometria (o ADR-0001 L62 adia o tipo para "o ADR do #6", que não existe) e a consulta espacial com 300 ou mais vivos;
- orçamento de frame por sistema (ADR-0001 L433 não fixa).

Fora do Core, sem ADR: ponte de entrada (TR-simulacao-015), render de multidão, pré-aquecimento de assets do chefe, háptico e tremor, e a validação entre aparelhos (ponto fixo, Alpha).

### Cross-ADR Conflicts
> **Áreas propensas a conflito** (`docs/consistency-failures.md`, 16 entradas, todas de 2026-11-04 e 2026-11-05): só 1 é de arquitetura, o contrato do snapshot entre ADR-0001 e ADR-0002 (abaixo, agora 🟠). As outras 15 são entre GDDs e se concentram na fronteira #2 × #6 × #7: capacidade de ids, efeito de mortes dentro do tick, fila de dano e rugido, causa de morte num enum de ADR `Proposed`, predicados removidos ainda citados, e casos especiais esquecidos quando uma regra geral muda (a oferta do rugido, a mais recente). Padrão para as próximas ADRs (0004 a 0006): todo campo, enum ou canal que um GDD de Feature nomeia precisa entrar na emenda do ADR do Core na mesma passada.

**Nenhum conflito bloqueante.** O conflito 🔴 da 1ª passada (`IPhaseSnapshot`) caiu para 🟠 depois da conferência direta do texto: o `IPhaseSnapshot` (ADR-0001 L231) expõe só capacidades e hash, o comentário diz que "o tipo do snapshot é do ADR-0002", e o `PhaseSnapshot` concreto do ADR-0002 (L113-115) implementa a interface e tem `SpawnsDeDados` e `CapacityMarginPct`. O que sobra é falta de clareza: o ADR-0001 (Emenda 6 L99; L291; critério L452) diz "lidos do snapshot" sem dizer que o compositor precisa do tipo concreto, e não declara a referência entre asmdefs. A referência `Gameplay.Sim` → `Forja.Data` vem do relatório do agente de conflitos (ADR-0002 L101) e não foi conferida linha a linha.

Três conflitos não bloqueantes (🟠):
1. **ADR-0001 × ADR-0003, `AttemptId`.** O `PhaseResult` (ADR-0001 L261, asmdef `Forja.Gameplay.Sim`) leva o `attemptId` de 128 bits, que o ADR-0003 (L139) define em `Forja.Save`. Nenhuma ADR declara a referência `Gameplay.Sim` → `Forja.Save`, e a regra do "mesmo tipo" (ADR-0003 L200) não lista o `PhaseResult`. Opções: declarar a referência e incluir o `PhaseResult` na regra, ou mover o `AttemptId` para um asmdef neutro.
2. **ADR-0002 × ADR-0003, FNV-1a 64.** O ADR-0003 (L34, L80, L182, L357) fixa a API pública da função FNV-1a 64 de `Forja.Data` e diz que não emenda o ADR-0002, que ainda não a tem nas Key Interfaces (ADR-0002 L319, pendência Q4). Há um terceiro FNV no `StateHasher` do Core (ADR-0001 L105). Opções: pôr `Fnv1a64` nas Key Interfaces do ADR-0002, ou usar a função do Core nos dois lugares.
3. **Orçamento da tela de carregamento.** `Create` e `Preparar` com a composição inteira das waves (ADR-0001 L296), o teto de 3000 ms a frio e 1500 ms a quente do #1 (ADR-0002 L289) e 3 a 4 `fsync` do `BeginStage`, com cauda de 100 a 500 ms cada (ADR-0003 L91). Nenhuma ADR é dona do orçamento total de entrada na fase. Opções: declarar o orçamento e o dono, ou medir no spike e, se estourar, usar a Alternativa 10.

As emendas 15 e 16 do ADR-0001 não criam conflito novo com o ADR-0002 nem com o ADR-0003.

Textos desatualizados dentro das ADRs (sem efeito de contrato, pedem limpeza):
- **Persistem da 1ª passada:** ADR-0003 L304 ("só depois de ler um save válido") contra L119 e L346; ADR-0003 L360 lista o `attemptId` de 128 bits como pendente de alinhar (já está em ADR-0001 L261); ADR-0001 L386 ("mínimo de 1 tick") contra o corpo (L69, L269); ADR-0001 L399 e L404 listam a Regra 13 do #2 como pendente.
- **Novos:** ADR-0001 L34 ("Depends On: None") e L465 ("Sem outros ADRs além dele"), com o ADR-0002 e o ADR-0003 existindo; ADR-0001 L37 ("Deve ser Accepted antes de `/design-system` de #6"), com o GDD #6 já existente; ADR-0002 L34 ("único outro ADR") e L317 (ADR do save como candidato futuro).
- **Resolvidos desde a 1ª passada:** "CRC do cabeçalho" no ADR-0003; #6 e #7 como "GDD pendente" no ADR-0001; a linha 23 da tabela Emendas do ADR-0001 existe (L499).
- **`PhaseForWrite` em `Created`:** o texto agora é coerente (a guarda aceita `Created`, e por convenção só o `IdDoHeroi` é escrito). A ficha inteira continua aberta em `Created`, protegida só por revisão (ADR-0001 L107, L199, L396). Um agente a deu por resolvida e outro por persistente com a linha L396 ("`Spawn` e a ficha") ainda contradizendo a L107; fica registrada como pendência de redação.

### ADR Dependency Order
Script `adr-dep-graph.sh`: 3 ADRs, 3 arestas, sem ciclo, sem `NO_DEPS_SECTION` nem `UNFILLED_DEPS`.

```
Foundation (sem dependências):
  1. ADR-0001: Simulação determinística float32, tick 30 Hz   [Proposed]
Depende de Foundation:
  2. ADR-0002: Dados e balanceamento, snapshot imutável       [Proposed] (requer ADR-0001)
  3. ADR-0003: Save local, envelope TLV, commit atômico       [Proposed] (requer ADR-0001, ADR-0002)
```

⚠️ Os três continuam `Proposed`. Nenhum dos dois últimos pode ser implementado com segurança antes de o ADR-0001 ser `Accepted`. O aceite do ADR-0001 depende da revisão independente dos GDDs #2 e #3 e não é condicionado ao spike de hash. O ADR-0003 só aceita depois do gate G1 a G4 num aparelho Android real.

### GDD Revision Flags (Architecture → Design Feedback)
Estas suposições do GDD conflitam com uma decisão de ADR ou com o comportamento verificado da engine.

| GDD | Suposição | Realidade (ADR / engine) | Ação |
|---|---|---|---|
| combate-e-dano.md (AC-D5, L723) | `StateHash` do tick 900 igual entre o Editor e o IL2CPP ARM64 | ADR-0001 só promete o mesmo build e o mesmo runtime, com golden por runtime (L391, L450); float entre runtimes é `NOT SOURCEABLE` | Revisar o GDD (ou emendar o ADR). **Continua aberto depois das edições de hoje no #6** |
| dados-e-balanceamento.md (AC-09) | Teste por reflexão: "nenhum tipo é `T[]`" | ADR-0002 §4 decodifica para `int[]`/`float[]` privados expostos por `ReadOnlySpan` | Revisar o GDD (não relido nesta passada; o GDD não mudou) |
| simulacao-deterministica.md (L103) e fluxo-de-fase.md (L133, L170) | Perda de foco conta como pausa | ADR-0003 §6: a pausa usa `OnApplicationPause` e nunca `Focus`; o ADR-0001 não diz quais callbacks a ponte ouve | Revisar os GDDs e a ponte |

Resolvidos desde a 1ª passada: o AC-D6 do #7 (Editor × aparelho) saiu, o `float2` na F4 do #7 virou `SimVec2`, e o "contagens podem virar remoto" do #7 foi removido.

Índice de sistemas (aplicado nesta passada, com autorização do usuário): **#6 passou de In Review para Needs Revision**, por causa do AC-D5. #1, #2 e #3 já estavam em Needs Revision.

Outras divergências GDD × ADR e entre GDDs (não são HIGH RISK de engine; entram nas emendas e nas ADRs novas). As de #1, #3 e #28 da 1ª passada continuam como estavam, porque os GDDs e as ADRs correspondentes não mudaram.

*Novas ou alteradas nesta passada:*
- **Morte por Rugido e XP:** a Emenda 15 (ADR-0001 L108) atribui ao #3 "metade do XP e limite de um nível" para a causa `Rugido`; o GDD #3, que não mudou, só conhece as causas "normal ou valor inválido" (L205) e a F2 soma só a causa normal (L246). Pelo GDD a morte por Rugido dá 0 XP, pelo ADR dá metade.
- **Evento `Death`:** o #2 (L374) e o #6 (L94) falam em `Death` com causa; o ADR-0001 (L108) diz que o evento não carrega a causa (ela fica em `DeathsThisTick`). Além disso o ADR emite `Death` por entidade (L99, L193), enquanto o #6 (L68, L419, AC-R14) quer evento agregado da horda por tick, e o `SimEvent` tem um único `Value` (L151-157).
- **Reserva de eventos e `Rugido`:** ADR-0001 L407 pede `EventCapacity` ≥ pico de vivos mais reserva, ou o `Rugido` em `EventosReservados`; a reserva do #2 (L88) não o prevê e o P6 (L595) não cobre o tick do rugido (~300 `Death`).
- **Causa por golpe:** a F2 do #6 (L147; AC-F2 L684) identifica a entrada da fila que matou; o `DeathRecord` (ADR-0001 L171) só tem o enum.
- **Cast direto:** a F4 do #6 (L107, L195) usa `(int)(x + 0,5f)`; ADR-0001 L287 manda nunca fazer cast direto.
- **Nascimento no `CombatTick`:** o #6 pula quem nasceu no tick corrente (L61, L367); o ADR-0001 (L99) deixa ids novos agirem a partir do sistema seguinte e o `Spawn` (L192) não tem `tickNascimento`, classe nem arquétipo; o `DeathRecord` não tem facção nem `xpValue`, que o #3 exige.
- **Canais e colunas:** `Combate.Aplicar`/`Curar` são chamadas entre sistemas e o #3 escreve `curaPendente` depois do #6 (#6 L56, L69), contra "comunicação só pelo `SimWorld`" (ADR-0001 L84, L267). ADR-0001 L82 manda o estado extra ficar no sistema, mas o #6 (L103) põe colunas no `SimWorld` que o #7 e o #12 leem.
- **Contadores do modo estrito:** `GolpesDescartados`, `ModForaDeFaixa` e `CurasDescartadas` do #6 (L351-362) ficam fora da Emenda 9 (ADR-0001 L102), e o `SimContext` não tem como contar nem lançar. O #2 (L374) regrava HP = 0 em NaN; a Emenda 8 só a posição (L101).
- **Marcas velhas no #2:** "exige no ADR (OQ-5)" em L59, L76, L110, L112 e "pedem linha no ADR" em L96 e L336, com a OQ-5 resolvida e a Emenda 8 já escrita. No #6, L57 e L435 ainda dizem "emenda pendente; o ADR só tem Normal e InvalidValue", já resolvido pela Emenda 15.
- **#6 × #7:** o #6 manda o #7 declarar a recarga `g` (L60); o #7 não declara, e a F10 do #6 (L374, L389) soma só Aviso, Impacto e Recuperação, então o `duelo_min` fica subestimado se `g` > 0. ~~O #7 ainda tem `atraso_oferta_rugido_ticks`, que contradiz a oferta imediata do #6 (Regra 16).~~ **Resolvido em 2026-11-05** pela `/consistency-check`: por decisão do autor (a reavaliar), a oferta do nível do rugido abre na hora, como as outras, e o knob saiu do #7. O #7 não depende mais do `AvisoPerto` (L439).
- **#7:** ADR-0002 L86 ordena as waves "por índice" e o #7 ordena por (`inicio`, `w`) (L76-77); `NextBounded` (#7 L92, L233) contra `Pcg32.NextInt` (ADR-0001 L164); "5 a 7 waves" (L814) contra 8 a 10 na Regra 5 (L90); `SimEventKind` sem `Rugido` e `Spawn` no tick parecendo emitir evento (ADR-0001 L154).
- **Testes:** o #6 depende de `BannedApiAnalyzers` (L722), cujo suporte no Unity é `NOT SOURCEABLE`, e marca como "PRONTO no Editor" a medição de alocação por `GC.GetAllocatedBytesForCurrentThread` (L728), enquanto o #2 (L591) diz que contar alocação em EditMode é `NOT SOURCEABLE`. O caminho de testes do #6 (`Assets/Tests/EditMode/Combate/`, L639) difere do do ADR-0001 (`.../Simulation/`, L281).

*Da 1ª passada, ainda abertas e sem mudança nos GDDs:* #1 F1 cita `MidpointRounding.AwayFromZero` (ADR-0002 proíbe) e F3 admite override de margem por capacidade (o ADR tem `CapacityMarginPct` única); #1 AC-08 compara a revisão por hash e `IDataVersion.Revision` expõe `int`; #28 usa `IDataResolver`, `IStageMarkHandler`, `IEventSink`, `OnMarkFound` e `ReadOnlyRejected`, que o ADR-0003 não tem (ele chama o sink de `ISaveEventSink`); #3 diz que o efeito da marca não precisa deduplicar e ADR-0003 L108 manda deduplicar; #3 ainda descreve `AttemptId` como `int` (L203, L398, L425, OQ-11); caminho de testes do #28 contra o do ADR-0003; `PhaseSheet` sem `MotivoFim` (#3 L80, L151, L427); ficha inteira gravada no `Preparar` contra a Emenda 14; `ISeedSource` sem decisão.

### Engine Compatibility Issues
Engine: Unity 6.3 LTS (6000.3.27f1). ADRs com seção Engine Compatibility: 3 de 3.

- Versão: as 3 ADRs concordam com o editor instalado e com `VERSION.md`. Item LOW: ADR-0001 L403 diz "6.5 ou 6.6 (Editor CoreCLR)", e `VERSION.md` só fala em "toward a CoreCLR Editor" no 6.5; a mudança que pesa é a do 6.6 (projetos novos pulam o domain reload por padrão).
- API depreciada: só a carga síncrona de `TextAsset` embarcado (ADR-0002 L98, L265-266), registrada como desvio deliberado de `deprecated-apis.md:73-74`. `Resources.Load` aparece só em frases que o proíbem. Nenhum `InstanceID` nas ADRs (a mudança para `EntityId` do 6.4 não as afeta).
- Pós-cutoff: nenhuma API usada. As emendas 15 e 16 são C# puro. Muitos itens `NOT SOURCEABLE`: float entre Mono, IL2CPP e ARM64, FMA, asmdef sem engine, `ref struct` com `ReadOnlySpan` nos dois runtimes, `File.Replace` atômico, `fsync` de diretório, callbacks de pausa e foco, Auto Backup, `BannedApiAnalyzers`, shader por instância e vibração do Android.
- Ausência de `modules/core.md`: nada do domínio Core foi checado contra módulo de referência.

### Engine Specialist Findings (`unity-specialist`)
Os 6 achados da 1ª passada **persistem**, porque as ADRs não mudaram. Itens marcados [conhecimento] não estão na referência local e pedem o spike no aparelho.

- **HIGH, ADR-0003 §7 (L119):** os XMLs de backup estão em `Assets/Plugins/Android/res/xml/`; a Unity recusa recursos soltos ali, e `Assets/Plugins/` nem existe no disco. Com `useCustomMainManifest: 0` (`ProjectSettings.asset:266`), as regras de backup não chegariam ao APK e o Auto Backup levaria tudo, inclusive `save.bak` e a quarentena. Mover para `.androidlib` ou AAR.
- **MEDIUM, GameActivity e manifesto:** `androidApplicationEntry: 2` (`ProjectSettings.asset:86`, GameActivity [conhecimento]). ADR-0003 L119 depende de um Custom Main Manifest desligado e de `UnityPlayer.currentActivity`, sem tratar a GameActivity.
- **MEDIUM, domain reload:** `EditorSettings.asset:27-28` (`m_EnterPlayModeOptionsEnabled: 1`, `m_EnterPlayModeOptions: 0`, ou seja, recarrega domínio e cena [conhecimento]); ADR-0003 L28 e L113 supõem "domain reload desligado". ADR-0001 L274 só fala condicionalmente. Os testes de `static` mutável passam no Editor atual por acaso.
- **MEDIUM, eventos estáticos da engine:** ADR-0003 L194 liga o `Dispose` a `Application.quitting` sem exigir desinscrição; ADR-0001 L295 e ADR-0003 L187 proíbem só `static event` próprio.
- **MEDIUM, thread do gravador:** ADR-0003 L113 e L194 não citam `IsBackground = true` nem join em `AssemblyReloadEvents.beforeAssemblyReload` [conhecimento].
- **MEDIUM, ordem de boot:** ADR-0002 L98, ADR-0003 L191 e L206 não fixam ordem nem uma raiz de composição única.
- **MEDIUM, novo: foco e pausa.** O GDD #3 (L170) põe a fase em Pausada por perda de foco e o ADR-0003 (L116, L186) proíbe `Focus` para o save. As regras são compatíveis (pausar a simulação e não gravar), mas o ADR-0001 (L289) não diz quais callbacks a ponte ouve. `OnApplicationFocus(false)` dispara com a cortina de notificações e em multi-janela, e a ordem foco/pausa no Android não é garantida [conhecimento]. A ponte precisa somar os dois sinais num único motivo de pausa.
- **LOW, novos:** o `RngWave` (Emenda 16) devolve um `Pcg32` mutável por valor, então encadear `ctx.RngWave(w).NextUInt()` duas vezes repete o valor sem erro (ADR-0001 L104, L290; vale um analisador ou teste); a composição inteira das waves no `Preparar` aloca na tela de carregamento (aceitável com o GC incremental [conhecimento], se a tabela for dimensionada pelo snapshot e reusada); o `DeathCause` vai para o log sem tipo-base declarado (ADR-0001 L108; fixar `: byte` ou `: int`).
- **LOW, da 1ª passada:** a thread do gravador nunca chama `Application.*` nem `Time.*`; `TextAsset.bytes` aloca cópia a cada acesso; o teto de 500 ms em `OnApplicationPause` precisa ficar abaixo do limite de ANR; o clang do NDK contrai `a*b+c` em FMA no ARM64, então gravar `il2cppCompilerConfiguration` na tag do build deve ser obrigatório; zerar o acumulador de tempo em `OnApplicationPause(false)`; alinhar "Auto Referenced" desligado também para `Forja.Save`.
- Consistência de threads entre as ADRs: consistente (simulação só na thread principal; retrato do save na principal; respostas por fila lida entre frames). Grafo de asmdefs sem ciclo.

### Architecture Document Coverage
**NOT ASSESSED — não existe `docs/architecture/architecture.md`.** Em modo full, isso por si só impede PASS. `/create-architecture` o gera.

---

### Verdict: FAIL

Motivos:
1. Requisitos de camada Core do #6 e do #7 sem nenhuma ADR (colunas do `SimWorld`, fila de dano, vetor e geometria, consulta espacial).
2. Nenhuma das 3 ADRs está `Accepted`; toda a cobertura é 🟡.

Além disso, Phase 6 está NOT ASSESSED (sem `architecture.md`). Não há conflito bloqueante entre ADRs nesta passada.

### Blocking Issues (must resolve before PASS)
1. Escrever as ADR-0004 (colunas do `SimWorld`), ADR-0005 (pipeline de dano e eventos) e ADR-0006 (vetor, geometria e consulta espacial), ou decidir explicitamente adiar #6 e #7.
2. Emendar o ADR-0001 e aceitá-lo; depois aceitar o ADR-0002 e o ADR-0003. A emenda cobre: `IPhaseSnapshot` explícito sobre o tipo concreto, ficha inteira no `Preparar` com `MotivoFim`, `Spawn` e `DeathRecord` estendidos (classe, arquétipo, `tickNascimento`, facção, `xpValue`), `SimEventKind.Rugido` e o `Death` agregado, contadores do modo estrito e NaN com HP = 0, callbacks de foco e pausa da ponte, e a limpeza dos textos desatualizados.
3. Corrigir o HIGH de engine do ADR-0003 §7 (XMLs de backup fora de `Plugins/Android/res`) e decidir a premissa de domain reload.
4. Gerar `docs/architecture/architecture.md` (`/create-architecture`).
5. Ajuste de GDD (não de ADR): reescrever o AC-D5 do #6 (hash Editor × IL2CPP).

### Required ADRs
Em ordem, as mais fundamentais primeiro:
1. **Emenda ao ADR-0001** (não é ADR novo): ver o bloqueio 2.
2. **ADR-0004:** colunas do `SimWorld` para combate e horda (Foundation/Core, engine LOW).
3. **ADR-0005:** pipeline de dano e eventos de combate (Core, LOW).
4. **ADR-0006:** vetor, geometria e consulta espacial determinísticos (Core, LOW; MEDIUM em desempenho).
5. **Ponte de entrada, tempo e ciclo de vida do app** (Feature, HIGH).
6. **Log de eventos e instrumentação do #5** (Core, MEDIUM).
7. **Emenda ao ADR-0003:** marca encontrada, enum de causas e `ReadOnlyRejected`, `IDataResolver`, registro do Grimório como 2º commit, `AttemptId` entre asmdefs e o FNV-1a 64 nas Key Interfaces do ADR-0002.
8. **Orçamento de frame por sistema e de entrada na fase** (Foundation; depois do spike de performance).
9. **Render de multidão e VFX em mobile** (Presentation, HIGH).
10. Depois: análise estática e CI; avisos do save para a UI; háptico e tremor; ADR do #29; ponto fixo para ranking (Alpha).

### Limites desta passada
- A extração dos requisitos e as citações de linha de #2, #6 e #7 vêm de 3 agentes de leitura; a reconferência de #3, #1 e #28 contra o ADR-0001 novo, de um quarto. Os conflitos entre ADRs e a auditoria de engine vêm de mais dois.
- Conferi diretamente: o grafo de ADRs, os status, a ausência de `architecture.md`, o contrato do `IPhaseSnapshot` entre ADR-0001 e ADR-0002, as contagens (feitas sobre as linhas da matriz) e a validade do registro. As linhas citadas por requisito não foram reconferidas uma a uma.
- As colunas "Fonte no GDD" de #3, #1 e #28 são as da 1ª passada.

---

## Requirements Traceability Matrix (completa)

#### #2 Simulação determinística (`design/gdd/simulacao-deterministica.md`)

| TR-ID | Requisito | Domínio | Fonte no GDD | ADR | Status | Nota |
|---|---|---|---|---|---|---|
| TR-simulacao-001 | Simulação e compositor em C# puro, asmdef sem engine, sem static mutável; uma instância por fase, sem serializar nem retomar | Core | R16 L114; C12 L542; A1 L588 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-simulacao-002 | Só float32; operações via SimMath, sem transcendentais, double nem Mathf; RoundToInt e FloorToInt com checagem de faixa; empate por id | Core | R9 L94-96; D9a-c L521-523 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-simulacao-003 | Ticks inteiros a 30 Hz; simulação sem relógio; ponte acumula dt, MaxTicksPerFrame descarta excedente, interpolação lê prev/atual | Core | R11 L101-102; FS1/FS2; T1, T2, T5 | ADR-0001, ADR-0002 | 🟡 Covered (Proposed) |  |
| TR-simulacao-004 | PCG32 com 3 streams via SplitMix64; RngWave(w) puro, sem estado, fora do hash, disponível no Preparar e no Tick; ids de stream registrados; política de IA não consome streams | Core | R1.3 L59; FS3-FS6 L198-276 | ADR-0001 (Emendas 11 e 16) | 🟡 Covered (Proposed) |  |
| TR-simulacao-005 | Simulation.Create(snapshot, hashLog, seed, sistemas, estrito) confere o hash; estados Created/Running/Ended/Broken/Destroyed; erros do host sempre lançam | Core | R1.3 L59; R14 L110; Estados L118-137 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-simulacao-006 | Tick em 7 passos com foto de CombatActive; compacta os vivos no fim; sem hash, relógio nem alocação; não reentrante, só na thread principal | Core | R2 L62-71; R7 L90; C2 L532 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-simulacao-007 | Command (ActorId, Kind, X, Y, ArgA, ArgB), validação e ordem por ator/tipo; vale só no tick; serial do PickOffer validado pelo #16 | Core | R3-R4 L73-80; C3, C4, C10 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-simulacao-008 | Compositor único fixa a ordem dos sistemas para jogo e teste sem tela; dentro do tick, comunicação só pelo SimWorld | Core | R5 L82-86; C5 L535 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-simulacao-009 | SimWorld SoA pré-alocado, id = índice sem reuso, capacidade = total de spawns, Spawn devolve -1, Kill único caminho; FS9 em long no compositor | Core | R7-R8 L90-92; FS9 L314-334; C13 | ADR-0001, ADR-0002 | ⚠️ Partial | O compositor lê `SpawnsDeDados` e `CapacityMarginPct` do `PhaseSnapshot` concreto (ADR-0002 L113-115); o `IPhaseSnapshot` (ADR-0001 L231) não os tem e o ADR-0001 não diz que o compositor usa o tipo concreto (conflito 🟠) |
| TR-simulacao-010 | EventBuffer só de saída, drenado após cada tick; descarta os novos, com EventosReservados e DroppedEvents; não muda o hash | Core | R6 L88; C6 L536; I5 L568 | ADR-0001 | 🟡 Covered (Proposed) | Reserva para o `Rugido` não prevista (ADR-0001 L407; GDD L88) |
| TR-simulacao-011 | CombatHold escrito só pelo #16 e hasheado; CombatTick só avança com o combate ativo | Core | R15 L112; C11 L541 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-simulacao-012 | Checagem de finitude no passo 6, marca Essencial, FalhaInterna > vitória > derrota; NaN regrava posição anterior e HP 0 | Core | R9 L97; R13 L108; Edge L374; D9a/b | ADR-0001 | ⚠️ Partial | Emenda 8 regrava só a posição; o GDD também grava HP = 0 |
| TR-simulacao-013 | Modo estrito por instância; contadores de diagnóstico, inclusive GolpesDescartados, ModForaDeFaixa e CurasDescartadas do #6, lançam no 1º caso em estrito; GolpesLimitados só conta | Core | R14 L110; R10 L99 | ADR-0001 | ⚠️ Partial | SimContext sem como um sistema contar ou lançar; a Emenda 9 lista 4 contadores |
| TR-simulacao-014 | Hash FNV-1a 64 por byte, fora do Tick; reprodutibilidade só no mesmo binário e ABI; goldens por runtime | Core | R10 L99; FS8 L295-312; R12 L106; D8 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-simulacao-015 | Ponte entrega Mover em todo tick do frame e ações discretas 1x; segura a ação em frame de 0 ticks; zera Mover até um toque novo | Entrada | R4 L80; R15 L112; T3a-T3f | — | ❌ GAP | Sem ADR da ponte de entrada |
| TR-simulacao-016 | Pausa, segundo plano e foco: zero Tick, acum zerado, 1º dt descartado, portão do joystick só com CombatHold = 0; callbacks na thread principal | Plataforma | R11 L103; Edge L359-361; T3e, T4, T6 | ADR-0001, ADR-0003 | ⚠️ Partial | Fonte do dt, foco e portão abertos; GDD L103 (foco = pausa) × ADR-0003 L186 (nunca `Focus`) |
| TR-simulacao-017 | Cabeçalho do log: seed antes do tick 0, hash dos dados, tag do build (IL2CPP), ABI e ordem dos sistemas; comparador 'não comparável' | Log | R1.2 L58; R12 L106; Edge L405-406 | ADR-0001 | ⚠️ Partial | Campos da tag e da ABI NOT SOURCEABLE; formato do log (#5) sem ADR |
| TR-simulacao-018 | Orçamentos no aparelho: p95 do Tick (X1), memória (X3), N vivos sem tick descartado, custo do hash (X6), zero alocação, buffer de eventos cobre o pior tick sem DroppedEvents (P6) | Performance | P1-P6 L590-598; OQ-14 | ADR-0001 | ⚠️ Partial | Só o zero alocação está decidido; X1, X3, X6 e N não reivindicados |
| TR-simulacao-019 | Analisador estático bane double, Mathf e System.Random; CI exige testcasecount > 0 | Ferramentas | D9d L524; A2 L589 | ADR-0001 | ⚠️ Partial | Proibições decididas; analisador e passo de CI sem decisão |
| TR-simulacao-020 | Validação entre aparelhos (replay por servidor #22, online #29, coop #35) exige simulação em ponto fixo | Core/Rede | Dependencies L437-439 | ADR-0001 (Negative) | ❌ GAP | Declarado não atendido; ADR futuro de ponto fixo (Alpha) |
| TR-simulacao-021 | Fora do Tick só no Preparar: Spawn do herói sem evento e RngWave do #7; o compositor chama IPreparaFase e IConcluiFase | Core | R1.4 L60; R5 L86; FS6 L275 | ADR-0001 (Emendas 14 e 16) | 🟡 Covered (Proposed) | Novo nesta passada |
| TR-simulacao-022 | Fim com motivo e detalhe (MissingBoss pelo #3, EssentialSpawnRejected pelo #2 no tick); dado inválido não é pedido de fim | Core | R13 L108; Estados L130 | ADR-0001 (Emendas 6 e 7) | 🟡 Covered (Proposed) | Novo nesta passada |

#### #3 Fluxo de fase (`design/gdd/fluxo-de-fase.md`)

| TR-ID | Requisito | Domínio | Fonte no GDD | ADR | Status | Nota |
|---|---|---|---|---|---|---|
| TR-fluxo-001 | Duas metades: SistemaFluxoDeFase (ISimSystem, entre #6 e #16) e TentativaDeFase fora do tick e do hash, uma por tentativa | Core | R2 L53-55; R17 L153; AC-R2 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-fluxo-002 | Ficha de fase no SimWorld, escrita só pelo #3, hasheada pelo Hash do #3, gravada inteira no Preparar, com MotivoFim | Core | R4 L65-82; R3.4 L62; R16 L151 | ADR-0001 | ⚠️ Partial | Emenda 14 libera só IdDoHeroi fora do tick; PhaseSheet não tem MotivoFim |
| TR-fluxo-003 | IPreparaFase e IConcluiFase chamadas pelo compositor, Concluir em toda causa; eventos nunca são canal; #3 não conhece o #16 | Core | R15 L141-149; R9.2 L126; AC-R15 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-fluxo-004 | Herói criado no Preparar por Spawn essencial sem evento, IdDoHeroi = 0, ids_de_preparacao = 1 conferido antes do Create | Core | R3.4 L62; L332-334; Edge L386 | ADR-0001, ADR-0002 | 🟡 Covered (Proposed) |  |
| TR-fluxo-005 | Varredura incremental dos ids novos e lista de mortos do tick com id, facção, causa e xpDaMorte, limpa em todo tick | Core | R5.2 L86; R6 L94; F2 L242-256 | ADR-0001 | ⚠️ Partial | DeathRecord só tem Id e Cause; leitura de facção e xpValue por id fora do contrato |
| TR-fluxo-006 | Fim avaliado num só ponto via RequestEnd com prioridade; PendingEnd faz pular XP e oferta; End/EndDetail traduzidos em causa | Core | R5.3-5.4 L87-88; R8 L103 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-fluxo-007 | Relógio da fase é o CombatTick; #3 inerte com CombatActive falso; somas da F4 em long | Core | R5.1 L85; R7 L101; F4 L281-300 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-fluxo-008 | XP e nível em int com intermediários em long, sem divisão; passo O(1) + O(mortes), sem alocação | Performance | R17 L153; F1-F3; P1, P2 | ADR-0001 | ⚠️ Partial | Orçamento do passo do #3 depende do X1 do #2, não reivindicado |
| TR-fluxo-009 | PhaseResult readonly struct (causa, nível, ChefeVisto, MorteSimultanea, hash, attemptId de 128 bits); ContaComoMorteDeFase função pura | Core | R8 L103-122; AC-X L551-565 | ADR-0001, ADR-0003 | 🟡 Covered (Proposed) |  |
| TR-fluxo-010 | Encerramento: drenar, StateHash (indisponível em Broken), Concluir, Discard, commit de fim, evento ao #5 após a resposta | Core/Persistência | R9 L124-128; Edge L342; E8 | ADR-0001, ADR-0003 | ⚠️ Partial | Evento ao #5 só depois da resposta do commit não tem dono (#5 sem ADR) |
| TR-fluxo-011 | BeginStage assíncrono com resultado real, attemptId e requestId de fonte única; resposta filtrada por requestId; CancelStage não grava | Persistência | R3.2 L60; R10 L131; S3, S10a | ADR-0003, ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-fluxo-012 | Thread única: respostas do #28 numa fila esvaziada entre frames, nunca dentro do Tick, sem continuação em outra thread | Plataforma | R2 L56; L203; S10b L589 | ADR-0003, ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-fluxo-013 | Marca encontrada no boot: o #3 devolve o efeito, gravado no mesmo commit do consumo; Entrar bloqueado até o callback | Persistência | R13 L137; Edge L373 | ADR-0003 | ⚠️ Partial | Notificação não está no ISaveService; ADR-0003 L108 manda deduplicar, o GDD diz que não precisa |
| TR-fluxo-014 | Conjunto de motivos de pausa (foco, segundo plano, ligação, diálogo); 1º dt descartado também após a carga; nasce Pausada; pausa não grava | Plataforma | R11 L133; Edge L343, L346 | ADR-0003, ADR-0001 | ⚠️ Partial | Conjunto de motivos e foco sem decisão; ADR-0003 proíbe Focus |
| TR-fluxo-015 | Fontes injetadas: ISeedSource (seed nova por tentativa, override em teste) e fonte de ids; nenhuma leitura de relógio nem System.Random | Core | R3.2-3.3 L60-61; R10 L131; H3, H4 | ADR-0001, ADR-0003 | ⚠️ Partial | ISeedSource e a origem da entropia da seed sem decisão |
| TR-fluxo-016 | Log do #3: seed antes do tick 0, hash final, causa, MorteSimultanea, abandonada, exceção, commit falhou, ordem dos Preparar | Log | R3.3 L61; R9.4 L128; I6; X11 | — | ❌ GAP | Sem ADR do log #5 |
| TR-fluxo-017 | Abandono confirmado entre ticks, sem Tick: hash marcado abandonada, depois Concluir, depois Discard | Core | R12 L135 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-fluxo-018 | Knobs validados no Preparar por exceção (DadosInvalidos); Create ou Preparar que lança leva a FalhaInterna com hash indisponível | Core | R14 L139; S8; Edge L365, L372 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-fluxo-019 | Checagens de setup no build: limiar <= 2^31-1, F5 nas duas pontas de XP, exatamente 1 Essencial, cronograma com chefe | Dados | F1 L232; F5 L304-326; Edge L353 | ADR-0002 | 🟡 Covered (Proposed) |  |
| TR-fluxo-020 | Registro no Grimório depois do fim, como 2º commit fora da simulação | Persistência | R9.5 L129; OQ-6 L660 | ADR-0003 | ⚠️ Partial | Perda do registro se o app morrer entre os dois commits em aberto (OQ-6) |

#### #1 Dados e balanceamento (`design/gdd/dados-e-balanceamento.md`)

| TR-ID | Requisito | Domínio | Fonte no GDD | ADR | Status | Nota |
|---|---|---|---|---|---|---|
| TR-dados-001 | Valores de gameplay só como dado externo, números escritos como texto e lidos em decimal com cultura invariante; nenhum literal no código | Dados | R1 L38; AC-05/06 | ADR-0002 §1 | 🟡 Covered (Proposed) |  |
| TR-dados-002 | Declaração de knob com dono, tipo, unidade, faixa, padrão, aceite, pior, sentido, remoto, validada por coerência (F6) | Dados | R2 L39; F6 L194; AC-02 | ADR-0002 §2 | 🟡 Covered (Proposed) |  |
| TR-dados-003 | IDs estáveis em snake_case, nunca reutilizados nem removidos, deprecated resolve; índice inteiro pela ordem ordinal | Dados | R3 L40; AC-03 | ADR-0002 §5 | 🟡 Covered (Proposed) |  |
| TR-dados-004 | Resolução de ID para definição fora do tick, com a resposta ID desconhecido para o save e o log | Interface | Edge L238-240; AC-I5 L379 | ADR-0002 §5 | ⚠️ Partial | Tabela de IDs existe, mas nenhuma ADR define a interface de resolução (IDataResolver do #28) |
| TR-dados-005 | Conversão única no build: floor(s*30+0,5) com recusa abaixo de 1 tick; taxa /30 em decimal para float, bits idênticos em todas as plataformas | Determinismo | R4 L41; F1 L108; F2 L124; AC-F1/F2 | ADR-0002 §3; ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-dados-006 | Um único DataValidator, tudo ou nada, sem clamp, seis checagens, relatório com todos os erros | Dados | R5 L42-49; AC-05; AC-16/17 | ADR-0002 §2 | 🟡 Covered (Proposed) |  |
| TR-dados-007 | A carga verifica estrutura e hash; uma falha bloqueia a fase (o catálogo bloqueia todas) e nunca usa valor padrão | Dados | R7 L51; Edge L244; AC-10 | ADR-0002 §2, §8 | 🟡 Covered (Proposed) |  |
| TR-dados-008 | Capacidades por fase (vivos, ids, eventos, pools) contra a demanda com margem e teto por tipo, em int64; compositor soma ids_de_preparacao | Memória | F3 L140-152; AC-F3; AC-I1 | ADR-0002 §4; ADR-0001 | ⚠️ Partial | GDD admite override de margem por capacidade; ADR tem CapacityMarginPct global única |
| TR-dados-009 | Snapshot binário imutável, canônico e little-endian, lido sem reflexão; o jogo e o headless leem o mesmo | Dados | R7 L51; AC-09; AC-I3 | ADR-0002 §4 | 🟡 Covered (Proposed) | AC-09 do GDD exige nenhum tipo T[], o ADR usa arrays privados |
| TR-dados-010 | Carga síncrona (catálogo no boot, fase antes do tick 0), zero I/O e conversão durante a fase, sem Addressables nem Resources | Engine | R7 L51; AC-11 | ADR-0002 §8 | 🟡 Covered (Proposed) |  |
| TR-dados-011 | Orçamento de carga fria e quente e memória do snapshot no aparelho de referência | Performance | Knobs L284-286; AC-P1; OQ-4 | ADR-0002 (Verification Required 3, 8) | ⚠️ Partial | ADR não reivindica orçamento; depende do spike e do aparelho |
| TR-dados-012 | Hash FNV-1a 64 de conteúdo, rótulo e versão efetiva (embarcado + pacote) para o log #5 e Simulation.Create | Interface | R6 L50; AC-07; AC-I2 | ADR-0002 §6 | 🟡 Covered (Proposed) |  |
| TR-dados-013 | Revisão por skill (fecho mais contador), classificação autoral obrigatória, histórico datado, só fatos expostos | Dados | R6 L50; Edge L233-237; AC-07/08 | ADR-0002 §7 | ⚠️ Partial | ADR não define a marcação gameplay/cosmético e não expõe o hash da revisão |
| TR-dados-014 | O pré-build revalida, refaz o bake e falha o build com dado inválido ou knob de aceite remoto; o snapshot fica versionado | Build | Edge L243, L246; AC-12 | ADR-0002 §9 | 🟡 Covered (Proposed) |  |
| TR-dados-015 | Assembly Forja.Data sem engine, sem rede, sem static mutável e sem API de escrita em runtime | Código | R10 L61; AC-15; AC-18 | ADR-0002 §9 | 🟡 Covered (Proposed) |  |
| TR-dados-016 | Análise estática no CI: literais numéricos de gameplay e lista de exceções | Ferramentas | AC-01; OQ-7 L403 | — | ❌ GAP | Nenhuma ADR decide ferramenta nem lista de exceções |
| TR-dados-017 | Contrato do pacote remoto: lista branca, atômico, mesma validação, sem segmentação, base = hash, maior sequência, só entre partidas | Live ops | R9-10 L53-61; AC-13; AC-19 | ADR-0002 §10 | 🟡 Covered (Proposed) |  |
| TR-dados-018 | Persistência atômica da última sobrescrita válida, assinatura, expiração, revalidação no boot, decimal idêntico no aparelho | Persistência/Rede | R9 L59; Edge L223, L226; AC-14 | ADR-0002 §10 (delega ao #29) | ⚠️ Partial | Delegado ao ADR futuro do #29 |
| TR-dados-019 | Histórico de revisão do aparelho (pacote aplicado, trocado, removido, expirado, descartado) persistido e somado ao History | Persistência | R6 L50; Edge L226, L229 | ADR-0002 §10; ADR-0003 | ⚠️ Partial | Delegado ao #29 ou ao save |
| TR-dados-020 | Aplicar o pacote só no hub, sem ritual de selo ou registro aberto (sinal do #17); tela das cartas lê a versão da próxima partida | Interface | R9 L58; AC-14b | ADR-0002 §10 | ⚠️ Partial | Falta a interface do #17 para o #1 |

#### #28 Save local (`design/gdd/save-local.md`)

| TR-ID | Requisito | Domínio | Fonte no GDD | ADR | Status | Nota |
|---|---|---|---|---|---|---|
| TR-save-001 | Um save por aparelho; envelope com fatias opacas versionadas pelo dono; tag e campo desconhecidos passam intactos | Persistência | R1, R4 L37-40; AC-01; AC-28 | ADR-0003 §2 | 🟡 Covered (Proposed) |  |
| TR-save-002 | O save guarda só IDs, carimbo da versão dos dados, revisão e data do selo, saveSequence e maxSeenUtc; nunca valores nem posses | Estado | R2-3 L38-39 | ADR-0003 §2 | 🟡 Covered (Proposed) |  |
| TR-save-003 | Cabeçalho fixo com checksum próprio, lido antes do corpo; cabeçalho inválido é corrupção; FNV-1a 64 no corpo | Persistência | R9 L45; AC-06 | ADR-0003 §2 | 🟡 Covered (Proposed) | ADR ainda cita CRC do cabeçalho em L80 |
| TR-save-004 | Commit atômico: temporário, releitura, rotação verificada do backup, troca do principal, fsync do diretório antes de Confirmado | Persistência | R7-8 L43-44; F4; AC-05, AC-10, AC-14, AC-26/27 | ADR-0003 §3, §4 | 🟡 Covered (Proposed) | Troca atômica no Android é gate G2 de aceitação (spike) |
| TR-save-005 | Estados de abertura (8), precedência por saveSequence, quarentena e pendente de decisão, leitura incerta com até 3 tentativas | Persistência | Estados L54-67; R14 L50; AC-15, AC-20, AC-29 | ADR-0003 §1 | 🟡 Covered (Proposed) |  |
| TR-save-006 | Versão do formato inteira; migração só estrutural, numa cópia em memória; formato mais novo e migração falhou abrem só leitura | Persistência | R9 L45; AC-06; AC-15c/f/g | ADR-0003 §2 | 🟡 Covered (Proposed) |  |
| TR-save-007 | Retrato montado na thread principal no orçamento F3; gravador único em thread própria; fila de capacidade 1 com substituição | Threading | R5 L41; F2, F3; AC-12, AC-13, AC-16 | ADR-0003 §5 | 🟡 Covered (Proposed) |  |
| TR-save-008 | Pontos seguros, flag de sujo, nunca grava na fase nem no tick; pausa por OnApplicationPause com flush e teto | Ciclo de vida | R5 L41; AC-02, AC-03 | ADR-0003 §6, §8 | 🟡 Covered (Proposed) |  |
| TR-save-009 | Marca de fase em andamento: BeginStage só retorna com resultado real; attemptId de 128 bits de fonte injetada; payload opaco; CancelStage | Interface #3 | R6 L42; AC-04a-c | ADR-0003 §3, Key Interfaces | 🟡 Covered (Proposed) |  |
| TR-save-010 | Avisar o #3 de marca encontrada e gravar o efeito do #3 no commit de consumo; restaurada consumida na restauração | Interface #3 | R6 L42; AC-04a; AC-08; AC-22/23 | ADR-0003 (ConsumeMark) | ⚠️ Partial | OnMarkFound não está nas Key Interfaces; MarkAnswer indefinido |
| TR-save-011 | Resultado real Pendente, Confirmado ou Falhou com causa tipada, sem tempo esgotado; selo idempotente; recusa em só leitura | Interface #17 | R12 L48; AC-21; AC-06 | ADR-0003 (CommitOutcome) | ⚠️ Partial | FailureCause é int sem enum; ReadOnlyRejected e idempotência do selo ausentes |
| TR-save-012 | Relógio injetável; hora efetiva monotônica na faixa de sanidade sobre BUILD_UTC; o avanço viaja no próximo commit | Tempo | R11 L47; F1; AC-11, AC-24/25 | ADR-0003 §8 | 🟡 Covered (Proposed) |  |
| TR-save-013 | Android: raiz interna por JNI getFilesDir(); Auto Backup só do save.dat; marcador em noBackupFilesDir para detectar restauração | Plataforma | Vira ADR L82; Edge L162 | ADR-0003 §1, §7 | 🟡 Covered (Proposed) | Revisão de engine: XMLs de backup em Plugins/Android/res são recusados; GameActivity a conferir |
| TR-save-014 | Armazenamento injetável com injeção de falha; o mesmo teste roda contra o fake e contra o adaptador real | Testabilidade | AC preâmbulo L246; AC-31 | ADR-0003 §10 | 🟡 Covered (Proposed) |  |
| TR-save-015 | Serialização à mão, sem reflexão; serviço injetado sem static mutável; ciclo de vida da thread (quitting, Play Mode) | Engine | Vira ADR L82 | ADR-0003 §9, §5 | 🟡 Covered (Proposed) | Revisão de engine: falta IsBackground, join no reload e -= de eventos estáticos |
| TR-save-016 | Interface de eventos para o #5 com sink nulo e buffer no boot, com a lista de eventos fixada | Interface | Interações #5 L74; AC-30 | ADR-0003 (ISaveEventSink) | 🟡 Covered (Proposed) |  |
| TR-save-017 | Pedidos de mensagem ao jogador (7 tipos), uma por vez por gravidade, consumidos no commit; indicador persistente | UI | UI Requirements L217-227; AC-19a/b | — | ❌ GAP | Nenhuma ADR define o canal do #28 para a UI nem a fila de avisos |
| TR-save-018 | Tratar ID desconhecido do #1: preservar o registro, slot indisponível; revisão do selo comparável ao histórico | Interface #1 | R10 L46; AC-07; AC-32 | ADR-0003; ADR-0002 | ⚠️ Partial | Sem IDataResolver; IDataVersion indexada por índice e o save guarda ID |
| TR-save-019 | Exportar e importar o retrato inteiro; detectar regressão por saveSequence e hash de conteúdo; só o #29 reduz maxSeenUtc | Persistência/Nuvem | Interações #29 L80; R11 L47; AC-17/18 | ADR-0003 | ⚠️ Partial | Delegado ao #29; sem API de exportação nem hash de conteúdo do save |

#### #6 Combate e dano (`design/gdd/combate-e-dano.md`)

| TR-ID | Requisito | Domínio | Fonte no GDD | ADR | Status | Nota |
|---|---|---|---|---|---|---|
| TR-combate-001 | Colunas hasheadas do #6 no SimWorld: hpMax, estadoCombate, timerTicks, iframes, contactCd, kbVel, intentVel, classe, arquetipoId, tickNascimento, aberto, punidoPesado, esquivaBuf, curaPendente, ultimoContatoTick, área travada do telegraph, prontoDesde, índice do ciclo do chefe, proximoHitStopTick, ultimaDirecao, poise, kb_refrat; escalares modDano e modCadencia do #8 | Core/Estado | L103, L426; OQ-1 | — | ❌ GAP | Nenhum ADR do #6; ADR-0001 L82 manda o estado extra ficar no sistema, mas as colunas são lidas pelo #7 e pelo #12 |
| TR-combate-002 | O #6 é o único escritor de posição e HP; o #7 só faz Spawn, o #8 só enfileira; um espião por sistema verifica | Core/Estado | L46; AC-R1 | ADR-0001 | ⚠️ Partial | Escritor único de posição e HP só está fixado para a ficha e o `CombatHold` |
| TR-combate-003 | Ordem fixa no tick #7, #8, #6, #3; dentro do #6 os passos 1 a 8 têm ordem fixa | Core/Sim | L46-55; AC-I2 | ADR-0001 | ⚠️ Partial | O ADR fixa o compositor, não a ordem concreta #7, #8, #6, #3 |
| TR-combate-004 | O #6 só age com CombatActive, conta todo tempo em CombatTick e as contagens regressivas congelam exatas; a oferta de carta abre na hora e o #16 é dono da contagem 3-2-1 sob CombatHold, sem predicado do #6 | Core/Tempo | L48, L70; AC-R16, E3 | ADR-0001 (Emenda 5) | 🟡 Covered (Proposed) |  |
| TR-combate-005 | Ponto único Combate.Aplicar/Curar com fila entre sistemas, pedido Rugido tipado na frente da fila e sem F1, cura do #3 via curaPendente (sobrevive ao CombatHold), resolução 7a/7b, scratch fora do hash, cap_fila com teto_vivos_horda + 1, estouro vira Quebrada | Core/Comunicação | L54-57, L69; F2, E1 | — | ❌ GAP | Canal entre sistemas (fila `Aplicar`/`Curar`, `curaPendente`, `modDano`/`modCadencia`) sem ADR; ADR-0001 L84 e L267 só preveem comunicação pelo `SimWorld` |
| TR-combate-006 | Morte só por Kill(id, causa) em 7b; herói e chefe podem morrer no mesmo tick; a causa identifica o golpe ou a fonte | Core/Estado | L57, L65; F2 L147 | ADR-0001 (Emendas 6 e 15) | ⚠️ Partial | A causa por golpe (F2, entrada k) não chega ao `Kill`; `DeathRecord` só tem o enum |
| TR-combate-007 | Eventos individuais só para herói, elite e chefe; a horda sai agregada por tick {mortes, acertos, danoTotal}; mortes por Rugido somam em mortes, acertos e danoTotal contam só pedidos com valor | Eventos | L68, L419; AC-R14 | ADR-0001 | ⚠️ Partial | `Kill` emite `Death` por entidade; `SimEvent` tem um único `Value` |
| TR-combate-008 | Contadores de diagnóstico fora do hash (GolpesDescartados, GolpesLimitados, ModForaDeFaixa, CurasDescartadas) que lançam no modo estrito | Diagnóstico | L351-362; E7 | ADR-0001 (Emenda 9) | ⚠️ Partial | Contadores do #6 fora da Emenda 9; `SimContext` sem modo estrito nem contador |
| TR-combate-009 | float32 na ordem escrita, sem FMA, SimMath, HP_RESIDUO contra resíduo de float, conversão float para int controlada | Numérico | L107; F2, F4 | ADR-0001 | 🟡 Covered (Proposed) | F4 ainda usa cast direto `(int)(x+0,5f)` (GDD L107, L195) contra ADR-0001 L287 |
| TR-combate-010 | Tipo vetorial próprio e geometria determinística: círculo, cone, segmento da linha (P0→P1 limitado na trava), clampArena AABB por eixo, EIXOS8[id mod 8] para vetor nulo do knockback, dir (1,0) se d² < 1e-6, sem trigonometria | Numérico | L60, L63; F3 | — | ❌ GAP | ADR-0001 L62 adia o `SimVec2` para o ADR do #6 |
| TR-combate-011 | Consulta espacial por tick com 300+ vivos: alvo mais próximo, contato, acerto do telegraph e áreas do #8; sem bloqueio de corpo | Desempenho | R4-R5; OQ-7 | — | ❌ GAP | Estrutura de consulta espacial não decidida |
| TR-combate-012 | Orçamento do Tick do #6: p95 ≤ 2,0 ms e p99 ≤ 4,0 ms com 300+ vivos e 3 avisos, no aparelho de referência; pior tick (300 mortes + 3 avisos) com máximo ≤ orcamento_combate_pior_tick_ms (valor ainda não definido) | Desempenho | L527; AC-P1 | — | ❌ GAP | ADR-0001 L433 não fixa orçamento por sistema |
| TR-combate-013 | Zero alocação gerenciada por tick, arrays pré-alocados, 300 mortes num tick | Memória | AC-P2 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-combate-014 | Laços por id crescente, empate pelo menor id, sem RNG, Hash do #6 com escopo definido; proibições verificadas por BannedApiAnalyzers | Determinismo | L424-426; AC-D3, AC-D4 | ADR-0001 | 🟡 Covered (Proposed) | Analisador estático não está no ADR |
| TR-combate-015 | Durações em ticks inteiros; segundos e taxas convertidos uma vez no build; validações F5-F10 em decimal pelo #1 | Dados | L483; F5 | ADR-0002 §3 | 🟡 Covered (Proposed) |  |
| TR-combate-016 | AvisoPerto como sinal somente leitura do #6 para o #16, que segura a oferta | Core/Comunicação | removido do GDD | — | ⛔ Superseded | `AvisoPerto` e F11 removidos; Regra 16 reescrita (oferta na hora, contagem 3-2-1 do #16); ver TR-combate-004 |
| TR-combate-017 | Hit-stop, flash, dissolve e cauda são só apresentação; a simulação nunca congela e a apresentação lê colunas e eventos | Presentation | L64; F8 | ADR-0001 (Tempo) | 🟡 Covered (Proposed) |  |
| TR-combate-018 | Efeitos por shader com propriedade por instância, pools de cartões e fantasmas, overdraw <= 2,5x, decal de telegraph, cortes por prioridade | Render | L565, L575, L585 | — | ❌ GAP | Sem ADR de render |
| TR-combate-019 | Háptico no Android e tremor de câmera como knobs de acessibilidade | Plataforma | L606, L609; OQ-6 | — | ❌ GAP | API de vibração do Android NOT SOURCEABLE; sem ADR |
| TR-combate-020 | StateHash do tick 900 igual entre o Editor e o aparelho IL2CPP ARM64 | Determinismo | AC-D5 L723 | ADR-0001 | ⚠️ Partial | Conflito: ADR-0001 L391 e L450 só prometem o mesmo build e o mesmo runtime; reescrever o AC-D5 ou emendar o ADR |
| TR-combate-021 | Capacidade de eventos ≥ Reservados + 5 + 3×individuais + 4; DeathsThisTick com a capacidade de entidades, sem descarte | Capacidade | L419-421, L526 | ADR-0001 (Emenda 10), ADR-0002 | ⚠️ Partial | Capacidade de `DeathsThisTick` não fixada; risco de ADR-0001 L407 pendente. Novo nesta passada |
| TR-combate-022 | O #6 expõe visões somente leitura: área travada do telegraph (fase, ticks_ate_dano, forma, raio, origem e destino), ultimoDanoTick, pesado, iframes, dash, cadência, HP e hpMax; posição, arquétipo e tick da horda morta legíveis 1 tick após a morte | Presentation | L68, L587; AC-I12 | ADR-0001 | ⚠️ Partial | Nomes e tipos das visões somente leitura não definidos. Novo nesta passada |
| TR-combate-023 | Spawn grava classe, arquetipoId e tickNascimento; a entidade nascida no CombatTick corrente não age no #6 | Core/Estado | L61, L367; AC-R7 | ADR-0001 (Emenda 6) | ⚠️ Partial | `Spawn` (ADR-0001 L192) não recebe classe, arquétipo nem tick de nascimento; ids novos agem a partir do sistema seguinte (L99). Novo nesta passada |

#### #7 Horda, waves e inimigos (`design/gdd/horda-waves-e-inimigos.md`)

| TR-ID | Requisito | Domínio | Fonte no GDD | ADR | Status | Nota |
|---|---|---|---|---|---|---|
| TR-horda-001 | O #7 é o 1º ISimSystem (#7, #8, #6, #3, #16), só faz Spawn e declara dados; depois do nascimento não escreve posição nem HP | Core/Sim | R1 L52; AC-R1, I2 | ADR-0001 | ⚠️ Partial | Ordem concreta do compositor e escritor único de posição e HP não decididos |
| TR-horda-002 | Composição inteira no Preparar via world.RngWave(w), sorteio sem viés; 0 sorteios por tick | Determinismo | R6 L92; F3 L233-246; D1, D7 | ADR-0001 (Emendas 11, 14 e 16) | 🟡 Covered (Proposed) | Era ⚠️: a Emenda 16 fechou o RNG no `Preparar` |
| TR-horda-003 | Tabela (chave long, sem comparador genérico sobre struct), janelas por elite e scratch da F4 pré-alocados; fora do hash; só cursores hasheados; zero alocação por tick | Memória | R6, R8 L104, R9, R13; P2, P3 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-horda-004 | Posição de nascimento como função pura: direções SimVec2 literais, espelho por eixo, dist², sem sin/cos nem raiz | Numérico | R7 L94-99; F4 L253-271 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-horda-005 | Geometria da arena AABB [0,L]x[0,A] e tipo vetorial compartilhados com o clampArena do #6 | Numérico | R2 L54; F4, F5 | — | ❌ GAP | `SimVec2` é "definido pelo ADR de #6" (ADR-0001 L62), que não existe |
| TR-horda-006 | vivos_horda e 'há elite vivo' por uma passada local O(n≤303) sobre Alive; nenhum contador no SimWorld | Estado | R8 L104; P3 L796 | ADR-0001 (`Alive`) | ⚠️ Partial | Era ❌: o GDD trocou o contador por uma passada local. Depende da coluna `classe` (TR-horda-007) |
| TR-horda-007 | Colunas classe, arquetipoId e tickNascimento escritas no Spawn; a escolta lê o estado de ataque do #6 do tick anterior | Estado | L169-172, L186; R11; I12 | ADR-0001 | ⚠️ Partial | `Spawn` (ADR-0001 L192) não recebe as colunas; leitura do estado de outro sistema não decidida |
| TR-horda-008 | Capacidades vêm dos dados: total_spawns_7 (FS9) e pico_vivos_7 (F3); Spawn -1 faz o cursor avançar, ou lança no modo estrito | Dados | R14; F7, F8; L501 | ADR-0001 (Emenda 6), ADR-0002 | 🟡 Covered (Proposed) |  |
| TR-horda-009 | Chefe Essencial: único, nunca espera; Spawn rejeitado encerra com EssentialSpawnRejected; reservar um id para o essencial? | Estado | R10.1 L110; OQ-3 | ADR-0001 (Emendas 6 e 7) | ⚠️ Partial | OQ-3 aberta: reservar o id do chefe? |
| TR-horda-010 | Rugido: pedido tipado, sem dano, na frente da fila Combate.Aplicar; Kill com causa Rugido, a primeira causa vence; cap_fila ≥ teto_vivos_horda + 1 | Comunicação | R10.2 L111; L471; R10, I6 | ADR-0001 (Emenda 15) | ⚠️ Partial | Era ❌: a Emenda 15 trouxe `DeathCause.Rugido`. Falta o contrato da fila `Combate.Aplicar` (ADR-0001 L84, L267) |
| TR-horda-011 | Movimento cinemático em C# puro: linha reta, sem NavMesh nem física, mira por id mod 32, encaixe no alvo sem normalizar | IA | L133; RB, RB2 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-horda-012 | Separação entre inimigos e bloqueio de corpo (grade uniforme O(n)) adiados ao spike de performance | Desempenho | L133; OQ-9, OQ-16 | — | ❌ GAP | Nenhuma estrutura espacial |
| TR-horda-013 | Orçamento do passo do #7: p95 0,3 ms e p99 0,5 ms com 300 vivos e 200 pendentes, no tick do rugido, na escolta e com 20 nascimentos/tick sustentados; marker Horda.Tick | Desempenho | L579; P1 L794 | — | ❌ GAP | ADR-0001 L433 não fixa orçamento por sistema |
| TR-horda-014 | Render de multidão: <= 400 triângulos, 1 LOD, 1 draw por tipo, dados por instância, zero efeito ou som por corpo, pool de ~300 fantasmas | Render | L640-658 | — | ❌ GAP | Sem ADR de render |
| TR-horda-015 | Pré-aquecer no Preparar os assets do chefe (modelo, shader, LUT por Volume, disco) para o tick do rugido caber no frame | Render/Carga | L182, L530; P4 L797 | — | ❌ GAP | Sem ADR de carga |
| TR-horda-016 | Evento Rugido (mesmo com 0 corpos); nenhum evento por corpo nascido | Eventos | L111, L469, L634 | ADR-0001 | ⚠️ Partial | `SimEventKind` não tem `Rugido`; `Spawn` no tick parece emitir evento (ADR-0001 L154) |
| TR-horda-017 | Diagnósticos do #7 (HordaEsperouTicks, EliteEsperouTicks, HordaCancelada, ElitesCancelados, TicksNoTeto, VivosHordaNoElite, TicksNoCanto) fora do hash, enviados ao log do #5 | Diagnóstico | R13 L119-126 | ADR-0001 | ⚠️ Partial | Sem canal de diagnóstico do sistema até o log |
| TR-horda-018 | Cronograma e arquétipos na seção de fase do snapshot: w explícito, ordem (inicio, w), instante 0 válido, checagens F2/F5/F10 em decimal | Dados | R4 L76-88; F1; F10 | ADR-0002 §4 | ⚠️ Partial | ADR-0002 L86 diz "por índice de wave"; o GDD ordena por (`inicio`, `w`); falta regra de instante |
| TR-horda-019 | Congela sem CombatActive; corpos vencem no mesmo CombatTick depois da oferta, sem lote na retomada | Tempo | R1; L436-441; E1, E2 | ADR-0001 (Emenda 5) | 🟡 Covered (Proposed) |  |
| TR-horda-020 | Mesmo build IL2CPP ARM64: tabela e hash iguais; golden por plataforma | Determinismo | D6 L789 | ADR-0001 L64, L450 | 🟡 Covered (Proposed) | Era ⚠️: o GDD deixou de exigir Editor × aparelho |
| TR-horda-021 | Id de classe de vetor pré-calculado em decimal no build; frentes comparadas por inteiro, nunca por float | Dados | R7.4 L98; F4 L254, L266 | ADR-0002 | 🟡 Covered (Proposed) | Novo nesta passada |
| TR-horda-022 | Tick do rugido: até teto_vivos_horda + 1 mortes mais o evento Rugido sem DroppedEvents | Eventos | L657, L686; P1(b) | ADR-0001 L407 | ⚠️ Partial | `EventCapacity` ou reserva para o `Rugido` não declaradas. Novo nesta passada |
