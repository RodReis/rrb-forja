# Game Concept: Forja das Hordas

*Created: 2026-11-02*
*Status: Congelado*
*Título provisório. Revisões do brainstorm: CD-PILLARS (CONCERNS, resolvido), AD-CONCEPT-VISUAL (CONCEPTS), TD-FEASIBILITY (HIGH RISK para o coop no lançamento, resolvido no escopo), PR-SCOPE (OPTIMISTIC, ajustes aplicados).*
*Revisões `/design-review` (full): histórico e veredito mais recente em `design/gdd/reviews/game-concept-review-log.md`. Correções por subtração: nenhuma frase falsa; metodologia no doc de aceite do MVP.*

---

## Elevator Pitch

> É um RPG mobile de sobrevivência contra hordas em que você enfrenta ondas de inimigos escolhendo skills aleatórias a cada level up, até descobrir a build que é sua. Aí você **sela** essa build e leva o seu herói, forjado no fogo das hordas, para dungeons com a trindade clássica de tanque, DPS, mago e healer.

---

## Core Identity

| Aspect | Detail |
| ---- | ---- |
| **Genre** | Ação RPG / survivor de hordas (roguelite por fase) com progressão de personagem e equipamento estilo MMORPG |
| **Platform** | Mobile (iOS e Android) |
| **Target Audience** | Jogadores mid-core e hardcore mobile que otimizam builds e equipamento (ver Target Player Profile) |
| **Player Count** | Single-player no lançamento (a trindade é completada pelos seus outros heróis selados ou por um companheiro NPC com teto); coop PvE de 4 e PvP em tempo real no pós-lançamento |
| **Session Length** | Fase de 3 a 5 min; sessão típica de 20 a 60 min |
| **Monetization** | **Em aberto:** F2P ou premium (ver Open Questions), a decidir antes do GDD de economia. Qualquer modelo segue o Princípio de Negócio (ver Game Pillars) |
| **Estimated Scope** | Large (48 a 72 meses, solo) na visão completa; o lançamento ajustado leva de 13 a 20 meses (esperado: 16), solo |
| **Comparable Titles** | Survivor.io e Archero (loop de horda com skill aleatória), Summoners War (otimização de equipamento e runas), MIR4 e Lineage 2M (progressão de MMORPG no mobile) |

---

## Core Fantasy

**"Eu forjei este herói no fogo das hordas, e cada skill dele foi conquistada."**

O jogador não recebe um herói pronto nem sorteia um em gacha: ele o **constrói** testando skills e sets contra ondas de inimigos até encontrar a combinação que é só dele. Quando sela a build, ele sela a própria identidade no jogo. A partir daí, esse herói é o Orc tanque que segura a linha para o grupo inteiro, ou a Elfa healer que mantém todos vivos no chefe. É a sensação de uma dungeon como Zul'Farrak, com um personagem que você mesmo forjou.

*Por que essa fantasia, e não as alternativas:* "colecionar heróis" (Summoners War) foi descartada porque dilui a identidade. "Power fantasy pura" (survivor clássico) foi descartada porque não deixa nada permanente depois da run e porque nada nela custa conquistar. O alvo é uma **power fantasy permanente com custo de conquista**: o poder no fim é real, mas cada skill selada foi escolhida e registrada contra um chefe. O selamento une as duas pontas: tem a liberdade do roguelite e o peso de um personagem de MMO.

*Teste da fantasia:* o jogador sabe dizer por que cada skill selada foi conquistada. Se o Grimório contém quase tudo, nada foi conquistado. O protótipo mostrou isso (11 de 12 skills registradas), e é por isso que o registro é escasso.

---

## Unique Hook

**É como um survivor de hordas mobile (skill aleatória a cada level up), E TAMBÉM a build que você descobre vira um personagem permanente de RPG, selado, que você leva para dungeons com a trindade clássica.**

- Dá para explicar em uma frase: runs de horda são o laboratório da build; o selamento a torna permanente.
- Afeta o gameplay: cada vitória contra um chefe registra skills no **Grimório**, e é dele que saem as skills definitivas.
- Está ligado à fantasia: "forjei no fogo das hordas" é literalmente o loop.
- Os survivors são solo e descartáveis. Este traz a trindade (tanque, DPS, mago, healer) e um herói que persiste.

---

## Player Experience Analysis (MDA Framework)

### Target Aesthetics (What the player FEELS)

| Aesthetic | Priority | How We Deliver It |
| ---- | ---- | ---- |
| **Expression** (self-expression, creativity) | 1 | Raça, função, skills seladas do Grimório, combinação de set; dois heróis no nível máximo não são iguais |
| **Challenge** (obstacle course, mastery) | 2 | Elites e chefes com golpes telegrafados e esquiva no timing; waves que apertam; ranking por função |
| **Fantasy** (make-believe, role-playing) | 3 | Ser a raça (animações, voz, skill racial, fase de origem); ser o tanque ou o healer de quem o grupo depende |
| **Fellowship** (social connection) | 4 | No lançamento é fraca: a trindade é feita com os seus próprios heróis selados (ou um NPC com teto). Vira Core no pós-lançamento, com o coop PvE de 4 humanos |
| **Sensation** (sensory pleasure) | 5 | Massacre da horda com feedback em massa; hit-stop e knockback nos golpes pesados; o ritual de forja do selamento |
| **Discovery** (exploration, secrets) | 6 | Sinergias e evoluções de skill a descobrir, guardadas no **Códex** da conta (conhecimento, não acesso) |
| **Narrative** (drama, story arc) | 7 | Fases de origem por raça e capítulos com tema; sem história linear pesada |
| **Submission** (relaxation, comfort zone) | 8 | Auto-battle e varredura em conteúdo já vencido |

### Key Dynamics (Emergent player behaviors)

- Os jogadores vão **experimentar combinações de skill** dentro das fases para descobrir sinergias antes de selar.
- Os jogadores vão **planejar o selamento** como um evento: comparar opções do Grimório, pedir opinião à comunidade.
- Os jogadores vão **compartilhar builds seladas** (prints, guias), e a diversidade delas é o sinal de saúde do pilar 1.
- Os jogadores vão **farmar materiais** em fases já vencidas no auto e voltar ao manual para conteúdo novo.
- Tanques e healers vão **assumir identidade de função** ("sou o tanque do grupo"), reforçada pelas fases de função.

### Core Mechanics (Systems we build)

