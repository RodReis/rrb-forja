# Review Log: game-concept.md

## Review — 2026-11-03 — Verdict: NEEDS REVISION
Review mode: full · Workflow: full
Scope signal: XL
Specialists: game-designer, economy-designer, systems-designer, qa-lead, creative-director (senior)
Blocking items: 10 | Recommended: 9 grupos (atribuídos a GDDs futuros)
Summary: a fantasia, os pilares, os anti-pilares e o gancho estão sólidos. O conceito, porém, não definia o objeto selado. Por isso o Grimório saturava (o protótipo chegou a 11 de 12 skills), o que vinha depois do selo era indefinido e o Princípio de Negócio tinha buracos de execução (Livro, reforja por nerf, entradas, escopo herói/conta). Os critérios do MVP não podiam reprovar. O CD aceitou a correção do game-designer sobre a L36: o problema é "power fantasy sem custo de conquista", e o remédio é escassez, não menos poder.
Prior verdict resolved: First review
Completeness note: avaliado contra o template de conceito (todas as seções presentes). O padrão de 8 seções de GDD de sistema não se aplica; `gdd-structure-check.sh` não distingue conceito de GDD de sistema.
Findings:
- [BLOCKING] Core Mechanics / Core Loop: Grimório sem escassez (registro automático satura).
- [BLOCKING] Core Loop / Content Volume / MVP: ambíguo qual chefe registra (L126 vs L309 vs L370).
- [BLOCKING] Core Mechanics (L78): o selo fixava "skills e o set", contradizendo a perseguição de set pós-selo; momento da escolha de função indefinido.
- [BLOCKING] Core Loop: loop pós-selo indefinido (cartas de level up nas dungeons?).
- [BLOCKING] Long-Term Progression: escopo herói vs conta indefinido (slot extra = respec grátis).
- [BLOCKING] Pillar 3: uso solo de skill de função corrói o pilar; companheiros NPC tornam a função irrelevante.
- [BLOCKING] Pillar 2 / Princípio de Negócio: Livro de Reforja vendido sem teto e reforja grátis em "toda alteração" são exploráveis.
- [BLOCKING] Princípio de Negócio / Anti-Pillars: sistema de entradas inexistente; varredura sem teto.
- [BLOCKING] MVP Definition: nenhum critério de aceite podia reprovar (performance sem aparelho, métrica nem janela; Android não instalado; Tank e hipótese subjetivos; arte de loja vs custo por peça).
- [BLOCKING] Next Steps / doc: achados do protótipo ausentes; Next Steps desatualizado.
- [RECOMMENDED] GDD do Grimório: registros < N, evoluções, profundidade de nível, loop do favorecer.
- [RECOMMENDED] GDD do Selamento: eixo de identidade com retorno mecânico, lockouts, níveis.
- [RECOMMENDED] GDD de Economia: sinks, material na morte, pity, simulador headless; modelo de negócio antes deste GDD.
- [RECOMMENDED] GDD de Poder de Combate / Ranking: fórmula, porta suave, affixes por função, métrica de diversidade.
- [RECOMMENDED] GDD de Sets e Forja: sets de arquétipo por função.
- [RECOMMENDED] UX/Onboarding: telegraph, números de dano, notificação do Grimório mensuráveis.
- [RECOMMENDED] Producer: âncora D0 e definição de pronto.
Decisions taken by the user (applied in the same session, pending re-review):
1. Escassez: escolher 1 a 2 skills por chefe de fase, com nível mínimo ou evoluída.
2. Pós-selo: só as seladas, e o level up as modifica.
3. Grimório por herói, com o Códex na conta.
4. O selo fixa só as skills; a função é escolhida na criação.
5. O chefe de fase registra.
6. Slots de função (2+2); companheiros são os outros heróis selados ou NPC com teto.
7. Livro vendido com teto por temporada somando todas as fontes; reforja grátis só em nerf líquido.
8. Sem energia, com teto diário por fonte.
Default applied (CD recommendation): o Poder de Combate vem só de equipamento e nível.
Receipt note: as linhas abaixo carimbam as versões **revisadas** (commit 9f40906), não o documento já editado. O próximo `check` deve ler CHANGED e disparar uma revisão completa.
Reviewed-Content-Hash: design/gdd/game-concept.md 8406f8021395daa7c2f5dbaa8c9f61586138192b
Reviewed-Content-Hash: design/registry/entities.yaml dfeacb02917f751cb1dfd88cf490c7ec3d8d2d0f
Reviewed-Content-Hash: .claude/skills/design-review/SKILL.md a63d8fba9b7142eeb43791f061e2e1533c429b43
Reviewed-Content-Hash: prototypes/grimorio-concept/REPORT.md dc311a9eb09c70bcf0ef847fc9e1063447c4e84c

