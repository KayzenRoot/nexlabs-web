# NexLabs Web GEF Review Protocol

Review the exact candidate/head against the active Work Order, Context Lock, Scope, Requirements, Architecture, Security, acceptance criteria and Definition of Done.

Review order:

1. Confirm authorized base and candidate head.
2. Confirm Context Lock validity.
3. Inspect semantic delta, not only file count.
4. Verify exact-head tests and evidence.
5. Check scope drift, security regressions and hidden assumptions.
6. Classify findings by severity.
7. Return one verdict: `APPROVED`, `CORRECTION REQUIRED` or `BLOCKED`.

Reports use Brazilian Portuguese unless a Work Order states otherwise. No checkpoint promotion occurs with unresolved HIGH or CRITICAL findings.


## Correction ownership

Before returning `CORRECTION REQUIRED` or `BLOCKED` because of a repairable defect, the reviewer must evaluate whether the defect can be safely corrected directly with the tools available in the review environment.

Prefer a direct reviewer correction when the change is small, deterministic, low-risk, in scope, does not require workstation-only/heavy execution, and can remain on the current PR branch with protected exact-head checks rerun afterward.

Escalate the correction to Codex/executor only when direct repair is unavailable or unsafe, including workstation/Blender state, unavailable external capabilities, substantial implementation work, ambiguous product decisions, secrets, destructive operations, or material scope changes.

When the reviewer applies a correction directly:
1. preserve branch/history and existing evidence;
2. document the correction in the PR review trail;
3. rerun required exact-head checks;
4. base the final verdict on the corrected exact head.