1. **Combate híbrido contra hordas:** joystick com um dedo, auto-ataque, botão de esquiva e uma suprema ativa. A horda fraca derrete em massa; elites e chefes têm golpes pesados e telegrafados.
2. **Skill aleatória por fase + Grimório:** a cada level up dentro da fase, você escolhe 1 de 3 skills ou melhorias (temporárias), com evoluções por sinergia; o pool de cartas é filtrado pela função do herói (skills da função + compartilhadas). Ao vencer o **chefe de fase**, você pode registrar **1** skill ativa elegível (acima de um nível mínimo, ou evoluída) no Grimório do herói, que tem **capacidade** C (knob; 5 no MVP; **5 ≤ C ≤ |pool da função| − 4**, com o pool da função = skills ativas da função + compartilhadas). Com o Grimório cheio, registrar é uma **troca opcional**, a skill substituída volta ao pool.
   **O selo pode abrir** a partir de **K_min = C + 2 vitórias de chefe de fase** daquele herói (7 no MVP), e só com um Grimório com ≥ 4 skills, sendo ≥ 2 de função. K_min conta vitórias, não registros: como o registro é opcional (1 por vitória), um herói com g skills no Grimório (f de função) precisa de até max(0, 4 − g, 2 − f) vitórias a mais, no máximo 4. Se o Grimório não é selável a partir de K_min, a **garantia** se arma: o nível mínimo deixa de valer e, se faltam skills de função, cada fase começa com 1 skill de função ativa ainda não registrada. Chefe de capítulo, morte, auto e varredura não registram nem contam vitória. O Grimório é **por herói** e se fecha no selo; a conta guarda só o **Códex** (as sinergias descobertas). Detalhes no GDD do Grimório.
3. **Selamento da build:** quando o selo abre, você escolhe do Grimório as **skills definitivas**: 4 slots, sendo 2 de função (só aceitam skills da sua função) e 2 livres (aceitam skills compartilhadas e também da própria função). Uma evolução descoberta e registrada pode ser selada; quantos slots ela ocupa fica no GDD do Grimório. O selo fixa **só as skills**: a função foi escolhida na criação do herói, a suprema é fixa por função e a skill racial é fixa por raça, as duas fora dos slots. O set continua livre e é a perseguição de longo prazo. É permanente; a **run de reforja** (pelo Livro ou por um nerf) troca uma skill selada.
4. **Forja e sets por raridade:** materiais de cinco raridades (Branco → Verde → Azul → Roxo → Dourado) craftam e melhoram peças de set por função.
5. **Trindade com companheiros:** dungeons com tanque, DPS, mago e healer. No lançamento, as vagas que você não ocupa são preenchidas pelos **seus outros heróis selados**; sem um herói da função, entra um companheiro NPC genérico, com poder limitado abaixo de um humano (knob).

---

## Player Motivation Profile

### Primary Psychological Needs Served

| Need | How This Game Satisfies It | Strength |
| ---- | ---- | ---- |
| **Autonomy** (freedom, meaningful choice) | Raça, gênero, função, skills do Grimório, set e (no pós-lançamento) runas: a identidade do herói é escolha do jogador, e o selamento dá peso a essa escolha | Core |
| **Competence** (mastery, skill growth) | Esquiva contra telegraphs, leitura de sinergias, waves mais difíceis, ranking por função como prova pública | Core |
| **Relatedness** (connection, belonging) | Trindade: no lançamento com os seus outros heróis selados (ou NPC com teto); no pós-lançamento, o grupo humano precisa do seu tanque ou do seu healer | Supporting (Core no pós-lançamento) |

### Player Type Appeal (Bartle Taxonomy)

- [x] **Achievers** (goal completion, collection, progression) — How: set dourado completo, Códex de sinergias completo, o selo, ranking por função. **Primário**, junto com os criadores de build (Quantic Foundry: Estratégia + Conclusão).
- [x] **Explorers** (discovery, understanding systems, finding secrets) — How: descobrir sinergias e evoluções de skill; entender o sistema de build a fundo.
- [x] **Socializers** (relationships, cooperation, community) — How: coop PvE com a trindade (pós-lançamento); compartilhar builds. **Secundário.**
- [x] **Killers/Competitors** (domination, PvP, leaderboards) — How: ranking por função; PvP em tempo real no pós-lançamento. **Terciário.**

**Não é para:** quem busca história linear (Storyteller), quem quer relaxar sem compromisso (o selamento pesa), e quem quer colecionar heróis por gacha.

### Flow State Design

- **Onboarding curve:** os primeiros 10 minutos são a fase de origem da raça escolhida. Ela ensina o movimento e o auto-ataque na primeira wave, a escolha de skill no primeiro level up, a esquiva no primeiro elite e a suprema no primeiro chefe. O Grimório e a Forja aparecem depois do primeiro chefe; o selamento só é explicado quando o jogador se aproxima das K_min vitórias.
- **Difficulty scaling:** a densidade da horda e a frequência de elites crescem por fase. Os chefes introduzem um padrão de telegraph novo por capítulo. O conteúdo novo é sempre manual; o conteúdo vencido pode ir para o auto.
- **Feedback clarity:** feedback de massa (inimigos caindo em cadeia), números de dano legíveis, telegraphs que nunca ficam escondidos (a camada mais alta da tela), registro visível no Grimório a cada chefe vencido, e o Poder de Combate visível.
- **Recovery from failure:** morrer numa fase custa de 3 a 5 minutos, e o jogador fica com os materiais coletados até ali (taxa a definir no GDD). O erro realmente punitivo é o selamento mal planejado, mitigado pela run de reforja (o Livro é conquistado jogando) e pelos slots extras de herói conquistados jogando.

---

## Core Loop

### Moment-to-Moment (30 seconds)

O jogador se move com um dedo, enquanto o auto-ataque e as skills varrem a horda e ele coleta orbes de XP. Um elite aparece e marca no chão um golpe em área; o jogador esquiva no último instante e pune com a suprema.

O loop é satisfatório por si só porque alterna dois prazeres:
- **Descarga:** dezenas de inimigos caindo de uma vez, com explosões em cadeia e feedback visual em massa.
- **Tensão:** um erro contra o elite custa caro, e o hit-stop e o knockback dão peso a cada golpe.

A sensação escolhida é uma média entre *massacre em massa* e *pesado e impactante*. A alternativa *tático e posicional* foi descartada como sensação principal, mas fica parcialmente presente nas fases de função.

### Short-Term (5-15 minutes)

Uma **fase** é formada por várias waves mais um **chefe de fase** (um elite-chefe, reaproveitado entre fases), de 3 a 5 minutos no total. Cada capítulo termina num **chefe de capítulo** único, com a recompensa maior. A cada level up dentro da fase, o jogador escolhe 1 de 3 skills ou uma melhoria de uma skill que já tem, e algumas combinações evoluem por sinergia.

- **Registro no Grimório:** só ao vencer o chefe de fase. O jogador escolhe se registra 1 skill ativa elegível e, com o Grimório cheio, qual substituir. Isso faz de cada registro uma pequena decisão de identidade e, com o Grimório cheio, de cada replay uma troca, e não um efeito colateral.
- **Depois do selamento:** as skills seladas já começam a fase presentes. O level up oferece 1 de 3 **melhorias ou modificadores das skills seladas**. O estado da Prova do Selo, que foi o pico do protótipo, vira o padrão do jogo.

- **Agência sobre o sorteio** (para que o selamento não vire caça-níquel): 1 reroll por fase, e a possibilidade de **favorecer uma skill já registrada no Grimório**, que passa a aparecer com mais frequência. Os números exatos são knobs.
- **O "só mais uma":** a chance de uma combinação de skills melhor na próxima tentativa, e o drop de material de raridade alta no chefe.
- **Fases de função:** objetivos como escoltar ou proteger um NPC, nos quais Tank e Healer brilham. Toda skill de função também tem **uso solo** (por exemplo, a cura gera um escudo que explode; a provocação puxa a horda para um ponto e reflete dano), para que Tank e Healer consigam forjar a build sozinhos.

