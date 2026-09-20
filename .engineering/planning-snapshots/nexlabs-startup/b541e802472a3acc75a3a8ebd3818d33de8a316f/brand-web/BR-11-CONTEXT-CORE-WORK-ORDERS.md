# BR-11 — Context Core Blender Work-Order Map

Status: PLANNED
Execution: NOT STARTED
Scene: NL-SCENE-CONTEXT-CORE-01

The work orders below are execution units, not prompts yet. BR-17 will package them for Codex.

## WO-B3D-001 — Bootstrap & Scene Hygiene
Scope:
- establish Blender master;
- units/orientation;
- collection tree;
- naming;
- canonical render settings;
- placeholder cameras/lights;
- manifest skeleton.

STOP CONDITION:
Clean deterministic master file opens without missing resources and passes source-hygiene gate.

## WO-B3D-002 — Primitive Foundation
Scope:
- Core;
- Shell;
- Route;
- Node;
- Lattice;
- Cell;
- Band;
- Fragment;
- Gate;
- Field.

Deliver reusable primitive source definitions and review sheet.

STOP CONDITION:
All ten primitives exist, are named, parameterized where appropriate and visually belong to one system.

## WO-B3D-003 — Material System
Scope:
- Mineral;
- Ceramic;
- Optical;
- Signal Cyan;
- Signal Violet;
- Signal Warm;
- Data.

Deliver material sphere/object reference sheet plus web-approximation notes.

STOP CONDITION:
Materials coexist under canonical rig and preserve BR-04 hierarchy.

## WO-B3D-004 — Context Core Structural Assembly
Scope:
- central core;
- nested shells;
- routing envelope;
- inner lattice;
- gates;
- outer field.

No final animation yet.

STOP CONDITION:
Static hero silhouette/composition approved in monochrome/material-neutral and branded material passes.

## WO-B3D-005 — Data Matter & Procedural Fields
Scope:
- deterministic fragments;
- node distributions;
- routing fields;
- density/seed controls;
- performance-aware instancing.

STOP CONDITION:
Data matter produces controlled repeatable compositions without random-confetti behavior.

## WO-B3D-006 — Lighting & Camera
Scope:
- Hero;
- Projection;
- Macro;
- Review cameras;
- Key/Rim/Environment rigs;
- HTML safe area.

STOP CONDITION:
Hero works at target aspect ratios and retains readable silhouette/negative space.

## WO-B3D-007 — Semantic Animation
Scope:
Dormant → Intake → Index → Retrieve → Assemble → Resolve → Idle.

STOP CONDITION:
Every transition communicates its named system state and resolved state becomes visually calmer.

## WO-B3D-008 — Logo Projection Integration
Depends on final BR-03 logo selection.

Scope:
- reconcile logo geometry with canonical 3D object;
- projection camera;
- motion-logo reference;
- 2D projection proof.

STOP CONDITION:
Approved static mark and 3D source relationship are reproducible.

## WO-B3D-009 — LOD & Web Variants
Scope:
- HIGH;
- MED;
- LOW;
- semantic simplification;
- material simplification;
- particle/instance budgets.

STOP CONDITION:
Each tier preserves identity and meets its BR-10 geometry targets or has documented approved exception.

## WO-B3D-010 — Web Export Pipeline
Scope:
- export collections;
- GLB;
- validation;
- optimization/compression experiment;
- object/material/animation checks;
- manifest generation.

STOP CONDITION:
Browser-loadable validated artifacts with reproducible source/hash trail.

## WO-B3D-011 — Static Fallback & Render Pack
Scope:
- hero fallback;
- responsive crops;
- macro reference;
- light-system reference;
- review contact sheet;
- OG-compatible visual source if suitable.

STOP CONDITION:
Site can look intentional with all live 3D disabled.

## WO-B3D-012 — Final Asset Acceptance
Scope:
- source hygiene;
- visual parity;
- budgets;
- browser inspection;
- missing resources;
- manifests;
- provenance;
- release bundle.

STOP CONDITION:
All BR-11 G1–G10 gates pass and production asset package is ready for web integration.

# Execution strategy
Preferred execution later:
- one broad Codex prompt may contain multiple adjacent work orders;
- each work order still retains an independent checkpoint and STOP CONDITION;
- review output is required before irreversible/final acceptance decisions;
- failures are corrected at the smallest affected work order.

# Dependency chain
001
→ 002
→ 003
→ 004
→ 005
→ 006
→ 007
→ 008 (after logo freeze)
→ 009
→ 010
→ 011
→ 012

Some production work may parallelize after 004, but BR-17 decides safe batching.
