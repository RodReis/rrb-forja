# Art Bible: Forja das Hordas

> **Status**: Draft
> **Owned By**: art-director
> **Last Updated**: 2026-11-03
> **Art Director Sign-Off (AD-ART-BIBLE)**: [Not yet reviewed]

`/art-bible` writes these nine sections in this order and replaces each
section's `[To be designed]` line as that section is approved. A section still
holding its placeholder is incomplete; a later run fills only those.

## 1. Visual Identity Statement

**Base:** a âncora "Hierarquia do Detalhe, com o Ritual da Forja" de `design/gdd/game-concept.md` (L251-279), escolhida pelo usuário entre as três direções do AD-CONCEPT-VISUAL e refinada nesta seção. O conceito está congelado; a bible é quem refina a âncora.

**Regra visual em uma linha:**

> *O detalhe é privilégio da ameaça, do herói e do que ele conquistou; todo o resto é silhueta.*

O acréscimo "e do que ele conquistou" dá dono visual à conquista. A regra anterior não o tinha, e a regra R2 do modelo de negócio (`design/business-model.md`) e o Princípio de Negócio exigem que a conquista seja legível só de olhar.

### Princípios de apoio

**A. Perigo pela cor, função pela forma** (serve P4, *Massacre com peso*)
O orçamento de detalhe segue ameaça > herói > horda. A horda fica em bloco, sem acessório solto. O vermelho-alaranjado quente é só do telegraph. Função e raridade nunca dependem só de cor.
- *Design test:* quando for ambíguo se um efeito, detalhe ou cor quente entra, escolha o que deixa o golpe inimigo legível. Se duas coisas se confundem, mude a forma, nunca a cor.

**B. Função é massa; raça é detalhe e movimento** (serve P5, *Ser a raça, não vestir a raça*, restringido por P3, *Cada função é indispensável*)
A silhueta em escala de cinza (Tank, DPS, Mago, Healer) pertence à função. A raça vive na camada de baixo: proporção de cabeça e ombro dentro do bloco, postura, idle, locomoção e voz. A raça nunca altera a massa da função.
- *Design test:* quando for ambíguo se uma marca racial vai na forma ou na animação, escolha a animação e a postura, e preserve a silhueta da função.

**C. Só a conquista é forjada** (serve P2, *Toda escolha pesa*, com o Princípio de Negócio *Poder conquistado, não comprado*)
O selo é encenado em três tempos, **fora de combate**: metal branco-incandescente, runa gravada, resfriamento em aço azulado. A marca gravada do selo é a assinatura visual de conquista, visível no herói e em outros jogadores. Assim, dois heróis de nível máximo diferem pelo selo (P1, *Sua build, sua assinatura*).
- **R1:** cosmético de loja muda material e cor dentro da silhueta da função. Nunca usa moldura, emissivo, tom de raridade ou de runa, nem a marca do selo.
- **R2:** a marca do selo e as insígnias de clear e ranking são exclusivas de conquista. Cosmético comprado com moeda de jogo conta como de loja.
- **R7:** pet e cosmético "de skill" são só animação.
- *Design test:* quando for ambíguo se um item parece conquistado ou comprado, escolha a distinção. Se um item de loja pode ser confundido com a marca do selo, ele muda ou sai.

### Cobertura dos pilares

P4 é servido por A. P5 é servido por B (era o pilar sem dono visual: com a silhueta pertencendo à função, a raça seria só troca de textura). P3 restringe B. P1 e P2 são servidos por C (o selo gravado visível). O Princípio de Negócio é servido por C (R1, R2 e R7).

### Mudança em relação à âncora do conceito

O ritual de selamento era "metal incandescente", que cai na faixa vermelho-alaranjada exclusiva dos telegraphs e furaria a regra de exclusividade. Passa a ser **branco-quente e aço azulado, só fora de combate**.

## 2. Mood & Atmosphere

Cada estado tem uma **luz própria** (hora, temperatura, contraste) e uma **energia própria**. Em escala de cinza e em miniatura, os oito ainda se distinguem. O custo mobile entra em cada estado: uma luz direcional, ambiente baked, sombras blob, troca de LUT e poucos cartões de partícula. Não há volumétrico real nem bloom em tela cheia.

### 2.1 Combate de fase
- **Emoção:** euforia pesada e controlada, a de quem ceifa.
- **Luz:** fim de tarde, cerca de 4500 K, direção 3/4 por cima, contraste médio. O chão é quente e a horda fica na sombra fria (contraste de valor, não de cor).
- **Adjetivos:** denso, ágil, poeirento, pesado. **Energia:** alta.
- **O que carrega o clima:** hit-stop, queda em massa e a faixa chão-quente/horda-fria.
- **Entrega mobile:** 1 luz direcional, 1 camada de poeira (um quad com scroll) e limite de partículas aliadas (P4).

### 2.2 Elite e chefe com telegraph
- **Emoção:** pavor lúcido, um erro custa caro.
- **Luz:** o ambiente cai cerca de 1 stop e esfria (LUT, ~7500 K). O telegraph quente é o único ponto saturado da tela.
- **Adjetivos:** contido, ameaçador, nítido, ritmado. **Energia:** tensão alta e movimento curto.
- **O que carrega o clima:** um telegraph isolado num ambiente frio.
- **Entrega mobile:** troca de LUT mais um decal de chão, sem partículas novas.

### 2.3 Registro no Grimório
- **Emoção:** reverência curiosa, pequena decisão de identidade.
- **Luz:** a cena congela e abre-se a luz de lamparina, ~3500 K, suave, com vinheta.
- **Adjetivos:** íntimo, tátil, solene, quieto. **Energia:** baixa.
- **O que carrega o clima:** um único glifo da skill sendo entintado na página.
- **Entrega mobile:** UI 2D sobre o frame congelado, com blur barato de 1 passe.

### 2.4 Ritual de selamento (fora de combate)
- **Emoção:** gravidade cerimonial, o ponto sem volta.
- **Luz:** interior da Forja quase escuro (valor ≤ 15%) e um ponto único. O metal passa de branco-quente a runa a aço azulado.
- **Adjetivos:** ritual, irreversível, incandescente, silencioso. **Energia:** lenta e crescente.
- **O que carrega o clima:** as três etapas de cor do metal.
- **Entrega mobile:** material emissivo local, um **cartão de halo aditivo** na bigorna (zero pós-processamento; o bloom real só entra se o spike mostrar folga, Seção 8.7), shimmer em 1 quad pequeno e até 8 cartões de vapor.

### 2.5 Forja e meta-jogo
- **Emoção:** orgulho de ofício, calma de quem otimiza.
- **Luz:** lâmpada de forja de ~3200 K na chave, preenchimento azul-aço, contraste médio. A brasa é **branco-âmbar** (matiz 38–45°, saturação ≤ 50%), **nunca vermelho-alaranjado**.
- **Adjetivos:** artesanal, denso, metálico, caloroso. **Energia:** baixa a média.
- **O que carrega o clima:** metal com reflexo (cubemap baked) e rebites.
- **Entrega mobile:** cena estática, sem partículas além de faíscas pontuais.

### 2.6 Dungeon da trindade
- **Emoção:** assombro e tensão compartilhada de quatro funções.
- **Luz:** meio-dia do deserto em ruínas, 6500 K, sol duro, sombras curtas e nítidas, contraste alto, pedra branqueada.
- **Adjetivos:** árido, grandioso, ofuscante, antigo. **Energia:** média a alta.
- **O que carrega o clima:** heat-haze no horizonte e sombras duras.
- **Entrega mobile:** haze como **distorção de vértice num cartão de horizonte**, sem cópia de tela (a distorção real em meia resolução só entra se o spike mostrar folga, Seção 8.7), e uma cascata de sombra só para os heróis e o chefe (1 cascata, mapa ≤ 1024, distância curta). A sombra é o primeiro corte no piso de 30 fps: vira blob.
- **Sombra na área jogável:** a sombra dura e densa fica nas paredes e no fundo; na área de combate, um fill levanta o chão sombreado para a horda continuar legível (regra 6.5).

### 2.7 Vitória
- **Emoção:** alívio e triunfo contido.
- **Luz:** sol baixo de ~3500 K, sombras longas, contraste suavizado, céu aberto.
- **Adjetivos:** aberto, quente, estável, ganho. **Energia:** média, em queda.
- **O que carrega o clima:** a horda se dissolvendo em poeira clara e o carimbo de clear, um escudo de aço punçado com o glifo de conquista, que esfria de branco-quente para aço azulado (ver a Seção 4, bloco (d)).
- **Entrega mobile:** lerp de LUT em 1,2 s, 1 sprite de feixe de sol e no máximo 30 partículas.

### 2.8 Derrota
- **Emoção:** pesar de "quase", sem humilhação.
- **Luz:** dessaturação de cerca de 60%, ~8000 K, topo plano, contraste baixo. O herói perde a cor por último.
- **Adjetivos:** apagado, pesado, silencioso, frio. **Energia:** muito baixa.
- **O que carrega o clima:** drenar a cor em câmera lenta.
- **Entrega mobile:** só LUT e vinheta, sem partículas. É o estado mais barato e libera a retentativa rápida.

### Regra global de fogo
Fogo vermelho-alaranjado vivo é proibido em todo o jogo, mesmo fora de combate, porque essa faixa é exclusiva do telegraph (ver a Seção 4). A brasa da Forja é branco-âmbar, coerente com o selo branco-quente da Seção 1.

## 3. Shape Language

### 3.1 Silhueta do personagem
A silhueta pertence à função e é lida em escala de cinza em miniatura (cerca de 48 px de altura).
- **Tank:** bloco largo e quadrado.
- **DPS:** fino e angular.
- **Mago:** vertical, com tecido em movimento.
- **Healer:** arredondado, com halo ou forma circular.

A raça só altera proporção de cabeça e ombro, postura e animação (Seção 1, princípio B). Heróis têm ombros e arma de 10 a 15% maiores que o natural, para continuar legíveis na câmera alta. Cada função tem **um** traço distintivo, e nenhum cosmético o apaga (R1).

### 3.2 Geometria do ambiente
Planos grandes e horizontais com pouca textura, ruínas de blocos retos e verticais quebrados por diagonais de desabamento. O chão é plano e legível, e o detalhe fica nos heróis e nas ameaças. Elites e chefes são grandes e assimétricos, com uma "parte que ataca" identificável. A horda é bloco simples, sem acessório solto. A **parte que ataca** de elites e chefes é o **"osso frio"**: H 200° a 230°, S 8 a 15%, V 80 a 92%. Fica fora da faixa do telegraph por construção, tem mais de 50 pontos de V acima da horda e ≥ 3:1 de luminância contra o corpo, ocupa ≤ 15% da silhueta e só a parte que ataca. Distingue-se da runa (S 30%) e do aço do selo (S 43%) pela saturação.

