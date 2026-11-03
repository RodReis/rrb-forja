# Modelo de Negócio e Receita: Forja das Hordas

> **Status**: Draft (decisões validadas em 2026-11-03; faltam preço por SKU, orçamento de aquisição e gatilho de saída)
> **Created**: 2026-11-03
> **Last Updated**: 2026-11-03 (validação das seções 11 e 12 pelo usuário)
> **Fontes**: `design/gdd/game-concept.md` (Princípio de Negócio L228-238, Open Questions L371), `design/gdd/systems-index.md`, revisões do economy-designer, do technical-director, do creative-director e do producer (2026-11-03)
> **Destino**: precisa estar fechado antes do GDD #26 Economia e tetos e do GDD #27 Monetização e loja. Este documento é um registro de decisão, não um GDD.

---

## 1. Decisão

O jogo é **F2P**, com receita complementar. O jogador baixa de graça e joga **todos os capítulos, dungeons e PvP sem pagar**: não existe conteúdo de gameplay pago. A receita vem de **cosméticos de loja** (skins e transmogs temáticos, pets só de animação). O passe de temporada (só de cosméticos) entra na 1ª temporada depois do lançamento. Há um **vídeo recompensado ao fim da partida** (PVE) que dobra só a **moeda de jogo sem poder**. O soft launch começa **só no Android**.

| Decisão | Valor | Quem decidiu | Quando |
|---|---|---|---|
| Modelo base | F2P com cosméticos de loja; **sem conteúdo de gameplay pago** (todos os capítulos, dungeons e PvP são grátis) | usuário | 2026-11-03 |
| Meta de receita | Complementar e reinvestir (cobrir custos de assets, lojas e backend e financiar o próximo conteúdo; o jogo não precisa sustentar o dev) | usuário | 2026-11-03 |
| DLC | **Só cosméticos:** skins e transmogs temáticos, e pets **só de animação** (o efeito do jogo é o mesmo com ou sem o pet) | usuário | 2026-11-03 |
| Passe de temporada | Só de cosméticos, **na 1ª temporada depois do lançamento** | usuário | 2026-11-03 |
| Anúncio: banner ou intersticial | **Cortados** (recomendação do CD, do Producer e do economy-designer) | usuário | 2026-11-03 |
| Anúncio: vídeo recompensado | **Só ao fim da partida (PVE), e só dobra a moeda de jogo sem poder.** Nunca durante a partida; nunca material, XP, skill, reroll, tempo nem velocidade | usuário | 2026-11-03 |
| Skill por vídeo durante a partida | **Vetado** (é agência sobre o sorteio e desfaz "cada skill foi conquistada") | usuário | 2026-11-03 |
| Moeda de jogo sem poder | **Aprovada:** ganha jogando e por vídeo, nunca vendida, gasta só em cosméticos | usuário | 2026-11-03 |
| Cosméticos de conquista | **Criar** uma família só de conquista, ganha jogando e visualmente distinta dos de loja | usuário | 2026-11-03 |
| Plataforma do soft launch | **Android primeiro**; iOS entra depois do go/no-go | usuário | 2026-11-03 |
| Cronograma | Soft launch no mês 19 a 20 (fim do Alpha) e lançamento global no mês 23 a 24 | usuário | 2026-11-03 |
| Dedicação | **80 h por semana** | usuário | 2026-11-03 |
| Escopo do #15 | Dividido: **Varredura** no Alpha e **Auto-battle com IA** no Full Vision | usuário | 2026-11-03 |

## 2. Veredictos dos revisores

Os 4 revisores avaliaram a versão com capítulos como DLC e sem vídeo recompensado. Os veredictos abaixo valem para aquela versão; a versão atual é mais simples no servidor (sem conteúdo pago de gameplay) e mais complexa nos anúncios (SDK e consentimento de vídeo). O Producer **não reavaliou** o cronograma com o SDK de vídeo.

| Revisor | Veredito | Resumo |
|---|---|---|
| economy-designer | Viável com condições | Viável como receita complementar, sem prazo de retorno garantido. Só deixa de ser viável com custo de aquisição pago ou conteúdo recorrente caro. |
| technical-director | Viável com condições | Cosméticos mantêm o servidor pequeno, desde que seja gerenciado e a posse abra por token assinado do servidor, não pelo save. |
| creative-director | CONCERNS | A identidade sobrevive, com regras inegociáveis (seção 4). |
| producer | Otimista | O lançamento cabe com cortes; a cadência de live ops do conceito somada a DLC e passe é irreal para um dev solo (seção 8). |

