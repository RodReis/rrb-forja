# Horda, waves e inimigos (#7)

> **Status**: In Review (2ª passada de `/design-review` em 2026-11-05: NEEDS REVISION, revisado na mesma sessão; sem 3ª conferência, pelo limite de 2 passadas do projeto)
> **Author**: Rodrigo Reis + agentes (game-designer, systems-designer, ai-programmer, level-designer)
> **Last Updated**: 2026-11-05
> **Last Verified**: 2026-11-05
> **Implements Pillar**: P4 *Massacre com peso* (hordas derretem, elites batem forte, o perigo é sempre legível) e P1 *Sua build, sua assinatura* (a horda é o teste em que a build aparece; a pressão é autoral, nunca adaptada à build)
> **Creative Director Review (CD-GDD-ALIGN)**: REVISED 2026-11-05 — CONCERNS 1 a 5 aplicados (rugido mata o elite vivo; sinal de XP do rugido (hoje `RugidoMuitosNiveis`); S1 com o Tank; Arremessador só inicia Aviso na área visível; pilar do cabeçalho corrigido de P2 para P1). O diretor leu o GDD inteiro, linhas 1 a 754.

## Summary

A Horda, waves e inimigos (#7) decide quem o jogador enfrenta em cada fase, quando e de onde: um cronograma autoral de waves de horda comum, elites que chegam no respiro, um por vez, e o chefe que fecha a fase com um rugido que limpa a arena. A composição de cada wave é sorteada por seed, sempre a mesma para a mesma seed. O jogador sente a "maré e a lâmina": dezenas de corpos fracos que derretem e empurram a posição dele, e um perigo com nome que avisa antes de bater. É o sistema que dá à fase o seu ritmo, a sua dificuldade crescente e o único inimigo cuja morte vence a fase. Ele só faz nascer e declara os dados de cada arquétipo; quem move e mata é o Combate.

> **Quick reference** — Layer: `Feature` · Priority: `MVP` · Key deps: `#1 Dados e balanceamento (Hard), #2 Simulação determinística (Hard), #6 Combate e dano (Hard); #3 Fluxo de fase lê o chefe, o XP e o tick de entrada`

## Overview

A Horda, waves e inimigos (#7) decide **o que o jogador enfrenta, quando e em que quantidade** em cada fase: o cronograma de waves, a composição de cada wave (sorteada por seed a partir de listas autorais), os arquétipos de inimigo (horda comum, elite e chefe), onde cada um nasce e a densidade que cresce de fase em fase, até o chefe que fecha o cronograma. O jogador não opera esse sistema: ele o sente como pressão. É a maré de dezenas de inimigos fracos que derrete sob o auto-ataque, o elite que surge e marca no chão um golpe a esquivar, e o chefe cujo padrão de telegraph é novo a cada capítulo. Ele existe porque sem ele não há fase: é dele a dificuldade, o ritmo de 3 a 5 minutos e o único inimigo `Essencial` cuja morte vence a fase. O #7 só faz nascer e declara os dados de cada arquétipo (velocidade, XP, ciclo de golpes, dano de contato, quantos e quando); quem move, acerta e mata é o #6, e quem lê as mortes para dar XP e encerrar a fase é o #3. Roda primeiro em cada tick da simulação determinística (#2): a composição de uma wave depende só da seed, do índice da wave e dos dados, nunca do que o jogador abateu, o que permite reproduzir uma fase pelo log e validar o auto-battle. Toda contagem e toda densidade são Tuning Knobs, porque o spike de performance no Android intermediário (cerca de 300 inimigos ativos, VFX no máximo, no minuto 20) pode mudá-las sem reescrever regra. As decisões de implementação (sorteio por índice de wave, colunas do `SimWorld`) estão no ADR-0001 e não neste GDD.

## Player Fantasy

**Enquadramento:** direto. O jogador sente este sistema a cada segundo da fase, mesmo sem nunca operá-lo.

**Pilar 4, *Massacre com peso*:** "Hordas derretem, elites batem forte, e o jogador sempre consegue ler o perigo." **Pilar 1, *Sua build, sua assinatura*:** a horda é o teste em que a build aparece.

**"A horda não quer te matar. Quer saber do que a sua build é feita."** A horda é a bigorna da Forja: cada wave mais densa é mais uma martelada, e a build aguenta ou racha. Dentro da fase, essa pressão tem dois ritmos, e o #7 é dono dos dois: **a maré e a lâmina.**

- **A maré** é a horda comum: volume, nunca precisão. Ela não telegrafa, é visualmente simples (hierarquia do detalhe da arte) e só causa dano por contato. No MVP o contato do #6 satura com poucos corpos (`dps_contato_max`) e a horda se sobrepõe, então a densidade **não é pressão de dano**: é **espetáculo, XP e cobertura** para a build mostrar o que faz *(decisão do autor, 2026-11-05, /design-review, 2ª passada)*. Nas fases densas, a pressão vem de **mais frentes ao mesmo tempo**, que obrigam o jogador a se mover. É a fonte da **Descarga**: dezenas de corpos caindo de uma vez.
- **A lâmina** é o elite e o chefe: precisão, nunca volume. Nasce com nome, marca no chão o golpe que vai dar e mata quem não lê. É a fonte da **Tensão**.

**Momento-âncora:** a wave cai em cascata sob o auto-ataque, vem um respiro de dois segundos com a tela quase vazia, e o chão se marca sob o elite que acabou de nascer. O jogador entende antes de pensar: *quando a tela esvazia, alguém grande está chegando.* No minuto 1 a build mal limpa a tela; no minuto 3, com o dobro de corpos, ela varre tudo, e então o elite entra para cobrar se ela também sabe se defender.

**"A quantidade é ruído que cai; o perigo tem nome."** Esta é a regra que a fantasia impõe ao design do #7: **a densidade cresce em corpos, não em ameaças simultâneas.** A Descarga é a recompensa por ter lido certo, nunca o ruído que esconde a lâmina. Entre "mais corpos" e "elite legível", o Pilar 4 já decidiu: elite legível. O teto de golpes telegrafados ao mesmo tempo já existe no #6 (`max_avisos`, F10 `intervalo_entre_impactos`); o #7 controla a outra metade, quando e quantos elites nascem (Core Rules e Tuning Knobs).

**O chefe que se aprende** *(confirmado pela Regra 3: ciclo fixo, roteiro determinístico da Regra 10 do #3)*: "a horda nunca é a mesma; o chefe sempre é." A seed muda a cada tentativa, então a maré se lê e não se decora. O chefe repete o mesmo ciclo de golpes, e a terceira tentativa é diferente da primeira: o jogador reconhece o padrão antes de o telegraph terminar e já está fora da área. Cada capítulo traz um padrão novo de chefe (conceito, Flow State Design), e é ali que o domínio se renova.

**O que esta fantasia não é** (e o #7 não promete):
- **Não é a sensação do golpe.** Impacto, dano, hit-stop e explosão em cadeia são do #6 e do #12. O #7 promete a **quantidade e o momento**, não o peso de cada acerto.
- **Não é caos imprevisível nem horda infinita.** Inimigo que nasce em cima do herói ou sem leitura quebra o Pilar 4, e a fase tem fim: o chefe fecha o cronograma.
- **Não é horda que se derrete sozinha.** A tela só se limpa se a build mata; movimento e esquiva continuam manuais (anti-pilar do auto-battle). A maré **não** promete empurrar a posição do jogador por dano, porque o contato satura (#6). A promessa é de **frentes**: mais direções de chegada nas fases densas, que o jogador precisa ler e contornar *(decisão do autor, 2026-11-05, /design-review, 2ª passada; OQ-16: se o playtest mostrar que o dano por minuto na fase 5 não passa o da fase 1, pedir bloqueio de corpo ou separação ao #6)*.
- **Não é horda que se adapta à build.** Dificuldade dinâmica pune a build bem feita e esvazia os Pilares 1 e 2. A pressão é autoral por fase, para a build forte se sentir forte.
- **Não é a fantasia da trindade.** Escolta, fases de função e dungeon com grupo ficam fora do MVP; no MVP o Tank enfrenta a horda sozinho.

*Consultado:* `creative-director` (escolhido o enquadramento B, "Maré e lâmina", com a frase de abertura de A, "a horda é a bigorna"; o C, "o chefe que se aprende", entra como parágrafo provisório).

## Detailed Design

### Core Rules

> **Marca de provisório.** Toda regra marcada *(provisória)* foi decidida por recomendação de especialista (`game-designer`, `systems-designer`, `ai-programmer`, `level-designer`), não pelo autor, e deve ser reavaliada com o jogo avançado (depois do spike de performance e do protótipo). As marcadas *(decisão do autor, 2026-11-05)* foram escolhidas pelo autor. O resto vem dos GDDs #1, #2, #3 e #6 ou do ADR-0001. Os números são valores iniciais e knobs do #1, nunca fixos no código.

1. **Papel e dono dos campos.** O #7 é um `ISimSystem` que roda **primeiro** na ordem do compositor (#7 → #8 → #6 → #3 → #16, Regra 5 do #2). Ele só age com `ctx.CombatActive`, e todo tempo dele conta em `CombatTick` (confirma a OQ-10 do #2 do lado do #7: o tempo de escolha de carta não conta para waves). O #7 **só faz nascer** (`SimWorld.Spawn`) e **declara os dados de cada arquétipo**; depois do nascimento ele nunca escreve posição nem HP (o #6 é o único escritor, Regra 1 do #6). Todo laço é por índice crescente; sem `static` mutável, sem `UnityEngine`, só `float` fracionário e contagens em `int`, sem alocação gerenciada por tick (ADR-0001).

2. **Arena.** Cada fase acontece numa **arena retangular alinhada aos eixos**, sem obstáculos no MVP, com largura e altura em metros declaradas por fase (`arena_largura_m`, `arena_altura_m`; ilustr. cerca de 2,5 × 2 telas) *(decisão do autor, 2026-11-05: arena fechada de algumas telas, câmera segue o herói; o tamanho é provisório)*. Isso confirma a suposição da F3 do #6 (OQ-10 do #6). O #6 limita todo movimento à arena; o #7 garante que todo nascimento cai dentro dela (Regra 7). A câmera é do #4.

3. **Arquétipos.** Um arquétipo é uma definição do #1 com ID estável e uma **classe**: `Horda`, `Elite` ou `Chefe` (a coluna `classe` que o #6 já lê). Cada arquétipo declara: velocidade (`vel_per_s`), HP, `xpDaMorte` (inteiro ≥ 0), `resist_knockback`; só a `Horda` declara **dano de contato** (`dano_contato`); e, para `Elite` e `Chefe`, o **ciclo de golpes** (lista ordenada de golpes do #6, cada um com forma, raio, `A`, `P`, base, `pesado`, knockback e `alcance_inicio_aviso_m`), a **graça de ataque** (`graca_ataque_ticks`, Regra 9) e a **distância de parada** (`dist_parada_m`, parágrafo Comportamento). A **horda comum nunca telegrafa**: ela só causa dano por contato (Player Fantasy, "a maré não telegrafa"). **Elite e chefe não causam dano por contato**: só batem com golpe telegrafado, porque "a lâmina avisa antes de bater" *(provisória; emenda (h) aplicada na Regra 5 do #6 em 2026-11-05)*. O ciclo do chefe é fixo, sem sorteio (Regra 6 do #6), e é o mesmo em todas as tentativas, para o jogador poder aprendê-lo *(confirma a Regra 10 do #3)*. Os dados de um arquétipo podem variar por fase (HP do chefe de fase, golpes do Campeão), declarados por fase no #1 *(provisória)*.
   **Todo ciclo de elite e de chefe tem pelo menos um golpe que alcança um herói em fuga** (a investida ou uma área sob o herói), para o herói não conseguir fugir do ciclo para sempre; o #1 valida pela marca `alcanca_fuga` do golpe (F10) *(provisória)*.
   **Elenco do MVP** *(provisória)*:

   | Arquétipo | Classe | Papel | Entra na |
   |---|---|---|---|
   | Soldado | Horda | base; velocidade e HP médios | fase 1 |
   | Enxame | Horda | rápido, frágil, pouco XP | fase 2 |
   | Bruto | Horda | lento, resistente, contato maior | fase 3 |
   | Campeão | Elite | **investida** curta e telegrafada; a partir da fase 2, também golpe corpo a corpo em círculo | fase 1 |
   | Arremessador | Elite | golpe em área marcada **sob o herói** a distância, travada no início do Aviso; é golpe telegrafado do #6, **sem projétil** (projétil não é entidade, decisão registrada na FS9 do #2) | fase 4 |

   **Investida do Campeão** *(decisão do autor, 2026-11-05, /design-review)*: o Aviso marca uma **linha** do Campeão na direção do herói, travada no início do Aviso; no Impacto o Campeão se desloca ao longo dela (o deslocamento é dado do golpe, executado pelo #6) e causa dano na linha. Na fase 1 o ciclo do Campeão tem **só a investida**, para a fase 1 ter um único tipo de telegraph; o golpe em círculo entra a partir da fase 2 (dado do arquétipo por fase) *(a divisão por fase é provisória; emenda (g) aplicada no #6 em 2026-11-05, Regra 6: golpe `linha` com `desloc_m`)*.
   | Chefe de fase | Chefe | um elite-chefe reaproveitado nas 5 fases; entre fases mudam só dados (HP, por exemplo), nunca o ciclo | fim de toda fase normal |
   | Chefe de capítulo | Chefe | arquétipo próprio, com um padrão de telegraph novo | fim da fase de capítulo |

   **O Arremessador só inicia um Aviso se estiver dentro da área visível** *(decisão do autor, 2026-11-05, após o CD-GDD-ALIGN; exige uma linha na passagem Perseguindo → Aviso do #6, exigência (e))*. A pose orientada dele é a única ligação entre causa e efeito, então o jogador sempre vê quem arremessou. Como medir a área visível *(provisória, a reavaliar quando o #4 definir a área visível)*: `meia_altura_visivel_m` é o menor meio-lado da área visível com a câmera centrada no herói (ilustr. 8; no retrato, a meia largura), e `margem_visivel_m` é uma folga para dentro da borda (ilustr. 1). **Todo golpe de elite e de chefe** declara `alcance_inicio_aviso_m` ≤ `meia_altura_visivel_m − margem_visivel_m`, validado pelo #1 (F10), e só inicia Aviso com `dist² ≤ alcance_inicio_aviso_m²`. A regra antiga, "até `R_spawn_m`", estava errada: `R_spawn_m` fica fora da tela por definição (Regra 7.6). Como o elite nasce a `R_spawn_m`, fora da tela, essa condição também garante que **o primeiro Aviso de qualquer elite começa na tela**, mesmo se a graça (Regra 9) passou com ele ainda fora da câmera.

   Nenhum inimigo da horda comum ataca à distância: teria de telegrafar (quebra "a maré não telegrafa") ou bateria sem aviso (quebra o Pilar 4).

4. **Cronograma da fase (dado autoral).** Cada fase traz um cronograma finito: uma lista de **entradas** ordenada por (`inicio`, `w`). Cada entrada declara:
   - `w`: inteiro ≥ 0, **único na fase e explícito** (não é a posição na lista), para que inserir uma entrada no meio não mude a composição das outras durante o balanceamento (resolve a OQ-9 do #2 do lado do #7; o #1 valida);
   - `inicio_s`: instante em segundos de combate, convertido pelo #1 para `CombatTick`;
   - `tipo`: `Horda`, `Elite` ou `Chefe`;
   - `pool`: pares (arquétipo, peso inteiro ≥ 1), só da classe do tipo;
   - `contagem`: inteiro ≥ 1, **fixo** (não uma faixa: a variedade entre seeds vem da composição e da posição, e assim o total de spawns, o pico e o XP da fase são números, não intervalos) *(provisória)*;
   - `espalhar_s` (só `Horda`): duração do pulso; o corpo `k` da entrada nasce no tick `inicio + floor(k × espalhar_ticks / contagem)`, para a wave chegar em fluxo e não como bloco (ilustr. 4 a 8 s) *(provisória)*;
   - `frentes`: quantas direções de chegada a entrada sorteia (de 1 até `contagem` e no máximo `N_DIR`; Regra 7) *(provisória)*;
   - só no `Chefe`: a **escolta** (Regra 11).

   Toda entrada `Elite` tem `contagem` = 1 e `frentes` = 1: um elite por entrada, porque a regra de um elite vivo por vez (Regra 9) conta entradas *(provisória)*.

   A **última entrada é sempre o `Chefe`**, com `contagem` = 1, pool de um único arquétipo de classe `Chefe`, e `inicio` **estritamente maior** que o fim de todas as outras entradas. Nada é agendado depois dele, a não ser a escolta. O instante do chefe é o `tick_entrada_chefe_agendado` que o #3 lê (Regra 7 do #3).

5. **Ritmo da fase: waves, respiros e elites.** As batidas são relógio puro *(decisão do autor, 2026-11-05: waves só pelo relógio, nada adianta por abate)*. Uma **wave** é uma entrada `Horda`. Um **respiro** é um intervalo em que nenhuma entrada `Horda` está em pulso; ele não é uma entrada, é o espaço entre elas. **A fase é uma maré quase contínua** *(decisão do autor, 2026-11-05, /design-review, 2ª passada)*: 8 a 10 waves por fase, com respiro entre pulsos de no máximo `respiro_max_s` (ilustr. 10 s); o respiro longo só aparece antes do elite e antes do chefe, e esses dois não acendem o sinal `RespiroLongo`. Toda entrada `Elite` cai **dentro de um respiro**, para a tela esvaziar antes de o elite chegar. O respiro conta **da chegada**, não do último nascimento: o último corpo de uma wave nasce a `R_spawn_m` (mais a formação) e ainda leva o tempo de viagem até o herói (`viagem_ticks`, F10, com o arquétipo mais lento do pool). Por isso o `inicio` do elite fica a pelo menos `fim_pulso + viagem_ticks + respiro_elite_min` de toda `Horda` anterior. **O elite tem duelo garantido, não abate garantido** *(decisão do autor, 2026-11-05, /design-review, 2ª passada: o abate depende da build, Pilar 1)*: a próxima `Horda` só começa `duelo_min_ticks` depois do nascimento do elite (a graça mais um ciclo completo de golpe do elite, F10), e o elite precisa de mais `duelo_min_ticks` antes do silêncio do chefe. Antes do chefe há um respiro longo (`silencio_pre_chefe_s`), também contado da chegada do último corpo. O Tank aceita respiros mais curtos porque mata mais devagar, mas **um elite nunca nasce no meio de um pulso de horda** (Regra 9). A forma de uma fase típica (8 a 10 waves, 1 a 3 elites, cerca de 2,5 a 3,5 minutos até o chefe: uma fase de 150 s com 10 waves de 6 s tem vãos médios de cerca de 9 s; fases mais longas pedem pulsos mais longos, `espalhar_s` até 12 s, não mais respiro) e a curva das 5 fases ficam nos dados e na Seção Tuning Knobs, não em regra *(provisória)*.

6. **Sorteio da composição, todo antes do tick 1.** O #7 implementa `IPreparaFase` e, no `Preparar` (depois do #3, antes do 1º `Tick`), sorteia a fase inteira: para cada entrada, na ordem de `w`, cria o gerador da wave da FS6 do #2 (`Pcg32(seed_w, seq = w)`) e sorteia, nesta ordem, `contagem` arquétipos (sorteio ponderado por pesos inteiros: soma dos pesos e `NextBounded` pela FS5 do #2, com o pool percorrido por ID de arquétipo crescente, para que reordenar o arquivo não mude o sorteio) e `frentes` índices de direção (`NextBounded(N_DIR)`). **O sorteio do arquétipo acontece mesmo com pool de um só arquétipo**, como a FS5 faz com `n = 1`: assim, acrescentar um 2º arquétipo a um pool não desloca as direções já sorteadas *(provisória)*. A escolta do chefe usa o mesmo gerador da entrada `Chefe` (`escolta_total` arquétipos e depois uma direção por pulso); o chefe em si não consome sorteio (pool de um arquétipo de classe `Chefe` e direção fixa nos dados). F3 dá o número exato de sorteios. O resultado é uma **tabela de composição imutável**, pré-alocada com Σ `contagem` linhas (mais a escolta). O número de sorteios depende só de (`seedMestre`, `w`, dados), e nenhum gerador atravessa ticks: a composição nunca depende de abates, vivos, HP, posição ou tick (FS6). A tabela é derivada da seed e dos dados e **não entra no hash**; entram só os cursores (Regra 13) *(provisória; exige ajustar a frase do #2 "waves que nunca começam não criam gerador", Edge Cases do #2)*.

7. **Onde cada inimigo nasce.** A posição **não é sorteio**: é uma função pura do índice de direção já sorteado, da posição do herói e da arena, aplicada no tick do nascimento *(provisória)*.
   1. O #1 guarda uma tabela de `N_DIR` direções unitárias (ilustr. 16) como literais `float`, validadas com módulo entre 0,99 e 1,01. Não há `sin` nem `cos` (ADR-0001).
   2. Para a frente com direção `d`, o ponto é `p = herói + d × R_spawn`, com a posição do herói lida no início do passo do #7 (a do fim do tick anterior, porque o #7 roda primeiro).
   3. **Espelhamento por eixo:** se `p.x` sai da arena, usa-se `herói.x − d.x × R_spawn`; o mesmo para `y`. A distância ao herói continua `R_spawn·|d|` (de 0,99·R a 1,01·R), sem raiz quadrada. Assim, com o herói encostado num canto, a horda nasce para dentro, nunca fora da arena nem em cima dele. O #1 recusa a fase se a arena não tiver largura e altura ≥ `2,02 × R_spawn + margem_spawn_m` (F5; o fator 2,02 cobre um componente de direção de até 1,01).
   4. **Frentes distintas depois do espelho** *(provisória)*: no canto, duas frentes podem espelhar para a mesma direção. A direção espelhada `e_f` da frente `f` é uma função pura de (entrada, `f`, posição do herói no início do passo). Para a frente `f` ela é comparada com a `e_g` de **todas** as frentes `g < f` da mesma entrada, **tenham ou não corpo nascendo neste tick** (leitura única: nada depende de quais frentes têm corpo agora). Duas direções espelhadas são iguais quando têm o mesmo **id de classe de vetor**, um inteiro que o #1 pré-computa em `decimal` para cada (índice, espelho em x, espelho em y), nunca por igualdade de `float`. Se `e_f` for igual a alguma `e_g` (já com o avanço de `g` aplicado), o índice de direção de `f` avança de forma cíclica (`idx + 1 mod N_DIR`) até ficar diferente, no máximo `N_DIR` passos e sem sorteio novo; o avanço vale só para o corpo que está nascendo (é recalculado a cada tick); se nenhuma for diferente, fica a original (F4). **A garantia é "até onde houver direções distintas":** num canto, 16 direções viram só 5 espelhadas distintas, então `frentes` perto das paredes pode repetir, e o caso vai ao log (`TicksNoCanto`). A escolta não deduplica (cada pulso é uma frente de um corpo). **A frente não é ancorada no mundo:** como a câmera segue o herói, a frente é lida relativa ao herói; com o herói andando junto à parede, corpos da mesma frente podem alternar entre `+d` e `−d` entre ticks *(aceito e medido no protótipo; arbitragem da 2ª passada)*.
   5. Os corpos de uma mesma frente somam um deslocamento de formação tirado de uma tabela fixa por índice dentro da frente (sem sorteio), são limitados à arena e, se ficarem a menos de `R_min_spawn` do herói (distância ao quadrado), nascem no ponto da frente sem deslocamento.
   6. `R_spawn` fica, por padrão, fora da área visível com a câmera centrada. A **garantia firme é a distância mínima** `R_min_spawn`, não "fora da tela" (o proxy testável hoje é a F5: `R_spawn_m ≥ meia_altura_visivel_m + margem_visivel_m`): com a câmera parada numa borda, um nascimento pode ser visível, e o #12 desenha um surgimento curto.
   7. Uma frente com várias chegadas lê como uma **frente de corpos**, não como uma nuvem uniforme (Player Fantasy).
   **O chefe nasce dentro da tela** *(decisão do autor, 2026-11-05, /design-review: o rugido acontece à vista)*: usa a mesma regra de direção e espelho, com o índice de direção **fixo nos dados** (`dir_chefe`, sem sorteio) e o raio `R_chefe_m` no lugar de `R_spawn`. A F5 exige `R_min_spawn_m ≤ 0,98 · R_chefe_m` e `1,01 · R_chefe_m ≤ meia_altura_visivel_m − margem_visivel_m` (Regra 3) *(o fator 1,01 cobre o módulo de `d`; provisória)*.

8. **Teto de vivos da horda: quem não cabe espera.** O #7 mantém a horda comum viva até `teto_vivos_horda` (por fase, ilustr. igual ao alvo de performance de cerca de 300). Em cada tick ativo, `vagas = max(0, teto_vivos_horda − vivos_horda)`, em que `vivos_horda` é a contagem de vivos de classe `Horda` na lista de vivos do `SimWorld`. `vivos_horda` e "há elite vivo" (Regra 9) são calculados no início do passo por **uma única passada local** sobre a lista de vivos (n ≤ 303, F8), em variáveis locais que também sobem a cada `Spawn` do próprio passo; não há coluna nem contador no `SimWorld` *(arbitragem da 2ª passada: O(n) em microssegundos tira a dependência do ADR das colunas; a reavaliar no spike, AC-P3)*. A tabela de composição da horda é ordenada no `Preparar` por (`tick_do_corpo`, `w`, `k`) (F1), por chave `long` composta e sem comparador genérico sobre struct (ADR-0001, IL2CPP), para que pulsos sobrepostos de duas entradas não prendam o corpo 0 da segunda atrás do resto da primeira, e a fila de espera continue sendo um prefixo a partir do cursor *(provisória)*. Nascem, nessa ordem, até `min(vagas, max_nascimentos_por_tick)` corpos de horda cujo tick já venceu (F6); os demais **esperam** e nascem nos ticks seguintes, na mesma ordem, quando abrir vaga *(decisão do autor, 2026-11-05; o limite por tick é provisório e vale para horda e escolta, não para elite e chefe, e não muda a composição)*. Ninguém é descartado antes da entrada do chefe: o jogador que mata devagar (o Tank) recebe a horda em fluxo contínuo e consegue todo o XP dos corpos que nascem, o que ataca a espiral "mata devagar, sobe menos, fica mais fraco". Corpos e elites que ainda esperam quando o chefe entra são cancelados sem XP (Regra 10.3); esse risco é medido pela F11 e pelo S2. O Tank fica com o XP inteiro de cada morte que ele causa *(decisão do autor, 2026-11-05, /design-review)*. O teto é fixo por fase e não lê a build, então não é dificuldade dinâmica. Só o **momento** do nascimento depende dos abates; a composição e o número de sorteios, não (FS6). **Elite e chefe nunca esperam por este teto.**

9. **Elite: uma lâmina por vez.** Quando vence o `inicio` de uma entrada `Elite`, o elite nasce **se nenhum outro inimigo de classe `Elite` estiver vivo**; senão ele **espera**. O elite só atrasa, nunca adianta, e entradas `Elite` nascem na ordem (`inicio`, `w`) *(decisão do autor, 2026-11-05)*.
   **Elite atrasado espera a próxima janela de respiro** *(decisão do autor, 2026-11-05, /design-review)*: um elite que esperou por outro elite vivo não nasce no meio de uma wave. Ele nasce no primeiro tick ativo `t` em que nenhum elite está vivo **e** `t` está numa **janela de respiro do cronograma**. A janela é calculada no `Preparar`, só dos dados (nunca lê a build), **por entrada `Elite`** (a graça e o duelo dependem do arquétipo sorteado) e guardada como intervalos inteiros: é todo tick `t` que passaria em `respiro_elite_ok` (F10) se o elite tivesse `inicio` = `t`, com `t ≤ inicio(C) − silencio_pre_chefe_ticks − duelo_min_ticks(E)` *(provisória)*. Como a F10 põe o `inicio` de todo elite numa janela, o elite que não esperou nasce no `inicio`, como antes. **Nunca nasce no meio de uma wave** *(decisão do autor, 2026-11-05, /design-review, 2ª passada)*: não há teto de segurança. Se não houver janela até o limite acima, o elite é **cancelado** na entrada do chefe (Regra 10.3), conta em `ElitesCancelados` e não dá XP. Para isso não virar rotina, a F10 exige que cada entrada `Elite` tenha uma janela de largura mínima `janela_reserva_ticks` (ilustr. 90 = 3 s) e que, entre dois elites consecutivos, exista janela de reserva para o segundo depois do duelo do primeiro (`reserva_ok`). A espera não é estado novo: sai de `CombatTick − inicio` e do cursor. Depois de nascer, elite e chefe só podem iniciar o primeiro Aviso a partir de `tickNascimento + graca_ataque_ticks` (ilustr. elite 30, chefe 60), para serem vistos antes de atacar *(provisória; emenda (a) aplicada na Regra 7 do #6 em 2026-11-05, que antes só pulava o tick do nascimento; usa a coluna `tickNascimento`, sem estado novo)*.

10. **Entrada do chefe e rugido.** No tick em que vence o `inicio` da entrada `Chefe`, nesta ordem *(decisão do autor, 2026-11-05: rugido com XP)*:
    1. O chefe nasce por `Spawn(essential = true)`, no ponto da Regra 7. Ele **nunca espera**: nem pelo teto de vivos nem por elite vivo. Assim o `tick_entrada_chefe_agendado` é exato, e `ChefeAusente` (Regra 7 do #3) volta a ser só bug de dado. Um `Spawn` essencial rejeitado encerra a simulação com `EssentialSpawnRejected` (Regra 13 do #2), e o #7 retorna na hora: sem rugido, sem mexer nos cursores e sem `chefe_nascido`.
    2. **Rugido:** toda a horda comum viva **e o elite vivo, se houver** levam o golpe `Rugido` do #7 *(decisão do autor, 2026-11-05, após o CD-GDD-ALIGN: "uma lâmina por vez" vale também para o chefe, e a luta começa só com ele)*. O pedido é **tipado**: leva o tipo `Rugido` e **nenhum valor de dano** (nada de `float.MaxValue`, que viraria infinito com os multiplicadores do #6). Ele é enfileirado pelo ponto único de dano do #6 (`Combate.Aplicar`) **na frente da fila** do tick; o #6, que roda depois do #7 no mesmo tick, **pula a F1 e a mitigação** e zera o HP no passo de resolução. A **causa da morte** (`DeathCause`) é a do primeiro pedido que zera o HP na ordem da fila, então um corpo que o auto-ataque do herói mataria no mesmo tick sai com causa `Rugido`. **Morte pelo rugido vale menos que morte pelo herói** *(decisão do autor, 2026-11-05, /design-review; resolve a OQ-1)*: ela dá **metade do XP** (`xp_rugido_permil`, padrão 500, faixa 0 a 1000, knob do #1), **não dispara os efeitos de abate da build** (#8) e **não dá loot** (#24). O princípio é "**matar sempre vale mais que esperar**": a build que limpou pior não ganha no rugido o que deixou de matar. **O rugido sobe no máximo 1 nível** *(decisão do autor, 2026-11-05, /design-review, 2ª passada)*: o XP das mortes por `Rugido` entra no #3 como **um total do tick**, `floor(Σ xpDaMorte × xp_rugido_permil / 1000)` em inteiro (sem arredondar morte a morte, para o Enxame de XP 1 não render 0), e o #3 aplica no máximo `niveis_rugido_max` (1) nível por ele; o excedente se perde. A oferta de carta desse nível abre na hora, como a de qualquer level-up (Regra 16 do #6; decisão do autor, 2026-11-05, a reavaliar depois de ver a cena: a oferta pode cobrir a Descarga, e a contagem 3-2-1 do #16 separa a escolha do combate). O #7 não dá XP: quem aplica o permil e o limite é o #3, por uma emenda pendente à Regra 6 do #3, e o #8 e o #24 recebem a exigência de ignorar mortes com causa `Rugido`. O #7 emite um evento `Rugido` para a apresentação e o log.
    3. **Cancelamento por cursor:** `cur_horda := N_horda` e `cur_elite := N_elite` (o total de linhas de horda e de entradas `Elite` da tabela). `HordaCancelada` e `ElitesCancelados` são as linhas puladas por essa atribuição, e vão para o log (#5). Esses corpos e elites não nascem e não dão XP *(provisória)*. Depois de `chefe_nascido`, o passo 2 da Regra 15 e a parte de horda do passo 3 nunca mais rodam; só a escolta.
    O primeiro ataque do chefe só vale depois da graça (Regra 9), e nunca no tick em que nasce (Regra 7 do #6).

11. **Escolta durante o chefe.** A entrada `Chefe` declara uma escolta: pool de horda, `escolta_total` (fixo, pode ser 0), `escolta_por_pulso` e `escolta_intervalo_s`, com o primeiro pulso um intervalo depois da entrada do chefe (F2). Cada pulso chega de uma direção sorteada no `Preparar` e usa a regra de posição da Regra 7 *(provisória)*. A composição da escolta é sorteada no `Preparar` como as outras (Regra 6), e os corpos seguem o teto de vivos e o limite por tick (Regra 8): esperam se não couberem e nunca são cancelados, porque não há outra entrada depois. **Um corpo de escolta que venceria com o chefe em Aviso ou Impacto espera** até o chefe sair desses estados; a espera é **por corpo**, a cada tick. O #7 lê o estado de ataque que o #6 gravou **no fim do tick anterior** (o #6 roda depois do #7), então o corpo nasce no primeiro tick em que o estado lido já é Perseguindo ou Recuperação, com defasagem de 1 tick aceita *(provisória)*. A escolta nasce a `R_spawn_m`, fora da tela: o risco real é a ordem, não a sobreposição. A F2 (`escolta_cabe`) continua checando o cronograma agendado. Ela dá alvos ao auto-ataque, XP ao Tank e um pouco de pressão de contato durante a luta *(decisão do autor, 2026-11-05: fio leve e ajustável; os valores são provisórios)*.

12. **O que o #7 não faz.** Não move, não dá dano (a não ser o pedido do rugido), não dá XP e não encerra a fase. Não adianta nem atrasa wave por abate (só o teto de vivos e o limite por tick, a regra de um elite por vez com a janela de respiro e o golpe do chefe para a escolta atrasam, Regras 8, 9 e 11). Não faz inimigo sumir sem causa. Não faz nascer nada fora da arena ou a menos de `R_min_spawn` do herói. Não cria mais de um `Essencial` por fase. Não deixa a horda comum telegrafar. Não tem invocações no MVP (`máx_invocações` = 0 na FS9 do #2) *(provisória: invocação só tem limite estático com teto por invocador e empilha ameaça, contra "corpos, não ameaças")*. Não adapta a dificuldade à build. O jogador não consegue chamar wave, adiar o chefe nem sair da arena.

13. **Estado hasheado do #7.** Entram no `Hash` do próprio #7 (a FS8 do #2 já o inclui na ordem do compositor): `cur_horda` (índice do próximo corpo de horda a nascer, na ordem `tick_do_corpo`, `w`, `k`), `cur_elite` (índice da próxima entrada `Elite`), `chefe_nascido` e `cur_escolta`. A fila de espera **não é um estado à parte**: é o intervalo entre `cur_horda` e o último corpo já vencido. Na entrada do chefe os cursores pulam para o fim (Regra 10.3), e o hash vê isso só pelos cursores. Ficam de fora: a tabela de composição (derivada da seed e dos dados), `vivos_horda` (derivado da lista de vivos), os dados e os **contadores e sinais de diagnóstico**, que vão ao log (#5) e não mudam nada na simulação:
    - `HordaEsperouTicks`: soma, sobre os ticks, dos corpos de horda vencidos que esperaram vaga (unidade: corpo × tick);
    - `EliteEsperouTicks`: soma, por elite, dos ticks entre o `inicio` e o nascimento (espera por elite vivo **ou** pela janela de respiro; unidade: tick, somado por elite);
    - `HordaCancelada` e `ElitesCancelados`: corpos e elites cancelados na entrada do chefe (Regra 10.3);
    - `TicksNoTeto`: ticks ativos com `vivos_horda` = `teto_vivos_horda`, medido depois dos nascimentos do passo do #7;
    - `VivosHordaNoElite`: `vivos_horda` no início do passo do #7 no tick em que cada elite nasce (um valor por elite);
    - `TicksNoCanto`: ticks ativos com o herói a menos de `R_spawn_m` de duas paredes ao mesmo tempo (só log; alimenta a OQ do chanfro de canto);
    - `OfertasNoRugido`: ofertas de carta abertas pelos level-ups do tick do chefe. O #7 não lê o #3: quem conta é o #5, pelos `NiveisGanhos` do #3 nesse tick (só log; alimenta a OQ-4).
    *(provisória; os sinais servem aos critérios AC-S de playtest.)*

14. **O que o #7 declara a outros sistemas** (fórmulas na Seção Formulas): o **total de spawns** do #7 (o termo `Σ spawns(w)` da FS9 do #2), o **pico de vivos** do #7 (para a F3 do #1), os dados de onde o #1 soma o `xp_total_fase` (F5 do #3), o `tick_entrada_chefe_agendado`, o `xpDaMorte` e a marca `Essencial` só no chefe. Como o pico e o total são **calculados dos dados** pela mesma validação, a **validação** nunca usa a demanda antiga (resolve a OQ-5 do #1); **no MVP e pelo ADR-0002, as contagens, os pesos, o pico e o total de spawns nunca são remotos** (abrir essa porta exigiria emendar o ADR-0002), nem `teto_vivos_horda`, as capacidades e a arena.

15. **Ordem dentro do passo do #7.** Em cada tick ativo, nesta ordem: (1) a entrada do chefe, se venceu (Regra 10: nascimento, rugido e cancelamentos por cursor), e nesse tick os passos 2 e 3 não rodam; (2) o elite da vez (Regra 9), só enquanto `chefe_nascido` é falso; (3) a horda até as vagas enquanto `chefe_nascido` é falso, e depois dele só a escolta (Regras 8 e 11). A ordem fixa a ordem dos ids emitidos no tick *(provisória)*. Depois que a simulação está *Encerrada*, nenhum `Tick` roda, então o #7 nunca faz nascer nada depois do fim da fase (Regra 13 do #2).

**Comportamento dos inimigos (executado pelo #6, declarado pelo #7).** No MVP todo inimigo em Perseguindo vai ao herói em linha reta, numa arena sem obstáculos: não há pathfinding, flanco, papéis em grupo nem separação entre inimigos (a horda pode se sobrepor, Regra 5 do #6). A separação não fica de fora por custo de algoritmo (uma grade uniforme é O(n) e não aloca), e sim por orçamento: ela é a principal candidata a pesar no spike de performance (OQ-9). Para a horda não virar um bolo único em cima do herói, **só a classe `Horda`** mira o herói somado a um deslocamento pequeno tirado de uma tabela de 32 entradas pelo id (`id mod 32`), sem sorteio *(provisória; emenda (b) aplicada na Regra 2.5 do #6 em 2026-11-05; revista no spike, com a OQ-7 do #6)*. Para a horda (e para quem tem `dist_parada_m` = 0), se o passo do tick alcança o alvo (`dist² ≤ passo²`), a posição vira o alvo, sem normalizar, para não haver NaN nem tremor (Regra 2.5 do #6, emenda (b) aplicada). Elite e chefe **andam em Perseguindo até `dist² ≤ dist_parada_m²` e nunca encaixam na posição do herói** (o #6 mira em `FATOR_PARADA` = 0,99 × `dist_parada_m`, uma margem de `float32`); com o vetor até o herói de módulo² abaixo de 1e-6, usam o eixo fixo (1,0) da regra `dir` da F3 do #6 (o knockback com vetor nulo usa outra regra no #6, `EIXOS8[id mod 8]`), então a linha da investida e a mira do Aviso nunca têm vetor nulo (o Arremessador para a `dist_parada_m`, perto do seu alcance de Aviso, e não anda até o herói quando a recarga ainda não acabou). Há **dois alvos distintos**: o do movimento é a posição atual do herói; o da trava do golpe é a posição do herói lida no tick de início do Aviso, sem deslocamento. Elite e chefe param de andar sozinhos durante Aviso, Impacto e Recuperação, porque só se movem em Perseguindo (a investida do Campeão é o deslocamento do próprio golpe, Regra 3). A horda causa dano por contato; elite e chefe, não (Regra 3).

### States and Transitions

**Estado do cronograma da fase** (um por tentativa; o #7 congela inteiro sem `CombatActive`, porque o `CombatTick` não avança):

| Estado | Vai para | Quando |
|---|---|---|
| Preparado | Em curso | primeiro tick com `CombatActive` (a tabela de composição já existe desde o `Preparar`) |
| Em curso | Chefe em campo | vence o `inicio` da entrada `Chefe`: nasce o chefe, rugido, cancelamentos (Regra 10) |
| Chefe em campo | Escolta esgotada | `cur_escolta` chega a `escolta_total` (imediato se for 0) |
| qualquer | Encerrado | o #3 pede o fim ou o #2 encerra a simulação; o #7 não decide o fim |

**Estado de uma entrada do cronograma:**

| Tipo | Estado | Vai para | Quando |
|---|---|---|---|
| `Horda` | Agendada | Em pulso | `CombatTick ≥ inicio` |
| | Em pulso | Esgotada | todos os `contagem` corpos nasceram |
| | Em pulso (corpo vencido sem vaga) | o corpo nasce | abre vaga no teto (Regra 8), na ordem |
| | Em pulso | Cancelada (resto) | entrada do chefe (Regra 10.3) |
| `Elite` | Agendada | Esperando | `CombatTick ≥ inicio` e um elite vivo |
| | Agendada | Nascida | `CombatTick ≥ inicio` e nenhum elite vivo (o `inicio` já está numa janela, F10) |
| | Esperando | Nascida | nenhum elite vivo e tick numa janela de respiro (Regra 9) |
| | Esperando | Cancelada | entrada do chefe (Regra 10.3) |
| `Chefe` | Agendada | Nascida | `CombatTick ≥ inicio`, sem nenhuma espera |

**Estado de ataque de elite e chefe:** dono é o #6 (Perseguindo, Aviso, Impacto, Recuperação). O #7 só acrescenta a condição de graça para a primeira passagem de Perseguindo a Aviso (Regra 9).

### Interactions with Other Systems

| Sistema | Entra no #7 | Sai do #7 | Dono da interface |
|---|---|---|---|
| #1 Dados e balanceamento | arquétipos, cronograma, arena, direções, formação, knobs, já convertidos em ticks e validados | as declarações da Regra 14 e as checagens de setup do #7 (Seção Formulas e Edge Cases) | #1 valida; o #7 é dono do significado |
| #2 Simulação | ordem do compositor, `ctx.CombatActive`, `CombatTick`, `seedMestre` e gerador da wave (FS6), `SimWorld.Spawn`, `IPreparaFase` | `Spawn` (com `essential` só no chefe), o `Hash` do #7, o termo do #7 no `total_spawns` (FS9) | #2 |
| #3 Fluxo de fase | só o `HeroId` (ficha de fase, para ler a posição do herói); nada do resto | o chefe `Essencial`, `xpDaMorte` por arquétipo (o `xpValue` do `Spawn`), `tick_entrada_chefe_agendado`, os dados do `xp_total_fase` | o #7 declara; o #3 lê |
| #6 Combate e dano | o estado de ataque (leitura; a escolta espera o chefe sair de Aviso e Impacto), a coluna `classe` | velocidade, HP, contato (só `Horda`), ciclo de golpes (com a investida), `resist_knockback`, `graca_ataque_ticks`, `dist_parada_m` (elite e chefe) e a tabela de mira da `Horda` (32 entradas, `id mod 32`); o pedido de golpe `Rugido` por `Combate.Aplicar` | o #7 declara; o #6 executa |
| #4 Input e câmera | (suposição) a câmera segue o herói e para na borda da arena | o tamanho da arena | #4 (sem GDD) |
| #5 Log | nada | `HordaEsperouTicks`, `EliteEsperouTicks`, `HordaCancelada`, `ElitesCancelados`, `TicksNoTeto`, `VivosHordaNoElite`, `TicksNoCanto`, o evento `Rugido` (o #5 conta `OfertasNoRugido` pelo #3) | #5 lê |
| #12 Feedback, VFX e HUD | nada | as colunas `classe`, `arquetipoId`, `tickNascimento` (surgimento, seta na borda para elite e chefe fora da tela), o evento `Rugido` | #12 lê |
| #20 Campanha | qual `faseId` roda | nada | #20 escolhe a fase; o #7 não conhece capítulo: a fase de capítulo é só um cronograma cujo `Chefe` aponta para outro arquétipo |
| #24 Inventário | nada | as mortes já estão no `DeathsThisTick` (quem dá loot é o #24, lendo as mortes; morte com causa `Rugido` não dá loot, Regra 10.2) | #24 |

**Exigências a outros documentos.** Catorze já foram aplicadas: as emendas (a), (b), (c), (e), (f), (g), (h) e (i) ao #6, as emendas (a), (b) e (c) ao #2, as Emendas 15 e 16 ao ADR-0001 (ainda `Proposed`) e a mudança da F5 do #3. **Todas as outras estão pendentes**, incluindo as novas do `/design-review` de 2026-11-05.
- **#6:** (a) a graça de ataque na passagem Perseguindo → Aviso (Regra 9) *(**aplicada no #6 em 2026-11-05**, Regra 7 do #6: `CombatTick ≥ tickNascimento + graca_ataque_ticks`, e a graça entra no `prontoDesde`)*; (b) *(**aplicada no #6 em 2026-11-05**: Regra 2.5, Edge Cases e AC R5c)* o deslocamento de mira só da classe `Horda`, por `id mod 32` (comportamento), e o encaixe no alvo: se `dist² ≤ passo²`, a posição vira o alvo, sem normalizar (evita NaN e tremor); (c) *(**aplicada no #6 em 2026-11-05**: Regras 1, 2.6, 3, 11 e 14, F2, Edge Cases e AC R3b; `DeathCause.Rugido` na Emenda 15 do ADR-0001, ainda `Proposed`)* o #7 como fonte do pedido `Rugido` em `Combate.Aplicar`: **pedido tipado, sem valor de dano**, na frente da fila, que pula a F1 e a mitigação e zera o HP; a causa da morte é a do primeiro pedido que zera o HP na ordem da fila, e a Regra 2.6 do #6 passa a listar o #7; (d) a OQ-10 do #6 (arena retangular) confirmada; (e) *(**aplicada no #6 em 2026-11-05**: Regra 6, tabela de transições, Edge Cases e AC R6d; o `prontoDesde` conta só recarga e graça, e o alcance é um portão lido a cada tick)* a condição `dist² ≤ alcance_inicio_aviso_m²` na passagem Perseguindo → Aviso dos golpes que a declaram (Arremessador, Regra 3); (f) a validação de `cap_fila` passa a somar `teto_vivos_horda + 1` (os golpes `Rugido` de um único tick, horda e elite), senão o tick do chefe deixa a simulação *Quebrada* *(achado no `/consistency-check` de 2026-11-05; **aplicada no #6 em 2026-11-05**)*; (g) *(**aplicada no #6 em 2026-11-05**: Regra 6 (forma `linha`), F5, F8, F10, Edge Cases e AC R6f)* **golpe com deslocamento**: o Aviso marca uma linha do atacante na direção do herói, travada no início do Aviso, e no Impacto o atacante se desloca ao longo dela e causa dano na linha (investida do Campeão, Regra 3); (h) *(**aplicada no #6 em 2026-11-05**: Regra 5, F7, Edge Cases e AC R5b)* **elite e chefe sem dano por contato**: `dano_contato` só existe na classe `Horda` (Regra 3); (i) *(**aplicada no #6 em 2026-11-05**: Regra 2.5, Edge Cases e AC R6e; o #6 mira em `FATOR_PARADA` = 0,99 × `dist_parada_m`)* **`dist_parada_m`** por arquétipo de elite e chefe: em Perseguindo eles param a essa distância do herói e nunca encaixam na posição dele, e o eixo fixo de reserva vale quando o vetor até o herói é nulo (Comportamento).
- **#3:** (a) a F5 (`teto_de_fase_ok`) roda com as **duas pontas** da F9 do #7, `xp_max` e `xp_min`, e a fase só passa se passar com ambas, em vez de um único `xp_total_fase` *(achado no `/consistency-check` de 2026-11-05; **aplicada no #3 em 2026-11-05**)*; (b) **XP do rugido**: na Regra 6 do #3, o XP das mortes com causa `Rugido` entra como **um total do tick**, `floor(Σ xpDaMorte × xp_rugido_permil / 1000)` em inteiro, e o #3 aplica no máximo `niveis_rugido_max` (1) nível por ele, perdendo o excedente (Regra 10.2).
- **#8 (GDD futuro):** morte com causa `Rugido` não dispara efeito de abate da build (Regra 10.2).
- **#24 (GDD futuro):** morte com causa `Rugido` não dá loot (Regra 10.2).
- **#16 (GDD futuro):** nenhuma exigência de atraso: a oferta de carta do nível do rugido abre na hora, como as outras (Regra 16 do #6; Regra 10.2, Edge Cases). O knob `atraso_oferta_rugido_ticks` foi removido em 2026-11-05, por decisão do autor, a reavaliar.
- **#12 (GDD futuro):** pré-aquecer no `Preparar` os assets do chefe (modelo, shader, LUT, disco do rugido), para o tick do rugido não pagar carga (AC-P4).
- **#4 (GDD futuro):** definir a área visível; até lá valem `meia_altura_visivel_m` e `margem_visivel_m` (Regra 3, F5).
- **#2:** *(**(a), (b) e (c) aplicadas no #2 em 2026-11-05**: FS6, Edge Cases, OQ-9, OQ-10, Dependencies e AC D6b; `RngWave(w)` no `Preparar` e `DeathCause.Rugido` nas Emendas 16 e 15 do ADR-0001, ainda `Proposed`)* (a) nota na FS6 separando composição (sorteada) de posição final (função pura da direção sorteada e da posição do herói no tick anterior, sem sorteio); (b) a frase dos Edge Cases sobre waves que nunca começam deixa de valer, porque toda a composição é sorteada no `Preparar`; (c) a OQ-10 confirmada pelo #7.
- **#1:** (a) regra para **instantes** (`inicio_s` ≥ 0 e dentro do máximo), diferente da regra "recusar menos de 1 tick" das durações; (b) as checagens de setup do #7; (c) a OQ-5 resolvida; (d) "waves ordenadas" passa a "ordenadas por (`inicio`, `w`), com `w` explícito"; (e) **relatório de autoria por fase** (texto ou CSV) com a linha do tempo em `CombatTick` (pulsos; respiros com início, fim e duração; elites; silêncio; chefe; pulsos da escolta), o pico agendado como % do teto, o XP (`xp_min`, `xp_max`), cada erro da F10 com o `w` da entrada e os sinais da F10 e da F11 (`RespiroLongo`, `CargaTankAlta`, `RespiroCurto`, `RugidoMuitosNiveis`), o **id de classe de vetor** de cada (índice, espelho em x, espelho em y) das direções (Regra 7.4), o `duelo_min_ticks` e a janela de cada entrada `Elite` (F10).
- **ADR das colunas do `SimWorld` (#6 e #7):** `classe`, `arquetipoId` e `tickNascimento` já estão na lista do #6; o #7 não acrescenta colunas.

## Formulas

*Os números dos exemplos são ilustrativos, não dados de balanceamento. As contas de setup (validação no build pelo #1) rodam em inteiros, `long` ou `decimal`; só a F4 e a F6 rodam no tick, em `float32` e `int`. Nada de `sin`, `cos`, `Mathf` nem `double` (ADR-0001). Todas as fórmulas são provisórias, consultado o `systems-designer`.*

### F1. tick_do_corpo

The tick_do_corpo formula is defined as:

`inicio_ticks = floor(inicio_s × 30 + 0,5)`; `tick_do_corpo(k) = inicio_ticks + floor(k × espalhar_ticks / contagem)`; `fim_pulso = inicio_ticks + espalhar_ticks`

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| inicio_s | decimal | 0 a `instante_max_s` | data file | instante autoral da entrada; 0 é válido (regra de **instante**, não de duração) |
| espalhar_ticks | int | ≥ 1 | calculated (F1 do #1, a partir de `espalhar_s`) | duração do pulso |
| contagem | int | ≥ 1 | data file | corpos da entrada |
| k | int | 0 a contagem − 1 | calculated | índice do corpo na entrada |
| tick_do_corpo | int | `inicio_ticks` a `fim_pulso − 1` | calculated | `CombatTick` em que o corpo vence |

**Output Range:** como (c − 1)·e/c < e, o último corpo vence em `fim_pulso − 1` ou antes, e `fim_pulso` é um limite conservador (usado na F10). `k × espalhar_ticks` em `long`. O #1 recusa `inicio_s` negativo ou acima de `instante_max_s`. A conversão usa a mesma regra de arredondamento da F1 do #1 (meio para longe de zero). Um corpo vence quando `CombatTick ≥ tick_do_corpo` e nasce pela F6. Entradas `Elite` e `Chefe` só têm k = 0.
**Example:** `inicio_s` = 30 → 900; `espalhar_s` = 6 → 180; contagem 40. k = 13: floor(2340/40) = 58 → **958**. k = 39: floor(7020/40) = 175 → **1075**. `fim_pulso` = 1080.

### F2. tick_da_escolta

The tick_da_escolta formula is defined as:

`tick_escolta(j) = inicio_chefe_ticks + (floor(j / escolta_por_pulso) + 1) × escolta_intervalo_ticks`; `n_pulsos = ceil(escolta_total / escolta_por_pulso)` se `escolta_total > 0`, senão `n_pulsos = 0` (sem `ceil(0/0)`); `escolta_cabe = n_pulsos × escolta_intervalo_ticks < ticks_max_apos_chefe`

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| j | int | 0 a escolta_total − 1 | calculated | índice do corpo da escolta |
| inicio_chefe_ticks | int | ≥ 1 | calculated (F1) | tick de entrada do chefe |
| escolta_total | int | ≥ 0 | data file | total fixo da escolta |
| escolta_por_pulso | int | ≥ 1 (exigido quando total > 0) | data file | corpos por pulso |
| escolta_intervalo_ticks | int | ≥ 1 | calculated (F1 do #1, de `escolta_intervalo_s`) | intervalo entre pulsos |
| ticks_max_apos_chefe | int | ≥ 1 | calculated (F4 do #3, `duracao_max_apos_chefe_s`) | teto de tempo depois que o chefe entra |

**Output Range:** conta em `long`. **`escolta_cabe` é bloqueante**: uma escolta que só venceria depois da derrota por tempo é dado errado. Com total = 0, `n_pulsos` = 0 e a checagem passa direto. `tick_escolta` é o tick **agendado**; em jogo o pulso ainda espera o teto, o limite por tick e o chefe sair de Aviso e Impacto (Regra 11), e a F2 não modela essa espera.
**Example:** chefe no tick 5400, total 30, 6 por pulso, intervalo 300 ticks. j = 0 → 5400 + 1 × 300 = **5700**; j = 29 → 5400 + (4 + 1) × 300 = **6900**. n_pulsos = 5: 1500 < 2700 (90 s) → **passa**.

### F3. composicao_entrada

The composicao_entrada formula is defined as:

`S = Σ peso_i`; `r = NextBounded(S)` (FS5 do #2); `arquetipo = primeiro i (ID crescente) com r < Σ_{m ≤ i} peso_m`; `dir_f = NextBounded(N_DIR)`, f = 0 … frentes − 1

`n_chamadas(Horda) = contagem + frentes`; `n_chamadas(Elite) = 2`; `n_chamadas(Chefe) = escolta_total + n_pulsos`; `linhas_tabela = Σ contagem + escolta_total`

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| peso_i | int | ≥ 1 | data file | peso do arquétipo i no pool |
| S | int | 1 a 2³¹ − 1 | calculated (validado em `long`) | soma dos pesos |
| r | int | 0 a S − 1 | calculated | sorteio sem viés (FS5) |
| N_DIR | int | ≥ 1 (ilustr. 16) | data file | tamanho da tabela de direções |
| n_chamadas | int | ≥ 0 | calculated | chamadas a `NextBounded` no gerador da entrada |

**Output Range:** P(i) = peso_i / S exatamente (FS5). Ordem no gerador `Pcg32(seed_w, w)`: primeiro os `contagem` arquétipos, depois as `frentes` direções; na entrada `Chefe`, o chefe não consome sorteio e vêm `escolta_total` arquétipos e depois `n_pulsos` direções. `n_chamadas` é exato e é o que o teste da FS6 conta. As saídas brutas do PCG podem ser mais (rejeição da FS5), mas são determinísticas por seed, e o teste fixa um golden.
**Example:** pool {Soldado 3, Enxame 1}, S = 4: r de 0 a 2 → Soldado, r = 3 → Enxame (25%). Horda com contagem 40 e frentes 3 → **43** chamadas. Chefe com escolta 30 em pulsos de 6 → 30 + 5 = **35** chamadas.

### F4. posicao_nascimento

The posicao_nascimento formula is defined as:

`px = H.x + d.x × R`; se `px < 0` ou `px > L`: `px = H.x − d.x × R` (o mesmo para `y` com `A`) → `P_f`; a direção espelhada é `e = (±d.x; ±d.y)`, com o sinal trocado em cada eixo espelhado
**Frentes distintas:** para f = 1 … frentes − 1, enquanto `id(e_f)` for igual a `id(e_g)` de algum g < f da mesma entrada (todas as g, com ou sem corpo no tick; `id` = id de classe de vetor do #1, Regra 7.4) e passos < `N_DIR`: `dir_f = (dir_f + 1) mod N_DIR` e recalcula `e_f` e `P_f`; se nenhuma direção for diferente, fica a original. A escolta não deduplica.
`frente(k) = k mod frentes`; `idx(k) = (k div frentes) mod N_FORM` (horda); escolta: `frente(j) = floor(j / escolta_por_pulso)`, `idx(j) = (j mod escolta_por_pulso) mod N_FORM`
`q = clamp(P_f + form[idx], [0, L] × [0, A])`; se `(q − H)·(q − H) < R_min²`: `q = P_f`
Chefe: o mesmo `P_f` com `d = dir[dir_chefe]` e `R = R_chefe`, sem formação

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| H | SimVec2 | dentro da arena | calculated | posição do herói no fim do tick anterior |
| d | SimVec2 | módulo de 0,99 a 1,01 | data file | direção sorteada da frente (fixa nos dados para o chefe) |
| R | float | > 0 | data file | `R_spawn` (ou `R_chefe` para o chefe) |
| R_min | float | 0 < R_min ≤ 0,98·R e ≤ 0,98·R_chefe | data file | `R_min_spawn` |
| e_f | SimVec2 | módulo de 0,99 a 1,01 | calculated | direção espelhada da frente f, comparada pelo id de classe de vetor (inteiro do #1), nunca por igualdade de `float` |
| form[i] | SimVec2 | módulo ≤ `formacao_max_m` | data file | deslocamento de formação (zero para elite e chefe) |
| N_FORM | int | ≥ 1 | data file | entradas da tabela de formação |
| L, A | float | F5 | data file | largura e altura da arena (origem no canto) |

**Output Range:** pela F5, `P_f` sempre cai dentro da arena, a uma distância R·|d| (de 0,99·R a 1,01·R) do herói, e 0,99·R ≥ R_min com folga de 1% para o arredondamento de `float32` (a F5 exige 0,98·R). A queda para `P_f` nunca viola `R_min`. A desduplicação faz no máximo `N_DIR` passos por frente, sem sorteio, e não muda a tabela de composição (só a posição). Sem raiz nem trigonometria; comparação por distância ao quadrado.
**Example:** arena 40 × 32, R = 12, R_min = 5, H = (36; 16), d = (1; 0). px = 48 > 40 → 36 − 12 = 24, então `P_f` = (24; 16). Com form = (−0,8; 0,6): q = (23,2; 16,6), dist² = 12,8² + 0,6² = 164,2 ≥ 25 → **fica em q**. **Canto:** H = (2; 2), frentes sorteadas (1; 0), (−1; 0) e (0; 1). A 2ª espelha em x (2 − 12 < 0) para e = (1; 0), igual à 1ª, então o índice dela avança até uma direção cuja espelhada seja nova: 3 pontos distintos.

### F5. arena_ok

The arena_ok formula is defined as:

`arena_ok = (L ≥ 2,02·R + m) ∧ (A ≥ 2,02·R + m) ∧ (0,98·R ≥ R_min > alcance_contato_m) ∧ ∀ d: (0,9801 ≤ d.x² + d.y² ≤ 1,0201) ∧ (0 ≤ dir_chefe < N_DIR)`
`chefe_na_tela_ok = (0,98·R_chefe ≥ R_min) ∧ (1,01·R_chefe ≤ meia_altura_visivel_m − margem_visivel_m) ∧ (R_chefe ≤ R)`; `spawn_fora_ok = (R ≥ meia_altura_visivel_m + margem_visivel_m)` (proxy testável de "fora da tela" até o #4 existir); a fase passa com `arena_ok ∧ chefe_na_tela_ok ∧ spawn_fora_ok`

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| L, A | decimal | > 0 | data file | `arena_largura_m`, `arena_altura_m` |
| R | decimal | > 0 | data file | `R_spawn` |
| m | decimal | ≥ 0,01 (com 0, `P_f` pode cair 1 ulp fora da arena em `float32`) | data file | `margem_spawn_m` |
| R_min | decimal | > 0 | data file | `R_min_spawn` |
| dir_chefe | int | 0 a N_DIR − 1 | data file | direção fixa do chefe |
| alcance_contato_m | decimal | > 0 | data file (#6) | o corpo nunca nasce já em contato com o herói |
| R_chefe | decimal | `R_min / 0,98` a `(meia_altura_visivel_m − margem_visivel_m) / 1,01` | data file | `R_chefe_m`, raio de nascimento do chefe, dentro da tela |
| meia_altura_visivel_m | decimal | > 0 | data file (provisório até o #4) | menor meio-lado da área visível com a câmera centrada |
| margem_visivel_m | decimal | ≥ 0 | data file | folga para dentro da borda da tela |
| 2,02, 1,01 e 0,98 | decimal | fixos | constant | 2,02 e 1,01 vêm da tolerância de módulo de 0,99 a 1,01; 0,98 deixa 1% de folga abaixo de 0,99 para o arredondamento de `float32` no tick |

**Output Range:** booleano, bloqueante (setup do #1). O fator é 2,02 porque um componente de `d` pode chegar a 1,01: com 2, o espelho poderia sair da arena. O módulo é comparado ao quadrado, sem raiz. **Quando o #4 existir**, a F5 ganha a cláusula `R ≥ meia_diagonal_visivel_m + margem` (com a meia-diagonal como knob do #4), que torna testável o "fora da área visível" da Regra 7.6; até lá a garantia testável é só `R_min`.
A fronteira é 0,98 e não 0,99: com 0,99, um `R_min` igual a 0,99·R podia ficar um ulp acima da distância calculada em `float32` e cair na queda para `P_f` à toa. `R_chefe ≤ R` garante que o espelho do chefe também cabe na arena.
**Example:** L = 40, A = 32, R = 12, m = 2: mínimo 2,02 × 12 + 2 = 26,24, e 32 passa; 0,98 × 12 = 11,76 ≥ 5, passa; `R_min` = 11,77 é **recusado**. Com R = 15, o mínimo vira 32,3 > 32 → **recusada**. Chefe: `R_chefe` = 6, `meia_altura_visivel_m` = 8, `margem_visivel_m` = 1: 0,98 × 6 = 5,88 ≥ 5 e 1,01 × 6 = 6,06 ≤ 7 → **passa**; `R_chefe` = 7 dá 7,07 > 7 → **recusada**. **Fora da tela:** `R` = 12 ≥ 8 + 1 = 9 passa; `R` = 8 é recusado.

### F6. vagas_horda

The vagas_horda formula is defined as:

`vagas = max(0, teto_vivos_horda − vivos_horda)`; `nascem = min(vagas, pendentes, max_nascimentos_por_tick)`; na escolta, cada corpo ainda exige `¬(chefe em Aviso ou Impacto)` no estado do fim do tick anterior (Regra 11), e `pendentes` conta só os que passam por isso

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| teto_vivos_horda | int | ≥ 1 | data file | teto por fase |
| vivos_horda | int | 0 a teto | calculated | vivos de classe `Horda` (escolta incluída) no início do passo do #7 |
| pendentes | int | ≥ 0 | calculated | corpos já vencidos a partir do cursor ativo (`cur_horda` antes do chefe, `cur_escolta` depois) |
| max_nascimentos_por_tick | int | ≥ 1 (ilustr. 20) | data file | limite de nascimentos de horda e escolta num tick; elite e chefe não contam |

**Output Range:** `nascem` vai de 0 a `min(teto, max_nascimentos_por_tick)`; o `max(0, …)` é defensivo. Os que não nascem esperam na ordem (Regra 8) e somam ao contador de diagnóstico `HordaEsperouTicks`. O limite por tick só espalha o momento do nascimento; a composição e o número de sorteios não mudam. O passo visita só as `nascem` + 1 primeiras linhas a partir do cursor; `pendentes` nunca é contado por varredura completa.
**Example:** teto 300, vivos 287, 20 pendentes → **13** nascem e 7 esperam (`HordaEsperouTicks` += 7). Teto 300, vivos 100, 200 pendentes, limite 20 → **20** nascem e 180 esperam.

### F7. total_spawns_7

The total_spawns_7 formula is defined as:

`total_spawns_7 = Σ_Horda contagem + N_elite + 1 + escolta_total`

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| Σ_Horda contagem | long | ≥ 0 | calculated | corpos de todas as entradas `Horda` |
| N_elite | int | ≥ 0 | calculated | entradas `Elite` (1 corpo cada) |
| 1 | int | 1 | constant | o chefe |
| escolta_total | int | ≥ 0 | data file | escolta do chefe |
| total_spawns_7 | long | ≥ 1 | calculated | termo do #7 em `Σ spawns(w)` na FS9 do #2 |

**Output Range:** é o **máximo**: cancelamentos (Regra 10) só reduzem o real, e como ids não se reutilizam, declara-se o máximo. Entra na FS9 junto com `ids_de_preparacao` (o herói, do #3) e o termo do #8.
**Example:** waves de 40 + 60 + 80 + 100 + 120 + 80 = 480, mais 3 elites, o chefe e escolta de 30 → **514**. Com o herói, 515 × 125 = 64.375, então `cap_ids` ≥ **644**.

### F8. pico_vivos_7

The pico_vivos_7 formula is defined as:

`pico_vivos_7 = min(teto_vivos_horda, Σ_Horda contagem + escolta_total) + min(1, N_elite) + 1`

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| teto_vivos_horda | int | ≥ 1 | data file | teto da horda viva |
| min(1, N_elite) | int | 0 ou 1 | calculated | no máximo um elite vivo (Regra 9) |
| 1 | int | 1 | constant | o chefe |
| pico_vivos_7 | int | ≥ 1 | calculated | termo do #7 no pico da lista de vivos |

**Output Range:** conservador. O pior instante é o tick do chefe: a horda ainda está viva até o teto (o rugido só se resolve no passo do #6, depois), há no máximo 1 elite vivo e o chefe entra. A lista de vivos passa pela F3 do #1 com `pico = pico_vivos_7 + 1` (o herói) mais o termo do #8.
**Example:** teto 300 → 300 + 1 + 1 = 302; com o herói, 303 × 125 = 37.875, então a capacidade da lista de vivos ≥ **379**.

### F9. xp_total_fase_dados

The xp_total_fase_dados formula is defined as:

`xp_max = Σ_Horda contagem × max_pool(xp) + Σ_Elite max_pool(xp) + escolta_total × max_pool_escolta(xp)`
`xp_min = Σ_Horda contagem × min_pool(xp) + Σ_Elite min_pool(xp)`

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| max_pool(xp), min_pool(xp) | int | ≥ 0 | calculated | maior e menor `xpDaMorte` entre os arquétipos do pool da entrada |
| max_pool_escolta(xp) | int | ≥ 0 | calculated | maior `xpDaMorte` do pool da escolta |
| xp_max, xp_min | long | ≥ 0 | calculated | as duas pontas de referência do XP da fase, **sem o chefe**; `xp_min` não é piso |

**Output Range:** a F5 do #3 (`teto_de_fase_ok`) roda com as duas pontas, e a fase só passa se passar com ambas: os level-ups contra o pool e o "cedo demais" pioram com `xp_max`; o "teto atingido" e o "nunca atingido" pioram com `xp_min` (que não conta a escolta, porque ela depende da duração da luta). **`xp_min` não é piso**: é a referência "todos mortos pelo herói, com o sorteio de menor XP". O XP real pode ficar abaixo dele, porque os corpos e elites cancelados na entrada do chefe não dão XP e as mortes pelo rugido dão só `xp_rugido_permil`/1000 do valor, somado no total do tick (Regra 10.2); esse risco é de ritmo, tratado pela F11 (`RugidoMuitosNiveis`, `espera_no_chefe`), não de setup. `xp_max` não muda. **XP igual dentro de um pool não é obrigatório**: as duas pontas cobrem a variação. Iguale só se a faixa não conseguir passar. **As 5 fases do MVP precisam passar juntas pela F5 do #3**, cada uma com as duas pontas. O #3 leva a curva de XP e o `nivel_max` no snapshot de cada fase, então a alavanca esperada é uma curva por fase, não XP diferente por fase no #7 (OQ-15) *(provisória)*.
**Example:** com `acum(10)` = 510 e faixa de 60 a 90%: `xp_max` = 700 passa (73%). `xp_min` = 520: 51.000 > 520 × 90 = 46.800, ou seja, o teto só seria atingido com 98% do XP → **recusada**.

### F10. cronograma_ok

The cronograma_ok formula is defined as:

`fim(e) = fim_pulso + viagem_ticks(e)` para `Horda` (a chegada do último corpo); `fim(e) = inicio_ticks + duelo_min_ticks(e)` para `Elite`
`viagem_ticks(H) = ceil((1,01 × R_spawn_m + formacao_max_m) / vel_min_pool(H) × 30)` (em `decimal`)
`duelo_min_ticks(E) = graca_max_pool(E) + ciclo_golpe_max_pool(E)` (o **pior caso do pool**: o build não conhece o arquétipo que a seed de cada tentativa sorteia)
`respiro_elite_ok(E) = [∀ Horda H com inicio(H) ≤ inicio(E): inicio(E) ≥ fim_pulso(H) + viagem_ticks(H) + respiro_elite_min_ticks] ∧ [∀ Horda H com inicio(H) > inicio(E): inicio(H) ≥ inicio(E) + duelo_min_ticks(E)]`
`janela(E) = { t : respiro_elite_ok com inicio(E) = t } ∩ { t ≤ inicio(C) − silencio_pre_chefe_ticks − duelo_min_ticks(E) }` (por entrada `Elite`, calculada no `Preparar` e guardada como intervalos inteiros, Regra 9)
`chefe_ok = inicio(C) ≥ max_{e ≠ C} fim(e) + silencio_pre_chefe_ticks` (o `max` do conjunto vazio vale 0; `fim` já inclui a viagem da horda e o duelo do elite)
`reserva_ok = ∀ E: janela(E) contém um intervalo contínuo de largura ≥ janela_reserva_ticks que começa em ou depois de inicio(E); e, para elites consecutivos E_i e E_{i+1}, esse intervalo de E_{i+1} começa em ou depois de inicio(E_i) + duelo_min_ticks(E_i)`
`cronograma_ok = estrutura_ok ∧ ∀ E: respiro_elite_ok(E) ∧ reserva_ok ∧ chefe_ok ∧ escolta_cabe (F2)`
**Sinal consultivo `RespiroLongo`** (não bloqueante, no relatório do #1): acende quando o vão entre pulsos de `Horda` consecutivos, `inicio(H_{i+1}) − max_{j ≤ i} fim_pulso(H_j)`, passa de `respiro_max_ticks` **e o vão não contém nenhum elite**, ou quando o silêncio antes do chefe, `inicio(C) − max_{e ≠ C} fim(e)` (contado da chegada), fica fora da faixa-alvo de 5 a 8 s do Game Feel *(provisória)*.

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| vel_min_pool(H) | decimal | > 0 | calculated | a menor `vel_per_s` entre os arquétipos do pool de H (o mais lento chega por último) |
| viagem_ticks(H) | int | ≥ 1 | calculated | ticks para o último corpo de H andar de `R_spawn_m·|d|` (até 1,01·R) até o herói parado |
| respiro_elite_min_ticks | int | ≥ 60 | calculated (F1 do #1, de `respiro_elite_min_s`) | tela vazia mínima antes de um elite, contada da chegada |
| graca_max_pool(E) | int | 15 a 60 | data file | a maior `graca_ataque_ticks` entre os arquétipos do pool de E (pior caso: o build não conhece o sorteio da tentativa) |
| ciclo_golpe_max_pool(E) | int | ≥ 1 | data file (#6) | a maior duração de golpe (Aviso + Impacto + Recuperação) entre os ciclos dos arquétipos do pool de E |
| duelo_min_ticks(E) | int | ≥ 45 | calculated | `graca_max_pool(E) + ciclo_golpe_max_pool(E)`: tempo garantido de duelo, do nascimento do elite até a próxima wave e até o silêncio do chefe |
| janela_reserva_ticks | int | ≥ 30 (ilustr. 90) | data file | largura mínima de uma janela de respiro (`reserva_ok`) |
| formacao_max_m | decimal | 0,5 a 2,0 | data file | maior deslocamento de formação; entra na `viagem_ticks` |
| silencio_pre_chefe_ticks | int | ≥ 1 | calculated (F1 do #1, de `silencio_pre_chefe_s`) | respiro antes do chefe |
| respiro_max_ticks | int | ≥ 1 | calculated (de `respiro_max_s`) | limiar do sinal `RespiroLongo` |
| estrutura_ok | bool | | calculated | as checagens estruturais listadas abaixo |

`estrutura_ok`: `w` ≥ 0 e único; exatamente um `Chefe`, último na ordem (`inicio`, `w`), com `contagem` = 1 e pool de um arquétipo de classe `Chefe`; toda `Elite` com `contagem` = 1 e `frentes` = 1; 1 ≤ `frentes` ≤ `min(contagem, N_DIR)`; pool só da classe da entrada e escolta só de `Horda`; `S` ≤ 2³¹ − 1; todo arquétipo citado existe e não está `deprecated`; nenhum arquétipo de classe `Chefe` fora da entrada `Chefe`; **todo arquétipo de classe `Horda` tem ciclo de golpes vazio** (a horda não telegrafa, Regra 3); **`graca_ataque_ticks` do chefe + `aviso_chefe_ticks_min` < `ticks_max_apos_chefe`** (o chefe precisa conseguir o 1º Impacto antes da derrota por tempo); **todo golpe de elite e de chefe declara `alcance_inicio_aviso_m` ≤ `meia_altura_visivel_m − margem_visivel_m`** (Regra 3; substitui a cláusula antiga "≤ `R_spawn_m`", que estava errada porque `R_spawn_m` fica fora da tela); **todo ciclo de elite e de chefe tem ao menos um golpe marcado `alcanca_fuga`** (investida ou área sob o herói, Regra 3); **na fase 1, o ciclo do Campeão só tem a investida** (um tipo de telegraph); **`escolta_por_pulso` ≥ 1 quando `escolta_total` > 0; nenhum arquétipo repetido no mesmo pool; `vel_per_s` > 0 em todo arquétipo de classe `Horda`; `inicio(C)` ≥ 1; `dist_parada_m` > 0 e ≤ o menor `alcance_inicio_aviso_m` do arquétipo em todo elite e chefe**; `tick_entrada_chefe_agendado = inicio(C)`.

**Output Range:** booleano, bloqueante (setup do #1). Checa o cronograma **agendado**: o teto de vivos pode atrasar corpos para dentro de um respiro em jogo, e isso é sinal da F11, não recusa. Com o silêncio ≥ 1 tick, o chefe entra estritamente depois de tudo. `viagem_ticks` supõe o herói parado: se ele foge, a chegada atrasa, e isso também é sinal (F11 `RespiroCurto`), não recusa. As contas em `decimal`, com `ceil` só no fim.
**Example:** wave termina em 1080, R = 12, `formacao_max_m` = 1,2, arquétipo mais lento a 3 m/s: `viagem` = ceil((1,01 × 12 + 1,2) / 3 × 30) = ceil(13,32 / 3 × 30) = ceil(133,2) = **134**; respiro mínimo de 2 s (60 ticks) → o elite precisa de `inicio` ≥ 1080 + 134 + 60 = **1274**: 1274 passa, 1273 é **recusado**. Com graça 30 e um ciclo de golpe de 60 ticks, `duelo_min` = **90**, e a próxima `Horda` precisa de `inicio` ≥ 1274 + 90 = **1364**. Chefe: último `fim` (já com a viagem da horda e o duelo do elite) em 4934 e silêncio de 10 s (300 ticks) → o chefe precisa de `inicio` ≥ **5234**.

### F11. carga_tank (sinal, não bloqueante)

The carga_tank formula is defined as:

`hp_med(e) = Σ peso_i × hp_i / S` (HP esperado de um corpo da entrada e); `dps_tick = dps_ref_tank_horda_per_s / 30`; `HP_horda = Σ_Horda contagem × hp_med(e)`; `hp_med_fase = HP_horda / Σ_Horda contagem`; `ρ = HP_horda / (dps_tick × inicio_chefe_ticks)`
`B_t = max(0, B_{t−1} + chegada_t − dps_tick)`, B₀ = 0, t de 0 até o chefe; `vivos_est_t = B_t / hp_med_fase`
`saturacao_pct = 100 × #{t : vivos_est_t ≥ teto_vivos_horda} / inicio_chefe_ticks`; `espera_no_chefe = max(0, vivos_est_chefe − teto_vivos_horda)`
`RespiroCurto` quando, para algum elite E, `vivos_est_{inicio(E)} > vivos_no_elite_max`
`XP_cheio = min(teto_vivos_horda, vivos_est_chefe) × max_xp_horda + max_xp_elite`; `XP_rugido = floor(XP_cheio × xp_rugido_permil / 1000)`; `pré = max(0, xp_min − XP_cheio)` (o XP já ganho antes do rugido, no pior caso do Tank); `niveis_no_rugido = #{n ≤ nivel_max : pré < acum(n) ≤ pré + XP_rugido}` (curva do #3); `RugidoMuitosNiveis` quando `niveis_no_rugido > niveis_rugido_max`

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| dps_ref_tank_horda_per_s | decimal | > 0 | data file (estimativa autoral até existirem os GDDs #8 e #10) | taxa efetiva de abate do Tank de referência contra a horda |
| hp_med(e) | decimal | > 0 | calculated | HP esperado de um corpo da entrada e, pelos pesos do pool |
| chegada_t | decimal | ≥ 0 | calculated (F1) | soma de `hp_med(e)` dos corpos que vencem no tick t |
| B_t | decimal | ≥ 0 | calculated | HP na fila (fila fluida, recursão de Lindley) |
| hp_med_fase | decimal | > 0 | calculated | média ponderada do HP de um corpo de horda da fase (a mesma base da chegada) |
| ρ | decimal | ≥ 0 | calculated | carga média da fase para o Tank |
| saturacao_pct | int | 0 a 100 | calculated | % dos ticks com a horda estimada no teto |
| max_xp_horda, max_xp_elite | int | ≥ 0 | calculated | maior `xpDaMorte` de horda e de elite da fase |
| acum(n), nivel_max | long, int | F5 do #3 | data file (#3) | curva de XP do snapshot da fase |
| niveis_no_rugido | int | 0 a `nivel_max − 1` | calculated | level-ups que o XP do rugido pagaria, partindo de `pré`; o #3 aplica no máximo `niveis_rugido_max` (1) e o resto do XP se perde |

**Output Range:** uma passada em `decimal` no build, com até cerca de 9.000 ticks. A chegada e a contagem de corpos usam a mesma base (`hp_med`), então `vivos_est` não mistura HP máximo com HP mínimo. A estimativa tem dois erros de sentido oposto: ignora o dano em área (que mata mais com densidade alta, então **superestima** a fila) e ignora o tempo que o Tank gasta no elite (que **subestima** a fila). `niveis_no_rugido` é uma estimativa: parte de `a ≈ xp_min − XP_rugido`, cortado em 0, e usa o XP agregado (o `floor` por morte só reduz). Se `xp_max` = 0, os sinais de XP não rodam (a F5 do #3 já recusa a fase). **Nada aqui é bloqueante hoje.** O build registra o aviso `CargaTankAlta` no relatório do #1 quando ρ > `rho_max`, `saturacao_pct` > `saturacao_max_pct` ou `espera_no_chefe` > 0. A F11 vira bloqueante quando `dps_ref` sair de fórmula dos #6, #8 e #10 (Open Questions). O sinal real vem do log (#5): no playtest com o Tank, `HordaCancelada` = 0. Se `Σ_Horda contagem` = 0 a F11 não roda; `saturacao_pct` usa `floor`, e t vai de 0 a `inicio_chefe_ticks − 1`.
O build também registra `RespiroCurto` e `RugidoMuitosNiveis` no mesmo relatório. O rugido dá só `xp_rugido_permil`/1000 do XP e **sobe no máximo `niveis_rugido_max` nível** (Regra 10.2); `RugidoMuitosNiveis` acende quando o XP do rugido pagaria mais níveis do que isso, ou seja, quando há **XP excedente que se perde**: o aviso mostra que a horda viva no chefe 'vale' sem efeito para a build (OQ-4, resolvida pelo limite).
**Example:** pool ilustrativo com todos os arquétipos a 20 HP, então `hp_med` = `hp_med_fase` = 20. 480 corpos × 20 HP = 9.600 HP; chefe no tick 5400; dps 60/s = 2 por tick → capacidade 10.800, ρ = **0,89** > 0,8 → **aviso**. Uma wave de 120 × 20 HP em 180 ticks chega a 13,3 HP por tick; a fila sobe 11,3 por tick até cerca de 2.040 HP, que dá 2.040 / 20 = **102 corpos**, abaixo de 300: esta wave não satura. **Rugido**, com a curva do #3 (`acum` de 2 a 10 = 10, 27, 53, 90, 140, 205, 287, 388, 510), `xp_min` = 600, `max_xp_horda` = 2, `max_xp_elite` = 10: com `vivos_est_chefe` = 300 e `xp_rugido_permil` = 500, `XP_cheio` = 610, `XP_rugido` = 305, `pré` = max(0, 600 − 610) = 0, e a faixa (0, 305] tem `acum(2)` a `acum(8)` → **7** níveis > `niveis_rugido_max` (1) → **`RugidoMuitosNiveis`**: o #3 aplica 1 nível e perde o resto. Com `vivos_est_chefe` = 20: `XP_cheio` = 50, `XP_rugido` = 25, `pré` = 550, e a faixa (550, 575] não tem nenhum `acum` → **0** níveis, sem sinal.

## Edge Cases

*Consultado:* `systems-designer`, cruzando com os Edge Cases do #2, do #3 e do #6. Itens marcados *(provisória)* são recomendação de especialista.

### Tempo, congelamento e pausa

- **If uma oferta de carta (`CombatHold` ≠ 0) abre no meio de um pulso**: o #7 não roda e o `CombatTick` não avança. Na retomada, os corpos vencem nos mesmos `tick_do_corpo`, como se a oferta não tivesse existido; nada vence "atrasado de uma vez" (Regra 15 do #2).
- **If há um elite esperando durante a oferta**: ele continua esperando e nasce no primeiro tick ativo, depois da retomada, em que nenhum elite esteja vivo e o tick esteja numa janela de respiro (Regra 9).
- **If uma oferta abre no fim do tick `inicio_chefe − 1`**: o chefe nasce no primeiro tick ativo depois da retomada. O `tick_entrada_chefe_agendado` continua exato, porque é contado em `CombatTick`.
- **If o XP do rugido dá nível no tick do chefe**: o tick termina inteiro antes do congelamento (o chefe nasce, o #6 resolve o rugido, o #3 aplica no máximo 1 nível pelo rugido, Regra 10.2). A oferta desse nível abre na hora, como qualquer level-up (Regra 16 do #6, re-revisão de 2026-11-05, sem `AvisoPerto` (a F11 saiu) e com contagem 3-2-1 na volta); não há atraso próprio do rugido *(decisão do autor, 2026-11-05, a reavaliar depois de ver a cena: a oferta pode cobrir a Descarga)*. A graça do chefe conta em `CombatTick` e não se gasta durante a oferta.
- **If o jogo é pausado**: zero `Tick`, e nada muda no #7.
- **If `inicio_s` = 0**: a entrada vence no primeiro tick com `CombatActive`, nunca no `Preparar` (tick 0). Os corpos nascem a `R_spawn` do herói, sem contato imediato. A premissa do #3 de que não há horda no tick 0 continua valendo.

### Ordem dentro do tick

- **If no mesmo tick vencem o chefe, um elite e corpos de horda**: vale a Regra 15. O chefe vem primeiro; elite e horda que esperavam são cancelados (Regra 10.3) e não nascem nesse tick.
- **If duas entradas vencem no mesmo tick**: vale a ordem da tabela, (`tick_do_corpo`, `w`, `k`) para a horda e (`inicio`, `w`) para elites.
- **If vencem mais corpos do que `max_nascimentos_por_tick`**: nascem os primeiros na ordem, e o resto espera para o tick seguinte, como na espera por vaga (F6) *(provisória)*.

### Teto de vivos e espera

- **If corpos que esperavam vaga nascem dentro de um respiro**: nascem normalmente, na direção sorteada da frente deles, relativa à posição atual do herói. A causa é o próprio jogador matar devagar. A horda não telegrafa e o contato no herói é limitado a 1 golpe a cada 6 ticks (Regra 5 do #6), então o Pilar 4 se mantém. O sinal vai ao log (`HordaEsperouTicks`) e ao build pela F11 *(provisória)*.
- **If esses corpos nascem no mesmo tick de um elite, ou logo depois**: o mesmo resultado. `R_min_spawn` vale para todos, e a graça do elite é independente da horda *(provisória)*.
- **If `vivos_horda` > `teto_vivos_horda`** (não deveria acontecer): `vagas` = 0 pelo `max` da F6, e ninguém nasce.

### Elite

- **If um elite que esperava fica livre no meio de uma wave**: ele não nasce ali. Espera a próxima janela de respiro do cronograma (Regra 9) *(decisão do autor, 2026-11-05, /design-review; resolve a OQ-2)*. A espera é contada em `EliteEsperouTicks`.
- **If não há janela antes do limite do chefe**: o elite atrasado **não nasce**: é cancelado na entrada do chefe (Regra 10.3) e conta em `ElitesCancelados` *(decisão do autor, 2026-11-05, /design-review, 2ª passada; a F10 exige uma janela de reserva para isso não ser rotina)*.
- **If o elite vivo morre no tick `t`, em que outro venceria**: o #7 roda antes do #6 e ainda o vê vivo, então o outro nasce em `t + 1` (se `t + 1` estiver numa janela). Esse atraso de 1 tick é determinístico e aceito.
- **If o elite chega ao herói sem ser visto**: não ataca. Ele só inicia Aviso dentro de `alcance_inicio_aviso_m`, que fica dentro da tela (Regra 3), mesmo que a graça tenha passado fora da câmera.
- **If o elite ou o chefe encosta no herói**: não há dano. Só a horda causa contato (Regra 3; Regra 5 do #6).
- **If duas entradas `Elite` têm o mesmo `inicio`**: nasce a de menor `w`, e a outra espera.
- **If há um elite vivo quando o chefe entra**: o rugido o mata no mesmo tick, com metade do XP (`xp_rugido_permil`, Regra 10.2). Se ele estava em Aviso, o golpe é cancelado pela morte do atacante (Regra 6 do #6). O pico ainda conta 1 elite mais o chefe (F8), porque o rugido só se resolve no passo do #6, depois do nascimento do chefe.
- **If o Arremessador está fora de `alcance_inicio_aviso_m` com a recarga pronta**: ele continua em Perseguindo até entrar no alcance; não há Aviso iniciado fora da área visível.

### Chefe, rugido e escolta

- **If o herói morre no tick em que o chefe nasce**: o contato da horda ainda vale, porque o atacante estava vivo no início do passe do #6 (o mesmo princípio de "o elite morre no Impacto e o golpe vale"). O resultado é `DerrotaHeroi`, com `ChefeVisto` verdadeiro (Edge Cases do #3). O XP do rugido desse tick se perde, como todo XP de tick de fim (Regra 5.4 do #3). O chefe não ataca nesse tick, pela graça.
- **If o rugido acontece com 0 corpos de horda vivos**: o evento `Rugido` sai mesmo assim, para a apresentação, sem nenhum pedido de golpe.
- **If o rugido dá XP para mais de um nível**: o #3 aplica só `niveis_rugido_max` (1) nível e perde o excedente (Regra 10.2); o build avisa com `RugidoMuitosNiveis` (F11) e o log conta `OfertasNoRugido`. Nunca há cadeia de ofertas no tick do chefe (OQ-4 resolvida pelo limite).
- **If o golpe `Rugido` chega ao #6**: ele não passa pela F1 do #6 (`base`, `modDano`, mitigação, `dano_max`). O HP vai a 0 e sai um `Kill` com causa `Rugido`, que o #3 lê para o multiplicador de XP, e que o #8 e o #24 ignoram (Regra 10.2). Não há knockback nem candidato a hit-stop, e `GolpesLimitados` não conta. A horda não tem i-frames, e `poise` e `kb_refrat` só bloqueiam knockback. O golpe entra primeiro na fila do #6. As mortes saem no evento agregado da horda por tick (Regra 14 do #6) *(provisória; exigência ao #6)*.
- **If um corpo de horda nasceria no próprio tick do chefe**: não acontece. A F10 põe o chefe estritamente depois de todo `fim_pulso`, e a Regra 15 cancela os que esperavam.
- **If `escolta_total` = 0**: o estado vai direto para Escolta esgotada, sem nenhum sorteio (`n_pulsos` = 0).
- **If um pulso da escolta vence com o chefe em Aviso ou Impacto**: o pulso espera o chefe sair desses estados e nasce no primeiro tick em Perseguindo ou Recuperação (Regra 11) *(provisória)*.
- **If o rugido mata no tick em que o chefe nasce longe da câmera**: não acontece. O chefe nasce a `R_chefe_m`, dentro da tela (Regra 7, F5).
- **If a escolta espera vaga além do teto de tempo**: esses corpos nunca nascem. A tentativa acaba em `DerrotaTempo` (#3), e a F2 cobre só o que foi agendado.
- **If o chefe morre antes de a escolta acabar**: a simulação vira *Encerrada* e os corpos pendentes não nascem. Não há contador novo: `cur_escolta` já está no hash final.

### Posição e arena

- **If o ponto calculado cai exatamente na borda (`px == L`)**: fica ali, porque a arena é um intervalo fechado [0, L], como no limite de arena do #6.
- **If o herói está na borda (`H.x == L`) e `d.x > 0`**: o ponto é espelhado; pela F5, `L − 1,01·R` > 0.
- **If o herói está num canto**: os dois eixos são espelhados de forma independente. O módulo de `d` se mantém, e a distância continua R·|d| ≥ `R_min_spawn`. Com `d.x` = 0, só o eixo `y` pode ser espelhado. Duas frentes que espelham para a mesma direção são separadas pela desduplicação da F4, e o tempo no canto vai ao log (`TicksNoCanto`).
- **If o deslocamento de formação clampa sobre o herói**: o corpo nasce no ponto da frente `P_f` (F4).
- **If dois corpos nascem no mesmo ponto**: é permitido (a horda pode se sobrepor, Regra 5 do #6). A mira por `id mod 32` os separa, e um knockback com vetor nulo usa `EIXOS8[id mod 8]` (F3 do #6).
- **If um corpo chega ao próprio alvo de mira**: a posição vira o alvo, sem normalizar um vetor quase nulo (Regra 2.5 do #6, emenda (b) aplicada).
- **If a posição do herói não é finita no início do passo do #7**: é bug interno. O NaN teria sido tratado no tick anterior pela Regra 9 do #2, que encerra a fase. O #7 confere `H` uma vez por tick e lança nos dois modos (a simulação vira *Quebrada*) *(provisória)*.

### Sorteio e dados

- **If a soma dos pesos passa de 2³¹ − 1, ou uma `contagem` é gigante**: o #1 recusa a fase (`S` validado em `long`; o total entra na FS9 contra `cap_ids`). Não há checagem em tempo de jogo.
- **If um arquétipo está `deprecated`**: o #1 recusa (`estrutura_ok`, F10).
- **If `xpDaMorte` = 0**: é válido, e a morte dá 0 XP. Se a fase inteira der 0 XP, a F5 do #3 recusa.
- **If `graca_ataque_ticks` do chefe ≥ `ticks_max_apos_chefe`**: o #1 recusa, porque o chefe nunca atacaria *(provisória)*.
- **If há retry com seed nova**: uma `Simulation` nova, outra composição e ids desde o 0.
- **If a seed é a mesma e os comandos são outros**: a tabela de composição é idêntica (arquétipos e direções). Mudam as posições finais (dependem do herói) e os momentos de nascimento (espera por vaga ou por elite). O teste de aceite compara a tabela, não o hash de cada tick.
- **If é auto-battle (#40)**: nada muda no #7; a política de auto-battle só troca a fonte dos comandos.

### Capacidade e ids

- **If `Spawn` devolve −1 para um corpo de horda, de escolta ou um elite**: no modo estrito, lança. No não estrito, conta `SpawnsRejected`, **o cursor avança** e o corpo se perde, sem XP. Como ids não se reutilizam, tentar de novo falharia para sempre e travaria a fila. Com a F7 e a F8 validadas pelo #1, isso só acontece por bug de dado (Regra 8 do #2) *(provisória)*.
- **If o `Spawn` essencial do chefe é rejeitado**: `EssentialSpawnRejected` → `FalhaInterna(ChefeAusente)` no mesmo tick (Regra 13 do #2 e Regra 7 do #3).

## Dependencies

### Upstream (o #7 depende de)

| Sistema | Natureza | O que o #7 usa | Já cita o #7? |
|---|---|---|---|
| #1 Dados e balanceamento | **Hard** | arquétipos, cronogramas, arena, direções, formação e knobs, validados e convertidos em ticks antes da fase; as checagens F5, F10 e o recálculo de F7, F8 e F9 | sim (Downstream do #1, "contagens, densidades, waves ordenadas, pico, total de spawns") |
| #2 Simulação determinística | **Hard** | `ISimSystem` na 1ª posição da ordem; `ctx.CombatActive` e `CombatTick`; gerador da wave (FS6) e `NextBounded` (FS5); `SimWorld.Spawn` com `essential`; `IPreparaFase`; o `Hash` do sistema na FS8 | sim (Downstream do #2, Hard) |
| #6 Combate e dano | **Hard** | o #6 executa movimento, contato, ciclo de golpes e mortes de todos os inimigos; o ponto único `Combate.Aplicar` (golpe `Rugido`); a coluna `classe` e o estado de ataque | sim (o #6 lista o #7 como Hard: "#7 declara os arquétipos; #6 os executa") |

**Não é dependência:** o #7 só lê do #3 o `HeroId` (para achar o herói na lista de vivos) e não lê mais nada da ficha, nem o #8, o #16 nem o #20 dentro do tick. A fase que roda é escolhida fora dele.

**Suposição sobre o #4 (Input e câmera, sem GDD):** a câmera segue o herói e para na borda da arena. Isso só afeta se um nascimento é visível (Regra 7.6), nunca a regra de nascimento. Não entra como dependência; vira pergunta em aberto (OQ-6). A área visível também mede o alcance de início de Aviso e o raio do chefe (`meia_altura_visivel_m`, `margem_visivel_m`, Regra 3 e F5); até o #4 existir esses dois são knobs provisórios do #7, e o #4 deve substituí-los.

### Downstream (dependem do #7)

| Sistema | Natureza | O que espera do #7 | GDD existe? |
|---|---|---|---|
| #3 Fluxo de fase | **Hard** (interface: o #3 define a leitura, o #7 a cumpre) | o chefe `Essencial` (exatamente 1), `xpDaMorte` por arquétipo, `tick_entrada_chefe_agendado`, os dados do `xp_total_fase` (F9), o primeiro ataque do chefe só depois do tick do nascimento | sim; **todas as exigências do #3 ao #7 estão cumpridas** (Regras 3, 4, 9, 10 e F9); em troca, o #7 pediu ao #3 que a F5 rode com as duas pontas de XP (aplicado em 2026-11-05) e que a Regra 6 aplique `xp_rugido_permil` ao total do tick das mortes com causa `Rugido`, com limite de `niveis_rugido_max` nível (pendente) |
| #12 Feedback, VFX e HUD | Hard | colunas `classe`, `arquetipoId`, `tickNascimento`; evento `Rugido`; surgimento e seta na borda | não |
| #20 Campanha e capítulos | Hard | um cronograma por `faseId`, incluindo o da fase de capítulo com o chefe de capítulo | não |
| #24 Inventário | Soft | as mortes de inimigos (pelo `DeathsThisTick`), para o loot; morte com causa `Rugido` não dá loot (Regra 10.2, OQ-1 resolvida) | não |
| #14 Dungeons e trindade (Vertical Slice) | Hard | arquétipos e cronogramas reutilizáveis em dungeon | não |
| #5 Log | Soft | os contadores de diagnóstico do #7 e o evento `Rugido` | não |
| #8 Skills e evoluções | Soft | morte com causa `Rugido` não dispara efeito de abate (Regra 10.2, OQ-1 resolvida); o #8 declara o próprio termo na FS9 | não |
| #16 Oferta do Grimório | Soft (indireta) | no máximo 1 oferta pelo nível do rugido (Regra 10.2), aberta na hora como as demais | não |
| #12 Feedback, VFX e HUD (pré-aquecimento) | Hard | pré-aquecer no `Preparar` o modelo, o shader, o LUT e o disco do chefe, para o tick do rugido caber no frame (AC-P4) | não |
**Dependência circular:** nenhuma. O #7 depende de 1, 2 e 6; o #3 lê o #7 por interface, sem ciclo (nota do índice).

### Bidirecionalidade e ajustes pendentes em outros documentos

- **`systems-index.md`:** a linha do #7 já tem "Depends On 1, 2, 6"; muda o status e o link do Design Doc (Fase 5). O #12, o #20, o #24 e o #14 já listam o #7.
- **#1, #2, #3, #6:** já citam o #7 com a natureza desta tabela. As exigências do #7 a cada um estão no fim de Interactions with Other Systems e nos Edge Cases. **Catorze foram aplicadas** (as emendas (a), (b), (c), (e), (f), (g), (h) e (i) ao #6, as emendas (a), (b) e (c) ao #2, as Emendas 15 e 16 ao ADR-0001 (ainda `Proposed`), com autorização do autor em 2026-11-05, e a mudança da F5 do #3); **as outras estão pendentes**: #6 (d) (só a confirmação da OQ-10); #3 (b); ADR-0001 (Emendas 15 e 16 escritas, ainda `Proposed`: falta o `/architecture-review` e o `accept`); #1 (as checagens de setup do #7, a regra de instante, "waves ordenadas" e o relatório por fase); #8; #24; #16; #12; #4. Elas ficam para a propagação (`/propagate-design-change` ou edição autorizada pelo autor).
- **GDDs ainda por escrever** (#5, #8, #12, #14, #16, #20, #24): cada um deve citar o #7 nas suas Dependencies, com a natureza desta tabela.

## Tuning Knobs

Os knobs **moram no #1**, que guarda valor, unidade e faixa; o significado e a faixa proposta são deste GDD. Os valores são iniciais e **a reavaliar** no protótipo e no spike de performance; `ilustr.` vem dos exemplos das fórmulas. *Derivado das listas do `systems-designer` (Formulas) e do `level-designer` (ritmo); sem consulta nova.*

**Não duplicados (a fonte está em outro lugar):** `ticks_per_second` (#2 e ADR-0001); `capacity_margin_pct` e os tetos de capacidade (#1); `duracao_max_apos_chefe_s` e a curva de XP (#3); `max_avisos`, `contato_gap_ticks`, `cad_contato_s`, `alcance_contato_m`, `aviso_ticks`, `recuperacao_ticks`, `tempo_morte_contato_min_s` (#6); HP e velocidade do herói (#1 e #10).

**Nenhum knob do #7 é de aceite no MVP** (`aceite: não`): as contagens e densidades nascem do spike de performance e do protótipo, como os tetos de capacidade (Regra 8 do #1). Nenhum é remoto no MVP. Pela Regra 14 e pelo ADR-0002, as **contagens, os pesos, o pico e o total de spawns** também **nunca** são remotos (abrir essa porta exigiria emendar o ADR-0002), nem `teto_vivos_horda`, a arena, as direções e as capacidades.

### Globais e por fase

| Knob | Padrão | Faixa segura | Afeta | Baixo demais | Alto demais |
|---|---|---|---|---|---|
| `teto_vivos_horda` (Regra 8, F6, F8) | ilustr. 300 (fixado no fim do spike) | `int`, 50 até o teto de vivos do spike menos elite, chefe e herói | horda viva ao mesmo tempo; o pico declarado | a maré nunca afoga; quem mata devagar fica sem pressão; Descarga fraca | o aparelho cai de fps; a F3 do #1 recusa a fase |
| `max_nascimentos_por_tick` (Regra 8, F6) | ilustr. 20 | `int`, ≥ 1 (ilustr. 10 a 40) | nascimentos de horda e escolta num tick | a wave chega aos pingos depois de um rugido ou de uma limpeza | pico de `Spawn` num tick só (AC-P1 a) |
| `respiro_elite_min_s` (Regra 5, F10) | 2,0 | `float`, s, 2,0 a 6,0 (o Game Feel diz nunca menos de 2 s) | tela vazia antes do elite, contada da chegada (`viagem_ticks`) | o elite nasce colado na wave; o momento-âncora some | ritmo arrastado; menos waves cabem na fase |
| `duelo_min_s` (Regra 5, F10) | derivado: graça + um ciclo de golpe do elite (ilustr. 3 s) | `float`, s, 2,0 a 8,0; não é digitado: sai da graça e do ciclo do pool (F10) | tempo garantido de duelo, do nascimento do elite até a próxima wave e até o silêncio do chefe | a wave seguinte afoga o elite recém-chegado; o elite nasce e morre pelo rugido sem luta | o elite vira duelo longo; a maré some |
| `janela_reserva_ticks` (Regra 9, F10) | 90 (3 s) | `int`, ticks, 60 a 300 | largura mínima da janela de respiro de cada elite e da reserva entre elites consecutivos | o elite atrasado quase nunca acha janela e é cancelado | o cronograma não deixa espaço para as waves |
| `respiro_max_s` (F10, sinal `RespiroLongo`) | ilustr. 10 | `float`, s, 8 a 14 | limiar do sinal de vão longo entre pulsos (vãos que contêm um elite não contam) | aviso em toda fase | tédio passa sem aviso |
| faixa-alvo do silêncio (F10, sinal `RespiroLongo`) | 5 a 8 s | `float`, s (Game Feel) | quando o silêncio antes do chefe acende o sinal | aviso em todo cronograma | silêncio fraco ou arrastado passa sem aviso |
| `silencio_pre_chefe_s` (Regra 5, F10) | 6,0 | `float`, s, 4,0 a 8,0 | respiro antes do chefe, contado da chegada do último corpo (F10) | o chefe chega no meio da última wave | o ritmo cai bem antes do clímax |
| `espalhar_s` (por entrada `Horda`, F1) | 6,0 | `float`, s, 1,0 a 15,0 | pulso da wave | a wave chega em bloco | a wave vira um gotejamento sem pico |
| `frentes` (por entrada, F3, F4) | 1 a 3 | `int`, 1 a `contagem` | de quantas direções a wave chega | uma só frente: fácil fugir para o outro lado | nuvem uniforme; a frente não se lê |
| `instante_max_s` (F1) | 600 | `float`, s, 60 a 900 | o maior `inicio_s` aceito | recusa fases legítimas | deixa passar erro de digitação |
| `arena_largura_m`, `arena_altura_m` (Regra 2, F5) | ilustr. 40 × 32 (cerca de 2,5 × 2 telas) | `float`, m; ≥ 2,02 · `R_spawn` + `margem_spawn_m` (F5) | espaço de manobra e de nascimento | a F5 recusa; sem espaço para sair das áreas | o herói foge para sempre; a pressão cai |
| `R_spawn_m` (Regra 7, F4) | ilustr. 12 | `float`, m; ≥ `meia_altura_visivel_m` + `margem_visivel_m` (proxy testável de "fora da tela", F5; a meia diagonal só quando o #4 existir) e ≤ (lado menor da arena − margem) / 2,02 | distância de nascimento | nasce à vista | a horda demora a chegar e a wave se esvazia |
| `R_min_spawn_m` (Regra 7, F4, F5) | ilustr. 5 (era 8; desceu para caber o chefe dentro da tela) | `float`, m; > `alcance_contato_m`, ≤ 0,98 · `R_spawn_m` e ≤ 0,98 · `R_chefe_m` | garantia firme de nunca nascer colado | contato no tick seguinte ao nascimento | a queda para `P_f` vira regra, não exceção; o chefe não cabe na tela |
| `R_chefe_m` (Regra 7, F4, F5) | ilustr. 6 | `float`, m; `R_min_spawn_m / 0,98` a `(meia_altura_visivel_m − margem_visivel_m) / 1,01`, e ≤ `R_spawn_m` | onde o chefe nasce, dentro da tela, para o rugido ser visto | o chefe nasce quase em cima do herói | o chefe nasce na borda ou fora da tela |
| `meia_altura_visivel_m` e `margem_visivel_m` (Regra 3, F5, F10) | ilustr. 8 e 1 *(provisórios até o #4)* | `float`, m; > 0 e ≥ 0 | a área em que elite e chefe podem iniciar Aviso e o raio do chefe | Aviso só colado no herói; o chefe não cabe | Aviso iniciado fora da tela (P4) |
| `margem_spawn_m` (F5) | 2,0 | `float`, m, 0,01 a 5 | folga entre o anel e a borda | o espelho encosta na borda | exige arena maior |
| `N_DIR` e a tabela de direções (F3, F5) | 16 | `int`, 4 a 64; módulo de cada direção de 0,99 a 1,01 | variedade de chegada | chegadas previsíveis | sem ganho de leitura |
| `N_FORM` e `formacao_max_m` (F4) | 8 e 1,2 | `int` 4 a 16; `float`, m, 0,5 a 2,0 | o desenho da frente | corpos empilhados | a frente se desfaz |
| `mira_offset_max_m` (comportamento, tabela de 32, só `Horda`) | ilustr. 0,4 | `float`, m, 0 a `alcance_contato_m` | o anel em volta do herói | bolo único sobre o herói | inimigos que "erram" o herói e não encostam |
| `graca_ataque_ticks` (Regra 9) | elite 30; chefe 60 | `int`, ticks; elite 15 a 60, chefe 30 a 120; `< ticks_max_apos_chefe` | tempo para ver o elite e o chefe antes do 1º Aviso | ataque sem leitura (P4) | o elite não ameaça; a luta do chefe se alonga |
| `escolta_total`, `escolta_por_pulso`, `escolta_intervalo_s` (Regra 11, F2) | ilustr. 30, 6 e 10 s | `int` 0 a 100; `int` ≥ 1; `float`, s, 3 a 30; F2 `escolta_cabe` | horda durante o chefe | sem alvos para o auto-ataque; o Tank fica sem XP na luta | ruído sobre o telegraph do chefe |
| `hp_horda_mult_fase` (por fase, aplicado no build) | 1,0 na fase 1, subida pequena até a 5 | `float`, 1,0 a 2,0 | resistência da horda por fase | a build madura não sente a fase 5 | a espiral do Tank (F11 avisa) |

### Desempenho

| Knob | Padrão | Faixa segura | Afeta | Baixo demais | Alto demais |
|---|---|---|---|---|---|
| `orcamento_horda_ms` (AC-P1) | alvo p95 0,3; piso p99 0,5 (a confirmar no spike) | `float`, ms por tick, 0 < x ≤ 1,5% de 33,3 ms | tempo máximo do passo do #7 com 300 vivos e 200 pendentes, e no tick do rugido, no aparelho de referência | aceite exigente demais; o spike falha à toa | o #7 consome o orçamento do #6 e a horda reduz |

### Sinal de carga do Tank (F11, não bloqueante)

| Knob | Padrão | Faixa segura | Afeta | Baixo demais | Alto demais |
|---|---|---|---|---|---|
| `dps_ref_tank_horda_per_s` | ilustr. 60 (estimativa autoral) | `float`, HP/s, > 0 | a carga estimada do Tank | aviso sempre aceso | o aviso nunca acende |
| `rho_max` | 0,8 | `float`, 0,5 a 1,0 | limiar do aviso de carga média | aviso demais | a horda acumula sem aviso |
| `saturacao_max_pct` | 10 | `int`, %, 0 a 50 | % dos ticks com a horda estimada no teto | aviso demais | o Tank vive no teto sem aviso |
| `xp_rugido_permil` (Regra 10.2; aplicado pelo #3) | 500 *(decisão do autor)* | `int`, 0 a 1000 (milésimos) | fração do XP das mortes pelo rugido, somada no total do tick e arredondada uma vez | o rugido não dá nada e o Tank perde a horda que não alcançou | esperar vale tanto quanto matar (P1) |
| `niveis_rugido_max` (Regra 10.2, F11) | 1 *(decisão do autor)* | `int`, 1 a 3 | máximo de níveis que o XP do rugido sobe no #3 (o excedente se perde); também o limiar do sinal `RugidoMuitosNiveis` | o rugido quase não recompensa a horda viva | cadeia de ofertas sobre a Descarga e incentivo a segurar a horda |
| `vivos_no_elite_max` (F11, `RespiroCurto`) | ilustr. 15 corpos | `int`, 5 a 60 | horda estimada viva quando o elite entra | aviso em quase toda fase | elite chegando na massa passa sem aviso |

### Dados por arquétipo (definições do #1; o significado é do #7, a execução é do #6)

| Campo | Faixa | Restrição de outro GDD |
|---|---|---|
| `vel_per_s` | `float`, m/s, > 0 | elite e chefe abaixo do herói mais lento, para a F5 do #6 valer (sair da área andando) |
| `dist_parada_m` (**só elite e chefe**; horda = 0) | `float`, m, > 0 e ≤ o menor `alcance_inicio_aviso_m` do arquétipo | em Perseguindo o inimigo para a essa distância do herói e nunca encaixa na posição dele (F10; Regra 2.5 do #6, emenda (i) aplicada) |
| `hp` | `float`, > 0 | com HP acima de ~5.000 o `hp_residuo` do #6 sobe (F2 do #6) |
| `xpDaMorte` | `int` ≥ 0 | F9 e a F5 do #3 |
| `dano_contato` (**só classe `Horda`**) | `float`, > 0 | o maior da fase é o `dano_contato_max` da F7 do #6: menor que HP do herói / 40 com X = 240; elite e chefe não têm o campo (Regra 5 do #6, emenda (h) aplicada) |
| `alcance_inicio_aviso_m` (todo golpe de elite e chefe) | `float`, m, > 0 e ≤ `meia_altura_visivel_m − margem_visivel_m` | F10; Regra 6 do #6 (emenda (e) aplicada) |
| `alcanca_fuga` (marca do golpe) | `bool`; ≥ 1 golpe marcado por ciclo de elite e chefe | F10; investida ou área sob o herói |
| deslocamento da investida (`desloc_m`, golpe de forma `linha`) | `float`, m, > 0 (ilustr. 3 a 5) | Regra 6 do #6 (emenda (g) aplicada) |
| `resist_knockback` | `float`, 0 a 1 | `Essencial` = 1 (#6) |
| ciclo de golpes (elite e chefe) | lista de golpes do #6 | `A` pela F5 do #6 (elite ≥ 24, chefe ≥ 36 ticks); `base` pela F9 do #6 (DPS aguenta 2, Tank 3) |
| `graca_ataque_ticks` | acima | Regra 9 |

### Curva de referência das 5 fases do MVP *(provisória, level-designer; alvo de autoria, não regra)*

| Fase | Tempo até o chefe | Horda no pico (% de `teto_vivos_horda`) | Elites | Arquétipo novo |
|---|---|---|---|---|
| 1 | cerca de 2,5 min | 30 a 40% | 1 (por volta de 50% da fase, depois do 1º nível e da 1ª carta) | Soldado e Campeão (exceção: a fase 1 apresenta dois; o Campeão só com a investida) |
| 2 | | 50% | 2 | Enxame (e o golpe em círculo do Campeão) |
| 3 | | 65% | 2 | Bruto |
| 4 | | 80% | 3 | Arremessador |
| 5 | cerca de 3,5 min | ≤ 85% (folga para a espera da Regra 8) | 3, mais próximos | todos misturados |

No máximo **um tipo novo de horda ou um elite novo por fase, nunca os dois**, com exceção da fase 1, e o novo é apresentado primeiro numa wave só dele *(provisória)*. A curva fixa 8 a 10 waves por fase (Regra 5) e **mais `frentes` ao mesmo tempo nas fases densas** (a pressão da maré é de frentes, Player Fantasy); ela ainda não fixa, por fase, o número exato de waves, os valores de `frentes`, o `espalhar_s` nem o `hp_horda_mult_fase`; isso fica na OQ-14. Vale também **no máximo 3 tipos de horda por capítulo** (orçamento de draws da arte, Visual/Audio Requirements). A fase 1 ensina (movimento na 1ª wave, carta no 1º level-up, esquiva no 1º elite com um único tipo de telegraph, suprema no chefe); a fase 5 cobra. O que não sobe entre fases: `A` dos golpes, a relação golpe do elite ÷ HP do herói, `max_avisos`, um elite por vez e o ciclo do chefe de fase.

### Interações entre knobs

- **Arena × `R_spawn_m` × `margem_spawn_m`:** a F5 amarra os três. Subir `R_spawn_m` exige arena maior; a câmera do #4 define o piso de `R_spawn_m`.
- **`teto_vivos_horda` × capacidades:** o teto entra no pico (F8) e na `cap_fila` do #6 (o rugido enfileira até `teto_vivos_horda` golpes num tick). Subir o teto exige rever as duas capacidades.
- **`respiro_elite_min_s` × `duelo_min_s` × `viagem_ticks` × `espalhar_s` × `respiro_max_s` × número de waves:** juntos decidem quanto cabe até o chefe. Cada elite custa, no mínimo, `viagem` + `respiro_elite_min` + `duelo_min` entre duas waves (no exemplo da F10, 134 + 60 + 90 = 284 ticks, cerca de 9,5 s). Um pool lento (Bruto) alonga a `viagem`; subir `R_spawn_m` ou a formação também. Alongar pulsos e respiros empurra o chefe para depois e alonga a fase; vãos sem elite acima de `respiro_max_s` acendem `RespiroLongo`, então fases longas pedem pulsos mais longos, não mais tela vazia.
- **`R_chefe_m` × `meia_altura_visivel_m` × `R_min_spawn_m`:** a F5 amarra os três (`R_min ≤ 0,98·R_chefe` e `1,01·R_chefe ≤ meia_altura − margem`). Uma tela menor (o #4) aperta a faixa do chefe e pode obrigar a baixar `R_min_spawn_m`.
- **`max_nascimentos_por_tick` × `teto_vivos_horda`:** com o limite baixo e o teto alto, a horda leva vários ticks para encher depois do rugido ou de uma limpeza; isso só muda o momento, não a composição.
- **`graca_ataque_ticks` do chefe × `duracao_max_apos_chefe_s` (#3):** a graça come o tempo da luta; a F10 recusa graça ≥ teto.
- **Densidade × `hp_horda_mult_fase` × `dps_ref_tank_horda_per_s`:** é a carga da F11. Para aliviar o Tank, o ajuste certo é a densidade ou o HP da horda, não o teto de vivos (que só esconde o acúmulo).
- **`escolta_*` × `duracao_max_apos_chefe_s`:** a F2 recusa escolta que só chegaria depois da derrota por tempo.

## Visual/Audio Requirements

**Regras gerais, dano, hit-stop, telegraph e morte agregada da horda: ver Visual/Audio Requirements do #6.** Aqui fica só o que é próprio do #7. Referência: `design/art/art-bible.md`. O #7 só emite eventos (`Rugido`) e expõe colunas (`classe`, `arquetipoId`, `tickNascimento`); quem desenha é o #12, e o áudio final é do #31.

### Eventos do #7

| Evento | O que se vê | Camada | Duração | Orçamento |
|---|---|---|---|---|
| **Surgimento da horda** (só quando o nascimento cai dentro da câmera, Regra 7.6) | o corpo sobe do chão ou um dissolve invertido; mantém V ≤ 30, sem flash | horda | 4 a 6 ticks | mesmo shader do dissolve do #6, com uma propriedade por instância lida de `tickNascimento`; zero partícula, zero decal, zero draw a mais. **Nada no chão:** um anel seria cura (3.3) e serrilha ou hachura seriam telegraph (3.6) |
| **Chegada do elite** (no respiro) | pose de entrada com antecipação exagerada de 1,3× (5.4); durante a graça quem faz a leitura é o osso frio, sem decal | elite | a graça (Regra 9) | 0 partículas (2.2); **sem troca de LUT**, que é assinatura do chefe *(provisória)* |
| **Seta na borda** (elite ou chefe fora da câmera) | chevron angular em aço neutro (`#8C96A3` ou `#E6EAF0`), como o chevron de aliado da 7.1; elite e chefe se distinguem **pela forma** (chevron simples × duplo), nunca pela cor; nunca redonda, serrilhada, hachurada nem na faixa 4.2a | HUD de borda, dentro da safe area | do nascimento até entrar na câmera | **não pulsa nem pisca** (7.4); cai para 40% de opacidade quando um telegraph passa por baixo (7.7) |
| **Entrada do chefe e rugido** | troca para o LUT do chefe (L2) no mesmo tick (2.2); a onda de choque é **um disco difuso sem contorno** (feather ≥ 40% do raio) que se expande a partir do chefe, em cor fria ou poeira clara, alfa ≤ 0,6; nunca anel fechado (exclusivo da cura, 3.6), nem serrilha, nem flash de tela cheia | abaixo do herói e acima da horda | 8 a 12 ticks | no máximo 2 cartões, nenhuma partícula por corpo; respeita o limite de 3 flashes/s (7.4); sem hit-stop (o golpe `Rugido` não é candidato no #6) *(provisória)* |
| **Morte em massa do rugido** | os dissolves começam **escalonados pela distância ao chefe**, para a onda "passar" pela horda; é só apresentação, a simulação já matou todos no mesmo tick | horda | atraso de até cerca de 10 ticks mais o dissolve do #6 | 100% em shader; **nenhum número de dano** nas mortes por `Rugido`; o excedente do pool de fantasmas do #6 (os mais distantes do chefe) some com fade direto *(provisória; o spike mede se cabem 300 fantasmas)* |

### Leitura por classe

- **Horda** (5.2, 3.2): bloco com V ≤ 30, matiz de 200 a 230°, 40 a 70 px de render, sem acessório solto. Os três tipos se separam **por massa e andar, nunca por cor própria**: Enxame cerca de 40 px, baixo, passo rápido; Soldado cerca de 55 px, ereto; Bruto 70 px, largo, passo pesado. O Bruto fixa a "maior horda do capítulo", e o elite mede de 1,5 a 2× ele.
- **Elite:** 105 a 140 px, assimétrico, corpo com S ≤ 20 e V ≤ 30, e o osso frio (≤ 1.000 px²) como único alto contraste.
- **Chefe:** 240 a 350 px, osso frio ≤ 4.000 px²; mesmo assim o herói vence pela saturação (3.4). O chefe de fase é o mesmo modelo nas 5 fases, **sem tingir por fase** (a cor quente invadiria a faixa proibida). A escolta tem o visual da horda.
- **Campeão × Arremessador** (princípio A, "função pela forma"): o Campeão é massa baixa e larga, inclinada para a frente, com o osso frio na arma à frente; no windup recolhe e abaixa, voltado para a linha da investida (a linha marcada no chão é o telegraph do golpe do #6, desenhado pelo #12). O Arremessador é vertical, com o osso frio no braço e na carga **acima da linha da cabeça**; no windup o braço vai para trás e para o alto e o corpo **aponta para o herói**. Como o decal dele fica longe dele, sem projétil, essa pose orientada é a única ligação entre causa e efeito. **Não acrescentar linha nem rastro até o alvo**: seria um segundo elemento com cara de telegraph.

### Restrições de arte que valem como regra de design

- **No máximo 3 tipos de horda por capítulo.** A horda tem ≤ 400 triângulos, 1 LOD, animação por partes rígidas e 1 draw por tipo (8.3, 8.5, 8.6); os 3 tipos do MVP já ocupam 3 dos 4 draws da horda, e um 4º tipo no mesmo capítulo estoura o teto. Isso limita a curva de autoria (Tuning Knobs).
- **Nenhum efeito, decal ou som por corpo nascido**: dezenas de nascimentos por segundo só usam a propriedade de instância.
- **Fora do #7, mas disparado por ele:** até `teto_vivos_horda` drops de XP (sem loot: morte pelo rugido não dá loot, Regra 10.2) no mesmo tick do rugido precisam de agregação visual (#3, #12, #24).
- **NOT SOURCEABLE** (não coberto por `docs/engine-reference/unity/`): custo de dados por instância com `RenderMeshInstanced` no Android; `MaterialPropertyBlock` com o SRP Batcher; GPU Resident Drawer em mobile; custo da troca de LUT por Volume em Android intermediário; URP Decal; VFX Graph em mobile. Tudo a medir no spike.

### Áudio (só intenção; specs do #31 e do audio-director)

- **Massa da horda:** uma cama de passos e murmúrio que cresce com `vivos_horda`, nunca um som por corpo nascido. O respiro tem de **soar** mais vazio: o silêncio relativo anuncia a lâmina.
- **Chegada do elite:** uma batida única, grave e contida, que diz "alguém com nome chegou" sem disputar com o som de aviso do telegraph.
- **Rugido:** o evento mais alto da fase, num único som, seguido da queda em massa da faixa de 21 ou mais mortes que o #6 já tem (`sfx_death_horde_l`), nunca 300 vozes.
- **Divisão:** o #7 emite os eventos; o placeholder do MVP é requisito do #12; o áudio final é do #31 (Vertical Slice); vozes, ducking e mixagem são do audio-director.

**Assets novos para `/asset-spec`:** `sfx_elite_arrive_01`, `sfx_boss_roar_01`, `sfx_horde_mass_loop`, `vfx_boss_roar_disc_large`, `ui_icon_offscreen_elite`, `ui_icon_offscreen_boss`.

*Consultado:* `art-director` (seções da Bíblia de Arte: 1, 2.1, 2.2, 3.2, 3.3, 3.4, 4.2a, 4.2e, 5.2, 5.4, 5.5, 6.5, 7.4, 7.7, 8.3, 8.6, 8.7).

## Game Feel

O #7 não tem entrada do jogador: o "feel" dele é **ritmo**, a alternância entre maré e lâmina ao longo da fase. As durações são as da Regra 5, das fórmulas e dos knobs; os valores são ilustrativos e a calibrar no protótipo. O feedback de cada momento é desenhado pelo #12 (e o golpe pelo #6); a coluna "Feedback" diz o que o jogador precisa perceber, não como.

| Momento | Sensação alvo | Duração (ilustr.) | Feedback (dono) | Não deve |
|---|---|---|---|---|
| Chegada de uma wave | A maré sobe: uma frente de corpos fecha o espaço | pulso de 4 a 8 s (`espalhar_s`) | corpos entrando pela borda da tela, em frente (#12) | chegar em bloco num único frame; nascer à vista sem surgimento |
| Respiro | Alívio curto, com expectativa | 3 a 10 s; nunca menos de 2 s (`respiro_elite_min_s`) | a tela esvazia pelo próprio massacre | durar mais de `respiro_max_s` (ilustr. 10 s; vira tédio; o #1 acende `RespiroLongo`, F10); ter horda nova nascendo, salvo a que esperava vaga |
| Chegada do elite | "Alguém grande chegou": o perigo tem nome | graça de 30 ticks (1 s) antes do 1º Aviso | silhueta distinta, seta na borda se fora da tela, som de chegada (#12, #31) | atacar antes de ser visto; chegar escondido na massa |
| Silêncio antes do chefe | A tela pesa | 5 a 8 s (`silencio_pre_chefe_s`) | queda de densidade e de som (#12, #31) | soar como fim de fase |
| Entrada do chefe e rugido | O chefe varre a horda e a arena é dele; o rugido acontece à vista (o chefe nasce a `R_chefe_m`, dentro da tela) | 1 tick de regra; a apresentação pode durar mais | onda de choque, mortes em massa em cascata, XP voando (#12) | esconder o 1º telegraph do chefe; travar a simulação (o hit-stop é só apresentação) |
| Escolta | O chefe não está sozinho, mas é o único perigo | pulsos a cada `escolta_intervalo_s` | poucos corpos fracos (#12) | encher a tela sobre o telegraph do chefe |
| Fase 1 → fase 5 | A build cresce e a fase cobra mais | curva da Seção Tuning Knobs | mais corpos por wave, elites mais próximos | subir a ameaça simultânea em vez dos corpos |

**Latência:** o #7 só faz nascer, e o nascimento aparece na tela até 1 tick depois (interpolação do #2), sem nenhuma entrada a medir.
**Medição no aparelho:** frame time no tick do rugido (até `teto_vivos_horda` mortes de uma vez), frame time durante um pulso da fase 5 e se o respiro é percebido (sinal de playtest, Acceptance Criteria).

## UI Requirements

- **Seta na borda da tela** para elite e chefe fora da câmera, lida pelo #12 nas colunas `classe` e posição, sumindo quando o inimigo entra na tela.
- **Aviso de chegada do chefe** (texto curto ou marca) no tick da entrada: a forma é decisão de UX.
- **Progresso da fase até o chefe** (opcional, decisão de UX): o #7 expõe o `tick_entrada_chefe_agendado` e o `CombatTick`; o tempo restante depois que o chefe entra é do #3 e do #12.
- **Nenhum contador de horda viva nem de wave no HUD do MVP** *(provisória)*: a maré se lê pela tela, e números de horda competem com o telegraph (Pilar 4).

> **📌 UX Flag — Horda, waves e inimigos (#7)**: este sistema tem requisitos de UI (seta de elite e chefe, aviso do chefe, progresso opcional). Na Fase 4 (Pre-Production), rode `/ux-design` para o HUD de combate **antes** de escrever épicos; as stories que citam UI devem citar `design/ux/[tela].md`, não este GDD.

## Cross-References

| Documento | Regra, seção ou ID | O que o #7 usa | Natureza |
|---|---|---|---|
| `dados-e-balanceamento.md` (#1) | Regras 2, 4, 5, 7, 10; F1, F3; OQ-5 | knobs, unidades, conversão para ticks, validação tudo-ou-nada, capacidade pela demanda declarada; contagens não remotas até o #7 derivar pico e total | Valor e regra |
| `simulacao-deterministica.md` (#2) | Regras 1, 5, 7, 8, 9, 13, 15; FS5, FS6, FS8, FS9; OQ-9, OQ-10 | ordem do compositor, `CombatTick`, `Spawn` e ids, `Essencial`, sorteio por índice de wave, hash, total de spawns | Regra e contrato |
| `fluxo-de-fase.md` (#3) | Regras 5, 6, 7, 10; F4, F5; Edge Cases (chefe e herói no mesmo tick); OQ-8 | chefe `Essencial` único, `xpDaMorte`, `tick_entrada_chefe_agendado`, XP do tick, roteiro fixo do chefe | Contrato |
| `combate-e-dano.md` (#6) | Regras 1, 2.5, 3, 5, 6, 7, 14; F5, F7, F9, F10; OQ-7, OQ-10 | o #6 move e mata; ciclo de golpes, contato, `Combate.Aplicar`, arena retangular, horda sobreposta | Contrato e exigências pendentes |
| `game-concept.md` | Core Loop, Flow State Design, Pilar 4, Technical Considerations (spike de 300 inimigos), MVP | fantasia, curva de dificuldade, conteúdo do MVP, alvo de performance | Âncora |
| ADR-0001 | `SimWorld`, `Spawn(faction, essential, xpValue, hp, x, y)`, float32, sem `Mathf` | tipos, assinatura e restrições | Decisão técnica |
| ADR-0002 | contagens de horda, pico e total nunca remotos (até a OQ-5) | regra de pacote remoto | Decisão técnica |
| `design/art/art-bible.md` | ver Visual/Audio Requirements | leitura por classe, camadas, orçamento | Requisito visual |
| `docs/consistency-failures.md` | entradas de 2026-11-04 (pico × total, `ids_de_preparacao`) | o #7 declara pico e total separados (F7, F8) | Lição aplicada |

## Acceptance Criteria

*Consultado:* `qa-lead`. Testes em `Assets/Tests/EditMode/Horda/[Classe]Tests.cs`, nomes `Cenario_Esperado`, e toda suíte afirma `testcasecount > 0` (um "0 testes, Passed" não vale). **Tipos:** [U] unidade, [I] integração, [PM] medição ou playtest do autor (n = 1), [EV] captura de tela. **BLOQ** marca o critério que depende de algo que ainda não existe. **Dublês:** `FakeWorld`, `FakeComandos` (parado, círculo, fuga), `FakeSistema6` (registra os pedidos a `Combate.Aplicar` e mata pela política do teste), `FakeSistema3`, `FakeLog`, `GeradorContador` (envolve o `Pcg32` e conta as chamadas a `NextBounded`). **Fixture `FaseTeste7`** (completa; as 16 direções e as 8 entradas de formação são literais do arquivo da fixture): arena 40 × 32, `R_spawn` 12, `R_min_spawn` 5, `margem_spawn` 2, `N_DIR` 16, teto 300, `max_nascimentos_por_tick` 20, `alcance_contato_m` 0,6; `R_chefe` 6, `dir_chefe` 0, `meia_altura_visivel_m` 8, `margem_visivel_m` 1; `respiro_elite_min` 2 s, `janela_reserva` 90 ticks, `silencio_pre_chefe` 6 s, `formacao_max_m` 1,2, `ticks_max_apos_chefe` 2700; graça elite 30, chefe 60, ciclo do Campeão 60 ticks (`duelo_min` 90), `xp_rugido_permil` 500, `respiro_max` 10 s, `instante_max` 600 s, `dps_ref` 60. Arquétipos: Soldado (HP 20, vel 3, xp 2), Enxame (HP 15, vel 4,5, xp 1), Campeão (HP 120, vel 2,5, xp 10, `dist_parada_m` 1, ciclo de 60 ticks), Chefe (HP 500, vel 2, xp 0, `dist_parada_m` 2). Horda w = 0 com `inicio` 30 s, `espalhar` 6 s, `contagem` 40, `frentes` 3 e pool {Soldado 3, Enxame 1} (fim 1080, `viagem` 134); Elite w = 1 com `inicio` 43 s (**1290**, passa a F10: ≥ 1080 + 134 + 60 = 1274); Elite w = 2 com `inicio` 44 s (**1320**); pool de elite {Campeão 1}; Chefe w = 9 no tick 5400 (passa `chefe_ok`: último `fim` 1410 = elite w = 2 em 1320 + duelo 90; 1410 + 180 = 1590 ≤ 5400), escolta 30 / 6 / 300 ticks com pool {Soldado 1}. **Variantes:** `FaseTeste7Janelas` (duas waves e um elite B que produzem as janelas [1274, 1500] e [2300, 2600]); `FaseTeste7Saturada` (teto 10); `FaseTeste7Escolta` (escolta 30 / 6 / 300 e um `FakeSistema6` que põe o chefe em Aviso nos ticks escolhidos pelo teste); `FaseTeste7Rugido` (Horda w = 0 com `contagem` 135 e teto 120). Os exemplos da Seção Formulas são casos de teste.

### Regras (AC-R)

- **R1 [I]** **GIVEN** uma `Simulation` com espião, **WHEN** roda 1 tick ativo e 1 tick com `CombatActive` falso, **THEN** o #7 é o 1º sistema, depois do nascimento não grava posição nem HP, e no tick inativo faz 0 `Spawn` com os cursores inalterados.
- **R2 [U]** **GIVEN** uma grade de 1.000 posições do herói (com cantos e bordas), **WHEN** cada corpo nasce, **THEN** 0 ≤ x ≤ L e 0 ≤ y ≤ A.
- **R3 [U]** **GIVEN** um arquétipo `Horda` com ciclo de golpes não vazio, **WHEN** o #1 valida a fase, **THEN** ela é recusada (`estrutura_ok`, F10).
- **R4 [U]** **GIVEN** a `FaseTeste7` com uma entrada w = 5 inserida no meio, **WHEN** roda o `Preparar`, **THEN** as linhas de w = 0, 1, 2 e 9 são idênticas às da fixture sem ela.
- **R5 [I]** **GIVEN** a `FaseTeste7` (teto ≥ total), **WHEN** o `FakeSistema6` mata tudo ao nascer numa execução e não mata nada na outra, **THEN** o tick de nascimento de cada corpo de horda e do elite w = 1 (1290) é idêntico nas duas; com abates, w = 2 nasce em 1320 (o `inicio` dele); sem abates, w = 2 só nasceria depois da morte de w = 1 (Regra 9 e janela), então não nasce antes do chefe e é cancelado (`ElitesCancelados` = 1); `VivosHordaNoElite` no nascimento de w = 1 (1290) é 40 sem abates e 0 com abates.
- **R6 [U]** **GIVEN** a mesma seed, **WHEN** o pool é reordenado no arquivo, **THEN** a tabela de composição é idêntica; **WHEN** um pool de 1 arquétipo ganha um 2º, **THEN** as direções sorteadas são idênticas; e o gerador recebe 0 chamadas a partir do tick 1.
- **R7 [U]** **GIVEN** o herói em (L, A) e d = (1, 0), (0, 1) e a diagonal, **THEN** o ponto é espelhado e dist² ∈ [0,9801·R², 1,0201·R²]. **GIVEN** que o herói andou no tick t, **THEN** o corpo nascido em t usa o H do fim de t − 1. O chefe usa `dir_chefe`.
- **R8 [U]** **GIVEN** teto 10, 25 corpos vencidos de 2 pulsos sobrepostos e 0 vivos, **WHEN** roda o passo, **THEN** nascem 10 na ordem (`tick_do_corpo`, w, k) e 15 esperam; com 4 mortes, os 4 seguintes nascem no tick seguinte; com a horda no teto, elite e chefe nascem assim mesmo.
- **R9a [U]** **GIVEN** o elite A vivo, a entrada B vencida em t e t + 41 dentro de uma janela, **WHEN** A morre no passo do #6 em t + 40, **THEN** B nasce em t + 41 e `EliteEsperouTicks` = 41; com dois `inicio` iguais, nasce primeiro o de menor w.
- **R9c [U]** (janela de respiro) **GIVEN** a `FaseTeste7Janelas` (janelas do elite B: [1274, 1500] e [2300, 2600]; `janela_reserva` 90), B vencido em 1300 com A vivo, e A morto no passo do #6 em 1550, **THEN** B não nasce em 1551 (fora de janela) e nasce em **2300** (`EliteEsperouTicks` = 1000, contado de `inicio` ao nascimento); **GIVEN** só a janela [1274, 1500], **THEN** B nunca nasce, é cancelado na entrada do chefe e `ElitesCancelados` = 1 (sem teto de segurança).
- **R9d [U]** **GIVEN** a `FaseTeste7`, **THEN** as janelas são calculadas no `Preparar` só dos dados (mudar os comandos ou a política de abate não muda nenhuma janela) e nenhuma passa de `inicio(C) − silencio_pre_chefe_ticks − duelo_min_ticks` = 5400 − 180 − 90 = 5130.
- **R9b [I]** **GIVEN** um elite com graça 30 (chefe 60) nascido em T, com o herói ao alcance, **THEN** o 1º Aviso começa em ≥ T + 30 (chefe ≥ T + 60). *(emenda (a) aplicada no #6 em 2026-11-05; o #6 cobre o lado dele em R7b; o BLOQ saiu)*
- **R10 [I]** **GIVEN** a `FaseTeste7Rugido` sem abates (no tick 5400: 120 corpos de horda vivos, 15 pendentes, o elite w = 1 vivo e w = 2 esperando), **WHEN** vence o chefe, **THEN**, nesta ordem: 1 `Spawn(essential)`; 121 pedidos `Rugido` tipados, sem valor de dano e na frente da fila (120 de horda e 1 no elite vivo); `cur_horda` = 135 e `cur_elite` = 2; `HordaCancelada` = 15 e `ElitesCancelados` = 1 no `FakeLog`; 1 evento `Rugido`; 0 nascimentos de horda ou elite nesse tick e em todos os seguintes (só escolta). **GIVEN** o `FakeWorld` cheio, **THEN** sai `EssentialSpawnRejected`.
- **R11 [U]** **GIVEN** a escolta da F2, **THEN** 30 corpos em 5 pulsos, de 5700 a 6900, uma direção por pulso; com o teto cheio eles esperam e nunca são cancelados; se o chefe morre antes, os pendentes não nascem.
- **R11b [U]** **GIVEN** a `FaseTeste7Escolta` com o chefe em Aviso de 5690 a 5729 e em Impacto em 5730, **WHEN** o pulso 0 vence em 5700, **THEN** o #7 lê o estado gravado no fim de t − 1, então os 6 corpos nascem em **5732** (em 5731 ele ainda lê Impacto); com o chefe em Perseguindo, nascem em 5700.
- **R16 [U]** (limite por tick) **GIVEN** teto 300, 100 vivos e 200 corpos pendentes, **THEN** nascem **20** por tick, em 10 ticks, na ordem (`tick_do_corpo`, w, k); um elite adiado que vence no mesmo tick que corpos de horda nasce além dos 20; no tick do chefe só nasce o chefe (Regra 15).
- **R17 [U]** (frentes distintas) **GIVEN** o herói em (2; 2), `R` 12, `frentes` 3 e direções sorteadas (1; 0), (−1; 0) e (0; 1), **THEN** em todo tick a frente 0 nasce em (14; 2), a frente 2 em (2; 14) e a frente 1 (espelhada para (1; 0), igual à frente 0) avança para a direção seguinte da tabela e nasce num ponto distinto dos outros dois (ilustr. (13,09; 6,59) com a tabela de 22,5°), **mesmo nos ticks em que as frentes 0 e 2 não têm corpo nascendo** (leitura única, Regra 7.4); a tabela de composição não muda e o gerador recebe 0 chamadas; com `frentes` > 5 e o herói no canto, a duplicata é aceita (fica a original) e conta em `TicksNoCanto`. **GIVEN** `frentes` > `N_DIR`, **THEN** o #1 recusa.
- **R18 [U]** (chefe na tela) **GIVEN** a grade de posições do herói e `R_chefe` 6, **THEN** a distância do chefe ao herói fica em [0,99 × 6, 1,01 × 6] = [5,94; 6,06], ou seja, ≥ `R_min_spawn` (5) e ≤ `meia_altura_visivel_m − margem_visivel_m` (7), e o ponto fica na arena.
- **R19 [I]** (sem contato de elite e chefe) **GIVEN** o herói parado colado num elite e no chefe por 300 ticks, ambos em Perseguindo e sem golpe, **THEN** o dano de contato recebido é **0**; com um Soldado colado, é > 0. *(emenda (h) aplicada no #6 em 2026-11-05; o #6 cobre o lado dele em R5b; o BLOQ saiu)*
- **R20 [I]** (investida) **GIVEN** um Campeão da fase 1 com o herói ao alcance, **THEN** o ciclo só tem a investida; o Aviso marca uma linha na direção do herói travada no 1º tick do Aviso; no Impacto o Campeão termina deslocado ao longo dessa linha e o herói na linha leva dano, mesmo que tenha andado para o lado da posição original. *(emenda (g) aplicada no #6 em 2026-11-05; o #6 cobre o lado dele em R6f; o BLOQ saiu)* A recusa do #1 a um Campeão da fase 1 com golpe em círculo fica PRONTA.
- **R12 [I]** **GIVEN** a varredura de `Seeds7` × 3 políticas de comando, **THEN**: 0 nascimentos fora da arena ou a menos de `R_min_spawn`; exatamente 1 `essential`; 0 invocações; spawns ≤ F7; 0 `Spawn` depois de *Encerrada*.
- **R13** → ver D3.
- **R14 [U]** **GIVEN** a `FaseTeste7` convertida, **THEN** `tick_entrada_chefe_agendado` = `inicio(C)` em ticks; o `xpValue` de cada `Spawn` = `xpDaMorte` do arquétipo; `essential` só no chefe.
- **R15 [U]** **GIVEN** um elite adiado (que esperava outro elite) que nasce num tick em que corpos de horda também vencem, **THEN** o id do elite é menor que os da horda; no tick do chefe só o chefe nasce.
- **RB [I]** (comportamento) **GIVEN** 64 corpos de horda em Perseguindo, **THEN** o alvo de cada um é herói + tabela[`id mod 32`] (≥ 32 alvos distintos); o alvo de elite e chefe é a posição do herói lida no tick de início do Aviso, sem deslocamento; elite e chefe ficam parados em Aviso, Impacto e Recuperação (fora o deslocamento da investida). *(emenda (b) aplicada no #6 em 2026-11-05; o #6 cobre o lado dele em R5c e R6e; o BLOQ saiu)*
- **RB2 [U]** (encaixe no alvo) **GIVEN** um corpo a 0,01 m do alvo com passo de 0,1 m, **THEN** a posição vira exatamente o alvo, é finita (sem NaN) e não oscila nos 10 ticks seguintes com o herói parado. *(emenda (b) aplicada no #6 em 2026-11-05; o #6 cobre o lado dele em R5c; o BLOQ saiu)*
- **C1 [I]** (contadores de diagnóstico) **GIVEN** a `FaseTeste7Saturada` (teto 10) sem abates, **THEN** `TicksNoTeto` = 4461 (o corpo k = 9 vence em 940; 5400 − 940 + 1; confirmar na implementação) e `HordaEsperouTicks` > 0; **GIVEN** o herói parado em (2; 2) por 100 ticks ativos, `TicksNoCanto` = 100, e em (20; 16) = 0. `VivosHordaNoElite` está no R5. `OfertasNoRugido` é contado pelo #5 (o AC mora no #5).

### Fórmulas (AC-F)

- **F1 [U]** Ticks 900, 958, 1075 e 1080 do exemplo. `inicio_s` = 0 vence no tick 1, nunca no 0. `inicio_s` = 0,05 → 2 (meio para longe de zero). `k × espalhar` em `long` com `contagem` 100.000, `espalhar_ticks` 30.000 e k = 99.999 (produto ≈ 3 × 10⁹, acima de `int`): `tick_do_corpo` = `inicio_ticks` + 29.999.
- **F2 [U]** 5700, 6900, `n_pulsos` 5, 1500 < 2700 passa; total 0 passa; intervalo 600 é recusado.
- **F3 [U]** Chamadas contadas pelo `GeradorContador`: Horda 40/3 → 43; Elite → 2; Chefe 30/6 → 35; escolta 0 → 0. Com um stub de r: 0 a 2 → Soldado, 3 → Enxame. O golden das saídas brutas do PCG por seed: **BLOQ: ADR-0001 Proposed.**
- **F4 [U]** O exemplo dá exatamente (23,2; 16,6) em `float32`; uma formação que clampa sobre o herói cai em `P_f`.
- **F5 [U]** 26,24 passa e R = 15 é recusado; `R_min` 11,76 passa e 11,77 é recusado; também são recusados `R_min` ≤ `alcance_contato_m`, |d|² 0,98 e `dir_chefe` = `N_DIR`. `chefe_na_tela_ok`: `R_chefe` 6 passa, 7 e `R_chefe` > `R` são recusados. `spawn_fora_ok`: `R` 12 passa e `R` 8 é recusado.
- **F6 [U]** Com 287 vivos e 20 pendentes nascem 13, esperam 7 e `HordaEsperouTicks` += 7; com 301 vivos, nascem 0.
- **F7 [U]** 514 e `cap_ids` ≥ 644 (exemplo da Seção Formulas). **[I]** Na `FaseTeste7`, `total_spawns_7` = 40 + 2 + 1 + 30 = 73, e os spawns reais ficam ≤ 73 em `Seeds7`.
- **F8 [U]** 302 → 379. **[I]** Na `FaseTeste7`, `pico_vivos_7` = min(300, 40 + 30) + 1 + 1 = 72, e o máximo de vivos observado fica ≤ 72.
- **F9 [U]** `xp_max` 700 passa e `xp_min` 520 é recusado. **[I]** Com todos os abates feitos pelo herói, `HordaCancelada` = 0 e `ElitesCancelados` = 0, o XP somado pelo `FakeSistema3` (sem o chefe) fica em [`xp_min`, `xp_max`].
- **F10 [U]** Elite em 1274 passa e em 1273 é recusado (`viagem` 134); a próxima `Horda` precisa de ≥ 1364 (`duelo_min` 90); o chefe precisa de ≥ 5234; uma fase inválida por cláusula de `estrutura_ok`, **uma linha de tabela por cláusula** (incluindo horda com ciclo de golpes, graça do chefe + `aviso_chefe_ticks_min` ≥ `ticks_max_apos_chefe`, `escolta_por_pulso` = 0 com escolta, arquétipo repetido no pool, `vel_per_s` = 0, `inicio(C)` = 0, `dist_parada_m` fora da faixa) e uma por faixa (`respiro_elite_min` ≥ 60, graça de 15 a 60); `reserva_ok` recusa um elite sem janela de largura ≥ 90 ticks.
- **F11 [U]** ρ = 0,89 gera `CargaTankAlta` e a fase **passa** (sinal não bloqueante); a wave de 120 × 20 dá fila de exatamente 2.040 HP, **102** corpos, sem saturação (dataset do exemplo: 480 corpos × 20 HP, chefe no tick 5400, `dps_ref` 60, `rho_max` 0,8); `RugidoMuitosNiveis`: o exemplo com `vivos_est_chefe` = 300 e `xp_rugido_permil` 500 dá **7** níveis (acende) e com 20 vivos dá **0** (não acende); `RespiroCurto` e `RespiroLongo` acendem e não acendem nos casos do exemplo; conta em `decimal`.

### Casos de borda (AC-E)

- **E1 [I]** **GIVEN** `CombatHold` aberto no meio de um pulso por 1.000 ticks, **THEN** os corpos nascem nos mesmos `CombatTick`, sem lote na retomada.
- **E2 [I]** **GIVEN** a oferta aberta no fim de `inicio_chefe − 1`, **THEN** o chefe nasce no 1º tick ativo, com `tickNascimento` em `CombatTick` igual ao agendado.
- **E3 [I]** **GIVEN** o rugido com 0 corpos de horda, **THEN** sai o evento `Rugido` e 0 pedidos.
- **E4 [U]** **GIVEN** escolta 0, **THEN** o estado vai a Escolta esgotada no tick do chefe, sem nenhum sorteio.
- **E5 [U]** **GIVEN** H não finito, **THEN** o #7 lança nos dois modos.
- **E6 [U]** **GIVEN** `Spawn` −1 para um corpo de horda, **THEN** no modo estrito lança; no não estrito `SpawnsRejected` +1, o cursor avança e o próximo corpo nasce no mesmo tick.
- **E7 [U]** `px == L` fica onde está; o herói com `H.x == L` e `d.x > 0` espelha.
- **E8 [I]** **GIVEN** o herói morto no tick do chefe, **THEN** `DerrotaHeroi` com `ChefeVisto` verdadeiro.
- **E9 [U]** **GIVEN** a graça do chefe ≥ `ticks_max_apos_chefe`, **THEN** o #1 recusa a fase.
- **E10 [I]** **GIVEN** um elite vivo em Aviso na entrada do chefe, **THEN** ele recebe `Rugido` e morre no mesmo tick com causa `Rugido` (o XP entra no total do tick do rugido: `floor(10 × 500 / 1000)` = 5 se for o único), e o golpe dele é cancelado pelo #6 real (nenhum Impacto; com o `FakeSistema6` vale só a causa).
- **E11 [I]** **GIVEN** um Arremessador com recarga pronta a mais de `alcance_inicio_aviso_m` do herói, **THEN** ele não inicia Aviso até entrar no alcance. **GIVEN** `meia_altura_visivel_m − margem_visivel_m` = 7, **THEN** o #1 aceita `alcance_inicio_aviso_m` = 7,0 e recusa 7,01 e 8 (entre 7 e `R_spawn_m` 12). *(emenda (e) aplicada no #6 em 2026-11-05; o #6 cobre o lado dele em R6d; o BLOQ saiu, e a recusa do #1 fica PRONTA)*.
- **E12 a E18** (casos de borda sem AC antes). **E12 [U]** `Spawn` −1 para um elite ou um corpo de escolta: no estrito lança; no não estrito `SpawnsRejected` +1 e o cursor correspondente avança. **E13 [I]** um elite esperando durante uma oferta (`CombatHold` ≠ 0) continua esperando e nasce no primeiro tick ativo livre dentro de uma janela. **E14 [I]** escolta que não nasce antes de `DerrotaTempo`: a tentativa acaba em derrota por tempo e os corpos pendentes não nascem. **E15 [I]** o herói morto no tick do rugido perde o XP do rugido (Regra 5.4 do #3). **E16 [I]** o ciclo do chefe é idêntico em tentativas com seeds diferentes. **E17 [I]** um elite adiado sem janela posterior é cancelado na entrada do chefe (`ElitesCancelados` = 1). **E18 [U]** o rugido soma o XP das mortes `Rugido` no total do tick e o #3 sobe no máximo 1 nível (excedente perdido); 10 Enxames (XP 1) rendem 5, não 0. **BLOQ: emenda (b) ao #3.**

### Integração (AC-I)

- **I2 [I]** A ordem é #7 → #8 → #6 → #3 → #16 por espião, e o tempo do #7 conta em `CombatTick`. **BLOQ: ADR-0001 Proposed.**
- **I3a [I]** Exatamente 1 `Essencial` por fase em `Seeds7`; o nascimento do chefe = `tick_entrada_chefe_agendado` lido pelo #3; 0 `ChefeAusente`. Nas 5 fases do MVP: **BLOQ: dados das 5 fases.**
- **I3b [I]** O rugido sobre 120 corpos soma ao `XpAtual`, no mesmo tick, `floor(Σ xpDaMorte × xp_rugido_permil / 1000)` e sobe no máximo 1 nível (o excedente se perde); a oferta desse nível abre na hora, sem atraso próprio. PRONTO com `FakeSistema3`; com o #3 real, **BLOQ: ADR-0001 e emenda (b) ao #3.**
- **I6 [I]** O `Rugido` no #6 real: letal, sem mitigação nem `dano_max`, sem knockback nem hit-stop, 1 evento agregado, `GolpesLimitados` = 0. **BLOQ: ADR-0001 *Proposed*** (emenda (c) aplicada no #6 e `DeathCause.Rugido` na Emenda 15 do ADR em 2026-11-05; o #6 cobre o lado dele em R3b).
- **I12 [I]** As colunas `classe`, `arquetipoId` e `tickNascimento` estão corretas em cada spawn. **BLOQ: ADR das colunas do `SimWorld`.**

### Determinismo e hash (AC-D)

- **D1 [I]** **GIVEN** a mesma (seed, w, dados), comandos parado × círculo e 3 políticas de abate, **THEN** a tabela de composição é idêntica byte a byte (posições finais e ticks de nascimento podem diferir).
- **D2 [U]** Mudar o w de uma entrada muda só a composição dela.
- **D3 [U]** Mudar `cur_horda`, `cur_elite`, `chefe_nascido` ou `cur_escolta` muda o `StateHash`; mudar a tabela, `vivos_horda` ou os contadores de diagnóstico não muda. **BLOQ: ADR-0001** (com `FakeWorld` vale a lista de campos).
- **D4 [U]** Por reflexão: sem `System.Random`, `UnityEngine`, `double` nem `static` mutável no assembly do #7.
- **D5 [I]** Mesma seed e mesmos comandos numa fase completa (≥ 7.000 ticks): o `StateHash` é igual em todos os ticks. **BLOQ: ADR-0001.**
- **D6 [PM]** Duas execuções no **mesmo build** IL2CPP ARM64 do aparelho dão tabela e hash do tick final iguais em todos os ticks; o golden é por plataforma, e Editor × aparelho **não** é critério (o ADR-0001 só promete mesmo build e mesmo runtime; `float` entre runtimes é NOT SOURCEABLE). **BLOQ: aparelho de referência não verificado.**
- **D7 [U]** Uma entrada que nunca começa (fase encerrada antes) tem a composição sorteada assim mesmo. *(emenda (b) aplicada no #2 em 2026-11-05; o BLOQ saiu)*

### Desempenho (AC-P)

- **P1 [PM]** No aparelho de referência, marker `Horda.Tick` via `ProfilerRecorder` (conferir se funciona em build Release/IL2CPP: NOT SOURCEABLE), 600 ticks depois de 60 de aquecimento, em 4 cenários: (a) 300 vivos e 200 pendentes no teto (`vagas` = 0); (b) tick do chefe com 300 pedidos `Rugido`, **repetido N vezes a partir de um snapshot** (o rugido ocorre uma vez por fase, então p95 e p99 sobre ticks distintos não valem: reportar o máximo e a distribuição, com o aparelho aquecido); (c) escolta; (d) **20 nascimentos por tick sustentados por 10 ticks** (100 vivos, 200 pendentes), incluindo o consumo de `tickNascimento` pelo #12. p95 e p99 contra `orcamento_horda_ms`. No cenário (b) reportar também o **passo completo da simulação** (todos os sistemas) no tick do chefe, p99 e ticks descartados por `MaxTicksPerFrame`. **BLOQ: aparelho e spike.** No Editor vale só como sanidade.
- **P2 [I]** O delta de `GC.GetAllocatedBytesForCurrentThread` é 0 em 600 ticks que **incluem** o tick do chefe (300 pedidos `Rugido`), a escolta e uma espera de elite, depois de 60 ticks de aquecimento (o JIT do Editor aloca no primeiro uso de um caminho); o `Preparar` aloca só o que declara (tabela de composição, direções, janelas, escolta e o scratch da F4), uma vez. PRONTO no Editor.
- **P3 [U]** Com 0 e com 5.000 pendentes, as linhas visitadas por tick ficam ≤ `nascem` + 1 (contador instrumentado), e a passada de `vivos_horda` e "há elite vivo" visita ≤ n vivos (n ≤ 303) uma vez por tick: prova o "sem custo por tick" da Regra 8 sem depender de relógio.
- **P4 [PM]** No tick do rugido, **0 cargas síncronas de asset** (o modelo, o shader, o LUT e o disco do chefe foram pré-aquecidos no `Preparar`, exigência ao #12) e o frame completo no aparelho cabe no orçamento. **BLOQ: #12 sem GDD, aparelho e spike.**

### Sinais de playtest, n = 1 (AC-S, ADVISORY, todos **BLOQ: `docs/acceptance/mvp.md` inexistente**)

O pior valor aceito entra no `mvp.md` **antes** da sessão, com o hash do build; nunca é fixado depois de ver o resultado.
- **S1** Leitura do respiro, **jogada com o Tank** (o perfil que mata devagar, para quem a espera da Regra 8 e da Regra 9 pode tirar o respiro), nas mesmas fases do S2: em 5 elites, o log grava `VivosHordaNoElite` e `EliteEsperouTicks`, e o autor marca "vi o elite chegar" (sim ou não). Pior valor sugerido: `VivosHordaNoElite` ≤ 20% do teto em ≥ 4 de 5.
- **S2** O Tank não se afoga: em 3 fases completas como Tank, `HordaCancelada` = 0, mais `HordaEsperouTicks` e `TicksNoTeto` (como % dos ticks), comparados com a `saturacao_pct` prevista pela F11.
- **S3** Maré e lâmina: por fase, o autor responde sim ou não; o log grava o pico de mortes de horda por segundo (Descarga) e os ticks com Aviso ativo enquanto `vivos_horda` > 50% do teto.
- **S4** Escolta: o dano de contato recebido durante o chefe (somado pelo #5 a partir dos eventos do #6), para medir a "pressão leve" da Regra 11.
- **S5** A maré (OQ-16): por fase, o dano de contato recebido por minuto (somado pelo #5 a partir dos eventos do #6); o valor da fase 5 deve passar o da fase 1. Se não passar, pedir bloqueio de corpo ou separação ao #6.

### Evidência de tela (AC-EV, bloqueante para a story)

- **EV1 [EV]** Capturas em `production/qa/evidence/horda-[caso]-[data].png`, com seed, fase e tick na legenda para a cena se reproduzir: (a) wave chegando por 3 frentes, com overlay dos pontos de nascimento de cada frente; (b) respiro com o elite nascendo; (c) o tick do rugido; (d) o herói no canto com o nascimento espelhado. Arte provisória vale como prova da regra; o surgimento e a seta na borda são do #12 e a câmera é do #4, ambos sem GDD.

### Não testável como escrito (verificação por revisão)

- A forma de fase típica (5 a 7 waves, cerca de 3 minutos até o chefe) e a curva das 5 fases são **meta de autoria**: o relatório do #1 lista waves, elites e o tempo até o chefe de cada fase, para revisão contra a curva de referência.
- "Fora da área visível" (Regra 7.6) só vira teste quando o #4 definir a meia-diagonal visível (F5); até lá vale o proxy `R_spawn_m ≥ meia_altura_visivel_m + margem_visivel_m`.

**Fixtures:** `Seeds7` (lista constante e versionada, só com acréscimos, ≥ 50 seeds, incluindo 0, 1, `uint.MaxValue` e toda seed que já revelou bug); fábricas `FaseTeste7`, `FaseTeste7Janelas`, `FaseTeste7Saturada` (teto 10), `FaseTeste7Escolta` e uma fase inválida por cláusula da F2, da F5 e de `estrutura_ok`; tabelas literais (16 direções, 8 de formação, grade de posições do herói); políticas de comando e de abate; golden de composição por seed, conferido primeiro contra o exemplo da F3 calculado à mão e **nunca regenerado para fazer um teste passar** (BLOQ: ADR-0001).

**Resumo dos BLOQ:** ADR-0001 *Proposed* (F3 golden, I2, I3b com o #3 real, I6, D3, D5); aparelho de referência (D6, P1, P4, que também esperam o spike); ADR das colunas do `SimWorld` (I12); emendas ao #6: nenhuma (as emendas (a), (b), (c), (e), (f), (g), (h) e (i) já estão aplicadas); emenda (b) ao #3 (XP do rugido em permil, no máximo 1 nível: I3b e E18); dados das 5 fases (I3a); `docs/acceptance/mvp.md` (S1 a S5). Todo o resto fica PRONTO com dublês.

## Open Questions

| ID | Pergunta | Dono | Quando |
|---|---|---|---|
| OQ-1 | **Resolvida em 2026-11-05 (decisão do autor, /design-review):** as mortes pelo rugido **não** disparam efeitos de abate (#8) nem dão loot (#24), e dão metade do XP (Regra 10.2). Pergunta original: as mortes pelo rugido disparam efeitos de abate da build e dão loot? | autor | resolvida |
| OQ-2 | **Resolvida em 2026-11-05 (decisão do autor, /design-review, 2ª passada):** o elite atrasado espera a próxima janela de respiro e nunca nasce no meio de uma wave; sem janela, é cancelado (Regras 9 e 10.3). Pergunta original: um elite que esperava e cai no meio de uma wave é aceitável? | autor | resolvida |
| OQ-3 | Ids esgotados por bug de dado da horda derrubam também o chefe (`Spawn` essencial rejeitado). Vale reservar 1 id para o essencial? | #2 (`technical-director`) | ADR das colunas do `SimWorld` |
| OQ-4 | **Resolvida em 2026-11-05 (decisão do autor, /design-review, 2ª passada):** o rugido sobe no máximo 1 nível (`niveis_rugido_max`), o excedente se perde; a oferta abre na hora (Regra 10.2, revista em 2026-11-05 por decisão do autor, a reavaliar). Pergunta original: a cadeia de level-ups pelo XP do rugido precisa de um sinal no build ou de um limite? | `systems-designer`, com #3 e #16 | resolvida |
| OQ-5 | Apresentação do rugido (hit-stop global, som, VFX, cascata das mortes) | #12 e #31 | GDD #12 |
| OQ-6 | A câmera para na borda da arena? Se sim, nascimentos perto dos cantos ficam visíveis e precisam de surgimento (Regra 7.6). | #4 | GDD #4 |
| OQ-7 | A F11 (`carga_tank`) vira bloqueante quando a taxa de abate do Tank sair de fórmula (#6, #8, #10)? | `systems-designer` | GDDs #8 e #10 |
| OQ-8 | **Resolvida em 2026-11-05 (decisão do autor, CD-GDD-ALIGN):** o rugido mata também o elite vivo, com XP (Regra 10.2). Pergunta original: o rugido deveria atingir elites vivos? | autor | resolvida |
| OQ-9 | Separação entre inimigos e bloqueio de corpo (hoje a horda se sobrepõe; o anel de mira por `id mod 32` é paliativo) | #6 e `ai-programmer` | depois do spike de performance (OQ-7 do #6) |
| OQ-10 | Inimigo à distância na horda comum, invocações e adds do chefe de capítulo por sub-cronograma (`máx_invocações` hoje 0) | `game-designer` | Vertical Slice |
| OQ-11 | Fases de função (escoltar, proteger um NPC): o NPC é um spawn do #7 ou do #20, e entra em `ids_de_preparacao`? | #20 | GDD #20 (fora do MVP) |
| OQ-12 | Mais de um `Essencial` por fase (OQ-8 do #3): `essenciais_declarados` e a vitória esperando "nascidos igual a declarados" | #7 e #1 | pós-MVP |
| OQ-13 | ADR das colunas do `SimWorld` (#6 e #7): o #7 não acrescenta colunas; confirma `classe`, `arquetipoId` e `tickNascimento` | `technical-director` | antes da primeira story do #7 |
| OQ-14 | Os números da curva das 5 fases, `teto_vivos_horda`, a arena e `R_spawn_m` | autor | protótipo e spike de performance |
| OQ-15 | Curva de XP por fase: as 5 fases precisam passar juntas pela F5 do #3 com as duas pontas da F9; a alavanca esperada é uma curva de XP e `nivel_max` por fase no snapshot do #3, não XP diferente por fase no #7. | autor, com `economy-designer` | protótipo e GDD #1 |
| OQ-16 | O contato satura com poucos corpos e não há bloqueio entre corpos (#6): a maré é espetáculo e XP, não pressão de dano. Se o playtest (AC-S5) mostrar que o dano por minuto na fase 5 não passa o da fase 1, o #6 ganha bloqueio de corpo ou separação (junto da OQ-9). | autor, com #6 | playtest do protótipo |
| OQ-17 | Recomendados da 2ª passada do `/design-review` **não aplicados** (ficam para o protótipo e o spike): canto como refúgio (fechar o chanfro de canto ou limiar em `TicksNoCanto`); circular sem tomar contato (fase 1 com um tipo de horda de `vel` ≥ 85% da do herói); suavizar os picos da curva (35, 45, 55, 70 e 85%) e adiar o círculo do Campeão para a fase 5; `viagem_ticks` por quantil do pool (o Bruto raro encarece todo vão de elite); `alcance_inicio_aviso_m` da investida ≤ deslocamento + raio da linha, e A ≥ 36 ticks no 1º elite da fase 1; a escolta chegar sobre o próximo Aviso do chefe (gatilho por ticks até o próximo Aviso); `xp_tank_est` e `hp_horda_mult_fase` na F11 e `dps_ref` como curva; loot perdido do Tank (#24); origem do `orcamento_horda_ms`; fingerprint FNV da tabela de composição no hash; `mira_offset_max_m` ≤ 0,9 × `alcance_contato_m`. | autor, `level-designer`, `economy-designer` | protótipo e spike |
