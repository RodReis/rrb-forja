# Review Log: Save local (#28)

## Review — 2026-11-03 — Verdict: NEEDS REVISION
Review mode: full · Workflow: full
Scope signal: L
Specialists: game-designer, systems-designer, qa-lead, unity-specialist, ux-designer; senior reviewer: creative-director
Blocking items: 8 | Recommended: 10 (mais os itens que vão para o ADR da OQ-1)
Summary: O núcleo (commit único, backup reverificado, só leitura, pilares e decisões do usuário) está sólido e nenhum pilar exige redesenho. Os problemas estavam na máquina de recuperação (precedência, temporário órfão, estado "armazenamento indisponível", cabeçalho sem verificação própria, marca "fase em andamento" sem idempotência, `saveSequence` reutilizável, relógio sem saída) e nas bordas que o jogador sente (selo pendente, fase perdida sem explicação, migração falha, Irrecuperável sem fluxo). Quatro decisões do usuário foram tomadas na revisão (selo pendente, "não recomeçar", texto do Auto Backup, Livro devolvido).
Prior verdict resolved: First review
Revision applied: o GDD foi revisado no mesmo dia (2026-11-03) e o registro `design/registry/entities.yaml` atualizado (`effective_utc`, `save_sequence`). **Não houve re-review.** O carimbo abaixo é do GDD e do registro **como foram revisados** (antes da revisão), de propósito: o próximo `/design-review` deve ler `CHANGED` e fazer a revisão completa, em vez de tratar o texto novo como já revisado.
Findings:
- [BLOCKING] States and Transitions / Core Rules 7, 8, 14: matriz de recuperação incompleta (precedência, temporário órfão nunca promovido, primeiro commit cortado = Ausente, "armazenamento indisponível", Irrecuperável sem recomeçar, selo fantasma por temporário não confirmado). [systems-designer, unity-specialist, ux-designer, creative-director]
- [BLOCKING] Core Rule 9: cabeçalho sem verificação própria; um bit invertido na versão prende o jogador em só leitura, com a mensagem errada e sem consultar o backup. [systems-designer, unity-specialist, creative-director] (o game-designer classificou como RECOMENDADO; o creative-director decidiu BLOQUEANTE)
- [BLOCKING] Core Rule 6: a marca "fase em andamento" garante "pelo menos uma vez", não "uma vez"; abrir o app não era ponto seguro; faltava `attemptId`. [systems-designer, qa-lead, game-designer]
- [BLOCKING] Formulas F1/F2/F4: `nowUtc` sem faixa (o valor máximo de `int64` trava o `maxSeenUtc` para sempre e estoura); `saveSequence` reutilizado entre tentativas diferentes; F4 degenera. [systems-designer]
- [BLOCKING] UI Requirements: faltavam as mensagens "fase interrompida", "migração falhou", selo pendente com ação, Irrecuperável com confirmação e a fila de avisos. [ux-designer, game-designer, creative-director]
- [BLOCKING] Core Rule 12: selo pendente sem ação, sem permanência e sem regra para iniciar fase; contrato com o #17 indefinido. [ux-designer, game-designer, creative-director]
- [BLOCKING] Acceptance Criteria: AC-10 não determinístico; AC-04 e AC-08 testam o sistema errado (a contagem é do #3); sem AC para precedência, causa "restaurado", marca achada 2 vezes, migração falha, fronteiras do relógio, `maxSeenUtc`. [qa-lead, creative-director]
- [BLOCKING] Player Fantasy (linha 26): prometia "nenhum caminho para desfazer o selo", mas o Auto Backup (decisão do usuário) abre uma brecha fora do jogo. [game-designer, creative-director]
- [RECOMMENDED] F3: faixa do knob e teto do retrato; métricas de GC e p95 vão para o ADR. [systems-designer, unity-specialist]
- [RECOMMENDED] Interactions/Dependencies: interface de eventos do #28 com sink nulo e buffer para eventos do boot; direção da dependência #5 ↔ #28. [systems-designer]
- [RECOMMENDED] Core Rule 6 / UI: o aviso de backup restaurado diz até onde o jogo voltou; "confirmado antes de mostrar" também para registro do Grimório e herói novo. [game-designer, ux-designer]
- [RECOMMENDED] Core Rule 9: a consulta em só leitura exige formato aditivo; "tela fixa" e "consulta" se contradizem (vai para a spec de UX). [game-designer]
- [RECOMMENDED] Acceptance Criteria: dividir AC-03, AC-15 e AC-19; AC-13 só desbloqueia com OQ-2, aparelho de referência e protocolo; dublês para #3, #5, #1, #16/#19 e #17; teste de contrato contra o adaptador real após o ADR. [qa-lead]
- [RECOMMENDED] Dependencies/metadados: "K períodos" não existe no GDD do #1; status do #1 ("In Review") e do #28; escopo L em vez de S no índice. [revisão principal, creative-director]
- [RECOMMENDED] Acessibilidade: `design/accessibility-requirements.md` não existe e é pré-requisito do `/ux-design` (rebaixado a gate da spec de UX pelo creative-director). [ux-designer]
- [RECOMMENDED] Livro de Reforja devolvido quando uma run é interrompida (reforja fora do MVP, `game-concept.md` L413): registrado como decisão do usuário e OQ-6. [game-designer, creative-director]
- [RECOMMENDED] Relógio: botão "recalibrar" fica para o Vertical Slice; só o #29 com hora do servidor reduz `maxSeenUtc` (OQ-4). [systems-designer, creative-director]
- [RECOMMENDED] Auto Backup: o ADR confirma a viabilidade; se não for viável, a decisão volta ao usuário (OQ-5). [unity-specialist, creative-director]
- [RECOMMENDED] Metadados do índice e do registro (`save_sequence`, `effective_utc`) alinhados ao GDD revisado. [revisão principal]
Carimbo dos arquivos como foram revisados (o GDD e o registro, antes da revisão aplicada):
Reviewed-Content-Hash: design/gdd/save-local.md a2b75a3eda06efa8e1e9b1db6a5b560084126b19
Reviewed-Content-Hash: design/registry/entities.yaml 3d397947ec5d1d2aff257e9de99a5248076b881a
Reviewed-Content-Hash: .claude/skills/design-review/SKILL.md a63d8fba9b7142eeb43791f061e2e1533c429b43
Reviewed-Content-Hash: design/gdd/dados-e-balanceamento.md d93a8dfb2afd3163a1958da6cdb1aa13747de408
Reviewed-Content-Hash: design/gdd/game-concept.md 3a61558d87c0374c253396d6a268ac932ac062f3
Reviewed-Content-Hash: design/business-model.md fef23ee16b19a6cc595afb7dda25d87d0c132c61

## Review — 2026-11-03 — Verdict: NEEDS REVISION
Review mode: full · Workflow: full
Scope signal: L
Specialists: game-designer, systems-designer, qa-lead, unity-specialist, ux-designer; senior reviewer: creative-director
Blocking items: 9 | Recommended: 9
Summary: A 2ª passada confirmou que a estrutura está certa (CRC do cabeçalho, temporário órfão nunca promovido, F4 como invariante, estados separados) e que os 8 bloqueantes anteriores foram atacados. Os 9 novos são pontos em que um programador teria de adivinhar (`attemptId`, estado Ausente × quarentena, `maxSeenUtc`, F1, F2, cópia do backup), em que o jogador fica sem saída ("Armazenamento indisponível", save irrecuperável) ou em que o Pilar 2 não se sustentava (selo cancelado gravado por um tempo esgotado, selo em uma cópia só). Nenhum pede redesenho. Três decisões do usuário foram tomadas na revisão: duas cópias do selo na hora, botão "Pedir ajuda" no save irrecuperável e selo gravado antes do aviso aparece selado sem aviso extra.
Prior verdict resolved: Yes (os 8 bloqueantes da 1ª passada foram resolvidos; os 9 desta passada são novos ou vieram da própria revisão)
Revision applied: o GDD, o registro (`effective_utc`, `save_sequence`) e o Dependency Map do índice foram revisados no mesmo dia (2026-11-03). **Não houve re-review.** O carimbo abaixo é de como os arquivos estavam **antes** dessa revisão, de propósito: o próximo `/design-review` deve ler `CHANGED` e fazer a revisão completa. O índice foi carimbado também (o Dependency Map foi corrigido depois).
Findings:
- [BLOCKING] Core Rule 6 / AC-22/23: `attemptId` sem tipo e "≤ lastConsumedAttemptId" quebrado; um backup restaurado faz o #5 engolir uma tentativa legítima; a causa "Restaurado" se perdia se o app morresse antes do consumo. [todos os especialistas]
- [BLOCKING] States and Transitions / AC-29: Ausente exige quarentena ausente, mas "recomeçar" a preserva; a quarentena não tinha nome, limite nem retenção. [systems-designer, qa-lead, game-designer]
- [BLOCKING] Core Rules 5 e 11 / AC-25 / AC-03a: o `maxSeenUtc` não tinha ponto de gravação. [systems-designer, unity-specialist, qa-lead]
- [BLOCKING] F1: o `output_range` era falso; o valor salvo não era saneado (`int64` máximo travava a hora e estourava a Economia); bordas ausentes no AC-11. [systems-designer, qa-lead]
- [BLOCKING] F2 / AC-12: lia arquivos não verificados e prometia unicidade que uma restauração quebra (o 42 se repete). [qa-lead, systems-designer]
- [BLOCKING] Core Rule 12 / Knobs / AC-04c: "Falhou (tempo esgotado)" mentia com o commit em andamento (selo cancelado podia aparecer gravado); o `BeginStage` não tinha teto. [ux-designer, unity-specialist, qa-lead, game-designer, systems-designer]
- [BLOCKING] Core Rule 12 / Player Fantasy L26: o selo vivia em uma cópia só até o próximo commit, e um corte depois da troca deixava o herói selado sem confirmação. [game-designer, systems-designer]
- [BLOCKING] Core Rule 7 / AC-10: `File.Copy` sobre o `.bak` destruía o backup bom; a falha da cópia não estava definida; faltavam cortes no meio da cópia e da troca; o teste de contrato era só prosa. [unity-specialist, qa-lead]
- [BLOCKING] States and Transitions (Armazenamento indisponível) / Core Rule 14: sem mensagem e sem saída; "relê até 2 vezes" ambíguo e sem AC. [ux-designer, systems-designer, qa-lead]
- [RECOMMENDED] UI Requirements: banner do selo pendente por causa, "Cancelar" desabilitado com rótulo, mensagem 5 neutra, mensagem 1 com "ações recentes", fila de avisos, só leitura com faixa persistente, acessibilidade própria do #28. [ux-designer]
- [RECOMMENDED] Acceptance Criteria: AC-24, AC-03b, AC-16, AC-20 e AC-19b vagos ou sem oráculo; AC-06 citava evento fora da lista; nenhum AC para a data do selo vinda de `effectiveUtc`. [qa-lead, unity-specialist]
- [RECOMMENDED] Estados: faltavam "principal sumiu" na quarentena, Corrompido com backup em formato antigo e backup com sequência maior que o principal. [systems-designer]
- [RECOMMENDED] Player Fantasy L24 ("nunca porque o aparelho esqueceu") convivia mal com o Auto Backup. [game-designer]
- [RECOMMENDED] Metadados: status "In Design" × índice "In Review"; bloco de review solto na regra 1; frase em inglês em F1 a F4; exemplo simbólico na F3. [revisão principal]
- [RECOMMENDED] Índice: o Dependency Map omitia o 28 em #3, #17 e #26 e punha o #28 em "Foundation (no dependencies)" apesar de depender do #1 (a tabela de enumeração estava certa; a constatação inicial da revisão principal de que a frase do GDD era falsa foi corrigida pelo creative-director). [revisão principal, creative-director]
- [RECOMMENDED] Core Rule 4: fatia conhecida com versão mais nova é problema do dono da fatia. [unity-specialist]
- [RECOMMENDED] ADR (OQ-1): API da troca atômica, `fsync` do diretório, `persistentDataPath` interno, `noBackupFilesDir`, `allowBackup` e `dataExtractionRules`, flush na pausa com espera com teto, formato TLV. [unity-specialist]
- [RECOMMENDED] OQ-5: sinal "pausada" na marca e devolver o custo de entrada em todo "app fechado" ficam para a revisão com dados (no MVP não existe energia nem custo de entrada). [game-designer, creative-director]
Carimbo dos arquivos como foram revisados (antes da revisão aplicada):
Reviewed-Content-Hash: design/gdd/save-local.md acc4e58c1ff5dfce3c55943d777e11121ab134a2
Reviewed-Content-Hash: design/registry/entities.yaml 22f3916d996bfd504c13aca09e6289cf70d21ead
Reviewed-Content-Hash: .claude/skills/design-review/SKILL.md a63d8fba9b7142eeb43791f061e2e1533c429b43
Reviewed-Content-Hash: design/gdd/dados-e-balanceamento.md d93a8dfb2afd3163a1958da6cdb1aa13747de408
Reviewed-Content-Hash: design/gdd/game-concept.md 3a61558d87c0374c253396d6a268ac932ac062f3
Reviewed-Content-Hash: design/business-model.md fef23ee16b19a6cc595afb7dda25d87d0c132c61
Reviewed-Content-Hash: design/gdd/systems-index.md b935c7ca747b94c5613d51ae8ed52547f5c1eb1c

## Ciclo encerrado — 2026-11-03
O usuário encerrou o ciclo de revisão após 2 passadas (limite do projeto), com todos os bloqueantes aplicados no texto. Não houve conferência final. Próximo trabalho: `/design-system #2 Simulação determinística`. Uma nova `/design-review` deste GDD só se surgir conflito com GDDs futuros.
