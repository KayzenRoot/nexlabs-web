# NexLabs Web GitHub Governance Target

Status: `TARGET_PENDING_ADMIN_UPDATE`

## Observed current protection

Ruleset `Protect main` is active and currently requires pull requests and the `quality` context, blocks deletion and non-fast-forward updates, and has no bypass actor recorded in the current evidence.

## Desired CP-02R protection

The protected `main` flow should require both `quality` and `Governance` after the Governance workflow has run successfully on the repaired PR and the required administration mutation is authorized. No paid plan or bypass is assumed.

## Activation boundary

Changing repository rulesets is an external GitHub administration mutation. This branch prepares and validates the workflow but does not claim the ruleset was changed. The returned ruleset snapshot must be recorded after authorized activation.
