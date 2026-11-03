# Game Concept: Forja das Hordas

*Created: 2026-11-02*
*Status: Draft*
*Título provisório. Revisões do brainstorm: CD-PILLARS (CONCERNS, resolvido), AD-CONCEPT-VISUAL (CONCEPTS), TD-FEASIBILITY (HIGH RISK para o coop no lançamento, resolvido no escopo), PR-SCOPE (OPTIMISTIC, ajustes aplicados).*

---

## Elevator Pitch

> É um RPG mobile de sobrevivência contra hordas em que você enfrenta ondas de inimigos escolhendo skills aleatórias a cada level up, até descobrir a build que funciona. Aí você **sela** essa build para sempre e leva o seu herói, forjado no fogo das hordas, para dungeons com a trindade clássica de tanque, DPS, mago e healer.

---

## Core Identity

| Aspect | Detail |
| ---- | ---- |
| **Genre** | Ação RPG / survivor de hordas (roguelite por fase) com progressão de personagem e equipamento estilo MMORPG |
| **Platform** | Mobile (iOS e Android) |
| **Target Audience** | Jogadores mid-core e hardcore mobile que otimizam builds e equipamento (ver Target Player Profile) |
| **Player Count** | Single-player no lançamento (com companheiros NPC na trindade); coop PvE de 4 e PvP em tempo real no pós-lançamento |
| **Session Length** | Fase de 3 a 5 min; sessão típica de 20 a 60 min |
| **Monetization** | F2P, só conveniência e cosmético, regido pelo Princípio de Negócio (ver Game Pillars). Premium ou soft launch seguem como questão aberta |
| **Estimated Scope** | Large (48 a 72 meses, solo) na visão completa; o lançamento ajustado leva de 16 a 20 meses, solo |
| **Comparable Titles** | Survivor.io e Archero (loop de horda com skill aleatória), Summoners War (otimização de equipamento e runas), MIR4 e Lineage 2M (progressão de MMORPG no mobile) |

---

## Core Fantasy

**"Eu forjei este herói no fogo das hordas, e cada skill dele foi conquistada."**

O jogador não recebe um herói pronto nem sorteia um em gacha: ele o **constrói** testando skills e sets contra ondas de inimigos até encontrar a combinação que é só dele. Quando sela a build, ele sela a própria identidade no jogo. A partir daí, esse herói é o Orc tanque que segura a linha para o grupo inteiro, ou a Elfa healer que mantém todos vivos no chefe. É a sensação de uma dungeon como Zul'Farrak, com um personagem que você mesmo forjou.

*Por que essa fantasia, e não as alternativas:* "colecionar heróis" (Summoners War) foi descartada porque dilui a identidade (a coleção de legados ficou de fora do conceito). "Power fantasy pura" (survivor clássico) foi descartada porque não deixa nada permanente depois da run. O selamento une as duas pontas: tem a liberdade do roguelite e o peso de um personagem de MMO.

---

## Unique Hook

**É como um survivor de hordas mobile (skill aleatória a cada level up), E TAMBÉM a build que você descobre vira um personagem permanente de RPG, selado para sempre, que você leva para dungeons com a trindade clássica.**

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
| **Fellowship** (social connection) | 4 | Trindade com companheiros NPC no lançamento; coop PvE de 4 humanos no pós-lançamento |
| **Sensation** (sensory pleasure) | 5 | Massacre da horda com feedback em massa; hit-stop e knockback nos golpes pesados; o ritual de forja do selamento |
| **Discovery** (exploration, secrets) | 6 | Sinergias e evoluções de skill a descobrir; o Grimório como um catálogo a completar |
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
2. **Skill aleatória por fase + Grimório:** a cada level up dentro da fase, você escolhe 1 de 3 skills ou melhorias (temporárias), com evoluções por sinergia. As skills usadas para vencer um chefe ficam registradas no Grimório permanente.
3. **Selamento da build:** no nível de selamento, você escolhe do Grimório as skills definitivas e o set. É permanente; o reset é feito com o Livro de Reforja.
4. **Forja e sets por raridade:** materiais de cinco raridades (Branco → Verde → Azul → Roxo → Dourado) craftam e melhoram peças de set por função.
5. **Trindade com companheiros:** dungeons com tanque, DPS, mago e healer; no lançamento, as vagas que você não ocupa são preenchidas por companheiros NPC.

---

## Player Motivation Profile

### Primary Psychological Needs Served

