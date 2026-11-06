## Architecture Review Report
Date: 2026-11-06
Mode: full
Workflow: full
Engine: Unity 6.3 LTS (6000.3.27f1)
GDDs Reviewed: 6 (de 8 arquivos em design/gdd/; game-concept.md e systems-index.md não são GDDs de sistema)
ADRs Reviewed: 6

Reviewed-Content-Hash: docs/architecture/adr-0001-simulacao-deterministica-float32-tick-30hz.md 0501f025c4bab398dee4338b0cdb2738cc1c888b
Reviewed-Content-Hash: docs/architecture/adr-0002-dados-e-balanceamento-snapshot-imutavel-gerado-no-build.md 9f40c08f9c59a92d0cebc7a8570192582f48066f
Reviewed-Content-Hash: docs/architecture/adr-0003-save-local-envelope-tlv-commit-atomico-gravador-unico.md b2b8e643afcb53e743598ece049e82c46d85c010
Reviewed-Content-Hash: docs/architecture/adr-0004-colunas-do-simworld-combate-e-horda.md 83f42c8de7d228061bc562bb3d892622c211dce5
Reviewed-Content-Hash: docs/architecture/adr-0005-pipeline-de-dano-e-eventos-de-combate.md 25c3b5d7348f5006c1581e8e6184189d8bd3ad64
Reviewed-Content-Hash: docs/architecture/adr-0006-vetor-geometria-e-consulta-espacial-deterministicos.md e9bdc151c4cc6e2c0e204fd2311394eddaa06a00
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

> **3ª passada (a primeira de 2026-11-06).** Substitui, como estado vigente, a 2ª passada de 2026-11-05 (FAIL; 125 requisitos: 64 🟡, 44 ⚠️, 17 ❌), que fica em `architecture-review-2026-11-05.md` como histórico. Motivo da nova passada: o ADR-0001 ganhou as Emendas 17 e 18 e entraram os ADR-0004 (colunas do `SimWorld`), ADR-0005 (pipeline de dano e eventos) e ADR-0006 (vetor, geometria e consulta espacial), todos `Proposed`. Os GDDs, o ADR-0002, o ADR-0003, o registro de TRs e as referências de engine não mudaram.

### Traceability Summary
Total requirements: 125 ativos (mais 1 superseded: TR-combate-016)
✅ Covered (ADR Accepted): 0
🟡 Covered (ADR Proposed): 73
⚠️ Partial: 41
❌ Gaps: 11

Os 6 ADRs estão `Proposed`; a cobertura é, portanto, 🟡 e limita o veredito a CONCERNS no máximo. A rota é `/architecture-decision accept ADR-NNNN`.

| GDD | Ativos | 🟡 | ⚠️ | ❌ | Mudança desde 2026-11-05 |
|---|---|---|---|---|---|
| #2 Simulação | 22 | 12 | 8 | 2 | `simulacao-008` caiu de 🟡 para ⚠️ |
| #3 Fluxo de fase | 20 | 11 | 8 | 1 | Nenhuma |
| #1 Dados | 20 | 12 | 7 | 1 | Nenhuma |
| #28 Save | 19 | 14 | 4 | 1 | Nenhuma |
| #6 Combate | 22 | 10 | 9 | 3 | `combate-001`, `005`, `010`: ❌ para ⚠️; `011`: ❌ para 🟡; `002`, `007`, `023`: ⚠️ para 🟡 |
| #7 Horda | 22 | 14 | 5 | 3 | `horda-005`, `012`: ❌ para 🟡; `006`, `007`, `009`, `016`: ⚠️ para 🟡 |

Total: 64 → 73 🟡, 44 → 41 ⚠️, 17 → 11 ❌. Nenhum ID novo, nenhum texto de requisito alterado; `tr-registry.yaml` não foi tocado.

**Critério usado nas linhas controversas.** `combate-003` e `horda-001` ficam ⚠️: a ordem #7→#8→#6→#3→#16 aparece só em diagrama e em texto de consequência nos ADR-0004 e ADR-0005 (ADR-0005 L128, L64, L89; ADR-0004 L116), e nenhum ADR a decide; ela só está no GDD #2 Regra 5 (provisória). `simulacao-008` caiu para ⚠️ porque a Emenda 18 (a) abre três canais diretos entre sistemas e o texto do requisito diz "comunicação só pelo SimWorld". `dados-009` e `save-013` mantêm 🟡 com a nota da passada anterior (nada neles mudou); pela regra literal ("GDD e ADR divergem") poderiam ser ⚠️, o que daria 71 / 43 / 11. A regradação dos 125 requisitos foi feita por um agente de leitura; as linhas citadas por requisito não foram reconferidas uma a uma.

