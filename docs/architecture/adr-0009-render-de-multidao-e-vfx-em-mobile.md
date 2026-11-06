# ADR-0009: Render de multidão e VFX em mobile: leitura da simulação por frame, tempo de efeito igual ao tempo da simulação, horda instanciada, efeitos por shader com dados por instância, pools com corte por prioridade, telegraph no chão e pré-aquecimento do chefe

## Status
Proposed

## Date
2026-11-06

## Last Verified
2026-11-06 (contra o ADR-0001 com as Emendas 1 a 18, o ADR-0004, o ADR-0005, o ADR-0007, o ADR-0008, `docs/registry/architecture.yaml`, os GDDs #6 e #7 e o art bible `design/art/art-bible.md` (Seções 2.2, 5.5, 8.3 a 8.9) em disco; Unity 6.3 LTS, pin 6000.3.x). **O spike de performance ainda não foi rodado e o aparelho de referência não está verificado** (`VERSION.md`; `technical-preferences.md` com a memória "TO BE CONFIGURED").

## Decision Makers
Rodrigo Reis (escolheu este ADR, confirmou em 2026-11-06 o escopo "arquitetura agora, com o spike como portão" e mandou revisar os pontos do gate; o resto é decisão técnica por recomendação, **provisória, a reavaliar com o resultado do spike e o jogo jogável**), Claude Code (autoria), `unity-specialist` (validação, 5.5) e `technical-director` (gate TD-ADR, 5.6; veredito CONCERNS, tratado nesta revisão).

## Summary
O jogo precisa desenhar cerca de 300 corpos de horda mais mortes, nascimentos, telegraphs e efeitos aliados num celular Android intermediário, e três documentos pedem isso sem dizer como: o GDD #6 (efeitos por shader, pools, overdraw, corte por prioridade), o GDD #7 (horda com 1 draw por tipo, pool de fantasmas, pré-aquecimento do chefe) e o art bible (horda ≤ 400 triângulos, `RenderMeshInstanced`, nunca `SkinnedMeshRenderer`). Nenhum ADR define a fronteira entre a simulação e a imagem. Decidido: a apresentação só **lê** a simulação (uma vez por frame no `LateUpdate`, mais um ponto de captura depois de cada tick para as mortes), mede o tempo de todo efeito em **ticks da simulação** (`SimTickF`, nunca `Time.time`), desenha a horda como uma **malha estática de partes rígidas por `RenderMeshInstanced`** (1 draw lógico por tipo) com os dados por instância (nascimento, morte, dano, fase da animação) numa **textura de float lida por `SV_InstanceID`**, trata flash, dissolve e nascimento como função desses dados, limita cartões e fantasmas por **pools de tamanho fixo** com uma política de corte por prioridade (telegraph > herói > elite e chefe > aliados > horda), desenha o telegraph como **quad no chão** e pré-aquece os assets do chefe na entrada da fase, antes do `Create`. Todo ponto que a referência local não cobre vira Verification Required com plano B e gatilho, e a story de render não fecha sem o spike.

## Engine Compatibility

| Field | Value |
|-------|-------|
| **Engine** | Unity 6.3 LTS (6000.3.x; editor instalado 6000.3.27f1) |
| **Domain** | Rendering (URP, instancing, shaders, VFX, mobile) |
| **Layer** | Presentation (a lista de Required ADRs de `architecture-review-2026-11-06.md`, linha 231, classifica como Presentation; não existe `docs/architecture/architecture.md` nem mapa de camadas, então a camada é **provisória, a reavaliar**) |
| **Knowledge Risk** | HIGH (a linha do engine é HIGH em `VERSION.md`; `modules/rendering.md` cobre URP, RenderGraph, GPU Resident Drawer e o SRP Batcher de forma genérica e `RenderMeshInstanced` só com `NativeArray<Matrix4x4>`; o resto do que este ADR usa **não é coberto por nenhum arquivo de `docs/engine-reference/unity/`**) |
| **References Consulted** | `docs/engine-reference/unity/VERSION.md`, `breaking-changes.md`, `deprecated-apis.md`, `modules/rendering.md`; ADR-0001 (FS2, `SimEvent`, Emendas 17 e 18, L210 `DeathsThisTick`), ADR-0004 (colunas do `SimWorld`, `ICombatReadView`, `IsAlive`, Regra 4), ADR-0005 (Seção 7, `SimEventKind`), ADR-0007 (`PhaseHost.Alpha`, ordem do frame, Decisão 6), ADR-0008 (`ICounterSource`, `NoteKind`); GDD #6 (Visual/Audio Requirements, prioridade quando a tela lota, assets de `/asset-spec`, hit-stop L412 e L440), GDD #7 (Visual/Audio, "Restrições de arte", Regras 7 e 10, AC-P4, L182, L530, L796); art bible 2.2, 5.5, 8.3 a 8.9. **Não existe `modules/core.md`**; `current-best-practices.md` não foi usado. |
| **Post-Cutoff APIs Used** | Nenhuma API nova de Unity 6 é essencial: `Graphics.RenderMeshInstanced` e `RenderParams` existem desde a 2022.1 (conhecimento do especialista, não da referência local), e **este ADR não escreve passe de render customizado, então não usa RenderGraph**. Usa `ShaderVariantCollection.WarmUp` e o GPU Resident Drawer (só para o ambiente, nunca para a horda). O comportamento no 6000.3.27f1 e no Android é **`NOT SOURCEABLE`** salvo onde `modules/rendering.md` o descreve (Verification Required 1 a 10). O código novo fica em **C# 9**. |
| **Verification Required** | (1) `NOT SOURCEABLE`: **como o shader lê os dados por instância** (nascimento, morte, dano, fase da animação) no `RenderMeshInstanced` no Android. Caminho primário: uma **textura de float** pequena (`RGBA32F`, 2 texels por instância) indexada por `SV_InstanceID`, escrita uma vez por frame; plano B1: um `GraphicsBuffer` estruturado lido por `SV_InstanceID` (exige GLES 3.1 ou Vulkan); otimização: o struct de instância com os campos depois da matriz, **só se o spike provar o mecanismo de leitura no shader** (não documentado como contrato estável; no Shader Graph exige HLSL manual); último recurso: `RenderMeshIndirect`. Medir também o que `SV_InstanceID` vale quando o draw se divide em lotes e com `startInstance`. (2) `NOT SOURCEABLE`: **300 vivos + até 300 fantasmas por tipo**: o **número real de draws** (a Unity divide o draw em lotes pelo limite do aparelho: UBO de 64 KB no GLES 3.0, SSBO onde houver), ms de CPU na montagem dos arrays e ms de GPU no aparelho de referência no minuto 20 (estrangulamento térmico). (3) `NOT SOURCEABLE`: animação da horda por **partes rígidas com matrizes em textura** contra **VAT**. (4) `NOT SOURCEABLE`: `MaterialPropertyBlock` com o SRP Batcher para elite e chefe (o MPB tira o renderer do SRP Batcher; aceitável para poucos). (5) **Overdraw médio ≤ 2,5× e pico local ≤ 4×**, medido no Rendering Debugger, com 150 cartões aliados e o telegraph. **Gatilho: se falhar, reduzir primeiro `ALLY_CARD_MAX` e o alfa dos aliados (os botões já existem) e depois reabrir o art bible 8.7 com o autor.** (6) `NOT SOURCEABLE`: telegraph como quad de chão **contra** o URP Decal. (7) `NOT SOURCEABLE`: **pré-aquecimento do chefe**: o frame do tick do rugido cabe no orçamento (AC-P4 do #7), no minuto 20; o desenho do chefe fora da tela é o que aquece o estado de pipeline (`ShaderVariantCollection.WarmUp` só compila variantes); custo da troca de LUT por Volume em Android intermediário. **Gatilho: se falhar mesmo com o pré-aquecimento completo, deixar o chefe instanciado e oculto desde a entrada da fase e reabrir a Decisão 8.** (8) Zero alocação gerenciada por frame no `RenderFrameBuilder`, nos pools e em `OnTick`, em IL2CPP. (9) `NOT SOURCEABLE`: VFX Graph **contra** o sistema de partículas para os poucos estados com partícula (art bible 2.4 a 2.7); nenhum estado de combate usa partícula. (10) `NOT SOURCEABLE`: GPU Resident Drawer em mobile, só para o ambiente; ASTC 6×6 e 4×4 no importador e no aparelho; Vulkan/GLES 3.1 no aparelho de referência (decide o plano B1). (11) **Precisão na GPU:** `SimTickF` e os ticks por instância chegam a cerca de 36.000 aos 20 minutos; em `half`/`mediump` o passo passa de 32 acima de 32.768, então as contas de idade são `float` (highp) e a textura é de 32 bits; testado no contrato dos shaders. **Gatilho dos itens 1 e 2: se falharem nos caminhos primário, B1 e na otimização, a Decisão 4 reabre e o `teto_vivos_horda` do #7 entra em revisão com o autor.** |

## ADR Dependencies

| Field | Value |
|-------|-------|
| **Depends On** | ADR-0001 (`Proposed`; `SimWorld`, `Alpha` da FS2, `SimEvent`, `DrainEvents`, `DeathsThisTick`), ADR-0004 (`Proposed`; colunas `PosX/PosY/PrevPosX/PrevPosY`, `Classes`, `ArchetypeIds`, `BirthCombatTicks`, `IsAlive`, linhas de morto não recicladas, `ICombatReadView`), ADR-0005 (`Proposed`; eventos de elite, chefe e `HordeTick`), ADR-0007 (`Proposed`; `PhaseHost`, `Alpha`, `LateUpdate`, pausa) e **ADR-0008 (`Proposed`; `ICounterSource` e `NoteKind`)**. Este ADR só pode ser aceito depois dos cinco. ADR-0002, ADR-0003, ADR-0006: nenhuma dependência. **Contrato pendente:** o GDD #12 (Feedback, VFX e HUD) não existe; este ADR entrega o contrato que ele implementa (pools, corte, pré-aquecimento). |
| **Enables** | GDD #12 (dono do VFX e do HUD), ADR de orçamento de frame (recebe o `LoadLevel` e os números do spike), as stories de render do #6 e do #7, a lista de assets de `/asset-spec` |
| **Blocks** | Stories de render da horda, dos efeitos de combate, do telegraph e do pré-aquecimento; TR-combate-018, TR-horda-014 e TR-horda-015 (hoje "❌ GAP"). |
| **Ordering Note** | **Emendas pedidas, a escrever junto com a aceitação deste:** (A) **ADR-0004**: `ICombatReadView` ganha `UltimoDanoTick` por id (o GDD #6, Visual/Audio, manda a apresentação lê-lo para o flash de cada corpo da horda e a vista de hoje não o traz). **Custo declarado:** é estado persistente entre ticks, então pela Regra 4 do ADR-0004 (coluna persistente fora do hash é estado oculto) ele entra no `Hash` do #6 e **o golden hash do #6 muda**. `Pesado` **não** é pedido: nada neste ADR o consome. **Sem a emenda, o flash por corpo da horda fica desligado** (não é um corte da Decisão 6 e não soma em `HordeFlashCut`). (B) **ADR-0007**, Decisão 6, passo 7: o `PhaseHost` entrega ao `IPresentationSink` os eventos **e** `DeathsThisTick` depois de **cada** tick, **inclusive o tick que encerra a fase, antes de parar o laço no `Ended`** (a lista é limpa a cada tick, então só dá para capturá-la ali). (C) **ADR-0008**: o enum `NoteKind` ganha `PrewarmIncomplete = 8` (o próximo livre), e a presentation implementa `ICounterSource` com ids próprios. O orçamento de carregamento, os grupos do Addressables e o teto de memória são do ADR de orçamento de frame (depois do spike); aqui só o contrato de pré-aquecimento. |

## Context

### Problem Statement
O GDD #7 quer ~300 corpos vivos no teto, cada um nascendo, apanhando e morrendo; o GDD #6 quer flash, dissolve, telegraph e cartões de efeito; e o art bible limita tudo a 150 draw calls, 300 mil triângulos por frame, overdraw médio de 2,5× e zero efeito ou som por corpo. Isso só cabe num celular se (a) a horda for instanciada, nunca um objeto por inimigo, (b) cada efeito for função de dados que a simulação já tem, e (c) o excesso for cortado por regra, não por acaso. Hoje nenhum ADR define a fronteira entre a simulação e a imagem, os requisitos TR-combate-018, TR-horda-014 e TR-horda-015 estão sem ADR, e a referência local não cobre quase nada do que o render móvel usa. Há ainda um problema de correção: a simulação morre num tick e a lista de mortes é limpa a cada tick, então quem desenha o dissolve precisa capturá-la a cada tick, não uma vez por frame.

### Constraints
- ADR-0001: a apresentação só lê; a posição anterior não é escrita fora do Core; `Alpha` vem da ponte; eventos são só saída; nenhum evento por corpo de horda (ADR-0005); `DeathsThisTick` é limpa a cada tick.
- ADR-0004: ids nunca reutilizados; a linha de um morto não é reciclada; os spans têm comprimento `IdCount`; todo consumidor filtra por `IsAlive` antes de usar coluna privada; um span não pode ser guardado em campo, lambda, coroutine ou `async`; coluna persistente fora do hash é estado oculto.
- ADR-0007: a apresentação lê no `LateUpdate`; a pausa congela o `Alpha`; nada de `Time.timeScale`; `PhaseHost` chama o sink depois de cada tick.
- Art bible 8: horda ≤ 400 triângulos, 1 LOD, partes rígidas (até 12 partes, 1 influência), nunca `SkinnedMeshRenderer`, ≤ 3 tipos por capítulo; ≤ 150 draws no total; ≤ 300k triângulos; overdraw médio ≤ 2,5×; ≤ 150 cartões aliados; hit-flash e dissolve por shader com propriedade por instância, nunca partícula; telegraph como quad no chão; sombra só de herói e chefe. **Todos provisórios até o spike.**
- GDD #7: nenhum efeito, decal ou som por corpo nascido; pré-aquecer o chefe; pool de ~300 fantasmas, o excedente some.
- Dev solo, uma pessoa valida: poucas classes, nenhuma ferramenta nova.
- Aparelho de referência não verificado; o orçamento de frame (~12 ms) é provisório.

### Requirements
- Cumprir TR-combate-018, TR-horda-014 e TR-horda-015 sem mudar a decisão dos GDDs além do registrado em GDD Sync.
- Nenhum estado de render pode alterar a simulação, o hash ou o log.
- Pausa, hit-stop e o congelamento de combate (`CombatHold`) param os efeitos sozinhos, sem código por efeito.
- Zero alocação gerenciada por frame no caminho quente.
- O excesso de efeitos é cortado por uma regra de prioridade testável em EditMode.
- Cada premissa não coberta pela referência é medida, tem plano B e tem gatilho.

## Decision

### 1. Fronteira, camadas e a regra de ouro
- **Lógica pura** em `Forja.Gameplay.Sim.View` (C# 9 sem `UnityEngine`; mesmo asmdef do `TentativaDeFase`, namespace à parte dos sistemas de tick): `EffectClock`, `RenderFrameBuilder` (monta os dados de instância a partir dos spans), `VfxBudget` (tetos e corte por prioridade), `GhostPool` e `CardPool` (índices e vida; sem objetos Unity), `PrewarmPlan`. Roda em EditMode.
- **Unity** em `Forja.Gameplay.Presentation` (dentro do asmdef `Forja.Gameplay`): `CrowdRenderer` (o `RenderMeshInstanced`), `TelegraphRenderer`, `CardRenderer`, `ShaderGlobals`, `PrewarmRunner` e o `PresentationDriver` (`LateUpdate`, implementa o `IPresentationSink`).
- **Regra de ouro:** a apresentação **nunca escreve** na simulação, nunca chama `Tick`, `Spawn` nem `Kill`, e nada que ela guarda entra no hash ou no log como estado de jogo. `Forja.Simulation` e os sistemas chamados por `ISimSystem.Step` **nunca** referenciam `Forja.Gameplay.Sim.View` nem `Forja.Gameplay.Presentation`. Como `Sim.View` vive no mesmo asmdef dos sistemas de tick, isso é regra de revisão **registrada em `forbidden_patterns`**; um asmdef próprio que referencia o Sim e não é referenciado por ele a tornaria erro de compilação (decisão de projeto pendente, a mesma de `Sim.Log` do ADR-0008).
- **Fora do escopo:** o render do herói, do elite e do chefe como `SkinnedMeshRenderer` (peças fundidas, raridade por material: art bible 8.6); o ambiente, a iluminação e a escala de render; a UI; o háptico e o tremor de câmera (TR-combate-019, na lista "depois"); o orçamento de carregamento e memória. Este ADR cobre a multidão, os efeitos de combate e o pré-aquecimento do chefe, **e a regra do relógio dos efeitos** (Decisão 3) que o render do herói e do elite herda.

### 2. Leitura da simulação: duas capturas, nenhuma escrita
- **Captura por tick** (`IPresentationSink.OnTick`): o `PhaseHost` (ADR-0007, passo 7) chama `OnTick(combatTick, events, deaths)` **depois de cada** `Tick` e do `DrainEvents()`, **inclusive no tick que encerra a fase e antes de parar o laço** (Ordering Note B), com `events` (`ReadOnlySpan<SimEvent>`) e `deaths` (`ReadOnlySpan<DeathRecord>` de `DeathsThisTick`, limpa a cada tick). O sink só **copia** para estruturas de tamanho fixo: para cada morte de `EntityClass.Horda`, um fantasma no `GhostPool` com `id`, `archetypeId`, posição lida da linha do morto (não reciclada) e `deathTick`; para cada evento de elite ou chefe (`Damage`, `Death`, `HitStop`, `TelegraphStart`, `Esquiva`, `Rugido`), um pedido de efeito no `CardPool`. Nenhum desenho acontece aqui.
- **Captura por frame** (`PresentationDriver.LateUpdate`, depois de todos os ticks do `Update` do `PhaseHost`): pega **uma vez** cada span necessário numa variável local (`PosX`, `PosY`, `PrevPosX`, `PrevPosY`, `Classes`, `ArchetypeIds`, `BirthCombatTicks`, `IsAlive` e a `ICombatReadView`), nunca dentro do laço por entidade e nunca em campo, e monta os dados de instância. Os spans valem até o próximo `Tick`; o `LateUpdate` roda antes dele.
- **Interpolação (FS2):** `pos = prev + (atual − prev) × Alpha`, com o `Alpha` do `PhaseHost` (congelado na pausa, ADR-0007). O render nunca extrapola. Uma entidade recém-nascida tem `prev = atual`.
- **Estado só da apresentação** (vetores de tamanho `EntityCapacity`, criados na tela de carregamento, fora do hash): `lastFacing[id]` (orientação a partir de `atual − prev`, mantida quando parado). Nada mais. Nenhum campo `static` mutável (com domain reload desligado, estado estático persistiria entre Play Modes; o que existir é zerado em `[RuntimeInitializeOnLoadMethod(SubsystemRegistration)]`).

### 3. Tempo de efeito = tempo da simulação (`EffectClock`)
- `SimTickF = max(SimTickFAnterior, CombatTick + (CombatHold == 0 ? Alpha : 0))`, publicado **uma vez por frame** com `Shader.SetGlobalFloat(_ForjaSimTick, SimTickF)`. O `max` evita um passo para trás de até 1 tick quando o combate retém (`CombatHold`); na pausa o `Alpha` está congelado, então `SimTickF` não anda.
- **Todo efeito de combate é função de `SimTickF` e de ticks guardados na instância ou no cartão**: `idade = (SimTickF − tickInicio) / duracaoTicks`. **Nenhum shader de combate lê `_Time`, e nenhum código de combate lê `Time.time` ou `Time.deltaTime`.** Resultado: a pausa, o menu de oferta de carta e o `CombatHold` congelam dissolves, flashes e telegraphs sem nenhum código por efeito.
- **Hit-stop.** A duração do hit-stop (3 ticks, GDD #6) **também se mede em `SimTickF`**: a pose do herói e do alvo congela por 3 ticks da simulação. O render do herói e do elite que o implementa está fora deste ADR; a regra do relógio é deste. Como o relógio global **congela** no `CombatHold` (e na pausa), o hit-stop em curso **congela junto**, em vez de ser cancelado. O GDD #6 (L412 e L440) manda o #12 *cancelar* o hit-stop quando `CombatHold ≠ 0`; é uma diferença de comportamento, **registrada em GDD Sync para o autor decidir**, e o padrão deste ADR é congelar (provisório).
- **Precisão.** As contas de idade no shader são `float` (highp) e a textura de instância é de 32 bits: `SimTickF` chega a cerca de 36.000 aos 20 minutos, e em `half` o passo passa de 32 acima de 32.768. O teste de contrato dos shaders falha se essas contas declararem `half` ou `fixed`.
- `BirthCombatTicks` é o `CombatTick` do `Spawn` (ADR-0001, Emenda 17), então o nascimento do GDD #7 (4 a 6 ticks, dissolve invertido) é `idade` desde esse valor, sem evento.
- Animação de UI, menus e a tela de resultado usam relógio próprio (`unscaledDeltaTime`) e ficam fora desta regra.

### 4. A horda: uma malha estática de partes rígidas, instanciada
- **Um draw lógico por tipo de horda** (≤ 3 tipos por capítulo): para cada `archetypeId`, uma `Mesh` estática (≤ 400 triângulos, 1 LOD) com as até 12 partes rígidas fundidas e o índice da parte em vertex color; um `Material` (uma variante de shader, sem keyword por raridade nem por estado); e uma chamada `Graphics.RenderMeshInstanced` com `RenderParams` por frame. **Nunca `SkinnedMeshRenderer`, nunca um `GameObject` por inimigo** (art bible 8.6). **"Um draw por tipo" é lógico:** a Unity divide o draw em lotes pelo limite do aparelho (UBO de 64 KB no GLES 3.0, SSBO onde houver; `NOT SOURCEABLE`), então com 300 vivos mais 300 fantasmas por tipo o número real de draws pode ser 2 por tipo; o spike mede o número real (Verification Required 2) e o teto de 150 draws do art bible se compara com ele.
- **`RenderParams`:** `worldBounds` definido **uma vez** como a área jogável da fase com folga (o `RenderMeshInstanced` não faz culling por instância e usa um único bounds por lote; o padrão vazio pode descartar o draw inteiro); `shadowCastingMode = Off` e `receiveShadows = false` (a horda não projeta sombra: art bible, sombra só de herói e chefe); o teste de caixa por instância na CPU continua (abaixo).
- **Dados por instância:** o `RenderFrameBuilder` (puro) produz `HordeInstanceData` (posição interpolada, orientação, `birthTick`, `deathTick` (−1 se vivo), `hitTick`, `animPhase`, `deathKind`) sem nenhum tipo da Unity. O `CrowdRenderer` (Unity) escreve a **matriz** em um `NativeArray<Matrix4x4>` (o que a referência cobre) e os **dados extras numa textura de float** (`RGBA32F`, 2 texels por instância, via `SetPixelData` com um array persistente), e o shader lê esses dois texels por `SV_InstanceID`. Esse é o caminho **primário**: não depende de nenhuma ligação não documentada entre campo C# e propriedade HLSL, e funciona em GLES 3.0. **Plano B1:** `GraphicsBuffer` estruturado (GLES 3.1/Vulkan). **Otimização, só se o spike provar o mecanismo de leitura no shader:** os campos extras num struct de instância depois da matriz (`HordeInstance { Matrix4x4 ObjectToWorld; Vector4 Fx; }`, o primeiro campo sendo a matriz). **Último recurso:** `RenderMeshIndirect`. Escolhe-se o primeiro que passa os itens 2 e 3 do spike, e o desenho do `RenderFrameBuilder` não muda (só o escritor final).
- **Animação:** partes rígidas, matrizes numa textura de ossos compartilhada, lidas no vértice por `animPhase` e pelo índice da parte (decisão do usuário, art bible 8.9); o spike compara com VAT (Verification Required 3). `animPhase` vem de `SimTickF` e do passo do arquétipo, não de `Time`.
- **Quem entra:** vivos de `Classes == Horda` (por `IsAlive`) **dentro do retângulo da câmera no plano do chão** (teste de caixa na CPU antes de montar o array), mais os fantasmas ativos do `GhostPool`. O array é **escrito em ordem de id crescente** (determinismo do desenho, sem ordenar).
- **Fantasmas** (mortes da horda): ficam no mesmo draw, com `deathTick` preenchido (V ≤ 30, GDD #6); o dissolve de 8 a 10 ticks é o do shader. O pool tem tamanho fixo `GHOST_POOL_MAX` (padrão provisório 300). **Excedente: some na hora, sem fade.** Uma morte sem vaga no pool não tem instância viva (o corpo morto sai do array no frame seguinte, pelo filtro `IsAlive`) nem fantasma para esmaecer; soma em `GhostPoolOverflow` (contador do log, Decisão 9). O GDD #7 e o #6 dizem "some com fade direto"; a diferença está registrada em GDD Sync, e o fade custaria um segundo pool de fantasmas curtos, adiado até o autor pedir. Nas mortes pelo `Rugido`, os dissolves começam escalonados pela distância ao chefe (atraso de até ~10 ticks) e o excedente é o dos mais distantes (GDD #7).
- **Zero custo por corpo fora da instância:** nenhum som, partícula, decal, `Animator`, `Collider` ou componente por corpo.

### 5. Efeitos por shader com propriedade por instância
- **Nascimento, flash e dissolve da horda** são o **mesmo shader** (`shd_enm_dissolve` e o da horda, GDD #6/#7) lendo os dados de instância: nascimento = dissolve invertido enquanto `idade desde birthTick < 6`; flash = branco-frio (H 200–230, S ≤ 15) enquanto `idade desde hitTick < 2`; dissolve = de `deathTick` por 8 a 10 ticks, V ≤ 30 inclusive na borda. Nada disso é partícula (art bible 8.7).
- **Flash por corpo exige `hitTick`**, que vem de `UltimoDanoTick` da `ICombatReadView`, que **a vista de hoje não tem** (Ordering Note A). Enquanto a emenda ao ADR-0004 não existir, `hitTick` vai sempre −1 e o **flash da horda fica desligado** (o `Damage` agregado só toca som, GDD #6). Isso não bloqueia nenhum outro efeito.
- **Elite e chefe** (poucos renderers): `MaterialPropertyBlock` com `hitTick` e `deathTick` vindos de `Damage`/`Death` (flash S ≤ 20, V ≤ 55, até 2 ticks; dissolve na morte). O MPB tira esses renderers do SRP Batcher (Verification Required 4); com poucos renderers é aceitável, e o plano B é uma instância de material por elite.
- **Propriedades com nomes fixos** (`Shader.PropertyToID` em campos `static readonly`; os IDs são estáveis na sessão, então com domain reload desligado são inofensivos): `_ForjaSimTick`, `_ForjaInstanceTex`, `_ForjaPartMatrices`, `_ForjaFlashTint`; mudar um nome exige mudar o shader e o teste de contrato.

### 6. Cartões, pools e o corte por prioridade (`VfxBudget`)
- **Cartões** (arco do auto-ataque, rastro do dash, arco pesado, rastro de esquiva, onda do rugido, cartões aliados): quads de **um único `Mesh` de quad** desenhados por `RenderMeshInstanced`, um draw lógico por material, com `tickInicio` e `duracaoTicks` por instância (a mesma textura de dados); sem `GameObject` por cartão. `CardPool` tem tamanho fixo `ALLY_CARD_MAX` (150, art bible 8.7) para aliados e `CARD_POOL_MAX` para os demais (padrão provisório 32). Alfa de aliado ≤ 0,85, nenhum cartão acima de 10% da tela.
- **Ordem de desenho dos transparentes.** Dentro de um `RenderMeshInstanced` não há ordenação por instância: a ordem é a do array. O `RenderFrameBuilder` **escreve o array de cartões ordenado por `tickInicio`** (o mais antigo primeiro), e o telegraph usa um material com `renderQueue` maior que o dos cartões e `ZWrite Off`. Decals sobrepostos se ordenam por Impacto mais próximo no topo, sem blend aditivo. Cartões aliados sobre a área do telegraph ficam com alfa ≤ 0,6.
- **Prioridade** (GDD #6): telegraph > herói > elite e chefe > aliados > horda. **O corte é na ordem inversa:** (1) a horda perde o flash e o dissolve (vira fade); (2) os aliados perdem cartões, os mais antigos primeiro (fila circular). **Telegraph e herói nunca perdem nada.**
- **`VfxBudget` é uma função pura**: entra com os pedidos por categoria, os tetos (`BudgetCaps`) e um `LoadLevel` (`Normal = 0`, `Alto = 1`) e devolve quanto cada categoria pode desenhar e quem é cortado; roda em EditMode. O `LoadLevel` real (a partir do p95 do frame) é do **ADR de orçamento de frame** (`NOT ASSESSED` aqui): até lá o nível é sempre `Normal`, e os cortes valem só pelos tetos fixos.
- **Os tetos medidos pelo spike**: overdraw médio e pico, draws, triângulos. Nada disso se mede em execução; o `Rendering Debugger` e o `Frame Debugger` são ferramentas de spike, não de jogo.

### 7. O telegraph é um quad no chão
- Cada telegraph ativo (`EstadoCombate == Aviso` e `Forma != Nenhuma`, lidos de `ICombatReadView`, filtrando por `IsAlive`) é uma instância de um `Mesh` de quad no plano do chão, orientado e escalado por `Forma` (`Circulo`, `Cone`, `Linha`), `Raio`, `Origem`, `Dir` e `Destino`; material transparente, unlit, `#FF4A1C` com alfa 0,70, hachura e serrilha; a frente cresce em `A` ticks como função de `SimTickF` e do `TimerTicks`; a cauda de apresentação de 3 ticks depois do Impacto. Até `max_avisos` instâncias (padrão 3, até 6), num único draw. Sem partículas (art bible 2.2).
- **Não é URP Decal** (`NOT SOURCEABLE`; Verification Required 6). Se o spike mostrar folga e o Decal ficar melhor, a troca é interna ao `TelegraphRenderer`.
- A ordem entre o decal e o LUT do chefe é do technical-artist (art bible 4.2); o decal é unlit e o LUT do chefe não o escurece.

### 8. Pré-aquecimento do chefe (contrato; TR-horda-015)
- **Quando:** na entrada da fase (estado *Entrando* do #3, quando o jogador toca Entrar), **em paralelo com o pedido do `BeginStage`** e **antes do `Simulation.Create`**. "Em paralelo" vale só para a **E/S assíncrona** (carga de assets); o aquecimento de shader e o desenho fora da tela rodam na thread principal ou de render, dentro da tela de carregamento.
- **O `PrewarmPlan` da fase, em ordem:** (1) carrega o modelo, os materiais e as texturas do chefe do capítulo e os deixa residentes; (2) compila as variantes de shader da horda, do chefe, dos cartões e do telegraph (`ShaderVariantCollection.WarmUp`, `NOT SOURCEABLE`); (3) carrega o perfil de Volume do LUT do chefe e o do estado de combate; (4) **desenha uma vez, fora da tela, o chefe e o disco do rugido: obrigatório, não opcional**, porque a compilação de variantes não cria o estado de pipeline e é o desenho que o aquece; (5) pede ao áudio que decodifique os clipes do rugido (o áudio é do audio-director).
- **Espera e teto.** O host aguarda o fim do plano até `PREWARM_MAX_WAIT_MS` (padrão provisório 3000) **depois** da confirmação do `BeginStage`, na tela de carregamento. Passado o teto, a fase **começa mesmo assim** (o pré-aquecimento nunca trava o jogo): **a carga continua em segundo plano**, o host grava `HostNote PrewarmIncomplete` no log (Ordering Note C) e soma `PrewarmIncompleteCount`. **No spike, um `PrewarmIncomplete` conta como falha do AC-P4**; fora do spike, o rugido pode pagar parte da carga e isso fica medido no log.
- **`PrewarmRunner`** aceita um `CancellationToken` (a Unity não espera uma `Task` ao sair do Play Mode ou da fase) e **pode alocar** (state machine, `Task`): o carregamento está fora do caminho quente, a regra de zero alocação por frame não se aplica a ele. Se o projeto já usa `Awaitable`, coroutine ou o handle do Addressables, prefere-se o que o resto usar.
- O custo do pré-aquecimento e o frame do tick do rugido são o AC-P4 do #7 e a Verification Required 7. O Addressables (como carregar) e o teto de memória são do ADR de orçamento de frame.

### 9. Contadores de render no log (#5)
A apresentação implementa `ICounterSource` (ADR-0008) com ids próprios num enum de valores explícitos que só cresce: `GhostPoolOverflow = 1` (mortes de horda sem fantasma), `AllyCardsCut = 2`, `HordeFlashCut = 3` (só cortes da Decisão 6; **não** conta o flash desligado por falta da emenda), `PrewarmMs = 4`, `PrewarmIncompleteCount = 5`, `MaxHordeInstances = 6` (maior número de instâncias num frame), `MaxGhostsActive = 7`, `MaxDrawBatches = 8` (maior número real de lotes num frame; alimenta a Verification Required 2). Servem ao aceite e ao spike; não influenciam nada.

### Architecture Diagram
```
 Simulation / SimWorld (thread principal, so leitura para a apresentacao)
   spans: PosX/Y, PrevPosX/Y, Classes, ArchetypeIds, BirthCombatTicks, IsAlive ; ICombatReadView (#6) ; DeathsThisTick ; DrainEvents
        │                                             │
        │  depois de CADA Tick (PhaseHost, ate o do Ended)  │  uma vez por frame (LateUpdate)
        ▼                                             ▼
  IPresentationSink.OnTick(events, deaths)      PresentationDriver  ── SimTickF = max(.., CombatTick + Alpha*(CombatHold==0))
   copia para GhostPool / CardPool                     │             Shader.SetGlobalFloat(_ForjaSimTick)  (float / highp)
   (sem desenhar)                                      ▼
                                          RenderFrameBuilder (C# puro, EditMode)
                                           ├─ horda viva + fantasmas ─▶ matriz (NativeArray) + textura de dados (SV_InstanceID) ─▶ RenderMeshInstanced
                                           │                            (1 draw logico por tipo; N lotes pelo limite do aparelho; worldBounds da area jogavel)
                                           ├─ cartoes (ordenados por tickInicio) ─▶ RenderMeshInstanced (1 draw logico por material)
                                           ├─ telegraphs (<= max_avisos) ─▶ quad de chao, renderQueue maior, 1 draw
                                           └─ VfxBudget(pedidos, BudgetCaps, LoadLevel) ─▶ corte por prioridade
   Planos: primario = textura de instancia | B1 = GraphicsBuffer | otimizacao = struct depois da matriz | ultimo recurso = RenderMeshIndirect
   Pre-aquecimento (PrewarmRunner) : Entrando -> em paralelo (E/S) com BeginStage -> antes do Create ; teto PREWARM_MAX_WAIT_MS ; carga continua depois do teto
 Forja.Gameplay.Sim.View (C# puro, EditMode): EffectClock, RenderFrameBuilder, VfxBudget, GhostPool, CardPool, PrewarmPlan
 Forja.Gameplay.Presentation (Unity):          PresentationDriver, CrowdRenderer, CardRenderer, TelegraphRenderer, ShaderGlobals, PrewarmRunner
```

### Key Interfaces
```csharp
namespace Forja.Gameplay.Sim.View   // C# 9 puro, sem UnityEngine; outro namespace que o dos ISimSystem; EditMode
{
    public interface IPresentationSink   // chamado pelo PhaseHost depois de CADA Tick e do DrainEvents, ate o tick do Ended (ADR-0007, passo 7); so copia, nunca desenha
    {
        void OnTick(int combatTick, System.ReadOnlySpan<SimEvent> events, System.ReadOnlySpan<DeathRecord> deaths);
    }

    public static class EffectClock   // funcao pura
    {
        public static float SimTickF(float previous, int combatTick, int combatHold, float alpha);   // max(previous, combatTick + (combatHold==0 ? alpha : 0))
    }

    public struct HordeInstanceData   // saida do RenderFrameBuilder; so floats e inteiros, sem tipo da Unity
    {
        public int ArchetypeSlot;                                // qual dos <= 3 tipos (qual draw logico)
        public float X, Y, FacingX, FacingY;                     // posicao interpolada (FS2) e orientacao
        public float BirthTick, DeathTick, HitTick, AnimPhase;   // DeathTick = -1 se vivo; HitTick = -1 sem a emenda ao ADR-0004
        public float DeathKind;                                  // reservado (0 = dissolve); o fade ficou adiado
    }

    public enum LoadLevel : byte { Normal = 0, High = 1 }
    public enum EffectCategory : byte { Telegraph = 0, Hero = 1, EliteBoss = 2, Allies = 3, Horde = 4 }   // ordem = prioridade (menor = cortado por ultimo)

    public readonly struct BudgetCaps    { public readonly int MaxTelegraphs, MaxHeroCards, MaxEliteBossCards, MaxAllyCards, MaxHordeFlashes, MaxHordeDissolves; }
    public readonly struct BudgetRequest { public readonly int Telegraphs, HeroCards, EliteBossCards, AllyCards, HordeFlashes, HordeDissolves; }
    public readonly struct BudgetGrant   { public readonly int Telegraphs, HeroCards, EliteBossCards, AllyCards, HordeFlashes, HordeDissolves, AllyCardsCut, HordeEffectsDegradedToFade; }

    public static class VfxBudget   // funcao pura; EditMode
    {
        public static BudgetGrant Grant(in BudgetRequest request, in BudgetCaps caps, LoadLevel level);   // telegraph e heroi nunca cortados; corte na ordem inversa da prioridade
    }

    public sealed class GhostPool   // tamanho fixo GHOST_POOL_MAX; sem alocacao por frame
    {
        public GhostPool(int max);
        public bool TryAdd(int archetypeId, float x, float y, int deathTick);   // false = excedente (some na hora; soma Overflow)
        public int Active { get; }  public int Overflow { get; }
        public void Expire(float simTickF, int dissolveTicks);                   // libera os que terminaram
    }

    public sealed class PrewarmPlan { public PrewarmStep[] Steps { get; } }      // ordem fixa da Decisao 8; lista de assets vem do snapshot da fase
}

namespace Forja.Gameplay.Presentation   // com Unity
{
    // Otimizacao SO se o spike provar a leitura no shader; o caminho primario escreve a matriz em NativeArray<Matrix4x4> e os dados extras na textura de instancia.
    [System.Runtime.InteropServices.StructLayout(System.Runtime.InteropServices.LayoutKind.Sequential)]
    public struct HordeInstance { public UnityEngine.Matrix4x4 ObjectToWorld; public UnityEngine.Vector4 Fx; }   // a matriz tem de ser o 1o campo

    public sealed class PresentationDriver : UnityEngine.MonoBehaviour, IPresentationSink   // 1 por fase; LateUpdate le uma vez cada span
    {
        void LateUpdate();                       // Decisao 2 (captura por frame), Decisao 3 (SimTickF), Decisoes 4 a 7 (desenho)
        public void OnTick(int combatTick, System.ReadOnlySpan<SimEvent> events, System.ReadOnlySpan<DeathRecord> deaths);
    }
    public sealed class PrewarmRunner { public System.Threading.Tasks.Task RunAsync(PrewarmPlan plan, int maxWaitMs, System.Threading.CancellationToken ct); }   // main thread; pode alocar (carregamento); nao trava a fase no teto
}
```

### Implementation Guidelines
- A apresentação **must never** escrever na simulação, chamar `Tick`/`Spawn`/`Kill`, nem guardar estado que entre no hash ou no log como estado de jogo; `Forja.Simulation` e os sistemas de tick **must never** referenciar `Forja.Gameplay.Sim.View` ou `Forja.Gameplay.Presentation`.
- Todo efeito de combate **must** ser função de `SimTickF` e de ticks guardados; **must never** ler `_Time`, `Time.time` ou `Time.deltaTime`. As contas de idade no shader **must** ser `float` (highp) e a textura de instância **must** ser de 32 bits.
- A horda **must** ser desenhada por `RenderMeshInstanced` (1 draw lógico por tipo; os lotes são do aparelho), com `RenderParams.worldBounds` da área jogável, `shadowCastingMode = Off` e `receiveShadows = false`; **must never** usar `SkinnedMeshRenderer`, um `GameObject` por inimigo, `Animator`, `Collider`, partícula, decal ou som por corpo.
- O shader **must** ler os dados extras por `SV_InstanceID` de uma textura (ou do plano B1); **must never** assumir uma ligação entre um campo extra do struct de instância e uma propriedade HLSL antes de o spike a provar.
- Cada span **must** ser lido uma vez por frame numa variável local, **must never** ser guardado em campo, lambda, coroutine ou `async`, e todo consumidor **must** filtrar por `IsAlive` antes de usar coluna privada (ADR-0004).
- As mortes da horda **must** ser capturadas em `OnTick`, depois de cada tick, inclusive o do `Ended`; **must never** ser lidas de `DeathsThisTick` no `LateUpdate` (a lista é limpa a cada tick).
- Os pools **must** ter tamanho fixo criado na tela de carregamento; o excedente **must** cortar pela prioridade da Decisão 6 e **must** somar nos contadores; telegraph e herói **must never** ser cortados. O array dos cartões **must** ser escrito ordenado por `tickInicio`.
- Nomes de propriedade de shader **must** vir de campos `static readonly` com `Shader.PropertyToID` e ter um teste de contrato contra o shader; nenhum outro campo `static` **must** guardar estado mutável.
- O pré-aquecimento **must** correr em paralelo (E/S) com o `BeginStage`, antes do `Create`, incluir o desenho do chefe fora da tela, e **must never** travar a fase além de `PREWARM_MAX_WAIT_MS`; depois do teto a carga **must** continuar e o `PrewarmIncomplete` **must** ser registrado.
- Nenhuma alocação gerenciada **must** acontecer por frame no `RenderFrameBuilder`, nos pools e em `OnTick`; arrays e a textura de instância **must** ser criados na tela de carregamento. (O `PrewarmRunner` está fora desta regra.)
- A duração do hit-stop **must** ser medida em `SimTickF`.
- `Span<T>` **must never** ser campo de classe; só variável local. C# 9 apenas.
- Testes em `Assets/Tests/EditMode/View/` (`EffectClock`, `RenderFrameBuilder`, `VfxBudget`, pools, `PrewarmPlan`) e `Assets/Tests/PlayMode/` só para os renderers, o contrato dos shaders e o pré-aquecimento.

## Alternatives Considered

### Alternative 1: Entities Graphics (DOTS) só para o render da horda
- **Description**: mover a horda para entidades ECS apenas na apresentação, desenhadas pelo Entities Graphics.
- **Pros**: batching e instancing prontos; escala para milhares de instâncias.
- **Cons**: traz o pacote Entities e um mundo ECS paralelo para uma simulação que é C# puro e lida por spans; a referência local do Entities é uma reescrita completa e marcada de alto risco; mais código de ponte do que o `RenderMeshInstanced` direto.
- **Rejection Reason**: custo e risco acima do necessário para ~300 instâncias. Reabrir só se todos os caminhos de `RenderMeshInstanced` falharem.

### Alternative 2: `SkinnedMeshRenderer` e `Animator` por inimigo
- **Description**: um objeto animado por corpo de horda.
- **Pros**: o fluxo padrão da Unity; animação rica.
- **Cons**: 300 renderers e 300 animators dominam a CPU e os draws; instancing de malha skinned não está na referência; estoura o teto de 150 draws.
- **Rejection Reason**: o art bible (8.6) o proíbe para a horda.

### Alternative 3: struct de instância com campos extras depois da matriz como caminho primário
- **Description**: `RenderMeshInstanced<T>` com `T { Matrix4x4 ObjectToWorld; Vector4 Fx; }` e o shader lendo `Fx` como propriedade instanciada.
- **Pros**: sem textura extra; é o mais simples de escrever se funcionar.
- **Cons**: o mecanismo de ligação entre o campo C# e a propriedade HLSL não é documentado como contrato estável (conhecimento do especialista, sem fonte local); no Shader Graph exige HLSL manual.
- **Rejection Reason**: não como primário (apontado pelo `unity-specialist`). Fica como **otimização**, só se o spike provar a leitura no shader.

### Alternative 4: `Graphics.RenderMeshIndirect` com buffer estruturado como caminho primário
- **Description**: todos os dados de instância num `GraphicsBuffer`, um draw indireto por tipo.
- **Pros**: o mais escalável; sem o limite de dados por instância.
- **Cons**: exige GLES 3.1 ou Vulkan no aparelho de referência (`NOT SOURCEABLE`); shader mais complexo; desnecessário para ~300 instâncias.
- **Rejection Reason**: último recurso. O `GraphicsBuffer` estruturado com `RenderMeshInstanced` é o **plano B1**.

### Alternative 5: partículas ou VFX Graph para nascimento, morte e golpe da horda
- **Description**: cada morte e cada nascimento emitem partículas.
- **Pros**: o fluxo comum de VFX.
- **Cons**: dezenas de nascimentos e mortes por segundo viram milhares de partículas e overdraw; o GDD #6 e o art bible mandam dissolve de shader; efeito por corpo é proibido.
- **Rejection Reason**: contradiz GDD #6 e GDD #7.

### Alternative 6: URP Decal para o telegraph
- **Description**: o telegraph como Decal do URP projetado no chão.
- **Pros**: encaixa em terreno irregular.
- **Cons**: o chão é plano; o suporte do URP Decal no mobile é `NOT SOURCEABLE`; precisa de uma renderer feature e de um passe extra.
- **Rejection Reason**: o quad no chão é mais barato e basta (art bible 8.7); o Decal fica como alternativa a medir.

### Alternative 7: carregar os assets do chefe sob demanda no tick do rugido
- **Description**: sem pré-aquecimento; o chefe e o LUT carregam quando entram.
- **Pros**: nenhum custo na tela de carregamento; menos memória.
- **Cons**: o tick do rugido paga carga de modelo, shader e LUT no mesmo frame: um engasgo exatamente no momento mais dramático (AC-P4 do #7).
- **Rejection Reason**: contradiz o GDD #7 (Regra 10, AC-P4).

### Alternative 8: efeitos com `_Time` e `Time.time` da Unity
- **Description**: shaders e scripts de efeito usam o relógio da engine.
- **Pros**: o jeito padrão; nenhuma integração com a simulação.
- **Cons**: a pausa, o menu de oferta e o `CombatHold` não congelam o efeito; é preciso zerar `timeScale` (proibido) ou pausar cada efeito; o hit-stop dessincroniza.
- **Rejection Reason**: contradiz o ADR-0007 (nada de `timeScale`) e o princípio de que pausar é "zero ticks".

### Alternative 9: um `GameObject` por cartão de efeito
- **Description**: cada arco, rastro e cartão é um objeto com `SpriteRenderer` ou `MeshRenderer`.
- **Pros**: simples de montar.
- **Cons**: até 150 cartões aliados viram até 150 draws e 150 objetos para gerenciar.
- **Rejection Reason**: estoura o teto de draws (VFX ≤ 30).

### Alternative 10: fade do excedente de fantasmas por instância viva ou por segundo pool (rascunho inicial)
- **Description**: o morto sem vaga esmaece por 2 ticks.
- **Pros**: segue o texto do GDD #7 ("some com fade direto").
- **Cons**: o corpo morto sai do array no frame seguinte (filtro `IsAlive`), então não há instância viva para esmaecer; o fade exigiria um segundo pool de fantasmas curtos.
- **Rejection Reason**: apontada pelo `technical-director` (concern 1); o excedente some na hora, e o fade fica adiado até o autor pedir (GDD Sync).

## Consequences

### Positive
- A fronteira simulação-imagem fica única e testável: a apresentação só lê, e a regra de prioridade e a interpolação são funções puras em EditMode.
- Pausa, congelamento de combate e menu de oferta param os efeitos sozinhos, sem código por efeito.
- A horda custa um draw lógico por tipo, sem objeto por inimigo, e o excesso é cortado por regra, não por acaso.
- Cada premissa que a referência não cobre tem plano B e um gatilho de reabertura.
- O caminho primário de dados por instância (textura por `SV_InstanceID`) não depende de nenhuma ligação não documentada entre C# e HLSL.

### Negative
- Vários caminhos de instancing possíveis (primário, B1, otimização) aumentam o trabalho do spike.
- O número real de draws da horda pode ser o dobro do lógico (lotes), o que aperta o teto de 150 draws.
- Os shaders da horda e dos cartões ficam acoplados a um layout de dados por instância e a um nome de propriedade, que o teste de contrato precisa vigiar.
- Sem a emenda ao ADR-0004 (`UltimoDanoTick`), o **flash por corpo da horda fica desligado**; com ela, o golden hash do #6 muda.
- O excedente de mortes de fantasmas some na hora, sem o fade que o GDD #7 descreve.
- O `LoadLevel` dinâmico é `NOT ASSESSED` aqui; até o ADR de orçamento de frame só valem os tetos fixos.
- Todos os tetos numéricos são provisórios até o spike no aparelho de referência, ainda não verificado.
- Três emendas pequenas a ADRs ainda `Proposed` (ADR-0004, ADR-0007, ADR-0008) e quatro sincronias de GDD pendentes.

## Risks
- **Leitura dos dados por instância no shader (`NOT SOURCEABLE`):** se a textura por `SV_InstanceID` não funcionar nos lotes do `RenderMeshInstanced`, a horda perde nascimento e dissolve por instância. Mitigação: B1, a otimização e o último recurso, e o gatilho (reabrir a Decisão 4 e rever `teto_vivos_horda` com o autor).
- **Aparelho de referência não verificado:** os tetos (150 draws, 300k triângulos, overdraw 2,5×) podem não caber. Mitigação: tudo provisório; gatilhos nos itens 5 e 7; a story de render não fecha sem o spike (itens 1, 2, 5, 7 e 11).
- **Frame do tick do rugido:** pré-aquecimento incompleto vira engasgo no pior momento. Mitigação: paralelo (E/S) com o `BeginStage`, desenho do chefe fora da tela obrigatório, teto de espera, a carga que continua, nota no log, e o gatilho do chefe instanciado e oculto desde a entrada.
- **Lista de mortes limpa a cada tick:** se o sink não capturar, o dissolve some. Mitigação: `OnTick` depois de cada tick (inclusive o do `Ended`) e a emenda ao ADR-0007; teste que roda 3 ticks no frame.
- **`worldBounds` mal definido:** o draw pode ser descartado inteiro. Mitigação: definido uma vez como a área jogável com folga, e coberto por teste de PlayMode.
- **Precisão do relógio na GPU:** `half` perde o passo acima de ~32.768 ticks (~18 minutos). Mitigação: `float` e textura de 32 bits no contrato dos shaders (Verification Required 11).
- **Hit-stop congelado em vez de cancelado no `CombatHold`:** diferença do GDD #6. Mitigação: registrada em GDD Sync para o autor; provisória.
- **Span guardado em campo:** não compila; usado fora do frame, lê lixo. Mitigação: o contrato do ADR-0004 repetido nas guidelines e revisado.
- **Estado estático com domain reload desligado:** pools ou `EffectClock` que persistam entre Play Modes. Mitigação: nenhum `static` mutável; o que existir é zerado em `SubsystemRegistration`.
- **Excedente que some na hora pode parecer "sumiço" no pico de mortes.** Mitigação: contador `GhostPoolOverflow` no log; aceito como padrão provisório.
- **Plano B1 exige GLES 3.1 ou Vulkan:** pode excluir o aparelho de referência. Mitigação: o caminho primário (textura) funciona em GLES 3.0.
- **`PrewarmRunner` aloca e a `Task` não é esperada ao sair da fase:** aceito fora do caminho quente; `CancellationToken` na interface.
- **Revisões 5.5 e 5.6 (resultado):** `unity-specialist`: abordagem geral idiomática; bloqueantes A (struct de dados extras como primário), B (`worldBounds` ausente) e C ("1 draw por tipo" vs lotes) **resolvidos** nesta revisão; D (estado estático sem reset) tratado como regra; notas incorporadas (RenderGraph removido de "Post-Cutoff", `RenderMeshInstanced` marcado como pré-cutoff, `WarmUp` só compila e o desenho fora da tela aquece o estado de pipeline, sombra explícita, ordenação dos transparentes, `CancellationToken`, MPB e SRP Batcher). `technical-director`: CONCERNS; concerns 1 a 7 (fade, hit-stop, custo de hash da emenda ao ADR-0004, gatilhos dos itens 5 e 7, comportamento depois do teto do pré-aquecimento, precisão highp, dependência do ADR-0008 e tick final) **resolvidos** no texto; o item de asmdef próprio ficou como decisão de projeto pendente e `BudgetCaps` foi definido. Um novo parecer do diretor sobre este texto revisado **não foi pedido**; o veredito vigente continua sendo o CONCERNS acima, tratado, e não um APPROVE.

## GDD Requirements Addressed

| GDD System | Requirement | How This ADR Addresses It |
|------------|-------------|--------------------------|
| combate-e-dano.md (#6) | TR-combate-018: efeitos por shader com propriedade por instância, pools de cartões e fantasmas, overdraw ≤ 2,5×, decal de telegraph, cortes por prioridade | Decisões 5, 6 e 7: shader com dados de instância, `CardPool`/`GhostPool`, `VfxBudget`, telegraph em quad; overdraw medido no spike com gatilho |
| combate-e-dano.md (#6) | "Prioridade quando a tela lota": telegraph > herói > elite e chefe > aliados > horda; corte na ordem inversa | Decisão 6: `VfxBudget` pura em EditMode |
| combate-e-dano.md (#6) | Por entidade, `ultimoDanoTick`; posição, arquétipo e tick da morte da horda legíveis | Decisões 2 e 5: captura da morte em `OnTick`; `UltimoDanoTick` pedido por emenda ao ADR-0004 (flash desligado sem ela) |
| combate-e-dano.md (#6) | Hit-stop de 3 ticks congela só a pose do herói e do alvo; o #12 cancela no `CombatHold` | Decisão 3: duração em `SimTickF`, congela no `CombatHold` (diferença registrada em GDD Sync) |
| horda-waves-e-inimigos.md (#7) | TR-horda-014: ≤ 400 triângulos, 1 LOD, 1 draw por tipo, dados por instância, zero efeito ou som por corpo, pool de ~300 fantasmas | Decisão 4: malha de partes rígidas, `RenderMeshInstanced`, textura de instância, `GhostPool` de 300 |
| horda-waves-e-inimigos.md (#7) | Nascimento derivado de `tickNascimento`, sem evento; morte em massa do rugido escalonada pela distância | Decisões 3 e 4: `idade` desde `BirthCombatTicks`; atraso por distância no `GhostPool` |
| horda-waves-e-inimigos.md (#7) | TR-horda-015, AC-P4: pré-aquecer modelo, shader, LUT, disco do rugido do chefe | Decisão 8: `PrewarmPlan` em paralelo (E/S) com o `BeginStage`, antes do `Create`, teto de espera, carga que continua, nota no log |
| art-bible.md (8.3 a 8.7, 2.2) | Horda ≤ 400 tri, nunca skinned, ≤ 150 draws, ≤ 300k tri, overdraw ≤ 2,5×, ≤ 150 cartões, telegraph quad, sem partícula de combate | Decisões 4, 6 e 7; Verification Required 2, 5 e 6 |
| simulacao-deterministica.md (#2) | FS2: interpolação `prev + (atual − prev) × alfa` na apresentação | Decisão 2 |

## Performance Implications
- **CPU**: por frame, O(vivos + fantasmas + cartões) para montar os dados (da ordem de algumas centenas de instâncias), sem alocação; mais o `SetPixelData` da textura de instância (poucas centenas de texels); `OnTick` copia no máximo `EventCapacity` eventos e as mortes do tick. O custo real é medido no spike (Verification Required 2).
- **GPU**: 1 draw lógico por tipo de horda (≤ 3, mais os lotes do aparelho), 1 por material de cartão, 1 de telegraph; ≤ 400 triângulos por corpo; overdraw ≤ 2,5× (alvo, não medido). Estimativa de triângulos da horda: 300 × 400 = 120k, dentro do teto provisório de 300k do art bible.
- **Memory**: arrays de instância, a textura de instância (`RGBA32F`, 2 texels por instância, da ordem de poucos KB) e `lastFacing` de tamanho `EntityCapacity` criados na tela de carregamento; pools fixos; textura de ossos compartilhada. Tetos de textura do art bible 8.4 (horda ≤ 2 MB, VFX ≤ 4 MB). O teto de memória total é do ADR de orçamento.
- **Load Time**: o pré-aquecimento roda em paralelo (E/S) com o `BeginStage`, com teto de espera de 3000 ms provisório.
- **Network**: não se aplica.

## Migration Plan
Não há código de render hoje. Ordem: (1) `EffectClock`, `VfxBudget`, `GhostPool`, `CardPool` e `RenderFrameBuilder` em EditMode com fixtures; (2) o `PresentationDriver` e o `IPresentationSink` ligados ao `PhaseHost`; (3) o spike da horda no aparelho de referência: caminho primário (textura por `SV_InstanceID`), depois B1 e a otimização, medindo o número real de lotes (Verification Required 1 a 3); (4) os shaders de horda, cartões e telegraph e o teste de contrato (inclui highp); (5) o `PrewarmRunner` e a medição do frame do rugido; (6) o spike de overdraw e de draws com 150 cartões (Verification Required 5 e 6).

## Validation Criteria
- `EffectClock.SimTickF`: monotônico; congela com `CombatHold != 0` e com o `Alpha` congelado na pausa; nunca anda para trás num reinício de `Alpha`.
- `VfxBudget`: telegraph e herói nunca cortados; com pedidos acima dos tetos, a horda perde flash e dissolve antes dos aliados, e os aliados perdem os mais antigos primeiro; mesmo pedido e mesmo `LoadLevel` dão o mesmo resultado.
- `GhostPool`: capacidade fixa; `TryAdd` devolve falso no excedente e conta `Overflow`; `Expire` libera os terminados; zero alocação.
- `RenderFrameBuilder`: com 3 ticks no frame e a lista de mortes limpa a cada tick, os 3 grupos de mortes aparecem como fantasmas (a captura por `OnTick`, não a leitura no `LateUpdate`), **inclusive as mortes do tick que encerra a fase**; a interpolação com `Alpha` 0 e 1 devolve `prev` e `atual`; entidade morta e id fora de `IdCount` nunca entram; o array de cartões sai ordenado por `tickInicio`.
- Teste de contrato dos shaders: os nomes de propriedade e o layout da textura de instância batem com o shader; **as contas de idade são `float` (nenhum `half`/`fixed`) e a textura é de 32 bits**.
- Zero alocação gerenciada por frame no `RenderFrameBuilder`, nos pools e em `OnTick` (IL2CPP, aparelho).
- **No aparelho** (Verification Required 1 a 11): horda, cartões e telegraph dentro do orçamento no minuto 20; o número real de draws; o frame do tick do rugido cabe (AC-P4) e nenhum `PrewarmIncomplete`; overdraw ≤ 2,5×. **A story de render não fecha sem a evidência do spike nos itens 1, 2, 5, 7 e 11** (Test Evidence Visual/UI: captura retida em `production/qa/evidence/`).

## Related
- Depende de ADR-0001, ADR-0004, ADR-0005, ADR-0007 e ADR-0008 (todos `Proposed`). Pede emendas ao ADR-0004 (`UltimoDanoTick` em `ICombatReadView`, com o golden hash do #6 mudando), ao ADR-0007 (passo 7 entrega `DeathsThisTick` ao sink, inclusive no tick do `Ended`) e ao ADR-0008 (`NoteKind.PrewarmIncomplete = 8`); ver Ordering Note.
- Candidatas de registro a apresentar depois de gravar: `state_ownership` do estado só de apresentação; interfaces `presentation_sink` (`IPresentationSink`) e `effect_clock`; `api_decisions` de horda instanciada, tempo de efeito, pools e telegraph, pré-aquecimento; `forbidden_patterns` (`presentation_writes_sim`, `sim_references_presentation`, `effect_uses_real_time`, `skinned_horde`, `deaths_read_after_tick`, `prewarm_blocks_phase`).
- GDDs: `design/gdd/combate-e-dano.md` (#6), `design/gdd/horda-waves-e-inimigos.md` (#7), `design/gdd/simulacao-deterministica.md` (#2); `design/art/art-bible.md` (2.2, 5.5, 8.3 a 8.9); `design/gdd/systems-index.md` (#12, sem GDD).
- `docs/architecture/architecture-review-2026-11-06.md` (Required ADRs, item 5); `docs/architecture/requirements-traceability.md` (TR-combate-018, TR-horda-014, TR-horda-015).

## GDD Sync (pendente; nenhum arquivo foi editado)
- **GDD #6 (Visual/Audio):** diz que o #6 "expõe por entidade `ultimoDanoTick` e `pesado`"; a `ICombatReadView` do ADR-0004 não os traz. Saída recomendada: a emenda ao ADR-0004 com só `UltimoDanoTick` (e o hash do #6 mudando). Até lá o flash da horda fica desligado.
- **GDD #6 (L412, L440), hit-stop:** manda o #12 *cancelar* o hit-stop quando `CombatHold ≠ 0`; este ADR faz o relógio de efeito *congelar* (provisório). **Pergunta aberta para o autor** (é decisão de sensação de jogo): cancelar ou congelar no `CombatHold`.
- **GDD #6 e #7, excedente de fantasmas:** dizem "some com fade direto"; este ADR faz o excedente sumir na hora (não há instância viva para esmaecer). Se o autor quiser o fade, o custo é um segundo pool de fantasmas curtos.
- **GDD #6:** "legíveis por 1 tick depois de `DeathsThisTick`" não basta com vários ticks por frame; este ADR captura a lista a cada tick (`OnTick`). O texto do GDD pode ficar, com uma nota.
- **GDD #7 (L182, L530 e L796, AC-P4):** atribuem o pré-aquecimento ao #12 "no `Preparar`"; este ADR o põe na entrada da fase, em paralelo (E/S) com o `BeginStage`, **antes do `Create`**, porque o `Preparar` é C# puro síncrono e a carga de assets é assíncrona. **Antes de aceitar, essas linhas do GDD #7 devem passar a dizer "antes do `Create`".** O GDD #12 deve implementar o `PrewarmRunner`.
- **GDD #12 (a escrever):** passa a ser dono dos renderers, do `PrewarmRunner`, do `LoadLevel` e dos assets de `/asset-spec`.
- **Art bible 8:** o orçamento numérico é provisório e continua sendo; "1 draw por tipo" é lógico (os lotes são do aparelho). Este ADR não altera o art bible.

## Decisões provisórias (a reavaliar com o spike e o jogo jogável)
1. O caminho primário de dados por instância (textura por `SV_InstanceID`) e a ordem dos planos B (Decisão 4).
2. Partes rígidas com matrizes em textura (decisão do usuário), VAT só se o spike pedir (Decisão 4).
3. `SimTickF = max(anterior, CombatTick + Alpha·(CombatHold==0))` como o relógio de efeito (Decisão 3), e o hit-stop que congela no `CombatHold`.
4. `GHOST_POOL_MAX` = 300, `ALLY_CARD_MAX` = 150, `CARD_POOL_MAX` = 32, `max_avisos` 3 a 6, `PREWARM_MAX_WAIT_MS` = 3000.
5. O excedente de fantasmas que some na hora e o corte da horda antes dos aliados (Decisão 6).
6. O telegraph como quad no chão, e o URP Decal como alternativa a medir (Decisão 7).
7. O pré-aquecimento em paralelo (E/S) com o `BeginStage`, antes do `Create`, e a fase que começa mesmo se ele não terminar, com a carga continuando (Decisão 8).
8. O flash da horda desligado até a emenda ao ADR-0004.
9. A camada **Presentation** (sem `architecture.md`) e o asmdef compartilhado com os sistemas de tick (um asmdef próprio é decisão de projeto pendente).
