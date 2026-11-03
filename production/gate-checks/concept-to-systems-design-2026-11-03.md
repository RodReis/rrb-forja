# Gate Check: Concept → Systems Design

**Date**: 2026-11-03
**Checked by**: gate-check skill
**Config**: `workflow: full`, `review_mode: full`, `qa.level: full`, `team.size: studio`
**Stage at check**: Concept (`project.yaml`, `production/stage.txt`)

## Required Artifacts: 3/3 present
- [x] `design/gdd/game-concept.md`: 55.456 bytes, conteúdo real (0 placeholders)
- [x] Pilares: 5 pilares + Princípio de Negócio + Anti-Pillars (L165-247)
- [x] Visual Identity Anchor (L251-279)

Recomendado:
- [x] `prototypes/grimorio-concept/REPORT.md`: PROCEED (CD-PLAYTEST com CONCERNS, aceito com ressalvas)

`artifact-check.sh --phase concept`: `engine-setup` PRESENT, `game-concept` PRESENT, `art-bible` ABSENT, `map-systems` ABSENT. `brainstorm` e `design-review-concept` são `NO_CHECK` (não obrigatórios; o segundo foi verificado pelo log de revisões). Nenhum dos dois ABSENT é exigido por este gate.

## Quality Checks: 4/4 passing
- [x] Conceito revisado, veredito ≠ MAJOR REVISION NEEDED: 6 passadas de `/design-review`, todas NEEDS REVISION; a 6ª teve os 4 bloqueadores de frase corrigidos e o CD encerrou o ciclo (`design/gdd/reviews/game-concept-review-log.md`)
- [x] Core loop descrito (L116-161)
- [x] Público-alvo identificado (L298-308)
- [x] VIA com regra de uma linha e 3 princípios de apoio (L259, L263-268)

## Director Panel Assessment
- **Creative Director: CONCERNS.** O NEEDS REVISION não rebaixa o gate; pilares e fantasia estáveis. Ressalvas operacionais.
- **Technical Director: CONCERNS.** Nenhum risco técnico bloqueia a entrada; condições para os GDDs.
- **Producer: CONCERNS.** Sem bloqueador; ressalvas de processo e cronograma.
- **Art Director: CONCERNS.** A VIA atende o gate, mas falta a faixa de cor do telegraph e as 5 molduras de raridade.

Panel: 4 de 4 (`workflow: full`).

## Blockers
Nenhum. Nenhuma verificação ficou sem rodar.

## Concerns
1. **Trabalho fora do git** [CD, PR]: conceito com 186 linhas alteradas desde `9f40906` e `design/gdd/reviews/` untracked. Commit antes do primeiro GDD.
2. **`Status: Draft` em L4** [CD]: contradiz o congelamento registrado no log.
3. **Art bible ausente** [AD]: rodar `/art-bible` no início de Systems Design, antes dos GDDs de combate, itens e Forja; até lá, os GDDs citam a VIA por princípio e deixam cor, forma e limite de VFX como `TBD-art-bible`.
4. **Modelo de negócio em aberto** [CD, PR, TD]: decidir F2P ou premium antes do GDD de Economia, com data logo após o `/map-systems`.
5. **Regra do Grimório mora no conceito** [CD]: o GDD do Grimório vem primeiro e é a fonte da verdade; L80, L81 e o invariante de L407 viram ponteiros quando ele for aprovado.
6. **Processo dos GDDs** [PR]: no máximo 2 passadas de `/design-review` por GDD (a 2ª só com bloqueadores; o CD encerra); timebox sugerido de 6 a 8 semanas para a fase de Systems Design, fora das faixas de 13 a 20 meses.
7. **Condições técnicas para os GDDs** [TD]: contagem de inimigos e densidade de VFX como Tuning Knobs; streams de RNG independentes (spawn, oferta, loot); o GDD de Ranking não assume validação no servidor antes do ADR de backend; o fim do suporte do 6.3 LTS (dezembro de 2027) cai perto do lançamento esperado (mês 16), então a janela de migração entra no plano de Pre-Production.
8. **Limites conhecidos** [CD]: o Pilar 3 só valida no Vertical Slice e o X do Pilar 1 é um knob sem valor; os GDDs de Ranking e de Companheiros os trazem como critérios de aceite.
9. **Ordem do spike** [PR, decisão do usuário]: o PR sugere antecipar a semana 0 e o spike em paralelo ao `/map-systems` e dividir o doc de aceite (performance agora, Grimório depois). Isso conflita com L428-430 e L456 do conceito; o TD diz que o spike pode correr em paralelo aos GDDs.

## Recommendations
- Commitar o conceito, o REPORT.md e `reviews/` antes de abrir a fase.
- Trocar `Draft` por um status de congelado em L4.
- Rodar `/map-systems` e, logo depois, `/art-bible`; começar pelo GDD do Grimório.

## Verdict: CONCERNS
Nenhum bloqueador. O estágio permanece **Concept**: com CONCERNS, o estágio só avança se o usuário aceitar os riscos explicitamente (Seção 6).

**Chain-of-Verification:** 5 questões checadas, 2 com checagem real [TOOL ACTION] (`git status` e `diff --stat`: 186 linhas fora do git; leitura de L4 e contagem de placeholders: `Status: Draft`, 0 placeholders) — veredito inalterado.
