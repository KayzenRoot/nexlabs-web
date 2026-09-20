# BR-11 — Blender MCP Production Specification

Status: PRODUCTION CONTRACT — PLANNING
Date: 2026-09-19
Execution: deferred to Codex + Blender MCP

## 1. Purpose
Translate NexLabs brand/3D decisions into deterministic Blender production rules so execution does not require Codex to invent art direction.

## 2. Master-file model
Canonical source:
NL_BRAND_3D_MASTER.blend

Scene packages may later be separated for performance/versioning, but the canonical relationships, materials, cameras and procedural definitions must remain traceable to the master.

Never treat exported GLB as source of truth.

## 3. Units and transforms
- Metric units.
- Consistent scale appropriate for Blender/web export.
- Apply transforms on export-ready meshes unless a documented runtime requirement needs otherwise.
- Intentional object origins.
- No unexplained negative scale.
- No hidden scale compensation in parent chains.
- Canonical forward/up orientation documented and tested against web importer.

## 4. Collection architecture
NL_MASTER
├─ NL_CORE
├─ NL_SHELLS
├─ NL_ROUTES
├─ NL_NODES
├─ NL_LATTICE
├─ NL_CELLS
├─ NL_BANDS
├─ NL_FRAGMENTS
├─ NL_GATES
├─ NL_FIELDS
├─ NL_LIGHTS
├─ NL_CAMERAS
├─ NL_MATERIALS_REF
├─ NL_HELPERS
├─ NL_RENDER_ONLY
├─ NL_EXPORT_HIGH
├─ NL_EXPORT_MED
└─ NL_EXPORT_LOW

Export collections contain only validated runtime assets.

## 5. Naming
Pattern:
NL_<TYPE>_<NAME>_<VARIANT>[_<LOD>]

Examples:
NL_CORE_Context_A
NL_SHELL_Context_01
NL_ROUTE_Primary_01
NL_NODE_Index_03
NL_CAM_Hero_A
NL_LIGHT_KeySculpt_A
NL_MAT_Mineral_A
NL_CORE_Context_A_HIGH

No Cube.001 / Material.003 style production names.

## 6. Geometry rules
- silhouette first;
- topology supports deformation/animation where required;
- avoid invisible geometry;
- repeated structures use instances where practical;
- procedural generation uses deterministic seeds;
- modifiers remain non-destructive until a production/export reason requires baking;
- web LODs preserve silhouette and semantic structure before microdetail.

## 7. Geometry Nodes
Use Geometry Nodes for systems that benefit from parameterization:
- route distributions;
- lattice/cell repetition;
- fragment fields;
- controlled shell variants;
- node placement;
- selected topology effects.

Every production node group needs:
- descriptive name;
- exposed inputs only when meaningful;
- sane defaults;
- seed input where randomness exists;
- short purpose note in production manifest.

Do not build an unreadable node graph merely to call it procedural.

## 8. Canonical parameters
Planned exposed controls may include:
- Seed
- Density
- LayerCount
- RouteCount
- Thickness
- CoreScale
- FragmentSpread
- SignalBias
- DetailLevel

Final set depends on the primitive.

## 9. Material library
Canonical families:
NL_MAT_Mineral
NL_MAT_Ceramic
NL_MAT_Optical
NL_MAT_SignalCyan
NL_MAT_SignalViolet
NL_MAT_SignalWarm
NL_MAT_Data

Each material records:
- visual purpose;
- Blender reference values;
- web approximation;
- texture dependencies;
- transparency/transmission needs;
- emission behavior.

High-end Blender appearance and web material may differ intentionally while preserving identity.

## 10. Lighting
Canonical rigs:
NL_LIGHT_KeySculpt
NL_LIGHT_RimStructure
NL_LIGHT_EnvMineral
NL_LIGHT_DetailMacro

Signal illumination should primarily originate from material/system behavior, not dozens of arbitrary lights.

## 11. Cameras
NL_CAM_Hero
NL_CAM_Projection
NL_CAM_Macro
NL_CAM_Review