| Need | How This Game Satisfies It | Strength |
| ---- | ---- | ---- |
| **Autonomy** (freedom, meaningful choice) | Raça, gênero, função, skills do Grimório, set e (no pós-lançamento) runas: a identidade do herói é escolha do jogador, e o selamento dá peso a essa escolha | Core |
| **Competence** (mastery, skill growth) | Esquiva contra telegraphs, leitura de sinergias, waves mais difíceis, ranking por função como prova pública | Core |
| **Relatedness** (connection, belonging) | Trindade: no lançamento com companheiros NPC; no pós-lançamento, o grupo humano precisa do seu tanque ou do seu healer | Supporting (Core no pós-lançamento) |

### Player Type Appeal (Bartle Taxonomy)

- [x] **Achievers** (goal completion, collection, progression) — How: set dourado completo, Grimório completo, nível de selamento, ranking por função. **Primário**, junto com os criadores de build (Quantic Foundry: Estratégia + Conclusão).
- [x] **Explorers** (discovery, understanding systems, finding secrets) — How: descobrir sinergias e evoluções de skill; entender o sistema de build a fundo.
- [x] **Socializers** (relationships, cooperation, community) — How: coop PvE com a trindade (pós-lançamento); compartilhar builds. **Secundário.**
- [x] **Killers/Competitors** (domination, PvP, leaderboards) — How: ranking por função; PvP em tempo real no pós-lançamento. **Terciário.**

**Não é para:** quem busca história linear (Storyteller), quem quer relaxar sem compromisso (o selamento pesa), e quem quer colecionar heróis por gacha.

### Flow State Design

- **Onboarding curve:** os primeiros 10 minutos são a fase de origem da raça escolhida. Ela ensina o movimento e o auto-ataque na primeira wave, a escolha de skill no primeiro level up, a esquiva no primeiro elite e a suprema no primeiro chefe. O Grimório e a Forja aparecem depois do primeiro chefe; o selamento só é explicado quando o jogador se aproxima do nível de selamento.
- **Difficulty scaling:** a densidade da horda e a frequência de elites crescem por fase. Os chefes introduzem um padrão de telegraph novo por capítulo. O conteúdo novo é sempre manual; o conteúdo vencido pode ir para o auto.
- **Feedback clarity:** feedback de massa (inimigos caindo em cadeia), números de dano legíveis, telegraphs que nunca ficam escondidos (a camada mais alta da tela), registro visível no Grimório a cada chefe vencido, e o Poder de Combate visível.
- **Recovery from failure:** morrer numa fase custa de 3 a 5 minutos, e o jogador fica com os materiais coletados até ali (taxa a definir no GDD). O erro realmente punitivo é o selamento mal planejado, mitigado pelo Livro de Reforja (que pode ser conquistado) e pelos slots extras de herói conquistados jogando.

---

## Core Loop

### Moment-to-Moment (30 seconds)

O jogador se move com um dedo, enquanto o auto-ataque e as skills varrem a horda e ele coleta orbes de XP. Um elite aparece e marca no chão um golpe em área; o jogador esquiva no último instante e pune com a suprema.

O loop é satisfatório por si só porque alterna dois prazeres:
- **Descarga:** dezenas de inimigos caindo de uma vez, com explosões em cadeia e feedback visual em massa.
- **Tensão:** um erro contra o elite custa caro, e o hit-stop e o knockback dão peso a cada golpe.

A sensação escolhida é uma média entre *massacre em massa* e *pesado e impactante*. A alternativa *tático e posicional* foi descartada como sensação principal, mas fica parcialmente presente nas fases de função.

### Short-Term (5-15 minutes)

Uma **fase** é formada por várias waves mais um chefe, de 3 a 5 minutos no total. A cada level up dentro da fase, o jogador escolhe 1 de 3 skills ou uma melhoria de uma skill que já tem, e algumas combinações evoluem por sinergia.

- **Agência sobre o sorteio** (para que o selamento não vire caça-níquel): 1 reroll por fase, e a possibilidade de **favorecer uma skill já registrada no Grimório**, que passa a aparecer com mais frequência. Os números exatos são knobs.
- **O "só mais uma":** a chance de uma combinação de skills melhor na próxima tentativa, e o drop de material de raridade alta no chefe.
- **Fases de função:** objetivos como escoltar ou proteger um NPC, nos quais Tank e Healer brilham. Toda skill de função também tem **uso solo** (por exemplo, a cura gera um escudo que explode; a provocação puxa a horda para um ponto e reflete dano), para que Tank e Healer consigam forjar a build sozinhos.

