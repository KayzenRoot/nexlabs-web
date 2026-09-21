# NXWEB-WO-0006-CP07-WEB-3D-RUNTIME-ADAPTIVE-FIDELITY

Status: `IN_PROGRESS`

## OBJECTIVE

Admit CP-07 as one governed GEF/HIVE increment from protected main `d01288967fca590029166e4b8532cdfd7fad5877`. Integrate the approved CP-06 Context Core HIGH/MED/LOW/STATIC package into the H01 homepage hero through an isolated, static-first Three.js/React Three Fiber boundary. The page remains complete and accessible when JavaScript, WebGL, animation, model loading or the live runtime is unavailable.

## AUTHORITY / PREFLIGHT

This Work Order is bound to Context Lock `NXWEB-LOCK-0006-CP07-WEB-3D-RUNTIME-ADAPTIVE-FIDELITY`, repository `KayzenRoot/nexlabs-web`, protected base `d01288967fca590029166e4b8532cdfd7fad5877`, GEF v1.0.0, HIVE v1.0.0 and the pinned planning cache at `KayzenRoot/nexlabs-startup@b541e802472a3acc75a3a8ebd3818d33de8a316f`. Run `scripts/hive_prepare.py` without an override after this Work Order is active and bind its exact Work Order SHA-256 to the Context Lock, HIVE task and evidence.

Read the tracked authority in startup order, verify the planning cache `MANIFEST.json`, and read BR-05, BR-06, BR-07, BR-09, BR-10, BR-13 and BR-17 runtime-relevant sources. Git, tracked canonical documents, this Work Order and the Context Lock are authoritative over derived context.

## SCOPE

- Promote the accepted CP-06 HIGH, MED, LOW GLBs and 16:9, 4:5 and 1:1 static fallbacks into deterministic public paths without reopening Blender or changing source bytes.
- Add a typed runtime asset manifest containing URL, tier, bytes, source hash, capabilities and fallback mapping, plus byte/hash parity validation against CP-06 acceptance.
- Add exact compatible Three.js and React Three Fiber dependencies only within the 3D module boundary. No Drei unless a concrete helper materially reduces complexity; no CDN, remote HDRI, external model host, backend, analytics or telemetry.
- Replace only the existing H01 `HeroVisualSlot` boundary with a `ThreeBoundary` static-first client island. Static fallback is in initial HTML/CSS, geometry remains stable, runtime is lazy near hero visibility, and the canvas is decorative.
- Implement isolated runtime failure handling: model/WebGL/context/runtime failure transitions to STATIC for the session with no retry/remount loop while hero text, navigation and CTAs remain functional.
- Implement the typed Context Core semantic state machine for DORMANT, INTAKE, INDEX, RETRIEVE, ASSEMBLE, RESOLVE and IDLE, with one bounded intro, IDLE settling, required-clip validation and pause/resume without unnecessary replay.
- Implement a pure, testable Adaptive Fidelity Controller with STATIC, LOW, MEDIUM and HIGH, conservative initialization, sustained rolling frame-time hysteresis, faster downgrade than upgrade, reduced-motion/static policy, session failure lock and local reason state.
- Implement Page Visibility and IntersectionObserver pause/throttle behavior, bounded responsive framing for desktop/tablet/mobile, reduced-motion accessibility, no focus trap and no pointer interference.
- Add development-only local instrumentation for tier, reason, frame-time/FPS, DPR, draw calls, triangles, asset tier, semantic state, pause state and transitions. Production debug UI and telemetry remain disabled.
- Add CP-07 validators and unit/component/E2E coverage for asset parity, state transitions, fallback-before-readiness, failures, reduced motion, visibility, non-home dependency isolation and responsive behavior.

## OUT OF SCOPE

- Blender mutation or rebuild; the frozen CP-06 package is consumed as-is and live Blender MCP is not required.
- UGAS provider startup or generation; CP-08, CP-09 hardening, deployment, release, domain/DNS, backend, auth, database, contact capture, analytics and visitor telemetry.
- BrandMark, header, favicon, selected-logo source or canonical asset changes.

## ACCEPTANCE CRITERIA

- Work Order, Context Lock and HIVE task are exact-base/digest bound; project/task/index/corpus are READY with extracted text and required HIVE/MCP context receipts.
- Every promoted CP-06 copy is byte-identical and hash-identical to its accepted source: HIGH `811ba946fa693c4151df3cb688cc73a4bf178e31a28fb88e39f1c9d18dec3870`, MED `016e2704a3c60fc61ccde1084c848330cc0cc8ff8d8961b09d74b83d139ccf2e`, LOW `97421e7c4c961b407f11d78fb924c022391f52731ac09deec2263fdbf94870e7`, static 16:9 `42833aa76e81070a2aa9a61c4d15673bcc6e21168d7f66dcf8bd34b309ca726b`, 4:5 `673530c6587376cdb8311d72189fa42f33dce0b5f1f17bc96661f4a74130a72e`, 1:1 `956fb4c5c584ed6c9ae40ae9fe1aad7735593b2c002d5f0d50545a44956918e6`.
- Three/R3F imports are isolated to the 3D module tree; non-home routes do not eagerly import or request the hero runtime/model.
- Static fallback is rendered before live runtime readiness; the fallback remains available for reduced motion, unsupported WebGL, model failure and runtime exception.
- Semantic clips map deterministically, intro runs once after successful load, missing clips fail closed, and visibility pause resumes current semantic state.
- AFC proves conservative initial selection, sustained downgrade, delayed one-tier upgrade, isolated-spike stability, reduced-motion STATIC, session STATIC lock and visibility throttling.
- Local validation is green, including governance, HIVE/CP06 regression, typecheck, lint, tests, build/validate, E2E, security, release-positive validation and Wrangler dry-run.
- One protected CP-07 PR is open with exact-head quality and Governance green. Do not merge and do not begin CP-08.

## REQUIRED VALIDATION

`python -m py_compile scripts/validate_governance.py scripts/hive_bootstrap.py scripts/hive_prepare.py scripts/hive_mcp.py`

`python scripts/validate_governance.py`

`python -m unittest discover -s tests -p "test_hive*.py" -v`

`python -m unittest discover -s tests -p "test_cp06*.py" -v`

`python scripts/cp06/validate_assets.py`

`npm run typecheck`, `npm run lint`, `npm run test`, `npm run validate`, `npm run check`, `npm run test:e2e`, `npm run security`, `npm run validate:release` with production variables, and `npx wrangler deploy --config wrangler.jsonc --dry-run`.

Add and run CP-07-specific runtime, AFC, boundary, asset and dependency-isolation validators.

## DELIVERABLES / STOP CONDITION

Deliver exact base/head/branch, Work Order and Context Lock digests, HIVE receipts, dependency versions, promoted paths/hashes, runtime manifest, static-first/failure-isolation receipt, semantic state matrix, AFC transition matrix, reduced-motion/visibility evidence, non-home isolation evidence, local validation matrix and exact-head PR checks.

Stop only when CP-07 is complete and auditable, its protected PR is open, and exact-head quality plus Governance are green. Do not merge. Explicitly confirm no Blender rebuild, no UGAS generation and no CP-08.