### 3.3 Gramática da UI
A UI é uma **linguagem própria que ecoa a forja**: placas de metal com cantos chanfrados e rebites. No HUD de combate é geometria mínima e plana. Três vocabulários de forma são **reservados**:
- **Serrilha e hachura:** só do telegraph.
- **Círculo liso e curvas:** só de cura e do Healer, no mundo (chão e VFX) e na UI de cura. Exceção: os controles em tela (joystick, esquiva, suprema) podem ser redondos (Seção 7.5). O efeito aliado em anel segue a regra da 3.6 (arco aberto ou disco difuso).
- **Glifo angular gravado:** só da assinatura de conquista (marca do selo e insígnias de clear e de ranking).

### 3.4 Herói versus apoio
O herói ocupa a camada alta, com a maior saturação do corpo e contorno leve. Aliados e companheiros usam formas menores e efeitos atenuados. A hierarquia de leitura é **telegraph > herói > aliados > horda > cenário**.

### 3.5 Cinco molduras de raridade
Cada moldura vale para o ícone, a placa do inventário e o decal de chão do drop. A forma não vive na malha do equipamento, porque a raridade é variante de material ou shader (conceito L278). A leitura é pela contagem de chanfros e pontas, nunca só pela cor:

| Raridade | Forma |
|---|---|
| Branco | placa retangular lisa, cantos retos, sem rebite |
| Verde | 2 cantos diagonais chanfrados |
| Azul | 4 cantos chanfrados (octógono) e 1 rebite |
| Roxo | 4 chanfros e 2 pontas (superior e inferior), hexágono apontado |
| Dourado | contorno duplo (moldura dentro de moldura), coroa de 3 pontas e rebites nos cantos |

### 3.6 Forma do telegraph
É um decal de chão com borda externa **serrilhada** (dentes triangulares para dentro) e **hachura diagonal** no preenchimento. Uma frente de preenchimento cresce da origem até a borda para marcar o tempo. Nenhuma skill aliada, VFX, cosmético ou elemento de UI pode ter serrilha ou hachura. Efeitos aliados são curvas lisas e translúcidas. **Anel (decisão do usuário em 2026-11-03):** o único anel **fechado** (360°, traço ≤ 4% do diâmetro, sempre menta) é o da cura. O efeito aliado em anel é um **arco aberto** (≤ 270°, abertura ≥ 90°) ou um **disco difuso sem contorno** (feather ≥ 40% do raio); isso se mede por contorno fechado e perfil radial. O Mago perde o anel de nova completo. O círculo de cura do Healer é liso e fino, então se distingue do telegraph circular pela forma, não pela cor.

**Gramática de forma do VFX aliado (medível):** (1) razão perímetro/envoltória convexa do contorno do sprite ≤ 1,15 (sem dentes); (2) nenhum atlas com listras paralelas periódicas (auditoria por nome de arquivo); (3) alfa máxima ≤ 0,85, e ≥ 40% da área do cartão com alfa ≤ 0,6.

## 4. Color System

### 4.1 Paleta primária

| Papel | Hex | Significado |
|---|---|---|
| Areia e pedra de ruína | `#8A7B66` | chão e cenário (H 35°, S 26%, V 54%) |
| Pedra-sombra | `#2B3340` | horda (H 215°, S 33%, V 25%) |
| Poeira de luz | `#F2DDB0` | luz dura do deserto |
| **Perigo** | `#FF4A1C` | exclusivo do telegraph (H 12°, S 89%, V 100%) |
| Cura | `#5ED8A0` | menta (H 152°); sempre acompanhada de forma circular |
| Selo | `#FFF1D6` (branco-quente), `#5E7FA6` (aço), `#A9CFF2` (runa) | só conquista: marca do selo, insígnias de clear e de ranking |
| Dourado | `#D8C54A` | raridade máxima (H 52°, S 66%, V 85%) |

Raridades secundárias: Branco `#E8E6E0`, Verde `#7FB347` (H 89°), Azul `#3F6FE0` (H 223°), Roxo `#8E4FD0` (H 269°).

O herói não tem swatch fixo. A regra é a do bloco (e): a saturação vem da armadura e do tecido, e os materiais quentes têm teto de S ≤ 45%.

### 4.2 Uso semântico

**(a) Faixa proibida do telegraph (testável).**
- **Condição:** matiz **350° a 38°** (HSV, com wrap), saturação **≥ 55%** e valor **≥ 55%**.
- **Medição:** HSV padrão (V = max, S = (max−min)/max) sobre o RGB sRGB de 8 bits do PNG capturado, pós-tonemap, no buffer de render, sem UI (px de render, ver a Seção 8). A UI é medida à parte, no canvas de 1080. Falha: bloco 4×4 com mediana na faixa. **Máscaras:** o telegraph fica em camada própria e sai da varredura; ele é medido à parte e tem de estar **dentro** da faixa em L1 a L3. **Conjunto mínimo de capturas:** L1 a L6 (tabela de 4.2e) × a grade de raridades r1 a r5 (item, decal de drop, UI), mais 1 frame de pico de cada skill aliada em L1 a L3, mais a matriz do herói, mais cada cosmético novo.
- **Escopo:** nenhuma skill de jogador, raridade, cosmético, VFX aliado ou marca do selo entra nessa faixa (R1).
- **Exceção medida:** só o telegraph. O dano sofrido **não** usa a faixa: é uma placa de ferro com número claro (7.2 e 7.7; decisão do usuário em 2026-11-03). Não há vinheta vermelha de vida baixa (decisão do usuário em 2026-11-03).
- **Fogo do jogador:** decisão do usuário em 2026-11-03, a exclusividade se mantém. O fogo das skills do Mago (e de qualquer skill aliada) é **amarelo-branco pálido**: núcleo H 60° a 72°, S 20 a 40%, V ≥ 92% (decisão do usuário em 2026-11-03). O roxo-azulado foi reprovado: H 245° a 255° fica a 22 a 32° do Azul e a 14 a 24° do Roxo de raridade, e o decal de drop é no chão. **Regra de teste:** nenhum pixel de VFX aliado em H 44° a 58° com S ≥ 50%. O núcleo fica a ≥ 19° do crítico (H 41°), a ≥ 15° da brasa (H 45°) e a ≥ 15 pontos de S do Dourado no pior caso (26 no nominal); em 3500 K (L4) o matiz desce, e isso se mede. O jogo abre mão da "bola de fogo" laranja clássica para proteger o Pilar 4: qualquer pixel na faixa é perigo.

**(b) Dourado de raridade.** Fica em H **48° a 58°**, nominal `#D8C54A`, a 10° da faixa proibida no ponto mais próximo (14° no nominal), a mesma folga que o herói ganhou: a luz quente puxa o matiz para baixo. É metálico, nunca pulsa e nunca é emissivo saturado. Se L6 ou L4 medirem o Dourado abaixo de H 44°, o nominal sobe para H 55°.

**(c) Daltonismo.** Verde, Azul e Roxo se distinguem pelas molduras da Seção 3.5, por chanfros e pontas, e não só pela cor. O Verde de raridade fica a 63° do matiz da cura, e a cura tem forma circular. O Dourado se separa do perigo pela moldura dupla e pela ausência de pulso e de hachura. **Teste e critério de aprovação:** protanopia, deuteranopia e **tritanopia** (matrizes de Machado, Oliveira e Fernandes 2009, severidade 1,0, em RGB linear; o filtro é do technical-artist, 8.1 nota 4), sobre L1 a L3 e a grade de raridades. Aprova se, nas três: (1) as 5 molduras embaralhadas são identificadas 5 em 5, em cinza a 48 px; (2) **telegraph sobre o chão:** a serrilha e a hachura têm razão de luminância ≥ 3:1 contra o chão (o mesmo 3:1 de 7.7); (3) o Dourado e o preenchimento do telegraph têm ΔE2000 ≥ 15 (a medir).

**Risco já visível (conferido):** pelo hex nominal, `#FF4A1C` tem luminância relativa ≈ 0,26 e a areia `#8A7B66` ≈ 0,21, uma razão de ≈ 1,2:1. A cor sozinha reprova, e sob protanopia a leitura do telegraph depende da forma. Caminho se a medição reprovar: hachura em tinta escura (V ≤ 20%) sobre o preenchimento, razão ≈ 4:1 contra o chão. Isso muda o desenho do telegraph, então o usuário aprova se a medição reprovar.

**(d) Selo versus loja (R2).**
- A assinatura de conquista é branco-quente → runa `#A9CFF2` → aço `#5E7FA6`, com **saturação ≤ 45%**, em glifo angular gravado.
- As insígnias de clear e de ranking usam a mesma família de cor e o mesmo glifo, sempre dentro do **escudo pentagonal** de aço. A marca do selo é o glifo solto, gravado no herói.
- Cosmético de loja muda material e cor dentro da silhueta, e nunca usa o glifo, a moldura nem o dourado de raridade.
- O Azul de raridade tem saturação ≥ 65% e é moldura, então não se confunde com o aço do selo (os matizes ficam a 12° um do outro: 211° e 223°). Como o risco é real, vale um teste de miniatura cedo.

**(e) Contraste de valor e regra do herói.**
- **Cenário (chão da área jogável, inclusive sombreado, com o fill de 6.5):** V de 50 a 75%, S ≤ 35%. A dungeon de meio-dia (2.6) fica em V 65 a 75. Paredes e fundo fora da área jogável podem passar de 75.
- **Horda:** V ≤ 30% (nominal 25), matiz de 200° a 230°, S ≤ 35%. A diferença de V entre o chão e a horda é de pelo menos 20 pontos, o que fecha por construção (50 − 30).
- **Herói, teto de calor:** todo material do herói com matiz entre 350° e 38° tem **S ≤ 45%** no framebuffer final. Isso vale para a pele de qualquer raça e gênero e também para cabelo ruivo, couro, bronze e cobre. Na textura de origem (albedo), o teto é S ≤ 40%. Os 5 pontos de folga absorvem as luzes quentes (3500 K na vitória, 3200 K na Forja), que puxam a saturação para cima. Consequência de criação: armadura de bronze, couro ou cobre saturados fica proibida.
- **Herói, saturação:** a saturação do herói fica na armadura e no tecido, não na pele. A mediana de S desses pixels fica entre 55 e 80%, só em matizes fora da faixa proibida, e é no mínimo 25 pontos acima da S média do chão. Fora o telegraph, o pico de S da tela pertence ao herói.

