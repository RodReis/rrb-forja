<!-- PROTOTYPE - NOT FOR PRODUCTION -->
<!-- Question: Skills aleatórias registradas no Grimório e seladas para sempre soam como expressão (a build é minha) ou como caça-níquel? -->
<!-- Date: 2026-11-02 -->

# Concept Prototype Report: Forja das Hordas — Grimório + selamento

> **Date**: 2026-11-02
> **Prototype Path**: HTML
> **Concept File**: design/gdd/game-concept.md

---

## Hypothesis

"Se o jogador jogar 3 fases curtas de horda, registrar no Grimório as skills ativas ao
vencer cada chefe e depois selar 4 delas, vai sentir que a build é **dele**, e não da sorte."

Sinais definidos antes do teste (5 testadores):
- Pelo menos 3 de 5 explicam em 1 frase *por que* selaram aquelas 4, por intenção e não por "as mais fortes".
- Pelo menos 3 de 5 pedem para jogar de novo para registrar uma skill específica.
- No máximo 1 de 5 descreve o sorteio como injusto ou "pura sorte".

---

## Riskiest Assumption Tested

Este é o 1º risco de design do conceito: **skill aleatória somada ao selamento permanente pode parecer
caça-níquel.** O sorteio não pareceu injusto, porque o reroll e o favorecer bastaram. A outra metade
do risco segue em aberto: o selamento ser vivido como **identidade**, e não só como eficácia.
A amostra de 1 testador não é suficiente para fechá-la.

---

## Approach

Um único `prototype.html` com tudo inline, que abre por duplo clique. Foi feito numa sessão.

- Arena top-down, movimento por WASD e setas, auto-ataque e horda de formas simples.
- 3 fases de 90 s, cada uma com chefe no fim.
- Level up com 1 de 3 cartas, a partir de 12 skills (8 ativas e 4 passivas) e 3 evoluções por sinergia.
- 1 reroll por fase e a opção de favorecer uma skill do Grimório (peso 3×).
- Grimório: registra as skills ativas ao vencer o chefe. Morrer não registra nada.
- Selamento: 4 skills do Grimório, campo obrigatório "Por que essas 4?" e botão "Jogar mais uma fase antes de selar".
- Prova do Selo: 60 s com a build selada no nível máximo, mais o chefe.
- Botão **Log**: exporta todos os eventos em JSON.

**Path chosen:** HTML
**Reason for path:** a hipótese é sobre escolha e autoria da build, não sobre timing. A latência do
navegador não contamina o resultado, e o arquivo vai para testadores externos em minutos.

**Shortcuts taken (intentional):**
- Todos os valores estão hardcoded no objeto `K`, e não há balanceamento.
- A arte é de formas geométricas, sem som e sem menus.
- Não há Tank, funções, Forja, sets, raridades, esquiva ou telegraph, nem controle de toque.
- O Grimório fica só em memória (recarregar a página o apaga).

**Verificação antes do playtest:**
- Uma checagem de sintaxe com `node --check`.
- Um smoke headless em Node com DOM simulado. O jogador ficou invulnerável e sempre escolheu a 1ª carta.
- O smoke venceu as 3 fases em cerca de 110 s cada (nível 11 a 14, cerca de 430 abates por fase) e venceu a Prova do Selo em 77 s.
- A evolução Tornado de Aço foi oferecida e substituiu o Machado Giratório.
- O smoke não exercitou a tela real (desenho, cliques, campo de texto). Isso foi coberto pelo playtest do usuário.

---

## Result

Houve 1 sessão de playtest, feita pelo próprio designer. Respostas do debrief, nas palavras do usuário:

- **Hipótese:** "CONFIRMADA".
- **Justificativa do selo:** "Gostei delas, me ajudaram".
- **Vontade de jogar mais antes de selar ou depois:** "não senti vontade de jogar mais".
- **Sorteio, reroll e favorecer:** "foi suficiente".
- **Melhor momento:** "jogar a Prova do Selo com a build no máximo".
- **Pior momento:** "os controles WASD, fica dificio com o mouse junto vai melhorar".
- **Surpresa:** "foi boa tudo dentro do padrão do jogo".
- **Veredito:** "PROCEED". O usuário não deu a frase do porquê.

O log JSON da sessão não foi colado no debrief. As escolhas, os rerolls e o tempo na tela de selamento
**não foram analisados**.

**Leitura contra os sinais definidos:**

| Sinal | Resultado | Observação |
|---|---|---|
| Sorteio justo (≤ 1/5 "pura sorte") | ✅ atingido (1/1) | reroll + favorecer bastaram |
| Selar por intenção (≥ 3/5) | ⚠️ ambíguo (1/1) | "me ajudaram" descreve eficácia, não identidade |
| Querer jogar de novo para registrar uma skill (≥ 3/5) | ❌ não atingido (0/1) | o "só mais uma" não apareceu |
| Amostra | ⚠️ 1 de 5 | testador interno, que conhece o design |

---

## Metrics

| Metric | Value |
|--------|-------|
| Path used | HTML |
| Iterations to playable | N/A (HTML) |
| Prototype duration | 1 sessão (02/11/2026) |
| Playtesters | 1 internal / 0 external |
| Feel assessment | Controle WASD + mouse foi o ponto mais fraco ("fica difícil com o mouse junto"). O movimento por cursor ou joystick deve melhorar. O pico de satisfação foi a Prova do Selo com a build no nível máximo. |
| Hypothesis verdict | CONFIRMED (declarado pelo testador; os sinais pré-definidos ficaram 1 atingido, 1 ambíguo e 1 não atingido) |

