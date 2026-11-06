## Architecture Review Report
Date: 2026-11-06
Mode: full
Workflow: full
Engine: Unity 6.3 LTS (6000.3.27f1)
GDDs Reviewed: 6 (de 8 arquivos em design/gdd/; game-concept.md e systems-index.md não são GDDs de sistema)
ADRs Reviewed: 9

Reviewed-Content-Hash: docs/architecture/adr-0001-simulacao-deterministica-float32-tick-30hz.md 0501f025c4bab398dee4338b0cdb2738cc1c888b
Reviewed-Content-Hash: docs/architecture/adr-0002-dados-e-balanceamento-snapshot-imutavel-gerado-no-build.md 9f40c08f9c59a92d0cebc7a8570192582f48066f
Reviewed-Content-Hash: docs/architecture/adr-0003-save-local-envelope-tlv-commit-atomico-gravador-unico.md b2b8e643afcb53e743598ece049e82c46d85c010
Reviewed-Content-Hash: docs/architecture/adr-0004-colunas-do-simworld-combate-e-horda.md 83f42c8de7d228061bc562bb3d892622c211dce5
Reviewed-Content-Hash: docs/architecture/adr-0005-pipeline-de-dano-e-eventos-de-combate.md 25c3b5d7348f5006c1581e8e6184189d8bd3ad64
Reviewed-Content-Hash: docs/architecture/adr-0006-vetor-geometria-e-consulta-espacial-deterministicos.md e9bdc151c4cc6e2c0e204fd2311394eddaa06a00
Reviewed-Content-Hash: docs/architecture/adr-0007-ponte-de-entrada-tempo-e-ciclo-de-vida-do-app.md fb2f6a3e8688f8f112ea14433c90786a27ab5f60
Reviewed-Content-Hash: docs/architecture/adr-0008-log-de-eventos-e-instrumentacao-do-5.md b37e0bd32a52b18f05d3563f640f58cefe0bf447
Reviewed-Content-Hash: docs/architecture/adr-0009-render-de-multidao-e-vfx-em-mobile.md e8e16a4dfee59761471c3712b408f1d6fa815831
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