**Como o QA testa o herói** (captura no buffer de render, sem UI, com a máscara do herói por camada):
1. **Matriz:** 4 raças × 2 gêneros × 6 luzes (tabela abaixo) × 2 enquadramentos (câmera de jogo e close de equipamento).
2. **Faixa (4.2a):** zero blocos 4×4 com H 350° a 38° (com wrap), S ≥ 55%, V ≥ 55%.
3. **Teto de calor:** zero blocos 4×4 cuja **mediana** tenha H em [350°, 38°], **S > 45%** e V ≥ 15%. Abaixo de V 15% o matiz é instável.
4. **Saturação:** mediana de S em armadura e tecido entre 55 e 80% e ≥ S média do chão + 25.

| ID | Luz | Área | Testes |
|---|---|---|---|
| L1 | 4500 K | fase de horda | herói, 6.5, telegraph |
| L2 | 7500 K (LUT do chefe) | arena de chefe | herói, 6.5, telegraph |
| L3 | 6500 K | dungeon | herói, 6.5, telegraph |
| L4 | 3500 K | vitória | herói |
| L5 | 8000 K, −60% de S | derrota | herói |
| L6 | 3200 K | Forja e ritual | herói em close, skins |

O Grimório (3500 K sobre o frame congelado) usa L1 mais UI e não é caso próprio.

### 4.3 Temperatura por área
O combate fica no quente do chão com sombra fria. O chefe esfria (LUT). A Forja é ~3200 K com brasa branco-âmbar (Seção 2.5). A dungeon é 6500 K, branqueada.

### 4.4 Paleta de UI
Fundo de ferro frio `#1E242C`, texto `#E6EAF0` e acento em aço neutro `#8C96A3` (H 214°, S 14%), distinto do aço do selo `#5E7FA6` (S 43%), que é exclusivo da conquista. A loja usa fundo de couro escuro `#3A2F28` (H 22°, S 31%, V 23%, fora da faixa proibida). Diverge do mundo ao evitar a faixa do telegraph e o dourado fora da raridade. O branco-quente e o aço do selo só aparecem nas insígnias de conquista.

## 5. Character Design Direction

### 5.1 Arquétipo do herói
O herói é um **corpo-base neutro**, e quem o veste é o jogador. A identidade vem do set de função, da raça e da marca do selo, nunca de um rosto ou de uma roupa de autor. Realismo estilo Lineage 2: proporções adultas, armadura com peso e tom sério. Ombros e arma ficam de 10 a 15% maiores que o natural (Seção 3.1). Tecnicamente, é um esqueleto compartilhado por raça e gênero, peças modulares e raridade por material (conceito L319).

*Por quê:* a fantasia é "eu forjei este herói". Um protagonista pré-definido competiria com a assinatura do jogador.

### 5.2 Leitura de relance

| Quem | Como se distingue |
|---|---|
| **O próprio herói** | Maior saturação do corpo, contorno leve e centro da câmera. Altura de **150 a 200 px de render** (Humano 175 px ±12%, regra de 5.3). **Sem anel no chão**, porque o círculo liso é da cura (3.3) |
| **Seus outros heróis selados** | Mesma silhueta de função, saturação de material −15 pontos, sem contorno. Levam a **própria marca do selo** |
| **NPC genérico** | Silhueta da função com set de raridade Branco, **sem marca do selo e sem insígnia**. A ausência é verdadeira: ele não conquistou nada |
| **Horda** | Bloco com V ≤ 30%, matiz de 200 a 230°, de 40 a 70 px de render de altura, sem acessório solto |
| **Elite** | 105 a 140 px (1,5 a 2× a maior horda do capítulo, 70 px), assimétrica, com uma "parte que ataca" em "osso frio" (3.2) que é o único detalhe de alto contraste do corpo |
| **Chefe** | 240 a 350 px (≥ 1,2× o maior herói), com o realismo do herói, que de perto é a regra de quem ameaça |
| **Pet** | Ver 5.6. Fica na camada de cenário e nunca acima da horda |

### 5.3 Raça e gênero
A raça mexe na **proporção dentro do bloco** (cabeça, ombro, centro de gravidade), no idle, na locomoção e na voz (a voz fica com o audio-director). A massa da função não muda (Seção 1, princípio B).

**Proporções no corpo-base nu** (silhueta em idle na câmera de jogo; tolerância ±0,01 nas razões de cabeça e ±0,05 nas de ombro/cintura; a massa da função vem da armadura):

| Raça | Altura (Humano = 1) | Cabeça/altura | Ombro/cintura (m / f) |
|---|---|---|---|
| Humano | 1,00 | 0,135 | 1,50 / 1,35 |
| Orc | 1,08 | 0,115 | 1,75 / 1,55 |
| Elfo | 1,10 | 0,125 | 1,35 / 1,25 |
| Anão | 0,88 | 0,175 | 1,55 / 1,40 |
- **Orc:** cabeça pequena para o ombro, tronco inclinado à frente, passada pesada, peso no calcanhar.
- **Humano:** a referência neutra. Postura marcial e ereta.
- **Elfo:** mais longo e estreito dentro do bloco, passada leve.
- **Anão, o caso difícil:** é baixo e largo, então *todo* Anão tende a ler como Tank. Duas regras:
  - na câmera de jogo, a altura de toda raça fica a ±12% da do Humano;
  - o traço distintivo da função (3.1) é **ampliado em 20% no Anão**: o DPS ganha arma longa e ângulos verticais, e o Mago ganha tecido alto.
- **Fit:** a armadura é autorada no Humano. O Orc e o Elfo usam blendshape de corpo. O Anão tem um **conjunto de fit próprio** (decisão do usuário em 2026-11-03), porque a deformação não fecha ombro e cintura. O custo final fica com o producer e o technical-artist antes da Raça 3.
- **Gênero:** dois por raça, com a mesma silhueta de função. A diferença fica na proporção e na animação, e os dois gêneros têm **a mesma cobertura de armadura** (decisão do usuário em 2026-11-03), porque o peso visual é o realismo prometido.

### 5.4 Expressão e pose
- **Heróis:** realismo contido. Poses de peso e rosto sério, legível só em close (Forja e inventário).
- **Horda:** rígida e quase mecânica. Sem expressão facial, a leitura vem do corpo inteiro, o que também barateia o VAT.
- **Elites e chefes:** realistas no repouso e **exagerados na antecipação**, com cerca de 1,3× de amplitude no windup. A pose avisa antes do decal (P4).

### 5.5 Filosofia de LOD
**Piso de detalhe:** um detalhe com menos de 4 px na resolução de render alvo (810 px de altura), na câmera de jogo, não ganha geometria nem contraste de albedo. No máximo vai para a normal.
- **Herói:** sobrevivem a silhueta, o traço de função, os blocos de material (armadura contra tecido) e a **marca do selo como bloco de no mínimo 6×6 px**.
- **Elite:** só a parte que ataca tem detalhe.
- **Chefe:** silhueta e partes de ataque. O detalhe fino fica para a câmera de intro.
- **Horda:** um único LOD de jogo, com forma e valor e nada mais (conceito L264).

### 5.6 Loja, transmog, pet e conquista
- **Skin e transmog (R1):**
  - passam no teste de silhueta em cinza a 48 px e preservam o traço de função;
  - o volume fica a no máximo +10% do bounding box;
  - obedecem ao teto de calor e à mediana de saturação do herói (4.2e);
  - não usam a faixa proibida, metal em matiz de 44 a 58° com S ≥ 50%, tom de runa, emissivo, serrilha, hachura nem glifo angular;
  - um transmog só copia peças **da mesma função**.
- **Pet (R7):** fica **na camada de cenário** (decisão do usuário em 2026-11-03, para proteger o P4; vende menos).
  - altura de no máximo 35% da do herói, valores de cenário (V de 50 a 75%, S ≤ 35%);
  - sem partículas e sem emissivo;
  - nunca em menta, nunca com anel, nunca no matiz e valor da horda;
  - a "skill" do pet é uma animação dele, sem efeito no chão.
- **Conquista (R2):** duas **âncoras reservadas** no corpo: o peito ou ombro dominante para a marca do selo, e a capa ou as costas para o escudo pentagonal das insígnias. Nenhuma peça de loja ocupa ou cobre essas âncoras.

### 5.7 Pontos que ficam para outras seções
- **Marcador do herói:** o anel no chão é proibido (círculo liso). Se o ux-designer quiser um marcador, a forma tem de ser outra, e a decisão escala ao creative-director como trade-off (Seção 7).
- **Animação por raça:** na visão completa são 8 sets de idle e locomoção (4 raças × 2 gêneros). O orçamento vai para a Seção 8.

## 6. Environment Design Language

### 6.1 Arquitetura
O tom é o de uma civilização antiga engolida pelo deserto: blocos retos monumentais e verticais quebradas por diagonais de desabamento (3.2). A história é da narrativa. Esta seção fixa só o vocabulário visual.
- **Fases de origem:** a raça muda a *forma* e o *material*, nunca a faixa de valor.
  - Orc: pedra bruta e paliçada inclinada.
  - Humano: alvenaria cortada e arcos.
  - Elfo: verticais finas.
  - Anão: talhe na rocha, em relevo **sem glifo angular** (o glifo é reservado à assinatura de conquista).
- **Capítulos:** cada um troca o material dominante e o landmark. A temperatura da Seção 4.3 não muda.
- **Chão:** nunca tem padrão serrilhado, hachurado nem circular liso, porque esses três são decais de chão reservados. Arcos e curvas são permitidos acima do chão. A reserva de vocabulário vale para o plano do chão, o VFX e a UI, não para paredes; na UI, os controles em tela podem ser redondos (Seção 7.5).

### 6.2 Textura
**PBR simplificado com albedo pintado em manchas largas.** Os heróis e os chefes usam PBR completo, porque o metal com peso e a raridade por material dependem dele. O ambiente usa:
- tiling e trim sheets;
- vertex color para variar;
- lightmap baked;
- mapas empacotados em ASTC;
- nenhum detail map na câmera de jogo.

*Por quê:* o PBR mantém o realismo coerente sob as luzes da Seção 4. O albedo de baixa frequência garante que o cenário fique abaixo do herói e da horda na escala de detalhe, e economiza banda e memória no Android intermediário. A escolha de shader é do technical-artist (Seção 8).

