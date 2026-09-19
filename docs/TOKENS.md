# NexLabs token contract

Status: `provisional-engineering`. The values in `design/tokens/source.json` are a replaceable engineering candidate, not final brand identity or approved artwork.

The source is organized as primitive values, semantic roles, component mappings, and a future-media bridge:

`primitive -> semantic -> component -> consuming UI`

`npm run build:tokens` deterministically produces `design/tokens/generated.css`, `design/tokens/generated.ts`, and `public/brand/tokens.json`. `npm run validate:tokens` checks the schema, required mappings, references, dark/light coverage, contrast pairs, and generated-file drift. It is part of `npm run validate` and therefore the required CI quality path.

The candidate palette is a dark mineral laboratory with controlled Spectral Cyan, Ion Violet, rare warm signal, functional states, spacing, typography, container, border, radius, shadow, motion, z-index, and breakpoint scales. Raw colors and arbitrary spacing do not belong in components. Theme values use explicit dark/light mappings; no mechanical inversion is used.

The `bridge.three.*` group is a stable future interface only. It does not add Three.js, R3F, Blender, UGAS, or a 3D runtime to this checkpoint.
