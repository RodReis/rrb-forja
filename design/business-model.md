# Modelo de Negócio e Receita: Forja das Hordas

> **Status**: Draft (decisões do usuário registradas; números do usuário pendentes)
> **Created**: 2026-11-03
> **Last Updated**: 2026-11-03
> **Fontes**: `design/gdd/game-concept.md` (Princípio de Negócio L228-238, Open Questions L371), `design/gdd/systems-index.md`, revisões do economy-designer, do technical-director, do creative-director e do producer (2026-11-03)
> **Destino**: precisa estar fechado antes do GDD #26 Economia e tetos e do GDD #27 Monetização e loja. Este documento é um registro de decisão, não um GDD.

---

## 1. Decisão

O jogo é **F2P**, com receita complementar. O jogador baixa de graça, joga o capítulo 1 sem pagar, e a receita vem de **cosméticos de loja** e de **capítulos como DLC**. O passe de temporada (só de cosméticos) entra na 1ª temporada depois do lançamento. **Não há anúncios no lançamento.** O soft launch começa **só no Android**.

| Decisão | Valor | Quem decidiu | Quando |
|---|---|---|---|
| Modelo base | F2P com cosméticos e capítulos como DLC | usuário | 2026-11-03 |
| Meta de receita | Complementar e reinvestir (cobrir custos de assets, lojas e backend e financiar o próximo conteúdo; o jogo não precisa sustentar o dev) | usuário | 2026-11-03 |
| Alavancas permitidas | Cosméticos, capítulos como DLC, passe de temporada só de cosméticos, anúncios fora do combate (este último cortado no lançamento, abaixo) | usuário | 2026-11-03 |
| Anúncios | **Cortados no lançamento** (recomendação do CD, do Producer e do economy-designer). Podem voltar depois, só na volta ao menu, com a compra "remover anúncios"; isso exige um ADR e a variante do spike | usuário | 2026-11-03 |
| Passe de temporada | **Na 1ª temporada depois do lançamento**, não no lançamento | usuário | 2026-11-03 |
| Cosméticos de conquista | **Criar** uma família só de conquista, ganha jogando e visualmente distinta dos de loja | usuário | 2026-11-03 |
| Plataforma do soft launch | **Android primeiro**; iOS entra depois do go/no-go | usuário | 2026-11-03 |

## 2. Veredictos dos revisores

| Revisor | Veredito | Resumo |
|---|---|---|
| economy-designer | Viável com condições | Viável como receita complementar, sem prazo de retorno garantido. Só deixa de ser viável com custo de aquisição pago ou conteúdo recorrente caro. |
| technical-director | Viável com condições | Cosméticos e DLC mantêm o servidor pequeno, desde que seja gerenciado e o conteúdo pago abra por token assinado do servidor, não pelo save. |
| creative-director | CONCERNS | A identidade sobrevive, com 3 regras inegociáveis (seção 4). |
| producer | Otimista | O lançamento cabe com cortes; a cadência de live ops do conceito somada a DLC e passe é irreal para um dev solo (seção 7). |

## 3. O que se vende e o que nunca se vende

**Vende:**
- O capítulo 1 é grátis. Capítulos pagos como DLC (acesso a conteúdo, que a "linha exata" do conceito já define como conteúdo; ver seção 11, ponto 1).
- Cosméticos de loja: skins de armadura e de arma, retratos, emotes, decoração da Forja. Preço direto por SKU, **sem moeda premium**.
- No futuro (1ª temporada depois do lançamento): passe de temporada só de cosméticos.

**Não vende, nunca:**
- Poder, Poder de Combate, a quantidade de recompensas não cosméticas por dia, período ou temporada, e velocidade de obter algo que conta para o ranking.
- Livro de Reforja, slot de herói, material de qualquer raridade, reforja, reroll, peso de favorecer, boosts de XP.
- Um ritual de selo alternativo, um aspecto de set dourado, títulos, molduras ou insígnias de clear ou de ranking, e qualquer coisa exibida no registro do selo ou no Grimório.
- Moeda premium. Se algum dia existir uma moeda, ela é unidirecional (só cosméticos e capítulos) e nunca é aceita na Forja, na reforja nem em slots.
- Cosméticos aleatórios (loot box): vetados até a regulação ser verificada (NOT SOURCEABLE).
- Anúncio com recompensa de jogo (material, tempo ou velocidade).

