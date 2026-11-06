# Review Log: Fluxo de fase (#3)

## Review — 2026-11-04 — Verdict: NEEDS REVISION
Review mode: full · Workflow: full
Scope signal: XL
Specialists: game-designer, systems-designer, economy-designer, qa-lead, unity-specialist, ux-designer; senior reviewer: creative-director
Blocking items: 5 | Recommended: 11
Summary: O desenho está sólido (retry limpo e idempotente, fim da fase avaliado num ponto só, prioridade entre fins clara, F1 a F3 passam em todas as fronteiras; o diretor leu as F1 a F3, que o CD-GDD-ALIGN anterior não tinha lido). Os defeitos são contradições locais no passo do tick, a definição de "morte de fase" divergindo do conceito L405, a máquina de estados com o #28 e o Gate de aceite. Nada pede redesenho. Registro (entities.yaml) sem conflito de valores; K_min = 7 e `duracao_ticks` conferem.
Prior verdict resolved: First review
Findings:
- [BLOCKING] Regras 5.5, 14, F2, E7, R14: `xpDaMorte` negativo checado dentro do tick (vira Quebrada pela Regra 14 do #2) contra "recusado no setup, sem clamp" na F2; o XP roda depois de `AvaliarFim`, então um dado inválido no tick da vitória passa por cima de `FalhaInterna > Vitoria`. Corrigir: validar só no `Preparar` e no #1. [systems-designer, qa-lead, creative-director]
- [BLOCKING] Regra 5 e 17, Regra 7, F4, X6: passo 5.3 "o resto não roda" impede o 5.6 de gravar a ficha hasheada no tick do fim; `ChefeVisto` varre a tabela inteira (O(capacidade), contra o O(1)+O(mortes) da Regra 17); `Spawn` do chefe = −1 não é detectável pelo #3 no mesmo tick. [systems-designer, creative-director]
- [BLOCKING] Regras 3 e 10, tabela de estados: duas respostas de commit com o mesmo `attemptId` em *Entrando* (BeginStage e limpeza do Voltar); *Cancelando* sem saída para `Falhou` ou timeout; falta *Entrando* → *Pausada*; falta uma regra de thread. [unity-specialist, ux-designer, systems-designer]
- [BLOCKING] Regra 8, X11, OQ-18: "morte de fase" exclui abandono pré-chefe, `AppFechado`, falhas e vitória simultânea, contra o conceito L405 ("tentativa que termina sem vencer o chefe"); falta a emenda do L405 e um pior valor por sinal à parte no aceite (L402 do conceito). [creative-director, game-designer, economy-designer]
- [BLOCKING] Gate e Acceptance Criteria: R4 e R7 fora das listas, R2 só advisory; Gate do MVP em deadlock (exige #5, #6, #7, #16, #20 e o #16 depende do #3); I2 e I3 "com falsos" mas BLOQ; R17 impossível (mesmo assembly pelo ADR); R4, R7, R11, R15, S9 e H1 não verificáveis como escritos. [qa-lead, unity-specialist, creative-director]
- [RECOMMENDED] F4: `tick_entrada_chefe_agendado + ticks_max` em `long`; teto de `nivel_max` e da duração no #1 antes do laço da F5. [systems-designer]
- [RECOMMENDED] Ficha: domínio de `Estado`, valor inicial canônico de `TickDeEntradaDoChefe`, `IdDoHeroi` fora do R16. [systems-designer]
- [RECOMMENDED] Transições faltantes: cancelar abandono → *Pausada*, saída de *Cancelada*, evento ao #5 quando o commit de fim falha. [systems-designer]
- [RECOMMENDED] Retry: tela de resultado já em *Concluindo* com Retry "preparando"; PT1 mede do toque ao tick 0. [ux-designer, game-designer]
- [RECOMMENDED] Dizer que a seed não alimenta o roteiro do chefe (é do #7). [game-designer]
- [RECOMMENDED] F5: P avaliado por função jogável; tirar o "até cerca de 99" da F1. [creative-director, economy-designer]
- [RECOMMENDED] Tabela da Regra 8: colunas K_min, Grimório e campanha não são decisão do #3. [qa-lead, economy-designer]
- [RECOMMENDED] OQ-16 e L98: tirar a frase normativa "AppFechado nunca rende menos que DerrotaHeroi" e reescrever como exigência à economia. [creative-director, economy-designer]
- [RECOMMENDED] AC-UI1 expõe `ChefeVisto`, `CombatTick` final, motivo do bloqueio e commit pendente; taxonomia de 3 famílias de resultado vai ao #12. [ux-designer]
- [RECOMMENDED] Critérios: E1 testa o fake, F6 não é critério, P1 sem limiar, `testcasecount > 0` é checagem de CI. [qa-lead]
- [RECOMMENDED] Órfãos de cobertura: `ChefeVencido` na vitória, lista de mortos velha somada duas vezes, abandono no tick em que o chefe nasce, diálogo de abandono ao voltar o foco, cópia da visão em *Quebrada*, armazém nulo, exigência ao #16 de não abrir oferta com pedido de fim. [qa-lead]
- [RECOMMENDED, outro documento] ADR-0001 (OQ-2): `Simulation.Create`, `IPreparaFase`/`IConcluiFase`, ficha escalar, `ctx.CombatActive`, pedido de fim com motivo; os especialistas apontaram, mas o diretor manteve como pendência registrada com dono. [unity-specialist]
Divergências arbitradas pelo creative-director:
- F5 e `folga_pool`: economy-designer (bloqueante) × diretor. Rebaixado: é knob a calibrar; a guarda contra o "quase tudo" é a capacidade C do Grimório (#16).
- Vitória com `MorteSimultanea` "sem morte": game-designer (bloqueante) × decisão do autor. A regra de jogo fica; a correção vai para o aceite (bloqueante 4).
- Reroll por abandono pré-chefe: game-designer e economy-designer × decisão do autor. Aceito como jogo; contar a partir do 1º level-up rejeitado por reabrir decisão do autor; entra no aceite como sinal com pior valor.
- "`AppFechado` nunca rende menos que `DerrotaHeroi`": economy-designer (bloqueante, inexecutável) × diretor. Rebaixado: reescrever na OQ-16, não bloqueia.
- Itens do ux-designer (taxonomia, toque vazado) e do unity-specialist (B3, ADR): ficam com o #12, o #4 e a OQ-2.
Reviewed-Content-Hash: design/gdd/fluxo-de-fase.md 5bb714fa7880a729e550ba1d069350eff2ee0999
Reviewed-Content-Hash: design/registry/entities.yaml 65eba26bd57655d264d9d95296c6ebe8e6e18315
Reviewed-Content-Hash: .claude/skills/design-review/SKILL.md a63d8fba9b7142eeb43791f061e2e1533c429b43
Reviewed-Content-Hash: design/gdd/simulacao-deterministica.md 6cdb627dd360bd9961c41a09f66fd4443a52b76e
Reviewed-Content-Hash: design/gdd/save-local.md 71e8fc1a4fee065db4920785ffd9cc35a4a34bbf
Reviewed-Content-Hash: design/gdd/dados-e-balanceamento.md 871745d1c91e60ec7bcc77bb55726282b6a65397
Reviewed-Content-Hash: design/gdd/game-concept.md 3a61558d87c0374c253396d6a268ac932ac062f3

## Review — 2026-11-05 — Verdict: NEEDS REVISION
Review mode: full · Workflow: full
Scope signal: XL
Specialists: game-designer, systems-designer, qa-lead, unity-specialist, economy-designer; senior reviewer: creative-director (ux-designer não chamado: os itens de UI da 1ª passada ficaram com o #12)
Blocking items: 7 | Recommended: 14
Summary: 2ª e última passada (limite do projeto). Dos 5 bloqueantes da 1ª, o passo do tick, a máquina de estados com o #28 e a divisão do Gate estão resolvidos; o aceite (X11) e o Gate (X6b, SEMTELA1) tinham pontas soltas. A cura no level-up, nova desde a 1ª passada, atravessava o tick fora do hash. Nada pede redesenho: 7 correções de texto, todas APLICADAS na mesma sessão. CICLO ENCERRADO sem 3ª passada, como no #1, #2 e #28. Registro sem conflito de valor.
Prior verdict resolved: Parcial (bloqueantes 2, 3 e 5 da 1ª passada resolvidos; 1 e 4 resolvidos aqui com os itens 2 e 5)
Decisão do autor (2026-11-05): OQ-19, a definição estreita de "morte de fase" fica; a emenda ao L405 do conceito fica anotada.
Findings:
- [BLOCKING, aplicado] Regra 6: cura do level-up pedida pelo #3 ao #6 atravessava o tick fora do hash e contradizia a Regra 15; agora o #6 lê `NiveisGanhos` por um cursor `NiveisCurados` no Hash dele; AC R6b novo. [systems, game, qa, economy, CD]
- [BLOCKING, aplicado] Regra 4: ficha sem `MorteSimultanea`, sem `MotivoFim` (o `EndKind` junta as duas derrotas) e sem valores iniciais; ficha inteira gravada no `Preparar`; causa sai primeiro de `End`/`EndDetail`; R4 com colunas novas. [systems, qa, CD]
- [BLOCKING, aplicado] Regras 12 e 14: descartavam antes do 9.1 (o `StateHash` lança depois do `Discard`). [unity, CD]
- [BLOCKING, aplicado] Gate: X6b com BLOQ velho (OQ-2) e nos dois Gates; SEMTELA1 dependia do `mvp.md`. [qa, CD]
- [BLOCKING, aplicado] X11: sinal "AppFechado com o chefe" não observável; faltavam `FalhaInterna` e `Quebrada`; `cura_levelup_pct` congelado antes do D0. [game, qa, CD]
- [BLOCKING, aplicado] OQ-11: "FIFO" desatualizado; exigências novas (CancelStage nunca grava marca, requestId único entre chamadores, AttemptId 128 bits). [unity, CD]
- [BLOCKING, aplicado] L102: regra normativa à economia virou exigência na OQ-16 (moeda de jogo, vídeo que dobra, guarda contra farm). [economy, CD]
- [RECOMMENDED, aplicado] Textos velhos: L15 (#6 tem GDD), seção da FS9, 5.3 "pula o 5.5", caso inalcançável no S3 e na L351.
- [RECOMMENDED] 5.3: usar `ctx.PendingEnd` para fins pedidos por outro sistema (o efeito é só o nível de uma `FalhaInterna`). [systems]
- [RECOMMENDED] F5: tirar a cláusula redundante `sem_teto = nivel_max`; corrigir a razão do exemplo `nivel_max` 12; declarar 100 % de abates; alinhar 60-90 % com 60-85 %; o #1 recusar `folga_pool ≥ P`. [systems, economy, qa]
- [RECOMMENDED] AC: lista de comandos no S9; lista branca de literais no R17; `testcasecount` como checagem de CI; P1 em alocação e tempo; E1 em falso e real; órfãos (evento "commit falhou", seed nova no R1, custo da Regra 17, cópia da visão em Quebrada, foco e diálogo, armazém nulo, menor P com duas funções). [qa]
- [RECOMMENDED] Tuning Knobs: `cura_levelup_pct` nas interações (a cura acaba no teto; o Tank ganha menos). [economy]
- [RECOMMENDED] HP% no resultado do abandono, como sinal; seed fixa por fase em build de dev para o Tank × DPS manual; roteiro do chefe fora do stream da seed (#7). [game]
- [RECOMMENDED] `Estado` da ficha duplica o pedido de fim; `xpValue` validado no `Spawn`. [systems]
- [RECOMMENDED, outro documento] ADR-0001 emenda 14 (ficha inteira no Preparar, `MotivoFim`); ADR-0003 e #28 (CancelStage substituto herda StageMark e grava a marca: bug de marca fantasma; requestId; AttemptId int); #6 Regra 15 com o cursor e edge case da oferta adiada (Regra 16); #26 contra farm; #1 `folga_pool ≥ P`; #7 `xpValue` e roteiro do chefe; `mvp.md` piores valores; conceito OQ-1 e OQ-19.
Divergências arbitradas pelo creative-director:
- AppFechado com o chefe: qa (contar o total) × game (#5 grava `ChefeEntrou` em disco). Ficou o qa; a ideia do game foi para a OQ-18 (vertical slice).
- OQ-19: game (decidir já) × texto (antes do `mvp.md`). Não bloqueia; perguntada ao autor e decidida.
- Abandono pré-chefe (farm, HP baixo): game e economy × decisão do autor. A decisão fica; a guarda vai ao #26 e o HP% vira sinal.
- Achado do #28/ADR-0003: o conserto é desses documentos; no #3 só a OQ-11 bloqueia.
- 5.3 e `PendingEnd`: rebaixado a recomendado pelo systems; o diretor concorda.
Carimbo: o GDD #3 NÃO é carimbado (foi revisado depois desta passada); os demais arquivos lidos:
Reviewed-Content-Hash: design/registry/entities.yaml df812874b67f3b1dfc1c98b9a526577f5ddab7ae
Reviewed-Content-Hash: .claude/skills/design-review/SKILL.md a63d8fba9b7142eeb43791f061e2e1533c429b43
Reviewed-Content-Hash: design/gdd/simulacao-deterministica.md da65d8de634c778730f3674a915380f61ed69db1
Reviewed-Content-Hash: design/gdd/save-local.md 23831ed39d616b6718e41774b81b14c1cb64f63f
Reviewed-Content-Hash: design/gdd/combate-e-dano.md bba3220f063460f41c4d4f35c3c8cf7c706679ad
Reviewed-Content-Hash: design/gdd/dados-e-balanceamento.md 97ba0623083570cfcb91bd8214350dcf96b3a1ea
Reviewed-Content-Hash: design/gdd/game-concept.md 3a61558d87c0374c253396d6a268ac932ac062f3
Reviewed-Content-Hash: docs/architecture/adr-0001-simulacao-deterministica-float32-tick-30hz.md 0c470fb5926c207b998a4ca9c22899c7cb5e2767
Reviewed-Content-Hash: docs/architecture/adr-0003-save-local-envelope-tlv-commit-atomico-gravador-unico.md b1b06e1826a3f78fdd5afa0a26c7e406a55b5316
Reviewed-Content-Hash: design/business-model.md fef23ee16b19a6cc595afb7dda25d87d0c132c61
