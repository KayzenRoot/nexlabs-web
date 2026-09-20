# BR-17 — Codex Prompt Template

Status: FROZEN TEMPLATE
Use: CP-01…CP-11

# [PROMPT_ID] — [TITLE]

## ROLE
Act as the implementation owner for this bounded NexLabs work package.
Work autonomously until STOP CONDITION or a true human/external blocker.

## TARGET
Repository: [TARGET_REPOSITORY]
Starting branch/state: inspect before changing anything.

## READ FIRST
Read the canonical documents listed below before implementation:
[CANONICAL_FILES]

Also inspect:
- repository tree;
- git status/history relevant to scope;
- current tests/build;
- current checkpoint/decision files.

Do not assume chat text overrides a newer canonical repository decision.

## OBJECTIVE
[OBJECTIVE]

## IN SCOPE
[SCOPE]

## OUT OF SCOPE
[OUT_OF_SCOPE]

## MANDATORY EXECUTION
[TASKS]

Execute all tasks in scope.
Do not stop after scaffolding if the prompt requires working implementation.

## NON-NEGOTIABLE CONSTRAINTS
- truthful public claims only;
- zero-cost infrastructure unless founder explicitly approves otherwise;
- static-first institutional experience;
- accessibility and reduced motion;
- 3D cannot be required for semantic content/navigation/CTA;
- no unnecessary backend/database/auth;
- no secrets in repository/client;
- preserve brand governance;
- preserve unrelated repository work;
- no destructive Git history operations unless explicitly authorized.

## AUTONOMOUS REPAIR LOOP
For ordinary in-scope failures:
1. diagnose;
2. fix;
3. rerun affected checks;
4. continue.

Do not ask the founder to solve routine code/test/lint/build errors.

## CHECKPOINTS
[CHECKPOINTS]

At each checkpoint:
- verify work;
- correct failures;
- record material architecture deviations.

## VALIDATION
Run all applicable:
[VALIDATION_COMMANDS_OR_GATES]

Do not claim a check passed unless it actually ran successfully.

## GIT / GITHUB
- inspect status before work;
- create coherent commits;
- do not discard unrelated changes;
- do not force push;
- update canonical docs when implementation changes reality;
- report resulting commit SHA(s).

## HUMAN GATES
Stop only if this package reaches one of:
[HUMAN_GATES]

Complete all work that does not depend on the gate before stopping.

## STOP CONDITION
[STOP_CONDITION]

Do not stop before this condition merely because a partial implementation works.

## FINAL REPORT
Return:
1. status: COMPLETE | BLOCKED | FAILED;
2. work completed;
3. important files changed;
4. validation/tests actually run;
5. build result;
6. performance/accessibility/security results where applicable;
7. commit SHA(s);
8. deviations from plan;
9. unresolved blockers;
10. exact next dependency/prompt.

If BLOCKED, identify the smallest founder action required.
