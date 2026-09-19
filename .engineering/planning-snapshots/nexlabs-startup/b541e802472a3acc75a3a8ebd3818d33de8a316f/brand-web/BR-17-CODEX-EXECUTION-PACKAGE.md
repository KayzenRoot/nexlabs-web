# BR-17 — Codex Execution Package

Status: PLANNED — NOT AUTHORIZED FOR EXECUTION
Date: 2026-09-19
Purpose: convert BR-01…BR-16 into a small number of high-throughput Codex execution packages.

## 1. Execution philosophy
Use few broad prompts.
Inside each prompt:
- read canonical sources first;
- inspect current repository state;
- execute multiple related work packages;
- validate after each internal checkpoint;
- repair failures within scope;
- commit coherent changes;
- stop only at explicit STOP CONDITION.

Do not trade prompt count for uncontrolled scope.

## 2. Canonical source hierarchy
Before execution Codex must treat as authority, in order:
1. current approved NexLabs startup/company canonical docs;
2. BRAND-WEB-MASTER-PLAN;
3. BR-01…BR-16;
4. approved ADRs;
5. current checkpoint/decisions;
6. actual target repository state.

If two sources conflict:
- newer explicit ADR/decision wins when scope matches;
- otherwise STOP and report the exact conflict;
- do not silently invent a compromise.

## 3. Planned macro-prompt sequence

### CP-01 — Repository Bootstrap + Engineering Foundation
Scope:
- create/bootstrap nexlabs-web repository;
- runtime/package manager;
- Next.js/React/TypeScript baseline;
- Cloudflare-compatible architecture;
- folder structure;
- lint/type/test/build;
- CI skeleton;
- environment policy;
- content/config schemas;
- documentation;
- no final visual implementation yet.

Expected result:
clean professional repository that builds and deploy architecture is technically viable.

### CP-02 — Brand Tokens + Design System + Semantic Shell
Scope:
- BR-04 token bridge;
- typography foundation;
- dark/light/system theme;
- UI primitives;
- Header/MobileNav/Footer;
- Section/layout system;
- accessibility primitives;
- component gallery/dev surface if justified;
- component tests.

Expected result:
complete reusable semantic UI foundation with no dependency on live 3D.

### CP-03 — Content + All Institutional Pages
Scope:
- typed canonical content;
- Home semantic structure;
- HIVE;
- Technology;
- Open Source;
- About;
- Contact;
- Privacy placeholder logic only where runtime facts are still unresolved;
- 404;
- metadata/SEO;
- evidence links;
- responsive implementation;
- no fabricated founder/contact/legal facts.

Expected result:
fully usable static institutional website before 3D.

### CP-04 — Logo Exploration Production
Scope:
- implement BR-03 candidate-generation system;
- produce 9 serious logo candidates:
  - 3 Topological N;
  - 3 Modular Core;
  - 3 Routed N;
- 16/24/32 px tests;
- monochrome;
- dark/light;
- horizontal lockup;
- square avatar;
- silhouette/blur;
- homepage-context previews;
- contact sheet/evaluation artifact.

STOP:
human logo selection required.

No candidate becomes canonical automatically.

### CP-05 — Blender MCP Context Core Foundation
Scope:
BR-11 WO-B3D-001 through WO-B3D-006:
- Blender master;
- primitives;
- materials;
- structural assembly;
- procedural data matter;
- cameras/lights;
- review renders;
- manifests/checkpoints.

Expected result:
approved static Context Core structure ready for semantic animation.

### CP-06 — Blender Motion + Logo Integration + Web Assets
Scope:
BR-11 WO-B3D-007 through WO-B3D-012:
- semantic animation;
- selected logo projection integration;
- LODs;
- export pipeline;
- GLB validation;
- static fallback;
- final asset acceptance.

Dependency:
CP-04 human-selected logo.

Expected result:
versioned HIGH/MED/LOW/STATIC production asset package.

### CP-07 — Web 3D Runtime + Adaptive Fidelity
Scope:
- ThreeBoundary;
- lazy Three/R3F runtime;
- ContextCore runtime;
- semantic state machine;
- BR-10 AFC;
- reduced motion;
- static-first boot;
- failure isolation;
- visibility pause/throttle;
- responsive composition;
- performance instrumentation in dev.

Expected result:
premium live hero that never becomes a functional dependency.

### CP-08 — UGAS Derivative Media + Release Visuals
Scope:
- approved concept/derivative assets only;
- OG cards;
- social/repository preview assets where destinations exist;
- responsive static hero derivatives;
- provenance manifests;
- optimization;
- no unapproved generated identity changes.