### Session-Level (30-120 minutes)

No mobile, a sessão típica dura de 20 a 60 minutos.
- **Antes do selamento:** fase → Forja → fase. O jogador gasta materiais na Forja para craftar e melhorar peças de set e testa outra combinação.
- **Depois do selamento:** dungeon com a trindade → Forja → farm no auto → conteúdo novo.
- **Pontos de parada naturais:** o fim de cada chefe.
- **O gancho para voltar:** ficar a poucos materiais da próxima peça de set, as dungeons diárias de material e, antes do selo, o próximo registro no Grimório (depois do selo, a próxima run de reforja ou um herói novo).

### Long-Term Progression

1. **Antes do selamento:** o jogador escolhe raça e **função** na criação do herói e sobe de nível pela campanha. As skills dentro da fase são temporárias (roguelite); a cada chefe de fase vencido, o jogador pode registrar 1 delas no **Grimório** do herói, que tem capacidade limitada. Testar skills e sets é o próprio jogo.
2. **Selamento** (a partir de K_min vitórias de chefe de fase, um knob): o jogador escolhe no Grimório as 4 skills definitivas (2 de função + 2 livres), encenado como um **ritual de forja**. É **definitivo**; a **run de reforja** troca uma skill selada. O selo pode abrir a partir de K_min vitórias, com um Grimório selável (ver Core Mechanics), e pode ser adiado para jogar mais fases, mas o herói não passa do nível de selamento sem selar.
3. **Depois do selamento:** dungeons com a trindade, level ups que modificam as skills seladas, peças de set aleatórias e materiais, set dourado completo e ranking por função. No pós-lançamento entram runas, coop de 4 humanos e PvP.
4. **Novos heróis:** slots extras de herói são **conquistados jogando** (nunca vendidos). Cada herói novo começa com o Grimório vazio e conquista as próprias skills; o Códex da conta guarda só o conhecimento das sinergias. O custo de um selamento ruim é principalmente tempo (o Livro de Reforja reduz esse custo, com teto), e o momento de expressão se renova. Heróis novos e runs de reforja são os caminhos pelos quais as skills de patches novos chegam ao jogador. Os heróis selados também viram os companheiros uns dos outros na trindade.

O jogo "termina" quando o jogador tem o set dourado da sua função e um lugar no ranking. Depois disso, o conteúdo de capítulos sustenta o jogo (e as temporadas, se o modelo de negócio as incluir).

### Retention Hooks

- **Curiosity:** sinergias e evoluções de skill ainda não descobertas; os próximos capítulos; as fases de origem das outras raças.
- **Investment:** o herói selado, o Grimório (antes do selo) e o set em construção, ou seja, o progresso que o jogador não quer perder.
- **Social:** compartilhar builds; no pós-lançamento, o grupo de coop que depende da sua função.
- **Mastery:** esquiva contra chefes mais difíceis, tempo de clear e posição no ranking por função.

---

## Game Pillars

Os pilares foram travados pelo usuário e revisados pelo creative-director (CD-PILLARS: CONCERNS). As cinco correções propostas foram aplicadas. Existem tensões deliberadas entre eles:
- o pilar 1 contra o 3 (expressão contra papel fixo);
- o pilar 2 contra o Princípio de Negócio, por causa do Livro de Reforja (resolvida: o Livro nunca é vendido);
- o pilar 1 contra o 4 (build vistosa contra leitura do perigo).

### Pillar 1: Sua build, sua assinatura

Dois heróis no nível máximo não devem parecer iguais.

*Design test:* entre "mais poder bruto" e "mais opções distintas de build", escolhe as opções distintas.

*Critério mensurável (sugerido pelo CD):* no top 100 de cada função, nenhum conjunto de skills seladas aparece em mais de X% dos heróis. X é um knob, e a medição é feita por analytics.

*Consequência aplicada:* o ranking é **por função e por desempenho** (tempo de clear de dungeon; PvP por rating), e não por Poder de Combate. O Poder de Combate continua visível e serve de requisito de entrada em conteúdo, mas **não é o placar**. Ele é calculado **só a partir de equipamento e nível, nunca das skills seladas**, para que a porta de conteúdo não puna builds de identidade. A fórmula e a escolha entre porta suave e dura ficam para o GDD de Poder de Combate. Essa decisão substitui o pedido original de ranking por poder de combate, que faria as builds convergirem.

### Pillar 2: Toda escolha pesa

Decisões de build são permanentes e têm consequência.

*Design test:* entre conveniência e consequência, escolhe consequência. O reset existe, mas é raro e custa.

*Consequências aplicadas:*
- A **run de reforja** troca **uma** skill selada. Usar o Livro de Reforja abre uma fase com as 3 skills seladas restantes e o slot escolhido aberto, com cartas do pool daquele tipo de slot, menos as seladas; vencer o chefe sela a substituta, pela mesma regra de registro. A substituta é conquistada no fogo das hordas, como as outras, e sempre existe alvo. Trocar de função exige outro herói.
- **Oferta e teto:** cada herói tem direito a **1 Livro por período**, obtido por um objetivo (não por drop) e alcançável antes de qualquer lockout de ranking. O teto é de 1 Livro por herói por período (knob); a reforja por nerf fica fora dele. Enquanto não existirem temporadas, o período é uma janela fixa (knob). **O Livro nunca é vendido:** só é obtido jogando. Reforjas feitas depois do lockout não contam para o ranking daquele período.
- **Política de nerf:** só um **nerf líquido** acima de um limiar (knob) dá uma **run de reforja grátis**, fora do teto do Livro e limitada a **1 por herói por período, sem acumular entre patches**. Ela troca uma das skills afetadas, como qualquer run de reforja. Por isso as runs de reforja e os heróis novos são as vias pelas quais skills de patches novos chegam a um herói selado. A reforja grátis vale para quem selou a skill antes do anúncio do patch e expira numa janela de tempo (knob). Buffs, correções de bug, mudanças de texto e ajustes abaixo do limiar não contam. Nerfs em evoluções ou passivas cobrem as skills seladas que dependem delas.
- Slots extras de herói são conquistados jogando.

### Pillar 3: Cada função é indispensável

No coop, tanque, DPS, mago e healer fazem coisas que os outros não fazem.

*Design test:* entre "qualquer função consegue solo" e "o grupo precisa da trindade", no coop escolhe a trindade.

*Termo:* neste documento, "trindade" é o grupo das quatro funções; o nome vem do MMO, e o Mago é a quarta. Cada função tem um verbo exclusivo: o Tank segura, o Healer mantém vivo, o DPS causa dano focado no chefe e o Mago **controla** a horda e as adds (lentidão, agrupamento, interrupção). Os affixes de dungeon dependem desse controle (GDD de Poder de Combate e Ranking).