## 4. Regras inegociáveis

Registradas pelo creative-director (R1 a R3) e pelo economy-designer (R4 e R5). Cada GDD que tocar monetização as cumpre.

- **R1. O cosmético nunca altera a leitura do jogo.** Mantém a silhueta da função (passa no teste em escala de cinza), fica fora da faixa vermelho-alaranjada exclusiva dos telegraphs, não usa moldura, emissivo nem tom de raridade ou de runa, e o VFX de skill obedece ao mesmo limite de opacidade e densidade dos aliados. As regras visuais e os testes moram no art bible; o catálogo e o processo de aprovação, no GDD #27, que cita o art bible.
- **R2. Conquista não se vende.** Ritual de selo, registro do selo e do Grimório, títulos e insígnias de clear e de ranking e cosméticos de conquista só se obtêm jogando, e os cosméticos de loja são visualmente distintos dos de conquista (o jogador precisa saber, ao ver outro herói, o que ali foi conquistado).
- **R3. Conteúdo pago não vaza para placares compartilhados.** Um placar por conteúdo, nenhum ranking agregado que atravesse conteúdo pago, equipamento de capítulo pago sem vantagem nos placares gratuitos, e o objetivo do Livro alcançável no conteúdo base.
- **R4. O teto de recompensa vale por conta e por categoria, nunca por fonte.** Comprar um capítulo cria fontes novas de material; o teto por fonte escalaria com o que o jogador comprou.
- **R5. Preço direto por SKU.** Sem moeda premium.

**Teste de catálogo:** cada SKU é classificado com a pergunta de L371 do conceito ("este item muda o resultado de alguma run ou a recompensa esperada por dia ou por temporada?"). Só entra se a resposta for não.

**Como vamos saber que acertamos** (CD): no teste em escala de cinza, nenhum cosmético faz uma função parecer outra; um jogador consegue apontar, só olhando, o que outro herói conquistou; e nenhum placar gratuito tem o top 100 dominado por equipamento de DLC.

## 5. Condições de viabilidade (economy-designer)

A viabilidade vale só com as três:
1. **Custo de aquisição pago igual a zero** (orgânico e comunidade). Com aquisição paga, o risco de mercado de L356 do conceito vira prejuízo.
2. **Custo recorrente mínimo:** backend em camada gratuita ou barata, e cosméticos feitos sobre o pipeline de peças existente.
3. **Critério de saída escrito antes do soft launch.** Se a receita projetada não cobrir o custo recorrente, o jogo vira premium ou capítulos pagos, sem retrabalho de economia.

## 6. Impacto por sistema

| Sistema | Mudança |
|---|---|
| #26 Economia e tetos | Teto por conta e por categoria; relógio do servidor (o período e os tetos só avançam ao sincronizar); sumidouros de cosméticos; sinks terminais depois do set dourado; paridade entre capítulo grátis e pago, sem power creep; o simulador headless como validador. |
| #27 Monetização e loja | Sobe de M para L: IAP, loja, liberação dos capítulos DLC e catálogo. O passe fica fora do lançamento. |
| #29 Serviços online | O núcleo deixa de ser cortável: validação de compras, relógio confiável, remote config, entitlements. Cloud save recomendado (perder um cosmético pago gera reembolso). |
| #34 Analytics e live ops | Não pode mais ser reduzido ao log do #5: o soft launch precisa medir funil e retenção. O consentimento (#39) controla o #34. |
| #20 Campanha e capítulos | Consulta o #37 Entitlements (nunca o #29) para saber o que está aberto. |
| #15 Auto-battle e varredura | Em aberto (seção 11, ponto 3): o economy-designer e o Producer propõem dividir; a varredura fica no Alpha e o auto-battle vai para o Full Vision. |
| **#37 Entitlements (novo)** | Foundation. Interface de leitura que o #29 alimenta, no mesmo padrão do remote config no #1. Entra antes do GDD #20. |
| **#38 Cosméticos e catálogo (novo)** | Alpha. Catálogo de loja e a família de cosméticos de conquista. |
| **#39 Consentimento e privacidade (novo)** | Alpha, bloqueia o soft launch. Controla o #34 e o #29. |