## 3. O que se vende e o que nunca se vende

**Vende:**
- Cosméticos de loja: skins e transmogs temáticos de armadura e arma, retratos, emotes, decoração da Forja, e pets **só de animação**. Preço direto por SKU em dinheiro real.
- No futuro (1ª temporada depois do lançamento): passe de temporada só de cosméticos.

**Dá de graça jogando:**
- Todos os capítulos, dungeons e PvP.
- Cosméticos de conquista (só por feitos no jogo).
- Moeda de jogo sem poder, gasta em cosméticos (seção 4, R5).

**Não vende, nunca:**
- Poder, Poder de Combate, a quantidade de recompensas não cosméticas por dia, período ou temporada, e velocidade de obter algo que conta para o ranking.
- Livro de Reforja, slot de herói, material de qualquer raridade, reforja, reroll, peso de favorecer, boosts de XP.
- Um ritual de selo alternativo, um aspecto de set dourado, títulos, molduras ou insígnias de clear ou de ranking, e qualquer coisa exibida no registro do selo ou no Grimório.
- **Pet ou cosmético com efeito mecânico** (coleta, cura, atributo): o efeito é o mesmo com ou sem o item.
- Moeda comprável com dinheiro real (moeda premium).
- Cosméticos aleatórios (loot box): vetados até a regulação ser verificada (NOT SOURCEABLE).
- Skill, reroll, material ou XP por vídeo, e qualquer vídeo durante a partida.

## 4. Regras inegociáveis

Registradas pelo creative-director (R1 a R3), pelo economy-designer (R4 e R5) e pela validação do usuário (R6 e R7). Cada GDD que tocar monetização as cumpre.

- **R1. O cosmético nunca altera a leitura do jogo.** Mantém a silhueta da função (passa no teste em escala de cinza), fica fora da faixa vermelho-alaranjada exclusiva dos telegraphs, não usa moldura, emissivo nem tom de raridade ou de runa, e o VFX de skill obedece ao mesmo limite de opacidade e densidade dos aliados. As regras visuais e os testes moram no art bible; o catálogo e o processo de aprovação, no GDD #27 e no #38, que citam o art bible.
- **R2. Conquista não se vende.** Ritual de selo, registro do selo e do Grimório, títulos e insígnias de clear e de ranking e cosméticos de conquista só se obtêm jogando, e os cosméticos de loja são visualmente distintos dos de conquista (o jogador precisa saber, ao ver outro herói, o que ali foi conquistado). Um cosmético comprado com moeda de jogo conta como **de loja** para esse efeito: só os de conquista usam a assinatura visual de conquista.
- **R3. Conteúdo pago não vaza para placares compartilhados.** Hoje não há conteúdo de gameplay pago, então esta regra é uma salvaguarda: se algum dia houver, um placar por conteúdo, nenhum ranking agregado que atravesse conteúdo pago, e equipamento pago sem vantagem nos placares gratuitos.
- **R4. O teto de recompensa vale por conta e por categoria, nunca por fonte.**
- **R5. Preço direto por SKU, e só uma moeda: a de jogo.** A moeda de jogo é **ganha jogando e por vídeo recompensado**, **nunca vendida**, gasta **só em cosméticos de loja** e nunca aceita na Forja, na reforja, em slots nem em nada com efeito mecânico. As taxas de ganho e o teto da moeda são definidos no GDD #26.
- **R6. Vídeo recompensado:** só ao fim da partida no PVE; dobra só a moeda de jogo; o SDK só inicializa depois do consentimento e fora da fase; nunca material, XP, skill, reroll, tempo ou velocidade.
- **R7. Pet e qualquer cosmético com "skill" ou "habilidade" é só animação.** Coleta, cura e atributo funcionam igual com ou sem o item.

**Teste de catálogo:** cada SKU é classificado com a pergunta de L371 do conceito ("este item muda o resultado de alguma run ou a recompensa esperada por dia ou por temporada?"). Só entra se a resposta for não. O pet com cura e atributo reais (como o usuário descreveu no primeiro rascunho) **reprovou** nesse teste e virou o pet só de animação.