Expected result:
release-ready supporting visual package.

UGAS is not required for runtime.

### CP-09 — Hardening + QA + Security + Performance
Scope:
- complete BR-15 gates;
- unit/component/integration/E2E;
- visual regression;
- accessibility;
- link/content validation;
- GLB validation;
- bundle budgets;
- 3D failure injection;
- security headers;
- CSP from actual runtime;
- dependency/secret checks;
- cross-browser fixes;
- performance profiling.

Expected result:
no CRITICAL/HIGH known defect and release evidence package.

### CP-10 — Cloudflare Preview + Production Readiness
Scope:
- current Cloudflare official-doc revalidation;
- Workers + Static Assets first;
- Pages fallback only if evidence justifies;
- preview;
- noindex/canonical;
- deployment configuration;
- caching;
- immutable GLB/assets;
- headers/redirects;
- rollback proof;
- production runbook.

Dependency:
domain/contact may remain founder gates.

Expected result:
deployable release candidate and verified preview.

### CP-11 — Production Launch
Scope:
- approved domain;
- DNS;
- HTTPS;
- canonical;
- final public contact;
- privacy generated from actual runtime inventory;
- final HIVE evidence refresh;
- production deployment;
- smoke tests;
- release record/tag.

Dependency:
founder-owned domain and required public identity/contact approvals.

Expected result:
NexLabs institutional web live as web-v1.0.0.

## 4. Why 11 macro-prompts
The project is large enough that one mega-prompt would couple:
branding decisions, Blender production, web implementation and deployment failures.

Eleven macro-prompts keep user interaction low while preserving recoverable checkpoints.

Adjacent prompts may later be safely combined if repository state and Codex execution quality prove strong.

## 5. Prompt contract
Every executable prompt must contain:

### Header
- Prompt ID
- objective
- target repository
- allowed tools
- execution mode

### Inputs
- canonical files to read
- dependencies
- previous checkpoint

### Mandatory tasks
ordered implementation work.

### Constraints
- zero-cost;
- truthfulness;
- accessibility;
- static-first;
- brand governance;
- no unnecessary backend;
- no secrets;
- no destructive history changes.

### Autonomous repair
Codex should fix in-scope failures it discovers instead of stopping at the first ordinary lint/test/build error.

### Verification
exact commands/checks appropriate to the repository.

### Git discipline
- inspect status first;
- preserve unrelated work;
- coherent commits;
- never force-push unless explicitly authorized;
- report commit SHA.

### Documentation
update relevant docs/checkpoint/decisions as work changes reality.

### STOP CONDITION
objective completion criteria.

### Output report
- completed;
- changed files;
- tests;
- build;
- commits;
- deviations;
- blockers;
- next dependency.

## 6. Human gates
Codex must STOP for:
HG-01 final logo selection;
HG-02 final domain selection/purchase;
HG-03 public founder bio/name approval;
HG-04 public business contact approval;
HG-05 any paid capability;
HG-06 material legal/company-status change;
HG-07 production launch approval if not already explicitly granted by launch prompt.

These are decision gates, not excuses to ask about routine implementation.

## 7. Autonomous decisions
Codex may autonomously decide within approved architecture:
- internal refactoring;
- test implementation details;
- minor component decomposition;
- bug fixes;
- build tooling details;
- safe performance optimization;
- accessibility corrections;
- asset-pipeline implementation detail.

It may not autonomously:
- change brand strategy;
- select final logo;
- buy/use paid services;
- fabricate public facts;
- create a new backend/business feature;
- change company/legal status;
- expand V1 scope materially.

## 8. Failure policy
Ordinary in-scope failure:
diagnose → repair → rerun validation.

Architecture conflict:
document → STOP at affected boundary.

External account/credential requirement:
complete all noncredential work → report exact founder action required → STOP.

Paid requirement:
find zero-cost compliant alternative first.
If none, STOP before spending.

## 9. Context-efficiency rule
Prompts reference canonical repository files rather than repeating their full content whenever Codex has repository access.

Use:
“Read BR-10…” instead of embedding BR-10 verbatim.

This makes the repository the context cache.

## 10. Execution ledger
Each macro-prompt creates/updates a ledger record:
- prompt id;
- start source SHA;
- resulting SHA;
- status;
- validation;
- blockers;
- next prompt.

This prevents chat history from becoming the only execution memory.

## 11. Completion
BR-17 is frozen when:
- all macro-prompts are mapped;
- dependencies are explicit;
- human gates are explicit;
- prompt template is frozen;
- execution ledger contract exists;
- BR-18 verifies planning completeness;
- no HIGH/CRITICAL planning ambiguity remains before CP-01.