*Consequências aplicadas:*
- Toda skill de função tem **uso solo**, para que a função possa ser forjada sozinha.
- **Slots de função no selo:** dos 4 slots, 2 só aceitam skills da função do herói. Como o pool de cartas já é filtrado pela função, skills de outra função nunca chegam ao Grimório (o DPS nunca vê a "cura que explode"); os slots de função garantem que pelo menos metade do selo seja da função. O efeito solo de uma skill de função escala com o bônus do set da função.
- Existem **fases de função** (escoltar ou proteger).
- No lançamento, as vagas da trindade são ocupadas pelos **outros heróis selados do jogador**; sem herói da função, entra um **companheiro NPC genérico com poder limitado** abaixo de um humano (knob). Isso dá motivo para forjar um Tank mesmo para quem joga de DPS. No pós-lançamento, os companheiros preenchem as vagas vazias da fila de coop, o que ajuda com a falta de tanques e healers.
- *Limite conhecido:* o pilar só pode ser validado a partir do vertical slice, porque o MVP não tem companheiros. No lançamento ele se expressa como "a dungeon exige a trindade"; a relação humana ("o grupo precisa de mim") só chega no pós-lançamento.
- *Em aberto:* o formato do PvP em relação a este pilar (ver Open Questions).

### Pillar 4: Massacre com peso

Hordas derretem, elites batem forte, e o jogador sempre consegue ler o perigo.

*Design test:* entre "mais efeitos na tela" e "golpe inimigo legível", escolhe o golpe legível.

*Regra derivada:* o telegraph inimigo fica sempre na camada mais alta da tela, e os efeitos aliados têm limite de opacidade e de densidade, ajustável pelo jogador. Ataque automático **não** é auto-battle: movimento e esquiva são manuais.

### Pillar 5: Ser a raça, não vestir a raça

Jogar de Orc tem que parecer jogar de Orc, e não usar um modelo com +5% de força.

*Design test:* entre "+% de atributo racial" e "habilidade ou animação racial distinta", escolhe a distinta.

*O que entra:* cada raça tem animações, voz, uma skill racial e uma **fase de origem** próprias. Os bônus de atributo existem, mas não são a identidade da raça.

*Por que existe:* o CD apontou que a fantasia pessoal do projeto (jogar de Orc de verdade) e o tom do mundo não tinham pilar.

### Princípio de Negócio: Poder conquistado, não comprado

Este era o pilar 5. Ele virou princípio de negócio, com a mesma força, por recomendação do CD: é uma política de monetização, não uma experiência do jogador.

O que coloca o jogador no ranking vem do jogo, não da loja.

*Linha exata:* **entre jogadores com o mesmo conteúdo, nenhuma compra aumenta o Poder de Combate, a quantidade de recompensas não cosméticas por dia, período ou temporada, nem a velocidade de obter algo que conta para o ranking.** Aqui, "conteúdo" é o acesso a capítulos e dungeons, não um pacote de recompensa.
- **Não existe energia.** As fontes de material (dungeon diária, fase já vencida) têm um **teto diário de recompensa** (knob; o escopo, por conta ou por herói e por fonte ou por categoria, fica no GDD de Economia). A varredura é grátis dentro desse teto; pular a animação é uma opção grátis e não adiciona entradas nem recompensa.
- O Livro de Reforja nunca é vendido (ver Pilar 2), e nenhuma recompensa de canal pago (passe, pacote, missão paga) contém Livro, slot de herói, material nem reforja.
- **Nunca são vendidos:** reroll, peso de favorecer ou qualquer outra agência sobre o sorteio (isso é poder); entradas do Grimório; slots de herói (seriam uma correção paga do selamento, vetada pelos anti-pilares).
- Cosméticos não podem imitar o vocabulário visual de raridade ou de runa.

### Anti-Pillars (What This Game Is NOT)

- **NOT gacha de heróis:** comprometeria *Sua build, sua assinatura*. O herói é construído, não sorteado.
- **NOT venda de sets, runas, materiais (de qualquer raridade) ou boosts de XP, em qualquer loja que o jogo venha a ter:** comprometeria o *Princípio de Negócio*.
- **NOT venda de skills ou de entradas do Grimório:** comprometeria os pilares 1 e 2. A build vem do jogo.
- **NOT correção paga de selamento:** o Livro de Reforja só é obtido jogando. Isso fecha a brecha do *Princípio de Negócio*.
- **NOT auto-battle em conteúdo inédito, coop ou competitivo:** comprometeria *Massacre com peso*. Conteúdo já vencido pela conta pode ser repetido no auto ou na varredura, com rendimento **por hora** um pouco menor que o manual. O auto é uma simulação determinística por seed e pode falhar. Auto e varredura **nunca registram no Grimório**, não contam vitória para o selo e nunca contam para o ranking; registrar exige vencer o chefe jogando.
- **NOT mundo aberto persistente estilo MMO:** o escopo engoliria o resto. O mundo é feito de fases e dungeons instanciadas.

---

## Visual Identity Anchor

**Direção: "Hierarquia do Detalhe", com o Ritual da Forja**

Escolhida pelo usuário a partir das três direções do art-director (AD-CONCEPT-VISUAL: CONCEPTS). As alternativas descartadas foram:
- **"A Marca da Forja"** (fantasia pintada estilo WoW), que abandonava o realismo pedido. Dela veio o ritual de selamento.
- **"Só o Perigo Brilha"** (penumbra), que era monótona, fraca em tela com pouco brilho e escondia os cosméticos.

**Regra visual em uma linha:** *O detalhe é privilégio da ameaça e do herói; todo o resto é silhueta.*

**Princípios de apoio:**

1. **Realismo onde a câmera chega perto.** O realismo estilo Lineage 2 (proporções adultas e heroicas, armaduras com peso, tom sério) vale para heróis, chefes, a Forja e as telas de equipamento e inventário. Em combate, a horda tem formas simples, em bloco, sem acessórios soltos, e cada tipo é reconhecível só pela silhueta. O herói tem ombros e arma de 10 a 15% maiores que o natural, para continuar legível na câmera alta.
   *Design test:* se um detalhe não aparece com o inimigo a 40–70 px na tela, ele não entra no inimigo da horda.
2. **A silhueta revela a função.** Tank largo e quadrado; DPS fino e angular; Mago vertical, com tecido em movimento; Healer arredondado, com halo ou forma circular. Elites e chefes têm silhueta grande e assimétrica, com uma "parte que ataca" bem identificável.
   *Design test:* se dois tipos de inimigo ou duas funções se confundem pela silhueta em escala de cinza, a forma muda, não a cor.
3. **O selamento é um ritual de forja.** O momento permanente é encenado: metal incandescente, a runa gravada e o resfriamento. A decisão irreversível tem que parecer cerimonial.
   *Design test:* entre um selamento rápido e um selamento memorável, escolhe o memorável, que pode ser pulado depois da primeira vez.

