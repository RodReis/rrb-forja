# Simulação de combate determinística (#2)

> **Status**: In Review (ciclo do `/design-review` encerrado em 2026-11-04 após 2 passadas, o limite do projeto: 1ª NEEDS REVISION com 7 bloqueantes e 2ª NEEDS REVISION com 4 bloqueantes, todos aplicados no texto; sem 3ª conferência, como no #1 e no #28)
> **Author**: Rodrigo Reis + Claude Code (agentes consultados por seção)
> **Last Updated**: 2026-11-05
> **Last Verified**: 2026-11-04
> **Implements Pillar**: P4 *Massacre com peso* (granularidade de tick e de esquiva); habilita a medição de aceite do MVP (comparação Tank × DPS na mesma seed). Base técnica: ADR-0001 (Proposed).
> **Creative Director Review (CD-GDD-ALIGN)**: CONCERNS → REVISED 2026-11-04. Nenhum achado bloqueante; aplicados os achados 1 a 4 e 6 a 9 (texto da fantasia, vitória × morte no mesmo tick, erro no herói ou chefe, regra de sorteio visível, auto-battle, retomada e escopo do MVP); o 5 entrou como restrição para o #9 e o #26. Decisões do autor em 2026-11-04: a vitória vale na morte simultânea; erro interno no herói ou chefe é tentativa falha sem derrota; regras que mudam sorteio são visíveis ao jogador.

## Summary

A Simulação determinística (#2) é o relógio e o motor de regras de cada fase de combate: ela avança o jogo em passos fixos de 1/30 de segundo, recebe os comandos de quem joga e devolve o que aconteceu, sempre do mesmo jeito para a mesma seed e os mesmos comandos no mesmo build do app. O jogador não a vê, mas é ela que faz o combate responder de forma honesta e aprendível ("a horda não trapaceia"). Ela existe para que a comparação Tank × DPS, o teste sem tela do Grimório, o auto-battle e a reprodução de bugs usem o mesmo código do jogo.

> **Quick reference** — Layer: `Core` · Priority: `MVP` · Key deps: `#1 Dados e balanceamento`

## Overview

A Simulação determinística (#2) é o relógio e o motor de uma fase de combate. Ela avança o jogo em passos fixos de 1/30 de segundo (cada passo é um *tick*), recebe a cada tick os comandos de quem joga e devolve o que aconteceu como uma lista de eventos. Com a mesma *seed* (o número que inicia todos os sorteios) e a mesma sequência de comandos, ela produz o mesmo estado, tick a tick, **no mesmo build do app** (mesmo binário e mesma arquitetura de CPU; ver Regra 12). Ela não conhece tela, toque nem som: a apresentação só lê os eventos e desenha. Os sorteios do jogo (composição das waves, ofertas de cartas, loot) saem de três fluxos independentes de números aleatórios, de modo que mudar a regra de um deles não altera o que os outros sorteiam na mesma seed.

O jogador não interage com o #2 diretamente: ele sente o resultado, um combate que responde do mesmo jeito toda vez que as mesmas escolhas são feitas. O projeto precisa dele por quatro razões. (1) A comparação Tank × DPS na mesma seed, que o aceite do MVP exige, só vale se as duas execuções veem as mesmas waves. (2) A simulação *headless* (sem tela) do MVP roda o **mesmo código** de oferta, registro e substituição do Grimório que o jogo roda, e não um modelo paralelo. (3) O auto-battle (#40, Full Vision) joga a fase sozinho sob as mesmas regras, com comandos vindos de uma política em vez de um dedo. (4) Qualquer bug de combate precisa poder ser reproduzido: mesma seed, mesmos comandos, mesmo resultado.

**Fronteira.** O #2 é dono do relógio (o tick), da ordem fixa em que os sistemas rodam em cada tick, dos fluxos de sorteio, do contrato de comandos de entrada e de eventos de saída, e da garantia de reprodutibilidade com o teste que a prova. Ele **não** é dono: das regras de dano e vida (#6), da composição das waves (#7), das skills (#8), do fluxo da fase (#3), do log de aceite (#5), do input e da câmera (#4), da conversão de segundos para ticks nem da validação dos dados (#1, F1 e F3), nem de replay gravado (Full Vision; o MVP só exige reprodutibilidade no mesmo build). O desenho técnico (float32, 30 Hz, PCG32, `Tick` + buffer de eventos, `SimWorld`) está decidido no ADR-0001 (*Proposed*), que este GDD cita e não repete.

## Player Fantasy

**Enquadramento: indireto.** O jogador nunca vê a simulação; ele sente a ausência de trapaça. O #2 é a razão técnica pela qual a frase abaixo pode ser verdadeira.

> **A horda não trapaceia.** Quando você cai, foi a horda, a sua build e a sua mão. Nada muda os dados da sua run em segredo: ajustes de balanceamento são globais, valem para todos e só entram entre fases, nunca no meio de uma. E o perigo segue um ritmo fixo, que se aprende: a esquiva que salvou você ontem salva hoje.

**O momento.** O jogador morre na wave 12, olha o que selou e o que lhe foi oferecido, e entende por quê. Quando vence um chefe e sela a build, sabe que foi mérito dele. Não existe dificuldade que se ajusta escondida nem sorteio escondido que ajuda ou atrapalha quem está perdendo; toda regra que muda um sorteio (como a garantia do Grimório) é regra de design **visível para o jogador** (decisão do autor, 2026-11-04) e escrita nos GDDs, nunca um ajuste silencioso. Isso vale como restrição para o #9, o #16 e o #26.

**Pilares que sustenta.**

- **P2 *Toda escolha pesa* (apoio indireto):** no conceito o P2 trata de decisões de build permanentes (o selo e a reforja). O #2 só sustenta que essas decisões são mérito do jogador: a build selada veio de ofertas que a máquina não refaz nem troca de lado.
- **Princípio de Negócio *Poder conquistado, não comprado*:** ninguém compra nem ganha uma sorte melhor no sorteio. Nenhum fluxo de sorteio lê estado de loja, de posse paga ou de vídeo, e nenhum comando que mexe em sorteio (reroll, favorecer) pode vir de compra ou de vídeo; esta segunda regra é do #9 e do #26.
- **P4 *Massacre com peso* (apoio):** o ritmo dos perigos é estável, o que torna a esquiva uma habilidade que se aprende. O *peso* do golpe em si pertence ao #6 e ao #12; o #2 só garante o ritmo.

**Teste de acerto (playtest do próprio autor).** Depois de uma derrota, a frase "perdi por causa da build ou da minha mão" sai com naturalidade, e "o jogo me roubou" não aparece.

**O que esta fantasia NÃO promete** (para que nenhum outro GDD a cite como garantia):

- replay, "reveja sua run" ou ranking verificado por reprodução (Full Vision; o ADR-0001 não garante isso);
- o mesmo resultado em qualquer aparelho, ou desafio diário igual para todos (a garantia vale só no mesmo build);
- "a fase é sempre igual" (a política de seed por tentativa é do #3; nada aqui promete a mesma composição a cada retry);
- que o auto-battle "joga como você" ou garante vitória (ele segue as mesmas regras e pode falhar);
- que os ajustes de balanceamento sejam anunciados: o anúncio é do #1 (que guarda `anunciado_em`) e da UI do #26 e do #34; o #2 só garante que o snapshot da fase não muda no meio dela;
- que a esquiva caia no mesmo tick em qualquer taxa de quadros: ela tolera ±1 tick de variação por fps, e a amostragem do toque e a janela de esquiva (no mínimo 5 ticks, contando o jitter de ±1; GDD #6, `janela_ticks`) são do #4 e do #6;
- precisão de frame (o passo é de cerca de 33 ms).

## Detailed Design

### Core Rules

> **Marca de provisório.** Toda regra marcada *(provisória)* foi decidida por recomendação de especialista, não pelo autor, e deve ser reavaliada com o jogo avançado (depois do spike de performance e do spike de hash). As demais vêm do ADR-0001 ou de decisão do autor em 2026-11-04.

1. **Início da fase.**
   1. A simulação só é criada depois que o #28 confirma a marca da fase e o #1 entregou o snapshot da fase **validado e já convertido em ticks**. Sem snapshot válido, a fase não começa e o #2 não é criado (o #1 bloqueia a entrada).
   2. O `seedMestre` vem do #3, por meio do host. A seed é **nova a cada tentativa** (decisão do autor, 2026-11-04; GDD #3, Regra 10, resolve a OQ-2). O host grava o `seedMestre` no log (#5) **antes** do tick 0.
   3. O host cria a simulação por `Simulation.Create(snapshot, hashDoCabeçalhoDoLog, seedMestre, sistemas na ordem do compositor, estrito)`. O `Create` confere o snapshot e compara o hash dele com o do cabeçalho do log; se falhar, lança exceção e a simulação não existe (erro de quem chama). `estrito` é uma opção da instância (Regra 14), nunca `#if` nem `static` *(provisória; exige a nova assinatura no ADR, OQ-5)*. O `SimWorld` e o `EventBuffer` são dimensionados pelas capacidades do snapshot (Regra 8). Cada stream (`Spawn`, `Offer`, `Loot`) nasce de `SplitMix64(seedMestre ^ idDoStream)`, com o id como sequência do PCG32.
   4. O estado inicial é o **tick 0**: `CurrentTick = 0` e nenhum `Tick` foi chamado. O herói é criado pelo #3 no `Preparar` (interface opcional `IPreparaFase`, chamada pelo compositor depois do `Create` e antes do 1º `Tick`; GDD #3, Regra 3.4, resolve a OQ-3, *provisória*); o #2 só exige que a criação seja por `SimWorld.Spawn`, sem emitir evento, e que o id saia do contador da fase.

2. **O que um Tick faz, em ordem.**
   1. Valida os comandos (Regra 3).
   2. Faz `CurrentTick += 1` e tira uma **foto** do estado do combate: `ctx.CombatActive = (CombatHold == 0)` (Regra 15). Se `CombatActive`, também faz `CombatTick += 1`. Todos os sistemas leem só a foto no `ctx`, nunca o `CombatHold` ao vivo, de modo que o resultado não depende da ordem dos sistemas. O primeiro `Tick` produz eventos com `Tick = 1`; o número do evento é o `CurrentTick` em execução.
   3. Limpa o `EventBuffer`.
   4. Copia, para cada entidade viva, a posição atual para a posição anterior (a interpolação lê as duas). Uma entidade que nasce durante o tick nasce com posição anterior igual à atual, para não deslizar na tela.
   5. Roda cada sistema, na ordem do compositor (Regra 5).
   6. Confere se posição e HP das entidades **vivas** são finitos (Regra 9). Uma entidade `Essencial` inválida encerra a simulação com `FalhaInterna` e **o pedido de fim feito pelo #3 neste tick é ignorado**: `FalhaInterna` > vitória > derrota *(provisória)*.
   7. Verifica o pedido de fim da fase (Regra 13).

   O `Tick` nunca calcula hash, nunca lê relógio ou frame, nunca aloca memória gerenciada e roda apenas na thread principal; ele **não é reentrante nem thread-safe**.

3. **Validação de comandos** (feita pela simulação, antes de qualquer sistema).
   - Comando para ator nunca emitido: descartado, contado em `CommandsRejected` e, em modo estrito, falha. Comando para ator **já morto**: descartado e contado, **sem** falha, porque a ponte não vê a morte entre dois ticks do mesmo frame. Se o ator morre no mesmo tick antes de o sistema ler o comando, o sistema o ignora sem contar. *(provisória)*
   - Dois comandos do mesmo ator e do mesmo tipo no mesmo tick: vale o primeiro; os demais são descartados e contados. Tipos diferentes do mesmo ator (Mover e Esquivar) são permitidos.
   - **Forma do comando.** `Command` leva `ActorId`, `Kind`, `X`, `Y` e dois inteiros, `ArgA` e `ArgB` (ignorados fora do tipo que os usa) *(provisória; exige os campos no ADR, OQ-5)*. `X` e `Y` só valem para `Mover` e só nele são validados: eixo que não seja número finito, ou com valor absoluto acima de `EixoMax` (inicial 1, *provisória*), faz o comando ser descartado e contado. O módulo do eixo é limitado a 1 pela FS7; a faixa de significado do eixo é do #4 e do #6.
   - **`PickOffer`** é `(ActorId do herói dono da oferta, ArgA = serial da oferta, ArgB = índice da carta)`. O serial é o número de ofertas abertas na fase, guardado pelo #16 e no `Hash` dele. **Quem valida o serial é o #16, no passo dele** (o passo 1 só confere a forma: `ActorId` e tipo): comando com serial diferente do da oferta pendente é descartado e o #16 incrementa `CommandsRejected` pelo contexto (é o caso do toque duplo e da segunda oferta da fila): um toque nunca escolhe a carta de uma oferta que o jogador não viu. Como leva `ActorId`, entra na ordenação normal abaixo *(provisória)*.
   - O chamador entrega os comandos ordenados por `ActorId` crescente e, depois, por tipo. A ordem recebida faz parte da entrada reproduzível; em modo estrito a simulação falha se a ordem não for essa. Em modo não estrito, ela processa os comandos na ordem recebida (não reordena, porque a ordem recebida é a entrada reproduzível) e não conta nada: o resultado segue reproduzível pela sequência de comandos. O `ReadOnlySpan` é do chamador: a simulação não o guarda depois do `Tick`. *(provisória)*

4. **Comandos valem só no tick em que chegam.** A simulação não guarda comando; sem comando, o joystick está solto. Quando um frame de tela roda vários ticks, a ponte entrega o `Mover` em **todos** eles e entrega `Esquivar`, `Suprema` e `PickOffer` **uma única vez**, no primeiro tick do frame. Se o frame de tela roda 0 ticks (tela a 60 Hz e simulação a 30 Hz), a ponte segura essas ações até o próximo `Tick` executado (dois toques viram um; a pausa apaga a ação guardada). A lógica de entrega é função pura, como a FS1 e a FS2, para rodar em EditMode. A amostragem do toque é do #4. *(provisória)*

5. **Ordem dos sistemas e comunicação.**
   - A lista de sistemas é única, montada em **um só lugar** (o compositor em `Forja.Gameplay.Sim`) e usada pelo jogo e pelo teste sem tela. O #2 é dono desta regra e da tabela abaixo; cada GDD de sistema declara "preciso rodar depois de X" e a tabela cresce quando ele existir.
   - Ordem provisória: **#7 Horda → #8 Skills → #6 Combate → #3 Fluxo de fase → #16 Oferta**. O #3 vem depois do combate porque XP e fim de fase dependem das mortes; o #16 vem depois do #3 porque a oferta nasce do level-up do mesmo tick. Quem move o herói e os inimigos foi decidido no GDD #6 (OQ-4): o #6 move todos e é o único escritor de posição e HP; o #7 só faz nascer e declara a velocidade do arquétipo. *(provisória)*
   - **Mudar a ordem muda os resultados**, então a ordem é regra de balanceamento: uma mudança exige revisar os GDDs afetados.
   - Os sistemas conversam **só pelo `SimWorld` dentro do Tick**, nunca por evento; fora do Tick, o compositor chama as interfaces opcionais `IPreparaFase` e `IConcluiFase` (GDD #3). Dentro de um sistema, a iteração é por índice crescente. Nenhum `Dictionary` ou `HashSet` decide ordem de efeito.

6. **Eventos.** O `EventBuffer` é só de saída, para a apresentação e o log (#5). A ordem é a de emissão (ordem dos sistemas e, dentro deles, índice crescente). O buffer só vale até o próximo `Tick`: o host o **drena depois de cada Tick**, nunca uma vez por frame. Ler `Events` durante o `Tick` é proibido. O catálogo `SimEventKind` só cresce no final, e cada GDD é dono do significado dos seus tipos. Com o buffer cheio, ficam os eventos mais antigos do tick e os novos são descartados e contados em `DroppedEvents`, cumulativo na fase. Uma constante `EventosReservados` (de 8 a 16 posições, *provisória*, sem spike) é reservada a tipos críticos (`Death` do herói, fim de fase, oferta e **início do telegraph de elite e de chefe**), que não são descartados enquanto houver reserva, para que o log de aceite não perca o que decide o resultado e o jogador não perca o aviso de um golpe (um telegraph perdido é "o jogo me roubou"). **O descarte nunca altera o estado**: evento é saída, e o tamanho do buffer não muda o hash. Em modo estrito, o primeiro `DroppedEvents` lança exceção; em modo não estrito, o contador vai para o log (#5) (Regra 14).

7. **Mortes e spawns dentro do tick.** Valem na hora: o sistema seguinte, no mesmo tick, já os vê. Uma entidade que nasce no tick pode ser alvo no mesmo tick. Quem zera o HP emite `Death` uma única vez; dano em alvo já morto é descartado. Ids nunca são reutilizados na fase. **Laço do sistema:** cada sistema captura a contagem de vivos no início do seu passe; a entidade que nasce durante o passe só age a partir do sistema seguinte (mas já pode ser alvo); a morte só marca a flag de vivo, sem remover da lista no meio do laço, e a lista de vivos é compactada no fim do tick (depois do passo 6), então nenhum elemento é pulado nem visitado duas vezes. **Exceção interna (GDD #6, Regra 3 e F2, provisória):** dentro do passo do #6, dano e cura são resolvidos em dois tempos (7a soma por alvo, 7b grava HP e chama `Kill` por id), então a morte só vale ao fim do passo do #6 e dois alvos fatais no mesmo passe morrem juntos; para os sistemas seguintes (#3, #16) a morte continua valendo na hora, no mesmo tick. *(provisória; a alternativa de aplicar mortes só no fim do tick foi avaliada e recusada por custo, e pode voltar se a ordem fixa gerar viés visível.)*

8. **Capacidade e ids.** O id de uma entidade é o seu índice na tabela, e ids nunca se reutilizam. Logo a capacidade de entidades da fase precisa cobrir o **total de spawns da fase** (soma das waves e invocações), e não só os vivos ao mesmo tempo. O #7 declara esse total; o #1 recusa a fase se ele não couber (F3 do #1, ver OQ-1). Quando a capacidade acaba, `SimWorld.Spawn` devolve `-1` e incrementa `SpawnsRejected`; em modo estrito lança exceção, em modo não estrito o contador vai ao log (#5) e a fase segue (decisão do autor, 2ª passada: em release isso é bug de dado do #7, a corrigir no dado, sem punir o jogador; o `Spawn` rejeitado do herói ou do chefe continua sendo bug interno e a fase falha). O `SimWorld` mantém a lista dos **vivos** em ordem de id, para que os sistemas não percorram os mortos. Se o total real de spawns de alguma fase não couber de jeito nenhum, a saída é um novo ADR (espaço reciclado com geração), não um remendo aqui. *(provisória; custo e tamanho a medir no spike.)*

9. **Aritmética e valores inválidos.** Valem as regras do ADR-0001 (só `float`; `+ - * /` e comparação direto, o resto por `SimMath`; sem funções transcendentais, sem `double`, sem `Mathf` nem `Unity.Mathematics`). Em acréscimo:
   - Somatórios sempre por índice crescente. Nenhum `==` entre floats calculados (comparar distâncias ao quadrado). Todo empate (alvo mais próximo, ordenação) desempata por id; nunca ordenar só por chave float.
   - Todo divisor é garantido maior que zero pela validação do #1 ou por guarda explícita. `SimMath.Sqrt` trata entrada negativa como 0. Conversão de float para inteiro só por `SimMath.RoundToInt` e `FloorToInt`, com checagem de faixa (valor fora da faixa do `int`, NaN ou infinito é bug interno e lança exceção); `RoundToInt` arredonda o meio para longe de zero (a mesma regra de `duracao_ticks`, F1 do #1) *(provisória; vira linha no ADR ou em `SimMath`)*.
   - **Valor inválido (NaN ou infinito).** No passo 6 de cada tick (depois de todos os sistemas e antes do pedido de fim), o `SimWorld` confere, por padrão de bits, se posição e HP das entidades **vivas** são finitos. Em modo estrito, lança exceção com tick e entidade (o sistema culpado só aparece se o host rodar a mesma checagem entre sistemas, opcional em modo estrito). Em modo não estrito, o caso é contado em `NonFiniteCount` e vai ao log (#5), e o jogo não cai. Uma entidade que morre no mesmo tick com posição inválida tem a posição regravada com a anterior, para que NaN nunca entre no hash. Se a entidade afetada for o **herói do jogador ou um chefe**, a fase termina como **tentativa falha sem derrota** (o mesmo caminho do app fechado pelo Android, #28: sem recompensa e sem contar como derrota), por decisão do autor em 2026-11-04. Quem é herói ou chefe é dito por uma marca `Essencial` no `SimWorld` (uma coluna de 1 bit, no hash), escrita por quem cria a entidade, como o parâmetro `essential` do `Spawn` (o #3 para o herói, o #7 para o chefe; ADR-0001, emenda 6); o #2 não adivinha. O fim é uma simulação *Encerrada* com motivo `FalhaInterna`, que não é vitória nem derrota, e o resultado vai ao #3 *(provisória)*. Nos demais casos, a entidade morre, sem XP nem loot. *(provisória, exceto a decisão do autor.)*

10. **Estado hasheado.** Entram: `CurrentTick`, `CombatTick` e `CombatHold` (Regra 15); o contador de ids; os 3 streams (estado e sequência); no `SimWorld`, id, vivo, facção, `Essencial`, HP e posição atual (como bits do float, com `-0` normalizado para `+0`); e o `Hash` de cada sistema, na ordem do compositor. Ficam de fora: posição anterior (derivada), `EventBuffer`, contadores de diagnóstico (`DroppedEvents`, `CommandsRejected`, `SpawnsRejected`, `NonFiniteCount`, `GolpesDescartados`, `GolpesLimitados`, `ModForaDeFaixa`, `CurasDescartadas`) e o snapshot (seu hash já está no cabeçalho do log). O algoritmo e a ordem de entrada são os da FS8. O `Hash` nunca é calculado dentro do `Tick`; o host pede `StateHash()`. Cadência: a cada 100 ticks nos testes (constante do teste); no jogo, só no fim da fase e sob demanda. O hash é por byte (FS8). O custo do hash é a medir no spike.

11. **Ritmo de tempo: ponte, câmera lenta, pausa e segundo plano.** A simulação **não tem relógio**. Quem acumula tempo real e decide quantos `Tick` chamar por frame é a ponte (Gameplay).
    - **Câmera lenta.** Se o atraso passar de `MaxTicksPerFrame` (inicial 4, a medir no aparelho), a ponte roda esse limite e **descarta** o excedente; o jogo desacelera e nunca pula. O limite vive só na ponte: é knob do próprio #2 (registro `max_ticks_per_frame`), não remoto, e **não passa pelo #1**. O teste sem tela não tem limite. A simulação **nunca muda o conteúdo da fase por desempenho** (por exemplo, menos inimigos): isso quebraria a promessa da Player Fantasy.
    - **Pausa e segundo plano (decisão do autor, 2026-11-04).** Ligação, app em segundo plano ou menu de pausa significam **zero chamadas de `Tick`**; ao voltar, o acumulador é zerado e o tempo ausente não vira ticks nem é recuperado. O primeiro `dt` depois da pausa também é descartado (a ponte o zera), porque ele embute o tempo ausente. **Retomada (decisão do autor, 2026-11-04):** ao voltar da pausa **com `CombatHold` = 0** (a ponte lê o valor por visão somente leitura, entre frames), a ponte só retoma os ticks no **primeiro toque no joystick**; até lá continua chamando zero `Tick`. **Com `CombatHold` ≠ 0** (oferta pendente ou aguardando retomada, Regra 15) **não há esse portão**: o combate já está congelado pela simulação e o `PickOffer` só age dentro de um `Tick`, então a ponte volta a chamar `Tick` na hora (sem isso, tocar na carta depois da pausa não faria nada). Enquanto o portão está fechado, `Esquivar`, `Suprema` e `PickOffer` tocados são **descartados** (coerente com "a pausa apaga a ação guardada"); o único toque que vale é o do joystick, que abre o portão *(decisão do autor, 2ª passada)*. Isso é decisão da ponte sobre quantos ticks chamar, fora da simulação e do hash. O aviso "toque para continuar" é do #12. O #3 decide *quando* pausar; o #2 só aceita "zero ticks". Se o Android matar o app durante a pausa, vale a regra do #28: tentativa falha sem derrota, e a fase não é retomável. Perda de foco sem pausa (notificação, janela flutuante) é tratada como pausa *(provisória; quais eventos o Android dispara é NOT SOURCEABLE em `docs/engine-reference/unity/`)*.
    - **Não são do #2:** o aviso visual de lentidão, qualidade gráfica adaptativa e a taxa de quadros alvo. Tudo isso é apresentação.

12. **Garantia de mesmo build.** Mesmo binário e mesma ABI, mesmo hash dos dados (#1), mesma seed e mesmos comandos por tick produzem o **mesmo hash em todo tick**. Não há garantia entre Editor e aparelho, entre ABIs diferentes de um mesmo APK, nem entre versões do app. O Editor (Mono, x64) **não prova** o aparelho até o spike de hash. Nada derivado de uma seed é recalculado depois de um update do app (se o resultado de um auto-battle for calculado de uma vez, o crédito é atômico e ele não é rederivado depois; o rendimento por hora do auto é decisão do #40). Todo log leva seed, hash dos dados, tag do build e ABI. O que vale ao vivo não é reproduzível pelo relógio de parede: a reprodução parte da sequência de comandos por tick.

13. **Fim da fase.** O #3 decide vitória ou derrota e pede o fim da fase pelo contexto do tick; a simulação vira *Encerrada* ao fim desse tick e o log recebe o hash final. Se vitória e derrota forem pedidas no mesmo tick (o chefe e o herói morrem no mesmo golpe), **a vitória vale** (decisão do autor, 2026-11-04); mas um valor inválido numa entidade `Essencial` no mesmo tick vence os dois (`FalhaInterna` > vitória > derrota, passo 6 da Regra 2, *provisória*: uma vitória vinda de estado corrompido não é mérito); a morte do herói fica registrada como fato no log, e o que ela implica para as métricas é do #3 (OQ-7). O **abandono pelo menu não passa por tick**: nenhum `Tick` roda para pedir o fim, então o host descarta a simulação (ver Estados). Em qualquer caso, depois do fim a `Simulation` inteira é descartada e o resultado vai ao #3. O pedido de fim do #3 também pode levar o motivo `FalhaInterna` com o detalhe `MissingBoss` (o chefe agendado nunca nasceu), e o próprio #2 encerra com `FalhaInterna` e o detalhe `EssentialSpawnRejected` quando um `Spawn` `Essencial` é rejeitado dentro do tick (o #3 traduz em `ChefeAusente`), com a mesma prioridade da Regra 2, passo 6 (ADR-0001, emenda 7; GDD #3, Regra 7) *(provisória)*. **Dado inválido não é pedido de fim**: o #3 valida os knobs no `Preparar`, por exceção (GDD #3, Regra 14). O pedido de fim em `SimContext`, com o motivo, está no ADR-0001 (emenda 7).

14. **Erros de contrato.** Três tipos. **Modo.** A instância recebe `estrito` no `Create` (Regra 1): é opção de instância, sem `#if` e sem `static`. Onde este GDD diz "em desenvolvimento", leia "em modo estrito"; onde diz "em release", leia "em modo não estrito". **Regra única de modo:** todo contador de diagnóstico (`CommandsRejected`, `SpawnsRejected`, `NonFiniteCount`, `DroppedEvents` e, do GDD #6, `GolpesDescartados`, `ModForaDeFaixa` e `CurasDescartadas`) **lança exceção no primeiro caso em modo estrito e só conta em modo não estrito**; `GolpesLimitados` (clamp de saneamento do #6) só conta, nos dois modos; a falha estrita lançada dentro do `Tick` leva a *Quebrada* (regra abaixo). Um script **sem erro** dá o mesmo hash nos dois modos; um script **com erro** só roda inteiro em modo não estrito, e lá o hash é o do script sem os comandos descartados. **Erro de comando** (comando para ator nunca emitido, comando duplicado ou com eixo inválido, comando fora de ordem): em modo estrito falha e, em modo não estrito, é descartado (fora de ordem é processado como veio, sem contador) e contado no log, o que é determinístico e não quebra a Regra 12. **Exceção:** `PickOffer` com serial errado, fora da faixa, fora de hora ou duplicado no mesmo tick é entrada normal do jogador (toque duplo) e é só descartado e contado (`CommandsRejected`, pelo #16), **sem falha nos dois modos**. **Erro do host** (`Tick` depois de Encerrada, `Tick` com buffer de eventos não drenado (conta como drenado depois que o host chama `DrainEvents()`; ADR-0001, emenda 2), `Tick` reentrante, leitura de `Events` ou `StateHash` durante o `Tick`): lança exceção **sempre**, nos dois modos; são bugs de quem integra, sem tolerância e sem contador *(provisória)*. **Bug interno** (estado impossível, índice fora da faixa, `w` negativo, `n ≤ 0` em FS5): lança exceção sempre; as checagens são explícitas no código, sem depender de `IndexOutOfRange` do runtime. **Regra do estado *Quebrada*:** qualquer exceção lançada **depois** que o `Tick` começou a mudar estado (do passo 2 da Regra 2 em diante) leva a simulação a *Quebrada*, inclusive `Tick` reentrante e leitura de `Events` ou `StateHash` durante o `Tick`; uma exceção lançada **antes** de qualquer mudança (argumento inválido, snapshot recusado) deixa a simulação intacta. *(provisória; exige os contadores `CommandsRejected`, `SpawnsRejected` e `NonFiniteCount`, além do `DroppedEvents` que o ADR já tem, e a opção `estrito`, no ADR, OQ-5.)*

15. **Escolha de carta, congelamento e retomada (decisões do autor, 2026-11-04).** No level-up, o combate **congela** enquanto o jogador escolhe, e **só volta quando o jogador toca o joystick** (retomada: o herói nunca volta sem controle, com a horda colada). O congelamento é **dentro da simulação**: enquanto o combate está retido, só o #3 e o #16 rodam e nenhum sistema de combate altera estado. O tick continua a contar, de modo que o jogo, o teste sem tela e o auto-battle seguem o mesmo caminho. **Fonte única:** o `SimWorld` tem um valor `CombatHold` (0 = livre, 1 = oferta pendente, 2 = aguardando retomada), escrito **só pelo #16** e incluído no hash (Regra 10). O #16 o põe em 1 ao abrir a oferta, em 2 quando o `PickOffer` válido a resolve e em 0 quando vê, no mesmo tick ou depois, um `Mover` do herói com módulo maior que zero (o toque é um comando comum, então é determinístico). **Toque novo (decisão do autor, 2ª passada):** o dedo que já estava no joystick quando a oferta abriu não retoma o combate. A **ponte** zera o `Mover` do herói (X = Y = 0) desde o frame que entrega o `PickOffer` até um novo início de toque (dedo levantado e apoiado de novo); a simulação continua só lendo comandos, então o determinismo não muda. O limiar de zona morta do `Mover` é do #4 (até lá, "módulo maior que zero" vale como módulo ao quadrado > 0). A **foto** `ctx.CombatActive` (Regra 2, passo 2) vale para o tick inteiro: uma mudança de `CombatHold` feita no meio do tick só vale a partir do tick seguinte. Os sistemas de combate não fazem nada quando `CombatActive` é falso, e isso não depende da ordem dos sistemas *(provisória; exige `CombatHold`, `ctx.CombatActive` e `CombatTick` no ADR, OQ-5)*. Para que o tempo congelado não vire waves atrasadas nem recargas vencidas, o #2 expõe um segundo contador, o `CombatTick`, que só avança nos ticks em que `CombatActive` é verdadeira: waves, recargas e duração da fase usam o `CombatTick`, e o `CurrentTick` serve ao log, ao número do evento e ao hash *(provisória; #3, #7 e #8 confirmam, OQ-10)*. A escolha entra como um comando `PickOffer` (serial da oferta e índice da carta, Regra 3; o conjunto de comandos de oferta, como reroll e favorecer, é do #9 e entra em `CommandKind` com a ordem entre eles e o `PickOffer` no mesmo tick definida lá). O #2 é dono do tipo de comando; o #16 implementa a oferta. Não há tempo-limite de escolha no MVP (OQ-6).

16. **Sem retomada nem snapshot do meio da fase.** O #2 não oferece serializar, retomar ou restaurar uma fase, porque o #28 proíbe guardar o estado de uma fase em andamento. A instância é criada por fase, nunca singleton, e `Forja.Simulation` não tem estado `static` mutável.

**Pressupostos sem fonte (NOT SOURCEABLE — não cobertos por `docs/engine-reference/unity/`), a verificar no spike e não afirmados como fato:** (a) a opção "No Engine References" do asmdef existe e falha a compilação ao usar `UnityEngine` no 6000.3.27f1, e vale para os dois asmdefs de simulação; (b) `ref struct` com `ReadOnlySpan` compila e roda em IL2CPP e em Mono; (c) `BitConverter.SingleToInt32Bits` existe nos dois runtimes (senão, plano B com struct de `FieldOffset`); (d) o IL2CPP não funde `a*b+c` de modo que mude o resultado entre execuções do mesmo build; (e) os callbacks de pausa e foco chegam na thread principal, entre frames, nunca no meio de um `Tick`; (f) qual propriedade de tempo da engine alimenta o acumulador sem saltos; (g) quais ABIs o APK leva (com mais de uma, o determinismo é separado por ABI).

### States and Transitions

A simulação tem poucos estados. **Pausa e segundo plano não são estados do #2**: a simulação não tem relógio, e pausar é a ponte não chamar `Tick`. Pôr a pausa dentro do #2 criaria estado que muda o hash conforme o tempo de parede e quebraria a Regra 12. O congelamento da escolha de carta (Regra 15) é estado do #16 (o `CombatHold`), não um estado do #2: para o #2, a simulação segue *Em execução*.

| Estado | Evento | Próximo estado |
|---|---|---|
| (nenhum) | Construir com snapshot válido | Criada |
| (nenhum) | Snapshot inválido | Não cria; o #1 bloqueia a entrada na fase |
| Criada | `Tick` | Em execução |
| Em execução | `Tick` | Em execução |
| Em execução | `Tick` em que o #3 pede o fim | Encerrada |
| Em execução | NaN ou infinito no herói ou num chefe (marca `Essencial`, Regra 9) | Encerrada com motivo `FalhaInterna` (tentativa falha, sem derrota) |
| Em execução | O #3 pede o fim com `FalhaInterna` (`MissingBoss`), ou um `Spawn` `Essencial` é rejeitado dentro do tick (`EssentialSpawnRejected`) | Encerrada com motivo `FalhaInterna` (tentativa falha, sem derrota) |
| Em execução | Ponte para de chamar `Tick` (pausa) | Em execução (nada muda) |
| Em execução | Um sistema lança exceção no meio do tick | Quebrada |
| Quebrada | `Tick`, `StateHash` | Exceção; a fase conta como tentativa falha, sem derrota e sem contar como morte de fase (GDD #3, Regra 8; contrato com o #28) |
| Em execução | Abandono pelo menu | Destruída (o host descarta a simulação e grava no log o `StateHash` marcado "abandonada") |
| Encerrada | `Tick` | Exceção sempre (erro do host, Regra 14) |
| Encerrada | `StateHash`, leitura de eventos | Encerrada |
| qualquer | Descartar | Destruída |

### Interactions with Other Systems

| Sistema | Natureza | Entra no #2 | Sai do #2 | Dono da interface |
|---|---|---|---|---|
| #1 Dados e balanceamento | Hard | Snapshot imutável da fase, já em ticks, mais as capacidades | Nada | O #1 é dono do snapshot; o #2 só lê e nunca converte segundos |
| #3 Fluxo de fase | Hard | Snapshot e comandos (é um `ISimSystem`); cria o herói no `Preparar` | Pedido de fim (vitória, derrota ou `FalhaInterna`) e resultado da fase | O #2 é dono do contrato e da ordem; o #3 é dono do resultado e da seed |
| #5 Log de eventos | Hard (aceite) | Nada | Eventos drenados após cada tick, `StateHash`, contadores | O #2 é dono do `SimEvent`; o #5 é dono do formato do log |
| #6 Combate, #7 Horda, #8 Skills | Hard | Snapshot, `SimWorld`, streams | Escritas no `SimWorld` e eventos | Cada GDD é dono do significado dos seus campos; o #2 é dono da ordem e dos streams; o `Spawn` do #7 sorteia por índice de wave |
| #9 Oferta de cartas e #16 Grimório | Hard | Comando `PickOffer`; sorteio do stream `Offer` | Eventos de oferta | O #16 implementa; o #2 é dono do tipo de comando |
| #4 Input e câmera | Soft | `Command[]` (pela ponte) | Visões somente leitura e eventos | O #4 é dono da tradução do toque em comando; a entrega única de ações (Regra 4) é da ponte |
| #13 IA e #40 Auto-battle | Soft (futuro) | O mesmo `Command[]` de um jogador | Os mesmos eventos | A política **não** consome os streams da simulação (deslocaria o `Spawn`); se precisar de sorteio, pede stream novo com id registrado. O #40 é dono da política |
| #28 Save local | Indireta, mediada pelo #3 e pelo host (não há dependência direta no índice) | Nada | Nada | O #2 só nasce depois da marca confirmada da fase e não guarda estado de fase em andamento (Regras 1 e 16) |

## Formulas

Nomeação: `FS1` a `FS9` são as fórmulas **do #2** (S de simulação), para não colidir com `F1` a `F6` do #1. Três fórmulas do #1 são usadas aqui **sem serem redefinidas**: `duracao_ticks` (F1, conversão de segundos em ticks), `taxa_por_tick` (F2) e `capacidade_ok` (F3). `FS1` e `FS2` rodam na ponte (Gameplay) e ficam **fora do hash e fora do determinismo**; `FS3` a `FS9` rodam dentro da simulação ou a definem. Toda constante de algoritmo público (SplitMix64, PCG32, FNV-1a) deve ser conferida contra a referência oficial no teste (AC-D2); nenhum vetor de teste numérico foi inventado aqui. Toda escolha de recomendação está marcada *(provisória)*.

### FS1. Ticks a executar no frame (ponte)

The ticks_por_frame formula is defined as:

`dt_ef = min(dt, (Max + 1) × TickSeconds)`
`n_devido = floor((acum + dt_ef) × 30)`
`n = min(n_devido, Max)`
`acum_novo = clamp((acum + dt_ef) − n_devido × TickSeconds, 0, TickSeconds)`

**Variables:**

| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| dt | float | ≥ 0; NaN, negativo ou infinito vira 0 | calculated (relógio da engine; qual propriedade usar é NOT SOURCEABLE) | segundos reais do frame |
| acum | float | [0, TickSeconds] | calculated | sobra do frame anterior; zerado na volta de uma pausa |
| Max (`MaxTicksPerFrame`) | int | 1 a 16 (teto provisório, evita estouro de `Max + 1`); inicial 4 | configuração da ponte (dono: o #2; não remoto; não passa pelo #1) | teto de ticks por frame |
| TickSeconds | float | 1f / 30f | constant (`SimClock`, ADR-0001) | duração de um tick |
| n | int | [0, Max] | calculated | quantos `Tick` chamar neste frame |
| acum_novo | float | [0, TickSeconds] | calculated | sobra, usada por FS2 |

**Output Range:** `n_devido − n` é o excedente descartado (câmera lenta) e vai para um contador da ponte. O tempo acima de `(Max + 1) × TickSeconds` num único frame (travão longo) é descartado sem contagem. `Max` fora de 1 a 16 (`Max < 1` congelaria o jogo) é recusado quando a ponte carrega a configuração, e não há tratamento em execução. O descarte da fração de tick é *(provisório)*.
**Example (Max = 4):** (a) `acum` 0,01 e `dt` 0,05: soma 0,06, × 30 = 1,8, então `n` = 1 e `acum_novo` = 0,06 − 0,033333 = **0,026667**. (b) `acum` 0,01 e `dt` 0,25: `dt_ef` = 5/30 = 0,166667, soma 0,176667, × 30 = 5,3, então `n_devido` = 5, `n` = **4**, 1 tick descartado e `acum_novo` = 0,01. (c) `acum` 0,01 e `dt` 0,005: soma 0,015, × 30 = 0,45, então `n` = **0** e `acum_novo` = 0,015.

### FS2. Fator de interpolação e posição desenhada (apresentação)

The alfa_interpolacao formula is defined as:

`alfa = clamp(acum_novo / TickSeconds, 0, 1)`
`pos_desenhada = prev + (atual − prev) × alfa`

**Variables:**

| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| acum_novo | float | [0, TickSeconds] | calculated (FS1) | sobra do frame |
| prev, atual | float (por eixo) | finito | calculated (`SimWorld`) | posição do tick anterior e do atual |
| alfa | float | [0, 1] | calculated | fração do tick já decorrida |
| pos_desenhada | float | de `prev` a `atual` | calculated | posição na tela |

**Output Range:** `alfa` NaN vira 0. Uma entidade recém-nascida tem `prev = atual`, então fica parada em `atual` com qualquer `alfa`. Quem teletransporta uma entidade (#6) deve igualar `prev` a `atual`, senão ela desliza pela tela. A tela mostra o estado com até 1 tick de atraso (cerca de 33 ms), inerente ao desenho.
**Example:** `prev` (2,0; 1,0) e `atual` (2,15; 1,0) (4,5 m/s ÷ 30 = 0,15 m/tick), com `acum_novo` = 0,8 × `TickSeconds` (≈ 0,026667, valor arredondado: o teste calcula `0,8f × TickSeconds` e não usa o literal): `alfa` = 0,8 e x = 2,0 + 0,15 × 0,8 = **2,12**, y = **1,0**.

### FS3. Semente do stream e gerador PCG32

The seed_do_stream formula is defined as:

`seed_s = Mix(seedMestre XOR id_s)`; gerador `Pcg32(seed_s, seq = id_s)`

`Mix(x)` é o SplitMix64, tudo módulo 2^64 e em `unchecked`:
1. `z = x + 0x9E3779B97F4A7C15`
2. `z = (z ^ (z >> 30)) × 0xBF58476D1CE4E5B9`
3. `z = (z ^ (z >> 27)) × 0x94D049BB133111EB`
4. `Mix = z ^ (z >> 31)`

PCG32 (XSH-RR 64/32). **Init:** `state = 0`; `inc = (seq << 1) | 1`; um passo; `state += seed_s`; um passo. **Passo:** `state = state × 6364136223846793005 + inc` (hexadecimal 0x5851F42D4C957F2D). **Saída** (usa `old` = o estado antes do passo): `xs = (uint)(((old >> 18) ^ old) >> 27)`; `rot = (int)(old >> 59)`; `out = (xs >> rot) | (xs << ((−rot) & 31))`.

**Variables:**

| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| seedMestre | ulong | 0 a 2^64 − 1 (o 0 vale) | data file (entregue pelo #3 via host) | seed da fase |
| id_s | ulong | {0 `Spawn`, 1 `Offer`, 2 `Loot`} | constant (`RngStream`) | id e sequência do stream |
| inc | ulong | sempre ímpar | calculated | incremento do PCG32 |
| state | ulong | 0 a 2^64 − 1 | calculated | estado do gerador (entra no hash) |
| out | uint | 0 a 2^32 − 1 | calculated | saída do `NextUInt` |

**Output Range:** não há entrada inválida, `Mix` é uma bijeção e cada stream tem período 2^64. A seed 0 não degenera, porque o `Mix` a espalha. Mestres diferentes não colidem: o `seed_s` pode coincidir entre (mestre 0, `Offer`) e (mestre 1, `Spawn`), que dão a mesma entrada 1 ao `Mix`, mas o `inc` difere (3 contra 1), e o par (`seed_s`, `inc`) é único por (mestre, stream), porque o `inc` fixa o stream e o `Mix` é bijeção. Criar um stream novo exige um novo id fixo e uma entrada no registro (ADR-0001).
**Example:** os ids 0, 1 e 2 dão `inc` = 1, 3 e 5. Com `seedMestre` = 12, as entradas do `Mix` são 12, 13 e 14 (12 XOR 0, 12 XOR 1 e 12 XOR 2 = 14).

### FS4. Float em [0, 1)

The float01 formula is defined as:

`f = (float)(out >> 8) × (1f / 16777216f)`

**Variables:**

| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| out | uint | 0 a 2^32 − 1 | calculated (FS3) | saída bruta |
| k = out >> 8 | uint | 0 a 16.777.215 | calculated | 24 bits altos |
| f | float | [0, 1 − 2^−24] | calculated | resultado |

**Output Range:** o 1 nunca sai; o 0 pode sair, então quem usa `log` ou divide por `f` deve proteger. O passo é 2^−24 (cerca de 5,96e−8). Todo `k` de 24 bits cabe exato em float e multiplicar por uma potência de 2 é exato. *(Provisória)* Chance de loot ou de oferta é decidida com inteiro (`NextInt(10000) < chance`), porque `0,1f` não é exato.
**Example:** `out` = 0x80000000 → `k` = 8.388.608 → **0,5**. `out` = 0xFFFFFFFF → `k` = 16.777.215 → **0,99999994**. `out` = 0xFF → `k` = 0 → **0**.

### FS5. Inteiro limitado, sem viés (rejeição)

The int_limitado formula is defined as:

`t = (uint)(0u − n) % n` (que é 2^32 mod n); sortear `r` (FS3) até `r ≥ t`; resultado = `r % n`

**Variables:**

| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| n | int | 1 a 2^31 − 1 (n ≤ 0 é bug interno e lança exceção) | calculated | limite exclusivo |
| t | uint | 0 a n − 1 | calculated | limite de rejeição |
| r | uint | 0 a 2^32 − 1 | calculated | saída de FS3 |
| resultado | int | 0 a n − 1 | calculated | sorteio sem viés |

**Em C#:** `uint un = (uint)n; uint t = unchecked(0u - un) % un;` — com `n` do tipo `int`, a conta `0u − n` viraria `long` e, em contexto `checked`, lançaria exceção. **Output Range:** aceitos = 2^32 − t, que é múltiplo de `n`, então não há viés de módulo. O número esperado de sorteios é 2^32 / (2^32 − t), menor que 2 para todo `n ≤ 2^31 − 1`. *(Provisória)* `n = 1` também consome um sorteio, para que a sequência não dependa dos dados.
**Example:** `n` = 6: 2^32 = 4.294.967.296 = 6 × 715.827.882 + 4, então `t` = **4** e a chance de rejeição é 4 / 2^32 ≈ 9,3e−10. `n` = 10: `t` = **6**.

### FS6. Sorteio do Spawn por índice de wave

The seed_da_wave formula is defined as:

`base = Mix(seedMestre XOR 0)` (a `seed_s` do `Spawn`, de FS3); `seed_w = Mix(base XOR (ulong)w)`; gerador da wave `Pcg32(seed_w, seq = w)`

**Variables:**

| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| w | int | 0 a 2^31 − 1 | data file (índice da wave no cronograma da fase, #7) | índice da wave |
| base | ulong | 0 a 2^64 − 1 | calculated | `seed_s` do stream `Spawn` |
| seed_w | ulong | 0 a 2^64 − 1 | calculated | semente do gerador desta wave |

**Output Range:** `w` negativo é bug interno. Duas waves nunca partilham gerador, e o stream `Spawn` vira só a raiz de derivação. A derivação é *(provisória)*.
**O que o #7 precisa obedecer:** sortear só do gerador da wave, nunca do `Spawn` bruto; a composição de uma wave depende só de (`seedMestre`, `w`, dados), nunca de abates, vivos, HP, posição ou tick; o número de sorteios da wave depende só de (`seedMestre`, `w`, dados) (a rejeição da FS5 pode consumir sorteios extras, mas de modo determinístico); o #7 sorteia toda a composição no `Preparar`, antes do tick 1 (Regra 6 do #7), então nenhum gerador de wave atravessa ticks nem entra no `Hash` (o `Hash` do #7 leva só os cursores); como esse uso é fora do `Tick`, `RngWave(w)` precisa existir no `Preparar` *(Emenda 16 do ADR-0001, ainda `Proposed`)*; o índice segue o cronograma, não a ordem de abate. **Composição × posição** *(emenda (a) do #7, 2026-11-05)*: o sorteio decide só o arquétipo e o índice de direção (a composição); a posição final de nascimento é função pura do índice de direção sorteado, da posição do herói no fim do tick anterior e da arena, calculada no tick do nascimento e **sem sorteio** (F4 do #7).
**Example:** `w` = 0 → `inc` = 1. `w` = 3 → entrada `base XOR 3` e `inc` = 7. O tick e os abates não entram em nenhum passo.

### FS7. Módulo do eixo do joystick

The eixo_limitado formula is defined as:

`m2 = X² + Y²`; se `m2 > 1`: `(X, Y) ← (X, Y) × (1 / SimMath.Sqrt(m2))`; senão mantém

**Variables:**

| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| X, Y | float | finito (Regra 3) e \|·\| ≤ `EixoMax` | data file (comando do #4) | eixo do joystick |
| EixoMax | float | inicial 1 | constant *(provisória; a medir com o #4)* | teto por componente aceito |
| m2 | float | 0 a 2 × `EixoMax`² | calculated | módulo ao quadrado |

**Output Range:** módulo ≤ 1 mais erro de arredondamento de float (alguns ulp); o #6 não pode assumir "≤ 1" estrito. O ponto (0, 0) fica (0, 0) e a divisão só ocorre com `m2 > 1`, então nunca divide por zero. NaN e infinito já foram descartados na Regra 3. Sem o teto `EixoMax`, componentes acima de cerca de 1,8e19 estouram `m2` para infinito e o vetor vira zero.
**Example:** (1, 1) → `m2` = 2 → fator 0,70710678 → **(0,70710678; 0,70710678)**. (0,3; 0,4) → `m2` = 0,25 → **fica igual**.

### FS8. Combinação do hash do estado

The hash_estado formula is defined as:

`h0 = 0xCBF29CE484222325`; para cada byte `b`: `h = (h XOR b) × 0x100000001B3` (FNV-1a de 64 bits)

**Variables:**

| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| b | byte | 0 a 255 | calculated | byte do campo, em ordem little-endian explícita (por deslocamento) |
| bits do float | uint | −0 (0x80000000) vira 0 | calculated | float lido pelos bits (pressuposto (c) da Regra 16) |
| h | ulong | 0 a 2^64 − 1 | calculated | hash acumulado |

**Ordem de entrada:** `CurrentTick`; `CombatTick`; `CombatHold`; contador de ids; para cada stream, `state` e `inc`; cada id emitido em ordem crescente (id, vivo como 1 byte, facção, `Essencial` como 1 byte, HP, x, y); depois, para cada sistema na ordem do compositor, um marcador (o índice) e o seu `Hash`. Seções de tamanho variável levam o tamanho na frente.
**Fica de fora:** posição anterior, `EventBuffer`, contadores de diagnóstico, snapshot, capacidades, relógio e frame, `GetHashCode` de objeto, bytes de preenchimento de struct (campo a campo, nunca memória bruta) e a ordem de `Dictionary`.
**Output Range:** qualquer `ulong`. NaN não pode chegar aqui (Regra 9).
**Example:** `1,0f` → bits 0x3F800000 → bytes **00 00 80 3F**. `−0,0f` → 0x80000000 → normalizado para **0x00000000**. O hash é **por byte** *(provisória)*; a variante por palavra de 32 bits foi descartada por YAGNI, porque mudaria todos os goldens e o hash do jogo só roda no fim da fase. O custo é a medir no spike. As constantes do FNV-1a foram conferidas por script em 2026-11-04 e continuam no AC-D2.

### FS9. Capacidade de ids da fase

The capacidade_ids_ok formula é a `capacidade_ok` do #1 (F3), com `pico := total_spawns`:

`spawns_de_dados = Σ spawns(w) + máx_invocações`
`total_spawns = ids_de_preparacao + spawns_de_dados`
`capacidade_ids_ok = (total_spawns × (100 + margem_pct) ≤ cap_ids × 100) ∧ (cap_ids ≤ teto)`

**Variables:**

| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| total_spawns | int | ≥ 1 | soma de `ids_de_preparacao` (código: o #3 declara 1, o herói) e de `spawns_de_dados` | todos os ids que a fase vai emitir |
| spawns_de_dados | int | ≥ 0 | data file (os spawns das waves vêm do #7 e as invocações do #8; vai no snapshot, ADR-0002) | a parte de dados do total |
| cap_ids | int | ≥ 1 | data file (por fase) | linhas do `SimWorld` |
| margem_pct | int | segura 10 a 50, padrão 25 | data file (`capacity_margin_pct`, do #1) | folga sobre a estimativa |
| teto | int | definido pelo spike de performance | data file (do #1, não remoto) | limite do aparelho de referência |

**Tipos:** a conta roda em `long` (`total_spawns × (100 + margem_pct)` estoura `int` acima de cerca de 14,3 milhões, e `Σ spawns(w)` também). **O que conta como spawn:** todo id emitido por `SimWorld.Spawn`; se projéteis ou gemas forem entidades, entram no total (decisão dos #6, #7 e #8, a confirmar nos GDDs deles; decidido no #6, 2026-11-05: projétil e orbe de XP não são entidades do `SimWorld`, e o pool de projéteis, se houver, é do #8). **Diferença de significado:** o "pico" do #1 mede os vivos ao mesmo tempo e dimensiona a lista de vivos. O `total_spawns` mede **todos** os ids da fase, porque ids não se reutilizam (Regra 8). Uma fase pode ter pico 300 e total 900. Se uma invocação não tem teto estático, o #7 ou o #8 declara o máximo possível; sem isso vale a saída da Regra 8 (novo ADR).
**Quem confere o quê** *(provisória, a reavaliar; ADR-0001, item 6; GDD #1, F3)*: **no build**, o `DataValidator` do #1 confere `spawns_de_dados` contra `cap_ids`; **no jogo, antes do `Create`**, o compositor soma `ids_de_preparacao` e refaz a conta completa em `long`; se não couber, a fase não começa (`FalhaInterna(DadosInvalidos)`, montada pelo #3). O `Create` e o Core não fazem esta conferência.
**Example (números ilustrativos, não são dado de balanceamento):** `total_spawns` = 900 e margem 25: 900 × 125 = 112.500 ≤ `cap_ids` × 100 exige `cap_ids` ≥ 1125. Com `cap_ids` = 1100: 110.000 < 112.500 → **recusado**; com 1125 → **OK**. Usar o pico 300 aceitaria `cap_ids` = 400 (37.500 ≤ 40.000), e a fase terminaria com `Spawn` devolvendo −1. Na fronteira: com `spawns_de_dados` = 899 e `ids_de_preparacao` = 1, `cap_ids` = 1124 passa a conferência do build e é recusado pelo compositor (900 × 125 = 112.500 > 112.400).

**Não é fórmula do #2:** a relação entre ticks e duração da fase não vira fórmula. O `EventBuffer` é drenado a cada tick, então seu tamanho depende do pico de eventos por tick (F3 do #1), não da duração. Uma fase de 5 minutos tem 9.000 ticks (F1 do #1); o `CurrentTick` em `int32` dura cerca de 2,27 anos de jogo contínuo, e por isso **não há regra de limite** (cortada na revisão de 2026-11-04). Duas lacunas ficam com outros donos: `SimMath.RoundToInt` e `FloorToInt` (regra do meio e checagem de faixa) pedem uma linha no ADR ou em `SimMath`, e o sorteio ponderado por pesos inteiros (soma dos pesos mais `NextInt(soma)`) é do #9, apoiado em FS5.

## Edge Cases

Formato: **If** condição, resultado. Itens marcados *(provisória)* são escolha de recomendação, a reavaliar com o jogo avançado. **Contrato pendente** aponta o GDD de outro sistema que ainda precisa confirmar a resolução; **OQ-n** remete a Open Questions.

### Tempo, congelamento e oferta de carta

- **If há oferta pendente (Regra 15) por centenas de ticks e um sistema usa `CurrentTick` como relógio**: ele vê o tempo "pulado" e solta waves atrasadas de uma vez, com recargas já vencidas. Por isso waves, recargas e duração da fase usam o `CombatTick`, que só avança quando o combate roda. *(provisória; contrato pendente: #3, #7, #8; OQ-10)*
- **If o #3 pede o fim da fase no mesmo tick em que o #16 abriria uma oferta**: o #16 não abre a oferta, porque a simulação vira *Encerrada* e um `PickOffer` depois disso seria `Tick` pós-Encerrada. *(provisória; contrato pendente: #3, #16)*
- **If um tick gera dois level-ups**: as ofertas entram numa fila, e a segunda só é sorteada depois do `PickOffer` da primeira, porque o conteúdo depende da carta escolhida. *(provisória; contrato pendente: #16, #9; OQ-11)*
- **If o herói morre durante a oferta pendente**: não pode acontecer, porque os sistemas de combate estão parados. Se algum dano ainda ocorrer, é bug do #6.
- **If o `PickOffer` tem serial diferente do da oferta pendente, índice fora da faixa, não há oferta pendente, ou chega no tick em que a oferta nasce**: é descartado e contado em `CommandsRejected`, não consome sorteio do stream `Offer` e **não** falha em modo estrito (toque duplo é normal). Dois `PickOffer` no mesmo tick: vale o primeiro. Um toque na carta chega uma única vez (Regra 4), então ele não escolhe também a carta da segunda oferta da fila: o serial dela é outro.
- **If `Mover` ou `Esquivar` chegam durante o congelamento**: passam na validação, os sistemas de combate os ignoram (a foto `CombatActive` é falsa) e eles não entram em `CommandsRejected`. `Esquivar` não é guardado. A única exceção é o `Mover` com módulo maior que zero do herói quando `CombatHold` = 2: o #16 o lê e libera o combate (Regra 15, retomada).
- **If o Android mata o app com oferta pendente ou em pausa**: tentativa falha, sem derrota e sem retomada (contrato com o #28).

### Ponte, dt e pausa

- **If o frame de tela roda 0 ticks e o jogador toca `Esquivar`**: a ponte segura a ação até o próximo `Tick` executado (Regra 4).
- **If `dt` é NaN, negativo ou infinito**: vira 0 (FS1). **If `dt` é finito e gigante**: `dt_ef` o limita e o excedente é descartado sem contagem. Nenhum dos dois afeta o hash.
- **If o primeiro `dt` depois de uma pausa é enorme**: a ponte o descarta e zera `acum` (Regra 11); a FS1 sozinha ainda rodaria `Max` ticks.
- **If `Max` muda entre frames**: é lido a cada frame e só muda quantos ticks rodam, nunca o estado. Um `Max` fora de 1 a 16 já foi recusado na carga da configuração da ponte (FS1). *(provisória)*
- **If a pausa chega com `acum` diferente de zero**: `acum` é zerado e a fração (até 33 ms) se perde. Isso é aceito.
- **If o jogador pausa com `CombatHold` ≠ 0 (oferta pendente ou aguardando retomada) e volta**: não há portão de toque no joystick; a ponte volta a chamar `Tick` na hora, o `PickOffer` tocado vale e o combate segue parado até a retomada da Regra 15. Com `CombatHold` = 0, o portão vale e ações tocadas antes do toque no joystick são descartadas (Regra 11).
- **If o dedo já estava no joystick quando a oferta abriu e o jogador escolhe a carta**: a ponte zera o `Mover` do herói até um novo início de toque, então o combate não retoma sozinho (Regra 15).
- **If um callback de pausa chega dentro do laço de n ticks**: o pressuposto (e) da Regra 16 falhou. A ponte confere a bandeira de pausa só entre frames, então o laço termina. Se o spike mostrar que o pressuposto é falso, vira pergunta aberta.

### Comandos e vida

- **If o comando é para um ator morto**: descartado e contado, sem falha (Regra 3). Só ator nunca emitido falha, e só em modo estrito.
- **If o ator estava vivo na validação e morre no mesmo tick antes de o sistema ler o comando**: o sistema o ignora e não conta.
- **If há dois `Mover` do mesmo ator com X e Y diferentes**: vale o primeiro na ordem entregue e o outro é contado; em modo estrito a duplicata é erro de quem chama (Regra 14).
- **If há 0 comandos**: o joystick está solto (X = Y = 0). Se há inércia, é decisão do #6 (decidido no #6: sem inércia, velocidade direta; provisória).
- **If a política do auto-battle ou do teste sem tela emite comando inválido** (NaN, ator inexistente): em modo estrito o teste falha com tick e ator no erro; em modo não estrito o comando é descartado e contado.
- **If duas mortes miram o mesmo alvo no tick**: só quem zerou o HP emite `Death`; dano e cura posteriores em morto são descartados, e morto não reanima (Regra 7).
- **If o HP chega a 0 ou menos**: o HP é gravado como exatamente 0 (sem sobra negativa no hash) e o `Death` sai na mesma escrita. "Vivo com HP 0" no fim do tick é bug interno. *(contrato pendente: #6)*
- **If uma entidade nasce e morre no mesmo tick**: o evento `Spawn` vem antes do `Death`, e a apresentação não pode supor que a viu em algum frame. *(contrato pendente: #12)*
- **If uma invocação nasce de um invocador que morreu antes no mesmo tick**: pergunta aberta para o #8 (OQ-8).
- **If HP ou posição vira NaN em modo não estrito** (em modo estrito lança, Regra 9): a entidade morre, `NonFiniteCount` sobe, a posição é regravada com a anterior e o HP com 0 (senão os bits do NaN entrariam no hash e na interpolação). O `Death` sai com motivo "inválido", sem XP nem loot. **Exceção (decisão do autor):** se for o herói do jogador ou um chefe, a fase termina como tentativa falha sem derrota, nunca como derrota. *(provisória nos demais casos; contrato pendente: #6, #3)*

### Capacidade e eventos

- **If `SimWorld.Spawn` devolve −1**: o #7 sorteia a composição inteira da wave **antes** de chamar `Spawn`, para que a falta de espaço não desloque os sorteios. Spawn essencial (herói, chefe) rejeitado é bug interno e a fase falha. *(provisória; contrato pendente: #7)*
- **If o `EventBuffer` enche no tick em que o herói morre ou a fase termina**: o estado não muda, e a reserva de posições (Regra 6) garante que o evento crítico chegue ao log.
- **If o host chama `Tick` sem ter drenado um buffer que não está vazio**: lança exceção sempre, nos dois modos (erro do host, Regra 14).
- **If `Events` é lido antes do tick 1**: vem vazio. **If é lido depois de *Encerrada***: vem o último tick, intacto. **If é lido durante o `Tick`**: exceção sempre.
- **If a lista de vivos e o total de spawns divergem do declarado**: vale a Regra 8 (`SpawnsRejected`); a validação do #1 e a conferência do compositor (FS9) deveriam ter recusado a fase antes.

### Ciclo de vida

- **If `Tick` é chamado depois de *Encerrada***: lança exceção sempre, nos dois modos (erro do host, Regra 14). `CurrentTick` e o hash não mudam.
- **If `Tick` é chamado de dentro de um `Tick`**: exceção sempre, por uma bandeira `emTick`.
- **If um sistema lança exceção no meio do tick**: o estado fica pela metade, a simulação vira *Quebrada* e todo `Tick` e `StateHash` seguinte lança. A fase conta como tentativa falha, sem derrota e sem contar como morte de fase (GDD #3, Regra 8). *(contrato pendente: #28)*
- **If o jogador abandona pelo menu de pausa**: nenhum `Tick` roda para o #3 pedir o fim, então o host descarta a `Simulation` (estado *Destruída*) e grava no log o `StateHash` marcado "abandonada". *(provisória; contrato pendente: #3; OQ-12)*
- **If vitória e derrota são pedidas no mesmo tick** (o chefe e o herói morrem no mesmo golpe): *a vitória vale* (decisão do autor, 2026-11-04), para não criar a sensação de trapaça no momento do selamento; a morte do herói fica registrada como fato no log, e o que ela implica para as métricas é do #3 (OQ-7).
- **If a fase dura 1 tick**: o `Tick` roda, o #3 pede o fim e o hash final é o de `CurrentTick` = 1, com eventos de `Tick` = 1. **If durasse 0 ticks**: o #1 recusa a fase (`duracao_ticks ≥ 1`).
- **If `StateHash` é pedido durante o `Tick`**: exceção. **If é pedido antes do tick 1**: vale, com `CurrentTick` = 0. **If há 0 entidades vivas**: vale, porque as seções de tamanho variável levam o tamanho (0) na frente.

### Streams e seeds

- **If `seedMestre` é 0 ou 2^64 − 1**: ambos valem e entram nos vetores de teste (AC-D2). O 0 não degenera por causa do `Mix`.
- **If `w` é negativo**: o cast `(ulong)w` viraria um número enorme em silêncio, então o #2 lança exceção de bug interno. **If `w` = 2^31 − 1**: vale.
- **If dois índices `w` iguais aparecem no cronograma da fase**: as duas waves teriam composição idêntica. A validação do #1 e o #7 devem exigir `w` único. *(contrato pendente: #1, #7; OQ-9)*
- **If uma wave sorteia mais ou menos vezes que o previsto**: só a própria wave muda, porque cada uma tem gerador próprio. A composição de toda wave é sorteada no `Preparar` (Regra 6 do #7), então uma wave que nunca começa (fase encerrada antes) tem a composição sorteada assim mesmo, e isso não muda a das outras *(emenda (b) do #7, 2026-11-05)*.
- **If um sistema sorteia do stream errado**: o teste de independência (AC-I2) roda a mesma seed com N sorteios extras no stream X e exige `state` e `inc` iguais nos outros. O `Spawn` bruto fica no estado inicial em todo tick, porque é só raiz de derivação.
- **If dois `ISimSystem` escrevem o mesmo campo no mesmo tick**: em atribuição (posição, facção) vence o último na ordem do compositor; em acumulação (HP) os efeitos se somam na ordem. A tabela da Regra 5 passa a listar **um dono por campo**. *(provisória; contrato pendente: #6, #7, #8)*

### Builds, updates e dados

- **If dois logs têm ABI, tag de build ou hash dos dados diferentes**: a ferramenta de comparação responde "não comparável", nunca "divergência". *(contrato pendente: #5)*
- **If a ordem dos sistemas muda entre versões**: o hash muda (o marcador de índice entra na FS8), e isso é esperado. O cabeçalho do log leva a lista de ids dos sistemas na ordem do compositor.
- **If o app é atualizado no meio de uma campanha**: nada derivado de seed é recalculado. Uma seed guardada, reexecutada com o build novo, gera outra fase, o que é permitido (Player Fantasy). O crédito do auto-battle é atômico com a marca da seed. *(contrato pendente: #28, #3)*
- **If o hash do snapshot recebido é diferente do hash registrado no cabeçalho do log**: o `Simulation.Create` lança exceção (erro de quem chama) e a fase não começa. *(contrato pendente: #1)*
- **If o Editor (Mono, x64) e o aparelho (IL2CPP, ARM64) dão hashes diferentes para a mesma seed**: não é bug, porque a garantia vale só no mesmo build (Regra 12). Isso só reabre o ADR se a divergência ocorrer dentro do mesmo build.

## Dependencies

### Upstream (o #2 depende de)

| Sistema | Natureza | O que o #2 lê | Observação |
|---|---|---|---|
| #1 Dados e balanceamento | **Hard** | O snapshot imutável da fase, já em ticks (F1 do #1); as capacidades de entidades, eventos e pools (F3 do #1); as waves como listas ordenadas por índice; `capacity_margin_pct` e os tetos | Sem snapshot válido a fase não começa e o #2 não é criado (Regra 1). O #1 já lista o #2 como dependente (Hard) |

**Decisões externas que o #2 respeita:** o ADR-0001 (*Proposed*: float32, 30 Hz, PCG32 em streams, `Tick` + buffer de eventos, `SimWorld`, três asmdefs) e o conceito congelado (`game-concept.md` L246, L323, L326, L349 e L400). O ADR precisa ser *Accepted* antes de qualquer story do #2. Sem ciclo: o #2 não referencia nenhum sistema de regra, porque os sistemas dependem de Core e não o contrário.

### Downstream (dependem do #2)

Nenhum destes GDDs existe ainda; **todo contrato abaixo é provisório** até o GDD dono confirmá-lo. A coluna "No índice" diz se `systems-index.md` já lista o #2 na coluna Depends On do sistema.

| Sistema | Natureza | O que flui | No índice |
|---|---|---|---|
| #3 Fluxo de fase | **Hard** | É um `ISimSystem`; cria o herói no `Preparar` (antes do tick 0); entrega o `seedMestre` (via host) e pede o fim da fase (vitória, derrota ou `FalhaInterna`); decide a pausa | sim |
| #5 Log de eventos | **Hard** (aceite) | Eventos drenados após cada tick, `StateHash`, contadores | sim |
| #6 Combate e dano | **Hard** | `ISimSystem`; escreve HP e posição no `SimWorld`; emite `Death` | sim |
| #7 Horda, waves e inimigos | **Hard** | `ISimSystem`; implementa `IPreparaFase` e sorteia toda a composição no `Preparar`, depois do #3, por índice de wave (FS6); declara o total de spawns (FS9) | sim |
| #8 Skills e evoluções | **Hard** | `ISimSystem` na ordem do compositor; comunica-se pelo `SimWorld` | sim (acrescentado em 2026-11-04) |
| #9 Oferta de cartas | **Hard** | Usa o stream `Offer` e o comando `PickOffer` | sim |
| #16 Grimório | **Hard** | `ISimSystem` de oferta, registro e substituição, o mesmo código no jogo e no teste sem tela | sim (acrescentado em 2026-11-04) |
| #4 Input e câmera de combate | **Soft** | Produz o `Command[]`; lê visões somente leitura e eventos | sim (acrescentado em 2026-11-04) |
| #12 Feedback de combate, VFX e HUD | **Soft** | Lê eventos e visões; nunca escreve no estado | sim (acrescentado em 2026-11-04) |
| #13 IA de herói e companheiro | **Hard** (Vertical Slice) | Entrega o mesmo `Command[]` de um jogador, sem consumir os streams | sim |
| #22 Ranking | **Hard** (Alpha) | **Replay validado por servidor não é atendido** pelo ADR-0001; exige ADR de substituição por ponto fixo | sim |
| #29 Serviços online | **Hard** (Alpha) | Mesma limitação do #22 para qualquer validação cruzada entre aparelhos | sim |
| #35 Coop PvE de 4 | **Hard** (Full Vision) | Autoridade de host e rede: fora da garantia do ADR | sim |
| #40 Auto-battle com IA | **Hard** (Full Vision) | A mesma simulação, com comandos de uma política; se o resultado for creditado de uma vez, o crédito é atômico; nunca é rederivado da seed depois de um update | sim |
| #28 Save local | Indireta | Contrato de ciclo de vida mediado pelo #3 e pelo host (Regras 1 e 16) | não se aplica |

### Bidirecionalidade e ajustes pendentes em outros documentos

- **`systems-index.md`:** acrescentar o #2 à coluna Depends On de #4, #8, #12 e #16 (dependências implícitas acima). *(feito em 2026-11-04, com a aprovação do autor)*
- **#1 Dados e balanceamento (já existe):** o #1 já cita o #2 como dependente. Dois pontos: a F3 foi ajustada em 2026-11-04 para validar a tabela de ids contra o *total de spawns* da fase (Regra 8, FS9, OQ-1, resolvida); resta o cronograma de waves exigir `w` único (OQ-9).
- **#28 Save local (já existe):** não cita o #2 e não precisa, porque a dependência é mediada pelo #3. O #3 deve declarar o contrato da marca da fase (Regra 1) e o descarte da simulação no abandono (OQ-12).
- **Cada GDD ainda por escrever** (#5, #8, #9, #16; o #3, o #6 e o #7 já existem e citam o #2) deve citar o #2 nas suas Dependencies, com a mesma natureza (Hard ou Soft) desta tabela.

## Tuning Knobs

Os knobs de **dados** moram no #1 (que guarda o valor, a unidade e a faixa segura) e o significado é do GDD dono; aqui estão os que o #2 define e os do #1 que ele consome. Nenhum é remoto: valores que mexem em determinismo ou em desempenho de aparelho não podem mudar por pacote remoto. **Todo valor "a medir" depende do spike de performance e do aparelho de referência, que ainda não foi verificado**, e por isso não recebe número aqui.

| Knob | Padrão | Faixa segura | Remoto | Afeta | Baixo demais | Alto demais |
|---|---|---|---|---|---|---|
| `MaxTicksPerFrame` (FS1) | 4 *(provisório; a medir no aparelho)* | 1 a 16 (teto provisório); recusado na carga se fora | não (dono: o #2, knob da ponte; não passa pelo #1) | quanto o jogo desacelera num engasgo antes de descartar tempo | desacelera cedo demais: a câmera lenta aparece mesmo em engasgos curtos | um engasgo vira uma rajada de ticks que estica o frame seguinte; em aparelho fraco o risco real é térmico (o custo do tick sobe com o calor) |

**Knobs do #1 que o #2 consome (sem duplicar):** `capacity_margin_pct` (25; 10 a 50), `capacity_ceiling` por tipo de capacidade (a medir no spike), as capacidades por fase de entidades, eventos e pools (F3 do #1) e `phase_snapshot_memory_kb`. O #2 só acrescenta uma exigência: a capacidade de ids é validada contra o **total de spawns** da fase (FS9, OQ-1).

**Constantes deliberadas (não são knobs):** `TICKS_PER_S` = 30 e `TickSeconds` = 1f / 30f (ADR-0001; mudar é um novo ADR); as constantes do SplitMix64, do PCG32 e do FNV-1a; os ids de stream 0, 1 e 2 (`Spawn`, `Offer`, `Loot`); a política de NaN da Regra 9; a ordem dos sistemas (Regra 5, regra de balanceamento, não botão). **Constantes provisórias:** `EixoMax` = 1 (a medir com o #4, spike); `EventosReservados` de 8 a 16 posições (Regra 6, sem spike); a cadência do hash (a cada 100 ticks nos testes; no jogo, só no fim da fase e sob demanda) e o hash por byte (FS8). Os três últimos eram knobs no rascunho e foram cortados em 2026-11-04 para reduzir o escopo do MVP.

**Interações entre knobs:**
- `MaxTicksPerFrame` × `TickSeconds`: o tempo máximo simulado por frame é `MaxTicksPerFrame × TickSeconds` (4 × 33 ms = cerca de 133 ms com o valor provisório); acima disso o jogo desacelera. Com o teto, não há espiral infinita de lentidão: o excedente é descartado, a câmera lenta é estável e se recupera sozinha. O que degrada antes é o fps (o jogo fica injogável muito antes de a câmera lenta aparecer), e por isso o spike mede fps e ticks descartados, não só o tempo do `Tick` (P5).
- `EventosReservados` × capacidade de eventos do #1: a reserva sai da capacidade, então a capacidade útil para eventos comuns é a diferença. Com a reserva em 8 a 16 posições, o efeito é pequeno.
- **Este knob não muda o estado de uma fase válida.** `MaxTicksPerFrame` só muda a ponte e a observação; a reserva e a capacidade mudam o que é descartado ou recusado, não o que a simulação calcula.

## Visual/Audio Requirements

Nenhum requisito visual ou sonoro **próprio**: o #2 é um sistema Core sem superfície que o jogador veja ou ouça, e por isso não gera especificação de ativos (`/asset-spec` não se aplica). Os eventos do buffer (`Damage`, `Death`, `Spawn`, `SkillCast` e os demais tipos que cada GDD dono definir) são o **gatilho** de VFX e SFX, cuja especificação pertence ao #12 e ao #31. O que o #2 garante a quem desenha e toca: a ordem dos eventos é a de emissão (Regra 6); os eventos são entregues depois de cada tick, sem perda silenciosa (Regra 6); uma entidade que nasce e morre no mesmo tick tem os dois eventos, `Spawn` antes de `Death`, e a apresentação não pode supor que a viu em algum frame (Edge Cases); o estado desenhado atrasa até 1 tick (cerca de 33 ms) em relação à simulação, por causa da interpolação (FS2).

## Game Feel

O #2 não tem alvos de feel próprios, mas **impõe a granularidade** que todo tempo de feel herda. Todos os valores abaixo são estimativas de projeto derivadas das regras e **ainda não foram medidas no aparelho** (a medir no spike).

| Aspecto | O que o #2 impõe | Dono do alvo |
|---|---|---|
| Granularidade de tempo | 1 tick = cerca de 33 ms. Janelas de esquiva, telegraph e i-frames são múltiplos de 33 ms, no mínimo 1 tick (F1 do #1) | #6 e #12 |
| Latência de entrada (e janela de esquiva: o #6 deve fixá-la em **pelo menos 5 ticks contando o jitter de ±1**, 2ª passada) | Um comando age no primeiro tick executado depois da amostragem do toque e o resultado é mostrado com até 1 tick de atraso: **até cerca de 2 ticks (≈ 67 ms) mais um frame de tela**, sem contar a latência do aparelho | #4 define o alvo; medir no aparelho |
| Engasgo | O jogo desacelera e nunca pula (Regra 11); a lentidão é visível, não oculta | #12 (aviso, se houver) |
| Escolha de carta e retomada | O combate congela (Regra 15): nenhuma pressão de tempo enquanto o jogador decide, e só volta num toque novo no joystick (Regra 15); a volta de uma pausa com combate livre segue o mesmo portão (Regra 11). O aviso "toque para continuar" não é do #2 | #9, #16 e #12 |
| Ritmo dos perigos | Estável entre tentativas: o mesmo golpe dura o mesmo número de ticks (a esquiva é uma habilidade que se aprende, Player Fantasy) | #6 e #7 |

## UI Requirements

Nenhum. O #2 não tem tela, menu nem HUD. Os contadores de diagnóstico vão ao log (#5), e qualquer painel de depuração é do #5 ou do #12. **Não há UX flag** para este sistema.

## Cross-References

| Este documento | Referencia | Documento e item | Natureza |
|---|---|---|---|
| Regra 1, FS3 | Conversão de segundos em ticks (`duracao_ticks`) e taxas por tick (`taxa_por_tick`) | `dados-e-balanceamento.md`, F1 e F2 (registro: `duracao_ticks`, `taxa_por_tick`) | Usadas, **não redefinidas** |
| Regra 8, FS9 | `capacidade_ok`, `capacity_margin_pct`, `capacity_ceiling` | `dados-e-balanceamento.md`, F3 e Tuning Knobs (registro: `capacidade_ok`) | Reaproveitada com `pico := total_spawns`; diferença de significado em OQ-1 |
| Regra 1 | O snapshot da fase é imutável e validado antes do tick 0 | `dados-e-balanceamento.md`, Detailed Design, item 7 (Entrega) | Contrato de entrada |
| Regra 11, Tuning Knobs | `MaxTicksPerFrame` como knob da ponte, não remoto | nenhuma: o dono é o próprio #2 (registro `max_ticks_per_frame`); o #1 **não** guarda este knob | Corrigido em 2026-11-04 (o rascunho dizia que o valor morava no #1) |
| Regras 1, 11 e 16 | A simulação só nasce depois da marca confirmada da fase; não guarda estado de fase em andamento; app fechado conta como tentativa falha | `save-local.md`, regra 3 (o que nunca entra) e a marca de fase em andamento (regra 6) | Contrato mediado pelo #3 e pelo host |
| Overview, Regras 2 a 16, FS1 a FS9 | Float32, 30 Hz, PCG32 em 3 streams, `Tick` + buffer de eventos, `SimWorld`, três asmdefs | `docs/architecture/adr-0001-simulacao-deterministica-float32-tick-30hz.md` (*Proposed*) | Decisão técnica que o GDD respeita; ajustes pedidos em OQ-5 |
| Overview, Player Fantasy | Simulação por seed, comparação Tank × DPS, headless, auto-battle, sem replay no MVP | `game-concept.md` L246, L323, L326, L349 e L400 | Origem dos requisitos |
| Dependencies | #5, #8, #9, #16 ainda sem GDD (o #3, o #6 e o #7 já existem) | `systems-index.md` | Contratos provisórios até cada GDD existir |
| Contratos | `sim_commands`, `sim_events`, `entity_table` | `docs/registry/architecture.yaml` | Registro de arquitetura (ADR-0001) |

## Acceptance Criteria

**Estado hoje.** Não existe código de simulação (`Assets/` só tem o modelo inicial do Unity), o doc de aceite do MVP (`docs/acceptance/mvp.md`) não existe e o ADR-0001 está *Proposed*. Por isso nenhum critério tem PASS ou FAIL ainda: **PRONTO** significa que o teste roda em EditMode assim que a story existir; **BLOCKED** conta como **não aprovado** e diz o que o desbloqueia.

**Convenções.** Os IDs são escopados por GDD: cite como "#2 AC-I2" (o #1 também tem AC-I1 a AC-I5). Salvo indicação, o tipo é Logic e o nível é BLOCKING (padrão do projeto), e o teste fica em `Assets/Tests/EditMode/Simulation/[Classe]Tests.cs`, com método `Cenario_Esperado`. FS1 e FS2 vivem na ponte (Gameplay) e devem ser função pura, sem `Time.deltaTime`, para rodar em EditMode. Todo teste afirma `testcasecount > 0`, porque um asmdef não compilado dá "0 tests, Passed" (AC-A2). Prefixos: **D** determinismo, RNG, hash e aritmética; **C** contrato de comandos, eventos e ciclo; **T** tempo e ponte; **I** independência e integração; **E** bordas; **A** arquitetura; **P** desempenho.

### Determinismo (AC-D)

| ID | Ref. | Critério | Status |
|---|---|---|---|
| D1a | R12 | **GIVEN** a mesma seed e o mesmo script de comandos, com sistemas-fixture que usam os 3 streams e o `SimWorld`, **WHEN** rodam 2 execuções na mesma sessão por pelo menos uma fase completa (≥ 9.000 ticks), **THEN** o `StateHash` é igual a cada 100 ticks. Controle negativo: mudar 1 comando ou a seed faz o hash divergir (o teste só vale se foi visto falhar). | PRONTO |
| D1b | R12 | Igual a D1a, com o compositor real. | BLOCKED: faltam #3, #6, #7 e o ADR *Accepted* |
| D2 | FS3, FS4, FS8 | **GIVEN** os vetores oficiais de referência, **WHEN** rodam o `Mix` (SplitMix64), o `Pcg32(initstate, initseq)` direto, sem `Mix`, e o FNV-1a 64, **THEN** as saídas batem, incluindo `seedMestre` 0 e 2^64 − 1. Vetores reproduzidos por script independente em 2026-11-04 (a conferir uma vez na fonte oficial ao commitar o teste): PCG32 `(42, 54)` começa com `a15c02b7 7b47f409 ba1d3330`; FNV-1a de `""` é `cbf29ce484222325`, de `"a"` é `af63dc4c8601ec8c` e de `"foobar"` é `85944171f73967e8`; `Mix(0)` = `e220a8397b1dcdaf` (regressão, não prova). Os valores de `Mix(12)` só podem ser gerados pelo próprio código (regressão, não prova). | PRONTO |
| D3 | FS3, R1 | **GIVEN** `seedMestre` = 12, **WHEN** os 3 streams nascem, **THEN** `inc` = 1, 3 e 5 (sempre ímpar) e as entradas do `Mix` são 12, 13 e 14. | PRONTO |
| D4 | FS4 | **GIVEN** `out` = `0x80000000`, `0xFFFFFFFF` e `0xFF`, **WHEN** converte para float, **THEN** o resultado é 0,5, 0,99999994 (menor que 1) e 0, por igualdade exata (as três saídas são exatas em float32). | PRONTO |
| D5 | FS5 | **GIVEN** `n` = 6 e `n` = 10, **WHEN** calcula o limite, **THEN** `t` = 4 e `t` = 6. Com gerador injetado que devolve r = 3 e depois 7 (n = 6), o resultado é 1 e foram consumidos 2 sorteios. `n` = 1 consome 1 sorteio. `n ≤ 0` lança exceção. | PRONTO |
| D6a | FS6 | **GIVEN** `w` = 0 e `w` = 3, **WHEN** deriva o gerador, **THEN** `inc` = 1 e `inc` = 7. `w` negativo lança exceção; `w` = 2^31 − 1 vale. Sorteios extras na wave A não mudam a wave B. | PRONTO |
| D6b | FS6 | **GIVEN** a mesma (seed, `w`, dados), **WHEN** a composição da wave é sorteada no `Preparar` com logs de comandos e abates diferentes, **THEN** a composição é igual (ela nunca lê abates, vivos, HP, posição nem tick). | BLOCKED: falta a implementação do #7 (o GDD existe) |
| D7 | FS8, R10 | **GIVEN** os campos hasheados, **WHEN** o hash é calculado, **THEN** os bytes de `1,0f` são `00 00 80 3F`; `−0f` gera o mesmo hash que `+0f`; mudar cada campo hasheado muda o hash; mudar posição anterior, `EventBuffer`, capacidades ou qualquer contador de diagnóstico da Regra 10 não muda; `CombatHold` e `Essencial` entram no hash; zero vivos é válido; `([A],[B,C])` difere de `([A,B],[C])` (prefixo de tamanho). | PRONTO |
| D8 | R12 | **GIVEN** um golden guardado **por runtime** (Editor-Mono-x64 e Android-ARM64; o Windows IL2CPP entra só se houver build Windows, *provisória*) em arquivo que nenhum teste escreve, **WHEN** a mesma seed roda, **THEN** o hash é igual ao golden do runtime atual. Golden ausente para o runtime atual **reprova** (nunca se auto-cria). O golden do Editor nunca vale para o aparelho. | Editor: PRONTO depois de D1a. Aparelho: BLOCKED (P7) |
| D9a | R9 | **GIVEN** um inimigo comum e entradas inválidas (NaN, +Infinity e −Infinity), **WHEN** a aritmética roda, **THEN** `Sqrt(−1)` = 0; empate de alvo vai ao menor id; em modo estrito o valor inválido lança com tick e entidade; em modo não estrito `NonFiniteCount` = 1, o inimigo morre com a posição anterior e o HP 0, sem XP nem loot. | PRONTO |
| D9b | R9 | **GIVEN** uma entidade com a marca `Essencial` (herói ou chefe, posta pelo fixture que a cria) e valor inválido em modo não estrito, **WHEN** o tick termina (passo 6), **THEN** a simulação fica *Encerrada* com motivo `FalhaInterna` (nem vitória nem derrota) e o resultado chega ao fixture do #3. **Caso simultâneo:** se no mesmo tick o fixture do #3 pediu vitória (ou derrota), o pedido é ignorado e o motivo final é `FalhaInterna`; um valor inválido em entidade comum, ou em entidade morta no mesmo tick, não aciona `FalhaInterna` e nunca deixa NaN no hash. | PRONTO (com fixture; o #3 real é BLOCKED) |
| D9c | R9 | **GIVEN** `RoundToInt` e `FloorToInt`, **WHEN** recebem 2,5, −2,5, −0,5, NaN, infinito e um valor fora da faixa do `int`, **THEN** `RoundToInt(2,5)` = 3, `RoundToInt(−2,5)` = −3, `FloorToInt(−0,5)` = −1, e NaN, infinito e fora da faixa lançam exceção de bug interno. | PRONTO |
| D9d | R9 | Banir `double` e `Mathf` por análise estática. | BLOCKED: analisador (OQ-7 do #1) |
| D10 | FS7 | **GIVEN** os eixos (1, 1) e (0,3; 0,4), **WHEN** o módulo é limitado, **THEN** saem (0,70710678; 0,70710678) e (0,3; 0,4). (0, 0) fica (0, 0) sem dividir. Tolerância de 1e−6 por componente (a FS7 admite alguns ulp). Eixo com \|X\| acima de `EixoMax` é descartado e contado antes da conta. | PRONTO |

### Contrato de comandos, eventos e ciclo (AC-C)

| ID | Ref. | Critério | Status |
|---|---|---|---|
| C1 | R1 | **GIVEN** uma `Simulation` criada por `Simulation.Create` com snapshot-fixture, **WHEN** nenhum `Tick` foi chamado, **THEN** `CurrentTick` = 0, `CombatTick` = 0, os eventos estão vazios e `StateHash` é igual entre duas `Simulation` idênticas, diferente com seed diferente e igual ao golden do tick 0. Snapshot inválido faz o `Create` lançar `SnapshotInvalido`; cabeçalho com 1 bit trocado faz lançar `SnapshotHashMismatch`; em ambos a `Simulation` não existe (o teste afirma o tipo da exceção, não só que lançou). | PRONTO |
| C2 | R2 | **GIVEN** um sistema-fixture, **WHEN** roda no 1º tick, **THEN** vê `CurrentTick` já +1, buffer vazio e prev = atual em entidades nascidas no tick; os eventos do 1º tick têm `Tick` = 1. | PRONTO |
| C3 | R3 | **GIVEN** comandos inválidos, **WHEN** entram no `Tick`, **THEN** ator nunca emitido lança em modo estrito e é contado em modo não estrito; ator morto é contado, sem falha; dois do mesmo tipo e ator: vale o 1º; `Mover` + `Esquivar` do mesmo ator: ambos valem; NaN, infinito ou \|X\| acima de `EixoMax` é descartado e contado; em modo não estrito, comandos fora de ordem são processados como vieram (sem contador); em modo estrito lançam. | PRONTO |
| C4 | R4 | **GIVEN** um comando entregue no tick N, **WHEN** o tick N + 1 roda sem comandos, **THEN** o comando não age no N + 1. | PRONTO |
| C5 | R5 | **GIVEN** sistemas-fixture, **WHEN** rodam, **THEN** a ordem é a do compositor; trocar a ordem muda o hash; cada sistema só escreve no `SimWorld`. | PRONTO |
| C6 | R6 | **GIVEN** o buffer cheio, **WHEN** novos eventos chegam, **THEN** ficam os mais antigos, `DroppedEvents` é cumulativo e a reserva guarda o `Death` do herói e o início do telegraph de elite e de chefe. Em modo não estrito, com buffer de K posições e um tick que emite K + 3 eventos comuns, `DroppedEvents` = 3, e mais 2 no tick seguinte dá 5; em modo estrito o primeiro descarte lança. O **hash é o mesmo** com buffer pequeno e com buffer grande (modo não estrito). | PRONTO |
| C7 | R7 | **GIVEN** duas mortes no mesmo alvo no tick, **WHEN** os sistemas rodam, **THEN** `Death` sai 1 vez; um alvo nascido no tick é atingível no mesmo tick; dano em morto é descartado; ids não se reutilizam. | PRONTO |
| C8 | R8 | **GIVEN** a capacidade de ids esgotada, **WHEN** `Spawn` é chamado, **THEN** devolve −1, o contador de ids não anda e `SpawnsRejected` sobe em modo não estrito (em modo estrito lança); a lista de vivos fica em ordem de id. Teste do laço (Regra 7): um sistema-fixture que faz `Spawn` e mata uma entidade durante o passe visita cada vivo uma vez, sem pular nenhum, e o recém-nascido só age no sistema seguinte. | PRONTO |
| C9 | R13 | **GIVEN** um pedido de fim no tick N, **WHEN** o tick termina, **THEN** a simulação está *Encerrada* e o hash final está disponível. | PRONTO |
| C10 | R14 | **GIVEN** um erro de comando (ator inexistente, duplicata, eixo inválido, fora de ordem), **WHEN** ocorre, **THEN** (a) um script **sem erro** dá o mesmo hash nos dois modos; (b) em modo estrito o primeiro erro lança; (c) em modo não estrito ator inexistente, duplicata e eixo inválido são descartados e o hash é o do script sem esses comandos, com `CommandsRejected` igual ao número injetado; (d) comando fora de ordem é processado como veio, e o hash é o da sequência recebida, sem contador. Um erro do host (`Tick` após Encerrada, buffer não drenado, `Tick` reentrante) lança nos dois modos. Um bug interno sempre lança e leva a *Quebrada* (se depois do passo 2 do tick) ou deixa a simulação intacta (se antes). | PRONTO |
| C11 | R15 | **GIVEN** um fixture na posição 1 da ordem que põe `CombatHold` = 1 no tick N, **WHEN** os ticks rodam, **THEN** no tick N os sistemas de combate ainda rodam e `CombatTick` sobe (a foto `CombatActive` era verdadeira); do tick N + 1 em diante nenhum sistema de combate muda estado, `CurrentTick` sobe e `CombatTick` não; um fixture que põe `CombatHold` = 2 e depois recebe um `Mover` com módulo > 0 do herói o libera, e o combate volta no tick seguinte; o resultado é o mesmo com o fixture em qualquer posição da ordem. | PRONTO (fixture); integração com o #16 real: BLOCKED |
| C12 | R16 | **GIVEN** `Forja.Simulation`, **WHEN** inspecionado por reflexão, **THEN** não tem campo `static` mutável; duas `Simulation` no mesmo processo dão o mesmo hash que isoladas. | PRONTO |
| C13 | FS9 | **GIVEN** `spawns_de_dados` = 899, `ids_de_preparacao` = 1 e margem 25, **WHEN** a capacidade é conferida, **THEN** `cap_ids` = 1100 é recusada no build; 1124 passa no build e é recusada pelo compositor; 1125 é aceita nas duas; usar o pico (300) aceitaria 400, que é o erro que a FS9 evita. | A função pura: PRONTO se vive no #1. O cruzamento com o total real do #7 e a conferência do compositor: BLOCKED |

### Tempo e ponte (AC-T)

| ID | Ref. | Critério | Status |
|---|---|---|---|
| T1 | FS1 | **GIVEN** `Max` = 4, **WHEN** (a) `acum` 0,01 e `dt` 0,05, **THEN** `n` = 1 e `acum_novo` = 0,026667; (b) `acum` 0,01 e `dt` 0,25, **THEN** `n` = 4, 1 tick descartado e `acum_novo` = 0,01; (c) `acum` 0,01 e `dt` 0,005, **THEN** `n` = 0 e `acum_novo` = 0,015; (d) `acum` 0 e `dt` = `TickSeconds` exato, **THEN** `n` = 1 (a conta de float no limite deve ser conferida; se der 0, a FS1 passa a acumular em ticks inteiros). `dt` NaN, negativo ou infinito vira 0. Tolerância 1e−6. | PRONTO |
| T2 | FS2 | **GIVEN** `prev` (2,0; 1,0), `atual` (2,15; 1,0) e `acum_novo` = `0,8f × TickSeconds` (calculado no teste; o literal 0,026667 daria `alfa` 0,80001 e erro de 1,5e−6), **WHEN** desenha, **THEN** `alfa` = 0,8 e a posição é (2,12; 1,0), com tolerância de 1e−6. `alfa` NaN vira 0; recém-nascido fica parado. | PRONTO |
| T3a | R4 | **GIVEN** um frame de 3 ticks, **WHEN** a ponte entrega comandos, **THEN** `Mover` vai nos 3 ticks. | PRONTO |
| T3b | R4 | **GIVEN** um frame de 3 ticks com um toque de `Esquivar` e um de `Suprema`, **THEN** cada um vai 1 vez, no 1º tick. | PRONTO |
| T3c | R4, R15 | **GIVEN** um frame de 3 ticks com um toque de carta, **THEN** o `PickOffer` aparece 1 vez, no 1º tick, e não nos outros dois; um frame de 0 ticks o segura até o próximo `Tick` executado. | PRONTO |
| T3d | R4, R11 | **GIVEN** uma ação guardada por um frame de 0 ticks, **WHEN** chega uma pausa, **THEN** a ação guardada é apagada. | PRONTO |
| T3e | R11, R15 | **GIVEN** `CombatHold` = 1 (oferta pendente) e uma pausa, **WHEN** o jogador volta e toca só na carta, **THEN** a ponte volta a chamar `Tick` sem exigir toque no joystick e o `PickOffer` chega ao 1º `Tick` do frame (≤ 1 frame depois do toque); o mesmo com `CombatHold` = 2, em que o combate segue parado até o `Mover` de um toque novo. Com `CombatHold` = 0, `Esquivar`, `Suprema` e `PickOffer` tocados antes do toque no joystick são descartados, e o toque no joystick abre o portão. | PRONTO |
| T3f | R15 | **GIVEN** o `Mover` do herói já ativo (dedo no joystick) quando a oferta abre, **WHEN** o `PickOffer` válido é entregue, **THEN** a ponte entrega `Mover` zerado até um novo início de toque, `CombatHold` fica em 2 e o combate só volta com o toque novo (nunca 1→2→0 no mesmo tick por causa do dedo antigo). Um `Mover` com módulo 0 (zona morta) não libera. | PRONTO |
| T4 | R11 | **GIVEN** duas execuções, uma com pausa simulada de 10 minutos e outra sem, **WHEN** terminam, **THEN** o hash é igual; na pausa há 0 chamadas de `Tick`, `acum` é zerado e o 1º `dt` depois é descartado. | PRONTO |
| T5 | Knobs | **GIVEN** uma execução, **WHEN** `MaxTicksPerFrame` muda entre frames, **THEN** o hash não muda. | PRONTO |
| T6 | R16(e) | **GIVEN** o app no aparelho, **WHEN** chega um callback de pausa ou foco, **THEN** ele chega na thread principal, entre frames, nunca no meio de um `Tick`. | BLOCKED: verificar no aparelho (NOT SOURCEABLE) |

### Independência e integração (AC-I)

| ID | Critério | Tipo | Status |
|---|---|---|---|
| I2 | **GIVEN** a mesma seed, **WHEN** N sorteios extras saem do stream X, **THEN** `state` e `inc` dos outros dois ficam iguais, e o `Spawn` bruto fica no estado inicial em todo tick. | Logic | PRONTO |
| I3 | **GIVEN** um snapshot inválido, ou com hash diferente do cabeçalho do log, **WHEN** `Simulation.Create` é chamado, **THEN** lança e a simulação não existe. Complementa o AC-I1 do #1. | Integration | Com snapshot-fixture: PRONTO. Com o #1 real: BLOCKED |
| I4 | **GIVEN** um `ISimSystem` que pede o fim, **WHEN** o tick termina, **THEN** vale C9 e o resultado chega ao #3. | Integration | BLOCKED: falta o #3 |
| I5 | **GIVEN** o host drenando após cada tick, **WHEN** o frame roda 3 ticks, **THEN** o #5 recebe 3 lotes com `Tick` crescente, sem perda. | Integration | Com log-fixture: PRONTO. Com o #5: BLOCKED |
| I6 | **GIVEN** uma oferta nascida do level-up, **WHEN** o jogador escolhe, **THEN** o #16 sorteia do stream `Offer`, um `PickOffer` válido a resolve e o resultado é igual no jogo e no teste sem tela. | Integration | BLOCKED: faltam #16 e #9 |
| I7 | **GIVEN** a política do auto-battle, **WHEN** joga uma fase, **THEN** ela não consome nenhum dos 3 streams. | Integration | BLOCKED: falta o #40 |

### Bordas (AC-E)

| ID | Critério | Status |
|---|---|---|
| E1 | **GIVEN** a simulação *Encerrada*, **WHEN** chega um `Tick`, **THEN** lança exceção nos dois modos (estrito e não estrito), e `CurrentTick` e o hash ficam intactos. | PRONTO |
| E2 | **GIVEN** um sistema que lança no meio do tick, **WHEN** o tick seguinte ou o `StateHash` é chamado, **THEN** lançam, e a fase conta como tentativa falha, sem derrota e sem contar como morte de fase. | PRONTO |
| E3 | **GIVEN** um `Tick` chamado de dentro de um `Tick`, ou `Events` e `StateHash` lidos durante o `Tick`, **THEN** exceção sempre e simulação *Quebrada*. | PRONTO |
| E4 | **GIVEN** um buffer não drenado, **WHEN** o `Tick` é chamado, **THEN** lança exceção nos dois modos (erro do host). | PRONTO |
| E5 | **GIVEN** um `PickOffer` com serial diferente do da oferta pendente, fora da faixa, sem oferta pendente ou no tick em que a oferta nasce, **WHEN** entra, **THEN** é descartado e contado pelo #16 em `CommandsRejected` (= N descartados), **sem falha nos dois modos** e sem consumir o stream `Offer` (o `state` dele fica igual ao de antes); dois no mesmo tick (mesmo serial): vale o 1º e o outro é contado, também sem falha. | PRONTO se `PickOffer` existir como tipo. Fila de 2 level-ups: BLOCKED (#16, OQ-11) |
| E6 | **GIVEN** uma fase de 1 tick, **WHEN** o #3 pede o fim no 1º `Tick`, **THEN** o hash final é o de `CurrentTick` = 1, com eventos de `Tick` = 1. (O limite do `int32` não tem critério: a regra foi cortada em 2026-11-04.) | PRONTO |
| E7 | **GIVEN** vitória e derrota pedidas no mesmo tick, **THEN** a vitória vale e a morte do herói fica registrada no log. | BLOCKED: falta o #3 (OQ-7) |

### Arquitetura e desempenho (AC-A, AC-P)

| ID | Critério | Status |
|---|---|---|
| A1 | `Forja.Simulation` não referencia `UnityEngine` (idealmente erro de compilação). | BLOCKED: verificar a opção "No Engine References" no 6000.3.27f1 (NOT SOURCEABLE). Enquanto isso, Config/Data, ADVISORY: um teste lê o `.asmdef` e confere `noEngineReferences` |
| A2 | O CI lê o XML do NUnit e exige `testcasecount > 0` e as classes esperadas presentes. | PRONTO (passo de CI) |
| P1 | p95 do custo do `Tick` ≤ X1 ms na "fase mais pesada", com X1 gravado em `docs/acceptance/mvp.md` **antes** do build de aceite, em ≥ 20 execuções, e X1 menor que 33,3 ms com folga para o resto do frame. | SPEC INCOMPLETO (conta como BLOCKED): falta X1; vem da conta "orçamento do frame menos p95 do resto do frame" no spike |
| P2 | Zero alocação gerenciada por `Tick`: Profiler (GC Alloc) no aparelho, build Release/IL2CPP, após aquecimento, ≥ 1 fase completa. Contar alocação em EditMode é NOT SOURCEABLE e, mesmo existindo, Mono não prova IL2CPP; pode servir de alarme ADVISORY. | BLOCKED: aparelho de referência |
| P3 | Memória do `SimWorld` e do buffer ≤ X3 KB na "fase mais pesada", com X3 gravado antes do build de aceite. | SPEC INCOMPLETO (conta como BLOCKED): falta X3 |
| P4 | A "fase mais pesada" roda com N entidades vivas (N nomeado no `mvp.md`) sustentando 30 ticks por segundo, com **zero ticks descartados** (contador da ponte, FS1) durante a fase inteira. | SPEC INCOMPLETO (conta como BLOCKED): falta N e o aparelho de referência |
| P5 | Valor final de `MaxTicksPerFrame` (1 a 16): escolhido pela medição de fps e de ticks descartados, com um engasgo provocado de 100 ms e outro de 300 ms; a câmera lenta aparece só nesses engasgos (liga-se ao PT2). | SPEC INCOMPLETO (conta como BLOCKED): falta o aparelho de referência |
| P6 | Capacidade do buffer de eventos cobre o pior tick medido (morte em massa) sem `DroppedEvents`; custo do hash do fim da fase ≤ X6 ms. | SPEC INCOMPLETO (conta como BLOCKED): falta o pior tick medido e X6 |
| P7 | Hash nos 2 runtimes (Editor-Mono-x64 e Android-ARM64) em Release; o Windows IL2CPP só se houver build Windows *(corte de escopo da 2ª passada, provisório)*. O objetivo é **registrar os goldens** (D8), não exigir igualdade entre eles, porque a garantia é só no mesmo build (R12). | BLOCKED: spike de hash, aparelho de referência não verificado, ADR *Proposed* |

**Protocolo que o `docs/acceptance/mvp.md` deve fixar para P1 a P6** (copiando o AC-P1 do #1): aparelho de referência verificado; a "fase mais pesada" nomeada por ID; ≥ 20 execuções por métrica, com aquecimento descartado; temperatura inicial e modo de energia registrados; máximo, mediana e p95 reportados; orçamento commitado **antes** do build de aceite. O spike mede, em Release/IL2CPP no aparelho (nunca no Editor): o frame que roda `Tick`, o que não roda e o pior frame (4 ticks); o custo do `Tick` por sistema e a curva para 100, 300 e 600 entidades (linear ou quadrática); um soak térmico de uma fase inteira (5 min); e o contador de ticks descartados da FS1, que na "fase mais pesada" deve ser zero.

### Só playtest humano

- **PT1 (autor, Player Fantasy):** depois de uma derrota, "perdi por causa da build ou da minha mão" sai com naturalidade e "o jogo me roubou" não aparece. Não há métrica automática; evidência: nota do autor em `production/qa/evidence/`.
- **PT2 (aparelho):** a câmera lenta aparece só em engasgos reais e o ritmo da esquiva é aprendível (liga-se a P5).

**Lacunas conhecidas, parametrizadas até o spike:** `EixoMax` é "a medir com o #4" e `EventosReservados` é constante provisória de 8 a 16; os testes usam o valor como parâmetro e não o fixam. P1 a P6 continuam sem PASS possível até o spike dar os limites X1, X3, X6 e N (SPEC INCOMPLETO).

## Open Questions

Ainda não há calendário de produção com datas; o "prazo" de cada pergunta é um **marco**. Toda regra marcada *(provisória)* neste GDD deve ser reavaliada junto com a OQ-13.

| ID | Pergunta | Dono | Marco |
|---|---|---|---|
| OQ-1 | **Resolvida em 2026-11-04** (`/consistency-check`, autorizada pelo autor): a F3 do #1 agora valida a tabela de ids contra o total de spawns e a lista de vivos contra o pico; resta ao #7 declarar os dois números. Pergunta original: a F3 do #1 valida a capacidade contra o *pico* de entidades declarado pelo #7, mas a Regra 8 exige cobrir o *total de spawns* da fase (ids sem reuso). O #1 e o #7 passam a declarar e validar o total (FS9)? Ou o espaço é reciclado, o que exige novo ADR? | #1 e #7 | Antes do GDD #7 |
| OQ-2 | **Resolvida em 2026-11-04 (GDD #3, Regra 10):** seed nova a cada tentativa (decisão do autor); a comparação Tank × DPS usa um override de teste. Pergunta original: o retry usa seed nova ou a mesma? | #3 | GDD #3 |
| OQ-3 | **Resolvida em 2026-11-04 (GDD #3, Regra 3.4; provisória):** o #3 cria o herói no `Preparar`, chamado pelo compositor depois do `Create` e antes do 1º `Tick`. Pergunta original: quem cria o herói e as entidades iniciais, e quando (antes do tick 0 pelo host, ou no 1º tick pelo #3)? | #3 | GDD #3 |
| OQ-4 | **Resolvida em 2026-11-05 no GDD #6:** o #6 move o herói e todos os inimigos e é o único escritor de posição e HP. Pergunta original: Quem move o herói e os inimigos na ordem da Regra 5 (#6 ou #7)? | #6 e #7 | GDD #6 e #7 |
| OQ-5 | **Resolvida em 2026-11-05 no ADR-0001 (emendas 1 a 16 e a matriz da seção Emendas); falta só a aceitação do ADR (`accept ADR-0001`).** Pergunta original: ajustes no ADR-0001 antes de aceitá-lo: pedido de fim em `SimContext`; contadores `CommandsRejected`, `SpawnsRejected` e `NonFiniteCount` (o `DroppedEvents` já existe); `Create` estático **sem campo `static` mutável**; a configuração do IL2CPP na tag do build; **`Simulation.Create(snapshot, cabeçalhoDoLog, seedMestre, sistemas, estrito)` no lugar do construtor**; `Command` com `ArgA` e `ArgB` e `PickOffer` em `CommandKind`; `CombatHold` no `SimWorld`, `ctx.CombatActive` e `CombatTick`; a coluna `Essencial` e o motivo de fim `FalhaInterna`; `RngWave(w)` (a FS6 exige um gerador por wave: no ADR-0001, Emendas 11 e 16, em `SimWorld` e disponível no `Preparar`); `SimWorld.Spawn` devolvendo −1 quando cheio, id = índice com capacidade igual ao total de spawns e lista de vivos; `EventosReservados` como constante; estados *Quebrada* e *Destruída*; `SimMath.RoundToInt` (meio para longe de zero) e `FloorToInt` com checagem de faixa; hash por byte; o asmdef do compositor também com "No Engine References"; **acrescentado pelo GDD #3 (2026-11-04):** a ficha de fase (escalares escritos só pelo #3, no `SimWorld`), as interfaces opcionais `IPreparaFase` e `IConcluiFase` chamadas pelo compositor, a escrita da marca `Essencial` no `Preparar` (fora do `Tick`) com `Spawn` sem evento, a coluna `xpDaMorte` e a lista de mortos do tick, e o motivo `FalhaInterna` (`MissingBoss`, e `EssentialSpawnRejected` gerado pelo próprio #2) no pedido de fim do `SimContext`. | Autor, via `/architecture-decision` | Antes de `accept ADR-0001` |
| OQ-6 | Existe tempo-limite para escolher a carta? (Nenhum no MVP.) **A retomada foi decidida em 2026-11-04:** o combate volta no primeiro toque no joystick (Regras 11 e 15); a invulnerabilidade curta foi recusada. Resta ao #12 o aviso "toque para continuar" e ao #9 e ao #16 o fluxo de oferta. | #3, #9 e #12 | GDD #9 |
| OQ-7 | **Resolvida em 2026-11-04 (GDD #3, Regra 8; provisória):** a vitória não conta como morte de fase, e o resultado leva `MorteSimultanea`. Pergunta original: vitória e derrota pedidas no mesmo tick: a vitória vale (decisão do autor). Falta o #3 definir o que a morte simultânea implica para as métricas (por exemplo, se conta para o limite de mortes do Tank até o selo). | #3 | GDD #3 |
| OQ-8 | Uma invocação nasce se o invocador morreu antes, no mesmo tick? | #8 | GDD #8 |
| OQ-9 | **Resolvida do lado do #7 em 2026-11-05 (GDD #7, Regra 4 e `estrutura_ok` da F10; provisória):** o #7 exige `w` ≥ 0, único e explícito; **falta o #1 validar**. Pergunta original: o cronograma de waves exige `w` único e o #1 valida? | #1 e #7 | GDD #7 |
| OQ-10 | **Resolvida em 2026-11-04 no lado do #3 (GDD #3, Regra 7):** o `CombatTick` é o relógio da fase e o #3 só lê o `CombatHold`; **o #7 confirmou em 2026-11-05 (GDD #7, Regra 1: todo o tempo dele conta em `CombatTick`); ainda falta o #8 e o #16 confirmarem**. Pergunta original: confirmar o `CombatTick` como relógio de waves, recargas e duração da fase, e o `CombatHold` gravado só pelo #16 (o #3 lê e decide o fim da fase). | #3, #7, #8 e #16 | GDD #3, #7, #8 e #16 |
| OQ-11 | Dois level-ups no mesmo tick: fila de ofertas, com a segunda sorteada só depois do `PickOffer` da primeira. | #16 e #9 | GDD #16 e #9 |
| OQ-12 | **Resolvida em 2026-11-04 (GDD #3, Regra 12):** quem avisa é a tela de pausa (#12), com confirmação em 2 passos; o #28 já trata o abandono como fim de partida; `Abandonada` conta como morte de fase só se o chefe já entrou (decisão do autor). Pergunta original: abandono pelo menu: o host grava no log o `StateHash` marcado "abandonada"; quem avisa o jogador e o que o #28 registra? | #3, #5 e #28 | GDD #3 |
| OQ-13 | Reavaliar todas as decisões *(provisórias)* com o jogo avançado: ordem dos sistemas, mortes imediatas, entrega única de esquiva, política de NaN, capacidade igual ao total de spawns, `MaxTicksPerFrame` = 4, `CombatHold` retido até o toque e o modo `estrito`. **Escopo do MVP (cortes já aplicados em 2026-11-04: `EventosReservados` e cadência do hash viraram constantes, hash por byte, sem regra do limite do `int32`, `TicksAfterEnd` e `UndrainedEvents` viraram exceção do host; restam candidatos):** o `creative-director` apontou o sistema como pesado para um dev solo; cortes aplicados na 2ª passada: `CommandsOutOfOrder` (restavam 4 contadores na época; hoje a Regra 10 lista 8) e P7 reduzido a 2 runtimes; o `technical-director` confirma. | Autor e `technical-director` | Depois do spike de performance e do spike de hash |
| OQ-14 | Fixar no `docs/acceptance/mvp.md` o protocolo de medição de P1 a P6 (aparelho de referência verificado, fase mais pesada, ≥ 20 execuções, aquecimento, temperatura, p95, orçamento commitado antes do build de aceite). **Acrescentado na 2ª passada:** p99 e máximo do `Tick`; pior frame com 4 ticks (resto do frame + 4 × custo do tick); **tempo real descartado** (`dt − dt_ef` mais os ticks do excedente), porque o contador de ticks descartados da FS1 não enxerga um frame degradado; PASS/FAIL do soak térmico (fases seguidas, 15 min ou mais); X1, X3, X6 e N em branco contam como FAIL; folga F de X1 definida; P5 como decisão com limites de ticks descartados por engasgo de 100 ms e de 300 ms. | Autor e `qa-lead` | Antes de D0 |