### Session-Level (30-120 minutes)

No mobile, a sessão típica dura de 20 a 60 minutos.
- **Antes do selamento:** fase → Forja → fase. O jogador gasta materiais na Forja para craftar e melhorar peças de set e testa outra combinação.
- **Depois do selamento:** dungeon com a trindade → Forja → farm no auto → conteúdo novo.
- **Pontos de parada naturais:** o fim de cada chefe.
- **O gancho para voltar:** ficar a poucos materiais da próxima peça de set, as dungeons diárias de material e o próximo registro no Grimório.

### Long-Term Progression

1. **Antes do selamento:** o jogador sobe de nível pela campanha. As skills dentro da fase são temporárias (roguelite), mas cada skill usada para vencer um chefe é registrada no **Grimório**. Testar skills e sets é o próprio jogo.
2. **Selamento** (no nível de selamento, um knob): o jogador escolhe no Grimório as skills definitivas e fixa a build, encenado como um **ritual de forja**. É **definitivo**, e só o **Livro de Reforja** desfaz.
3. **Depois do selamento:** dungeons com a trindade, peças de set aleatórias e materiais, set dourado completo e ranking por função. No pós-lançamento entram runas, coop de 4 humanos e PvP.
4. **Novos heróis:** slots extras de herói são **conquistados jogando**, então o custo de um selamento ruim é tempo, não dinheiro, e o momento de expressão se renova.

O jogo "termina" quando o jogador tem o set dourado da sua função e um lugar no ranking. Depois disso, o conteúdo de capítulos e as temporadas sustentam o jogo.

### Retention Hooks

- **Curiosity:** sinergias e evoluções de skill ainda não descobertas; os próximos capítulos; as fases de origem das outras raças.
- **Investment:** o herói selado, o Grimório e o set em construção, ou seja, o progresso que o jogador não quer perder.
- **Social:** compartilhar builds; no pós-lançamento, o grupo de coop que depende da sua função.
- **Mastery:** esquiva contra chefes mais difíceis, tempo de clear e posição no ranking por função.

---

## Game Pillars

Os pilares foram travados pelo usuário e revisados pelo creative-director (CD-PILLARS: CONCERNS). As cinco correções propostas foram aplicadas. Existem tensões deliberadas entre eles:
- o pilar 1 contra o 3 (expressão contra papel fixo);
- o pilar 2 contra o Princípio de Negócio, por causa do Livro de Reforja;
- o pilar 1 contra o 4 (build vistosa contra leitura do perigo).

### Pillar 1: Sua build, sua assinatura

Dois heróis no nível máximo não devem parecer iguais.

*Design test:* entre "mais poder bruto" e "mais opções distintas de build", escolhe as opções distintas.

*Critério mensurável (sugerido pelo CD):* no top 100 de cada função, nenhum conjunto de skills seladas aparece em mais de X% dos heróis. X é um knob, e a medição é feita por analytics.

*Consequência aplicada:* o ranking é **por função e por desempenho** (tempo de clear de dungeon; PvP por rating), e não por Poder de Combate. O Poder de Combate continua visível e serve de requisito de entrada em conteúdo, mas **não é o placar**. Essa decisão substitui o pedido original de ranking por poder de combate, que faria as builds convergirem.

### Pillar 2: Toda escolha pesa

Decisões de build são permanentes e têm consequência.

*Design test:* entre conveniência e consequência, escolhe consequência. O reset existe, mas é raro e custa.

*Consequências aplicadas:*
- O **Livro de Reforja** pode ser conquistado jogando (recompensa rara de temporada ou de dungeon), e a loja vende o atalho.
- **Política de nerf:** toda alteração de balanceamento numa skill dá **reforja grátis** a quem a selou.
- Slots extras de herói são conquistados jogando.

### Pillar 3: Cada função é indispensável

No coop, tanque, DPS, mago e healer fazem coisas que os outros não fazem.

*Design test:* entre "qualquer função consegue solo" e "o grupo precisa da trindade", no coop escolhe a trindade.

*Consequências aplicadas:*
- Toda skill de função tem **uso solo**, para que a função possa ser forjada sozinha.
- Existem **fases de função** (escoltar ou proteger).
- No lançamento, **companheiros NPC** ocupam as vagas da trindade. No pós-lançamento, eles preenchem as vagas vazias da fila de coop, o que ajuda com a falta de tanques e healers.
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

