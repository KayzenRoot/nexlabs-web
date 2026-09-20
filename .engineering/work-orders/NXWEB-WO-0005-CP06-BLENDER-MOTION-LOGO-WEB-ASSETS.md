# NXWEB-WO-0005-CP06-BLENDER-MOTION-LOGO-WEB-ASSETS

Status: `IN_PROGRESS`

## OBJECTIVE

Admit CP-06 as one governed GEF/HIVE increment and extend the approved CP-05 Context Core source through WO-B3D-012. Produce a deterministic, versioned HIGH/MED/LOW/STATIC asset package for CP-07 consumption, stopping before web runtime integration.

## CONTEXT/HIVE PREFLIGHT

This Work Order is bound to Context Lock `NXWEB-LOCK-0005-CP06-BLENDER-MOTION-LOGO-WEB-ASSETS`, repository `KayzenRoot/nexlabs-web`, protected base `9b502c1d618e93e1be45864acf19648e132515c6`, planning source `KayzenRoot/nexlabs-startup@b541e802472a3acc75a3a8ebd3818d33de8a316f`, GEF v1.0.0 and HIVE v1.0.0. Run `scripts/hive_prepare.py` without an override after this Work Order is active. Bind the exact Work Order SHA-256 to the Context Lock, HIVE task and evidence.

## CANONICAL BASIS

Read the repository authority in the established order, verify the immutable planning cache MANIFEST, and read the CP-05 Work Order, Context Lock, evidence and manifests before production mutation. The CP-06 source cache is authoritative for the BR-03, BR-04, BR-05, BR-06, BR-09, BR-10, BR-11, BR-12 and BR-17 rules named by this Work Order.

## SCOPE

- `WO-B3D-007`: deterministic semantic animation for DORMANT, INTAKE, INDEX, RETRIEVE, ASSEMBLE, RESOLVE and IDLE, including bounded transitions and a resolved/reduced-motion reference.
- `WO-B3D-008`: controlled 3D projection of selected logo `NX-C-02 r1` from the immutable SVG, orthographic projection proof, PFR metrics and motion-logo reference.
- `WO-B3D-009`: authored semantic HIGH, MED and LOW variants plus first-class STATIC fallback, with LIPG identity evidence and BR-10 budgets.
- `WO-B3D-010`: deterministic validated HIGH/MED/LOW GLB exports, export collections, EBL metrics, round-trip validation and isolated browser-oriented parity evidence.
- `WO-B3D-011`: canonical resolved hero fallback, responsive crops, macro/detail and light-system references, contact sheet and suitable OG-compatible source.
- `WO-B3D-012`: BR-11 G1-G10 final acceptance, machine-readable and human-readable gate reports, provenance and final package manifest.
- Create `scripts/cp06/`, `artifacts/cp06/`, ignored `.local/cp06/` working masters/exports and final accepted GLBs only under the approved production asset path.

## OUT OF SCOPE

- CP-07 Three.js, React Three Fiber, runtime loading, adaptive fidelity controller and production route wiring.
- Production BrandMark, header or favicon replacement.
- Production deployment, domain, launch, analytics or visitor telemetry.
- UGAS generation, provider startup or UGAS derivative media.
- CP-08 media and any unapproved public brand claim.
- Mutation of `.local/cp05/context_core_master.blend` or recreation of a different CP-05 scene.

## BLENDER/MCP GATE

- Blender production is authorized only under the active Work Order and a passing live MCP hard preflight.
- Record the actual Blender version, add-on/protocol, `get_addon_status` and `get_scene_info` results immediately before scene mutation.
- One bounded recovery/reconnect is permitted. If the live path remains unavailable, stop `BLOCKED` with exact diagnostics.
- UGAS generation remains unauthorized and unready; do not start a provider or generation.

## REPOSITORY AND DETERMINISM

- Recover the CP-05 master by exact SHA `8a83889dcf012f1917a2bb2d9286369490ba5d576183aafef586e37a307142dd` and copy/derive it under `.local/cp06/`; never mutate the CP-05 master in place.
- Require scene id `NL-SCENE-CONTEXT-CORE-01` and fingerprint `eb409383e8ffab522da6b162940e6bd3a46e44f89f73f3ceeb1cc45c017c0e61` before mutation.
- Verify `brand/logo/candidates/NX-C-02.svg` SHA-256 `16daeac469520dbae6ba224dbd87bc8f07510c734940d35412248f32d2364165` before import; the 2D source remains unchanged.
- Use deterministic seeds, versioned filenames and source/parameter/hash receipts. Blender remains the canonical source; GLB is interchange only.
- Preserve static-first and reduced-motion behavior in the asset package. No baked essential text.

