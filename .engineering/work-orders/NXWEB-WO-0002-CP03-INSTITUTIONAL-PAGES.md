# NXWEB-WO-0002-CP03-INSTITUTIONAL-PAGES

Status: `IN_PROGRESS`

## OBJECTIVE

Ship CP-03 factual static institutional pages after corrected HIVE preflight.

## CONTEXT/HIVE PREFLIGHT

- Project `NEXLABS-WEB`; relative path `nexlabs-web`; API `http://localhost:8000`.
- Resolve this active Work Order from `GEF-CURRENT.json`; bind exact UTF-8 SHA-256.
- Require a READY/extracted/project-scoped HIVE task before retrieval.
- Prove `project.list`, `project.status`, `checkpoint.read`, `context.search`, Core/MCP `context.build`.
- Prove `top_k=1`/`L0`, then default; default failure stops CP-03.
- Required context <=6,144 tokens; MCP output <=64 KiB; never raise limits or bypass `context.build`.

## CANONICAL BASIS

- Repo/base: `KayzenRoot/nexlabs-web` / `d94f9b5520834ef05d0adc735ac7422068780ae1`.
- Planning/cache: `KayzenRoot/nexlabs-startup@b541e802472a3acc75a3a8ebd3818d33de8a316f`; manifest/SHA verified.
- GEF `866fe3af8cccc65c929aaf6a47a924401fa448b3`; HIVE `a53b5b9fcf55c32a5696180fb1b1ef80ccd1edcf`.
- Workstation: Blender MCP ready; UGAS core installed; generation provider not ready.

## SCOPE

- Keep workstation capability layers truthful without machine paths.
- Implement `/`, `/hive`, `/technology`, `/open-source`, `/about`, `/contact`, `/privacy`, and 404.
- Compose Home H00-H10 with semantic static content and neutral visual slots.
- Separate typed content/presentation; validate fields, routes, metadata, and evidence links.
- Reconcile HIVE claims/license; add route/content/link tests, E2E, exact-head evidence, and checkpoint delta.

## OUT OF SCOPE

- No logo selection, Blender assets, Three.js/R3F, canonical 3D, or UGAS media generation.
- No domain/DNS/email approval, backend/auth/database/analytics/CRM/contact capture, or CP-04+ work.
- No fabricated facts, placeholders, dead links, secrets, HIGH/CRITICAL defects, force-push, bypass, merge, or deployment.

## FILES/SOURCES TO READ

- Brain: `docs/project-brain/{02-REQUIREMENTS,03-SCOPE,04-ARCHITECTURE,13-CHECKPOINT,15-DEFINITION-OF-DONE,16-DECISIONS-LEDGER}.md`.
- Governance: `.engineering/SOURCE-HIERARCHY.md`, active GEF/Lock, verified planning `MANIFEST.json`.
- Seams/sources: `scripts/{hive_prepare,hive_mcp}.py`, cache BR-07/08/13, pinned HIVE docs/license.

## REQUIREMENTS

- Static/server-first; core content works without JavaScript.
- Every route is factual, typed, accessible, responsive, and uniquely metadated.
- Canonical/indexability fail closed without approved production origin.
- Verify internal evidence; reject missing fields, placeholders, false claims, and dead links.
- Test mobile menu, theme, 404, reduced motion, static export, security, E2E, and Wrangler.
- Core content never depends on 3D, UGAS, live providers, or unresolved legal/business facts.
- Pinned HIVE v1.0.0 is not Apache-2.0/open-source; verified license is All Rights Reserved.
- Reuse CP-02 tokens/components; preserve Cloudflare static-export compatibility.

## ARCHITECTURE RULES

- Prefer server/static rendering; client JavaScript only for required interaction.
- Separate content, metadata, presentation, validators, and visual slots.
- Use semantic accessible headings/names, internal links, responsive and reduced-motion behavior.
- Keep origins and business/legal facts configuration-driven and fail-closed.

## CONSTRAINTS

- Preserve Work Order ID, Lock ID, CP-03 scope, and lineage.
- Reduce duplication, never requirements or governance.
- Use verified repo/cache/GEF/HIVE/workstation facts only.
- Do not mutate pinned HIVE source or budget/transport constants.
- Keep media neutral until separately admitted.
- Bind receipts to exact Work Order digest and Git SHA.
- No PR before product gates and independent review.
- Local tests or CI alone never mean approval.

## ACCEPTANCE CRITERIA

- Cache manifest and source SHAs match.
- HIVE task is READY, extracted, scoped, and digest-bound.
- Minimal Core/MCP builds pass without prior errors.
- Default Core/MCP builds pass within 6,144 tokens/64 KiB.
- Project status matches HEAD; checkpoint/search receipts exist.
- All routes render factual content without live 3D or JS-dependent core content.
- Typed validation rejects missing fields deterministically.
- HIVE claims, license, and evidence links match pinned sources.
- Metadata is unique; canonical/indexability fail closed without origin.
- Accessibility, mobile/theme/404, static, security, E2E, and Wrangler checks pass.
- `validate:release` fails closed without approved production configuration.
- No HIGH/CRITICAL or CP-04+ scope; evidence and checkpoint delta exist.

## TESTS

Run Python compile/governance/HIVE tests; `npm ci`; typecheck, lint, test, validate, check, E2E, security; expected-failing release validation; Wrangler dry-run.

## DELIVERABLES

- CP-03 routes, typed content, metadata, validators, tests, neutral slots.
- Digest/task/context receipts, route/evidence inventory, tests, risks, checkpoint delta.
- PT-BR report separating product, HIVE, local, hosted, review, merge, post-merge status.

## REVIEW FORMAT

PT-BR report with exactly one verdict: `APPROVED`, `CORRECTION REQUIRED`, or `BLOCKED`.

## STOP CONDITION

If compaction cannot make Core and MCP default builds pass, stop `BLOCKED` with `HIVE_CORE_CORRECTION_REQUIRED`; otherwise resume only after both pass. `APPROVED` requires implementation, independent review, protected merge, post-merge checks, and resulting-main proof.

## EXECUTION REFERENCES / CANONICAL REFERENCES

- Planning cache, Project Brain, governance paths, Git, and exact-head receipts are authoritative.
- Pinned HIVE checkout/license is authoritative for HIVE capability and licensing claims.
