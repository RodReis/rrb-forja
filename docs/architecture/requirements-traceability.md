# Architecture Traceability Index
Last Updated: 2026-11-06
Engine: Unity 6.3 LTS (6000.3.27f1)

## Coverage Summary
- Total requirements: 125 ativos (mais 1 superseded: TR-combate-016)
- Covered by an Accepted ADR: 0 (0%) — os 6 ADRs estão `Proposed`
- Covered by a Proposed ADR (🟡): 79 (63%)
- Partial: 40 (32%)
- Gaps: 6 (5%)

| GDD | Ativos | 🟡 | ⚠️ | ❌ |
|---|---|---|---|---|
| #2 Simulação | 22 | 14 | 7 | 1 |
| #3 Fluxo de fase | 20 | 14 | 6 | 0 |
| #1 Dados | 20 | 12 | 7 | 1 |
| #28 Save | 19 | 14 | 4 | 1 |
| #6 Combate | 22 | 10 | 10 | 2 |
| #7 Horda | 22 | 15 | 6 | 1 |

**4ª passada (2026-11-06, `docs/architecture/architecture-review-2026-11-06-2.md`).** Entraram os ADR-0007, 0008 e 0009 (todos `Proposed`). Mudaram 8 linhas: simulacao-015, fluxo-016 e horda-014 de ❌ para 🟡; combate-018 e horda-015 de ❌ para ⚠️; simulacao-016, fluxo-010 e fluxo-014 de ⚠️ para 🟡. Total anterior: 73 / 41 / 11. A regradação das 8 linhas é de quem rodou a passada; as outras 117 não foram reconferidas. Os IDs seguem os de `tr-registry.yaml`, que não mudou.

Origem da 3ª passada: `docs/architecture/architecture-review-2026-11-06.md` (3ª passada; a anterior, de 2026-11-05, tinha 64 🟡, 44 ⚠️ e 17 ❌ e vê só os ADR-0001 a 0003). Mudaram 14 linhas, todas ligadas às Emendas 17 e 18 do ADR-0001 e aos ADR-0004, 0005 e 0006: 10 subiram de status, 3 de ❌ para ⚠️ e 1 (TR-simulacao-008) caiu. As linhas de #3, #1 e #28 não foram tocadas (GDDs e ADR-0002/0003 sem mudança). Os IDs são os de `docs/architecture/tr-registry.yaml`, que não mudou. As colunas "Fonte no GDD" são as da passada anterior.

## Full Matrix

#### #2 Simulação determinística (`design/gdd/simulacao-deterministica.md`)

