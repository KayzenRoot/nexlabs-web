# NXWEB-WO-0002-CP03-INSTITUTIONAL-PAGES

Status: `IN_PROGRESS`

## OBJECTIVE

Resume CP-03 from the synchronized protected-main base and implement the complete static institutional content surface for NexLabs: typed canonical content, all planned institutional routes, route metadata, verified evidence links, responsive composition, and route-level/E2E validation.

## HIVE PREFLIGHT

Project name: `NEXLABS-WEB`.
Default API: `http://localhost:8000`.
Relative path: `nexlabs-web` below the machine-local HIVE projects root.
Required read-only context tools: `project.list`, `project.status`, `context.build`, `context.search`, `memory.search`, `memory.get`, `checkpoint.read`.
The Work Order task must be READY, extracted, project-scoped and bound to this file's exact UTF-8 SHA-256 before context retrieval.

## CANONICAL BASIS

- Repository: `KayzenRoot/nexlabs-web`.
- Authorized base: `d94f9b5520834ef05d0adc735ac7422068780ae1`.
- Planning source: `KayzenRoot/nexlabs-startup@b541e802472a3acc75a3a8ebd3818d33de8a316f`.
- Planning cache: `.engineering/planning-snapshots/nexlabs-startup/b541e802472a3acc75a3a8ebd3818d33de8a316f/`, verified by `MANIFEST.json` and source blob SHA.
- GEF: v1.0.0 @ `866fe3af8cccc65c929aaf6a47a924401fa448b3`.
- HIVE: v1.0.0 @ `a53b5b9fcf55c32a5696180fb1b1ef80ccd1edcf`.
- Workstation: `BLENDER_MCP_READY=true`, `UGAS_CORE_INSTALLED=true`, `UGAS_GENERATION_PROVIDER_READY=false`.

## CONTEXT BUDGET

Use the target Project Brain, verified planning cache, current HIVE documentation and the minimum read-only HIVE context required for the admitted routes. Do not import planning cache files into the website build.

## RISK / ASSURANCE

Fail closed for stale base, cache mismatch, missing HIVE task evidence, exact-head mismatch, false product/company claims, placeholder links, secrets, absolute machine paths and HIGH/CRITICAL findings. Local tests are not approval or merge evidence.

## SCOPE

1. Canonicalize the workstation capability layers without recording machine-specific paths.
2. Implement `/`, `/hive`, `/technology`, `/open-source`, `/about`, `/contact`, `/privacy` and not-found.
3. Compose Home sections H00-H10 with static semantic content and a stable future visual boundary.
4. Separate typed canonical content from page presentation and validate required fields, routes and evidence links.
5. Reconcile HIVE claims and license wording against the pinned HIVE repository before publishing.
6. Add route metadata/SEO while keeping production origin and canonical URLs fail-closed.
7. Add route/content/link tests and extend E2E coverage for navigation, mobile menu, theme persistence and 404.
8. Record exact-head evidence and a CP-03 checkpoint delta.

## OUT OF SCOPE

No final logo selection or production; no Blender asset production; no Three.js/R3F runtime; no canonical 3D; no UGAS derivative media or generation; no production domain, DNS, email approval, backend, auth, database, analytics, CRM or contact capture; no fabricated founder, customer, pricing, legal, traction, protocol, token, TVL or audit claims; no force-push, history rewrite, ruleset bypass, merge or deployment without the required gates.

## ARCHITECTURE RULES

Keep the site static/server-first and useful with JavaScript disabled. Reuse CP-02 tokens and semantic components. Keep client JavaScript limited to required interaction. Keep `VisualSlot`/`HeroVisualSlot` as future enhancement boundaries. Use one H1 per page composition, accessible headings, meaningful internal links, responsive composition, reduced-motion behavior and Cloudflare static-export compatibility.

## CONTENT / TRUTH RULES

English-first V1. Omit unresolved founder and public-business-contact facts. Render only verified contact channels. Treat the pinned HIVE repository as the current evidence source; its v1.0.0 checkout is public but `LICENSE` states All Rights Reserved, so do not publish an Apache-2.0/open-source license claim unless a newer verified source changes that fact. Do not render placeholder tokens or `href="#"`.

## ACCEPTANCE CRITERIA

- Planning cache manifest and all required local Git blob SHAs match.
- Work Order, Context Lock and HIVE task preparation are exact-head and digest bound.
- Workstation status is truthful: Blender MCP ready, UGAS core installed, generation provider not ready.
- All institutional routes render useful factual content and remain usable without live 3D or JavaScript-dependent core content.
- Typed content is separated from page presentation and required fields fail deterministically.
- HIVE claims and evidence links are verifiable against the pinned repository.
- No unresolved placeholder leaks to users; no fake metrics or dead production links exist.
- Every route has unique metadata and production canonical/indexability remains fail-closed without an approved origin.
- Accessibility, mobile navigation, theme persistence and 404 behavior are tested.
- Static export, build, security, E2E, governance and Wrangler dry-run pass, with `validate:release` remaining an expected fail-closed gate without production config.
- No HIGH/CRITICAL defect remains and no CP-04+ scope is introduced.

## TESTS

Run `npm ci`, `npm run typecheck`, `npm run lint`, `npm run test`, `npm run validate`, `python scripts/validate_governance.py`, `python -m unittest discover -s tests -p "test_hive*.py" -v`, `npm run check`, `npm run test:e2e`, `npm run security`, expected-failing `npm run validate:release`, and `npx wrangler deploy --config wrangler.jsonc --dry-run`. Run focused route/content/link/metadata tests directly when useful.

## EVIDENCE / DELIVERABLES

Bind evidence to this Work Order, `NXWEB-LOCK-0002-CP03-INSTITUTIONAL-PAGES`, authorized base, final candidate head, GEF/HIVE/planning pins, HIVE project/task/head receipts, changed files, route inventory, evidence-link inventory, tests, hosted checks, known risks and proposed checkpoint delta.

## STOP CONDITION

Stop with `APPROVED` only after the implemented CP-03 candidate is validated, reviewed, merged through protected main, post-merge quality and Governance pass on the exact resulting main SHA, no HIGH/CRITICAL issue remains and canonical docs match reality. Otherwise report `CORRECTION REQUIRED` or `BLOCKED`. Do not start CP-04 or any logo, 3D, Blender asset or UGAS media work.