### Coverage Gaps (no ADR exists)
11 requisitos, listados em `requirements-traceability.md` (Known Gaps). Nenhum deles é um dos gaps de Core que travavam o #6 e o #7 na passada anterior (colunas do `SimWorld`, fila de dano, vetor e geometria, consulta espacial): esses agora são 🟡 ou ⚠️.

| TR | Requisito | ADR sugerida | Domínio | Risco de engine |
|---|---|---|---|---|
| simulacao-015 | Ponte de entrada (Move por tick, ações discretas) | Ponte de entrada, tempo e ciclo de vida do app | Entrada | HIGH |
| simulacao-020 | Validação entre aparelhos exige ponto fixo | Simulação em ponto fixo (Alpha) | Core/Rede | MEDIUM |
| fluxo-016 | Log do #3 | Log de eventos e instrumentação (#5) | Log | LOW |
| dados-016 | Análise estática de literais de gameplay no CI | Análise estática e CI | Ferramentas | MEDIUM |
| save-017 | Avisos do save para a UI | Avisos do save para a UI | UI | LOW |
| combate-012 | Orçamento do Tick do #6 (p95 ≤ 2,0 ms, p99 ≤ 4,0 ms) | Orçamento de frame (após o spike) | Desempenho | MEDIUM |
| horda-013 | Orçamento do passo do #7 (p95 0,3 ms, p99 0,5 ms) | Orçamento de frame (após o spike) | Desempenho | MEDIUM |
| combate-018, horda-014, horda-015 | Render de multidão, efeitos, pré-aquecimento do chefe | Render de multidão e VFX em mobile | Render | HIGH |
| combate-019 | Háptico e tremor | Feedback de plataforma | Plataforma | HIGH (API NOT SOURCEABLE) |

`combate-012` e `horda-013` são de camada Core. Os ADR-0004, 0005 e 0006 os deixam para o spike de propósito ("medido no spike", ADR-0004 L290, ADR-0005 L286, ADR-0006 L271); um orçamento sem medição seria um número inventado. Isso entra no veredito abaixo.

### Cross-ADR Conflicts
Áreas propensas a conflito (`docs/consistency-failures.md`): a fronteira #2 × #6 × #7 (ids, mortes dentro do tick, fila de dano, rugido, causa de morte num enum de ADR `Proposed`, regras gerais que esquecem casos especiais). Os ADR novos seguiram o padrão recomendado: todo campo, enum ou canal que um GDD de Feature nomeia entrou na emenda do ADR do Core na mesma passada (Emendas 17 e 18).

**Nenhum conflito bloqueante (🔴).** Implementar os seis ADRs como escritos não quebra a integração. As Emendas 17 e 18 batem com o que o ADR-0004 §7 e o ADR-0005 §8 pediram: assinatura do `Spawn` com `EntityClass` e `archetypeId`, valores de `EntityClass` (0 a 4) e de `SimEventKind` (0 a 11), `ArgA`/`ArgB`, `HpAndPosForWrite`, `Kill` e `Spawn` sem evento, as três formas de canal direto, `SimContext.Strict`, `SimInvariantException` e a ordem do hash do Core. Só as letras dos subitens diferem entre o ADR-0005 §8 e a Emenda 18; o conteúdo é o mesmo.

Nove conflitos 🟠 (lacuna de dono ou de clareza). Os quatro primeiros foram conferidos diretamente no texto; os outros vêm do agente de conflitos.

