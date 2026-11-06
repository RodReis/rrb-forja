# Change Impact: GDD #1 Dados e balanceamento

**GDD**: `design/gdd/dados-e-balanceamento.md`
**Data**: 2026-11-05
**Origem do diff**: `git diff HEAD` (alterações não commitadas; "Last Updated" 2026-11-04)
**ADRs verificados**: 3 de 3 (`adr-0001`, `adr-0002`, `adr-0003`, todos `Proposed`). Todos citam este GDD em tabela de requisitos e também em prosa.
**Revisão técnica**: TD-CHANGE-IMPACT = **CONCERNS** (aceitos pelo usuário em 2026-11-05; ver Pendências)

## Resumo da mudança

Seções alteradas:
- **Core Rules 3, 4, 5**: conversão para ticks e atribuição de índices passam a ser "no build (ADR-0002)". A Regra 5 diz que a mesma função (`DataValidator`) valida no editor, no teste EditMode e no pacote remoto, e que o carregamento do embarcado usa o `SnapshotVerifier` (estrutura e hash).
- **Regra 5, checagem "capacidades"**: a capacidade cobre a **demanda declarada**: o pico simultâneo e, para a tabela de ids do `SimWorld`, o **total de spawns da fase** (ids nunca se reutilizam; ADR-0001, #2 Regra 8 e FS9).
- **Dependências**: o #7 passa a declarar também o total de spawns.
- **"Vira ADR"**: marcado como decidido no ADR-0002, exceto persistência, escrita atômica, assinatura e expiração do pacote remoto.
- **F2 (Output Range)**: caminho decidido no ADR-0002 (dividir em `decimal`, conversão própria só com inteiros, gravar os bits do `float`).
- **F3**: renomeada para "contra a demanda declarada"; variável `pico` redefinida; novo parágrafo "Tabela de ids" (exemplo: total 900, margem 25, `cap` 1100 recusado, 1125 passa).
- **Edge Cases**: escrita atômica passa ao ADR do #29 ou do save; o pacote remoto não pode alterar contagens de horda, o pico declarado nem o total de spawns.
- **Tuning Knobs**: `capacity_margin_pct` e `capacity_ceiling` valem para a demanda declarada; a tabela de ids tem teto próprio (OQ-4).
- **Acceptance Criteria**: AC-F3 ganha o caso da tabela de ids; a tabela de ACs bloqueados cita o ADR-0002.
- **Open Questions**: OQ-2 resolvida pelo ADR-0002 (`Proposed`); OQ-5 cobre pico e total de spawns.

Sem alteração: Overview, Player Fantasy, Regras 1, 2, 7 a 10, F1 e F4 em diante, Visual/Audio.

GDDs a reconferir (registro `design/registry/entities.yaml`): `simulacao-deterministica.md` (#2), `fluxo-de-fase.md` (#3), `horda-waves-e-inimigos.md` (#7). O valor de `capacity_margin_pct` (25) não mudou.

## Análise por ADR

### ADR-0001 (simulação determinística, Core): Still Valid
- **Assumia**: "Snapshot da fase imutável, em ticks, com capacidades e hash" e, no item 6 das Decisões, que a capacidade da tabela de ids cobre o total de spawns da fase.
- **O GDD agora diz**: a F3 valida a tabela de ids contra o total de spawns; a conversão acontece no build.
- **Avaliação**: alinhado. As emendas de conversão no build já estão no ADR-0001. Único texto defasado: "o tipo do snapshot é do ADR de dados do #1" (agora é o ADR-0002).
- **Ação**: manter. Ponteiro opcional para o ADR-0002 nessa linha.

### ADR-0002 (dados e balanceamento, Foundation): Still Valid
- **Assumia**: Regra 5 com `SnapshotVerifier` no carregamento ("a ajustar no GDD"); total de spawns nunca remoto; `EntityCapacity` = total de spawns da fase.
- **O GDD agora diz**: exatamente esses refinamentos.
- **Avaliação**: o ADR já antecipava a mudança. Nada de decisão a reverter.
- **Ação**: manter. Ver Pendências P1, P3 e P4 para os ajustes de texto.

### ADR-0003 (save local, Foundation): Still Valid
- **Assumia**: o save grava só IDs, carimbo da versão e revisão da skill selada (`IDataVersion`).
- **O GDD agora diz**: contrato inalterado; só mudou onde os IDs viram índices.
- **Avaliação**: o save não consome nenhuma regra alterada (F3, redação da Regra 5, dono da escrita atômica).
- **Ação**: manter.

## Resolução

Nenhum ADR em Needs Review ou Likely Superseded. Nenhum status de ADR foi alterado.

## Pendências (concerns do technical-director, aceitos)

| ID | Pendência | Onde |
|---|---|---|
| P1 | Atualizar 4 trechos do GDD que mantêm o texto antigo: linha 385 ("mesma função de validação no editor, no teste e no carregamento", contradiz a nova Regra 5), linha 102 ("o formato exato é do ADR, OQ-2"), linha 368 (corpo do AC-F2, ainda condicional) e linha 335 (AC-15/18 aponta para "ADR (OQ-2, OQ-7)"). Só depois, anotar no ADR-0002 que o GDD foi ajustado; a nota "a ajustar no GDD" aparece em 4 lugares (Consequências, Riscos, tabela de requisitos, Related). | GDD #1, ADR-0002 |
| P2 | Contrato do total de spawns ambíguo. O GDD #1 diz que o #7 declara o total; o ADR-0001 (item 6), a FS9 do #2, o registro `capacidade_ids_ok`, o #3 e a F7 do #7 definem o total como `ids_de_preparacao` (#3) + Σ spawns (#7) + `máx_invocações` (#8). `ids_de_preparacao` é soma de código (calculada pelo compositor), enquanto o `EntityCapacity` é validado no build só sobre dados; nenhum ADR diz onde esse termo entra na checagem. Recomendação do TD: o compositor confere em runtime, antes do `Create`, que `EntityCapacity` cobre o total declarado mais `ids_de_preparacao`; se não cobrir, a fase falha com `DadosInvalidos`. Registrar uma frase no ADR-0001 ou no ADR-0002 e fazer o GDD #1 citar os três termos. **Decisão pendente do usuário** (i: dado da fase somado pelo `DataValidator`; ii: conferência em runtime). | GDD #1, ADR-0001/0002 |
| P3 | O teto da tabela de ids precisa de chave própria em `capacity_ceiling`, conferida pelo `SnapshotVerifier`. | GDD #1, ADR-0002 |
| P4 | Menores: OQ-5 está desatualizada (a F7 do #7 já calcula `total_spawns_7`); a escrita atômica do pacote remoto deve dizer "ADR do #29, podendo reaproveitar o mecanismo do ADR-0003"; o GDD #8, quando existir, deve anotar que as invocações entram no total de spawns e que o `DataValidator` recalcula a demanda sobre o conjunto resultante do pacote. | GDD #1, GDD #8 |

## Follow-up

- Nenhum ADR a escrever nem a substituir.
- Editar o GDD #1 (P1, P4) e o ADR-0002/ADR-0001 (P2, P3) exige aprovação de arquivo a arquivo (fluxo colaborativo do projeto).
- Depois das edições: `/architecture-review` para conferir a matriz de rastreabilidade.
