# Review Log: Horda, waves e inimigos (#7)

## Review — 2026-11-05 — Verdict: NEEDS REVISION
Review mode: full · Workflow: full
Scope signal: L
Specialists: game-designer, systems-designer, level-designer, ai-programmer, economy-designer, performance-analyst, qa-lead; senior: creative-director (não consultados: ux-designer, audio-director, unity-specialist; escopo mínimo no #7)
Blocking items: 9 | Recommended: 10
Summary: A base (maré e lâmina, composição sorteada no Preparar, teto de vivos com fila, rugido) serve aos pilares. Os furos estavam no momento-âncora (o respiro contava do último nascimento e uma wave podia vir 1 tick depois do elite; o Arremessador podia atacar de fora da tela) e em ambiguidades que impediam implementar de forma determinística (ordem dos elites, cancelamento sem cursor, NaN na chegada ao alvo, fronteira de float32). Revisado na mesma sessão com 5 decisões do autor; aguarda propagação das emendas e re-revisão.
Prior verdict resolved: First review
Author decisions (2026-11-05): Tank com XP completo; rugido dá metade do XP (`xp_rugido_mult` 0,5), sem efeitos de abate e sem loot (OQ-1 resolvida); elite atrasado espera a próxima janela de respiro do cronograma, com `espera_elite_max_s` (OQ-2 resolvida); Campeão ganha investida telegrafada; chefe nasce à vista (`R_chefe_m`).
Findings:
- [BLOCKING] F10 / Regra 5: respiro contado do último nascimento, sem tempo de viagem nem respiro depois do elite. Aplicado: `viagem_ticks` e `respiro_pos_elite_min_s`.
- [BLOCKING] Regra 3: `alcance_inicio_aviso_m ≤ R_spawn_m` deixa atacar de fora da tela. Aplicado: ≤ `meia_altura_visivel_m − margem_visivel_m` (provisório até o #4).
- [BLOCKING] Regras 9, 10.3, 13, 15: elites "na ordem de w" contra o cursor (inicio, w); cancelamento sem operação de cursor. Aplicado.
- [BLOCKING] Comportamento: NaN/tremor ao chegar no alvo. Aplicado na emenda (b) ao #6 (pendente no #6).
- [BLOCKING] F4/F5: fronteira de float32 com R_min = 0,99·R. Aplicado: 0,98·R.
- [BLOCKING] Regra 3: dano de contato de elite e chefe indefinido. Aplicado: só a horda tem contato (emenda (h) ao #6, pendente).
- [BLOCKING] Regra 7 / F4: espelhamento colapsa as frentes no canto. Aplicado: deduplicação sem sorteio extra e sinal `TicksNoCanto`.
- [BLOCKING] Dependencies / Player Fantasy: linhas 35, 168 e 489 contraditórias; emendas a #6, #2, #1 não aplicadas. Texto corrigido; emendas pendentes (propagação).
- [BLOCKING] Acceptance Criteria: fixture incompleta, R5 contra a Regra 9, R10 fora da fixture, F7/F9 [I] na fixture errada, contadores sem AC, E8/E10 sem BLOQ, AC-P1 não mensurável, sem AC do frame do rugido. Aplicado (P4 novo).
- [RECOMMENDED] Curva de fases: dois arquétipos novos nas fases 1 e 3; fase 5 a 100% do teto. Aplicado.
- [RECOMMENDED] Ritmo: sem limite máximo de respiro e silêncio. Aplicado como sinal `RespiroLongo`.
- [RECOMMENDED] Escolta pode cair no Aviso do chefe. Aplicado: pulso espera.
- [RECOMMENDED] Refill sem teto por tick. Aplicado: `max_nascimentos_por_tick`.
- [RECOMMENDED] F11 mistura HP máximo e mínimo. Aplicado: `hp_med` dos dois lados.
- [RECOMMENDED] `XpRugidoAlto` sempre acende. Aplicado: `RugidoMuitosNiveis`.
- [RECOMMENDED] F9 `xp_min` não é piso. Documentado.
- [RECOMMENDED] Curva de XP por fase precisa passar na F5 do #3 em conjunto. Nova OQ.
- [RECOMMENDED] Separação entre inimigos (grade O(n)) ao spike; tabela de mira de 32. Aplicado.
- [RECOMMENDED] Relatório de autoria por fase no #1. Exigência ao #1 (pendente).
Note on receipt: o #7 foi revisado depois desta revisão, por isso o alvo fica sem recibo; a próxima execução faz a re-revisão completa. O registro foi editado na revisão (expressões do #7 sincronizadas) e está carimbado na versão final.
Reviewed-Content-Hash: design/registry/entities.yaml f0b9889095e2e1724b3b5bf21b5398ba0a5f192b
Reviewed-Content-Hash: .claude/skills/design-review/SKILL.md a63d8fba9b7142eeb43791f061e2e1533c429b43
Reviewed-Content-Hash: design/gdd/combate-e-dano.md 163d47d18252f23b97e17a42b2331a5d29451dd6
Reviewed-Content-Hash: design/gdd/fluxo-de-fase.md 022ecda6c354b3fda492fca85492943bc3ebff62
Reviewed-Content-Hash: design/gdd/simulacao-deterministica.md da65d8de634c778730f3674a915380f61ed69db1
Reviewed-Content-Hash: design/gdd/dados-e-balanceamento.md 97ba0623083570cfcb91bd8214350dcf96b3a1ea
Reviewed-Content-Hash: design/gdd/game-concept.md 3a61558d87c0374c253396d6a268ac932ac062f3

## Review — 2026-11-05 — Verdict: NEEDS REVISION
Review mode: full · Workflow: full
Scope signal: XL
Specialists: game-designer, systems-designer, level-designer, ai-programmer, economy-designer, performance-analyst, qa-lead; senior: creative-director (2ª e última passada; não consultados: ux-designer, audio-director, unity-specialist)
Blocking items: 19 (11 de determinismo e implementação, 7 de contradição com decisão ou ADR, 1 de fórmula), mais um pacote obrigatório de texto e critérios de aceite | Recommended: 13 (vão para a OQ-17)
Summary: A lâmina (um elite por vez, Aviso só na tela, ciclo fixo do chefe, graça) e a máquina de cursores estão sólidas. Os furos estavam na desduplicação de frentes (leitura ambígua que muda o hash), no encaixe de elite e chefe sobre o herói (vetor nulo), no golpe `Rugido` (valor letal e causa da morte), na janela do `niveis_no_rugido` da F11 (o exemplo dava 7 níveis, não 2) e na promessa da maré, que o contato do #6 não sustenta. Revisado na mesma sessão com 4 decisões do autor; sem 3ª conferência, pelo limite do projeto.
Prior verdict resolved: Yes (os 9 bloqueantes da 1ª passada estavam aplicados; esta passada achou 19 novos, nenhum reabre uma decisão do autor)
Author decisions (2026-11-05, 2ª passada, todas na recomendação do creative-director): (1) a maré é espetáculo, XP e cobertura, com mais frentes nas fases densas; o dano de verdade vem da lâmina e do movimento (OQ-16 e AC-S5 medem; se falhar, pedir bloqueio ou separação ao #6); (2) o rugido sobe no máximo 1 nível (`niveis_rugido_max`), o excedente se perde e a oferta abre depois da Descarga (pedido ao #16); (3) fase em maré quase contínua: 8 a 10 waves, `respiro_max_s` 10 s, vãos de elite e o silêncio do chefe fora do `RespiroLongo`; (4) e (5) duelo garantido (`duelo_min_ticks` = graça + um ciclo de golpe, no lugar de `respiro_pos_elite_min`) e elite que não acha janela é cancelado, sem teto de segurança (`espera_elite_max` removido; `reserva_ok` na F10).
Arbitragem do creative-director: vivos por passada local única (não contadores no `SimWorld`; fecha a OQ-13 do lado do #7, a reavaliar no spike); a alternância do espelho entre ticks é aceita e medida (frente não ancorada no mundo); "segurar a fila do Tank na janela de elite" rejeitado (o `RespiroCurto` já mede).
Findings:
- [BLOCKING] Regra 7.4 / F4: "mesmo tick" indefinido, duas leituras dão hashes diferentes. Aplicado: leitura única sobre todas as frentes g<f, id inteiro de classe de vetor, escolta sem desduplicação.
- [BLOCKING] Comportamento / Regra 3: encaixe `dist² ≤ passo²` leva elite e chefe à posição do herói (investida com vetor nulo). Aplicado: `dist_parada_m`, eixo fixo de reserva, dois alvos distintos; emenda (i) ao #6 pendente.
- [BLOCKING] Regra 10.2: `Rugido` letal sem tipo (`float.MaxValue` vira infinito) e causa da morte indefinida. Aplicado: pedido tipado na frente da fila; causa do primeiro pedido que zera o HP; emenda (c) ao #6 reescrita.
- [BLOCKING] Regra 11 / F6: tick de estado lido pela escolta. Aplicado: estado do fim de t−1, espera por corpo, R11b recalculado (5732).
- [BLOCKING] F4: `float2` proibido na simulação. Aplicado: `SimVec2`.
- [BLOCKING] Regra 8: ordenação com comparador genérico em IL2CPP; contagem de vivos "contadores ou passada". Aplicado: chave `long` composta; passada local única.
- [BLOCKING] Regra 10.2: XP do rugido arredondado por morte (o Enxame de XP 1 rende 0). Aplicado: `xp_rugido_permil` inteiro, `floor` no total do tick (emenda (b) ao #3 reescrita).
- [BLOCKING] F10: validação de build usava a graça sorteada, ignorava a formação na viagem, aceitava `vel_per_s` = 0, fase só com o chefe, `escolta_por_pulso` = 0, pool com arquétipo repetido; "o chefe pode atacar" fraco. Aplicado: pior caso do pool, `formacao_max_m`, cláusulas novas no `estrutura_ok`, `graça + aviso_chefe_ticks_min < ticks_max_apos_chefe`.
- [BLOCKING] F11 / `niveis_no_rugido`: janela de XP no lugar errado (`a = xp_min − XP_rugido`). Aplicado: `pré = max(0, xp_min − XP_cheio)`, janela (pré, pré + XP_rugido]; exemplo refeito (7 níveis, o #3 aplica 1).
- [BLOCKING] Regra 14 e Tuning Knobs: contagens e pesos "podem virar remotos" contra o ADR-0002. Aplicado: nunca remotos.
- [BLOCKING] AC-D6 (hash igual Editor × aparelho) contra o ADR-0001. Aplicado: mesmo build e mesmo runtime.
- [BLOCKING] AC-E11, AC-R16, AC-E10, AC-I3b, F10, F7/F8, F9, F11, R9c, R11b, R17, contadores sem AC, AC-P4 e OQ-15 inexistentes, OQ-1/2/4/9 desatualizadas, Resumo BLOQ. Aplicado (pacote do qa-lead); `FaseTeste7` refeita (`viagem` 134, elite em 1290, `duelo_min` 90, `FaseTeste7Janelas`).
- [BLOCKING] Player Fantasy / Regra 5 / F10: a maré não pressiona (contato satura com ~3 corpos), o duelo do elite não é garantido, os números do ritmo não fecham (vãos de ~20 s, `respiro_max_s` 8 s). Aplicado conforme as decisões 1, 3, 4 e 5.
- [RECOMMENDED] Canto como refúgio, circular sem contato, curva de picos, Bruto por quantil, alcance da investida, escolta sobre o próximo Aviso, `xp_tank_est` e `dps_ref` como curva, loot do Tank, origem do orçamento de 0,3 ms, fingerprint FNV, mira ≤ 0,9 × alcance. Registrado na OQ-17, não aplicado.
Note on receipt: o #7 foi revisado depois desta revisão, por isso o alvo fica sem recibo; a próxima execução faria a revisão completa (não haverá 3ª passada). O registro foi editado na revisão (F5, F6, F10, F11, F4 e `carga_tank` sincronizados) e está carimbado na versão final.
Reviewed-Content-Hash: design/registry/entities.yaml aa940d14701b43a00d54fe00a80b8692dec8c347
Reviewed-Content-Hash: .claude/skills/design-review/SKILL.md a63d8fba9b7142eeb43791f061e2e1533c429b43
Reviewed-Content-Hash: design/gdd/combate-e-dano.md 163d47d18252f23b97e17a42b2331a5d29451dd6
Reviewed-Content-Hash: design/gdd/fluxo-de-fase.md 022ecda6c354b3fda492fca85492943bc3ebff62
Reviewed-Content-Hash: design/gdd/simulacao-deterministica.md 0114640766ff0248443a8b8608d9cb9d61b2b56b
Reviewed-Content-Hash: design/gdd/dados-e-balanceamento.md 36e6d1886f91d8c766b2e4a9a6b43fe91834a9d7
Reviewed-Content-Hash: design/gdd/game-concept.md 3a61558d87c0374c253396d6a268ac932ac062f3
