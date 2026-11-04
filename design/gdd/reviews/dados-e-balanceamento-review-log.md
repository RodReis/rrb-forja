# Review Log: Dados e balanceamento (#1)

## Review — 2026-11-03 — Verdict: NEEDS REVISION
Review mode: full · Workflow: full
Scope signal: L
Specialists: game-designer, systems-designer, qa-lead, unity-specialist, performance-analyst; senior reviewer: creative-director
Blocking items: 6 | Recommended: 11 (mais itens menores e os que vão para o ADR)
Summary: A base do GDD é boa: posse dos dados, validação "tudo ou nada", "nunca usar valor padrão" e as fórmulas F2 a F6 foram refeitas à mão e conferem. Os problemas estavam em texto e em pontos localizados, não na estrutura. Três coisas não podiam chegar aos programadores como estavam: a revisão por skill contradizia o conceito (L191), a Regra 4 trazia afirmações numéricas falsas e alguns ACs passavam sem testar nada.
Prior verdict resolved: First review
Findings:
- [BLOCKING] Core Rule 6: a revisão da skill era o hash do bloco dela, e não cobria evoluções, passivas, modificadores, fórmulas e knobs globais (conceito L191). [game-designer, systems-designer]
- [BLOCKING] Core Rule 4 / F1 / F2: "um único arredondamento" e "matematicamente igual a × TickSeconds" eram falsos; o exemplo de 0,15 s estava justificado errado; a constante 1/60 não existe em decimal. [systems-designer, unity-specialist, qa-lead]
- [BLOCKING] Acceptance Criteria: faltava o estado BLOCKED para ACs que dependem de OQ-2, OQ-4, OQ-7, #2, #5, #7, #26 e do aparelho de referência. [qa-lead, performance-analyst]
- [BLOCKING] AC-P1 (p95 de 10 amostras e folga decidida depois) e AC-I3 [EM] (comparação circular) passavam por construção. [performance-analyst, qa-lead]
- [BLOCKING] Acceptance Criteria: Regras 5 (referências cruzadas, relatório com todos os erros) e 10 (proibições) sem AC. [qa-lead]
- [BLOCKING] Interactions / Dependencies / Tuning Knobs: texto "nenhum GDD dependente existe" desatualizado (o #28 existe), knob `K` períodos do #28 não declarado, status do cabeçalho. [revisão principal, game-designer]
- [RECOMMENDED] Core Rule 6: gravar valor antigo e novo de cada knob no histórico; direção da mudança calculada pelo `sentido`; `correcao` com nota publicada. [game-designer]
- [RECOMMENDED] Interações com o selo: o registro do selo guarda a revisão do conjunto Ativo da partida do selo; bloquear o selo com pacote pendente fica com o #17 e a elegibilidade com o #18. [game-designer, creative-director]
- [RECOMMENDED] Core Rule 10: "knob que conta para o ranking" indefinido, ranking sem versão, buff temporário que expira vira nerf. [game-designer]
- [RECOMMENDED] F3: pico declarado à mão pode estar subestimado; override de margem sem faixa; teto sem definição de desempenho; margem global para tipos de capacidade diferentes. [systems-designer, performance-analyst]
- [RECOMMENDED] F4 / F5: são só condições necessárias (alvo da reforja do slot de função, `R_max` finito, estouro com ∞). [systems-designer]
- [RECOMMENDED] Hash / ADR: dado autoral como texto, normalização (0,15 contra 0,150, −0), ordem e cultura, conversão no build, pacote como bytes sem Addressables. [systems-designer, unity-specialist]
- [RECOMMENDED] ACs menores: AC-F6 (`maior_melhor`), fronteiras de F3 a F5, AC-15 (System.Net), AC-09 (arrays mutáveis), um caso de teste por item, checklist dos itens [MAN]. [qa-lead, unity-specialist]
- [RECOMMENDED] Custos de GC e de boot, orçamento de validação do pacote remoto, fragmentação após várias partidas. [performance-analyst, unity-specialist]

Disagreements adjudicadas pelo creative-director: (a) revisão por skill = fecho de dependências define *quando* muda (GDD) e contador sequencial identifica *qual* é (ADR); (b) lacuna de AC bloqueia só quando uma regra central fica sem teste ou o AC passa por construção; (c) selo irreversível com pacote pendente fica com o #17 e o #18, não reabre o #1; (d) conversão no build com bits do float é decisão do ADR do #1 (OQ-2), com recomendação provisória.

Revisões aplicadas na mesma sessão (2026-11-03): os 6 bloqueantes foram resolvidos no GDD; as recomendações ficaram na OQ-11 e os itens de ADR na OQ-2. O GDD foi alterado depois da revisão, então **não há carimbo de hash**: a próxima `/design-review` deve ser uma revisão completa e não pode usar o recibo desta.

## Review — 2026-11-03 (2ª passada) — Verdict: NEEDS REVISION
Review mode: full · Workflow: full
Scope signal: L (no limite de XL)
Specialists: game-designer, systems-designer, qa-lead, unity-specialist, performance-analyst; senior reviewer: creative-director
Blocking items: 8 | Recommended: 18 (mais itens de ADR)
Summary: As fórmulas F1 e F3 a F6 estão corretas e a arquitetura se sustenta; os 6 bloqueantes da 1ª passada foram resolvidos no texto. Os defeitos novos eram pontuais e se resolviam com edição: um AC (F2) que já tomava a decisão do ADR e um registro que contradizia o GDD, uma regra de classificação de nerf que deixava passar um nerf escondido (fura o Pilar 2), o número da carta que podia mudar entre o selo e a partida (fura a Player Fantasy) e ACs que passavam por construção. O creative-director recomendou fechar com uma conferência curta só dos 8 pontos, sem 3ª revisão completa (limite de 2 passadas do projeto); a decisão final é do usuário.
Prior verdict resolved: Yes — os 6 bloqueantes da 1ª passada; 1 deles (tabela BLOCKED) estava incompleto e voltou como bloqueante 2.
Findings:
- [BLOCKING] Formulas F2 / AC-F2 / registro: o AC fixava 3.33333325f antes de o ADR decidir dividir ou multiplicar; `entities.yaml` fixava "(float)(r/30), one rounding", o que contradizia o GDD e era impreciso (são dois arredondamentos). [systems-designer, qa-lead, unity-specialist]
- [BLOCKING] Acceptance Criteria (tabela BLOCKED): faltavam AC-F2, AC-I3 [EM], hash do AC-07, AC-08, AC-09, AC-13/14 (escrita atômica), AC-15/18, AC-10/11/14 [PM]; AC-F1 estava bloqueado inteiro quando só a leitura de texto depende do formato. [qa-lead, game-designer, unity-specialist]
- [BLOCKING] Core Rule 6 / Edge Cases: a classificação comparava com o embarcado, não com a revisão efetiva anterior (troca P1→P2 e descarte por update escondiam nerfs); "impossível por construção" era falso. [systems-designer]
- [BLOCKING] Core Rule 6 / Edge Case de pacote: uma etiqueta por definição contra uma por skill afetada. [game-designer, systems-designer]
- [BLOCKING] Core Rule 9 / Player Fantasy: o pacote só valia na partida seguinte, mas o selo acontece entre partidas; o jogador podia ler X, selar e jogar com Y. [game-designer]
- [BLOCKING] Acceptance Criteria: AC-P1 (só pegava regressão; frio e quente num orçamento só), AC-19 (cláusula não verificável), AC-09 (passava com arrays mutáveis), AC-I3 (dourado regenerável pelo próprio código). [qa-lead, performance-analyst, game-designer, unity-specialist]
- [BLOCKING] Core Rule 8 / AC-P1: os orçamentos nascem no spike, depois do congelamento de D0. [performance-analyst]
- [BLOCKING] Core Rule 2 / F6 / Edge Cases: "knob de aceite" era deduzido da presença de `pior`, então um aceite sem `pior` passava despercebido e podia ser `remoto: sim`. [systems-designer]
- [RECOMMENDED] 18 itens na OQ-11 (ACs a dividir, fronteiras de F3 a F5, K_min > C, `reversao`, `anunciado_em`, quantização, hash em partida multi-humano, custos de boot e GC, teto ativo × alocado) e itens técnicos de engine na OQ-2 (cast decimal→float, hash canônico, snapshot fora de StreamingAssets, análise de símbolos banidos).

Disagreements adjudicadas pelo creative-director: (D1) o registro divergia do GDD, e o systems-designer estava certo; (D2) vírgula nos ACs: entradas de teste em notação de código, recomendado; (D3) só bloqueia o que faz implementar errado, passa por construção ou quebra uma promessa (cerca de 8 dos ~12 BLOCKING do qa-lead viraram recomendados); (D4) pacote entre selo e partida é lacuna real (bloqueante), mesmo número entre aparelhos é pós-lançamento; (D5) teto ativo × alocado não bloqueia, mas precisa ser resolvido antes da OQ-4; (D6) o arredondamento de meio tick muda tempos curtos, e a frase da OQ-9 foi corrigida.

Revisões aplicadas na mesma sessão (2026-11-03): os 8 bloqueantes foram resolvidos no GDD e no registro (só a expressão de `taxa_por_tick`). Decisões do usuário: teto absoluto de carga 3 s frio e 1,5 s quente (provisório, a reavaliar); pacote remoto só entra no hub, sem ritual de selo aberto. O GDD foi alterado depois da revisão, então **não há carimbo de hash**: a próxima `/design-review` deve ler o documento inteiro; pelo limite de 2 passadas, pode ser uma conferência curta dos 8 pontos.

## Ciclo encerrado — 2026-11-03
O usuário encerrou o ciclo de revisão após 2 passadas (limite do projeto), com todos os bloqueantes aplicados no texto. Não houve conferência final. Próximo trabalho: `/design-system #2 Simulação determinística`. Uma nova `/design-review` deste GDD só se surgir conflito com GDDs futuros.
