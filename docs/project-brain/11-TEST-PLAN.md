# 11 - Test Plan

## Application

Run `npm ci`, token generation/validation, typecheck, lint, Vitest, content/link/asset validation, static build, `npm run check`, Playwright, audit, release-gate expected failure and Wrangler dry-run.

## Governance

Run Python compilation for governance/HIVE scripts, the deterministic governance validator and Python unittest discovery for `test_hive*.py`. The Governance workflow binds checkout to the exact PR head and runs the same checks.

## HIVE runtime

When Docker/HIVE is available, verify Compose config, service health, exact HIVE release source, project registration by relative path, `READY` inspection, `COMPLETED` indexing, `CURRENT` or `COMPLETED` corpus, and read-only MCP protocol surface. Missing runtime evidence remains an explicit blocker.

## Review

Bind every result to the candidate SHA, Work Order, Context Lock and hosted run identity. Tests are evidence, not independent approval.