## Review — 2026-11-03 (re-review) — Verdict: NEEDS REVISION
Review mode: full · Workflow: full
Scope signal: XL
Specialists: game-designer, economy-designer, systems-designer, qa-lead, creative-director (senior)
Blocking items: 5 | Recommended: 5 grupos (atribuídos aos GDDs de Grimório, Selamento, Economia, Skills e ao doc de aceite do MVP)
Summary: as 8 decisões da 1ª revisão foram aplicadas e resolveram 6 dos 10 bloqueadores (2, 3, 5, 7, 8, 10). Combinadas, as decisões 1, 2, 6 e 7 abriram três buracos: o Grimório satura mesmo sem replay (2 registros por chefe cobrem 91-100% do pool), o selo pode travar o herói sem 2 skills de função e a reforja por nerf fica sem alternativa porque o Grimório é escasso e congela no selo. Somam-se a oferta do Livro (rara × "comprar não aumenta a frequência") e critérios do MVP que passam por construção. A fantasia, os pilares e os anti-pilares seguem de pé.
Prior verdict resolved: Partial (6 resolvidos; 1, 4, 6 e 9 parciais, cobertos por B1, B2, B3 e B5)
Completeness note: avaliado contra o template de conceito; o padrão de 8 seções de GDD de sistema não se aplica.
Findings:
- [BLOCKING] Core Mechanics / Core Loop: Grimório sem limite cumulativo; "1 a 2 à escolha" degenera em 2; satura na 1ª passada.
- [BLOCKING] Core Mechanics / Long-Term Progression: softlock no selo sem 2 skills de função (L149).
- [BLOCKING] Pillar 2: reforja grátis por nerf sem alvo com Grimório escasso e congelado.
- [BLOCKING] Pillar 2 / Princípio de Negócio: Livro "raro" + teto deixa a compra aumentar a frequência; "temporada" inexistente no lançamento.
- [BLOCKING] MVP Definition: L397 tautológica, L398 sem limiar e medindo o testador, L399 com unidades misturadas e faixa degenerada, simulação headless fora do MVP.
- [RECOMMENDED] Texto: modelo de negócio afirmado como F2P, companheiros NPC desatualizados, exemplo impossível na L201, L151 vs Livro vendido, "teto de entradas".
- [RECOMMENDED] GDD do Grimório: nível mínimo 2-5 e regra para E = 0, re-registro, peso do favorecer ≤ 4, ≥ 5 skills por função, evoluções, glossário dos 3 níveis.
- [RECOMMENDED] GDD do Selamento: ritual vira confirmação, Livro sem alvo, reforja por nerf fora do teto e 1 por patch com métrica publicada.
- [RECOMMENDED] GDD de Economia: escopo do teto diário (conta/herói, por categoria), XP de varredura, relógio offline, ticket de varredura (cortar), sinks terminais.
- [RECOMMENDED] GDD de Skills / doc de aceite do MVP: ~60 modificadores pós-selo ou re-leveling; knobs com commit antes de D0, campos do log, orçamento de farm, [H]/[X]/[Y].
Disagreements arbitrated by the CD: replay → capacidade C com substituição (não "só o 1º clear"); softlock → garantia no chefe (não skill "não conquistada"); modelo de negócio → só a contradição de texto é obrigatória, a decisão fica nas Open Questions; qa-lead → parte é do conceito (B5), parte do doc de aceite do MVP; evoluções → RECOMMENDED, com uma linha de invariante.
Decisions taken by the user (all CD recommendations, applied in the same session, pending re-review):
1. B1: Grimório com capacidade C (knob, ~6) e substituição; R = 1 por chefe, fixado pelo design; o chefe de capítulo não registra.
2. B2: garantia de skill de função no chefe quando o Grimório tem < 2; a substituição nunca baixa de 2.
3. B3: a reforja grátis por nerf escolhe em todo o pool do tipo de slot; o Livro fica restrito ao Grimório.
4. B4: 1 cópia conquistável garantida por herói por período (objetivo, não drop); teto 1; a loja só antecipa; L231 ganha "nem a velocidade de obter algo que conta para o ranking".
5. B5: rubrica e limiar com commit antes de D0, classificados por um avaliador cego (agente).
Receipt note: o conceito revisado era a cópia de trabalho não commitada, editada nesta mesma sessão antes que pudesse ser carimbada. Por isso este registro **não** carimba design/gdd/game-concept.md: o carimbo mais recente continua sendo o da 1ª revisão (commit 9f40906), e o próximo `check` lê CHANGED e dispara uma revisão completa, como deve.
Reviewed-Content-Hash: design/registry/entities.yaml dfeacb02917f751cb1dfd88cf490c7ec3d8d2d0f
Reviewed-Content-Hash: .claude/skills/design-review/SKILL.md a63d8fba9b7142eeb43791f061e2e1533c429b43
Reviewed-Content-Hash: prototypes/grimorio-concept/REPORT.md ef64cc8638c4f4b904c03659f10202a824948b3e