> **4ª passada (a segunda de 2026-11-06).** Substitui, como estado vigente, a 3ª passada de hoje (`architecture-review-2026-11-06.md`: CONCERNS; 125 requisitos: 73 🟡, 41 ⚠️, 11 ❌), que fica como histórico. Motivo: entraram os ADR-0007 (ponte de entrada, tempo e ciclo de vida do app), ADR-0008 (log de eventos do #5) e ADR-0009 (render de multidão e VFX em mobile), todos `Proposed`. O ADR-0001 a 0006, os GDDs, o `tr-registry.yaml` e as referências de engine não mudaram (o recibo mostra só 0007, 0008 e 0009 como `NEW`).

### Traceability Summary
Total requirements: 125 ativos (mais 1 superseded: TR-combate-016)
✅ Covered (ADR Accepted): 0
🟡 Covered (ADR Proposed): 79
⚠️ Partial: 40
❌ Gaps: 6

Os 9 ADRs estão `Proposed`; a cobertura é, portanto, 🟡 e limita o veredito a CONCERNS no máximo. A rota é `/architecture-decision accept ADR-NNNN`.

| GDD | Ativos | 🟡 | ⚠️ | ❌ | Mudança desde a 3ª passada |
|---|---|---|---|---|---|
| #2 Simulação | 22 | 14 | 7 | 1 | `simulacao-015`: ❌ para 🟡; `016`: ⚠️ para 🟡 |
| #3 Fluxo de fase | 20 | 14 | 6 | 0 | `fluxo-016`: ❌ para 🟡; `010` e `014`: ⚠️ para 🟡 |
| #1 Dados | 20 | 12 | 7 | 1 | Nenhuma |
| #28 Save | 19 | 14 | 4 | 1 | Nenhuma |
| #6 Combate | 22 | 10 | 10 | 2 | `combate-018`: ❌ para ⚠️ |
| #7 Horda | 22 | 15 | 6 | 1 | `horda-014`: ❌ para 🟡; `horda-015`: ❌ para ⚠️ |

Total: 73 → 79 🟡, 41 → 40 ⚠️, 11 → 6 ❌. Nenhum ID novo, nenhum texto de requisito alterado; `tr-registry.yaml` não foi tocado.

**Critério nas linhas que mudaram.** `combate-018` fica ⚠️: o flash por corpo da horda fica desligado sem a emenda `UltimoDanoTick` no ADR-0004 (que muda o golden hash do #6), o caminho primário de dados por instância tem um HIGH de engine (ver abaixo) e overdraw e draws só se medem no spike. `horda-015` fica ⚠️: o GDD #7 (L182, L530, L796) manda pré-aquecer no `Preparar` e o ADR-0009 faz antes do `Create`; a lista de assets "vem do snapshot" sem campo no ADR-0002; o desenho "fora da tela" é descartado pelo culling. `simulacao-016`, `fluxo-014` e `fluxo-010` sobem para 🟡, com a ressalva de que o ADR-0003 L186 ainda contradiz o texto até a Emenda ao ADR-0003. Seguem ⚠️ de propósito: `simulacao-017` (tag do build e ABI NOT SOURCEABLE; a comparação aparelho × headless fica indisponível), `horda-017` (colisão de ids de contador, conflito 3) e `simulacao-018` (orçamentos não reivindicados). A regradação das 8 linhas é de quem rodou a passada; as outras 117 não foram reconferidas.

### Coverage Gaps (no ADR exists)
6 requisitos, listados em `requirements-traceability.md` (Known Gaps).

| TR | Requisito | ADR sugerida | Domínio | Risco de engine |
|---|---|---|---|---|
| simulacao-020 | Validação entre aparelhos exige ponto fixo | Simulação em ponto fixo (Alpha) | Core/Rede | MEDIUM |
| dados-016 | Análise estática de literais de gameplay no CI | Análise estática e CI | Ferramentas | MEDIUM |
| save-017 | Avisos do save para a UI | Avisos do save para a UI | UI | LOW |
| combate-012 | Orçamento do Tick do #6 (p95 ≤ 2,0 ms, p99 ≤ 4,0 ms) | Orçamento de frame (após o spike) | Desempenho | MEDIUM |
| horda-013 | Orçamento do passo do #7 (p95 0,3 ms, p99 0,5 ms) | Orçamento de frame (após o spike) | Desempenho | MEDIUM |
| combate-019 | Háptico e tremor | Feedback de plataforma | Plataforma | HIGH (API NOT SOURCEABLE) |

`combate-012` e `horda-013` são de camada Core; os ADR-0004 a 0006 os deixam para o spike de propósito. Isso entra no veredito.

### Cross-ADR Conflicts
Áreas propensas a conflito (`docs/consistency-failures.md`, 16 entradas): a fronteira #2 × #6 × #7 e regras gerais que esquecem casos especiais. Os três ADRs novos tocam outra fronteira, a de ciclo de vida do host (ponte, log, apresentação), onde o padrão se repete: cada ADR pede emenda a um vizinho em vez de definir um ponto de extensão.

**Nenhum conflito bloqueante (🔴).** Implementar os nove ADRs como escritos não quebra a integração. Catorze itens 🟠 (lacuna de dono ou de clareza), achados por um agente de leitura. **Conferidos diretamente no texto:** 4, 5, 6, 10, 11 e 14, e a premissa do 7 (ADR-0007 L118). Os demais vêm só do agente.

1. **Ciclos de dependência.** ADR-0008 L34 e ADR-0009 L34 dependem do 0007, e cada um pede ao 0007 (Ordering Note, item B) que chame tipos que eles mesmos definem (`PhaseLog.FlushSession/FlushPending`, ADR-0008 L180-181; `IPresentationSink`, ADR-0009 L146). Aplicadas as emendas, o 0007 passa a depender do 0008 e do 0009: dois ciclos. O conteúdo das três emendas ao 0007 combina (decisões 5 e 6, e a ordem do frame já drena depois de cada Tick, L124-125). Opção: o 0007 define ganchos neutros em `Sim.Host` (observador de tick e de pausa do app), implementados pelo log e pela apresentação.
2. **`FlushSession` no objeto errado.** Está em `IPhaseLog` (ADR-0008 L181) mas é chamado "fora de fase" (L37, L131), quando não existe `PhaseLog` (só é aberto na tela de carregamento, L95). Opção: mover para o `LogHost` ou para a interface do log de sessão.
3. **Ids de contador sem fonte.** O registro `Counters` é uma lista de `(CounterId u16, Value, Available)` sem campo de fonte (ADR-0008 L84); o ADR-0009 numera os dele a partir de `GhostPoolOverflow = 1` (L118) e vai colidir com os do #7 e do Core. Opção: `Source u8` por registro, ou faixas globais.
4. **Dois enums de status de commit.** ADR-0008 L164 `CommitStatus { NotRequested 0, Confirmed 1, Failed 2, Pending 3 }`; ADR-0003 L137 `CommitOutcome { Pending 0, Confirmed 1, Failed 2 }`. Um cast direto troca `Pending` por `NotRequested`. Opção: função de mapeamento explícita, com teste. *(Conferido.)*
5. **Lote do último tick pode sair duplicado.** O host drena depois de cada Tick, inclusive o que termina em `Ended`, e manda ao log (ADR-0007 L124-125); a sequência de fim do ADR-0008 drena de novo e chama `WriteBatch` (L100). O ADR-0001 L262 diz que `DrainEvents` "devolve os eventos do último Tick" e não diz que a 2ª chamada vem vazia; lido ao pé da letra, o último lote é gravado duas vezes e quebra o "`Tick` crescente" (AC I5). Opção: o passo 1 do ADR-0008 roda só quando o host não drenou, ou o ADR-0001 fixa que a 2ª chamada devolve vazio. *(Conferido.)*
6. **Hash final no abandono.** ADR-0008 L122 põe o abandono entre os casos de `FinalHashAvailable = 0`, mas L101 calcula o `StateHash` (só `Broken` fica indisponível) e o ADR-0001 L95 só lança em `Broken` e `Destroyed`. Opção: escolher um comportamento e corrigir o outro texto. *(Conferido.)*
7. **`PhaseHost` pode nunca rodar um tick.** ADR-0007 L118 sai se `Status != Running`; o ADR-0001 L95 define os estados mas, até onde foi lido, não diz quem passa de `Created` para `Running` nem quando. Opção: o ADR-0001 fixa que o compositor passa a `Running` depois do `Preparar`, ou o 0007 aceita `Created`. *(Só a premissa conferida.)*
8. **Último frame da fase.** O `Ended` leva a *Concluindo* dentro do `Update` (ADR-0007 L126); o fim faz `Concluir` e `Discard` (ADR-0008 L103) e o 0007 L65 destrói o `PhaseHost` no `Discard`; o ADR-0009 L71 lê os spans no `LateUpdate`. Nada diz se o `Discard` vem antes desse `LateUpdate`. Opção: `Discard` no frame seguinte, ou a apresentação só lê com `Running`.
9. **`DroppedTicks` não chega ao log.** ADR-0007 L35 e L212 dizem "lido pelo log (#5)"; o ADR-0008 não o cita nem o inclui nos contadores do Core (L84). Opção: o `PhaseHost` vira fonte de contador.
10. **`IsAlive` não é um span.** O ADR-0009 (L34, L71) lê `IsAlive` como coluna; o ADR-0001 tem o método `IsAlive(int id)` (L203) e o span `Alive` com os vivos (L209). Opção: usar o método ou o span `Alive`. *(Conferido.)*
11. **Dependência oculta 0009 → 0002.** ADR-0009 L34 diz "ADR-0002: nenhuma dependência", mas a lista de assets do pré-aquecimento "vem do snapshot da fase" (L184) e o `worldBounds` é a "área jogável da fase" (L85); o snapshot do ADR-0002 só tem dados, sem referência de asset. Opção: declarar a dependência e criar o campo, ou tirar a lista dos dados do #12. *(Conferido.)*
12. **Camada e asmdef.** O ADR-0001 L76-78 põe a ponte em `Forja.Gameplay`; o 0007 e o 0008 se declaram Core (L24) e ficam em `Forja.Gameplay.Sim` (0007 L66, 0008 L69). Não viola "No Engine References" (C# puro; `ThreadPool` é BCL), mas o `Sim.Log` usa `ISaveStorage`, `ISaveClock`, `ISaveEventSink`, `CommitResult` e `AttemptId` de `Forja.Save`, o que exige uma referência que nenhum dos três ADRs declara. Opção: emendar o ADR-0001 L78 e declarar as referências, ou um asmdef próprio (sem engine) para o host e o log.
13. **Desempenho e memória.** O "teto de 16 eventos por tick" do ADR-0008 L301 não existe em outro ADR; pelo ADR-0005 L121 a `EventCapacity` tem o termo `R` (8 a 16, ADR-0001 L103) e pode passar de 16, então o pior arquivo passa dos ~3 MB estimados e o gatilho da Verification Required 7 fica mal calibrado. Somam-se ~2 MiB + 64 KiB fixos desde o boot (L128, L268) sem orçamento para comparar (`phase_snapshot_memory_kb` sem valor, ADR-0002 L290; o art bible só limita textura).
14. **ADR-0003 × ADR-0007/0008.** A L186 diz "**must never** usar `Focus`" e o 0007 L109 pausa no foco perdido; a L116 mostra que a regra é sobre gravar, então a contradição é de texto e a Emenda ao ADR-0003 que os dois pedem a fecha. O ADR-0003 não proíbe dois chamadores do `ISaveStorage`, mas com o gravador único (L113) e a injeção de falha do armazenamento em memória (L128), os testes ficam não determinísticos com duas threads. O `Emit` não diz em que thread roda (L158): lacuna, não contradição. *(Conferido: L186.)*

**Texto desatualizado nos ADRs novos (⚪, sem efeito de contrato):** ADR-0009 L47 atribui ao 0007 o "sink depois de cada tick" (é a emenda pedida); ADR-0007 L34 escreve `PhaseSheet.IdDoHeroi` onde o struct usa `HeroId` (ADR-0001 L193); ADR-0009 L101 diz que o corte "vira fade" e L89/L161 adiam o fade; ADR-0008 L114 usa nomes de enum em português e o código (L164) em inglês; ADR-0007 L136 `Command[4]` "um por `CommandKind`" contra o ADR-0001 L141 (o #9 vai acrescentar tipos).

**Conferido sem conflito:** os 21 bytes por evento do ADR-0008 são a codificação no arquivo (`Kind u8` + 5×4 B, com o `Tick` no cabeçalho do lote); o `SimEvent` em memória segue com 28 B. Os valores de `SimEventKind`, `DeathsThisTick`, `DrainEvents`, `SimStatus` e `StateHash` batem com o ADR-0001 e o ADR-0005. `PrewarmIncomplete = 8` é o próximo valor livre de `NoteKind`. `UltimoDanoTick` é coerente com o ADR-0004 (coluna privada nova; a mudança é expô-la na vista, e o hash do #6 muda). As colunas `PosX/PosY/PrevPosX/PrevPosY`, `Classes`, `ArchetypeIds` e `BirthCombatTicks` existem no ADR-0004 (L159-165).

**Efeito sobre os conflitos da 3ª passada.** Pioram: o nº 8 (memória, +~2,1 MiB fixos), o nº 7 (`EventCapacity`: o "16 por tick" é uma terceira leitura) e o nº 3 (dependência oculta: o padrão se repete em 0009 → 0002). Persistentes que pioram: `AttemptId` entre asmdefs (o `Sim.Log` inteiro precisa de `Forja.Save`), FNV-1a (o checksum do log, ADR-0008 L79, é um 4º uso e não cita o `Fnv1a64` de `Forja.Data`), orçamento da tela de carregamento (entram até 3000 ms de pré-aquecimento, ADR-0009 L113, e a codificação do cabeçalho, ADR-0008 L90, ainda sem dono) e `IPhaseSnapshot` × tipo concreto (reforçado pelo ADR-0009 L184). Sem efeito sobre os demais. Os nove 🟠 da 3ª passada continuam abertos; nenhum ADR novo os resolve.

### ADR Dependency Order
Script `adr-dep-graph.sh`: 9 ADRs, 31 arestas, sem ciclo, sem `NO_DEPS_SECTION` nem `UNFILLED_DEPS`.

```
Foundation (sem dependências):
  1. ADR-0001: Simulação determinística float32, tick 30 Hz        [Proposed]
Depende de Foundation:
  2. ADR-0002: Dados e balanceamento, snapshot imutável             [Proposed] (requer ADR-0001)
  3. ADR-0003: Save local, envelope TLV, commit atômico             [Proposed] (requer ADR-0001, ADR-0002)
  4. ADR-0004: Colunas do SimWorld, combate e horda                 [Proposed] (requer ADR-0001, ADR-0002)
Camada seguinte:
  5. ADR-0005: Pipeline de dano e eventos de combate                [Proposed] (requer ADR-0001, ADR-0002, ADR-0004)
  6. ADR-0006: Vetor, geometria e consulta espacial                 [Proposed] (requer ADR-0001, ADR-0004)
Host, log e apresentação:
  7. ADR-0007: Ponte de entrada, tempo e ciclo de vida do app       [Proposed] (requer ADR-0001, ADR-0003)
  8. ADR-0008: Log de eventos e instrumentação do #5                [Proposed] (requer ADR-0001, 0002, 0003, 0005, 0007)
  9. ADR-0009: Render de multidão e VFX em mobile                   [Proposed] (requer ADR-0001, 0004, 0005, 0007, 0008; e, sem declarar, 0002)
```

**O script conta arestas que não existem.** Ele lê todo `ADR-NNNN` da linha `Depends On`, inclusive em "nenhuma dependência" (confirmado pelo ADR-0007, que diz não depender do 0002, 0004, 0005 e 0006, e pelo 0008 e 0009, que fazem o mesmo). As arestas 0007 → 0002/0004/0005/0006, 0008 → 0004/0006 e 0009 → 0003/0006 são falsas; a ordem acima usa só as declaradas na prosa. A aresta 0009 → 0002 é real e não aparece no script (conflito 11).

**Ciclos latentes:** as emendas pedidas ao ADR-0007 pelo 0008 e pelo 0009 criam 0007 → 0008 e 0007 → 0009 (conflito 1); o script só os acusa quando o `Depends On` for atualizado. Arestas ausentes da 3ª passada (0006 → 0005, 0006 → 0002) seguem ausentes.

⚠️ Os nove continuam `Proposed`. Nenhum dos outros oito pode ser implementado com segurança antes de o ADR-0001 ser `Accepted`. O aceite do 0001 depende da revisão independente dos GDDs #2 e #3; o 0003 só aceita depois dos gates G1 a G4 num aparelho Android real; o 0007 e o 0008 dependem do 0003; o 0009 depende do 0008.

### GDD Revision Flags (Architecture → Design Feedback)
Sem flag nova de comportamento de engine HIGH contra um GDD. Os três flags da 3ª passada persistem (GDDs e ADRs envolvidos não mudaram):

| GDD | Suposição | Realidade (ADR / engine) | Ação |
|---|---|---|---|
| combate-e-dano.md (AC-D5, L723) | `StateHash` do tick 900 igual entre o Editor e o IL2CPP ARM64 | ADR-0001 só promete o mesmo build e o mesmo runtime | Revisar o GDD (ou emendar o ADR) |
| dados-e-balanceamento.md (AC-09) | Teste por reflexão: "nenhum tipo é `T[]`" | ADR-0002 §4 decodifica para `int[]`/`float[]` privados expostos por `ReadOnlySpan` | Revisar o GDD |
| simulacao-deterministica.md (L103) e fluxo-de-fase.md (L133, L170) | Perda de foco conta como pausa | ADR-0003 §6 (L186): a pausa usa `OnApplicationPause` e nunca `Focus`; o ADR-0007 resolve com `FocusLost` como motivo de pausa que não grava | Revisar os GDDs e a Emenda ao ADR-0003 |

Divergências novas GDD × ADR (contrato, não engine): (1) **horda-waves-e-inimigos.md L182, L530, L796 e AC-P4** atribuem o pré-aquecimento ao #12 "no `Preparar`"; o ADR-0009 o põe antes do `Create`, em paralelo com o `BeginStage`; **antes de aceitar, essas linhas devem passar a dizer "antes do `Create`"**. (2) **combate-e-dano.md L412 e L440**: o #12 *cancela* o hit-stop no `CombatHold`; o ADR-0009 o *congela* (decisão de sensação de jogo, pergunta aberta para o autor). (3) GDD #6 e #7 dizem que o excedente de fantasmas "some com fade"; o ADR-0009 faz sumir na hora. (4) GDD #6 Visual/Audio pede `ultimoDanoTick` e `pesado` na vista; só `UltimoDanoTick` é pedido por emenda. (5) GDD #2 e #3 citam "ligação" como causa de pausa; a Unity não a distingue de `AppPaused`/`FocusLost`.

Índice de sistemas: nenhuma mudança proposta nesta passada (as divergências acima são ADR × GDD de contrato). Nenhuma pergunta de escrita no índice foi feita.

### Engine Compatibility Issues
Engine: Unity 6.3 LTS (6000.3.27f1). ADRs com a seção Engine Compatibility: 9 de 9. Os três novos dizem "6000.3.x; editor instalado 6000.3.27f1", batendo com `VERSION.md`.

- **API depreciada:** nenhuma usada. As ocorrências de `InstanceID` no ADR-0009 são `SV_InstanceID` (HLSL), não o `InstanceID` trocado por `EntityId` no 6.4+. O ADR-0009 VR9 põe "VFX Graph contra o sistema de partículas"; `deprecated-apis.md:91` manda trocar o *Legacy Particle System* (anterior ao Shuriken) por VFX Graph, que exige compute e não roda em GLES 3.0.
- **Pós-cutoff:** nenhuma API nova. O ADR-0009 diz "nenhuma API nova de Unity 6" mas usa o GPU Resident Drawer, que é recurso do Unity 6 (`VERSION.md` L75); isso é corrigido sugerindo tirá-lo do ADR (ver MEDIUM abaixo).
- **Ausência de `modules/core.md`:** nada do domínio Core foi checado contra módulo de referência. Segue NOT SOURCEABLE o que dependia disso (ver 3ª passada), mais os callbacks de pausa e foco do Android, `Time.unscaledDeltaTime` na volta do segundo plano e `Application.isFocused`, que nenhum arquivo de `docs/engine-reference/unity/` cobre.
- **Configurações do projeto** (da 3ª passada, inalteradas): `apiCompatibilityLevel: 6`, `m_EnterPlayModeOptionsEnabled: 1` com flags 0 (domain reload ligado), nenhum `.asmdef`, `Assets/Plugins` ausente.

### Engine Specialist Findings (`unity-specialist`)
Itens [conhecimento] não estão na referência local e pedem o spike no aparelho. As linhas do ADR-0009 L73, L84, L86 e L112 e a linha de partículas de `deprecated-apis.md` foram conferidas no texto; o resto vem do agente.

**HIGH**
- **ADR-0009 L84, L86, VR1: índice da textura por `SV_InstanceID`.** Quando a Unity divide o `RenderMeshInstanced` em lotes, o `SV_InstanceID` recomeça em 0 a cada lote, e o GLES não tem baseInstance [conhecimento, média-alta]. A partir do 2º lote, a instância N leria os texels da instância 0. A divisão é certa com 600 instâncias por tipo, e o ADR estima "2 por tipo": com o limite de UBO do GLES 3.0 podem ser 4 a 5 [conhecimento, média]. Correção: dividir no C# em pedaços de N instâncias (`#pragma instancing_options maxcount:N`), com base por pedaço num `MaterialPropertyBlock` via `RenderParams.matProps`, somada ao `unity_InstanceID`; ou um array de propriedade por instância (`UNITY_DEFINE_INSTANCED_PROP` + `SetVectorArray`), que a Unity divide junto com as matrizes. Medir no spike antes de adotar.

**MEDIUM**
- Premissa "domain reload desligado" nos três ADRs (ADR-0007 L28 VR8 e L243; ADR-0008 L133 e L275; ADR-0009 L73, L96, L307): `EditorSettings` tem flags 0, então o domínio recarrega. Mesmo ponto aberto do ADR-0003, agora propagado. Frase comum: "independe do domain reload (hoje ligado)". `Time.timeScale` é estado nativo; restaurar no teste continua certo, mas por outro motivo.
- ADR-0009 L73 e L307: `[RuntimeInitializeOnLoadMethod(SubsystemRegistration)]` é tipo do `UnityEngine` e não compila no asmdef sem engine onde mora o `Sim.View`. Apagar a cláusula; vale "zero `static` mutável" mais o teste de reflexão.
- ADR-0009 L86 e L79: a `RGBA32F` lida com o modelo de precisão padrão do Android perde os ticks perto de 36.000 [conhecimento, média-alta]; o GLES 3.0 não filtra float sem extensão. Usar `TEXTURE2D_FLOAT` com `.Load()`, sem mips, filtro `Point`, e checar `SystemInfo.IsFormatSupported` no boot.
- ADR-0009 VR1 e VR10: o plano B1 (`StructuredBuffer`) exige `SystemInfo.maxComputeBufferInputsVertex > 0`, que muitas Mali em GLES 3.1 não têm [conhecimento, média-alta]; na prática o B1 exige Vulkan.
- ADR-0009 L112 passo 4: o desenho "fora da tela" é descartado pelo culling e nada aquece. Desenhar dentro do frustum da câmera real, atrás da UI de carregamento, com o Volume do LUT do chefe ativo. `GraphicsStateCollection` (PSO no Vulkan) a medir [conhecimento, média; não verificado no 6.3].
- ADR-0009 L27 e VR10: o GPU Resident Drawer exige Forward+ e compute e se desliga sozinho no GLES [conhecimento, alta]. Com no máximo 150 draws o SRP Batcher basta; tirar do ADR ou mover para o de orçamento.
- ADR-0008 VR1 e L37 (A-ii): attach e detach de JNI por chamada num `ThreadPool` pode quebrar as próximas chamadas da thread [conhecimento, média-baixa]. O log usa só `System.IO`; JNI fica na thread dedicada do save, com attach uma vez ao iniciar e detach ao sair.
- ADR-0007 L64: não diz como o `AppLifecycle` persiste; no Editor, dar Play a partir de outra cena deixa o `PhaseHost` sem `PauseGate`. Criar por `[RuntimeInitializeOnLoadMethod(BeforeSceneLoad)]` em `Forja.Gameplay`, com `DontDestroyOnLoad` e guarda de duplicata.

**LOW:** (a) ADR-0007 L67 "falha o início do app": lançar no `Awake` não para o app; usar um estado de falha explícito que bloqueia o `BeginStage`; (b) ADR-0007 VR7: o padrão no Android é 30 fps, e o cenário a 60 Hz só existe com `Application.targetFrameRate = 60` explícito; (c) ADR-0009 L84: o `RenderMeshInstanced` lança sem `enableInstancing` no material, e o shader precisa de `#pragma multi_compile_instancing`; pôr no teste de contrato; (d) `DrainEvents` com dois consumidores (ADR-0007 L124, ADR-0008 L97, ADR-0009 L70): o `PhaseHost` chama uma vez por tick e passa o mesmo span; (e) três namespaces (`Sim.Host`, `Sim.Log`, `Sim.View`) num asmdef só; um asmdef `Forja.Gameplay.Host` sem engine tornaria os `forbidden_patterns` erro de compilação; (f) `Application.quitting` no Editor dispara no fim do Play Mode; desinscrever no `OnDestroy`; no Android não é confiável (o flush de verdade é o `OnApplicationPause(true)`).

**Confirmados sem ressalva:** `[DefaultExecutionOrder]` vale por tipo, inclusive em `DontDestroyOnLoad`; callbacks de pausa na thread principal, entre frames; `new ReadOnlySpan(buffer, 0, n)` não copia; `BinaryPrimitives`, `Span`, `BitConverter.SingleToInt32Bits` e `FileStream.Write(ReadOnlySpan)` existem no .NET Standard 2.1 (`Read/WriteSingleLittleEndian` não); `Volatile` e `Interlocked` certos no IL2CPP ARM64; o MPB tira o renderer do SRP Batcher e o `RenderMeshInstanced` não passa por ele; `WarmUp` só compila variantes e é o desenho que aquece; quad em vez de URP Decal; `worldBounds` explícito e sombra desligada; `float` (highp) nas contas de idade; `EnhancedTouchSupport.Enable` (`modules/input.md` L180-190).

**NOT SOURCEABLE que pede spike:** `unscaledDeltaTime` no 1º frame depois da volta (provavelmente não limitado por `maximumDeltaTime`); ordem de `Focus` e `Pause` com a GameActivity, multi-janela e picture-in-picture; `InputSettings.backgroundBehavior` e o dedo que continua apoiado na volta; tamanho real do lote de instancing e `unity_BaseInstanceID` no GLES 3.0 e Vulkan; `maxComputeBufferInputsVertex` no aparelho de referência; `GraphicsStateCollection` no 6.3; se a Unity anexa threads ao JNI sozinha; GPU Resident Drawer com Vulkan; o Shader Precision Model do projeto.

### Architecture Document Coverage
**NOT ASSESSED: não existe `docs/architecture/architecture.md`.** Em modo full isso por si só impede PASS. `/create-architecture` o gera. A camada dos ADR-0007 e 0008 (Core) e do 0009 (Presentation) é provisória por esse motivo; o ADR-0001 L76-78 põe a ponte em `Forja.Gameplay`.

---

### Verdict: CONCERNS

Igual à 3ª passada. Os ADR-0007, 0008 e 0009 fecharam cinco dos onze gaps (e três ⚠️ subiram), mas:
1. *Nenhum ADR `Accepted` (0 de 9).* Isso, sozinho, impede PASS.
2. *Phase 6 NOT ASSESSED* (sem `architecture.md`), que por si só impede PASS em modo full.
3. Catorze conflitos 🟠 novos e um HIGH de engine no caminho primário do render.

Por que não FAIL: FAIL exige gap crítico de Core ou conflito bloqueante, e não há conflito 🔴. Sobram duas linhas de Core sem ADR, `combate-012` e `horda-013` (orçamentos de frame), que dependem de medição no aparelho e que os ADRs adiam ao spike de propósito. **Esta é uma decisão de julgamento, a mesma da 3ª passada: se `combate-012` e `horda-013` forem tratados como gap crítico de Core, o veredito é FAIL.**

### Blocking Issues (must resolve before PASS)
1. Aceitar os ADRs na ordem 0001 a 0009 (o 0001 depende da revisão independente dos GDDs #2 e #3; o 0003 dos gates G1 a G4 em Android real).
2. Corrigir os conflitos 🟠 da 3ª passada (1 a 7) e os 14 desta, em especial 1 (ciclos nas emendas), 4, 5, 6, 10 e 11, antes de aceitar.
3. Resolver ou medir o HIGH do ADR-0009 (`SV_InstanceID` por lote) e decidir o plano B1 pela capacidade do aparelho.
4. Escrever a Emenda ao ADR-0003 com todos os itens: marca encontrada, enum de causas, `ReadOnlyRejected`, `IDataResolver`, `AttemptId`, FNV-1a 64, `Focus` só como gatilho de gravação, `ISaveStorage` seguro para dois chamadores, `Emit` na thread principal, fila do #28 esvaziada pelo `AppLifecycle`.
5. Corrigir o HIGH do ADR-0003 §7 (XMLs de backup fora de `Plugins/Android/res`) e o `Curar` sem guarda (ADR-0005).
6. Decidir a premissa de domain reload (ligado hoje) nos ADR-0003, 0007, 0008 e 0009.
7. Gerar `docs/architecture/architecture.md` (`/create-architecture`).
8. Aplicar o GDD Sync dos ADR-0005 a 0009, e reescrever o AC-D5 do #6.
9. Limpar os textos desatualizados (títulos "pendente" das Emendas 17 e 18, Last Verified, Related, GDD Sync dos ADRs novos).

### Required ADRs
Em ordem, as mais fundamentais primeiro. Os ADR-0004 a 0009 e as Emendas 17 e 18 do ADR-0001 já estão escritos e aguardam aceite.
1. **Emenda ao ADR-0003** (Core; maior que na 3ª passada, ver bloqueio 4): `save-010/011/018`, `fluxo-013`, `simulacao-016`, `fluxo-014`.
2. **Orçamento de frame por sistema e de entrada na fase** (Foundation; depois do spike de performance): `combate-012`, `horda-013`, `simulacao-018`, `fluxo-008`, e o dono do orçamento de carregamento e da memória.
3. Depois: análise estática e CI (`dados-016`), avisos do save para a UI (`save-017`), feedback de plataforma (`combate-019`), ADR do #29, ponto fixo para ranking (`simulacao-020`, Alpha).

### Pré-gate (todos ❌)
- `Assets/Tests/EditMode` e `Assets/Tests/PlayMode` ❌ → `/test-setup`
- `.github/workflows/tests.yml` ❌ → `/test-setup`
- `design/accessibility-requirements.md` ❌ → `/ux-design`
- `design/ux/interaction-patterns.md` ❌ → `/ux-design`

### Limites desta passada
- A detecção de conflitos entre ADRs (e a lista dos 14) vem de um agente de leitura; a auditoria de engine, do `unity-specialist`. Nenhum dos dois editou arquivo.
- Conferi diretamente: o recibo (só 0007, 0008 e 0009 são `NEW`), o grafo de ADRs, a estrutura das seções dos três ADRs novos, os conflitos 4, 5, 6, 10, 11 e 14 e a premissa do 7, as linhas L73, L84, L86 e L112 do ADR-0009, a linha de partículas de `deprecated-apis.md`, os quatro itens pré-gate e a contagem final da matriz (79 / 40 / 6 / 1 superseded) sobre as linhas da tabela.
- Não conferi: os conflitos 1, 2, 3, 8, 9, 12 e 13 e todos os achados do `unity-specialist`; os GDDs nas linhas citadas pelos ADRs novos; `docs/registry/architecture.yaml`; as seções Alternatives do 0008 e do 0009; o ADR-0006 e o ADR-0002 além do grep.
- Toda afirmação de engine marcada [conhecimento] é do especialista, não da referência local.
- A regradação das 8 linhas que mudaram é de quem rodou a passada; as demais 117 vêm da 3ª passada.
