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