## Review — 2026-11-03 (2º re-review) — Verdict: NEEDS REVISION
Review mode: full · Workflow: full
Scope signal: XL
Specialists: game-designer, economy-designer, systems-designer, qa-lead, creative-director (senior)
Blocking items: 5 | Recommended: 6 grupos (GDDs de Grimório, Selamento, Economia, Skills, Ranking e doc de aceite do MVP)
Summary: nenhum dos 5 bloqueadores anteriores fechou por completo. Com R = 1, K = 5 e C ≈ 6, o Grimório do MVP nunca enche, então a substituição não é testada e os critérios (b), (c) e (d) davam o resultado por construção. "O selo é sempre possível" era falso (garantia ambígua, nenhuma regra para "sem elegível", selo com < 4). A reforja por nerf no pool inteiro e o Livro sem alvo quebravam o teste da fantasia, e vender a antecipação do Livro feria a L232. O CD reverteu duas arbitragens próprias (B3 nerf no pool inteiro, B5 avaliador cego como gate) e pediu que a passada deixasse o texto menor. A fantasia, os pilares e o gancho seguem de pé.
Prior verdict resolved: Partial (B1-B5 todos parciais, cobertos pelos novos B1-B5)
Completeness note: avaliado contra o template de conceito; o padrão de 8 seções de GDD de sistema não se aplica.
Findings:
- [BLOCKING] Core Mechanics / MVP Definition: escassez não exercitada no MVP; L402 (b)(c)(d) por construção.
- [BLOCKING] Core Mechanics / Long-Term Progression: "o selo é sempre possível" falso (garantia, sem elegível, < 4 skills).
- [BLOCKING] Pillar 2: reforja por nerf entrega skill não conquistada; Livro com ≤ C−4 alvos, muitas vezes 0.
- [BLOCKING] Pillar 2 / Princípio de Negócio: antecipação vendida = velocidade de algo que conta para o ranking.
- [BLOCKING] MVP Definition: vsync na performance, aparelho sem classe, N sem teto, pigeonhole dos 3 heróis, identidade mede o designer, colchetes sem pior valor, arte sem mínimo de peças.
- [RECOMMENDED] Texto: pitch "a build que funciona", "trindade" com 4 funções e Mago sem verbo, ganchos pós-selo, anti-pilar de materiais, IAP como fato.
- [RECOMMENDED] GDD do Grimório: nível mínimo 2-3, ordem das operações, registro opcional, skill substituída queimada, favorecer só não registradas, C do lançamento.
- [RECOMMENDED] GDD do Selamento: detalhes da run de reforja, exclusões do nerf (buffadas no patch, taxa de escolha X).
- [RECOMMENDED] GDD de Economia: período ≥ N semanas no relógio do servidor, Livro vinculado ao herói, objetivo de participação, escopo do teto, cortar ticket.
- [RECOMMENDED] GDD de Skills / Ranking: papel do Mago, slots ociosos pós-selo, ranking por herói ou conta.
- [RECOMMENDED] Doc de aceite do MVP: políticas P1-P4, proxies, seed do hash, fluxos aleatórios separados, classificação cega dos tiers, registro de bugs do marco.
Disagreements arbitrated by the CD: página por chefe (game-designer) rejeitada, mantida a capacidade C com o invariante K > C; garantia híbrida (gatilho no nível de selamento, skill de função de maior nível da run, sem sorteio no pool); run de reforja em vez de troca fina; identidade como sinal (qa-lead) em vez de gate comportamental. O CD sugeriu um re-review só dos parágrafos alterados; a skill proíbe re-review parcial, então o próximo é completo.
Decisions taken by the user (all CD recommendations, applied in the same session, pending re-review):
1. D1: C = 5 no MVP; o selo abre antes do chefe de capítulo, com ~7 vitórias (5 fases + 2 replays); o chefe de capítulo é a Prova do Selo.
2. D2: run de reforja para o Livro e para o nerf; o nerf fica fora do teto, 1 por skill por patch.
3. D3: o Livro nunca é vendido.
4. D4: identidade e sessões de 20 min não validáveis com n = 1, rebaixadas a sinais.
Also applied: alvo de 60 fps com métrica por percentil, classe "Android intermediário", proxies com orçamento, piores valores (N ≤ 2, tentativas ≤ 3, razão ≤ 1,5, z = 25% proposto pelo main review e aprovado, ≥ 6 peças), Mago com o verbo "controle".
Receipt note: como na passada anterior, este registro **não** carimba design/gdd/game-concept.md (a cópia de trabalho foi editada nesta sessão). O próximo `check` lê CHANGED e dispara uma revisão completa.
Reviewed-Content-Hash: design/registry/entities.yaml dfeacb02917f751cb1dfd88cf490c7ec3d8d2d0f
Reviewed-Content-Hash: .claude/skills/design-review/SKILL.md a63d8fba9b7142eeb43791f061e2e1533c429b43
Reviewed-Content-Hash: prototypes/grimorio-concept/REPORT.md ef64cc8638c4f4b904c03659f10202a824948b3e