### 6.3 Densidade de props

| Área | Regra | O que a dirige |
|---|---|---|
| **Fase de horda** | Pelo menos 75% da área jogável livre. Props nas bordas. Nada acima do joelho dentro da área jogável | Esquiva manual, leitura da massa da horda, overdraw |
| **Arena de chefe** | Pelo menos 90% do chão limpo. Verticais altas só emolduram a borda | O decal de telegraph precisa de fundo uniforme |
| **Dungeon da trindade** | Salas de combate seguem a regra da arena. O assombro mora nos corredores e no fundo, por escala, não por acúmulo | Grandiosidade, mais o custo do heat-haze |
| **Forja e meta-jogo** | A densidade mais alta do jogo: rebites, ferramentas e metal com reflexo. Uma zona escura atrás da bigorna e da UI | Câmera próxima e estática. É o único lugar do micro-detalhe |

### 6.4 Storytelling ambiental
- **Areia acumulada a sotavento de um vento constante:** as linhas de vento levam à saída.
- **Trilhas pisadas** mostram por onde a horda veio.
- **Armas quebradas** ficam deitadas, na faixa de valor do cenário e nunca em pé (em pé leriam como inimigo).
- **Forjas antigas apagadas**, em aço frio: ecoam o ritual sem roubar o branco-quente do selo.
- **Fogo** só branco-âmbar ou já apagado, com fumaça (regra global de fogo, Seção 2).

### 6.5 Regra de legibilidade personagem contra ambiente
Três condições medidas no framebuffer final, na câmera de jogo:
1. **Δ de valor local:** V_anel(i) é a **mediana** de V do chão num anel de 8 px em volta do inimigo i, lida numa captura **só do chão**: o mesmo frame com horda, herói, VFX e telegraph ocultos, então o anel nunca é feito de outros inimigos. V_inim(i) é a mediana de V na máscara do inimigo. Δ_i = V_anel − V_inim, também nas sombras. **Aprovado:** em ≥ 95% dos inimigos Δ_i ≥ 20, e nenhum abaixo de 12. Cena: 300 inimigos na densidade máxima de spawn.
2. **Frequência do chão:** em qualquer janela de 64×64 px (o tamanho de um inimigo), o desvio-padrão de V do chão fica em no máximo 8 pontos. A textura do chão nunca gera bordas com o tamanho de uma silhueta.
3. **Herói:** a mediana de S cumpre a regra 4.2e.

**Sombras na área jogável** (decisão do usuário em 2026-11-03): a sombra densa fica nas paredes e fora da área jogável, e um fill levanta o chão sombreado na área de combate, para a condição 1 valer também na dungeon de meio-dia (Seção 2.6). O contraste alto fica no fundo.

**Teste:** as luzes L1, L2 e L3 (4.2e), cada uma na sua área com inimigos (diagonal luz-área, não produto cartesiano); a Forja não tem horda, e para ela só vale a regra do herói. Em luminância linear, com blur gaussiano σ = 2 px, mede-se o contraste de Michelson por inimigo, C = (L_anel − L_inim)/(L_anel + L_inim). **Aprovado com ≥ 95% dos inimigos em C ≥ 0,35** (o pior caso permitido, V 50 contra V 30, dá ≈ 0,49 para cinza neutro). O mesmo vale para o herói contra o anel dele. O brilho de tela a 30% é escala linear e o C o ignora, então vira uma foto de aparelho real por marco. Uma falha clareia a sombra ou suaviza a textura, nunca o personagem.

## 7. UI/HUD Visual Direction

**Regra-mãe:** no combate, a UI é **borda plana e muda**: ocupa as faixas da safe area e nunca disputa o centro, que pertence a telegraph > herói > aliados > horda > cenário. No meta-jogo, a UI vira **ofício**: placas chanfradas e rebitadas sobre cenas diegéticas. Isso aplica a Seção 1 ("todo o resto é silhueta") à própria interface.

Esta seção foi escrita pelo art-director e revisada em paralelo pelo ux-designer. Onde os dois discordaram, o usuário decidiu (7.8).

### 7.1 Diegético versus tela

| Contexto | Na tela (screen-space) | No mundo / diegético |
|---|---|---|
| **Fase** | Barra de XP fina no topo, wave e tempo, pausa, linha de ícones das skills da run a 60% de opacidade. **Vida do herói na faixa da safe area.** Embaixo ficam os controles: joystick flutuante, esquiva e suprema | Números de dano. Decal do drop com a moldura de raridade (3.5) |
| **Elite e chefe** | Barra do chefe no topo, larga, segmentada por fase do chefe, com o nome na fonte de título | Barra fina sobre a elite. O telegraph é decal de mundo, não é UI |
| **Trindade** | Três placas de grupo na borda esquerda, cada uma com vida e o retrato numa moldura com a **forma da função** (Tank quadrada, DPS angular, Mago vertical, Healer redonda; a curva é legítima porque é do Healer). Aliado fora da tela ganha um chevron na borda, nunca em vermelho-alaranjado. Um aliado caído muda de forma, não só de cor | Sem barra sobre os companheiros, para não poluir o centro com quatro heróis |
| **Oferta de carta** (jogo pausado) | Três placas verticais na metade inferior, ao alcance do polegar, e botões de reroll e de favorecer com contador visível. A tela ignora toques que começaram antes de ela abrir. A skill já registrada leva o ícone de livro. Nova, melhoria e evolução se distinguem por ícone; a evolução se marca por **placa invertida** (fundo claro, texto escuro), nunca por dourado nem por glifo | — |
| **Grimório** | Página 2D ilustrada sobre o frame congelado (2.3). Na troca, comparação lado a lado. Skill inelegível aparece apagada e com o motivo escrito, sem hachura. "Não registrar" tem o mesmo peso visual de "registrar" | A página é o objeto |
| **Ritual do selo** | A decisão (os 4 slots legíveis e uma confirmação por toque segurado) acontece antes da cerimônia. O texto fica sempre sobre placa `#1E242C`, fora da região de bloom. A partir da 2ª vez, o botão de pular fica fixo no canto superior, dentro da safe area | Totalmente diegético: bigorna e metal (2.4) |
| **Forja, inventário** | Placas, grade com molduras de raridade, **Poder de Combate** no cabeçalho. Sem hover: tocar seleciona e abre um painel de detalhes com a variação de Poder de Combate | Cena da Forja ao fundo (6.3) |

O Poder de Combate aparece no meta-jogo e na tela pré-fase, **nunca no HUD de combate**, onde seria ruído. Vida, esquiva e suprema ficam sempre em screen-space.

### 7.2 Tipografia
- **Duas famílias, no máximo.** Para título, uma serifada de inscrição em caixa-alta (pedra monumental, 6.1). Candidata: Cinzel (OFL). Para texto e números, uma sans humanista condensada com **algarismos tabulares**. Candidata: Barlow Condensed (OFL). **Licença e cobertura de pt-br (ã, ç, õ) ainda não verificadas.**
- **Referência:** canvas com lado curto de 1080 px, então 1 pt (dp) = 3 px.
- **Mínimos:**
  - meta-jogo: 12 pt (36 px);
  - **combate: 14 pt (42 px)**, piso provisório a validar em playtest no aparelho de referência;
  - peso nunca abaixo de Regular em ≤ 16 pt; Light e Thin são proibidos.
- **Hierarquia:** título 28 a 32 pt; cabeçalho 20 pt; corpo 14 a 16 pt; legenda 12 pt.
- **Escala de texto:** controle no próprio jogo; as placas crescem com o conteúdo (9-slice, com o chanfro em tamanho fixo).
- **Números de dano:** na sans, em Bold, com contorno SDF de 2 px em `#1E242C`, legível tanto sobre o chão quente quanto sobre a horda fria.

| Tipo | Cor | Tamanho |
|---|---|---|
| Dano causado | `#E6EAF0` | 14 pt |
| Crítico | `#F2DDB0`, marcado sobretudo por escala e peso | 20 pt, pop de no máximo 1,15× |
| Dano sofrido | `#E6EAF0` dentro de uma placa `#1E242C` a 80%, com prefixo "−" (fora da faixa de 4.2a) | 16 pt |
| Cura | menta, sempre com **●** antes (4.1 exige forma circular) | 14 pt |

- **Dano sofrido (decisão do usuário em 2026-11-03):** placa de ferro com número claro, ancorada no herói e **caindo**, enquanto os números aos inimigos sobem; a placa mede no máximo 96×40 no canvas, a 75% de opacidade, no máximo 3 por segundo. O chip de vida perdida é um contorno vazio `#8C96A3` que drena em 400 ms, e o corpo do herói pisca em 3 quadros a 30 fps (S ≤ 10%). O som é do audio-director; o requisito visual é um gancho sincronizado ao flash. Isso remove a exceção da faixa proibida: só o telegraph fica nela.
- Abreviação a partir de 5 caracteres (por exemplo, 12,4k).
- **Densidade:** a horda gera **um número somado por golpe de área**, não um por inimigo. Crítico e dano em elite ou chefe são individuais. Teto de 24 números na tela (knob), regulado pelo mesmo controle do jogador que limita os efeitos aliados (P4).

### 7.3 Iconografia
São três estilos, cada um com dono:
1. **Sistema e skill:** silhueta **chapada** monocromática (`#E6EAF0` ou acento), no máximo um corte interno. Skill de fogo usa amarelo-branco, nunca laranja.
2. **Item:** **ilustrado**, um render do material, *dentro* da moldura de raridade.
3. **Conquista:** o **único** estilo **gravado** (incisão com sombra interna e luz de borda), em glifo angular, nas cores do selo.

Regras de convivência:
- Nada além do glifo usa bevel inciso.
- O glifo nunca entra numa moldura de raridade.
- O escudo pentagonal é exclusivo das insígnias, em slot próprio, fora da grade de itens.
- As formas de raridade só significam algo **em volta de item**. Placas de controle são aço monocromático, sem rebite.
- **Painéis genéricos** nunca combinam chanfro e rebite na contagem de uma moldura de raridade (um painel octogonal com rebite lê como "Azul"). O rebite e o chanfro ficam no padding, nunca na área de toque nem de texto. Abaixo de um tamanho de placa, o rebite decorativo some. O rebite das molduras de raridade é a exceção, porque carrega informação.
- **Pip de raridade de 1 a 5** (decisão do usuário): onde a moldura fica pequena ou ausente (decal de drop visto de longe, ícones abaixo de ~48 dp, log de loot e listas só de texto), um pip de 1 a 5 acompanha o item, para a raridade ler sem cor.

