# ADR-0001: Simulação de combate determinística (#2): float32 em C# puro, tick fixo de 30 Hz, PCG32 com streams e interface por Tick + buffer de eventos

## Status
Proposed

## Date
2026-11-03

## Last Verified
2026-11-03 (contra Unity 6.3 LTS, pin 6000.3.x, e `design/gdd/game-concept.md` congelado)

## Decision Makers
Rodrigo Reis (decisão de projeto, as quatro escolhas abaixo confirmadas em 2026-11-03), Claude Code (autoria), `unity-specialist` (validação de API, 5.5) e `technical-director` (gate TD-ADR, 5.6). Os resultados das duas revisões entram na seção Risks e no log deste ADR antes de gravar.

## Summary
A simulação de combate (#2) precisa de um tipo numérico, de uma taxa de tick e de um gerador aleatório decididos antes dos GDDs #6 Combate, #7 Horda e #8 Skills, porque cada fórmula desses GDDs herda a escolha. Decidido: simulação em `float` (32 bits) em C# puro, sem referência à engine, com tick fixo de 30 Hz, PRNG próprio PCG32 com streams independentes, e uma interface em que a apresentação chama `Tick(comandos)` e lê um buffer de eventos; a reprodutibilidade garantida é a do mesmo build, e o ponto fixo fica como substituição futura registrada.

## Engine Compatibility

| Field | Value |
|-------|-------|
| **Engine** | Unity 6.3 LTS (6000.3.x; editor instalado 6000.3.27f1) |
| **Domain** | Core |
| **Layer** | Core |
| **Knowledge Risk** | HIGH (`docs/engine-reference/unity/VERSION.md`) |
| **References Consulted** | `docs/engine-reference/unity/VERSION.md`, `current-best-practices.md`, `deprecated-apis.md`, `breaking-changes.md`; `design/gdd/game-concept.md` (L246, L323, L326, L349, L400); `design/gdd/systems-index.md` |
| **Post-Cutoff APIs Used** | None. O código da simulação usa só C# 9 (`System`, `System.Runtime.CompilerServices`, `Span<T>`) e a opção de asmdef "No Engine References". Nenhuma API Unity 6 é necessária dentro da simulação; a ponte com a apresentação (MonoBehaviour que acumula tempo e chama `Tick`) usa APIs antigas e estáveis. |
| **Verification Required** | (1) Spike de hash entre runtimes: mesma seed e mesmo fluxo de comandos gravado, hash do estado a cada N ticks, rodando no Editor (Mono, x64), em build Windows IL2CPP e em Android IL2CPP ARM64; comparar. Hoje `NOT SOURCEABLE`: determinismo de float entre Mono, IL2CPP e ARM64 não está coberto por `docs/engine-reference/unity/`. (2) Confirmar no aparelho que o IL2CPP ARM64 não funde `a*b+c` em FMA de modo que mude o resultado entre execuções do mesmo build (esperado estável no mesmo build; o spike (1) mostra). (3) Profiler: zero alocação gerenciada por `Tick` em regime. (4) Confirmar no 6000.3.27f1 que a opção "No Engine References" do asmdef existe e falha a compilação ao usar `UnityEngine` (`NOT SOURCEABLE`: `docs/engine-reference/unity/` não a cobre), e que `ref struct` + `ReadOnlySpan<T>` + interface compilam e rodam no asmdef sem engine, no Editor (Mono) e em IL2CPP. (5) O spike (1) roda em build **Release** (IL2CPP, stripping ligado), não só Debug. |

## ADR Dependencies

| Field | Value |
|-------|-------|
| **Depends On** | None (varredura conclusiva: não existe outro ADR em `docs/architecture/` e `docs/registry/architecture.yaml` está vazio) |
| **Enables** | GDDs #6 Combate e dano, #7 Horda/waves/inimigos e #8 Skills e evoluções (unidades de tempo em ticks, fórmulas em float32, ordem de sistemas). ADR futuro de replay e validação de ranking (#22) e de auto-battle (#40), que podem substituir este ADR pelo ponto fixo. |
| **Blocks** | Épicos de #2 Simulação, #3 Fluxo de fase e #5 Log de eventos e instrumentação; qualquer story de #6, #7 e #8 que escreva fórmula com unidade de tempo. Nenhuma story existe ainda, então nenhuma está `Blocked` hoje. |
| **Ordering Note** | Deve ser Accepted antes de `/design-system` de #6. A tabela de ordem de implementação do índice põe #2 logo depois de #28 Save local. O spike de hash entre runtimes (Verification Required 1) roda junto do spike de performance já previsto antes do vertical slice; ele não condiciona a aceitação, mas um resultado de divergência no mesmo build reabre este ADR. |

## Context

### Problem Statement
O conceito exige tick fixo, RNG com seed e lógica de combate sem MonoBehaviour (L326), e uma simulação headless que chama o mesmo código do jogo para medir oferta, registro e substituição do Grimório (L400). Ele também deixa a escolha entre float e inteiro ou ponto fixo para este ADR, porque só o inteiro ou o ponto fixo viabilizaria replay validado por servidor, ranking por replay e autoridade de host no futuro (L326). Os GDDs #6, #7 e #8 vão definir fórmulas, durações, cooldowns e taxas de spawn; se o tipo numérico e a unidade de tempo mudarem depois deles, toda fórmula é reescrita. A decisão precisa vir agora.

### Constraints
- Dev solo, MVP dentro de 13 a 20 meses; custo de código e de depuração pesa mais que o ganho teórico de determinismo que o MVP não usa.
- Android primeiro, aparelho de referência ainda não verificado; horda grande em CPU móvel: sem alocação por tick e custo do tick na ordem de poucos milissegundos.
- C# 9 no Unity 6.3; Burst só aceita tipos blittable; determinismo de `Unity.Mathematics` e semântica de float sob Burst são `NOT SOURCEABLE`.
- No MVP basta reprodutibilidade no mesmo build. Replay, validação cross-device e ranking por replay são pós-lançamento (#22 Alpha, #40 Full Vision).
- Valores de gameplay vêm de dados externos, nunca fixos no código (`.claude/docs/coding-standards.md`); isto vale para o tick: a taxa é a única constante de simulação.
- Rules de `Assets/**/Core/**`: zero alocação nos caminhos quentes.

### Requirements
- Mesma `seed` e mesmo fluxo de comandos por tick produzem o mesmo estado, tick a tick, no mesmo build.
- RNG com streams independentes (spawn, oferta, loot): consumir um sorteio num stream nunca desloca outro.
- Lógica sem MonoBehaviour e sem `UnityEngine`; a simulação roda headless em teste EditMode chamando o mesmo código do jogo.
- O auto-battle (#40, Full Vision) e o teste headless rodam a mesma simulação, com comandos vindos de uma política em vez do jogador. A Varredura (#15) credita a recompensa sem simular a fase (`systems-index.md`) e não usa este ADR.
- Apresentação nunca escreve no estado da simulação; a simulação nunca chama a apresentação.

## Decision

### Numérico
A simulação usa **`float` (System.Single)** como único tipo fracionário. `double` e `decimal` ficam fora do estado da simulação. Os tipos de vetor da simulação são próprios (`SimVec2` ou equivalente, definido pelo ADR de #6 conforme os eixos do combate), e **toda operação além de `+ - * /` e comparação passa por `SimMath`**: `Sqrt`, `Abs`, `Min`, `Max`, `Clamp`, `Lerp`. Funções transcendentais (`Sin`, `Cos`, `Atan2`, `Pow`, `Exp`, `Log`) **não entram** no estado da simulação; quando uma fórmula as pedir, usar tabela pré-computada e versionada, ou trocar a fórmula. `Unity.Mathematics`, `UnityEngine.Mathf` e `Vector3` ficam fora do código da simulação (determinismo de `Unity.Mathematics` é `NOT SOURCEABLE`; `Mathf` e `Vector3` exigem `UnityEngine`).

**"Mesmo build" neste ADR significa mesmo binário e mesma ABI** (mesmo código IL2CPP gerado para a mesma arquitetura). Um APK com `armeabi-v7a` e `arm64-v8a` tem dois caminhos de código e não se compara entre eles. Consequência: o resultado de um auto-battle (#40) é calculado e creditado de uma vez, e **nunca é derivado de novo da seed depois de um update do app**, porque um build novo pode mudar o resultado.

Escolha e custo: o float dá reprodutibilidade no mesmo build (o que o MVP exige) pelo menor custo de código nos GDDs #6, #7 e #8, mas não garante o mesmo resultado entre runtimes diferentes (Editor Mono x64, IL2CPP ARM64). `SimMath` e o vetor próprio são o ponto único por onde uma troca futura para ponto fixo passa, mas a troca ainda toca toda fórmula; ela não é gratuita.

### Tempo
`SimClock.TicksPerSecond = 30` e `SimClock.TickSeconds = 1f / 30f` são constantes de compilação. A simulação nunca lê `Time`, relógio de parede nem frame. **Os GDDs e os dados escrevem tempo em segundos; a simulação trabalha em ticks inteiros.** No carregamento da fase: durações e cooldowns viram ticks por **arredondamento ao inteiro mais próximo com mínimo de 1 tick** (não `ceil`, que é frágil em float: `0,1 × 30` pode dar `3,0000x` e virar 4 ticks); taxas por segundo (velocidade, DPS, regeneração) são multiplicadas por `SimClock.TickSeconds`. Janelas curtas (i-frames, telegraph) podem ser escritas direto em ticks nos dados. Um valor de dado que resulte em menos de 1 tick é recusado na validação dos dados. A apresentação acumula tempo real e executa `N` ticks por frame, limitada por `MaxTicksPerFrame` (valor inicial 4, botão de ajuste a medir no aparelho): se o atraso passar do limite, o excedente é descartado e a simulação roda em câmera lenta, o que é determinístico porque o resultado depende só da sequência de ticks e de comandos, nunca do tempo de parede. A renderização interpola entre o estado anterior e o atual; **quem guarda o estado anterior é a simulação** (o `SimWorld` mantém a posição do tick anterior), a apresentação só lê. A ponte e o log (#5) **drenam os eventos depois de cada `Tick`**, não uma vez por frame, porque com até `MaxTicksPerFrame` ticks por frame o buffer só vale até o próximo `Tick`.

### Aleatoriedade
O PRNG é **PCG32** (estado de 64 bits, saída de 32 bits) implementado em C# puro, na simulação. `UnityEngine.Random` e `System.Random` são proibidos em todo código chamado pela simulação ou pelo código de oferta do Grimório. Cada stream é uma instância `Pcg32` inicializada com a seed `SplitMix64(seedMestre ^ idDoStream)` e com o id como sequência (incremento) do PCG32: o incremento sozinho deixaria streams de mesma seed correlacionados. Streams iniciais: `Spawn`, `Offer`, `Loot`. Criar um stream novo exige um novo id fixo e uma entrada no registro. **Regra para o GDD #7:** o `Spawn` sorteia por índice de wave (subsequência derivada de `(seedMestre, índiceDaWave)` ou número fixo de sorteios por wave), nunca por tick; senão o ritmo de abate desloca a sequência e a comparação Tank × DPS na mesma seed (systems-index #2) deixa de ver a mesma composição de waves. Sorteios limitados usam o método de rejeição (sem viés de módulo) e o float em `[0,1)` é `(saída >> 8) * (1f / 16777216f)`, que é exato em float32. Nenhuma estrutura de iteração não ordenada (`Dictionary`, `HashSet`) pode ser percorrida para decidir ordem de efeito; a iteração é sempre por índice crescente.

### Interface
A simulação é uma classe de C# puro. **Três asmdefs**, para que o teste headless e o jogo montem exatamente a mesma lista de sistemas (L400):
- `Forja.Simulation` (Core, "No Engine References", `Assets/Scripts/Core/Simulation/`): relógio de ticks, streams, `SimWorld`, buffers de comandos e de eventos, `ISimSystem`.
- `Forja.Gameplay.Sim` (sem engine, `Assets/Scripts/Gameplay/Sim/`): os sistemas de regra (#3 Fluxo de fase, #6 Combate, #7 Horda, #8 Skills, a oferta do Grimório #16, …) e o **compositor**, que fixa a ordem dos sistemas. O jogo e o teste headless chamam o mesmo compositor.
- `Forja.Gameplay` (com Unity, `Assets/Scripts/Gameplay/`): conversão de `ScriptableObject` em structs de fase, a ponte (acumulador de tempo, drenagem de eventos, interpolação) e a apresentação.

A dependência vai sempre de Gameplay para Core. A ordem de execução dos sistemas dentro do tick é a ordem de registro no compositor, fixa e documentada.

**Estado compartilhado: `SimWorld` mínimo em Core.** Tabela de entidades com arrays pré-alocados (SoA): id, posição atual e posição do tick anterior, facção, HP e flag de vivo, com capacidade fixada no início da fase a partir dos dados da fase. **IDs são monotônicos por fase e nunca reutilizados**, de modo que um `ActorId` num evento lido pela apresentação nunca aponta para outra entidade depois de uma morte (handle com geração só entra se o pool exigir, e isso é uma mudança de ADR). Os sistemas leem e escrevem esses campos pelo mesmo contrato; dado extra de um sistema (cooldowns, estados de skill) fica no sistema, indexado pelo índice da entidade. O ADR do #6 e do #7 pode acrescentar colunas ao `SimWorld`, nunca outra tabela de entidades.

**Eventos são só saída.** O `EventBuffer` serve à apresentação e ao log (#5); **não é barramento entre sistemas**. A comunicação interna do tick passa pelo `SimWorld`, para que ordem de assinatura nunca vire regra. A capacidade do buffer vem dos dados da fase; se encher, a simulação incrementa `DroppedEvents` e **nunca descarta em silêncio**: em desenvolvimento o teste e o host falham quando o contador é diferente de zero, em release o contador vai para o log (#5).

**#3 e a oferta do Grimório (#16) são `ISimSystem`.** Eles rodam dentro do `Step`, na ordem do compositor, e sorteiam do stream `Offer` pelo contexto; o teste headless chama o mesmo código de oferta, registro e substituição do jogo.

Fluxo de um tick: a apresentação (ou a política de auto-battle, ou o teste headless) chama `Tick(comandos)`; a simulação limpa o buffer de eventos, executa cada sistema em ordem, que lê comandos e o `SimWorld`, sorteia dos streams e escreve eventos; a ponte e o log drenam os eventos e a apresentação lê as visões somente leitura. O `Hash` de cada sistema e o do `SimWorld` compõem o hash global usado em testes. A política do auto-battle (#40) obedece às mesmas regras da simulação (float, sem `System.Random`, sem `UnityEngine`).

### Architecture Diagram
```
 Forja.Gameplay (Unity)                        Core: Forja.Simulation (sem UnityEngine)
 ┌────────────────────────────────┐             ┌──────────────────────────────────────┐
 │ input → Command[]              │  Tick(cmds) │ Simulation                            │
 │ acumula tempo → N ticks (≤cap) │───────────▶│  ├ SimClock (30 Hz)                   │
 │ drena eventos após CADA Tick   │             │  ├ RngStreams: Spawn / Offer / Loot   │
 │ interpola prev/curr no render  │◀───────────│  ├ SimWorld (entidades, ids, prev pos)│
 │ lê eventos, anima, toca SFX    │ eventos +   │  ├ EventBuffer (só saída)             │
 └────────────────────────────────┘ visões RO   │  └ ISimSystem[] em ordem fixa         │
 Auto-battle (#40) / teste headless              └────────┼───────────────────────────────┘
 = outra fonte de Command[]                                │ registrados pelo compositor
                                                  Forja.Gameplay.Sim (sem engine):
                                                  #3 Fluxo, #6 Combate, #7 Horda, #8 Skills,
                                                  #16 Oferta (dependem de Core; estado e hash próprios)
```

### Key Interfaces
```csharp
namespace Forja.Simulation
{
    /// <summary>Unidade de tempo de toda a simulação e dos GDDs: o tick.</summary>
    public static class SimClock
    {
        public const int TicksPerSecond = 30;
        public const float TickSeconds = 1f / TicksPerSecond;
    }

    /// <summary>Entrada de um ator num tick; a simulação só vê comandos, nunca o dispositivo.</summary>
    public readonly struct Command
    {
        public readonly int ActorId;
        public readonly CommandKind Kind;   // Move, Dodge, Ultimate, ...
        public readonly float X, Y;         // eixo do joystick; ignorado nos outros tipos
    }

    /// <summary>Evento de saída, escrito pela simulação e lido pela apresentação e pelo log (#5).</summary>
    public readonly struct SimEvent
    {
        public readonly int Tick;
        public readonly SimEventKind Kind;  // Damage, Death, Spawn, SkillCast, ...
        public readonly int ActorId, TargetId;
        public readonly float Value;
    }

    /// <summary>PCG32 em C# puro; estado de 64 bits, uma sequência por stream.</summary>
    public struct Pcg32
    {
        public Pcg32(ulong seed, ulong stream);
        public uint NextUInt();
        public int NextInt(int exclusiveMax);   // sem viés de módulo
        public float NextFloat01();             // [0,1), exato em float32
    }

    public enum RngStream { Spawn = 0, Offer = 1, Loot = 2 }

    /// <summary>Tabela de entidades compartilhada (SoA, pré-alocada). Ids monotônicos, nunca reutilizados.</summary>
    public sealed class SimWorld
    {
        public int Spawn(int faction);                 // devolve o id novo
        public bool IsAlive(int id);
        // posição atual e do tick anterior, facção e HP por id; colunas extras só por ADR de #6/#7
    }

    /// <summary>Contexto passado a cada sistema durante um tick.</summary>
    public ref struct SimContext
    {
        public int Tick { get; }
        public SimWorld World { get; }
        public ReadOnlySpan<Command> Commands { get; }
        public ref Pcg32 Rng(RngStream stream);
        public void Emit(in SimEvent e);
    }

    /// <summary>Uma regra da simulação (combate, horda, skills). Estado próprio, sem UnityEngine.</summary>
    public interface ISimSystem
    {
        void Step(ref SimContext ctx);
        void Hash(ref StateHasher hasher);  // para testes de reprodutibilidade
    }

    public sealed class Simulation
    {
        public Simulation(ulong masterSeed, ISimSystem[] systemsInExecutionOrder);
        public int CurrentTick { get; }
        public SimWorld World { get; }
        public int DroppedEvents { get; }               // nunca descarta em silêncio
        public ReadOnlySpan<SimEvent> Events { get; }   // válido até o próximo Tick: drenar após cada Tick
        public void Tick(ReadOnlySpan<Command> commands);
        public ulong StateHash();
    }
}
```
Os nomes e as assinaturas são o contrato do ADR; campos e enums completos pertencem aos ADRs e GDDs de #6, #7 e #8.

### Implementation Guidelines
- O compositor que fixa a ordem dos sistemas **must** viver em `Forja.Gameplay.Sim` (sem engine) e ser o único lugar que monta a lista; o teste headless e o jogo **must never** montar listas próprias. **Must** drenar `Events` depois de cada `Tick` e **must never** ler um `Events` de um tick anterior. Eventos **must never** ser usados como canal entre sistemas dentro do tick (usar o `SimWorld`).
- IDs de entidade **must never** ser reutilizados na mesma fase.
- Dados de tempo **must** vir em segundos (ou em ticks, nas janelas curtas) e ser convertidos no carregamento com arredondamento ao mais próximo, mínimo 1 tick; **must never** usar `ceil` sobre float para isso.
- O código da simulação e de qualquer sistema chamado por `ISimSystem.Step` **must** estar em asmdef com "No Engine References"; **must never** referenciar `UnityEngine`, `MonoBehaviour`, `ScriptableObject` (carregar dados e converter em structs antes da fase), `Time`, `Mathf`, `Vector3` nem `Unity.Mathematics`.
- **Must** usar só `float`; **must never** usar `double` ou `decimal` no estado; **must never** chamar funções transcendentais no estado; **must** passar `Sqrt`, `Abs`, `Min`, `Max`, `Clamp` e `Lerp` por `SimMath`.
- **Must never** usar `UnityEngine.Random` nem `System.Random`; todo sorteio vem de um `RngStream` do contexto; **must never** fazer um sistema compartilhar sorteios de outro stream.
- Sistemas `ISimSystem` **must** ser `class` (nunca `struct`: seriam boxed ao entrar em `ISimSystem[]`); o buffer interno de eventos **must** ser `SimEvent[]` com contador, e `Events` só o expõe como `ReadOnlySpan` em propriedade (span não pode ser campo de classe).
- `Forja.Simulation` **must never** ter estado `static` mutável (tabelas de streams, `SimMath` e tabelas de lookup são imutáveis): com "Enter Play Mode Options" sem domain reload, estado estático sobreviveria entre execuções. **Must never** registrar sistemas por reflexão (stripping do IL2CPP); registrar por referência direta no compositor.
- A conversão de `ScriptableObject` para structs de fase **must** ocorrer fora do asmdef da simulação (Gameplay ou apresentação).
- **Must** pré-alocar arrays no início da fase; **must never** alocar memória gerenciada dentro de `Tick` (sem LINQ, sem `new` de classe, sem lambda capturante, sem boxing).
- **Must** iterar por índice crescente; **must never** decidir ordem de efeito iterando `Dictionary` ou `HashSet`.
- **Must** escrever tempo em ticks inteiros dentro da simulação; **must never** acumular tempo em float entre ticks (contagem regressiva em ticks inteiros).
- A apresentação **must** só ler eventos e visões somente leitura; **must never** escrever no estado dos sistemas.
- Todo sistema novo **must** implementar `Hash` e entrar no teste de reprodutibilidade (mesma seed, mesmos comandos, duas execuções, mesmo hash).
- Testes ficam em `Assets/Tests/EditMode/Simulation/` e usam `Assets/Tests/PlayMode/` só para a ponte com a apresentação.

## Alternatives Considered

### Alternative 1: Ponto fixo (inteiros, Q-format, intermediários em 64 bits)
- **Description**: Posições, velocidades, dano e tempo em inteiros com formato Q (por exemplo Q16.16), multiplicação com intermediário em `long`, divisão e raiz por rotinas próprias.
- **Pros**: Mesmo resultado em qualquer runtime e arquitetura por construção; viabiliza replay validado por servidor, ranking por replay e auto-battle verificável sem trabalho extra (L326).
- **Cons**: Cada fórmula dos GDDs #6, #7 e #8 vira aritmética manual com risco de overflow e perda de precisão; mais código e mais bug para um dev solo; multiplica o custo dos testes de balanceamento; o ganho só é usado após o lançamento.
- **Rejection Reason**: O MVP só exige reprodutibilidade no mesmo build, e o custo recai antes de qualquer retorno. Fica como substituição registrada, disparada quando #22 ou #40 exigirem verificação entre dispositivos ou servidor.

### Alternative 2: DOTS com Burst e float
- **Description**: Simulação em Entities/Burst/Jobs, componentes blittable, sistemas paralelizados.
- **Pros**: Throughput alto para hordas muito grandes; ECS como modelo.
- **Cons**: Burst só aceita tipos blittable e restringe o C# da lógica; semântica de float sob Burst e determinismo de `Unity.Mathematics` são `NOT SOURCEABLE`; exige o modelo de ECS inteiro na equipe de um; os testes headless precisam do mundo ECS; o risco do Unity 6.3 (HIGH) cresce.
- **Rejection Reason**: Complexidade e risco desproporcionais para um dev solo antes de existir um aparelho de referência medido. Se o spike de performance mostrar que a horda não cabe em C# puro, este ADR é revisto com dado.

### Alternative 3: Tipo escalar próprio (`SimReal`) desde já, como hedge para o ponto fixo
- **Description**: Todo o código da simulação e as fórmulas usam um tipo `SimReal` (struct fino sobre `float` ou alias por arquivo) em vez de `float`; trocar o ponto fixo depois seria trocar a definição do tipo.
- **Pros**: A troca futura para ponto fixo fica quase mecânica no texto das fórmulas; responde de antemão à pergunta de quem lê "a troca ainda toca toda fórmula".
- **Cons**: C# 9 não tem `global using` (alias vale por arquivo); um struct fino adiciona ruído a cada operação e depende de otimização do IL2CPP/Mono para não custar em horda; paga-se o custo de legibilidade de todas as fórmulas por um gatilho (#22, #40) que pode nunca vir; o tipo não resolve overflow, precisão nem a ausência de funções transcendentais, que continuam sendo o trabalho real da troca.
- **Rejection Reason**: O custo é imediato e certo, o benefício é hipotético e parcial. `SimMath` e o vetor próprio já concentram as operações além de `+ - * /`; se o gatilho vier, o ADR de substituição decide se introduz o tipo então.

### Alternative 4: Outras taxas de tick (20 Hz e 60 Hz)
- **Description**: Manter a mesma arquitetura com `TicksPerSecond` de 20 ou 60.
- **Pros**: 20 Hz custa ainda menos CPU em Android; 60 Hz casa com o frame alvo, dispensa interpolação e dá precisão de esquiva e telegraph para o "Massacre com peso".
- **Cons**: 20 Hz põe hit e telegraph em granularidade de 50 ms e arrisca a sensação de combate; 60 Hz dobra o custo da horda no aparelho de referência, que ainda não foi verificado.
- **Rejection Reason**: 30 Hz é o meio-termo que cabe no orçamento móvel provável com interpolação; a taxa é uma constante e o ADR é reaberto se o spike de performance ou o playtest mostrarem que 30 Hz não serve. Nenhum GDD pode fixar valor "por tick": os dados usam segundos, o que mantém a troca barata.

### Alternative 5: Eventos por delegate ou função pura `Step(estado, comandos)`
- **Description**: (a) sistemas notificam por `event`/delegate direto; (b) a simulação como função pura que devolve novo estado e eventos.
- **Pros**: (a) liga fácil à UI; (b) fácil de testar e de repetir.
- **Cons**: (a) a ordem dos efeitos depende de quem assinou e dificulta teste headless; (b) copiar ou alocar o estado a cada tick pesa na horda em Android (GC) e exigiria pooling pesado.
- **Rejection Reason**: Buffer de eventos limpo por tick dá ordem determinística, zero alocação e leitura simples pela apresentação.

## Consequences

### Positive
- Fórmulas dos GDDs em float, sem aritmética manual: menor custo de design e de teste.
- Um único tick, uma única conversão de segundos para ticks e um único contrato de estado (`SimWorld`) para #3, #6, #7, #8 e o auto-battle (#40, futuro); o headless e o jogo montam a mesma lista de sistemas pelo mesmo compositor.
- Streams independentes: mudar a regra de loot não altera spawns nem ofertas da mesma seed, o que preserva as métricas de oferta do aceite.
- Teste headless chama o mesmo código do jogo, com hash para detectar divergência.
- Simulação sem engine roda em EditMode e é fácil de reaproveitar.

### Negative
- **Sem garantia cross-runtime.** Não há replay validado por servidor, nem ranking por replay, nem autoridade de host com este ADR. Se #22 ou #40 pedirem isso, é preciso um ADR de substituição (ponto fixo) que reescreve as fórmulas; `SimMath` e o vetor próprio reduzem, não eliminam, esse custo.
- **O teste headless no Editor (Mono, x64) não é o mesmo runtime do jogo (IL2CPP, ARM64).** As métricas de aceite da oferta são estatísticas e não dependem de igualdade bit a bit, mas um resultado do Editor não prova o resultado do aparelho até o spike de hash.
- Proibir funções transcendentais e `Unity.Mathematics` limita fórmulas (curvas, ângulos) e obriga tabelas.
- 30 Hz coloca o hit e o telegraph numa granularidade de 33 ms e exige interpolação na apresentação.
- Dois estados (anterior e atual) por entidade visível custam memória e cópia por tick.
- O `SimWorld` fixa em Core a forma mínima de uma entidade (id, posição, facção, HP, vivo): o ADR do #6 e do #7 só podem acrescentar colunas, e uma mudança de modelo (por exemplo handle com geração) é um novo ADR.
- Um APK com mais de uma ABI tem determinismo separado por ABI; o resultado de um auto-battle não pode ser rederivado da seed depois de um update.

## Risks
- **Float divergente no mesmo build** (fusão FMA, otimizações do IL2CPP): mitigação é o spike de hash no aparelho antes do vertical slice; se divergir, este ADR é reaberto com a alternativa de ponto fixo.
- **Valor de tempo em segundos que arredonda para 0 tick** (cooldown ou duração menor que ~17 ms): mitigação é a conversão ao inteiro mais próximo com mínimo de 1 tick e a validação de dados que recusa o valor.
- **Eventos perdidos numa horda grande:** `DroppedEvents` nunca descarta em silêncio; a capacidade do buffer vem dos dados da fase e é medida no spike de performance.
- **`MaxTicksPerFrame` baixo demais** deixa o jogo em câmera lenta em aparelho fraco; alto demais causa espiral: o valor inicial 4 é provisório e deve ser medido no aparelho de referência (ainda não verificado).
- **Sistema de gameplay referencia `UnityEngine` por descuido:** mitigação é o asmdef "No Engine References" e a revisão de `code-reviewer`.
- **Novo stream de RNG criado sem registro:** mitigação é a regra de registro e um teste que lista os ids.
- **Divergência por desenho entre Editor x64 e ARM64 IL2CPP.** O hash do Editor pode diferir do hash do aparelho sem que isso seja bug: este ADR só promete determinismo no mesmo build e no mesmo runtime. O spike registra o resultado e a divergência entre runtimes é aceita (não reabre o ADR) enquanto #22 e #40 não exigirem o contrário; divergência dentro do mesmo build reabre o ADR.
- **Validação do `unity-specialist` (5.5, 2026-11-03):** sem achado bloqueante. Notas incorporadas: regra de classe para sistemas, buffer `SimEvent[]`, zero estado `static` mutável, sem reflexão, spike em Release, e verificação de compilação de `ref struct` + `ReadOnlySpan`. As afirmações sobre asmdef sem engine, `ref struct` em interface e `Span` em Mono/IL2CPP são `NOT SOURCEABLE` em `docs/engine-reference/` e ficam como verificação, não como fato.
- **Revisão TD-ADR (5.6, 2026-11-03): CONCERNS na 1ª passada, sem REJECT.** Itens 1 a 10 e os menores foram revisados neste texto: Varredura fora da simulação (#15), "mesmo build" = mesmo binário e ABI, `SimWorld` com ids monotônicos, eventos só saída com `DroppedEvents`, drenagem após cada tick, #3 e #16 como `ISimSystem`, três asmdefs com compositor sem engine, segundos nos dados e ticks na simulação com arredondamento ao mais próximo, alternativas de taxa e de tipo escalar próprio, seed de stream por SplitMix64, `Spawn` por índice de wave, política de auto-battle sob as mesmas regras e estado anterior guardado pela simulação. As escolhas confirmadas pelo usuário (float32, 30 Hz, PCG32, `Tick` + buffer de eventos) não mudaram. A revisão do TD sobre o texto revisado não foi refeita.

## GDD Requirements Addressed

Os GDDs de sistema ainda não existem em disco; as linhas abaixo citam o conceito congelado e o índice. O requisito de cada GDD pendente é o esperado, e deve ser conferido quando o GDD existir.

| GDD System | Requirement | How This ADR Addresses It |
|------------|-------------|--------------------------|
| `design/gdd/game-concept.md` L326 | Separar simulação de apresentação: tick fixo, RNG com seed, lógica sem MonoBehaviour | Asmdef sem engine, `Tick(comandos)`, 30 Hz, PCG32 com seed mestre |
| `design/gdd/game-concept.md` L400 | Seeds determinísticas para spawn e oferta; simulação headless chama o mesmo código do jogo | Streams `Spawn` e `Offer`; teste EditMode chama `Simulation.Tick` |
| `design/gdd/game-concept.md` L323 | Composição das waves por seed | Stream `Spawn` independente de `Loot` e `Offer` |
| `design/gdd/game-concept.md` L246 | O auto-battle é simulação determinística por seed e pode falhar (a Varredura não simula: #15) | Mesma simulação, comandos vindos de uma política em vez do jogador (#40, futuro); determinismo do mesmo binário e da mesma ABI; o resultado se calcula e se credita de uma vez, nunca se rederiva da seed depois de um update |
| #3 Fluxo de fase e #16 Grimório (GDDs pendentes) | XP e level-up disparam a oferta; oferta, registro e substituição são o mesmo código no headless | Ambos são `ISimSystem` no compositor; oferta sorteia do stream `Offer` |
| #6 Combate e dano (GDD pendente) | Fórmulas de dano, cooldowns e telegraphs | Float32; segundos nos dados convertidos para ticks; `SimWorld` para HP e posição |
| #7 Horda, waves e inimigos (GDD pendente) | Spawn por seed, hordas grandes em Android | Stream `Spawn` por índice de wave; arrays pré-alocados, zero alocação por tick; `SimWorld` para as entidades |
| #8 Skills e evoluções (GDD pendente) | Efeitos de skill em ordem previsível | `ISimSystem` em ordem de registro fixa; comunicação pelo `SimWorld`, não por eventos |
| #5 Log de eventos e instrumentação (GDD pendente) | Registro dos eventos de combate para o aceite | Buffer de eventos limpo por tick, lido pelo log |
| #22 Ranking (GDD pendente) | Replay validado por servidor | **Não atendido**: exige ADR de substituição por ponto fixo (ver Negative) |

## Performance Implications
- **CPU**: tick de 30 Hz, metade do custo de um tick a 60 Hz; o orçamento em ms por tick **não é reivindicado aqui** (aparelho de referência não verificado), então nenhum orçamento é registrado; cada sistema recebe o seu na medição do spike de performance.
- **Memory**: arrays por fase pré-alocados com capacidade máxima vinda dos dados da fase; dois estados por entidade visível para interpolação.
- **Load Time**: nenhum impacto relevante; conversão de dados para structs no início da fase.
- **Network**: não se aplica.

## Migration Plan
Não se aplica: o projeto não tem código de jogo (`Assets/` só contém o modelo inicial do Unity). A estrutura de pastas e os asmdefs nascem com a primeira story de #2.

## Validation Criteria
- Teste de reprodutibilidade em EditMode: mesma seed e mesmos comandos, duas execuções, mesmo hash a cada 100 ticks, por pelo menos uma fase completa.
- Teste de independência dos streams: consumir N sorteios extras em `Loot` não altera a sequência de `Spawn` nem de `Offer`.
- Spike de hash entre Editor, Windows IL2CPP e Android IL2CPP ARM64: resultado registrado (iguais ou divergentes) neste ADR.
- Profiler: 0 B de alocação gerenciada por `Tick` em regime, no aparelho de referência.
- Compilação falha ao usar `UnityEngine` dentro do asmdef da simulação.

## Reavaliação prevista
O usuário aceitou as escolhas deste ADR por recomendação (float32, 30 Hz, PCG32, `Tick` + buffer de eventos, `SimWorld`, #3 e #16 como `ISimSystem`, segundos nos dados) sem dominar todos os conceitos, e pediu para reavaliá-las com o jogo avançado. Momento natural: depois do spike de performance e do spike de hash entre runtimes, com o vertical slice jogável. Até lá o ADR segue `Proposed`.

## Related
- `design/gdd/game-concept.md` (L246, L323, L326, L349, L400) e `design/gdd/systems-index.md` (#2, #5, #6, #7, #8, #22, #40).
- Sem outros ADRs. Candidatos de substituição: ADR futuro de replay e validação de ranking (#22) e de auto-battle (#40).
- `design/business-model.md` não depende deste ADR.
