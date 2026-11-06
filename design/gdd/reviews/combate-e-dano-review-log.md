# Review Log: Combate e dano (#6)

## Review — 2026-11-05 — Verdict: MAJOR REVISION NEEDED
Review mode: full · Workflow: full
Scope signal: XL
Specialists: game-designer, systems-designer, qa-lead, gameplay-programmer, ai-programmer, performance-analyst, ux-designer; senior reviewer: creative-director (art-director, audio-director e unity-specialist não rodaram: o art-director já foi consultado na seção Visual/Audio, os sons são placeholders do #12 e o #6 não usa API da engine)
Blocking items: 8 | Recommended: 10
Summary: Os erros de fórmula são muitos, mas corrigíveis; a revisão grande vem de dois pontos. A simulação não entrega a Player Fantasy ("saí no último instante e devolvi com tudo"): andar domina a esquiva contra o elite e a punição é ×1,5 em 1 ou 2 auto-ataques. O movimento e a IA dos inimigos não estão especificados. Registro sem conflito de valor numérico; três divergências de texto (F2 [0, HP], `max_avisos` "near the hero", fonte de REACAO/JANELA). Seis decisões de jogo ficam com o autor; o resto segue a recomendação do diretor, marcado "a reavaliar".
Prior verdict resolved: First review
Findings:
- [BLOCKING] Player Fantasy, Regras 6, 8 e 10, F5, F6, l.566: andar sempre basta contra o elite (R 60 > ciclo 55), o último instante não rende nada; punição ×1,5 em auto-ataque; l.566 promete golpe pesado na Recuperação e a Regra 10 não o torna elegível a HitStop. Proposta do diretor: esquiva no limite reembolsa a recarga e abre o alvo; primeiro golpe em alvo em Recuperação vira `pesado` (×2,0 a 2,5) e o auto-ataque prioriza elite/chefe em Recuperação. [game-designer, creative-director]
- [BLOCKING] Regras 2.5, 5 e 6, tabela de estados: perseguição sem ponto de parada (oscila); horda sem separação vira um blob e o knockback de vetor nulo manda todos para +x; "em contato", alcance e direção do Aviso, recarga do elite e quem se move em cada estado indefinidos; chefe pode ficar sem vez pelo GAP; nenhum AC de movimento, E5 errado. [ai-programmer, gameplay-programmer, qa-lead]
- [BLOCKING] F9 e F10: F9 só vale com 1 atacante (3 elites matam o Tank em 18 ticks, não 134); margem de 1% no lado errado (Tank morre em 2); `mit_golpe` único para golpes de base diferente e "maior_melhor" numa janela de dois lados; ignora contato. F10 assimétrica, avaliada no início do Aviso, GAP 9 só serve até raio 0,78 m com o Tank a 0,12 m/tick; elite de referência raio 1,35 exige A ≥ 27 (registro 24); fixture-base usa 0,15 m/tick. [systems-designer, qa-lead]
- [BLOCKING] Determinismo: cura pendente (Regra 15) numa fila fora do hash atravessa o tick e o CombatHold; espaçamento de 6 ticks do contato fora do hash (l.420); knockback anda 1 tick a menos (passo 2 antes do 5: 0,5 m vira 0,3 m); i-frames lidos em dois instantes (l.136 × l.385); `mit` NaN deixa o herói imortal; F2 sem HPmax de inimigo. [gameplay-programmer, systems-designer, qa-lead]
- [BLOCKING] Contradições: R5 (10 golpes) × tabela de estados (4); R3 × E8 sobre `Esquiva`; l.566 × Regra 10; F8 3,75 hit-stops/s × art bible ≤ 3 flashes/s (N = 10 resolve). [qa-lead, ux-designer, creative-director]
- [BLOCKING] AC-P1: p95/p99 não pegam o pior tick (300 mortes de uma vez) e o cenário não gera 3 avisos; o valor em ms fica provisório até o X1 do #2. [performance-analyst]
- [BLOCKING] Classificação dos AC: E11 fora das listas da l.712; E4, I3 e R16 testam o dublê; D4 PRONTO dependendo do D3 BLOQ; reflexão não vê `double` no corpo. [qa-lead]
- [BLOCKING] Regra 8 e UI: sem buffer de esquiva; toque 2 ticks antes de a recarga zerar some e parece entrada perdida. [ux-designer, creative-director]
- [RECOMMENDED] Kite com auto-ataque dominante; decidir se é legítimo. [game-designer, ai-programmer]
- [RECOMMENDED] F7 erra nas bordas (`d_c < HP / ceil(X/gap)`); R = I+1 dá 94% de invulnerabilidade; F4 congela em vez de clamp com bônus > 3; HP_RESIDUO só vale até HP ≈ 5 243. [systems-designer]
- [RECOMMENDED] F2 Output Range e linha 151: [0, HPmax], não [0, HP]; `max_avisos` alinhar com o registro; fonte de REACAO/JANELA (l.216). [revisão principal]
- [RECOMMENDED] AC-P2 sem controle negativo; teste de escala N = 300/600/1200; dados de morte copiados na drenagem de eventos, não no frame. [performance-analyst]
- [RECOMMENDED] Quem copia `prev` ← atual durante a pausa; sem evento de início de dash nem de swing; "janela percebida 9 − 2" está errada (a latência desloca, não encurta). [gameplay-programmer]
- [RECOMMENDED] Origem da área do golpe (atacante ou herói) não definida. [game-designer]
- [RECOMMENDED] Rim da Recuperação na mesma família de cor do flash da horda; escala de dano grave; limiar de vida baixa; decal coberto pela horda; espera da oferta parece bug. [ux-designer]
- [RECOMMENDED] AC com vários GIVEN; faltam AC de `poise_ticks`, `kb_refrat`, auto-ataque com `modCadencia`, `ModForaDeFaixa`. [qa-lead]
- [RECOMMENDED] Dissolve em massa (alpha-clip, overdraw da horda, pool de fantasmas sem knob) vai para o #12 e o art-director. [performance-analyst]
- [RECOMMENDED] Interactions diz que `tickNascimento` vem do #3; Dependencies diz SimWorld; proposta: `SimWorld.Spawn` grava. [revisão principal, gameplay-programmer]
Divergências arbitradas pelo creative-director:
- Oferta de carta: game-designer (abrir na hora, retomar com contagem 3-2-1 sob CombatHold, ≥ 19 ticks) × ux-designer (abrir só com Impacto a > ~24 ticks) × systems-designer (após o teto, abrir com `ticks_ate_dano` > REACAO). Diretor: game-designer; elimina a F11 e a fila de cura fora do hash.
- Contato: ai-programmer (horda anda sempre, `contactCd` por inimigo) × qa-lead (decidir se o não escolhido gasta). Diretor: ai-programmer.
- Esquiva × andar: game-designer (reembolso) × systems-designer (R ≥ 4×I). Diretor: as duas juntas.
- Orçamento de desempenho: performance-analyst (2 ms frouxo, conflita com o X1 do #2) × GDD (knob de aceite). Diretor: medir o pior tick; ms provisório.
- Auto-ataque: GDD (mais próximo) × ai-programmer e ux-designer (priorizar elite em Recuperação). Diretor: priorizar.
Decisões de jogo pendentes do autor: recompensa da esquiva no limite; valor da punição na Recuperação; alvo do auto-ataque; como a oferta interrompe o combate; golpes aguentados por classe e por fonte (o chefe pode bater bem mais que o elite?); kite legítimo ou desestimulado.
Reviewed-Content-Hash: design/gdd/combate-e-dano.md bba3220f063460f41c4d4f35c3c8cf7c706679ad
Reviewed-Content-Hash: design/registry/entities.yaml df812874b67f3b1dfc1c98b9a526577f5ddab7ae
Reviewed-Content-Hash: .claude/skills/design-review/SKILL.md a63d8fba9b7142eeb43791f061e2e1533c429b43
Reviewed-Content-Hash: design/gdd/dados-e-balanceamento.md 97ba0623083570cfcb91bd8214350dcf96b3a1ea
Reviewed-Content-Hash: design/gdd/simulacao-deterministica.md da65d8de634c778730f3674a915380f61ed69db1
Reviewed-Content-Hash: design/gdd/fluxo-de-fase.md 03267ba2966a5daf6502a68ae46d0eb17284d881
Reviewed-Content-Hash: design/gdd/game-concept.md 3a61558d87c0374c253396d6a268ac932ac062f3
Reviewed-Content-Hash: design/art/art-bible.md 8e91b355ec554487ee8adae28798c53e069868ee

## Revision — 2026-11-05 — aplicação do veredito MAJOR REVISION NEEDED (nenhum review rodou; sem veredito novo)
Review mode: n/a (revisão pelo autor, sem especialistas) · Workflow: full
Resultado: GDD #6 revisado e marcado **In Review**; o **re-review (`/design-review`, modo full) em sessão limpa** decide APPROVED. Sem `Reviewed-Content-Hash`: nenhum review leu esta versão.
Decisões do autor (as seis perguntas do log, todas na recomendação do diretor, marcadas "a reavaliar"):
1. Esquiva no limite: a recarga volta (1 por Impacto) e o atacante fica `Aberto` até o fim da Recuperação (Regra 8; `lim_esquiva_ticks` = 3).
2. Punição: 1º golpe `pesado` em Recuperação ×2,0 (`mult_punicao_pesado`); golpe comum ×1,5; Recuperação `Aberto`: todo golpe ×2,0 (`mult_punicao_aberto`); nunca o produto (Regra 6, F1).
3. Auto-ataque: mira primeiro elite ou chefe em Recuperação, depois o mais próximo (Regra 4).
4. Oferta de carta: abre na hora, contagem 3-2-1 sob `CombatHold` na volta (Regra 16); saem `AvisoPerto`, F11 e `espera_oferta_max_ticks`.
5. Golpes aguentados: igual para elite e chefe (DPS 2, Tank 3); `mit_golpe_chefe` opcional.
6. Kite do elite: legítimo.
Bloqueios do review anterior e onde foram tratados:
- B1 (Player Fantasy, Regras 6/8/10, F5, F6): decisões 1 a 3; `pesado` decide punição e hit-stop (Regra 10); Fantasy ganhou "sair no último instante é premiado".
- B2 (movimento e IA): `dist_parada_m` e mira da horda já vinham das emendas do #7; novos: recarga de ataque `g`, "em contato" definido (Regra 5), vez do chefe no slot (Regra 6, AC-R24), knockback de vetor nulo por `EIXOS8[id mod 8]` (Regra 9, F3).
- B3 (F9 e F10): margem de 1% nos dois lados, `ttk_multi` (3 elites: 42 ticks), `mit_golpe_chefe`, janela do Tank 0,18 a 0,43, `n_Tank` como knob de aceite no lugar de `mit_golpe`; F10 simétrica e com `vel_heroi_min_tick` (GAP 9 só até raio 0,78 m; elite de referência do Tank raio 1,02, GAP 11).
- B4 (determinismo): `curaPendente`, `ultimoContatoTick`, `aberto`, `punidoPesado`, `esquivaBuf` entram no hash; i-frames lidos uma vez no início de 7a; `r` do knockback decrementa depois de aplicar (AC-R23); `mit` NaN lança; HPmax é coluna de toda entidade (F2).
- B5 (contradições): R3 e E8 alinhados (`Esquiva` só se telegraph); F8 com N = 10 (3 por segundo, 30% do tempo); linha 566 resolvida pela Regra 10.
- B6 (AC-P1): dois cenários (3 avisos ativos; pior tick de 300 mortes), p95, p99 e máximo; ms ainda provisórios até o X1 do #2 e o spike.
- B7 (classificação dos AC): E4, I3 e E11 marcados como contrato com dublê; E11 entra nas listas; D4 por analisador estático e a parte do hash fica BLOQ; `AC-R6d` duplicado virou R6g.
- B8 (buffer de esquiva): Regra 8 e UI, `buffer_esquiva_ticks` = 3 (AC-R17).
Recomendados tratados: F2 em [0, HPmax]; `max_avisos` e REACAO/JANELA alinhados ao registro; F7 com `ceil(X / gap)`; `R ≥ 3 × I`; janela de esquiva percebida corrigida (a latência desloca, não encurta). **Novos ACs:** R17 a R25, S7. **Novas OQs:** 17 (sinal visual do `Aberto`), 18 (reembolso pode virar quase invulnerabilidade, medir), 19 (contagem 3-2-1 é do #16/#2).
Não tratados (seguem recomendados): F4 congela em vez de clamp com bônus > 3; `HP_RESIDUO` só vale até HP ≈ 5 243; AC com vários GIVEN; AC de `poise_ticks`, `kb_refrat` e `ModForaDeFaixa`; dissolve em massa (vai ao #12); `tickNascimento` gravado por `SimWorld.Spawn`; origem da área do golpe.
Pendências em outros docs (nenhuma aplicada): #16 (abrir na hora, contagem 3-2-1, Soft); #3 (somar `curaPendente`); #7 (parar de ler `aviso_perto`, declarar `g`); #2 (`DeathCause.Rugido` segue pendente); #1 (knobs novos, `R ≥ 3 × I`, `n_Tank`); #10 (`mit_golpe_chefe`); ADR das colunas do `SimWorld` (cinco colunas novas); art-director (OQ-17). Registro: +`lim_esquiva_ticks`, +`buffer_esquiva_ticks`; `aviso_perto` deprecated; fórmulas dano_final, esquiva_coerente, contato_maximo, folga_de_golpes, intervalo_entre_impactos e orcamento_hitstop sincronizadas (`registry.sh validate` limpo).
