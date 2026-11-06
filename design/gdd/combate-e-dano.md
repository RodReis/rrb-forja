# Combate e dano (#6)

> **Status**: In Review (revisado em 2026-11-05 depois do MAJOR REVISION NEEDED: 6 decisões de jogo e os 8 bloqueios do log aplicados; aguarda re-review em sessão limpa)
> **Author**: Rodrigo Reis + agentes (game-designer, systems-designer)
> **Last Updated**: 2026-11-05
> **Last Verified**: 2026-11-05
> **Implements Pillar**: P4 *Massacre com peso* (a horda derrete, o elite bate forte, o golpe inimigo é legível) e P3 *Cada função é indispensável* (o Tank segura, o DPS causa dano focado)
> **Creative Director Review (CD-GDD-ALIGN)**: REVISED 2026-11-05 — CONCERNS 1 a 5 aplicados (o diretor não leu F1 a F4, os Edge Cases do auto-ataque em diante, Dependencies, Cross-References e AC-F/E/I/D/P: esse trecho não passou pelo gate)

## Summary

O Combate e dano (#6) é o conjunto de regras que, a cada tick da simulação, decide quem acerta quem, quanto dano sai, quem morre e como cada golpe empurra e trava o alvo: inclui o auto-ataque, os golpes marcados no chão dos elites e chefes, a esquiva no timing e o hit-stop. O jogador sente a horda que derrete, o elite que bate forte e o golpe que sempre dá para ler e evitar: "li o golpe, saí no último instante e devolvi com tudo". Existe porque sem ele não há derrota, vitória nem o peso do Pilar 4, e quase todo sistema de gameplay depende dele; roda dentro da simulação determinística e todo número vem do #1.

> **Quick reference** — Layer: `Core` · Priority: `MVP` · Key deps: `#1 Dados e balanceamento (Hard), #2 Simulação determinística (Hard), #4 Input e câmera de combate (Soft)`

## Overview

O Combate e dano (#6) é o conjunto de regras que decide, a cada tick da simulação, quem acerta quem, quanto dano sai, quem morre e como cada golpe empurra e trava o alvo. Ele é dono do dano e da vida de heróis, inimigos, elites e chefes; dos golpes marcados no chão que o jogador precisa ler (os telegraphs) e da janela de esquiva que os responde; do knockback e do hit-stop; e da morte, que é o ponto onde a vida chega a zero e a simulação avisa o resto do jogo. O jogador o vive de três jeitos: o herói ataca sozinho, enquanto o jogador move com um dedo, esquiva no último instante e dispara a suprema; a horda fraca derrete em massa; e um elite ou chefe pune um erro com um golpe que dói de verdade, mas que sempre foi possível ler e evitar. Sem o #6 não há derrota nem vitória, nem o peso dos golpes que sustenta o Pilar 4, e quase todo sistema de gameplay (#3, #7, #8, #10, #11, #12) depende dele.

O #6 roda dentro da simulação determinística (#2, ADR-0001): em float32, a 30 ticks por segundo, sem acesso a nada da engine, e toda regra que é número (dano, vida, tempos de telegraph, de esquiva, de hit-stop) vem dos dados do #1, nunca fixa no código. Ele **não** decide a composição das waves nem o que cada inimigo é (#7), o efeito de cada skill (#8), o XP e o fim da fase (#3), a leitura do toque (#4) nem a aparência e o som do impacto (#12): ele fornece a regra de dano e de vida que os outros usam. *(As fronteiras com o #8 e com o #7 são provisórias e fecham na Seção Detailed Design.)*

## Player Fantasy

**"Eu li o golpe, saí no último instante e devolvi com tudo."**

Um elite marca no chão, no meio da horda, uma área que vai doer. O jogador vê, espera, sai nos últimos instantes da janela, e a suprema acerta enquanto o elite ainda se recupera. A pose do herói e do alvo trava por um instante, a horda é arremessada para trás, e o elite fica aberto. É o momento que o #6 existe para entregar: a **Tensão** (um erro custa caro, e ninguém decide por você) e a **Descarga** (dezenas de inimigos caindo de uma vez) se encontram no mesmo gesto.

O peso é a forma de sentir esse momento, não uma promessa à parte: o golpe que o jogador devolve derruba e empurra, e o golpe que ele toma, quando erra, dói de verdade e pode acabar a fase. Como não há continue, esse custo pesa porque o erro foi dele: o golpe sempre foi possível ler e evitar. É a Core Fantasy do jogo em escala de segundos: *"cada skill foi conquistada"* vira *"cada esquiva foi conquistada"*.

**Pilar 4, *Massacre com peso*:** "Hordas derretem, elites batem forte, e o jogador sempre consegue ler o perigo." O *design test* ("entre mais efeitos na tela e golpe inimigo legível, escolhe o golpe legível") manda neste sistema: se um efeito atrapalha a leitura de um telegraph, o efeito perde.

**No Tank (Pilar 3, *o Tank segura*):** a mesma leitura vira "qual golpe aguentar e qual esquivar". Segurar não é imunidade à leitura: o Tank também precisa ler, só que escolhe ficar de pé onde o DPS sai. *(Provisório: a mitigação do Tank é definida em Detailed Design.)*

**O que esta fantasia promete:** todo golpe de elite e de chefe é legível e dura sempre o mesmo número de ticks, então a esquiva é uma habilidade que se aprende, não sorte, e **sair no último instante é premiado** (a recarga volta e o elite fica `Aberto`); os golpes pesados, os do jogador e os do elite, têm hit-stop e knockback; o dano se lê na hora.

**O que ela não promete:** que "nenhuma morte parece injusta" (o dano da horda sem telegraph e o acúmulo de contato não passam pela leitura); que "todo golpe tem hit-stop" (em massa ele mataria a Descarga, então tem orçamento); que "a esquiva perfeita anula qualquer dano" ou que "o Tank nunca precisa esquivar" (criariam requisitos de invulnerabilidade que o #6 não define e esvaziariam a Tensão).

*Tom da seção:* verbos físicos e curtos (ler, sair, devolver, aguentar, derrubar), sem vocabulário de estratégia nem de posicionamento.

## Detailed Design

### Core Rules

*(Tudo é provisório e a reavaliar. Os números são valores iniciais e knobs do #1, nunca fixos no código.)*

1. **Posição e dono dos campos.** O #6 é um `ISimSystem` que roda depois do #7 e do #8 e antes do #3. Ele só age com `CombatActive`, e todo tempo conta em `CombatTick`. Todo laço é por id crescente. **O #6 é o único escritor de posição e de HP**, de todas as entidades vivas. O #7 faz nascer (`Spawn`), declara os dados do arquétipo (velocidade, `xpValue`, ciclo de golpes) e, só no tick de entrada do chefe, enfileira o pedido `Rugido` (Regra 3). O #7 e o #8 não gravam HP: enfileiram pedidos.
2. **Passo do #6 em cada tick, nesta ordem.**
   1. Sem `CombatActive`, retorna sem tocar em nada, e as contagens regressivas congelam.
   2. Decrementa os timers: i-frames, recarga, cooldown de contato e fase do telegraph (o `r` do knockback **não** decrementa aqui: decrementa depois de aplicado, no passo 5). **Antes de qualquer início**, para que `I` i-frames valham `I` ticks (F6).
   3. Lê os comandos do herói. `Mover` vira velocidade de intenção. `Esquivar` válido (herói vivo e recarga zerada) inicia o dash com i-frames. Em recarga com `recarga ≤ buffer_esquiva_ticks` (inicial 3), o pedido fica guardado em `esquivaBuf` (1 só, no hash) e dispara neste passo no tick em que a recarga zera, com o eixo desse tick (Regra 8); com mais ticks restantes é ignorado, sem contar como rejeitado.
   4. Avança a máquina de ataque de cada inimigo (Regra 6).
   5. **Move todos.** Herói: intenção mais dash. Inimigo em Perseguindo: vai ao herói na velocidade do arquétipo. **Elite e chefe** *(emenda (i) do #7, 2026-11-05; provisória)* andam só até `dist_parada_m` do herói e nunca encaixam na posição dele: com `d²` = distância² até o herói no início do tick, se `d² ≤ dist_parada_m²` ficam parados; senão o passo é `min(passo, Sqrt(d²) − FATOR_PARADA × dist_parada_m)` na direção do herói. O alvo de 0,99 × `dist_parada_m` deixa uma margem de float32, e o #1 valida `0 < dist_parada_m ≤` o menor `alcance_inicio_aviso_m` do arquétipo, então quem parou está dentro do alcance da Regra 6. Há **dois alvos distintos**: o do movimento é a posição do herói no início do tick; o da trava do Aviso é a posição lida no tick de início do Aviso, sem deslocamento. A direção travada (cone ou linha) é `d/Sqrt(d²)`, ou (1,0) se `d² < 1e-6` (a regra `dir` da F3), então nunca é nula nem NaN. Em Aviso, Impacto e Recuperação a entidade não anda por conta própria (a única exceção é o deslocamento do golpe `linha` no Impacto, Regra 6). **Classe `Horda`** (`dist_parada_m` = 0) *(emenda (b) do #7, 2026-11-05; provisória; revista no spike, OQ-7)*: o alvo é a posição do herói no início do tick somada a `mira[id mod 32]`, um deslocamento de uma tabela fixa de 32 entradas (dado do #7 guardado pelo #1, sem sorteio; cada entrada com módulo ≤ `mira_offset_max_m` ≤ `alcance_contato_m`), para a horda não virar um bolo único sobre o herói. Se `dist² ≤ passo²` até o alvo, a posição vira exatamente o alvo, sem normalizar; senão avança `passo` na direção `d/Sqrt(d²)`. Parado no alvo, `dist²` = 0 e a posição se repete, então nunca há NaN nem tremor. O contato (Regra 5) mede a distância ao herói, não ao alvo de mira. Soma o knockback (`v_t` com o `r` atual), decrementa o `r` do knockback, limita à arena e grava a posição, então o 1º passo do knockback aplica `v0` inteiro (F3). O herói usa a posição do início do tick, o que é determinístico.
   6. **Coleta os pedidos de golpe**, nesta ordem contratual: os `Rugido` que o #7 enfileirou (só no tick de entrada do chefe, por id crescente do alvo), os que o #8 enfileirou (ordem de enfileiramento), os impactos de telegraph (por id do atacante), os contatos e o auto-ataque do herói.
   7. **Resolve em dois tempos.** (7a) soma o dano por alvo na ordem da fila, só para alvos vivos no início do passe; (7b) por id, `HP = max(0, HP − dano)`, e quem chega a 0 recebe `Kill` na mesma escrita.
   8. Aplica knockback e emite os eventos.
3. **Ponto único de dano:** `Combate.Aplicar(golpe)`, usado pelo #6, pelo #8 e, só para o `Rugido`, pelo #7, só enfileira. Na resolução: alvo morto é descartado; dano NaN, infinito ou negativo é descartado e contado (lança no modo estrito); i-frames ativos (lidos uma vez, no início de 7a, depois do passo 3, então o dash iniciado neste tick já vale) descartam o golpe e emitem `Esquiva` uma vez por tick e por herói, **só se o descartado era telegraph**; senão `dano = base × modDano × (1 − mitigação) × punição` (F1), com punição só se o alvo está em Recuperação (Regra 6: `mult_punicao`, 1º golpe `pesado` e `Aberto`). `mit` NaN é erro interno (exceção nos dois modos): descartar o golpe deixaria o herói imortal. **Dois tempos relaxam a Regra 7 do #2** (a morte só vale em 7b): é o que permite herói e chefe morrerem no mesmo tick, com a vitória valendo (Regra 13 do #3). *O #2 precisa de uma nota.*
   **Pedido `Rugido`** *(emenda (c) do #7, 2026-11-05; provisória)*. É um pedido **tipado e sem valor de dano** (nunca `float.MaxValue`, que viraria infinito com os multiplicadores). Só o #7 o origina, uma vez por fase, no tick de entrada do chefe, um por entidade viva de classe `Horda` ou `Elite` (nunca o herói nem o `Essencial`), e ele entra **na frente da fila**. **Pula a F1 e a mitigação**: sem `base`, `modDano`, `mit` nem punição, e sem clamp de `DANO_MAX`, então `GolpesLimitados` não conta. Em 7b zera o HP do alvo e chama `Kill(id, Rugido)`, com `dano_aplicado` = HP. Alvo morto no início do passe é descartado como qualquer pedido. Não emite `Damage`, não dá knockback nem `HitStop`. **A causa da morte é a do primeiro pedido da fila que zera o HP**; como o `Rugido` está na frente, todo alvo do rugido sai com causa `Rugido`, inclusive o corpo que o auto-ataque do herói mataria no mesmo passe. `Rugido` é valor novo de `DeathCause` *(emenda pendente ao ADR-0001 e ao #2)*.
4. **Auto-ataque (do #6).** Alvo *(decisão do autor, 2026-11-05)*: primeiro o elite ou chefe vivo em Recuperação (inclui `Aberto`) dentro do alcance; se não há, o hostil vivo mais próximo dentro do alcance. Em cada grupo vale a menor distância ao quadrado e, no empate, o menor id. O campo `pesado` do golpe vem do dado do herói (#10). Cadência em ticks inteiros do dado, multiplicada por `modCadencia` (que **multiplica o intervalo**: menor que 1 é mais rápido; o #8 escreve `1/(1+Σbônus)`, F4) e com dano base × `modDano`, os dois escalares escritos pelo #8. Sem alvo não gasta cadência. Movimento e esquiva continuam manuais, então não é auto-battle.
5. **Contato da horda** *(decisão do autor, 2026-11-05).* Cada inimigo de classe `Horda` **em contato** (`dist² ≤ alcance_contato_m²` até o herói, com as posições gravadas no passo 5 do tick anterior) bate a cada `cad_contato_ticks` (inicial 15). O herói recebe no máximo **1 golpe de contato a cada 6 ticks** (menor id entre os prontos; o tick do último fica na coluna `ultimoContatoTick` do herói, no hash). Os i-frames da esquiva anulam o contato. Nenhuma entidade bloqueia o corpo de outra: **a horda pode se sobrepor no MVP**, a rever depois do spike de performance. **Elite e chefe não causam dano por contato** *(emenda (h) do #7, 2026-11-05; provisória)*: o contato só existe na classe `Horda`. O dado de elite e de chefe não tem `dano_contato` (o #1 recusa o campo). Elite ou chefe sobreposto ao herói, ou parado em `dist_parada_m` dentro de `alcance_contato_m`, não bate, não gasta cooldown e não conta em `n_c` (F7); eles só batem com golpe telegrafado (Regra 6).
6. **Telegraph (elite e chefe).** Ciclo: Perseguindo → **Aviso** `A` → **Impacto** (1 tick) → **Recuperação** `P` → Perseguindo, onde a **recarga de ataque** `g` (dado do #7, em ticks; 0 se o arquétipo não declara) conta a partir do fim da Recuperação e o próximo Aviso só começa com ela cumprida. Valores iniciais: elite A = 24 e P = 30; chefe A = 36 e P = 36 ticks; **24 e 36 são o aviso mínimo por golpe, não o padrão**: golpe de área maior pede `A` maior, validado pelo #1 (F5). A **área trava no início do Aviso** e não segue o herói. O Aviso gravado no tick T tem o Impacto em T+A. O teste de acerto é um só, no tick do Impacto (círculo ou cone, distância ao quadrado, ordem de id). Morte do atacante cancela o golpe. Nenhum knockback ou interrupção altera as fases (nunca prorroga nem reinicia), e há `poise_ticks` de imunidade a knockback (nunca a dano) depois da Recuperação. **Janela de punição** *(decisão do autor, 2026-11-05)*: em Recuperação o alvo leva `mult_punicao` (inicial ×1,5); o **1º golpe `pesado`** que o acerta nela leva `mult_punicao_pesado` (inicial ×2,0; coluna `punidoPesado` do atacante, no hash, zerada ao fim da Recuperação; vale o primeiro da fila no passe); e, se a Recuperação está **`Aberto`** (Regra 8), todo golpe leva `mult_punicao_aberto` (inicial ×2,0). Os multiplicadores **não se multiplicam**: vale o que se aplica, nunca o produto. A Recuperação tem ≥ 6 ticks abertos. **Regra de leitura:** `A ≥ reação (~8) + ticks para sair da área + janela (≥ 5)`, validada pelo #1 por golpe. O chefe segue um ciclo fixo de golpes dos dados, **sem sorteio**. No máximo **3 avisos simultâneos**: o seguinte espera, por id. Um Aviso novo só começa se o seu Impacto ficar a pelo menos `GAP_IMPACTO` ticks (inicial 9) de outro Impacto em área que alcance o herói (F10), para o dano nunca somar sem leitura *(decisão do autor, 2026-11-05)*. **Vez do chefe** *(re-revisão, a reavaliar)*: o chefe pronto tem prioridade no slot (ordem: chefe, depois menor `prontoDesde`, depois menor id), e enquanto ele só espera o GAP nenhum elite inicia Aviso novo; assim o GAP nunca deixa o chefe sem vez. **Alcance de início do Aviso** *(emenda (e) do #7, 2026-11-05; provisória)*: cada golpe do ciclo de elite e de chefe declara `alcance_inicio_aviso_m` (dado do #7; o #1 o limita à área visível, F10 do #7). A passagem Perseguindo → Aviso do próximo golpe do ciclo só vale com `dist² ≤ alcance_inicio_aviso_m²` (inclusivo), com a `dist²` entre o atacante e o herói nas posições do início do tick (gravadas no passo 5 do tick anterior, porque o passo 4 vem antes do movimento). Fora do alcance a entidade segue em Perseguindo e o ciclo não pula golpe. Depois que o Aviso começa, o herói sair do alcance não muda nada: a área já está travada. **Golpe com deslocamento, a forma `linha`** *(emenda (g) do #7, 2026-11-05; provisória)*: além de `circulo` e `cone`, o golpe de elite e de chefe pode ter `forma = linha` (a investida do Campeão), com `desloc_m` (deslocamento) e `raio_golpe` (meia largura). **Trava no início do Aviso:** `P0` = posição do atacante, `dir` pela regra `dir` da F3 e `P1 = P0 + dir × desloc_m`, com `P1` limitado à arena por eixo já na trava, para a linha desenhada no chão ser a que vale; comprimento² < 1e-6 (atacante colado na parede de frente) vira um círculo em `P0`. **Impacto (1 tick):** no passo 5 o atacante termina em `P1`, sem teleporte (o `prev` fica, e o #12 desenha um deslize de 1 tick), e no passo 6 o teste de acerto é um só, `dist²(herói, segmento P0→P1) ≤ raio_golpe²`, com a projeção limitada a [0, 1] e a posição do herói após o passo 5, como nos outros golpes. O knockback do herói tem a direção `dir` da linha. Nenhum corpo bloqueia o deslocamento (Regra 5), e empurrar o atacante durante o Aviso não muda a linha travada nem o destino. A F5 e a F10 tratam a linha como área (`raio_golpe` é a meia largura), e a F8 mede a distância ao segmento travado.
7. **Nascimento e graça de ataque.** O #6 pula toda entidade que nasceu neste `CombatTick`. Vale para todo `Essencial`: o primeiro ataque do chefe nunca vale no tick em que ele nasce. **Graça de ataque** *(emenda (a) do #7, 2026-11-05; provisória)*: o arquétipo de elite e de chefe declara `graca_ataque_ticks` (dado do #7, ilustr. elite 30 e chefe 60; vale 0 se o arquétipo não declara), e a passagem Perseguindo → Aviso só vale com `CombatTick ≥ tickNascimento + graca_ataque_ticks`. Durante a graça a entidade anda, é alvo e pode morrer; só não inicia Aviso, para o jogador vê-la antes de apanhar. A condição continua verdadeira depois que passa, então vale em toda passagem sem estado novo (usa só a coluna `tickNascimento`, já no hash). **Estar pronto para o slot do Aviso inclui a graça**: `prontoDesde` nunca fica antes de `tickNascimento + graca_ataque_ticks`. Com graça 0, vale só a regra do tick de nascimento.
8. **Esquiva.** Direção: o eixo atual, ou a última direção não nula. Dá `I` ticks de i-frames (inicial 9; o #1 valida `I ≥ 7`) junto com um dash, e recarga `R > I` (inicial 60). I-frames nunca somam (vale o maior restante). *(Anula também o contato da horda, decisão do autor.)* **Buffer** *(re-revisão, a reavaliar)*: um `Esquivar` com `recarga ≤ buffer_esquiva_ticks` (inicial 3) fica guardado (1 pedido, coluna `esquivaBuf` no hash) e inicia o dash no tick em que a recarga zera, com o eixo desse tick; com mais ticks restantes é ignorado. **Esquiva no limite** *(decisão do autor, 2026-11-05)*: se os i-frames negam o Impacto de um telegraph de elite ou chefe e `I − iframes ≤ lim_esquiva_ticks` (inicial 3: o toque veio nos últimos ticks antes do Impacto), **a recarga zera** (reembolso, no máximo 1 por Impacto) e o atacante fica **`Aberto`** (coluna `aberto`, no hash) até o fim daquela Recuperação.
9. **Knockback.** Deslocamento total `D` em `K` ticks (inicial 4), decaindo linear, na direção fonte → alvo (vetor nulo usa `EIXOS8[id mod 8]`, uma tabela constante de 8 direções unitárias, para a horda sobreposta não ir toda para +x). Dois knockbacks não somam: vence o novo se `v0_novo > |v_atual|` (F3), com empate para o 1º da fila. A resistência do alvo (0 a 1) vem do dado. Sempre dentro da arena. O `Essencial` tem `resist_knockback = 1`, e o elite fica `kb_refrat_ticks` (inicial 30) imune a novo knockback depois de sofrer um, contado do tick em que o knockback foi aceito (Edge Cases).
10. **Hit-stop é só apresentação.** A simulação nunca congela e o telegraph nunca congela. O #6 emite o evento `HitStop` (3 ticks de apresentação) apenas para golpe pesado (campo booleano `pesado` no dado do golpe, validado pelo #1) do herói em elite ou chefe, para a suprema e para golpe com telegraph sofrido pelo herói (**nunca contato**, F8), com orçamento de **1 a cada `N` ticks** (inicial 10, contador no `Hash` do #6; no máximo 3 por segundo, o limite de flashes da art bible). Fica suprimido se há telegraph com ≤ 12 ticks até o dano perto do herói. O campo `pesado` também decide a punição ×2,0 da Recuperação (Regra 6): o golpe que trava a mão é o que pune.
11. **Morte.** A morte é só `Kill(id, causa)`. O herói morrendo encerra a tentativa, sem continue nem revive. O #6 não dá XP nem loot: a lista de mortos é o `DeathsThisTick` do `SimWorld`, o #3 lê o id e a causa ali e o `xpValue` na linha do id. A causa pode ser `Rugido` (Regra 3): o #6 só a carimba, e o que ela vale (metade do XP, sem efeito de abate, sem loot) é do #3, do #8 e do #24. Valor inválido segue a Regra 9 do #2.
12. **Mitigação do Tank**, sem subsistema novo: três campos no dado do herói, `mit_contato` e `mit_golpe` (reduções de 0 a `MIT_MAX < 1`) e `resist_knockback`. O Tank segura a horda barato: o DPS aguenta 2 golpes de elite e o Tank 3, e nenhum morre em 1 com a vida cheia (F9, *decisão do autor, 2026-11-05*); ele continua tendo de ler (Player Fantasy).
13. **Dano contínuo** do #8 usa a taxa por tick (F2 do #1). **O #6 nunca afirma que 30 ticks somam exatamente a taxa.**
14. **Eventos para o #12.** Individuais só para herói, elite e chefe (`Damage`, `Esquiva`, `Knockback`, `HitStop`, `Morte`); a horda sai agregada por tick (`{mortes, acertos, danoTotal}`, só se algum valor for maior que 0), nunca um evento por acerto ou morte. Mortes por `Rugido` somam em `mortes` (o elite sai no `Morte` individual); `acertos` e `danoTotal` contam só pedidos com valor, nunca o rugido. **O #12 desenha o telegraph lendo as colunas do #6** (fase, ticks até o dano, forma, raio, origem e, na `linha`, destino), não os eventos, para que um descarte nunca esconda o aviso.
15. **Cura** *(decisão do autor, 2026-11-05).* `Combate.Curar(alvo, valor)` é o ponto único de cura e, como `Aplicar`, só enfileira. Fonte no MVP: o level-up, em que o #3 pede `cura_levelup_pct × hpMax` do herói (o #3 roda depois do #6: o pedido dele soma na coluna `curaPendente` do herói, no hash e limitada a `hpMax`, e entra em 7b do próximo tick com `CombatActive`, então sobrevive à oferta de carta sem fila fora do hash); o #8 pode usar o mesmo ponto em skills futuras. Em 7b a cura soma antes do dano (F2), é limitada a `hpMax`, nunca reanima (só vale para alvo vivo no início do passe) e não passa pela mitigação. Valor NaN, infinito ou negativo é descartado e contado (`CurasDescartadas`).
16. **Oferta de carta** *(decisão do autor, 2026-11-05; substitui a espera por `AvisoPerto`).* O #16 abre a oferta na hora do level-up (`CombatHold` = 1) e o combate congela por inteiro (Regra 2.1), com Aviso, Impacto e Recuperação no valor exato. Ao escolher a carta, o #16 mostra uma **contagem 3-2-1** ainda sob `CombatHold` (≥ 19 ticks; a duração é do #16) e só então solta o combate. O #6 não guarda estado de oferta nem expõe predicado para ela: o jogador relê a tela antes de o tempo andar, e o Impacto que estava marcado cai com os mesmos ticks restantes (E3). Cura e dano pedidos no tick do level-up seguem a Regra 15.

### States and Transitions

| Entidade | Estado | Vai para | Quando |
|---|---|---|---|
| Inimigo atacante (elite, chefe) | Perseguindo | Aviso | `dist² ≤ alcance_inicio_aviso_m²` do golpe da vez (Regra 6), recarga pronta e `CombatTick ≥ tickNascimento + graca_ataque_ticks` (Regra 7; com graça 0, só não é o tick do nascimento) |
| | Aviso | Impacto | `A` ticks cumpridos (cancela se o atacante morre) |
| | Impacto | Recuperação | 1 tick |
| | Recuperação | Perseguindo | `P` ticks cumpridos |
| | Recuperação | Recuperação `Aberto` | esquiva no limite negou o Impacto (Regra 8); a marca dura até o fim daquela Recuperação |
| Horda comum | Perseguindo | Golpe (1 tick) | em contato e recarga pronta |
| | Golpe | Recarga | 1 tick |
| | Recarga | Perseguindo | `cad_contato_ticks` cumpridos |
| Elite, chefe | qualquer | n/a | sem estado nem golpe de contato (Regra 5); só o telegraph da Regra 6 |
| Herói | Livre | Esquivando | `Esquivar` válido |
| | Esquivando | Livre | `I` ticks cumpridos |
| Qualquer | Vivo | Morto | HP chega a 0 em 7b |

### Interactions with Other Systems

| Sistema | Entra no #6 | Sai do #6 | Dono da interface |
|---|---|---|---|
| #1 Dados | dano, cadências, A, P, `I`, `R`, mitigações, orçamentos | validação de `I ≥ 7`, `R > I` e `A` pela regra de leitura | #1 valida |
| #2 Simulação | ordem, `Kill`, `DeathsThisTick`, comandos, eventos | `Death` com causa; nota na Regra 7 | #2 |
| #3 Fluxo de fase | `tickNascimento`; pedido `Curar` no level-up | morte do herói e dos inimigos | #3 lê e pede a cura |
| #4 Input | `Mover`, `Esquivar`, `Suprema` | nada | #4 |
| #7 Horda | `Spawn`, velocidade, `xpValue`, ciclo de golpes do arquétipo (com `alcance_inicio_aviso_m` por golpe; forma `circulo`, `cone` ou `linha`, esta com `desloc_m`), `dist_parada_m` (elite e chefe), tabela de mira da `Horda` (32 entradas), pedido `Rugido` (tipado, uma vez por fase) | estado de ataque (leitura) | #7 declara |
| #8 Skills | pedidos de dano, `modDano`, `modCadencia`, a suprema | resultado dos golpes | #8 |
| #10 Funções | mitigação do Tank | nada | #10 |
| #12 Feedback | colunas e eventos | nada | #12 |
| #16 Oferta do Grimório | nada | nada: o #16 abre a oferta na hora sob `CombatHold` e é dono da contagem 3-2-1 (Regra 16) | #16 |

**Vira ADR (colunas do `SimWorld`, #6 e #7):** colunas hasheadas `hpMax`, `estadoCombate`, `timerTicks`, `iframes`, `contactCd`, `kbVel`, `intentVel`, `classe`, `arquetipoId`, `tickNascimento`, `aberto`, `punidoPesado`, `esquivaBuf`, `curaPendente`, `ultimoContatoTick`, e a área travada do telegraph (origem, direção, raio e, na `linha`, destino); scratch fora do hash (fila de golpes, dano acumulado); #6 como escritor único de posição e HP; capacidades da fila de golpes e de eventos validadas pelo #1.

## Formulas

**Convenções:** float32 na ordem escrita, sem FMA. Ticks são `int`. Floor de valor ≥ 0 é `(int)(x + 0,5f)`, o mesmo meio-tick para cima do F1 do #1. **Todo número de exemplo é ILUSTRATIVO**, porque o #1 ainda não tem dados de arquétipo. Os nomes de knob em MAIÚSCULAS são novos e entram no registro depois de aprovados.

### F1. dano_final

The dano_final formula is defined as:

```
ok         = base ≥ 0 && base ≤ FLOAT_MAX && modDano ≥ 1 && modDano ≤ MODDANO_MAX   // NaN e infinito falham
mit_ef     = clamp(mit, 0, MIT_MAX)        // mit NaN: exceção nos dois modos (bug interno; descartar deixaria o herói imortal)
punicao    = !emRecuperacao ? 1f : aberto ? mult_punicao_aberto : (pesado && !punidoPesado) ? mult_punicao_pesado : mult_punicao   // não se multiplicam
dano       = base * modDano * (1f - mit_ef) * punicao
dano_final = ok ? min(dano, DANO_MAX) : DESCARTE   // descarte e clamp são contados
modDano    = 1 + Σ bonus_i                                                // bônus aditivos escritos pelo #8
```

**Variables:**
| Variable | Type | Range | Source | Description |
|---|---|---|---|---|
| base | float | 0 a `DANO_MAX` | data file | dano base do golpe |
| bonus_i | float | ≥ 0 (sem negativo no MVP) | data file (#8) | bônus aditivo |
| modDano | float | 1 a `MODDANO_MAX` (ilustr. 10) | calculated | escalar escrito pelo #8; o piso é 1 porque `modDano = 1 + Σ bonus_i` e `bonus_i ≥ 0` |
| mit | float | 0 a `MIT_MAX` < 1 (ilustr. 0,6) | data file | `mit_contato` ou `mit_golpe` do alvo, conforme o golpe |
| mult_punicao | float | 1 a 3 (inicial 1,5) | data file | só se o alvo está em Recuperação |
| mult_punicao_pesado | float | `mult_punicao` a 3 (inicial 2,0) | data file | 1º golpe `pesado` em alvo em Recuperação (`punidoPesado` falso) |
| mult_punicao_aberto | float | `mult_punicao` a 3 (inicial 2,0) | data file | todo golpe numa Recuperação `Aberto` (esquiva no limite) |
| DANO_MAX | float | ≥ maior dano legítimo × bônus × punição, e ≤ 1e6 | data file | teto de saneamento |

**Output Range:** de 0 a `DANO_MAX`. Com `base > 0` o resultado é `> 0`, pois `1 − MIT_MAX > 0`. Dano acima de `DANO_MAX` é clamp contado (`GolpesLimitados`), nunca silencioso; entrada inválida (NaN, infinito, negativo, `modDano` fora da faixa) é descarte contado (`GolpesDescartados`).
**Example (ilustrativo):** o herói acerta um elite em Recuperação com base 12 e bônus 0,25 e 0,10: 12 × 1,35 × 1,5 = **24,3** (golpe comum); o 1º golpe `pesado` na mesma Recuperação: 12 × 1,35 × 2,0 = **32,4**; numa Recuperação `Aberto`, qualquer golpe: **32,4** (nunca o produto). Elite contra o Tank (mit_golpe 0,4): 80 × 0,6 = **48**.

### F2. hp_resolucao

The hp_resolucao formula is defined as:

```
// 7a, por alvo, na ordem da fila, só entradas com vivoNoInicio[alvo] e sem i-frames (lidos uma vez, no início de 7a, depois do passo 3)
acc[alvo] += dano_final_k;   curaAcc[alvo] += cura_k      // cura só para vivo no início do passe
// 7b, por id crescente
base = min(HPmax, HP + curaAcc)                              // a cura soma antes do dano e nunca passa de HPmax
HP' = (base - acc < HP_RESIDUO) ? 0f : base - acc;   morreu = (HP' == 0f);   dano_aplicado = base - HP'
causa = primeira entrada k da fila cuja soma corrente leva base − soma abaixo de HP_RESIDUO
// pedido Rugido (tipado, Regra 3): marca rugido[alvo] em 7a, sem acc; em 7b HP' = 0, morreu = true, dano_aplicado = HP, causa = Rugido (está na frente da fila)
```

**Variables:**
| Variable | Type | Range | Source | Description |
|---|---|---|---|---|
| HP | float | (0, `HP_MAX_FAIXA`] (ilustr. ≤ 1e5) | calculated (coluna) | vida no início do passe |
| HPmax | float | > 0 | data file (#1, #7 e #10) / coluna `hpMax` | vida máxima da entidade (herói, elite, chefe e horda) |
| curaAcc | float | 0 a `HPmax` por pedido | calculated | cura somada por alvo (scratch fora do hash) mais a coluna `curaPendente` (no hash; a do #3 no level-up vale `cura_levelup_pct × HPmax`) |
| acc | float | 0 a capFila × `DANO_MAX` | calculated | soma por alvo (scratch fora do hash) |
| HP' | float | 0 a `HPmax` | calculated | vida gravada |
| HP_RESIDUO | float | 0 < r ≤ 0,1 (inicial 0,01) | data file | abaixo disto a vida vira 0 e a entidade morre, para nunca existir "vivo com 0,00001" |

**Output Range:** `[0, HPmax]` (HP' ≤ base ≤ HPmax; sem cura, HP' ≤ HP). A cura (Regra 15) soma antes do dano e é limitada a `HPmax`; ela nunca reanima e não passa pela mitigação. Herói e chefe com `acc ≥ HP` morrem no mesmo tick, e o #3 aplica a Regra 13. A soma float depende da ordem, por isso **a ordem da fila é contratual**. O `Rugido` do #7 não soma em `acc`: zera o HP sozinho e, na frente da fila, fixa a causa. Regra para o #1: `dano_efetivo_mín ≫ HPmax × 2⁻²³`.
**Example (ilustrativo):** o herói com HP 30 leva 20 (elite) e 15 (contato) no mesmo passe: acc = 35, HP' = 0, causa = o 2º golpe, dano_aplicado = 30. Com cura: HP 30, HPmax 100, cura 20 e dano 35 → base 50, HP' 15.

### F3. knockback

The knockback formula is defined as:

```
D_ef = D * (1f - resist)                 // resist 0..1 (1 = imune: descarta)
v0   = 2f * D_ef / (K + 1)               // 1º tick aplica v0
v_t  = v0 * dir_kb * (r / (float)K)         // r = ticks restantes, K..1
dir  = d / Sqrt(dx² + dy²), ou (1,0) se dx² + dy² < 1e-6      // Aviso e investida
dir_kb = d / Sqrt(dx² + dy²), ou EIXOS8[id_alvo mod 8] se dx² + dy² < 1e-6   // só o knockback
vence = v0_novo > |v_atual|              // estrito; o 1º da fila vence o empate; o vencedor reinicia com r = K
pos' = clampArena(pos + move + kb)       // por eixo, com o raio da entidade; desliza ao longo da parede
```

**Variables:**
| Variable | Type | Range | Source | Description |
|---|---|---|---|---|
| D | float | 0 a `D_MAX` (ilustr. 3 m) | data file | deslocamento total |
| K | int | 1 a 8 (inicial 4) | data file (`_ticks`) | duração |
| resist | float | 0 a 1 | data file | `resist_knockback` |
| v0 | float | 0 a `D_MAX` | calculated | velocidade inicial, m/tick |

**Output Range:** o deslocamento é `D_ef`, pois Σ(K−t)/K = (K+1)/2. Com K = 4, v0 = 0,4·D_ef; com K = 1, v0 = D_ef (sem divisão por zero). Perde-se o que passar da parede. *(A arena como retângulo alinhado aos eixos é suposição: confirmar.)*
**Example (ilustrativo):** D = 1 m, K = 4, resist 0,5 → D_ef 0,5, v0 = 0,2; passos 0,2 / 0,15 / 0,10 / 0,05 = **0,5 m**.

### F4. cadencia_efetiva

The cadencia_efetiva formula is defined as:

```
x           = cad_ticks * modCadencia      // 1 multiplicação em float32
cad_efetiva = max(1, (int)(x + 0.5f))      // meio tick para cima
```

**Variables:**
| Variable | Type | Range | Source | Description |
|---|---|---|---|---|
| cad_ticks | int | ≥ 1 | data file (`_ticks`) | intervalo base |
| modCadencia | float | `MOD_CAD_MIN` (ilustr. 0,25) a `MOD_CAD_MAX` (ilustr. 2) | calculated (#8) | **multiplica o intervalo**: menor que 1 é mais rápido |
| cad_efetiva | int | 1 a `cad_ticks × MOD_CAD_MAX` | calculated | intervalo usado |

**Output Range:** ≥ 1. O #1 exige `cad_ticks × MOD_CAD_MIN ≥ ~3` (1 tick seria 30 ataques por segundo). O novo valor vale na próxima recarga. Sem alvo, o timer fica pronto. O #8 deve escrever `modCadencia` como `1/(1+Σbônus)`, nunca como "+20% de velocidade".
**Example (ilustrativo):** cad 15, mod 0,75 → 11,25 → **11**. Mod `0.7f` (literal float32) → 10,5 → **11**.

### F5. aviso_minimo

The aviso_minimo formula is defined as:

```
ticks_para_sair = ceil((raio_golpe + margem) / vel_heroi_min_tick)   // decimal, no build
A ≥ REACAO + ticks_para_sair + JANELA
raio_max = (A − REACAO − JANELA) × vel_heroi_min_tick − margem
```

**Variables:**
| Variable | Type | Range | Source | Description |
|---|---|---|---|---|
| raio_golpe | decimal | > 0 | data file | raio do círculo, alcance do cone ou meia largura da linha |
| margem | decimal | 0,2 a 0,5 m (ilustr. 0,3) | data file | folga do corpo |
| vel_heroi_min_tick | decimal | > 0 (ilustr. 0,15) | data file | do herói mais lento, com a lentidão máxima possível |
| REACAO / JANELA | int | 8 / ≥ 5 | constant (GDD #6; o piso de 5 da janela vem do #2; no registro como `reacao_ticks` e `janela_ticks`) | reação e folga |
| A | int | ≥ 1 | data file | Aviso em ticks |

**Output Range:** `ticks_para_sair ≥ 1`. A conta é em `decimal` (em float, 1,65/0,15 dá 11,0000001 e o `ceil` erra). Pior caso: o herói no centro da área. **24 e 36 são o aviso mínimo por golpe, não o padrão:** golpe de área maior pede `A` maior, validado por golpe.
**Example (ilustrativo):** elite A = 24: folga de 11 ticks, raio + margem ≤ **1,65 m** (raio ≤ 1,35). Chefe A = 36: folga de 23, ≤ **3,45 m** (raio ≤ 3,15) com 0,15 m/tick. **Com o Tank a 0,12 m/tick (o herói mais lento, que a regra usa):** o elite cai para 1,32 m (raio ≤ 1,02) e o chefe para **2,76 m** (raio ≤ 2,46); um raio de 3,15 dá 29 ticks para sair e exige A ≥ 42.

### F6. esquiva_coerente

The esquiva_coerente formula is defined as:

```
I ≥ 7;  R ≥ 3 × I   // o piso absoluto R > I só vale para a redução de recarga do #8
v_dash    = Ddash / I                            // m/tick durante I ticks (decimal, no build)
saiDaArea ⇔ Ddash ≥ raio_golpe_max + margem      // só o dash, sem contar a intenção
cobertura = Impacto dentro dos I ticks de i-frames
```

**Variables:**
| Variable | Type | Range | Source | Description |
|---|---|---|---|---|
| I | int | 7 a 15 (inicial 9) | data file | i-frames e duração do dash |
| R | int | 3×I a 120 (inicial 60); o piso absoluto I+1 só vale para a redução de recarga do #8 | data file | recarga, contada do início do dash; zera com a esquiva no limite (Regra 8) |
| Ddash | float | 2× a 4× (I × vel_heroi) (ilustr. 2,7 m) | data file | deslocamento total |
| v_dash | float | > vel_heroi | calculated | com I = 9, 0,3 m/tick (9 m/s) |

**Output Range:** com Impacto de 1 tick, a segurança vem do timing (janela de 9 ticks ≈ 300 ms); o deslocamento garante a saída quando o toque é cedo demais. Com Ddash = 2,7 o elite (≤ 1,65) é coberto; o chefe (3,15 + 0,3) **não**: ali valem o timing e a caminhada (F5). O ciclo do elite (A + 1 + P = 55) é menor que R (60), então a caminhada tem de bastar sozinha. **Os timers são decrementados antes de qualquer início** (Regra 2), senão `I` valeria `I − 1` ticks. **Reembolso** (Regra 8): a esquiva no limite zera a recarga, no máximo 1 vez por Impacto e só ao negar telegraph de elite ou chefe; com 3 elites em ciclo de 55 ticks são no máximo 3 reembolsos a cada 55, cobertura ≈ 3 × 9 / 55 ≈ 49% (o sinal S3 mede).
**Example (ilustrativo):** toque 3 ticks antes do Impacto → 9 ticks de i-frames cobrem o tick do Impacto.

### F7. contato_maximo

The contato_maximo formula is defined as:

```
taxa_golpes_tick = min(1/contato_gap_ticks, n_c / cad_contato_ticks)     // n_c = inimigos de classe Horda em contato; contato_gap_ticks inicial 6
d_c              = dano_contato_max × (1 − mit_contato)
dps_contato_max  = (ticks_per_second / contato_gap_ticks) × d_c   // inicial 30/6 × d_c = 5 × d_c; saturado com n_c ≥ ceil(cad_contato_ticks / contato_gap_ticks) = 3
n                = menor n com n × d_c ≥ HP               // laço float32 de subtração
t_morte_min      = contato_gap_ticks × (n − 1) ticks
condição do #1:  t_morte_min ≥ X  ⇔  d_c < HP / ceil(X / contato_gap_ticks)
```

**Variables:**
| Variable | Type | Range | Source | Description |
|---|---|---|---|---|
| dano_contato_max | float | > 0 | data file (#7) | maior `dano_contato` entre os arquétipos de classe `Horda` da fase (elite e chefe não têm contato, Regra 5) |
| mit_contato | float | 0 a `MIT_MAX` | data file | do Tank |
| contato_gap_ticks | int | 1 a `cad_contato_ticks` (inicial 6) | data file | ticks mínimos entre dois golpes de contato no herói |
| HP | float | > 0 | data file | vida do herói |
| X | int | 240 (decisão do autor, 2026-11-05) | data file | piso de tempo para morrer só por contato, sem esquiva |

**Output Range:** dps constante, independente do tamanho da horda (limite superior conservador). Com esquiva a taxa cai no máximo `I/R` = 15%. Com X = 240, **o contato por golpe tem de ser menor que HP/40**.
**Example (ilustrativo):** HP 100, contato 2,4: n = 42, **246 ticks** (8,2 s), passa. Contato 4: n = 25, 144 ticks, **reprovado** pelo #1. Tank (mit 0,4) permite contato até ~4,16.

### F8. orcamento_hitstop

The orcamento_hitstop formula is defined as:

```
suprimido = ∃ aviso: 1 ≤ ticks_ate_dano ≤ HS_SUPR && dist²(heroi, origem) ≤ (raio_golpe + margem_supr)²
emitir    = elegivel && !suprimido && CombatTick ≥ proximoHitStopTick
se emitir: proximoHitStopTick = CombatTick + N      // fica no Hash; suprimido NÃO consome orçamento
```

**Variables:**
| Variable | Type | Range | Source | Description |
|---|---|---|---|---|
| N | int | ≥ H (inicial 10) | data file | espaço mínimo entre eventos |
| H | int | 1 a 5 (inicial 3) | data file | duração de apresentação |
| HS_SUPR | int | ≥ H + REACAO (inicial 12) | data file | janela de supressão |
| margem_supr | float | ilustr. 1,8 m | data file | "perto do herói" |
| elegivel | bool | | calculated | golpe pesado do herói em elite ou chefe, suprema, ou **golpe com telegraph sofrido pelo herói (nunca contato)** |

**Output Range:** no máximo 30/N = **3 eventos por segundo** (o limite de flashes da art bible), e a apresentação ocupa H/N = 30% do tempo. Um evento por tick; empate por prioridade (sofrido > suprema > pesado), depois id. O descartado não vira fila.
**Example:** eventos nos ticks 100 e 110 (`proximoHitStopTick` = 120). No tick 120, um elegível com Aviso a 10 ticks do dano e o herói a 1 m é suprimido, e o contador continua em 120; no 121, sem aviso perto, o evento sai e o contador vai a 131.

### F9. folga_de_golpes (golpes com telegraph de elite e de chefe que cada herói aguenta)

The folga_de_golpes formula is defined as:

```
d_ef  = base_elite × (1 − mit_golpe)
n     = ceil(HP / d_ef)
ttk_ticks = A + (n − 1) × (A + 1 + P + g)          // g = ticks em Perseguindo entre ciclos
exigência (decisão do autor, 2026-11-05):  n_DPS = 2  e  n_Tank = 3     // vale para todo golpe com telegraph de elite e de chefe; nenhum morre em 1 golpe com a vida cheia
n = 2 ⇔ HP/2 × 1,01 ≤ d_ef < HP × 0,99        n = 3 ⇔ HP/3 × 1,01 ≤ d_ef < HP/2 × 0,99     // 1% de margem float nos dois lados: nunca morre em n−1
ttk_multi = A + (n − 1) × GAP_IMPACTO          // n elites alternando: o pior caso real, informativo (ttk acima é de 1 atacante)
```

**Variables:**
| Variable | Type | Range | Source | Description |
|---|---|---|---|---|
| base_elite | float | > 0 | data file (#7) | dano do golpe |
| HP, mit_golpe, mit_golpe_chefe | float | > 0; 0 a `MIT_MAX` | data file | do herói da função (`mit_golpe_chefe` omitido = `mit_golpe`) |
| A, P | int | 24, 30 (iniciais) | data file | fases do ciclo |
| g | int | ≥ 0 | data file | recarga de ataque do elite |

**Output Range:** `n ≥ 1`. Com g = 0, A = 24 e P = 30: DPS (n = 2) → **79 ticks** (2,6 s); Tank (n = 3) → **134 ticks** (4,5 s). O #1 valida os dois intervalos para cada herói da fase. Esses `ttk` valem para **1 atacante**. Com 3 elites alternando, o Tank chega a n = 3 em `ttk_multi` = 24 + 2 × 9 = **42 ticks** (1,4 s): é o piso real, e o `max_avisos` o limita. O contato (F7) soma por fora, e o aceite do Tank (S5) cobre o conjunto. **Um `mit_golpe` único não serve a golpes de bases muito diferentes:** o #1 valida cada golpe na janela do herói (elite com `mit_golpe`, chefe com `mit_golpe_chefe`).
**Example (ilustrativo):** DPS HP 100, mit 0, base 60 → d_ef 60, n = 2 ✓. Tank HP 100, mit 0,4 → d_ef 36, n = 3 ✓. Nenhum dos dois morre em 1 golpe.

### F10. intervalo_entre_impactos

The intervalo_entre_impactos formula is defined as:

```
um Aviso novo só começa se, para todo outro Impacto em área que alcance o herói:
    |tick_impacto_novo − tick_impacto_outro| ≥ GAP_IMPACTO     // GAP_IMPACTO ≥ max(I, ticks_para_sair do golpe novo), validado pelo #1
tick_impacto_novo = CombatTick + A
```

**Variables:**
| Variable | Type | Range | Source | Description |
|---|---|---|---|---|
| GAP_IMPACTO | int | ≥ `max(I, ticks_para_sair do golpe novo)` (inicial 9) | data file | afastamento mínimo entre Impactos que alcançam o herói |
| A | int | ≥ 1 | data file | Aviso do golpe novo |

**Output Range:** com 3 avisos simultâneos no máximo, os Impactos que alcançam o herói ficam a pelo menos 9 ticks uns dos outros, então o dano nunca soma em 7a e cada golpe tem o seu Aviso. Como `R` (60) é maior que o afastamento (9), só um dos dois golpes se evita pela esquiva; o outro se evita andando, e por isso o piso do afastamento é também o tempo de sair da área (F5). O Aviso que não cabe espera, por id. A `linha` conta como área (a cápsula travada do segmento), com `raio_golpe` = meia largura.
**Example (ilustrativo):** um Impacto em T+30 e um Aviso novo com A = 24 começando em T+8 (Impacto em T+32), com `GAP_IMPACTO` 11 (= `ticks_para_sair` do elite de raio 1,02 com o Tank a 0,12 m/tick: ceil(1,32 / 0,12)): 2 < 11, então espera até T+17 (Impacto em T+41). **Simetria:** a checagem usa o módulo da diferença e roda em todo Aviso novo contra todo Impacto já agendado, então vale para qualquer par, inclusive um Aviso curto que cairia antes de um longo já marcado. `ticks_para_sair` usa `vel_heroi_min_tick`, como a F5: com 0,12 m/tick, `GAP_IMPACTO` 9 só serve a raio ≤ 0,78 m.

*Consultado:* `systems-designer` (F1 a F9; F10 derivada da proposta dele e das decisões do autor de 2026-11-05; a F11 foi removida na re-revisão de 2026-11-05).

## Edge Cases

*(Provisório e a reavaliar, salvo onde indica decisão do autor. `GolpesDescartados`, `GolpesLimitados`, `ModForaDeFaixa`, `HP_RESIDUO`, `kb_refrat_ticks`, `prontoDesde` e `ultimaDirecao` são nomes novos.)*

**HP, dano e números**
- **If uma entidade viva tem HP ≤ 0 no início do passe**: é bug interno, exceção nos dois modos (Regra 14 do #2), nunca `Kill` silencioso. O #3 já recusa herói com HP ≤ 0 no `Preparar`.
- **If `dano_final` = 0**: o golpe é válido, sem `Damage` e sem `Kill`; knockback e `Esquiva` valem. O #1 exige `base > 0` nos golpes do #6 e do #7; só o #8 pode mandar 0 (empurrão puro).
- **If `base` é NaN, infinito ou negativo, ou `modDano` fica fora de [1, `MODDANO_MAX`]**: descarta o golpe e soma em `GolpesDescartados` (fora do hash); o modo estrito lança com tick e fonte.
- **If o dano está entre `DANO_MAX` e `FLOAT_MAX`**: grava `DANO_MAX` e soma em `GolpesLimitados`. O clamp nunca é silencioso.
- **If a fila de golpes enche**: exceção nos dois modos e a simulação vira *Quebrada*. Descartar mudaria HP, que está no hash. O #1 valida `capFila ≥ vivos_máx × fontes_de_área_do_#8_por_tick + 8 + teto_vivos_horda + 1`; o último termo são os golpes `Rugido` que o #7 enfileira no tick de entrada do chefe (toda a horda viva e o elite; GDD #7, Regra 10.2) *(emenda de 2026-11-05, `/consistency-check`)*.
- **If `modCadencia` é NaN, infinito ou fora de [`MOD_CAD_MIN`, `MOD_CAD_MAX`]**: mantém o último valor válido (inicial 1) e soma em `ModForaDeFaixa`; o modo estrito lança. Não faz clamp em `MIN`, porque viraria a cadência mais rápida.
- **If `modCadencia` muda no meio de uma recarga**: o timer em curso não é recalculado; o valor novo vale na próxima.
- **If `HP − acc` fica abaixo de `HP_RESIDUO` (inicial 0,01) sem chegar a 0**: HP' = 0 e `Kill`. Emenda o F2: `morreu = (base − acc) < HP_RESIDUO`.
- **If `Curar` e dano fatal chegam no mesmo passe**: a cura soma antes do dano (F2), então pode salvar o herói; a cura nunca passa de `HPmax`.
- **If o `Rugido` e um golpe do herói atingem o mesmo alvo no mesmo passe**: o alvo morre em 7b com causa `Rugido` (o pedido está na frente da fila); o golpe do herói só conta como acerto no evento agregado, nunca como causa.
- **If o elite está em Aviso ou Recuperação quando o rugido o mata**: igual ao atacante morto (colunas zeradas no passo 8, sem Impacto novo). Se estava no próprio Impacto, o golpe vale, porque ele estava vivo no início do passe.
- **If o `Rugido` chega com o herói em i-frames**: nada muda; o herói nunca é alvo do rugido.
- **If o herói morre no mesmo tick do level-up**: não há cura, porque o alvo estava morto no início do passe seguinte e a cura vale só para vivo.
- **If `Curar` recebe NaN, infinito ou negativo, ou alvo morto**: descarta e soma em `CurasDescartadas` (fora do hash); o modo estrito lança no valor inválido.
- **If o level-up acontece com Aviso, Impacto ou Recuperação em curso**: a oferta abre na hora e o combate congela no valor exato (Regra 16); depois da contagem 3-2-1 o Impacto cai com os mesmos ticks restantes.

**Tempo e fases**
- **If `CombatActive` é falso em qualquer fase** (Aviso, Recuperação, dash, i-frames, recarga, knockback, hit-stop): tudo congela no valor exato e nada reinicia. O Impacto não é interrompido, porque dura 1 tick e a oferta só abre depois do #6 no mesmo tick; o que estava marcado cai depois da contagem 3-2-1, com os mesmos ticks restantes (Regra 16).
- **If a entidade nasceu neste `CombatTick`**: não decrementa timer, não age, não se move e não escolhe alvo, mas pode ser alvo e morrer. Entidades de `Preparar` têm `tickNascimento = 0` e agem no tick 1. Elite e chefe com `graca_ataque_ticks` > 0 agem normalmente depois do tick do nascimento, mas seguem em Perseguindo (andam e são alvo) até `tickNascimento + graca_ataque_ticks`, e só então podem iniciar o primeiro Aviso (Regra 7).
- **If o atacante morre em Aviso ou Recuperação**: as colunas de telegraph são zeradas no passo 8, não há Impacto, o #12 para de desenhar no tick seguinte e o slot dos 3 avisos libera no tick seguinte.
- **If o chefe `Essencial` morre durante o próprio Aviso**: igual ao caso anterior; o #3 dá a vitória no mesmo tick.
- **If o elite morre no mesmo tick do próprio Impacto**: o golpe vale, porque ele estava vivo no início do passe *(decisão do autor, 2026-11-05)*.
- **If o elite é empurrado durante o Aviso**: origem, direção e raio continuam travados no início do Aviso (na `linha`, também o destino: o atacante termina em `P1` mesmo empurrado).
- **If a `linha` bate na parede**: `P1` é limitado à arena já na trava, por eixo, e a linha desenhada é a limitada; com comprimento² < 1e-6 o teste é um círculo de raio `raio_golpe` em `P0`.
- **If o herói tem i-frames no Impacto de uma `linha`**: descarta o golpe e emite `Esquiva` uma vez; o atacante se desloca do mesmo jeito.
- **If o atacante morre no tick do Impacto de uma `linha`**: o golpe vale e o deslocamento já ocorreu no passo 5, porque ele estava vivo no início do passe.
- **If dois elites prontos disputam o slot do Aviso**: vence o menor `prontoDesde` (tick em que a recarga **e a graça de ataque** ficaram cumpridas), depois o menor id. Só disputa quem está dentro de `alcance_inicio_aviso_m` naquele tick; o alcance é um portão lido a cada tick, não entra no `prontoDesde` (que está no hash e não reinicia quando o herói entra ou sai do alcance).
- **If o atacante está fora de `alcance_inicio_aviso_m` com recarga e graça prontas**: segue em Perseguindo, não ocupa slot dos 3 avisos e não disputa por `prontoDesde`; entra na disputa no primeiro tick em que a `dist²` do início do tick cabe no alcance.
- **If o herói sai do alcance depois de o Aviso começar**: nada muda; o Aviso, a área travada e o Impacto seguem (Regra 6).
- **If elite ou chefe chega a `dist_parada_m` e o herói não se move**: fica parado em Perseguindo, sem tremor nem NaN, até poder iniciar Aviso; o knockback ainda o empurra.
- **If o herói fica sobre o atacante (`d² < 1e-6`)**: o atacante não anda (`d² ≤ dist_parada_m²`) e a direção travada do Aviso ou da investida é (1,0), a regra `dir` da F3; nunca vetor nulo.
- **If o herói atravessa o atacante com o dash**: permitido, porque ninguém bloqueia o corpo de outro (Regra 5); a posição do herói no início do tick manda no alvo do movimento.
- **If um corpo da horda chega ao próprio alvo de mira**: a posição vira o alvo, sem normalizar um vetor nulo ou quase nulo; nos ticks seguintes, com o herói parado, a posição se repete. Nunca NaN, nunca tremor (Regra 2.5).
- **If dois corpos têm o mesmo `id mod 32`**: o alvo de mira é o mesmo e eles se sobrepõem; é aceito, porque a horda pode se sobrepor (Regra 5).

**Esquiva**
- **If Esquivar sem eixo (módulo² < 1e-6) e sem última direção**: usa `ultimaDirecao` (coluna do herói no hash, inicial (0,1), "para cima" na tela). O dash é sempre o `Ddash` completo, em vetor normalizado.
- **If Esquivar no tick em que a recarga zera**: é válido, porque os timers decrementam antes (Regra 2). Cobertura sem reembolso = I/R = 15%; o reembolso da esquiva no limite (Regra 8) a eleva (F6).
- **If Esquivar com a recarga em até `buffer_esquiva_ticks` (3)**: o pedido fica guardado e o dash inicia no tick em que a recarga zera, com o eixo desse tick; um 2º `Esquivar` guardado substitui o 1º (vale só um); com a recarga acima de 3 o comando é ignorado, sem contar como rejeitado. `CombatActive` falso congela o buffer.
- **If os i-frames negam o Impacto de um telegraph de elite ou chefe e `I − iframes ≤ lim_esquiva_ticks`**: a recarga zera no mesmo passe (no máximo 1 reembolso por Impacto; contato e auto-ataque descartados não reembolsam) e o atacante fica `Aberto` até o fim daquela Recuperação; se o atacante morre antes, a marca some com as colunas. Fora do limite (`> lim_esquiva_ticks`) a esquiva só nega o golpe.
- **If Esquivar no mesmo tick de um golpe já na fila**: protege, porque os i-frames são lidos em 7a. O golpe descartado não dá dano, knockback nem hit-stop. `Esquiva` sai uma vez por tick e por herói, só se o descartado era telegraph.
- **If os i-frames anulam um contato**: o cooldown do inimigo é consumido e a janela de 6 ticks conta esse pedido.
- **If elite ou chefe encosta no herói** (sobreposto, ou parado em `dist_parada_m` dentro de `alcance_contato_m`): não há dano, não há cooldown de contato e a entidade não entra em `n_c`. Só a classe `Horda` causa contato (Regra 5).
- **If o dash bate na parede**: `clampArena` por eixo, o excedente se perde, e recarga e i-frames não são devolvidos.
- **If Esquivar durante knockback**: zera o `kbVel` do herói ao iniciar o dash.

**Knockback**
- **If dois knockbacks caem no mesmo tick**: vence quem tem `v0` estritamente maior (F3); o perdedor ainda causa dano.
- **If o knockback leva o alvo para dentro de outra entidade**: é permitido (Regra 5).
- **If `resist` = 1**: descarta sem evento `Knockback`, e o dano vale. `resist` fora de [0,1] é erro de dado, recusado pelo #1.
- **If o alvo morre em 7b**: não recebe knockback.
- **If o vetor é nulo**: usa `EIXOS8[id mod 8]`; alvos sobrepostos se espalham em até 8 direções, determinístico.
- **If elite ou chefe é empurrado em loop** *(decisão do autor, 2026-11-05)*: o `Essencial` tem `resist_knockback = 1`, e o elite fica `kb_refrat_ticks` (inicial 30) imune a novo knockback depois de sofrer um. A horda comum é arremessada sem limite (é a Descarga). `poise_ticks` é imunidade só a knockback, nunca a dano.

**Auto-ataque**
- **If o alvo é escolhido no passo 6**: usa as posições do passo 5, com `dist² ≤ alcance²` inclusivo.
- **If o alvo morre no mesmo passe por outro golpe**: o excedente se perde, não há nova escolha e a cadência fica gasta.
- **If não há alvo**: a cadência não é gasta.
- **If há elite ou chefe em Recuperação e um corpo da horda mais perto**: o auto-ataque mira o elite (Regra 4); fora da Recuperação volta ao mais próximo.

**Hit-stop**
- **If um evento é suprimido**: some, não vira fila e não consome orçamento.
- **If há vários elegíveis no tick**: sai 1, por prioridade (sofrido > suprema > pesado) e depois menor id.
- **If `CombatTick` está parado**: `proximoHitStopTick` não anda e nenhum evento nasce. O #12 cancela o hit-stop em curso quando `CombatHold ≠ 0`.

**Tank e DPS**
- **If `mit = MIT_MAX`**: o dano é sempre > 0. O #1 recusa se `n_DPS ≠ 2` ou `n_Tank ≠ 3` (F9).
- **If o herói não tem mitigação ou o golpe não tem tipo**: `mit_*` explícito em 0 é válido; campo ou tipo ausente é recusado pelo #1.

**Capacidade e eventos**
- **If 300 mortes caem no mesmo tick**: a horda vira 1 evento agregado, montado em scratch e emitido no passo 8. `DeathsThisTick` não é evento e nunca descarta (perderia XP); sua capacidade é a de entidades, e estourar é bug interno.
- **If o buffer de eventos precisa de espaço**: um `Damage` por alvo individual por tick (soma). O #1 valida `EventCapacity ≥ EventosReservados + 5 + 3 × individuais_máx + 4`.
- **If há `DroppedEvents` no modo estrito**: lança no primeiro. O início de telegraph usa a reserva.

**Determinismo**
- **If há empate**: menor id, sempre, com laços por id crescente.
- **Ordem contratual da fila:** `Rugido` do #7 (por id do alvo), pedidos do #8 (ordem de enfileiramento), impactos por id do atacante, contatos, auto-ataque.
- **O `Hash` do #6 inclui:** as colunas listadas na Detailed Design, `proximoHitStopTick`, recarga da esquiva, dash restante e direção, `ultimaDirecao`, cadência do auto-ataque, kb restante, `poise`, `kb_refrat`, `prontoDesde`, o índice do ciclo do chefe, `aberto`, `punidoPesado`, `esquivaBuf`, `curaPendente`, `ultimoContatoTick` e a área travada do telegraph. **Fica fora do hash:** fila, `acc`, `vivoNoInicio`, contadores de diagnóstico e a supressão (derivada).

**Estratégias degeneradas**
- **If o jogador esquiva sem parar**: `R` limita a invulnerabilidade a I/R = 15% (R = 60), mais o reembolso da esquiva no limite (F6: ≈ 49% no pior caso com 3 elites). Se o #8 criar redução de recarga, `R_ef = max(R × mod, I + 1)`.
- **If o jogador fica no canto**: o contato continua limitado a 1 a cada 6 ticks. A F5 deve validar o pior caso com o herói no canto escapando ao longo da parede, não só no centro.
- **If o jogador faz kite do elite**: se `vel_heroi > vel_elite`, o elite nunca alcança, e isso é legítimo *(decisão do autor, 2026-11-05)*. Contra o chefe vale o teto de tempo do #3 (`DerrotaTempo`).
- **If há stun-lock do chefe**: o #6 não tem stun, e knockback não altera fases; o `Essencial` é imune a knockback.

**Emendas e notas pedidas a outros GDDs**
- **#2:** contadores `GolpesDescartados`, `GolpesLimitados`, `ModForaDeFaixa`, `CurasDescartadas` na Regra 14 e fora do hash na Regra 10; nota na Regra 7 sobre os dois tempos; `DeathsThisTick` com capacidade igual à de entidades; `DeathCause.Rugido` como valor novo (hoje o ADR-0001 só tem `Normal` e `InvalidValue`).
- **#3:** pedir `Curar` (`cura_levelup_pct × hpMax`) no level-up; confirmar vitória no mesmo tick se o chefe morre no Aviso e a lista de mortos limpa a cada tick.
- **#7:** primeiro Aviso de elite e chefe a partir de `tickNascimento + graca_ataque_ticks` (Regra 7); ordem de Aviso por `prontoDesde`; ciclo do chefe fixo, com índice no hash; `resist_knockback` e `kb_refrat_ticks` por arquétipo; o pedido `Rugido` tipado, uma vez por fase (Regra 3); `alcance_inicio_aviso_m` por golpe (Regra 6); `dist_parada_m` de elite e chefe (Regra 2.5); sem `dano_contato` em elite e chefe (Regra 5); tabela de mira de 32 entradas e `mira_offset_max_m` (Regra 2.5); golpe `linha` com `desloc_m` (Regra 6); recarga de ataque `g` por arquétipo (Regra 6); parar de ler `aviso_perto` (F11 removida; o registro marcava o #7 como referência).
- **#8:** ordem de enfileiramento; `modDano ∈ [1, MAX]`, `modCadencia` na faixa; dano 0 só para empurrão; sem bônus negativo; redução de recarga com piso `I + 1`.
- **#1:** recusar `dano_contato` em arquétipo de elite e de chefe (Regra 5); validar cada entrada da tabela de mira com módulo ≤ `mira_offset_max_m` ≤ `alcance_contato_m` (Regra 2.5); `desloc_m` > 0 e forma `linha` só em golpe de elite e de chefe, com a meia largura na F5 (Regra 6); validar `alcance_inicio_aviso_m` ≤ `meia_altura_visivel_m − margem_visivel_m` por golpe e `0 < dist_parada_m ≤` o menor `alcance_inicio_aviso_m` do arquétipo (F10 do #7); knobs e validações `capFila`, `EventCapacity`, `HP_RESIDUO`, `MOD_CAD_MIN/MAX`, `MODDANO_MAX`, `kb_refrat_ticks`; `base > 0`, tipo de golpe obrigatório, mitigações explícitas, `resist ∈ [0,1]`; F5 com herói no canto; `cura_levelup_pct`, `mult_punicao_pesado`, `mult_punicao_aberto`, `lim_esquiva_ticks`, `buffer_esquiva_ticks`, `mit_golpe_chefe`, `R ≥ 3 × I` e `n_Tank` como knob de aceite (no lugar de `mit_golpe`).
- **#12:** cancelar o hit-stop quando `CombatHold ≠ 0`; parar de desenhar o telegraph na morte do atacante.
- **#16:** abrir a oferta na hora (`CombatHold` = 1) e ser dono da contagem 3-2-1 (≥ 19 ticks) na volta; sem `AvisoPerto`; listar o #6 nas dependências (Soft).
- **#3 e #2:** o pedido de cura do level-up soma em `curaPendente` (coluna no hash), não numa fila fora dele.

*Consultado:* `systems-designer`.

## Dependencies

**Upstream (o #6 depende deles)**

| Sistema | Natureza | O que o #6 recebe | Dono da interface |
|---|---|---|---|
| #1 Dados e balanceamento | **Hard** | todos os números (dano, cadências, A, P, `I`, `R`, mitigações, orçamentos) já convertidos em ticks e `float`, e a validação F5 a F10 | #1 valida; o #6 é dono do significado de cada campo |
| #2 Simulação determinística | **Hard** | ordem dos sistemas, `CombatActive`, `CombatTick`, `SimWorld` (posição, facção, HP), `Kill`, `DeathsThisTick`, streams, comandos, eventos | #2 |
| #4 Input e câmera de combate | **Soft** | `Mover`, `Esquivar` e `Suprema` chegam como `Command` do #2; sem o #4 o #6 roda com comandos de teste | #2 define o `Command`; o #4 produz |

**Downstream (dependem do #6)**

| Sistema | Natureza | O que recebe do #6 | Dono da interface |
|---|---|---|---|
| #3 Fluxo de fase | **Hard** | morte do herói e dos inimigos (`DeathsThisTick` com causa), HP do herói; o #3 pede `Curar` no level-up | #6 produz as mortes; #3 lê e pede a cura |
| #7 Horda, waves e inimigos | **Hard** | o ciclo de ataque (com `alcance_inicio_aviso_m` por golpe e, na `linha`, `desloc_m`), a `dist_parada_m` de elite e chefe, a tabela de mira da `Horda` e o contato dos arquétipos de classe `Horda`, a `graca_ataque_ticks` de elite e chefe, o pedido `Rugido` (único dano que o #7 origina), o estado de ataque (leitura) | #7 declara os arquétipos; #6 os executa |
| #8 Skills e evoluções | **Hard** | `Combate.Aplicar`, `modDano`/`modCadencia` lidos pelo #6, a suprema | #6 dono do ponto único de dano |
| #10 Funções | **Hard** | os campos de mitigação do Tank e a regra de hit-stop por função | #10 declara; #6 aplica |
| #11 Raças | **Soft** | a mesma regra de dano para a skill racial | #8 |
| #12 Feedback de combate, VFX e HUD | **Hard** | colunas de telegraph (fase, ticks até o dano, forma, raio, origem e, na `linha`, destino) e os eventos `Damage`, `Esquiva`, `Knockback`, `HitStop`, `Morte` | #6 produz; #12 lê |
| #16 Oferta do Grimório | **Soft** | nada: o #16 abre a oferta na hora sob `CombatHold` e é dono da contagem 3-2-1 (Regra 16); o #6 não expõe predicado de oferta | #16 |
| #5 Log de eventos | **Soft** | mortes e danos relevantes para as métricas de aceite | #5 lê os eventos do #2 |

**Bidirecionalidade (o que cada documento precisa dizer sobre o #6)**
- **#1 e #2:** já listam o #6 como Hard. O #2 recebe as notas da seção Edge Cases (contadores, Regra 7 em dois tempos).
- **#3:** lista o #6 como Hard com contrato provisório; falta confirmar que a lista de mortos é o `DeathsThisTick` do `SimWorld` (fecha a OQ-4 do #3).
- **#4, #5, #7, #8, #10, #11, #12 e #16:** ainda sem GDD; cada um deve citar o #6 nas suas Dependencies com a natureza desta tabela.
- **Índice (`systems-index.md`):** a coluna "Depends On" do #6 continua "1, 2". O #4 não entra nela porque é interface via #2; vale uma nota no Dependency Map. O #16 lista o #6 como Soft (não lê mais nada dele).

**Dependência circular:** nenhuma. O #6 não depende do #3 nem do #7; ele lê o `tickNascimento` e o arquétipo de colunas do `SimWorld`.

## Tuning Knobs

Os knobs **moram no #1**, que guarda o valor, a unidade e a faixa; o significado e a faixa proposta são deste GDD. Os valores são iniciais e **a reavaliar**; `ilustr.` vem das fórmulas. Nenhum é remoto no MVP.

**Não duplicados (a fonte está em outro lugar):** `ticks_per_second` (#2 e ADR-0001); `xp_*`, `nivel_max` e `duracao_max_apos_chefe_s` (#3); HP do herói e `vel_heroi_per_s` (#1 e #10; `vel_heroi_min_tick` não é knob, a F5 deriva do herói mais lento: ilustr. 4,5 m/s = 0,15 m/tick, Tank 3,6 m/s = 0,12); `dano_contato_max` (só classe `Horda`), `base_elite`, o ciclo de golpes (forma e `desloc_m`), o `alcance_inicio_aviso_m` por golpe, a `dist_parada_m`, a tabela de mira da `Horda` (32 entradas, `mira_offset_max_m`) e a `graca_ataque_ticks` (#7; o #6 só lê, Regras 2.5, 6 e 7); `fontes_de_area_por_tick` (#8).
**Constantes, não knobs:** `REACAO` = 8 ticks, `JANELA` = 5 ticks (piso) e `FATOR_PARADA` = 0,99 (alvo de parada em fração de `dist_parada_m`, margem de float32). Vão para as constantes deliberadas do #1; mudar `REACAO` ou `JANELA` redefine o aviso mínimo de todo golpe.
**Nomes:** os IDs são `snake_case`. Durações longas usam `_s` no dado (Regra 4 do #1) e viram ticks pela F1 do #1: `cad_s` → `cad_ticks`, `cad_contato_s` → `cad_contato_ticks`, `recarga_esquiva_s` → `R`, `kb_refrat_s` → `kb_refrat_ticks`, `tempo_morte_contato_min_s` → `X`. As fórmulas mantêm os símbolos em ticks depois da conversão.

| Knob | Padrão | Faixa segura | Remoto | Afeta | Baixo demais | Alto demais |
|---|---|---|---|---|---|---|
| `dano_max` (F1) | a calibrar; ≥ maior `base` × `moddano_max` × `mult_punicao` | `float`, pontos, ≤ 1e6 | não | teto de saneamento de um golpe | clampa dano legítimo (`GolpesLimitados` sobe) | deixa bug de bônus passar; `acc` perde precisão |
| `moddano_max` (F1) | ilustr. 10 | `float` ≥ 1 | não | teto do escalar do #8 | bônus legítimo vira descarte do golpe | bug do #8 vira dano absurdo |
| `mit_max` (F1) | ilustr. 0,6 | `float`, 0 a < 1 (proposta 0,3 a 0,9) | não | maior `mit_*` aceita | o #1 recusa o Tank | Tank quase imortal |
| `mit_contato` (herói) | Tank 0,4 ilustr.; DPS 0 | `float`, 0 a `mit_max` | não | contato recebido (F7) | Tank não segura a horda; F7 reprova | horda sem ameaça |
| `mit_golpe` (herói) | Tank 0,4 ilustr.; DPS 0 | `float`, 0 a `mit_max`, dentro da janela da F9 | não | golpe com telegraph (F9) | n_Tank cai para 2; F9 recusa | n_Tank sobe a 4; F9 recusa |
| `resist_knockback` (herói e arquétipo) | `Essencial` 1; horda 0; Tank a calibrar | `float`, 0 a 1 | não | F3 | Tank sai do posto; elite voa | horda não voa e perde a Descarga |
| `mult_punicao` (F1) | 1,5 | `float`, 1 a 3 | não | dano em Recuperação | 1 = ler o golpe não rende nada | elite cai num golpe; `dano_max` precisa cobrir |
| `mult_punicao_pesado` (F1) | 2,0 | `float`, `mult_punicao` a 3 | não | 1º golpe `pesado` em Recuperação | ler o golpe rende pouco | elite cai no 1º golpe pesado |
| `mult_punicao_aberto` (F1) | 2,0 | `float`, `mult_punicao` a 3 | não | todo golpe na Recuperação `Aberto` | sair no limite não rende | elite aberto cai rápido demais |
| `lim_esquiva_ticks` (Regra 8) | 3 | `int`, ticks, 0 a `iframes_ticks` − 1 | não | quão tarde o toque precisa ser para valer o reembolso | quase ninguém acerta | esquiva cedo também reembolsa; i-frames quase permanentes (OQ-18) |
| `buffer_esquiva_ticks` (Regra 8) | 3 | `int`, ticks, 0 a 6 | não | toque na recarga que fica guardado | toque cedo parece entrada perdida | esquiva sai quando o jogador não pediu |
| `mit_golpe_chefe` (herói) | omitido = `mit_golpe`; Tank a calibrar | `float`, 0 a `mit_max`, na janela da F9 com a `base` do chefe | não | golpe de chefe (F9) | n_Tank cai para 2 | n_Tank sobe a 4 |
| `mod_cad_min` (F4) | ilustr. 0,25 | `float`, > 0 e ≤ 1; `cad_s` × min ≥ ~3 ticks | não | cadência mais rápida aceita | 30 ataques/s; F4 recusa | bônus do #8 fora da faixa congela a cadência no último valor válido |
| `mod_cad_max` (F4) | ilustr. 2 | `float` ≥ 1 | não | cadência mais lenta aceita | < 1 rejeita o valor inicial 1 | sem uso no MVP (o #8 escreve ≤ 1) |
| `cad_s` (auto-ataque do herói) | a calibrar | `float`, s; ≥ 3 ticks ÷ `mod_cad_min` (≥ 0,4 s com 0,25) | não | frequência do auto-ataque | F4 recusa | Tank mata devagar e estoura `duracao_max_apos_chefe_s` |
| `alcance_auto_m` | a calibrar | `float`, m, > 0 | não | alcance do auto-ataque | herói sem alvo; cadência não gasta | herói acerta fora da leitura |
| `cad_contato_s` | 0,5 s (15 ticks) | `float`, s; ≥ `contato_gap_ticks` | não | ritmo de cada inimigo em contato | teto de contato sempre saturado | horda pouco ameaçadora |
| `contato_gap_ticks` (por herói) | 6 | `int`, ticks, 1 a `cad_contato` | não | golpes de contato no herói (F7) | contato vira rajada | com gap > `cad_contato` o cooldown perde sentido |
| `alcance_contato_m` | a calibrar | `float`, m (proposta 0,3 a 1,0) | não | raio do contato | horda precisa se sobrepor ao herói | contato "de longe" lê como injusto |
| `aviso_ticks` A (por golpe) | elite 24; chefe 36 | `int`, ticks; ≥ piso da F5 do golpe; proposta ≤ 90 | não | tempo para ler | F5 recusa; golpe ilegível | luta lenta; `ttk` da F9 sobe |
| `recuperacao_ticks` P (por golpe) | elite 30; chefe 36 | `int`, ticks, 6 a 90 (proposta) | não | janela de punição e ritmo do ciclo | punição curta demais para ler | alvo parado demais; golpes escassos |
| `gap_impacto_ticks` (F10) | 9 (piso = `iframes_ticks`); ilustr. 11 para o elite de raio 1,35 | `int`, ticks, `max(iframes_ticks, ticks_para_sair do golpe novo)` a 30 (proposta) | não | espaço entre Impactos que alcançam o herói | dano soma sem leitura; sem tempo para andar | avisos esperam demais; elite ataca menos que o projetado |
| `max_avisos` | 3 | `int`, 1 a 6 (o `+8` de `cap_fila` cobre 6 avisos + contato + auto-ataque) | não | avisos simultâneos | elites esperam | tela ilegível (P4); `cap_fila` curto |
| `margem_m` (F5) | ilustr. 0,3 | `float`, m, 0,2 a 0,5 | não | folga do corpo no aviso mínimo | F5 otimista | F5 recusa golpes legítimos |
| `iframes_ticks` I (F6) | 9 | `int`, ticks, 7 a 15 | não | janela de esquiva | esquiva vira sorte | invulnerabilidade longa |
| `recarga_esquiva_s` R (F6) | 2,0 s (60 ticks) | `float`, s; de 3×I ticks a 4,0 s | não | frequência de esquiva | spam; I/R ≥ 15% | esquiva rara; Tank sofre |
| `ddash_m` (F6) | ilustr. 2,7 | `float`, m, 2× a 4× (I × `vel_heroi`) | não | deslocamento do dash | não sai do elite | cruza a arena |
| `kb_d_m` D (por golpe) | a calibrar | `float`, m, 0 a `kb_d_max` | não | empurrão (F3) | sem peso (P4) | jogado para fora da leitura |
| `kb_ticks` K (F3) | 4 | `int`, ticks, 1 a 8 | não | duração do empurrão | teleporte (K = 1) | arrasto lento |
| `kb_d_max` D_MAX | ilustr. 3 | `float`, m (proposta 0,5 a 5) | não | teto de D | recusa golpes legítimos | knockback de bug |
| `poise_ticks` | a calibrar | `int`, ticks, 0 a 30 | não | imunidade a knockback após Recuperação | elite empurrado ao sair da Recuperação | elite não reage ao knockback |
| `kb_refrat_s` | 1,0 s (30 ticks) | `float`, s; ≥ K ticks | não | refratário do elite | elite em loop de knockback | elite imune; perde peso |
| `hitstop_n_ticks` N (F8) | 10 | `int`, ticks, ≥ H a 30 | não | espaço entre hit-stops | apresentação ocupa tempo demais | Descarga sem peso |
| `hitstop_h_ticks` H (F8) | 3 | `int`, ticks, 1 a 5 | não | duração do hit-stop | imperceptível | tela trava |
| `hs_supr_ticks` (F8) | 12 | `int`, ticks, ≥ H + `REACAO` (11) e < A mínimo (proposta ≤ 20) | não | janela de supressão antes do telegraph | hit-stop na leitura | quase nunca emite |
| `margem_supr_m` (F8) | ilustr. 1,8 | `float`, m, `margem_m` a 3 | não | "perto do herói" | não suprime | suprime demais |
| `tempo_morte_contato_min_s` X (F7) | 8,0 s (240 ticks) | `float`, s | não | piso para morrer só por contato | horda mata sem leitura | F7 recusa quase tudo |
| `hp_residuo` (F2) | 0,01 | `float`, pontos, 0 < r ≤ 0,1 e ≥ ~16 × HPmax × 2⁻²³; **com HPmax acima de ~5 000 o resíduo sobe ou o HP é limitado** | não | HP abaixo disto vira morte | "vivo com 0,00001" | mata quem tem vida visível |
| `cap_fila` | a calibrar | `int` ≥ `vivos_max × fontes_de_area_por_tick + 8 + teto_vivos_horda + 1` (o último termo é o rugido do #7); teto pelo spike | não | pedidos de golpe por tick | fila cheia: simulação *Quebrada* | memória |
| `event_capacity` | a calibrar | `int` ≥ `EventosReservados + 5 + 3 × individuais_max + 4`; teto pelo spike | não | buffer de eventos | `DroppedEvents` lança no modo estrito | memória |
| `orcamento_combate_ms` (AC-P1) | alvo p95 2,0; piso p99 4,0 (a confirmar no spike) | `float`, ms por tick, 0 < x ≤ 12% de 33,3 ms | não | tempo máximo do `Tick` do #6 com 300+ vivos no aparelho de referência | aceite exigente demais para o aparelho; o spike falha à toa | o #6 consome o orçamento dos outros sistemas e a horda reduz |
| `cura_levelup_pct` (Regra 15, F2) | a calibrar | `float`, 0 a 1 do `hpMax` | não | vida recuperada a cada level-up | o Tank fica sem fôlego ao longo da fase e o critério de aceite (≤ 2 mortes) corre risco | o level-up apaga o erro e a Tensão some |

**Knobs de aceite do MVP** (`aceite: sim`, nunca remotos, `pior` obrigatório; o critério é o Tank abrir o selo com ≤ 2 mortes de fase, e o `pior` de cada um só se confirma medindo o Tank no protótipo)

| Knob | Sentido | Pior valor aceitável |
|---|---|---|
| `n_Tank` (golpes de elite que o Tank aguenta; sai de `mit_golpe` pela F9) | maior_melhor | 3 (a janela de `mit_golpe` tem dois lados, então o knob de aceite é o resultado, não a mitigação) |
| `mit_contato` (Tank) | maior_melhor | `1 − contato_gap·HP/(X·dano_contato_max)` (ilustr. 0,4) |
| `aviso_ticks` | maior_melhor | 24 (elite) e 36 (chefe), os pisos da F5 |
| `recuperacao_ticks` | maior_melhor | a calibrar (piso da regra 6) |
| `mult_punicao` | maior_melhor | a calibrar (piso 1,0) |
| `mult_punicao_pesado` e `mult_punicao_aberto` | maior_melhor | a calibrar (piso 1,5) |
| `iframes_ticks` | maior_melhor | 7 |
| `recarga_esquiva_s` | menor_melhor | a calibrar |
| `gap_impacto_ticks` | maior_melhor | 9 |
| `max_avisos` | menor_melhor | 3 |
| `contato_gap_ticks` | maior_melhor | 6 |
| `cad_contato_s` | maior_melhor | 0,5 s |
| `tempo_morte_contato_min_s` | maior_melhor | 8,0 s |
| `resist_knockback` (Tank) | maior_melhor | a calibrar |
| `cad_s` e `alcance_auto_m` (Tank) | menor_melhor e maior_melhor | a calibrar, atados a `duracao_max_apos_chefe_s` do #3 |
| `vel_heroi_per_s` (Tank, dono #1) | maior_melhor | 3,6 m/s (ilustr.; F5 com elite 1,32 m) |
| `cura_levelup_pct` | maior_melhor | a calibrar |

**Fora do aceite:** hit-stop (só apresentação), capacidades (fixadas no fim do spike), `dano_max`, `moddano_max`, `mod_cad_*`, `margem_*`, `hp_residuo`, `poise_ticks`, `kb_*`, `alcance_contato_m`.

**Interações**
- **A:** diminuir A, subir o raio do golpe, subir `margem_m` ou baixar `vel_heroi` faz a F5 recusar. Subir A alonga o ciclo A+1+P: a F9 muda o `ttk` e a regra "ciclo do elite < R" muda.
- **I:** subir I exige `gap_impacto_ticks` ≥ I, move a faixa de `ddash_m` e exige `R > I`. Com I = 15 e R = 60 são 25% de i-frames, não os 15% citados.
- **HP do Tank:** F7 e F9 são homogêneas em HP e dano, então escalar HP, `base_elite` e `dano_contato_max` juntos não quebra nada; mudar só o HP quebra a F9 (janela de `mit_golpe` ≈ 0,18 a 0,43 com HP 100 e base 60, estreita).
- **F9 trava o Tank em exatamente 3 golpes** de elite e de chefe. As alavancas livres são esquiva, A/P, contato, `X` e a velocidade com que o Tank mata.
- **Capacidades:** `max_avisos` > 6 estoura o `+8` de `cap_fila`; subir `teto_vivos_horda` (#7) sobe o piso de `cap_fila`. **Elite:** `kb_refrat_s` ≥ K e `poise_ticks` se sobrepõem; revise juntas.

*Consultado:* `systems-designer`.

## Visual/Audio Requirements

**Regras gerais.** A faixa proibida (H 350° a 38°, S ≥ 55%, V ≥ 55%) é só do telegraph (art bible 4.2a). Todo o resto fica fora dela por H, S ou V. Efeito aliado: curva lisa, alfa ≤ 0,85, ≥ 40% da área do cartão com alfa ≤ 0,6, sem serrilha nem hachura; em anel, só arco aberto ≤ 270° ou disco difuso. Nenhum pixel em H 44°–58° com S ≥ 50%. No máximo 150 cartões aliados, overdraw médio ≤ 2,5×, nenhum cartão acima de 10% da tela (8.7). Hit-flash e dissolve são shader com propriedade por instância, nunca partícula.

| Evento | Requisito visual | Requisito sonoro |
|---|---|---|
| Auto-ataque | Arco liso aberto em amarelo-branco pálido (H 60–72, S 20–40, V ≥ 92), 1 cartão de pool por golpe | Acerto leve, só se acertou |
| `Damage` na horda (agregado) | Flash de shader por 2 ticks em branco-frio (H 200–230, S ≤ 15); sem hit-stop e sem partícula | Acerto leve, escolhido pela contagem `acertos` (1, 2–5, 6 ou mais) |
| `Damage` em elite ou chefe | Flash S ≤ 20, V ≤ 55 no corpo, **nunca na "parte que ataca"** (osso frio), com **teto de brilho próprio medido e no máximo 2 ticks** *(decisão do autor, 2026-11-05)* | Acerto pesado se `pesado`; senão leve |
| `Knockback` | Horda e elite deslizam por 4 ticks; **o chefe não se desloca** (`resist` = 1): o peso dele vem de flash, hit-stop e som | Nenhum som próprio |
| `HitStop` | Congela só a pose do herói e do alvo por 3 ticks; telegraph, decal, câmera e relógio seguem | Nenhum |
| `Esquiva` (só quando nega telegraph) | Rastro liso translúcido de 1 cartão e flash pálido no herói; sem anel fechado | Esquiva (o dash) e uma confirmação distinta quando nega telegraph |
| Início do Aviso | O decal é o único objeto na faixa: `#FF4A1C` com alfa 0,70, hachura e serrilha (3.6), frente crescendo em `A` ticks; no chefe, LUT frio; 0 partículas | Aviso de telegraph, um por golpe, que sobe até o Impacto |
| Impacto (1 tick) e cauda | Cauda de apresentação de 3 ticks: decal cheio na tinta clara, depois some; não pode parecer perigo ativo | Impacto do elite (seco) e do chefe (grave) |
| Recuperação aberta | Pose exposta mantida por `P` ticks e rim frio (H 200–230, S ≤ 20) que fecha nos últimos 6 ticks; na Recuperação `Aberto` o rim é mais forte e a marca da punição ×2,0 fica visível (OQ-17); sem hachura nem serrilha | O acerto na Recuperação usa o pesado |
| Dano ao herói | Placa de ferro com número claro junto da barra (7.2) e flash pálido. **Zero vermelho e zero vinheta** | Golpe sofrido, o som mais audível do herói |
| Morte de elite ou chefe | Dissolve de shader; chefe: transição para 2.7 no mesmo tick (vitória) | Morte de elite ou chefe, 2 timbres |
| Morte agregada da horda | Dissolve de shader de 8 a 10 ticks (a decidir), V ≤ 30 inclusive na borda; pool limitado de fantasmas, o excedente some sem dissolve | Queda em massa por faixas de `mortes` (1–4, 5–20, 21 ou mais) |
| Suprema | Visual é do #8; o #6 só dá `HitStop` e `pesado` | Do #8, no registro de acerto pesado |

**Sons mínimos (placeholder, requisito do #12):** acerto leve, acerto pesado, golpe sofrido, aviso de telegraph, Impacto elite/chefe, esquiva, morte elite/chefe e a queda em massa da horda (sem ela a Descarga fica muda). Clima: seco, pesado e poeirento, com o aviso nítido e contido (2.2). Número de vozes, ducking e mixagem são do audio-director.

**Prioridade quando a tela lota:** telegraph > herói > elite e chefe > aliados > horda. O corte é na ordem inversa: a horda perde flash e dissolve (vira fade), depois os aliados perdem cartões (os mais antigos primeiro). Telegraph e herói nunca perdem nada. Cartões aliados sobre a área do telegraph ficam com alfa ≤ 0,6, e decals sobrepostos se ordenam por Impacto mais próximo no topo, sem blend aditivo.

**O que o #6 expõe além da Regra 14:** por entidade, `ultimoDanoTick` e `pesado`; posição, arquétipo e tick da morte de cada horda, legíveis por 1 tick depois de `DeathsThisTick`, sem reciclar o slot; ticks restantes da Recuperação; e as colunas já hasheadas de dash restante, `iframes` e cadência (não há evento de início de dash nem de auto-ataque).

**Assets para `/asset-spec`** (prefixos novos `sfx_` e `shd_`): `shd_enm_dissolve` e `tex_vfx_dissolve_noise_256.png`; `tex_vfx_telegraph_hatch_alb.png`, `mat_vfx_telegraph_decal.mat`, `vfx_telegraph_circle_fill`, `vfx_telegraph_cone_fill` e `vfx_telegraph_impact_tail_small`; `vfx_dash_trail_small`, `vfx_hit_arc_light_small` e `vfx_hit_arc_heavy_medium`; `ui_plate_damage_taken_9s.png`; animações `anim_shared_hero_dodge_01`, `anim_shared_hero_attack_light_01`, `anim_shared_tank_attack_heavy_01`, `anim_shared_hero_hit_react_01`, `anim_enm_elite_aviso_01`, `anim_enm_elite_recovery_01`; e `sfx_hit_light_01..03`, `sfx_hit_heavy_01..02`, `sfx_hurt_hero_01..02`, `sfx_telegraph_warn_01`, `sfx_impact_elite_01`, `sfx_impact_boss_01`, `sfx_dodge_01`, `sfx_dodge_negate_01`, `sfx_death_horde_s/m/l`, `sfx_death_elite_01`, `sfx_death_boss_01`.

*Consultado:* `art-director`.

## Game Feel

Orçamento de latência do #2: o comando age no tick seguinte à amostragem e a tela mostra até 1 tick depois, ≈ 2 ticks (67 ms) mais 1 frame. Alvo de simulação ≤ 2 ticks; alvo toque-a-tela ≤ 100 ms, **a medir no aparelho**.

| Ação | Sensação alvo | Entrada | Duração (ticks) | Feedback | Não deve |
|---|---|---|---|---|---|
| Esquiva | Tranco seco: escorrego e sumo do golpe | ≤ 2 + frame; os i-frames já valem antes de a tela mostrar o dash | Dash e i-frames: 9. Recarga: 60 | Rastro, som, confirmação ao negar telegraph, háptico leve (knob) | O hit-stop atrasar o dash (o dash cancela a pose congelada); o botão em recarga não mostrar se recusou ou se guardou o toque (buffer de 3 ticks) |
| Auto-ataque | Corte contínuo, rítmico, sem pedir dedo | n/a | Swing ≤ `cad_efetiva` | Arco, acerto leve | Swing ou som sem alvo |
| Acerto na horda | Ceifar: o grupo cede e cai | Acerto em T, visível em T+1 no máximo | Knockback 4; flash 2 | Flash, deslize, som agregado | Hit-stop, número ou partícula por acerto |
| Acerto pesado no elite | Baque que trava a mão | Igual | Hit-stop 3, no máximo 3/s | Flash parcial, som pesado, knockback (refratário de 30) | Hit-stop com telegraph a ≤ 12 ticks do dano; flash embranquecer o osso |
| Golpe sofrido | Pancada que sacode e passa rápido | n/a | Hit-stop 3 (só com telegraph); knockback 4 | Placa de ferro, flash pálido, som, háptico (knob) | Vinheta vermelha; hit-stop por contato |
| Morte da horda | Derreter em onda, não estourar | n/a | Dissolve 8–10 (a decidir) | Dissolve e queda em massa por faixa | Um som por morte; cor na faixa |
| Telegraph do elite | O chão avisa e eu decido | Visível ≤ 1 tick + frame após o início | Aviso 24; Recuperação 30 | Frente de preenchimento e som de aviso | Hit-stop congelar a frente; efeito aliado cobrir o decal |
| Impacto do chefe | O chão racha | n/a | Aviso 36; Impacto 1 + 3 de cauda; Recuperação 36 | Cauda do decal, som grave, **tremor mínimo com knob de acessibilidade** *(decisão do autor, 2026-11-05)* | A cauda parecer perigo ativo; tremor durante um Aviso perto do herói |

**Janela de esquiva percebida:** a latência de ≈ 2 ticks **desloca** a janela, não a encurta: o jogador reage ao que viu 2 ticks atrás, e isso já está na `REACAO` da F5. A janela útil continua 9 ticks (300 ms), o que respeita o piso de 5 do #2 e o `I ≥ 7` do #1, e o toque precisa vir ~2 ticks antes do que o olho sugere (OQ-3). O buffer de 3 ticks e o reembolso da esquiva no limite (Regra 8) são o que torna esse toque justo.
**Háptico** *(decisão do autor, 2026-11-05)*: knob de acessibilidade, ligado por padrão só em golpe sofrido e em esquiva que nega telegraph. A API de vibração do Android é `NOT SOURCEABLE` (spike).
**Medição no aparelho:** toque-a-tela, frame time com 300 mortes e 3 telegraphs, custo do dissolve com fantasmas, overdraw e a vibração.

*Consultado:* `art-director`.

## UI Requirements

- **Barra de vida do herói** junto da placa de ferro de dano sofrido (7.2), com número claro, **sem vermelho e sem vinheta**. Mostra a vida que o #6 grava em 7b.
- **Botão de esquiva** com estado de recarga (`R` ticks) e feedback do buffer: o toque nos últimos `buffer_esquiva_ticks` da recarga é **guardado** (sinal de 'aceito'); fora disso é **recusado** de forma visível (o #6 ignora o comando sem contá-lo como rejeitado).
- **Telegraph é decal no mundo**, não elemento de UI; o #12 o desenha lendo as colunas do #6.
- **Knobs de acessibilidade** (nas opções): reduzir efeitos aliados (só o #12; o #6 não muda regra por causa disso), háptico e tremor de câmera.
- **Barras de vida de elite e chefe:** a UX decide no `/ux-design`; o #6 expõe `HP` e `hpMax`.

> **📌 UX Flag — Combate e dano (#6)**: este sistema tem requisitos de UI. Na Fase 4 (Pre-Production), rode `/ux-design` para o HUD de combate e para os controles **antes** de escrever épicos; as stories que citam UI devem citar `design/ux/[tela].md`, não este GDD.

## Cross-References

| Documento | Regra, seção ou ID | O que o #6 usa | Natureza |
|---|---|---|---|
| `dados-e-balanceamento.md` (#1) | F1, F2, Regras 2 e 4 | segundos→ticks (`floor(s×30+0,5)`), taxa por tick (`r÷30`), IDs de knob e `_s`/`_ticks` | Valor e regra |
| `dados-e-balanceamento.md` (#1) | F6 | coerência de knob de aceite com `pior` e `sentido` | Regra |
| `simulacao-deterministica.md` (#2) | Regras 5, 7, 9, 13, 14 | ordem dos sistemas; morte na hora (relaxada em 7b); valor inválido; erro nos dois modos | Regra e nota pendente |
| `simulacao-deterministica.md` (#2) | OQ-4 | quem move: o #6 | Decisão deste GDD |
| `fluxo-de-fase.md` (#3) | Regras 7, 9, 13 e OQ-4 | morte do herói e do chefe, vitória na morte simultânea, lista de mortos do `SimWorld` | Contrato |
| `game-concept.md` | Pilares 3 e 4; Core Loop; MVP (Tank ≤ 2 mortes) | a fantasia e os critérios de aceite | Âncora |
| ADR-0001, ADR-0002 | `SimWorld`, float32, conversão no build | tipos, ordem e dados | Decisão técnica |
| Art bible | 2.2, 3.6, 4.2a, 7.2, 8.7 | telegraph, faixa proibida, placa de ferro, orçamentos | Requisito visual |

## Acceptance Criteria

**Convenções.** Os IDs valem só neste GDD ("#6 AC-R3"). Os testes ficam em `Assets/Tests/EditMode/Combate/[Classe]Tests.cs`, com método `Cenario_Esperado`, e todo teste afirma `testcasecount > 0`. Fixtures vêm de arquivo constante ou função de fábrica. Dublês: `FakeWorld` (ou `SimWorld` real), `FakeComandos`, `FakeSistema7` (nasce arquétipos declarados), `FakeSistema8` (enfileira pedidos e escreve `modDano` e `modCadencia`), `FakeSistema3` (lê `DeathsThisTick`) e `FakeLog`. Tipos: **[U]** unitário EditMode; **[I]** integração com uma `Simulation` real e dublês; **[PM]** playtest manual do autor (n = 1) ou medição no aparelho; **[R]** revisão. Cada critério é **PRONTO** por padrão, ou leva **BLOQ: motivo**, que conta como não aprovado. Os exemplos ILUSTRATIVOS das Formulas valem como casos de teste. Fixture-base: `vel_heroi` 0,15 m/tick, `margem` 0,3, HP do herói 100, I = 9, R = 60, `contato_gap` 6, `cad_contato` 15.

### Regras (AC-R)

- **R1 [I]** **GIVEN** `FakeWorld` com herói, inimigos e um `FakeSistema8` que tenta gravar HP e posição, **WHEN** um tick roda, **THEN** só o #6 grava posição e HP (espião de escrita por sistema) e o `FakeSistema8` só enfileira. Com `CombatActive` falso: 0 escritas e todas as contagens regressivas ficam iguais.
- **R2a [U]** **GIVEN** o herói com recarga da esquiva = 1, **WHEN** `Esquivar` chega nesse tick, **THEN** o dash inicia (o timer decrementa antes do comando) e `recarga` = 60. **GIVEN** `Esquivar` no tick T e golpes de 5 de dano em T..T+9, **THEN** os de T..T+8 são descartados (9 ticks) e o de T+9 causa 5.
- **R2b [I]** **GIVEN** dois pedidos do #8 (A, B), impactos de elites id 5 e id 3, um contato e um auto-ataque, **WHEN** o passo 6 roda, **THEN** a fila é [A, B, impacto id 3, impacto id 5, contato, auto-ataque].
- **R2c [U]** **GIVEN** herói HP 30 e golpes de 20 e 15 no mesmo passe, **THEN** 7a soma acc = 35, 7b grava HP = 0 e `Kill` sai uma vez. **GIVEN** herói e chefe que morrem no mesmo passe, **THEN** os dois entram em `DeathsThisTick` em 7b.
- **R3 [U]** **GIVEN** alvo morto, dano NaN, infinito ou negativo, i-frames ativos ou alvo em Recuperação, **THEN**, respectivamente: descarte; descarte e `GolpesDescartados` +1; descarte e `Esquiva` 1× (só se o golpe descartado era telegraph, como na E8); dano × `mult_punicao`. Em todos, `Aplicar` só enfileira e o HP não muda antes de 7b.
- **R3b [U]** **GIVEN** 3 corpos de horda (HP 5, 5 e 40) e 1 elite (HP 100, em Recuperação) vivos, um `Rugido` por entidade, um pedido do #8 e um auto-ataque do herói que mataria o corpo de HP 5, no mesmo passe, **THEN** a fila é [`Rugido` ×4 por id, pedido do #8, auto-ataque]; em 7b os 4 vão a HP 0 com `Kill(id, Rugido)`, inclusive o corpo de HP 5 que o auto-ataque mataria, com `dano_aplicado` = HP; sem `Damage`, `Knockback` nem `HitStop` do rugido; `GolpesLimitados` = 0 e `GolpesDescartados` = 0; saem 1 evento agregado (`mortes` = 3; `acertos` e `danoTotal` só do auto-ataque) e 1 `Morte` do elite, e as colunas de telegraph do elite são zeradas no passo 8. **GIVEN** um `Rugido` para alvo já morto no início do passe, **THEN** descarte sem contar. **GIVEN** o herói em i-frames no tick do rugido, **THEN** nada muda no herói.
- **R4 [U]** **GIVEN** hostis a dist² 4 (id 7), 4 (id 9) e 9, e alcance² = 9 (inclusivo), **THEN** o alvo é o id 7. Sem alvo, o timer fica pronto e o primeiro tick com alvo ataca. Se o alvo morre no passe por outro golpe, o excedente se perde e a cadência fica gasta.
- **R5 [U]** **GIVEN** 5 inimigos prontos em contato, **WHEN** passam 60 ticks, **THEN** o herói recebe exatamente 10 golpes de contato (ticks 0, 6, …, 54), sempre do menor id pronto, e cada inimigo só repete após 15 ticks. Com i-frames o contato é anulado, o cooldown do inimigo é consumido e a janela de 6 ticks conta o pedido. Nenhum corpo é empurrado por colisão (a horda se sobrepõe).
- **R5b [U]** (sem contato de elite e chefe) **GIVEN** o herói parado, sobreposto (`d²` = 0) a um elite e a um chefe com a recarga de ataque não pronta, e um Soldado em contato, **WHEN** passam 60 ticks, **THEN** só o Soldado bate (`n_c` = 1: golpes nos ticks 0, 15, 30 e 45), o `contactCd` de elite e chefe fica 0 e o dano de contato deles é 0.
- **R5c [U]** (mira e encaixe da horda) **GIVEN** 64 corpos de horda em Perseguindo com ids 0 a 63, **THEN** o alvo de cada um é herói + `mira[id mod 32]` (≥ 32 alvos distintos; os ids i e i+32 têm o mesmo alvo). **GIVEN** um corpo a 0,01 m do alvo com passo de 0,1 m, **THEN** a posição vira exatamente o alvo, é finita e não muda nos 10 ticks seguintes com o herói parado. **GIVEN** um corpo a 0,5 m do alvo com passo de 0,1 m, **THEN** avança 0,1 m na direção do alvo, sem passar dele. **GIVEN** um corpo já no alvo (`dist²` = 0), **THEN** sem NaN. **GIVEN** um corpo parado no alvo com módulo da mira ≤ `alcance_contato_m`, **THEN** ele bate por contato (a distância é medida até o herói).
- **R6a [U]** **GIVEN** elite A = 24 e P = 30 que grava o Aviso no tick T, **THEN** o Impacto resolve em T+24, a Recuperação vai de T+25 a T+54 e volta a Perseguindo em T+55. Colunas: fase e `ticks_ate_dano` corretos a cada tick. Knockback ou comando nunca prorrogam nem reiniciam fases.
- **R6b [U]** **GIVEN** o herói que sai da área no Aviso e o elite empurrado no Aviso, **THEN** a área (origem, direção, raio) fica travada no início do Aviso. Herói fora no Impacto: 0 dano. Herói dentro: dano. Atacante morto em Aviso ou Recuperação: 0 Impacto e colunas zeradas no passo 8.
- **R6c [U]** **GIVEN** 4 elites prontos, **THEN** só 3 avisam, e o 4º espera (menor `prontoDesde`, depois menor id). **GIVEN** um Impacto em T+30 e `GAP` 11, **THEN** um Aviso novo (A = 24) pedido em T+8 espera e inicia em T+17 (Impacto em T+41). O chefe segue o ciclo de golpes dos dados, sem sorteio (índice no hash).
- **R6d [U]** **GIVEN** um Arremessador com recarga e graça prontas a 9 m do herói e `alcance_inicio_aviso_m` = 7 (`dist²` 81 > 49), **THEN** no tick T ele segue em Perseguindo e não ocupa slot; se o passo 5 de T o leva a `dist² ≤ 49`, o Aviso é gravado em T+1, e 7,0 m exatos vale (inclusivo). **GIVEN** dois elites prontos e só um dentro do alcance, **THEN** só ele disputa o slot, e o `prontoDesde` do outro não muda ao entrar depois. **GIVEN** um ciclo de chefe com golpes de alcance 5 e 7, **THEN** o 2º só começa com `dist² ≤ 49` e o ciclo não pula golpe. **GIVEN** o herói que sai do alcance depois de o Aviso começar, **THEN** o Aviso, a área travada e o Impacto seguem.
- **R6e [U]** (parada de elite e chefe) **GIVEN** um Campeão com `dist_parada_m` = 1 e 0,1 m/tick e o herói parado a 5 m, **THEN** ele anda e para com a distância final em [0,99; 1] (tolerância de float32), nunca 0, sem NaN, e não se move nos 10 ticks seguintes com a recarga não pronta. **GIVEN** `d²` = 1,0201 com `dist_parada_m` = 1, **THEN** o passo é `min(0,1; 1,01 − 0,99)` = 0,02 e a distância final é 0,99, sem passar da parada. **GIVEN** o herói na posição exata do elite (`d²` = 0), **THEN** o elite não anda e a direção travada do Aviso é (1,0), sem NaN. **GIVEN** um elite em Aviso, Impacto ou Recuperação e o herói em movimento, **THEN** a posição do elite não muda por movimento próprio (só por knockback e pelo deslocamento do golpe `linha` no Impacto).
- **R6f [U]** (golpe `linha`, a investida) **GIVEN** um Campeão em (0; 0), o herói em (5; 0) no tick de início do Aviso, `desloc_m` = 4 e `raio_golpe` = 0,6, **THEN** a linha trava em P0 = (0; 0) → P1 = (4; 0). **GIVEN** o herói em (3; 0,5) no Impacto, **THEN** leva dano (`dist²` 0,25 ≤ 0,36), mesmo que tenha andado para o lado da posição original; em (3; 0,7) (`dist²` 0,49) leva 0; em (4,5; 0) (`dist²` 0,25 na ponta) leva dano; em (4,7; 0) (0,49) leva 0. O Campeão termina o Impacto em (4; 0), com o `prev` mantido (deslize de 1 tick), e o knockback do herói tem a direção da linha. **GIVEN** o Campeão empurrado durante o Aviso, **THEN** a linha segue a travada e ele termina em (4; 0). **GIVEN** o atacante a 2 m da parede de frente para ela com `desloc_m` 4, **THEN** `P1` já sai limitado à arena na trava; com comprimento² < 1e-6 o teste é um círculo de raio 0,6 em `P0`. **GIVEN** o herói com i-frames no Impacto, **THEN** `Esquiva` e 0 dano.
- **R6g [U]** **GIVEN** um golpe em Recuperação, **THEN** o dano é × 1,5 (golpe comum), × 2,0 no 1º golpe `pesado` e × 2,0 em todo golpe se a Recuperação é `Aberto` (nunca o produto); a janela aberta tem ≥ 6 ticks.
- **R7 [U]** **GIVEN** um chefe nascido no tick 9 com `graca_ataque_ticks` = 0, **THEN** ele não age, não se move e não decrementa timer no tick 9, mas pode ser alvo e morrer. O primeiro Aviso inicia a partir do tick 10. Entidades de `Preparar` (`tickNascimento` 0) agem no tick 1.
- **R7b [U]** **GIVEN** um chefe nascido no tick 9 com `graca_ataque_ticks` = 60, alcance e recarga prontos desde o nascimento, **THEN** no tick 68 ele segue em Perseguindo (anda e é alvo) e o primeiro Aviso inicia no tick 69 (Impacto em 69 + A). **GIVEN** dois elites com graça 30 nascidos nos ticks 100 e 105, ambos com alcance e recarga prontos e só um slot de Aviso livre, **THEN** `prontoDesde` é 130 e 135, e o de menor `prontoDesde` (nascido no 100) vence o slot.
- **R8 [U]** **GIVEN** `Esquivar` com eixo (1,0) e `Ddash` 2,7, **THEN** o dash anda 0,3 m/tick por 9 ticks. Sem eixo usa `ultimaDirecao`, e sem ela, (0,1). Em T+59 o `Esquivar` é ignorado sem contar como rejeitado, e em T+60 é válido. Durante knockback, zera `kbVel`. Na parede o excedente se perde e recarga e i-frames não voltam. Dois i-frames não somam.
- **R9 [U]** **GIVEN** D = 1, K = 4 e resist 0,5, **THEN** os passos são 0,2 / 0,15 / 0,10 / 0,05 (total 0,5). Vence o novo knockback se `v0_novo > |v_atual|` (F3), com empate para o 1º da fila. O alvo morto em 7b não é empurrado. Vetor nulo vai a `EIXOS8[id mod 8]` (ids 0 a 7 dão 8 direções distintas). `Essencial` (resist 1) não gera evento. O elite fica 30 ticks (contados do tick em que o knockback foi aceito) imune a novo knockback. `poise_ticks` nunca anula dano.
- **R10 [U]** **GIVEN** eventos elegíveis nos ticks 100 e 110 e um elegível no 104, **THEN** o do 104 some (sem fila). Contato nunca emite `HitStop`; só golpe com o campo `pesado` ou com telegraph é elegível. `CombatTick` avança 1 por tick, e telegraph e simulação nunca congelam. Prioridade: sofrido > suprema > pesado, depois menor id.
- **R11 [U]** **GIVEN** HP que chega a 0 em 7b, **THEN** `Kill(id, causa)` sai 1×, `DeathsThisTick` traz id e causa, e nenhuma coluna de XP ou loot é escrita pelo #6. Herói morto encerra a tentativa (o `FakeSistema3` vê a morte), sem revive.
- **R12 [U]** **GIVEN** elite base 80 contra Tank (`mit_golpe` 0,4), **THEN** dano 48. **GIVEN** contato 4 contra Tank (`mit_contato` 0,4), **THEN** 2,4. **GIVEN** o DPS (mit 0), **THEN** o dano é integral.
- **R13 [U]** **GIVEN** 30 pedidos de 0,1f (taxa por tick) do `FakeSistema8`, **THEN** o HP final é igual à soma float32 em laço no teste. O #6 não reescala o dano, e o teste não exige "soma exata".
- **R14 [I]** **GIVEN** 300 mortes de horda e 1 do elite no mesmo tick, **THEN** saem 1 evento agregado de horda (`{mortes, acertos, danoTotal}`, só se algum valor > 0) e 1 `Morte` individual do elite, sem evento por acerto ou morte. Cada alvo individual tem 1 `Damage` por tick (a soma). **GIVEN** buffer de eventos sem espaço, **THEN** as colunas do telegraph continuam corretas (o #12 lê colunas, não eventos).
- **R15 [U]** **GIVEN** HP 30, HPmax 100, `Curar` 20 e golpe 35 no mesmo passe, **THEN** base 50 e HP' 15. **GIVEN** HP 95, HPmax 100 e `Curar` 20, **THEN** HP' 100. **GIVEN** alvo morto no início do passe, ou cura NaN, infinita ou negativa, **THEN** descarte e `CurasDescartadas` +1 (modo estrito lança). A cura não passa pela mitigação do Tank. O #3 pede `Curar` com `cura_levelup_pct × hpMax` no level-up. **BLOQ (só para o pedido real do #3): emenda do #3.**
- **R16 [I]** (oferta na hora) **GIVEN** um Aviso a 10 ticks do dano e o `FakeSistema16` abrindo a oferta (`CombatHold` = 1) no tick T por 200 ticks, **THEN** as colunas do telegraph ficam idênticas nos 200 ticks e, ao soltar o combate, o Impacto cai com 10 ticks restantes; o assembly do #6 não expõe `AvisoPerto` nem predicado de oferta. **BLOQ: #16 sem GDD** (vale com `FakeSistema16`).
- **R17 [U]** (buffer de esquiva) **GIVEN** `recarga` = 3 e `Esquivar` no tick T, **THEN** o pedido fica em `esquivaBuf` e o dash inicia em T+3, com o eixo lido em T+3. **GIVEN** `recarga` = 4, **THEN** o comando é ignorado, sem contar como rejeitado. **GIVEN** dois `Esquivar` guardados, **THEN** vale só um. **GIVEN** `CombatActive` falso, **THEN** o buffer fica congelado.
- **R18 [U]** (esquiva no limite) **GIVEN** um elite com Impacto em T e `Esquivar` em T−3 (`I − iframes` = 3), **THEN** o golpe é descartado, `Esquiva` sai 1×, a recarga vira 0 no mesmo passe e o elite fica `Aberto`. **GIVEN** `Esquivar` em T−4 (`I − iframes` = 4 > 3), **THEN** o golpe é descartado, sem reembolso e sem `Aberto`. Dois Impactos no mesmo passe reembolsam 1 vez por Impacto (a recarga continua 0). Contato anulado e auto-ataque descartado não reembolsam. `Aberto` zera no fim da Recuperação e na morte do atacante.
- **R19 [U]** (punição) **GIVEN** um elite em Recuperação e golpe de base 12, bônus 0,35 (`modDano` 1,35), **THEN** o auto-ataque comum causa **24,3**; o 1º golpe `pesado` **32,4**; o 2º `pesado` na mesma Recuperação **24,3** (`punidoPesado`); com a Recuperação `Aberto`, o comum e o `pesado` causam **32,4** (nunca 48,6); fora da Recuperação ×1. `punidoPesado` zera ao fim da Recuperação. Dois `pesado` no mesmo passe: só o 1º da fila leva ×2,0.
- **R20 [U]** (alvo do auto-ataque) **GIVEN** um elite em Recuperação a dist² 9 e um Soldado a dist² 4 (alcance² 16), **THEN** o alvo é o elite. **GIVEN** o elite fora da Recuperação, ou fora do alcance, **THEN** o alvo é o Soldado. **GIVEN** dois elites em Recuperação, **THEN** vale a menor dist², e no empate o menor id.
- **R21 [U]** (`mit` inválido) **GIVEN** `mit` NaN, **THEN** exceção nos dois modos. **GIVEN** `mit` 0,9 com `MIT_MAX` 0,6, **THEN** clamp (F1), sem exceção.
- **R22 [I]** (`curaPendente`) **GIVEN** `Curar` do #3 no tick T (depois do #6) e `CombatHold` = 1 de T a T+200, **THEN** `curaPendente` muda o `StateHash`, nada é curado nesses 200 ticks, e a cura entra em 7b do primeiro tick com `CombatActive`, limitada a `hpMax`. **BLOQ: ADR das colunas** (hash) **e emenda do #3**.
- **R23 [U]** (knockback no 1º tick) **GIVEN** D = 1, K = 4, resist 0,5 aceito no passo 8 do tick T, **THEN** o deslocamento é 0,2 em T+1, 0,15 em T+2, 0,10 em T+3 e 0,05 em T+4 (total 0,5; o `r` decrementa depois de aplicar).
- **R24 [U]** (vez do chefe) **GIVEN** um chefe pronto cujo Aviso cairia a menos de `GAP_IMPACTO` de um Impacto de elite já marcado, e dois elites prontos, **THEN** nenhum elite inicia Aviso enquanto o chefe espera, e o chefe inicia no primeiro tick em que o GAP permite. **GIVEN** o chefe e um elite prontos, o chefe vence o slot.
- **R25 [U]** (contato no hash) **GIVEN** dois golpes de contato pedidos a menos de 6 ticks, **THEN** só o 1º vale e `ultimoContatoTick` guarda o tick dele; mudar `ultimoContatoTick` muda o `StateHash`.

### Fórmulas (AC-F)

- **F1 [U]** Base 12, bônus 0,25 e 0,10, em Recuperação → **24,3** (tolerância 1e-4, e igualdade bit a bit com a mesma expressão float32). Elite 80 × Tank 0,4 → **48**. `mit` 0,9 com `MIT_MAX` 0,6 → clamp, dano 32. Base 12, bônus 0,25 e 0,10, 1º `pesado` em Recuperação → **32,4**. `mit` NaN → exceção. Dano > `DANO_MAX` → clamp e `GolpesLimitados` +1. `modDano` 0,99 → descarte.
- **F2 [U]** HP 30, 20 + 15 → HP' 0, `causa` = 2º golpe, `dano_aplicado` 30. HP 10, acc 9,995 (resto 0,005 < 0,01) → HP' 0 e `Kill`. Com cura: HP 30, HPmax 100, cura 20, dano 35 → base 50, HP' 15.
- **F3 [U]** D = 1, K = 4, resist 0,5 → D_ef 0,5, v0 0,2, soma **0,5 m**. K = 1 → v0 = D_ef, sem divisão por zero. Perde o excedente da parede e desliza no eixo livre.
- **F4 [U]** cad 15 × 0,75 → **11**. cad 15 × `0.7f` → **11** (literal float32). cad 3 × 0,25 → 1 (piso). `modCadencia` NaN ou fora da faixa mantém o último valor, com `ModForaDeFaixa` +1. Mudar o mod no meio da recarga não recalcula o timer em curso.
- **F5 [U]** Elite A = 24, raio 1,35, margem 0,3 → `ticks_para_sair` 11, passa. Raio 1,36 → 12 → exige A ≥ 25, reprova. Chefe A = 36, raio 3,15 com 0,15 m/tick → 23, passa; com o Tank a 0,12: raio 3,15 → 29, exige A ≥ 42 e reprova, e raio 2,46 → 23, passa. Elite com o Tank a 0,12: raio 1,35 → 14, reprova, e raio 1,02 → 11, passa. A conta é em `decimal` (1,65/0,15 = 11 exato).
- **F6 [U]** I = 6 recusa, R = I recusa. `Ddash` 2,7 sai do elite (1,65) e **não** do chefe (3,45). Esquiva 8 ticks antes do Impacto cobre; **9 ticks antes não cobre** (dano). Ciclo do elite 55 < R 60 (informativo).
- **F7 [U]** HP 100, contato 2,4 → n 42, **246 ticks**, passa. Contato 4 → n 25, **144**, reprova. Limite: contato < 100 × 6 / 240 = 2,5. Tank permite até ~4,16. `taxa_golpes_tick` com n_c = 1, 2, 3 e 10 → 1/15, 2/15, 1/6, 1/6.
- **F8 [U]** Emissões em 100 e 110 (`proximoHitStopTick` = 120). No 120, elegível com aviso a 10 ticks e herói a 1 m → suprimido, e `proximoHitStopTick` continua 120. O atacante morre; no 121 emite e `proximoHitStopTick` = 131. Máximo de 30/10 = 3 eventos/s.
- **F9a [U]** (elite, g = 0) DPS HP 100, base 60 → d_ef 60, n = 2, ttk **79**. Tank mit 0,4 → d_ef 36, n = 3, ttk **134**. Base 100 (n = 1) reprova. Base 50 no DPS (< 50,5) reprova pela margem de 1%. Base 99 (≥ 0,99 × HP) reprova pela margem de cima. Tank: `mit` 0,43 passa, 0,45 e 0,16 reprovam (janela ~0,18 a 0,43).
- **F9b [U]** (chefe A = 36, P = 36, g = 0, `base_chefe` 60, mesma HP) DPS n = 2 → ttk **109**. Tank n = 3 → ttk **182**.
- **F10 [U]** (`vel_heroi_min_tick` 0,12, o Tank) O exemplo T+30/T+32 → espera até T+17 com GAP 11. `GAP` < `max(I, ticks_para_sair)` é recusado. O elite de raio 1,02 tem `ticks_para_sair` 11 e reprova com GAP 9; raio 0,78 (ceil(1,08 / 0,12) = 9) passa com 9; raio 1,35 tem 14. A checagem é simétrica: um Aviso curto cujo Impacto cairia antes de um longo já marcado também espera.

### Casos de borda (AC-E)

- **E1 [U]** `cap_fila` = 4 com 5 pedidos → exceção nos dois modos e `Simulation` *Quebrada*. Nada é descartado em silêncio.
- **E2 [U]** Entidade viva com HP ≤ 0 no início do passe → exceção nos dois modos, sem `Kill` silencioso.
- **E3 [I]** `CombatActive` falso no tick 10 de 24 do Aviso, no 4º do dash e no 2º do knockback, por 1.000 ticks → colunas idênticas. Ao retomar, o Impacto cai com 14 ticks restantes, e dash e knockback terminam com o resto exato.
- **E4 [U]** Elite que morre no tick do próprio Impacto → o golpe vale (vivo no início do passe) e o herói perde HP. O chefe que morre no próprio Aviso gera 0 Impacto, e o `FakeSistema3` vê a morte do chefe no mesmo tick (o #6 só garante o contrato; a regra de `Vitoria` é do #3 real, no aceite do #3).
- **E5 [U]** O chefe `Essencial` leva o golpe com knockback → dano aplicado, 0 evento `Knockback`, posição inalterada.
- **E6 [I]** 300 mortes no mesmo tick → `DeathsThisTick` com 300 entradas por id crescente (0 descartes), 1 evento agregado, e a lista é limpa no tick seguinte.
- **E7 [U]** Modo estrito: dano NaN lança com tick e fonte. No modo normal, `GolpesDescartados` +1. `DroppedEvents` > 0 lança no primeiro. O início de telegraph usa a reserva.
- **E8 [U]** `Esquivar` no tick de um golpe já na fila → o golpe é descartado, sem dano, sem knockback e sem `HitStop`. `Esquiva` sai 1× por tick, só se o golpe era telegraph.
- **E9 [U]** `dano_final` 0 (empurrão do #8) → sem `Damage` e sem `Kill`, e o knockback vale.
- **E10 [U]** Dois elites prontos disputam o slot → vence o menor `prontoDesde`, depois o menor id. O slot de quem morre libera no tick seguinte.
- **E11 [I]** **GIVEN** o herói que morre no mesmo tick do level-up, **THEN** `Curar` é descartada (alvo morto), `CurasDescartadas` +1 e o `FakeSistema3` vê a morte (a derrota é do #3 real). **GIVEN** `Curar` e dano fatal no mesmo passe com cura suficiente, **THEN** o herói sobrevive com `base − acc`.

### Integração (AC-I)

- **I2 [I]** (#2) **GIVEN** `Simulation` real, **THEN** a ordem é #7, #8, #6, #3 por espião. `Kill` e `DeathsThisTick` usam a API do #2. **BLOQ: ADR das colunas do SimWorld** e a nota do #2 sobre a Regra 7 em dois tempos.
- **I3 [I]** (#3, `FakeSistema3`) Herói e chefe morrem no mesmo tick → os dois ids entram em `DeathsThisTick` no mesmo tick (o resultado `Vitoria` é do #3 real, no aceite do #3). Os ids e a causa chegam na linha do `xpValue`.
- **I7 [I]** (#7 falso) `FakeSistema7` faz nascer horda, elite e chefe com dados declarados, e o #6 executa o ciclo. **BLOQ (só para dados reais): #7 sem GDD.**
- **I8 [I]** (#8 falso) Ordem de enfileiramento preservada, `modDano` 0,99 descartado, `modCadencia` fora da faixa mantém o valor, e o #8 nunca grava HP. **BLOQ (só para o #8 real): #8 sem GDD.**
- **I12 [I]** Um leitor de colunas reconstrói fase, `ticks_ate_dano`, forma, raio e origem a cada tick, sem depender de evento. **BLOQ: ADR das colunas do SimWorld** (nomes e tipos).

### Determinismo e hash (AC-D)

- **D1 [I]** Duas execuções com a mesma seed e os mesmos comandos, 900 ticks, 300 inimigos + elite + chefe → `StateHash` idêntico em **todos** os ticks. **BLOQ: ADR-0001 em *Proposed* e ADR das colunas.**
- **D2 [I]** Trocar a ordem de dois pedidos do #8 cuja soma float32 difere por ordem muda o hash; o teste afirma antes que as duas somas diferem. **BLOQ: igual a D1.**
- **D3 [U]** Mudar qualquer campo do hash muda o `StateHash`: colunas hasheadas, `proximoHitStopTick`, recarga, dash, `ultimaDirecao`, cadência, kb, `poise`, `kb_refrat`, `prontoDesde`, índice do ciclo do chefe, área travada, `aberto`, `punidoPesado`, `esquivaBuf`, `curaPendente`, `ultimoContatoTick`. Mudar fila, `acc`, `vivoNoInicio`, contadores de diagnóstico ou supressão **não** muda. **BLOQ: ADR das colunas** (com `FakeWorld`, vale só a lista).
- **D4 [U]** Por analisador estático (`BannedApiAnalyzers`; reflexão não enxerga o corpo dos métodos): o assembly do #6 não usa `System.Random`, `UnityEngine` nem `double`, e não tem `static` mutável. Todo laço é por id crescente. A parte 'nascer em ordem embaralhada dá o mesmo hash' depende do hash (**BLOQ: ADR das colunas**, só essa parte).
- **D5 [PM]** O hash do tick 900 gravado no Editor é igual ao do aparelho (IL2CPP ARM64). **BLOQ: ADR-0001 *Proposed* e aparelho de referência não verificado** (VERSION.md).

### Desempenho (AC-P)

- **P1 [PM]** No aparelho de referência, em dois cenários: (a) 300+ vivos, 1 elite, 1 chefe e **3 avisos ativos ao mesmo tempo** (3 elites prontos e dentro do alcance, para o slot encher); (b) o pior tick: 300 mortes no mesmo tick (o rugido do chefe) com os 3 avisos. Em 600 ticks após 60 de aquecimento, registra **p95, p99 e o máximo**. No cenário (a): p95 ≤ **2,0 ms** (alvo) e p99 ≤ **4,0 ms** (12% do tick de 33,3 ms); no (b): o máximo ≤ `orcamento_combate_pior_tick_ms`, **sem valor até o X1 do #2 e o spike**. Todos os ms são provisórios, a confirmar no spike (`orcamento_combate_ms`). **BLOQ: aparelho de referência não verificado e spike inexistente.** No Editor vale só como sanidade.
- **P2 [I]** **GIVEN** 300 inimigos, fila a 80% de `cap_fila` e 300 mortes em 1 tick, **THEN** `GC.GetAllocatedBytesForCurrentThread` tem delta 0 em 600 ticks após aquecimento (arrays pré-alocados). PRONTO no Editor. No aparelho, o `ProfilerRecorder` "GC.Alloc" dá 0 B/tick **[PM]** (**BLOQ: aparelho**).

### Sinais de playtest, n = 1 (AC-S, não bloqueantes)

- **S1 [PM]** Em 5 encontros com elite como Tank, o autor anota no máximo 1 morte "não vi o golpe", registrando o tick e a fase do Aviso.
- **S2 [PM]** O hit-stop não esconde telegraph: o autor anota 0 vezes "perdi o aviso no travamento".
- **S3 [PM]** O autor acerta a esquiva no último instante (≤ 8 ticks antes do Impacto) em ≥ 7 de 10 tentativas.
- **S4 [PM]** Morte só por contato leva ≥ 8 s sem esquiva, e a horda derretendo lê como Descarga (autor: sim ou não).
- **S5 [PM]** O Tank abre o selo com ≤ 2 mortes de fase. **BLOQ: `docs/acceptance/mvp.md` inexistente.**
- **S6 [PM]** Em 5 elites, a suprema (ou um golpe pesado) está pronta durante a Recuperação em pelo menos 3: a punição típica não pode virar só auto-ataque × 1,5. **BLOQ: #8 sem GDD.**
- **S7 [PM]** Em 10 elites, o autor anota quantas vezes sair no limite (reembolso + `Aberto`) rendeu o 'devolvi com tudo' (meta ≥ 5 de 10) e se a esquiva reembolsada virou invulnerabilidade quase contínua (anotar a fração de i-frames; OQ-18).

**Critérios BLOQ (resumo):** I2, I12, D1, D2, D3, D5, P1, P2 (no aparelho), S5, S6, R15 (pedido real do #3), R16 (com o #16 real), R22, D4 (só a ordem embaralhada) e I7 e I8 com os dados reais. Os demais (R1 a R14, R17 a R21, R23 a R25, F1 a F10, E1 a E11, I3, D4 sem a parte do hash, P2 no Editor, S1 a S4 e S7) estão PRONTOS com `FakeWorld` e dublês. E4, I3 e E11 usam o `FakeSistema3`: provam o contrato do #6, não as regras do #3 real.

*Consultado:* `qa-lead`.

## Open Questions

| # | Pergunta | Dono | Quando |
|---|---|---|---|
| OQ-1 | ADR das colunas do `SimWorld` (#6 e #7): colunas hasheadas, scratch fora do hash, capacidades | `technical-director` | antes da primeira story do #6 |
| OQ-2 | **Resolvida em 2026-11-05:** nota na Regra 7 do #2 (dois tempos) e contadores nas Regras 14 e 10, aplicadas no #2 com autorização do autor | #2 | — |
| OQ-3 | `REACAO = 8` pode estar otimista: o jogador vê o Aviso ~2 ticks tarde e a folga do elite cai de 11 para ≈ 9; verificar a F5 com a latência de tela | #1 | spike no aparelho |
| OQ-4 | O hit-stop no teto ocupa 30% do tempo (N = 10, 3 por segundo, no limite da art bible); fotossensibilidade (≤ 3 por segundo para o que for grande) | #12 | playtest |
| OQ-5 | Orçamento de brilho do flash do elite e do rim da Recuperação (teto próprio medido) | art-director | medição no aparelho |
| OQ-6 | API de vibração do Android (`NOT SOURCEABLE`) | spike | antes do háptico |
| OQ-7 | Horda pode se sobrepor no MVP; rever depois do spike de performance **e nas fases de função (escoltar e proteger), onde sem bloqueio de corpo "o Tank segura" é só numérico** | autor | pós-spike e GDD do #20 |
| OQ-8 | **Substituída na re-revisão de 2026-11-05:** a oferta abre na hora, com contagem 3-2-1 na volta (Regra 16); sem `AvisoPerto`, F11 nem espera | autor | — |
| OQ-9 | Valores a calibrar: dano do elite e do chefe, `cad_s`, `alcance_auto_m`, `kb_d_m`, `mit_*` do Tank | #1, #7, #10 | protótipo |
| OQ-10 | Arena como retângulo alinhado aos eixos (suposição da F3) | #7 e nível | GDD do #7 |
| OQ-11 | O `Ddash` não cobre a área do chefe: só o timing e a caminhada; reavaliar com o sinal S1 | autor | playtest |
| OQ-12 | A janela de `mit_golpe` do Tank na F9 é estreita (≈ 0,18 a 0,43 com HP 100); mudar só o HP a quebra | #10 e #1 | balanceamento |
| OQ-13 | Duração do dissolve da horda (8 a 10 ticks) | art-director e #12 | spike visual |
| OQ-14 | Orçamento do `Tick` do #6 (`orcamento_combate_ms`: p95 2,0 ms, p99 4,0 ms) | `performance-analyst` | spike de performance |
| OQ-15 | Frequência da suprema (#8) contra a frequência de elites: se a suprema raramente estiver pronta na Recuperação, a punição típica vira auto-ataque × 1,5 e a fantasia "devolvi com tudo" murcha (sinal S6) | #8 | GDD do #8 e playtest |
| OQ-16 | Emendas no #3 (somar `curaPendente` no level-up), no #16 (abrir a oferta na hora, contagem 3-2-1, listar o #6 como Soft) e no #7 (a F11/`aviso_perto` saiu; o registro marcava o #7 como referência) | #3, #16 e #7 | antes do re-review do #3, do #7 e do GDD do #16 |
| OQ-17 | Sinal visual do `Aberto` (rim mais forte e marca da punição ×2,0) fora da família de cor do flash da horda | art-director | medição no aparelho |
| OQ-18 | Reembolso da esquiva no limite (`lim_esquiva_ticks` = 3): medir a cobertura de i-frames com 3 elites (≈ 49% no pior caso) e se vira invulnerabilidade quase contínua; ajustar `lim` ou limitar a 1 reembolso por N ticks | autor | playtest S3 e S7 |
| OQ-19 | Duração e apresentação da contagem 3-2-1 da oferta (≥ 19 ticks, sob `CombatHold`) pertencem ao #16 e ao #2 | #16 | GDD do #16 |