### 7.4 Animação
**Peso de metal:** entra rápido, para seco e assenta 1 a 2 px. Nunca há elástico nem quique.

| Caso | Duração | Easing |
|---|---|---|
| Painel entra | 200 ms | ease-out forte, `cubic-bezier(0.2,0.8,0.2,1)` |
| Painel sai | 120 ms | ease-in |
| Botão pressionado | 60 ms, escala 0,96 e escurece | linear |
| Botão solto | 100 ms | ease-out |
| Cartas | 200 ms cada, escalonadas em 50 ms, **total ≤ 350 ms** | ease-out |
| Ritual (entintar, selo, carimbo) | 600 a 1200 ms | sine in-out |

**Nunca anima no combate:** pulso, piscar contínuo, tremor da UI e barras que balançam. As únicas exceções:
- **chip** de vida perdida, em contorno vazio `#8C96A3`, que drena em 400 ms, e o flash do corpo do herói em 3 quadros a 30 fps;
- suprema pronta: um flash único de 150 ms, com o estado de pronta lido também pela forma (moldura acesa e escala);
- números subindo por 0,6 s.

A carga da suprema é um **molde enchendo de baixo para cima** em `#F2DDB0`, não um preenchimento radial. A recarga da esquiva se mostra por preenchimento vertical ou por contagem, **nunca por hachura**. Há opção de movimento reduzido. Hit-stop e queda em massa respeitam o limite de flashes do requisito de acessibilidade (até 3 por segundo, a verificar).

### 7.5 Controles e marcador do herói
- **Controles em tela redondos** (decisão do usuário): joystick e botões de esquiva e de suprema podem ser redondos, porque o círculo é a affordance mais forte do joystick virtual. A reserva do círculo liso (3.3, 6.1) vale para o mundo (chão e VFX) e para a UI de cura, não para os controles em tela. Os controles ficam fora da área de gesto do sistema na borda inferior.
- **Marcador do herói** (decisão do usuário): por padrão não há marcador; o herói se distingue pela maior saturação, pelo contorno e pelo centro da câmera (5.2). Um **chevron acima da cabeça** pode ser ligado nas opções de acessibilidade. Nunca há marca no chão. Requisito do ux-designer: o jogador acha o herói depois de uma explosão de VFX; a métrica sai de playtest.

### 7.6 Loja versus conquista (R1, R2)
**Regra-chave: o que tem preço não tem glifo, e o que tem glifo não tem preço.**
- **Loja:** fundo de couro escuro `#3A2F28` (H 22°, S 31%, V 23%, fora da faixa proibida). Placa de linha fina em aço, **etiqueta de preço** pendurada em cada item, preview **vestido no seu herói** em 3D. Sem moldura de raridade, sem dourado, sem tons de selo. Dinheiro real e moeda de jogo têm rótulos distintos, e toda compra pede confirmação.
- **Conquista:** Forja acesa, escudo pentagonal, glifo gravado, o esfriamento de 2.7 e "Conquistado: [feito]" no lugar do preço.

### 7.7 Obrigações e requisitos de UX
- **Paleta 4.4:** acento de UI em aço neutro `#8C96A3`, distinto do aço do selo `#5E7FA6`, que é exclusivo da conquista.
- **Barras de vida** sem vermelho: preenchimento `#E6EAF0`. Vida baixa se sinaliza pela barra e por som, **sem vinheta vermelha** (decisão do usuário; ver 4.2a).
- **Faixa proibida:** zero pixels de UI nela, sem exceção (o dano sofrido usa placa de ferro com número claro, 7.2).
- **Ordem de render (decisão do usuário em 2026-11-03, híbrido):** cenário < horda < aliados < herói < números aos inimigos (world-space) < **telegraph** < placa de dano sofrido do herói < HUD de borda. A HUD de borda cai para 40% de opacidade quando um telegraph passa sob ela. Nenhuma UI opaca oclui o telegraph; a única exceção é a **placa de dano sofrido** (≤ 96×40 no canvas, 75% de opacidade, no máximo 3 por segundo), que o creative-director precisa confirmar.
- **Opacidade e densidade de efeitos (P4):** o controle do jogador vale para VFX aliado, números de dano e pet, e **nunca para o telegraph**. Fica acessível pela pausa, com prévia ao vivo.
- **Mobile:** nenhum painel translúcido de tela cheia no combate. Safe areas respeitadas, com recuo para os gestos de navegação.
- **Requisitos de UX citados pelo ux-designer de memória, a verificar antes de registrar em `design/accessibility-requirements.md`:** alvo de toque de 48×48 dp com 8 dp entre alvos (Material Design; iOS HIG: 44 pt); contraste de texto de 4,5:1 (3:1 para texto grande, WCAG 1.4.3); contraste de componente de 3:1 (WCAG 1.4.11); até 3 flashes por segundo (WCAG 2.3.1).
- **Contraste da paleta:** `#E6EAF0` sobre `#1E242C` dá cerca de 13:1. As cores de raridade e o aço ficam entre cerca de 3,1 e 3,8:1 sobre o fundo, então servem para borda e moldura, nunca para texto pequeno; o nome do item vai em texto claro dentro da moldura.

### Inegociáveis
1. Nada de UI no plano do chão (inclui o anel).
2. Nenhum pixel na faixa 4.2a além do telegraph.
3. Telegraph nunca ocluído por UI opaca (única exceção: a placa de dano sofrido, 7.7).
4. Bevel gravado e escudo só na conquista.
5. Nada pulsa no combate.
6. Mínimo de 14 pt no combate.
7. Nenhum ornamento no HUD de combate.
8. Vida, esquiva e suprema em screen-space.

### 7.8 Decisões de conflito (art-director contra ux-designer)

| Ponto | ux-designer | art-director | Decisão do usuário (2026-11-03) |
|---|---|---|---|
| Forma dos controles | Círculo em tela | Base octogonal sem rebite (risco de ler como Azul) | **Círculo em tela** |
| Vida do herói | Em tela | Barra sobre a cabeça | **Em tela** |
| Marcador do herói | Opcional nas opções | Nenhum; contorno por oclusão se o playtest provar | **Opcional nas opções** |
| Raridade para daltônicos | Pip de 1 a 5 | Só a moldura | **Pip de 1 a 5** |
| Vinheta vermelha de vida baixa | — | A exceção "dano inimigo" não a cobre | **Não há vinheta** |

### 7.9 Pendências para o sign-off (AD-ART-BIBLE)
- **Números de dano abaixo do telegraph (resolvido, D4):** os números aos inimigos são world-space no passe 3D, antes do telegraph; o dano sofrido é a placa de UI da 7.7. **Pendente:** o creative-director confirma a exceção da placa ao inegociável 3, e o technical-artist implementa o passe 3D (o custo mobile da projeção mundo→tela é NOT SOURCEABLE).
- **Anéis aliados contra o círculo da cura (resolvido, D1):** ver a Seção 3.6 (anel fechado só da cura; efeito aliado em arco aberto ou disco difuso).
- **Escudo pentagonal contra o hexágono apontado do Roxo:** teste de miniatura junto com o de 4.2d.
- **Fontes:** licença e glifos de pt-br das candidatas.

## 8. Asset Standards

Escrita em paralelo pelo art-director (preferências de arte) e pelo technical-artist (limites técnicos). Onde divergiram, os dois lados e a decisão do usuário estão em 8.9.

> **Todo orçamento numérico desta seção é PROVISÓRIO** e precisa ser confirmado pelo spike de performance (build Release, IL2CPP ARM64, aparelho de referência, minuto 20). Premissas: orçamento de frame de ~12 ms (`.claude/docs/technical-preferences.md`), escala de render de ~0,75 sobre 1080p, câmera alta com o herói ocupando de 150 a 200 px. **Resolução de referência de todo "px" desta bible:** buffer de render de 810 px de altura (1080 × 0,75), sem UI. A UI se mede no canvas de 1080 (canvas = render ÷ 0,75). "Altura" é a silhueta da malha em idle, do chão ao topo da cabeça, sem arma, capa nem VFX. Se o jogo for em retrato, escalar pela altura de render (a orientação não está fixada: `A VERIFICAR` com o ux-designer). O teto de memória continua **TO BE CONFIGURED** até o spike.

### 8.1 Formatos

**Cadeia de ferramentas (decisão do usuário em 2026-11-03):** a criação usa o melhor de **Canva, Tripo, Blender e Unity**, e só elas. Substance Painter, Photoshop e Figma estão fora da cadeia. Fontes e datas de consulta estão em 8.12; o que não pôde ser confirmado está marcado `A VERIFICAR`.

