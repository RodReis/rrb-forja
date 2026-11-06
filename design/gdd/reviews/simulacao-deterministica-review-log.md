# Review Log: Simulação de combate determinística (#2)

## Review — 2026-11-04 — Verdict: NEEDS REVISION
Review mode: full · Workflow: full
Scope signal: XL (producer deve verificar antes do sprint planning)
Specialists: game-designer, systems-designer, qa-lead, unity-specialist, performance-analyst; senior reviewer: creative-director
Blocking items: 7 | Recommended: 12 (mais os itens que vão para o spike, o ADR-0001 e os GDDs #3, #4, #6, #7, #9 e #16)
Summary: A arquitetura está sólida (vetores numéricos, registro de entidades e decisões do autor conferem) e nenhum pilar exige redesenho. Os 7 bloqueantes eram correções pontuais de contrato e de critérios de aceite, não mudança de direção. Uma conferência curta desses pontos basta na próxima passada.
Prior verdict resolved: First review
Revision applied: o GDD e o registro `design/registry/entities.yaml` foram revisados no mesmo dia (2026-11-04) e o índice marcou o #2 como In Review. **Não houve re-review.** O GDD foi alterado depois da revisão, então **não há carimbo de hash**: a próxima `/design-review` deve ser uma revisão completa e não pode usar o recibo desta. O ADR-0001 não foi tocado; as emendas dele estão na OQ-5 do GDD.
Decisão de jogo do autor nesta revisão: depois da escolha de carta (e da volta de uma pausa), o combate só retoma no primeiro toque no joystick; a invulnerabilidade curta foi recusada.
Findings:
- [BLOCKING] Acceptance Criteria T2: `acum_novo` = 0,026667 dá `alfa` 0,80001 e erro de 1,5e-6 contra a tolerância de 1e-6 (conferido por script). Corrigido: o teste calcula `0,8f × TickSeconds`. [revisão principal, qa-lead]
- [BLOCKING] Core Rule 11, FS1, Cross-References: `MaxTicksPerFrame` dizia ser knob do #1, mas o #1 não o tem e o registro aponta o #2. Corrigido: dono é o #2 (knob da ponte, não remoto). [revisão principal, qa-lead, systems-designer, game-designer]
- [BLOCKING] Core Rules 3, 4, 15 e Edge Cases: `PickOffer` sem identidade nem entrega única; um toque podia escolher duas cartas com a fila de ofertas. Corrigido: `(ActorId, serial, índice)` com `ArgA` e `ArgB`, entrega única pela ponte, T3 dividido em T3a-d. [game-designer, systems-designer, qa-lead, unity-specialist]
- [BLOCKING] Core Rules 2 e 15: `CombatFrozen` lida ao vivo pelos sistemas e `CombatTick` pelo início do tick; só coerentes pela ordem provisória. Corrigido: `CombatHold` escrito só pelo #16 e no hash, foto `ctx.CombatActive` no passo 2, retomada pelo toque. [systems-designer, qa-lead, game-designer]
- [BLOCKING] Core Rule 1.3 e ACs C1/I3: o construtor não recebia o snapshot, mas validava o hash dele. Corrigido: `Simulation.Create(snapshot, cabeçalhoDoLog, seedMestre, sistemas, estrito)`. [systems-designer, qa-lead, unity-specialist, game-designer]
- [BLOCKING] Core Rule 14: "dev falha, release descarta" sem mecanismo. Corrigido: opção `estrito` na instância, sem `#if`; erros do host sempre lançam (cortou `TicksAfterEnd` e `UndrainedEvents`, ficaram 5 contadores). [unity-specialist, performance-analyst]
- [BLOCKING] Acceptance Criteria P1-P6 e D9, Core Rule 9: P1-P6 nunca dariam PASS ("a medir"); D9 empacotava 8 coisas e não dizia como a simulação sabe quem é herói ou chefe. Corrigido: SPEC INCOMPLETO com formato "p95 ≤ X", D9a-d, marca `Essencial` e motivo `FalhaInterna`. [qa-lead, performance-analyst]
- [RECOMMENDED] Cortes de escopo aplicados: `EventosReservados` e cadência do hash viraram constantes, hash por byte, sem regra do limite do `int32`. [performance-analyst, unity-specialist, creative-director]
- [RECOMMENDED] FS9 em `long` e definição de spawn; FS5 com `unchecked`; faixa de `Max` (1 a 16); nota do FS3 sobre a seed; texto do knob (sem espiral infinita). [systems-designer, performance-analyst]
- [RECOMMENDED] Player Fantasy: "anunciados" sem dono (agora em "não promete") e Pilar 2 esticado (agora apoio indireto). [game-designer, creative-director]
- [RECOMMENDED] **Não aplicados**, ficam para a próxima passada ou para outros documentos: controles negativos (mutantes pareados) em D7, T4, T5, C5, C6, C12 e D1a; E7, C11 (feito), D6b e I4 rodam já com fixture; `RequestEnd` idempotente com prioridade vitória > falha > derrota e o #16 vendo `EndRequested`; lista de vivos compactada no fim do tick e contagem capturada no início do passe; NaN validado na escrita do `SimWorld`; registro de colunas hasheadas com teste; regras sem AC (R2 passos 3 e 4, R3 fora de ordem, R5, R6, R8, R9 divisor, R11 foco sem pausa, R12). [qa-lead, systems-designer, performance-analyst]
- [RECOMMENDED] Para o spike e o ADR-0001: pressupostos NOT SOURCEABLE (a)-(g), plano B `FieldOffset` desde o início, ARM64 fixo em ProjectSettings, chave do golden com configuração, versão do editor e tag do build, `Math.Round` meio-para-par (o #1 deve usar o mesmo `SimMath.RoundToInt`), `IRelogio` na ponte, `RngWave(w)`, `Rng` por stream e `StateHasher` sempre por `ref`. [unity-specialist]
- [RECOMMENDED] Para os GDDs #4, #6, #7: horário do toque e janela de esquiva de no mínimo 3 ticks; grade espacial com desempate por id; `total_spawns` com teto estático; `EntityId` opaco; `Death` do herói com quem matou. [game-designer, performance-analyst]

Disagreements arbitrated:
- Seed (`Mix(seedMestre XOR id_s)`): o systems-designer marcou como bloqueante; a revisão principal e o creative-director discordaram (o par `seed_s`, `inc` é único por mestre e stream). Não mudou a fórmula; entrou uma frase no FS3.
- `CombatFrozen`: game-designer (derivar de "oferta pendente") e systems-designer (foto no passo 2) foram unidos pelo creative-director.
- Release: unity-specialist (`estrito` testado nos dois caminhos) e performance-analyst (tudo vira exceção) foram unidos: `estrito` só para erro de comando, exceção sempre para erro do host.

Carimbo de hash: nenhum (o GDD mudou depois da revisão, de propósito).

## Review — 2026-11-04 (2ª passada) — Verdict: NEEDS REVISION
Review mode: full · Workflow: full
Scope signal: XL (estimativa do creative-director; producer deve verificar antes do sprint planning)
Specialists: game-designer, systems-designer, qa-lead, unity-specialist, performance-analyst; senior reviewer: creative-director
Blocking items: 4 | Recommended: lista abaixo (os especialistas levantaram 7 a 17 itens cada; o creative-director rebaixou H, I, J e K e empurrou o resto para o spike, o ADR-0001 e os GDDs donos)
Summary: Os 7 bloqueantes da 1ª passada não foram reabertos por nenhum especialista; os 4 novos nasceram das próprias correções (pausa × oferta, modo `estrito`, checagem de NaN) e de um recomendado antigo promovido (laço da R7). Todos tinham correção de poucas frases, sem mexer em pilar nem na fantasia "A horda não trapaceia". Os 4 foram aplicados no mesmo dia; **o ciclo do #2 está encerrado após 2 passadas** (limite do projeto), como no #1 e no #28, sem 3ª conferência.
Prior verdict resolved: Yes (7 de 7 aplicados; nenhum reaberto)
Decisões do autor nesta passada: (1) depois de escolher a carta o combate só volta com **toque novo** no joystick (dedo já apoiado não conta; regra na ponte); (2) com o portão da pausa fechado, `Esquivar`, `Suprema` e `PickOffer` tocados são **descartados**; (3) `SpawnsRejected` em release **só registra no log** (bug de dado do #7, sem punir o jogador). Decisão técnica por recomendação *(provisória, a reavaliar)*: `FalhaInterna` > vitória > derrota.
Findings:
- [BLOCKING] Regras 11 e 15: pausa com oferta pendente travava (`PickOffer` só age num `Tick`, e o portão do joystick não olhava o `CombatHold`). Corrigido: portão só com `CombatHold` = 0; toque novo pela ponte; ACs T3e e T3f. [game-designer, qa-lead, revisão principal, creative-director]
- [BLOCKING] Regra 14, 6, 8, 9 e ACs C3, C6, C8, C10, E5: `estrito` só governava erro de comando; C10 se contradizia; faltava dono do serial. Corrigido: regra única de modo, `PickOffer` nunca lança, #16 valida e conta. [qa-lead, unity-specialist]
- [BLOCKING] Regras 2, 9, 13 e D9b: checagem de NaN fora da lista de passos e sem precedência contra o pedido de fim. Corrigido: passo 6 novo, `FalhaInterna` > vitória > derrota. [systems-designer, qa-lead, revisão principal]
- [BLOCKING] Regra 7: laço durante spawns e mortes indefinido. Corrigido: contagem capturada, morte só marca a flag, compactação no fim do tick. [systems-designer]
- [RECOMMENDED, aplicado] Cortes de escopo: `CommandsOutOfOrder` (restam 4 contadores, registro atualizado) e P7 em 2 runtimes. Telegraph de elite e chefe na reserva de eventos (R6). C1 com golden e tipo de exceção. OQ-14 com p99, pior frame, tempo real descartado e soak. OQ-5 com `Create` sem `static` mutável e configuração do IL2CPP na tag. [creative-director, performance-analyst, unity-specialist]
- [RECOMMENDED, não aplicado] D7/FS8: tabela de larguras em bytes, teste da ordem de campos com sink de bytes injetado, normalizar −0 na escrita do `SimWorld`. [qa-lead, systems-designer]
- [RECOMMENDED, não aplicado] Controles negativos (mutantes pareados) extras em D7, T4, T5, C5, C6, C12; D9a dividido; C4 e E4 com efeito observável; C5 "só escreve no SimWorld" não é testável (vai para análise estática D9d); A1 sem "idealmente"; E2 e E6 reescritos; T1(d) como critério; PT1 e PT2 mensuráveis. [qa-lead]
- [RECOMMENDED, não aplicado] FS: `EixoMax` ≤ 1e6 e zona morta (#4); FS9 com `margem_pct` entre 0 e 100 e `total_spawns` em `long`; FS5 com pool vazio não é "bug interno" (#16 testa antes); `seq = w + 3` e `Mix(Mix(M) ^ id)` contra correlação entre seeds sequenciais; teste de `k × TickSeconds` para k = 1..18. [systems-designer]
- [RECOMMENDED, não aplicado] R3: dedupe por (ator, tipo) em modo não estrito; `Kind` fora do catálogo; `ActorId` negativo; compositor marca `RodaCongelado` por sistema. [systems-designer]
- [RECOMMENDED, não aplicado] `CombatTick` também para i-frame, telegraph, buff e DoT (#6, #8); janela de esquiva ≥ 5 ticks com jitter (#6, anotada no Game Feel); app fechado com pouca vida como fuga da derrota (#3, #28). [game-designer]
- [RECOMMENDED, não aplicado] Ponte: try/catch em volta do laço de ticks quando a simulação fica *Quebrada*; callbacks de pausa só levantam bandeira e o `Update` a consome; `dt` de relógio sem escala se a pausa usar `timeScale = 0`; `Max` inicial derivado do orçamento; dono da qualidade adaptativa. [unity-specialist, performance-analyst]
- [RECOMMENDED, não aplicado] Desempenho: zero coletas de GC por fase e `SimWorld` reaproveitável; mensagens de assert, strings e delegates no `Tick`; "projétil é entidade?" antes do ADR-0001 ser aceito; hash por byte é aceitável. [performance-analyst]
- [RECOMMENDED, outro documento] `dados-e-balanceamento.md` L337 (AC-I1) ainda diz "os GDDs #2 e #7 não existem"; atualizar na próxima edição do #1. [revisão principal]
Divergências arbitradas pelo creative-director:
- P1-P6: performance-analyst (bloqueante, medem a coisa errada) × qa-lead ("SPEC INCOMPLETO = BLOCKED" é honesto). Rebaixado: não há falso verde antes do spike; as métricas entraram na OQ-14.
- Contadores em release: unity e qa-lead (tabela de modos) × game-designer (`SpawnsRejected` invalidaria a run). Decidido pelo autor: só registrar.
- Negativos do D1a: qa-lead (bloqueante) × demais. Rebaixado: o D1a já exige ver o controle negativo falhar.
- 3ª passada: game-designer e systems-designer não pedem. Encerrado.

Carimbo de hash: nenhum (o GDD mudou depois da revisão, de propósito).
