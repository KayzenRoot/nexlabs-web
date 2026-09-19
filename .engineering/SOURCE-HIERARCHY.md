# NexLabs Web Source Hierarchy

Status: `FROZEN_FOR_CP02R_EXECUTION`

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
- **BRAND_PARENT_INPUT:** pinned planning source `KayzenRoot/nexlabs-startup` at `b541e802472a3acc75a3a8ebd3818d33de8a316f`.
- **CONVERSATION:** transient input only.

## Startup order

Checkpoint -> decisions -> scope -> Definition of Done -> architecture -> requirements -> security/test/deployment as required by the Work Order.

## Conflict behavior

Missing, stale or conflicting authority blocks the affected progression. UNKNOWN never becomes ALLOW or DONE by inference.