| Tipo | Ferramenta e passo | Exportação | Por que esta é a melhor das quatro |
|---|---|---|---|
| **Concept e moodboard** | **Canva:** moodboard, paleta de swatches da 4.1, folha de silhueta em cinza a 48 px. **Tripo:** concept 3D rápido a partir de imagem ou texto, para julgar a massa da função de vários ângulos | PNG (referência, não vai para o jogo) | O Canva é o único com layout livre de colagem. O Tripo troca o desenho 2D pelo volume, que é o que a 3.1 testa |
| **Malha** | **Tripo:** base ou high-poly de referência. **Blender:** retopo para o orçamento da 8.3, UV, pivô, escala e eixo da 8.8, LOD manual | FBX binário. O Tripo exporta FBX, GLB, OBJ, USD, STL e 3MF | Só o Blender tem edição de malha e UV com controle. O Tripo acelera o volume, mas não respeita o orçamento: o modo low-poly vai de 1.000 a 20.000 triângulos e o modo quad de 500 a 10.000 quads |
| **Textura, bake** | **Blender (Cycles):** normal em espaço tangente e AO, do high do Tripo para o low, com Selected to Active ou cage | PNG 8 bits | É o único das quatro que faz bake. Exige UV e um nó Image Texture ativo no material |
| **Textura, pintura** | **Blender** com o add-on **Ucupaint** (decisão do usuário): pintura em camadas sobre o albedo, com a paleta travada. O PBR do Tripo (base color, metallic, roughness, normal) serve só de ponto de partida | PNG 8 bits | É o único com pintura no modelo. O Blender não tem camadas nativas; o Ucupaint as recupera (ver nota 1) |
| **Textura, máscara empacotada** (metal, AO, smooth) | **Blender:** combinar os canais e inverter roughness para smoothness. O Unity URP usa smoothness, e o próprio Tripo avisa dessa inversão | PNG 8 bits, `_msk` | `A VERIFICAR` — empacotar canais no Compositor do Blender (Separate/Combine Color mais File Output) no Blender 5.x. Fallback: o technical-artist empacota na importação no Unity |
| **Animação e rig** | **Blender:** os 8 esqueletos da família (hum, orc, elf e dwf × m e f), skin, blendshapes de fit, clipes a 30 fps. O auto-rig do Tripo **é descartado**: o esqueleto dele não é o nosso | FBX só com o esqueleto, um clipe por arquivo | A 8.6 exige hierarquia e nomes de osso idênticos. Só um rig feito à mão garante isso |
| **VFX** | **Unity:** Shader Graph (dissolve da horda, quad do telegraph, halo da bigorna) e sistema de partículas (8.7). **Blender:** render de flipbook com câmera ortográfica e fundo transparente | PNG em atlas | A maior parte do VFX da 8.7 é shader, não flipbook. `A VERIFICAR` — montar a grade do atlas de flipbook no Blender (planos em grade e render ortográfico) ou no Canva (manual) |
| **UI: molduras 9-slice e placas** | **Blender:** a placa de metal da 3.3 e 3.5 modelada (chanfros e rebites exatos), render ortográfico com um rig de luz fixo. **Unity:** bordas de 9-slice no Sprite Editor (Mesh Type Full Rect) e slice em UI Toolkit | PNG com alfa, 2× | Os chanfros contados são a leitura da raridade. Geometria real os deixa exatos e com o metal da Forja. O Canva não tem precisão para isso |
| **UI: ícones** | **Blender:** render do próprio modelo 3D do item com câmera 3/4 e luz padrão, **sem moldura** | PNG com alfa, autorado em 256 | Família visual consistente. A moldura é composta pelo Unity por raridade |
| **UI: telas e layout** | **Canva** (plano pago, decisão do usuário): mockup de tela e hierarquia. **Unity:** layout final no UI Builder e sprite atlas | Mockup em PNG. A tela final vive no Unity | O Canva é o mais rápido para iterar layout. O Unity é o dono do runtime |

**Notas da 8.1:**
1. **Pintura PBR em camadas, a lacuna que era do Substance.** O Blender não tem sistema de camadas nativo: um foi anunciado, sem data confirmada. O contorno escolhido pelo usuário é o **Ucupaint**, add-on gratuito de terceiros no Blender Extensions (v2.4.9 de 2026-07-29, Blender 4.2 ou superior, segundo a consulta de 2026-11-03). O contorno alternativo, se o add-on falhar, são camadas manuais (imagens misturadas por nós Mix no material, com o AO baked como máscara de desgaste de borda, depois bake final para um mapa só), que custam de 1,5 a 2× o tempo por peça. O estilo reduz a perda, porque a 6.2 pede albedo em manchas largas e não micro-detalhe.
2. **Concept 2D pintado.** Nenhuma das quatro é ferramenta de pintura. Contorno: concept 3D no Tripo com paintover no Grease Pencil do Blender (`A VERIFICAR` — Grease Pencil no Blender 5.x). Custo: menos exploração de silhueta por hora do que um esboço à mão.
3. **Canva.** PNG transparente e SVG exigem plano pago, que o usuário tem ou vai ter. `A VERIFICAR` — se a escala do PNG chega a 2× exato; contorno: criar o documento já em 2× (por exemplo, 512 px para uma moldura de 256).
4. **Daltonismo (4.2c).** `A VERIFICAR` — se alguma das quatro simula protanopia e deuteranopia. Se nenhuma simular, o technical-artist faz um filtro de captura no Unity.

**Compressão em Android:** ASTC, com 6×6 no albedo e na máscara empacotada (metal, AO, smooth) e 4×4 no normal (3,56 e 8 bpp, mais 33% de mip). O fallback é ETC2. **NOT SOURCEABLE:** as opções de ASTC no importador do Unity 6.3 e o suporte a ASTC no GPU do aparelho de referência não estão em `docs/engine-reference/unity/`; verificar no manual do importador e no aparelho.

### 8.2 Convenção de nomes
Para arquivos de arte: `categoria_nome_variante_tamanho`, tudo em minúsculas, com códigos curtos em inglês. Código, cenas e prefabs seguem PascalCase (`project.yaml` e `.claude/docs/technical-preferences.md`: a regra "Files: PascalCase" vale para arquivos de código, com o nome da classe; arquivos de arte não estavam cobertos).

Códigos: raça `orc|hum|elf|dwf`, gênero `m|f`, raridade `r1` a `r5`. Raridade nunca leva nome de cor.
- Peça de set: `char_tank_chest_ironwall_hum_m.fbx`
- Variante de raridade: `mat_tank_chest_ironwall_r4.mat`
- Horda: `enm_horde_ghoul_a.fbx`
- Elite: `enm_elite_brute_01.fbx`
- Chefe: `enm_boss_sandwyrm_01.fbx`
- Prop: `env_prop_column_broken_large.fbx`
- Textura: `tex_char_tank_chest_ironwall_alb.png` (sufixos `_alb`, `_nrm`, `_msk`)
- Material: `mat_env_ruin_trim_ch02.mat`
- Animação: `anim_orc_m_idle_01.fbx` (por raça) e `anim_shared_tank_attack_heavy_01.fbx` (combate compartilhado)
- Ícone: `ui_icon_item_tank_chest_ironwall_256.png`
- Moldura: `ui_frame_rarity_r4_9s.png`
- Cosmético de loja: `cos_shop_tank_chest_dunewalker_hum_m.fbx`
- Cosmético de conquista: `cos_ach_seal_glyph_07.png`, `cos_ach_insignia_clear_ch03.png`
- Pet: `pet_sandfox_01.fbx`

Os prefixos `cos_shop_` e `cos_ach_` permitem auditar R1 e R2 por busca de nome.

### 8.3 Triângulos (provisório)

| Categoria | LOD de jogo | Close (Forja, intro) |
|---|---|---|
| Herói, set completo (por raça e gênero; o Anão tem o mesmo teto, mesmo com fit próprio) | ≤ 8k | ≤ 20k |
| Elite | ≤ 3k (1 LOD) | n/a |
| Chefe | ≤ 15k | ≤ 30k |
| Horda | ≤ 400 (1 LOD, 5.5) | n/a |
| Pet | ≤ 1,5k | n/a |
| Prop pequeno / médio | ≤ 300 / ≤ 1,5k | n/a |
| Módulo de ambiente | ≤ 3k | Forja: cena inteira ≤ 150k |

**Pior caso do spike:** horda 300 × 400 = 120k, heróis 4 × 8k = 32k, chefe 15k, elites ~12k, ambiente ≤ 60k e passe de sombra ~40k. Teto provisório de **≤ 300k triângulos por frame**. Todos os orçamentos ficam bem abaixo de 65k vértices por malha.

**Orçamento de proxy de herói do spike** (critério de pipeline do MVP, `design/gdd/game-concept.md` L408): 8k / 20k triângulos, ≤ 3 MB de textura em jogo, ≤ 2 materiais e ≤ 75 ossos.

### 8.4 Textura (provisório)

| Categoria | Resolução máxima | Memória |
|---|---|---|
| Herói | 3 mapas de 1024² em jogo; 2048² **só na Forja**, carregado por Addressables | ≤ 3 MB em jogo, ≤ 10 MB na Forja |
| Chefe | 1024² em jogo, 2048² na intro | ≤ 6 MB |
| Elite | 512² | ≤ 0,7 MB |
| Horda | atlas compartilhado por capítulo, **só albedo** | ≤ 2 MB no total |
| Pet | 256² | ≤ 0,15 MB |
| Prop | trim sheet de 1024 por capítulo; prop único em 512 | dentro do ambiente |
| Ambiente | trim sheets e tiling de 1024 (~256 px/m) mais lightmap | ≤ 12 MB |
| VFX | atlas | ≤ 4 MB |
| UI | 2× a referência de 1080p; moldura 9-slice de 256 | fora do orçamento de cena |
| Ícone | autorado em 256, 128 em runtime | fora do orçamento de cena |

**Por cena de combate: ≤ 50 MB de textura**, sem contar UI e render targets.

### 8.5 LOD

| Categoria | Níveis |
|---|---|
| Herói | **2:** jogo (silhueta, traço de função, blocos de material e marca do selo de no mínimo 6×6 px) e close (Forja e inventário) |
| Elite | 1. Só a parte que ataca tem detalhe |
| Chefe | 2: intro e jogo |
| Horda | **1**, sem exceção |
| Prop | 2. O LOD automático do Mesh LOD (Unity 6.2+) é aceito se o technical-artist o validar (NOT SOURCEABLE: o Mesh LOD só é citado em `docs/engine-reference/unity/VERSION.md`) |
| Ambiente | 1, mais lightmap |
| Pet | 1 |

### 8.6 Materiais, draw calls e rig (provisório)
- **Herói:** ≤ 2 slots de material (opaco em atlas mais 1 cutout de tecido).
- **Raridade por peça na malha fundida:** 1 instância de material por conjunto equipado. O **índice de slot** vai em vertex color (canal R, constante por peça, Color Attribute no Blender), e o Shader Graph o usa para ler a raridade de 8 slots em duas propriedades `float4` do material. **Custo:** 4 B por vértice (≤ 32 KB em jogo, ≤ 80 KB no close), 0 textura, mesma variante de shader. **Descartados:** o canal do atlas `_msk`, porque o ASTC 6×6 sangra o índice nas bordas de bloco e os 3 canais já estão em uso; e material por peça, que volta a multiplicar draws. **NOT SOURCEABLE / `A VERIFICAR`:** o vertex color sobreviver à fusão de skinned meshes e ao FBX do Blender 5.x; a leitura sem conversão sRGB; `float4` por slot com o SRP Batcher.
- **Peças modulares:** cada peça como renderer separado multiplica os draws. As peças são fundidas numa malha só ao equipar. Isso é trabalho do engine-programmer; a API de combinar skinned meshes é **NOT SOURCEABLE**.
- **Raridade:** parâmetro de material sobre a **mesma variante de shader**, nunca keyword: o SRP Batcher agrupa por variante, e uma keyword por raridade multiplica variantes (conceito L350). Se MaterialPropertyBlock é compatível com o SRP Batcher: **NOT SOURCEABLE**.
- **Horda:** mesma malha e mesmo material por tipo, com `RenderMeshInstanced` (1 draw por tipo). Instancing de malha skinned não está na referência, por isso a horda **não pode** ser SkinnedMeshRenderer. O GPU Resident Drawer em mobile e em skinned é **NOT SOURCEABLE**.
- **Teto provisório de ≤ 150 draw calls:** ambiente 40, heróis com sombra 16, chefe e elites 11, horda 4, VFX 30, UI 30, pós 10.
- **Ossos:** herói ≤ 70 de corpo mais ≤ 10 de tecido ou capa, sem ossos faciais; elite ≤ 60; chefe ≤ 90. Um esqueleto por raça e gênero (8), uma **família de hierarquia e nomes de osso idênticos** que só muda bind pose e proporção (5.3); as peças não trazem ossos novos, exceto uma lista fixa de ossos de tecido e capa (Mago).
- **Influências:** autorar com 4 e medir com 2 no LOD de jogo (o limite por qualidade é **NOT SOURCEABLE**).
- **Ajuste de corpo por raça (Orc, Elfo):** **blendshape em runtime** sobre a armadura autorada no Humano (decisão do usuário). O custo de CPU por personagem é medido no spike; a alternativa registrada é o bake offline de uma malha por raça. O Anão tem fit próprio (5.3).
- **Horda animada por partes rígidas** (decisão do usuário): até 12 partes com 1 influência, com matrizes em textura de ossos. É a forma mais barata e casa com a horda "rígida, quase mecânica" (5.4). O spike compara com VAT (300 vértices × 60 frames × 8 B ≈ 144 KB por clipe).
- **Culling:** Cull Update Transforms em heróis e elites.
- **Memória de clipes** dos 8 sets de idle e locomoção: **NOT SOURCEABLE** (compressão de clipe), a medir.

