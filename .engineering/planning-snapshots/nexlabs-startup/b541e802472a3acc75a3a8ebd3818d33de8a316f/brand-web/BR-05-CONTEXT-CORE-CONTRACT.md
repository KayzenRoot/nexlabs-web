# BR-05 — Context Core Scene Contract

Status: PROPOSED
Scene ID: NL-SCENE-CONTEXT-CORE-01

## Role
Primary institutional hero and reusable brand storytelling asset.

## Composition
Central resolved core offset to permit headline/CTA negative space.
Exact side/position remains responsive and may mirror by breakpoint.

## Structural layers
1. Outer field — sparse incoming fragments.
2. Routing envelope — controlled paths/gates.
3. Context shells — nested semantic layers.
4. Inner lattice — infrastructure support.
5. Stable core — resolved/coherent state.

## Runtime state machine
BOOT_STATIC
→ DORMANT
→ INTAKE
→ INDEX
→ RETRIEVE
→ ASSEMBLE
→ RESOLVE
→ IDLE

EXPLORE is a bounded overlay state driven by page interaction.

Reduced motion:
BOOT_STATIC → RESOLVE_STATIC

Failure/unsupported:
STATIC_FALLBACK

## Data-matter behavior
Fragments do not move as random confetti.
They have:
- source region;
- target;
- route/field influence;
- deterministic seed;
- lifecycle;
- bounded count by quality tier.

## Signal hierarchy
Primary cyan: active/high-priority path.
Secondary violet: contextual/secondary system activity.
Warm accent: exceptional state only.

## Hero UI coexistence
3D must reserve compositional quiet space for:
- NexLabs identity;
- thesis/headline;
- supporting copy;
- primary CTA;
- secondary CTA.

Text never renders into the 3D canvas as the sole accessible version.

## Responsive composition
Desktop: richest depth and interaction.
Tablet: tighter camera and reduced field density.
Mobile: simplified scene/crop or static asset based on measured performance.
Do not shrink desktop composition blindly.

## Quality controller inputs
- viewport size;
- device pixel ratio cap;
- measured frame behavior;
- reduced-motion preference;
- capability/support;
- optional data-saving signal if reliably available.

No invasive device fingerprinting.

## Performance instrumentation
During implementation capture:
- asset transfer size;
- decode/load time;
- time until static hero visible;
- time until interactive 3D ready;
- frame timing;
- draw calls;
- triangles/instances;
- texture memory estimates where tooling supports it;
- fallback rate/errors.

## Failure behavior
If 3D initialization fails:
1. stop retry loop;
2. retain/replace with static branded hero;
3. preserve all content and CTA functionality;
4. record privacy-respecting diagnostic event if analytics/observability is enabled.

## Blender deliverables
- canonical master scene;
- canonical hero camera;
- lighting rig;
- approved materials;
- deterministic procedural controls;
- animation/state source;
- web export collection;
- high-quality still render;
- static fallback render;
- asset manifest.

## Web deliverables
- optimized asset variants;
- loader with static-first behavior;
- quality controller;
- semantic state controller;
- reduced-motion path;
- failure fallback;
- performance telemetry hooks;
- visual regression references.