**Como vamos saber que acertamos** (CD): no teste em escala de cinza, nenhum cosmético faz uma função parecer outra; um jogador consegue apontar, só olhando, o que outro herói conquistou; e nenhum placar tem o top 100 dominado por quem comprou algo.

## 5. Condições de viabilidade (economy-designer)

A viabilidade vale só com as três:
1. **Custo de aquisição pago igual a zero** (orgânico e comunidade). Com aquisição paga, o risco de mercado de L356 do conceito vira prejuízo. **Ainda não confirmado** (seção 12).
2. **Custo recorrente mínimo:** backend em camada gratuita ou barata, e cosméticos feitos sobre o pipeline de peças existente. **Sem teto numérico** (seção 12): cada gasto é aprovado pelo usuário.
3. **Critério de saída escrito antes do soft launch.** Se a receita projetada não cobrir o custo recorrente, o jogo muda de modelo. **O gatilho ainda não foi definido** (seção 12).

Com o conteúdo de gameplay 100% grátis, o "premium" ou os "capítulos pagos" deixaram de ser saída sem mudar a regra do jogo: o critério de saída precisa nomear a mudança (por exemplo, premium com preço único), e isso é decisão do usuário.

## 6. Impacto por sistema

| Sistema | Mudança |
|---|---|
| #26 Economia e tetos | Teto por conta e por categoria; relógio do servidor (o período e os tetos só avançam ao sincronizar); a **moeda de jogo sem poder** (taxas de ganho, teto, dobra pelo vídeo); sumidouros de cosméticos; sinks terminais depois do set dourado; o simulador headless como validador. |
| #27 Monetização e loja | Sobe de M para L: IAP, loja, catálogo de cosméticos e o vídeo recompensado. O passe fica fora do lançamento. |
| #29 Serviços online | O núcleo deixa de ser cortável: validação de compras, relógio confiável, remote config, entitlements. Cloud save recomendado (perder um cosmético pago gera reembolso). |
| #34 Analytics e live ops | Não pode mais ser reduzido ao log do #5: o soft launch precisa medir funil e retenção. O consentimento (#39) controla o #34. |
| #20 Campanha e capítulos | Sem conteúdo pago, **não consulta o #37**. |
| #15 Varredura / #40 Auto-battle com IA | **Dividido** (aprovado): a Varredura fica no Alpha, e o Auto-battle vai para o Full Vision. |
| **#37 Entitlements (novo)** | Passa de MVP para **Alpha**: só guarda a posse de cosméticos. Interface de leitura que o #29 alimenta, no mesmo padrão do remote config no #1. |
| **#38 Cosméticos e catálogo (novo)** | Alpha. Catálogo de loja (inclui pets só de animação), a família de cosméticos de conquista e os cosméticos de moeda. |
| **#39 Consentimento e privacidade (novo)** | Alpha, bloqueia o soft launch. Cobre também o SDK do vídeo recompensado. Controla o #34 e o #29. |
| **#40 Auto-battle com IA (novo, por divisão do #15)** | Full Vision. Depende de #2, #3, #13 (IA), #15, #17 e #20. |

## 7. Arquitetura (technical-director)

