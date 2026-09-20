# BR-05 — NexLabs 3D Language

Status: SYSTEM ARCHITECTURE
Date: 2026-09-19
Execution target: Codex + Blender MCP
Brand direction: Dark Mineral Laboratory / Computational Matter

## 1. Purpose
Build a reusable NexLabs 3D visual language rather than a one-off hero scene.

The system must support:
- institutional website hero;
- HIVE/product storytelling;
- motion logo;
- technical visualizations;
- pitch/deck renders;
- social/launch media;
- future product launches.

## 2. Core metaphor
**Computation becomes matter.**

Information is represented through spatial behavior:
fragment → route → index → layer → retrieve → resolve → stabilize.

3D motion must express system concepts, not generic ambient spectacle.

## 3. Primitive library

### P01 — Core
Central stable structure. Represents resolved/coherent system state.

### P02 — Shell
Nested layer around a core. Represents context boundaries, memory layers or system scopes.

### P03 — Route
Directed path between structures. Represents information movement/retrieval.

### P04 — Node
Addressable point/anchor. Used sparingly and hierarchically.

### P05 — Lattice
Structural field connecting modules. Represents infrastructure rather than literal neural tissue.

### P06 — Cell
Reusable modular unit capable of assembling larger systems.

### P07 — Band
Layer/ribbon with controlled topology. Useful for context streams and logo-derived geometry.

### P08 — Fragment
Unresolved data-matter element before organization.

### P09 — Gate
Structural transition between scopes/layers.

### P10 — Field
Sparse spatial distribution controlling particles, attraction, flow or state.

Every production scene should be expressible primarily through these primitives.

## 4. Canonical scene — Context Core

### State S0 Dormant
Stable silhouette, low signal activity. Content/UI is already usable.

### S1 Intake
Sparse fragments/signals enter peripheral field.

### S2 Index
Fragments align to nodes/routes/layers.

### S3 Retrieve
Relevant routes activate selectively; unrelated structure remains quiet.

### S4 Assemble
Selected information converges into nested context layers.

### S5 Resolve
Core becomes coherent and structurally legible.

### S6 Explore
User movement/scroll reveals subsystems without destroying the resolved composition.

### S7 Idle
Low-amplitude system activity; no distracting perpetual spinning.

## 5. Geometry strategy
Prefer procedural/non-destructive authoring for repeatable structures:
- Geometry Nodes where appropriate;
- instancing for repeated modules;
- curves for routes;
- controlled modifiers;
- named parameters for density, layer count, thickness and seed.

Hero silhouette must remain authored and art-directed. Procedural does not mean random.

## 6. Determinism
Randomized systems use explicit seeds.
Same source + parameters + seed must reproduce the approved visual.
This is required for review, regression and re-export.

## 7. Material families

### MAT-MINERAL
Dark structural body; roughness variation; subtle edge response.

### MAT-CERAMIC
Precision surface; controlled smoothness; readable under restrained lighting.

### MAT-OPTICAL
Selective transparent/transmissive layer.
Use only where it adds structural meaning; expensive web effects require fallback.

### MAT-SIGNAL-CYAN
Primary emissive system signal.

### MAT-SIGNAL-VIOLET
Secondary emissive signal.

### MAT-SIGNAL-WARM
Rare accent/state material.

### MAT-DATA
Particle/fragment material optimized for instancing.

All materials need high-quality render and web-safe equivalents where necessary.

## 8. Lighting rig

Canonical rig families:
- KEY-SCULPT: defines primary geometry.
- RIM-STRUCTURE: separates silhouette from mineral background.
- SIGNAL-EMISSION: material-driven system activity.
- ENV-MINERAL: extremely restrained environment contribution.
- DETAIL-MACRO: optional close-up rig for cinematic assets.

Avoid large uncontrolled bloom. Bloom is a post/runtime enhancement, not a substitute for lighting.

## 9. Camera system

### CAM-HERO
Canonical website composition.

### CAM-PROJECTION
Exact camera used to derive/test logo projection when relevant.

