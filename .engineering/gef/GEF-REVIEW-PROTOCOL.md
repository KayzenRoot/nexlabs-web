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


## Stale session policy guard

When an executor report cites repository policy that no longer matches protected `main`, reviewers must verify the current tracked policy first.

If protected main is already correct, classify the mismatch as `STALE_EXECUTOR_POLICY_SNAPSHOT` and treat it as AUTO-REPAIR rather than a product blocker.

Recovery order:
1. preserve local work and synchronize to the intended protected base;
2. re-read current tracked governance sources in the same executor session;
3. continue immediately if the harness adopts the refreshed policy;
4. only if the harness demonstrably continues enforcing superseded policy, restart the executor session once and continue from the synchronized checkout.

Do not mutate valid canonical policy merely to satisfy stale cached instructions.


## Continuity classification

Review findings must be classified before verdict:

- `AUTO_REPAIR`: small/deterministic/in-scope issue that reviewer or executor can fix safely now. Fix it, rerun gates, and continue.
- `CORRECTION_REQUIRED`: product or governance defect that requires material executor work but does not require external user input.
- `BLOCKED`: progress is impossible without external user decision, unavailable mandatory capability, secret/credential, destructive authorization, irreconcilable integrity conflict, or an unrepaired HIGH/CRITICAL issue outside the admitted correction capacity.

A transient Git/HIVE/MCP/CI/policy-snapshot/branch/PR/validator condition is not `BLOCKED` by itself when a bounded repair path exists.


## Attachment supersession guard

If an executor blocks on an operational requirement that exists only in an older PDF/Markdown attachment, compare it with:
1. the user's latest direct instruction;
2. current protected-main policy;
3. the active governed Work Order.

When the old attachment detail is superseded at the same instruction priority and current repository policy permits continuation, classify the condition as `SUPERSEDED_ATTACHMENT_INSTRUCTION` and AUTO_REPAIR it by re-reading current tracked authority and continuing.

A stale attachment bootstrap detail is not a hard blocker by itself.