- **Compras:** o recibo é validado **no servidor**, nunca no cliente. O servidor guarda as posses ("entitlements") e devolve um **token assinado**; o cliente confere com uma chave pública embutida. A restauração de compra passa pela loja e é revalidada no servidor.
- **Sem rede:** vale o último token em cache. Comprar exige rede.
- **O save local (#28) não guarda posses.** Um booleano "skin comprada" no save é editável. A posse abre pelo token, e o save só guarda o progresso. Risco aceito: um aparelho com root que modifica o binário ainda libera cosméticos; isso custa receita, não justiça, porque não há vantagem paga.
- **Relógio:** online vale a hora do servidor. Offline usa o relógio do aparelho, mas o save guarda a maior hora já vista e nunca volta abaixo dela; o acúmulo offline é limitado a K períodos até a próxima sincronização (knob no #1). Um score enviado com hora suspeita não entra no ranking.
- **Vídeo recompensado:** inicializar o SDK e carregar o vídeo **só fora da fase**; um símbolo de compilação (`FORJA_ADS`) tira o SDK dos builds de desenvolvimento e de teste; o SDK só inicializa depois do consentimento; o spike de performance ganha uma variante com o SDK ativo, medida no minuto 20.
- **ADRs:** backend (gerenciado, sem servidor próprio) e compras no app com restauração, juntos, **antes do GDD #26** (início do Vertical Slice, na leitura do usuário "início da necessidade"); consentimento, privacidade e anúncios, no Alpha. Um spike de compra e restauração em sandbox roda ainda no Vertical Slice. A preferência de fornecedor do usuário é Railway e Supabase (seção 12); o ADR compara com um backend gerenciado.
- **Android Build Support:** **verificado em 2026-11-03**: o editor 6000.3.27f1 tem o módulo `AndroidPlayer` com SDK, NDK, OpenJDK e a variação IL2CPP. O aparelho de referência não foi verificado. O iOS não está instalado (não é necessário no soft launch).

## 8. Cronograma e escopo

- O F2P soma de 2 a 3 meses de trabalho (compras, backend, consentimento, analytics) e mais 2 a 3 de soft launch. Estimativa do Producer, **sem o SDK de vídeo recompensado**; ele não a reavaliou.
- **Aprovado pelo usuário:** soft launch no fim do Alpha (mês 19 a 20), só Android, e lançamento global no **mês 23 a 24**. O conceito congelado diz 16 meses.
- **Dedicação:** 80 h por semana. As estimativas do Producer (MVP em ~60 dias úteis de implementação) pressupõem dedicação próxima de tempo integral; 80 h por semana é cerca de duas jornadas completas, e o risco é o ritmo sustentado por mais de 20 meses.
- **Cadência:** o conceito (L363) pede um evento por mês e um capítulo por trimestre. Sem capítulo pago, a regra deixa de ser comercial. Proposta: temporada de 10 a 12 semanas, eventos feitos só com dados (remote config sobre fases que já existem) e um set cosmético por temporada.
- **Arte:** um set cosmético são cerca de 6 peças com fit em 4 corpos (Orc e Humano, 2 gêneros): 150 a 250 h por temporada, estimativa **sem calibração**. As peças cosméticas entram no denominador do H do critério de pipeline antes de D0.
- **Nova ordem de corte** (substitui a do índice): (1) vídeo recompensado e o SDK de anúncios; (2) passe (já adiado); (3) #22 Ranking; (4) reduzir a cadência de sets cosméticos por temporada; (5) reforja grátis por nerf (o Livro e a run de reforja ficam, por decisão do CD). **Nunca cortar:** o baseline de #33, o #28, o núcleo do #29 e o consentimento (#39).

## 9. Métricas de soft launch (limiares NOT SOURCEABLE)

Crash e ANR dentro do Play vitals; retenção D1, D7 e D30; % de pagantes; receita por usuário ativo; receita de vídeo recompensado; payback; % de jogadores que atingem os tetos diários. **Os limiares de go/no-go precisam de commit antes do soft launch**, derivados de benchmarks públicos de jogos mobile, do que o fornecedor de pagamentos informar e do próprio soft launch, com intervalos largos porque a amostra será pequena. O soft launch também é o primeiro playtest externo.

## 10. O que não pode ser afirmado e precisa ser verificado

`NOT SOURCEABLE` significa que nenhum revisor pôde afirmar o fato com fonte do repositório; cada item abaixo precisa ser verificado antes do lançamento:
- **Mercado:** conversão, ARPU, retenção e eCPM de jogos comparáveis, e quanto cosmético sem vantagem de poder e vídeo recompensado rendem. Como obter: relatórios públicos de benchmark e dados do soft launch.
- **Lojas:** comissão de cada loja, tipo de produto para o cosmético e o passe (consumível, não consumível ou assinatura), versão exigida da Play Billing Library, botão de restaurar compras, exclusão de conta se houver conta, política de cada loja para passes e para vídeo recompensado.
- **Privacidade e lei:** LGPD e GDPR, regras dos EUA, política de privacidade, formulário Data Safety no Google Play, classificação etária (IARC) e regras para menores e para anúncios a menores. O soft launch em Brasil, EUA e Europa soma as três frentes.
- **Regulação** de cosméticos aleatórios (loot box).
- **Unity 6.3:** Unity IAP, SDK de anúncios e mediação, UGS (Cloud Save, Leaderboards, Remote Config), hora do servidor e relógio monotônico no Android. Nada disso está em `docs/engine-reference/unity/`; verificar com a documentação do fornecedor, um ADR e um spike em aparelho.
- **Fiscal:** a tributação de receber como CNPJ.
- **Preço dos planos de backend e de ferramentas** (Railway, Supabase, etc.): não verificado.

## 11. Pontos em aberto, resolvidos em 2026-11-03

| # | Ponto | Resolução (usuário) |
|---|---|---|
| 1 | Quais capítulos são grátis e quais são pagos | **Todos são grátis.** Não há parte paga nos capítulos, dungeons nem PvP. |
| 2 | Aceitar o mês 23 a 24 como lançamento global e o soft launch no mês 19 a 20 | **Aprovado.** |
| 3 | Dividir o #15 | **Aprovado:** Varredura no Alpha, Auto-battle com IA no Full Vision. |
| 4 | Moeda sem poder para cosméticos ganhos jogando | **Aprovada** (R5). |
| 5 | Data do ADR de backend | **No início da necessidade:** antes do GDD #26, no início do Vertical Slice. |
| 6 | DLC | **Cosméticos:** skins e transmogs temáticos e pets. O pet com "1 skill e 1 habilidade" que pega loot, poção de cura e atributo foi reprovado no teste de catálogo e virou **só animação** (R7). |
| 7 | Vídeo ao fim da partida (PVE) para dobrar os ganhos | **Só dobra a moeda de jogo sem poder** (R6). |
| 8 | Vídeo durante a partida para pegar skill (rara ou legend) | **Vetado.** |

**Ainda em aberto:** preço por SKU, orçamento de aquisição, gatilho de saída (seção 12); o Producer precisa reavaliar o cronograma com o SDK de vídeo; as taxas de ganho e o teto da moeda de jogo (GDD #26 e #27); o CD precisa revisar a assinatura visual dos cosméticos de moeda contra os de conquista (R2).

## 12. Dados que só o usuário pode fornecer

| Campo | Valor |
|---|---|
| Horas por semana disponíveis | 80 h por semana |
| Caixa mensal e total disponíveis | Sem teto numérico. Cada gasto é aprovado pelo usuário. Ferramentas citadas: Figma (grafado "Gigma"; confirmar), Canva, Tripo, Codex, Gemini |
| Prazo aceitável para cobrir os custos | Sem prazo |
| Teto de custo mensal do backend | Preferência: Railway Pro e Supabase Pro (planos, sem valor; o ADR de backend compara) |
| Preço por SKU de cosmético e moeda base | [A DEFINIR DEPOIS] |
| Verba para comprar arte | Ferramentas citadas (Figma, Canva, Tripo, Codex, Gemini); o usuário quer ver packs antes de decidir |
| Como receber | CNPJ |
| Países do soft launch | Brasil (grafado "Brail"), EUA e Europa ("EURO"; confirmar se é a União Europeia) |
| Orçamento de aquisição de usuários (esperado: zero; confirmar) | [A DEFINIR DEPOIS] |
| Gatilho para mudar de modelo (critério de saída da seção 5) | [A DEFINIR DEPOIS] |

## 13. Próximos passos

- [x] Responder aos pontos em aberto da seção 11 (feito em 2026-11-03)
- [ ] Fechar na seção 12: preço por SKU, orçamento de aquisição e gatilho de saída (o gatilho precisa de commit antes do soft launch)
- [x] Instalar o módulo Android Build Support no editor 6000.3.27f1 (verificado em 2026-11-03; falta o aparelho de referência)
- [ ] ADR de backend e de compras no app, antes do GDD #26 (**não existe**: `docs/architecture/` só tem `tr-registry.yaml`)
- [ ] O Producer reavalia o cronograma com o SDK de vídeo recompensado e a decisão do #15
- [ ] O creative-director revisa a distinção visual entre cosméticos de conquista, de loja e de moeda (R2)
- [ ] `/art-bible` com as regras R1, R2 e R7 como requisito
- [ ] Escrever o GDD #26 Economia e tetos com este documento como entrada, e o #27 Monetização e loja
- [ ] Definir os limiares de go/no-go e o critério de saída com commit antes do soft launch