### 8.7 Partículas e efeitos por estado (provisório)
**Overdraw médio ≤ 2,5×**, com pico local ≤ 4×, medido no Rendering Debugger. Nenhum cartão passa de 10% da tela.

| Estado (Seção 2) | Teto |
|---|---|
| 2.1 e 2.6 | 1 quad de poeira mais ≤ 150 cartões aliados (≤ 36 por herói × 4 = 144, 6 de reserva compartilhada). A morte da horda é dissolve de shader, não partícula |
| 2.2 | 0 partículas novas. O telegraph é um quad projetado no chão plano (o URP Decal é **NOT SOURCEABLE**) |
| 2.3 e 2.8 | 0 |
| 2.4 | ≤ 8 de vapor mais 1 quad de shimmer |
| 2.5 | ≤ 20 faíscas |
| 2.7 | ≤ 30 |

O VFX Graph em mobile é **NOT SOURCEABLE**; o spike compara VFX Graph com o sistema de partículas legado.

**Efeitos caros (decisão do usuário):**
- **Sombra:** só heróis e chefe projetam, 1 cascata, mapa ≤ 1024, distância curta. É o primeiro corte no piso de 30 fps (vira blob).
- **Heat-haze (2.6):** por padrão, **distorção de vértice num cartão de horizonte**, sem cópia de tela. A distorção real em meia resolução só entra se o spike mostrar folga.
- **Bloom da bigorna (2.4):** por padrão, **cartão de halo aditivo**, com zero pós-processamento. O bloom real só entra na Forja estática, se a medição permitir.
- **PBR completo em herói e chefe:** cabe com 3 amostras e máscara empacotada, sem detail map.

### 8.8 Exportação, assets comprados e cosméticos
- **Escala:** 1 unidade = 1 m e fator de importação 1,0. Transformações aplicadas antes de exportar.
- **Eixo:** Y para cima, frente em +Z, sem rotação residual no root.
- **Pivô:** personagem no chão, entre os pés. Peça modular na origem do esqueleto, para encaixar sem offset. Prop na base de contato. Arma no punho.
- **Raridade:** `r1` a `r5` são **presets de parâmetros**, aplicados por slot no material único do conjunto (8.6), sobre a mesma malha (tom de metal, rugosidade e padrão de friso). Nunca malha nova, nunca emissivo pulsante. A moldura vive na UI e no decal.
- **Asset comprado ou Tripo:**
  - **Aceita-se de asset comprado:** topologia dentro da 8.3, UV limpo e normal esculpida.
  - **Aceita-se do Tripo:** só o volume, como high-poly ou base de retopo, e o PBR como **referência** de cor. A UV automática do Tripo só fica se passar na densidade da 8.4 e no atlas. O auto-rig do Tripo nunca fica.
  - **Refaz-se sempre, no Blender:** escala, eixo e pivô; skin no esqueleto compartilhado; retopo dentro da 8.3 (o Tripo não chega ao piso da horda); bake de normal e AO; repintura do albedo em manchas largas, com S ≤ 40% nos tons quentes; conversão de roughness para smoothness; remoção de acessório solto (horda) e de serrilha, hachura ou glifo angular; renomeação com `cos_shop_` ou `cos_ach_` quando for cosmético.
  - **Nunca entra cru:** nenhum GLB ou FBX do Tripo vai direto para `Assets/`.
  - **Licença:** cada pasta guarda um `_license.txt`. Para o Tripo, registrar o plano usado e os termos de uso comercial. **`A VERIFICAR` — os termos de licença comercial do Tripo no plano do usuário, antes de qualquer asset do Tripo entrar num build que será vendido.**
- **Pipeline de cosméticos** (provas retidas em `production/qa/evidence/`):
  - **Skin (R1 e 5.6):** as malhas em todos os esqueletos, com o fit próprio do Anão; a captura em cinza a 48 px lado a lado com o set base; bounding box ≤ +10%; a matriz de 6 luzes (4.2e) com zero blocos 4×4 na faixa proibida e a mediana de S conforme a 4.2e; a declaração de que não usa emissivo, metal entre 44 e 58° com S ≥ 50, tom de runa, serrilha, hachura nem glifo; e a máscara das âncoras de conquista com sobreposição zero.
  - **Transmog:** nenhum asset novo. Entrega a tabela de mapeamento travada na mesma função e uma captura mostrando a marca do selo visível.
  - **Pet (R7):** altura ≤ 35% da do herói; capturas nas luzes L1 a L6 com V de 50 a 75% e S ≤ 35%; a prova de que não é menta, não tem anel e não está no matiz e valor da horda; a "skill" como **só um clipe de animação**, sem partícula, emissivo ou decal de chão; e a atribuição à camada de cenário.

### 8.9 Divergências e decisões (2026-11-03)

| Ponto | Ideal (art-director) | Limite (technical-artist) | Decisão do usuário |
|---|---|---|---|
| Textura de herói, elite e horda | Atlas de 2048 do herói com mip de 512 em jogo; elite 1024; horda com máscara | Herói 1024 em jogo e 2048 só na Forja; elite 512; horda só albedo | **Limite do technical-artist** |
| LOD do herói | 3 feitos à mão | 2 | **2** |
| Animação da horda | VAT padrão, partes rígidas fallback | Partes rígidas padrão, VAT no spike | **Partes rígidas, VAT no spike** |
| Heat-haze e bloom (2.4, 2.6) | Distorção em meia resolução; bloom na bigorna | Distorção de vértice em cartão; halo aditivo | **Alternativa barata como padrão** |
| Ajuste de corpo por raça | Blendshape em runtime | Bake offline por raça | **Blendshape em runtime** |
| Nomes de arquivo de arte | snake_case | — | **snake_case** (a regra PascalCase do projeto é para código) |
| Cadeia de ferramentas | — | — | **Canva, Tripo, Blender e Unity**, só essas; **Ucupaint** conta como Blender; **Canva em plano pago** |

**Prioridade de corte do art-director, se o spike apertar:** primeiro o 2048 do chefe, por último o 2048 do herói na Forja, que é onde o jogo vende o "eu forjei".

### 8.10 Importador e build
- **Com fonte:** API mínima 24 (`docs/engine-reference/unity/breaking-changes.md`). URP com Render Graph. Luzes adicionais limitadas pelo asset do URP: o combate usa só a luz principal. O módulo Android está instalado (`docs/engine-reference/unity/VERSION.md`).
- **NOT SOURCEABLE**, a verificar com import de proxy no spike e no manual do 6.3: escala e eixo do FBX; tamanho máximo de textura; formato de índice; quantidade de cascatas; Opaque Texture; Mesh LOD (6.2, só citado); Shader Build Settings (6.3, só citado).

### 8.11 Cadeia de ferramentas por asset

**(a) Peça de set de herói, do Tripo ao prefab**
1. **Canva:** a folha da peça com o swatch do set e a silhueta da função a 48 px.
2. **Tripo:** image-to-3D em alta, usado como high-poly. Exportar FBX ou GLB. A textura do Tripo é só referência.
3. **Blender:** retopo dentro de ≤ 8k triângulos para o set completo em jogo e ≤ 20k no close; UV no atlas do herói; bake de normal e AO do high do Tripo.
4. **Blender, skin:** skin no esqueleto Humano **do gênero da peça** (`hum_m` ou `hum_f`, dois dos 8) e nos ossos de tecido da lista fixa; blendshapes de Orc e Elfo; fit próprio do Anão. Pivô na origem do esqueleto, Y para cima, frente em +Z.
5. **Blender (com Ucupaint), pintura:** albedo com **teto de S ≤ 40% em todo matiz de 350° a 38°** (4.2e), usando só a paleta travada; nenhum pixel na faixa proibida; a máscara empacotada com smoothness invertida.
6. **Exportação:** `char_tank_chest_ironwall_hum_m.fbx`, `tex_…_alb/_nrm/_msk.png`.
7. **Unity:** importação com ASTC (8.1); **um** Shader Graph do herói e os presets `r1` a `r5` por slot, só por parâmetro (8.6); prefab em PascalCase; a matriz de 6 luzes da 4.2e, com captura em `production/qa/evidence/`.
8. **Se for de loja:** prefixo `cos_shop_`; no passo 5, nenhum glifo, serrilha, hachura, tom de runa, emissivo ou metal de 44 a 58° com S ≥ 50; as âncoras do selo livres (máscara de sobreposição zero, 8.8). **Se for de conquista:** `cos_ach_`, e o glifo vai só na âncora reservada.

