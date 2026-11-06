# ADR-0003: Save local (#28): envelope binário TLV com FNV-1a, commit atômico com backup, gravador único fora da thread principal e Auto Backup só do arquivo principal

## Status
Proposed

## Date
2026-11-05

## Last Verified
2026-11-05 (contra Unity 6.3 LTS, pin 6000.3.x; `design/gdd/save-local.md` (#28), `fluxo-de-fase.md` (#3), `dados-e-balanceamento.md` (#1), ADR-0001 e ADR-0002)

## Decision Makers
Rodrigo Reis (premissas confirmadas em 2026-11-05; as decisões de jogo do GDD #28 já vêm do autor), Claude Code (autoria), `unity-specialist` (validação de API, 5.5) e `technical-director` (gate TD-ADR, 5.6). Os resultados das duas revisões entram na seção Risks antes de gravar.

## Summary
O save local (#28) precisa de uma decisão técnica sobre como o progresso vira bytes no disco do Android sem nunca perder o último save bom: o formato do arquivo, a ordem do commit e a troca atômica, o checksum, o backup, a thread de gravação, o comportamento na pausa e a política do Auto Backup. Decidido: um envelope binário TLV com fatias opacas e FNV-1a de 64 bits no cabeçalho e no corpo; um commit atômico com temporário, backup por troca e quarentena; um gravador único numa thread própria, com o retrato montado na thread principal; flush síncrono com teto só na pausa fora de fase; e o Auto Backup do Android só para o `save.dat`. **Quase tudo que toca o Android (arquivos, `fsync`, JNI, backup, ciclo de vida) é `NOT SOURCEABLE`** e entra como hipótese a verificar num spike, não como fato.

## Engine Compatibility

| Field | Value |
|-------|-------|
| **Engine** | Unity 6.3 LTS (6000.3.x; editor instalado 6000.3.27f1) |
| **Domain** | Core |
| **Layer** | Foundation |
| **Knowledge Risk** | HIGH (`docs/engine-reference/unity/VERSION.md`) |
| **References Consulted** | `docs/engine-reference/unity/VERSION.md` (módulo Android com IL2CPP instalado; aparelho de referência não verificado), `breaking-changes.md` (Android: API mínima 24 desde o Unity 6.0), `deprecated-apis.md`, `current-best-practices.md`; `design/gdd/save-local.md` (#28, regras 1 a 14, F1 a F4, estados, Edge Cases, Knobs, "Vira ADR"); ADR-0001, ADR-0002 e `docs/registry/architecture.yaml`. **Não existe `docs/engine-reference/unity/modules/core.md`** e a referência **não cobre** nada do armazenamento no Android (`NOT SOURCEABLE`) |
| **Post-Cutoff APIs Used** | Nenhuma API da Unity dentro do envelope, do serializador e da máquina de estados (asmdef sem engine). A camada com Unity usa `Application.persistentDataPath`, `OnApplicationPause`, `AndroidJavaObject` (JNI) e a thread do gravador; APIs antigas e estáveis, mas o comportamento delas no 6000.3.27f1 e no Android é `NOT SOURCEABLE`. BCL usada: `System.IO` (`File.Replace`, `FileStream.Flush(true)`), `System.Threading`; disponibilidade e semântica no perfil de API do projeto e no IL2CPP são `NOT SOURCEABLE`. |
| **Verification Required** | **Gate de aceitação (só isto bloqueia a aceitação, porque muda o desenho):** (G1) a raiz do save resolvida, com os 4 caminhos logados (item 1); (G2) existe uma troca atômica por **algum** dos três caminhos: `File.Replace`, libc `rename` ou JNI `Os.rename` (itens 2 e 4); (G3) o `fsync` do diretório é viável por libc ou JNI (item 3); (G4) `File.Replace` com destino ausente e presente se comporta como previsto (item 2). **Os itens 5 a 10 e as medições do item 11 (c a g) são Validation Criteria das primeiras stories e não bloqueiam a aceitação.** (1) No Android, `Application.persistentDataPath` resolve para o armazenamento **externo específico do app** (`.../Android/data/<pkg>/files`, por `getExternalFilesDir`), o que a ScriptReference genérica de `Application.persistentDataPath` **documenta** (revisão TD-ADR; não é uma página específica do 6000.3, e a referência local não cobre isso); a queda para o interno quando o externo está indisponível é conhecimento do especialista (`NOT SOURCEABLE`); por isso a raiz do save vem do JNI `getFilesDir()`, e o spike loga os quatro caminhos (`persistentDataPath`, `getFilesDir`, `getExternalFilesDir`, `getNoBackupFilesDir`) nas combinações de "Write Permission" e "Install Location". (2) `File.Replace(origem, destino, null)` troca de forma **atômica** no IL2CPP ARM64 do aparelho (se só houver `Delete` + `Move`, existe uma janela com o principal ausente; ver a tabela de pontos de queda). O `File.Replace` costuma lançar quando o destino não existe (primeiro commit e primeira rotação): a interface trata o destino ausente com `Move`. **Sem uma troca atômica comprovada no spike, o ADR não é aceito** (ou se aceita explicitamente a perda de um commit já confirmado na janela). (3) `FileStream.Flush(true)` leva o conteúdo ao disco (`fsync`) no Android, e se o `fsync` do **diretório** é necessário e como fazê-lo (libc ou JNI). O `fsync` do diretório só protege contra queda de energia ou do kernel (a morte do processo não perde o cache de páginas), e o **Confirmado só vem depois dele**. (4) Plano B da troca atômica: P/Invoke direto no libc (`rename`, `open`, `fsync`, `close`; `NOT SOURCEABLE` que `DllImport("libc")` resolve no IL2CPP Android) e, se não resolver, plano C por JNI (`android.system.Os.rename`). (5) O flush síncrono com teto na pausa termina antes de o Android congelar ou matar o app (`OnApplicationPause`, congelador de apps em cache do Android 11+), e o `OnApplicationPause(true)` chega na thread principal entre frames; o congelador também pode parar o gravador no meio de uma escrita (a tabela de pontos de queda cobre). O teto fica em 150 a 250 ms (máximo 500 ms), porque o SO não espera a pausa por muito mais. (6) O Auto Backup inclui só o `save.dat` por `fullBackupContent` e `dataExtractionRules` (Android 12+), e o comportamento de restauração foi testado com `adb shell bmgr`. (7) O marcador em `noBackupFilesDir` (caminho por `UnityPlayer.currentActivity.getNoBackupFilesDir()`, uma chamada JNI no boot) não é restaurado e sobrevive a um update (`adb install -r`); a reinstalação apaga save e marcador. A build que introduz o marcador não precisa de regra especial antes do lançamento (não há usuários nem builds antigas com save relevante); **gatilho:** se alguma build com save for a testadores externos antes do marcador, a regra volta. (8) A thread do gravador (`System.Threading.Thread`) roda em IL2CPP sem custo de GC por commit e sem deadlock com a thread principal; parada cooperativa (sem `Thread.Abort`), buffer de serialização reutilizado, o loop todo em `try/catch` e `Dispose` ligado a `Application.quitting` e ao fim do Play Mode (domain reload desligado). (9) Tempo de montagem do retrato (F3), bytes alocados na montagem e na serialização, p95 do tempo total de escrita com `fsync` o tempo até a confirmação e o **tempo até Confirmado do `BeginStage`** (dois commits, duas releituras e 3 a 4 `fsync` antes de a fase começar), com o roster máximo, no aparelho de referência. (10) O stripping do IL2CPP não remove nada do serializador, que é escrito à mão e registrado por referência direta. (11) **Spike curto num aparelho Android real, build de desenvolvimento, com logcat:** (a) logar os quatro caminhos nas combinações de "Write Permission" e "Install Location" e num aparelho com cartão SD; (b) `File.Replace` com destino ausente e presente, com 100 mil leituras numa outra thread conferindo que o destino nunca some, comparado com `rename` via libc; (c) medir `Flush(true)`, `fsync` de arquivo e `fsync` de diretório (p50, p95 e p99 em 200 gravações de cerca de 50 KB); (d) `kill -9` no meio de um loop de commits e a abertura seguinte; (e) a pausa: tempo do callback, atraso na transição com espera de 200 ms e se a thread termina com o app em segundo plano por 15 minutos ou mais no Android 12+; (f) `bmgr` (backup, restauração e `dumpsys backup`) e o marcador; (g) Profiler no aparelho (GC.Alloc) na montagem do retrato e na thread do gravador. A queda de energia **não se simula** no Editor nem por `kill -9`: a injeção de falha prova a lógica, não a durabilidade. |

## ADR Dependencies

| Field | Value |
|-------|-------|
| **Depends On** | ADR-0001 (`Proposed`: serialização sem reflexão, sem `static` mutável, as respostas do #28 entram na thread principal) e ADR-0002 (`Proposed`: IDs estáveis, `IDataVersion`, a função FNV-1a 64 pública e sem estado de `Forja.Data`, ADR-0002 §6; o nome `Fnv1a64` não consta nas Key Interfaces dele e se fixa neste ADR). A varredura é conclusiva: são os únicos outros ADRs. Devem estar `Accepted` antes deste. |
| **Enables** | GDD #3 (`BeginStage`, a marca e o commit de fim), #16, #17 e #19 (as fatias de cada sistema), #26 (hora efetiva), #5 (a interface de eventos do #28), #29 (exportação e importação do retrato, `saveSequence`, `maxSeenUtc`). |
| **Blocks** | Épicos do #28 e qualquer story que grave progresso, marca de fase ou selo. Nenhuma story existe ainda, então nenhuma está `Blocked` hoje. |
| **Ordering Note** | Depois do ADR-0001 e do ADR-0002 aceitos. Só o **gate de aceitação** (G1 a G4, no início de Verification Required) precisa passar num spike curto num aparelho Android real antes da aceitação; o resto do spike vira Validation Criteria das primeiras stories e não bloqueia. A queda de energia não se simula. |

## Context

### Problem Statement
O GDD #28 define o que o save guarda e como ele nunca perde o último estado bom (commit único, principal e backup verificados, temporário órfão nunca promovido, marca "fase em andamento", quarentena, só leitura para formato mais novo). Ele deixa para este ADR (OQ-1) as decisões de implementação: formato autodescritivo e envelope, local de gravação, escrita atômica e `fsync`, checksum e backup, gravação fora da thread principal e na pausa, Auto Backup, flag de "sujo", tabela de pontos de queda, serialização sem reflexão, limpeza do temporário, interface de armazenamento injetável, API concreta da troca atômica, o marcador de restauração e o formato TLV. A decisão precisa vir antes dos GDDs dos sistemas que entregam fatias.

### Constraints
- Dev solo; o custo de implementação e de teste pesa mais que a sofisticação.
- Android primeiro, aparelho de referência não verificado; o Android pode matar o app a qualquer momento.
- Nunca durante uma fase e nunca dentro do tick (ADR-0001); a gravação não pode travar o frame (F3).
- Um gravador único; toda resposta ao #3 e ao #17 volta à thread principal (ADR-0001, GDD #3).
- Sem reflexão (stripping do IL2CPP) e sem `static` mutável (`mutable_static_in_simulation`).
- O save nunca guarda valores de balanceamento nem posses pagas; só IDs, carimbo da versão e revisão da skill selada (GDD #28, regra 3).
- A referência de engine não cobre o armazenamento no Android (`NOT SOURCEABLE`).

### Requirements
- Um commit é inteiro; uma gravação que falha nunca destrói o save bom; o principal nunca fica ausente durante uma gravação.
- Detectar corrupção (cabeçalho e corpo), restaurar o backup, preservar evidência em quarentena e nunca apagar sem confirmação.
- Campos e fatias desconhecidos passam intactos; formato mais novo abre em só leitura.
- Interface de armazenamento injetável, com injeção de falha, para testar cada ponto de queda em EditMode.
- O resultado de um commit é sempre real (Confirmado ou Falhou com causa), nunca "tempo esgotado".

## Decision

### Visão geral
```
 Sistemas (#16, #17, #19, #3, #26)      Forja.Save (sem engine)                     Camada com Unity (Forja.Gameplay)
 entregam a fatia (retrato) ───────▶  SaveService: estados, commit, marca,   ◀──▶  AndroidStorage : ISaveStorage
 na thread principal (F3)               quarentena, F1/F2, flag "sujo"               persistentDataPath, File.Replace,
                                        └ gravador único (thread própria)            Flush(true), JNI (rename, fsync dir,
                                          serializa TLV + FNV-1a, grava,             noBackupFilesDir), OnApplicationPause
                                          verifica, rotaciona                        resposta ──▶ fila lida entre frames
```

### 1. Local e arquivos
Os arquivos ficam numa subpasta `Save/` da **raiz do save**: no Android, a raiz vem do JNI `getFilesDir().getAbsolutePath()` (armazenamento **interno** do app), chamado uma vez no boot, na thread principal, e guardado (nunca se persiste caminho absoluto, porque o caminho pode mudar se o app for movido); no Editor, vem de `Application.persistentDataPath` e os testes usam uma pasta temporária. O boot loga os quatro caminhos; se o JNI falhar ou devolver um caminho sob `/Android/data/`, o estado é `StorageUnavailable` com evento e o jogo **nunca** cai em silêncio para o `persistentDataPath` (a origem real dele no Android é `NOT SOURCEABLE` além do que a ScriptReference documenta, item 1 de Verification Required). Os arquivos são `save.dat` (principal), `save.bak` (backup), `save.tmp` (temporário do commit), `save.bak.tmp` (temporário da rotação) e a quarentena `q-{utc}-{motivo}` (só dígitos, letras e `-` no nome, sem `:`, porque alguns sistemas de arquivos rejeitam outros caracteres; sufixo se colidir, nunca sobrescreve evidência; as 3 mais novas de Corrompido rotacionam, e a de Irrecuperável fica "pendente de decisão", estado que persiste entre aberturas sem save por um sufixo `-pendente` no nome, retirado por `MoveNoOverwrite` quando o jogador decide; o move para a quarentena também usa `MoveNoOverwrite`, nunca `Replace`). `PlayerPrefs` **não** serve para progresso (sem atomicidade nem backup). O espaço de disco cheio é tratado pela regra 12 do GDD: a gravação falha com `IOException`, o progresso fica em memória, e o ADR **não** tenta prever o espaço (a API é `NOT SOURCEABLE`); o necessário é cerca de 3 cópias mais a quarentena.

### 2. Envelope binário TLV
Um arquivo é um **cabeçalho fixo** seguido de um **corpo TLV**, `little-endian` explícito, escrito e lido campo a campo (nunca memória bruta de struct):
- **Cabeçalho (posições que nunca mudam entre versões):** `magic`, versão do formato (inteiro), algoritmo do checksum (`1` = FNV-1a de 64 bits), tamanho do corpo, **checksum do corpo** e **checksum do próprio cabeçalho** sobre os bytes anteriores a ele. O cabeçalho é lido e verificado **antes** do corpo, e o tamanho do corpo é conferido contra o tamanho real do arquivo e contra um teto antes de alocar: cabeçalho com checksum inválido é **corrupção** (vai ao backup), nunca "formato mais novo" (GDD #28, regra 9). O layout exato dos bytes fixa-se na primeira story do #28.
- **Corpo:** uma sequência de TLV (`tag` de 16 bits, `tamanho` de 32 bits, valor opaco). Os campos do envelope (carimbo dos dados, `saveSequence`, `maxSeenUtc`, a lista de fatias, a marca "fase em andamento") e **cada fatia** são TLV. Uma fatia leva o seu identificador, a **versão própria** e os bytes do dono; o #28 guarda e devolve os bytes e **não** interpreta o que está dentro. **Tag, fatia ou campo desconhecido passa intacto** de uma gravação para a seguinte.
- **Aditivo:** campo novo só no fim ou em tag nova; um binário antigo ignora o que não conhece. É isso que permite a consulta em só leitura quando o formato é mais novo (se o formato não for aditivo, a tela mostra só a mensagem, GDD #28, regra 9).
- **Checksum:** **FNV-1a de 64 bits** (a função pública e sem estado de `Forja.Data`, ADR-0002 §6; o nome `Fnv1a64` se fixa aqui), por byte, para o cabeçalho e para o corpo, sem algoritmo novo. Ele detecta **corrupção acidental, não é anti-cheat** (regra 8). O "CRC do cabeçalho" do GDD é, aqui, um FNV-1a independente do checksum do corpo.
- **Limites:** `saveSequence` lido acima de 2^53 faz o arquivo ser tratado como corrompido (F2).

### 3. Commit atômico
Cada gravação é um commit inteiro, nesta ordem (regra 7 do GDD):
1. serializar o retrato e escrever `save.tmp`, com `Flush(true)`;
2. reler `save.tmp` do disco e conferir o checksum (detecta bug do serializador e escrita curta, **não** corrupção física);
3. reverificar o principal; só então copiar para `save.bak.tmp`, reler e conferir, e **trocar** `save.bak.tmp` por `save.bak` (nunca se copia por cima do backup; se a cópia falhar, é **rotação pulada** e o commit segue);
4. trocar `save.tmp` por `save.dat`. **O commit passa a existir depois dessa troca (vale para a morte do processo, porque o cache de páginas sobrevive) e só é confirmado a quem o pediu depois do `fsync` do diretório (vale para a queda de energia).** Num commit de **selo**, logo depois (5), o principal novo, reverificado, vira o backup por uma segunda rotação, sem atrasar o "Confirmado".
A **troca** é uma operação atômica da interface de armazenamento: `File.Replace(origem, destino, null)` é a primeira escolha, e, como o `File.Replace` costuma lançar quando o destino não existe (primeiro commit e primeira rotação), a interface faz `Move` se o destino não existe e `File.Replace` se existe (um gravador único não cria corrida). O plano B é um P/Invoke direto no libc (`rename`, que sobrescreve de forma atômica pelo POSIX, e `open`, `fsync`, `close`; `NOT SOURCEABLE`), e o plano C é o JNI `android.system.Os.rename`. **Se só existir `Delete` + `Move`, existe uma janela com o principal ausente**: como o commit ainda não foi confirmado, a abertura seguinte restaura o backup, que é o commit anterior **desde que a rotação não tenha sido pulada** (F4c); com rotação pulada e troca não atômica, um commit já confirmado se perderia, e por isso **a troca atômica comprovada no spike é condição para aceitar este ADR**. O `fsync` do arquivo é `Flush(true)` (se o caminho da libc vencer no spike, a escrita inteira passa a ser por libc, com `open`, `write`, `fsync` e `close`, em vez de misturar `FileStream` com o descritor, cujo acesso no IL2CPP Android é `NOT SOURCEABLE`; a latência do `Flush(true)` no spike indica se sincronizou: microssegundos = não); o do **diretório** só protege contra queda de energia ou do kernel (a morte do processo não perde o cache de páginas) e é feito por libc (`open`, `fsync`, `close` no diretório) ou por JNI (`Os.fsync`). **O `Confirmed` só é enviado depois do `FsyncDirectory`**: sem ele a troca poderia ser desfeita e um commit já confirmado seria perdido (o custo é o de um `fsync` a mais, de 5 a 50 ms em flash boa e com cauda de 100 a 500 ms em eMMC barata, `NOT SOURCEABLE`). Um temporário que sobra é **órfão e nunca é promovido** (promovê-lo ressuscitaria um selo que o #17 não confirmou) e é apagado na próxima abertura; **antes de apagar um temporário órfão com checksum válido, a abertura lê o `saveSequence` dele**, porque ele entra no máximo da F2.

A **marca de fase** (`BeginStage`) é um commit como os outros e **rotaciona o backup**: é a opção mais simples e mantém a F4 em "normalmente 1 commit". O custo é o `BeginStage` ter duas escritas, duas releituras e 3 a 4 `fsync` antes de a fase começar (latência na tela de carregamento, com cauda de 100 a 500 ms por `fsync` em eMMC barata, `NOT SOURCEABLE`); o tempo até Confirmado do `BeginStage` é medido (item 9), e uma **marca sem rotação do backup** fica como plano de ajuste a reavaliar contra a F4 e a regra 8 do GDD (Alternativa 10). *(Provisória.)*

### 4. Tabela de pontos de queda
O que fica no disco se o app morrer em cada ponto, e o que acontece na abertura seguinte (`N` = último commit confirmado):

| Ponto do corte | Disco depois do corte | Abertura seguinte |
|---|---|---|
| Durante a escrita de `save.tmp` | `save.dat` = N, `save.bak` = N−1, `save.tmp` parcial | O temporário é órfão e é apagado; estado Válido (N) |
| `save.tmp` completo, antes da troca | `save.dat` = N, `save.tmp` completo e não confirmado | Órfão, nunca promovido, apagado; Válido (N) |
| Durante a cópia para `save.bak.tmp` | `save.dat` = N, `save.bak` intacto, `save.bak.tmp` parcial | `save.bak.tmp` apagado; Válido (N); o backup é refeito no próximo commit |
| `save.bak.tmp` completo, antes da troca | `save.bak.tmp` = cópia de N, `save.bak` = N−1 | `save.bak.tmp` apagado; Válido (N) com o backup mais velho (rotação pulada, F4c) |
| Durante a troca `save.bak.tmp` por `save.bak` | atômica: `save.bak` = N−1 ou N; sem API atômica, o backup pode faltar | Backup ausente ou inválido com principal válido: refeito no próximo commit, sem aviso |
| Durante a troca `save.tmp` por `save.dat` | atômica: `save.dat` = N ou N+1; sem API atômica, o principal pode faltar | Atômica: Válido (N ou N+1). Sem API atômica: principal ausente e o backup é restaurado como "Corrompido": se a rotação não foi pulada ele já é N, e o commit N+1 não tinha sido confirmado a ninguém, então nada confirmado se perde; com rotação pulada ele é N−k e um commit confirmado se perde (por isso a troca atômica é condição de aceitação) |
| Troca concluída, antes de avisar quem pediu (morte do processo) | `save.dat` = N+1 | Válido (N+1); o herói aparece selado, sem aviso extra (regra 12) |
| Troca concluída, antes do `fsync` do diretório, **queda de energia** | `save.dat` = N ou N+1 (a troca pode ser desfeita) | Válido (N ou N+1); os dois são aceitáveis porque nada foi confirmado; no selo, o #17 nunca mostrou concluído |
| Durante a segunda rotação do selo | `save.dat` = N+1, `save.bak` = N (ou `save.bak.tmp` parcial) | Válido (N+1); a rotação é refeita no próximo commit |
| Durante o move do principal suspeito para a quarentena, ou a restauração do backup | principal em quarentena e/ou ausente, backup intacto | O estado é reavaliado: restaura de novo; os nomes `q-...` colidem com sufixo, nunca sobrescrevem evidência |
| Durante o commit de consumo da marca ou da restauração | a marca ainda está no disco | A marca é informada de novo com o mesmo `attemptId`; o efeito do #3 e o #5 deduplicam (regra 6) |
| Durante o commit síncrono do "recomeçar" | a marca "pendente de decisão" continua | A pergunta volta; só um commit concluído limpa a marca |
| Voltar (`CancelStage`) cobre um `BeginStage` pendente | nenhuma marca no disco (o `CancelStage` nunca grava a marca); se cobre um `Seal`, a 2ª rotação é mantida | A abertura seguinte não encontra marca; nada a consumir |

### 5. Gravador único, fora da thread principal
O retrato das fatias é montado **na thread principal** dentro do orçamento da F3 (`SAVE_MAIN_THREAD_BUDGET_MS`, a medir no aparelho de referência); **a serialização, o checksum e todo o disco** rodam numa **thread dedicada** (o gravador único). **O retrato entregue ao gravador é uma cópia própria**, sem referência a estado vivo; os serializadores das fatias são **funções puras e thread-safe** sobre o retrato, e nenhum objeto do jogo é lido fora da thread principal (contrato que os donos das fatias, #16, #17 e #19, herdam). Os pedidos entram numa fila de capacidade 1: **um pedido novo substitui o que esperava** (cada retrato é inteiro), e cada tentativa reserva o seu `saveSequence` (F2). O pedido substituto resolve duas coisas por regras separadas. **A rotação do backup** segue o tipo mais forte (`Seal` > os demais), para que um `Seal` coberto por um `Normal` (a pausa) ou por um `CancelStage` não perca a segunda rotação. **A marca "fase em andamento"** não segue o tipo: vale o **último pedido** (um `BeginStage` põe a marca, um `CancelStage` limpa a marca do seu `attemptId`, os demais mantêm a marca em vigor); por isso um `CancelStage` que cobre um `BeginStage` ainda pendente nunca grava a marca; **cada pedido coberto recebe o seu próprio `CommitResult`** (com o `RequestId` e o `AttemptId` dele) quando o commit que o cobre termina. O resultado (`Confirmado` ou `Falhou` com causa, **nunca** "tempo esgotado") volta numa fila que a ponte esvazia **entre frames, na thread principal**; nenhuma continuação do #28 roda em outra thread. O `SAVE_COMMIT_CONFIRM_TIMEOUT_MS` é só o limite de espera da tela. Nos testes a fila é manual. O gravador é uma `System.Threading.Thread` com parada **cooperativa** (sem `Thread.Abort`, que o IL2CPP não suporta), o loop inteiro em `try/catch` (uma exceção não tratada derrubaria o app), buffer de serialização reutilizado (para a thread não gerar lixo e disparar um GC que pausa a thread principal) e `Dispose` ligado a `Application.quitting` e ao fim do Play Mode (com domain reload desligado a thread sobreviveria). O `Dispose` drena o commit em andamento com o mesmo teto da pausa e abandona o pedido que ainda não começou (melhor esforço, a tabela cobre). O gravador roda em prioridade normal (uma prioridade baixa o deixaria sem CPU e atrasaria a confirmação). JNI a partir dessa thread exigiria `AttachCurrentThread` e `DetachCurrentThread` no `finally`; o caminho por libc evita isso. *(Provisória; o custo de GC e a ausência de deadlock são `NOT SOURCEABLE`, itens 8 e 9.)*

### 6. Pausa e segundo plano
Fora de uma fase, `OnApplicationPause(true)` (nunca `Focus`, que também dispara por notificação e janela flutuante) pede um commit e **espera de forma síncrona com um teto de tempo** (`SAVE_PAUSE_FLUSH_CEILING_MS`, knob novo do #28; padrão provisório de 150 a 250 ms e **máximo de 500 ms**, nunca segundos, porque o SO não espera a pausa por muito mais) pela thread do gravador; passado o teto, o resultado continua Pendente e o gravador segue. Durante a espera a thread principal só bloqueia em `Wait(timeout)`, nunca no disco. **Durante uma fase, a pausa não grava** (a marca já cobre, regra 5); "durante a fase" é **do pedido de `BeginStage` até o commit de fim**, e durante a espera do `BeginStage` a pausa não cria pedido novo (a tentativa nasce Pausada, GDD #3, Regra 11). Com um commit em andamento a pausa espera **dois** commits (o atual e o substituto), então o teto estoura com frequência em eMMC lenta; isso é aceito (melhor esforço) e o resultado fica Pendente. Se o flush termina antes de o Android congelar ou matar o app é `NOT SOURCEABLE` (item 5). Sem nada alterado desde o último commit não há commit novo (Seção 8).

### 7. Auto Backup e o marcador de restauração
O save **entra** no Auto Backup do Android (decisão do autor, GDD #28, Edge Cases). Só o `save.dat` é incluído; `save.bak`, os temporários e a quarentena **ficam de fora**, pelo "Custom Main Manifest" do Unity (`Assets/Plugins/Android/AndroidManifest.xml`) com `android:allowBackup="true"`, `android:fullBackupContent` (Android 6 a 11) e `android:dataExtractionRules` (Android 12+), cujos XML ficam em `Assets/Plugins/Android/res/xml/` e incluem `Save/save.dat` com o domínio `file` (a raiz é interna). Nas `dataExtractionRules` as seções `cloud-backup` e `device-transfer` se declaram **as duas**, porque uma seção sem `<include>` leva tudo. **Avaliação pedida pelo GDD #28** (transferência de aparelho incluída e backup na nuvem excluído): mantidas as duas incluindo o `save.dat`, porque excluir a nuvem tiraria a cobertura de "reinstalei o app" que a decisão do autor lista (Alternativa 11), e o marcador avisa quando o que voltou é um snapshot restaurado; *(provisória, a reavaliar)*. com qualquer `<include>` o resto é excluído, inclusive o `PlayerPrefs` (decidir se serve). **Um marcador em `noBackupFilesDir`** (que o Auto Backup não restaura) é criado **no boot em que o estado é `Absent`, antes do primeiro commit** (sem save não há restauração a confundir; criá-lo depois do commit abriria a janela de um falso "restaurado" se o app morresse entre os dois). Se o save existe e o marcador não, o jogo sabe que **acabou de ser restaurado**, avisa e cria o marcador. Não há regra especial para a build que o introduz: antes do lançamento não há usuários nem builds antigas com save relevante, só aparelhos de teste; **se alguma build com save for a testadores externos antes do marcador, a regra volta.** O caminho do `noBackupFilesDir` vem de uma chamada JNI no boot (`UnityPlayer.currentActivity.getNoBackupFilesDir()`), e o arquivo é criado e conferido com `System.IO`. Tudo isso é `NOT SOURCEABLE` e entra no spike com `adb shell bmgr` (item 6 e 7).

### 8. Flag de "sujo" e a hora efetiva
Cada fatia entrega junto com o retrato um contador de alteração, e o envelope tem o seu. O save está **sujo** se alguma fatia **ou algum campo do envelope** mudou (marca posta ou limpa, "pendente de decisão", restauração), **exceto o `maxSeenUtc`**; um commit sem nada sujo **não é feito**. `BeginStage`, `ConsumeMark`, `CancelStage` e o "recomeçar" sempre sujam o envelope, então **sempre gravam**, mesmo sem fatia alterada. **O avanço do `maxSeenUtc` sozinho não suja o save** (ele viaja no próximo commit, qualquer que seja o motivo, regra 11). A hora vem de um `ISaveClock` injetável; a **hora efetiva** é a F1 do GDD (sanidade entre `BUILD_UTC` e `BUILD_UTC + CLOCK_SANITY_MS`; só cresce). `BUILD_UTC` vem de um `IBuildInfo` implementado na camada com Unity; **não** pode vir do snapshot de dados do ADR-0002, que não leva timestamp, e a origem exata é decisão da primeira story (`NOT SOURCEABLE`) dentro destas restrições: gerado no build, fora do snapshot, maior que 0, lido só por `IBuildInfo`, injetado nos testes e nunca derivado de data de arquivo em tempo de execução.

### 9. Serialização sem reflexão e serviço sem estado estático
Cada fatia tem um serializador **escrito à mão** (leitores e escritores TLV), **registrado por referência direta**: sem reflexão, sem `JsonUtility`, sem `BinaryFormatter`, sem `link.xml`. O `SaveService` é uma instância injetada: **sem `static` mutável**, sem `static event` e sem cache estático (`mutable_static_in_simulation`). Todo `Parse` e `ToString` usa a cultura invariante e toda ordenação de IDs usa `StringComparer.Ordinal` (`culture_dependent_parse`).

### 10. Interface de armazenamento injetável
Todo acesso a disco passa por `ISaveStorage` (`WriteAll` com flush, `TryReadAll`, `Exists`, `Replace` atômico, `MoveNoOverwrite`, `Delete`, `TryList`, `FsyncDirectory`, `PersistentRoot`). Há duas implementações: a do Android (camada com Unity) e uma em memória com **injeção de falha** (corta a operação N, devolve `IOException`, simula disco cheio, sumiço de arquivo), usada pelos testes EditMode para exercitar **cada linha da tabela de pontos de queda**.

### Key Interfaces
```csharp
namespace Forja.Save   // asmdef sem engine; referencia Forja.Data (FNV-1a 64, IDataVersion); Forja.Data nunca referencia Forja.Save
{
    public enum SaveState { Absent = 0, Valid = 1, OldFormat = 2, Corrupted = 3, Unrecoverable = 4, NewerFormat = 5, MigrationFailed = 6, StorageUnavailable = 7 }
    public enum CommitKind { Normal = 0, StageMark = 1, StageEnd = 2, Seal = 3, Restore = 4, StageCancel = 5 }   // na substituição, a ROTAÇÃO do backup segue o mais forte (Seal > os demais); o estado da MARCA não segue o tipo: vale o último pedido (BeginStage põe, CancelStage limpa a marca do seu attemptId)
    public enum ReadResult { Ok = 0, NotFound = 1, IoError = 2 }     // a regra 14 separa "não existe" de "erro de leitura"
    public enum CommitOutcome { Pending = 0, Confirmed = 1, Failed = 2 }   // nunca "tempo esgotado"

    public readonly struct AttemptId : IEquatable<AttemptId> { public readonly ulong High; public readonly ulong Low; }   // 128 bits, comparado só por igualdade; o valor vem de fonte injetada (GDD #3, #28 OQ-7)

    public readonly struct CommitResult { public readonly int RequestId; public readonly AttemptId AttemptId; public readonly CommitOutcome Outcome; public readonly int FailureCause; }   // um resultado por pedido, inclusive os cobertos por substituição

    public interface ISaveStorage     // injetável; implementação Android na camada com Unity, e uma em memória com injeção de falha
    {
        string PersistentRoot { get; }   // Android: JNI getFilesDir(), lido uma vez no boot; Editor: persistentDataPath (testes usam pasta temporária)
        void WriteAll(string path, ReadOnlySpan<byte> bytes);   // com flush ao disco
        ReadResult TryReadAll(string path, out byte[] bytes);
        bool Exists(string path);
        void Replace(string source, string destination);        // troca atômica; destino ausente = Move, senão File.Replace; plano B: libc rename; plano C: JNI Os.rename
        void Delete(string path);
        ReadResult TryList(string folder, out string[] names);
        void MoveNoOverwrite(string source, string destination);   // falha se o destino existe; quarentena e sufixo "-pendente"
        void FsyncDirectory(string folder);                      // NOT SOURCEABLE; libc (open, fsync, close no diretório); JNI Os.fsync só como plano C, com attach e detach
    }

    public interface ISaveClock { long NowUtcMs { get; } }
    public interface IBuildInfo { long BuildUtcMs { get; } }
    public interface ISaveEventSink { void Emit(in SaveEvent e); }   // #5; sink nulo e buffer no boot

    public interface ISaveService     // thread principal; um gravador único por trás
    {
        SaveState State { get; }
        void RequestCommit(int requestId, CommitKind kind, in SaveSnapshot snapshot);     // retrato montado na thread principal (F3); o requestId vem de uma fonte única, compartilhada e injetada, usada por todos os chamadores (#3, #17), e é único entre eles
        void BeginStage(int requestId, in StageMark mark);                                 // marca "fase em andamento"; só começa a fase depois de Confirmed ou Failed real; em só leitura ou com StorageUnavailable o Failed entra na fila na hora (regra 6)
        bool TryDequeueResult(out CommitResult result);                    // lido entre frames, na thread principal
        long EffectiveUtcMs { get; }                                       // F1; só cresce
        void CancelStage(int requestId);                                   // Voltar do #3: limpa a marca (CommitKind.StageCancel); nunca grava a marca, mesmo quando cobre um BeginStage pendente
        void ConsumeMark(in MarkAnswer answer);                            // resposta do #3 ao "marca encontrada"
    }
    // SaveSnapshot, StageMark, MarkAnswer, SaveEvent e o layout dos bytes do cabeçalho: definidos na primeira story do #28. StageMark, MarkAnswer e o campo TLV da marca levam o attemptId como AttemptId (128 bits), nunca como int.
}
```
Os nomes e as assinaturas são o contrato do ADR; as fatias pertencem aos GDDs e ADRs dos sistemas donos.

### Implementation Guidelines
- O save **must never** gravar durante uma fase nem dentro do `Tick`, e **must never** ser acionado de dentro de um `ISimSystem`.
- Todo acesso a disco **must** passar por `ISaveStorage`; **must never** haver `File`, `Directory` ou `PlayerPrefs` fora da implementação do armazenamento.
- A ordem do commit **must** ser: temporário, releitura e conferência, reverificação do principal, cópia para `save.bak.tmp`, troca do backup, troca do principal, e só então Confirmado; **must never** copiar por cima do backup nem promover um temporário que sobrou.
- A troca **must** ser atômica por `File.Replace`, libc `rename` ou JNI `Os.rename`; `Delete` + `Move` **must never** ser usado sem um aceite explícito registrado neste ADR, e a janela dele **must** estar na tabela de pontos de queda.
- O cabeçalho **must** ser verificado antes do corpo, com o próprio checksum; cabeçalho inválido **must** ser tratado como corrupção, **must never** como "formato mais novo".
- O envelope **must** ser TLV `little-endian`, escrito campo a campo; **must never** gravar memória bruta de struct, nem usar `BinaryFormatter`, `JsonUtility` ou reflexão; fatia, tag e campo desconhecidos **must** passar intactos.
- O checksum **must** ser a função FNV-1a 64 pública e sem estado de `Forja.Data` (nome `Fnv1a64` fixado aqui), `unchecked`; **must never** introduzir outro algoritmo sem emenda.
- O resultado de um commit **must** ser sempre `Confirmed` ou `Failed` real; **must never** existir "Falhou por tempo esgotado", e o timeout **must** ser só da tela.
- Toda resposta do `ISaveService` **must** chegar à thread principal por uma fila lida entre frames; **must never** haver continuação em outra thread.
- Um commit sem fatia nem campo do envelope alterado **must never** ser feito; o avanço do `maxSeenUtc` sozinho **must never** sujar o save; `BeginStage`, `ConsumeMark`, `CancelStage` e o "recomeçar" **must** sempre gravar.
- A pausa **must** usar `OnApplicationPause`, **must never** usar `Focus`, e **must never** gravar durante a fase.
- O serviço **must never** ter `static` mutável, `static event` nem cache estático; **must** ser uma instância injetada.
- Nada **must** apagar a quarentena de Irrecuperável sem a confirmação em 2 passos, e **must never** sobrescrever evidência (sufixo no nome).
- O Auto Backup **must** incluir só o `save.dat`; `save.bak`, os temporários e a quarentena **must never** entrar.
- Testes ficam em `Assets/Tests/EditMode/Save/`, com armazenamento em memória e injeção de falha, e **must** cobrir cada linha da tabela de pontos de queda e o caso de dois pedidos quase juntos.
- A raiz do save no Android **must** vir do JNI `getFilesDir()`, lida uma vez no boot na thread principal; **must never** persistir caminho absoluto nem usar `persistentDataPath` como raiz no aparelho.
- `ISaveStorage.Replace` **must** tratar o destino ausente (`Move` quando não existe), e o serviço **must never** enviar `Confirmed` antes do `FsyncDirectory`.
- A espera da pausa **must** usar o teto `SAVE_PAUSE_FLUSH_CEILING_MS` (padrão provisório e máximo na Seção 6), e a thread principal **must never** bloquear no disco.
- O gravador **must** ter parada cooperativa, loop em `try/catch`, buffer reutilizado e `Dispose` ligado a `Application.quitting` e ao fim do Play Mode; **must never** usar `Thread.Abort`.
- O tamanho do corpo do cabeçalho **must** ser conferido contra o tamanho real do arquivo e contra um teto antes de alocar, e os nomes da quarentena **must** usar só dígitos, letras e `-`.
- Os testes **must** usar uma pasta temporária; **must never** usar a pasta do jogo.
- O retrato entregue ao gravador **must** ser cópia própria, sem referência a estado vivo; os serializadores das fatias **must** ser funções puras e thread-safe; **must never** haver leitura de objeto do jogo fora da thread principal.
- O `requestId` **must** vir de uma **fonte única, compartilhada e injetada**, usada por todos os chamadores (#3, #17), de modo que seja único entre eles (contador determinístico nos testes); o resultado **must** levar `RequestId` e `AttemptId` (128 bits); **must** haver um `CommitResult` por pedido, inclusive os cobertos por substituição.
- Na substituição de pedidos, a rotação do backup **must** seguir o tipo mais forte (`Seal` > os demais) e o estado da marca **must** valer o último pedido; um `CancelStage` **must never** gravar a marca, mesmo ao cobrir um `BeginStage` pendente.
- O `attemptId` (128 bits) **must** vir de fonte injetada; **must never** usar `System.Random` nem `Guid.NewGuid()` dentro do código determinístico; **must** ser comparado só por igualdade e ter o mesmo tipo em `CommitResult`, `StageMark`, `MarkAnswer` e no campo TLV da marca.
- A quarentena e o sufixo `-pendente` **must** usar `MoveNoOverwrite`; **must never** usar `Replace` para eles.
- A abertura **must** ler o `saveSequence` de um temporário órfão com checksum válido antes de apagá-lo (F2).
- `ISaveStorage.TryReadAll` e `TryList` **must** distinguir `NotFound` de `IoError`; a regra 14 (até 3 leituras) só se aplica a `IoError`.
- `Forja.Data` **must never** referenciar `Forja.Save`; se o histórico de revisão do aparelho (ADR-0002) vier a ser persistido, isso **must** passar por uma interface definida em `Forja.Data` e implementada na raiz de composição.
- O `AndroidStorage` **must** morar em `Forja.Gameplay` (sem asmdef próprio) e **must** guardar a thread do gravador sem `static` mutável.
- Os eventos do #28 ao #5 **must** sair por `ISaveEventSink`, com sink nulo e buffer no boot.

## Alternatives Considered

### Alternative 1: `PlayerPrefs` para o progresso
- **Description**: Guardar o progresso em `PlayerPrefs`.
- **Pros**: Zero código de arquivo.
- **Cons**: Sem atomicidade, sem backup, sem checksum, sem controle do tamanho; o GDD #28 e o ADR-0001 o desaconselham para progresso.
- **Rejection Reason**: Não dá nenhuma das garantias da regra 7. Fica só para preferências triviais.

### Alternative 2: SQLite (plugin) ou outro banco embarcado
- **Description**: Um banco transacional no lugar do arquivo e do backup.
- **Pros**: Transações e recuperação prontas.
- **Cons**: Dependência de plugin nativo no Android (`NOT SOURCEABLE`); outro runtime para o dev solo manter; o GDD já descreve o commit inteiro, o backup e a quarentena em arquivos.
- **Rejection Reason**: O custo e o risco de plataforma superam o ganho para o tamanho do save do MVP.

### Alternative 3: JSON de texto (`JsonUtility` ou biblioteca) como envelope
- **Description**: Um JSON legível com um campo por fatia.
- **Pros**: Fácil de inspecionar e de editar à mão.
- **Cons**: `JsonUtility` é reflexão sobre tipos conhecidos e perderia campos e fatias desconhecidos (a regra 4 exige passar intactos); stripping do IL2CPP; sem tamanho por fatia; checksum sobre texto.
- **Rejection Reason**: O TLV opaco com tamanho dá a passagem de desconhecidos e a leitura aditiva sem reflexão. Um utilitário de editor pode exibir o save em texto.

### Alternative 4: Um arquivo só com diário (write-ahead log) em vez de principal, backup e temporário
- **Description**: Anexar commits a um único arquivo e compactar de vez em quando.
- **Pros**: Menos arquivos; leitura da última entrada válida.
- **Cons**: Compactação e truncamento são outra fonte de corrupção; a restauração e a quarentena do GDD (arquivos inteiros) ficam menos claras; o Auto Backup copia um arquivo que cresce.
- **Rejection Reason**: Três arquivos com troca atômica são mais simples de provar e de testar com injeção de falha, e já são o que o GDD descreve.

### Alternative 5: Gravar na thread principal (coroutine ou frame) em vez de uma thread dedicada
- **Description**: Serializar e gravar no próprio loop do jogo, em pedaços.
- **Pros**: Sem thread; sem risco de concorrência.
- **Cons**: A F3 exige que o disco e a serialização fiquem fora da thread principal; um `fsync` bloqueia o frame; em aparelho lento o hitch é perceptível ao selar ou ao ir para segundo plano.
- **Rejection Reason**: Um gravador único numa thread dedicada atende a F3. O risco de concorrência é contido pela fila de capacidade 1 e pelas respostas lidas entre frames.

### Alternative 6: Nuvem do Google Play Games no lugar do Auto Backup
- **Description**: Salvar o progresso como Saved Games na nuvem.
- **Pros**: Troca de aparelho mais robusta e detecção de conflito.
- **Cons**: Depende de conta e de rede; é escopo do Alpha (#29); o MVP é offline.
- **Rejection Reason**: Fica para o #29 (Alpha). O Auto Backup cobre troca de aparelho e reinstalação no MVP, com as ressalvas do GDD.

### Alternative 7: `File.Move(origem, destino, overwrite: true)` como troca
- **Description**: Trocar com a sobrecarga de `Move` que sobrescreve.
- **Pros**: Uma chamada só, sem tratar destino ausente.
- **Cons**: O GDD a cita; a sobrecarga talvez não exista no perfil de API do projeto (o .NET Standard 2.1 não a tem; `NOT SOURCEABLE`), e a atomicidade dela no Android também é `NOT SOURCEABLE`.
- **Rejection Reason**: Não há como saber se existe nem se é atômica sem o spike. Entra como candidata do item 2 se o perfil a expuser.

### Alternative 8: `android.util.AtomicFile` ou um plugin nativo que faça o commit inteiro
- **Description**: Delegar o commit à classe nativa da plataforma.
- **Pros**: É o recurso nativo para escrita atômica.
- **Cons**: Cruza o JNI com o buffer inteiro, não roda em EditMode, tem semântica própria de backup, e ainda exigiria a verificação, a rotação e a quarentena do GDD por cima.
- **Rejection Reason**: Perde a testabilidade com injeção de falha e não elimina a lógica do GDD.

### Alternative 9: `FileOptions.WriteThrough` ou `SafeFileHandle` no lugar do `fsync`
- **Description**: Pedir a escrita direta ao abrir o arquivo.
- **Pros**: Sem libc nem JNI para o arquivo.
- **Cons**: Não resolve o `fsync` do diretório nem a troca atômica, só o do arquivo; o comportamento no Android é `NOT SOURCEABLE`.
- **Rejection Reason**: Insuficiente sozinha; o `Flush(true)` ou a escrita por libc cobrem o arquivo.

### Alternative 10: Marca de fase sem rotação do backup
- **Description**: O commit de `BeginStage` grava só o principal, sem copiar para o backup.
- **Pros**: Menos `fsync` na tela de carregamento (um commit mais barato antes de cada fase).
- **Cons**: Muda a F4 e a regra 8 do GDD (backup só de principal reverificado a cada commit); o backup fica mais velho por mais tempo.
- **Rejection Reason**: Adotada a rotação em todo commit por ser a opção mais simples. Fica como plano de ajuste se o tempo até Confirmado do `BeginStage` estourar no aparelho.

### Alternative 11: `dataExtractionRules` só com transferência de aparelho (backup na nuvem excluído)
- **Description**: Incluir o `save.dat` só na seção `device-transfer` e excluir a `cloud-backup`.
- **Pros**: Cobre "troquei de celular" sem trazer de volta, depois de uma reinstalação, um snapshot velho de um backup de nuvem.
- **Cons**: Uma reinstalação ou um aparelho novo sem transferência direta perde todo o progresso; o GDD #28 (Edge Cases) decidiu que o save **entra** no Auto Backup justamente para cobrir reinstalação e troca de aparelho.
- **Rejection Reason**: Contradiz a cobertura que o autor decidiu. Fica como alternativa a reavaliar com dados do vertical slice, junto com a OQ-7 do GDD.

## Consequences

### Positive
- O último save bom nunca é destruído por uma gravação que falha: tmp, verificação, troca atômica e backup rotacionado só depois de reverificar.
- Cada ponto de queda tem um resultado definido e testável em EditMode, com injeção de falha, sem aparelho.
- O envelope TLV aditivo deixa fatias novas e campos novos entrarem sem migração, e abre em só leitura um formato mais novo.
- Nenhum algoritmo novo: o FNV-1a do projeto cobre cabeçalho e corpo.
- O serializador escrito à mão e o serviço sem estado estático combinam com o stripping do IL2CPP e com o domain reload desligado.

### Negative
- Quase tudo o que toca o Android é `NOT SOURCEABLE`: o ADR depende de um spike (aparelho, corte de energia, `bmgr`) antes de ser aceito.
- Se só existir `Delete` + `Move`, a troca não é atômica e a restauração cobre a janela; a garantia "principal nunca ausente" fica mais fraca.
- JNI para `fsync` de diretório, rename e `noBackupFilesDir` é código de plataforma que um dev solo precisa manter e testar no aparelho.
- O FNV-1a não é CRC: não tem a detecção de rajadas de erro de um CRC (para o tamanho do save do MVP, basta).
- A durabilidade contra queda de energia só se prova no aparelho: o Editor usa outro sistema de arquivos e outra implementação do `File.Replace`.
- Um gravador em thread dedicada traz risco de concorrência e de GC que só o spike mede.

## Risks
- **Troca não atômica no IL2CPP ARM64:** mitigação é a interface injetável, o plano B por JNI e a cobertura da janela pela restauração; o item 2 de Verification Required decide.
- **`fsync` do diretório necessário e não feito:** uma queda de energia logo depois da troca poderia desfazê-la; mitigação é o JNI se o spike mostrar que precisa, e o fato de o commit só ser confirmado depois do `FsyncDirectory`.
- **Flush da pausa não termina antes do congelamento ou da morte do app:** mitigação é o teto de tempo, o resultado Pendente e a regra de "tentativa falha" do #3; `NOT SOURCEABLE` (item 5).
- **Auto Backup restaurando um save mais velho que um selo:** é a brecha aceita pelo autor (GDD #28); o marcador avisa o jogador, e o #29 detecta a regressão no Alpha.
- **A queda de energia não se simula no Editor nem por `kill -9`:** a injeção de falha prova a lógica, não a durabilidade; mitigação é o spike no aparelho (item 11).
- **`persistentDataPath` fora do armazenamento interno (Android):** o caminho pode mudar entre sessões, o usuário pode ver e apagar a pasta, o FUSE tem `rename` e `fsync` menos previsíveis e o domínio do backup muda; mitigação é a raiz do save por JNI `getFilesDir()` e o estado `StorageUnavailable` no boot.
- **Thread do gravador:** deadlock ou GC por commit; mitigação é a fila de capacidade 1, o retrato imutável entregue ao gravador e o item 8 de Verification Required.
- **Serializador que perde campo desconhecido:** mitigação é o teste que grava um TLV desconhecido e confere que ele sobrevive a dois commits.
- **Dois escritores do mesmo arquivo (dois processos ou duas instâncias):** o gravador único é por processo; mitigação é o serviço ser singleton por injeção, sem `static`, e um teste.
- **Rotação pulada silenciosa:** o backup fica mais velho (F4c); mitigação é o evento ao #5 e a OQ-7 do GDD.
- **Validação do `unity-specialist` (5.5, 2026-11-05):** sem achado bloqueante; todas as afirmações são conhecimento do especialista (`NOT SOURCEABLE`). Incorporado: a raiz do save por JNI `getFilesDir()` (o `persistentDataPath` provavelmente aponta para o armazenamento externo do app), com `StorageUnavailable` no boot (ajustado pelo TD-ADR); `File.Replace` com destino ausente tratado por `Move`, plano B por libc e plano C por JNI, e a troca atômica comprovada como condição de aceitação; `Confirmed` só depois do `FsyncDirectory`; linha da tabela de pontos de queda corrigida para a rotação pulada; teto da pausa de 150 a 250 ms (máximo 500 ms); gravador com parada cooperativa, `try/catch`, buffer reutilizado e `Dispose`; XML de backup com as duas seções de `dataExtractionRules`; marcador criado só depois de ler um save válido, sem regra especial para a build que o introduz (cortada do MVP); tamanho do corpo conferido contra o arquivo; nomes da quarentena sem `:`; spike curto de 7 passos num aparelho real (item 11). O especialista não leu o GDD #28, então a fidelidade ao GDD não foi conferida por ele.
- **Revisão TD-ADR (5.6, 2026-11-05): CONCERNS, revisados a pedido do autor.** Sem REJECT e sem decisão tecnicamente errada. Corrigidos: (A) a flag de "sujo" pulava os commits de marca, consumo, cancelamento e recomeçar (agora o envelope também suja, exceto `maxSeenUtc`); (B) "só conta" contra "existe" (agora o commit existe depois da troca e só é confirmado depois do `FsyncDirectory`, com nova linha de queda de energia); a Guideline da troca agora cobre os três caminhos; o gate de aceitação foi enxugado a G1 a G4 e o resto virou Validation Criteria; o contrato com o GDD #3 (`requestId` do chamador, `AttemptId` no resultado, `CancelStage`, um resultado por pedido coberto, tipo mais forte herdado); `TryReadAll` de três valores, `MoveNoOverwrite` e `ISaveEventSink`; thread-safety do retrato como regra; `Fnv1a64` fixado como nome aqui; raiz com `StorageUnavailable`; fonte `persistentDataPath` documentada; marcador criado antes do primeiro commit; justificativa e medição da marca que rotaciona; "durante a fase" definido; alternativas 7 a 10; restrições do `BUILD_UTC`; o `AndroidStorage` em `Forja.Gameplay`. O TD não leu UI Requirements, Acceptance Criteria nem Open Questions do GDD #28, nem os ADRs vizinhos inteiros, e não avaliou o comportamento Android (`NOT SOURCEABLE`). **Decisão do autor sobre o escopo: um ADR só, com gate enxuto.** Plano de reserva: se o aparelho de referência não estiver disponível logo, separar um "ADR núcleo" (envelope, commit, tabela, `ISaveService` e `ISaveStorage`, testável em EditMode) de um "ADR do adaptador Android".
- **Caminho crítico e prazo:** três ADRs `Proposed` encadeados e um spike num aparelho ainda não verificado (VERSION.md); pelo `docs/CLAUDE.md`, stories que citam um ADR `Proposed` ficam bloqueadas, então o loop de meta (#16, #17, #19 e o #3 com a marca) espera o spike. É o maior risco de prazo para o dev solo; mitigação é o gate enxuto (G1 a G4), o spike em `prototypes/` que não depende do status do ADR e o plano de reserva de separar o núcleo.
- **Tamanho do contrato:** 8 estados, 6 tipos de commit, 12 linhas de pontos de queda, 3 planos de troca, JNI, P/Invoke e uma thread. Mitigação: o plano B (libc) e o plano C (JNI) só se implementam se o spike os exigir; não se escreve o que pode não ser preciso.
- **Corrida entre o gravador e a pausa:** a pausa espera dois commits quando há um em andamento e o teto estoura em eMMC lenta; aceito como melhor esforço, com o resultado Pendente. O congelador do Android 11+ pode parar o gravador no meio da escrita (a tabela cobre) e uma prioridade baixa o deixaria sem CPU (prioridade normal).
- **Pedido pendente no `Application.quitting`:** o `Dispose` drena o commit em andamento com o teto da pausa e abandona o pedido que ainda não começou (melhor esforço).

## GDD Requirements Addressed

| GDD System | Requirement | How This ADR Addresses It |
|------------|-------------|--------------------------|
| `design/gdd/save-local.md` (#28), regras 1 a 4 | Um save por aparelho; o que entra e o que nunca entra; fatias e envelope; campos desconhecidos passam intactos | Seções 1 e 2: envelope TLV com fatias opacas, nunca valores de balanceamento |
| `save-local.md`, regra 5 e F3 | Pontos seguros, nunca durante a fase, a gravação não trava o frame | Seções 5 e 6: gravador único, retrato na thread principal, pausa só fora de fase |
| `save-local.md`, regra 6 | Marca "fase em andamento", `attemptId`, consumo com efeito do #3 no mesmo commit | `BeginStage`, `CancelStage`, `ConsumeMark`; a marca rotaciona o backup como qualquer commit |
| `save-local.md`, regras 7 e 8 e F4 | Commit único, principal nunca ausente, backup só de principal reverificado, segunda rotação do selo | Seção 3 e a tabela de pontos de queda (Seção 4) |
| `save-local.md`, regra 9 | Versão do formato, cabeçalho verificado antes do corpo, só leitura para formato mais novo | Seção 2: cabeçalho com checksum próprio; formato aditivo |
| `save-local.md`, regras 10 a 12 | ID desconhecido; relógio e F1; erro de gravação e resultado real (Confirmado, Falhou, Pendente) | Seção 8, `ISaveClock`, `CommitOutcome` sem "tempo esgotado" |
| `save-local.md`, regras 13 e 14 e F2 | Perda máxima tolerada; leitura incerta (3 leituras); `saveSequence` por tentativa | Seção 3 e `SaveState.StorageUnavailable`; a reserva do número no gravador |
| `save-local.md`, Edge Cases (Auto Backup, reinstalação) | O save entra no Auto Backup; o marcador detecta a restauração | Seção 7 |
| `save-local.md`, "Vira ADR" e OQ-1 | Formato, local, escrita atômica, checksum, pausa, Auto Backup, "sujo", pontos de queda, sem reflexão, armazenamento injetável, marcador | Seções 1 a 10 |
| `design/gdd/fluxo-de-fase.md` (#3) | `BeginStage` com resultado real, respostas na thread principal, commit de fim que limpa a marca | `ISaveService` (o chamador passa o `requestId`, o resultado leva `RequestId` e `AttemptId`, `CancelStage` limpa a marca no Voltar) e a fila lida entre frames |
| `design/gdd/dados-e-balanceamento.md` (#1) e ADR-0002 | O save grava só IDs, carimbo da versão e revisão da skill selada | `IDataVersion` (hash, rótulo, revisão) como entrada do envelope |
| #5 Log de eventos (GDD pendente) | Interface de eventos com sink nulo e buffer no boot | `ISaveService` emite os eventos do GDD; o sink é do #5 |
| #29 Serviços online (GDD pendente) | Exportar e importar o retrato; `saveSequence` e `maxSeenUtc` | Envelope com ambos desde o MVP; o retrato inteiro é a unidade de exportação |

## Performance Implications
- **CPU**: a montagem do retrato na thread principal tem o orçamento da F3 (`SAVE_MAIN_THREAD_BUDGET_MS`, a medir com o roster máximo no aparelho de referência, que não foi verificado); a serialização, o FNV-1a e o disco rodam na thread do gravador. O orçamento **não é reivindicado aqui**.
- **Memory**: o retrato e os buffers do gravador; o ADR pede a medição de bytes alocados na montagem e na serialização; o save do MVP é pequeno (a estimar na primeira story).
- **Load Time**: leitura do cabeçalho e do corpo no boot, com no máximo 3 leituras em caso de erro (regra 14).
- **Network**: não se aplica.

## Migration Plan
Não se aplica: o projeto não tem código de jogo (`Assets/` só contém o modelo inicial do Unity). Os asmdefs `Forja.Save` (sem engine) e o de testes nascem com a primeira story do #28; o `AndroidStorage` mora em `Forja.Gameplay`, sem asmdef próprio. Uma migração de formato futura é só estrutural e roda sobre uma cópia em memória (GDD #28, regra 9).

## Validation Criteria
- Teste de injeção de falha para **cada linha da tabela de pontos de queda**: o estado seguinte é o esperado e o principal nunca fica ausente quando a troca é atômica.
- Dois pedidos quase juntos: o pedido novo substitui o pendente, cada pedido coberto recebe o seu `CommitResult`, o pedido substituto leva a marca do último pedido e a rotação do mais forte (um `Seal` coberto por um `Normal` ou por um `CancelStage` mantém a segunda rotação).
- `CancelStage` substitui um `BeginStage` pendente: o commit grava 0 marcas e a abertura seguinte não encontra marca (espelho do I3a do #3); `CancelStage` que cobre um `Seal` pendente limpa a marca e mantém a segunda rotação.
- `requestId` único entre #3 e #17 (fonte compartilhada) e `attemptId` de 128 bits idêntico em `CommitResult`, `StageMark`, `MarkAnswer` e no TLV da marca, comparado só por igualdade.
- Um TLV, uma fatia e um campo desconhecidos sobrevivem a dois commits seguidos.
- Cabeçalho adulterado dá corrupção e vai ao backup; um byte do corpo adulterado dá corrupção; um formato mais novo com cabeçalho válido abre em só leitura e nunca é sobrescrito.
- Um commit sem fatia nem campo do envelope alterado não é feito, o avanço do `maxSeenUtc` sozinho não o provoca, e um `BeginStage` sem fatia alterada grava.
- O marcador é criado antes do primeiro commit com o estado `Absent`; save sem marcador avisa "restaurado" uma vez.
- Um `TryReadAll` devolve `NotFound` para arquivo ausente e `IoError` para erro, e só o `IoError` consome as 3 leituras.
- **Gate de aceitação, no aparelho:** G1 a G4 (raiz resolvida, troca atômica por algum caminho, `fsync` de diretório viável, `File.Replace` com destino ausente).
- **Validation das primeiras stories, no aparelho (não bloqueiam a aceitação):** flush da pausa antes do congelamento (item 5), Auto Backup só do `save.dat` e o marcador depois de uma restauração por `bmgr` (itens 6 e 7), p95 da escrita, os bytes alocados e o tempo até Confirmado do `BeginStage` (item 9).
- O serviço não tem `static` mutável (revisão de código).

## Reavaliação prevista
O usuário confirmou as premissas deste ADR por recomendação sem dominar todos os conceitos, e pediu para reavaliá-las com o jogo avançado. **Todas as decisões deste ADR (seções 1 a 10) são provisórias**, mesmo onde o texto não traz a marca. Momento natural: depois do spike no aparelho (troca atômica, `fsync`, pausa, Auto Backup e marcador) e do spike de performance. Até lá o ADR segue `Proposed`.

## Related
- `design/gdd/save-local.md` (#28, OQ-1 e OQ-7), `design/gdd/fluxo-de-fase.md` (#3), `design/gdd/dados-e-balanceamento.md` (#1).
- ADR-0001 (`Proposed`: serialização sem reflexão, sem `static` mutável, thread principal) e ADR-0002 (`Proposed`: IDs estáveis, `IDataVersion`, função FNV-1a 64 pública). Este ADR **não emenda** nenhum dos dois (o nome `Fnv1a64` não consta no ADR-0002 e se fixa aqui; o registro cita este ADR em `data_content_hash` e `data_version`).
- Candidatos futuros: o ADR do #29 (transporte do pacote remoto e nuvem; persistência do histórico de revisão do aparelho, que o ADR-0002 delegou a ele ou a este) e os ADRs de #6 e #7.
- **Knob novo a declarar no GDD #28 e no #1:** `SAVE_PAUSE_FLUSH_CEILING_MS` (a medir). **Ajustes de redação pedidos ao GDD #28:** o "CRC do cabeçalho" passa a ser um FNV-1a de 64 bits independente; "Vira ADR" e a OQ-1 apontam para este ADR; a marca de fase rotaciona o backup como qualquer commit. **Feitos no GDD #28 em 2026-11-05** (conferidos em `/propagate-design-change design/gdd/save-local.md`, `docs/architecture/change-impact-2026-11-05-save-local.md`).
- **Revisão de 2026-11-05 (`/propagate-design-change`, TD-CHANGE-IMPACT: CONCERNS aceitos):** (a) a substituição de pedidos separa a rotação do backup (o mais forte) do estado da marca (o último pedido), para o Voltar do #3 nunca gravar a marca; (b) o `requestId` vem de uma fonte única compartilhada entre #3 e #17; (c) o `attemptId` passa a 128 bits em toda a cadeia. Itens pendentes fora deste ADR: ressincronizar `docs/registry/architecture.yaml` (`signal_signature` do `ISaveService`) e alinhar o `attemptId` do `PhaseResult` do ADR-0001 (linha 258).
- Registro de arquitetura (na gravação, com aprovação): novas posições `save_files` (state_ownership, escrita só pelo gravador por `ISaveStorage`), `effective_utc` (state_ownership, dono #28, lida por #26 e #17, só cresce), `save_events` (interface #28 → #5, sink nulo), `save_service`, `save_storage`, `save_envelope_format`, `save_atomic_replace`, `playerprefs_for_progress`, `save_during_phase` e `save_main_thread_io` (escopo: "arquivos do save", para não conflitar com `data_embedded_load`); ADR-0003 acrescentado ao `referenced_by` de `data_content_hash` e `data_version`; revisada `mutable_static_in_simulation` para incluir `Forja.Save` e o adaptador Android (quem guarda a thread).