## 7. Arquitetura (technical-director)

- **Compras:** o recibo é validado **no servidor**, nunca no cliente. O servidor guarda as posses ("entitlements") e devolve um **token assinado**; o cliente confere com uma chave pública embutida. A restauração de compra passa pela loja e é revalidada no servidor.
- **Sem rede:** vale o último token em cache. Comprar exige rede.
- **O save local (#28) não guarda posses.** Um booleano "capítulo 2 pago" no save é editável. O conteúdo pago abre pelo token, e o save só guarda o progresso. Risco aceito: um aparelho com root que modifica o binário ainda libera cosméticos; isso custa receita, não justiça, porque não há vantagem paga.
- **Capítulos pagos e ranking:** o #29 cruza a posse com o score no servidor antes de aceitá-lo. O #22 Ranking continua sem saber de posse, então não surge ciclo.
- **Relógio:** online vale a hora do servidor. Offline usa o relógio do aparelho, mas o save guarda a maior hora já vista e nunca volta abaixo dela; o acúmulo offline é limitado a K períodos até a próxima sincronização (knob no #1). Um score enviado com hora suspeita não entra no ranking.
- **ADRs:** backend (gerenciado, sem servidor próprio) e compras no app com restauração, juntos, **antes do GDD #26** (o Producer pede no início do Vertical Slice; o TD havia dito no fim; a data de início do Vertical Slice decide); consentimento e privacidade, no Alpha. Um spike de compra e restauração em sandbox roda ainda no Vertical Slice.
- **Bloqueio prático:** os módulos de build Android e iOS **não estão instalados** (`docs/engine-reference/unity/VERSION.md`). Sem o módulo Android não dá para testar IAP nem o spike.

## 8. Cronograma e escopo (proposta do Producer; ainda não aceita pelo usuário)

- O F2P soma de 2 a 3 meses de trabalho (compras, backend, consentimento, analytics) e mais 2 a 3 de soft launch.
- **Marco novo: soft launch no fim do Alpha (mês 19 a 20)**, só Android, com o capítulo 1 grátis. O lançamento global esperado passaria do mês 20 para o **mês 23 a 24**.
- **Cadência:** o conceito (L363) pede um evento por mês e um capítulo por trimestre. Isso mais DLC e passe é irreal para um dev solo. Proposta: temporada de 10 a 12 semanas alinhada ao capítulo DLC, eventos feitos só com dados (remote config sobre fases que já existem) e um set cosmético por temporada.
- **Arte:** um set cosmético são cerca de 6 peças com fit em 4 corpos (Orc e Humano, 2 gêneros): 150 a 250 h por temporada, estimativa **sem calibração**. As peças cosméticas entram no denominador do H do critério de pipeline antes de D0.
- **Nova ordem de corte** (substitui a do índice): (1) anúncios (já cortados no lançamento); (2) passe (já adiado); (3) #22 Ranking; (4) auto-battle, mantendo a varredura; (5) capítulo 2 como 1º DLC, o corte que agora gera receita; (6) reforja grátis por nerf (o Livro e a run de reforja ficam, por decisão do CD). **Nunca cortar:** o baseline de #33, o #28, o núcleo do #29 e o consentimento (#39).

## 9. Métricas de soft launch (limiares NOT SOURCEABLE)

Crash e ANR dentro do Play vitals; retenção D1, D7 e D30; % de pagantes; receita por usuário ativo; payback; conversão do capítulo 1 para o DLC; % de jogadores que atingem os tetos diários. **Os limiares de go/no-go precisam de commit antes do soft launch**, derivados de benchmarks públicos de jogos mobile, do que o fornecedor de pagamentos informar e do próprio soft launch, com intervalos largos porque a amostra será pequena. O soft launch também é o primeiro playtest externo.

## 10. O que não pode ser afirmado e precisa ser verificado

`NOT SOURCEABLE` significa que nenhum revisor pôde afirmar o fato com fonte do repositório; cada item abaixo precisa ser verificado antes do lançamento:
- **Mercado:** conversão, ARPU, retenção e eCPM de jogos comparáveis, e quanto cosmético e DLC sem vantagem de poder rendem. Como obter: relatórios públicos de benchmark e dados do soft launch.
- **Lojas:** comissão de cada loja, tipo de produto para o DLC e o passe (consumível, não consumível ou assinatura), versão exigida da Play Billing Library, botão de restaurar compras, exclusão de conta se houver conta, política de cada loja para passes.
- **Privacidade e lei:** LGPD e GDPR, política de privacidade, formulário Data Safety no Google Play, classificação etária (IARC) e regras para menores.
- **Regulação** de cosméticos aleatórios (loot box).
- **Unity 6.3:** Unity IAP, UGS (Cloud Save, Leaderboards, Remote Config), hora do servidor e relógio monotônico no Android. Nada disso está em `docs/engine-reference/unity/`; verificar com a documentação do fornecedor, um ADR e um spike em aparelho.
- **Fiscal:** como receber (CNPJ ou MEI) e a tributação.

## 11. Pontos em aberto

1. **Quais capítulos são grátis e quais são pagos.** O Producer propõe o capítulo 1 grátis no soft launch e o capítulo 2 como 1º DLC (o corte já previsto no conceito). O conceito tem 2 capítulos no lançamento e os capítulos 3 e 4 no pós-lançamento. Os capítulos pagos não podem exceder o Poder de Combate alcançável no conteúdo grátis, ou o ranking é segmentado por capítulo. No coop (pós-lançamento), o host paga e o convidado entra, senão a fila fragmenta e o Pilar 3 sofre.
2. **Aceitar o mês 23 a 24** como lançamento global esperado e o soft launch no mês 19 a 20.
3. **Dividir o #15?** Varredura no Alpha e auto-battle no Full Vision (economy-designer e Producer propõem; o CD notou que o #15 não serve a nenhum pilar).
4. **Moeda sem poder** para cosméticos ganhos jogando: se parte do catálogo for ganha, precisa de uma moeda sem poder e de um catálogo que não se esgote antes do fim da fonte. Sem decisão ainda.
5. **Data do ADR de backend** (início ou fim do Vertical Slice).

## 12. Dados que só o usuário pode fornecer

| Campo | Valor |
|---|---|
| Horas por semana disponíveis | [A DEFINIR] |
| Caixa mensal e total disponíveis | [A DEFINIR] |
| Prazo aceitável para cobrir os custos | [A DEFINIR] |
| Teto de custo mensal do backend | [A DEFINIR] |
| Preço do DLC e moeda base | [A DEFINIR] |
| Verba para comprar arte | [A DEFINIR] |
| Como receber (CNPJ ou MEI) | [A DEFINIR] |
| Países do soft launch | [A DEFINIR] |
| Orçamento de aquisição de usuários (esperado: zero; confirmar) | [A DEFINIR] |
| Gatilho para voltar ao premium (critério de saída da seção 5) | [A DEFINIR] |

## 13. Próximos passos

- [ ] Preencher a seção 12 e responder aos pontos em aberto da seção 11
- [ ] Instalar o módulo Android Build Support no editor 6000.3.27f1 (bloqueia o spike de compras)
- [ ] ADR de backend e de compras no app, antes do GDD #26
- [ ] `/art-bible` com as regras R1 e R2 como requisito (cosméticos e família de conquista)
- [ ] Escrever o GDD #26 Economia e tetos com este documento como entrada, e o #27 Monetização e loja
- [ ] Definir os limiares de go/no-go e o critério de saída com commit antes do soft launch