**(b) Inimigo da horda por partes rígidas**
1. **Tripo:** a massa a partir do concept, em modo low-poly. Isso **não** chega aos ≤ 400 triângulos, porque o piso do Tripo é de 1.000 triângulos (valor de wrappers de API, não da documentação oficial: `A VERIFICAR`).
2. **Blender, malha:** redução manual até ≤ 400 triângulos; corte em ≤ 12 partes rígidas, cada uma com **1 influência** num osso (8.6); nenhum acessório solto.
3. **Blender, textura:** albedo só, no atlas do capítulo; V ≤ 30%, H de 200 a 230°, S ≤ 35% (4.2e); sem normal nem máscara.
4. **Blender, animação:** clipes rígidos e "quase mecânicos" (5.4), exportados em FBX como `enm_horde_ghoul_a.fbx`.
5. **Unity:** a textura de matrizes de osso e o `RenderMeshInstanced` ficam com o technical-artist. Captura da regra 6.5 (Δ de V ≥ 20, também na sombra).

**(c) Moldura de raridade e ícone de item**
1. **Canva:** a grade das 5 raridades em mockup, com teste em cinza e em miniatura.
2. **Blender, moldura:** uma placa por raridade, com o chanfro contado da 3.5; render ortográfico em 2× com fundo transparente: `ui_frame_rarity_r4_9s.png`. **Regra de 9-slice:** as **pontas do Roxo e a coroa do Dourado não ficam na borda que estica**; elas viram sprites sobrepostos, ancorados no centro, senão o 9-slice as deforma.
3. **Blender, ícone:** render do modelo do item com câmera e luz fixas, fundo transparente, sem moldura: `ui_icon_item_tank_chest_ironwall_256.png`. Um ícone serve às 5 raridades.
4. **Unity:** Sprite Editor com Mesh Type Full Rect e bordas L, R, T, B; sprite atlas; composição de ícone, moldura, pontas e **pip de raridade** no UI Toolkit. Ícone de loja (`cos_shop_`) nunca carrega moldura de raridade, glifo ou dourado (R1). Insígnia `cos_ach_` sempre no escudo pentagonal (4.2d).

### 8.12 Fontes e ressalvas da cadeia de ferramentas
Consultadas pelo art-director em 2026-11-03: documentação do Tripo e dos seus modelos (formatos de exportação, modo low-poly e quad, PBR, rig), o manual do Blender (Render Baking), o Blender Extensions (Ucupaint), o 80.lv (sistema nativo de camadas, anunciado), o manual do Unity (9-slice no Sprite Editor e no UI Toolkit) e a ajuda do Canva (tipos de arquivo e fundo transparente).

**Ressalvas:**
- Parte das fontes do Tripo é de wrappers de API ou conteúdo promocional, e não da documentação oficial.
- A documentação de 9-slice do Unity consultada é do 6.4 (e uma página do UI Toolkit é do 2022.3), não do 6.3 que o projeto fixa.
- O exportador FBX nativo do Blender 5.x só tem relatos da comunidade de quebra em add-on de terceiro: `A VERIFICAR` — o exportador FBX nativo no Blender 5.x com skin e blendshape, num proxy do spike.
- `A VERIFICAR` (resumo): termos de licença comercial do Tripo; piso de triângulos do modo low-poly do Tripo; escala 2× do PNG do Canva; empacotamento de canais no Compositor; Grease Pencil no Blender 5.x; atlas de flipbook; simulação de daltonismo.

### 8.13 Risco de escopo de arte para um dev solo
A bible exige um conjunto grande para uma pessoa:
- 8 esqueletos (4 raças × 2 gêneros), com blendshapes de Orc e Elfo e **fit próprio do Anão**.
- 5 raridades por parâmetro, com a malha fundida.
- 2048 na Forja.
- **Retopo manual de tudo**, porque o piso do Tripo (1.000 triângulos, `A VERIFICAR`) não chega ao de 400 da horda.
- Pintura em Ucupaint, com fallback manual de 1,5 a 2× o tempo de textura.
- A matriz de QA da 4.2e (6 luzes × 8 esqueletos × 2 enquadramentos).

O risco é de prazo, não de qualidade. Este bloco **não altera o MVP do conceito**.

**Recomendação ao producer, que decide:** uma **fatia vertical de arte**. Humano, um gênero, duas funções de silhueta oposta (Tank e Mago), 1 tipo de horda, 1 elite, o telegraph e a Forja, com o QA 100% pelo `ArtQaRunner` (8.14). Raças e gêneros restantes só depois que a fatia passar nas regras 4.2 e 6.5 e o custo real de retopo e fit for medido.

### 8.14 Automação de QA de arte
`ArtQaRunner` em `Assets/Tests/PlayMode/`, mais a cena `QA_Capture` (câmera de jogo e 1 luz direcional fixas).
- **Loop:** L1 a L6 × lista de prefabs (ScriptableObject) × enquadramentos. A temperatura vem de `Light.colorTemperature` com `GraphicsSettings.lightsUseColorTemperature` (`A VERIFICAR` no 6.3). Os LUTs de chefe e derrota entram por peso de Volume URP (`A VERIFICAR`).
- **Captura:** renderiza num `RenderTexture` fixo de 1440×810 e lê com `ReadPixels`. Isso independe do render scale.
- **Máscaras:** re-renderiza por camada (`Camera.cullingMask`), com materiais trocados por unlit chapado. Replacement shader em SRP: **NOT SOURCEABLE**.
- **Análise** em C# puro sobre `Color32[]` (`Color.RGBToHSV`): faixa 4.2a, teto de calor, mediana de S, Δ e Michelson por inimigo, filtro de daltonismo (matriz 3×3), cinza a 48 px, altura da silhueta (tamanhos de 5.2).
- **Saída:** CSV de pass/fail por regra, PNGs e uma contact sheet por skin em `production/qa/evidence/`.
- **Execução:** `-runTests` em batchmode **com GPU**, sem `-nographics` (`A VERIFICAR`).
- **Manual:** julgar a silhueta a 48 px e a foto de aparelho.
- **Escala:** uma skin roda hum_m, hum_f e dwf_m (pior fit) × 6 luzes × 2 enquadramentos = 36 capturas. Os outros esqueletos só quando o fit muda.

## 9. Reference Direction

Cinco referências. Cada uma alimenta uma seção diferente da bible, então nenhuma duplica a direção de outra.

### 9.1 Lineage 2 (e MIR4 como prova de que esse visual roda em mobile)
- **O que tomar:** o mesmo set de armadura vestido em corpos de raças diferentes. O set continua reconhecível, e a raça aparece na proporção, na postura e no idle. Isso alimenta a 5.3 e o princípio B: a armadura é autorada no Humano e ajustada por blendshape. Tomar também a armadura em placas com blocos de material bem separados (metal, couro, tecido), que são o que sobrevive no LOD de jogo (5.5).
- **O que evitar:** o brilho de encantamento da arma (emissivo pulsante e às vezes vermelho), que viola a 8.8, a R1 e a 4.2a. Evitar a armadura feminina com menos cobertura, contra a 5.3 (mesma cobertura nos dois gêneros). Evitar a filigrana fina, que fica abaixo de 4 px e morre na câmera de jogo (5.5). Do MIR4, evitar o bloom de tela cheia (8.7).

### 9.2 Survivor.io e Archero
- **O que tomar:** a composição da tela de horda. O chão é claro e quase sem padrão, e a horda é uma massa escura de unidades iguais e simples, legível de cima. Alimenta a 3.2, a horda da 5.2, os 75% de área livre da 6.3 e as condições 1 e 2 da 6.5.
- **O que evitar:** a proporção chibi e a paleta saturada, contra a 5.1 e a 4.2e. Evitar um número de dano por inimigo, contra a 7.2 (um número somado por golpe de área). Evitar a escada de raridade por cor, que nesses jogos termina em vermelho no topo: viola a 3.5 e a 4.2a ao mesmo tempo.

### 9.3 World of Warcraft, Zul'Farrak
- **O que tomar:** a dungeon composta em volta de **um** landmark monumental que se lê só pela silhueta, como a pirâmide de degraus de onde a horda desce. Alimenta a 6.1 (cada capítulo troca o landmark) e a 6.3 (o assombro vem da escala, não do acúmulo). Tomar também o albedo pintado em manchas largas e de baixa frequência (6.2).
- **O que evitar:** as proporções estilizadas (ombreiras enormes), contra o teto de 10 a 15% da 3.1. Evitar a saturação do cenário pintado, contra o S ≤ 35% da 4.2e. Evitar a luz pintada dentro do albedo, que quebra as 4 luzes da Seção 4. Evitar entalhes de glifo em parede e chão, contra a 6.1. Evitar a cor por classe, contra o princípio A (função pela forma).

### 9.4 Joseph Wright of Derby, *An Iron Forge* (1772)
- **O que tomar:** a luz de ponto único. A barra incandescente é a única fonte de luz, ilumina o metal e os rostos por baixo, e o fundo é quase preto. Alimenta a 2.4 (valor ≤ 15% e um ponto único), a 2.5 e a zona escura atrás da bigorna da 6.3.
- **O que evitar:** o halo laranja-avermelhado que se espalha pela cena. Ele cai na faixa proibida (4.2a, regra global de fogo) e exigiria bloom (8.7). Aqui o núcleo é branco-quente, a brasa é branco-âmbar (H 38 a 45°, S ≤ 50%) e o halo é um cartão aditivo local. Evitar também a cena de grupo narrativa: o ritual é silencioso e fica centrado no herói e no metal.

### 9.5 *Lawrence da Arábia* (1962, fotografia de Freddie Young)
- **O que tomar:** a miragem e o heat-haze só na linha do horizonte, como na entrada de Ali pelo poço, e o sol a pino com sombra curta e dura. Alimenta a 2.6 e o cartão de horizonte com distorção de vértice da 8.7.
- **O que evitar:** a areia ocre e laranja saturada do Technicolor, que fura o S ≤ 35% do cenário (4.2e) e se aproxima da 4.2a. Aqui a pedra é branqueada, sem esse laranja. Evitar a figura minúscula no plano aberto: o herói ocupa de 150 a 200 px (Seção 8), e a escala grandiosa vale só para corredores e fundo. Evitar a distorção de tela inteira (8.7) e a sombra densa sobre a área de combate (6.5).

### Fora da lista
Summoners War, Lords Mobile e Diablo 2 valem para o design (runas, forja, respec) e não para a arte. Os três marcam raridade por cor, o que viola a 3.5.

### Lacuna
Nenhuma referência cobre o VFX aliado. Isso inclui o fogo amarelo-branco ou roxo-azulado (4.2a) e o critério que separa o anel aliado do círculo da cura (pendência 7.9). Também falta referência para a linguagem de placa forjada da UI (Seção 7). Os jogos de origem resolvem os dois de jeitos que violam a 4.2a ou a 7. Uma referência dedicada entra quando a 7.9 for decidida.