1. **ADR-0001 L473, critério de teste.** Diz que `Kill` duas vezes no mesmo id e tick "gera 1 `Death`". Pela Emenda 18 o `Kill` não emite evento; esse teste falharia como escrito. Tem efeito de contrato.
2. **ADR-0001 Emenda 8 × Emenda 17(b) (NaN e hash).** O hash do Core agora percorre todo id < `IdCount`, vivo ou morto, com HP, x e y. A Emenda 8 (L101) só regrava a posição da entidade com NaN, então o HP com NaN ficaria numa linha morta que entra no hash. Além disso o Core passa a escrever numa coluna que o ADR-0004 L211 e o ADR-0001 L302 dizem ser só do #6. Opções: o Core grava HP = 0 no caminho do NaN e a exceção entra no texto do "escritor único", ou o hash pula o HP de linhas mortas. Corrigir antes de aceitar.
3. **ADR-0005 L37 × L196 (dependência oculta no ADR-0006).** L37 diz que o ADR-0006 é independente; L196 exige que `Aplicar` lance se `SourceId == −1`, `KbDistancia > 0` e não há `DirExplicita` ("ADR-0006"), e o ADR-0006 L113 define que o #6 calcula `KbDir` com as posições depois do passo 5. O `Depends On` do ADR-0006 (L34) não lista o ADR-0005 nem o ADR-0002 (`cos2Meia` em `decimal` no build, `Arena` do snapshot). O grafo de dependências não enxerga essas arestas.
4. **`xpValue` ilegível.** A Emenda 17(c) (ADR-0001 L110) promete `ReadOnlySpan` para as colunas-base e as quatro novas, e o ADR-0004 L287 diz que o #3 lê `xpValue`; nenhuma Key Interface (ADR-0001 L210-211, ADR-0004 L157-166) expõe `XpValues` ou `Essentials`, só `IsEssential(id)`. O #3 não tem como ler `xpValue`.
5. **Ordem do compositor.** Nenhum ADR fixa #7→#8→#6→#3→#16; ADR-0004 e ADR-0005 dependem dela e ela só existe no GDD #2 Regra 5 (provisória). O ADR-0001 L107 diz que o `Preparar` roda "na ordem do compositor com o #3 primeiro", o que é ambíguo frente ao #3 em 4º no tick. O ADR-0004 L122 diz que a ordem entre o `Preparar` do #6 e o do #3 não importa.
6. **ADR-0005 × ADR-0002, `cap_fila`.** O ADR-0005 (L34, L62) diz que vem do snapshot; o ADR-0004 L125 diz que a fórmula é do GDD #6; o `PhaseSnapshot` do ADR-0002 (L111-121) e o `IPhaseSnapshot` do ADR-0001 (L243) não têm o campo. Opção: `QueueCapacity` no `PhaseSnapshot`, com a fórmula do #6 e a validação do #1.
7. **ADR-0005 (Decisão 7) × ADR-0001 (Emenda 10), `EventCapacity`.** A fórmula tem o termo `R` = `EventosReservados`, constante de código do Core (8 a 16) que o #1 não conhece; o ADR-0005 diz "validada pelo #1". `K` (`SkillCast`) e `E_3_16` ficam `NOT ASSESSED`. A fórmula também difere da do GDD #6 ("+5"), e o GDD Sync do ADR-0005 (L303) não lista essa troca.
8. **Memória.** ADR-0004 ~110 KB (1124 linhas), ADR-0005 fila de `cap_fila` × 28 B (~10 KB) mais `SimEvent` de 20 para 28 B por posição, ADR-0006 ~4,5 KB por chamador. O único orçamento existente é o `phase_snapshot_memory_kb` do ADR-0002 (L290), sem valor. Não dá para conferir a soma (~130 KB mais eventos) porque não há número nem está dito se as tabelas dos sistemas contam nele.
9. **ADR-0006 L89.** Diz que as mortes ocorrem "depois de todos os `Step`"; o #3 e o #16 rodam depois do 7b do #6 (ADR-0005 L128). Sem efeito prático (`SimQuery` filtra por `IsAlive`).

**Persistem da passada anterior (nada disso foi tocado pelo diff do ADR-0001):**
- `AttemptId` entre asmdefs (`Gameplay.Sim` → `Forja.Save`): nenhum ADR declara a referência.
- FNV-1a 64: ADR-0003 fixa a API em `Forja.Data` (L34, L182, L357), o ADR-0002 L319 ainda a lista como pendência Q4, e o `StateHasher` do Core tem um terceiro FNV.
- Orçamento da tela de carregamento: cresceu, porque o `Preparar` agora também zera ~110 KB do #6, aloca a fila (ADR-0005 L288) e a `Arena` e os buffers de consulta (ADR-0006 L273). Continua sem dono.
- `IPhaseSnapshot` × tipo concreto: reforçado pelo ADR-0006 L62, que exige que o compositor leia o snapshot concreto para a `Arena`. A referência `Gameplay.Sim` → `Forja.Data` não foi conferida linha a linha.

