# Technical Preferences

<!-- project.yaml at the repo root is the machine-readable source of truth for
     engine, specialists, naming, performance, platform, and testing.framework.
     This file is the human-readable LEGACY FALLBACK: agents and skills resolve
     each key from project.yaml first and fall back here only when the
     project.yaml key is absent. /setup-engine dual-writes both.
     Forbidden patterns and allowed libraries are NOT migrated — they live only
     in this file. Populated by /setup-engine; updated as decisions are made. -->

## Engine & Language

- **Engine**: Unity 6.3 LTS (6000.3.x; editor installed at pin time: 6000.3.27f1)
- **Language**: C#
- **Rendering**: URP (Universal Render Pipeline) with Render Graph from day one
- **Physics**: PhysX (Unity default)

## Input & Platform

<!-- Written by /setup-engine. Read by /ux-design, /ux-review, /test-setup, /team-ui, and /dev-story -->
<!-- to scope interaction specs, test helpers, and implementation to the correct input methods. -->

- **Target Platforms**: Mobile (iOS, Android)
- **Input Methods**: Touch
- **Primary Input**: Touch (virtual joystick for movement, dodge button, one active ultimate)
- **Gamepad Support**: None
- **Touch Support**: Full
- **Platform Notes**: One-thumb play: movement must work with a single thumb, and every in-combat control must be reachable without moving the hand. No hover-only interactions. Enemy telegraphs stay on the top-most visual layer (design pillar "Massacre com peso"). Respect device safe areas.

## Naming Conventions

- **Classes**: PascalCase (e.g., `PlayerController`)
- **Variables**: camelCase for locals and parameters; `_camelCase` for private fields; PascalCase for public fields and properties (e.g., `MoveSpeed`)
- **Signals/Events**: PascalCase, handlers named `On<Event>` (e.g., `OnWaveCleared`)
- **Files**: PascalCase matching the class (e.g., `PlayerController.cs`)
- **Scenes/Prefabs**: PascalCase
- **Constants**: UPPER_SNAKE_CASE (UNVERIFIED — not sourceable from `docs/engine-reference/unity/`; PascalCase is also common in Unity code. Confirm before relying on it)

## Performance Budgets

<!-- Provisional: from the TD-FEASIBILITY review of the game concept. To be validated by the
     performance spike (300 enemies, 4 heroes, VFX, one boss telegraph, on a mid-range Android
     reference device, measured at minute 20 for thermal throttling). -->

- **Target Framerate**: 60 fps (floor: 30 fps)
- **Frame Budget**: ~12 ms (leaves thermal headroom under the 16.6 ms frame at 60 fps)
- **Draw Calls**: [TO BE CONFIGURED — set after the performance spike; not sourceable from docs/engine-reference/]
- **Memory Ceiling**: [TO BE CONFIGURED — set after the performance spike on the reference device]

## Testing

- **Framework**: NUnit (Unity Test Framework)
- **Minimum Coverage**: 80%
- **Required Tests**: Balance formulas, gameplay systems, networking (if applicable)

## Forbidden Patterns

<!-- Add patterns that should never appear in this project's codebase -->
- [None configured yet — add as architectural decisions are made]

## Allowed Libraries / Addons

<!-- Add approved third-party dependencies here -->
- [None configured yet — add as dependencies are approved]

## Architecture Decisions Log

<!-- Quick reference linking to full ADRs in docs/architecture/ -->
- [No ADRs yet — use /architecture-decision to create one]

## Engine Specialists

<!-- Written by /setup-engine when engine is configured. -->
<!-- Read by /code-review, /architecture-decision, /architecture-review, and team skills -->
<!-- to know which specialist to spawn for engine-specific validation. -->

- **Primary**: unity-specialist
- **Language/Code Specialist**: unity-specialist (C# review — primary covers it)
- **Shader Specialist**: unity-shader-specialist (Shader Graph, HLSL, URP/HDRP materials)
- **UI Specialist**: unity-ui-specialist (UI Toolkit UXML/USS, UGUI Canvas, runtime UI)
- **Additional Specialists**: unity-dots-specialist (ECS, Jobs system, Burst compiler), unity-addressables-specialist (asset loading, memory management, content catalogs)
- **Routing Notes**: Invoke primary for architecture and general C# code review. Invoke DOTS specialist for any ECS/Jobs/Burst code. Invoke shader specialist for rendering and visual effects. Invoke UI specialist for all interface implementation. Invoke Addressables specialist for asset management systems.

### File Extension Routing

<!-- Skills use this table to select the right specialist per file type. -->
<!-- If a row says [TO BE CONFIGURED], fall back to Primary for that file type. -->

| File Extension / Type | Specialist to Spawn |
|-----------------------|---------------------|
| Game code (.cs files) | unity-specialist |
| Shader / material files (.shader, .shadergraph, .mat) | unity-shader-specialist |
| UI / screen files (.uxml, .uss, Canvas prefabs) | unity-ui-specialist |
| Scene / prefab / level files (.unity, .prefab) | unity-specialist |
| Native extension / plugin files (.dll, native plugins) | unity-specialist |
| General architecture review | Primary |
