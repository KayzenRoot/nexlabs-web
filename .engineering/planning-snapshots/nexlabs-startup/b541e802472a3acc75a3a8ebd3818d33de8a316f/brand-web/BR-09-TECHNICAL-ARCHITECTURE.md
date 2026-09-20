# BR-09 — Technical Architecture

Status: PROPOSED
Date: 2026-09-19
Primary deployment direction: Cloudflare free-tier stack
Implementation repository: planned separate repo `KayzenRoot/nexlabs-web`

## 1. Architecture goals
- zero-cost infrastructure at launch, excluding founder-purchased domain;
- premium interactive 3D without making 3D critical to content;
- static-first institutional content;
- excellent Core Web Vitals;
- accessibility and reduced-motion support;
- portable architecture;
- no unnecessary backend;
- deterministic build/deploy;
- evidence-backed content;
- secure-by-default public surface.

## 2. Hosting decision

### Primary — Cloudflare
Current direction: Cloudflare Pages/static assets or Workers static assets, with Workers only where dynamic behavior is actually required.

Rationale:
- zero-cost path suitable for public institutional deployment;
- static-heavy site aligns with architecture;
- global asset delivery;
- custom-domain support;
- dynamic Worker budget can be avoided for most traffic.

### Vercel
Not selected for zero-cost production because the current Hobby terms/pricing position Hobby for personal/non-commercial use.

Vercel remains a technically viable future provider if a suitable paid/business plan or program credit is available.

## 3. Framework decision

### Proposed application layer
Next.js + React + TypeScript.

Reasons:
- mature metadata/routing model;
- strong React ecosystem;
- static generation;
- component architecture;
- good fit for R3F;
- portable enough if we constrain provider-specific features.

### Cloudflare deployment compatibility
Two acceptable strategies are retained until implementation compatibility test:

A. Static-first Next.js export where all required V1 functionality permits it.
B. Cloudflare Workers deployment using the then-current recommended Next.js compatibility path.

Preference: **A whenever possible**.

The institutional V1 should not require SSR merely because the framework supports it.

## 4. 3D stack
- Three.js;
- React Three Fiber;
- Drei only where individual helpers justify their cost;
- Blender-authored GLB/glTF assets;
- compressed production variants;
- static AVIF/WebP fallback.

Do not load the 3D stack into routes that do not need it.

## 5. Rendering architecture

### Server/build/static layer
Owns:
- page HTML;
- content;
- metadata;
- navigation;
- evidence links;
- SEO;
- static fallback imagery.

### Client island layer
Owns:
- Context Core;
- interaction state;
- motion;
- adaptive 3D quality;
- optional theme controls;
- nonessential enhancements.

Core institutional meaning remains available before client enhancement.

## 6. Content architecture
V1 content lives in version-controlled typed local content/config rather than a CMS.

Reasons:
- zero cost;
- low editorial frequency;
- reviewable changes;
- no external runtime dependency;
- strong evidence traceability.

Future CMS is an explicit migration, not launch scope.

## 7. Planned repository structure

```
nexlabs-web/
├─ app/
│  ├─ page.*
│  ├─ hive/
│  ├─ technology/
│  ├─ open-source/
│  ├─ about/
│  ├─ contact/
│  ├─ privacy/
│  ├─ not-found.*
│  ├─ layout.*
│  ├─ sitemap.*
│  └─ robots.*
├─ components/
│  ├─ brand/
│  ├─ layout/
│  ├─ sections/
│  ├─ ui/
│  ├─ diagrams/
│  └─ three/
├─ content/
│  ├─ site.*
│  ├─ pages/
│  └─ evidence/
├─ design/
│  ├─ tokens/
│  └─ themes/
├─ three/
│  ├─ core/
│  ├─ scenes/
│  ├─ materials/
│  ├─ quality/
│  └─ state/
├─ public/
│  ├─ brand/
│  ├─ models/
│  ├─ images/
│  ├─ og/
│  └─ fonts/
├─ lib/
│  ├─ metadata/
│  ├─ content/
│  ├─ observability/
│  └─ runtime/
├─ tests/
│  ├─ unit/
│  ├─ component/
│  ├─ e2e/
│  ├─ accessibility/
│  ├─ visual/
│  └─ performance/
├─ scripts/
│  ├─ validate-content.*
│  ├─ validate-links.*
│  ├─ validate-assets.*
│  └─ build-brand-manifest.*
├─ docs/
└─ .github/
```

