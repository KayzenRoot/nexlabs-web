# NexLabs Web GitHub Governance Target

Status: `TARGET_PENDING_ADMIN_UPDATE`

## Observed current protection

Live snapshot at 2026-09-19T15:18Z: ruleset `Protect main` (ID `23698968`) is active for `main`. It blocks deletion and non-fast-forward updates, requires pull requests and the `quality` context, and has no bypass actor. The branch-protection endpoint reports `404 Branch not protected` because this repository uses rulesets rather than legacy branch protection.

## Desired CP-02R protection

The protected `main` flow should require both `quality` and `Governance` after the Governance workflow has run successfully on the repaired PR and the required administration mutation is authorized. The live ruleset currently requires only `quality`; no paid plan or bypass is assumed.

## Activation boundary

Changing repository rulesets is an external GitHub administration mutation. This branch prepares and validates the workflow but does not claim the ruleset was changed. The returned ruleset snapshot must be recorded after authorized activation.
