<!-- PROTOTYPE - NOT FOR PRODUCTION -->
<!-- Question: Skills aleatórias registradas no Grimório e seladas para sempre soam como expressão (a build é minha) ou como caça-níquel? -->
<!-- Date: 2026-11-02 -->

# Protótipo de conceito: Grimório + selamento

**Status:** concluído em 2026-11-02, com veredito **PROCEED**. Detalhes em [REPORT.md](REPORT.md).

## Hipótese
Se o jogador jogar 3 fases curtas de horda, registrar no Grimório as skills ativas ao
vencer cada chefe e depois selar 4 delas, vai sentir que a build é **dele**, e não da sorte.

**Sinais com 5 testadores:**
- Pelo menos 3 de 5 explicam em uma frase *por que* selaram aquelas 4, por intenção e não por "as mais fortes".
- Pelo menos 3 de 5 pedem para jogar de novo para registrar uma skill específica (o log registra `more_before_seal` / `new_hero`).
- No máximo 1 de 5 descreve o sorteio como injusto ou "pura sorte".

## Como rodar
Dê duplo clique em `prototype.html`. Não precisa de servidor nem de instalação.
Controles: WASD ou setas. O ataque é automático, e as escolhas são feitas com o mouse.
Botão **Log** (canto superior direito): exporta em JSON as escolhas, rerolls, favorecimentos, selo, justificativa e tempo gasto na tela de selamento.

## Protocolo de playtest
Entregue o arquivo e não explique nada: as regras aparecem na tela.
Observe em silêncio e anote onde a pessoa hesita.
Ao final, pergunte só: "O que ficou confuso?" e "Por que essas 4?" (compare com o que ela escreveu no campo).
Peça o log.

## Fora do escopo
Tank e funções, Forja, sets, raridades, esquiva e telegraph, toque, arte, som, save real e balanceamento.

## Achados
Houve 1 testador, interno. Ele declarou a hipótese CONFIRMADA.
- O sorteio pareceu justo: o reroll e o favorecer bastaram.
- O melhor momento foi a Prova do Selo com a build no máximo.
- O pior momento foi o WASD junto com o mouse.
- A justificativa do selo foi por eficácia, e não houve vontade de jogar mais.
- O Grimório enche rápido demais (11 de 12 skills em 3 fases com `MAX_SKILLS = 6`).

Veja o [REPORT.md](REPORT.md).