## Review — 2026-11-03 (3º re-review) — Verdict: NEEDS REVISION
Review mode: full · Workflow: full
Scope signal: XL
Specialists: game-designer, systems-designer, economy-designer, qa-lead, creative-director (senior)
Blocking items: 7 | Recommended: 5 grupos (texto do conceito, GDDs de Grimório, Selamento e Economia, doc de aceite do MVP)
Summary: a raiz comum é que o selo abria por nível (XP). Mortes, auto e varredura levavam ao selo com poucas vitórias, contornavam K > C e faziam o invariante do simulador passar por construção. A garantia tinha um softlock duro (queima + pool de função pequeno), e três métricas do MVP mais o critério do Tank passavam por construção. O CD considera que os bloqueadores são de regra, não de identidade, e pede que esta seja a última passada de regra no conceito.
Prior verdict resolved: Partial (D1-D4 aplicados; a passada abriu os buracos de K por XP, da garantia e das métricas)
Completeness note: avaliado contra o template de conceito; o padrão de 8 seções de GDD de sistema não se aplica.
Findings:
- [BLOCKING] Core Mechanics: selo por nível; XP de morte, auto e varredura contorna K > C.
- [BLOCKING] Core Mechanics: "toda vitória tem registro" falso; softlock com queima; troca forçada pelo fallback.
- [BLOCKING] Pillar 2: "a trocada volta ao Grimório" estoura C; Grimório pós-selo indefinido.
- [BLOCKING] MVP Definition: mediana de selos ≥ 3 e ≥ 70% passam por construção; ≤ 60% sem política.
- [BLOCKING] MVP Definition: Tank N ≤ 2 vazio; razão de tempo por construção com waves por timer.
- [BLOCKING] MVP Definition: [350], [X] e [Y] sem pior valor; entradas de H sem commit.
- [BLOCKING] Pillar 2: nerf em passiva dá até 4 reforjas (respec grátis).
- [RECOMMENDED] Texto: L429 com Sinais sem PASS, linha exata "mesmo conteúdo", risco de pacing.
- [RECOMMENDED] GDD do Grimório: slots na fase (testar 4), origem guardada em cada entrada.
- [RECOMMENDED] GDD do Selamento: Livro consumido ao entrar na run.
- [RECOMMENDED] GDD de Economia: período ≥ 4 semanas, auto e varredura ≤ [80]% do teto, cortar o ticket.
- [RECOMMENDED] Doc de aceite do MVP: piso dos proxies, teto de GPU, S1 com registro de bugs, VS e "uma run", rubrica de "distinguíveis", políticas.
Disagreements arbitrated by the CD: K_min = C + 2 (economy queria C + 1), substituindo o nível; sem queima (systems e L376 queriam queima), aceitando a troca ilimitada com o selo adiado; Grimório fecha no selo (contra arquivo com queima e capacidade C − 4); métrica de 90% do poder (contra métricas de troca); Tank ≤ 9 tentativas; nerf 1 por herói por patch (systems: 2); período de 4 semanas (systems: 2); US$ 350 (systems: 400).
Decisions taken by the user (all CD recommendations, applied in the same session, pending re-review):
1. O selo abre com K_min = C + 2 vitórias de chefe de fase (7 no MVP); o nível de selamento é só o teto antes do selo.
2. Sem queima: a substituída volta ao pool; troca opcional com o Grimório cheio; garantia em K_min (suspende o nível mínimo e, se faltam skills de função, a fase começa com 1 ativa). Extensão do main review: a garantia também cobre < 4 skills.
3. O Grimório fecha no selo; a reforja oferece o pool do tipo menos as seladas.
4. Métricas, Tank, colchetes e nerf conforme o CD.
Receipt note: como nas passadas anteriores, este registro **não** carimba design/gdd/game-concept.md (a cópia de trabalho foi editada nesta sessão). O próximo `check` lê CHANGED e dispara uma revisão completa.
Reviewed-Content-Hash: design/registry/entities.yaml dfeacb02917f751cb1dfd88cf490c7ec3d8d2d0f
Reviewed-Content-Hash: .claude/skills/design-review/SKILL.md a63d8fba9b7142eeb43791f061e2e1533c429b43
Reviewed-Content-Hash: prototypes/grimorio-concept/REPORT.md ef64cc8638c4f4b904c03659f10202a824948b3e

