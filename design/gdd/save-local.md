# Save local (#28)

> **Status**: In Design
> **Author**: Rodrigo Reis + agentes (systems-designer)
> **Last Updated**: 2026-11-03
> **Last Verified**: 2026-11-03
> **Implements Pillar**: Habilitador; sustenta o Pilar 2 (Toda escolha pesa) e o Princípio de Negócio (Poder conquistado, não comprado)
> **Creative Director Review (CD-GDD-ALIGN)**: REVISED 2026-11-03 — CONCERNS na 1ª passada (fantasia reduzida ao que o MVP garante; "app fechado" separado das derrotas no log, contagem decidida pelo doc de aceite)

## Summary

O #28 Save local grava no aparelho o progresso do jogador (heróis, selos, registros do Grimório, vitórias) e o devolve intacto, sem nunca guardar valores de balanceamento nem cosméticos comprados. Ele grava só em pontos seguros, em commit único com backup, conta como tentativa falha uma fase interrompida pelo fechamento do app, e existe para que o que o jogador selou continue lá: a permanência de que o Pilar 2 depende.

> **Quick reference** — Layer: `Foundation` · Priority: `MVP` · Key deps: `#1 Dados e balanceamento` (dependem dele: #3, #5, #16, #17, #19, #22, #26, #29)

## Overview

O **#28 Save local** grava no aparelho o progresso do jogador e o devolve intacto na próxima vez que o jogo abrir. Ele **só serializa**: não decide regra nenhuma, e cada sistema continua dono da sua fatia (o Herói #19 é dono dos heróis e do estado "selado"; o Grimório #16 é dono dos registros e do contador de vitórias; e assim por diante). O save guarda **progresso, nunca valores de balanceamento nem posses pagas**: os números vêm sempre do #1 (o save só guarda os IDs estáveis, o carimbo da versão dos dados e a revisão de cada skill selada), e um cosmético comprado é liberado pelo token do servidor, não por um campo editável do save (`design/business-model.md` §7). No MVP é o **único sistema de persistência**, porque o jogo é todo offline; o cloud save do #29 chega no Alpha e usa este mesmo conteúdo. O jogador nunca vê o sistema; ele sente o efeito: o que ele conquistou e selou continua lá.

## Player Fantasy

**Enquadramento: indireto.** O jogador nunca usa este sistema; ele sente o efeito.

**"O selo não se desfaz sozinho."** O jogador nunca vê este sistema, mas conta com ele toda vez que fecha o jogo depois de selar uma skill. O que foi selado no fogo das hordas só muda por uma run de reforja, nunca porque o aparelho esqueceu. Fechar o app, reiniciar o telefone ou atualizar o jogo não apaga nem altera o que ele conquistou, e também não devolve nada que ele perdeu. Quando ele abre o Grimório no dia seguinte, os registros, os heróis selados e as vitórias estão como ele deixou.

*Pilar servido:* **Pilar 2, Toda escolha pesa.** Uma decisão permanente só tem peso se a permanência for real, tanto contra a perda quanto contra o desfazer: o save não pode perder o selo, e o jogo não oferece nenhum caminho para desfazê-lo.

*O que esta seção não promete:* cloud save, sincronização ou mais de um aparelho no MVP (#29, Alpha); recuperar o progresso se o aparelho for perdido ou trocado, o app for desinstalado ou os dados forem limpos; proteção contra edição, root ou trapaça, nem integridade do ranking (exigem servidor); guardar ou restaurar cosméticos comprados (o token do servidor libera, `business-model.md` §7); "nunca perde nada" em queda de energia ou crash (a garantia exata está nas Core Rules); compatibilidade ao voltar para uma versão antiga do app; impedir que uma cópia antiga restaurada pelo backup automático do Android traga de volta um estado anterior a um selo (detectado a partir do Alpha, pelo #29); que o balanceamento das skills seladas nunca muda (os valores vêm do #1).

*Consultado:* `creative-director` (2 enquadramentos; recomendado e adotado o A).

## Detailed Design

### Core Rules

1. **Um save por aparelho.** Há um único progresso por aparelho; os vários heróis do jogador vivem dentro dele (o roster do #19). Trocar de aparelho é papel do cloud save do #29 (Alpha).
2. **O que entra:** a fatia de cada sistema com progresso (heróis e o estado "selado" do #19; registros e contador de vitórias de chefe de fase do #16; progresso de capítulo e fase; roster), os **IDs estáveis** do #1, o **carimbo da versão dos dados**, a **revisão e a data do selo** de cada skill selada, a **maior hora já vista** (`maxSeenUtc`) e um **contador de gravações** que só cresce (`saveSequence`).
3. **O que nunca entra:** valores de balanceamento (vêm do #1); posses pagas e cosméticos comprados (vêm do token do servidor, `business-model.md` §7); o estado de uma fase em andamento (só a marca da regra 6); o log de eventos (#5, telemetria separada); o placar do ranking (#22, é do servidor).
4. **Fatias e envelope.** Cada sistema entrega uma fatia nomeada, com versão própria, e é dono do conteúdo dela; o #28 só guarda e devolve. O #28 é dono do **envelope**: versão do formato, carimbo dos dados, `saveSequence`, `maxSeenUtc`, checksum e a lista de fatias. Campos ou fatias que o #28 não reconhece passam intactos de uma gravação para a seguinte.
5. **Quando grava (pontos seguros):** ao entrar numa fase (só a marca da regra 6), ao fim de cada partida (vitória, derrota ou abandono pelo menu), ao registrar no Grimório, ao selar, ao criar um herói, ao sair de uma tela de meta e quando o app vai para segundo plano. **Nunca durante uma fase** e nunca dentro do tick (ADR-0001). A gravação **não pode travar o frame** (orçamento em Tuning Knobs).
6. **App fechado no meio da fase.** Ao entrar numa fase, o save grava a marca "fase em andamento" (qual herói, qual fase). Se o jogo abrir e encontrar a marca, aquela fase conta como **tentativa falha**, igual a uma derrota: sem recompensa, sem registro no Grimório e contando como morte (o conceito define morte como "uma tentativa que termina sem vencer o chefe de fase", L405). O log (#5) registra essa tentativa com a **causa própria "app fechado"**, separada das derrotas; se ela entra na contagem de mortes das métricas de aceite (por exemplo, o Tank com ≤ [2] mortes) é decisão do doc de aceite (`docs/acceptance/mvp.md`), porque o Android pode fechar o jogo sem o jogador escolher. A marca é limpa ao fim de toda partida. Não existe retomar uma fase do ponto em que parou.
7. **Commit único.** Cada gravação é um commit inteiro: selo, registro e herói alterados no mesmo momento vão juntos, então nunca existe um selo gravado sem o seu registro. **Uma gravação que falha nunca destrói o save bom**: o save anterior continua valendo até o novo estar completo e verificado.
8. **Integridade e backup.** O save tem checksum e um backup da última gravação válida. Isso detecta **corrupção** (bateria acabou, disco falhou), **não é anti-cheat**: o jogo é offline e não há vantagem paga para proteger.
9. **Versão do formato.** A versão do formato é um inteiro. Um save de formato mais antigo é migrado **só na estrutura, nunca nos valores** (os valores vêm sempre do #1). Um save de formato **mais novo** que o suportado (o jogador voltou para uma versão antiga do app) abre **só para leitura** e nunca é sobrescrito, e o jogo pede para atualizar o app.
10. **ID desconhecido** (o #1 responde "ID desconhecido"). O #28 preserva o registro como está, não cria nada e não apaga nada. Uma skill selada desconhecida mantém o herói selado, com aquele slot marcado "indisponível" até o ID voltar a existir.
11. **Relógio.** A cada abertura e a cada gravação, `maxSeenUtc = max(maxSeenUtc, hora atual)`. O #28 entrega a "hora efetiva", que nunca volta atrás; quem aplica o limite de acúmulo offline (K períodos, knob no #1) é a Economia (#26).
12. **Erro de gravação** (disco cheio, falha de I/O). O save anterior continua valendo, o jogador é avisado uma vez sem bloquear o jogo, e o #28 tenta de novo no próximo ponto seguro. O progresso em memória nunca é descartado em silêncio.
13. **Perda máxima tolerada:** o progresso desde o último ponto seguro, ou seja, no máximo a fase em curso (que já conta como tentativa falha pela regra 6) ou a última ação de meta antes de um corte de energia.

### States and Transitions

| Estado ao abrir | Condição | O que acontece | Próximo |
|---|---|---|---|
| **Ausente** | nenhum save no aparelho | cria um save novo (primeira vez) | Válido |
| **Válido** | checksum ok, formato atual | carrega; se houver a marca "fase em andamento", registra a tentativa falha (regra 6) e limpa a marca | Válido |
| **Formato antigo** | versão do formato menor que a atual | migra a estrutura e grava | Válido |
| **Corrompido** | checksum falha, backup ok | **restaura o backup automaticamente** e avisa que a última partida pode ter se perdido | Válido |
| **Irrecuperável** | save e backup falham | o arquivo vai para quarentena (nunca é apagado sem confirmação) e o jogador escolhe recomeçar ou não | Ausente, só se o jogador escolher |
| **Formato mais novo** | versão do formato maior que a suportada | abre só para leitura, nunca grava, pede para atualizar o app | Válido, depois do update |

### Interactions with Other Systems

Nenhum GDD dependente existe além do #1; as interfaces abaixo são **provisórias**. Entre parênteses, o dono da interface.

- **#1 Dados e balanceamento** (o #1 resolve IDs e responde "ID desconhecido"; o #28 trata a resposta). O save grava só os IDs, o carimbo da versão e a revisão e data do selo; nunca valores, e nunca migra valores (contrato já fixado no GDD #1).
- **#5 Log de eventos** (o #5 é dono do log). O #28 emite eventos de falha de gravação, restauração de backup, quarentena e tentativa falha por app fechado.
- **#16 Grimório e #19 Herói** (cada um é dono do conteúdo da sua fatia e entrega um retrato serializável). O #28 é dono do commit.
- **#17 Selamento** (o #17 dispara o selo). O #28 grava, no mesmo commit, o estado "selado" do herói, a revisão e a data do selo de cada skill selada.
- **#3 Fluxo de fase** (o #3 avisa a entrada e o fim de cada partida). O #28 grava e limpa a marca "fase em andamento".
- **#22 Ranking** (Alpha). Nada no MVP; uma fila de envios pendentes só entra se o GDD #22 pedir.
- **#26 Economia** (Vertical Slice). Lê a "hora efetiva" do #28 para os tetos e o acúmulo offline.
- **#29 Serviços online** (Alpha). O #28 é dono do formato e da exportação e importação do retrato inteiro; o #29 é dono do transporte e da decisão local × nuvem. O `saveSequence` e o `maxSeenUtc` existem desde o MVP para que o #29 consiga detectar um save que regrediu (por exemplo, um backup automático do Android que restaurou uma cópia velha).

**Vira ADR (técnico, não é decisão de jogo):** formato de serialização e do envelope; local de gravação no Android; mecanismo de escrita atômica (arquivo temporário e troca); algoritmo do checksum e política do backup; gravação fora da thread principal e na pausa do app; política do Auto Backup do Android; serialização sem reflexão (stripping do IL2CPP, ADR-0001) e sem estado `static` mutável no serviço de save. `PlayerPrefs` não serve para progresso (sem atomicidade nem backup), só para preferências triviais. Tudo isso é `NOT SOURCEABLE` em `docs/engine-reference/unity/`.

*Consultados:* `systems-designer` (regras, estados, interações) e `engine-programmer` (viabilidade, Android e Unity). Decisões do usuário: app fechado no meio da fase perde a fase e conta como tentativa falha; um save por aparelho; save corrompido volta ao backup automaticamente com aviso.

## Formulas

### F1. Hora efetiva

The effectiveUtc formula is defined as:

`maxSeenUtc_novo = max(maxSeenUtc_salvo, nowUtc); effectiveUtc = maxSeenUtc_novo`

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| maxSeenUtc_salvo | int64 (ms UTC) | 0 a 2^63 − 1 | calculated | maior hora já vista, lida do envelope (0 num save novo) |
| nowUtc | int64 (ms UTC) | qualquer valor | calculated | relógio do aparelho na abertura ou na gravação |
| effectiveUtc | int64 (ms UTC) | ≥ maxSeenUtc_salvo | calculated | hora que o #28 entrega à Economia (#26) e usa na data do selo |

**Output Range:** só cresce, sem teto. Atrasar o relógio não faz a hora voltar; adiantar faz a hora pular para a frente, e quem limita o ganho desse pulo é o teto de K períodos do #26.
**Example:** salvo 10:00 e aparelho 09:40 → effectiveUtc = 10:00. Salvo 10:00 e aparelho 11:00 → effectiveUtc = 11:00.

### F2. Número do commit

The saveSequence formula is defined as:

`saveSequence_novo = saveSequence_salvo + 1`, só quando um commit é concluído e verificado

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| saveSequence_salvo | int64 | 0 a 2^63 − 1 | calculated | número do último commit válido (0 num save novo) |
| saveSequence_novo | int64 | ≥ 1 | calculated | número deste commit |

**Output Range:** cresce de 1 em 1, sem teto prático. Uma gravação que falha não consome número.
**Example:** o selo grava o commit 41 e a ida para segundo plano grava o 42; se o 42 falhar, o save continua no 41.

### F3. Custo da gravação no frame

The saveFrameCost formula is defined as:

`saveFrameCost_ok = t_retrato_thread_principal ≤ SAVE_MAIN_THREAD_BUDGET_MS`

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| t_retrato_thread_principal | float (ms) | ≥ 0 | calculated | tempo para montar o retrato das fatias na thread principal; a serialização e a escrita em disco ficam fora dela |
| SAVE_MAIN_THREAD_BUDGET_MS | float (ms) | a medir | data file | orçamento; só é fixado depois da medição no aparelho de referência (ainda não verificado) |

**Output Range:** passa ou falha. Estourar o orçamento é bug de desempenho; a gravação nunca é cortada para caber.
**Example:** com orçamento de X ms, um retrato de X/2 ms passa.

### F4. Perda máxima por corrupção

The commitsLost_max formula is defined as:

`commitsLost_max = 1`

**Variables:**
| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| commitsLost_max | int | 1 | constant | quantos commits se perdem, no máximo, quando o save principal está corrompido |

**Output Range:** 1. O backup é sempre o commit anterior ao principal. A regra 13 conta pontos seguros, não tempo, então não há janela em segundos para ajustar.
**Example:** principal no commit 42 corrompido e backup no 41 → o jogo volta ao 41.

*Consultado:* `systems-designer`.

## Edge Cases

- **If o relógio do aparelho é adiantado e depois corrigido**: `maxSeenUtc` fica na hora futura, a hora efetiva não anda até a hora real passar dela e, nesse intervalo, não há acúmulo offline. O #5 recebe o evento "relógio atrás da maior hora vista" uma vez por sessão. *(Decisão provisória: aceitar o congelamento, que só afeta quem mexeu no relógio; a alternativa, limitar o pulo com um relógio interno, fica para reavaliar.)*
- **If o app morre durante uma gravação**: o arquivo incompleto é descartado na próxima abertura, o save principal continua intacto e só se perde o que veio depois do último commit.
- **If o app morre durante a gravação da marca "fase em andamento"**: a marca não chega a existir e o save anterior vale. A fase só começa depois que o commit da marca é confirmado (na tela de carregamento), então nada conta como tentativa falha.
- **If a marca não pode ser gravada (erro de disco)**: o jogador entra na fase mesmo assim, e o problema de disco segue a regra 12 (aviso uma vez). A brecha (fechar o app para escapar de uma derrota) só engana o próprio jogador num jogo offline. *(Decisão provisória: não bloquear o jogo por falta de espaço.)*
- **If duas gravações chegam quase juntas (por exemplo, selar e o app ir para segundo plano)**: existe um único gravador. Um pedido que chega com outra gravação em andamento substitui o pedido que estava esperando (cada retrato é inteiro), e cada commit recebe o seu próprio `saveSequence`. Se o Android matar o app no meio, vale o último commit concluído.
- **If o backup automático do Android restaura um save velho num aparelho novo**: o save é aceito como válido, porque no MVP não há com o que comparar. O jogador recebe o progresso antigo; se a cópia é de antes de um selo, esse selo não existe nela. Isso fica aceito como fora de escopo (sem anti-cheat); incluir ou não o save no backup automático é decisão do ADR. A partir do Alpha, o #29 detecta a regressão pelo `saveSequence`.
- **If o app é reinstalado**: sem backup automático, o save fica Ausente e o jogo cria um novo; com backup automático, vale o caso anterior. A quarentena some junto com os dados do app.
- **If o disco continua cheio**: cada ponto seguro tenta gravar e falha, o progresso fica em memória, e o aviso aparece uma vez por sessão dizendo que o progresso **não está sendo salvo**. Se o app morrer, perde-se tudo desde o último commit bem-sucedido: nesse cenário a garantia da regra 13 não vale, e o aviso precisa deixar isso claro.
- **If o save tem a fatia de um sistema removido do jogo**: a fatia passa intacta de commit em commit (regra 4) e nenhum sistema a lê. Ela só é apagada se uma migração de formato futura a retirar explicitamente.
- **If a marca "fase em andamento" aponta uma fase que não existe mais nos dados**: conta como tentativa falha do herói, com o ID desconhecido da fase registrado no #5, e a marca é limpa. Se o herói também é desconhecido, a marca é limpa, o #5 recebe um evento e nada é contado.

*Consultado:* `systems-designer`. Decisões menores adotadas no modo guided e marcadas como provisórias: congelar a hora efetiva com relógio adiantado; não bloquear a fase quando a marca não grava.

## Dependencies

### Upstream (o #28 depende de)
| Sistema | O que usa | Dependência |
|---|---|---|
| #1 Dados e balanceamento (GDD Designed) | IDs estáveis, carimbo da versão dos dados, revisão das skills, resposta "ID desconhecido" | **Hard**: sem o #1 o save não sabe resolver o que guardou |

### Downstream (dependem do #28)
Contratos provisórios: nenhum destes GDDs existe ainda.

| Sistema | O que lê ou entrega | Dependência |
|---|---|---|
| #3 Fluxo de fase | avisa entrada e fim de partida; o #28 grava e limpa a marca "fase em andamento" | **Hard** (regra 6) |
| #5 Log de eventos | recebe eventos de falha, restauração, quarentena, tentativa falha e relógio atrás | **Soft** (o save funciona sem o log; o aceite precisa dele) |
| #16 Grimório | entrega e recebe a sua fatia (registros, contador de vitórias) | **Hard** |
| #17 Selamento | dispara o commit do selo | **Hard** |
| #19 Herói | entrega e recebe a sua fatia (heróis, estado "selado", roster) | **Hard** |
| #22 Ranking (Alpha) | nada no MVP | **Soft** |
| #26 Economia (Vertical Slice) | lê a hora efetiva | **Hard** para os tetos |
| #29 Serviços online (Alpha) | exporta e importa o retrato inteiro; usa `saveSequence` e `maxSeenUtc` para detectar regressão | **Hard** para o cloud save |

**Bidirecionalidade:** o índice lista o #28 como dependência de #5, #16, #19, #22 e #29. Faltam **#3, #17 e #26**, que passam a depender do #28 por este GDD; o índice é atualizado na Fase 5. O GDD #1 já cita o #28 (Interactions e Dependencies).

## Tuning Knobs

| Knob | Padrão | Faixa segura | Remoto | Afeta | Baixo demais | Alto demais |
|---|---|---|---|---|---|---|
| `SAVE_MAIN_THREAD_BUDGET_MS` (F3) | a medir no aparelho de referência | definida pela medição | não | tempo máximo de montagem do retrato na thread principal | falha de desempenho em aparelhos lentos, sem ganho para o jogador | hitch perceptível ao gravar (por exemplo ao selar ou ao ir para segundo plano) |

**Não são knobs:** `commitsLost_max = 1` (consequência de ter um único backup; mudar isso é mudar a regra 8). **De outro dono:** o limite de acúmulo offline (K períodos) é knob do #1, aplicado pela Economia (#26), não pelo #28.

## Visual/Audio Requirements

Nenhum. O #28 não tem superfície visual nem sonora própria; os avisos que ele dispara estão em UI Requirements.

## Game Feel

Não se aplica, exceto por um requisito: a gravação nunca pode causar um travamento perceptível (F3).

## UI Requirements

O #28 não tem tela própria, mas dispara quatro mensagens ao jogador, que precisam de UX:
1. **Backup restaurado:** aviso, ao abrir o jogo, de que o save estava danificado e a última partida pode ter se perdido (não bloqueia).
2. **Progresso não está sendo salvo:** aviso uma vez por sessão quando o disco está cheio ou a gravação falha (não bloqueia; precisa dizer com clareza que o progresso pode se perder se o app fechar).
3. **Atualize o app:** o save é de uma versão mais nova; o jogo abre só para leitura até o update.
4. **Save irrecuperável:** o jogador escolhe recomeçar ou não; o arquivo antigo fica em quarentena e nunca é apagado sem confirmação.

> **📌 UX Flag — #28 Save local**: este sistema tem requisitos de UI. Na Pré-Produção, rode `/ux-design` para essas quatro mensagens **antes** de escrever épicos; as stories devem citar `design/ux/[tela].md`, não este GDD.

## Cross-References

| Documento | Trecho | O que este GDD usa ou impõe |
|---|---|---|
| `design/gdd/dados-e-balanceamento.md` | Interactions (#28), Edge Cases "Selo, revisão e save", Dependencies | o save guarda IDs, carimbo e revisão + data do selo; nunca valores; trata "ID desconhecido" |
| `design/business-model.md` | §7 (L106-107) | o save não guarda posses; guarda a maior hora já vista e nunca volta abaixo dela |
| `design/gdd/game-concept.md` | L399, L405 | MVP todo offline; "morte" = tentativa que termina sem vencer o chefe (base da regra 6) |
| `design/gdd/systems-index.md` | #28, #29 | só serializa, cada sistema é dono da sua fatia; cloud save no #29 |
| `docs/architecture/adr-0001-simulacao-deterministica-float32-tick-30hz.md` | Implementation Guidelines | nada de I/O no tick; sem reflexão (stripping); sem estado `static` mutável |
| GDDs #3, #5, #16, #17, #19, #22, #26, #29 | ainda não existem | cada um deve citar o #28 e confirmar a interface provisória |

## Acceptance Criteria

Evidência: **[EM]** teste EditMode em `Assets/Tests/EditMode/SaveLocal/SaveLocalTests.cs`, com armazenamento em memória injetado (`FakeSaveStorage`, que simula falha, corte no meio da escrita e bytes corrompidos) e relógio injetado, sem tocar o disco; **[PM]** PlayMode ou build no aparelho; **[MAN]** manual. **MVP** bloqueia o MVP; **PÓS** só quando o sistema dependente existir.

### Regras
- **AC-01 (regras 1 a 4)** — **GIVEN** um save com as fatias do #16 e do #19, mais uma fatia e um campo que o #28 não conhece, **WHEN** grava e recarrega, **THEN** tudo volta igual, inclusive o desconhecido, e o envelope só tem campos da lista permitida (sem valores de balanceamento, sem posses). `RoundTrip_PreservesKnownAndUnknownSlices` **[EM]** MVP
- **AC-02 (regra 5)** — **GIVEN** uma fase em andamento, **WHEN** chega um pedido de gravação, **THEN** nada é escrito até o próximo ponto seguro. `SaveRequest_DuringStage_IsDeferred` **[EM]** MVP
- **AC-03 (regra 5)** — **GIVEN** o build no aparelho, **WHEN** o app vai para segundo plano, **THEN** sai um commit (`saveSequence` sobe 1). **[PM]** MVP
- **AC-04 (regra 6, #3)** — **GIVEN** a marca "fase em andamento" gravada, **WHEN** o jogo abre, **THEN** conta 1 tentativa falha, sem recompensa nem registro, e a marca é apagada; **GIVEN** uma partida que termina, **THEN** a marca é apagada no mesmo commit. **[EM]** MVP
- **AC-05 (regra 7, #17)** — **GIVEN** um selo, **WHEN** o armazenamento falha no meio da escrita, **THEN** no próximo carregamento o selo, o registro e o herói estão todos no estado anterior; nunca existe selo sem registro. **[EM]** MVP
- **AC-06 (regra 9)** — **GIVEN** um save de formato N + 1, **WHEN** carrega, **THEN** fica só para leitura e nenhuma gravação o sobrescreve. **[EM]** MVP
- **AC-07 (regra 10, #1)** — **GIVEN** uma skill selada com ID que o #1 não conhece, **WHEN** carrega e grava de novo, **THEN** o registro continua intacto, o herói continua selado, o slot fica "indisponível" e nada é criado nem apagado. **[EM]** MVP
- **AC-08 (Edge Cases, ID desconhecido na marca)** — **GIVEN** a marca "fase em andamento" de uma fase que não existe mais nos dados, **WHEN** o jogo abre, **THEN** conta 1 tentativa falha com o ID desconhecido registrado no #5 e a marca é limpa; **GIVEN** que o herói da marca também é desconhecido, **THEN** a marca é limpa, o #5 recebe o evento e nada é contado. **[EM]** MVP
- **AC-09 (regra 12)** — **GIVEN** um armazenamento que sempre falha, **WHEN** passam 3 pontos seguros, **THEN** o progresso em memória continua lá, sai 1 aviso por sessão e há uma tentativa de gravar em cada ponto. **[EM]** MVP
- **AC-10 (regra 13)** — **GIVEN** o aparelho, **WHEN** o processo é morto durante uma gravação, **THEN** ao reabrir vale o último commit concluído. **[PM]** MVP

### Formulas
- **AC-11 (F1)** — **GIVEN** salvo 10:00 e aparelho 09:40, **WHEN** calcula, **THEN** `effectiveUtc` = 10:00; com aparelho 11:00, **THEN** 11:00. **[EM]** MVP
- **AC-12 (F2)** — **GIVEN** `saveSequence` = 41, **WHEN** um commit conclui, **THEN** vira 42; **WHEN** um commit falha, **THEN** continua 41. **[EM]** MVP
- **AC-13 (F3)** — **GIVEN** o aparelho de referência, **WHEN** grava ao selar e ao ir para segundo plano, **THEN** a montagem do retrato fica dentro de `SAVE_MAIN_THREAD_BUDGET_MS`. **[PM]** MVP — **BLOQUEADO** até a medição (o knob não tem valor e o aparelho de referência não foi verificado).
- **AC-14 (F4)** — **GIVEN** o principal no commit 42 corrompido e o backup no 41, **WHEN** o jogo abre, **THEN** carrega o 41. **[EM]** MVP

### Estados e concorrência
- **AC-15 (tabela de estados)** — **GIVEN** cada estado da tabela, **WHEN** o jogo abre, **THEN**: Ausente cria um save novo; Válido carrega; Formato antigo migra a estrutura sem mudar nenhum valor e grava; Corrompido restaura o backup e emite o evento; Irrecuperável põe o arquivo em quarentena e nunca o apaga sem confirmação; Formato mais novo fica só para leitura. Um teste por estado. **[EM]** MVP
- **AC-16 (gravações simultâneas)** — **GIVEN** uma gravação em andamento, **WHEN** chegam dois pedidos, **THEN** o que esperava é substituído pelo mais novo e cada commit recebe o seu `saveSequence`. **[EM]** MVP

### Pós-MVP e UI
- **AC-17 (#26)** — **GIVEN** a Economia, **WHEN** calcula um teto, **THEN** lê `effectiveUtc` do #28. **[EM]** PÓS (Vertical Slice)
- **AC-18 (#29)** — **GIVEN** um save que voltou atrás, **WHEN** o #29 compara, **THEN** detecta a regressão pelo `saveSequence`. **[EM]** PÓS (Alpha)
- **AC-19 (UI)** — **GIVEN** as 4 mensagens de UI Requirements, **WHEN** cada situação é provocada, **THEN** a mensagem aparece com o texto aprovado no UX (a de disco cheio diz literalmente que o progresso pode se perder se o app fechar), com screenshot de cada uma em `production/qa/evidence/`. **[MAN]** MVP — **BLOQUEADO** até existir a spec de UX.

### Não testável por teste de comportamento
- "Nunca dentro do tick", "sem reflexão", "sem `static` mutável" e "`PlayerPrefs` não serve para progresso" são regras de arquitetura: valem por revisão de código e pelo ADR do save.
- Backup automático do Android e reinstalação dependem do ADR, e no MVP estão fora de escopo.
- A troca de relógio no próprio aparelho é **[MAN]** opcional; a matemática está coberta pelo AC-11.

*Consultado:* `qa-lead`. Decisões de formato adotadas no modo guided: AC próprio para fase ou herói desconhecido; os seis estados agrupados num só critério.

## Open Questions

| # | Pergunta | Dono | Resolver até |
|---|---|---|---|
| OQ-1 | ADR do save: formato e envelope, local de gravação no Android, escrita atômica, checksum e backup, gravação fora da thread principal e na pausa, política do backup automático do Android, serialização sem reflexão. Tudo `NOT SOURCEABLE` em `docs/engine-reference/unity/` | `technical-director` (via `/architecture-decision`) | antes da primeira story do #28 |
| OQ-2 | Valor de `SAVE_MAIN_THREAD_BUDGET_MS` | usuário, com `performance-analyst` | spike de performance; o AC-13 fica bloqueado até lá |
| OQ-3 | Textos das 4 mensagens ao jogador | `ux-designer` (via `/ux-design`) | Pré-Produção, antes dos épicos; o AC-19 fica bloqueado até lá |
| OQ-5 | Risco para o lançamento: perder uma fase longa por uma interrupção que o jogador não causou (o Android fechou o app) pesa no celular. Rever a regra 6 com dados de playtest. Também: o ADR da OQ-1 deve usar o Pilar 2 como critério para decidir se o save entra no backup automático do Android | usuário e `game-designer` | primeiro playtest externo; o ADR antes da primeira story |
| OQ-4 | **Decisões a reavaliar com o jogo avançado** (aceitas por recomendação): congelar a hora efetiva quando o relógio foi adiantado e depois corrigido; não bloquear a fase quando a marca não grava; aceitar no MVP um save velho trazido pelo backup automático do Android | usuário | primeira revisão com o jogo jogável (vertical slice) |