## ACCEPTANCE CRITERIA

- Work Order, Context Lock and HIVE task are exact-base/digest bound and READY/extracted.
- Planning cache validates against MANIFEST.json.
- CP-05 source is exact-hash recovered and exact-fingerprint verified before CP-06 mutation.
- Blender MCP hard preflight passes immediately before mutation.
- WO-B3D-007 through WO-B3D-012 each have explicit PASS evidence.
- Seven semantic actions/clips and resolved/static reference are reproducible.
- NX-C-02 projection is hash-bound and PFR-reviewed without changing the SVG.
- HIGH/MED/LOW preserve identity and meet BR-10 transfer, triangle and draw-call targets; otherwise stop for documented correction.
- Validated versioned GLBs, EBL metrics, round-trip receipts and browser-oriented parity evidence exist.
- STATIC fallback pack is complete, responsive, provenance-bound and within the typical 250 KiB target where quality permits.
- G1-G10 all PASS with no unresolved HIGH/CRITICAL issue.
- No CP-07/runtime wiring, BrandMark change or UGAS generation appears in the branch.
- Local validation is green and protected PR quality/Governance pass on the exact candidate head.

## TESTS

- `python -m py_compile scripts/validate_governance.py scripts/hive_bootstrap.py scripts/hive_prepare.py scripts/hive_mcp.py`
- `python scripts/validate_governance.py`
- `python -m unittest discover -s tests -p "test_hive*.py" -v`
- `python -m py_compile scripts/cp06/*.py`
- `python -m unittest discover -s tests -p "test_cp06*.py" -v`
- Detected Blender CP-06 builder, animation, LOD, export, round-trip and package validators.
- Selected pinned zero-cost glTF validator/inspection tool.
- `npm run check`, `npm run test:e2e`, `npm run security`, `npm run validate:release` and `npx wrangler deploy --config wrangler.jsonc --dry-run`.

## DELIVERABLES

- Exact base/head/branch, Work Order digest, Context Lock and HIVE task/receipts.
- CP-05 reconstruction receipt and Blender/MCP preflight receipt.
- SSAC, PFR, LIPG and per-tier EBL receipts.
- Versioned HIGH/MED/LOW GLBs and static fallback pack with hashes.
- Top-level CP-06 asset manifest/provenance and `cp06-asset-acceptance.json` plus human gate report.
- Local validation matrix and protected PR number with exact-head quality/Governance run IDs.

## REVIEW FORMAT

Return exactly one verdict: `APPROVED`, `CORRECTION REQUIRED` or `BLOCKED`. Report WO-B3D-007 through WO-B3D-012 separately, then HIVE, Blender/MCP, semantic animation, logo projection, LOD budgets, GLB validation, STATIC fallback, G1-G10, tests and hosted checks.

## STOP CONDITION

Stop only when WO-B3D-007 through WO-B3D-012 are complete and auditable, the HIGH/MED/LOW/STATIC package is final-asset accepted, the branch is pushed, one protected CP-06 PR is open, and quality plus Governance are green on its exact head. Do not merge and do not begin CP-07.

## EXECUTION REFERENCES / CANONICAL REFERENCES

- `NEXLABS-CP06-BLENDER-MOTION-LOGO-WEB-ASSETS-WORK-ORDER.pdf`
- `docs/project-brain/13-CHECKPOINT.md`
- `docs/project-brain/16-DECISIONS-LEDGER.md`
- `docs/project-brain/03-SCOPE.md`
- `docs/project-brain/15-DEFINITION-OF-DONE.md`
- `docs/project-brain/04-ARCHITECTURE.md`
- `docs/project-brain/02-REQUIREMENTS.md`
- `docs/project-brain/10-SECURITY-GOVERNANCE.md`
- `.engineering/SOURCE-HIERARCHY.md`
- `docs/WORKSTATION-MODE.md`
- `.engineering/planning-snapshots/nexlabs-startup/b541e802472a3acc75a3a8ebd3818d33de8a316f/MANIFEST.json`
- `.engineering/work-orders/NXWEB-WO-0004-CP05-BLENDER-CONTEXT-CORE-FOUNDATION.md`
- `.engineering/context-locks/NXWEB-LOCK-0004-CP05-BLENDER-CONTEXT-CORE-FOUNDATION.json`
- `.engineering/evidence/NXWEB-WO-0004-CP05-BLENDER-CONTEXT-CORE-FOUNDATION.json`
- `artifacts/cp05/*` and `.local/cp05/context_core_master.blend`