## Review — 2026-11-03 (4º re-review) — Verdict: NEEDS REVISION
Review mode: full · Workflow: full
Scope signal: XL
Specialists: game-designer, systems-designer, economy-designer, qa-lead, unity-specialist, performance-analyst, creative-director (senior)
Blocking items: 6 | Recommended: 8 grupos (GDDs de Grimório, Selamento e Economia, ADR técnico, doc de aceite do MVP, texto condicional)
Summary: o padrão das 4 passadas não é de má regra, e sim de má localização. Nenhum achado tocou a fantasia, os pilares ou o gancho; os bloqueadores saem de texto de GDD do Grimório e de protocolo de aceite colocados no conceito, e cada regra numérica nova abriu de 4 a 7 buracos. O CD assumiu o erro da 3ª revisão (pediu a "última passada de regra" e ela acrescentou regra) e mandou corrigir por subtração: o conceito não afirma nada falso, e a metodologia vai para o doc de aceite do MVP. O invariante de selabilidade de L407 era falso (o selo exige ≥ 4 skills, o registro é opcional, g = 0 ou 1 precisa de 4 ou 3 vitórias).
Prior verdict resolved: Partial (o selo por nível, a queima e o Livro foram resolvidos; K_min = C + 2 abriu o buraco de g, e as métricas e o Tank seguiam passando por construção)
Completeness note: avaliado contra o template de conceito; o padrão de 8 seções de GDD de sistema não se aplica.
Findings:
- [BLOCKING] Core Mechanics / MVP Definition: invariante de selabilidade falso (L81, L149-150, L397, L407); o limite correto é max(0, 4 − g, 2 − f), no máximo 4.
- [BLOCKING] MVP Definition: "~15 skills" pode incluir passivas; o pool da função não estava definido; o abort da checagem de setup deixava o MVP fechar sem Escassez.
- [BLOCKING] Core Mechanics / MVP Definition: sem piso de C (C ≤ 3 impede o selo; C = 4 faz o Grimório ser o selo).
- [BLOCKING] MVP Definition: métricas de oferta por construção (função de poder circular, elegibilidade com nível mínimo baixo); Tank com ≤ 9 tentativas reprovava pela escolha de registro.
- [BLOCKING] Princípio de Negócio: "linha exata" só cobria "por dia"; ticket de varredura contradizia a linha; reforja grátis por nerf sem limite de cadência (~25 trocas por herói por ano).
- [BLOCKING] MVP Definition: o doc de aceite do MVP não existe, não tem caminho nem item no Next Steps, e "commit antes de D0" não era verificável.
- [RECOMMENDED] Texto: L154, L243, L326, L349 (lista NOT SOURCEABLE incompleta), L364 e L413 afirmavam como fato o que está em aberto. Aplicado.
- [RECOMMENDED] GDD do Grimório: grind pela fase mais fácil (chefe reaproveitado, troca ilimitada), skill de nível 1 dada pela garantia, favorecer só as já registradas (L145 sem alavanca), loop e XP pós-selo.
- [RECOMMENDED] GDD do Selamento: a run de reforja pode terminar sem substituta elegível; o Livro só deve ser consumido quando a substituta sela.
- [RECOMMENDED] GDD de Economia: teto de heróis, critério de "conquistados jogando", força dos companheiros no ranking.
- [RECOMMENDED] ADR técnico: PRNG em C# puro com matemática inteira (Mono × IL2CPP), Burst × classes puras, Render Graph, asmdef do Grimório.
- [RECOMMENDED] Doc de aceite do MVP: frame time e vsync (60 Hz, métrica = intervalo entre frames apresentados), janela de reinício, "inimigos ativos", 3 execuções a frio, térmico, proxies com piso (mediana de 3 assets de loja), colunas do CSV, registro de bugs, "distinguíveis" e "uma run".
Disagreements arbitrated by the CD: invariante → relaxar o limite (as alternativas que mudam a regra ficaram com o usuário); C = 5 mantido (o game-designer sugeriu C = 6, o risco do selo "qual das 5 descartar" vai para o GDD do Selamento); Tank → "≤ [2] mortes" (nem a proposta do systems-designer nem a do qa-lead); métricas de oferta saem inteiras do conceito (o main review as mantinha com as definições no doc); nerf → por período (REVERTE a arbitragem do próprio CD na 3ª revisão, "1 por herói por patch"); ticket de varredura → cortar.
Decisions taken by the user (applied in the same session, pending re-review):
1. Invariante: relaxar o limite para ≤ max(0, 4 − g, 2 − f) vitórias, no máximo 4 (recomendação do CD).
2. Nerf: máx. 1 reforja grátis por herói por período, sem acumular entre patches (recomendação do CD; reverte "por patch").
Also applied (CD, sem pergunta): setup 5 ≤ C ≤ |pool| − 4; ~15 skills ativas (5 + 5 + 5); métricas de oferta e política movidas para o doc de aceite (`docs/acceptance/mvp.md`); L404 reduzida a alvo e PASS (≥ 95% dos frames ≤ 17,5 ms); L405 com mortes; ticket de varredura apagado; "linha exata" com período e temporada; recompensa de canal pago nunca contém Livro, slot, material nem reforja; D0 só depois do commit do doc de aceite; item novo no Next Steps.
Caveats: (1) o conceito NÃO ficou menor (55.744 → 56.711 bytes, +1 linha), então o sinal de sucesso que o CD definiu para a 5ª revisão não está atendido por tamanho; (2) L404 manteve o PASS de frame time (o CD mandou o conceito não repetir o item de performance), e as ressalvas do performance-analyst (vsync, execução única) estão só apontadas para o doc de aceite; (3) os alinhamentos L37 × L130 e L135 × L145 ficaram para o GDD do Grimório.
Rule for the next review (CD): checar só duas coisas, que nenhuma frase do conceito é falsa e que o doc de aceite está agendado antes de D0. Achado de regra novo vai por padrão ao GDD correspondente ou ao doc de aceite, sem bloquear.
Receipt note: como nas passadas anteriores, este registro **não** carimba design/gdd/game-concept.md (a cópia de trabalho foi editada nesta sessão). O próximo `check` lê CHANGED e dispara uma revisão completa.
Reviewed-Content-Hash: design/registry/entities.yaml dfeacb02917f751cb1dfd88cf490c7ec3d8d2d0f
Reviewed-Content-Hash: .claude/skills/design-review/SKILL.md a63d8fba9b7142eeb43791f061e2e1533c429b43
Reviewed-Content-Hash: prototypes/grimorio-concept/REPORT.md ef64cc8638c4f4b904c03659f10202a824948b3e

