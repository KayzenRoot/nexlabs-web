# CP06 Asset Acceptance — G1-G10

Status: `PASS`

Source scene: `NL-SCENE-CONTEXT-CORE-01` from `.local/cp06/context_core_cp06_master.blend`.
Blender: `5.2.1 LTS`; Blender MCP add-on `1.7`; protocol `7`.
Selected logo: `NX-C-02 r1`, source SVG unchanged and SHA-bound.

| Gate | Result | Evidence |
| --- | --- | --- |
| G1 Source hygiene | PASS | Deterministic names, no external GLB buffers, CP05 source untouched |
| G2 Geometry/topology | PASS | HIGH/MED/LOW GLB inspection; 1,428 / 1,268 / 1,108 triangles |
| G3 Materials | PASS | Three bounded materials per export and no missing external resources |
| G4 Animation | PASS | DORMANT, INTAKE, INDEX, RETRIEVE, ASSEMBLE, RESOLVE, IDLE in each tier |
| G5 Camera/composition | PASS | Orthographic logo projection proof and 16:9, 4:5, 1:1 renders |
| G6 Export integrity | PASS | Self-contained glTF 2.0 GLBs with exact hashes |
| G7 Web visual parity | PASS | Isolated GLB structure/name parity; CP-07 runtime remains out of scope |
| G8 Performance budget | PASS | Tier byte/triangle budgets recorded in `cp06-asset-manifest.json` |
| G9 Fallback | PASS | Static-first responsive PNG fallback and reduced-motion identity |
| G10 Manifest/provenance | PASS | Machine manifest, GLB inspection, provenance and contact sheet |

No CP-07 runtime, production BrandMark, UGAS generation or deployment was introduced.