**Textos desatualizados dentro das ADRs (sem efeito de contrato, pedem limpeza):**
- *ADR-0004:* L127 título "Emenda 17 (pendente; só com aprovação do autor)", superado porque a Emenda 17 está aplicada em ADR-0001 L110; L34, L296 e L307 ("precisa receber / aprovar e aplicar / Emenda 17 pendente"); L10 "verificado contra as Emendas 1 a 16"; L308 "ADRs vizinhos ainda não escritos"; L64 o scratch ainda lista "dano e cura" (contradiz L98, L104 e a nota de sincronia em L37); L101 "é decisão do ADR-0005", já decidido.
- *ADR-0005:* L123 título "Emenda 18 (pendente)"; L10 "Emendas 1 a 16" e "ADR-0004 em rascunho"; L34, L292 e L309 (mesmo padrão); L268 pendências já feitas (nota de sincronia no ADR-0004 L37, entradas do registro); L306 GDD Sync lista o ADR-0004 como pendente; L310 "ADR-0006 ainda não escrito"; L75 × L166 `HitFlags.Suprema = 8` ausente da declaração.
- *ADR-0006:* L288 título "GDD Sync (pendente; nenhum arquivo foi editado)" contradiz L289-290; L62 diz que o compositor confere `IsValid`, L152 diz que é o `Preparar`.
- *ADR-0001:* L473 (ver o conflito 1); L62 "definido pelo ADR de #6" (agora ADR-0006); L35 `Enables` não lista 0004, 0005 e 0006; L7, L15, L22 e L484 citam 0004 e 0005 mas não a linha 30 da tabela de Emendas (ADR-0006); L34 ("Depends On: None"), L37 ("Accepted antes de `/design-system` de #6"), L404 ("mínimo de 1 tick"), L414, L417 e L422 (Regra 13 do #2 como pendente), L483 ("Sem outros ADRs além dele").
- *ADR-0002:* L34 ("único outro ADR") e L317 (ADRs de #6/#7 e do save como futuros).
- *ADR-0003:* L360 (pede alinhar o `attemptId`, já em ADR-0001 L276) e L304 (marcador "só depois de ler um save válido").

### ADR Dependency Order
Script `adr-dep-graph.sh`: 6 ADRs, 10 arestas, sem ciclo, sem `NO_DEPS_SECTION` nem `UNFILLED_DEPS`.

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
```

Arestas ausentes (conflito 3): 0006 → 0005 e 0006 → 0002, mais a leitura em sentido contrário do ADR-0005 L196 para o ADR-0006. Se forem declaradas as duas direções entre 0005 e 0006 haverá um ciclo a evitar; a opção é o ADR-0005 depender do 0006 e o 0006 não depender do 0005 (mover a regra de `dir_kb` para o 0006 ou para o 0005, mas só uma vez).

⚠️ Os seis continuam `Proposed`. Nenhum dos outros cinco pode ser implementado com segurança antes de o ADR-0001 ser `Accepted`. O aceite do ADR-0001 depende da revisão independente dos GDDs #2 e #3; o ADR-0003 só aceita depois dos gates G1 a G4 num aparelho Android real; os ADR-0004 a 0006 só podem ser aceitos depois dos seus `Depends On`.

### GDD Revision Flags (Architecture → Design Feedback)
Sem flag nova de comportamento de engine HIGH. Os três flags da passada anterior persistem, porque nem os GDDs nem as ADRs envolvidas mudaram:

| GDD | Suposição | Realidade (ADR / engine) | Ação |
|---|---|---|---|
| combate-e-dano.md (AC-D5, L723) | `StateHash` do tick 900 igual entre o Editor e o IL2CPP ARM64 | ADR-0001 só promete o mesmo build e o mesmo runtime; ADR-0005 L28 (VR3) reforça "não igual ao do Editor" | Revisar o GDD (ou emendar o ADR) |
| dados-e-balanceamento.md (AC-09) | Teste por reflexão: "nenhum tipo é `T[]`" | ADR-0002 §4 decodifica para `int[]`/`float[]` privados expostos por `ReadOnlySpan` | Revisar o GDD |
| simulacao-deterministica.md (L103) e fluxo-de-fase.md (L133, L170) | Perda de foco conta como pausa | ADR-0003 §6: a pausa usa `OnApplicationPause` e nunca `Focus`; o ADR-0001 não diz quais callbacks a ponte ouve | Revisar os GDDs e a ponte |

Índice de sistemas: nenhuma mudança proposta nesta passada (os GDDs afetados já estavam em Needs Revision, e as divergências abaixo são ADR × GDD de contrato, não HIGH RISK de engine).

**Divergências GDD × ADR, resolvidas do lado do ADR (falta só o sync no GDD):**
- Evento `Death`: leva a causa em `ArgA`, `Kill` e `Spawn` não emitem evento, a horda sai agregada em `HordeTick` (ADR-0001 L108, L111, L164, L201; ADR-0005 L109-119). Resta renomear "Morte" no GDD #6 L68 e corrigir o GDD #2 L374 (que ainda diz que o `Death` sai com motivo inválido; pela Emenda 18(f) o caminho do NaN não emite `Death`).
- Reserva de eventos e `Rugido`: reserva por tipo, capacidade com termos nomeados que não depende da horda (ADR-0005 L121; ADR-0001 L103, L425). Resta `K` e `E_3_16` NOT ASSESSED, a fórmula diferente da do GDD #6 L420/L526, e renomear `HeroDeath` no GDD #2 L88.
- Nascimento no `CombatTick`: `Spawn` recebe classe e arquétipo e o `SimWorld` carimba `tickNascimento` e `hpMax` (ADR-0001 L99, L110, L200; ADR-0004 L105). Resta o `XpValues` legível (conflito 4).
- Canais e colunas: três formas de canal direto (Emenda 18a) e as colunas do ADR-0004. Resta o GDD #2 L86 ("só pelo SimWorld").
- Contadores do modo estrito (mecanismo): `SimContext.Strict` (ADR-0001 L223) e `CombatCounters` (ADR-0005 L95, L185-188). Surgiram duas divergências novas (abaixo).
- #7: `SimEventKind` sem `Rugido` e `Spawn` no tick emitindo evento: resolvidos (ADR-0001 L155, L200).

**Divergências novas:**
1. `GolpesLimitados` lança no modo estrito (ADR-0005 L95, L205); o GDD #2 L110 diz que só conta, nos dois modos, e o GDD #6 L352 não pede lançamento.
2. `CurasDescartadas` não conta alvo morto (ADR-0005 L87); o GDD #6 L361 conta.
3. O `Rugido` virou sinal único `PedirRugido` fora da fila (ADR-0005 L83); contradiz o GDD #6 L56-57, L353 e o knob `cap_fila` (L525), e o GDD #7 L111 (rugido via `Aplicar`, na frente da fila) e L177(f) (`cap_fila` com `teto_vivos_horda + 1`). Sync em ADR-0005 L304.
4. Cura sem `curaAcc`: `Curar` acumula direto em `curaPendente` (ADR-0005 L86-89); o GDD #6 L69 diz "como `Aplicar`, só enfileira" e a F2 ainda tem `curaAcc`.
5. `intentVel` é coluna hasheada no GDD #6 L103 e scratch no ADR-0004 L98; `esquivaBuf`, `ultimoContatoTick` e `ultimaDirecao` vão para o bloco do herói (L96, L267); a semântica de `cicloIdx` está "a confirmar" (L91).
6. **Hash do Core (Emenda 17b):** acrescenta `xpValue`, `classe`, `arquetipoId`, `tickNascimento` e `hpMax`; a FS8 do GDD #2 (L309) e a R10 (L99) só listam id, vivo, facção, `Essencial`, HP, x, y. Esta divergência não está em nenhuma lista de GDD Sync (o ADR-0004 nem tem essa seção).
7. `ICombatReadView` (ADR-0004 L179-196) não expõe `ultimoDanoTick` nem `pesado`, que o GDD #6 L587 pede.
8. Pendências do ADR-0006 (GDD Sync, L291-293): abertura do cone (NOT ASSESSED), predicado da F10 do #6 (L109), F4 do #7 com [0,L] e raio 0 contra o clamp [r, L−r] do #6, regra "vence" sem raiz, `passo_min_tick` e `dist_parada_m` ≥ 0,001, `cos2Meia` como obrigação do #1.

**Persistem (GDDs não mudaram):** morte por `Rugido` e XP (ADR-0001 L108 dá metade; GDD #3 L205 e L246 não preveem a causa); causa por golpe (GDD #6 L147 e AC-F2 L684 contra `DeathRecord {Id, Cause}`, mantido de propósito, ADR-0004 L105 e ADR-0005 L93); cast direto (GDD #6 L107 e L195 contra ADR-0001 L305); NaN com HP = 0 (GDD #2 L374 contra ADR-0001 L101); a recarga `g` entre #6 e #7; no #7: ordenação por índice contra (`inicio`, `w`), `NextBounded` contra `Pcg32.NextInt`, "5 a 7" contra "8 a 10" waves; marcas velhas no GDD #6 (L57, L435); `BannedApiAnalyzers` NOT SOURCEABLE; mais as divergências de #1, #3 e #28 da 1ª passada de 2026-11-05, que ficam como estavam.

### Engine Compatibility Issues
Engine: Unity 6.3 LTS (6000.3.27f1). ADRs com a seção Engine Compatibility: 6 de 6.

- **Versão:** os seis concordam com o editor instalado e com `VERSION.md`. O ADR-0004 cita também o 6000.5.5f1 só para dizer que não é o pin.
- **API depreciada:** nenhuma nova. `Vector3`, `Mathf` e `Unity.Mathematics` aparecem nos ADR-0004/0005/0006 só como proibições. Nenhum `InstanceID`. Persiste, do ADR-0002, o desvio deliberado da carga síncrona de `TextAsset` (`deprecated-apis.md:73-74`).
- **Pós-cutoff:** nenhuma API usada nos três ADR novos nem nas Emendas 17 e 18 (só `struct`, `readonly struct`, enums, arrays, `Span<T>`/`ReadOnlySpan<T>`, `in`, `MathF.Sqrt`).
- **Ausência de `modules/core.md`:** nada do domínio Core foi checado contra módulo de referência. Segue `NOT SOURCEABLE` o que dependia disso: comportamento de float entre Mono, IL2CPP e ARM64, FMA, `ReadOnlySpan` em propriedade de interface entre asmdefs sob IL2CPP com stripping, `in` de `readonly struct` sob IL2CPP, stack trace de exceção em Release IL2CPP, `BannedApiAnalyzers` no pipeline do 6.3.
- **Configurações lidas do projeto** (`ProjectSettings.asset` e `EditorSettings.asset`): `apiCompatibilityLevel: 6` (L928), `m_EnterPlayModeOptionsEnabled: 1` com `m_EnterPlayModeOptions: 0` (L27-28), `il2cppCompilerConfiguration: {}`, `managedStrippingLevel: {}`, `allowUnsafeCode: 0`, `AndroidTargetArchitectures: 2`. `Assets/Plugins` não existe e não há nenhum `.asmdef`. `com.unity.mathematics` 1.3.2, `burst` 1.8.17 e `collections` 2.4.3 estão no projeto como dependências transitivas.

### Engine Specialist Findings (`unity-specialist`)
Itens marcados [conhecimento] não estão na referência local e pedem o spike no aparelho.

**Novos nesta passada:**
- **MEDIUM, ADR-0005 L63 e L170-176.** A afirmação de que chamar `Aplicar`/`Curar`/`PedirRugido` fora do tick é "inexpressável" é falsa: `default(SimContext)` compila em qualquer lugar. `Aplicar` e `PedirRugido` lançam porque `CombatActive` vem falso, mas `Curar` vale sem `CombatActive` e grava `curaPendente`, que está no hash; chamado pela ponte ou por um cheat de debug fora do tick, quebra o replay sem erro. Correção: guarda de uma linha em `Curar` (`ctx.World != null`, tick corrente e estado `Running`, lançando nos dois modos) e trocar "inexpressável" por "guardado". [conhecimento, alta confiança]
- **MEDIUM, medição de alocação (ADR-0004 L28 VR2, ADR-0005 L28 VR1, ADR-0006 L28 VR2).** Um `ProfilerRecorder "GC.Alloc"` acumula por frame; num teste EditMode síncrono pode ler 0, e num player que não é Development Build os marcadores não existem. Usar `Is.Not.AllocatingGCMemory()` (Test Framework) com aquecimento e um controle positivo (um teste que aloca de propósito tem de falhar). [conhecimento]
- **MEDIUM, guarda de `HpAndPosForWrite` (ADR-0004 L28 VR6, L102).** `BannedApiAnalyzers` não fecha: o `BannedSymbols.txt` precisa chegar como AdditionalFile e o pipeline da Unity não usa csproj; o RS0030 é aviso por padrão; e o #6, o #7, o #8 e o #3 estão no mesmo assembly (`Forja.Gameplay.Sim`), então banir o método ali bane o #6 também. Recomendado, sem analisador: um objeto de capacidade (`CombatWriteAccess` sealed, construtor `internal` no Core, entregue pelo compositor só ao construtor do #6). [conhecimento]
- **MEDIUM, VR1 do ADR-0004.** Mistura domain reload com teste EditMode: testes EditMode não passam por domain reload, e a caixa "Enter Play Mode Options" está ligada mas com flags 0 (o domínio recarrega). O perigo real é `static` mutável; o código novo não tem nenhum. Substituir o eixo "sem domain reload" por um teste de reflexão (nenhum campo `static` não-`const` em `Forja.Simulation` e `Forja.Gameplay.Sim`) e corrigir a frase "ligado".
- **LOW:** (a) VR7 e VR5 do ADR-0004 e VR4 do ADR-0005 fecham quase de graça (`ReadOnlySpan<float> s = arr;` no asmdef; o nível 6 é .NET Standard 2.1; sem reflexão e sem genéricos virtuais não há problema de AOT, de generic sharing nem de `link.xml`); (b) criar os asmdefs de `Forja.Simulation` e `Forja.Gameplay.Sim` com `noEngineReferences`, `overrideReferences` e `precompiledReferences` vazio torna `Vector2`, `Mathf` e `Unity.Mathematics` erro de compilação, em vez de revisão (ADR-0006 L186-190); (c) separar produto e soma no C# não impede FMA: o Roslyn em Release elimina os locais, e quem decide é o C++ que o IL2CPP gera e o `-ffp-contract` do clang; abrir o C++ gerado no spike (ADR-0006 L143, L192; ADR-0005 L93, L197); (d) `[MethodImpl(AggressiveInlining)]` nos operadores de `SimVec2` antes de medir (ADR-0006 VR5); (e) `MathF.Sqrt`: bits iguais para a mesma entrada estão garantidos por IEEE 754, então a VR4 pesa pouco e não deve segurar o spike; (f) citar `il2cppStacktraceInformation` na VR6 do ADR-0005; (g) a regra "o span nunca escapa" (ADR-0004 L181-183, L209) o compilador já garante, e os escapes reais são `.ToArray()` e chamar a propriedade dentro do laço; (h) `DeathCause` (ADR-0001 L178) continua sem tipo-base declarado (`EntityClass`, `SimEventKind`, `HitKind` e `FactionFilter` já têm `: byte`).
- **Confirmados sem ressalva:** `in` com `readonly struct` (`HitRequest`) sem cópia defensiva; `SimVec2` por valor (8 B); `ref readonly` local e `fila[n++] = hit`; `HeroCombatView` por valor; Burst não se aplica (classes gerenciadas e exceções); `Kill` e `Spawn` sem evento não tocam API da engine.

**Da passada anterior, persistem** (ADR-0003 e a configuração do projeto não mudaram):
- **HIGH, ADR-0003 §7 (L119):** os XMLs de backup em `Assets/Plugins/Android/res/xml/`; a Unity recusa recursos soltos ali, e `Assets/Plugins/` nem existe no disco. Com `useCustomMainManifest: 0` as regras de backup não chegariam ao APK. Mover para `.androidlib` ou AAR.
- **MEDIUM:** GameActivity e manifesto; premissa de "domain reload desligado" (ADR-0003 L28 e L113) contra o `EditorSettings.asset`; `Application.quitting` sem desinscrição; `IsBackground = true` e join no reload na thread do gravador; ordem de boot sem raiz de composição única; callbacks de foco e pausa da ponte.
- **LOW:** `RngWave` devolve `Pcg32` mutável por valor (ADR-0001 L202, L227); e os LOW da 1ª passada (`TextAsset.bytes` aloca cópia, teto de 500 ms em `OnApplicationPause` contra ANR, FMA no clang do NDK, zerar o acumulador em `OnApplicationPause(false)`, "Auto Referenced" em `Forja.Save`).
- Consistência de threads entre as ADRs: consistente (simulação só na thread principal; retrato do save na principal; respostas por fila). Grafo de asmdefs sem ciclo.

### Architecture Document Coverage
**NOT ASSESSED: não existe `docs/architecture/architecture.md`.** Em modo full isso por si só impede PASS. `/create-architecture` o gera.

---

### Verdict: CONCERNS

Subiu de FAIL (2026-11-05). Os dois motivos daquele FAIL mudaram assim:
1. *Requisitos de Core do #6 e do #7 sem nenhuma ADR* — resolvido pelo lado do ADR: colunas, fila de dano, vetor, geometria e consulta espacial agora têm ADR (ADR-0004, 0005, 0006), ainda `Proposed`.
2. *Nenhuma ADR Accepted* — continua (0 de 6). Isso, sozinho, impede PASS, mas é o que o veredito CONCERNS descreve.

Por que não FAIL: FAIL exige gap crítico de Core ou conflito bloqueante, e não há mais nenhum dos dois. Sobram duas linhas de Core sem ADR, `combate-012` e `horda-013` (orçamentos de frame). Elas dependem de medição no aparelho, e os ADRs as adiam ao spike de propósito. **Esta é uma decisão de julgamento: se `combate-012` e `horda-013` forem tratados como gap crítico de Core, o veredito é FAIL.**

Além disso: Phase 6 NOT ASSESSED (sem `architecture.md`), que por si só impede PASS em modo full. Nove conflitos 🟠, sendo que os conflitos 1 e 2 devem ser corrigidos antes de aceitar.

### Blocking Issues (must resolve before PASS)
1. Aceitar os ADRs, nesta ordem: ADR-0001 (depende da revisão independente dos GDDs #2 e #3), ADR-0002, ADR-0003 (depois dos gates G1 a G4 em Android real), ADR-0004, ADR-0005, ADR-0006.
2. Corrigir os conflitos 🟠 1 a 7 antes de aceitar: o critério de teste do ADR-0001 L473; NaN × hash e escritor único; dependência do ADR-0005 no ADR-0006 e as arestas ausentes; `XpValues` e `Essentials` nas Key Interfaces; ordem do compositor registrada num ADR; `QueueCapacity` e o dono da fórmula de `cap_fila`; validação do termo `R` da `EventCapacity`.
3. Corrigir o HIGH de engine do ADR-0003 §7 (XMLs de backup fora de `Plugins/Android/res`) e decidir a premissa de domain reload; guardar o `Curar` do ADR-0005 (MEDIUM).
4. Gerar `docs/architecture/architecture.md` (`/create-architecture`).
5. Aplicar o GDD Sync: as listas do ADR-0005 (L302-307) e do ADR-0006 (L288-293), e a divergência do hash (Emenda 17b), que não está em lista nenhuma.
6. Reescrever o AC-D5 do #6 (hash Editor × IL2CPP).
7. Limpar os textos desatualizados (títulos "pendente" das Emendas 17 e 18, Last Verified, Related).

### Required ADRs
Em ordem, as mais fundamentais primeiro. ADR-0004, 0005 e 0006 e as Emendas 17 e 18 do ADR-0001 já foram escritos nesta data e aguardam aceite.
1. **Ponte de entrada, tempo e ciclo de vida do app** (Feature, HIGH): `simulacao-015/016`, `fluxo-014`; inclui a soma dos sinais de foco e pausa.
2. **Log de eventos e instrumentação do #5** (Core, MEDIUM): `simulacao-017`, `fluxo-010/016`.
3. **Emenda ao ADR-0003:** marca encontrada, enum de causas e `ReadOnlyRejected`, `IDataResolver`, registro do Grimório como 2º commit, `AttemptId` entre asmdefs e o FNV-1a 64 nas Key Interfaces do ADR-0002.
4. **Orçamento de frame por sistema e de entrada na fase** (Foundation; depois do spike de performance): `combate-012`, `horda-013`, `simulacao-018`, `fluxo-008`, e o dono do orçamento de carregamento e da memória.
5. **Render de multidão e VFX em mobile** (Presentation, HIGH): `combate-018`, `horda-014/015`.
6. Depois: análise estática e CI, avisos do save para a UI, háptico e tremor, ADR do #29, ponto fixo para ranking (Alpha).

### Limites desta passada
- A regradação dos 125 requisitos, as citações de linha por requisito e o levantamento de divergências GDD × ADR vêm de um agente de leitura; a detecção de conflitos entre ADRs, de outro; a auditoria de engine, do `unity-specialist`.
- Conferi diretamente: o recibo (o ADR-0001 mudou e os ADR-0004/0005/0006 são novos; o resto estava inalterado), o grafo de ADRs, as seções obrigatórias dos 6 ADRs, o diff do ADR-0001, a ausência de `architecture.md`, as APIs depreciadas e versões nos ADRs novos, o ADR-0001 L473, o texto da Emenda 8, o ADR-0005 L37 e L196, a ausência de `XpValues` no ADR-0004, os valores de `ProjectSettings.asset` e `EditorSettings.asset` citados e a contagem final da matriz (73 / 41 / 11 / 1 superseded) sobre as linhas da tabela.
- Não verifiquei: `docs/registry/architecture.yaml` (não li; o diff do ADR-0001 e o agente de conflitos indicam que o registro já recebeu as entradas da Emenda 17 e 18), `docs/consistency-failures.md`, a L119 e a L346 do ADR-0003 contra a L304, e se `Forja.Gameplay.Sim` pode referenciar `Forja.Data`.
- O significado de `apiCompatibilityLevel: 6` (.NET Standard 2.1) e o comportamento de `m_EnterPlayModeOptions: 0` são conhecimento do especialista, não da referência local.
- As colunas "Fonte no GDD" da matriz de #3, #1 e #28 são as da 1ª passada de 2026-11-05.
- O Edge Case de capacidade "até 300 `Death`" no GDD #2 não foi localizado pelo agente; o ADR-0005 L305 diz que essas linhas precisam ser conferidas.
