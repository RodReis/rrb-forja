# Change Impact: GDD #28 Save local

**GDD**: `design/gdd/save-local.md`
**Data**: 2026-11-05
**Origem do diff**: `git diff HEAD` (alterações não commitadas; 13 inserções e 12 remoções)
**ADRs verificados**: 3 de 3 (`adr-0001`, `adr-0002`, `adr-0003`, todos `Proposed`). Todos citam este GDD (ADR-0001: 3 menções; ADR-0002: 3; ADR-0003: 12).
**Revisão técnica**: TD-CHANGE-IMPACT = **CONCERNS** (aceitos pelo usuário em 2026-11-05; ver Pendências)

## Resumo da mudança

O diff aplica ao GDD as edições que o ADR-0003 pediu (linha 352 do ADR) e declara o knob que ele pediu. Não introduz decisão nova.

Seções alteradas:
- **Regras 4, 9 e tabela de estados (Corrompido, Formato mais novo)**: "CRC do cabeçalho" vira "checksum do próprio cabeçalho" (FNV-1a de 64 bits, ADR-0003), independente do checksum do corpo. Só redação; o comportamento (cabeçalho lido e verificado antes do corpo; checksum de cabeçalho inválido = Corrompido, nunca "formato mais novo") não muda.
- **Regra 7 (Commit único)**: **mudança de comportamento, não só de redação.** Antes: o commit "só conta" depois da troca. Agora: o commit passa a existir depois da troca e só é confirmado depois do `fsync` do diretório (ADR-0003). Para o #3 (`BeginStage`) e o #17 (selo), "Confirmado" passa a incluir o `fsync` do diretório. Bate com o ADR-0003 (correção (B) da revisão TD-ADR), então nenhum ADR muda por causa disso.
- **Dependências, linha do #3**: a marca também é limpa no Voltar do #3 (`CancelStage`); o #3 passa o `requestId` e o resultado volta com `RequestId` e `AttemptId` (ADR-0003). Dependência Hard.
- **"Vira ADR"**: marcado como decidido no ADR-0003 (`Proposed`, a reavaliar depois do spike no aparelho); a marca de fase rotaciona o backup como qualquer commit.
- **Tuning Knobs**: novo `SAVE_PAUSE_FLUSH_CEILING_MS` (regra 5): 150 a 250 ms provisório, máximo 500 ms, não remoto, a medir no aparelho de referência.
- **AC-06**: CRC passa a checksum. **AC-31**: bloqueado até o ADR-0003 ser aceito (adaptador `AndroidStorage` em `Forja.Gameplay`, raiz pelo JNI `getFilesDir()`; falta o spike no aparelho).
- **OQ-1**: resolvida pelo ADR-0003 (`Proposed`). **OQ-5**: `dataExtractionRules` avaliadas (Alternativa 11, provisório). **OQ-7**: CRC passa a checksum.

Sem alteração: Overview, Player Fantasy, Regras 1 a 3, 5, 6, 8, 10 a 14 (corpo), F1 a F4, regras de quarentena e retenção, demais Edge Cases.

Registro (`design/registry/entities.yaml`): as únicas entradas com `source: save-local.md` são `effective_utc` e `save_sequence`; nenhuma fórmula nem valor mudou. Nenhum knob de save (`SAVE_MAIN_THREAD_BUDGET_MS`, `SAVE_PAUSE_FLUSH_CEILING_MS`) está no registro, o que é consistente com a prática atual.