**Filosofia de cor:**
- O cenário fica em valores médios e dessaturados. A horda é mais escura e mais fria que o chão (o contraste é de valor, não de cor). O herói tem a maior saturação do corpo.
- **O vermelho-alaranjado quente e luminoso é exclusivo dos telegraphs de perigo.** Nenhuma skill de jogador, raridade ou cosmético pode usar essa faixa.
- **Raridades:** Branco → Verde → Azul → Roxo → Dourado. **Toda raridade tem também uma moldura ou forma própria**, e não só cor, porque:
  - o verde se confunde com cura;
  - o dourado se aproxima do perigo;
  - verde, azul e roxo são difíceis de distinguir para daltônicos.
  O dourado precisa de um tom que não invada a faixa dos telegraphs.
- **Raridade é variante de material ou shader** (cor, emissivo, VFX), nunca uma malha nova. Essa regra é técnica e de produção (TD e producer).
- **Hierarquia de desenho no coop:** telegraph inimigo > o próprio herói > aliados (efeitos atenuados) > horda > cenário. Essa escolha entre os pilares 1 e 4 foi escalada ao CD e aplicada pela regra derivada do pilar 4.

---

## Inspiration and References

| Reference | What We Take From It | What We Do Differently | Why It Matters |
| ---- | ---- | ---- | ---- |
| Survivor.io / Archero (survivor de hordas mobile) | Loop de wave com skill aleatória a cada level up; controle com um dedo; sessões curtas | A run alimenta um herói permanente (Grimório + selamento); elites com golpes pesados e esquiva | Valida que o loop de horda com skill aleatória segura o jogador mobile |
| World of Warcraft (Zul'Farrak) | A trindade; dungeons com identidade forte; a fantasia de ser a raça | No formato de hordas; no lançamento, a trindade com os seus próprios heróis selados | É a memória que define o projeto; valida o apelo da trindade |
| Summoners War | Otimização profunda de equipamento e runas | Não tem gacha de heróis: o herói é construído | Valida que o jogador mobile passa centenas de horas otimizando build |
| Lineage 2 / MIR4 | Fantasia adulta e realista; progressão de equipamento de MMORPG | O realismo só onde a câmera chega perto; sem mundo aberto | Valida o público de MMORPG mobile e o apelo do visual realista |
| Lords Mobile (forja) | Forja de equipamento com materiais por raridade | Os sets são por função; a raridade se expressa por material | Valida a Forja como gancho de retorno |
| Diablo 2 (Token of Absolution) | Lição: build permanente com patches gera revolta; o respec precisa existir | Livro de Reforja conquistável e reforja grátis em caso de nerf | Evita o principal risco do pilar 2 |

**Non-game inspirations:** a forja de ferreiro como ritual (o metal incandescente e o resfriamento são a metáfora do selamento); o deserto em ruínas, com luz dura e calor visível no ar, como tom dos calabouços.

---

## Target Player Profile

| Attribute | Detail |
| ---- | ---- |
| **Age range** | 18 a 40 |
| **Gaming experience** | Mid-core a hardcore |
| **Time availability** | Sessões de 20 a 30 min nos dias de semana (farm no auto e algumas fases) e sessões longas no fim de semana (conteúdo novo e dungeons) |
| **Platform preference** | Mobile, com histórico em MMORPG de PC |
| **Current games they play** | Summoners War, MIR4 ou Lineage 2M, Survivor.io ou Archero |
| **What they're looking for** | A profundidade de build e equipamento de um MMORPG, em sessões curtas de ação, com um herói que é realmente seu |
| **What would turn them away** | Pay-to-win, gacha de herói, auto-battle em tudo (jogo sem jogador) e selamento sem nenhuma saída (perder a build por um patch) |

---

## Technical Considerations

| Consideration | Assessment |
| ---- | ---- |
| **Recommended Engine** | Preferência do usuário: **Unity**. O TD considera a escolha compatível e não recomenda trocar. A referência fixada no projeto é o Unity 6.3 LTS, e o `/setup-engine` confirma a versão instalada. Atenção: o suporte do 6.3 LTS termina em dezembro de 2027, então é preciso reservar uma janela de migração. Usar URP + Render Graph desde o primeiro dia |
| **Key Technical Challenges** | (1) Centenas de inimigos animados com heróis realistas em Android intermediário: animação por partes rígidas ou VAT, instancing, Jobs/Burst; o overdraw de partículas é o gargalo provável; throttling térmico. (2) No pós-lançamento: coop em tempo real em rede móvel, PvP com servidor autoritativo e anti-cheat. (3) Um backend leve no lançamento: cloud save, validação de compras (se o modelo tiver) e leaderboard |
| **Art Style** | 3D realista nos heróis, chefes e na Forja; 3D simplificado em bloco na horda ("Hierarquia do Detalhe") |
| **Art Pipeline Complexity** | High (3D personalizado). Mitigação: personagens modulares, esqueleto compartilhado, raridade por material, assets comprados como base |
| **Audio Needs** | Moderate: feedback de impacto e de massa, áudio dos telegraphs, voz por raça (pilar 5), o ritual da Forja |
| **Networking** | Lançamento: None no gameplay, com backend leve (cloud save, validação de compras se o modelo tiver, leaderboard). Pós-lançamento: coop com host ou servidor autoritativo; PvP em tempo real com servidor dedicado ou autoritativo. A tecnologia exige um ADR, porque nenhum backend está na referência do engine |
| **Content Volume** | Lançamento: 2 raças, 4 funções, 2 capítulos com 20 fases (cada uma com chefe de fase), de 8 a 10 inimigos, de 3 a 4 chefes de capítulo, de 25 a 30 skills mais 2 raciais, sets por função em 5 raridades. Visão completa: 4 raças × 2 gêneros, 4 capítulos com uns 40 estágios, de 15 a 20 inimigos, de 6 a 8 chefes, de 40 a 60 skills mais 4 raciais, runas |
| **Procedural Systems** | Composição das waves por seed (útil para o auto-battle e para validação por replay); o drop de peças e runas é aleatório; as fases são feitas à mão |

**Decisões de arquitetura baratas agora e caras depois** (recomendação do TD, para registrar como ADRs depois do `/setup-engine`):
1. **Separar simulação de apresentação:** tick fixo, RNG com seed, lógica de combate sem MonoBehaviour. Isso pode viabilizar o auto-battle, o replay para validar o ranking e a autoridade de host no futuro, se a simulação for em inteiro ou ponto fixo (decisão do ADR).
2. **Progressão e economia como transações puras sobre dados**, que rodam no cliente offline e depois no servidor sem reescrita.
3. **Remote config para balanceamento** desde o início.

---

## Risks and Open Questions

### Design Risks

- **Skill aleatória somada ao selamento permanente pode parecer caça-níquel** ("rodei a fase 40 vezes"). Mitigação: reroll e favorecer skills do Grimório. No protótipo (n = 1, com registro automático), os dois **bastaram** contra a sensação de sorte. Isso **não foi testado sob escassez**: com o Grimório limitado, favorecer puxa skills já registradas, que não ajudam a registrar uma nova. A escolha garantida após o chefe fica como knob de reserva.
- **Selar por eficácia em vez de identidade** (sinal do protótipo: "gostei delas, me ajudaram"). Um Grimório escasso não produz sozinho uma escolha por identidade. Mitigação: registro por escolha, slots de função e um eixo de identidade com retorno mecânico na tela de selo (a definir no GDD do Selamento).
- **Tank e Healer podem não ser divertidos sozinhos.** Mitigação: uso solo das skills de função e fases de função. O MVP testa isso explicitamente.
- **Meta resolvido:** tier lists convergem as builds em semanas. Mitigação: ranking por função e por desempenho, critério de diversidade mensurável, raças pela identidade e não pelo atributo.
- **Balancear raça × função × skill × set × runa** é combinatoriamente pesado, sobretudo no PvP.
- **Nerf em build selada** gera revolta. Mitigação: política de reforja grátis.

### Technical Risks

- **Performance da horda em Android intermediário** (MEDIUM, segundo o TD). O spike é obrigatório: 300 inimigos, 4 heróis, efeitos e um chefe, medidos no **minuto 20** (por causa do aquecimento do aparelho).
- **Coop em tempo real em rede móvel** (HIGH no lançamento, segundo o TD): reconexão, app em segundo plano, latência de 80 a 200 ms contra esquiva no timing, sincronização da horda. **Movido para o pós-lançamento.**
- **PvP em tempo real** (HIGH, segundo o TD): servidor autoritativo, anti-cheat, predição. O usuário escolheu tempo real em vez de assíncrono. O TD recomendou o assíncrono como alternativa viável e íntegra para um dev solo, e essa recomendação fica registrada. **É o último item do pós-lançamento.**
- **Integridade do ranking:** um score calculado no cliente é trapaceado. O leaderboard do lançamento é casual; o ranking competitivo exige validação no servidor.
- **NOT SOURCEABLE:** Netcode for Entities, Relay/Lobby, UGS, Unity IAP (se o modelo tiver compras), o GPU Resident Drawer em mobile e em malhas skinned, o VFX Graph em mobile, o licenciamento atual do Unity, IL2CPP e ARM64 no build Release, o remote config, as versões de JDK, NDK e SDK do módulo Android, a medição de frame time no aparelho e o determinismo do RNG entre Mono, IL2CPP e servidor não estão cobertos por `docs/engine-reference/unity/`. Cada um precisa de verificação ou de um ADR.
- **Fragmentação de Android:** hitches de compilação de shader (Adreno e Mali), explosão de variantes de shader no URP.

### Market Risks

- O gênero survivor está saturado, e os MMORPGs mobile têm orçamentos gigantes.
- A arte realista feita por uma pessoa compete com estúdios.
- Se o modelo for F2P, o Princípio de Negócio (sem venda de poder) limita a receita, e a aquisição de usuário custa caro.
- Um lançamento só single-player perde o diferencial social no primeiro dia.

### Scope Risks

- **Volume de arte:** cerca de 400 encaixes de peça no lançamento sem a regra de raridade por material (cálculo do producer). Com raridade por material, o multiplicador de 5× vira 1×. O Anão é o caso difícil de *fit*.
- **Árvore de modificadores pós-selo (custo oculto):** depois do selo, o level up só oferece modificadores das 4 skills seladas. Para não repetir carta em 10 a 13 level ups por fase, são precisos cerca de 4 modificadores por skill. A alternativa é o re-leveling (as seladas voltam ao nível 1 e sobem de novo). A escolha fica no GDD de Skills.
- **Backend e live ops** concorrem com o roadmap pós-lançamento. É preciso planejar uma cadência mínima (por exemplo, um evento por mês e um capítulo por trimestre).
- **Pacing do MVP:** abrir o selo exige ao menos 2 replays (K_min = 7 com 5 fases). É grind num MVP em que o "só mais uma" deu 0 de 1, então pouca vontade de fazer os replays não é, sozinha, evidência contra o loop.
- **Nenhuma estimativa está calibrada:** o MVP calibra a velocidade real. Se ele levar mais de 4 meses, multiplicar todas as faixas pela razão do atraso.
- **Ponto de corte mais provável:** entre o mês 16 e o 20, com a campanha incompleta. Os capítulos são unidades lançáveis, então o corte vira "lançar com menos capítulos".

### Open Questions

- **Formato do PvP diante do pilar 3:** é 1v1, em grupo, ou só por função? Um Healer vale alguma coisa no 1v1? A resposta vai no GDD de PvP antes de ele entrar no roadmap.
- **Modelo de negócio:** F2P com soft launch em poucos países, ou premium? **Precisa ser decidido antes do GDD de economia** (não só antes do Pre-Production), porque o valor do teto diário de recompensa e a existência de passe de temporada dependem dele (o Livro não entra nessa conta: nunca é vendido). O economy-designer alertou que um F2P só de conveniência é provavelmente inviável para um dev solo, e recomenda desenhar a economia como premium primeiro e acrescentar só o que passar no teste: "este item muda o resultado de alguma run ou a recompensa esperada por dia ou por temporada?"
- **Gênero do herói:** a premissa é que masculino e feminino são só visuais, sem diferença de atributo. Confirmar no GDD de raças.
- **K_min e nível de selamento:** knobs a calibrar no MVP. K_min abre o selo; o nível de selamento é só o teto de nível antes do selo. O GDD do Selamento define o que o XP faz depois do selo e separa os termos "nível de selamento" e "nível máximo".
- **Quanto material o jogador guarda ao morrer numa fase:** será definido no GDD da economia. Regra estrutural sugerida: só o drop das waves, nunca o do chefe.
- **Agência sobre o sorteio:** *parcialmente respondida pelo protótipo* (reroll + favorecer bastaram, com n = 1). Falta confirmar com o Grimório escasso, porque favorecer pode travar a descoberta.
- **GDD do Grimório:** o C do lançamento (C ≤ |pool da função| − 4); o nível mínimo de elegibilidade (faixa segura: 2 a 3); os slots de skill dentro da fase (o protótipo saturou com 6; testar 4); cada entrada guarda a origem (qual chefe, qual run) e o ritual do selo a mostra (teste da fantasia); o que acontece ao registrar de novo uma skill já registrada; o peso do favorecer (≤ 4), se ele vale só para skills ainda não registradas e se trava a descoberta sob escassez; quantas skills por função (≥ 5, para o selo não ficar forçado); como as evoluções são registradas e seladas (quantos slots, se exigem a passiva); glossário dos três níveis (herói, run e skill) e do termo "ativas"; se o registro também guarda o nível (profundidade, como knob opcional).
- **GDD do Selamento:** o eixo de identidade com retorno mecânico (Juramento ou tag temática, epíteto gerado), já que com o Grimório escasso a identidade migra para o registro e o selo corre o risco de virar só confirmação; o lockout de selo antes de temporada para o ranking; se as passivas têm slots próprios; os detalhes da run de reforja (o Livro é consumido ao entrar; abandonar conta como falhar); e a reforja por nerf (limiar publicado sobre a skill isolada; excluir da oferta as skills buffadas ou novas no mesmo patch e as acima da taxa de escolha X do Pilar 1, para ninguém torcer por nerf).
- **GDD de Economia:** escopo do teto diário de recompensa (por conta ou por herói, por categoria de fonte, para não escalar com o número de fases nem de alts); se a varredura dá XP a um herói que ainda não venceu a fase; relógio confiável para os tetos num jogo offline; o que define o "período" do Livro antes de existirem temporadas (nunca menos de 4 semanas, pelo relógio do servidor; offline, o período e os tetos só avançam na sincronização); o Livro vinculado ao herói, sem acumular entre períodos; o objetivo que dá o Livro como objetivo de participação, sem limiar de desempenho; auto e varredura chegam a no máximo [80]% do teto diário (o resto só no manual); sinks terminais depois do set dourado, conversão entre raridades, relação entre peça craftada e peça dropada, pity no loot de raridade alta, e um simulador de economia headless como validador (sem testadores externos).
- **GDD de Poder de Combate e Ranking:** a fórmula com pesos por função, porta suave ou dura, affixes de dungeon por função (o tempo de clear sozinho mede o DPS) e a métrica de diversidade (taxa de escolha por skill e sobreposição entre builds).
- **GDD de Sets e Forja:** 2 a 3 sets de arquétipo por função, para que o endgame não convirja num único set dourado.
- **Backend gerenciado ou próprio (UGS, PlayFab, Nakama ou Firebase):** será decidido por ADR.

---

## MVP Definition

**Core hypothesis:** *"Forjar uma build em fases de horda, registrando por escolha no Grimório as skills que venceram cada chefe e selando-as, entrega uma power fantasy permanente com custo de conquista, para DPS e também para Tank, em sessões de mais de 20 minutos, e roda num Android intermediário."*

*Escopo da validação com n = 1:* o MVP valida o custo de conquista (pela simulação), o Tank viável sozinho e a performance. A parte de identidade (selar pela identidade, não pela eficácia) e as sessões de mais de 20 minutos **não são validáveis com um único testador que é o próprio designer**: ficam como sinais registrados, e a validação delas vai para o primeiro playtest externo.

*Resultado do protótipo do Grimório (2026-11-02, HTML, n = 1):* **parcialmente suportada, não conclusiva** (ver Prototype Findings).

**Required for MVP:**
1. Combate híbrido (horda, elites com telegraph, esquiva, suprema) com o Orc.
2. Duas funções, **DPS e Tank**, escolhidas na criação do herói, para testar logo se o Tank consegue forjar a build sozinho.
3. 1 capítulo com 5 fases (cada uma com chefe de fase) e um chefe de capítulo, e cerca de 15 skills **ativas** com sinergias (5 de função por função + 5 compartilhadas, para um pool da função de 10; passivas e evoluções à parte).
4. Grimório **com a regra de escassez** (1 registro opcional por chefe de fase, nível mínimo, capacidade C = 5 com troca e garantia) e selamento de 4 skills (2 de função + 2 livres), incluindo o ritual básico. O selo pode abrir **antes** do chefe de capítulo, a partir de K_min = 7 vitórias de chefe de fase (as 5 fases mais 2 replays), e o chefe de capítulo é a **Prova do Selo**. Sem a regra de escassez, o MVP só reproduz a saturação que o protótipo já mostrou.
5. Forja com 3 raridades.
6. Tudo **offline**, com **log de eventos exportável** (escolhas, registros, selo, mortes, tempos). Ele é a fonte das medições abaixo.
7. **Instrumentação de aceite:** seeds determinísticas para o spawn e para a oferta de cartas, e uma **simulação headless** que chama o **mesmo** código de oferta, registro e substituição do Grimório do jogo (não um modelo paralelo), rodando como teste EditMode em `Assets/Tests/EditMode/Grimorio/`.

**Critérios de aceite do MVP** (reescritos na revisão de 2026-11-03 para valerem com n = 1, o próprio designer, por log). Os valores entre colchetes são knobs, decididos **antes** da medição e registrados com commit anterior a D0 (o arquivo e o procedimento ficam no doc de aceite do MVP). Cada colchete tem um **pior valor aceitável**, fixado ao lado da sua definição (aqui ou no doc de aceite), que o knob não pode ultrapassar. **Métrica que passa ou reprova por construção não vale como PASS.** A metodologia vive no **doc de aceite do MVP** (`docs/acceptance/mvp.md`), com commit antes de D0:
- **Semana 0 (antes de D0, pré-requisito do spike):** o módulo Android Build Support está instalado e o aparelho de referência, da classe **Android intermediário**, está escolhido e registrado em `docs/`, com um APK vazio rodando nele. A definição da classe e a evidência ficam no doc de aceite.
- **Performance (spike, semanas 1 a 3 a partir de D0):** build Release, IL2CPP ARM64, no aparelho de referência, alvo de 60 fps, com ≥ 300 inimigos ativos, 4 modelos de herói, VFX no máximo e o chefe, com **proxies com orçamento** no lugar dos assets reais. **Tem PASS/FAIL**: o limiar de frame time e a metodologia ficam no doc de aceite. Um FAIL abre uma decisão registrada (reduzir a contagem, mudar a técnica de render ou rever o conceito).
- **Tank viável sozinho:** com o build congelado (tag git no log) e a previsão escrita antes de jogar, o Tank é jogado **antes** do DPS. **PASS** se o Tank abre o selo com ≤ [2] mortes de fase (pior valor: 2; morte é uma tentativa que termina sem vencer o chefe de fase) e vence o chefe de capítulo (a Prova do Selo, já selado) em ≤ 3 tentativas. São **sinais registrados**, sem bloquear: a razão entre os tempos dos chefes de fase do Tank e do DPS na mesma seed (o DPS vem depois e tem efeito de aprendizado), uma fase voluntária com o Tank depois do selo, e a justificativa do selo citando função, estilo ou tema.
- **Sinais de identidade e de sessão (registrados, sem bloquear; ver Escopo da validação):** a justificativa de cada selo é digitada na tela do selo, antes de confirmar, e fica no log. Registram-se (1) a classificação cega das justificativas (identidade × eficácia) por um agente, com a rubrica com commit antes de D0, e a do próprio autor, só para comparar; (2) se o selo se desvia do selo de maior poder que a simulação calcula para aquele Grimório; (3) as sessões contínuas ≥ 20 minutos. Checagem de setup: há ≥ 1 Tank e ≥ 1 DPS selados.
- **Escassez (teste automatizado na simulação headless do item 7):** 100 seeds por função (DPS e Tank), de uma lista versionada, com C = 5 e K_min = 7. *Checagem de setup* (se falhar, a Escassez **não está fechada**): 5 ≤ C ≤ |pool da função| − 4, com o pool contando só skills ativas (função + compartilhadas). *Invariantes* (testes EditMode): o Grimório nunca passa de C; e, de todo estado alcançado com ≥ K_min vitórias, existe uma sequência de escolhas que abre o selo em ≤ max(0, 4 − g, 2 − f) vitórias adicionais, no máximo 4 (g = skills no Grimório, f = skills de função). *Métricas de oferta* (elegibilidade, selos distintos, garantia, concentração do selo): políticas, função de poder e piores valores ficam no doc de aceite e só viram gate quando ele as definir de modo que possam reprovar.
- **Pipeline de arte:** as horas por peça (modelagem, textura, rig, fit) ficam numa planilha que separa o comprado do produzido. Com ≥ 6 peças produzidas (o set do herói nos 2 tiers), **PASS** se a média das peças **produzidas** for ≤ [H] h, com pior valor H = horas de arte disponíveis até o lançamento ÷ peças do lançamento (os dois números com commit antes de D0). Um FAIL abre uma decisão registrada (comprar mais ou cortar peças por set). Os 2 tiers de set são distinguíveis na câmera de jogo, no aparelho de referência, com uma captura por tier em `production/qa/evidence/`. O herói fica dentro do orçamento de proxy de herói do spike (triângulos e MB de textura), e a cena de performance continua passando com ele.

**Explicitly NOT in MVP** (defer to later):
- Healer, Mago, outras raças e companheiros (heróis selados como companheiros e NPC com teto)
- Coop, PvP, ranking e backend
- Runas, loja (se houver), Livro de Reforja e run de reforja, auto-battle e varredura
- Arte final (o MVP usa arte de loja ou placeholder; só o herói do critério de pipeline é produzido)

### Scope Tiers (if budget/time shrinks)

Estimativas solo, ainda **sem calibração**. A ordem foi corrigida pelo producer: cada tier é um superconjunto do anterior, e os companheiros (seus heróis selados ou NPC com teto) vêm antes do coop.

| Tier | Content | Features | Timeline |
| ---- | ---- | ---- | ---- |
| **MVP** | Orc; DPS e Tank; 1 capítulo com 5 fases; cerca de 15 skills | Combate, Grimório, selamento, Forja com 3 raridades; offline | 2,5 a 4,5 meses (esperado: 3) |
| **Vertical Slice** | Capítulo 1 completo com companheiros; arte final de 1 herói | As 4 funções, companheiros (seus heróis selados ou NPC com teto) na trindade, Forja com 5 raridades | Marco: capítulo 1 jogável com companheiros até o mês 10 |
| **Lançamento (single-player ajustado)** | 2 raças (Orc e Humano), 4 funções, 2 capítulos com 20 fases, de 8 a 10 inimigos, de 3 a 4 chefes de capítulo, de 25 a 30 skills | Selamento, run de reforja (Livro conquistado, teto por período; reforja grátis por nerf), Forja com 5 raridades, companheiros, auto e varredura (com teto diário de recompensa), leaderboard simples; monetização conforme o modelo de negócio (em aberto) | 13 a 20 meses (esperado: 16) |
| **Pós-lançamento** | Na ordem: (1) capítulos 3 e 4; (2) coop PvE de 4 humanos; (3) ranking por função validado no servidor; (4) runas; (5) Elfo e Anão; (6) PvP em tempo real | Coop com companheiros preenchendo as vagas da fila, servidor autoritativo, live ops | Contínuo; o coop sozinho leva de 8 a 11 meses de trabalho |
| **Full Vision** | 4 raças × 2 gêneros, 4 capítulos com uns 40 estágios, de 15 a 20 inimigos, de 6 a 8 chefes, de 40 a 60 skills mais 4 raciais | Tudo acima, polido, com coop PvE e PvP | 48 a 72 meses (o producer estima 60 ou mais) |

**Como vamos saber se estamos no caminho** (D0 = data do 1º sprint do MVP, registrada só depois do commit do doc de aceite do MVP):
- **MVP fechado** significa todos os critérios de aceite acima que têm PASS/FAIL em PASS, com a Escassez fechada (setup e invariantes passando; as métricas de oferta, depois que o doc de aceite as definir) (os Sinais só registram) e os itens 1 a 7 com stories em Done. Verde até D0 + 3 meses, amarelo entre 3 e 4 meses, vermelho acima de 4 meses. No vermelho, aplica-se o multiplicador dos Scope Risks.
- O spike de performance passa até D0 + 21 dias, com a semana 0 concluída antes de D0.
- Até D0 + 10 meses, o designer completa as fases e o chefe do capítulo 1 numa única run, com a trindade de companheiros, no aparelho de referência, com zero bugs S1 abertos. Se esse marco escorregar mais de 2 meses, o capítulo 2 vira atualização pós-lançamento.

---

## Prototype Findings

**Protótipo do Grimório + selamento** (2026-11-02, HTML, `prototypes/grimorio-concept/REPORT.md`). Veredito PROCEED; o CD-PLAYTEST deu CONCERNS, aceito com ressalvas. Houve 1 testador, o próprio designer.

- **Confirmado:** reroll + favorecer bastaram contra a sensação de caça-níquel. O pico foi jogar a Prova do Selo com a build selada no nível máximo, e isso virou a regra do loop depois do selo.
- **Não confirmado:** o "só mais uma" (voltar para registrar uma skill específica) ficou 0 de 1, e segue como hipótese. A justificativa do selo foi por eficácia ("me ajudaram"), não por identidade.
- **Estrutural:** com 6 slots e registro automático, o Grimório chegou a 11 de 12 skills em 3 fases. Daí veio a regra de escassez por escolha.
- **Controle:** o movimento deve ser por cursor ou joystick de um dedo, não WASD.
- **Não avaliado:** sensação de combate (Pilar 4), Tank (Pilar 3), raça (Pilar 5) e performance.

---

## Next Steps

O conceito está bem definido, mas o loop central (o selamento é divertido? o Tank funciona sozinho? a horda roda no aparelho?) ainda não foi provado. Por isso o caminho é **prototype-first**:

- [x] Configurar o engine e a referência de versão (`/setup-engine`: Unity 6.3 LTS, 6000.3.27f1)
- [ ] Escrever o doc de aceite do MVP (`docs/acceptance/mvp.md`: políticas, função de poder, proxies com piso, limiar de PASS e metodologia de frame time, registro de bugs), com commit e revisão do qa-lead **antes de D0**
- **Prototipar o loop central:**
  - [x] Grimório + selamento (`/prototype`, HTML, 2026-11-02): PROCEED, CD com CONCERNS
  - [ ] Tank divertido sozinho (2º risco de design)
- [ ] Definir a identidade visual (`/art-bible`)
- [ ] Validar este conceito (`/design-review design/gdd/game-concept.md`): falta um re-review completo; o histórico está no log de revisões
- [ ] Decidir o modelo de negócio (F2P ou premium) **antes** do GDD de economia
- [ ] Decompor o conceito em sistemas (`/map-systems`)
- [ ] Desenhar cada sistema (`/design-system [system-name]`), com `/design-review` depois de cada GDD
- [ ] Revisar todos os GDDs (`/review-all-gdds`)
- [ ] Criar a arquitetura (`/create-architecture`) e os ADRs (`/architecture-decision`), começando pela separação simulação/apresentação e pela economia transacional
- [ ] Revisar a arquitetura (`/architecture-review`)
- [ ] Planejar o primeiro sprint (`/sprint-plan new`): a data de início é D0
- [ ] Spike de performance da horda (semanas 1 a 3 após D0; depende da semana 0: módulo Android e aparelho de referência)
- [ ] Construir o vertical slice (`/vertical-slice`) e validá-lo com playtest (`/playtest-report`)