## Review — 2026-11-03 (5º re-review) — Verdict: NEEDS REVISION
Review mode: full · Workflow: full
Scope signal: S (a revisão do conceito; a implementação do jogo segue XL)
Specialists: game-designer, systems-designer, economy-designer, qa-lead, unity-specialist, performance-analyst, creative-director (senior)
Blocking items: 6 | Recommended: 6 grupos (doc de aceite do MVP, ADR técnico, GDDs de Grimório, Selamento e Economia)
Summary: nenhum achado tocou a fantasia, os pilares ou o gancho. Os 6 bloqueadores eram frases falsas ou fora de ordem, todos resolvidos por edição de uma linha. O único não cosmético foi L80: a cláusula "nenhuma troca deixa menos de 2 skills de função" tornava falso o limite de selabilidade da 4ª passada (g = 5, f = 0 é alcançável e bloqueava toda troca). O conserto foi apagar a cláusula, não acrescentar regra. O critério (b) do CD (doc de aceite agendado antes de D0) estava atendido.
Prior verdict resolved: Partial (o invariante de selabilidade foi relaxado, mas a cláusula de L80 o contradizia; as métricas de oferta e o Tank saíram do conceito como pedido)
Completeness note: avaliado contra o template de conceito; o padrão de 8 seções de GDD de sistema não se aplica. O registro (`design/registry/entities.yaml`) não tem entradas, então nenhum valor foi cruzado.
Findings:
- [BLOCKING] Core Mechanics (L80, L407): "nenhuma troca deixa menos de 2 skills de função" contradiz L81/L407 (softlock em g = 5, f = 0). Cláusula e invariante apagados.
- [BLOCKING] Core Mechanics (L81): a garantia podia dar skill de função já registrada. Agora "ainda não registrada".
- [BLOCKING] Core Identity (L26) contra Scope Tiers (L424): prazo 16 a 20 contra 13 a 20 meses. L26 alinhada.
- [BLOCKING] L12, L45, L387: "para sempre" falso (reforja repetível, L189-191). Apagado nas três.
- [BLOCKING] Core Loop (L133): "nunca skills novas" contra a run de reforja (L189). Apagado.
- [BLOCKING] Next Steps (L456) contra L404/L430: spike com duas agendas. Doc de aceite subiu para antes de "Prototipar"; spike agendado em "semanas 1 a 3 após D0".
- [RECOMMENDED] Doc de aceite: definição de "morte" e janela de contagem do Tank, replays só de fase distinta, "inimigo ativo", vsync/Hz e p99,9 de frame time, busca exaustiva na grade (g, f) no lugar de 100 seeds, definição de H, onde D0 é registrada (commit que cria `production/milestones/mvp.md` com o doc como ancestral), limiar de PASS de frame time.
- [RECOMMENDED] ADR técnico: lista NOT SOURCEABLE de L349 incompleta (VAT, instancing skinned, Jobs/Burst em IL2CPP, overdraw e térmico, hitches Adreno/Mali), PRNG próprio, `targetFrameRate` e `vSyncCount`, asmdef do código do jogo, "sem reescrita" (L327) só vale se o servidor rodar C#.
- [RECOMMENDED] GDD do Grimório: "o registro é escasso" (L39) não está provado (C = 5 de pool 10 enche na 5ª vitória); skill de nível 1 dada pela garantia contradiz "conquistada"; pool com ≥ 9 skills para dar folga a C = 5.
- [RECOMMENDED] GDD do Selamento: "sempre existe alvo" (L189) é apertado (oferta pode ter < 3 cartas); "pela mesma regra de registro" soa a registro em Grimório fechado; termo "lockout de ranking" contra "lockout de selo".
- [RECOMMENDED] GDD de Economia: "e dungeons" em L234 deixa passar venda de entradas; L246 "um pouco menor" contra L378 "≤ [80]%"; "reset raro e custa" (L186) sem custo definido; L413 não valida as consequências do Pilar 2.
- [RECOMMENDED] MVP Definition: L431 "trindade de companheiros" é marco do Vertical Slice, não do MVP; L408 "2 tiers" contra "3 raridades"; L422 "2,5 a 4,5 meses" entra no vermelho acima de 4.
Disagreements arbitrated by the CD: Q2 (onde D0 é registrada; qa-lead: bloqueador) → rebaixado a doc de aceite e /gate-check, porque o critério (b) pede só "agendado". E2 (teto diário contra L371; economy-designer: bloqueador) → rebaixado, com micro-correção "valor do teto" em L371. E3 ("lockout de ranking"; economy-designer: bloqueador) → rebaixado, vai ao glossário do GDD do Selamento. Cortes de tamanho do game-designer: aceitos L443 e "uns 60" de L362; rejeitados Retention Hooks, Key Dynamics, Full Vision e o 2º parágrafo de L37 (seções do template e justificativa da fantasia), com corte só do parêntese "(a coleção de legados…)". L404: opção B (alvo mais ponteiro; o PASS vai ao doc de aceite).
Decisions applied in the same session (user chose "Revisar agora"; every CD recommendation, subtraction only): as 6 correções acima; L404 reduzida (B); L403 enxuta; antiga L443 apagada (duplicava o REPORT.md); "se cada vitória registrar" apagado em L364 e L397; L6 e L458 viraram ponteiros ao log; L371 com "valor do". O arquivo foi de 56.711 para 55.471 bytes (466 linhas), medido com `wc`: o sinal de tamanho do CD está atendido.
Caveats: (1) o CD sugeriu que a 6ª passada "cheque só o diff"; a skill proíbe re-review parcial, e o recibo lê CHANGED, então será completa. (2) A estimativa do CD de ~55,3 KB não era medida; a medida real é 55.471 bytes. (3) Os achados RECOMMENDED acima ainda não têm dono no repositório: o doc de aceite e os GDDs não existem.
Rule for the next review (CD): checar só se alguma frase do conceito ficou falsa depois destas edições e se o doc de aceite segue agendado antes de D0. Achado de regra novo vai ao GDD ou ao doc de aceite, sem bloquear.
Receipt note: como nas passadas anteriores, este registro **não** carimba design/gdd/game-concept.md (a cópia de trabalho foi editada nesta sessão). O próximo `check` lê CHANGED e dispara uma revisão completa.
Reviewed-Content-Hash: design/registry/entities.yaml dfeacb02917f751cb1dfd88cf490c7ec3d8d2d0f
Reviewed-Content-Hash: .claude/skills/design-review/SKILL.md a63d8fba9b7142eeb43791f061e2e1533c429b43
Reviewed-Content-Hash: prototypes/grimorio-concept/REPORT.md ef64cc8638c4f4b904c03659f10202a824948b3e

