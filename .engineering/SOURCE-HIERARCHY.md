# NexLabs Web Source Hierarchy

Status: `CP08_IN_PROGRESS`

Authority is domain-specific. HIVE indexes, memories and GEF metadata accelerate work but cannot override tracked Git sources.

## Domains

- **REPOSITORY_STATE:** exact Git files, commits, diffs and executable facts.
- **PROJECT_STATE:** `docs/project-brain/13-CHECKPOINT.md`.
- **DECISION:** `docs/project-brain/16-DECISIONS-LEDGER.md` and accepted ADRs.
- **SCOPE:** `docs/project-brain/03-SCOPE.md`.
- **REQUIREMENT:** `docs/project-brain/02-REQUIREMENTS.md`.
- **ARCHITECTURE:** `docs/project-brain/04-ARCHITECTURE.md`.
- **SECURITY:** `docs/project-brain/10-SECURITY-GOVERNANCE.md`.
- **COMPLETION:** `docs/project-brain/15-DEFINITION-OF-DONE.md`.
- **EXECUTION:** the active Work Order under `.engineering/work-orders/`.
- **VALIDATION:** `docs/project-brain/11-TEST-PLAN.md`, exact-head tests and evidence.
- **DEPLOYMENT:** `docs/project-brain/12-LOCAL-DEPLOYMENT.md`.
- **FUTURE_WORK:** `docs/project-brain/14-BACKLOG.md`.
- **BRAND_PARENT_INPUT:** authoritative pinned planning source `KayzenRoot/nexlabs-startup` at `b541e802472a3acc75a3a8ebd3818d33de8a316f`.
- **BRAND_PARENT_INPUT_CACHE:** immutable local execution mirror at `.engineering/planning-snapshots/nexlabs-startup/b541e802472a3acc75a3a8ebd3818d33de8a316f/`, verified by `MANIFEST.json`; cache never overrides the pinned parent source.
- **CONVERSATION:** transient input only.

## Startup order

Checkpoint -> decisions -> scope -> Definition of Done -> architecture -> requirements -> security/test/deployment as required by the Work Order.

## Conflict behavior

Missing, stale or conflicting authority blocks the affected progression. UNKNOWN never becomes ALLOW or DONE by inference.

## CP-03 external-source availability rule

Executor access to the private parent repository is optional once the pinned local cache is present and verified. A parent-repository HTTP 404 or missing local clone does not block CP-03 when the cache manifest matches the authoritative commit and source blob SHAs. A source pin change invalidates the cache and requires regeneration before execution.


## CP-05 workstation authorization rule

The protected repository policy authorizes governed Blender production on this workstation for CP-05 and later Work Orders that explicitly require Blender and pass the live MCP preflight. This authorization does not enable UGAS generation, provider startup, runtime 3D, logo promotion or CP-06+ scope by itself.

The preserved local branch `codex/cp05-blender-context-core` completed CP-05 from protected `main` without rewriting the blocked ancestry; its Work Order, Context Lock and HIVE proof lineage are closed and bound to the independent review receipt, while CP-06 requires a new Work Order.

## CP-06 closure

The CP-06 Work Order `NXWEB-WO-0005-CP06-BLENDER-MOTION-LOGO-WEB-ASSETS` and Context Lock `NXWEB-LOCK-0005-CP06-BLENDER-MOTION-LOGO-WEB-ASSETS` are completed/closed from the independently reviewed asset-package head `8ff6d8ded268c5acb56e5147788be971b890a47e`. The frozen package remains hash-bound; persistent Blender transport is a carried operational risk for future edits, not a CP-06 closure blocker. CP-07 runtime, BrandMark replacement and UGAS generation remain outside scope until a new Work Order and Context Lock are admitted.


## CP-07 runtime admission rule

After CP-06 is complete and merged, a dedicated CP-07 Work Order + Context Lock may authorize Three.js/React Three Fiber web runtime work that consumes the approved, hash-bound CP-06 HIGH/MED/LOW/STATIC assets. This runtime consumption does not require Blender MCP to be live unless the admitted CP-07 scope explicitly requires new Blender source mutation or asset rebuild.

Persistent Blender transport issues remain a carried operational risk for future Blender edits, not a blocker to consuming already accepted CP-06 assets. UGAS generation, deployment and unrelated scope remain separately governed.

## CP-07 completed runtime

`NXWEB-WO-0006-CP07-WEB-3D-RUNTIME-ADAPTIVE-FIDELITY` is independently reviewed and complete. Its Context Lock is closed. The canonical runtime baseline is the static-first H01 Three.js/React Three Fiber integration consuming the approved frozen CP-06 HIGH/MED/LOW/STATIC assets with semantic state, adaptive fidelity, reduced-motion fallback, failure isolation, visibility throttling and non-home isolation.

The HIVE product proof remains bound to the recorded API-ready head/task lineage. The later read-only MCP `Transport closed` condition is carried as an operational risk without any false MCP PASS claim. Reviewer corrections after the HIVE product proof are bounded, enumerated and exact-head validated.

No CP-08 work is admitted until a new Work Order + Context Lock are created after protected merge/post-merge verification.

## CP-08 derivative media admission

CP-07 PR #33 was merged into protected `main` at `d971047d25dc01e7338aba369ea1bd7cf7452490`. Post-merge Governance run `35671341225` and quality run `35671341040` both succeeded on that exact commit. CP-08 is admitted from that protected head under Work Order `NXWEB-WO-0007-CP08-UGAS-DERIVATIVE-MEDIA-RELEASE-VISUALS` and Context Lock `NXWEB-LOCK-0007-CP08-UGAS-DERIVATIVE-MEDIA-RELEASE-VISUALS`.

The active increment is a deterministic no-generation derivative-media package. It may create provenance-bound OG/repository visuals and optimized responsive static derivatives from accepted CP-06/CP-07 sources. UGAS provider startup and generation remain unavailable and unauthorized; neither is required. CP-08 does not authorize identity changes, release, deployment, merge or CP-09. Its assets remain `PRODUCTION` or `OPTIMIZED`, never `RELEASED`.


## Execution continuity rule

Missing or conflicting canonical authority remains fail-closed. Transient executor/runtime conditions do not become authority conflicts by themselves.

Stale local branches, stale policy snapshots after sync, transient Git/HIVE/MCP failures, CI flakes, publication gaps and validator defects must be repaired and revalidated in place when a safe bounded path exists. They become hard blockers only when the bounded repair path is exhausted and the active Work Order has no valid degraded continuation.