Exact filenames/extensions depend on framework version selected at implementation.

## 8. Dependency policy
Every dependency must answer:
- why is it needed?
- can platform/browser/framework already do it?
- does it materially affect client bundle?
- is license compatible?
- is maintenance healthy?

No giant animation/UI framework merely for one effect.

## 9. JavaScript budget philosophy
Route-level code splitting.
3D dependencies lazy-loaded only where needed.
Non-3D pages should not inherit hero 3D payload.
Prefer native CSS for ordinary UI transitions.

Exact KB budgets freeze in BR-10 after prototype measurements.

## 10. Asset architecture
Critical HTML/CSS/brand static image first.
3D model second.
High-quality enhancements last.

Model manifest should describe:
- asset id;
- quality tier;
- URL;
- approximate transfer size;
- fallback;
- required capabilities;
- version/hash.

## 11. Fonts
Self-host approved open-license font assets when practical.
Subset only if licensing/tooling and language requirements permit.
Use fallback stack to avoid invisible text.

## 12. Contact architecture
Default V1 preference: verified public business email + GitHub.
No backend contact form at launch unless there is a clear benefit.

If a form is later approved:
- minimal Worker endpoint or suitable service;
- spam controls;
- validation;
- rate limiting;
- privacy disclosure;
- no paid dependency by default.

## 13. Analytics
Default: no analytics dependency required to launch.

If approved, choose a privacy-respecting, zero-cost-compatible approach and document actual collection before enabling it.

Performance/technical observability may use build-time tests and provider logs without turning visitor tracking into a launch requirement.

## 14. Security
Public site should minimize attack surface:
- mostly static;
- no database;
- no authentication;
- no secrets shipped client-side;
- security headers;
- CSP designed around actual asset/runtime needs;
- dependency scanning;
- lockfile;
- automated CI checks;
- no unsafe HTML injection from content.

## 15. CI/CD
GitHub is source of truth.

Pull request gates planned:
- install/lockfile integrity;
- typecheck;
- lint;
- unit/component tests;
- build;
- link/content validation;
- accessibility smoke tests;
- asset validation;
- security/dependency checks;
- performance budget check when stable.

Main deploys production only after gates pass.

## 16. Environments
LOCAL
PREVIEW
PRODUCTION

Preview:
- noindex;
- noncanonical;
- safe test assets/config.

Production:
- canonical domain;
- indexing enabled;
- final evidence/content gates.

## 17. Domain/DNS
Founder purchases approved domain only after brand/name/domain review.

Preferred production DNS/CDN path: Cloudflare.

Requirements:
- apex + www policy;
- HTTPS;
- redirects;
- canonical origin;
- DNSSEC evaluation;
- email DNS separated from web deployment;
- no domain transfer required merely to use Cloudflare DNS where avoidable.

## 18. Portability contract
Avoid unnecessary provider-specific APIs.
Provider integration lives behind narrow configuration/adapters where dynamic functionality exists.

Static content, assets and React components remain portable.

## 19. Build reproducibility
- pinned package manager;
- lockfile committed;
- supported runtime version declared;
- deterministic asset manifest;
- no manual production edits;
- deployment from Git state;
- release SHA visible in internal diagnostics/build metadata where useful.

## 20. Acceptance criteria
BR-09 freezes when:
- framework/runtime versions are validated at implementation start;
- static-first deployment feasibility confirmed;
- Cloudflare deployment route selected;
- repository architecture approved;
- dynamic features minimized;
- CI/CD and environment model defined;
- domain/DNS contract defined;
- no launch requirement forces paid infrastructure.
