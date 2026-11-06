# Fluxo de fase (#3)

> **Status**: In Review (`/design-review` de 2026-11-04 e de 2026-11-05, as duas NEEDS REVISION; os bloqueantes das duas foram aplicados; ciclo encerrado pelo limite de 2 passadas)
> **Design Review**: 2026-11-04 e 2026-11-05, NEEDS REVISION (ver `design/gdd/reviews/fluxo-de-fase-review-log.md`)
> **Author**: Rodrigo Reis + agentes (game-designer, systems-designer)
> **Last Updated**: 2026-11-05 (2ª passada aplicada)
> **Last Verified**: 2026-11-04
> **Implements Pillar**: P2 *Toda escolha pesa* (oferta de level-up e registro após o chefe) e P4 *Massacre com peso* (ritmo das waves e do chefe)
> **Creative Director Review (CD-GDD-ALIGN)**: REVISED 2026-11-04 — CONCERNS A a E aplicados (o diretor não leu as F1 a F3 nem a maior parte dos Acceptance Criteria: esse trecho não passou pelo gate)

## Summary

O Fluxo de fase (#3) é o regente de cada tentativa de fase: ele sabe em que ponto a fase está, conta o XP e o nível do herói, avisa a oferta de cartas a cada level-up, decide se o jogador venceu ou perdeu e cuida do retry. O jogador sente o ritmo da fase, a pausa a cada level-up e a clareza do resultado, inclusive quando o Android fecha o app no meio (a fase se perde, mas não vira derrota). Ele existe para que o teste sem tela e o auto-battle joguem uma fase inteira sob as mesmas regras, para que "morte de fase" seja contada de um jeito só (o critério do Tank) e para que o Grimório registre uma skill ao vencer o chefe sem que o #3 o conheça.

> **Quick reference** — Layer: `Core` · Priority: `MVP` · Key deps: `#1 Dados e balanceamento, #2 Simulação determinística, #6 Combate e dano, #28 Save local; #7 Horda (contrato provisório, sem GDD)`
>
> **Referência de engine** — Unity 6.3 LTS, domínio `Core`: **não há módulo para esse domínio** em `docs/engine-reference/unity/modules/` (só animação, áudio, input, navegação, rede, física, render e UI), então a viabilidade não foi checada contra a engine fixada. O ciclo de vida do Android é `NOT SOURCEABLE` (OQ-9).

## Overview

O Fluxo de fase (#3) é o regente de uma **tentativa de fase**: a máquina de estados que sabe em que ponto a fase está (começando, em combate, com uma carta a escolher, no chefe, terminada) e que decide quando ela acaba, ganhando ou perdendo. Ele conta o XP que os inimigos mortos dão, sobe o nível do herói dentro da fase e, a cada level-up, avisa a oferta de cartas (#9 e #16) de que há uma escolha a abrir. Quando o chefe de fase cai, ou quando o herói morre, o #3 decide o resultado, pede o fim da fase à simulação (#2) e entrega o resultado a quem vem depois: o registro no Grimório (#16), a campanha (#20) e o log (#5). Depois de uma derrota ou de um app fechado, ele também cuida do **retry**: uma nova tentativa é uma nova simulação, criada do zero, porque o #28 proíbe retomar uma fase do meio.

O jogador não interage com o #3 diretamente: ele sente o resultado, que é o ritmo da fase (waves que sobem até o chefe), a pausa do combate a cada level-up e a clareza de ter vencido ou perdido. O projeto precisa dele por quatro razões. (1) A simulação headless do MVP e o auto-battle (#40, Full Vision) jogam uma fase inteira sozinhos, então a máquina de estados da fase tem de ser lógica pura, sem input nem apresentação, e rodar igual no jogo e no teste. (2) A comparação Tank × DPS e o critério do Tank (≤ 2 mortes de fase) só valem se "morte de fase" for contada de um jeito só, e é o #3 quem a define. (3) O Grimório só registra uma skill ao vencer o chefe de fase, e o #3 é quem avisa isso por **ganchos** (início de fase, level-up, chefe vencido), sem conhecer o Grimório: ele se registra nos ganchos, e o #3 nunca o chama pelo nome. (4) O contrato de "app fechado no meio da fase" com o #28 (marca da fase, tentativa falha que não conta como morte) precisa de um dono, e é o #3.

Parte do trabalho acontece **dentro do tick**, como um sistema da simulação na ordem do compositor (XP, nível, chefe, fim). Outra parte acontece **fora do tick**, no ciclo de vida da tentativa (entrar na fase, criar a simulação, retry, abandono pelo menu). As duas são C# puro. Como essa divisão se desenha é decidido na seção Detailed Design *(provisório)*.

**Fronteira.** O #3 é dono: dos estados da tentativa e das transições entre eles; do XP e do nível dentro da fase (a curva vem do #1); dos ganchos de início de fase, level-up e chefe vencido; da decisão de vitória ou derrota e do resultado entregue; da política de seed por tentativa e do retry; do contrato da marca da fase com o #28; e de *quando* pausar. Ele **não** é dono: do relógio, da ordem dos sistemas e dos sorteios (#2); de dano e vida (#6); da composição das waves e do chefe (#7); das skills (#8); da oferta de cartas, do `CombatHold` e do registro no Grimório (#9 e #16); do input e da câmera (#4); do formato do save e da marca em disco (#28); do formato do log (#5); da curva de XP e de qualquer valor, que moram no #1; da ordem das fases e dos capítulos (#20, a confirmar); e da recompensa de fim de fase (economia, a confirmar). O desenho técnico (`ISimSystem` em `Forja.Gameplay.Sim`, sem engine, float32, tick fixo de 30 Hz) está no ADR-0001 (*Proposed*), que este GDD cita e não repete.

## Player Fantasy

**Enquadramento: indireto.** O jogador nunca vê este sistema; ele sente o arco de uma tentativa.

**Cada tentativa é uma forja nova.** A fase começa do começo e termina de um jeito só: o chefe cai, ou a tentativa é sua derrota (você cai, ou o relógio do chefe acaba). No meio, a horda sobe, e cada nível ganho para o combate e põe uma escolha na sua mão. Se o chefe cair, mesmo no golpe que derruba vocês dois, a vitória é sua, e você escolhe qual skill daquela build o Grimório guarda. Se você cair, a próxima tentativa começa limpa: sem retomar, sem meio caminho.

**O momento.** Morrer no chefe de fase, apertar retry e chegar de novo ao chefe com outra build.

**Pilares.** P2 *Toda escolha pesa* (principal): a derrota é real, a vitória é mérito, e não existe desfazer nem retomar. P1 *Sua build, sua assinatura* (apoio): cada tentativa é a busca pela build que é sua. O P4 *Massacre com peso* é servido pelo ritmo da fase, mas a cena do level-up (o combate parado, as 3 cartas) pertence ao #9, e o #3 só decide *quando* ela abre.

**Teste de acerto (observação do próprio autor, n = 1).** Depois de uma derrota, o retry sai sem hesitação e "onde eu parei?" não aparece como pergunta. Se o Android fechar o app no meio da fase, a sensação de "o jogo me puniu" também não aparece: a fase se perde, mas não vira morte nas contas.

**O que esta seção não promete.** Que a próxima tentativa seja mais fácil (ela é diferente, porque a seed é nova a cada tentativa, Regra 10, mas isso não a torna mais fácil); qualquer forma de continuar, retomar ou salvar uma fase pela metade; tempo-limite para escolher a carta (não existe no MVP); nada sobre o chefe de capítulo (é do #20); e nada sobre recompensa de fim de fase (a confirmar com a economia).

*Consultado: `creative-director` (enquadramento C, "cada tentativa é uma forja nova", com a clareza do fim do enquadramento A numa frase; o B, a cena do level-up, ficou com o #9).*

## Detailed Design

### Core Rules

> **Marca de provisório.** Toda regra marcada *(provisória)* foi decidida por recomendação de especialista (`systems-designer`, `game-designer`, `gameplay-programmer`, `engine-programmer`), não pelo autor, e deve ser reavaliada com o jogo avançado. As marcadas *(decisão do autor, 2026-11-04)* foram escolhidas pelo autor. O resto vem do #2, do #28, do #1 ou do ADR-0001.

1. **Uma tentativa.** Uma tentativa é uma `Simulation` mais um `attemptId`, da entrada na fase até o resultado. Só existe uma por vez. Cada retry é **outra** tentativa: nova simulação, novo `attemptId`, nova seed, wave 1, nível 1 e XP 0. Nada do estado de uma tentativa passa para a seguinte; só o que o #28 gravou (progresso, Grimório) sobrevive. Não existe retomar uma fase do meio (#28, regra 6).

2. **Duas metades, as duas em C# puro.** *(provisória)*
   - **Dentro do tick:** o `SistemaFluxoDeFase` (um `ISimSystem` em `Forja.Gameplay.Sim`, na ordem do compositor, depois do #6 e antes do #16). Fica aqui tudo o que depende de mortes e do estado da simulação, precisa ser reproduzível e entra no hash: fim da fase, XP, nível, a entrada do chefe.
   - **Fora do tick:** a `TentativaDeFase` (mesmo assembly, outro namespace, uma instância por tentativa, sem `static`), chamada pelo host entre frames. Fica aqui tudo o que depende de relógio de parede, disco, seed do host ou tela: entrar na fase, a marca com o #28, sortear a seed, criar a simulação, pausa, abandono, encerrar e retry.
   - **Thread única.** Toda entrada na `TentativaDeFase` (respostas do #28, pausa, retry, abandono) acontece na thread principal: o #28 entrega as respostas numa fila que a ponte esvazia entre frames, e nenhuma continuação roda em outra thread. Nos testes a fila é manual. *(provisória; NOT SOURCEABLE: o comportamento do contexto de sincronização e do `Awaitable` no 6000.3.27f1 não é coberto por `docs/engine-reference/unity/`, OQ-9 A)*

3. **Entrada na fase** (fora do tick, nesta ordem). *(provisória)*
   1. O snapshot do #1 tem de ser válido; senão a fase não começa (o #1 bloqueia a entrada).
   2. A `TentativaDeFase` gera o `attemptId` (128 bits aleatórios, comparado só por igualdade) por uma fonte injetada, **antes** do pedido, e um `requestId` por pedido de commit (`BeginStage`, limpeza, fim), também pela fonte injetada (nos testes a fonte é um contador determinístico): a resposta do #28 devolve os dois, e o #3 só age sobre a resposta cujo `requestId` é o do pedido pendente, ignorando as de commits antigos. Chama `BeginStage` no #28, com um payload opaco **vazio no MVP** (não há custo de entrada nem energia), e **espera o resultado real do commit**. A espera nunca bloqueia a thread principal e o timer de "ainda gravando…" usa tempo real, só de apresentação. **Confirmado**: segue. **Falhou com causa**, ou "sem marca" (modo só leitura, armazenamento indisponível): a fase **começa sem marca**, como o #28 aceitou (OQ-4 dele). **Voltar durante a espera**: a tentativa vai a *Cancelando*: o #3 pede o commit que limpa a marca (outro `requestId`), `Entrar` fica desabilitado **com o motivo na tela** ("Gravando…") e só *Cancelada* (não é tentativa) sai da resposta desse commit de limpeza, `Confirmado` ou `Falhou`; uma resposta do `BeginStage` que chegue nesse meio-tempo é ignorada. Em `Falhou`, a marca que talvez tenha sobrado vira "marca encontrada" no próximo boot e conta como `AppFechado` (risco aceito, a mesma janela da regra 6 do #28) *(provisória)*. **Não há timeout que devolva "sem marca"** (regra 6 do #28): a saída do jogador durante a espera é o Voltar, e em *Cancelando* sem resposta ele pode sair da tela, com a limpeza seguindo em segundo plano.
   3. Sorteia a seed por uma fonte injetada (`ISeedSource`), fora da simulação, e entrega ao host gravá-la no log (#5) **antes** do tick 0 (Regra 1 do #2).
   4. O host chama `Simulation.Create(...)`. Logo depois, **antes do 1º `Tick`**, o compositor chama `Preparar` em cada sistema que implementa a interface opcional `IPreparaFase`, com o #3 primeiro: ele cria o herói por `SimWorld.Spawn(faction, essential, xpValue, hp, x, y)`, com a marca `Essencial` passada no próprio `Spawn` e HP e posição vindos do snapshot (a linha nasce inteira; ADR-0001, emenda 6). No mesmo `Preparar` o #3 grava a **ficha de fase inteira** com os valores iniciais da Regra 4 (não só o `IdDoHeroi`; exige estender a emenda 14 do ADR-0001, que hoje só libera o `Spawn` do herói e o `IdDoHeroi` fora do tick). O herói consome um id da tabela, então entra no **total de spawns** da fase (FS9 do #2): o #3 declara 1 como `ids_de_preparacao` (ver Formulas). O compositor é o único dono dessa preparação, e o `Spawn` de preparação não emite evento (ou o host drena o buffer antes do 1º `Tick`, senão o `Tick` falha por buffer não drenado, Regra 14 do #2).
   5. A tentativa passa a *Em andamento*.

4. **Ficha de fase** (dentro do tick). Um bloco de escalares no `SimWorld`, **escrito só pelo #3 e lido por qualquer sistema**, do mesmo modo que o `CombatHold` (Regra 15 do #2). Campos e **valor inicial**, gravado inteiro no `Preparar` (Regra 3.4), para o hash do tick 1 ser canônico e nenhum campo ficar com o padrão do código (`IdDoChefe` = 0 seria o herói, `Nivel` = 0 daria limiar negativo na F3):

   | Campo | Inicial | Observação |
   |---|---|---|
   | `Estado` | `EmCombate` | dentro do tick só `EmCombate` ou `FimPedido`; os demais estados da tentativa vivem fora do tick |
   | `Nivel` | 1 | |
   | `XpAtual` | 0 | inteiro |
   | `NiveisGanhos` | 0 | só cresce, nunca é zerado |
   | `ChefeVisto`, `ChefeVencido`, `MorteSimultanea` | falso | |
   | `TickDeEntradaDoChefe` | −1 | em `CombatTick`; −1 até o chefe ser visto |
   | `IdDoHeroi` | 0 | o herói é o primeiro `Spawn` |
   | `ProximoIdAVer` | 1 | o herói (id 0) já foi visto no `Preparar` |
   | `IdDoChefe` | −1 | gravado no primeiro inimigo `Essencial` visto |
   | `EssenciaisInimigosVivos` | 0 | Regra 5.2 |
   | Pedido de fim: tipo, detalhe e tick | nenhum, nenhum, −1 | o tipo e o detalhe são os do Core (`EndKind`, `FailureDetail`) |
   | `MotivoFim` | nenhum | do #3: `Vitoria`, `DerrotaHeroi`, `DerrotaTempo` ou `ChefeAusente`; separa as duas derrotas, que o `EndKind` do Core junta em `Defeat` |

   Todos entram no hash **pelo `Hash` do próprio sistema #3**: a FS8 do #2 já inclui o `Hash` de cada sistema, na ordem do compositor, então a ficha não muda a Regra 10 nem a FS8 *(resolve o conflito de escopo do hash achado no `/consistency-check` de 2026-11-04)*. *(provisória; exige acrescentar a ficha ao `SimWorld` e a lista de pendências do ADR, OQ-5 do #2; a Regra 10 e a FS8 do #2 não mudam.)*

5. **O passo do #3 em cada tick**, em ordem. *(provisória)*
   1. Se `ctx.CombatActive` for falso (oferta pendente ou aguardando retomada), o #3 **não faz nada**: com o combate retido ninguém morre e nenhum XP é dado. O `CombatTick` não avançou, então nenhum relógio da fase andou.
   2. **Atualiza `ChefeVisto`.** O #3 lê a **tabela de ids**, não só a lista de vivos, mas **só os ids novos**: guarda na ficha `ProximoIdAVer` e a cada tick varre `[ProximoIdAVer, contador de ids)` (ids são monotônicos e nunca se reutilizam, Regra 8 do #2), então o custo não cresce com a capacidade. Para cada id novo `Essencial` **e** de facção inimiga, soma 1 em `EssenciaisInimigosVivos` e, no primeiro, grava `IdDoChefe`; depois, para cada morte do tick (`DeathsThisTick` do `SimWorld`), se o id morto é `Essencial` inimigo, subtrai 1 (a coluna `Essencial` continua na linha do id depois da morte). `ChefeVisto` fica verdadeiro quando algum `Essencial` inimigo já foi visto, vivo ou morto. Assim um chefe que nasce e morre no mesmo tick (soma 1 e subtrai 1 no mesmo passo) não deixa a vitória escapar. Na primeira vez, grava `TickDeEntradaDoChefe`. *(provisória)*
   3. **Avalia o fim, em um único ponto (`AvaliarFim`)**, nesta ordem de prioridade (mesma da Regra 13 do #2): a **falha interna por chefe ausente** (Regra 7, F4), depois a **vitória** (há `ChefeVisto` e `EssenciaisInimigosVivos` = 0, isto é, nenhum inimigo `Essencial` vivo; "inimigo `Essencial`" é `Essencial` **e** facção inimiga, nunca o herói, e o MVP tem exatamente 1 por fase, que o #1 valida), depois **derrota por herói morto**, depois **derrota por tempo** (Regra 7). Se houver pedido de fim, ele sai pelo contexto do tick e o #3 pula o 5.5 (sem XP e sem nível, Regra 5.4), mas **vai ao 5.6**, que grava a ficha com o tipo, o detalhe e o tick do pedido, o `MotivoFim`, `MorteSimultanea` e `ChefeVencido`. `MorteSimultanea` é verdadeira só se a vitória e o herói com `vivo = falso` ocorrem no mesmo tick; um herói morto num tick anterior já teria encerrado a fase.
   4. **Sem XP e sem nível no tick em que a fase termina**, para o #16 não abrir uma oferta que nasce depois do fim. O nível final do resultado é o do tick anterior. Como o #16 roda depois no mesmo tick, ele **não abre oferta quando o contexto traz um pedido de fim** *(exigência ao #16, a confirmar)*.
   5. **XP e nível** (Regra 6).
   6. Atualiza a ficha (também no tick do fim).

6. **XP e nível.**
   - **O XP é direto na morte do inimigo** *(decisão do autor, 2026-11-04)*. O orbe de XP é só um efeito visual que voa até o herói (apresentação, #12), nunca uma entidade: orbe como entidade dobraria a conta de spawns da fase (ids nunca se reutilizam) e pesaria no aparelho com 300 ou mais inimigos. Isso **muda a linha 120 do conceito** ("coleta orbes de XP"), que está congelado; a emenda fica anotada em Open Questions.
   - O XP do tick é a soma do `xpDaMorte` dos inimigos mortos **neste tick**, em ordem crescente de índice. Mortes por valor inválido (Regra 9 do #2) não dão XP. O `xpDaMorte` é declarado pelo #7 por arquétipo e entra no `SimWorld` como coluna inteira *(provisória; exige ADR do #6 e do #7)*.
   - O nível **zera a cada tentativa**: as skills de dentro da fase são temporárias. O XP em excesso passa ao nível seguinte. Existe um **teto de nível** (knob do #1); no teto, o excedente é descartado, `XpAtual` vale 0 (para o hash ser canônico) e não há mais level-up. O XP do tick é somado inteiro **antes** do laço de nível (F2 e F3). O XP e os level-ups continuam durante o chefe.
   - **Forma da curva.** Crescente, com o primeiro level-up cedo para a primeira escolha chegar logo. Os números são knobs do #1 e entram em Formulas.
   - **Ritmo.** A intenção, a calibrar no protótipo: o número de level-ups numa fase fica **abaixo do pool `P = P_f + P_c` de skills ativas da função** (5 de função mais 5 compartilhadas, 10 no MVP), para que uma tentativa não consiga todas e o Grimório não vire "quase tudo" (o erro que o protótipo já mostrou). Isso é uma **checagem de setup do #1** (F5), não só intenção *(provisória; a faixa de X a Y level-ups é pergunta de calibração, OQ-5)*.
   - **Level-up sem chamar ninguém.** O #3 só incrementa `NiveisGanhos`. O #16, que roda depois no mesmo tick, compara esse valor com o serial de ofertas que ele guarda: a diferença é o número de ofertas devidas, e é assim que dois level-ups no mesmo tick viram uma fila (OQ-11 do #2). O #3 não conhece o #16, e o contador, ao contrário de uma flag, não perde nada se o #16 não tiver rodado.
   - **Cura no level-up** *(decisão do autor, 2026-11-05)*. Cada nível ganho cura o herói em `cura_levelup_pct × hpMax` (knob declarado no #6, Regra 15). **O #3 não pede a cura**: ele só sobe `NiveisGanhos`, e o #6 lê esse contador do mesmo jeito que o #16. O #6 guarda um cursor `NiveisCurados` (inicial 0, no `Hash` do #6) e, no passo dele, num tick com `CombatActive`, aplica `(NiveisGanhos − NiveisCurados) × cura_levelup_pct × hpMax` e avança o cursor. Como o #6 roda antes do #3, a cura de um level-up no tick T sai no primeiro tick ativo depois de T (se o #16 abre a oferta em T, só depois da carta). O estado pendente é a diferença entre dois contadores no hash, então nada atravessa o tick fora do hash. No tick do fim não há level-up (Regra 5.4), então não há cura; no teto (`nivel_max`) também não. *(provisória; exige emendar a Regra 15 do #6, que hoje recebe um pedido `Curar` do #3)*

7. **Tempo da fase.** O relógio da fase é o `CombatTick` (OQ-10 do #2, confirmada): o tempo de escolha de carta não conta. Antes do chefe entrar, quem manda é o cronograma de waves do #7, que termina com o chefe. **Depois que o chefe entra, existe um tempo máximo** (knob do #1, `duracao_max_apos_chefe`, em segundos convertidos em ticks pelo #1): ao estourar, a tentativa termina em **derrota por tempo, que conta como morte de fase** *(decisão do autor, 2026-11-04)*. O teto precisa ser folgado e calibrado para o Tank, que mata devagar: ele é guarda contra travamento, não alavanca de dificuldade. O #12 mostra o tempo restante, para o jogador saber por que perdeu (P2). Como o cronograma é finito e o teto também, nenhuma fase roda para sempre, nem no teste sem tela nem no auto-battle, **desde que o chefe entre**. Se o `Spawn` do chefe devolve −1, a falha é do #2 (Regra 8: `Spawn` rejeitado do chefe é bug interno e a fase falha), dentro do tick, todo `Spawn` `Essencial` rejeitado encerra a simulação **no mesmo tick** com `FalhaInterna` e o detalhe `EssentialSpawnRejected`, que o #3 traduz em `FalhaInterna(ChefeAusente)` no resultado, sem esperar o teto (ADR-0001, emenda 6; *provisória*); o #3 **não detecta esse caso sozinho**, porque o `SpawnsRejected` é diagnóstico e não distingue o chefe de um inimigo comum. Para o caso em que ele nunca entra por dado errado ou atraso, o #7 declara o `tick_entrada_chefe_agendado` e o #3 termina a tentativa como `FalhaInterna(ChefeAusente)` quando o `CombatTick` passa desse tick mais o teto do chefe (F4): é bug nosso e não conta como morte *(provisória; a validação no setup do #1 é a primeira defesa)*. **Para o aceite**, a `DerrotaTempo` é registrada como sinal à parte (como a `MorteSimultanea`), e se alguma morte de fase do Tank for `DerrotaTempo`, o `duracao_max_apos_chefe_s` é revisto e a medição repetida antes de julgar o Tank (intenção de calibração: o teto é folgado, N vezes o tempo de luta esperado do Tank, com N a calibrar). Waves que ainda não nasceram quando o chefe entra são do cronograma do #7 (o padrão é não nascer wave nova); o #3 não decide isso.

8. **Resultados possíveis** (um enum que só cresce; o fim é avaliado em um único lugar, o que deixa a porta aberta para fases de função, que ficam **fora do MVP**). Se vários valem no mesmo tick, a prioridade é `FalhaInterna` > `Vitoria` > `DerrotaHeroi` > `DerrotaTempo` (a `FalhaInterna` vem da Regra 9 do #2). O resultado leva: a causa, o nível final, `ChefeVisto`, `MorteSimultanea`, o `CombatTick` final, o `StateHash` final e o `attemptId`. **De onde sai a causa:** primeiro de `Simulation.End` e `Simulation.EndDetail` (o Core pode anular o pedido do #3, por exemplo com NaN num `Essencial` no passo 6, e um `EssentialSpawnRejected` vira `FalhaInterna(ChefeAusente)`); só quando o fim é o que o #3 pediu, o `MotivoFim` da ficha separa `DerrotaHeroi` de `DerrotaTempo`. `ChefeVencido` na ficha nunca decide a causa: ele pode estar verdadeiro num resultado `FalhaInterna`.

   | Causa | Conta como morte de fase (aceite) | Vitória para o K_min | Grimório | Campanha (recompensa de fim de fase) |
   |---|---|---|---|---|
   | `Vitoria` | não | +1 (replay conta, dentro do `replay_limit` do #1) | oferece o registro | avança |
   | `DerrotaHeroi` | **sim** | não | nada | sem recompensa |
   | `DerrotaTempo` | **sim** | não | nada | sem recompensa |
   | `Abandonada` | **sim, só se `ChefeVisto`** | não | nada | sem recompensa |
   | `AppFechado` | **não** (decisão do #28) | não | nada | sem recompensa |
   | `FalhaInterna` (inclui `ChefeAusente`) | não (bug nosso; o mesmo caminho do app fechado, Regra 9 do #2) | não | nada | sem recompensa |
   | `Quebrada` | não *(provisória)* | não | nada | sem recompensa |
   | `Cancelada`, `Restaurado` | não são tentativa | não | nada | nada |

   - **Esta definição de "morte de fase" é mais estreita que a do conceito** (L405: "morte é uma tentativa que termina sem vencer o chefe de fase"): por decisões do autor e do #28, ficam fora da conta o abandono antes de o chefe entrar, `AppFechado`, `FalhaInterna`, `Quebrada` e a vitória em que os dois caem juntos. **A definição estreita foi aceita pelo autor em 2026-11-05 (OQ-19)**; a emenda ao L405 do conceito congelado fica anotada lá. Para a métrica do Tank não passar por construção (L402 do conceito), cada um desses sinais tem de ter um pior valor fixado no aceite (X11).
   - **As colunas "Vitória para o K_min", "Grimório" e "Campanha" da tabela** são o que cada dono (#16, #20) faz com a causa, um contrato provisório; o #3 só decide a causa e a coluna "Conta como morte de fase".
   - **Vitória em que herói e chefe morrem juntos:** vale a vitória (Regra 13 do #2), **não conta como morte de fase** e o resultado leva `MorteSimultanea = verdadeiro`. O log a registra, e o aceite a contabiliza como sinal à parte, para um Tank não passar o critério "empatando" o chefe sem ninguém notar *(resolve a OQ-7 do #2; a regra de não contar é provisória)*.
   - **Sem continue e sem revive.** Não existe continue nem revive, nem pago, nem por vídeo, nem grátis: o herói morto encerra a tentativa no tick em que morre *(decisão do autor, 2026-11-04; P2 e Princípio de Negócio; a R6 do `business-model.md` veta só o vídeo durante a partida, e esta regra cobre toda forma de continue)*.
   - **"Sem recompensa" é só a recompensa de fim de fase.** O que foi coletado durante a fase (materiais, por exemplo) segue a regra da economia: o conceito (L112) diz que, ao morrer, o jogador fica com os materiais coletados até ali, com a taxa a definir no GDD de economia. O #3 **não define** quanto cada causa rende, nem em materiais, nem em moeda de jogo, nem na dobra por vídeo do fim da partida (R6 do `business-model.md`): é uma exigência à economia, registrada na OQ-16.
   - **Tipo de fase e origem.** O resultado não traz o tipo da fase nem a origem da tentativa: o #16 filtra pelo tipo de fase que vem do snapshot do #1 (o chefe de capítulo é do #20 e não registra nem conta vitória para o K_min, conceito L81) e, quando o auto-battle existir, o resultado ganha a origem manual ou automática (OQ-17). O enum de causas só cresce e comporta isso.
   - **Quem conta o quê.** O #3 só entrega a causa e as marcas. A contagem de mortes de fase é do #5 (por causa), e o contador de vitórias de chefe de fase é do #16 (fatia do #28). Auto-battle e varredura nunca geram vitória para o K_min nem registro. A coluna "conta como morte de fase" da tabela é uma **função pura**, `Resultado.ContaComoMorteDeFase` (da causa e de `ChefeVisto`), que o #5 chama para contar e que os testes verificam sem depender do #5.

9. **Encerrar a tentativa** (fora do tick, nesta ordem). *(provisória)*
   1. O host drena os eventos finais, lê o `StateHash` e o grava no log (em `Quebrada` o `StateHash` lança: o resultado leva hash, nível e `CombatTick` como "indisponível", e `IConcluiFase` é chamada com a causa `Quebrada`, e o #16 não age).
   2. O compositor monta o resultado e chama `IConcluiFase(resultado)` em cada sistema que a implementa, em **toda** causa, com a causa no resultado; cada implementador filtra o que lhe interessa (o #16 só avança o contador em `Vitoria`). O #16 atualiza em memória a fatia dele (o contador de vitórias). **É assim que o "chefe vencido" chega ao Grimório, sem o #3 conhecê-lo.** A ficha também mostra `ChefeVencido`.
   3. A `Simulation` é descartada.
   4. O #3 pede ao #28 o **commit de fim de partida**, que limpa a marca no mesmo commit das fatias (regra 6 do #28). O evento do #5 sai **depois** da resposta do commit (confirmada, ou falha marcada "commit falhou").
   5. Só em vitória, o #16 abre a escolha de registro **fora da simulação**, que já está encerrada: o `Tick` depois do fim lança exceção, então o registro nunca é um `PickOffer`. Ele é um segundo commit, no ponto seguro "ao registrar no Grimório" do #28. Se o app morrer entre os dois commits, a vitória conta e o registro daquela vitória se perde (a avaliar com o #16, OQ-6).

10. **Retry.** Disponível só quando a tentativa está *Resolvida*: a primeira chamada passa a *Entrando* de forma síncrona, antes de qualquer pedido assíncrono, e em qualquer outro estado `Retry` é ignorado sem erro (um toque duplo gera um só `attemptId` e um só `BeginStage`). Recomeça sempre da wave 1, sem custo (não existe energia) e sem limite de tentativas, com uma simulação nova, um novo `attemptId` e **uma seed nova a cada tentativa** *(decisão do autor, 2026-11-04, resolve a OQ-2 do #2)*: a mesma seed deixaria o jogador decorar as cartas e mataria o "só mais uma". A seed muda as ofertas e os sorteios da horda; o roteiro do chefe é determinístico (do #7), para o jogador poder aprendê-lo entre tentativas *(provisória; a confirmar com o #7)*. O novo `BeginStage` só é pedido **depois** do commit que limpou a marca anterior. Nos testes, a fonte de seeds é a lista versionada do aceite, e a comparação Tank × DPS usa um override de teste que repete a seed entre as duas funções: isso é decisão de teste, não de jogo. **Não há retry automático** depois de `AppFechado`, `FalhaInterna` ou `Quebrada`: o jogador decide.

11. **Pausa.** O #3 decide *quando* pausar; o #2 só aceita "zero ticks" (Regra 11). O jogador pode pausar **a qualquer hora**, inclusive com uma oferta pendente (nesse caso não há portão de joystick, como a Regra 11 do #2 define). Perda de foco, segundo plano e ligação valem como pausa. A ponte guarda um **conjunto de motivos de pausa**, não um booleano, e só retoma quando o conjunto esvazia *(provisória; recomendação do `engine-programmer`)*. O primeiro `dt` depois de uma pausa **ou depois do carregamento da fase** é descartado. Se a tentativa fica pronta com um motivo de pausa já ativo (o app foi para segundo plano durante a espera do commit), ela nasce *Pausada*, não *Em andamento* *(provisória)*. Não existe pausa na tela de resultado (a simulação já terminou). A pausa **não grava** (regra 5 do #28). Se o Android matar o app durante a pausa, vale `AppFechado`.

12. **Abandono.** Só pelo menu de pausa, com **confirmação em 2 passos** (a tela é do #12): `PedirAbandono()` abre a confirmação ("Perde esta tentativa. Abandonar?") e a fase segue pausada; cancelar volta à pausa; `ConfirmarAbandono()` age **entre ticks**, sem rodar `Tick` para pedir o fim (Regra 13 do #2); só vale em *Pausada* com a confirmação aberta (o diálogo conta como motivo de pausa) e é ignorado em qualquer outro estado ou numa segunda chamada. O resultado é `Abandonada` e segue a Regra 9, do 9.1 ao 9.4, na ordem dela: drenar, ler o `StateHash` e gravar "abandonada" no log (9.1), `IConcluiFase` (9.2) e só então o descarte (9.3), porque o `StateHash` lança depois do `Discard` e o `IConcluiFase` vem antes dele (ADR-0001, emendas 2 e 14). **Conta como morte de fase só se o chefe já entrou** *(decisão do autor, 2026-11-04)*: recomeçar cedo com uma build ruim é normal num survivor e não é punido, mas fugir do chefe para esconder uma derrota conta (o aceite não aceita métrica que passa por construção). Resolve a OQ-12 do #2.

13. **Marca encontrada ao abrir o app** (contrato com o #28, regra 6). O #28 informa ao #3 "marca encontrada: herói, fase, `attemptId`, causa" e a consome. **Causa "app fechado"**: a tentativa é resolvida como `AppFechado` (falha, sem recompensa, **não conta como morte**, sem retry automático), e o #3 devolve na resposta do callback o efeito que quer gravar (vazio no MVP), que o #28 grava no mesmo commit do consumo; assim o #3 não precisa deduplicar. **Causa "restaurado"** (marca vinda de um backup): não é tentativa. Herói ou fase desconhecidos para o #1: o #28 informa mesmo assim, e o #3 não aplica efeito. O payload opaco existe para o Livro de Reforja (Alpha, OQ-6 do #28).

14. **Falhas da simulação.** `FalhaInterna` (valor inválido num `Essencial`) e `Quebrada` (exceção dentro do `Tick`) terminam a tentativa como falha **sem derrota** e sem recompensa. O host registra a exceção no log e segue a Regra 9, na ordem dela (o descarte é o passo 9.3, depois do `IConcluiFase`) *(provisória)*. A entrada com snapshot inválido não cria nada. **Knob inválido** tem um caminho só: o `Preparar` valida os knobs uma vez, incluindo o `xpDaMorte` de todo arquétipo do snapshot (caminho de *Entrando*, `FalhaInterna(DadosInvalidos)`). Dentro do tick não há checagem de dado: o `xpDaMorte` é constante por arquétipo e já foi validado antes do tick 0.

15. **Ganchos.** São três e nenhum é chamada de um sistema a outro:

   | Gancho | Onde | Como |
   |---|---|---|
   | Início de fase | fora do tick, antes do tick 0 | `IPreparaFase.Preparar`, chamada pelo compositor; a garantia de skill do #16 é dele e, se precisar de sorteio, ele a faz no 1º `Step` lendo a ficha |
   | Level-up | dentro do tick | `NiveisGanhos` na ficha, lido pelo #16 no passo dele |
   | Chefe vencido | fora do tick, depois do fim | `IConcluiFase(resultado)`, e `ChefeVencido` na ficha |

   Só o compositor conhece todos os sistemas. Os eventos `FaseIniciada`, `LevelUp`, `ChefeEntrou`, `ChefeVencido` e `FaseEncerrada` são emitidos **só para a apresentação e o log**, nunca lidos como canal entre sistemas; `FaseEncerrada` usa a reserva de eventos críticos (Regra 6 do #2).

16. **Estado hasheado do #3.** Entram: a ficha de fase inteira, inclusive `MotivoFim` (hasheada uma vez, pelo `Hash` do próprio sistema #3, que a FS8 do #2 já inclui na ordem do compositor; o `SimWorld` não a hasheia, ao contrário do `CombatHold`, que é do #16 e entra pelo `SimWorld`; os testes verificam pelo `StateHash` da `Simulation`, com fixtures), `ChefeVisto`, `TickDeEntradaDoChefe`, `ProximoIdAVer`, `IdDoChefe`, `EssenciaisInimigosVivos`, o motivo e o tick do pedido de fim e `MorteSimultanea` (o `IdDoHeroi` é constante 0 e está na ficha, mas nenhum teste o exercita). Ficam de fora: `attemptId` e seed (a seed está no cabeçalho do log e o estado dos streams já entra no hash do #2), os estados fora do tick (Entrando, Cancelando, Cancelada, Pausada, Concluindo, Resolvida), o tempo de parede, contadores de diagnóstico, o snapshot, o resultado já montado e o limiar do próximo nível (derivado de `Nivel` e da curva).

17. **Restrições herdadas do ADR-0001 e do #2.** Só `float` fracionário, e XP, nível e contagens em `int`; sem `System.Random`, sem `UnityEngine` e sem estado `static` mutável (inclusive eventos e caches estáticos); nenhum valor de gameplay fixo no código; o passo do #3 é O(1) por tick mais O(mortes e ids novos do tick), sem alocação gerenciada.

### States and Transitions

Os subestados "combate livre", "oferta pendente" e "aguardando retomada" **não são do #3**: vêm do `CombatHold` do #16 (fonte única, Regra 15 do #2). A tabela cobre o ciclo de vida da tentativa; os estados *Entrando*, *Cancelando*, *Cancelada*, *Pausada*, *Concluindo* e *Resolvida* vivem fora do tick e fora do hash.

| Estado | Evento | Próximo estado e efeito |
|---|---|---|
| (nenhum) | Snapshot inválido | Não cria; o #1 bloqueia a entrada |
| (nenhum) | Snapshot válido | Entrando |
| Entrando | #28 confirma a marca | Em andamento (seed, log, `Create`, `Preparar`); *Pausada* se já há motivo de pausa ativo |
| Entrando | #28 falha ou "sem marca" | Em andamento, sem marca (OQ-4 do #28) |
| Entrando | Voltar | Cancelando (pede o commit que limpa a marca, com outro `requestId`; `Entrar` fica desabilitado, com o motivo na tela, até a resposta) |
| Cancelando | Resposta do commit de limpeza (o `requestId` do pedido pendente), `Confirmado` ou `Falhou` | Cancelada (não é tentativa); respostas de outro `requestId` são ignoradas |
| Cancelada | Sair da tela | Fim (uma nova entrada começa em "(nenhum)", com novo `attemptId`) |
| Entrando | `Create` ou `Preparar` lança, ou herói inválido | Concluindo(`FalhaInterna`), hash "indisponível"; o #3 pede o commit que limpa a marca antes de liberar o retry |
| Em andamento | `Tick` sem fim | Em andamento |
| Em andamento | Pausa, perda de foco, ligação | Pausada (zero `Tick`, não grava) |
| Pausada | Todos os motivos de pausa encerrados (retomada pelo portão do #2) | Em andamento |
| Pausada, com `PedirAbandono` aberto | `ConfirmarAbandono` | Concluindo(`Abandonada`) |
| Pausada, com `PedirAbandono` aberto | Cancelar o abandono | Pausada (a confirmação fecha e sai do conjunto de motivos de pausa) |
| Em andamento | Vitória pedida no tick | Concluindo(`Vitoria`), com `MorteSimultanea` se couber |
| Em andamento | Herói morto, sem vitória | Concluindo(`DerrotaHeroi`) |
| Em andamento | Tempo máximo após o chefe estourado | Concluindo(`DerrotaTempo`) |
| Em andamento | Valor inválido num `Essencial` (#2, Regra 9) | Concluindo(`FalhaInterna`) |
| Em andamento | Exceção dentro do `Tick` | Concluindo(`Quebrada`) |
| Concluindo | Drena, `StateHash`, `IConcluiFase`, descarta, commit de fim, evento ao #5 | Resolvida (também se o commit de fim falhar: o resultado vale na sessão, o aviso é do #28, regra 12, e o evento ao #5 sai mesmo assim, marcado "commit falhou", para a contagem do aceite não se perder) |
| Resolvida | Retry | Entrando (novo `attemptId`, nova seed) |
| Resolvida | Sair | Fim |
| Qualquer estado em jogo | Android mata o app | A marca fica em disco; no próximo boot o #28 informa e o #3 resolve como `AppFechado` (Regra 13) |
| (boot) | Marca com causa "restaurado" | Não é tentativa |
| Concluindo | O app morre antes do commit de fim | Vira `AppFechado` (a janela é de milissegundos; risco aceito) |

### Interactions with Other Systems

| Sistema | Natureza | Entra no #3 | Sai do #3 | Dono da interface |
|---|---|---|---|---|
| #1 Dados e balanceamento | Hard | Snapshot da fase (em ticks), os knobs da curva de XP (`xp_base`, `xp_inc`, `xp_quad`), `nivel_max`, `duracao_max_apos_chefe_s` (já em ticks) e a checagem de setup da F5 (`folga_pool`, `teto_xp_min_pct`, `teto_xp_max_pct`) | Nada | O #1 é dono do snapshot; o #3 nunca converte segundos |
| #2 Simulação | Hard | O contexto do tick (`CombatActive`, `CombatTick`, `Rng`, `Emit`) e a criação por `Simulation.Create` | Pedido de fim e a ficha de fase | O #2 é dono do contrato e da ordem; o #3 é dono do resultado e da seed |
| #28 Save local | Hard | Resposta da marca (`Confirmado` ou `Falhou(causa)`), "marca encontrada" no boot | `BeginStage` (payload opaco), commit de fim de partida, efeito da marca no callback | O #28 é dono do formato e do commit; o #3 é dono do efeito |
| #5 Log de eventos | Hard (aceite) | Nada | Seed antes do tick 0, `StateHash` final, resultado com causa, `MorteSimultanea`, "abandonada", exceção | O #5 é dono do formato do log |
| #6 Combate e dano | Hard | Mortes do tick; HP do herói | `NiveisGanhos` na ficha, que o #6 lê para a cura do level-up (cursor `NiveisCurados` do #6); nenhuma chamada | O #6 é dono do dano, da vida e da cura |
| #7 Horda, waves e inimigos | Hard | O chefe com a marca `Essencial`; `xpDaMorte` por arquétipo; a lista de mortos do tick, com a causa; o cronograma de waves que termina com o chefe e o `tick_entrada_chefe_agendado`; os dados de onde o #1 soma o `xp_total_fase` | Nada | O #7 declara; o #3 lê |
| #16 Grimório e #9 Oferta | Hard | `CombatHold` (lido), serial de ofertas | Ficha de fase (`NiveisGanhos`, `ChefeVencido`), `IPreparaFase`, `IConcluiFase` | O #16 implementa; o #3 não o conhece |
| #4 Input e câmera | Soft | Nada | Visão somente leitura do estado | O #4 é dono da tradução do toque em comando |
| #12 Feedback de combate e HUD | Soft | Nada | Eventos e visões somente leitura (nível, XP, tempo restante do chefe) | O #12 desenha o aviso de tempo, o "toque para continuar" e a confirmação de abandono |
| #20 Campanha | Hard (no MVP: stub) | Nada | O resultado (causa, vitória, nível final) | O #20 é dono da ordem das fases; o #3 só entrega o resultado |
| #40 Auto-battle (Full Vision) | Soft (futuro) | O mesmo fluxo, com comandos de uma política | O mesmo resultado | O #40; nunca gera registro nem vitória para o K_min |

**Exigências feitas aos outros GDDs** *(todas provisórias, até o dono confirmar)*:
- **#28 (e ADR-0003):** (a) um `CancelStage` **nunca grava a marca**: se ele substitui um `BeginStage` que ainda espera, o substituto limpa a marca daquele `attemptId` (hoje o ADR-0003 faz o substituto herdar o tipo mais forte, e `StageMark` vence, então o Voltar gravaria a marca que devia limpar); (b) o `requestId` é **único entre todos os chamadores** (#3, #17): o #28 o emite, ou há uma fonte única compartilhada; (c) o `AttemptId` do resultado tem **128 bits** (hoje é `int` no ADR-0003); (d) um resultado por `requestId`, em qualquer ordem, entregue numa fila que a ponte esvazia na thread principal; (e) o callback nunca é dentro do `Tick`. A ordem não precisa ser FIFO: o retrato é inteiro e o #3 só pede o `BeginStage` seguinte depois da resposta do commit que limpou a marca anterior.
- **#2:** a FS9 passa a somar `ids_de_preparacao` (o #3 declara 1, o herói) em vez de "entidades iniciais"; a ficha de fase entra no `SimWorld`; a regra "os sistemas só conversam pelo `SimWorld`" vale **dentro do tick**, e fora dele o compositor chama as interfaces opcionais.
- **#7:** declara o `xpDaMorte`, marca o chefe como `Essencial` e entrega a lista de mortos do tick. A **interface mínima de leitura que o #3 exige** é: para cada morte do tick, o id, a facção, a causa (normal ou valor inválido) e o `xpDaMorte` inteiro, em ordem crescente de id, limpa em todo tick. A lista de mortos é o `DeathsThisTick` do `SimWorld` (ADR-0001), com a causa gravada por `Kill`; o `xpValue` está na linha do id (decidido no GDD #6, 2026-11-05).
- **#16:** guarda um cursor de ofertas já tratadas e implementa `IPreparaFase` e `IConcluiFase`.

*Consultados:* `systems-designer` (regras, estados, hash e a divisão dentro e fora do tick), `game-designer` (XP, estrutura da fase, resultados, retry, abandono e continue), `gameplay-programmer` (viabilidade, ganchos, tipos e criação do herói) e `engine-programmer` (ciclo de vida do Android e a espera do commit). Decisões do autor, 2026-11-04: XP direto na morte; derrota por tempo conta como morte; abandono conta só se o chefe já entrou; sem continue; seed nova a cada tentativa.

## Formulas

O #3 não define dano nem vida: as fórmulas abaixo são as regras numéricas do XP, do nível e do fim da fase. Os números de cada knob moram no #1 (com unidade e faixa segura); aqui está a forma.

**Regra transversal.** Nenhuma fórmula usa divisão: percentuais viram multiplicação (como a F3 do #1), então não há regra de arredondamento a definir. XP, nível e contagens são `int`; as contas intermediárias rodam em `long` e só o valor guardado volta a `int` (o mesmo critério da FS9 do #2). **Todo número de exemplo é ILUSTRATIVO**: a calibração é do protótipo. Os valores de `nivel_max`, da curva e do tempo máximo são **a calibrar**, e nenhum deles é balanceamento definitivo.

### F1. Limiar de XP por nível

The limiar_xp formula is defined as:

`limiar_xp(n) = xp_base + xp_inc × k + xp_quad × k × k`, com `k = n − 1`, para `1 ≤ n ≤ nivel_max − 1`

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| n | int | 1 a `nivel_max` − 1 | calculated | nível atual do herói |
| xp_base | int | ≥ 1 | data file (#1, knob do #3) | XP necessário para o 1º level-up |
| xp_inc | int | ≥ 1 | data file (#1, knob do #3) | acréscimo linear por nível |
| xp_quad | int | ≥ 0 (0 = curva linear) | data file (#1, knob do #3) | acréscimo quadrático por nível |
| nivel_max | int | ≥ 2; o #1 impõe um máximo e confere `nivel_max − 1 ≤ P − folga_pool` antes do laço da F5 | data file (#1, knob do #3) | teto de nível da fase |
| limiar_xp | int | 1 a 2³¹ − 1 | calculated | XP para ir de `n` a `n + 1` |

**Output Range:** de `xp_base` (em n = 1) a `limiar_xp(nivel_max − 1)`. Estritamente crescente: `limiar_xp(n+1) − limiar_xp(n) = xp_inc + xp_quad × (2k + 1) ≥ 1`, o que basta `xp_inc ≥ 1` e `xp_quad ≥ 0` garantirem. O #1 calcula `limiar_xp(nivel_max − 1)` em `long` e **recusa** o conjunto se passar de 2³¹ − 1 (nunca ajusta). Não existe limiar no teto.
**Example (ilustrativo):** `xp_base` = 10, `xp_inc` = 6, `xp_quad` = 1.

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| `limiar_xp(n)` | 10 | 17 | 26 | 37 | 50 | 65 | 82 | 101 | 122 |
| XP acumulado ao chegar a `n + 1` | 10 | 27 | 53 | 90 | 140 | 205 | 287 | 388 | 510 |

**Knobs criados:** `xp_base`, `xp_inc`, `xp_quad` e `nivel_max`. O primeiro level-up é cedo porque `xp_base` é o menor limiar da curva.

### F2. XP do tick

The xp_do_tick formula is defined as:

`xp_do_tick = Σ xpDaMorte[i]`, somado sobre as mortes **deste tick** com causa normal, em ordem crescente de índice

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| xpDaMorte[i] | int | ≥ 0 | data file (#7 declara por arquétipo, #1 valida) | XP do arquétipo morto |
| mortes | lista | 0 a a capacidade da lista de vivos | calculated | mortos do tick, por índice crescente |
| xp_do_tick | long | 0 a `capacidade de vivos × max(xpDaMorte)` | calculated | XP somado no tick |

**Output Range:** em `long` nunca estoura, porque cada entidade morre no máximo uma vez. Uma morte por **valor inválido** (Regra 9 do #2) vale 0 e não é erro; para isso o #3 precisa saber a **causa** da morte, então a lista de mortos do `SimWorld` (`DeathsThisTick`) a marca. `xpDaMorte < 0` é recusado no setup do #1 e de novo no `Preparar`, antes do tick 0, sem clamp em runtime e sem checagem dentro do tick. A soma de inteiros não depende da ordem; a ordem crescente só importa se algo emitir um evento por morte. A soma é feita **inteira antes** do laço de nível (F3).
**Example (ilustrativo):** mortes de 2, 2 e 5 XP e uma morte por valor inválido: `xp_do_tick` = 9.

### F3. Laço de nível

The laco_de_nivel formula is defined as:

```
xp = XpAtual + xp_do_tick                                  (long)
enquanto Nivel < nivel_max E xp ≥ limiar_xp(Nivel):
    xp -= limiar_xp(Nivel); Nivel += 1; NiveisGanhos += 1
se Nivel == nivel_max: xp = 0                              (descarte do excedente)
XpAtual = (int) xp
```

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| Nivel | int | 1 a `nivel_max` | calculated | nível atual (começa em 1 a cada tentativa) |
| XpAtual | int | 0 a `limiar_xp(Nivel)` − 1; 0 no teto | calculated | XP dentro do nível |
| NiveisGanhos | int | 0 a `nivel_max` − 1 | calculated | contador que o #16 lê (Regra 6) |
| xp_do_tick | long | F2 | calculated | XP que entra no tick |

**Output Range:** cada passo gasta ao menos `xp_base ≥ 1`, então o laço faz no máximo `nivel_max − 1` passos. Invariantes: fora do teto, `XpAtual < limiar_xp(Nivel)`; **no teto, `XpAtual = 0`**, para o hash ser canônico (o excedente descartado nunca fica guardado); e `NiveisGanhos = Nivel − 1` em toda tentativa (o contador é o contrato com o #16, e um teste verifica a igualdade). O #16 pode receber até `nivel_max − 1` ofertas em fila num único tick.
**Example (ilustrativo):** Nivel 3, `XpAtual` 20, `xp_do_tick` 60 → xp = 80; gasta 26 (sobra 54, Nivel 4); gasta 37 (sobra 17, Nivel 5); 17 < 50, para. Resultado: Nivel 5, `XpAtual` 17, `NiveisGanhos` +2. **No teto** (`nivel_max` = 10): Nivel 9, `XpAtual` 100, `xp_do_tick` 50 → xp = 150; gasta 122 (Nivel 10, o teto); `XpAtual` = 0 e os 28 de sobra são descartados.

### F4. Derrota por tempo e chefe ausente

The derrota_por_tempo formula is defined as:

`ticks_max_apos_chefe = F1 do #1 (duracao_max_apos_chefe_s)` e `derrota_por_tempo = ChefeVisto ∧ (CombatTick − TickDeEntradaDoChefe ≥ ticks_max_apos_chefe)`

e, para o caso em que o chefe nunca entra, `chefe_ausente = ¬ChefeVisto ∧ (CombatTick ≥ tick_entrada_chefe_agendado + ticks_max_apos_chefe)`

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| duracao_max_apos_chefe_s | decimal | segundos; a calibrar com o Tank | data file (#1, knob do #3) | tempo máximo depois que o chefe entra |
| ticks_max_apos_chefe | int | ≥ 1 | calculated (F1 do #1) | o mesmo tempo, em ticks; o #3 não reconverte, só lê o inteiro do snapshot |
| CombatTick | int | ≥ 0 | calculated (#2) | relógio da fase, parado durante oferta e pausa |
| TickDeEntradaDoChefe | int | ≥ 0 | calculated | `CombatTick` em que o #3 viu o chefe pela primeira vez (Regra 5.2) |
| tick_entrada_chefe_agendado | int | ≥ 0 | data file (#7 declara, #1 valida) | `CombatTick` em que o cronograma de waves põe o chefe |
| ChefeVisto | bool | verdadeiro ou falso | calculated | existe uma entidade `Essencial` inimiga na tabela de ids |

**Output Range:** booleanos. A prioridade da Regra 5.3 vale: se o chefe morre no tick do estouro, **a vitória vence**. `derrota_por_tempo` leva a `DerrotaTempo`, que **conta como morte de fase**. `chefe_ausente` leva a `FalhaInterna(ChefeAusente)`, que é bug nosso (dado errado ou `Spawn` rejeitado) e **não conta como morte**; ele reaproveita o teto do chefe como tolerância e não cria knob novo. O #1 também recusa um cronograma sem chefe (validação no setup); o guarda de runtime cobre o que a validação não alcança *(provisória)*. A soma `tick_entrada_chefe_agendado + ticks_max_apos_chefe` roda em `long` (os dois são `int` e a soma pode passar de 2³¹ − 1; em `int` ela viraria negativa e daria `ChefeAusente` no tick 1), e o #1 impõe um máximo ao tick agendado e à duração, além do `> 0`.
**Example (ilustrativo):** 90 s → `floor(90 × 30 + 0,5)` = 2700 ticks. Chefe entra no `CombatTick` 4000, então a derrota por tempo sai no 6700 (o `CombatTick` é o valor que o sistema vê, já incluído o tick atual: o tick 6699 não dá derrota e o 6700 dá). Se o chefe agendado era o 4000 e nunca nasceu, a `FalhaInterna(ChefeAusente)` sai também no 6700.

**Knob criado:** `duracao_max_apos_chefe_s`. Precisa ser folgado para o Tank (que mata devagar): é guarda contra travamento, não alavanca de dificuldade.

### F5. Teto de fase e níveis alcançáveis

The teto_de_fase_ok formula is defined as:

`acum(n) = Σ limiar_xp(m)`, para `m` de 1 a `n − 1`; `sem_teto` = o maior `n ≤ nivel_max` com `acum(n) ≤ xp_total_fase` (cortado no teto, para o domínio da F1, que vai até `nivel_max − 1`, bastar); `niveis_alcancaveis = sem_teto`

`teto_de_fase_ok = (niveis_alcancaveis − 1 ≤ P − folga_pool) ∧ (sem_teto = nivel_max) ∧ (acum(nivel_max) × 100 ≥ xp_total_fase × teto_xp_min_pct) ∧ (acum(nivel_max) × 100 ≤ xp_total_fase × teto_xp_max_pct)`

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| xp_total_fase | long | ≥ 0 | calculated (o #1 soma os dados do #7) | soma dos `xpDaMorte` dos spawns da fase, **sem o chefe** (a morte dele encerra a fase), em **duas pontas** da F9 do #7: `xp_max` (tudo o que pode nascer, com a escolta e o maior XP de cada pool) e `xp_min` (sem a escolta e com o menor XP de cada pool) |
| P | int | ≥ 1 | calculated (F4 do #1, `P_f + P_c`) | pool de skills ativas da função (5 de função + 5 compartilhadas = 10 no MVP); a checagem vale para cada função jogável naquela fase, com o menor P |
| folga_pool | int | ≥ 1 | data file (#1, knob do #3) | folga mínima entre os level-ups possíveis e o pool |
| teto_xp_min_pct | int | 1 a 100 | data file (#1, knob do #3) | porcentagem mínima do XP total em que o teto deve ser atingido |
| teto_xp_max_pct | int | `teto_xp_min_pct` a 100 | data file (#1, knob do #3) | porcentagem máxima do XP total em que o teto deve ser atingido |
| acum(n) | long | ≥ 0 | calculated | XP acumulado para chegar ao nível `n` |
| nivel_max, limiar_xp | int | F1 | data file / calculated | o teto e a curva |

**Output Range:** booleano, só inteiros, com laço de no máximo `nivel_max` passos no setup. É uma **checagem de setup** que o #1 aplica (como as F3 a F6 dele): falha recusa a fase, nunca ajusta. Ela impede dois erros: a build saturada (level-ups demais para o pool, o erro que o protótipo mostrou) e o teto que nunca é atingido, ou que é atingido cedo demais. `P` é `P_f + P_c` do F4 do #1, **não** o pool só da função (que seria 5). Se uma carta de level-up puder melhorar uma skill que o herói já tem, o limite real fica mais folgado: isso é do #9. A faixa `teto_xp_min_pct` a `teto_xp_max_pct` é uma leitura minha de "cedo demais" e "nunca atingido" *(provisória; a calibrar no protótipo)*.
**Quem declara:** o #7 declara os dados (spawns e `xpDaMorte`, as mesmas listas do `total_spawns` do FS9 do #2); o #1 calcula `xp_total_fase` e valida; o #3 é dono da fórmula. Calcular o total em vez de digitá-lo evita que ele desande.
**Duas pontas** *(emenda de 2026-11-05, `/consistency-check`, a pedido do GDD #7, F9)*: o #7 entrega o XP da fase como `xp_max` e `xp_min`, porque o pool de uma wave pode misturar arquétipos com XP diferente e a escolta do chefe depende da duração da luta. A checagem `teto_de_fase_ok` roda **duas vezes**, com `xp_total_fase = xp_max` e com `xp_total_fase = xp_min`, e a fase só passa se passar nas duas: o limite de level-ups contra o pool e o "cedo demais" pioram com `xp_max`; o "nunca atingido" piora com `xp_min`. A expressão da fórmula não muda.
**Example (ilustrativo):** P = 10, `folga_pool` = 1, `nivel_max` = 10, faixa de 60 a 90 %, `xp_total_fase` = 700. `acum(10)` = 510 ≤ 700, então `sem_teto` = 10 (cortado no teto) e `niveis_alcancaveis` = 10, com 9 level-ups ≤ 10 − 1. Também 51000 ≥ 700 × 60 e 51000 ≤ 700 × 90: o teto é atingido em 73 % do XP, então **passa**. Com `nivel_max` = 12: `sem_teto` = 11, `niveis_alcancaveis` = 11, 10 level-ups > 9, então **recusado**.

### F6. Contagem de vitórias para o K_min

O #3 **não define fórmula** aqui. O contador de vitórias de chefe de fase é do #16 (fatia do #28) e o #1 valida o estático (F5 do #1). A tabela de "conta como morte de fase" da Regra 8 é lógica booleana, já definida em Detailed Design.

### O herói e o total de spawns

O herói que o #3 cria na Regra 3.4 consome um id da tabela. A FS9 do #2 soma `ids_de_preparacao`, a soma do que cada `IPreparaFase` declara, mais as waves e as invocações (ajuste feito no #2 em 2026-11-04 e na emenda 6 do ADR-0001); o #3 declara **1** (o herói), como constante e não como knob. É o mesmo padrão de falha registrado em `docs/consistency-failures.md` (a capacidade de ids mede o total de spawns, não o pico). A lista de vivos e o hash não mudam. O retry cria uma simulação nova, então os ids não acumulam entre tentativas.

## Edge Cases

Cada caso diz a condição exata e o resultado exato. O que o #2 e o #28 já resolvem é citado, não repetido: herói e chefe morrendo no mesmo tick (Regra 13 do #2 e Regra 8 daqui); `FalhaInterna` coincidindo com vitória ou derrota (Regra 2, passo 6 do #2); e o app morrendo entre o commit de fim e a tela de registro (Regra 9.5 daqui).

### Tempo e pausa

- **Se um frame roda `n` ticks e o tick `k < n` encerra a simulação**: a ponte para o laço, drena os eventos e descarta os ticks que sobram, sem acumulá-los. Senão o `Tick` seguinte lança exceção (erro do host, Regra 14 do #2).
- **Se pausa, perda de foco ou a morte do app chega com a simulação já *Encerrada***: o fim já foi decidido dentro do tick. O host vai a *Concluindo* antes de olhar qualquer motivo de pausa; pausa em *Concluindo* ou *Resolvida* é ignorada, e o Android matar o app aí vira `AppFechado`.
- **Se há oferta pendente (`CombatHold` ≠ 0) quando o tempo máximo estouraria**: nada estoura. `CombatTick` e `CombatTick − TickDeEntradaDoChefe` usam o mesmo relógio e param juntos. No jogo, a fase pode ficar parada sem limite, porque não há tempo-limite de escolha (OQ-6 do #2). No teste sem tela, o runner tem um teto de `CurrentTick` (constante do teste, não do jogo), e estourá-lo é falha de teste, não um resultado de fase.
- **Se o tick em que sairia `DerrotaTempo` é o mesmo em que o herói subiria de nível**: vale `DerrotaTempo`, sem XP e sem nível (Regra 5.4), então nenhuma oferta nasce.
- **Se a tentativa fica pronta com um motivo de pausa já ativo** (o app foi para segundo plano durante a espera do commit): ela nasce *Pausada*, não *Em andamento*. A demora do commit não importa, porque a simulação não tem relógio e o primeiro `dt` é descartado. Não há portão de joystick na entrada, porque não há horda no tick 0 *(provisória)*.

### Fim da fase e resultado

- **Se o herói morre no tick em que o chefe nasce**: o passo 5.2 marca `ChefeVisto` e o 5.3 dá `DerrotaHeroi`, que conta como morte. Como o #7 roda antes do #6, o chefe poderia atacar no tick em que nasce: exigência ao #7, o primeiro ataque do chefe só vale a partir do tick seguinte.
- **Se o chefe nasce e morre no mesmo tick**: `ChefeVisto` vem da tabela de ids, então a vitória vale. O XP daquele tick se perde (Regra 5.4) e o nível final é o do tick anterior.
- **Se a leitura de `ChefeVisto` não filtra a facção**: o herói é `Essencial`, então `ChefeVisto` seria verdadeiro no tick 1 e a vitória sairia ali, porque nenhum inimigo `Essencial` estaria vivo. A regra é `Essencial` **e** facção inimiga, com teste de aceite "`ChefeVisto` é falso no tick 1".
- **Se há mais de um inimigo `Essencial`, ou nenhum**: no MVP há **exatamente 1** por fase, e o #1 recusa 0 ou 2 ou mais. `Essencial` só existe em spawn do cronograma, nunca em invocação nem em reviver (morto não reanima, Regra 7 do #2). Sem essa regra, com dois chefes nascendo em ticks diferentes, matar o primeiro daria vitória antes de o segundo nascer *(provisória; para 2 ou mais, o #7 declara `essenciais_declarados` e a vitória espera "nascidos igual a declarados")*.
- **Se um inimigo `Essencial` nasce no mesmo tick em que o chefe morre**: ele já está vivo quando o #3 avalia (o #7 roda antes), então não há vitória nesse tick.
- **Se a simulação sai *Quebrada***: `StateHash` lança depois de *Quebrada* (#2). O resultado leva hash, nível e `CombatTick` como "indisponível", o host guarda uma cópia da visão do último tick bom, e `IConcluiFase` é chamada com a causa `Quebrada` (o #16 não age).
- **Se o `Spawn` do chefe devolve −1**: a falha é do #2 (Regra 8), que a pede na hora; a tentativa termina como `FalhaInterna(ChefeAusente)` **no mesmo tick**, sem esperar o teto da F4, que cobre só cronograma sem chefe ou chefe atrasado. O #3 não detecta esse caso sozinho (OQ-2).

### XP e nível

- **Se morre o herói, um aliado ou uma invocação** (facção não inimiga): dá 0 XP. Só a morte de inimigo com causa normal soma (F2).
- **Se a lista de mortos do `SimWorld` (`DeathsThisTick`) não é limpa em todo tick**: o #3 não roda nos ticks com `CombatActive` falso, e a lista velha seria somada de novo. A lista é do tick atual e é limpa em **todo** tick.
- **Se saem `nivel_max − 1` ofertas em fila, ou o pool do #9 não tem 3 cartas**: o #3 só incrementa `NiveisGanhos`. Quem decide é o #9 (oferta com menos de 3 cartas) e o #16 (o cursor avança mesmo sem oferta possível). Exigência registrada ao #9 e ao #16, senão `CombatHold` = 1 sem carta trava o combate para sempre.
- **Se `nivel_max` = 2**: é válido, com uma única oferta. **Se `xp_base` é tão alto que ninguém sobe de nível**: a F5 recusa no setup, e no runtime zero level-ups é válido (o #3 não recalcula a F5).
- **Se `xp_total_fase` = 0 ou a fase não tem inimigos antes do chefe**: a F5 recusa, porque o teto nunca é atingido. Fase só de chefe não existe no MVP *(provisória; se um dia existir, entra uma exceção explícita `fase_sem_levelup`)*.
- **Se um knob chega ao runtime fora da faixa do #1** (`xp_base` < 1, `xp_inc` < 1, `xp_quad` < 0, `nivel_max` < 2, `ticks_max_apos_chefe` < 1, `xpDaMorte` < 0, ou limiar acima de 2³¹ − 1): é bug interno: o `Preparar` valida os knobs uma vez, incluindo o `xpDaMorte` de todo arquétipo do snapshot, e recusa antes do tick 0. O resultado é `FalhaInterna(DadosInvalidos)` (*Entrando* → *Concluindo*), sem clamp em runtime, e não há checagem de dado dentro do tick.

### Entrada, marca e retry

- **Se o retry é tocado duas vezes**: `Retry` só vale em *Resolvida*. A primeira chamada passa a *Entrando* de forma síncrona, antes de qualquer pedido assíncrono; em qualquer outro estado `Retry` é ignorado sem erro. Resultado: um `attemptId` e um `BeginStage`.
- **Se o jogador volta na espera da marca e entra de novo antes de o commit antigo responder**: a tentativa fica *Cancelando* e `Entrar` fica desabilitado, com o motivo na tela ("Gravando…"), até a resposta do commit de limpeza (`Confirmado` ou `Falhou`). O novo `BeginStage` só sai depois, e uma resposta com `requestId` diferente do pendente é ignorada. Em *Entrando* o `BeginStage` está sempre pendente (qualquer resposta dele já leva a *Em andamento*), então o Voltar sempre pede o commit de limpeza; em modo só leitura ele falha na hora e leva a *Cancelada*. A ponte esvazia a fila de respostas do #28 antes de processar a entrada do jogador no frame.
- **Se o commit de fim falha** (disco cheio): *Concluindo* vai a *Resolvida* mesmo assim. O resultado vale na sessão, o aviso é do #28 (regra 12 dele) e o retry é permitido; o `BeginStage` seguinte substitui a marca velha (Edge Cases do #28). Se o app morre antes, a vitória conta como app fechado (já resolvido no #28).
- **Se `Create` ou `Preparar` lança, ou o herói é inválido** (HP ≤ 0, NaN, `Spawn` −1): não existe tick 0. A tentativa vai a *Concluindo*(`FalhaInterna`), com hash "indisponível". O #3 pede o commit que limpa a marca antes de liberar o retry; isso não conta como morte e não tem retry automático. HP 0 nunca vira `DerrotaHeroi` no tick 1.
- **Se a marca do boot é de uma fase que o #1 não conhece** (update do app): `AppFechado` sem efeito, que não conta como morte, com o id desconhecido no log. Herói desconhecido: nada é contado. A causa "restaurado" já está resolvida (não é tentativa). **`Entrar` fica bloqueado até o callback "marca encontrada" retornar**, senão a marca velha seria sobrescrita pela nova e a tentativa se perderia.
- **Se o #16 ou o #28 não existem no teste sem tela**: o compositor só chama quem implementa a interface. Sem o #16, `NiveisGanhos` sobe, `CombatHold` nunca vira 1 e a fase corre. Sem o #28, um armazém nulo devolve "sem marca" (o mesmo caminho do modo só leitura). O #3 ausente do compositor é erro de host na montagem.
- **Se o auto-battle ou o teste sem tela tenta retry**: o retry é sempre um pedido explícito de quem chama. O runner pede N retries com seeds da lista do aceite, e o auto-battle nunca gera vitória para o K_min (#40).

### Abandono e app fechado

- **Se `ConfirmarAbandono` é chamado fora de *Pausada* com a confirmação aberta, ou uma segunda vez**: é ignorado e idempotente. O diálogo conta como motivo de pausa, então voltar o foco não o fecha.
- **Se vitória e abandono caem no mesmo frame**: não ocorre. A vitória sai de um `Tick`, o `Tick` não roda em *Pausada*, e se o `Tick` encerrou antes no frame o host já está em *Concluindo*.
- **Se o jogador abandona com oferta pendente**: vale, e conta como morte se `ChefeVisto`. **Se abandona no tick em que o chefe nasce**: `ChefeVisto` já é verdadeiro, sem janela de visibilidade *(provisória, aceita)*.
- **Se o Android mata o app durante o diálogo, ou em *Concluindo*(`Abandonada`) antes do commit**: vira `AppFechado` e não conta como morte. A janela é de milissegundos, risco aceito (#28).

### Capacidade e ids

- **Se um `IPreparaFase` cria entidades sem declará-las em `ids_de_preparacao`**: em modo estrito lança exceção; em modo não estrito `SpawnsRejected` sobe e vai ao log. O herói é sempre o primeiro `Spawn` (`IdDoHeroi` = 0), porque o #3 prepara primeiro, e a ordem dos `Preparar` faz parte do cabeçalho do log.

**Os três casos mais perigosos para o MVP:** (1) a fila de ofertas sem carta possível, que é um soft-lock (`CombatHold` = 1 sem carta; no teste sem tela vira loop infinito), cujo dono é o #16 e o #9; (2) a vitória falsa ou prematura (herói lido como chefe, ou dois `Essencial`), que contamina o K_min e o critério do Tank sem que nada trave; (3) a marca fantasma ou a tentativa dupla (retry duplicado, Voltar seguido de Entrar, commit de fim que falha, `Create` que lança), que distorce a contagem de mortes do aceite.

## Dependencies

### Upstream (o #3 depende de)

| Sistema | Natureza | O que o #3 lê | Observação |
|---|---|---|---|
| #1 Dados e balanceamento (GDD em revisão) | **Hard** | Snapshot imutável da fase, já em ticks; os knobs da curva de XP, `nivel_max`, `duracao_max_apos_chefe_s` (convertido pela F1 do #1) e os da checagem F5; a validação da F5 e a recusa de cronograma sem chefe ou com 2 ou mais | Sem snapshot válido a fase não começa. O #1 já cita o #3 (curvas de XP e regras da fase) |
| #2 Simulação determinística (GDD em revisão) | **Hard** | O contexto do tick (`CombatActive`, `CombatTick`, `Emit`), `Simulation.Create`, o `SimWorld` (ficha de fase, tabela de ids, marca `Essencial`) | O ADR-0001 ainda é *Proposed*; a ficha de fase e a FS9 pedem emenda (OQ-5 do #2) |
| #28 Save local (GDD em revisão) | **Hard** | `BeginStage` e a resposta do commit da marca, "marca encontrada" no boot, o commit de fim de partida | `CancelStage` nunca grava a marca, `requestId` único entre chamadores, `AttemptId` de 128 bits (exigências ao #28 e ao ADR-0003, Interactions) |
| #6 Combate e dano | **Hard** (GDD #6 de 2026-11-05) | Vida e morte do herói e dos inimigos; a causa de cada morte | O #6 lê `NiveisGanhos` da ficha para a cura do level-up (Regra 6), sem chamada do #3; ajuste pendente na Regra 15 do #6 |
| #7 Horda, waves e inimigos | **Hard** (contrato provisório, sem GDD) | O chefe com a marca `Essencial`; `xpDaMorte` por arquétipo; o cronograma e o `tick_entrada_chefe_agendado`; os dados de onde o #1 soma o `xp_total_fase`; a lista de mortos do tick (o dono, #6 ou #7, sai no ADR deles) | Não há ciclo: o #7 depende de 1, 2 e 6 |

**Decisões externas que o #3 respeita:** o ADR-0001 (*Proposed*: `ISimSystem` em `Forja.Gameplay.Sim`, sem engine, float32, 30 Hz, sem `static` mutável); o conceito congelado (`game-concept.md`, exceto a linha 120, ver Open Questions); e o modelo de negócio (R6 veta o revive por vídeo durante a partida; a regra de que não existe nenhuma forma de continue é a Regra 8 daqui).

### Downstream (dependem do #3)

Nenhum destes GDDs existe ainda; **todo contrato abaixo é provisório** até o GDD dono confirmá-lo. A coluna "No índice" diz se `systems-index.md` já lista o #3 na coluna Depends On do sistema.

| Sistema | Natureza | O que flui | No índice |
|---|---|---|---|
| #16 Grimório | **Hard** | Lê a ficha de fase (`NiveisGanhos`, `ChefeVencido`); implementa `IPreparaFase` e `IConcluiFase`; escreve o `CombatHold` | sim |
| #9 Oferta de cartas | **Hard** | O nível e o contador de level-ups chegam pelo #16; o #9 decide a oferta com menos de 3 cartas | sim |
| #20 Campanha | **Hard** (no MVP: stub) | O resultado da tentativa (causa, vitória, nível final) | sim |
| #4 Input e câmera | **Soft** | Visão somente leitura do estado da fase; a ponte lê o resultado | sim |
| #40 Auto-battle (Full Vision) | **Hard** | O mesmo fluxo, com comandos de uma política; nunca gera vitória para o K_min nem registro | sim |
| #12 Feedback de combate e HUD | **Soft** | Eventos e visões (nível, XP, tempo restante do chefe); a tela de abandono e o "toque para continuar" | **não** (acrescentar) |
| #5 Log de eventos | **Soft** (aceite) | Seed antes do tick 0, `StateHash` final, resultado com causa, `MorteSimultanea`, "abandonada", exceção | **não** (acrescentar) |

### Bidirecionalidade e ajustes pendentes em outros documentos

Nenhum destes foi editado por este GDD (um GDD não altera outro sem aprovação do autor):

- **`systems-index.md`:** (a) acrescentar #6 e #7 (Hard) à coluna Depends On do #3, hoje "1, 2, 28"; (b) o Dependency Map (linha 213) diz "2, 28" e deve acompanhar a tabela; (c) acrescentar o #3 (Soft) ao #5 e ao #12. *(feito em 2026-11-04, com a aprovação do autor; o #7 entrou como "interface" porque é Feature: o #3 define a leitura e o #7 a cumpre, sem ciclo)*
- **#1 Dados e balanceamento:** acrescentar os knobs do #3 (`xp_base`, `xp_inc`, `xp_quad`, `nivel_max`, `duracao_max_apos_chefe_s`, `folga_pool`, `teto_xp_min_pct`, `teto_xp_max_pct`), o `xp_total_fase`, a checagem F5 e a recusa de cronograma sem chefe ou com 2 ou mais.
- **#2 Simulação:** a ficha de fase no `SimWorld` (OQ-5; o hash dela é do `Hash` do #3, e a Regra 10 e a FS8 não mudam); a FS9 somando `ids_de_preparacao`; a Regra 5 valendo "só pelo `SimWorld`" **dentro do tick**; a linha *Quebrada* da tabela de estados ("falha sem derrota"); o `Spawn` de preparação sem evento; e **fechar as OQ-2, OQ-3, OQ-7, OQ-10 e OQ-12**, que este GDD resolve. *(feito em 2026-11-04, com a aprovação do autor, exceto a ficha de fase, que fica na OQ-5 do #2 até a emenda do ADR-0001)*
- **#28 Save local e ADR-0003:** `CancelStage` nunca grava a marca; `requestId` único entre chamadores; `AttemptId` de 128 bits; callback fora do `Tick`; o payload opaco do #3 é vazio no MVP.
- **#6 Combate e dano:** a Regra 15 passa a ler `NiveisGanhos` com um cursor `NiveisCurados` no `Hash` do #6, em vez de receber `Curar` do #3; tirar o "BLOQ: emenda do #3" do R15 do #6; o edge case da oferta adiada pelo aviso de golpe (Regra 16 do #6) quando a fase termina antes de ela abrir.
- **ADR-0001, emenda 14:** o `Preparar` grava a ficha inteira (não só o `IdDoHeroi`), e o `PhaseSheet` ganha `MotivoFim`.
- **#7 Horda:** `xpDaMorte`, `Essencial` no chefe (exatamente 1), `tick_entrada_chefe_agendado`, a lista de mortos com causa limpa a cada tick, e o primeiro ataque do chefe só no tick seguinte ao nascimento.
- **#16 Grimório e #9 Oferta:** o cursor de ofertas tratadas; `IPreparaFase` e `IConcluiFase`; não abrir oferta quando o contexto traz um pedido de fim; a fila de ofertas sem carta possível (soft-lock); o registro no Grimório depois do fim, como segundo commit.
- **ADR-0001 (via `/architecture-decision`):** a ficha de fase, as interfaces `IPreparaFase` e `IConcluiFase`, o caminho de escrita da marca `Essencial` fora do tick, a coluna `xpDaMorte` e a lista de mortos do tick.
- **Conceito (`game-concept.md`, congelado):** a linha 120 ("coleta orbes de XP") pede emenda, porque o XP é direto.

## Tuning Knobs

Os knobs do #3 **moram no #1** (que guarda o valor, a unidade e a faixa segura); o significado e a faixa proposta são deste GDD. **Nenhum recebe valor padrão aqui**: todos são "a calibrar no protótipo" (o balanceamento definitivo não é decidido num GDD), e a faixa segura abaixo é a *forma* que o #1 valida, não um número de jogo. Nenhum é remoto no MVP; no pós-lançamento a lista branca do #29 decide quais podem mudar, sempre entre partidas.

| Knob | Padrão | Faixa segura | Remoto | Afeta | Baixo demais | Alto demais |
|---|---|---|---|---|---|---|
| `xp_base` (F1) | a calibrar | inteiro ≥ 1 | não | XP do 1º level-up; quão cedo vem a primeira escolha | o 1º level-up vem no primeiro segundo e a escolha perde peso | a primeira escolha demora e a fase começa sem build |
| `xp_inc` (F1) | a calibrar | inteiro ≥ 1 | não | quanto cada nível custa a mais que o anterior (parte linear) | os level-ups ficam colados e a fase vira uma fila de ofertas | o fim da fase fica sem level-up e o teto é inalcançável |
| `xp_quad` (F1) | a calibrar (0 = curva linear) | inteiro ≥ 0 | não | a parte quadrática: quanto a curva acelera nos níveis altos | a curva é linear e os últimos níveis chegam cedo demais | os níveis finais ficam inalcançáveis; o limiar de `nivel_max − 1` pode passar de 2³¹ − 1 (o #1 recusa) |
| `nivel_max` (F1, F3, F5) | a calibrar | inteiro ≥ 2; o limite superior é a F5 (level-ups possíveis ≤ `P` − `folga_pool`) | não | teto de nível da fase e o número máximo de ofertas por tentativa | poucas escolhas por fase (2 dá uma só) | uma tentativa consegue quase todas as skills do pool e o Grimório vira "quase tudo" (o erro do protótipo) |
| `duracao_max_apos_chefe_s` (F4) | a calibrar com o Tank | segundos, > 0, convertidos em ticks pela F1 do #1 (recusado se der menos de 1 tick) | não | quanto tempo o jogador tem para vencer o chefe depois que ele entra | derrota por tempo injusta; o Tank, que mata devagar, passa a morrer de relógio e estoura o critério de aceite (≤ 2 mortes de fase) | o chefe vira corrida de resistência e o teste sem tela demora mais para fechar uma fase travada |
| `folga_pool` (F5) | a calibrar | inteiro ≥ 1 | não | quantas skills do pool a tentativa não consegue pegar, no mínimo | a tentativa pode pegar quase todo o pool | a F5 recusa fases legítimas com muitos level-ups |
| `teto_xp_min_pct` (F5) | a calibrar | 1 a 100 | não | a fração mínima do XP total da fase em que o teto de nível deve ser atingido | o teto é atingido cedo demais e o XP do resto da fase é descartado | a F5 recusa fases em que o teto chega com folga |
| `teto_xp_max_pct` (F5) | a calibrar | `teto_xp_min_pct` a 100 | não | a fração máxima do XP total em que o teto deve ser atingido | a F5 recusa quase tudo | o teto quase nunca é atingido e os últimos níveis são letra morta |

**Knobs de outros GDDs que o #3 consome (sem duplicar):** `xpDaMorte` por arquétipo e o cronograma de waves (#7), `P = P_f + P_c` (#1, F4 do #1), `replay_limit` (#1, F5 do #1: quantos replays contam vitória para o K_min), `K_min` (#16 e #17) e as capacidades (#1, F3 do #1). O `MaxTicksPerFrame` (#2) não passa pelo #3.

**Constantes deliberadas (não são knobs):** `ids_de_preparacao` = 1 (o herói); o nível inicial é 1 e o XP inicial é 0; o MVP tem exatamente 1 inimigo `Essencial` por fase; a prioridade `FalhaInterna` > `Vitoria` > `DerrotaHeroi` > `DerrotaTempo`; a seed nova a cada tentativa (decisão do autor); e `NiveisGanhos = Nivel − 1`. Mudar qualquer uma delas é decisão de design, não ajuste de balanceamento.

**Interações entre knobs:**
- `xp_base`, `xp_inc`, `xp_quad` e `nivel_max` só significam algo juntos, junto com o `xp_total_fase` que o #7 declara: a F5 os valida em conjunto. Subir um deles sem rever os outros costuma estourar a F5, e o ajuste certo é na curva ou no XP dos inimigos, não no teto da F5.
- `duracao_max_apos_chefe_s` × a velocidade de morte do chefe do Tank: o valor é calibrado no Tank, porque o DPS vai bem em qualquer valor razoável e o Tank é o caso em que a derrota por tempo pode distorcer o critério de aceite.
- `nivel_max` × `folga_pool` × `P`: aumentar o pool de skills (mais skills ativas) abre espaço para subir `nivel_max`, sem tocar a F5.
- **Este bloco não muda o determinismo**: todos são lidos uma vez do snapshot. Eles mudam o que a fase *calcula*, mas a mesma seed, os mesmos comandos e os mesmos dados dão sempre o mesmo resultado (Regra 12 do #2).

## Visual/Audio Requirements

O #3 é lógica pura e **não tem arte nem áudio próprios**: não há asset a especificar, então nenhum `/asset-spec` sai deste GDD. Ele só emite os eventos que a apresentação (#12) usa: `FaseIniciada`, `LevelUp`, `ChefeEntrou`, `ChefeVencido` e `FaseEncerrada`. Duas exigências de leitura para o #12, pelo P4 e pelo P2:
- Cada causa de resultado precisa de um retorno visual e sonoro **distinguível**: vitória, vitória em que herói e chefe caem juntos (continua sendo vitória), derrota, derrota por tempo, abandono, e as falhas que **não são derrota** (`AppFechado`, `FalhaInterna`, `Quebrada`). Essas últimas não podem soar como derrota: o jogador não a causou.
- O orbe de XP é um efeito puramente visual que voa até o herói (Regra 6); ele não existe no estado da simulação.

*`art-director` não consultado: sistema Core sem superfície visual própria. Revisar quando o GDD do #12 for escrito.*

## Game Feel

O #3 não tem alvo de feel próprio (a responsividade do toque é do #4, e o congelamento e a retomada do level-up são do #2 e do #16). Três pontos qualitativos que o #12 e o #4 devem honrar, **sem número** (a calibrar com o autor no protótipo):
- Uma vitória em que herói e chefe caem no mesmo golpe tem de **parecer vitória**.
- O caminho da tela de resultado até o retry não tem fricção extra (é o que o teste de acerto PT1 observa).
- A derrota por tempo tem de ser explicável: o jogador vê o tempo restante do chefe antes de perder por ele.

## UI Requirements

O #3 não desenha telas. Ele **expõe** o estado por uma visão somente leitura (AC-UI1) e os eventos, e estas são as necessidades de tela que ficam para os GDDs e specs dos donos:

| Tela ou elemento | Dono | O que o #3 exige que ela mostre ou faça |
|---|---|---|
| HUD de combate | #12 | Nível, barra de XP, e o **tempo restante do chefe** (só depois que ele entra, nunca negativo); o tempo não pode depender só de cor |
| Menu de pausa | #12 | Continuar e Abandonar; o abandono pede **confirmação em 2 passos** ("Perde esta tentativa. Abandonar?") |
| Retomada | #12 | O aviso "toque para continuar" (decisão do #2) |
| Tela de carregamento da fase | #12 e #28 | Indicador da espera do commit da marca, "ainda gravando…" depois do tempo do #28, e o botão Voltar |
| Tela de resultado | #12 e #20 | Texto próprio por causa (vitória, derrota, tempo esgotado, abandonada, e as falhas que não são derrota), **Retry** e Sair; em vitória, segue para a tela de registro do #16 |
| Aviso de "app fechado" ao abrir | #12 e #28 | Informa que a fase se perdeu **sem contar como derrota** |

> **📌 UX Flag — Fluxo de fase**: este sistema tem requisitos de UI. Na Pré-Produção, rode `/ux-design` para criar a spec de cada tela ou elemento acima **antes** de escrever épicos; as stories de UI citam `design/ux/[tela].md`, não este GDD. O pré-requisito `design/accessibility-requirements.md` ainda não existe (OQ-3 do #28).

*`ux-designer` não consultado: a UI é de dono externo (#12, #20, #28) e ainda sem GDD.*

## Cross-References

| Este documento referencia | Documento | Elemento | Natureza |
|---|---|---|---|
| Ordem dos sistemas #7 → #8 → #6 → #3 → #16 | `simulacao-deterministica.md` (#2) | Regra 5 | Regra de ordem (provisória) |
| `CombatHold` e `CombatTick`, congelamento da oferta e retomada no toque | `simulacao-deterministica.md` (#2) | Regras 11 e 15 | Relógio e estado do #16 |
| Vitória vale sobre a derrota; `FalhaInterna` vence as duas | `simulacao-deterministica.md` (#2) | Regras 2 (passo 6) e 13 | Regra de resultado |
| Marca `Essencial`, valor inválido, `Spawn` rejeitado | `simulacao-deterministica.md` (#2) | Regras 8 e 9 | Regra de erro |
| Total de spawns e capacidade de ids | `simulacao-deterministica.md` (#2) | FS9 (`capacidade_ids_ok`) | Fórmula (ajuste pedido) |
| `Simulation.Create`, modo estrito, estados *Quebrada* e *Encerrada* | `simulacao-deterministica.md` (#2) | Regras 1, 14 e Estados | Contrato |
| Marca "fase em andamento", `attemptId`, payload opaco, app fechado sem morte | `save-local.md` (#28) | Regra 6 | Contrato e decisão do usuário |
| Pontos seguros de gravação, nunca durante a fase | `save-local.md` (#28) | Regra 5 | Regra |
| A fase começa sem marca quando o commit falha | `save-local.md` (#28) | OQ-4 | Decisão por recomendação, a reavaliar |
| Conversão de segundos em ticks | `dados-e-balanceamento.md` (#1) | F1 (`duracao_ticks`) | Fórmula (reutilizada, não repetida) |
| Pool de skills `P = P_f + P_c` | `dados-e-balanceamento.md` (#1) | F4 (`grimorio_setup_ok`) | Fórmula (variável usada na F5) |
| `replay_limit` e K_min | `dados-e-balanceamento.md` (#1) e `game-concept.md` | F5 do #1; K_min = 7 | Valor e fórmula |
| Critério do Tank (≤ 2 mortes de fase) e "morte é uma tentativa que termina sem vencer o chefe" | `game-concept.md` | MVP Definition (L405) | Critério de aceite |
| XP por orbe | `game-concept.md` | Core Loop (L120) | **Emenda pedida** (OQ-1) |
| Revive por vídeo vetado durante a partida (a regra completa de "sem continue" é a Regra 8 daqui) | `business-model.md` | R6 | Princípio de Negócio |
| `ISimSystem`, compositor, `Simulation`, três asmdefs, sem `static` mutável | ADR-0001 | Decisão e Key Interfaces | Decisão técnica (*Proposed*) |

## Acceptance Criteria

**Convenções.** Os IDs valem só neste GDD ("#3 AC-R3"). Os testes ficam em `Assets/Tests/EditMode/FluxoDeFase/[Classe]Tests.cs`, com método `Cenario_Esperado`, e todo teste afirma `testcasecount > 0`, para não passar vazio. Fixtures vêm de arquivo constante ou de função de fábrica. Dublês: `FakeSistema` (roteirizado: mortes, `Essencial`, `CombatHold`), `FakeSave` (espião do #28, com portão manual e `CommitCount`), `FakeSeed`, `FakeId` (contador), `FakeGrimorio` (`IPreparaFase` e `IConcluiFase` espiões) e `FakeLog`. Tipos de teste: **[U]** unitário EditMode; **[I]** integração com uma `Simulation` real e dublês; **[PM]** playtest manual do autor (n = 1) ou medição no aparelho; **[R]** revisão de documento ou de processo. Cada critério é **PRONTO** por padrão; quando não é, leva **BLOQ: motivo**, e BLOQ conta como não aprovado. Os exemplos numéricos das Formulas são ilustrativos e valem aqui como casos de teste.

### Regras (AC-R)

- **R1 [U]** **GIVEN** uma tentativa *Resolvida* (Nível 5, XP 17), **WHEN** `Retry`, **THEN** a nova `Simulation` tem `CombatTick` 0, Nível 1, XP 0, `NiveisGanhos` 0 e um `attemptId` novo; chamar `Tick` na simulação antiga lança.
- **R2 [U]** **GIVEN** o `SistemaFluxoDeFase` e a `TentativaDeFase`, **WHEN** inspecionados por reflexão, **THEN** nenhum tem campo `static` mutável; duas `TentativaDeFase` no mesmo processo dão o mesmo hash que cada uma isolada.
- **R3a [I]** **GIVEN** um snapshot válido, **WHEN** a tentativa entra na fase, **THEN** o espião registra, nesta ordem: gerar `attemptId` e `requestId`, `BeginStage` (payload vazio), espera, seed, seed no log, `Create`, `Preparar` do #3 primeiro, *Em andamento*.
- **R3b [I]** **GIVEN** o `BeginStage` pendente (portão manual fechado), **THEN** a chamada retorna com `Estado` = *Entrando* e o `Create` tem 0 chamadas.
- **R3c [I]** `Falhou` ou "sem marca" levam a *Em andamento* sem marca; snapshot inválido faz 0 chamadas.
- **R3d [I]** O herói tem `IdDoHeroi` 0, `Essencial`, HP e posição do snapshot, e o `Spawn` de preparação não emite evento.
- **R4 [U]** **GIVEN** a curva `xp_base` 10, `xp_inc` 6, `xp_quad` 1, `nivel_max` 10, `CombatHold` sempre 0 (então `CombatTick` = tick) e este roteiro, **THEN** a ficha (Regra 4) assume os valores da tabela, e `NiveisGanhos` nunca decresce:

  | Tick | Entrada | Nivel | XpAtual | NiveisGanhos | ChefeVisto | TickDeEntradaDoChefe | ChefeVencido | IdDoChefe | EssenciaisInimigosVivos | MotivoFim |
  |---|---|---|---|---|---|---|---|---|---|---|
  | 0 (depois do `Preparar`) | nenhuma | 1 | 0 | 0 | falso | −1 | falso | −1 | 0 | nenhum |
  | 5 | morrem inimigos de 2, 2 e 5 XP | 1 | 9 | 0 | falso | −1 | falso | −1 | 0 | nenhum |
  | 6 | morre 1 inimigo de 2 XP | 2 | 1 | 1 | falso | −1 | falso | −1 | 0 | nenhum |
  | 9 | o chefe nasce (id `B` do fixture) | 2 | 1 | 1 | verdadeiro | 9 | falso | `B` | 1 | nenhum |
  | 20 | o chefe morre, com mortes de 100 XP no mesmo tick | 2 | 1 | 1 | verdadeiro | 9 | verdadeiro | `B` | 0 | `Vitoria` |

  O `IdDoHeroi` é 0 e `MorteSimultanea` é falso em todas as linhas; `ProximoIdAVer` é 1 no tick 0 e, ao fim de cada tick, igual ao `IdCount` do `SimWorld`. A linha do tick 0 é a ficha inteira gravada pelo `Preparar` (Regra 4), antes de qualquer `Tick`. No tick 20 o pedido de fim é `Vitoria` e o XP do tick se perde (Regra 5.4).
- **R5 [U]** (a) **GIVEN** `CombatActive` falso com 3 mortes na lista, **THEN** a ficha e o hash ficam iguais antes e depois do passo. (b) **GIVEN** um chefe que nasce e morre no mesmo tick, **THEN** a vitória vale. (c) **GIVEN** 100 XP que dariam nível no tick do fim, **THEN** Nível e `NiveisGanhos` ficam os do tick anterior.
- **R6 [U]** **GIVEN** mortes de inimigo comum, de aliado, de invocação, do herói e uma por valor inválido, **THEN** só a de inimigo comum soma XP; XP e level-ups continuam com o chefe vivo; dois level-ups no mesmo tick dão `NiveisGanhos` +2.
- **R6b [I]** Cura no level-up (Regra 6), num compositor [#6 real ou um falso que implementa o cursor, #3, #16 falso], com `cura_levelup_pct` 0,25 e `hpMax` 100: (a) **GIVEN** 2 level-ups no tick T e herói com HP 40, **THEN** no tick T+1 o HP é 90 (limitado a `hpMax`) e `NiveisCurados` = `NiveisGanhos`; (b) **GIVEN** o #16 falso abre a oferta em T e a carta só sai em T+50, **THEN** o HP não muda de T a T+50 e sobe no 1º tick ativo depois da carta; (c) **GIVEN** duas execuções iguais exceto por `NiveisCurados`, **THEN** o `StateHash` difere; (d) no tick do fim e no teto (`nivel_max`) não há cura; (e) por reflexão e espião, o #3 não chama nenhum método do #6. O HP aplicado com o #6 real fecha no I4.
- **R7 [U]** Tempo: ver F4. **GIVEN** oferta pendente (`CombatHold` = 1) por 100.000 `Tick` seguidos, **THEN** o delta de `CombatTick` é 0, nenhum pedido de fim sai e a ficha fica igual à do 1º tick retido.
- **R8:** ver a tabela AC-X.
- **R9 [I]** **GIVEN** uma vitória, **THEN** a ordem registrada é: hash, `IConcluiFase`, descarte, commit de fim, evento ao #5; com portão manual o evento não sai antes de `Confirmado`. Em `Quebrada`, `StateHash` lança e o resultado traz hash, nível e `CombatTick` como "indisponível". O registro do Grimório é um segundo commit, nunca um `PickOffer`; `Tick` depois do fim lança.
- **R10 [U]** Dois `Retry` seguidos geram 1 `attemptId` e 1 `BeginStage`; `Retry` em *Em andamento* é ignorado sem erro; depois de `AppFechado`, `FalhaInterna` e `Quebrada` o número de `BeginStage` fica 0 até o pedido explícito; o novo `BeginStage` só sai depois do commit que limpou a marca.
- **R11 [U]** Com 2 motivos de pausa e 1 encerrado, segue *Pausada* (0 `Tick`); o 1º `dt` depois de pausa ou do carregamento é descartado; a tentativa pronta com motivo ativo nasce *Pausada*; a pausa não grava (`CommitCount` igual); pausa em *Concluindo* ou *Resolvida* é ignorada; com um `FakeRelogio` que avança 600 s durante a pausa, 0 `Tick` são chamados e o `StateHash` depois de N ticks é igual ao de uma execução sem pausa (a classe sob teste é a ponte de tempo, função pura da FS1 do #2).
- **R12 [U]** `PedirAbandono` mantém a pausa e cancelar volta; `ConfirmarAbandono` fora de *Pausada* com a confirmação aberta, ou repetido, é ignorado; ele roda 0 `Tick`; com `ChefeVisto` falso o resultado é `Abandonada` e não conta como morte, com `ChefeVisto` verdadeiro conta; vale com oferta pendente.
- **R13 [U]** Marca "app fechado": `AppFechado`, 0 morte, 0 retry automático, efeito vazio devolvido no callback. Marca "restaurado": não é tentativa. Fase desconhecida: `AppFechado` sem efeito e sem morte, com o id no log. Herói desconhecido: nada é contado e nenhum resultado é criado. `Entrar` fica bloqueado até o callback retornar.
- **R14 [U]** Valor inválido num `Essencial`: `FalhaInterna`. Exceção no `Tick`: `Quebrada`. Nenhum dos dois conta morte nem dá recompensa. Snapshot inválido não cria nada.
- **R15 [I]** Os três ganchos disparam como na Regra 15: `Preparar` 1× antes do tick 0; `NiveisGanhos` lido pelo fixture do #16 igual a `Nivel − 1` ao fim de cada tick; `IConcluiFase` 1× por tentativa, com a causa. Os 5 eventos saem: `FaseIniciada` 1×, `LevelUp` uma vez por nível ganho (com o nível novo), `ChefeEntrou` 1×, `ChefeVencido` 1× só em `Vitoria`, `FaseEncerrada` 1× no tick do fim; `FaseEncerrada` sobrevive a um buffer cheio (reserva). Por reflexão, nenhum membro do contexto do tick devolve `Events` (evento não é canal entre sistemas; *provisória*, depende da forma do `SimContext`, OQ-2).
- **R16 [U]** Mudar um campo da ficha, `ChefeVisto`, `TickDeEntradaDoChefe`, `ProximoIdAVer`, `IdDoChefe`, `EssenciaisInimigosVivos`, o pedido de fim ou `MorteSimultanea` muda o `StateHash`; mudar `attemptId`, estado fora do tick ou contador de diagnóstico não muda.
- **R17 [U]** Por reflexão e varredura de código: o assembly de simulação tem `noEngineReferences`; nenhum tipo do #3 usa `System.Random`, `UnityEngine` ou `double`; nenhum tipo do namespace do #3 referencia tipo do namespace do #16 (os dois ficam no mesmo assembly, ADR-0001, então o asmdef não os separa); os únicos literais de gameplay permitidos são `ids_de_preparacao` = 1, nível inicial 1 e XP inicial 0.

### Tabela de resultados (AC-X), cada linha [U]

| ID | GIVEN / WHEN | THEN |
|---|---|---|
| X1 | Chefe morto, herói vivo | `Causa` = `Vitoria`; `ContaComoMorteDeFase` falso |
| X2 | Herói morre, chefe vivo | `DerrotaHeroi`; `ContaComoMorteDeFase` verdadeiro |
| X3 | Estouro do tempo do chefe | `DerrotaTempo`; `ContaComoMorteDeFase` verdadeiro |
| X4 | Abandono com e sem `ChefeVisto` | `Abandonada`; `ContaComoMorteDeFase` verdadeiro só com `ChefeVisto` |
| X5 | Marca com causa "app fechado" | `AppFechado`; `ContaComoMorteDeFase` falso |
| X6a | Valor inválido num `Essencial` | `FalhaInterna`; `ContaComoMorteDeFase` falso |
| X6b | `Spawn` do chefe = −1: um `FakeSistema` encerra com `InternalFailure` e `EndDetail` = `EssentialSpawnRejected` (ADR-0001, emenda 6) | `FalhaInterna(ChefeAusente)` no mesmo tick, sem esperar o teto; `ContaComoMorteDeFase` falso |
| X7 | Exceção no `Tick` | `Quebrada`; `ContaComoMorteDeFase` falso; hash "indisponível" |
| X8 | Voltar na espera, ou marca "restaurado" | `Cancelada` ou `Restaurado`: não é tentativa e não chega ao #20 |
| X9 | Herói e chefe morrem no mesmo tick | `Vitoria` com `MorteSimultanea` verdadeiro; `ContaComoMorteDeFase` falso |
| X10 | Os 6 pares de fins válidos no mesmo tick (`FalhaInterna` × `Vitoria`, × `DerrotaHeroi`, × `DerrotaTempo`; `Vitoria` × `DerrotaHeroi`, × `DerrotaTempo`; `DerrotaHeroi` × `DerrotaTempo`) | vale a causa de maior prioridade: `FalhaInterna` > `Vitoria` > `DerrotaHeroi` > `DerrotaTempo` |

Cada linha afirma `Resultado.Causa`, `Resultado.ContaComoMorteDeFase(causa, chefeVisto)` e que o `IConcluiFase` é chamado 1 vez com essa causa. K_min, Grimório e campanha são o que o #16 e o #20 fazem com a causa (Regra 8): o #3 só afirma a causa e a função.

- **X11 [R]** O aceite do MVP (`docs/acceptance/mvp.md`) registra como sinais à parte, todos observáveis no log do #5, `DerrotaTempo`, `MorteSimultanea`, `Abandonada` sem `ChefeVisto`, `AppFechado` (o total; a marca não guarda `ChefeVisto`, então não dá para separar o app fechado no chefe, OQ-18), `FalhaInterna` e `Quebrada`, e **fixa, antes do D0, um pior valor para cada um** (a métrica do Tank não pode passar por construção, L402 do conceito). Manda revisar `duracao_max_apos_chefe_s` antes de julgar o Tank se alguma morte de fase do Tank for `DerrotaTempo`. `duracao_max_apos_chefe_s` e `cura_levelup_pct` (#6) ficam **congelados antes do D0**: alterar qualquer um depois de ver o resultado do Tank reinicia a medição com um novo commit do build. **BLOQ: `mvp.md`, que ainda não existe.**

### Fórmulas (AC-F), todos [U]

- **F1** (a) **GIVEN** `xp_base` 10, `xp_inc` 6, `xp_quad` 1, **THEN** `limiar_xp(1..9)` = 10, 17, 26, 37, 50, 65, 82, 101, 122 e o acumulado = 10, 27, 53, 90, 140, 205, 287, 388, 510. (b) Para `nivel_max` = 100, uma varredura confirma `limiar(n+1) − limiar(n) = xp_inc + xp_quad × (2k + 1) ≥ 1`, incluindo o caso mínimo (`xp_inc` 1, `xp_quad` 0). (c) Limiar acima de 2³¹ − 1: o `Preparar` recusa com `FalhaInterna(DadosInvalidos)`, nunca faz clamp.
- **F2** Mortes de 2, 2 e 5 mais uma por valor inválido dão 9; sem mortes dá 0; três mortes com `xpDaMorte` = 2³¹ − 1 somam em `long` sem estourar.
- **F3** Nível 3, XP 20, +60 dá Nível 5, XP 17, +2. `nivel_max` 10, Nível 9, XP 100, +50 dá Nível 10, XP 0, +1. No limite exato (`xp` = `limiar`) sobe e `XpAtual` = 0. Uma varredura em grade fixa (sem aleatório) sobre (Nível, XP, ganho) afirma: `XpAtual < limiar` fora do teto, `XpAtual` = 0 no teto, `NiveisGanhos = Nivel − 1`, no máximo `nivel_max − 1` passos, e XP conservado fora do teto. `nivel_max` = 2 dá uma só oferta; XP 0 não muda nada.
- **F4** **GIVEN** o chefe entra no `CombatTick` 4000 e o teto é de 2700 ticks, **THEN** no tick 6699 não há derrota e no 6700 há `DerrotaTempo`; se o chefe morre no 6700, a vitória vale. Chefe agendado no 4000 e nunca nascido: `FalhaInterna(ChefeAusente)` no 6700, sem contar morte. Chefe que nasce depois do agendado e antes do teto: sem `ChefeAusente`. O teste não converte segundos (o #1 entrega o inteiro). Fronteira da soma: `tick_entrada_chefe_agendado` = 2³¹ − 1 com teto de 2700 não dá `ChefeAusente` no tick 1 (a conta é em `long`).
- **F5** (função pura, chamada pelo #1) Com P = 10, `folga_pool` 1, `nivel_max` 10, faixa de 60 a 85 % e total 700: passa. `nivel_max` 12: recusado. Fronteiras com a faixa de 60 a 85 %: total 850 passa e 851 reprova (mínimo); total 600 passa e 599 reprova (máximo); P = 9 reprova (folga); `xp_total_fase` = 0 reprova. A conta usa `long`, então `acum × 100` não estoura.
- **F6** Removido: não é um critério (o #3 não define fórmula de contagem para o K_min; a tabela da Regra 8 é coberta por X1 a X10).

### Estados e transições (AC-S), todos [U]

- **S1** Snapshot inválido: nada é criado (ver R3).
- **S2** *Entrando* vai a *Em andamento* com confirmação, e sem marca quando o #28 falha ou devolve "sem marca".
- **S3** Voltar em *Entrando* vai a *Cancelando*: `Entrar` fica desabilitado, com o motivo exposto na visão (UI1); a resposta do `BeginStage` com o `requestId` do pedido antigo é ignorada; só a resposta do commit de limpeza (`Confirmado` ou `Falhou`) leva a *Cancelada*; o Voltar em *Entrando* sempre pede 1 commit de limpeza (`CommitCount` +1).
- **S4** *Em andamento* e *Pausada* alternam, e `Tick` sem fim mantém o estado.
- **S5** *Concluindo* vai a *Resolvida* também com o commit de fim falhando, e o retry é permitido.
- **S6** *Resolvida* vai a *Entrando* (retry) ou a Fim (sair).
- **S7** App morto, em fase ou em *Concluindo* antes do commit: o boot seguinte dá `AppFechado`.
- **S8** `Create` ou `Preparar` lança, ou herói com HP ≤ 0, NaN ou `Spawn` −1: *Concluindo*(`FalhaInterna`), hash "indisponível", commit de limpeza antes de liberar o retry; HP 0 nunca vira `DerrotaHeroi` no tick 1.
- **S9** Tabela estado × comando: para cada par fora da tabela de estados (exceto `Tick` depois do fim, que lança por contrato, R1 e R9), o estado não muda, há 0 chamadas ao `FakeSave` e nada lança.
- **S10** (a) Duas respostas com o mesmo `attemptId` e `requestId` diferentes: só a do `requestId` pendente é aplicada. (b) Resposta do #28 entregue fora da fila da ponte (thread principal) é erro de host e lança nos dois modos.

### Edge cases (AC-E)

- **E1 [I]** Fila de ofertas sem carta possível. **GIVEN** um `FakeGrimorio` que avança o cursor sem abrir oferta, **THEN** o #3 sobe `NiveisGanhos` até `nivel_max − 1` sem lançar e a fase termina antes do teto de `CurrentTick` do runner (1,5 × (tick agendado do chefe + `ticks_max`)). Isso testa o #3, não o #16: o soft-lock real é contrato do #16 e do #9. **BLOQ: #16 e #9** para o real.
- **E2 [U]** Vitória falsa por `ChefeVisto` sem filtro de facção. **GIVEN** só o herói `Essencial`, **THEN** `ChefeVisto` é falso no tick 1 e não há vitória; o chefe nasce no tick N e só depois a vitória é possível; um inimigo `Essencial` vivo no tick em que o chefe morre impede a vitória.
- **E3** Vitória falsa por 2 `Essencial`. **BLOQ: emenda do #1** (recusa de 0 ou 2 ou mais). Um teste de caracterização ADVISORY documenta que o #3, em runtime, vence ao matar o primeiro.
- **E4 [I]** Marca fantasma ou tentativa dupla. Em cada sequência (retry duplo, Voltar e Entrar, commit de fim que falha, `Create` que lança), o `FakeSave` nunca fica com mais de 1 marca; em *Resolvida* com commit OK fica com 0; a soma de `ContaComoMorteDeFase` sobre os resultados entregues bate com X1 a X7.
- **E5 [U]** Herói morre no tick em que o chefe nasce: `DerrotaHeroi`, conta morte.
- **E6 [U]** `DerrotaTempo` e level-up no mesmo tick: sem nível e sem oferta.
- **E7 [U]** `xpDaMorte` negativo em qualquer arquétipo do snapshot, ou knob fora da faixa: o `Preparar` recusa antes do tick 0, `FalhaInterna(DadosInvalidos)`, sem clamp; nenhum dado é checado dentro do tick.
- **E8 [U]** Um frame de 3 ticks cujo tick 2 encerra: o host chama `Tick` 2 vezes, drena e descarta o resto.

### Integração (AC-I)

- **I1 [I] #3 com #2:** num compositor [#6 falso, #3, #16 falso], trocar a ordem muda o hash; o pedido de fim sai pelo contexto; `CombatActive` falso congela o #3; a `FalhaInterna` do #2 vence o pedido do #3.
- **I2a [I] #3 com #16 falso:** o cursor do falso lê `NiveisGanhos`; sem `IPreparaFase` e `IConcluiFase` implementadas o compositor não chama nada; sem o #16 a fase corre. **I2b [I]** com o #16 real. **BLOQ: #16** (Gate de integração do MVP).
- **I3a [I] #3 com #28 falso:** `BeginStage`, a resposta com o `attemptId` e o `requestId` do pedido pendente, o commit de fim, um `CancelStage` que substitui um `BeginStage` pendente deixa 0 marcas no `FakeSave`, o callback fora do `Tick` e a marca encontrada. **I3b [I]** com o #28 real. **BLOQ: #28 real e as emendas pedidas ao #28** (Gate de integração do MVP).
- **I4 [I] #3 com #6 e #7:** `xpDaMorte`, a lista de mortos com causa, `Essencial` no chefe, o primeiro ataque do chefe só no tick seguinte. **BLOQ: #6 e #7 sem GDD.**
- **I5 #3 com #1:** snapshot, knobs e F5 reais. **BLOQ: emenda do #1.**
- **I6 [I] #3 com #5 falso:** seed antes do tick 0, hash final, causa, `MorteSimultanea`, "abandonada" e exceção chegam ao `FakeLog`. **BLOQ: #5** para o real.
- **I7 [I] #3 com #20 stub:** o resultado (causa, vitória, nível final) chega ao stub. **BLOQ: #20** para o real.

### Hash e determinismo (AC-H)

- **H1 [I]** **GIVEN** mesma seed, dados e comandos, e uma fase roteirizada própria de 9.000 ticks (chefe agendado no `CombatTick` 6000, teto de 3000 ticks e um chefe que não morre, então fecha em `DerrotaTempo` no tick 9000), **WHEN** duas execuções, **THEN** o `StateHash` é igual **em todo tick**, nos modos estrito e não estrito. Controle negativo obrigatório, com o tick da divergência afirmado: mudar o `xpDaMorte` do arquétipo A diverge no tick da 1ª morte de A; mudar o comando C diverge no tick de C; mudar a seed diverge no primeiro tick que consome o stream afetado.
- **H2 [U]** O hash do #3 isolado: ver R16.
- **H3 [U]** O `ISeedSource` é chamado 1 vez por tentativa; o valor vai ao log antes do tick 0 e ao `Create`. Com um `FakeSeed` que repete a seed, duas tentativas dão o mesmo resultado (é o override do Tank × DPS).
- **H4 [U]** O `attemptId` vem de um `FakeId` (contador); nenhuma leitura de relógio nem de `System.Random`.
- **H5 [I]** Um script sem erro dá o mesmo hash nos dois modos; um `Preparar` que cria entidade não declarada lança em modo estrito e sobe `SpawnsRejected` em modo não estrito.
- **H6** Golden de hash por runtime. **BLOQ: #2 D8 e P7.**

### Teste sem tela e custo por tick

- **SEMTELA1 [I]** **GIVEN** uma fase roteirizada (waves, chefe e XP de falsos) e 3 retries com as seeds fixas do fixture próprio do #3, `SeedsFluxoDeFase` (não da lista do aceite, que mora no `mvp.md`, ainda inexistente; a lista do aceite entra no SEMTELA2), **WHEN** roda até o resultado, **THEN** fecha com a causa e o nível final esperados, sem UI. Estourar o teto de `CurrentTick` do runner reprova o teste; não vira resultado de fase.
- **SEMTELA2 [I]** Tank × DPS. **GIVEN** dois perfis falsos (mata devagar e mata rápido) e a mesma seed por override, **THEN** a sequência de spawns é igual e só o resultado muda. **BLOQ: #6, #7, #8, #16 e `docs/acceptance/mvp.md`** para a comparação real.
- **P1 [PM]** Zero alocação gerenciada por tick. O protocolo é o do #2 (aparelho de referência, Release IL2CPP, aquecimento, 20 ou mais execuções, ao menos 1 fase completa), reportando p95 e máximo do passo do #3 com 100, 300 e 600 mortes no tick; passa se o p95 ficar dentro do orçamento do #3 (X1 do #2). **BLOQ: spike, aparelho verificado e o orçamento, que ainda não existe.**
- **P2 [U] (ADVISORY)** Alarme: `GC.GetAllocatedBytesForCurrentThread` perto de 0 em 10.000 ticks roteirizados, depois do aquecimento. Medir alocação é `NOT SOURCEABLE` como prova em `docs/engine-reference/unity/`, então vale só como alarme.

### O que o #3 expõe ao #12, #20 e #28

- **UI1 [U]** A visão somente leitura traz estado, Nível, `XpAtual`, tempo restante do chefe, causa do resultado, `MorteSimultanea`, `ChefeVisto`, o `CombatTick` final, o motivo do bloqueio de `Entrar` ou `Retry` e se há commit pendente. O tempo restante é vazio antes do chefe, nunca negativo, e igual a `ticks_max − (CombatTick − TickDeEntradaDoChefe)` depois dele (0 no tick do estouro). As telas e os screenshots em `production/qa/evidence/` são dos GDDs dos outros sistemas.

### Só playtest humano ou não automatizável (n = 1)

O único testador do MVP é o próprio designer, que conhece o design e enviesa o resultado: nenhum item abaixo é prova estatística.

- **PT1** "Depois de uma derrota, o retry sai sem hesitação." Evidência: nota em `production/qa/evidence/` mais o tempo medido entre a tela de resultado e o toque em retry, em ao menos 5 derrotas seguidas, com mediana ≤ 3 s (calibração do protótipo, não prova) e o tempo do toque ao 1º tick. ADVISORY.
- **PT2** "Fechar o app não me puniu." **[PM]** O `adb` mata o app em fase e, ao reabrir, a marca resolve `AppFechado`. A contagem (0 mortes) é automática; a sensação é só do autor.
- **PT3** "A derrota por tempo é injusta" e o Tank com ≤ 2 mortes de fase: n = 1 não generaliza. O número é calibração do protótipo, não critério estatístico.
- **PT4** O ritmo das waves e do chefe (P4) e a faixa de X a Y level-ups por fase (OQ-5) não são testáveis até haver número calibrado.

### Gate

**Gate do #3 (BLOQUEANTE para fechar a story do #3; fecha só com dublês, sem depender de outro sistema):** R1 a R7, incluindo R6b (R8 = X1 a X10), R9 a R17; X1 a X10, incluindo X6b; F1 a F5; S1 a S10; E2 e E4 a E8; H1 a H5; SEMTELA1; I1; I2a e I3a (as partes com falsos); UI1.

**Gate de integração do MVP (BLOQUEANTE para fechar o MVP; cada item vive na story do último sistema a chegar e fica BLOQ até o dono existir):** I2b e I3b (as partes com o #16 e o #28 reais), I4 a I7, E1, X11, SEMTELA2, H6 e P1. Assim o #3 e o #16, que dependem um do outro, não travam um ao outro.

**ADVISORY:** E3 (caracterização), P2 e PT1 a PT4.

## Open Questions

Ainda não há calendário de produção com datas; o "marco" de cada pergunta é um **evento**. Toda regra marcada *(provisória)* neste GDD deve ser reavaliada junto com a OQ-10.

| ID | Pergunta | Dono | Marco |
|---|---|---|---|
| OQ-1 | **Emenda ao conceito congelado:** a linha 120 diz "coleta orbes de XP", e este GDD decidiu XP direto na morte, com o orbe só visual (decisão do autor, 2026-11-04). Registrar a emenda no conceito e anotar o que passa a dar ao jogador motivo para se mover sem os orbes: observar no protótipo, e se o movimento ficar sem rumo a resposta é de desenho de horda, não de reabrir a decisão. | Autor | Antes do GDD #12 |
| OQ-2 | **Resolvida em 2026-11-05 no ADR-0001 (emendas 1 a 14; falta só a aceitação do ADR, `accept ADR-0001`).** Pergunta original: **emenda do ADR-0001** (junto da OQ-5 do #2): a ficha de fase no `SimWorld`; as interfaces `IPreparaFase` e `IConcluiFase`; o caminho de escrita da marca `Essencial` fora do tick; a coluna `xpDaMorte` e a lista de mortos do tick; `Simulation.Create` e o `Spawn` de preparação sem evento; e o motivo `FalhaInterna` no pedido de fim do `SimContext` (`MissingBoss` pedido pelo #3, e `EssentialSpawnRejected` gerado pelo #2, que o #3 traduz em `ChefeAusente`); `DadosInvalidos` fica por exceção no `Preparar`, fora do Core. | `technical-director`, via `/architecture-decision` | Antes de `accept ADR-0001` |
| OQ-3 | **Ajustes no #2:** a FS9 somando `ids_de_preparacao`; a Regra 5 valendo "só pelo `SimWorld`" dentro do tick; a linha *Quebrada* ("falha sem derrota", sem contar morte); **fechar as OQ-2, OQ-3, OQ-7, OQ-10 e OQ-12 do #2**, que este GDD resolve. | Autor | **Feito em 2026-11-04** (a ficha de fase segue na OQ-5 do #2) |
| OQ-4 | **Resolvida em 2026-11-05 no GDD #6:** a lista de mortos é o `DeathsThisTick` do `SimWorld` e o `xpValue` está na linha do id (gravado no `Spawn` pelo #7). Pergunta original: Quem é dono da lista de mortos do tick e da coluna `xpDaMorte`: o #6 ou o #7? (a interface mínima de leitura está na Seção F) | #6 e #7 | GDD #6 e #7 |
| OQ-5 | **Calibração no protótipo:** a faixa de X a Y level-ups por fase, `nivel_max`, a curva (`xp_base`, `xp_inc`, `xp_quad`), `duracao_max_apos_chefe_s` calibrado no Tank, e `folga_pool`, `teto_xp_min_pct` e `teto_xp_max_pct`. | Autor, com `systems-designer` | Protótipo do MVP |
| OQ-6 | O registro no Grimório é um segundo commit depois do commit de fim. Se o app morrer entre os dois, a vitória conta e o registro daquela vitória se perde: devolver a oferta de registro na próxima abertura, ou aceitar a perda? | #16 e #28 | GDD #16 |
| OQ-7 | **Soft-lock:** fila de ofertas sem carta possível (`CombatHold` = 1 sem carta). Quem garante que o cursor avança e que o combate volta, e o que o #9 faz com menos de 3 cartas? | #9 e #16 | GDD #9 e #16 |
| OQ-8 | Mais de um inimigo `Essencial` por fase (pós-MVP): `essenciais_declarados` e a vitória esperando "nascidos igual a declarados". No MVP há exatamente 1, e o #1 recusa 0 ou 2 ou mais. | #7 e #1 | GDD #7 |
| OQ-9 | **Spikes NOT SOURCEABLE** (nenhum coberto por `docs/engine-reference/unity/`): (A) callbacks de pausa e foco no 6000.3.27f1 (ordem, thread, entre frames); (B) app morto (`adb shell am kill`, deslizar nos recentes) e se a Activity é recriada sem matar o processo; (C) tamanho do `dt` depois de pausa e de carga, e a fonte de tempo; (D) latência do commit da marca no aparelho (mediana, p95, pior caso) para calibrar o timeout; (E) substituição de pedidos no gravador do #28 (saiu do spike: vira teste EditMode do gravador, OQ-11); (F) custo e alocação do `Create` e reuso de buffers (hash igual com arena nova e reusada); (G) configuração de Enter Play Mode do projeto e varredura de estáticos; (H) orientação travada ou recriação da Activity; (I) a continuação de uma resposta assíncrona cair na thread principal (contexto de sincronização e `Awaitable` no 6000.3.27f1) e o `OnApplicationPause` num `am kill`. **Pré-requisito de todos: o aparelho de referência, ainda não verificado** (`VERSION.md`). | `technical-director` e `engine-programmer` | Spike de performance |
| OQ-10 | **Reavaliar as decisões *(provisórias)*** com o jogo avançado: a divisão dentro e fora do tick; os ganchos por ficha de fase; o herói criado pelo compositor; a vitória em que ambos caem não contar como morte; sem XP nem nível no tick do fim; `Quebrada` e `FalhaInterna` não contarem como morte; a tentativa nascer *Pausada* quando há motivo ativo; o guarda `ChefeAusente`; a faixa de porcentagem da F5. | Autor e `technical-director` | Depois dos spikes do #2 e da OQ-9 |
| OQ-11 | **Exigências ao #28 e ao ADR-0003** (revistas em 2026-11-05; o "FIFO" anterior saiu, porque o gravador único substitui o pedido que espera): (a) um `CancelStage` nunca grava a marca, inclusive quando substitui um `BeginStage` pendente (hoje o substituto herda o tipo mais forte, `StageMark`); (b) `requestId` único entre todos os chamadores (#3, #17), emitido pelo #28 ou por uma fonte única; (c) `AttemptId` de 128 bits no `CommitResult` (hoje `int`); (d) um resultado por `requestId`, numa fila que a ponte esvazia na thread principal; (e) callback fora do `Tick`; (f) payload opaco do #3 vazio no MVP. A OQ-9 (E) deixa de ser spike de engine e vira teste EditMode do gravador. | #28 e `technical-director` | Antes da primeira story do #3 |
| OQ-12 | **Ajustes no índice** (`systems-index.md`): listar #6 e #7 (Hard) nas dependências do #3, acompanhar o Dependency Map (linha 213), e listar o #3 (Soft) no #5 e no #12. | Autor, na Fase 5 deste skill | **Resolvida em 2026-11-04** |
| OQ-13 | Fases de função (escoltar ou proteger um NPC) ficam fora do MVP. O gancho é o `AvaliarFim` único com uma causa que só cresce; o desenho da condição de resultado é do GDD de fases de função. | #14 | Vertical Slice |
| OQ-14 | **Telas e textos** (HUD, pausa, carregamento, resultado por causa, aviso de app fechado): dono e redação. Pré-requisito: `design/accessibility-requirements.md`. | `ux-designer`, via `/ux-design` | Pré-Produção, antes dos épicos |
| OQ-15 | O #2 (Edge Cases) diz que `Quebrada` conta como "tentativa falha", e o #3 diz que não conta como morte de fase. Harmonizar a redação (a tabela de resultados deste GDD vale). **Feito em 2026-11-04.** | #2 | Ajustes da OQ-3 |
| OQ-16 | **Materiais na morte** (conceito L112): "sem recompensa" na Regra 8 é só a recompensa de fim de fase; o que foi coletado durante a fase segue a economia. A economia decide como `DerrotaHeroi`, `DerrotaTempo`, `Abandonada` e `AppFechado` rendem **materiais e moeda de jogo** (R5 do `business-model.md`), preferindo **igualdade** entre as quatro (com "maior ou igual", fechar o app dominaria morrer), e diz em quais causas o vídeo que dobra a moeda é oferecido (R6): o `AppFechado` não tem tela de resultado, então nunca recebe a dobra. Exigência contra farm: o rendimento por minuto de `CombatTick` de um abandono antes do chefe tem de ser menor ou igual ao de uma tentativa completa (abandonar cedo não conta morte e sorteia seed nova). O #3 não garante isso sozinho: o payload da marca é vazio e os materiais não estão no save no meio da fase, então ou a morte não dá material, ou o crédito sai por commit em marcos (fim de wave, entrada do chefe). `FalhaInterna` pode compensar a mais. | Economia (#26) e `game-designer` | GDD de economia |
| OQ-17 | O resultado ganha a **origem manual ou automática** quando o auto-battle existir, e o #16 filtra o **tipo de fase** (chefe de fase ou de capítulo) pelo snapshot do #1. | #40, #16 e #20 | GDD #40 e #16 |
| OQ-18 | **Limite conhecido do aceite:** fechar o app no chefe vira `AppFechado` e escapa da contagem de mortes (a marca não guarda `ChefeVisto`), a mesma brecha que a regra de abandono fecha. Com n = 1 o impacto é pequeno; no MVP o X11 conta o `AppFechado` total, com pior valor próprio. Opção para o vertical slice: o #5 grava `ChefeEntrou` em disco na hora em que o evento sai, e o sinal vira "`AppFechado` cujo `attemptId` tem `ChefeEntrou` no log" (abre um contrato novo com o #28 e o #5). | Autor e `qa-lead` | Vertical Slice |
| OQ-19 | **Decidida em 2026-11-05 pelo autor: a definição estreita fica.** O conceito define morte de fase como "tentativa que termina sem vencer o chefe de fase", e o #3 exclui da conta o abandono antes do chefe, `AppFechado`, `FalhaInterna`, `Quebrada` e a vitória simultânea (decisões do autor e do #28). Falta registrar a emenda no L405 do conceito congelado (junto da OQ-1) e fixar no `mvp.md` um pior valor por sinal à parte (X11). | Autor | Emenda no conceito junto da OQ-1; pior valor antes de `docs/acceptance/mvp.md` |