For each approved camera store:
- transform;
- focal length/FOV relationship;
- sensor assumptions if relevant;
- target/composition notes;
- safe area for HTML copy;
- expected aspect-ratio adaptations.

## 12. Hero safe area
The canonical hero composition must reserve negative space for semantic HTML.

No baked text in hero renders.
No critical logo copy embedded solely in 3D.

## 13. Animation
Semantic clips/actions:
NL_ANIM_Dormant
NL_ANIM_Intake
NL_ANIM_Index
NL_ANIM_Retrieve
NL_ANIM_Assemble
NL_ANIM_Resolve
NL_ANIM_Idle

Where runtime control is superior, Blender provides reference animation/poses rather than forcing a baked timeline.

## 14. Animation constraints
- deterministic;
- loop boundaries clean where loops exist;
- no random unbounded drift;
- stable resolved state;
- root/object transforms documented;
- avoid excessive keyframe density;
- optimize curves before export where safe.

## 15. LOD production
HIGH:
brand-rich geometry/material structure.

MED:
preserve silhouette and major context layers; reduce internal detail.

LOW:
preserve core identity and primary signal paths; aggressive simplification.

STATIC:
rendered first-class fallback.

LOD is authored/validated, not only an automatic decimation percentage.

## 16. UV/textures
- UV only where needed;
- consistent texel strategy;
- no unused image textures packed into exports;
- no blanket 4K;
- texture names deterministic;
- external/generated textures tracked by manifest;
- optimize/compress downstream after visual validation.

## 17. Web export
Preferred interchange:
glTF/GLB.

Export must validate:
- orientation;
- scale;
- object names needed at runtime;
- material compatibility;
- animation clips;
- no helper/render-only objects;
- no unintended cameras/lights unless explicitly needed;
- no unused payload.

## 18. Export pipeline
MASTER
→ validate source
→ select export collection
→ duplicate/bake only as pipeline requires
→ optimize geometry
→ validate materials
→ export GLB
→ run glTF validation/inspection
→ optimize/compress
→ browser preview
→ compare against reference
→ record manifest/hash.

## 19. Render outputs
Required Context Core reference renders:
- hero dark canonical;
- hero static fallback;
- light-system reference;
- macro detail;
- logo projection proof where applicable;
- thumbnail/contact sheet for review.

Prefer reproducible render settings stored in file.

## 20. Static fallback
Fallback composition must match HTML layout/crop.
Generate responsive framing variants where necessary rather than one universal image.

## 21. Source cleanliness
Before acceptance:
- no orphan production junk;
- no unnamed objects/materials;
- no accidental duplicate meshes;
- no missing external resources;
- no hidden high-poly object leaking into export;
- no unsupported production dependency without documentation.

## 22. Manifest
Every exported scene/package receives a machine-readable manifest containing at least:
- scene id;
- source revision;
- source file;
- export tier;
- export filename;
- content hash;
- object/mesh count;
- triangle count;
- material count;
- texture list;
- animation list;
- bounding box;
- approximate transfer size after web optimization;
- fallback asset;
- license/provenance notes for any external input.

## 23. Versioning
Do not overwrite approved production assets without version traceability.
Source commit + manifest + asset hash must allow reconstruction of what was deployed.

## 24. Validation gates
G1 Source hygiene
G2 Geometry/topology
G3 Materials
G4 Animation
G5 Camera/composition
G6 Export integrity
G7 Web visual parity
G8 Performance budget
G9 Fallback
G10 Manifest/provenance

Failure of a gate blocks production acceptance.

## 25. MCP execution rule
Codex/Blender MCP work orders must:
1. read current canonical brand/3D specs;
2. modify only declared scope;
3. save source;
4. generate requested review renders/metrics;
5. validate gates;
6. report deviations;
7. stop at work-order STOP CONDITION.

No autonomous aesthetic expansion beyond approved design language.

## 26. Acceptance
BR-11 freezes when:
- master scene structure is complete;
- naming/export conventions are unambiguous;
- Context Core can be decomposed into work orders;
- manifests/gates are specified;
- Codex can execute without inventing visual direction;
- web team can consume outputs without reopening Blender design decisions.
