# NXWEB-WO-0003-CP04-LOGO-EXPLORATION

Status: `COMPLETED`

## OBJECTIVE

Execute the CP-04 NexLabs logo exploration batch as a bounded, deterministic candidate study. Produce exactly nine reviewable candidates across the Topological N, Modular Core and Routed N families, with reproducible SVG masters, evaluation evidence and no canonical brand selection.

## CONTEXT/HIVE PREFLIGHT

This Work Order is bound to Context Lock `NXWEB-LOCK-0003-CP04-LOGO-EXPLORATION`, repository `KayzenRoot/nexlabs-web`, authorized base `b989606949bd362a2bd63d039448505f3220918e`, planning source `KayzenRoot/nexlabs-startup@b541e802472a3acc75a3a8ebd3818d33de8a316f`, GEF v1.0.0 and HIVE v1.0.0. The active Work Order must be prepared through `scripts/hive_prepare.py` without an override and the exact Work Order SHA-256 must be recorded in the lock and evidence.

## CANONICAL BASIS

The CP-04 planning cache under `.engineering/planning-snapshots/nexlabs-startup/b541e802472a3acc75a3a8ebd3818d33de8a316f/` is the pinned local mirror for BR-03, BR-04, BR-12, BR-17 and the related brand source documents. Tracked Git state, the checkpoint, source hierarchy and this Work Order remain authoritative.

## SCOPE

- Admit CP-04 with a new Work Order and Context Lock.
- Generate exactly `NX-D-01`, `NX-D-02`, `NX-D-03`, `NX-C-01`, `NX-C-02`, `NX-C-03`, `NX-B-01`, `NX-B-02`, and `NX-B-03`.
- Keep all masters monochrome, normalized SVG path geometry on a 12x12 construction grid, without baked generated text, gradients, motion or final 3D.
- Produce deterministic contact sheets, small-size and light/dark context comparisons, evaluation, provenance, candidate index and modest review artifacts.
- Attempt lightweight Blender MCP projection proof. If the external Blender addon is unavailable, record the exact blocker and do not claim a Blender pass.
- Use UGAS only as an optional exploration reference. Do not start providers, perform real generation, or mutate the frozen UGAS V1 source.
- Keep the candidate lab outside runtime brand wiring. Do not replace or promote `BrandMark` or publish a canonical NexLabs identity.

## OUT OF SCOPE

Canonical logo selection or approval, production BrandMark/favicon assets, final 3D geometry, animation, CP-05 through CP-08, paid/legal/domain/backend/auth/database/analytics work, trademark clearance, and merge before HG-01.

## FILES/SOURCES TO READ

- `AGENTS.md`
- `.engineering/SOURCE-HIERARCHY.md`
- `.engineering/gef/GEF-CURRENT.json`
- `docs/project-brain/13-CHECKPOINT.md`
- `docs/project-brain/03-SCOPE.md`
- `docs/project-brain/04-ARCHITECTURE.md`
- `docs/project-brain/10-SECURITY-GOVERNANCE.md`
- `docs/project-brain/15-DEFINITION-OF-DONE.md`
- `docs/project-brain/16-DECISIONS-LEDGER.md`
- `docs/DESIGN-SYSTEM.md`
- `docs/WORKSTATION-MODE.md`
- pinned CP-04 planning cache files in `.engineering/planning-snapshots/`

## REQUIREMENTS

Every candidate must have a stable ID, family, revision, construction grid, clean path-only SVG master, deterministic content hash, provenance record and evaluation row. Each candidate must be checked for 16 px, 24/32 px, 64/128 px, monochrome, dark/light, no-gradient, blur/squint, square avatar, horizontal lockup, reduced-motion and SVG cleanliness. Evaluation must retain strengths, weaknesses, PASS/FAIL dimensions, elimination rationale and similarity-risk caveat without computing a fake aggregate winner.

## ARCHITECTURE RULES

The candidate lab is a non-runtime source under `brand/logo/`. `scripts/logo_lab.py` is the deterministic generator and validator seam. Generated review sheets may contain labels and wordmarks, but symbol masters contain only normalized SVG paths. PNG/PDF generation is optional when the local renderer is unavailable; SVG review artifacts remain authoritative. No absolute paths, secrets or font binaries may enter tracked artifacts.

## CONSTRAINTS

No automatic winner. No canonical runtime wiring. No provider startup. No real UGAS generation. No heavy `.blend` files. No external similarity or trademark clearance is claimed. A missing Blender MCP is an external blocker for the 3D-proof criterion only and must not be silently converted into PASS.

## ACCEPTANCE CRITERIA

- The nine stable IDs exist exactly once and are represented in the deterministic index.
- Work Order, Context Lock, GEF current state, checkpoint and Source Hierarchy are exact-head consistent.
- HIVE preparation, project/task binding and minimum read-only context evidence are recorded, or the exact fail-closed blocker is recorded.
- SVG masters and review artifacts are deterministic, clean and validated by tests.
- Evaluation contains strengths, weaknesses, objective failures/repairs and no automatic selection.
- No runtime canonical logo wiring or CP-05+ work is present.
- Local static/security/release gates are run and reported truthfully.
- A protected PR may be opened only after the exact candidate head is green. Merge remains forbidden before HG-01.

## TESTS

```text
python -m py_compile scripts/validate_governance.py scripts/hive_bootstrap.py scripts/hive_prepare.py scripts/hive_mcp.py scripts/logo_lab.py
python scripts/logo_lab.py --check
python -m unittest discover -s tests -p "test_hive*.py" -v
python -m unittest discover -s tests -p "test_logo*.py" -v
npm run check
npm run test:e2e
npm run security
npm run validate:release
npx wrangler deploy --config wrangler.jsonc --dry-run
```

`validate:release` is expected to fail closed while the human selection and production promotion gates are intentionally incomplete.

## DELIVERABLES

`brand/logo/candidates/`, `brand/logo/review/`, `brand/logo/candidate-index.json`, `brand/logo/evaluation.md`, `brand/logo/provenance/`, the deterministic generator and tests, plus exact-head governance/HIVE evidence.

## REVIEW FORMAT

Report in PT-BR with exactly one state: `HUMAN_SELECTION_REQUIRED`, `CORRECTION REQUIRED`, or `BLOCKED`. Include exact Git/HIVE bindings, the nine IDs, objective failures and repairs, artifact locations, local/hosted checks, Blender/UGAS availability and external similarity-research gaps. Do not recommend a candidate.

## STOP CONDITION

After the full nine-candidate package, artifact validation, local gates, protected PR quality/Governance checks and exact-head evidence are green, stop at HG-01 with the Work Order `IN_PROGRESS`, Context Lock `OPEN`, review state `CP04_HUMAN_SELECTION_PENDING`, and no merge or canonical promotion.

## EXECUTION REFERENCES / CANONICAL REFERENCES

Source PDF: `NEXLABS-CP04-LOGO-EXPLORATION-WORK-ORDER.pdf`.
Planning source: `KayzenRoot/nexlabs-startup@b541e802472a3acc75a3a8ebd3818d33de8a316f`.
UGAS V1 frozen source: `0169f84248703931bb7578177d9773bce319c14e`.