---

## Recommendation: PROCEED

O usuário deu o veredito PROCEED, mas **não deu a frase do porquê**. Ela fica em aberto aqui, sem ser
inferida.

**Evidência a favor:** a hipótese foi declarada confirmada e o sorteio não pareceu caça-níquel. O momento mais
forte foi justamente ver a build selada em ação, que é o coração do pilar "Sua build, sua assinatura".

**Ressalvas que seguem com o PROCEED:**
1. A amostra é de 1 testador interno.
2. A justificativa do selo foi por eficácia e não por identidade.
3. O loop do "só mais uma" (voltar para registrar uma skill) não se manifestou.

O usuário é dev solo e não haverá testadores externos. A validação do GDD do Grimório e do selamento é por
métricas de log com n = 1, definidas nos critérios de aceite do MVP em `design/gdd/game-concept.md`.

*Correção de 2026-11-03, no `/design-review` do conceito:* a saturação do Grimório **não** era só uma questão de
tuning do GDD. Ela é estrutural (o systems-designer discordou deste relatório, e o CD concordou com ele). A regra de
escassez entrou no conceito: o jogador escolhe 1 a 2 skills por chefe de fase, com nível mínimo de elegibilidade.

---

## Creative Director Review (CD-PLAYTEST)

**Verdict: CONCERNS.** A decisão do usuário foi **aceitar com ressalvas**: PROCEED mantido, sem novos testes.

O CD vê a metade "este herói é meu e eu o uso" presente, porque a Prova do Selo foi o pico. A metade "cada skill foi conquistada / selar a identidade" não apareceu. Ressalvas que seguem para os GDDs:
1. **Selo por eficácia, pico no poder máximo e falta de vontade de voltar** apontam para a "power fantasy pura" que o conceito descartou.
2. O **Pilar 1 está em risco**: a tela de selamento não convida a escolher por identidade (função, estilo, tema). O GDD do selamento deve provocar essa escolha, não só medi-la.
3. O **Grimório saturado** (11 de 12) esvazia o Pilar 2 e a "conquista". A escassez é a variável principal do GDD do Grimório: 4 registros por fase, ou registro só acima de um nível mínimo.
4. O gancho do **"só mais uma"** ficou 0 de 1 e deve ser tratado como não validado.
5. A evidência é de **n = 1, e o testador é o designer**. O registro correto da hipótese é **parcialmente suportada, não conclusiva**. O usuário é dev solo e não fará testes externos, o que fica como limite conhecido.
6. Os **Pilares 3, 4 e 5 não foram avaliados.** O selo com peso de função (o "Orc tanque") pode mudar o ponto 2.

---

## If Proceeding

- **Core tuning values discovered:**
  - Fases de 90 s até o chefe, mais cerca de 20 s de chefe, dão cerca de 10 a 13 level ups por fase.
  - Com `MAX_SKILLS = 6`, o Grimório chegou a **11 de 12 skills em 3 fases** no smoke. Quase tudo fica registrado,
    o que esvazia a escassez da escolha no selamento. O ponto de partida para o GDD é testar 4 slots por fase
    ou registrar só as skills acima de um nível mínimo.
  - Reroll 1 por fase e favorecer com peso 3×: "foi suficiente" contra a sensação de sorte.
- **Assumptions confirmed:**
  - A agência sobre o sorteio (reroll + favorecer) neutraliza a sensação de caça-níquel.
  - Jogar com a build selada é recompensador.
- **Assumptions disproved:** nenhuma de forma conclusiva. Fica **não confirmado** que o Grimório gere o "só mais uma"
  (voltar à fase para registrar uma skill específica). O conceito lista isso como gancho de retenção.
- **Emergent mechanics:**
  - O retorno emocional se concentrou **depois** do selamento (a Prova), não no ato de selar. O ritual e a primeira
    luta com a build selada merecem peso de design no GDD.
  - O movimento por cursor aparece como mais natural, e está alinhado ao joystick de um dedo do alvo mobile.

> Note: o caminho HTML foi usado. A sensação de combate (impacto, esquiva) não foi avaliada. Ela precisa de um
> protótipo na engine antes dos GDDs de combate.

**Next steps:**
O usuário decidiu não fazer mais testes.

1. `/design-review design/gdd/game-concept.md`
2. `/gate-check`
3. `/map-systems`
4. `/design-system [mechanic]`, usando estes achados e as ressalvas do CD em Tuning Knobs e Formulas.

---

## If Pivoting

Não se aplica (veredito PROCEED).

---

## If Killing

Não se aplica (veredito PROCEED).

---

## Lessons Learned

- **What assumptions were broken by actually building this?**
  Com 6 slots e 3 fases, o Grimório acaba contendo quase todas as skills. O valor de "conquistar" uma skill
  depende de escassez que o desenho atual não garante.
- **What surprised us that didn't show up in the brainstorm?**
  O pico de satisfação foi a Prova do Selo, ou seja, *usar* a build. Não foi a escolha. O testador não relatou
  surpresas durante o jogo.
- **What would we test differently next time?**
  - O designer não é um testador ingênuo e não haverá testadores externos. Compensar com critérios escritos antes de jogar, justificativa registrada antes da Prova e configurações de knob ocultas, identificadas só no log.
  - Coletar o Log obrigatoriamente.
  - Mover pelo cursor em vez de WASD.
  - Medir o "só mais uma" com uma pergunta direta após a Prova: "Quer forjar outro herói?"

---

> *Prototype code location: `prototypes/grimorio-concept/`*
> *This code is throwaway. Never refactor into production.*
