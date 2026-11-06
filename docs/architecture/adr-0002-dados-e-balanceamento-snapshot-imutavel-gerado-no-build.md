# ADR-0002: Dados e balanceamento (#1): autoria em texto, validação em C# puro, snapshot imutável gerado no build com os bits do float, hash de conteúdo FNV-1a e revisão por skill

## Status
Proposed

## Date
2026-11-05

## Last Verified
2026-11-05 (contra Unity 6.3 LTS, pin 6000.3.x; `design/gdd/dados-e-balanceamento.md` (#1), `simulacao-deterministica.md` (#2), `fluxo-de-fase.md` (#3), `save-local.md` (#28) e o ADR-0001 emendado)

## Decision Makers
Rodrigo Reis (premissas e a resolução do conflito de conversão de taxas confirmadas em 2026-11-05), Claude Code (autoria), `unity-specialist` (validação de API, 5.5) e `technical-director` (gate TD-ADR, 5.6). Os resultados das duas revisões entram na seção Risks antes de gravar.

## Summary
O #1 Dados e balanceamento precisa de uma decisão técnica sobre onde moram os números de gameplay, quem os valida, como o tempo vira ticks e como o jogo identifica a versão dos dados, antes dos GDDs #6, #7, #8, #10, #16, #17 e #26 declararem os knobs deles. Decidido: autoria em texto (JSON, com os números escritos como texto) no repositório; uma validação em C# puro; um passo de build que lê os números em `decimal`, valida, converte **uma vez** e grava os bits do `float` e os ticks inteiros num **snapshot binário imutável**; carga síncrona do snapshot embarcado, sem Addressables; hash de conteúdo FNV-1a de 64 bits; revisão por skill com classificação autoral obrigatória. O pacote remoto do pós-lançamento fica só como contrato aqui, e transporte, assinatura e persistência ficam para o ADR do #29.

## Engine Compatibility

| Field | Value |
|-------|-------|
| **Engine** | Unity 6.3 LTS (6000.3.x; editor instalado 6000.3.27f1) |
| **Domain** | Core |
| **Layer** | Foundation |
| **Knowledge Risk** | HIGH (`docs/engine-reference/unity/VERSION.md`) |
| **References Consulted** | `docs/engine-reference/unity/VERSION.md`, `breaking-changes.md` (Addressables, 6.2+: falha de carga lança exceção), `deprecated-apis.md` (`Resources.Load()` e carga síncrona), `current-best-practices.md`; `design/gdd/dados-e-balanceamento.md` (Core Rules 1 a 10, Formulas F1 a F6, Edge Cases, AC-F1, AC-F2, AC-I3, AC-P1); ADR-0001 e `docs/registry/architecture.yaml`. **Não existe `docs/engine-reference/unity/modules/core.md`**: nada deste ADR foi checado contra um módulo de referência (`NOT SOURCEABLE`) |
| **Post-Cutoff APIs Used** | Nenhuma API da Unity dentro dos dados, do validador e do verificador (asmdef sem engine). Só a camada com Unity (carregador) toca a engine, para ler bytes embarcados no player; essa leitura (como o Unity empacota e carrega um asset de bytes) é `NOT SOURCEABLE` em `docs/engine-reference/unity/` e fica para o spike. `System.Decimal`, `BitConverter` e `System.Globalization` são BCL anteriores ao cutoff; a disponibilidade e o comportamento deles no perfil de API do projeto são `NOT SOURCEABLE`. |
| **Verification Required** | (1) O snapshot gerado no editor é lido com os mesmos bits no Mono do Editor e no IL2CPP ARM64 do aparelho (o hash recomputado no boot é igual ao campo do cabeçalho do arquivo). (2) `System.Decimal` (inclusive `decimal.GetBits`) no editor faz a conta de F1 e F2 como o GDD espera (AC-F1 e AC-F2), e a rotina própria de conversão dá os mesmos bits em duas execuções e em duas máquinas do editor, conferida contra o `(float)decimal`. (3) Como o Unity empacota e carrega o asset de bytes do snapshot (síncrono, sem Addressables) e o custo dessa carga fria e quente contra os tetos do #1 (`phase_load_ceiling_*`); `NOT SOURCEABLE`. Um spike curto cobre este item: um build Android de teste com o `.bytes`, o hash conferido na carga e o pré-build falhando. (4) O passo de pré-build do editor consegue **falhar o build** quando a validação ou o bake falham (a API esperada é `IPreprocessBuildWithReport` com `BuildFailedException`; `NOT SOURCEABLE`). (5) O asmdef `Forja.Data` aceita "No Engine References" e o asmdef de editor referencia só ele; o stripping do IL2CPP não remove nada, porque a leitura é por offsets, sem reflexão (`NOT SOURCEABLE`). (6) `BitConverter.SingleToInt32Bits` e `Int32BitsToSingle` existem nos dois runtimes (o mesmo item 6 do ADR-0001). (7) Se o pacote remoto validar `decimal` no aparelho (pós-lançamento), `System.Decimal` dá os mesmos resultados no Mono do Editor, no IL2CPP ARM64 e no servidor; é pré-requisito do ADR do #29. (8) Memória do snapshot e tempo de carga no aparelho de referência, que ainda não foi verificado (spike de performance, AC-P1). |

## ADR Dependencies

| Field | Value |
|-------|-------|
| **Depends On** | ADR-0001 (`Proposed`, deve estar `Accepted` antes deste): float32, 30 Hz, `IPhaseSnapshot` e `Simulation.Create`, os três asmdefs e a regra de que a conversão de dados fica fora do asmdef da simulação. A varredura é conclusiva: é o único outro ADR. |
| **Enables** | GDDs #6, #7, #8, #10, #16, #17, #18 e #26 (declaram knobs e definições no #1); o ADR do save (#28: carimbo de versão e revisão da skill selada); o ADR do #29 (contrato do pacote remoto); o cabeçalho de log do #5. |
| **Blocks** | Épicos do #1 e qualquer story que carregue dados de fase. Nenhuma story existe ainda, então nenhuma está `Blocked` hoje. |
| **Ordering Note** | **Emenda ao ADR-0001** (feita junto com a gravação deste ADR): (a) a seção **Tempo**, que manda converter "no carregamento da fase" e multiplicar as taxas por `SimClock.TickSeconds`, passa a dizer que a conversão acontece **uma vez, no build** (`Forja.Data`), com a taxa dividida em `decimal` e convertida pela rotina própria; (b) a seção **Interface** e a Guideline que citam a "conversão de `ScriptableObject` em structs de fase" passam a citar o snapshot gerado no build e a carga fora do asmdef da simulação; (c) o registro `sim_time` é reescrito; (d) a tabela Emendas do ADR-0001 ganha a linha 23, com origem neste ADR. A emenda entra no texto do ADR-0001 antes de ele ser aceito, e o ADR-0002 nunca é aceito antes dele. Aceito, este ADR desbloqueia AC-F1, AC-F2 e AC-I3 (parte EM) do GDD #1. |

## Context

### Problem Statement
O GDD #1 exige que todo valor de gameplay seja dado externo, validado "tudo ou nada", convertido para ticks uma única vez, entregue à fase como um conjunto imutável e identificado por um hash e um rótulo de versão. A seção "Vira ADR" do GDD #1 lista as decisões que ficaram para este ADR (OQ-2): formato de autoria, hash canônico e ordem de serialização, onde roda a validação, layout dos structs de fase, cálculo da revisão por skill, e a persistência do pacote remoto. O ADR-0001 deixou uma contradição aberta: a conversão de taxas por segundo em taxas por tick (multiplicar por `TickSeconds`, ou dividir em `decimal`), que dá bits diferentes. Os GDDs #6, #7 e #8 vão escrever fórmulas em cima disso, então a decisão precisa vir agora.

### Constraints
- Dev solo; o custo de ferramenta e de depuração pesa mais que a elegância.
- O resultado da conversão tem de ser **idêntico bit a bit** em todas as plataformas (Editor, Windows, Android IL2CPP ARM64); o `decimal` autoral nunca pode virar `float` antes da validação (GDD #1, regra transversal).
- Nenhuma leitura de arquivo, conversão ou sobrescrita durante a fase; os dados da fase ficam imutáveis até o fim da partida (GDD #1, Core Rule 7).
- Falha de carga ou de validação bloqueia a entrada na fase e **nunca** cai em valor padrão.
- A simulação roda sem engine (ADR-0001): o carregador com Unity fica fora dela.
- Android primeiro, aparelho de referência ainda não verificado: os tetos de carga (3000 ms a frio e 1500 ms a quente) são provisórios.
- Referência de engine para este domínio: só Addressables e `Resources` aparecem; o resto é `NOT SOURCEABLE`.

### Requirements
- Uma única função de validação, a mesma no editor, no teste EditMode e (para pacotes) no aparelho.
- A conversão `decimal` para `float` acontece uma vez e não é refeita em runtime nos dados embarcados.
- O jogo e a simulação headless leem exatamente o mesmo snapshot.
- IDs estáveis, nunca reutilizados nem removidos; hash de conteúdo e rótulo legível por conjunto; revisão por skill com classificação autoral.
- O #1 nunca depende de rede; o pacote remoto entra por um provedor injetado pelo #29.

## Decision

### Visão geral
```
 Autoria (texto)        Validador (C# puro)      Baker (build)            Snapshot imutável        Jogo
 Assets/GameData/*.json ──▶ decimal, faixas,  ──▶ converte 1 vez,    ──▶ bytes: ticks inteiros  ──▶ carga síncrona no boot
 (números como texto)       IDs, referências      grava bits do float     e bits do float, ordem      Verifier (hash, estrutura)
                            revisão/classif.      e o hash FNV-1a 64      canônica, hash              PhaseSnapshot : IPhaseSnapshot
                                                                                                       Simulation.Create(...)
```

### 1. Autoria em texto (JSON), números como texto
Os dados vivem em arquivos JSON no repositório (`Assets/GameData/`, caminho provisório), com diff legível no git. **Todo número autoral é escrito como texto** (`"cooldown_s": "0.15"`), em cultura invariante (ponto decimal; vírgula, `NaN`, infinito e valor acima de `float.MaxValue` são recusados). Assim nenhum parser de `float` ou `double` toca o valor autoral: o validador lê o texto direto para `decimal`. `ScriptableObject` e números JSON puros ficam fora da autoria porque os dois passariam o valor por `float` ou `double` antes da validação. O texto é lido só no editor (validador e baker); o jogador nunca lê JSON. Dentro de `Forja.Data` (sem engine) o JSON é lido por um **tokenizador próprio e pequeno**, porque `JsonUtility` é da engine e uma biblioteca de terceiros (como Newtonsoft) exigiria um pacote e o aval do `technical-director`; como todo número é texto, o tokenizador só precisa de objetos, arrays e strings. Todo `Parse` e `ToString` (valores, livros-razão, mensagens, texto de hash) **usa `CultureInfo.InvariantCulture`** explícito, e o `decimal` é lido com `NumberStyles.AllowLeadingSign | NumberStyles.AllowDecimalPoint` (sem expoente), porque o Windows em pt-BR tem a vírgula como cultura padrão.

### 2. Validação em C# puro, em dois níveis
- **`DataValidator`** (`Forja.Data`, asmdef sem engine): as seis checagens do GDD #1 (tipo e unidade, faixa segura e pior valor, referências cruzadas e checagens de setup, regra do tick, capacidades contra a demanda declarada (para a tabela de ids, a parte de dados: `SpawnsDeDados`; o termo de código `ids_de_preparacao` o compositor soma antes do `Create`, ADR-0001, item 6), IDs), mais a revisão por skill. Trabalha em `decimal`, compara a faixa com o **valor autoral** (nunca com o `float` convertido), é tudo ou nada e **recusa, nunca ajusta**. Roda no passo de build, nos testes EditMode e, no pós-lançamento, na validação do pacote remoto.
- **`SnapshotVerifier`** (`Forja.Data`): roda **no carregamento do embarcado**, no domínio de inteiros e bits: no boot, o cabeçalho, o diretório e o catálogo global (e o hash do arquivo inteiro, uma vez); em cada fase, **só a seção dela** (versão do formato, contagens, IDs únicos e em ordem, capacidades contra os tetos por tipo (lista de vivos, tabela de ids, eventos e pools, cada um com a sua chave de `capacity_ceiling`), em inteiro de 64 bits, NaN e infinito recusados e o FNV-1a da seção igual ao do diretório). Falha no catálogo bloqueia todas as fases; falha numa seção bloqueia só aquela fase (GDD #1, Edge Cases). O verificador **detecta corrupção e identifica a versão**; a prova de que o snapshot é o que o validador aprovou é o pré-build (seção 9), que refaz o bake e compara o hash. *(Provisória: o GDD #1, Core Rule 5, diz "mesma função no editor, no teste e no carregamento"; este ADR refina para "mesma função no editor, no teste e na validação de pacote; hash e estrutura no carregamento do embarcado", e o GDD foi ajustado em 2026-11-05.)*

### 3. Conversão uma única vez, no build
O baker (`Forja.Data`, chamado pelo passo de build do editor) converte em `decimal` e grava o resultado:
- **Duração:** `duracao_ticks = floor(s × 30 + 0,5)` (o meio arredonda **para cima**: `floor(x + 0,5)` já é essa regra, então não se usa `MidpointRounding` em paralelo); recusa-se o conjunto se o resultado for menor que 1 (nunca é ajustado). Campos `_ticks` não passam por conversão.
- **Taxa por segundo:** `taxa_por_tick = DecimalParaFloat(r ÷ 30)`, com a divisão feita **em `decimal`** e **uma única** conversão para `float` por uma **rotina própria, só com inteiros** (`Forja.Data`): ela extrai o sinal, o expoente e a mantissa do `decimal` (por `decimal.GetBits`) e arredonda ao `float` de 32 bits **ao par mais próximo**, sem passar por `double` nem pelo `(float)decimal` da BCL, de modo que atualizar o editor (por exemplo para um runtime CoreCLR) nunca muda os bits, as revisões nem o hash *(provisória)*. Os vetores de AC-F1 e AC-F2 e um teste com hash dourado fixam os bits; a rotina é conferida contra o `(float)decimal` do editor numa bateria de valores, e a diferença, se houver, é registrada. Este é o caminho único que o GDD #1 pedia: ele **substitui** o "multiplicar por `SimClock.TickSeconds`" do ADR-0001 (emenda feita junto com este ADR). Os bits do `float` são gravados com `BitConverter.SingleToInt32Bits`.
- **Valor `int`:** gravado como `int` de 32 bits; `float` de gameplay, como seus 32 bits.
Em runtime **nada** é convertido nos dados embarcados: a simulação só lê ticks inteiros e bits.

### 4. Snapshot binário imutável
Um arquivo binário gerado no build, em ordem canônica e `little-endian` explícita, sem preenchimento: cabeçalho (magic, versão do formato, `TICKS_PER_S` = 30), diretório de seções (id, offset, tamanho) e as seções, cada uma um array plano de structs somente leitura (inteiros e bits de `float`). Há um **catálogo global pequeno** (raridades, tetos, pesos), carregado no boot, e **uma seção por fase** com as capacidades, o `SpawnsDeDados`, as waves como listas ordenadas por índice de wave e os dados que cada GDD declara. **O layout de cada seção é do GDD dono** (#3, #6, #7, #8, #10, #16, #17, #26); este ADR fixa só o contêiner, a ordem, a leitura por offsets (sem reflexão) e o que o `IPhaseSnapshot` expõe (as capacidades de entidades, de vivos e de eventos, e o `ContentHash`). Os objetos de leitura (`PhaseSnapshot`) são imutáveis: **no carregamento o snapshot é decodificado uma vez** para `int[]` e `float[]` privados com `BinaryPrimitives.ReadInt32LittleEndian` e `BitConverter.Int32BitsToSingle` (sem `MemoryMarshal.Cast`, que dependeria do endianness do hospedeiro, e sem `unsafe`); só `ReadOnlySpan` desses arrays é exposto, e o verificador recusa NaN e infinito nas seções. O **diretório de seções leva o FNV-1a de 64 bits de cada seção**, e o cabeçalho leva o hash do arquivo inteiro (a identidade da versão), calculado sobre os bytes que vêm depois do campo do hash (nenhum `.cs` é gerado, o que causaria recompilação). Há um arquivo só, com o catálogo global e uma seção por fase.

### 5. IDs e índices
Todo knob e toda definição têm ID estável em `snake_case`. Cada ID vira um **índice inteiro pela ordem ordinal dos IDs** (comparação ordinal, sem cultura: `StringComparer.Ordinal` em todo `Sort` e `CompareTo` de IDs, porque o `Sort()` padrão de strings usa a cultura), nunca pela ordem de iteração de um dicionário. Um livro-razão de IDs (`ids.ledger.json`, versionado) guarda o tipo de cada ID já publicado: o baker falha se um ID sumiu, mudou de tipo ou foi reutilizado; uma definição aposentada vira `deprecated` e continua resolvendo para saves (#28) e logs (#5). Uma tabela de IDs (nome para índice) existe no snapshot **só para uso fora do tick** (save, log, ferramentas).

### 6. Hash de conteúdo e rótulo
O hash de conteúdo é **FNV-1a de 64 bits sobre os bytes canônicos do snapshot, menos o campo do hash no cabeçalho** (o mesmo algoritmo, por byte, do hash do estado da simulação), sem timestamp nem tag de build. O **rótulo legível** é `<rotulo_dos_dados>-<8 primeiros hex do hash>`. A **versão efetiva** de uma partida é o FNV-1a de 64 bits sobre os bytes de (hash do embarcado ‖ hash do pacote aplicado); **sem pacote, é o hash do embarcado** (o MVP não muda). É o que vai no cabeçalho do log (#5) e no `logHeaderDataHash` do `Simulation.Create`, e o `PhaseSnapshot.ContentHash` é esse mesmo valor. Com um pacote, a conversão para `float` acontece no aparelho, entre partidas *(provisória)*. O hash serve para **identidade e detecção de corrupção**, não para segurança: assinatura e integridade do pacote remoto são do ADR do #29. *(Provisória.)*

### 7. Revisão por skill
A revisão de uma skill muda quando muda qualquer coisa que altere o comportamento dela (a definição, tudo que ela referencia, as fórmulas compartilhadas e os knobs globais que ela usa). A revisão é o **hash do fecho de dependências** da skill (sobre uma forma canônica **sem índices**: as referências entram pelo **ID em texto** e os valores pelos **bits**, de modo que inserir uma definição no meio da ordem nunca muda a revisão de quem não mudou) mais um **contador sequencial por skill**, guardados num livro-razão versionado (`revisions.ledger.json`). Quando o fecho muda, o baker **exige uma classificação autoral** (`nerf`, `buff`, `correcao` ou `neutra`, com data) num arquivo de mudanças versionado, por par (mudança, skill afetada), e falha sem ela. `neutra` só vale se nenhum bit de gameplay do fecho mudou; uma mudança mista exige `nerf` ou `buff`. O histórico de passos (classificação e data) vai **dentro do snapshot**, e o #1 só expõe fatos sobre ele (`IDataVersion`). Quem decide a reforja grátis é o #18. *(Provisória.)*

### 8. Carga
O snapshot é **embarcado no player** como um arquivo `.bytes` (importado como `TextAsset`, bytes crus; a mecânica de importação e de empacotamento é `NOT SOURCEABLE`) referenciado por um campo `[SerializeField]` de um componente de boot, e lido de forma **síncrona**: o catálogo global no boot e os dados de cada fase antes do tick 0, fora do `Tick`. **Sem Addressables** para o conjunto embarcado (o risco do 6.2 de falha de carga que lança exceção não se aplica, e não há o que baixar) e **sem `Resources`** (diretriz do projeto em `deprecated-apis.md`). Um `TextAsset` referenciado por `[SerializeField]` sobe junto com a cena e não é `Resources.Load`; o que se usa é a leitura síncrona dos bytes dele, antes do tick 0, e o `deprecated-apis.md` desencoraja a carga síncrona de assets em geral (ver a Alternative 4). O `SnapshotVerifier` roda no boot (cabeçalho, diretório e catálogo) e, em cada fase, só na seção dela; uma falha bloqueia a fase (catálogo global inválido bloqueia todas as fases) e **nunca** usa valor padrão. A carga acontece na tela de carregamento e respeita os tetos do #1. O carregador copia os bytes para um `byte[]` e passa o span ao asmdef sem engine; enquanto o componente de boot guardar a referência ao `TextAsset`, o asset fica na memória, e o custo disso é do item 8 de Verification Required. O baker **sobrescreve o arquivo no lugar** (nunca apaga e recria: o GUID mudaria e a referência do componente de boot quebraria) e **só grava se os bytes mudaram**; o `.gitattributes` leva `*.bytes -text`, para o git nunca converter fim de linha no binário.

### 9. Integração com o editor e o build
`Forja.Data` ("No Engine References", "Auto Referenced" desligado: modelo, tokenizador, validador, verificador, baker, FNV-1a, livros-razão), `Forja.Data.Editor` (só editor: menu manual de validar e gerar, e o passo de pré-build), um asmdef de testes próprio (só editor; referencia os dois anteriores; `UNITY_INCLUDE_TESTS`) em `Assets/Tests/EditMode/Data/` e o carregador na camada `Forja.Gameplay` (com Unity). **O snapshot fica versionado (commitado) num caminho fixo.** O passo de pré-build (`IPreprocessBuildWithReport`, que falha o build lançando `BuildFailedException`; a API é `NOT SOURCEABLE`) **revalida, refaz o bake em memória e compara o hash com o do arquivo versionado**, e falha o build se divergir ou se o conjunto for inválido; ele **nunca grava** o snapshot durante o build (o asset poderia não ser importado a tempo). A regeneração é só pelo menu manual: **sem `AssetPostprocessor`** (evita laço de reimport) e **sem gravar em Play Mode**. O conjunto embarcado inválido não gera build (GDD #1, Edge Cases). Os mesmos fixtures de teste alimentam o validador e o baker. **Grafo de referências:** `Forja.Data` → `Forja.Simulation` (só para implementar `IPhaseSnapshot`); `Forja.Gameplay.Sim` → `Forja.Data`; `Forja.Data.Editor` → `Forja.Data`; `Forja.Simulation` **nunca** referencia `Forja.Data`.

### 10. Pacote remoto (pós-lançamento): só o contrato
Este ADR fixa o que o GDD #1 já decide e deixa o resto: o pacote é **atômico**, só toca a **lista branca** com valores na faixa segura, passa pela **mesma validação** do conjunto resultante, **não carrega campo de segmentação**, só vale **entre partidas, no hub e sem ritual de selo ou de registro aberto**, tem a **base** igual ao hash do embarcado e a **maior sequência de publicação** vence. Um provedor injetado pelo #29 (`IDataOverrideProvider`) entrega o pacote bruto; o #1 valida e decide, e nunca espera a rede. **Fica para o ADR do #29 (e para o ADR do save, no que reaproveitarem o mecanismo de arquivo):** transporte, cache, assinatura, expiração, a persistência atômica da última sobrescrita válida, o formato numérico do pacote (validar `decimal` no aparelho exige o item 7 de Verification Required) e o uso de Addressables. **Também fica para o ADR do #29 (ou do save) a persistência do histórico de revisão deste aparelho**: os passos de pacote aplicado, trocado, removido, expirado ou descartado por base nova dependem do que este aparelho viu e são estado persistido fora do snapshot; depois do lançamento, `History` junta os passos autorais do snapshot e o registro do aparelho. O MVP não é afetado.

### Key Interfaces
```csharp
namespace Forja.Data   // asmdef sem engine
{
    /// <summary>Implementa o IPhaseSnapshot do Core (ADR-0001): imutável; o Core só lê capacidades e hash.</summary>
    public sealed class PhaseSnapshot : Forja.Simulation.IPhaseSnapshot
    {
        public int EntityCapacity { get; }      // capacidade da tabela de ids; cobre o total de spawns da fase = ids_de_preparacao (código, #3) + SpawnsDeDados (GDD #2, FS9)
        public int SpawnsDeDados { get; }       // spawns das waves (#7) + máx_invocações (#8); o compositor soma ids_de_preparacao e confere EntityCapacity (ADR-0001, item 6)
        public int CapacityMarginPct { get; }   // do catálogo global (capacity_margin_pct, não remoto)
        public int AliveCapacity { get; }
        public int EventCapacity { get; }
        public ulong ContentHash { get; }    // FNV-1a 64 do snapshot efetivo (embarcado + pacote, se houver)
        public ReadOnlySpan<int> SectionInts(int sectionId);        // sobre int[] privado decodificado uma vez (little-endian); sem reflexão
        public ReadOnlySpan<float> SectionFloats(int sectionId);    // sobre float[] privado decodificado uma vez
    }

    public static class DataValidator   // decimal; editor, testes e pacote remoto
    {
        public static ValidationResult Validate(in AuthoringSet set, in PreviousLedgers previous);   // tudo ou nada; lista de erros
    }

    public static class DecimalConversion   // rotina própria, só inteiros
    {
        public static int ToFloatBits(decimal value);   // arredonda ao float de 32 bits ao par mais próximo; sem double nem (float)decimal
    }

    public static class Baker           // editor/build: converte uma vez e grava os bits
    {
        public static byte[] Bake(in AuthoringSet validated, out ulong contentHash, out string label);
    }

    public static class SnapshotVerifier   // carregamento: estrutura e hash, em inteiros e bits
    {
        public static VerifyResult VerifyBoot(ReadOnlySpan<byte> snapshot);                // cabeçalho, diretório, catálogo; hash do arquivo contra o campo do cabeçalho
        public static VerifyResult VerifySection(ReadOnlySpan<byte> snapshot, int sectionId);   // só a seção da fase; FNV-1a contra o diretório
    }

    public readonly struct RevisionStep { public readonly int Revision; public readonly RevisionClass Class; public readonly long PublishedUtc; }
    public enum RevisionClass { Nerf = 0, Buff = 1, Correcao = 2, Neutra = 3 }   // valores explícitos: vão para o snapshot e o log

    public interface IDataVersion          // só fatos; a regra de reforja é do #18
    {
        ulong Hash { get; }
        string Label { get; }
        int Revision(int skillIndex);
        ReadOnlySpan<RevisionStep> History(int skillIndex);   // MVP: passos autorais do snapshot; depois do lançamento, também o registro do aparelho
    }

    public interface IDataOverrideProvider   // injetado pelo #29; o #1 nunca espera rede
    {
        bool TryGetPending(out ReadOnlyMemory<byte> rawPackage);
    }
}
```
Os nomes e as assinaturas são o contrato do ADR; os campos de cada seção pertencem aos GDDs donos, e `AuthoringSet`, `PreviousLedgers`, `ValidationResult` e `VerifyResult` são definidos na primeira story do #1.

### Implementation Guidelines
- Todo valor de gameplay **must** vir de dado externo; **must never** haver literal de gameplay no código (`.claude/docs/coding-standards.md`).
- Os números autorais **must** ser escritos como texto e lidos para `decimal` em cultura invariante; **must never** passar por `float`, `double`, `JsonUtility` ou `System.Text.Json` com número JSON puro antes da validação.
- A faixa **must** ser comparada em `decimal` contra o valor autoral; **must never** comparar contra o `float` convertido nem usar `clamp`: valor fora da faixa **must** recusar o conjunto inteiro.
- A conversão `decimal` para `float` **must** acontecer uma única vez, no baker, pela rotina própria só com inteiros (**must never** usar `(float)decimal`, `Convert.ToSingle` nem `double`); **must never** haver conversão, parse de texto ou leitura de arquivo de dados durante a fase, nem parse de `float` em runtime nos dados embarcados.
- Duração **must** usar `floor(s × 30 + 0,5)` (sem `MidpointRounding` em paralelo) e **must** recusar o resultado menor que 1; taxa **must** usar `DecimalParaFloat(r ÷ 30)` com a divisão em `decimal`; todo `Parse` e `ToString` **must** usar `CultureInfo.InvariantCulture`, e o `decimal` **must** ser lido com `NumberStyles.AllowLeadingSign | NumberStyles.AllowDecimalPoint`.
- O snapshot **must** ser serializado em ordem canônica, `little-endian` explícito, campo a campo; **must never** hashear memória bruta de struct, `GetHashCode` de objeto nem a ordem de iteração de um `Dictionary`.
- Cada ID **must** virar índice pela ordem ordinal dos IDs (`StringComparer.Ordinal` em todo `Sort` e `CompareTo`); **must never** reutilizar nem remover um ID publicado (o baker compara com o livro-razão).
- O snapshot **must** ser imutável depois de carregado: arrays privados, acesso por `ReadOnlySpan`; **must never** expor um array mutável nem escrever no #1 em runtime.
- `Forja.Data` **must** ter "No Engine References", "Auto Referenced" desligado e **must never** exigir `unsafe`, `static` mutável, `static event` nem reflexão; o carregador com Unity **must** ficar fora dele, e a proibição de `static` mutável vale também para o carregador em `Forja.Gameplay` e para os caches do menu do editor.
- O carregamento **must** rodar o `SnapshotVerifier` e **must never** cair em valor padrão: falha bloqueia a fase.
- O conjunto embarcado **must** ser lido de forma síncrona e **must never** passar por Addressables nem `Resources`.
- Mudar o fecho de dependências de uma skill **must** exigir uma classificação autoral (`nerf`, `buff`, `correcao` ou `neutra`); `neutra` **must never** valer se algum bit de gameplay do fecho mudou.
- O passo de pré-build **must** revalidar, refazer o bake em memória e comparar o hash com o snapshot versionado, e **must** falhar o build quando divergir ou quando a validação falhar; **must never** gravar o snapshot durante o build nem gerar build com conjunto inválido. O baker **must** sobrescrever o arquivo no lugar (nunca apagar e recriar, por causa do GUID) e só gravar se os bytes mudaram; **must never** regenerar por `AssetPostprocessor` nem gravar em Play Mode.
- O `PhaseSnapshot` **must** expor `SpawnsDeDados` e `CapacityMarginPct`; o `DataValidator` **must** conferir `SpawnsDeDados × (100 + margem) ≤ EntityCapacity × 100` e **must never** somar `ids_de_preparacao`, que é código e é conferido pelo compositor (ADR-0001, item 6); o `SnapshotVerifier` **must** conferir os mesmos limites em inteiro de 64 bits.
- Knob com `aceite: sim` **must never** ser `remoto: sim`; contagens de horda, pico, total de spawns, tetos da economia, capacidades e constantes de tick **must never** ser remotos.
- Testes ficam em `Assets/Tests/EditMode/Data/`, com asmdef de testes próprio, e usam fixtures por arquivo constante ou fábrica, sem número solto; os vetores de AC-F1 e AC-F2 **must** sair do editor real, e um teste com hash dourado **must** fixar os bits do snapshot (o runtime do editor pode mudar).
- O JSON **must** ser lido por um tokenizador próprio em `Forja.Data` (objetos, arrays e strings); **must never** usar `JsonUtility` nem um pacote de terceiros sem o aval do `technical-director`.
- O `.gitattributes` **must** ter `*.bytes -text`; o `SnapshotVerifier` **must** recusar NaN e infinito nas seções.
- No Play Mode do editor, uma checagem só de editor **must** comparar o bake em memória com o snapshot versionado e avisar ou bloquear; **must never** gravar. O `.bytes` e os livros-razão **must never** ser resolvidos por merge: **must** ser regenerados pelo menu.

## Alternatives Considered

### Alternative 1: Autoria em `ScriptableObject`
- **Description**: Os dados em `ScriptableObject` editados no Inspector, convertidos em structs de fase no carregamento.
- **Pros**: Fluxo nativo do Unity; referências por objeto; edição visual.
- **Cons**: O Unity serializa `float` ou `double`: o valor autoral perde o texto antes de qualquer validação (o GDD #1 proíbe isso); o diff no git é opaco; a conversão e a validação ficariam presas ao editor ou ao runtime.
- **Rejection Reason**: Conflita com a regra do GDD #1 de nunca gravar o valor autoral como `float`. Se a ergonomia do Inspector pesar depois, um editor customizado pode editar o JSON.

### Alternative 2: JSON com números JSON puros e parser da engine
- **Description**: Os mesmos arquivos, mas com números sem aspas, lidos por `JsonUtility` ou por uma biblioteca JSON.
- **Pros**: Mais natural de escrever e de ler.
- **Cons**: O parser entrega `float` ou `double` antes da validação; o resultado de parse de `float` entre Mono e IL2CPP é `NOT SOURCEABLE`; seria preciso um tokenizador que preservasse o texto do número.
- **Rejection Reason**: Os números como texto dispensam esse cuidado no formato: qualquer tokenizador serve, porque nenhum número passa por parser numérico. O tokenizador próprio e pequeno (objetos, arrays e strings) é necessário de qualquer jeito dentro de `Forja.Data`, sem engine. Números JSON puros ficam como saída se a autoria como texto atrapalhar o dia a dia, com um tokenizador que preserve o texto do número.

### Alternative 3: Converter e validar em runtime, no carregamento
- **Description**: Embarcar o texto e rodar o validador e a conversão em `decimal` no aparelho, a cada carga.
- **Pros**: Uma só função em todo lugar (a redação literal do GDD #1, Core Rule 5); nenhum passo de build separado.
- **Cons**: A conversão `decimal` para `float` (e `System.Decimal`) entre Mono, IL2CPP ARM64 e o editor é `NOT SOURCEABLE`; custo de CPU e de GC no carregamento; um valor autoral errado só apareceria no aparelho.
- **Rejection Reason**: A conversão uma única vez no build tira a divergência entre runtimes dos dados embarcados. Escolhida a conversão no build, com verificação por hash na carga.

### Alternative 4: Addressables para o conjunto embarcado
- **Description**: Servir o catálogo e as fases como assets Addressables.
- **Pros**: A recomendação do projeto para carga assíncrona; prepara o terreno para o pacote remoto.
- **Cons**: Falha de carga lança exceção a partir do 6.2 (risco MEDIUM, `breaking-changes.md`); carga assíncrona de dados que precisam estar prontos antes do tick 0; dependência do catálogo de Addressables para dados que nunca mudam entre partidas.
- **Rejection Reason**: Os dados embarcados são pequenos e imutáveis, e a carga síncrona de bytes embarcados evita o risco. Addressables continua em aberto para o pacote remoto (ADR do #29). O `deprecated-apis.md` desencoraja a carga síncrona de assets: este ADR lê **de forma síncrona** os bytes de um blob pequeno, embarcado e necessário antes do tick 0, sem `Resources.Load` e sem Addressables.

### Alternative 5: SHA-256 como hash de conteúdo
- **Description**: Usar `System.Security.Cryptography` para o hash do snapshot.
- **Pros**: Resistente a colisões.
- **Cons**: Dependência de criptografia da BCL, cujo comportamento sob stripping do IL2CPP é `NOT SOURCEABLE`; o hash aqui é identidade e detecção de corrupção, não segurança.
- **Rejection Reason**: FNV-1a de 64 bits, já escolhido para o hash do estado da simulação, basta e não tem dependência. A integridade do pacote remoto fica com o ADR do #29, que decide a criptografia.

### Alternative 6: Conversão `decimal` para `float`
- **Description**: (a) o `(float)decimal` da BCL; (b) uma rotina própria, só com inteiros, que arredonda ao `float` de 32 bits ao par mais próximo (o próprio GDD #1, F2, sugere "ou usar uma conversão própria").
- **Pros**: (b) tira a BCL do caminho: atualizar o editor ou migrar de runtime nunca muda os bits, as revisões nem o hash; (a) é uma linha de código.
- **Cons**: (b) são algumas dezenas de linhas de código novo e crítico, com testes de vetores; (a) a BCL pode arredondar duas vezes (por exemplo passando por `double`), e uma mudança de runtime do editor mudaria bits, hash e revisões (`neutra` proibida), o que viraria um "patch" de nerf ou buff por causa de uma atualização de ferramenta.
- **Rejection Reason**: Escolhida a (b), por recomendação (provisória).

### Alternative 7: Snapshot versionado ou gerado só no build
- **Description**: (a) o snapshot não é versionado e o pré-build o gera a cada build; (b) o snapshot fica versionado num caminho fixo e o pré-build o revalida, refaz o bake em memória e compara o hash.
- **Pros**: (b) o asset já existe e já foi importado quando o build começa (gerar dentro do pré-build é frágil: o asset pode não ser importado a tempo); o diff do `.bytes` mostra quando os dados mudaram; o hash versionado e o recomputado se conferem.
- **Cons**: (b) o `.bytes` vira um arquivo versionado a regenerar pelo menu e que nunca se resolve por merge; (a) evita esse arquivo, mas o build passa a depender de gravar um asset no meio do build.
- **Rejection Reason**: Escolhida a (b) (provisória). O ADR faz as duas conferências do hash: o campo versionado do cabeçalho e o recomputado no pré-build.

### Alternative 8: Um arquivo só ou um arquivo por fase
- **Description**: (a) um arquivo com o catálogo global e uma seção por fase, com hash por seção no diretório; (b) um arquivo por fase mais o do catálogo.
- **Pros**: (a) um único asset e um único GUID; a verificação por seção já bloqueia só a fase com problema.
- **Cons**: (a) o arquivo cresce com o número de fases; (b) mais assets e mais referências a manter no componente de boot.
- **Rejection Reason**: Escolhida a (a) (provisória); reavaliar se o tamanho do snapshot, medido no spike, pedir carga por fase.

## Consequences

### Positive
- Um só caminho de conversão, no build, com bits idênticos em todas as plataformas: o jogo e a simulação headless leem o mesmo snapshot.
- Nenhum parse de texto e nenhuma conversão em runtime nos dados embarcados: menos risco de engine e carga rápida.
- A validação roda no editor e nos testes EditMode com os mesmos fixtures; um dado inválido nunca gera build.
- Hash e rótulo identificam a versão em todo log; a revisão por skill dá ao #18 e ao #28 fatos confiáveis.
- O contrato do pacote remoto fica fixado sem comprometer o MVP com transporte nem assinatura.

### Negative
- Os números autorais viram texto no JSON: a edição é menos natural que um número puro, e o jogo precisa de um passo de build para gerar o snapshot.
- A validação em `decimal` não roda no aparelho para os dados embarcados: ali só a integridade (hash e estrutura) é conferida.
- O ADR-0001 e o registro `sim_time` precisam de emenda (taxas por tick).
- O GDD #1 (Core Rule 5) foi ajustado em 2026-11-05 para dizer onde a validação roda.
- O layout de cada seção fica espalhado nos GDDs donos: a primeira story do #1 precisa de uma convenção comum de seção.
- Validar `decimal` no aparelho (pacote remoto) continua dependendo de uma verificação de runtime (`NOT SOURCEABLE`).

## Risks
- **Divergência de `System.Decimal` entre runtimes:** só importa para o pacote remoto no aparelho; mitigação é gravar os bits no build para o embarcado e fazer o spike do item 7 antes do ADR do #29.
- **Carga do asset de bytes no Android** (como o Unity empacota e carrega) e o tempo contra os tetos do #1: `NOT SOURCEABLE`; mitigação é o spike de performance e os tetos provisórios do #1.
- **Passo de pré-build que não falha o build:** mitigação é o item 4 de Verification Required e um teste que força um dado inválido e confere que não sai build.
- **Números como texto digitados com vírgula** ou com formato errado: o validador recusa o conjunto, com a lista de erros.
- **Livros-razão (`ids.ledger.json`, `revisions.ledger.json`) fora de sincronia** com o git (merge, branch): mitigação é o baker recusar quando o livro-razão não bate com os dados e um teste de CI.
- **Ajuste de redação do GDD #1 feito em 2026-11-05** (Core Rules 3, 4 e 5; o Edge Case "a escrita é atômica; o mecanismo é do ADR do #1"; a tabela de AC bloqueados (AC-13 e AC-14); as frases de "Não testável" sobre a escrita atômica e sobre "mesma função… no carregamento"; a F2, Output Range, cuja decisão foi tomada; e a seção "Vira ADR"): resta a conferência no `/design-review` do #1.
- **Conversão própria `decimal` para `float`:** a rotina só com inteiros tira a BCL do caminho, mas é código novo e crítico (uma divergência muda todos os bits); mitigação é a bateria de testes contra o `(float)decimal` do editor, os vetores de AC-F1 e AC-F2 e o teste de hash dourado. Se a rotina própria for abandonada e se voltar ao `(float)decimal`, uma atualização do editor (o `VERSION.md` cita a direção de um Editor CoreCLR) pode mudar bits e, com eles, hash e revisões, e `neutra` ficaria proibida.
- **Cultura do Windows em pt-BR:** `decimal.Parse` ou `ToString` sem cultura invariante trocaria ponto por vírgula e quebraria os dados, os livros-razão e o hash de texto; mitigação é a regra de cultura explícita e o teste em duas máquinas.
- **Importação ou fim de linha alterando o `.bytes`:** mitigação é `*.bytes -text` no `.gitattributes` e o hash conferido na carga (que pegaria a alteração, mas tarde).
- **Tamanho do snapshot não estimado:** sem estimativa, o tempo de carga e a memória só saem do spike (AC-P1); a primeira story do #1 deve registrar uma estimativa.
- **Snapshot velho no Play Mode do editor:** você edita o JSON, esquece o menu e o Play Mode roda com o `.bytes` antigo sem aviso (o pré-build só protege o build); mitigação é uma checagem só de editor ao entrar no Play Mode, que compara o bake em memória com o arquivo e avisa ou bloqueia, **sem gravar nada**.
- **Merge do `.bytes` e dos livros-razão:** um conflito de merge no binário ou nos livros-razão nunca se resolve à mão; mitigação é a regra de sempre regenerar pelo menu e o baker recusar um livro-razão que não bate com os dados.
- **Tamanho do contrato contra o prazo do MVP, com um dev solo:** tokenizador, seis checagens, baker, verificador, dois livros-razão, classificação e pré-build; mitigação é ordenar as stories pelo núcleo primeiro (tokenizador, validador, baker, verificador, pré-build) e os livros-razão e a revisão antes do primeiro build externo (o GDD #1 exige revisão e classificação desde o MVP, então é sequenciamento, não corte).
- **Validação do `unity-specialist` (5.5, 2026-11-05):** sem achado bloqueante. Incorporado: tokenizador próprio dentro de `Forja.Data` (sem `JsonUtility` nem pacote de terceiros); cultura invariante e `NumberStyles` explícitos; `floor(x + 0,5)` sem `MidpointRounding` em paralelo e a ressalva de que `(float)decimal` pode arredondar duas vezes por dentro (vetores do editor real e hash dourado); hash no cabeçalho do `.bytes`, baker que sobrescreve no lugar e só grava se os bytes mudaram, `*.bytes -text`; decodificação única para arrays privados com `BinaryPrimitives` e verificador que recusa NaN e infinito; pré-build que refaz o bake em memória e compara com o snapshot versionado, sem `AssetPostprocessor` nem escrita em Play Mode; asmdef de testes separado; `StringComparer.Ordinal`; proibição de `static` estendida ao carregador e ao editor; carga síncrona registrada como desvio deliberado do `deprecated-apis.md`. Segue `NOT SOURCEABLE`: perfil de API e `System.Decimal`, `(float)decimal` entre runtimes, empacotamento e carga de `TextAsset` no Android, `IPreprocessBuildWithReport` e `BuildFailedException` no 6000.3.27f1, configuração de asmdef e o stripping do IL2CPP; o que veio do conhecimento próprio do especialista precisa de um spike curto.
- **Revisão TD-ADR (5.6, 2026-11-05):** CONCERNS na 1ª passada, sem REJECT. Revisados neste texto: (C1) emenda ao ADR-0001 ampliada (Tempo, Interface, uma Guideline, `sim_time` e a linha 23 das Emendas); (C2) hash por seção no diretório, verificação por fase e a frase de "prova" corrigida; (C12) revisão calculada sobre IDs em texto e bits, sem índices; (C3) conversão própria `decimal` para `float`, só com inteiros (Alternative 6, provisória), no lugar do `(float)decimal`; (C4) histórico de revisão do aparelho delegado; (C5) hash efetivo definido; (C6) posições do registro listadas em Related (gravação com aprovação); (C7) grafo de asmdefs; (C8) Alternatives 6 a 8; (C9) riscos do Play Mode, do merge do `.bytes` e do prazo, e a checagem de editor no Play Mode; (C10) lista completa de ajustes no GDD #1; (C11) redação sobre `TextAsset` e carga síncrona; marcação de provisória em todas as decisões. Pendente: a ordem (o ADR-0001 é aceito antes ou junto; a emenda entra no texto dele antes de aceitá-lo). A revisão do TD sobre o texto revisado não foi refeita.

## GDD Requirements Addressed

| GDD System | Requirement | How This ADR Addresses It |
|------------|-------------|--------------------------|
| `design/gdd/dados-e-balanceamento.md` (#1) Core Rule 1 | Todo valor de gameplay é dado externo com dono, unidade e faixa | Autoria em JSON; o validador exige dono, unidade e faixa |
| `dados-e-balanceamento.md` Core Rules 3 e 4 | IDs estáveis; unidades; conversão uma vez e bit a bit idêntica em todas as plataformas | IDs por ordem ordinal e livro-razão (seção 5); conversão em `decimal` no build com os bits gravados (seção 3) |
| `dados-e-balanceamento.md` Core Rule 5 e AC-F1 | Validação tudo ou nada, mesma função, recusa sem ajuste | `DataValidator` em `decimal` (seção 2); no carregamento, `SnapshotVerifier` por hash e estrutura (refinamento da redação, ajustado no GDD em 2026-11-05) |
| `dados-e-balanceamento.md` Core Rule 6 e Edge Cases | Hash de conteúdo, rótulo, revisão por skill e classificação autoral | FNV-1a 64 e rótulo (seção 6); revisão por fecho e contador com classificação obrigatória (seção 7) |
| `dados-e-balanceamento.md` Core Rule 7 | Dados completos, validados e imutáveis antes do tick 0; falha bloqueia a fase | Carga síncrona e verificação em toda carga (seção 8); snapshot imutável (seção 4) |
| `dados-e-balanceamento.md` Core Rules 8 e 10 | Congelamento de aceite; proibições; lista branca | Guidelines (knob de aceite nunca remoto; contagens e tetos nunca remotos) e seção 10 |
| `dados-e-balanceamento.md` Core Rule 9 | Sobrescrita remota atômica e entre partidas | Contrato fixado na seção 10; transporte e persistência ficam para o ADR do #29 |
| `dados-e-balanceamento.md` AC-F2 | O caminho da taxa por tick (dividir em `decimal` ou multiplicar por `TickSeconds`) | Dividir em `decimal`, converter uma vez (seção 3); emenda ao ADR-0001 |
| `dados-e-balanceamento.md` AC-I3 (EM) | Hash canônico e formato dos bits do snapshot | Seções 4 e 6 |
| `dados-e-balanceamento.md` AC-P1 e knobs `phase_load_*` | Orçamento de carga e de memória do snapshot | Carga síncrona do embarcado; medição no spike (Verification Required 3 e 8) |
| `design/gdd/simulacao-deterministica.md` (#2) | `Simulation.Create` recebe um snapshot com capacidades e hash; capacidade de ids = total de spawns | `PhaseSnapshot : IPhaseSnapshot` (Key Interfaces); capacidades validadas pelo `DataValidator` |
| `design/gdd/fluxo-de-fase.md` (#3) | Curva de XP, `nivel_max`, tempo máximo e `tick_entrada_chefe_agendado` já em ticks e inteiros | Conversão no build; a seção da fase leva esses campos; F1 e F5 do #3 validadas pelo `DataValidator` |
| `design/gdd/save-local.md` (#28) | O save grava só IDs, carimbo da versão e revisão da skill selada; "ID desconhecido" | IDs estáveis e tabela de IDs fora do tick; `IDataVersion` expõe hash, rótulo e revisão |
| #5 Log de eventos (GDD pendente) | O cabeçalho de cada partida leva hash, rótulo, tag do build e o pacote aplicado | Hash e rótulo (seção 6); a tag do build é do ADR-0001 |
| #29 Serviços online (GDD pendente) | O #1 define o contrato do pacote; o #29 implementa o provedor | `IDataOverrideProvider` e a seção 10 |

## Performance Implications
- **CPU**: nenhum custo por tick (os dados são lidos uma vez); a carga custa uma leitura de bytes, o `SnapshotVerifier` (um FNV-1a por byte do snapshot) e a montagem dos objetos de leitura. Os tetos de carga são os do #1 (3000 ms a frio e 1500 ms a quente, provisórios); o orçamento em ms **não é reivindicado aqui**, porque o aparelho de referência não foi verificado.
- **Memory**: o snapshot em memória mais as capacidades pré-alocadas (`phase_snapshot_memory_kb`, a medir no spike); arrays imutáveis, sem cópia por fase.
- **Load Time**: carga fria e quente medidas no spike (AC-P1); nada de carga durante a fase.
- **Network**: não se aplica (o pacote remoto é do #29).

## Migration Plan
Não se aplica: o projeto não tem código de jogo (`Assets/` só contém o modelo inicial do Unity). A estrutura de pastas (`Assets/GameData/`, os asmdefs `Forja.Data` e `Forja.Data.Editor`) nasce com a primeira story do #1.

## Validation Criteria
- AC-F1 do #1: as durações 0,15 s, 2,5 s, 0,0167 s, 0,0166 s e 0,01 s dão 5, 75, 1 tick e as duas últimas são recusadas, **no baker**, com o meio para cima.
- AC-F2 do #1: 100 de dano por segundo dá os bits de `DecimalParaFloat(100m ÷ 30m)` no snapshot (comparados com o `(float)decimal` do editor, com a diferença registrada, se houver), e o teste fixa esse valor.
- O snapshot gerado duas vezes a partir dos mesmos dados dá os mesmos bytes e o mesmo hash (determinismo do baker), em duas máquinas do editor.
- O `SnapshotVerifier` recusa um snapshot com um byte alterado, com ID fora de ordem e com capacidade acima do teto; um byte alterado numa seção de fase bloqueia só aquela fase, e um byte alterado no catálogo bloqueia todas.
- Capacidade de ids (GDD #1, F3): com `SpawnsDeDados` 899 e margem 25, `EntityCapacity` 1124 passa no `DataValidator` e no `SnapshotVerifier`, e `EntityCapacity` 1100 é recusada já no build; o compositor recusa 1124 e aceita 1125 quando `IdsDePreparacao` = 1 (ADR-0001, item 6).
- Um dado inválido (valor fora da faixa, `neutra` com valor mudado, ID removido, mudança de fecho sem classificação) faz o pré-build falhar e **não gera build**.
- O hash recomputado no aparelho (Android IL2CPP ARM64) é igual ao campo do cabeçalho do snapshot (Verification Required 1).
- Nenhuma leitura de arquivo de dados nem conversão acontece entre o tick 0 e o fim da partida.
- Inserir uma skill nova no meio da ordem de IDs não muda a revisão de nenhuma skill existente.
- O pré-build refaz o bake em memória e falha se o hash diverge do snapshot versionado (testado chamando a lógica do passo em EditMode; um build real, uma vez, manual ou de CI).
- Um teste com hash dourado fixa os bits do snapshot, e os vetores de AC-F1 e AC-F2 saem do editor real.
- Em duas máquinas do editor (inclusive com cultura pt-BR no Windows), o mesmo JSON dá os mesmos bytes e o mesmo hash.

## Reavaliação prevista
O usuário confirmou as premissas deste ADR por recomendação (autoria em texto, snapshot gerado no build, carga síncrona sem Addressables, FNV-1a, revisão por skill, pacote remoto só como contrato) sem dominar todos os conceitos, e pediu para reavaliá-las com o jogo avançado. Momento natural: depois do spike de performance (carga e memória) e do spike de runtimes (`decimal`, bits e carga do asset de bytes). Até lá o ADR segue `Proposed`, e **todas as decisões deste ADR (seções 1 a 10) são provisórias**, mesmo onde o texto não traz a marca.

## Related
- `design/gdd/dados-e-balanceamento.md` (#1, OQ-2), `design/gdd/simulacao-deterministica.md` (#2), `design/gdd/fluxo-de-fase.md` (#3) e `design/gdd/save-local.md` (#28).
- ADR-0001 (`Proposed`): **este ADR emenda as seções Tempo e Interface, uma Guideline e o registro `sim_time`** (conversão no build e sem `ScriptableObject`; taxas por segundo: dividir em `decimal` e converter uma vez, em vez de multiplicar por `SimClock.TickSeconds`).
- Candidatos futuros: o ADR do #29 (transporte, assinatura, expiração, persistência atômica e o formato do pacote remoto), o ADR do save (#28, OQ-1: mecanismo de escrita atômica, que o pacote pode reaproveitar) e os ADRs de #6 e #7 (colunas do `SimWorld`).
- Ajuste de redação pedido ao GDD #1 (feito em 2026-11-05): Core Rules 3 e 4 ("no carregamento" passa a "no build"), Core Rule 5 (onde a validação roda), o Edge Case da escrita atômica do pacote, a tabela de AC bloqueados (AC-13 e AC-14), as frases de "Não testável", a F2 (Output Range) e a seção "Vira ADR".
- Revisão de 2026-11-05 (`/propagate-design-change`, GDD #1, pendência P2): o total de spawns tem três termos; o `PhaseSnapshot` ganha `SpawnsDeDados` e `CapacityMarginPct`; a conferência do termo de código fica no compositor (ADR-0001, item 6; emenda 24). Pendências restantes: teto próprio da tabela de ids em `capacity_ceiling` (P3) e `Fnv1a64` nas Key Interfaces (Q4).
- Registro de arquitetura (na gravação, com aprovação): novas `data_authoring_format`, `data_content_hash`, `data_embedded_load`, `game_data_snapshot`, `phase_snapshot`, `data_version`, `data_override_provider`, `authored_number_through_float`, `data_conversion_during_phase` e `culture_dependent_parse`; revisadas `sim_time`, `sim_numeric_type` (o `not: decimal` vale só para o estado da simulação) e `mutable_static_in_simulation` (inclui `Forja.Data`, o carregador e os caches do editor).
