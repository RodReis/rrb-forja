# Systems Index: Forja das Hordas

> **Status**: Draft
> **Created**: 2026-11-03
> **Last Updated**: 2026-11-03
> **Source Concept**: design/gdd/game-concept.md (congelado; o histórico de revisões está em design/gdd/reviews/game-concept-review-log.md)

---

## Overview

Forja das Hordas é um RPG mobile de ação em que o jogador descobre uma build em fases de horda e a sela de forma permanente. O escopo mecânico cobre três coisas ao mesmo tempo: um survivor de hordas (combate com um dedo, skill aleatória a cada level up), um sistema de identidade (o Grimório e o selamento) e um RPG de equipamento de MMO (Forja, sets por função, trindade de tanque, DPS, mago e healer). O índice enumera **40 sistemas** em 4 tiers: 19 de MVP, 7 de Vertical Slice, 10 de Alpha (o lançamento ajustado) e 4 de Full Vision (pós-lançamento). Os pilares que guiam a prioridade são: P1 *Sua build, sua assinatura*, P2 *Toda escolha pesa*, P3 *Cada função é indispensável*, P4 *Massacre com peso* e P5 *Ser a raça, não vestir a raça*, mais o Princípio de Negócio *Poder conquistado, não comprado*.

O desenho tem um núcleo estreito e arriscado: a simulação determinística (#2), o Grimório (#16) e o Selamento (#17). Quase tudo o mais depende de um dos três ou os alimenta. O resto é conteúdo e acabamento sobre esse núcleo, e a economia (#26, #27) é o ponto em que o Princípio de Negócio vira regra de produto.

### Core: o chão técnico da run

**#1 Dados e balanceamento.** Dono de todo valor de gameplay como dado externo (os knobs de cada GDD moram aqui), e do ponto de injeção do remote config no pós-lançamento. Sem ele os GDDs viram constantes no código, o que o padrão do projeto proíbe. Não depende de rede: o remote config entra como provedor que os Serviços online (#29) injetam.

**#2 Simulação de combate determinística.** Tick fixo, RNG com seed e **streams independentes** (spawn, oferta de cartas, loot), lógica de combate sem MonoBehaviour. É o gargalo do grafo (10 ou mais sistemas dependem dele) e o maior risco técnico: a comparação Tank × DPS na mesma seed, a simulação headless do MVP e o auto-battle dependem dela. A gravação de replay saiu do MVP por decisão do Producer (vai para Full Vision com o coop e o ranking validado); o MVP só exige reprodutibilidade no mesmo build. Um ADR fixa o tipo numérico (inteiro, ponto fixo ou float) e a interface antes dos GDDs de Combate, Horda e Skills.

**#3 Fluxo de fase (inferido).** Máquina de estados da run: waves, chefe, resultado, morte, retry, e os ganchos de início de fase, level-up e chefe vencido. Contém também o XP e o nível dentro da fase, que disparam a oferta de cartas. É lógica pura, sem input nem apresentação, para que a simulação headless e o auto-battle a rodem sozinhos. O Grimório (#16) se registra nos ganchos; o fluxo de fase não o conhece.

**#4 Input e câmera de combate.** Joystick de um dedo, botão de esquiva, suprema ativa e câmera alta. Fica na camada de Presentation, separado do fluxo de fase, para que nada da simulação referencie input.

**#5 Log de eventos e instrumentação de aceite.** Log exportável (escolhas, registros, selo, mortes, tempos), seeds e a simulação headless que chama o mesmo código do jogo. É a fonte de toda medição de aceite do MVP e só carrega telemetria; a gravação de replay não vive aqui.

### Gameplay: o que torna o jogo divertido

**#6 Combate e dano.** Dano, vida, esquiva no timing, hit-stop e knockback. Dá o peso do Pilar 4: a horda derrete e o elite bate forte. É dependência de quase todo sistema de gameplay.

**#7 Horda, waves e inimigos.** Composição das waves por seed, spawn, densidade, elites e chefes com telegraphs, e um padrão novo por capítulo. A contagem de inimigos e a densidade de efeitos são **Tuning Knobs**, nunca regra fixa, porque o spike de performance no Android pode mudá-las.

**#8 Skills e evoluções.** Catálogo de skills ativas e passivas, níveis e sinergias, filtrado pela função do herói. Seu custo escondido é a árvore de modificadores pós-selo (cerca de 4 por skill, uns 60 cards no lançamento). Define o que cada skill dá e o que é "elegível" para o Grimório.

**#9 Oferta de cartas no level-up.** 1 de 3 skills ou melhorias, 1 reroll por fase e o "favorecer" uma skill já registrada. É onde a agência do jogador sobre o sorteio vive, e o ponto em que o selamento pode virar caça-níquel (Risco de Design do conceito). Lê o Grimório só para o favorecer.

**#10 Funções.** Tank, DPS, Mago e Healer, cada um com um verbo exclusivo (segurar, manter vivo, dano focado, controlar). Toda skill de função tem uso solo, para o Tank e o Healer poderem forjar a build sozinhos (Pilar 3). O MVP implementa DPS e Tank.

**#11 Raças (Vertical Slice).** Skill racial, atributos, animações, voz e fase de origem (Pilar 5). No MVP o Orc é um stub em Dados e o GDD generaliza isso quando entra a segunda raça. A skill racial fica fora dos slots do selo.

**#12 Feedback de combate, VFX e HUD.** Hit-stop visual, feedback em massa, telegraph sempre na camada mais alta, limites de opacidade e densidade ajustáveis, números de dano. Reúne o que o jogador sente e lê em combate (Pilar 4). Depende do `/art-bible` e do orçamento de partículas medido no spike. A evidência visual é bloqueante no padrão de testes do projeto.

**#13 IA de herói e companheiro (inferido).** Ninguém a citou no conceito, mas três sistemas precisam dela: os companheiros da trindade (#14), o auto-battle (#15, que joga a fase sozinho) e o preenchimento de vagas do coop (#35). Estava escondida em Dungeons; o TD pediu o sistema próprio.

**#14 Dungeons e trindade.** Dungeons com tanque, DPS, mago e healer preenchidos pelos heróis selados do jogador ou por um NPC com teto; fases de função (escoltar, proteger); affixes que dependem do controle do Mago. É onde o Pilar 3 só pode ser validado (a partir do Vertical Slice).

**#15 Varredura (Alpha).** Repete conteúdo já vencido e credita a recompensa dentro do teto diário, sem simular a fase. Sem energia, o teto sem varredura viraria tarefa diária. Nunca registra no Grimório, nunca conta vitória para o selo e nunca conta para o ranking. O auto-battle saiu para o #40.

### Progression: como o herói cresce e vira permanente

**#16 Grimório.** Registro de até 1 skill por chefe de fase vencido, capacidade C, K_min, a garantia e o Códex da conta. É o sistema mais arriscado do desenho: o conceito já passou por seis revisões em torno dele. O GDD do Grimório vira a fonte da verdade das regras que hoje estão em L80, L81 e L407 do conceito. A função de "selável" é implementada como função pura dentro do módulo do Grimório, e o contador de vitórias de chefe de fase por herói também é dele.

**#17 Selamento da build.** Escolha das 4 skills definitivas (2 de função e 2 livres), o ritual de forja, a Prova do Selo e o teto de nível antes do selo. É dono do predicado de selabilidade e do K_min como especificação, e o Grimório o implementa. O risco de design conhecido é o selo ser só uma confirmação (descartar 1 de 5).

**#18 Reforja (Alpha).** O Livro de Reforja (1 por herói por período, nunca vendido), a run de reforja e a reforja grátis por nerf. Fecha a saída do selamento permanente (Pilar 2). Ela toca a identidade, então um corte dela precisa do aval do creative-director.

**#19 Herói.** Criação (raça, gênero, função), XP e nível, slots de herói conquistados jogando, roster. O estado "selado" é um campo do registro do herói, gravado pelo Selamento; o Herói não depende do Selamento nem do Grimório.

**#20 Campanha e capítulos.** Estrutura de fases e capítulos, chefes de capítulo, desbloqueio e fases de origem por raça. Absorve a narrativa, que o conceito mantém mínima (sem história linear pesada), e por isso não há sistema de diálogo, quests ou cutscenes.

**#21 Poder de Combate (Vertical Slice).** Fórmula calculada só de equipamento e nível, nunca das skills seladas, e a porta de entrada das dungeons. Foi separado do Ranking para quebrar o ciclo com Dungeons.

**#22 Ranking (Alpha).** Placar por função e por desempenho (tempo de clear), critério de diversidade de builds (Pilar 1). Define a regra e os dados; os Serviços online fazem o transporte e a validação.

**#23 Runas (Full Vision).** Pós-lançamento. Entra depois do coop no roadmap do conceito.

### Economy: o que se ganha, se gasta e se compra

**#24 Inventário: materiais, moedas e loot.** Cinco raridades de material, drops de chefe, o que o jogador guarda ao morrer, e a carteira de moedas (que o TD tirou da Economia para não recriar o ciclo).

**#25 Forja e sets.** Craft e melhoria de peças de set por função, 2 a 3 arquétipos por função para o endgame não convergir. Carrega o critério de pipeline de arte do MVP (horas reais por peça).

**#26 Economia e tetos (Vertical Slice).** Fontes, sumidouros, teto diário de recompensa, período do Livro e a auditoria do Princípio de Negócio. Passa ao Vertical Slice por decisão do Producer, porque a Forja de 5 raridades já precisa das regras de fonte e sumidouro. Os tetos continuam Alpha. É projetada depois de #24 e #25 e audita Reforja e Monetização quando elas existem; o valor do teto é dado em #1, sem API que as fontes chamem.

**#27 Monetização e loja (Alpha).** Modelo F2P decidido (ver `design/business-model.md`): todo o conteúdo de gameplay é grátis; a receita vem de cosméticos de loja (skins, transmogs e pets só de animação), com preço direto por SKU e sem moeda premium, e de um vídeo recompensado ao fim da partida que dobra só a moeda de jogo sem poder. O passe de temporada só de cosméticos fica para a 1ª temporada depois do lançamento. Cresceu de M para L com o F2P.

**#38 Cosméticos e catálogo (inferido, Alpha).** Catálogo de loja (skins, transmogs temáticos e pets só de animação), a família de cosméticos de conquista (ganha jogando, visualmente distinta dos de loja) e os cosméticos comprados com a moeda de jogo. Obedece às regras R1, R2 e R7 de `design/business-model.md`: o cosmético nunca altera a leitura do jogo, conquista não se vende e o pet é só animação.

### Persistence: o que sobrevive à sessão

**#28 Save local (inferido).** Só serializa o estado; cada sistema é dono da sua fatia. É o único sistema de persistência do MVP (tudo offline).

**#29 Serviços online (Alpha).** Cloud save, validação de compras, relógio confiável para os tetos, leaderboard, remote config e, no pós-lançamento, validação do ranking e anti-cheat. O ADR de backend e de compras vem antes do GDD #26 (início ou fim do Vertical Slice, em aberto). Com o F2P, o núcleo (validação de compras, relógio, entitlements) deixa de ser cortável. A preferência de fornecedor do usuário é Railway e Supabase; o ADR de backend compara.

**#37 Entitlements (inferido, Alpha).** Interface de leitura das posses de cosméticos comprados. O #29 a alimenta com um token assinado do servidor, e o resto do jogo só lê. O save local nunca guarda posses. Como não há conteúdo de gameplay pago, a Campanha (#20) não a consulta e o #37 saiu do MVP.

### UI, Audio e Meta

**#30 UI de meta-jogo.** Telas de Grimório e ritual do selo, Forja e equipamento, menus e roster. Só exibe e não tem regra própria. O ritual do selo é o momento cerimonial do jogo (princípio visual 3).

**#31 Áudio.** Impacto e massa, áudio do telegraph, voz por raça e o ritual da forja. Pesa no Pilar 4 e no Pilar 5.

**#32 Onboarding.** Os 10 primeiros minutos são a fase de origem; o Grimório e a Forja aparecem depois do primeiro chefe.

**#33 Acessibilidade (inferido).** Raridade por forma (não só cor), opacidade de efeitos, remapeamento. O baseline (texto e telegraph legível para daltônicos) é requisito do GDD do #12 já no Vertical Slice, e nunca é cortado.

**#34 Analytics e live ops.** Diversidade de builds (Pilar 1), eventos e temporadas. Pode ser reduzido ao log do #5 se o orçamento apertar.

**#35 Coop PvE de 4.** Rede, lobby e fila com companheiros. **#36 PvP em tempo real.** Último item do roadmap pós-lançamento (o TD recomendou o assíncrono como alternativa viável; a recomendação está registrada no conceito).

**#39 Consentimento e privacidade (inferido, Alpha).** Consentimento, política de privacidade e formulários das lojas para o analytics, o backend e o cloud save. Bloqueia o soft launch. Cobre também o SDK do vídeo recompensado (só ao fim da partida, no PVE); não há banner nem intersticial.

**#40 Auto-battle com IA (inferido, Full Vision).** A fase jogada sozinha pela IA de herói (#13), em conteúdo já vencido. Saiu do #15 por decisão do usuário. Nunca registra no Grimório, nunca conta vitória para o selo e nunca conta para o ranking.

---

## Systems Enumeration

Legenda: `#n` na coluna Depends On aponta para o número desta tabela. "(inferred)" marca o que o conceito não cita de forma explícita.

| # | System Name | Category | Priority | Status | Design Doc | Depends On |
|---|-------------|----------|----------|--------|------------|------------|
| 1 | Dados e balanceamento | Core | MVP | Designed | [dados-e-balanceamento.md](dados-e-balanceamento.md) | — |
| 2 | Simulação de combate determinística | Core | MVP | Not Started | — | 1 |
| 3 | Fluxo de fase (inferred) | Core | MVP | Not Started | — | 1, 2, 28 |
| 4 | Input e câmera de combate | Core | MVP | Not Started | — | 3 |
| 5 | Log de eventos e instrumentação de aceite | Core | MVP | Not Started | — | 1, 2, 28 |
| 6 | Combate e dano | Gameplay | MVP | Not Started | — | 1, 2 |
| 7 | Horda, waves e inimigos | Gameplay | MVP | Not Started | — | 1, 2, 6 |
| 8 | Skills e evoluções | Gameplay | MVP | Not Started | — | 1, 6, 10 |
| 9 | Oferta de cartas no level-up | Gameplay | MVP | Not Started | — | 2, 3, 8, 10, 16 (leitura) |
| 10 | Funções | Gameplay | MVP | Not Started | — | 1, 6 |
| 11 | Raças | Gameplay | Vertical Slice | Not Started | — | 6, 8 (no MVP: stub do Orc em 1) |
| 12 | Feedback de combate, VFX e HUD | Gameplay | MVP | Not Started | — | 6, 7, 10 |
| 13 | IA de herói e companheiro (inferred) | Gameplay | Vertical Slice | Not Started | — | 2, 6, 10, 17 |
| 14 | Dungeons e trindade | Gameplay | Vertical Slice | Not Started | — | 6, 7, 13, 17, 19, 21 |
| 15 | Varredura | Gameplay | Alpha | Not Started | — | 17, 20, 24, 26 |
| 16 | Grimório | Progression | MVP | Not Started | — | 1, 3, 5, 8, 10, 19, 28 |
| 17 | Selamento da build | Progression | MVP | Not Started | — | 1, 8, 16, 19, 28 |
| 18 | Reforja | Progression | Alpha | Not Started | — | 1, 8, 9, 17, 26 |
| 19 | Herói: criação, nível e roster | Progression | MVP | Not Started | — | 10, 11 (no MVP: stub), 28 |
| 20 | Campanha e capítulos | Progression | MVP | Not Started | — | 3, 7, 11 (no MVP: stub) |
| 21 | Poder de Combate | Progression | Vertical Slice | Not Started | — | 19, 25 |
| 22 | Ranking | Progression | Alpha | Not Started | — | 2, 14, 21, 28 |
| 23 | Runas | Progression | Full Vision | Not Started | — | 19, 21, 25 |
| 24 | Inventário: materiais, moedas e loot | Economy | MVP | Not Started | — | 7, 20 |
| 25 | Forja e sets | Economy | MVP | Not Started | — | 10, 19, 24 |
| 26 | Economia e tetos | Economy | Vertical Slice | Not Started | — | 1, 24, 25, 28 (audita 18 e 27 quando existirem) |
| 27 | Monetização e loja | Economy | Alpha | Not Started | — | 26 |
| 28 | Save local (inferred) | Persistence | MVP | Designed | [save-local.md](save-local.md) | 1 |
| 29 | Serviços online | Persistence | Alpha | Not Started | — | 1, 2, 22, 27, 28, 37 |
| 30 | UI de meta-jogo | UI | MVP | Not Started | — | 16, 17, 19, 24, 25 |
| 31 | Áudio | Audio | Vertical Slice | Not Started | — | 6, 10, 11, 17 |
| 32 | Onboarding | Meta | Vertical Slice | Not Started | — | 16, 20, 30 |
| 33 | Acessibilidade (inferred) | Meta | Alpha | Not Started | — | 12, 25, 30 |
| 34 | Analytics e live ops | Meta | Alpha | Not Started | — | 5, 22, 26 |
| 35 | Coop PvE de 4 | Meta | Full Vision | Not Started | — | 2, 13, 14, 22, 29 |
| 36 | PvP em tempo real | Meta | Full Vision | Not Started | — | 6, 29, 35 |
| 37 | Entitlements (inferred) | Persistence | Alpha | Not Started | — | — |
| 38 | Cosméticos e catálogo (inferred) | Economy | Alpha | Not Started | — | 19, 25, 27, 37 |
| 39 | Consentimento e privacidade (inferred) | Meta | Alpha | Not Started | — | 29, 34 |
| 40 | Auto-battle com IA (inferred) | Gameplay | Full Vision | Not Started | — | 2, 3, 13, 15, 17, 20 |

---

## Categories

| Category | Description | Systems |
|----------|-------------|---------|
| **Core** | Foundation systems everything depends on | 1 a 5 |
| **Gameplay** | The systems that make the game fun | 6 a 15, 40 |
| **Progression** | How the player grows over time | 16 a 23 |
| **Economy** | Resource creation and consumption | 24 a 27, 38 |
| **Persistence** | Save state and continuity | 28, 29, 37 |
| **UI** | Player-facing information displays | 30 (o HUD de combate está em 12) |
| **Audio** | Sound and music systems | 31 |
| **Meta** | Systems outside the core game loop | 32 a 36, 39 |

A categoria Narrative do template foi removida: o conceito mantém a narrativa mínima e ela está dentro de Campanha (#20). Não há sistema de diálogo, quests, cutscenes, inventário com peso, mapa nem mundo aberto (os dois últimos contrariam os anti-pilares).

---

## Priority Tiers

| Tier | Definition | Target Milestone | Design Urgency |
|------|------------|------------------|----------------|
| **MVP** | Required for the core loop to function. Without these, you can't test "is this fun?" | First playable prototype | Design FIRST |
| **Vertical Slice** | Required for one complete, polished area. Demonstrates the full experience. | Vertical slice / demo | Design SECOND |
| **Alpha** | All features present in rough form. Complete mechanical scope, placeholder content OK. | Alpha milestone (lançamento ajustado) | Design THIRD |
| **Full Vision** | Polish, edge cases, nice-to-haves, and content-complete features. | Pós-lançamento | Design as needed |

| Tier | Sistemas | Qtd |
|------|----------|-----|
| MVP | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16, 17, 19, 20, 24, 25, 28, 30 | 19 |
| Vertical Slice | 11, 13, 14, 21, 26, 31, 32 | 7 |
| Alpha | 15, 18, 22, 27, 29, 33, 34, 37, 38, 39 | 10 |
| Full Vision | 23, 35, 36, 40 (e a gravação de replay do #2) | 4 |

> **Creative Director Note** (CD-SYSTEMS: CONCERNS): todos os pilares têm dono e a core fantasy está inteira no MVP (combate, Grimório, Selamento, Forja e Campanha). O único sistema que não serve a nenhum pilar é o #15 Auto-battle, que já está na ordem de corte. Raças no Vertical Slice com o Orc como stub foi aceito (com uma raça só, o Pilar 5 não pode ser testado). Seis ajustes, que os GDDs correspondentes devem cumprir; o conjunto de 36 sistemas da data da revisão e os tiers não mudam (o índice tem 40 depois do modelo de negócio e da divisão do #15, ver a Business Model Note):
> - **(MVP) Fases de função** (escoltar, proteger) passam de #14 (Vertical Slice) para #20 Campanha, com tier explícito, porque são o que torna o Tank forjável sozinho. O GDD do #20 declara se o MVP tem pelo menos uma.
> - **(MVP) A suprema ativa** tem a regra em #6 Combate ou #8 Skills, não em #4 Input (apresentação).
> - **(MVP e Vertical Slice) Skill racial:** o stub do Orc reserva o slot da skill racial em #4, #8, #12 e #17 (como dado). O Vertical Slice ganha um critério de aceite do Pilar 5 que possa reprovar: duas raças distinguíveis sem olhar atributos.
> - **(MVP) SFX placeholder de impacto** é requisito do #12, porque o #31 Áudio só chega no Vertical Slice e o Pilar 4 depende do som de impacto.
> - **(Alpha) Reforja:** o aval ao corte inteiro foi **negado**. O Livro conquistado (1 por herói por período) e a run de reforja ficam no lançamento, porque sem eles o Pilar 2 passa de "pesa" para "pune". Só a **reforja grátis por nerf** pode ir para o pós-lançamento, com compromisso registrado: até ela existir, nenhuma skill selável recebe nerf líquido acima do limiar (política só de buffs).
> - **(Alpha) Analytics (#34):** se for reduzido ao log do #5, mantém um evento agregado "conjunto selado por função", senão o critério mensurável do Pilar 1 (diversidade de selos) fica sem medição.

---

## Dependency Map

Sistemas em ordem de dependência: projete e construa de cima para baixo.

### Foundation Layer (no dependencies)

1. **#1 Dados e balanceamento**: todo valor de gameplay é dado; o remote config é injetado depois pelo #29, sem o #1 depender de rede.
2. **#28 Save local**: só serializa; cada sistema é dono da sua fatia.
3. **#37 Entitlements**: interface de leitura das posses de cosméticos comprados; o #29 a alimenta e o resto do jogo só lê (Alpha).

### Core Layer (depends on foundation)

1. **#2 Simulação determinística** — depends on: 1
2. **#3 Fluxo de fase** — depends on: 2
3. **#5 Log de eventos** — depends on: 2, 28
4. **#6 Combate e dano** — depends on: 1, 2

### Feature Layer (depends on core)

1. **#10 Funções** — depends on: 1, 6
2. **#8 Skills e evoluções** — depends on: 6, 10
3. **#7 Horda, waves e inimigos** — depends on: 1, 2, 6
4. **#19 Herói** — depends on: 10, 11 (stub no MVP), 28
5. **#16 Grimório** — depends on: 3, 5, 8, 10, 19, 28
6. **#17 Selamento da build** — depends on: 8, 16, 19
7. **#9 Oferta de cartas** — depends on: 2, 3, 8, 10, 16 (só leitura)
8. **#20 Campanha e capítulos** — depends on: 3, 7, 11 (stub no MVP)
9. **#24 Inventário** — depends on: 7, 20
10. **#25 Forja e sets** — depends on: 10, 19, 24
11. **#11 Raças** — depends on: 6, 8
12. **#13 IA de herói e companheiro** — depends on: 2, 6, 10, 17
13. **#21 Poder de Combate** — depends on: 19, 25
14. **#14 Dungeons e trindade** — depends on: 6, 7, 13, 17, 19, 21
15. **#26 Economia e tetos** — depends on: 1, 24, 25
16. **#18 Reforja** — depends on: 8, 9, 17, 26
17. **#15 Varredura** — depends on: 17, 20, 24, 26
18. **#27 Monetização e loja** — depends on: 26
19. **#22 Ranking** — depends on: 2, 14, 21, 28
20. **#23 Runas** — depends on: 19, 21, 25
21. **#38 Cosméticos e catálogo** — depends on: 19, 25, 27, 37
22. **#40 Auto-battle com IA** — depends on: 2, 3, 13, 15, 17, 20

### Presentation Layer (depends on features)

1. **#12 Feedback de combate, VFX e HUD** — depends on: 6, 7, 10
2. **#4 Input e câmera de combate** — depends on: 3
3. **#30 UI de meta-jogo** — depends on: 16, 17, 19, 24, 25
4. **#31 Áudio** — depends on: 6, 10, 11, 17

### Polish Layer (depends on everything; inclui o online)

1. **#32 Onboarding** — depends on: 16, 20, 30
2. **#33 Acessibilidade** — depends on: 12, 25, 30
3. **#34 Analytics e live ops** — depends on: 5, 22, 26
4. **#29 Serviços online** — depends on: 2, 22, 27, 28, 37
5. **#35 Coop PvE de 4** — depends on: 2, 13, 14, 22, 29
6. **#36 PvP em tempo real** — depends on: 6, 29, 35
7. **#39 Consentimento e privacidade** — depends on: 29, 34

### Gargalos e folhas

- **Gargalos (muitos dependentes):** #2 Simulação (10 ou mais), #6 Combate, #1 Dados, #8 Skills, #19 Herói e o par #16/#17. Mudanças nesses sistemas propagam para todo o resto.
- **Folhas (menor risco, podem ser desenhadas tarde):** #31 Áudio, #33 Acessibilidade, #34 Analytics, #32 Onboarding, #23 Runas, #36 PvP.

---

## Recommended Design Order

**Pré-requisitos (não são GDDs):**
- **ADR da Simulação** (tipo numérico e interface) antes dos GDDs #6, #7 e #8 [TD].
- **`/art-bible`** antes dos GDDs #12, #25 e #30 [AD]. Até lá, os GDDs citam a VIA por princípio e deixam cor, forma e limite de VFX como `TBD-art-bible`.
- **Decisão F2P ou premium** (etapa de formalização do modelo de negócio) antes do GDD #26.

| Order | System | Priority | Layer | Agent(s) | Est. Effort |
|-------|--------|----------|-------|----------|-------------|
| 1 | #1 Dados e balanceamento | MVP | Foundation | systems-designer | S |
| 2 | #28 Save local | MVP | Foundation | technical-director | S |
| 3 | #2 Simulação determinística | MVP | Core | technical-director, systems-designer | L |
| 4 | #3 Fluxo de fase | MVP | Core | game-designer, systems-designer | M |
| 5 | #5 Log de eventos e instrumentação | MVP | Core | qa-lead, analytics-engineer | M |
| 6 | #6 Combate e dano | MVP | Core | game-designer, systems-designer | L |
| 7 | #10 Funções | MVP | Feature | game-designer | M |
| 8 | #8 Skills e evoluções | MVP | Feature | game-designer, systems-designer | L |
| 9 | #19 Herói | MVP | Feature | game-designer | M |
| 10 | #16 Grimório | MVP | Feature | game-designer, systems-designer | L |
| 11 | #17 Selamento da build | MVP | Feature | game-designer, ux-designer | L |
| 12 | #9 Oferta de cartas | MVP | Feature | game-designer, systems-designer | M |
| 13 | #7 Horda, waves e inimigos | MVP | Feature | game-designer, level-designer, ai-programmer | M |
| 14 | #20 Campanha e capítulos | MVP | Feature | game-designer, level-designer | M |
| 15 | #24 Inventário | MVP | Feature | economy-designer | S |
| 16 | #25 Forja e sets | MVP | Feature | economy-designer, art-director | M |
| 17 | #12 Feedback de combate, VFX e HUD | MVP | Presentation | technical-artist, ux-designer | L |
| 18 | #4 Input e câmera de combate | MVP | Presentation | gameplay-programmer, ux-designer | S |
| 19 | #30 UI de meta-jogo | MVP | Presentation | ux-designer | M |
| 20 | #11 Raças | Vertical Slice | Feature | game-designer | S |
| 21 | #13 IA de herói e companheiro | Vertical Slice | Feature | ai-programmer | L |
| 22 | #21 Poder de Combate | Vertical Slice | Feature | systems-designer | M |
| 23 | #14 Dungeons e trindade | Vertical Slice | Feature | game-designer, level-designer | L |
| 24 | #26 Economia e tetos | Vertical Slice | Feature | economy-designer | L |
| 25 | #31 Áudio | Vertical Slice | Presentation | audio-director | M |
| 26 | #32 Onboarding | Vertical Slice | Polish | ux-designer | M |
| 27 | #18 Reforja | Alpha | Feature | game-designer, economy-designer | M |
| 28 | #15 Varredura | Alpha | Feature | game-designer | S |
| 29 | #27 Monetização e loja | Alpha | Feature | economy-designer | M |
| 30 | #22 Ranking | Alpha | Feature | systems-designer | M |
| 31 | #29 Serviços online | Alpha | Polish | technical-director, security-engineer | L |
| 32 | #33 Acessibilidade | Alpha | Polish | accessibility-specialist | S |
| 33 | #34 Analytics e live ops | Alpha | Polish | analytics-engineer, live-ops-designer | M |
| 34 | #37 Entitlements | Alpha | Foundation | technical-director | S |
| 35 | #38 Cosméticos e catálogo | Alpha | Feature | art-director, economy-designer | M |
| 36 | #39 Consentimento e privacidade | Alpha | Polish | technical-director, security-engineer | M |
| 37 | #23 Runas | Full Vision | Feature | systems-designer | L |
| 38 | #35 Coop PvE de 4 | Full Vision | Polish | network-programmer | L |
| 39 | #36 PvP em tempo real | Full Vision | Polish | network-programmer, security-engineer | L |
| 40 | #40 Auto-battle com IA | Full Vision | Feature | ai-programmer | L |

Esforço: S = 1 sessão, M = 2 a 3 sessões, L = 4 ou mais. O Grimório e o Selamento (ordem 10 e 11) são os sistemas de maior risco de design e entram assim que Funções, Skills e Herói existem. Os dois são revisados juntos.

---

## Circular Dependencies

Quatro ciclos de design, todos com resolução de interface (sem ciclo no código):

1. **Grimório (#16) ↔ Selamento (#17).** O predicado de "selável" (4 slots, 2 de função, pelo menos 4 skills) e o K_min amarram os dois. *Resolução:* o GDD do Selamento é dono do predicado, do K_min e do teto de nível antes do selo; o Grimório o implementa como **função pura** dentro do próprio módulo (ele a avalia em tempo de execução para armar a garantia). O contador de vitórias de chefe de fase por herói é do Grimório, alimentado por um evento do Fluxo de fase que informa o modo da run (manual, auto, varredura). Os dois GDDs são revisados juntos. O GDD do Grimório entra primeiro e declara o predicado como contrato.
2. **Dungeons (#14) ↔ Poder de Combate e Ranking.** A dungeon usa o PC como porta de entrada, e o ranking usa o tempo de clear da dungeon. *Resolução:* dividido em Poder de Combate (#21, antes das dungeons) e Ranking (#22, depois).
3. **Economia (#26) ↔ Inventário, Forja, Reforja e Monetização.** O teto limita as fontes, e as fontes e sumidouros alimentam a Economia. *Resolução:* o valor do teto é dado em #1 e nenhuma API de tempo de execução é chamada por #24, #25 ou #18; a Economia é projetada depois de #24 e #25 e é auditoria de design mais simulação. Quando Reforja (#18) e Monetização (#27) forem projetadas, o GDD da Economia é revisado.
4. **Oferta de cartas (#9) ↔ Grimório (#16).** O "favorecer" lê o registro, e a garantia concede uma skill no início da fase. *Resolução:* o Grimório expõe só leitura; a concessão no início da fase é um gancho do Fluxo de fase (#3) definido pelo Grimório, e o Fluxo de fase o expõe como evento ou interface sem conhecer o Grimório.

Dois acoplamentos de dependência que **não** são ciclos e devem ficar assim: o Herói (#19) não depende do Grimório nem do Selamento (o Grimório cria o registro sob demanda pela chave do herói; o estado "selado" é um campo do Herói que o Selamento grava); e o Ranking (#22) não depende dos Serviços online (#29), porque o #29 depende do #22 para validar.

---

## High-Risk Systems

| System | Risk Type | Risk Description | Mitigation |
|--------|-----------|-----------------|------------|
| #2 Simulação determinística | Technical | O determinismo entre Mono, IL2CPP e servidor e entre Burst e Jobs está NOT SOURCEABLE em `docs/engine-reference/unity/`; a escolha numérica muda as fórmulas de #6, #7 e #8. | ADR fixa tipo numérico e interface antes dos GDDs; protótipo cedo (não no ritmo dos GDDs); o MVP exige só reprodutibilidade no mesmo build. |
| #7 e #12 Horda e Feedback | Technical | 300 inimigos, 4 heróis e VFX no máximo, em Android intermediário, no minuto 20 (térmico). | Spike com proxies; contagens e densidades como Tuning Knobs; resultado FAIL vira ajuste de knob, não reescrita de regra. |
| #16 e #17 Grimório e Selamento | Design | Cerca de 15 pontos em aberto; invariantes de selabilidade; o selo pode virar só confirmação (descartar 1 de 5); seis revisões do conceito giraram em torno disso. | GDDs revisados juntos; métrica "selo = confirmação" no doc de aceite; enumeração exaustiva da grade (g, f) em vez de seeds. |
| #8 Skills e evoluções | Scope | Árvore de modificadores pós-selo: ~4 por skill, uns 60 cards no lançamento. | Escolher entre modificadores e re-leveling no GDD; começar com o pool de ~15 skills ativas do MVP. |
| #10 Funções (Tank solo) | Design | O Tank pode não ser divertido sozinho; o Pilar 3 só valida a partir do Vertical Slice. | Critério de aceite do MVP: Tank com no máximo [2] mortes até abrir o selo; uso solo em toda skill de função. |
| #25 Forja e sets | Scope | Cerca de 400 encaixes de peça sem a regra de raridade por material; critério de pipeline de arte do MVP. | Raridade como variante de material ou shader; horas reais por peça medidas no MVP. |
| #13 e #14 Healer + IA de companheiro | Scope / Design | O Producer aponta como o trecho mais arriscado do Vertical Slice. | IA como sistema próprio; companheiro NPC com poder limitado (knob). |
| #26 e #27 Economia e Monetização | Design / Scope | O F2P devolve ao Alpha o escopo de #27, #29 e #34 e exige receita sem vender poder; custo de aquisição pago inviabiliza a meta. | Modelo decidido em `design/business-model.md` (só cosméticos, sem conteúdo de gameplay pago, vídeo recompensado só da moeda sem poder); catálogo filtrado pelo teste "este item muda o resultado de alguma run ou a recompensa esperada por dia ou por temporada?"; critério de saída escrito antes do soft launch. |
| #29, #35 e #36 Serviços online, Coop e PvP | Technical | Rede móvel, servidor autoritativo e anti-cheat; nenhum backend está coberto pela referência do engine. | Pós-lançamento; ADR de backend no fim do Vertical Slice. |

---

## Notas dos diretores

> **Technical Director Note** (TD-SYSTEM-BOUNDARY: CONCERNS): o grafo é sólido e não há dependência contra a ordem das camadas. Quatro mudanças de fronteira foram **aplicadas** neste índice (dividir o save local dos serviços online e o fluxo de fase do input e câmera, criar a IA de herói e companheiro, mover a carteira de moedas para o Inventário e o XP de fase para o Fluxo de fase). Cuidados que ficam para os GDDs: a gravação de replay é do #2 e não do #5; o predicado de selabilidade é função pura dentro do Grimório; o valor dos tetos é dado em #1, sem API de tempo de execução; os ganchos de fase são eventos, e o Fluxo de fase não conhece o Grimório. O **#2 deve ser prototipado cedo**: a simulação headless do MVP deve rodar #3, #9, #16 e #17 sem nenhuma referência a #4, #30 ou #29.

> **Producer Note** (PR-SCOPE: OPTIMISTIC): os 20 sistemas de MVP em 3 meses esperados dão cerca de 3 dias de implementação por sistema, e os GDDs não cabem em 6 a 8 semanas com 2,5 por semana. Estimativa honesta do Producer: MVP em 4 a 5 meses, Vertical Slice entre os meses 13 e 15 pela regra de 1,5× do conceito, e **mês 20 como lançamento esperado**.
> - **Aplicado:** Raças (#11) e Economia (#26) passam ao Vertical Slice; a gravação de replay sai do MVP (Full Vision).
> - **Não aplicado:** fundir Campanha (#20) em Fluxo de fase (#3) e Inventário (#24) em Forja (#25) (mistura conteúdo com a lógica pura do TD e põe a carteira na Forja). O Producer sugeriu; o usuário não marcou.
> - **Plano pré-D0 (recomendação, não está em `project.yaml`):** GDD completo só para #2, #6, #7, #8, #9, #16 e #17; spec leve para #19, #28 e #30; o resto é escrito na hora em que for necessário; timebox de 8 semanas para o Systems Design. Para valer, usa `workflow_overrides.system_overrides` via `/settings`.
> - **Ordem de corte se o orçamento apertar** (revista para o F2P, ver `design/business-model.md`): (1) o vídeo recompensado e o SDK de anúncios; (2) o passe de temporada (já adiado); (3) #22 Ranking; (4) reduzir a cadência de sets cosméticos por temporada; (5) só a reforja grátis por nerf do #18 (o Livro e a run de reforja ficam; o creative-director negou o corte inteiro). O auto-battle (#40) já está no Full Vision. **Nunca cortar:** o baseline de #33, o #28, o núcleo do #29 e o consentimento (#39). As antigas opções "decidir premium" e "capítulo 2 como DLC" deixaram de existir: todo o conteúdo de gameplay é grátis.
> - **Também registrado:** o baseline de acessibilidade é requisito do GDD do #12 já no Vertical Slice; o ADR de backend e de compras (#29) vem antes do GDD #26.

> **Business Model Note** (2026-11-03, modelo F2P validado; detalhes em `design/business-model.md`): F2P **sem conteúdo de gameplay pago** (todos os capítulos, dungeons e PvP são grátis). Receita: cosméticos de loja (skins, transmogs temáticos e pets só de animação) e um vídeo recompensado ao fim da partida (PVE) que dobra só a moeda de jogo sem poder, nunca material, XP, skill nem reroll. Passe de temporada só de cosméticos na 1ª temporada depois do lançamento; soft launch só no Android. Revisão dos 4 diretores (feita sobre uma versão com capítulos como DLC e sem vídeo): economy-designer e TD viáveis com condições, CD CONCERNS (regras R1 a R7), Producer otimista. Três sistemas novos: #37 Entitlements (Alpha), #38 Cosméticos e catálogo (Alpha) e #39 Consentimento e privacidade (Alpha, bloqueia o soft launch); o #15 foi dividido em Varredura (Alpha) e #40 Auto-battle com IA (Full Vision). O #29 perde o corte do núcleo e o #34 deixa de poder ser reduzido ao log. **Cronograma aprovado pelo usuário:** soft launch no mês 19 a 20 e lançamento global no mês 23 a 24 (o conceito congelado diz 16), com 80 h por semana; o Producer ainda não o reavaliou com o SDK de vídeo. Em aberto: preço por SKU, orçamento de aquisição e gatilho de saída; taxas da moeda de jogo (GDD #26); distinção visual entre cosméticos de conquista, de loja e de moeda (CD).

---

## Progress Tracker

| Metric | Count |
|--------|-------|
| Total systems identified | 40 |
| Design docs started | 2 |
| Design docs reviewed | 0 |
| Design docs approved | 0 |
| MVP systems designed | 2/19 |
| Vertical Slice systems designed | 0/7 |

---

## Next Steps

- [x] Gate de direção criativa do índice (CD-SYSTEMS): CONCERNS, registrado na `Creative Director Note` abaixo da tabela de Priority Tiers
- [x] Etapa de formalização do modelo de negócio: decisões validadas em `design/business-model.md` (F2P, só cosméticos); **faltam preço por SKU, orçamento de aquisição e gatilho de saída (seção 12)** e a reavaliação do Producer com o SDK de vídeo, antes do GDD #26 e do #27
- [ ] Escrever o doc de aceite do MVP (`docs/acceptance/mvp.md`) com commit e revisão do qa-lead antes de D0
- [ ] Decidir a ordem do spike de performance e da semana 0 (o Producer quer em paralelo ao Systems Design; o conceito os põe depois de D0)
- [ ] Rodar `/art-bible` antes dos GDDs #12, #25 e #30
- [x] ADR da Simulação (tipo numérico e interface) antes dos GDDs #6, #7 e #8: `docs/architecture/adr-0001-simulacao-deterministica-float32-tick-30hz.md` (Proposed, 2026-11-03)
- [ ] Projetar os sistemas do MVP na ordem acima (`/design-system [system-name]`), começando por #1; o Grimório (#16) e o Selamento (#17) são revisados juntos
- [ ] Rodar `/design-review` em cada GDD concluído (máximo de 2 passadas por GDD, como regra de saída)
- [ ] Rodar `/gate-check technical-setup` quando os GDDs do MVP estiverem concluídos
- [ ] Validar os sistemas de maior risco com protótipo antes de Production (`/vertical-slice`)
