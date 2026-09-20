# BR-12 — UGAS Asset Pipeline

Status: SYSTEM ARCHITECTURE
Date: 2026-09-19
Role: multimodal exploration, production support and derivative media
Canonical brand authority: NexLabs Brand/Web specifications

## 1. Purpose
Use UGAS to accelerate visual exploration and media production without allowing generated output to redefine the NexLabs identity.

Governance hierarchy:
Brand Bible / approved BR specs
→ approved visual direction
→ UGAS exploration/production
→ review gate
→ Blender/web integration
→ release assets.

## 2. Responsibility boundary

### Brand/Web specs own
- identity;
- geometry grammar;
- palette;
- typography;
- motion semantics;
- messaging;
- acceptance criteria.

### UGAS owns
- visual exploration;
- concept frames;
- texture/material source exploration;
- backgrounds;
- derivative renders;
- social/launch media;
- motion/video production support;
- image optimization workflow support where appropriate.

### Blender owns
- canonical 3D geometry;
- canonical cameras;
- canonical 3D materials/reference look;
- 3D animation source;
- canonical high-quality renders.

### Codex owns
- automation/integration;
- deterministic pipelines;
- asset validation;
- manifests;
- web optimization/build;
- production wiring.

UGAS output does not automatically become canonical.

## 3. Asset lifecycle
EXPLORE
→ CANDIDATE
→ REVIEW
→ APPROVED_SOURCE
→ PRODUCTION
→ OPTIMIZED
→ RELEASED
→ ARCHIVED/SUPERSEDED

Only APPROVED_SOURCE or later may feed production builds.

## 4. Asset classes

### A — Concept
Mood frames, composition experiments, material ideas, lighting studies.
Never shipped directly unless separately promoted through review.

### B — Source
Approved input used to build a production asset.

### C — Production
Canonical high-quality working asset.

### D — Web
Optimized derivative for website/runtime.

### E — Social
Open Graph, launch image, social card, campaign crop.

### F — Motion
Video/motion derivative.

### G — Archive
Superseded but traceable source/release history.

## 5. Planned directory model
```
assets/
├─ explore/
├─ candidates/
├─ approved-source/
├─ production/
│  ├─ brand/
│  ├─ three/
│  ├─ images/
│  ├─ motion/
│  └─ social/
├─ web/
├─ release/
├─ manifests/
└─ archive/
```

The actual storage/repository split is decided during implementation to avoid bloating the web Git repository with heavy source files.

## 6. Visual exploration
UGAS may explore:
- Computational Matter;
- Dark Mineral Laboratory;
- mineral/ceramic/optical surfaces;
- spectral signal energy;
- topology;
- routing;
- macro structural photography-like renders;
- Context Core compositions.

Exploration must preserve BR-01/04/05 constraints.

## 7. Exploration constraints
Reject by default:
- robot/brain AI clichés;
- generic glowing orb;
- cyberpunk city;
- crypto token imagery;
- random circuitry;
- rainbow AI gradients;
- excessive neon;
- unrelated sci-fi machinery;
- fake UI/text/logos generated into final assets.

## 8. Texture/material source
UGAS may create/reference texture concepts and source imagery.

Before production:
- verify provenance/licensing where external material is involved;
- remove generated text/logos/artifacts;
- validate tiling/scale;
- derive web-appropriate maps only when needed;
- record source lineage.

Do not use AI-generated texture detail to conceal poor 3D/material design.

## 9. Concept-frame protocol
Each exploration batch should define:
- objective;
- scene/asset id;
- brand constraints;
- aspect ratio;
- intended use;
- variations count;
- rejection criteria.

Avoid unlimited prompt iteration without decision checkpoints.

## 10. Review contact sheets
Exploration batches should produce review sheets with:
- candidate id;
- thumbnail;
- short rationale;
- known issues;
- intended destination.

Approved candidate ids become traceable source references.

## 11. Blender handoff
When UGAS exploration informs Blender:
- provide approved frame(s);
- identify what is authoritative: composition, material, lighting, geometry idea, or atmosphere;
- do not ask Blender MCP to copy accidental generated artifacts;
- translate concept into BR-11 primitives/materials.

## 12. Social system
Planned derivative formats:
- Open Graph;
- GitHub/social preview where applicable;
- X/LinkedIn launch graphics if accounts exist;
- portrait/vertical social;
- square;
- widescreen presentation.

Do not create empty social-channel assets before a real publishing destination exists unless they are reusable templates.

## 13. OG cards
Prefer deterministic brand templates driven by:
- NexLabs mark;
- page/product title;
- controlled Computational Matter visual;
- canonical tokens.

UGAS may produce background/source imagery, but text/layout should be programmatically controlled where possible for accuracy.

## 14. Video/motion
Future optional outputs:
- 5–8 s logo ident;
- 10–20 s website/launch teaser;
- 30–60 s institutional/product overview;
- HIVE technical explainer sequences.

These are not blockers for V1 website launch unless explicitly promoted to scope.

## 15. Audio
No website autoplay audio.
UGAS may later create sonic identity/audio for video assets under a separate approval gate.

## 16. Provenance manifest
For each production/released asset record:
- asset id;
- purpose;
- source type;
- UGAS workflow/version where applicable;
- generation/editing notes;
- source references;
- human/Blender modifications;
- license/provenance status;
- approval status;
- output dimensions;
- format;
- content hash;
- release destinations.

Do not store secrets/API keys in provenance.

## 17. Naming
Pattern:
NL_<AREA>_<ASSET>_<VARIANT>_<VERSION>

Examples:
NL_BRAND_ContextCore_Hero_v001
NL_SOCIAL_HIVE_OG_v001
NL_TEXTURE_Mineral_A_v002

Production/release names should be deterministic and human-readable.

## 18. Optimization
Master/source assets remain lossless/high-quality where justified.
Delivery derivatives use fit-for-purpose compression.

Website image pipeline should prefer:
- responsive dimensions;
- AVIF/WebP where compatible;
- metadata stripping where appropriate;
- quality review after compression.

Never optimize the only source copy destructively.

## 19. Quality gates
UG1 Brand compliance
UG2 Composition
UG3 Artifact inspection
UG4 Text/logo integrity
UG5 Provenance
UG6 Technical resolution
UG7 Destination crop
UG8 Compression quality
UG9 Accessibility/meaning
UG10 Release manifest

## 20. AI-generated asset rule
Generated media is a production input, not unquestioned truth.
Human/brand review remains mandatory for public identity assets.

## 21. Repository/storage rule
Heavy binary source files should not automatically live in the application repository.
BR-16/implementation decides Git LFS, release storage, cloud object storage or local canonical archive based on zero-cost limits and operational needs.

## 22. Acceptance
BR-12 freezes when:
- UGAS responsibility boundary is clear;
- lifecycle prevents accidental publishing;
- Blender handoff is explicit;
- provenance exists;
- social/OG pipeline is defined;
- optimization rules exist;
- no UGAS dependency is required for runtime website operation.
