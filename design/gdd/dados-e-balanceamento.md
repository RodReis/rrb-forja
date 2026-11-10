# Dados e balanceamento (#1)

> **Status**: In Review — `/design-review` de 2026-11-03: 1ª passada NEEDS REVISION (6 bloqueantes, aplicados) e 2ª passada NEEDS REVISION (8 bloqueantes, aplicados no mesmo dia); falta só a conferência curta dos 8 pontos, sem 3ª revisão completa
> **Author**: Rodrigo Reis + agentes (systems-designer)
> **Last Updated**: 2026-11-05 (F3: o total de spawns da tabela de ids tem três termos e a conferência se divide entre o build e o compositor; origem: `/propagate-design-change`, pendência P2); 2026-11-04 (F3: capacidade da tabela de ids contra o total de spawns; origem: `/consistency-check` e OQ-1 do #2)
> **Last Verified**: 2026-11-03
> **Implements Pillar**: Habilitador; sustenta o Pilar 2 (Toda escolha pesa) e o Princípio de Negócio (Poder conquistado, não comprado)
> **Creative Director Review (CD-GDD-ALIGN)**: REVISED 2026-11-03 — CONCERNS na 1ª passada (C1 elegibilidade da reforja movida para o #18; C2 data em cada passo do histórico; C3 efeito de buff temporário anotado; C4 pacote nunca escolhido por pagamento); C5 (política interina "só buffs") anotada na OQ-10, não aplicada

## Summary

O #1 Dados e balanceamento é a camada onde moram todos os valores de gameplay do jogo, com dono, unidade e faixa segura: ele os valida tudo ou nada, converte o tempo para os ticks da simulação e entrega a cada fase um conjunto imutável e versionado, que o jogo e a simulação headless leem igual. Ele existe para que nenhum número seja fixo no código, para que todo balanceamento seja rastreável (o histórico de revisões classificadas como `nerf`, `buff`, `correcao` ou `neutra`, com data, é o fato de que a Reforja #18 precisa para decidir a reforja grátis por nerf) e para que a sobrescrita remota do pós-lançamento entre por lista branca, só entre partidas, sem o #1 depender de rede.

> **Quick reference** — Layer: `Foundation` · Priority: `MVP` · Key deps: `None` (dependem dele: #2, #3, #5, #6, #7, #8, #10, #16, #17, #18, #26, #28, #29)

## Overview

O **#1 Dados e balanceamento** é a camada de onde todo sistema de gameplay lê os seus valores: dano, cooldowns, curvas de XP, pesos de oferta de skills, capacidades da fase, contagens de horda e tetos da economia. Ele é dono de três coisas. Primeiro, das **definições autorais** (o que existe no jogo: skills, inimigos, fases, raridades) e dos **knobs** de cada GDD, que vivem aqui e não no código, como exige o padrão do projeto. Segundo, da **validação** desses dados antes de qualquer uso: tipos, faixas seguras de cada knob, referências cruzadas entre definições e a regra do ADR-0001 de que nenhum tempo pode virar menos de 1 tick; um valor inválido nunca chega ao jogo em silêncio. Terceiro, da **versão do conjunto de dados**, que identifica o balanceamento vigente em cada partida, no log de eventos (#5) e na simulação headless, que lê exatamente os mesmos números do jogo. O remote config do pós-lançamento entra como um **provedor de sobrescrita** injetado pelos Serviços online (#29): o #1 não depende de rede e funciona igual offline. O jogador nunca interage com este sistema; ele sente o que o sistema permite: números coerentes entre o que vê e o que a simulação mede, e, no pós-lançamento, balanceamento corrigível e rastreável sem uma nova versão do app.

## Player Fantasy

**Enquadramento: indireto.** O jogador nunca usa este sistema; ele sente os efeitos.

**"A balança do ferreiro não mente."** O jogador nunca vê este sistema, mas aposta nele toda vez que sela uma skill. Antes de uma decisão irreversível, ele precisa confiar que o número da carta é o número que a horda vai sentir: dano, cooldown e área se comportam como prometem, e o que ele lê é o que o combate aplica. Quando a run termina e ele sente que foi a build que venceu, ou que perdeu, quem sustenta essa leitura é este sistema. Nenhum valor chega ao jogo sem ser aferido, e um erro de dado nunca vira surpresa no meio da fase. Quando o balanceamento muda, a mudança deixa marca: cada partida sabe sob qual balanceamento foi jogada.

*Pilar servido:* **Pilar 2, Toda escolha pesa** — uma consequência permanente só é aceitável se os números em que ela se apoia forem honestos (o selamento é definitivo, e a lição do Diablo 2 em `game-concept.md` L292 é que build permanente com patch silencioso gera revolta). Apoio ao **Pilar 4, Massacre com peso**: o impacto que o jogador sente é o impacto que o dado define.

*O que esta seção não promete* (fica com outros sistemas): balanceamento justo ou bem calibrado (o #1 garante coerência e validação, não a qualidade do tuning); números exatos visíveis na UI ou nas notas de patch (UI e Live Ops); a reforja grátis por nerf (política do Pilar 2 e da Reforja #18, que o #1 só viabiliza ao guardar a versão dos dados); dispensar update do app para conteúdo novo (só o ajuste de valores existentes dispensa); remote config já no lançamento (o conceito pede a arquitetura desde o início, mas o remote config é `NOT SOURCEABLE`, L349); integridade do ranking ou anti-cheat (exigem servidor).

*Consultado:* `creative-director` (3 enquadramentos; recomendado o A com o fecho do B, adotado).

## Detailed Design

### Core Rules

Termos: **partida** = uma run de fase (do carregamento da fase até a vitória, a derrota ou o abandono); **conjunto de dados** = todas as definições e knobs que um build carrega; **knob** = um valor ajustável que um GDD declara; **definição** = algo que existe no jogo (skill, inimigo, fase, raridade, função).

1. **Posse.** O #1 é dono do **valor**, da **unidade**, da **faixa segura** e, quando houver, do **pior valor aceitável** de cada knob, além das **definições autorais** (skills, inimigos, fases, raridades, funções, capacidades por fase) e dos **tetos da economia** (#26). Cada GDD continua dono do **significado** e da **fórmula** do seu knob. Todo valor de gameplay nasce como entrada do #1 e nunca como literal no código.
2. **Nascimento de um knob.** O GDD dono declara o knob com: ID estável, GDD dono, tipo (`float` de 32 bits ou `int`), unidade, faixa segura (mínimo e máximo), valor padrão, pior valor aceitável e `sentido` (`menor_melhor` ou `maior_melhor`), marca `remoto` (sim ou não), marca `aceite` (`sim` ou `não`, **sempre explícita**: o knob de aceite nunca é deduzido da presença de `pior`) e a justificativa (link para a fórmula ou para a razão). `pior` e `sentido` são obrigatórios quando `aceite: sim` e proibidos quando `aceite: não` (fórmula F6). Knob sem dono, sem unidade ou sem faixa é recusado pela validação.
3. **Identificadores.** Todo knob e toda definição têm ID estável em `snake_case`, único dentro do seu tipo. Um ID **nunca é reutilizado nem removido**: uma definição aposentada é marcada `deprecated` e continua resolvendo para saves (#28) e logs (#5) antigos. No build (ADR-0002), cada ID vira um índice inteiro atribuído pela ordem ordinal dos IDs, nunca pela ordem de iteração de um dicionário (ADR-0001).
4. **Unidades.** O nome do campo declara a unidade: `_s` (segundos), `_ticks` (só janelas curtas, como i-frames e telegraph), `_per_s` (taxas por segundo, como velocidade, DPS e regeneração). Os demais seguem a unidade declarada no knob (distância em metros do mundo, dano em pontos). A conversão para ticks acontece **uma única vez**, no build (ADR-0002) e fora da simulação: durações viram ticks por arredondamento ao inteiro mais próximo, e o conjunto é **recusado** se o resultado for menor que 1 (fórmula `duracao_ticks`; recusa, nunca ajuste para 1; vale só para durações, ver instantes abaixo), e taxas por segundo viram taxas por tick (fórmula `taxa_por_tick`). **Instantes não são durações** *(emenda do #7, 2026-11-06)*: um campo `_s` que marca um ponto do relógio de combate (como o `inicio_s` das entradas do cronograma do #7) usa a mesma conta e o mesmo arredondamento, mas a regra é outra: **0 é válido** (vence no primeiro tick ativo) e o campo é recusado se for negativo ou maior que o máximo declarado pelo GDD dono (`instante_max_s`, #7); a recusa de menos de 1 tick vale só para durações. O resultado da conversão precisa ser **idêntico bit a bit** em todas as plataformas (editor, Windows, Android IL2CPP ARM64). **Decidido no ADR-0002 (`Proposed`, provisório):** converter no passo de build e gravar os bits do `float` no snapshot, dividindo em `decimal` e convertendo uma só vez por uma rotina própria só com inteiros; o ADR-0001 foi emendado para esse caminho único (antes mandava multiplicar por `SimClock.TickSeconds`, e os dois caminhos davam bits diferentes: 100 por segundo, 3,3333335f contra 3,33333325f). A regra de `delta time` de `.claude/rules/gameplay-code.md` vale só para a apresentação; a simulação trabalha em ticks.
5. **Validação.** Ela roda antes de qualquer uso, sempre pela **mesma função** (`DataValidator`) no editor, no teste EditMode e na validação de pacote remoto; no carregamento do embarcado, o `SnapshotVerifier` confere a estrutura e o hash do snapshot, que o pré-build provou ser o validado (ADR-0002, provisório); e o resultado é **tudo ou nada**: um único valor inválido invalida o conjunto inteiro. Valor fora da faixa é **recusado, nunca ajustado** (sem clamp). São seis checagens gerais, mais as de setup que cada GDD dono declara (hoje as do #7, na última linha da lista):
   - **tipo e unidade** de cada campo;
   - **faixa segura** de cada knob, e o pior valor aceitável dos knobs de aceite (os colchetes do conceito, como as mortes do Tank ≤ [2]);
   - **referências cruzadas**: toda referência vinda de uma definição ativa aponta para uma definição existente e não `deprecated` (a skill para uma função, a fase para inimigos e chefe), e valem as checagens de setup do conceito, como `5 ≤ C ≤ |pool da função| − 4` e `K_min` alcançável;
   - **regra do tick**: nenhuma **duração** pode resultar em menos de 1 tick (ADR-0001); um **instante** pode valer 0 (Regra 4);
   - **capacidades**: toda capacidade da fase (entidades, eventos, pools) tem um campo e um teto, e cobre a **demanda declarada** pelo GDD dono: o pico simultâneo (vivos, eventos por tick, pools) e, para a **tabela de ids** do `SimWorld`, o **total de spawns da fase**, porque ids nunca se reutilizam (ADR-0001; #2, Regra 8 e FS9). O #7 declara o pico de vivos e os spawns das waves, e o #8 as invocações. O total de spawns tem três termos (ver a F3): os dois termos de dado o #1 valida no build, e o termo de código (`ids_de_preparacao`, declarado pelo #3) o compositor confere antes do `Create` (ADR-0001, item 6; provisório, a reavaliar);
   - **IDs**: unicidade e estabilidade em relação à versão anterior (nenhum ID sumiu nem mudou de tipo).
   - **checagens de setup do #7** *(emenda do #7, 2026-11-06; o #7 é dono das fórmulas e o #1 as roda, por fase)*: `arena_ok`, `chefe_na_tela_ok` e `spawn_fora_ok` (F5 do #7: arena, raio de nascimento, direções e área visível); `cronograma_ok` (F10 do #7: estrutura, `w` único e explícito, o chefe como última entrada e exatamente um `Essencial`, respiro e duelo dos elites, escolta que cabe, `alcance_inicio_aviso_m` dentro da área visível); e o **recálculo** do pico de vivos (F8), do total de spawns (F7) e do XP (`xp_min` e `xp_max`, F9) a partir das contagens, que alimentam a F3 daqui e a F5 do #3. Nenhum desses números é digitado.
   - **relatório de autoria por fase** *(emenda do #7, 2026-11-06; saída de ferramenta, em texto ou CSV, gerada na validação do editor e no build; não é dado do jogo e não entra no hash)*: para cada fase, a linha do tempo em `CombatTick` (pulsos de horda; respiros com início, fim e duração; elites; silêncio antes do chefe; chefe; pulsos da escolta), o pico agendado como porcentagem do teto de vivos, o XP (`xp_min` e `xp_max`), cada erro da F10 do #7 com o `w` da entrada, os sinais da F10 e da F11 (`RespiroLongo`, `CargaTankAlta`, `RespiroCurto`, `RugidoMuitosNiveis`), o id de classe de vetor de cada direção (índice, espelho em x, espelho em y; Regra 7.4 do #7) e, por entrada `Elite`, o `duelo_min_ticks` e a janela. Sem ele a validação só diz "recusado"; com ele o autor vê onde a curva da fase quebra.
   Números são lidos em cultura invariante. Uma definição marcada `placeholder` (como um stub do MVP) pode existir sem ser referenciada, mas a validação sempre informa quantas existem.
6. **Versão.** Todo conjunto validado tem um **hash de conteúdo** e um **rótulo legível**. Cada skill tem uma **revisão** própria, que muda quando muda **qualquer coisa que altere o comportamento da skill**: a sua definição e tudo que ela referencia (evoluções, passivas, modificadores, funções), as fórmulas compartilhadas e os knobs globais que ela usa (conceito L191: nerfs em evoluções e passivas cobrem as skills seladas que dependem delas). Um knob sem skill dona declara as skills que afeta, ou "todas"; sem essa declaração, a validação o recusa. A classificação é dada **por par (mudança, skill afetada)**: a mesma mudança pode ser `buff` para uma skill e `nerf` para outra, e cada skill afetada recebe a sua. Numa mudança que melhora e piora a mesma skill, vale `nerf` para ela. Cada **transição da versão efetiva** de uma skill é um passo do histórico, classificado contra a **revisão efetiva anterior da skill** e nunca contra o embarcado puro: dados embarcados novos (update do app), pacote aplicado, troca de um pacote por outro, remoção, expiração e descarte de pacote por base nova. Sem isso, trocar um pacote de nerf de 20% por um de nerf de 10% ficaria registrado como `nerf`, e um pacote de +50% trocado por +10% passaria por `buff`. *Como a revisão é calculada e identificada (por exemplo, hash do fecho de dependências mais um contador sequencial por skill) é decisão do ADR-0002 (hash do fecho sobre IDs em texto e bits, mais um contador sequencial por skill), provisória e a reavaliar.* **Toda mudança na revisão de uma skill exige uma classificação autoral: `nerf`, `buff`, `correcao` (conserto de bug) ou `neutra`**, e a validação recusa a mudança que vier sem ela. `neutra` só é aceita quando nenhum valor de gameplay da skill mudou. O #1 guarda o **histórico de revisões** de cada skill; cada passo registra a classificação e a **data de publicação** (para pacote remoto, a data emitida pelo #29). **O #1 só expõe fatos** sobre esse histórico (a revisão mudou desde o selo? há `nerf` no caminho? em que datas?). **Quem decide se há reforja grátis é a Reforja (#18)**, seguindo o conceito (L191: só nerf líquido acima de um limiar; buffs, correções de bug, mudanças de texto e ajustes abaixo do limiar não contam; vale para quem selou antes do anúncio do patch, numa janela e com teto).
7. **Entrega.** Um catálogo global pequeno (raridades, tetos, pesos) é carregado no boot. Os dados de cada fase ficam **completos, validados e convertidos** antes do primeiro tick, e são **imutáveis** até o fim da partida. Nenhuma leitura de arquivo, conversão ou sobrescrita acontece durante a fase. O jogo e a simulação headless leem exatamente o mesmo conjunto. Uma falha de carga ou de validação **bloqueia a entrada na fase** e nunca cai em valor padrão.
8. **Congelamento para o aceite.** Os knobs de aceite e seus piores valores entram no commit anterior a D0, e o build de aceite é congelado por tag git (conceito L402). Knobs de aceite (`aceite: sim`) nunca são marcados `remoto`, e a sobrescrita remota fica desligada durante as medições de aceite. **Exceção declarada:** `phase_load_budget_cold_ms`, `phase_load_budget_warm_ms`, `phase_snapshot_memory_kb` e os tetos de capacidade **não** são knobs de aceite: nascem das medições do spike de performance e são fixados (commit) no fim do spike, antes do build de aceite (AC-P1). Os tetos absolutos de carga da fase (`phase_load_ceiling_*`) são decididos pelo usuário antes do spike.
9. **Sobrescrita remota (pós-lançamento).** Ela chega como um **pacote** de pares knob → valor, com a versão-base a que se destina, um número de sequência de publicação e a classificação de cada skill afetada, entregue pelo provedor que o #29 injeta. O pacote:
   - só pode tocar knobs da **lista branca** (`remoto: sim`), com valores dentro da faixa segura;
   - passa pela **mesma validação** do conjunto embarcado, aplicada ao conjunto resultante;
   - é **atômico**: vale inteiro ou é rejeitado inteiro;
   - **não carrega campo de segmentação** (público, segmento, status de pagante ou equivalente): se carregar, é rejeitado inteiro (Regra 10);
   - só passa a valer **no início da próxima partida, no hub e com nenhum ritual de selo ou de registro aberto**, nunca durante uma fase. A tela das cartas lê a mesma versão efetiva que a próxima partida vai usar, e o selo grava essa revisão: assim o número que o jogador leu antes de uma decisão irreversível é o número da partida (Player Fantasy). O #17 sinaliza ao #1 quando o ritual abre e fecha (interface provisória);
   - fica persistido como a última sobrescrita válida, para uso offline; sem ela, o jogo usa o conjunto embarcado, que é sempre válido.
   A versão efetiva de uma partida é a do conjunto embarcado mais a do pacote aplicado.
10. **Proibido:** literal de gameplay no código; qualquer sistema escrever no #1 em tempo de execução; sobrescrita no meio de uma fase; pacote remoto parcial; sobrescrita fora da lista branca ou da faixa segura; sobrescrita de tetos da economia, capacidades, constantes de tick ou da existência de definições; uma API que as fontes de recompensa chamem para saber o teto (#26); o #1 depender de rede; **um pacote remoto escolhido por compra ou por status de pagante** (Princípio de Negócio: todos os jogadores lutam com os mesmos números; se o #29 um dia segmentar pacotes, a segmentação nunca pode depender de pagamento nem alterar knob que conte para o ranking).

### States and Transitions

O ciclo de vida de um conjunto de dados e de um pacote remoto:

| Estado | Entra por | Sai para | Observação |
|---|---|---|---|
| **Autoria** | edição dos dados | Validado | pode estar inválido; nunca é carregado |
| **Validado** | a validação passou; hash, rótulo e revisões gerados | Congelado, Ativo | uma falha volta para Autoria, com a lista de erros |
| **Congelado** | tag git do build de aceite | Ativo | fixo durante as medições de aceite; sem sobrescrita |
| **Ativo** | carregamento antes de uma partida | Ativo (outra versão), na próxima partida | imutável durante a fase |
| **Sobrescrita pendente** | pacote recebido do provedor do #29 | Validada remota ou Rejeitada | nunca toca o Ativo |
| **Validada remota** | passa na lista branca, na faixa, na validação completa e na versão-base | Aplicada | espera o fim da partida em curso |
| **Aplicada** | início da próxima partida, no hub e sem ritual de selo ou de registro aberto | Ativo (versão efetiva = embarcado + pacote) | a versão efetiva entra no log (#5); cada skill afetada ganha um passo no histórico (Regra 6) |
| **Rejeitada** | pacote inválido ou versão-base incompatível | descartado; o Ativo continua | o motivo entra no log (#5) |
| **Revertida** | pacote removido ou expirado pelo #29 | conjunto embarcado, na próxima partida | o embarcado é sempre válido e offline |

### Interactions with Other Systems

Só o GDD #28 existe entre os dependentes (e já confirma a interface do save); as demais interfaces abaixo são **provisórias** e devem ser confirmadas quando o GDD dono for escrito. Entre parênteses, quem é dono da interface.

- **#2 Simulação e #3 Fluxo de fase** (o #1 define o snapshot; #2 e #3 consomem). Entram: os structs imutáveis da fase, já em ticks; as capacidades de entidades, de eventos e de pools que dimensionam o `SimWorld` e o `EventBuffer`; as curvas de XP do #3. Sai: nada; os sistemas só leem.
- **#5 Log de eventos** (o #5 define o log; o #1 fornece a identidade). O cabeçalho de cada partida e de cada execução headless leva o hash, o rótulo, a tag do build e o pacote remoto aplicado. Sobrescritas rejeitadas e falhas de validação entram no log. A simulação headless pode aplicar um pacote candidato para testá-lo antes de publicar.
- **#6 Combate e #7 Horda** (cada GDD é dono do significado). Entram dano, cooldowns, contagens e densidades. O #7 declara, por fase, o pico de entidades vivas **e os spawns das waves** (o #8 declara as invocações), e a validação cruza o pico com a capacidade da lista de vivos e a soma dos spawns de dados com a da tabela de ids; o termo de código (`ids_de_preparacao`, #3) é conferido pelo compositor (F3). As waves chegam como listas **ordenadas por (`inicio`, `w`), com `w` explícito e único**, e o sorteio de cada wave usa o `w` (ADR-0001, `RngWave(w)`), nunca a posição na lista.
- **#8 Skills** (o #8 é dono do significado). Entram as definições de skills e de modificadores, com as referências cruzadas e a contagem máxima de níveis.
- **#10 Funções** (o #10 é dono). Define os pools por função; a checagem de setup do pool usa esses pools.
- **#16 Grimório e #17 Selamento** (o #17 especifica o predicado de selabilidade e o `K_min`; o #16 os implementa). O #1 guarda só os valores (`C`, `K_min`, pesos de oferta) e a validação cruzada; "selável" é uma regra do #17, não um dado. O #17 também sinaliza ao #1 quando um ritual de selo ou de registro abre e fecha, e o #1 não aplica pacote remoto enquanto algum estiver aberto (Regra 9); a interface é provisória.
- **#18 Reforja** (o #1 expõe o histórico de revisões por skill, com classificação e data de cada passo; o #18 é dono da regra de elegibilidade). O registro do selo guarda a revisão de cada skill selada e a data do selo; o #18 compara com o histórico e aplica a regra do conceito (L191). A reforja por nerf é do Alpha, mas a revisão, a classificação e a data existem desde o MVP.
- **#26 Economia e tetos** (leitura somente). Os tetos são valores do #1; o #26 os aplica e audita. Nenhuma fonte de recompensa chama uma API do #1.
- **#28 Save local** (o #28 define o formato). O save grava só o carimbo da versão, para diagnóstico, e a revisão de cada skill selada. Ele não grava valores nem migra: um save antigo é lido contra os dados vigentes pelos IDs estáveis.
- **#29 Serviços online** (o #1 define o contrato do pacote; o #29 implementa transporte, cache, assinatura e expiração). O #1 valida e decide; ele nunca espera pela rede.

**Vira ADR (implementação, fora deste GDD; decidido no ADR-0002, `Proposed`, exceto a persistência, a escrita atômica, a assinatura e a expiração do pacote remoto, que ficam para o ADR do #29, que pode reaproveitar o mecanismo de escrita atômica do ADR-0003):** formato de autoria (ScriptableObject, JSON ou híbrido) e o passo de build que gera o snapshot; hash canônico e ordem de serialização; onde e como o hook de validação roda no editor; layout dos structs de fase; cálculo da revisão por skill; persistência, escrita atômica, assinatura e expiração do pacote remoto, e se ele passa por Addressables. Riscos de engine levantados pelos especialistas para esse ADR: o Addressables lança exceção na falha de carga a partir do 6.2 (`breaking-changes.md`, risco MEDIUM, a confirmar no 6000.3.27f1); o comportamento com domain reload desligado, o stripping do IL2CPP para tipos de dados, a recarga a quente no editor e o parse de float entre Mono e IL2CPP são `NOT SOURCEABLE` em `docs/engine-reference/unity/`.

*Consultados:* `systems-designer` (regras, estados, interações, decisões D1 a D3), `gameplay-programmer` (viabilidade, unidades, IDs) e `engine-programmer` (carregamento, riscos de engine, sobrescrita). Decisões do usuário: partida = run de fase; sobrescrita por lista branca; aplicada só entre partidas; nerf por marcação autoral obrigatória.

## Formulas

O #1 não define balanceamento de combate: as fórmulas abaixo são as regras numéricas que ele mesmo aplica na validação e na conversão. O significado de cada knob (dano, cooldown, pesos) é da fórmula do GDD dono.

**Regra transversal (vale para todas):** os números são lidos do dado como `decimal`, em cultura invariante, a partir de **texto** (o valor autoral nunca é gravado antes como `float`, senão `0,15` já chega como 0,15000000596; o formato de autoria (JSON, com os números escritos como texto) foi decidido no ADR-0002, ainda `Proposed`). Faixa, conversão e arredondamento são calculados em `decimal`, e o resultado vira `float` ou `int` uma única vez, no fim. A faixa é comparada com o **valor autoral**, nunca com o `float` convertido: `0,1` em float vale `0,100000001` e sairia de uma faixa com máximo `0,1`.

### F1. Duração em ticks

The duracao_ticks formula is defined as:

`duracao_ticks = floor(s × TICKS_PER_S + 0,5)`; recusar o conjunto se `duracao_ticks < 1`

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| s | decimal | faixa segura do knob, > 0 | data file (campo `_s`) | duração autoral em segundos |
| instante | decimal | 0 a `instante_max_s` do GDD dono | data file (campo `_s` que marca um ponto do relógio de combate) | instante autoral em segundos de combate; não passa pela recusa de menos de 1 tick (emenda do #7) |
| TICKS_PER_S | int | 30 | constant (`SimClock.TicksPerSecond`, ADR-0001) | ticks por segundo |
| duracao_ticks | int | 1 a `floor(s_max × 30 + 0,5)` | calculated | duração usada pela simulação |

**Output Range:** de 1 tick ao máximo da faixa do knob. Se a conta dá 0 (`s` abaixo de 1/60 s), o valor é **recusado, nunca ajustado** (Core Rule 5): o "mínimo de 1 tick" do ADR-0001 é cumprido pela recusa. A regra é a conta (`duracao_ticks < 1`), não uma constante: 1/60 não existe em `decimal`, e o menor `s` autoral que vale 1 tick depende das casas decimais (0,017 com três casas; 0,0167 com quatro; 0,0166 já dá 0). O meio tick arredonda **para cima** (`MidpointRounding.AwayFromZero`), e não para o par (o padrão do .NET leva 1,5 a 2 e 4,5 a 4, o que surpreende quem faz o tuning); um teste fixa esse comportamento. Campos `_ticks` não passam por conversão; só são checados contra o mínimo de 1. Duração zero nunca é válida: a ausência de cooldown se expressa pela ausência do campo. **Instantes** *(emenda do #7, 2026-11-06)*: `inicio_ticks = floor(s × 30 + 0,5)` com a mesma conta e o mesmo arredondamento, mas `s` ≥ 0 e ≤ o máximo do GDD dono (`instante_max_s`, #7: 60 a 900, padrão 600). **0 é válido** (a entrada vence no primeiro tick ativo, nunca no `Preparar`); negativo e acima do máximo são recusados; `duracao_ticks < 1` não se aplica a instantes.
**Example:** 0,15 s → 0,15 × 30 = 4,5 → **5 ticks** (meio tick para cima; o padrão do .NET sem `AwayFromZero` daria 4, e é isso que o teste fixa; em `double` este caso também dá 5, então o exemplo não depende do `decimal`). 2,5 s → 75 ticks. 0,0167 s → 1,001 → **1 tick**. 0,0166 s → 0,998 → 0 → **recusado**. 0,01 s → 0,3 → 0 → **recusado**. **Instante:** 0 s → 0 tick (válido); 0,05 s → 1,5 → **2 ticks**; −0,1 s → **recusado**; 601 s com `instante_max_s` = 600 → **recusado**.

### F2. Taxa por tick

The taxa_por_tick formula is defined as:

`taxa_por_tick = (float)(r ÷ TICKS_PER_S)`

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| r | decimal | faixa segura do knob (pode ser 0 ou negativa) | data file (campo `_per_s`) | taxa autoral por segundo |
| TICKS_PER_S | int | 30 | constant (ADR-0001) | ticks por segundo |
| taxa_por_tick | float | `r_min / 30` a `r_max / 30` | calculated | taxa aplicada a cada tick |

**Output Range:** limitada pela faixa do knob. A regra do mínimo de 1 tick não vale aqui, porque taxa não é tempo. A divisão feita em `decimal` e a multiplicação por `SimClock.TickSeconds` (ADR-0001) podem dar bits diferentes; qual das duas vale foi decidido no ADR-0002 (provisório): dividir em `decimal` no build, converter uma só vez por uma rotina própria só com inteiros e gravar os bits do `float`. O que se exige aqui é um único caminho, com o mesmo resultado em todas as plataformas. Dividir em `decimal` tem **dois** arredondamentos (a divisão e a conversão para `float`), e o algoritmo da conversão `decimal` para `float` entre Mono, IL2CPP Windows e IL2CPP ARM64 é `NOT SOURCEABLE` em `docs/engine-reference/unity/`; por isso o ADR-0002 grava os bits no build e usa uma conversão própria, e o AC-I3 [PM] fecha o risco.
**Example:** 4,5 m/s → **0,15f m/tick** (igual nos dois caminhos). 100 de dano/s: **3,33333325f** por tick se dividir em `decimal` (soma de 30 ticks ≈ 99,9999976) ou **3,3333335f** se multiplicar por `1f/30f` (soma ≈ 100,000005). Em nenhum dos dois a soma é exatamente 100, então o GDD #6 **não pode** afirmar que a soma em 1 s é exatamente 100.

### F3. Capacidade da fase contra a demanda declarada

The capacidade_ok formula is defined as:

`capacidade_ok = (pico × (100 + margem_pct) ≤ cap × 100) ∧ (cap ≤ teto)`

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| pico | int | ≥ 1 | data file (declarado pelo GDD dono; o #7 para entidades) | demanda declarada: o pico simultâneo estimado e, para a tabela de ids do `SimWorld`, os **spawns de dados da fase** (`spawns_de_dados` = spawns das waves + `máx_invocações`; o termo de código `ids_de_preparacao` é somado pelo compositor, ver "Tabela de ids") |
| margem_pct | int | segura 10 a 50, padrão 25 | data file (`capacity_margin_pct`, global, não remoto; override por capacidade quando preciso) | folga sobre a estimativa |
| cap | int | ≥ 1 | data file (por fase e por tipo de capacidade) | entidades, eventos ou pools pré-alocados |
| teto | int | definido pelo spike de performance | data file (por tipo de capacidade, não remoto) | limite de performance do aparelho de referência |

**Output Range:** booleano. A conta é toda inteira, sem float. A margem existe porque o pico é uma estimativa e o transbordo de buffers custa caro (`DroppedEvents` do ADR-0001 nunca pode ser diferente de zero em desenvolvimento).
**Example:** pico 300, margem 25: 300 × 125 = 37.500 ≤ 400 × 100 = 40.000 e 400 ≤ 512 → **OK**. Com `cap` = 360: 37.500 > 36.000 → **recusado**.
**Tabela de ids.** Como os ids nunca se reutilizam (ADR-0001; #2, Regra 8), a tabela de ids do `SimWorld` é uma capacidade própria que usa esta mesma fórmula, e o total de spawns da fase tem três termos: `total_spawns = ids_de_preparacao + spawns_de_dados` (FS9 do #2, registro `capacidade_ids_ok`), com `spawns_de_dados` = soma dos spawns das waves (#7) + `máx_invocações` (#8). A conferência se divide em duas (decisão provisória, a reavaliar): **no build**, o #1 valida com `pico` = `spawns_de_dados` (condição necessária; o snapshot leva esse número); **no jogo, antes do `Create`**, o compositor soma `ids_de_preparacao` (código; o #3 declara 1, o herói) e refaz a conta completa em inteiro de 64 bits, com a mesma margem; se não couber, a fase não começa (`FalhaInterna(DadosInvalidos)`, montada pelo #3; ADR-0001, item 6). **Example (números ilustrativos):** `spawns_de_dados` 899 e `ids_de_preparacao` 1, margem 25: `cap` = 1124 passa no build (899 × 125 = 112.375 ≤ 112.400) e é **recusado pelo compositor** (900 × 125 = 112.500 > 112.400); `cap` = 1125 passa nas duas. A lista de vivos continua validada pelo pico simultâneo, e cada uma das duas capacidades tem a sua própria chave de `capacity_ceiling`: o teto da lista de vivos mede frame time e o da tabela de ids mede memória alocada (OQ-4).

### F4. Setup do Grimório

The grimorio_setup_ok formula is defined as:

`grimorio_setup_ok = (S + 1 ≤ C ≤ P − S) ∧ (P_f ≥ S_f)`, com `P = P_f + P_c`, avaliada para cada função

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| C | int | padrão 5 (conceito L397) | data file (não remoto) | capacidade do Grimório |
| S | int | 4 | constant (2 de função + 2 livres, conceito L397) | tamanho do selo |
| S_f | int | 2 | constant (conceito L397) | slots de função no selo |
| P_f | int | ≥ 0 | calculated (contado das definições) | skills **ativas** de função, sem `deprecated` nem `placeholder` |
| P_c | int | ≥ 0 | calculated (contado das definições) | skills **ativas** compartilhadas, sem `deprecated` nem `placeholder` |

**Output Range:** booleano. Lê o `5` da checagem do conceito (L407, `5 ≤ C ≤ |pool| − 4`) como `S + 1` (sempre há escolha no selo) e o `4` como `S` (o pool excede o Grimório, ou seja, há escassez). **Essa leitura é uma interpretação; o GDD #17 precisa confirmá-la** (ver Open Questions). O termo `P_f ≥ S_f` é novo: é o que torna alcançável o `2 − f` do invariante da L407. Um `placeholder` não conta no pool, para que um stub não feche a checagem de escassez de mentira.
**Example:** MVP, P = 5 + 5 = 10, C = 5: 5 ≤ 5 ≤ 6 e 5 ≥ 2 → **OK**. Com C = 7: 7 > 6 → **recusado**.

### F5. K_min alcançável (parte estática)

The k_min_ok formula is defined as:

`k_min_ok = S ≤ K_min ≤ N_fases + R_max`

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| K_min | int | padrão 7 (conceito L397) | data file (não remoto) | vitórias de chefe de fase que abrem o selo |
| S | int | 4 | constant | tamanho do selo |
| N_fases | int | 5 no MVP | calculated (contado das fases do capítulo) | fases com chefe de fase |
| R_max | int ou ∞ | ≥ 0 | data file (∞ quando os replays não têm limite) | replays de fase que contam vitória |

**Output Range:** booleano. O limite de baixo vem de 1 registro por vitória: sem S vitórias não há S skills para selar. Com replays ilimitados, o limite de cima não restringe nada.
**Example:** 4 ≤ 7 ≤ 5 + ∞ → **OK**. Com K_min = 3: 3 < 4 → **recusado**.
**Fora do #1:** o invariante dinâmico `≤ max(0, 4 − g, 2 − f)` (L407) depende dos estados alcançados; é teste da simulação headless do #16 e do #17, não validação de dados.

### F6. Coerência da declaração de um knob

The knob_ok formula is defined as:

`knob_ok = (min ≤ padrao ≤ max) ∧ (aceite = sim → pior em [min, max] ∧ padrao do lado bom de pior) ∧ (aceite = não → sem pior e sem sentido)`

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| min, max, padrao | decimal | — | data file (declaração do knob, Core Rule 2) | faixa segura e valor padrão |
| aceite | enum {`sim`, `não`} | — | data file (campo explícito de todo knob, Core Rule 2) | marca o knob de aceite; nunca é deduzido da presença de `pior` |
| pior | decimal | dentro de `[min, max]` | data file (só quando `aceite: sim`) | pior valor aceitável |
| sentido | enum {`menor_melhor`, `maior_melhor`} | — | data file (só quando `aceite: sim`) | define o "lado bom" de `pior` |

**Output Range:** booleano. Sem `sentido`, um knob de aceite não pode ser comparado com o seu pior valor e é recusado. Um knob com `pior` ou `sentido` mas sem `aceite: sim` também é recusado (sem o campo explícito, um knob de aceite sem `pior` passaria despercebido e poderia ser `remoto: sim`).
**Example:** mortes do Tank até abrir o selo: padrão 2, pior 2, `menor_melhor` → 2 ≤ 2 → **OK**. Com padrão 3 → **recusado**.

**Cortada:** uma "faixa remota" mais estreita que a faixa segura. A Core Rule 9 já valida o pacote contra a faixa segura, e um campo a mais para um recurso `NOT SOURCEABLE` não se paga agora; entra quando o Live Ops pedir um limite mais apertado.

*Consultado:* `systems-designer` (F1 a F6; decisões menores adotadas no modo guided: meio tick para cima, margem global de 25%, duração zero recusada, `placeholder` fora do pool).

## Edge Cases

### Zero, máximo e fora da faixa
- **If o valor autoral é exatamente `min` ou `max`**: é aceito. A faixa é fechada e a comparação é feita em `decimal` (regra transversal das Formulas).
- **If `min > max`, `pior` fica fora de `[min, max]`, um knob com `aceite: sim` não tem `pior` ou `sentido`, ou um knob sem `aceite: sim` traz `pior` ou `sentido`**: a declaração é recusada e, com ela, o conjunto inteiro (F6).
- **If um campo `_s` declara `min` cuja conversão dá menos de 1 tick (F1; por exemplo 0,0166)**: a declaração é recusada. Sem isso, a faixa "segura" conteria valores que a F1 recusa, e um pacote dentro da faixa cairia na regra do tick.
- **If um `int` vem com parte fracionária, ou um número vem com vírgula decimal, `NaN`, infinito ou acima de `float.MaxValue`**: é recusado na checagem de tipo.
- **If o produto da F3 passa de 32 bits**: a conta é feita em inteiro de 64 bits e nunca estoura.

### Pacotes remotos (pós-lançamento)
- **If um pacote chega durante a fase**: o provedor do #29 só o persiste bruto. O #1 o valida e converte no próximo intervalo entre partidas, porque a Core Rule 7 proíbe conversão durante a fase.
- **If o jogador abandona a fase com um pacote pendente**: o abandono encerra a partida, que fica registrada com a versão com que começou. Se o pacote passar na validação, ele vale na partida seguinte.
- **If o app morre durante a fase ou durante a escrita do pacote**: no boot vale a última sobrescrita válida persistida (a escrita é atômica; o mecanismo é do ADR do #29, que pode reaproveitar o do ADR-0003, não do ADR-0002), e o pacote bruto é revalidado.
- **If há dois pacotes pendentes**: vale o de **maior número de sequência de publicação**, um campo que o #29 emite ao publicar; o outro é descartado e registrado no log (#5). Pacotes não se mesclam nem se empilham: todo pacote se aplica sobre o embarcado. A ordem de chegada no aparelho (cache, offline) nunca decide.
- **If a versão-base do pacote difere do hash do embarcado vigente**: o pacote é Rejeitado, o motivo vai para o log (#5) e o Ativo continua.
- **If um update do app troca o embarcado**: no boot o pacote persistido é revalidado (isso acontece em todo boot), falha na versão-base e é descartado. O jogo usa o embarcado puro até o #29 entregar um pacote para a nova base. **O descarte é uma transição da versão efetiva (Regra 6):** se o pacote alterava alguma skill, cada skill afetada ganha um passo no histórico com a classificação inversa do que o pacote fazia, contra a revisão efetiva anterior; sem o passo, o buff ou o nerf que o jogador perdeu ficaria invisível. O mesmo vale para a troca de um pacote por outro.
- **If o pacote está vazio, repete um knob ou cita um ID inexistente, `deprecated` ou fora da lista branca**: é rejeitado inteiro. Reverter é sempre remover o pacote (estado Revertida), nunca enviar um pacote vazio.
- **If o pacote altera um knob que afeta alguma skill (direto, por uma definição que ela referencia ou por um knob global)**: a revisão de cada skill afetada muda, e o pacote precisa trazer a classificação (`nerf`, `buff`, `correcao` ou `neutra`) de cada skill afetada; sem ela, é rejeitado (a Core Rule 6 vale para o conjunto resultante).
- **If um pacote que alterou uma skill é removido**: a remoção conta como a mudança inversa, com a classificação inversa (`nerf` vira `buff`, `buff` vira `nerf`, `neutra` continua `neutra`; a remoção de uma `correcao` exige classificação autoral, porque desfazer um conserto não tem inverso automático), e entra no histórico de revisões da skill. **Consequência para o Live Ops e o #18:** um buff temporário de skill selável por pacote (evento) gera, ao expirar, um passo `nerf` para quem selou durante o evento; o #18 precisa decidir se isso conta.
- **If um pacote tenta alterar contagens de horda (para mais ou para menos)**: é rejeitado, porque **contagens de horda, o pico declarado e o total de spawns não são remotos**. O #7 já deriva o pico e o total das contagens (F7 e F8 do #7, 2026-11-05), mas um pacote remoto teria de recalcular os dois e revalidar a capacidade; abrir essa porta exige emendar o ADR-0002 (OQ-5). Sem isso, a F3 compararia a demanda antiga e um transbordo passaria pela validação.

### Selo, revisão e save
- **If uma skill selada muda e há ao menos um `nerf` entre a revisão do selo e a vigente**: o #1 responde "há nerf no caminho" = verdadeiro, com as classificações e datas de cada passo, mesmo que um `buff` posterior tenha compensado. Se isso dá reforja grátis (nerf líquido, limiar, anúncio, janela) é decisão do #18. *(A decisão do usuário "qualquer nerf no caminho libera" fica como insumo para o GDD #18, que a confronta com o conceito L191.)*
- **If a revisão vigente tem o mesmo hash da revisão do selo**: o #1 responde "sem mudança desde o selo", mesmo que exista um `nerf` no caminho (por exemplo, um pacote de nerf aplicado e depois removido).
- **If a mudança é um conserto de bug que baixou um valor**: é classificada `correcao`, nunca `nerf`; o conceito (L191) diz que correção de bug não conta para a reforja.
- **If uma mudança é classificada `neutra` mas algum valor de gameplay da skill mudou**: a validação recusa. `neutra` só vale quando nenhum número mudou (texto, referência de arte); uma mudança mista exige `nerf` ou `buff`. Isso fecha a fuga por `neutra`. A classificação `nerf`, `buff` ou `correcao` continua sendo palavra autoral do estúdio, que também é quem decide a reforja grátis; conferir essa marcação (por exemplo, nerf rotulado como `correcao`) fica para o #18 e o Live Ops (OQ-11).
- **If a revisão de uma skill selada muda com `neutra` legítima**: o #1 não registra nerf; o selo continua, e o save mantém a revisão do momento do selo.
- **If um save antigo tem uma skill selada `deprecated`**: ela resolve pelo ID e funciona com os seus últimos valores, que continuam sendo validados. Ela só sai dos pools (a F4 não a conta). Se a aposentadoria dá direito a reforja é decisão do GDD #18.
- **If uma definição `deprecated` referencia outra `deprecated`**: é válida. A exigência de "não `deprecated`" vale só para referências vindas de definições ativas; sem essa exceção, aposentar uma função quebraria as skills já aposentadas dela.
- **If o save cita um ID ausente dos dados**: o #1 responde "ID desconhecido" e não cria nada. O tratamento é do #28.

### Builds e ferramentas
- **If o conjunto embarcado é inválido**: o passo de build falha e nenhum build é gerado.
- **If o embarcado chega inválido ao aparelho mesmo assim (por exemplo, instalação corrompida)**: falha no catálogo global bloqueia todas as fases; falha nos dados de uma fase bloqueia só essa fase. Nunca há valor padrão, e o pacote persistido não é aplicado, porque a sua base é o embarcado.
- **If a simulação headless roda com um pacote candidato**: o candidato passa pela mesma validação; um candidato inválido aborta antes do tick 0 com a lista de erros. O cabeçalho do log (#5) registra o candidato, que nunca é persistido como última sobrescrita válida. Uma mudança fora da lista branca se testa editando o embarcado.
- **If um knob com `aceite: sim` está marcado `remoto: sim`**: a declaração é recusada e o build falha.
- **If o build de aceite encontra um pacote persistido no aparelho**: o pacote é ignorado, mas não apagado, porque o provedor do #29 não é injetado no build Congelado.

*Consultado:* `systems-designer`. Decisões do usuário: qualquer `nerf` no caminho é registrado como fato (a elegibilidade da reforja foi movida para o #18 na revisão CD-GDD-ALIGN); `neutra` só sem mudança de valor; entre dois pacotes vale o de maior sequência de publicação; remover um pacote herda a classificação inversa. Padrão adotado no modo guided: contagens de horda e pico não remotos; o #7 já deriva o pico (2026-11-05), e abrir a porta é a OQ-5.

## Dependencies

### Upstream (o #1 depende de)
**Nenhum sistema.** O #1 não depende de rede nem de outro GDD. Ele respeita duas decisões externas: o **ADR-0001** (unidade de tempo, conversão para ticks, dados imutáveis durante a fase, conversão de `ScriptableObject` fora da simulação) e o **conceito** (`game-concept.md` L327-328, L397, L402, L407: progressão e economia como transações sobre dados, remote config desde o início, valores de C e K_min, knobs de aceite congelados antes de D0).

### Downstream (dependem do #1)
Só o #28 existe e já confirma o seu contrato (IDs estáveis, carimbo da versão, revisão e data do selo, resposta "ID desconhecido"); os demais contratos são provisórios.

| Sistema | Natureza | O que lê do #1 | Dependência |
|---|---|---|---|
| #2 Simulação | dados da fase em ticks, capacidades | snapshot imutável por fase | **Hard**: sem dados válidos a fase não começa |
| #3 Fluxo de fase | curvas de XP, regras da fase | snapshot da fase | **Hard** |
| #5 Log de eventos | identidade da versão | hash, rótulo, tag, pacote aplicado, rejeições | **Hard** para o aceite: sem versão o log não é comparável |
| #6 Combate e dano | dano, cooldowns, telegraphs | knobs do #6 | **Hard** |
| #7 Horda, waves e inimigos | contagens, densidades, waves ordenadas por (`inicio`, `w`), pico, spawns das waves, XP | knobs e definições do #7 | **Hard** |
| #8 Skills e evoluções | definições de skills e modificadores | definições, referências, revisões | **Hard** |
| #10 Funções | pools por função | definições de função | **Hard** |
| #16 Grimório e #17 Selamento | C, K_min, pesos de oferta | knobs não remotos | **Hard** |
| #18 Reforja (Alpha) | histórico de revisões e classificações | revisão por skill | **Soft** no MVP (a reforja por nerf é Alpha), **Hard** depois |
| #26 Economia e tetos (Vertical Slice) | tetos | valores, leitura somente | **Hard** |
| #28 Save local | IDs estáveis, carimbo de versão, revisão das skills seladas | identidade, não valores | **Hard** |
| #29 Serviços online (Alpha) | contrato do pacote remoto | o #29 implementa o provedor que o #1 consome | **Soft** para o #1 (ele funciona sem o #29); **Hard** para o #29 |

**Bidirecionalidade:** o índice (`systems-index.md`) já lista o #1 como dependência de todos os 13 dependentes acima (#2, #3, #5, #6, #7, #8, #10, #16, #17, #18, #26, #28 e #29). Falta cada GDD ainda por escrever citar o #1 nas suas Dependencies (o #28 já cita).

## Tuning Knobs

Só os knobs que o próprio #1 define. Os knobs dos outros sistemas **moram** no #1 mas pertencem ao GDD dono, que declara a faixa e o significado; aqui eles não são duplicados.

| Knob | Padrão | Faixa segura | Remoto | Afeta | Baixo demais | Alto demais |
|---|---|---|---|---|---|---|
| `capacity_margin_pct` (F3) | 25 | 10 a 50 | não | folga das capacidades sobre a demanda declarada (o pico, ou o total de spawns na tabela de ids) | transbordo de `SimWorld` e `EventBuffer` quando o pico real passa da estimativa (`DroppedEvents` > 0) | memória pré-alocada desperdiçada; mais fases recusadas por passar do teto |
| `capacity_ceiling` por tipo de capacidade (F3) | a medir no spike de performance | ≥ 1; fixado pelo spike no aparelho de referência | não | teto por tipo de capacidade, cada um com a sua chave: lista de vivos (entidades ativas, frame time), tabela de ids (memória alocada), eventos e pools por fase (ver OQ-4) | fases legítimas recusadas | aceita fases que o aparelho não sustenta (frame time, térmico) |
| `phase_load_ceiling_cold_ms` e `phase_load_ceiling_warm_ms` | 3000 e 1500 (decididos pelo usuário em 2026-11-03; provisórios, a reavaliar com o aparelho de referência verificado e o jogo rodando) | ≥ 1; fixados antes do spike | não | teto absoluto do tempo de "entrar na fase" até o tick 0, em carga fria (app recém-aberto) e quente (segunda carga na sessão); sem ele o AC-P1 só pegaria regressão | recusa cargas aceitáveis | aceita cargas que o jogador percebe como travadas |
| `phase_load_budget_cold_ms` e `phase_load_budget_warm_ms` | o **menor** entre (máximo de 20 cargas da fase mais pesada no spike × 1,2; fator provisório) e o teto absoluto correspondente | definida pela medição, nunca acima do teto | não | orçamento do AC-P1, um para a carga fria e outro para a quente; a mediana tem limite próprio de 70% do orçamento (fator provisório) | recusa fases legítimas na medição | aceita cargas que o jogador percebe como travadas |
| `phase_snapshot_memory_kb` | a medir no spike (mesmo protocolo) | definida pela medição | não | memória do snapshot da fase mais as capacidades pré-alocadas (AC-P1) | recusa fases legítimas | aceita fases que pressionam a memória do aparelho de referência |
| `replay_limit` (`R_max`, F5) | ilimitado | ≥ 0 ou ilimitado | não | quantos replays de fase contam vitória para o K_min | o selo pode ficar inalcançável (F5 recusa) | nenhum efeito de validação; grind pela fase mais fácil (decisão do #17) |

**Constantes deliberadas (não são knobs):** `TICKS_PER_S` = 30 (ADR-0001; mudar é um novo ADR); `S` = 4 e `S_f` = 2 (tamanho e slots de função do selo, conceito L397; mudar é decisão do #17). **Valores registrados aqui mas de outro dono:** `C` = 5 e `K_min` = 7 pertencem ao #16 e ao #17, que definem faixa e significado; o #1 só os valida (F4, F5). O limite de acúmulo offline (`K` períodos) é declarado pelo #28 como knob do #1: o significado e a faixa são da Economia (#26), que o declara ao ser escrita; ainda não tem valor.

**Interações entre knobs:** `capacity_margin_pct` e `capacity_ceiling` agem juntos: com margem alta e teto baixo, um pico perto do teto torna a fase inválida, e o ajuste certo é baixar o pico no #7, não subir o teto. `replay_limit` torna a F5 restritiva só quando é finito.

## Visual/Audio Requirements

Nenhum. O #1 é um sistema Core sem superfície visual nem sonora para o jogador. Os valores que definem feedback de combate (duração de hit-stop, de telegraph, densidade de efeitos) moram aqui como knobs, mas os requisitos visuais e sonoros pertencem aos GDDs donos (#6, #7, #12).

## Game Feel

Não se aplica diretamente. O #1 só garante que os tempos de feel definidos pelos GDDs donos cheguem à simulação sem distorção: a conversão F1 (meio tick para cima, mínimo de 1 tick) é a granularidade que todo tempo de feel herda, 33 ms a 30 Hz (ADR-0001).

## UI Requirements

Nenhuma UI de jogador. A única superfície é de desenvolvimento: o relatório de validação (lista de erros com o ID, o campo e a regra violada, e a contagem de `placeholder`) exibido no editor e no CI, e as rejeições de pacote no log (#5). Essa superfície é ferramenta interna, não tela do jogo, e não exige spec de UX.

## Cross-References

| Documento | Trecho | O que este GDD usa ou impõe |
|---|---|---|
| `design/gdd/game-concept.md` | L292, L341 | lição do Diablo 2 e risco de nerf em build selada: origem do histórico de revisões e da classificação `nerf` |
| `design/gdd/game-concept.md` | L327-328 | progressão e economia como transações sobre dados; remote config desde o início |
| `design/gdd/game-concept.md` | L349 | remote config `NOT SOURCEABLE` |
| `design/gdd/game-concept.md` | L397, L407 | C = 5, K_min = 7, selo de 4 (2 + 2), checagem `5 ≤ C ≤ |pool| − 4` (F4, F5) |
| `design/gdd/game-concept.md` | L402 | knobs de aceite com pior valor e commit antes de D0 (Regra 8, F6) |
| `design/gdd/systems-index.md` | #1, #26, #29 | o #1 é dono dos valores e do ponto de injeção; o teto é dado aqui sem API; o remote config vem do #29 |
| `docs/architecture/adr-0001-simulacao-deterministica-float32-tick-30hz.md` | Decision → Tempo, Interface; Implementation Guidelines | 30 Hz, conversão para ticks, recusa de < 1 tick, dados imutáveis na fase, `ScriptableObject` fora da simulação, capacidades vindas dos dados |
| `.claude/rules/gameplay-code.md` | "Use delta time" | a regra vale só para a apresentação; a simulação usa ticks (Regra 4) |
| `design/gdd/save-local.md` | Interactions (#1), Dependencies | o #28 guarda IDs, carimbo da versão, revisão e data do selo; nunca valores (contrato confirmado) |
| GDDs #2, #3, #5, #6, #7, #8, #10, #16, #17, #18, #26, #29 | ainda não existem | cada um deve citar o #1 nas suas Dependencies e confirmar a interface provisória de "Interactions with Other Systems" |

## Acceptance Criteria

Evidência: **[EM]** teste EditMode automatizado em `Assets/Tests/EditMode/` (classes `DadosValidacaoTests`, `DadosConversaoTests`, `DadosVersaoTests`, `DadosSobrescritaTests`); **[PM]** teste PlayMode ou build no aparelho; **[MAN]** verificação manual ou por ferramenta de CI. **MVP** bloqueia o MVP; **PÓS** está escrito agora mas só bloqueia quando a sobrescrita remota existir. Para não haver I/O em teste unitário, a validação recebe o conjunto em memória e as fixtures são montadas em código.

**Resultado de um critério:** PASS, FAIL ou **BLOCKED**. BLOCKED significa que o critério ainda não pode ser executado (falta decisão, sistema ou medição) e **conta como não aprovado**. Ele só sai dessa condição passando, ou com uma dispensa escrita no doc de aceite do MVP (`docs/acceptance/mvp.md`: quem dispensa, data e risco; neste projeto solo, o usuário). Critérios BLOCKED hoje:

| AC | Parte bloqueada | Motivo e prazo |
|---|---|---|
| AC-05, AC-06, AC-F1 | só a leitura de texto em cultura invariante (vírgula decimal, `0,1` contra `0,100000001`). Em AC-F1, a conversão com `decimal` montado em código **já é testável** e não está bloqueada | formato de autoria decidido no ADR-0002 (JSON com números como texto; ainda `Proposed`); antes da primeira story do #1 |
| AC-F2 | todo | o caminho foi decidido no ADR-0002 (dividir em `decimal`, conversão própria só com inteiros; ainda `Proposed`); os bits esperados saem do editor real depois que o ADR for aceito |
| AC-07 | o hash (hashes iguais, só a revisão da skill afetada muda) e a regra de `neutra` | hash canônico e marcação de campos de gameplay vêm do ADR-0002 (ainda `Proposed`) |
| AC-08 | a parte de passiva, evolução, função e fórmula compartilhada referenciadas por uma skill selada | o cálculo da revisão por skill (fecho de dependências) é do ADR-0002 (hash sobre IDs em texto e bits, mais contador; ainda `Proposed`) |
| AC-09 | a inspeção dos tipos do snapshot | o contêiner do snapshot é do ADR-0002 e o layout de cada seção é do GDD dono |
| AC-13, AC-14 | a parte de persistência e de escrita atômica do pacote | o mecanismo é do ADR do #29, que pode reaproveitar o do ADR-0003 (o ADR-0002 só fixa o contrato do pacote); testes PÓS, escritos depois do ADR do #29 |
| AC-14 [PM], AC-14b [PM], AC-10 [PM], AC-11 [PM] | todo | dependem do fluxo de fase (#3) e dos Serviços online (#29), que não têm GDD |
| AC-15, AC-18 | a verificação das referências do assembly | o assembly puro (`Forja.Data`, sem engine) foi decidido no ADR-0002 (ainda `Proposed`); o analisador de símbolos banidos continua em aberto (OQ-7) |
| AC-01 | todo | ferramenta do analisador (OQ-7); antes da primeira story de gameplay |
| AC-I1 | todo | o #2 e o #7 têm GDD, mas não há implementação do `SimWorld` nem do #7 para rodar o tick 0 (a primeira porta é o ADR das colunas do `SimWorld`) |
| AC-I2 | todo | o GDD #5 não existe |
| AC-I3 [EM] | todo | o hash canônico e o formato dos bits do snapshot são do ADR-0002 (FNV-1a por seção e por arquivo; ainda `Proposed`) |
| AC-I3 [PM] | comparação no aparelho | aparelho de referência não verificado (semana 0) |
| AC-18 | a parte das fontes de recompensa | o GDD #26 não existe |
| AC-P1 | todo | números do spike (OQ-4) e aparelho de referência verificado; prazo: fim do spike (semana 3 a partir de D0). Trava o fechamento do MVP. Medição em emulador ou no editor **não** substitui o aparelho |

### Core Rules
- **AC-01 (Regra 1)** — **GIVEN** o código de gameplay, **WHEN** o CI roda o analisador de literais numéricos nas pastas de gameplay, **THEN** ele reporta 0 ocorrências fora da lista de exceções. **[MAN]** MVP
- **AC-02 (Regra 2)** — **GIVEN** três knobs de fixture, um sem dono, um sem unidade e um sem faixa, **WHEN** o conjunto é validado, **THEN** cada um é recusado com um erro que nomeia o campo ausente. **[EM]** MVP
- **AC-03 (Regra 3)** — **GIVEN** dois IDs iguais no mesmo tipo, **WHEN** o conjunto é validado, **THEN** ele é recusado; **GIVEN** a versão anterior com o ID `x` e a atual sem `x`, ou com `x` de outro tipo, **THEN** é recusado; **GIVEN** os mesmos IDs inseridos em ordens diferentes, **WHEN** o conjunto é carregado, **THEN** os índices inteiros são idênticos. **[EM]** MVP
- **AC-04 (Regra 4)** — **GIVEN** um campo `_ticks` = 0, **WHEN** validado, **THEN** é recusado; **GIVEN** um campo `_ticks` = 3, **THEN** a simulação recebe 3, sem conversão. **[EM]** MVP
- **AC-05 (Regra 5)** — **GIVEN** um conjunto com 1 valor fora da faixa entre 100 válidos, **WHEN** validado, **THEN** o conjunto inteiro é recusado e o valor original não é alterado. Também: `min` e `max` exatos aceitos; `0,1` com máximo `0,1` aceito; número com vírgula decimal, `NaN`, infinito e `int` fracionário recusados; `min > max` recusado; `min` de campo `_s` que converte para 0 tick (0,0166) recusado; 2 `placeholder` sem referência aceitos, com contagem = 2 no relatório. **[EM]** MVP
- **AC-06 (Regra 5, cultura)** — **GIVEN** a cultura corrente `pt-BR`, **WHEN** o valor `"2.5"` é validado, **THEN** ele é lido como 2,5. **[EM]** MVP
- **AC-07 (Regra 6)** — **GIVEN** o mesmo conteúdo serializado duas vezes, **WHEN** o hash é calculado, **THEN** os hashes são iguais; mudar 1 valor muda o hash do conjunto e só a revisão da skill afetada; revisão nova sem classificação é recusada; `neutra` com valor de gameplay alterado é recusada; `neutra` com só texto alterado é aceita. **[EM]** MVP
- **AC-08 (Regra 6, histórico)** — **GIVEN** uma skill selada na revisão A e o histórico A → B (`nerf`) → C (`buff`), **WHEN** a Reforja consulta, **THEN** "há nerf no caminho" é verdadeiro e cada passo traz classificação e data; **GIVEN** a revisão C com o mesmo hash de A, **THEN** a resposta é "sem mudança desde o selo"; **GIVEN** um passo `correcao`, **THEN** ele não conta como `nerf`. **GIVEN** uma passiva ou evolução referenciada por uma skill selada que sofre um `nerf`, **THEN** a revisão da skill selada muda e "há nerf no caminho" é verdadeiro; **GIVEN** um knob global alterado sem skills declaradas, **THEN** a validação recusa. Nenhuma resposta do #1 afirma elegibilidade de reforja. **[EM]** MVP
- **AC-09 (Regra 7, imutável)** — **GIVEN** uma fase carregada, **WHEN** os tipos do snapshot são inspecionados por reflexão, **THEN** todo campo é `readonly` e nenhum tipo é `T[]`, `List<T>` ou `Dictionary` (um `readonly int[]` não tem setter e continua mutável); um tipo-isca de fixture que viola a regra faz o teste reprovar. **GIVEN** uma partida headless inteira, **THEN** o hash do snapshot é igual antes e depois dela. **[EM]** MVP (a parte de reflexão fica BLOCKED até o ADR fixar o layout)
- **AC-10 (Regra 7, bloqueio)** — **GIVEN** uma fase com um dado inválido, **WHEN** o jogador tenta entrar, **THEN** a entrada é bloqueada e nenhum valor padrão é usado; com o catálogo global inválido, todas as fases ficam bloqueadas; com uma fase inválida, só ela. **[PM]** MVP
- **AC-11 (Regra 7, sem carga na fase)** — **GIVEN** uma partida em andamento com a fonte de dados instrumentada, **WHEN** 5 minutos de fase rodam, **THEN** há 0 leituras de arquivo e 0 conversões depois do tick 0. **[PM]** MVP
- **AC-12 (Regra 8)** — **GIVEN** um knob com `aceite: sim` marcado `remoto: sim`, **WHEN** validado, **THEN** o validador o recusa. **[EM]** MVP. **GIVEN** o mesmo conjunto no passo de build, **THEN** o build falha. **[MAN]** MVP (verificado no CI, não em EditMode). **GIVEN** um knob com `pior` mas sem `aceite: sim`, **THEN** é recusado. **[EM]** MVP. **GIVEN** o build de aceite com tag git e um pacote persistido no aparelho, **WHEN** o jogo inicia, **THEN** o pacote é ignorado e não é apagado. **[PM]** PÓS
- **AC-13 (Regra 9, validação do pacote)** — **GIVEN** um pacote de fixture fora da lista branca, fora da faixa, vazio, com knob repetido, com ID `deprecated`, alterando contagem de horda, com versão-base diferente ou alterando skill sem classificação, **WHEN** validado, **THEN** o pacote inteiro é rejeitado e o Ativo mantém o mesmo hash; **GIVEN** dois pacotes pendentes, **THEN** vale o de maior sequência mesmo que tenha chegado primeiro; **GIVEN** um pacote de `nerf` removido, **THEN** o histórico ganha um passo `buff`. **[EM]** PÓS
- **AC-14 (Regra 9, momento)** — **GIVEN** um pacote recebido durante a fase, **WHEN** a fase termina, **THEN** a partida seguinte usa a versão efetiva nova e a partida em curso fica registrada com a antiga; **GIVEN** o app morto durante a escrita do pacote, **WHEN** o jogo reinicia, **THEN** vale a última sobrescrita válida. **[PM]** PÓS
- **AC-14b (Regra 9, selo)** — **GIVEN** um pacote validado e um ritual de selo ou de registro aberto, **WHEN** o pacote chega, **THEN** a versão efetiva não muda até o ritual fechar; a revisão gravada no selo é a mesma que a partida seguinte usa; e a tela das cartas mostra os valores dessa mesma versão. **[PM]** PÓS (BLOCKED até existirem o #3 e o #17)
- **AC-15 (Regra 10, sem rede)** — **GIVEN** o assembly do #1, **WHEN** suas referências são inspecionadas, **THEN** não há `System.Net*` nem `UnityEngine.Networking`. **[EM]** MVP
- **AC-16 (Regra 5, referências cruzadas)** — **GIVEN** uma skill apontando para uma função inexistente ou `deprecated`, uma fase apontando para um inimigo ou chefe inexistente ou `deprecated`, e uma capacidade sem campo ou sem teto, **WHEN** validado, **THEN** cada caso é recusado com o ID, o campo e a regra violada; **GIVEN** uma definição `deprecated` que referencia outra `deprecated`, **THEN** é válida. **[EM]** MVP
- **AC-17 (Regra 5, relatório)** — **GIVEN** um conjunto com 3 erros de tipos diferentes, **WHEN** validado, **THEN** o relatório lista os 3 (não para no primeiro) e o conjunto inteiro é recusado. **[EM]** MVP
- **AC-18 (Regra 10, MVP)** — **GIVEN** o assembly do #1, **WHEN** os seus tipos públicos são inspecionados, **THEN** nenhum método de escrita é exposto a outros sistemas em tempo de execução; e nenhum assembly de fonte de recompensa referencia uma API de teto do #1. **[EM]** MVP (a parte das fontes de recompensa fica BLOCKED até o #26 existir)
- **AC-19 (Regra 10, pacote)** — **GIVEN** pacotes de fixture que tocam um teto da economia, uma capacidade, uma constante de tick ou a existência de uma definição, que citam um ID inexistente, ou que trazem 1 valor inválido entre N válidos, **WHEN** validados, **THEN** cada pacote é rejeitado inteiro e o Ativo mantém o mesmo hash; **GIVEN** um pacote com qualquer campo de segmentação (por exemplo `audience`, `segmento`, `pagante`), **THEN** é rejeitado inteiro e o Ativo mantém o mesmo hash. **[EM]** PÓS

### Formulas
- **AC-F1** — **GIVEN** as durações 0,15 s, 2,5 s, 0,0167 s, 0,0166 s e 0,01 s, **WHEN** convertidas, **THEN** as três primeiras dão 5, 75 e 1 ticks, e as duas últimas são recusadas (sem ajuste). **[EM]** MVP
- **AC-F1b (instantes)** — **GIVEN** os instantes `inicio_s` de 0, 0,05, −0,1 e 601 (com `instante_max_s` = 600), **WHEN** convertidos como instantes, **THEN** dão 0 (válido), 2 (válido, meio tick para cima), recusado e recusado; **GIVEN** uma duração de 0 s, **THEN** é recusada (a regra de instante não vale para durações). **[EM]** MVP
- **AC-F2** — **GIVEN** as taxas 4,5, 100, 0 e −4,5 por segundo (montadas como `decimal` em código), **WHEN** convertidas, **THEN** `BitConverter.SingleToInt32Bits(resultado)` é igual aos bits esperados de cada caso, sem tolerância: `0.15f`, `0f` e `-0.15f` valem em qualquer caminho; para 100 por segundo os bits são `3.33333325f` (o ADR-0002 decidiu dividir em `decimal`; multiplicar por `1f/30f`, que daria `3.3333335f`, foi descartado). Os bits esperados em hexadecimal saem do editor real e são fixados no teste depois que o ADR-0002 for aceito. **[EM]** MVP — **BLOQUEADO até o ADR-0002 ser aceito**
- **AC-F3** — **GIVEN** pico 300 e margem 25, **WHEN** a capacidade é checada, **THEN** `cap` 400 com teto 512 passa, `cap` 360 é recusado e `cap` 600 com teto 512 é recusado; valores perto de `int.MaxValue` não estouram. Para a tabela de ids (`spawns_de_dados` 899, `ids_de_preparacao` 1, margem 25): `cap` 1100 é recusado no build; `cap` 1124 passa no build (a recusa pelo compositor é critério do ADR-0001, item 6); `cap` 1125 passa nas duas. **[EM]** MVP
- **AC-F4** — **GIVEN** P = 5 + 5, **WHEN** o setup do Grimório é checado, **THEN** C = 5 passa, C = 7 é recusado, `P_f` = 1 é recusado, e um `placeholder` não conta em P. **[EM]** MVP
- **AC-F5** — **GIVEN** N_fases = 5, **WHEN** o K_min é checado, **THEN** K_min 7 com replays ilimitados passa, K_min 3 é recusado, e K_min 7 com `R_max` = 1 é recusado. **[EM]** MVP
- **AC-F6** — **GIVEN** um knob de aceite com padrão 2, pior 2 e `menor_melhor`, **WHEN** validado, **THEN** passa; com padrão 3, ou sem `sentido`, é recusado. **[EM]** MVP

### Interações entre sistemas
- **AC-I1 (#2)** — **GIVEN** uma fase carregada, **WHEN** o tick 0 executa, **THEN** o snapshot já estava completo, o `SimWorld` e o `EventBuffer` foram dimensionados pelas capacidades do #1, e `DroppedEvents` = 0 ao fim de uma partida de referência. **[PM]** MVP
- **AC-I2 (#5)** — **GIVEN** uma partida e uma execução headless, **WHEN** o cabeçalho do log é lido, **THEN** ele traz hash, rótulo e tag (e o pacote aplicado, no pós-lançamento); uma rejeição gera uma entrada com o motivo. **[EM]** MVP (campo do pacote PÓS)
- **AC-I3 (headless)** — **GIVEN** um hash dourado do snapshot convertido, commitado no repositório, **WHEN** o editor (jogo e simulação headless) carrega o conjunto, **THEN** o hash é igual ao dourado. O dourado vive num arquivo dedicado que **nenhum teste escreve**, só muda por revisão explícita (commit próprio, com entrada no changelog), e cobre os bits do snapshot convertido, não o texto autoral. **GIVEN** um fixture negativo (1 bit alterado no snapshot), **THEN** o teste reprova. **[EM]** MVP — **BLOQUEADO até o ADR-0002 ser aceito**. (Comparar jogo e headless entre si, no mesmo editor, passa por construção e não conta como evidência.) O mesmo teste no build Android IL2CPP ARM64 comparando com o mesmo dourado: **[PM]** MVP, é o que fecha o risco do parse de float entre Mono e IL2CPP, `NOT SOURCEABLE` hoje.
- **AC-I4 (headless, candidato)** — **GIVEN** um pacote candidato inválido, **WHEN** a simulação headless roda, **THEN** ela aborta antes do tick 0 com a lista de erros e nada é persistido. **[EM]** PÓS
- **AC-I5 (#28)** — **GIVEN** um save com uma skill selada `deprecated`, **WHEN** ela é resolvida pelo ID, **THEN** resolve com os seus últimos valores e fica fora da F4; um ID ausente responde "desconhecido" sem criar nada. **[EM]** MVP
- **AC-I6 (#7, relatório)** — **GIVEN** uma fase válida do MVP, **WHEN** o build valida, **THEN** o relatório traz, por fase, a linha do tempo em `CombatTick`, o pico agendado como % do teto, `xp_min` e `xp_max`, os sinais da F10 e da F11, o id de classe de vetor de cada direção e, por elite, o `duelo_min_ticks` e a janela; **GIVEN** uma fase inválida, **THEN** o relatório nomeia cada erro da F10 com o `w` da entrada. **[EM]** MVP

### Performance
- **AC-P1** — **GIVEN** o aparelho de referência e a fase mais pesada, **WHEN** são feitas 20 cargas frias (processo reiniciado) e 20 quentes (segunda carga na mesma sessão), com a temperatura inicial e o modo de energia registrados, **THEN**, **separadamente para a carga fria e para a quente**, o **máximo** das 20 cargas fica dentro do orçamento correspondente (`phase_load_budget_cold_ms` ou `phase_load_budget_warm_ms`), a **mediana** fica dentro de 70% desse orçamento (fator provisório, a reavaliar), e o p95 é registrado no relatório; e a memória do snapshot com as capacidades pré-alocadas fica dentro de `phase_snapshot_memory_kb`. Cada orçamento é o **menor** entre (máximo medido no spike × 1,2; fator provisório) e o teto absoluto decidido pelo usuário (`phase_load_ceiling_cold_ms` = 3000, `phase_load_ceiling_warm_ms` = 1500; provisórios, a reavaliar): assim o AC reprova uma fase lenta desde o início e não só uma regressão. A "fase mais pesada" é uma fase nomeada por ID no relatório do spike, e o instrumento de memória também é definido nele. Os orçamentos são commitados **antes** do build de aceite, onde o AC é verificado; assim ele pode reprovar. **[PM]** MVP — **BLOQUEADO pelo spike de performance e pelo aparelho de referência**: os orçamentos e a memória não têm valor até a medição (ver Tuning Knobs), e o critério não conta como aprovado antes disso. Prazo: fim do spike (semana 3 a partir de D0); ele trava o fechamento do MVP.

### Não testável por teste automatizado (verificação por revisão ou processo)
- "A mesma função de validação (`DataValidator`) no editor, no teste e na validação de pacote remoto" (Regra 5) é estrutural: verifica-se por revisão de código (um único ponto de entrada). No carregamento do embarcado a verificação é outra (`SnapshotVerifier`: estrutura e hash), coberta pelos testes do ADR-0002.
- "`neutra` só sem mudança de valor de gameplay" (Regra 6) depende de cada campo estar marcado como de gameplay ou não; a marcação é definida pelo ADR de formato do #1 (Open Questions).
- O congelamento dos knobs de aceite por tag git antes de D0 (Regra 8) é processo: item de checklist manual no doc de aceite.
- "O #6 não pode afirmar soma exata" (F2) é restrição sobre outro GDD: cabe ao `/design-review` do #6.
- Escrita atômica e expiração do pacote dependem do ADR do #29, que pode reaproveitar o mecanismo do ADR-0003 (o ADR-0002 só fixa o contrato do pacote); os testes PÓS correspondentes são escritos depois dele.

*Consultado:* `qa-lead` (critérios, tipos de evidência, orçamento a medir). Decisões menores adotadas no modo guided: AC-01 como verificação manual ou de CI; orçamento de performance como knobs a medir, com o AC-P1 bloqueado até o spike.

## Open Questions

| # | Pergunta | Dono | Resolver até |
|---|---|---|---|
| OQ-1 | A leitura da F4 está certa? O `5` da checagem do conceito (L407) é `S + 1` e o `4` é `S`? E o termo novo `P_f ≥ S_f` é o que o #17 quer? | GDD #17 Selamento (`game-designer`, `systems-designer`) | ao escrever o GDD #17, revisado junto com o #16 |
| OQ-2 | **Resolvida em 2026-11-05 no ADR-0002 (`Proposed`; falta a aceitação e os spikes).** Pergunta original: ADR do #1: formato de autoria (ScriptableObject, JSON ou híbrido), passo de build que gera o snapshot, hash canônico e ordem de serialização, hook de validação no editor, layout dos structs de fase, cálculo da revisão por skill, **marcação de cada campo como de gameplay ou não** (exigida pela regra de `neutra`) e persistência, escrita atômica, assinatura e expiração do pacote remoto. **Acrescentado na revisão de 2026-11-03 (provisório, a reavaliar):** dado autoral guardado como texto; onde converter (recomendação: no build, gravando os bits do `float`); concordar com o ADR-0001 sobre dividir ou multiplicar por `TickSeconds`; revisão da skill (hash do fecho de dependências mais contador sequencial por skill); pacote chegando como bytes (JSON) pelo #29, sem Addressables; assembly puro e sem estado `static` mutável no carregador. **Acrescentado na 2ª passada (provisório, a reavaliar):** não confiar no cast `(float)decimal` (gravar os bits do `float` no build, ou guardar o valor como inteiro escalado e dividir dois `float` exatos); hash canônico com `string.CompareOrdinal`, FNV-1a próprio (não `string.GetHashCode`), bits do `float`, `-0` canonicalizado ou recusado e endianness explícita; snapshot embutido como `TextAsset` ou `ScriptableObject` baked (síncronos), não em StreamingAssets, e a exceção do Addressables, se usado, vira "bloqueia a fase"; verificação de referências proibidas (`System.Net`, `UnityEngine.Networking`) por análise de símbolos, com assembly puro `Forja.Data`; registrar que o GDD recusa o tempo que dá menos de 1 tick, enquanto o ADR-0001 L188 diz "mínimo 1 tick"; ponto único público de entrada para a validação | `technical-director` (via `/architecture-decision`) | antes da primeira story do #1 |
| OQ-3 | Riscos de engine levantados pelos especialistas para o ADR da OQ-2: Addressables lança exceção na falha de carga a partir do 6.2 (`breaking-changes.md`, MEDIUM, confirmar no 6000.3.27f1); domain reload desligado, stripping do IL2CPP para tipos de dados, recarga a quente no editor e parse de float entre Mono e IL2CPP são `NOT SOURCEABLE` | `unity-specialist` | no ADR da OQ-2; o parse de float é fechado pelo AC-I3 [PM] |
| OQ-4 | Valores de `capacity_ceiling` (separar o teto de entidades ativas, medido em frame time com ocupação real em `cap` = pico × 1,25, do teto de memória alocada), `phase_load_budget_cold_ms`, `phase_load_budget_warm_ms` e `phase_snapshot_memory_kb` (os tetos absolutos de carga, 3000 e 1500 ms, já estão decididos e são provisórios) | usuário, com `performance-analyst` | spike de performance (semanas 1 a 3 a partir de D0); o AC-P1 fica bloqueado até lá |
| OQ-5 | **Resolvida do lado do #7 em 2026-11-06 (Regra 14 do #7):** o #7 deriva o pico (`pico_vivos_7`) e os spawns das waves (`total_spawns_7`, F7) das contagens, e no MVP, pelo ADR-0002, contagens, pesos, pico, total de spawns, `teto_vivos_horda`, capacidades e arena nunca são remotos. Abrir essa porta é decisão pós-MVP e exige emendar o ADR-0002 (o pacote remoto teria de recalcular os dois números e revalidar a capacidade); até lá continuam não remotas | GDD #7 Horda e usuário | antes do pacote remoto (#29) |
| OQ-6 | A aposentadoria (`deprecated`) de uma skill selada dá direito a reforja? | GDD #18 Reforja | ao escrever o GDD #18 (Alpha) |
| OQ-7 | Qual ferramenta faz o analisador de literais numéricos do AC-01, e qual é a lista de exceções? | `tools-programmer` | antes da primeira story de gameplay |
| OQ-9 | **Decisões aceitas por recomendação, a reavaliar com o jogo avançado.** O usuário aceitou as recomendações técnicas sem dominar todos os conceitos e pediu para revisitá-las quando houver jogo rodando: partida = run de fase; sobrescrita remota por lista branca e só entre partidas; nerf por marcação autoral (`nerf`, `buff`, `correcao`, `neutra`), com `neutra` só sem mudança de valor e "qualquer nerf no caminho" levado como insumo ao #18; entre dois pacotes vale o de maior sequência; remover um pacote herda a classificação inversa; meio tick arredonda para cima; margem de capacidade de 25%; contagens de horda não remotas. Nenhuma delas muda o que o jogador vê no MVP (a parte remota é pós-lançamento), com uma exceção apontada na 2ª passada: o arredondamento de meio tick para o inteiro mais próximo (ADR-0001) muda levemente tempos curtos (um cooldown de 0,45 s roda a 0,467 s; um hit-stop de 0,05 s roda a 0,067 s). | usuário | primeira revisão com o jogo jogável (vertical slice) |
| OQ-8 | `.claude/rules/data-files.md` L27 proíbe entradas órfãs ("every entry must be referenced"), mas este GDD permite definições `placeholder` sem referência (Regra 5). Acrescentar a exceção à regra ou eliminar os stubs do MVP? | usuário | antes da primeira story do #1 |
| OQ-10 | Para a regra de elegibilidade do conceito (L191, nerf líquido **acima de um limiar**), o #18 precisa da magnitude de cada mudança? Se precisar, o histórico do #1 ganha um campo de magnitude (ou a marca `acima_do_limiar`) antes do Alpha. Junto: a política interina do índice (L195: até existir a reforja por nerf, nenhuma skill selável recebe nerf líquido acima do limiar) deve virar uma checagem mecânica do #1 a partir do lançamento? Durante o desenvolvimento ela não se aplica, para não travar o balanceamento. | GDD #18 Reforja e Live Ops | ao escrever o GDD #18 (Alpha), antes do soft launch |
| OQ-11 | Revisões **recomendadas** da 2ª passada de 2026-11-03, ainda não aplicadas (nada disso bloqueia): separar AC-05 em casos independentes (05a a 05h) com entradas em notação de código (`0.1m`, `"2,5"`), e AC-06 com `try/finally` e o caso `tr-TR`; separar AC-07, AC-08 e AC-13 em casos (nove pacotes inválidos parametrizados, desempate por sequência, inversão de `buff`, `neutra` e `correcao` na remoção); AC-10 e AC-11 viram EditMode (retorno de falha; 9.000 ticks headless com contador) e "leitura" passa a significar leitura de dados de gameplay; AC-F6 com `maior_melhor` e `padrao < min`; fronteiras exatas de F3 a F5 (`cap` 375 passa e 374 recusa; `R_max` total de replays, com representação de ∞); isolar P_f = 1 e P_c = 9 no AC-F4; faixa do override de margem por capacidade; AC-01 com lista de exceções limitada a `{0, 1, -1}`; AC-02 e AC-03 com todos os campos da Regra 2; ACs para o estado Revertida, o abandono com pacote pendente, o update que descarta o pacote e o embarcado inválido que derruba o build; padronizar a notação da F1; medir o custo de boot e de validação, o GC e a fragmentação entre partidas; margem por tipo de capacidade; "tudo ou nada" por unidade (catálogo ou fase, L241); direção da mudança derivada do `sentido`; padrão "todo campo é de gameplay até ser marcado cosmético" e knob global sem skills declaradas assume "todas"; expiração ou remoção de pacote como classificação `reversao` que o #18 pode excluir; campo `anunciado_em` no pacote (L191 do conceito); exigir K_min > C (a confirmar no #17); avisar quando o erro de quantização passar de cerca de 5% em cooldowns; mesmo hash efetivo em partida com mais de um humano e hash na submissão de ranking (pós-lançamento). **1ª passada (2026-11-03):** gravar valor antigo e novo de cada knob no histórico; direção da mudança calculada pelo `sentido` do knob, e `correcao` com referência a nota publicada; o registro do selo guarda a revisão do conjunto Ativo da partida do selo; "knob que conta para o ranking", ranking versionado e buff temporário que expira; pico declarado ≥ pico derivado das waves; faixa do override de margem e erro quando não há `cap` possível; F4 e F5 são só condições necessárias (alvo da reforja, `R_max` finito); teto separado em ativo (frame time) e alocado (memória), medido com ocupação real em `cap` = pico × 1,25 (um teto igual ao máximo sustentado pelo spike recusaria o próprio cenário do spike); margem por tipo de capacidade; ACs menores (AC-F6, fronteiras de F3 a F5, AC-15, AC-09, checklist dos itens [MAN]); hash do subconjunto de aceite; orçamento de validação do pacote e custos de GC e de boot | usuário (via re-review) | antes do ADR do #1 |
