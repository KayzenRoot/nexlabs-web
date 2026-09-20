# NexLabs Web Source Hierarchy

Status: `CP03_IN_REVIEW`

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
