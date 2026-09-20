# BR-10 — Preliminary Web Performance & 3D Budgets

Status: PROVISIONAL

These are planning targets and may be tightened after prototypes.

## Experience tiers
### Tier A — Full
Capable desktop GPU/browser: interactive 3D, procedural motion, richer particles/shaders.

### Tier B — Balanced
Typical laptop/mobile: simplified geometry, lower DPR, reduced particles/effects, compressed textures.

### Tier C — Static/Safe
Low-power device, unsupported WebGL/WebGPU, data-saving or reduced-motion preference: pre-rendered/static visual with complete content and CTAs.

## Architecture rule
HTML/content/navigation/primary CTA must not depend on the 3D runtime becoming ready.

## Preliminary budgets
- Keep critical initial UI payload independent from hero 3D.
- Lazy-load noncritical 3D and below-fold media.
- Prefer compressed glTF/GLB pipeline.
- Texture resolution selected per actual screen contribution; avoid blanket 4K assets.
- Establish per-scene triangle/draw-call/texture-memory budgets during BR-11.
- Adaptive DPR and quality scaling required.
- No autoplay video required for core comprehension.

## Quality gates
Measure on real representative desktop and mobile profiles, not only developer workstation.
Targets must include Core Web Vitals, runtime FPS/frametime for 3D tiers, memory behavior, fallback success and no layout dependency on WebGL.

## Accessibility
- reduced motion respected;
- keyboard navigation independent of 3D;
- semantic content outside canvas;
- decorative canvas hidden appropriately from assistive tech;
- contrast validated;
- animation never required to understand product claims.