GDDs a reconferir: `fluxo-de-fase.md` (#3, consumidor Hard de `BeginStage`, `CancelStage`, `requestId` e `AttemptId`) e `business-model.md` (lê `effective_utc`; sem mudança).

## Análise por ADR

### ADR-0003 (save local, Foundation): Needs Review
- **Assumia**: linha "save-local.md, regra 6" e Key Interfaces: `BeginStage`, `CancelStage`, `ConsumeMark`; `CommitKind` com a regra de substituição "Seal > StageMark > os demais" (linha 134); `CommitResult { int RequestId; int AttemptId; ... }` (linha 138); Guideline "o pedido substituto must herdar o tipo mais forte" (linha 195); `requestId` vindo do chamador por fonte injetada (linhas 160 e 195); checksum FNV-1a 64 (`Fnv1a64`) para cabeçalho e corpo; knob `SAVE_PAUSE_FLUSH_CEILING_MS`.
- **O GDD agora diz**: checksum, knob e OQ-1 batem com o ADR (o diff fecha os "ajustes de redação pedidos"). A linha do #3 agora promete: o Voltar limpa a marca por `CancelStage`, o `requestId` vem do #3 e o resultado volta com `RequestId` e `AttemptId`.
- **Avaliação**: nenhuma decisão do ADR-0003 é contrariada pelo diff. Mas o contrato do #3, agora explícito, expõe três divergências entre o ADR e `fluxo-de-fase.md` (linha 203, linha 60, OQ-11), já presentes antes deste diff:
  - **(a) Substituição:** o `CancelStage` nunca deve gravar a marca. Pelo ADR-0003, um substituto herda o tipo mais forte e `StageMark` vence `StageCancel`, então o Voltar que substitui um `BeginStage` ainda pendente gravaria a marca que devia limpar.
  - **(b) `requestId`:** precisa ser único entre todos os chamadores (#3 e #17); o ADR deixa a fonte por conta do chamador, sem garantir unicidade.
  - **(c) `attemptId`:** os GDDs #3 e #28 (OQ-7) o definem como valor aleatório de 128 bits comparado por igualdade; o `CommitResult.AttemptId` do ADR é `int` (o tipo de `StageMark` ainda não está definido, linha 167).
- **Recomendação**: Review and update, no mesmo arquivo, antes de aceitar. Sem substituição por outro ADR.

### ADR-0001 (simulação determinística, Core): Still Valid
- **Assumia**: "save-local.md (#28): nada de estado de fase em andamento no save; abandono e app fechado não passam por tick; a simulação não serializa nem restaura fase" (linha 415).
- **Avaliação**: o diff toca só nome do checksum, knob, ACs e OQs. Não afetado.
- **Ação**: manter. Na próxima vez que alguém mexer nele, dar o tipo de 128 bits ao `attemptId` do `PhaseResult` (linha 258, hoje sem tipo).

### ADR-0002 (dados e balanceamento, Foundation): Still Valid
- **Assumia**: "o save grava só IDs, carimbo da versão e revisão da skill selada; 'ID desconhecido'" (linha 281); expõe a FNV-1a 64 pública e sem estado de que o ADR-0003 depende.
- **Avaliação**: contrato inalterado.
- **Ação**: manter. Opcional: acrescentar o nome `Fnv1a64` às Key Interfaces na próxima vez que mexer (o ADR-0003 declina emendá-lo).

## Resolução

| ADR | Status | Resolução escolhida |
|---|---|---|
| ADR-0003 | Needs Review | **Atualizar no lugar** (pequena revisão; o status do ADR **não** foi alterado nesta skill) |
| ADR-0001 | Still Valid | Manter |
| ADR-0002 | Still Valid | Manter |

## Campos a mudar no ADR-0003 (revisão no lugar, sujeita à aprovação do usuário)

Refinados pelo technical-director:

1. **(a) Substituição de pedidos**: separar o que o `CommitKind` mistura hoje.
   - Força da rotação do backup: `Seal` vence, como hoje (um `CancelStage` que substitui um `Seal` pendente ainda precisa da segunda rotação).
   - Estado da marca: vale o último pedido (a marca em vigor no envelope na hora de montar o retrato). O `CancelStage` limpa a marca do seu `attemptId`.
   - Atualizar: comentário da linha 134, regra da linha 195, caso da linha 335, tabela de pontos de queda e um novo teste EditMode "CancelStage substitui BeginStage pendente → 0 marcas" (espelho do I3a do #3).
2. **(b) `requestId`**: fonte única, compartilhada e injetada entre #3 e #17 (não o #28 emitindo o id), para manter as assinaturas `BeginStage(int requestId, …)` e os testes do #3.
3. **(c) `attemptId`**: tipo único de 128 bits em `CommitResult`, `StageMark`, `MarkAnswer` e no campo TLV da marca. O valor vem de fonte injetada, nunca de `System.Random` nem `Guid.NewGuid()` dentro do código determinístico (teste H4 do #3).
4. Registrar no ADR que os ajustes de redação pedidos ao GDD #28 (linha 352) foram feitos.

## Pendências (concerns do technical-director, aceitos)

| ID | Pendência | Onde |
|---|---|---|
| Q1 | Revisão no lugar do ADR-0003 conforme a seção acima (a, b, c e nota da linha 352). | ADR-0003 |
| Q2 | Ressincronizar `signal_signature` do `ISaveService` (tipo do `AttemptId`, regra de substituição, origem do `requestId`) e incluir `design/gdd/fluxo-de-fase.md` no `referenced_by`, que hoje só tem o ADR-0003 e o `save-local.md`. | `docs/registry/architecture.yaml` (linha ~257) |
| Q3 | Trocar as referências velhas ao "ADR da OQ-1" por ADR-0003 no GDD #28: regra 7 (2 ocorrências, linha 43) e também linhas 40, 162, 218, 246, 261 e 309. | `design/gdd/save-local.md` |
| Q4 | Alinhar o `attemptId` do `PhaseResult` (128 bits) na próxima edição do ADR-0001; acrescentar `Fnv1a64` às Key Interfaces do ADR-0002 na próxima edição dele. | ADR-0001, ADR-0002 |

Observação: `docs/architecture/requirements-traceability.md` não existe, então a Fase 8 (índice de rastreabilidade) não se aplica.

## Follow-up

- Nenhum ADR marcado Superseded; nenhum ADR novo a escrever.
- Cada edição acima (Q1 a Q4) exige aprovação de arquivo a arquivo (fluxo colaborativo do projeto).
- Depois das edições: `/architecture-review` para conferir a matriz de rastreabilidade.