## Review — 2026-11-03 (6º re-review) — Verdict: NEEDS REVISION
Review mode: full · Workflow: full
Scope signal: S (a revisão do conceito; a implementação do jogo segue XL)
Specialists: game-designer, systems-designer, economy-designer, qa-lead, unity-specialist, performance-analyst, creative-director (senior)
Blocking items: 4 | Recommended: 5 grupos (conceito em uma linha, GDDs de Grimório, Selamento e Economia, ADR técnico, doc de aceite do MVP)
Summary: nenhum achado tocou a fantasia, os pilares, o gancho ou a hipótese do MVP. Os 4 bloqueadores eram frases falsas ou fora de ordem, todos resolvidos por edição de uma linha. O CD diagnosticou de novo que o texto de regra do Grimório (L80, L81 e o invariante de L407) é especificação de GDD no lugar errado, e que cada edição nele abre um caso de borda novo. O critério (b) do CD (doc de aceite agendado antes de D0) estava atendido; a ordem do Next Steps era o que estava errada.
Prior verdict resolved: Partial (os 6 bloqueadores da 5ª passada foram resolvidos; a cláusula "se arma em K_min" e o "escolhe 1 delas" deixaram duas frases contraditórias com o invariante e com o registro opcional)
Completeness note: avaliado contra o template de conceito; o padrão de 8 seções de GDD de sistema não se aplica. Nenhum dos GDDs citados existe, nem design/gdd/systems-index.md nem docs/acceptance/mvp.md. O registro (design/registry/entities.yaml) tem 0 entradas, então nenhum valor foi cruzado.
Findings:
- [BLOCKING] Core Mechanics (L81): "não é selável em K_min" não cobre estados com ≥ K_min vitórias; trocar uma skill de função (g = 5, f 2 para 1) deixava o limite falso sem garantia. Agora "a partir de K_min".
- [BLOCKING] Core Loop (L132) e Long-Term Progression (L149): "escolhe 1 delas para registrar" lia-se como registro obrigatório, contra L80/L81. Agora "pode registrar" e "escolhe se registra".
- [BLOCKING] Princípio de Negócio (L234): a linha exata proibia compra que aumente "recompensas por dia, período ou temporada", mas L236/L238 admitem passe e pacote pagos (cosméticos). Agora "recompensas não cosméticas".
- [BLOCKING] Next Steps (L464-466): /sprint-plan new (que marca D0) vinha depois de /vertical-slice (D0 + 10 meses), e o spike (D0 + 1 a 3 semanas) aparecia acima. Agora sprint-plan, spike, vertical slice, nessa ordem.
- [RECOMMENDED] Conceito (uma linha): L82/L150/L37/L45 "É definitivo; a run de reforja troca…" se contradiz na mesma frase; L398 (3 raridades) × L408 (2 tiers); L422 (até 4,5 meses) × vermelho acima de 4 em L429; L349 sem VAT, instancing skinned, Jobs/Burst em IL2CPP, overdraw, térmico, Adreno/Mali, Render Graph no 6.3; L406 (≥ 1 Tank e ≥ 1 DPS selados) sob "sem bloquear"; L6 autorreferente; L246 × L378; L371; L396 sem dizer se suprema e racial entram em "5 de função".
- [RECOMMENDED] GDD do Grimório: o selo é "descartar 1 de 5" (155 combinações possíveis, no máximo 5 por Grimório); "o registro é escasso" (L39) não provado; a garantia registra skill de nível 1; o chefe reaproveitado esvazia "registrada contra um chefe"; evolução com mais de 1 slot pode falsear o invariante; F ≥ 2 na checagem de setup.
- [RECOMMENDED] GDD do Selamento e da Economia: arbitragem de nerf; até ~26 trocas por ano por herói; objetivos do Livro e do slot só no manual; DLC de capítulos × teto por fonte; moeda comprável fora dos anti-pilares.
- [RECOMMENDED] ADR técnico: "sem reescrita" (L327) só vale se o servidor rodar C# com a mesma simulação determinística; asmdef do Grimório; Render Graph em URP mobile no 6.3; fallback de fps por térmico.
- [RECOMMENDED] Doc de aceite: janela de medição (minuto 20, 3 execuções a frio, minuto 40 a 60, temperatura, bateria); orçamento de proxy de herói (piso × teto); "VFX no máximo" e "distinguíveis"; exaustão da grade (g, f) no lugar de 100 seeds; política de registro do Tank (até 11 vitórias no pior caso); gate do chefe de capítulo; Android API ≥ 24 e módulo Android no editor 6000.3.27f1 com IL2CPP; testcasecount > 0; métrica "selo = confirmação" (se passar de X%, C = 6); onde D0 é registrada; [80]% e K_min sem pior valor.
Disagreements arbitrated by the CD: B1 (L33 × L82, "cada skill foi conquistada") → rebaixado, a frase é a fantasia na voz do jogador e L37 dá a versão operacional. B2 (L389, "valida o custo de conquista pela simulação"; game-designer e qa-lead queriam reescrever) → frase mantida, a condição vai à revisão do qa-lead sobre o doc de aceite: ele reprova se não definir métricas que possam reprovar. B6 (L327, "sem reescrita"; unity-specialist queria BLOCKING) → rebaixado a ADR, mantendo a arbitragem da 5ª passada; o determinismo de L349 é o do RNG de combate, não o das transações de economia. Tank em L455 → rebaixado, um /prototype antes de D0 é outra coisa que o critério de L405. O performance-analyst não viu bloqueador; o CD discordou dele em 4 itens (contradições verificáveis de uma linha).
Decisions applied in the same session (user chose "Revisar agora"; every CD recommendation, subtraction or word swap): as 4 correções acima mais o corte de " (cada vitória a mais é outra troca possível)" em L150 (falso com g < 5). O arquivo foi de 55.471 para 55.456 bytes (466 linhas), medido com wc: o conceito não cresceu.
Cycle closure (CD, aceito pelo usuário): o ciclo de re-reviews do conceito está encerrado, sem 7ª passada. Critério de saída: todo bloqueador da passada (i) se conserta com edição de no máximo uma linha, (ii) não faz o arquivo crescer e (iii) não toca fantasia, pilares, gancho nem hipótese do MVP. A 5ª e a 6ª passadas cumpriram os três. O conceito fica congelado: achado novo vai ao GDD ou ao doc de aceite, e o conceito só muda quando um GDD aprovado mudar uma regra (então L80, L81 e o invariante de L407 viram ponteiros ao GDD do Grimório). Próximo: /gate-check (pode dar CONCERNS, porque o último veredito deste log é NEEDS REVISION), depois /map-systems, com o GDD do Grimório primeiro.
Caveats: (1) o unity-specialist e o systems-designer rodaram sem Bash para o script de enumeração (inv.py foi escrito mas não executado); a grade de (g, f) foi enumerada à mão. (2) Os RECOMMENDED acima ainda não têm dono no repositório: o doc de aceite e os GDDs não existem. (3) O recibo não carimba design/gdd/game-concept.md (a cópia de trabalho foi editada nesta sessão); o próximo check lê CHANGED.
Receipt note: este registro não carimba design/gdd/game-concept.md. As demais linhas abaixo carimbam os arquivos lidos.
Reviewed-Content-Hash: design/registry/entities.yaml dfeacb02917f751cb1dfd88cf490c7ec3d8d2d0f
Reviewed-Content-Hash: .claude/skills/design-review/SKILL.md a63d8fba9b7142eeb43791f061e2e1533c429b43
Reviewed-Content-Hash: prototypes/grimorio-concept/REPORT.md ef64cc8638c4f4b904c03659f10202a824948b3e
