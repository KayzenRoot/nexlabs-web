# NXWEB-WO-0007-CP08-UGAS-DERIVATIVE-MEDIA-RELEASE-VISUALS

Status: `IN_PROGRESS`

## OBJECTIVE

Complete CP-08 as a deterministic, no-generation, provenance-first derivative-media package from protected main `d971047d25dc01e7338aba369ea1bd7cf7452490`. Produce release-ready supporting visuals while keeping every asset `PRODUCTION` or `OPTIMIZED`; this work order does not release or deploy anything.

## AUTHORITY / PREFLIGHT

Repository: `KayzenRoot/nexlabs-web`. Context Lock: `NXWEB-LOCK-0007-CP08-UGAS-DERIVATIVE-MEDIA-RELEASE-VISUALS`. Source PDF: `NEXLABS-CP08-DERIVATIVE-MEDIA-RELEASE-VISUALS-WORK-ORDER.pdf`, SHA-256 `B89CC978F695CD990AE3D4D8A473AF5DF53B47EA161411D7432E782C65718990`. Protected base: `d971047d25dc01e7338aba369ea1bd7cf7452490`; CP-07 merge PR #33 is verified at this commit with post-merge Governance run `35671341225` and quality run `35671341040`, both successful.

Use GEF/HIVE v1.0.0 and the verified immutable planning cache `KayzenRoot/nexlabs-startup@b541e802472a3acc75a3a8ebd3818d33de8a316f`. Run `scripts/hive_prepare.py` with no Work Order override after admission and bind its exact Work Order digest, task, project, index/corpus receipts and bounded Core context result to evidence. The explicitly admitted `HIVE_MCP_DEGRADED_SAFE` path applies only when HIVE API preparation and bounded Core context succeed but the read-only MCP transport alone closes; never claim an MCP PASS unless observed.

## SCOPE

- Create deterministic tracked templates, source/output manifests, contact sheet, per-asset BR-12 provenance, machine-readable and human-readable UG1–UG10 reports, generators, validators and tests under `artifacts/cp08/` and `scripts/cp08/`.
- Produce local 1200x630 Open Graph cards for the existing NexLabs default, HIVE and Technology destinations, preserving canonical copy and using only approved local inputs.
- Produce one 1280x640 GitHub repository social-preview image and one reusable generic social template. Do not invent an X/LinkedIn destination, handle or social proof.
- Produce 16:9, 4:5 and 1:1 responsive static hero delivery derivatives from accepted CP-06/CP-07 images. Preserve framing, never upscale, retain the accepted sources, strip nonessential metadata safely, and emit deterministic WebP/AVIF when local Pillow codecs support them.
- Bind source/output dimensions, byte counts, SHA-256, codec settings and measured visual-parity results. Wire local Open Graph assets into existing metadata without changing canonical text.
- Validate source parity, dimensions/formats, text, paths, provenance, destinations, no placeholders/fabricated claims, all ten UG gates, and no-generation/no-release/no-deployment/no-CP-09 boundaries.

## OUT OF SCOPE / HARD BOUNDARIES

- Do not start or configure UGAS/ComfyUI/providers; do not perform UGAS generation. `ugas` core installation is not generation readiness or authorization.
- Do not change logo direction, canonical identity, site copy, CP-06/CP-07 source assets, create long-form video/audio, add social accounts, start CP-09, deploy, publish a production release, or merge.
- Do not mark any asset `RELEASED`, invent approval identities/timestamps, add unverified external inputs, or destructively alter the only accepted source copy.

## ACCEPTANCE CRITERIA

1. Work Order, Context Lock and HIVE task are bound to the exact CP-08 Work Order digest and protected base; project/task/index/corpus and extracted text are READY/COMPLETED. Record bounded Core context and truthful MCP status.
2. Three metadata destinations resolve to committed local OG cards, with existing canonical title/description unchanged.
3. Repository preview and reusable generic template exist; no fake social destination or account appears.
4. All three hero framings preserve their source dimensions and composition intent with no upscale; supported WebP/AVIF derivatives are smaller, format-valid and pass a documented visual-parity threshold. Accepted source bytes remain unchanged.
5. Every production/optimized asset has a complete BR-12 record, truthful null UGAS fields, `external_inputs: []`, complete outputs and no release/approval fiction. The top-level manifest and size/hash report are reproducible.
6. UG1 Brand compliance, UG2 Composition, UG3 Artifact inspection, UG4 Text/logo integrity, UG5 Provenance, UG6 Technical resolution, UG7 Destination crop, UG8 Compression quality, UG9 Accessibility/meaning and UG10 Release manifest all PASS with machine and human-readable reports; no HIGH/CRITICAL defect passes.
7. CP-08 validators and automated tests prove dimensions/formats, source/output hashes, canonical text, metadata-local-asset links, provenance, no placeholders/fabricated facts, no provider startup/generation, no CP-09 and no deployment.
8. Required Python, HIVE, CP-06, Node/npm, E2E, security, release-validation and Wrangler dry-run checks pass at the exact final candidate head. One protected PR is open and exact-head Governance and quality are green.

## REQUIRED VALIDATION

`python -m py_compile scripts/validate_governance.py scripts/hive_bootstrap.py scripts/hive_prepare.py scripts/hive_mcp.py`

`python scripts/validate_governance.py`

`python -m unittest discover -s tests -p "test_hive*.py" -v`

`python -m unittest discover -s tests -p "test_cp06*.py" -v`

`python scripts/cp06/validate_assets.py`

`python -m py_compile scripts/cp08/*.py`

`python -m unittest discover -s tests -p "test_cp08*.py" -v`

`npm run typecheck`, `npm run lint`, `npm run test`, `npm run validate`, `npm run check`, `npm run test:e2e`, `npm run security`, `npm run validate:release`, and `npx wrangler deploy --config wrangler.jsonc --dry-run`.

## DELIVERABLES / STOP CONDITION

Record exact base/head/branch, Work Order and Context Lock digests, HIVE evidence, source and output hashes, every asset destination/status, optimization byte table, ten gate verdicts, local validation matrix and exact-head PR check IDs. Stop with one protected CP-08 PR open, quality and Governance green, and independent review requested. Do not merge or begin CP-09. Confirm provider startup/generation, identity changes and deployment did not occur.