### CAM-MACRO
Material/detail storytelling.

### CAM-ORBIT-REFERENCE
Internal review camera, not necessarily user-controllable.

Camera metadata must be exportable/documented so web composition can reproduce intended framing.

## 10. Interaction philosophy
User influences the system; user does not freely dismantle it.

Possible inputs:
- pointer parallax;
- scroll progress;
- section state;
- hover/focus on product concepts;
- device orientation only if justified and permission-free.

Interaction amplitudes remain bounded and deterministic.

## 11. Blender vs runtime boundary

### Blender owns
- canonical geometry;
- art-directed topology;
- high-quality materials/reference look;
- baked animation where appropriate;
- cinematic renders;
- canonical cameras;
- UVs/mesh optimization source;
- source-of-truth scene organization.

### Web runtime owns
- adaptive quality;
- bounded pointer response;
- scroll-state transitions;
- lightweight particles where cheaper than baked geometry;
- selective shader animation;
- visibility/LOD;
- device-dependent effects;
- reduced-motion/static behavior.

Rule: do not implement runtime complexity merely because WebGL can do it.

## 12. Asset tiers

### MASTER
High-quality Blender source. Never shipped directly.

### WEB-HIGH
Capable desktop.

### WEB-MED
Typical desktop/laptop/mobile.

### WEB-LOW
Simplified geometry/materials.

### STATIC
Pre-rendered AVIF/WebP or equivalent fallback.

Each hero-critical asset requires at least WEB-MED + STATIC; other tiers depend on measured need.

## 13. LOD
LOD is semantic as well as geometric:
- remove invisible internal detail first;
- reduce particle density;
- simplify transmission/refraction;
- simplify shaders;
- merge/instance repeated geometry;
- preserve silhouette and signal hierarchy.

## 14. Texture policy
Prefer procedural/material solutions and compact texture sets.
No automatic 4K textures.
Use texture compression compatible with final web stack.
Resolution selected by projected screen size and visual importance.

## 15. Animation architecture
Animation clips/states should map to semantic states:
dormant
intake
index
retrieve
assemble
resolve
idle

Avoid one giant opaque timeline where web cannot control meaningful transitions.

## 16. Naming contract
Planned Blender naming:
NL_<TYPE>_<NAME>_<VARIANT>

Examples:
NL_CORE_Context_A
NL_ROUTE_Primary_01
NL_SHELL_Context_02
NL_CAM_Hero_A
NL_MAT_Mineral_A

Final conventions detailed in BR-11.

## 17. Scene organization
Collections should separate:
- CORE
- SHELLS
- ROUTES
- NODES
- DATA
- LIGHTS
- CAMERAS
- HELPERS
- EXPORT
- RENDER_ONLY

Export collection contains only production-approved web objects.

## 18. Web export philosophy
Target format: glTF/GLB unless BR-09 establishes a superior justified path.

Pipeline must evaluate:
- geometry compression;
- mesh optimization;
- texture compression;
- animation optimization;
- material compatibility;
- naming preservation where runtime needs it.

No compression technology is frozen before browser/deployment compatibility review.

## 19. Static fallback
Every essential 3D composition needs a visually intentional static state.
Fallback is not an error screenshot. It is a first-class brand asset.

## 20. Accessibility
3D conveys enhancement, not exclusive information.
All product meaning exists in semantic HTML/copy.
Reduced-motion mode removes nonessential movement.
Canvas interaction never blocks keyboard navigation.

## 21. Reuse rule
A new NexLabs 3D scene should first ask:
Can this be built from existing primitives/materials/rigs?
Only create a new primitive when the current language cannot express the concept cleanly.

## 22. Acceptance
BR-05 freezes when:
- primitive library is sufficient for hero + product story + logo motion;
- Context Core states are approved;
- Blender/runtime boundary is explicit;
- material families are compatible with BR-04;
- camera/lighting grammar is reproducible;
- LOD/fallback architecture exists;
- BR-11 can translate the system into Blender MCP work orders without inventing art direction.