| TR-ID | Requisito | Domínio | Fonte no GDD | ADR | Status | Nota |
|---|---|---|---|---|---|---|
| TR-simulacao-001 | Simulação e compositor em C# puro, asmdef sem engine, sem static mutável; uma instância por fase, sem serializar nem retomar | Core | R16 L114; C12 L542; A1 L588 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-simulacao-002 | Só float32; operações via SimMath, sem transcendentais, double nem Mathf; RoundToInt e FloorToInt com checagem de faixa; empate por id | Core | R9 L94-96; D9a-c L521-523 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-simulacao-003 | Ticks inteiros a 30 Hz; simulação sem relógio; ponte acumula dt, MaxTicksPerFrame descarta excedente, interpolação lê prev/atual | Core | R11 L101-102; FS1/FS2; T1, T2, T5 | ADR-0001, ADR-0002 | 🟡 Covered (Proposed) |  |
| TR-simulacao-004 | PCG32 com 3 streams via SplitMix64; RngWave(w) puro, sem estado, fora do hash, disponível no Preparar e no Tick; ids de stream registrados; política de IA não consome streams | Core | R1.3 L59; FS3-FS6 L198-276 | ADR-0001 (Emendas 11 e 16) | 🟡 Covered (Proposed) |  |
| TR-simulacao-005 | Simulation.Create(snapshot, hashLog, seed, sistemas, estrito) confere o hash; estados Created/Running/Ended/Broken/Destroyed; erros do host sempre lançam | Core | R1.3 L59; R14 L110; Estados L118-137 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-simulacao-006 | Tick em 7 passos com foto de CombatActive; compacta os vivos no fim; sem hash, relógio nem alocação; não reentrante, só na thread principal | Core | R2 L62-71; R7 L90; C2 L532 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-simulacao-007 | Command (ActorId, Kind, X, Y, ArgA, ArgB), validação e ordem por ator/tipo; vale só no tick; serial do PickOffer validado pelo #16 | Core | R3-R4 L73-80; C3, C4, C10 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-simulacao-008 | Compositor único fixa a ordem dos sistemas para jogo e teste sem tela; dentro do tick, comunicação só pelo SimWorld | Core | R5 L82-86; C5 L535 | ADR-0001 (Emenda 18) | ⚠️ Partial | Emenda 18a (ADR-0001 L84, L111) abre três canais diretos (fila do consumidor, acumulador hasheado do dono, vista só de leitura); o GDD #2 L86 ainda diz 'só pelo SimWorld' (sync pendente, ADR-0005 L305) |
| TR-simulacao-009 | SimWorld SoA pré-alocado, id = índice sem reuso, capacidade = total de spawns, Spawn devolve -1, Kill único caminho; FS9 em long no compositor | Core | R7-R8 L90-92; FS9 L314-334; C13 | ADR-0001, ADR-0002 | ⚠️ Partial | O compositor lê `SpawnsDeDados` e `CapacityMarginPct` do `PhaseSnapshot` concreto (ADR-0002 L113-115); o `IPhaseSnapshot` (ADR-0001 L231) não os tem e o ADR-0001 não diz que o compositor usa o tipo concreto (conflito 🟠) |
| TR-simulacao-010 | EventBuffer só de saída, drenado após cada tick; descarta os novos, com EventosReservados e DroppedEvents; não muda o hash | Core | R6 L88; C6 L536; I5 L568 | ADR-0001 | 🟡 Covered (Proposed) | Reserva para o `Rugido` não prevista (ADR-0001 L407; GDD L88) |
| TR-simulacao-011 | CombatHold escrito só pelo #16 e hasheado; CombatTick só avança com o combate ativo | Core | R15 L112; C11 L541 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-simulacao-012 | Checagem de finitude no passo 6, marca Essencial, FalhaInterna > vitória > derrota; NaN regrava posição anterior e HP 0 | Core | R9 L97; R13 L108; Edge L374; D9a/b | ADR-0001 | ⚠️ Partial | Emenda 8 regrava só a posição; o GDD também grava HP = 0 |
| TR-simulacao-013 | Modo estrito por instância; contadores de diagnóstico, inclusive GolpesDescartados, ModForaDeFaixa e CurasDescartadas do #6, lançam no 1º caso em estrito; GolpesLimitados só conta | Core | R14 L110; R10 L99 | ADR-0001 | ⚠️ Partial | SimContext sem como um sistema contar ou lançar; a Emenda 9 lista 4 contadores |
| TR-simulacao-014 | Hash FNV-1a 64 por byte, fora do Tick; reprodutibilidade só no mesmo binário e ABI; goldens por runtime | Core | R10 L99; FS8 L295-312; R12 L106; D8 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-simulacao-015 | Ponte entrega Mover em todo tick do frame e ações discretas 1x; segura a ação em frame de 0 ticks; zera Mover até um toque novo | Entrada | R4 L80; R15 L112; T3a-T3f | ADR-0007 | 🟡 Covered (Proposed) | Novo nesta passada. Depende do contrato `InputSample`/`TouchGeneration` do GDD #4, que não existe; `PhaseHost` pode nunca rodar um tick se ninguém passar `Created` para `Running` (ADR-0007 L118 × ADR-0001 L95) |
| TR-simulacao-016 | Pausa, segundo plano e foco: zero Tick, acum zerado, 1º dt descartado, portão do joystick só com CombatHold = 0; callbacks na thread principal | Plataforma | R11 L103; Edge L359-361; T3e, T4, T6 | ADR-0001, ADR-0003, ADR-0007 | 🟡 Covered (Proposed) | Era ⚠️. ADR-0007 decide fonte do dt, motivos de pausa e portão; ADR-0003 L186 ("nunca `Focus`") contradiz o texto até a Emenda ao ADR-0003. Callbacks na thread principal: NOT SOURCEABLE |
| TR-simulacao-017 | Cabeçalho do log: seed antes do tick 0, hash dos dados, tag do build (IL2CPP), ABI e ordem dos sistemas; comparador 'não comparável' | Log | R1.2 L58; R12 L106; Edge L405-406 | ADR-0001 | ⚠️ Partial | Campos da tag e da ABI NOT SOURCEABLE; formato do log (#5) sem ADR |
| TR-simulacao-018 | Orçamentos no aparelho: p95 do Tick (X1), memória (X3), N vivos sem tick descartado, custo do hash (X6), zero alocação, buffer de eventos cobre o pior tick sem DroppedEvents (P6) | Performance | P1-P6 L590-598; OQ-14 | ADR-0001 | ⚠️ Partial | Só o zero alocação está decidido; X1, X3, X6 e N não reivindicados |
| TR-simulacao-019 | Analisador estático bane double, Mathf e System.Random; CI exige testcasecount > 0 | Ferramentas | D9d L524; A2 L589 | ADR-0001 | ⚠️ Partial | Proibições decididas; analisador e passo de CI sem decisão |
| TR-simulacao-020 | Validação entre aparelhos (replay por servidor #22, online #29, coop #35) exige simulação em ponto fixo | Core/Rede | Dependencies L437-439 | ADR-0001 (Negative) | ❌ GAP | Declarado não atendido; ADR futuro de ponto fixo (Alpha) |
| TR-simulacao-021 | Fora do Tick só no Preparar: Spawn do herói sem evento e RngWave do #7; o compositor chama IPreparaFase e IConcluiFase | Core | R1.4 L60; R5 L86; FS6 L275 | ADR-0001 (Emendas 14 e 16) | 🟡 Covered (Proposed) | Novo nesta passada |
| TR-simulacao-022 | Fim com motivo e detalhe (MissingBoss pelo #3, EssentialSpawnRejected pelo #2 no tick); dado inválido não é pedido de fim | Core | R13 L108; Estados L130 | ADR-0001 (Emendas 6 e 7) | 🟡 Covered (Proposed) | Novo nesta passada |

#### #3 Fluxo de fase (`design/gdd/fluxo-de-fase.md`)

| TR-ID | Requisito | Domínio | Fonte no GDD | ADR | Status | Nota |
|---|---|---|---|---|---|---|
| TR-fluxo-001 | Duas metades: SistemaFluxoDeFase (ISimSystem, entre #6 e #16) e TentativaDeFase fora do tick e do hash, uma por tentativa | Core | R2 L53-55; R17 L153; AC-R2 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-fluxo-002 | Ficha de fase no SimWorld, escrita só pelo #3, hasheada pelo Hash do #3, gravada inteira no Preparar, com MotivoFim | Core | R4 L65-82; R3.4 L62; R16 L151 | ADR-0001 | ⚠️ Partial | Emenda 14 libera só IdDoHeroi fora do tick; PhaseSheet não tem MotivoFim |
| TR-fluxo-003 | IPreparaFase e IConcluiFase chamadas pelo compositor, Concluir em toda causa; eventos nunca são canal; #3 não conhece o #16 | Core | R15 L141-149; R9.2 L126; AC-R15 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-fluxo-004 | Herói criado no Preparar por Spawn essencial sem evento, IdDoHeroi = 0, ids_de_preparacao = 1 conferido antes do Create | Core | R3.4 L62; L332-334; Edge L386 | ADR-0001, ADR-0002 | 🟡 Covered (Proposed) |  |
| TR-fluxo-005 | Varredura incremental dos ids novos e lista de mortos do tick com id, facção, causa e xpDaMorte, limpa em todo tick | Core | R5.2 L86; R6 L94; F2 L242-256 | ADR-0001 | ⚠️ Partial | DeathRecord só tem Id e Cause; leitura de facção e xpValue por id fora do contrato |
| TR-fluxo-006 | Fim avaliado num só ponto via RequestEnd com prioridade; PendingEnd faz pular XP e oferta; End/EndDetail traduzidos em causa | Core | R5.3-5.4 L87-88; R8 L103 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-fluxo-007 | Relógio da fase é o CombatTick; #3 inerte com CombatActive falso; somas da F4 em long | Core | R5.1 L85; R7 L101; F4 L281-300 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-fluxo-008 | XP e nível em int com intermediários em long, sem divisão; passo O(1) + O(mortes), sem alocação | Performance | R17 L153; F1-F3; P1, P2 | ADR-0001 | ⚠️ Partial | Orçamento do passo do #3 depende do X1 do #2, não reivindicado |
| TR-fluxo-009 | PhaseResult readonly struct (causa, nível, ChefeVisto, MorteSimultanea, hash, attemptId de 128 bits); ContaComoMorteDeFase função pura | Core | R8 L103-122; AC-X L551-565 | ADR-0001, ADR-0003 | 🟡 Covered (Proposed) |  |
| TR-fluxo-010 | Encerramento: drenar, StateHash (indisponível em Broken), Concluir, Discard, commit de fim, evento ao #5 após a resposta | Core/Persistência | R9 L124-128; Edge L342; E8 | ADR-0001, ADR-0003, ADR-0008 | 🟡 Covered (Proposed) | Era ⚠️. ADR-0008 Decisão 5 fixa a ordem de fim e o rodapé só depois da resposta do commit. Lacunas: `FinalHashAvailable` no abandono (ADR-0008 L101 × L122), lote final possivelmente gravado duas vezes (ADR-0007 L124-125 × ADR-0008 L100), `CommitStatus` × `CommitOutcome` |
| TR-fluxo-011 | BeginStage assíncrono com resultado real, attemptId e requestId de fonte única; resposta filtrada por requestId; CancelStage não grava | Persistência | R3.2 L60; R10 L131; S3, S10a | ADR-0003, ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-fluxo-012 | Thread única: respostas do #28 numa fila esvaziada entre frames, nunca dentro do Tick, sem continuação em outra thread | Plataforma | R2 L56; L203; S10b L589 | ADR-0003, ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-fluxo-013 | Marca encontrada no boot: o #3 devolve o efeito, gravado no mesmo commit do consumo; Entrar bloqueado até o callback | Persistência | R13 L137; Edge L373 | ADR-0003 | ⚠️ Partial | Notificação não está no ISaveService; ADR-0003 L108 manda deduplicar, o GDD diz que não precisa |
| TR-fluxo-014 | Conjunto de motivos de pausa (foco, segundo plano, ligação, diálogo); 1º dt descartado também após a carga; nasce Pausada; pausa não grava | Plataforma | R11 L133; Edge L343, L346 | ADR-0003, ADR-0001, ADR-0007 | 🟡 Covered (Proposed) | Era ⚠️. ADR-0007 decide o conjunto de motivos (`AppPaused`, `FocusLost`, `PauseMenu`, `Dialog`) e o foco; ADR-0003 L186 proíbe `Focus` ao pé da letra e pede a Emenda |
| TR-fluxo-015 | Fontes injetadas: ISeedSource (seed nova por tentativa, override em teste) e fonte de ids; nenhuma leitura de relógio nem System.Random | Core | R3.2-3.3 L60-61; R10 L131; H3, H4 | ADR-0001, ADR-0003 | ⚠️ Partial | ISeedSource e a origem da entropia da seed sem decisão |
| TR-fluxo-016 | Log do #3: seed antes do tick 0, hash final, causa, MorteSimultanea, abandonada, exceção, commit falhou, ordem dos Preparar | Log | R3.3 L61; R9.4 L128; I6; X11 | ADR-0008 | 🟡 Covered (Proposed) | Era ❌. Contrato técnico sem o GDD #5; `HostNote` e `External` genéricos até o GDD #5 existir |
| TR-fluxo-017 | Abandono confirmado entre ticks, sem Tick: hash marcado abandonada, depois Concluir, depois Discard | Core | R12 L135 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-fluxo-018 | Knobs validados no Preparar por exceção (DadosInvalidos); Create ou Preparar que lança leva a FalhaInterna com hash indisponível | Core | R14 L139; S8; Edge L365, L372 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-fluxo-019 | Checagens de setup no build: limiar <= 2^31-1, F5 nas duas pontas de XP, exatamente 1 Essencial, cronograma com chefe | Dados | F1 L232; F5 L304-326; Edge L353 | ADR-0002 | 🟡 Covered (Proposed) |  |
| TR-fluxo-020 | Registro no Grimório depois do fim, como 2º commit fora da simulação | Persistência | R9.5 L129; OQ-6 L660 | ADR-0003 | ⚠️ Partial | Perda do registro se o app morrer entre os dois commits em aberto (OQ-6) |

#### #1 Dados e balanceamento (`design/gdd/dados-e-balanceamento.md`)

| TR-ID | Requisito | Domínio | Fonte no GDD | ADR | Status | Nota |
|---|---|---|---|---|---|---|
| TR-dados-001 | Valores de gameplay só como dado externo, números escritos como texto e lidos em decimal com cultura invariante; nenhum literal no código | Dados | R1 L38; AC-05/06 | ADR-0002 §1 | 🟡 Covered (Proposed) |  |
| TR-dados-002 | Declaração de knob com dono, tipo, unidade, faixa, padrão, aceite, pior, sentido, remoto, validada por coerência (F6) | Dados | R2 L39; F6 L194; AC-02 | ADR-0002 §2 | 🟡 Covered (Proposed) |  |
| TR-dados-003 | IDs estáveis em snake_case, nunca reutilizados nem removidos, deprecated resolve; índice inteiro pela ordem ordinal | Dados | R3 L40; AC-03 | ADR-0002 §5 | 🟡 Covered (Proposed) |  |
| TR-dados-004 | Resolução de ID para definição fora do tick, com a resposta ID desconhecido para o save e o log | Interface | Edge L238-240; AC-I5 L379 | ADR-0002 §5 | ⚠️ Partial | Tabela de IDs existe, mas nenhuma ADR define a interface de resolução (IDataResolver do #28) |
| TR-dados-005 | Conversão única no build: floor(s*30+0,5) com recusa abaixo de 1 tick; taxa /30 em decimal para float, bits idênticos em todas as plataformas | Determinismo | R4 L41; F1 L108; F2 L124; AC-F1/F2 | ADR-0002 §3; ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-dados-006 | Um único DataValidator, tudo ou nada, sem clamp, seis checagens, relatório com todos os erros | Dados | R5 L42-49; AC-05; AC-16/17 | ADR-0002 §2 | 🟡 Covered (Proposed) |  |
| TR-dados-007 | A carga verifica estrutura e hash; uma falha bloqueia a fase (o catálogo bloqueia todas) e nunca usa valor padrão | Dados | R7 L51; Edge L244; AC-10 | ADR-0002 §2, §8 | 🟡 Covered (Proposed) |  |
| TR-dados-008 | Capacidades por fase (vivos, ids, eventos, pools) contra a demanda com margem e teto por tipo, em int64; compositor soma ids_de_preparacao | Memória | F3 L140-152; AC-F3; AC-I1 | ADR-0002 §4; ADR-0001 | ⚠️ Partial | GDD admite override de margem por capacidade; ADR tem CapacityMarginPct global única |
| TR-dados-009 | Snapshot binário imutável, canônico e little-endian, lido sem reflexão; o jogo e o headless leem o mesmo | Dados | R7 L51; AC-09; AC-I3 | ADR-0002 §4 | 🟡 Covered (Proposed) | AC-09 do GDD exige nenhum tipo T[], o ADR usa arrays privados |
| TR-dados-010 | Carga síncrona (catálogo no boot, fase antes do tick 0), zero I/O e conversão durante a fase, sem Addressables nem Resources | Engine | R7 L51; AC-11 | ADR-0002 §8 | 🟡 Covered (Proposed) |  |
| TR-dados-011 | Orçamento de carga fria e quente e memória do snapshot no aparelho de referência | Performance | Knobs L284-286; AC-P1; OQ-4 | ADR-0002 (Verification Required 3, 8) | ⚠️ Partial | ADR não reivindica orçamento; depende do spike e do aparelho |
| TR-dados-012 | Hash FNV-1a 64 de conteúdo, rótulo e versão efetiva (embarcado + pacote) para o log #5 e Simulation.Create | Interface | R6 L50; AC-07; AC-I2 | ADR-0002 §6 | 🟡 Covered (Proposed) |  |
| TR-dados-013 | Revisão por skill (fecho mais contador), classificação autoral obrigatória, histórico datado, só fatos expostos | Dados | R6 L50; Edge L233-237; AC-07/08 | ADR-0002 §7 | ⚠️ Partial | ADR não define a marcação gameplay/cosmético e não expõe o hash da revisão |
| TR-dados-014 | O pré-build revalida, refaz o bake e falha o build com dado inválido ou knob de aceite remoto; o snapshot fica versionado | Build | Edge L243, L246; AC-12 | ADR-0002 §9 | 🟡 Covered (Proposed) |  |
| TR-dados-015 | Assembly Forja.Data sem engine, sem rede, sem static mutável e sem API de escrita em runtime | Código | R10 L61; AC-15; AC-18 | ADR-0002 §9 | 🟡 Covered (Proposed) |  |
| TR-dados-016 | Análise estática no CI: literais numéricos de gameplay e lista de exceções | Ferramentas | AC-01; OQ-7 L403 | — | ❌ GAP | Nenhuma ADR decide ferramenta nem lista de exceções |
| TR-dados-017 | Contrato do pacote remoto: lista branca, atômico, mesma validação, sem segmentação, base = hash, maior sequência, só entre partidas | Live ops | R9-10 L53-61; AC-13; AC-19 | ADR-0002 §10 | 🟡 Covered (Proposed) |  |
| TR-dados-018 | Persistência atômica da última sobrescrita válida, assinatura, expiração, revalidação no boot, decimal idêntico no aparelho | Persistência/Rede | R9 L59; Edge L223, L226; AC-14 | ADR-0002 §10 (delega ao #29) | ⚠️ Partial | Delegado ao ADR futuro do #29 |
| TR-dados-019 | Histórico de revisão do aparelho (pacote aplicado, trocado, removido, expirado, descartado) persistido e somado ao History | Persistência | R6 L50; Edge L226, L229 | ADR-0002 §10; ADR-0003 | ⚠️ Partial | Delegado ao #29 ou ao save |
| TR-dados-020 | Aplicar o pacote só no hub, sem ritual de selo ou registro aberto (sinal do #17); tela das cartas lê a versão da próxima partida | Interface | R9 L58; AC-14b | ADR-0002 §10 | ⚠️ Partial | Falta a interface do #17 para o #1 |

#### #28 Save local (`design/gdd/save-local.md`)

| TR-ID | Requisito | Domínio | Fonte no GDD | ADR | Status | Nota |
|---|---|---|---|---|---|---|
| TR-save-001 | Um save por aparelho; envelope com fatias opacas versionadas pelo dono; tag e campo desconhecidos passam intactos | Persistência | R1, R4 L37-40; AC-01; AC-28 | ADR-0003 §2 | 🟡 Covered (Proposed) |  |
| TR-save-002 | O save guarda só IDs, carimbo da versão dos dados, revisão e data do selo, saveSequence e maxSeenUtc; nunca valores nem posses | Estado | R2-3 L38-39 | ADR-0003 §2 | 🟡 Covered (Proposed) |  |
| TR-save-003 | Cabeçalho fixo com checksum próprio, lido antes do corpo; cabeçalho inválido é corrupção; FNV-1a 64 no corpo | Persistência | R9 L45; AC-06 | ADR-0003 §2 | 🟡 Covered (Proposed) | ADR ainda cita CRC do cabeçalho em L80 |
| TR-save-004 | Commit atômico: temporário, releitura, rotação verificada do backup, troca do principal, fsync do diretório antes de Confirmado | Persistência | R7-8 L43-44; F4; AC-05, AC-10, AC-14, AC-26/27 | ADR-0003 §3, §4 | 🟡 Covered (Proposed) | Troca atômica no Android é gate G2 de aceitação (spike) |
| TR-save-005 | Estados de abertura (8), precedência por saveSequence, quarentena e pendente de decisão, leitura incerta com até 3 tentativas | Persistência | Estados L54-67; R14 L50; AC-15, AC-20, AC-29 | ADR-0003 §1 | 🟡 Covered (Proposed) |  |
| TR-save-006 | Versão do formato inteira; migração só estrutural, numa cópia em memória; formato mais novo e migração falhou abrem só leitura | Persistência | R9 L45; AC-06; AC-15c/f/g | ADR-0003 §2 | 🟡 Covered (Proposed) |  |
| TR-save-007 | Retrato montado na thread principal no orçamento F3; gravador único em thread própria; fila de capacidade 1 com substituição | Threading | R5 L41; F2, F3; AC-12, AC-13, AC-16 | ADR-0003 §5 | 🟡 Covered (Proposed) |  |
| TR-save-008 | Pontos seguros, flag de sujo, nunca grava na fase nem no tick; pausa por OnApplicationPause com flush e teto | Ciclo de vida | R5 L41; AC-02, AC-03 | ADR-0003 §6, §8 | 🟡 Covered (Proposed) |  |
| TR-save-009 | Marca de fase em andamento: BeginStage só retorna com resultado real; attemptId de 128 bits de fonte injetada; payload opaco; CancelStage | Interface #3 | R6 L42; AC-04a-c | ADR-0003 §3, Key Interfaces | 🟡 Covered (Proposed) |  |
| TR-save-010 | Avisar o #3 de marca encontrada e gravar o efeito do #3 no commit de consumo; restaurada consumida na restauração | Interface #3 | R6 L42; AC-04a; AC-08; AC-22/23 | ADR-0003 (ConsumeMark) | ⚠️ Partial | OnMarkFound não está nas Key Interfaces; MarkAnswer indefinido |
| TR-save-011 | Resultado real Pendente, Confirmado ou Falhou com causa tipada, sem tempo esgotado; selo idempotente; recusa em só leitura | Interface #17 | R12 L48; AC-21; AC-06 | ADR-0003 (CommitOutcome) | ⚠️ Partial | FailureCause é int sem enum; ReadOnlyRejected e idempotência do selo ausentes |
| TR-save-012 | Relógio injetável; hora efetiva monotônica na faixa de sanidade sobre BUILD_UTC; o avanço viaja no próximo commit | Tempo | R11 L47; F1; AC-11, AC-24/25 | ADR-0003 §8 | 🟡 Covered (Proposed) |  |
| TR-save-013 | Android: raiz interna por JNI getFilesDir(); Auto Backup só do save.dat; marcador em noBackupFilesDir para detectar restauração | Plataforma | Vira ADR L82; Edge L162 | ADR-0003 §1, §7 | 🟡 Covered (Proposed) | Revisão de engine: XMLs de backup em Plugins/Android/res são recusados; GameActivity a conferir |
| TR-save-014 | Armazenamento injetável com injeção de falha; o mesmo teste roda contra o fake e contra o adaptador real | Testabilidade | AC preâmbulo L246; AC-31 | ADR-0003 §10 | 🟡 Covered (Proposed) |  |
| TR-save-015 | Serialização à mão, sem reflexão; serviço injetado sem static mutável; ciclo de vida da thread (quitting, Play Mode) | Engine | Vira ADR L82 | ADR-0003 §9, §5 | 🟡 Covered (Proposed) | Revisão de engine: falta IsBackground, join no reload e -= de eventos estáticos |
| TR-save-016 | Interface de eventos para o #5 com sink nulo e buffer no boot, com a lista de eventos fixada | Interface | Interações #5 L74; AC-30 | ADR-0003 (ISaveEventSink) | 🟡 Covered (Proposed) |  |
| TR-save-017 | Pedidos de mensagem ao jogador (7 tipos), uma por vez por gravidade, consumidos no commit; indicador persistente | UI | UI Requirements L217-227; AC-19a/b | — | ❌ GAP | Nenhuma ADR define o canal do #28 para a UI nem a fila de avisos |
| TR-save-018 | Tratar ID desconhecido do #1: preservar o registro, slot indisponível; revisão do selo comparável ao histórico | Interface #1 | R10 L46; AC-07; AC-32 | ADR-0003; ADR-0002 | ⚠️ Partial | Sem IDataResolver; IDataVersion indexada por índice e o save guarda ID |
| TR-save-019 | Exportar e importar o retrato inteiro; detectar regressão por saveSequence e hash de conteúdo; só o #29 reduz maxSeenUtc | Persistência/Nuvem | Interações #29 L80; R11 L47; AC-17/18 | ADR-0003 | ⚠️ Partial | Delegado ao #29; sem API de exportação nem hash de conteúdo do save |

#### #6 Combate e dano (`design/gdd/combate-e-dano.md`)

| TR-ID | Requisito | Domínio | Fonte no GDD | ADR | Status | Nota |
|---|---|---|---|---|---|---|
| TR-combate-001 | Colunas hasheadas do #6 no SimWorld: hpMax, estadoCombate, timerTicks, iframes, contactCd, kbVel, intentVel, classe, arquetipoId, tickNascimento, aberto, punidoPesado, esquivaBuf, curaPendente, ultimoContatoTick, área travada do telegraph, prontoDesde, índice do ciclo do chefe, proximoHitStopTick, ultimaDirecao, poise, kb_refrat; escalares modDano e modCadencia do #8 | Core/Estado | L103, L426; OQ-1 | ADR-0004, ADR-0005 | ⚠️ Partial | Catálogo em ADR-0004 L68-98; `ICombatModifiers` em ADR-0005 L99. O GDD #6 L103 tem `intentVel` como coluna hasheada e o ADR-0004 L98 a põe em scratch; semântica de `cicloIdx` a confirmar (ADR-0004 L91); sync de nomes pendente (ADR-0004 L267) |
| TR-combate-002 | O #6 é o único escritor de posição e HP; o #7 só faz Spawn, o #8 só enfileira; um espião por sistema verifica | Core/Estado | L46; AC-R1 | ADR-0004, ADR-0005 | 🟡 Covered (Proposed) | `HpAndPosForWrite` só pelo #6 (ADR-0004 L101-102, L211); o #7 só faz Spawn e o #8 só enfileira (ADR-0005 L60-64). A guarda por `BannedApiAnalyzers` é NOT SOURCEABLE (ADR-0004 L28, VR6); o especialista sugere um objeto de capacidade no lugar |
| TR-combate-003 | Ordem fixa no tick #7, #8, #6, #3; dentro do #6 os passos 1 a 8 têm ordem fixa | Core/Sim | L46-55; AC-I2 | ADR-0001; ADR-0004 e ADR-0005 (pressupõem) | ⚠️ Partial | ADR-0005 L128, L64, L89 e ADR-0004 L116 pressupõem #7→#8→#6→#3→#16, mas nenhum ADR a decide: a ordem só está no GDD #2 Regra 5 (provisória). ADR-0001 L107 manda o `Preparar` rodar com o #3 primeiro |
| TR-combate-004 | O #6 só age com CombatActive, conta todo tempo em CombatTick e as contagens regressivas congelam exatas; a oferta de carta abre na hora e o #16 é dono da contagem 3-2-1 sob CombatHold, sem predicado do #6 | Core/Tempo | L48, L70; AC-R16, E3 | ADR-0001 (Emenda 5) | 🟡 Covered (Proposed) |  |
| TR-combate-005 | Ponto único Combate.Aplicar/Curar com fila entre sistemas, pedido Rugido tipado na frente da fila e sem F1, cura do #3 via curaPendente (sobrevive ao CombatHold), resolução 7a/7b, scratch fora do hash, cap_fila com teto_vivos_horda + 1, estouro vira Quebrada | Core/Comunicação | L54-57, L69; F2, E1 | ADR-0005 | ⚠️ Partial | Decisões 1-5 cobrem fila, `Curar`, resolução 7a/7b, scratch e Broken. Diverge do GDD #6: o `Rugido` virou sinal único `PedirRugido` fora da fila, saíram o termo `teto_vivos_horda + 1` de `cap_fila` e o `curaAcc` (GDD #6 L56-57, L69, L353, L525; sync em ADR-0005 L303). `cap_fila` não existe no `PhaseSnapshot` do ADR-0002 |
| TR-combate-006 | Morte só por Kill(id, causa) em 7b; herói e chefe podem morrer no mesmo tick; a causa identifica o golpe ou a fonte | Core/Estado | L57, L65; F2 L147 | ADR-0001 (Emendas 6 e 15) | ⚠️ Partial | A causa por golpe (F2, entrada k) não chega ao `Kill`; `DeathRecord` só tem o enum |
| TR-combate-007 | Eventos individuais só para herói, elite e chefe; a horda sai agregada por tick {mortes, acertos, danoTotal}; mortes por Rugido somam em mortes, acertos e danoTotal contam só pedidos com valor | Eventos | L68, L419; AC-R14 | ADR-0001 (Emenda 18), ADR-0005 | 🟡 Covered (Proposed) | `HordeTick`, `Death`/`HeroDeath` e `ArgA`/`ArgB` (ADR-0005 L109-119) batem com o GDD L68; resta renomear 'Morte' no GDD (sync ADR-0005 L303) |
| TR-combate-008 | Contadores de diagnóstico fora do hash (GolpesDescartados, GolpesLimitados, ModForaDeFaixa, CurasDescartadas) que lançam no modo estrito | Diagnóstico | L351-362; E7 | ADR-0001 (Emenda 9) | ⚠️ Partial | Contadores do #6 fora da Emenda 9; `SimContext` sem modo estrito nem contador |
| TR-combate-009 | float32 na ordem escrita, sem FMA, SimMath, HP_RESIDUO contra resíduo de float, conversão float para int controlada | Numérico | L107; F2, F4 | ADR-0001 | 🟡 Covered (Proposed) | F4 ainda usa cast direto `(int)(x+0,5f)` (GDD L107, L195) contra ADR-0001 L287 |
| TR-combate-010 | Tipo vetorial próprio e geometria determinística: círculo, cone, segmento da linha (P0→P1 limitado na trava), clampArena AABB por eixo, EIXOS8[id mod 8] para vetor nulo do knockback, dir (1,0) se d² < 1e-6, sem trigonometria | Numérico | L60, L63; F3 | ADR-0006 | ⚠️ Partial | Parcial no próprio ADR (L259): `SimVec2`, `SimGeometry`, `Arena` e `Axis8` cobertos; a abertura do cone é NOT ASSESSED (ADR-0006 L28 VR6, L116) |
| TR-combate-011 | Consulta espacial por tick com 300+ vivos: alvo mais próximo, contato, acerto do telegraph e áreas do #8; sem bloqueio de corpo | Desempenho | R4-R5; OQ-7 | ADR-0006 | 🟡 Covered (Proposed) | `SimQuery` por varredura linear em ordem de id, sem grade (ADR-0006 L84-90); o custo com 300 vivos no aparelho fica na VR3 |
| TR-combate-012 | Orçamento do Tick do #6: p95 ≤ 2,0 ms e p99 ≤ 4,0 ms com 300+ vivos e 3 avisos, no aparelho de referência; pior tick (300 mortes + 3 avisos) com máximo ≤ orcamento_combate_pior_tick_ms (valor ainda não definido) | Desempenho | L527; AC-P1 | — | ❌ GAP | ADR-0001 L433 não fixa orçamento por sistema |
| TR-combate-013 | Zero alocação gerenciada por tick, arrays pré-alocados, 300 mortes num tick | Memória | AC-P2 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-combate-014 | Laços por id crescente, empate pelo menor id, sem RNG, Hash do #6 com escopo definido; proibições verificadas por BannedApiAnalyzers | Determinismo | L424-426; AC-D3, AC-D4 | ADR-0001 | 🟡 Covered (Proposed) | Analisador estático não está no ADR |
| TR-combate-015 | Durações em ticks inteiros; segundos e taxas convertidos uma vez no build; validações F5-F10 em decimal pelo #1 | Dados | L483; F5 | ADR-0002 §3 | 🟡 Covered (Proposed) |  |
| TR-combate-016 | AvisoPerto como sinal somente leitura do #6 para o #16, que segura a oferta | Core/Comunicação | removido do GDD | — | ⛔ Superseded | `AvisoPerto` e F11 removidos; Regra 16 reescrita (oferta na hora, contagem 3-2-1 do #16); ver TR-combate-004 |
| TR-combate-017 | Hit-stop, flash, dissolve e cauda são só apresentação; a simulação nunca congela e a apresentação lê colunas e eventos | Presentation | L64; F8 | ADR-0001 (Tempo) | 🟡 Covered (Proposed) |  |
| TR-combate-018 | Efeitos por shader com propriedade por instância, pools de cartões e fantasmas, overdraw <= 2,5x, decal de telegraph, cortes por prioridade | Render | L565, L575, L585 | ADR-0009 | ⚠️ Partial | Era ❌. O flash por corpo da horda fica desligado sem a emenda `UltimoDanoTick` no ADR-0004 (muda o golden hash do #6); caminho primário de dados por instância com HIGH de engine (`SV_InstanceID` por lote); overdraw e draws só com spike |
| TR-combate-019 | Háptico no Android e tremor de câmera como knobs de acessibilidade | Plataforma | L606, L609; OQ-6 | — | ❌ GAP | API de vibração do Android NOT SOURCEABLE; sem ADR |
| TR-combate-020 | StateHash do tick 900 igual entre o Editor e o aparelho IL2CPP ARM64 | Determinismo | AC-D5 L723 | ADR-0001 | ⚠️ Partial | Conflito: ADR-0001 L391 e L450 só prometem o mesmo build e o mesmo runtime; reescrever o AC-D5 ou emendar o ADR |
| TR-combate-021 | Capacidade de eventos ≥ Reservados + 5 + 3×individuais + 4; DeathsThisTick com a capacidade de entidades, sem descarte | Capacidade | L419-421, L526 | ADR-0001 (Emenda 10), ADR-0002 | ⚠️ Partial | Capacidade de `DeathsThisTick` não fixada; risco de ADR-0001 L407 pendente. Novo nesta passada |
| TR-combate-022 | O #6 expõe visões somente leitura: área travada do telegraph (fase, ticks_ate_dano, forma, raio, origem e destino), ultimoDanoTick, pesado, iframes, dash, cadência, HP e hpMax; posição, arquétipo e tick da horda morta legíveis 1 tick após a morte | Presentation | L68, L587; AC-I12 | ADR-0001 | ⚠️ Partial | Nomes e tipos das visões somente leitura não definidos. Novo nesta passada |
| TR-combate-023 | Spawn grava classe, arquetipoId e tickNascimento; a entidade nascida no CombatTick corrente não age no #6 | Core/Estado | L61, L367; AC-R7 | ADR-0001 (Emenda 17), ADR-0004 | 🟡 Covered (Proposed) | `Spawn` com classe e arquétipo; `tickNascimento` e `hpMax` carimbados pelo SimWorld (ADR-0001 L200, L110; ADR-0004 L74-77) |

#### #7 Horda, waves e inimigos (`design/gdd/horda-waves-e-inimigos.md`)

| TR-ID | Requisito | Domínio | Fonte no GDD | ADR | Status | Nota |
|---|---|---|---|---|---|---|
| TR-horda-001 | O #7 é o 1º ISimSystem (#7, #8, #6, #3, #16), só faz Spawn e declara dados; depois do nascimento não escreve posição nem HP | Core/Sim | R1 L52; AC-R1, I2 | ADR-0001, ADR-0004 | ⚠️ Partial | Escritor único de posição e HP decidido (ADR-0004 L101-102); a ordem concreta do compositor continua sem ADR (ver TR-combate-003) |
| TR-horda-002 | Composição inteira no Preparar via world.RngWave(w), sorteio sem viés; 0 sorteios por tick | Determinismo | R6 L92; F3 L233-246; D1, D7 | ADR-0001 (Emendas 11, 14 e 16) | 🟡 Covered (Proposed) | Era ⚠️: a Emenda 16 fechou o RNG no `Preparar` |
| TR-horda-003 | Tabela (chave long, sem comparador genérico sobre struct), janelas por elite e scratch da F4 pré-alocados; fora do hash; só cursores hasheados; zero alocação por tick | Memória | R6, R8 L104, R9, R13; P2, P3 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-horda-004 | Posição de nascimento como função pura: direções SimVec2 literais, espelho por eixo, dist², sem sin/cos nem raiz | Numérico | R7 L94-99; F4 L253-271 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-horda-005 | Geometria da arena AABB [0,L]x[0,A] e tipo vetorial compartilhados com o clampArena do #6 | Numérico | R2 L54; F4, F5 | ADR-0006 | 🟡 Covered (Proposed) | Uma só `Arena`, construída pelo compositor (ADR-0006 L62, L196). Pendente entre GDDs: a F4 do #7 usa [0,L] com raio 0 e o clamp do #6 usa [r, L−r] (ADR-0006 L292) |
| TR-horda-006 | vivos_horda e 'há elite vivo' por uma passada local O(n≤303) sobre Alive; nenhum contador no SimWorld | Estado | R8 L104; P3 L796 | ADR-0001 (`Alive`), ADR-0004 | 🟡 Covered (Proposed) | Coluna `classe` e vista `Classes` (ADR-0004 L74) |
| TR-horda-007 | Colunas classe, arquetipoId e tickNascimento escritas no Spawn; a escolta lê o estado de ataque do #6 do tick anterior | Estado | L169-172, L186; R11; I12 | ADR-0001 (Emenda 17), ADR-0004 | 🟡 Covered (Proposed) | Decisões 2 e 5 do ADR-0004; a escolta lê o estado do tick anterior (L116) |
| TR-horda-008 | Capacidades vêm dos dados: total_spawns_7 (FS9) e pico_vivos_7 (F3); Spawn -1 faz o cursor avançar, ou lança no modo estrito | Dados | R14; F7, F8; L501 | ADR-0001 (Emenda 6), ADR-0002 | 🟡 Covered (Proposed) |  |
| TR-horda-009 | Chefe Essencial: único, nunca espera; Spawn rejeitado encerra com EssentialSpawnRejected; reservar um id para o essencial? | Estado | R10.1 L110; OQ-3 | ADR-0001 (Emendas 6 e 7), ADR-0004 | 🟡 Covered (Proposed) | Sem id reservado para o chefe (ADR-0004 L124, provisória) |
| TR-horda-010 | Rugido: pedido tipado, sem dano, na frente da fila Combate.Aplicar; Kill com causa Rugido, a primeira causa vence; cap_fila ≥ teto_vivos_horda + 1 | Comunicação | R10.2 L111; L471; R10, I6 | ADR-0001 (Emenda 15) | ⚠️ Partial | Era ❌: a Emenda 15 trouxe `DeathCause.Rugido`. Falta o contrato da fila `Combate.Aplicar` (ADR-0001 L84, L267) |
| TR-horda-011 | Movimento cinemático em C# puro: linha reta, sem NavMesh nem física, mira por id mod 32, encaixe no alvo sem normalizar | IA | L133; RB, RB2 | ADR-0001 | 🟡 Covered (Proposed) |  |
| TR-horda-012 | Separação entre inimigos e bloqueio de corpo (grade uniforme O(n)) adiados ao spike de performance | Desempenho | L133; OQ-9, OQ-16 | ADR-0006 | 🟡 Covered (Proposed) | Grade uniforme adiada: decidido (ADR-0006 L90, Alternativa 1 L204-208) |
| TR-horda-013 | Orçamento do passo do #7: p95 0,3 ms e p99 0,5 ms com 300 vivos e 200 pendentes, no tick do rugido, na escolta e com 20 nascimentos/tick sustentados; marker Horda.Tick | Desempenho | L579; P1 L794 | — | ❌ GAP | ADR-0001 L433 não fixa orçamento por sistema |
| TR-horda-014 | Render de multidão: <= 400 triângulos, 1 LOD, 1 draw por tipo, dados por instância, zero efeito ou som por corpo, pool de ~300 fantasmas | Render | L640-658 | ADR-0009 | 🟡 Covered (Proposed) | Era ❌. Mesmo HIGH de engine do combate-018 sobre o índice por lote; depende do spike (itens 1, 2 e 11) |
| TR-horda-015 | Pré-aquecer no Preparar os assets do chefe (modelo, shader, LUT por Volume, disco) para o tick do rugido caber no frame | Render/Carga | L182, L530; P4 L797 | ADR-0009 | ⚠️ Partial | Era ❌. O ADR-0009 pré-aquece antes do `Create`, em paralelo com o `BeginStage`; o GDD #7 L182, L530 e L796 diz "no `Preparar`" (sync pendente). Lista de assets "vem do snapshot" sem campo no ADR-0002; desenho "fora da tela" é descartado pelo culling |
| TR-horda-016 | Evento Rugido (mesmo com 0 corpos); nenhum evento por corpo nascido | Eventos | L111, L469, L634 | ADR-0001 (Emenda 18), ADR-0005 | 🟡 Covered (Proposed) | `SimEventKind.Rugido` (ADR-0001 L155), `Spawn` sem evento (L200), `Rugido` sempre emitido (ADR-0005 L116) |
| TR-horda-017 | Diagnósticos do #7 (HordaEsperouTicks, EliteEsperouTicks, HordaCancelada, ElitesCancelados, TicksNoTeto, VivosHordaNoElite, TicksNoCanto) fora do hash, enviados ao log do #5 | Diagnóstico | R13 L119-126 | ADR-0001 | ⚠️ Partial | Sem canal de diagnóstico do sistema até o log |
| TR-horda-018 | Cronograma e arquétipos na seção de fase do snapshot: w explícito, ordem (inicio, w), instante 0 válido, checagens F2/F5/F10 em decimal | Dados | R4 L76-88; F1; F10 | ADR-0002 §4 | ⚠️ Partial | ADR-0002 L86 diz "por índice de wave"; o GDD ordena por (`inicio`, `w`); falta regra de instante |
| TR-horda-019 | Congela sem CombatActive; corpos vencem no mesmo CombatTick depois da oferta, sem lote na retomada | Tempo | R1; L436-441; E1, E2 | ADR-0001 (Emenda 5) | 🟡 Covered (Proposed) |  |
| TR-horda-020 | Mesmo build IL2CPP ARM64: tabela e hash iguais; golden por plataforma | Determinismo | D6 L789 | ADR-0001 L64, L450 | 🟡 Covered (Proposed) | Era ⚠️: o GDD deixou de exigir Editor × aparelho |
| TR-horda-021 | Id de classe de vetor pré-calculado em decimal no build; frentes comparadas por inteiro, nunca por float | Dados | R7.4 L98; F4 L254, L266 | ADR-0002 | 🟡 Covered (Proposed) | Novo nesta passada |
| TR-horda-022 | Tick do rugido: até teto_vivos_horda + 1 mortes mais o evento Rugido sem DroppedEvents | Eventos | L657, L686; P1(b) | ADR-0001 L407 | ⚠️ Partial | `EventCapacity` ou reserva para o `Rugido` não declaradas. Novo nesta passada |

## Known Gaps
Requisitos sem nenhuma ADR (6): TR-simulacao-020, TR-dados-016, TR-save-017, TR-combate-012, TR-combate-019, TR-horda-013.

| ADR sugerida | Cobre |
|---|---|
| ADR de orçamento de frame por sistema e de entrada na fase (após o spike) | combate-012, horda-013, simulacao-018, fluxo-008 |
| ADR de análise estática e CI | dados-016, simulacao-019, combate-014 |
| ADR de avisos do save para a UI | save-017 |
| ADR de feedback de plataforma (háptico, tremor) | combate-019 |
| ADR do #29 (pacote remoto, exportação do save) | dados-018/019, save-019 |
| ADR futuro de simulação em ponto fixo (Alpha) | simulacao-020 |
| Emenda ao ADR-0003 (marca encontrada, enum de causas, `ReadOnlyRejected`, `IDataResolver`, `AttemptId`, FNV-1a 64; mais, pedidos pelos ADR-0007 e 0008: `Focus` só como gatilho de gravação, `ISaveStorage` seguro para dois chamadores, `Emit` na thread principal, fila do #28 esvaziada pelo `AppLifecycle`) | save-010/011/018, fluxo-013, simulacao-016, fluxo-014 |

Escritos em 2026-11-06, ainda `Proposed` (aguardam aceite): ADR-0007 (simulacao-015/016, fluxo-014), ADR-0008 (simulacao-017 parcial, fluxo-010/016, horda-017 parcial) e ADR-0009 (combate-018, horda-014/015); pendências deles (ciclos nas emendas ao ADR-0007, `CommitStatus` × `CommitOutcome`, lote final duplicado, `IsAlive` como span, dependência 0009 → 0002, `SV_InstanceID` por lote) estão no relatório da 4ª passada. ADR-0004 (combate-001/002/021/023, horda-006/007/009), ADR-0005 (combate-005/007/008, horda-010/016/017) e ADR-0006 (combate-010/011, horda-005/012). Pendências deles (ordem do compositor, dono de `cap_fila`, `XpValues`, abertura do cone, GDD Sync) estão no relatório de 2026-11-06.

## Superseded Requirements
- TR-combate-016 (`AvisoPerto` como sinal do #6 para o #16): superseded-by TR-combate-004. O GDD #6 removeu o `AvisoPerto` e a F11; a oferta abre na hora e o #16 é dono da contagem 3-2-1.

Requisitos cujo GDD mudou depois da ADR e que pedem revisão estão em "Divergências GDD × ADR" no relatório.