*Linha exata:* **nenhuma compra aumenta o Poder de Combate nem a quantidade de recompensas por dia.**
- Ticket de varredura só economiza tempo; ele não adiciona entradas.
- O Livro de Reforja vende flexibilidade (um atalho para algo que também se conquista jogando), nunca poder.
- Cosméticos não podem imitar o vocabulário visual de raridade ou de runa.

### Anti-Pillars (What This Game Is NOT)

- **NOT gacha de heróis:** comprometeria *Sua build, sua assinatura*. O herói é construído, não sorteado.
- **NOT venda de sets, runas ou materiais de raridade alta na loja:** comprometeria o *Princípio de Negócio*.
- **NOT venda de skills ou de entradas do Grimório:** comprometeria os pilares 1 e 2. A build vem do jogo.
- **NOT correção paga de selamento além do Livro de Reforja**, e o Livro também pode ser obtido jogando. Isso fecha a brecha do *Princípio de Negócio*.
- **NOT auto-battle em conteúdo inédito, coop ou competitivo:** comprometeria *Massacre com peso*. Conteúdo já vencido pode ser repetido no auto ou na varredura, com rendimento um pouco menor que o manual.
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
| World of Warcraft (Zul'Farrak) | A trindade; dungeons com identidade forte; a fantasia de ser a raça | No formato de hordas; companheiros NPC no lançamento | É a memória que define o projeto; valida o apelo da trindade |
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
| **Key Technical Challenges** | (1) Centenas de inimigos animados com heróis realistas em Android intermediário: animação por partes rígidas ou VAT, instancing, Jobs/Burst; o overdraw de partículas é o gargalo provável; throttling térmico. (2) No pós-lançamento: coop em tempo real em rede móvel, PvP com servidor autoritativo e anti-cheat. (3) Um backend leve no lançamento: cloud save, validação de IAP e leaderboard |
| **Art Style** | 3D realista nos heróis, chefes e na Forja; 3D simplificado em bloco na horda ("Hierarquia do Detalhe") |
| **Art Pipeline Complexity** | High (3D personalizado). Mitigação: personagens modulares, esqueleto compartilhado, raridade por material, assets comprados como base |
| **Audio Needs** | Moderate: feedback de impacto e de massa, áudio dos telegraphs, voz por raça (pilar 5), o ritual da Forja |
| **Networking** | Lançamento: None no gameplay, com backend leve (cloud save, IAP, leaderboard). Pós-lançamento: coop com host ou servidor autoritativo; PvP em tempo real com servidor dedicado ou autoritativo. A tecnologia exige um ADR, porque nenhum backend está na referência do engine |
| **Content Volume** | Lançamento: 2 raças, 4 funções, 2 capítulos com 20 fases, de 8 a 10 inimigos, de 3 a 4 chefes, de 25 a 30 skills mais 2 raciais, sets por função em 5 raridades. Visão completa: 4 raças × 2 gêneros, 4 capítulos com uns 40 estágios, de 15 a 20 inimigos, de 6 a 8 chefes, de 40 a 60 skills mais 4 raciais, runas |
| **Procedural Systems** | Composição das waves por seed (útil para o auto-battle e para validação por replay); o drop de peças e runas é aleatório; as fases são feitas à mão |

**Decisões de arquitetura baratas agora e caras depois** (recomendação do TD, para registrar como ADRs depois do `/setup-engine`):
1. **Separar simulação de apresentação:** tick fixo, RNG com seed, lógica de combate sem MonoBehaviour. Isso viabiliza o auto-battle, o replay para validar o ranking e a autoridade de host no futuro.
2. **Progressão e economia como transações puras sobre dados**, que rodam no cliente offline e depois no servidor sem reescrita.
3. **Remote config para balanceamento** desde o início.

---

## Risks and Open Questions

### Design Risks

- **Skill aleatória somada ao selamento permanente pode parecer caça-níquel** ("rodei a fase 40 vezes"). Mitigação: reroll, favorecer skills do Grimório, escolha garantida após o chefe (a validar no MVP).
- **Tank e Healer podem não ser divertidos sozinhos.** Mitigação: uso solo das skills de função e fases de função. O MVP testa isso explicitamente.
- **Meta resolvido:** tier lists convergem as builds em semanas. Mitigação: ranking por função e por desempenho, critério de diversidade mensurável, raças pela identidade e não pelo atributo.
- **Balancear raça × função × skill × set × runa** é combinatoriamente pesado, sobretudo no PvP.
- **Nerf em build selada** gera revolta. Mitigação: política de reforja grátis.

### Technical Risks

- **Performance da horda em Android intermediário** (MEDIUM, segundo o TD). O spike é obrigatório: 300 inimigos, 4 heróis, efeitos e um chefe, medidos no **minuto 20** (por causa do aquecimento do aparelho).
- **Coop em tempo real em rede móvel** (HIGH no lançamento, segundo o TD): reconexão, app em segundo plano, latência de 80 a 200 ms contra esquiva no timing, sincronização da horda. **Movido para o pós-lançamento.**
- **PvP em tempo real** (HIGH, segundo o TD): servidor autoritativo, anti-cheat, predição. O usuário escolheu tempo real em vez de assíncrono. O TD recomendou o assíncrono como alternativa viável e íntegra para um dev solo, e essa recomendação fica registrada. **É o último item do pós-lançamento.**
- **Integridade do ranking:** um score calculado no cliente é trapaceado. O leaderboard do lançamento é casual; o ranking competitivo exige validação no servidor.
- **NOT SOURCEABLE:** Netcode for Entities, Relay/Lobby, UGS, Unity IAP, o GPU Resident Drawer em mobile e em malhas skinned, o VFX Graph em mobile, e o licenciamento atual do Unity não estão cobertos por `docs/engine-reference/unity/`. Cada um precisa de verificação ou de um ADR.
- **Fragmentação de Android:** hitches de compilação de shader (Adreno e Mali), explosão de variantes de shader no URP.

### Market Risks

- O gênero survivor está saturado, e os MMORPGs mobile têm orçamentos gigantes.
- A arte realista feita por uma pessoa compete com estúdios.
- O Princípio de Negócio (sem venda de poder) limita a receita de um F2P, e a aquisição de usuário custa caro.
- Um lançamento só single-player perde o diferencial social no primeiro dia.

### Scope Risks

- **Volume de arte:** cerca de 400 encaixes de peça no lançamento sem a regra de raridade por material (cálculo do producer). Com raridade por material, o multiplicador de 5× vira 1×. O Anão é o caso difícil de *fit*.
- **Backend e live ops** concorrem com o roadmap pós-lançamento. É preciso planejar uma cadência mínima (por exemplo, um evento por mês e um capítulo por trimestre).
- **Nenhuma estimativa está calibrada:** o MVP calibra a velocidade real. Se ele levar mais de 4 meses, multiplicar todas as faixas pela razão do atraso.
- **Ponto de corte mais provável:** entre o mês 16 e o 20, com a campanha incompleta. Os capítulos são unidades lançáveis, então o corte vira "lançar com menos capítulos".

### Open Questions

- **Formato do PvP diante do pilar 3:** é 1v1, em grupo, ou só por função? Um Healer vale alguma coisa no 1v1? A resposta vai no GDD de PvP antes de ele entrar no roadmap.
- **Modelo de negócio:** F2P com soft launch em poucos países, ou premium? Será decidido antes do Pre-Production, com dados do vertical slice.
- **Gênero do herói:** a premissa é que masculino e feminino são só visuais, sem diferença de atributo. Confirmar no GDD de raças.
- **Nível de selamento e número de skills seladas:** são knobs a calibrar no MVP.
- **Quanto material o jogador guarda ao morrer numa fase:** será definido no GDD da economia.
- **Agência sobre o sorteio:** reroll, favorecer skills e escolha garantida após o chefe. Qual combinação elimina a sensação de caça-níquel? O MVP responde.
- **Backend gerenciado ou próprio (UGS, PlayFab, Nakama ou Firebase):** será decidido por ADR.

---

## MVP Definition

**Core hypothesis:** *"Forjar uma build em fases de horda, com skills aleatórias registradas no Grimório e seladas para sempre, é divertido para DPS e também para Tank, em sessões de mais de 20 minutos, e roda num Android intermediário."*

**Required for MVP:**
1. Combate híbrido (horda, elites com telegraph, esquiva, suprema) com o Orc.
2. Duas funções, **DPS e Tank**, para testar logo se o Tank consegue forjar a build sozinho.
3. 1 capítulo com 5 fases e um chefe, e cerca de 15 skills com sinergias.
4. Grimório e selamento, incluindo o ritual básico.
5. Forja com 3 raridades.
6. Tudo **offline**.

**Critérios de aceite do MVP** (definidos pelo producer e pelo TD):
- **Performance:** um número concreto de inimigos simultâneos (alvo: 300) a 60 fps, com piso de 30 fps, num **aparelho Android intermediário definido**, medido no minuto 20. É o primeiro spike, nas semanas 1 a 3. Se ele falhar, o conceito é revisto antes de qualquer outra coisa.
- **Pipeline de arte:** 1 herói realista com 2 tiers de set visíveis, rodando no aparelho alvo. Isso prova o custo por peça.
- **O Tank é divertido sozinho?** Uma sessão de playtest em que o jogador de Tank consegue vencer o capítulo e quer selar uma build de Tank.

**Explicitly NOT in MVP** (defer to later):
- Healer, Mago, outras raças e companheiros NPC
- Coop, PvP, ranking e backend
- Runas, loja, Livro de Reforja, auto-battle e varredura
- Arte final (o MVP usa arte de loja ou placeholder)

### Scope Tiers (if budget/time shrinks)

Estimativas solo, ainda **sem calibração**. A ordem foi corrigida pelo producer: cada tier é um superconjunto do anterior, e os companheiros NPC vêm antes do coop.

| Tier | Content | Features | Timeline |
| ---- | ---- | ---- | ---- |
| **MVP** | Orc; DPS e Tank; 1 capítulo com 5 fases; cerca de 15 skills | Combate, Grimório, selamento, Forja com 3 raridades; offline | 2,5 a 4,5 meses (esperado: 3) |
| **Vertical Slice** | Capítulo 1 completo com companheiros; arte final de 1 herói | As 4 funções, companheiros NPC na trindade, Forja com 5 raridades | Marco: capítulo 1 jogável com companheiros até o mês 10 |
| **Lançamento (single-player ajustado)** | 2 raças (Orc e Humano), 4 funções, 2 capítulos com 20 fases, de 8 a 10 inimigos, de 3 a 4 chefes, de 25 a 30 skills | Selamento, Livro de Reforja, Forja com 5 raridades, companheiros NPC, auto e varredura, leaderboard simples, IAP de conveniência e cosmético | 13 a 20 meses (esperado: 16) |
| **Pós-lançamento** | Na ordem: (1) capítulos 3 e 4; (2) coop PvE de 4 humanos; (3) ranking por função validado no servidor; (4) runas; (5) Elfo e Anão; (6) PvP em tempo real | Coop com companheiros preenchendo as vagas da fila, servidor autoritativo, live ops | Contínuo; o coop sozinho leva de 8 a 11 meses de trabalho |
| **Full Vision** | 4 raças × 2 gêneros, 4 capítulos com uns 40 estágios, de 15 a 20 inimigos, de 6 a 8 chefes, de 40 a 60 skills mais 4 raciais | Tudo acima, polido, com coop PvE e PvP | 48 a 72 meses (o producer estima 60 ou mais) |

**Como vamos saber se estamos no caminho:**
- O MVP fecha em até 3 meses.
- O spike de performance passa até a semana 3.
- O capítulo 1 com companheiros está jogável no mês 10. Se esse marco escorregar mais de 2 meses, o capítulo 2 vira atualização pós-lançamento.

---

## Next Steps

O conceito está bem definido, mas o loop central (o selamento é divertido? o Tank funciona sozinho? a horda roda no aparelho?) ainda não foi provado. Por isso o caminho é **prototype-first**:

- [ ] Configurar o engine e a referência de versão (`/setup-engine`, preferência: Unity)
- [ ] **Prototipar o loop central** (`/prototype` horda + Grimório + selamento, com DPS e Tank, incluindo o spike de performance)
- [ ] Se o protótipo for adiante (PROCEED): definir a identidade visual (`/art-bible`)
- [ ] Validar este conceito (`/design-review design/gdd/game-concept.md`)
- [ ] Decompor o conceito em sistemas (`/map-systems`)
- [ ] Desenhar cada sistema (`/design-system [system-name]`), com `/design-review` depois de cada GDD
- [ ] Revisar todos os GDDs (`/review-all-gdds`)
- [ ] Criar a arquitetura (`/create-architecture`) e os ADRs (`/architecture-decision`), começando pela separação simulação/apresentação e pela economia transacional
- [ ] Revisar a arquitetura (`/architecture-review`)
- [ ] Construir o vertical slice (`/vertical-slice`) e validá-lo com playtest (`/playtest-report`)
- [ ] Planejar o primeiro sprint (`/sprint-plan new`)
