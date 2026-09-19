# CP-01 Decisions

## ADR-CP01-001 - Static export on Workers Static Assets

Status: accepted for CP-01.

The application uses Next.js static export and publishes `out/` through Cloudflare Workers + Static Assets. This preserves portability and the zero-cost/static-first architecture. Cloudflare's current `vinext` recommendation is beta, so it is not a foundational dependency; OpenNext remains a future option if static export stops meeting the approved scope.

## ADR-CP01-002 - Native CSS token placeholder

Status: accepted for CP-01.

Native CSS custom properties provide the dark/light/system-ready substrate without selecting the final logo, palette or design system. No UI framework, animation framework or Three.js dependency is added.

## ADR-CP01-003 - No license file yet

Status: accepted for CP-01.

Company website licensing has not been approved. The repository is private and does not copy HIVE's Apache-2.0 license.

## ADR-CP01-004 - npm and Node 24

Status: accepted for CP-01.

Node 24 LTS and npm 11 are pinned by the runtime files, package manager field and CI. The lockfile is the install authority.

## ADR-CP01R-001 - Static export local start contract

Status: accepted for CP-01R.

Because `output: "export"` produces `out/` without a Next.js server runtime, `npm start` invokes the repository-owned static server. Wrangler remains the separate preview path for the Cloudflare runtime boundary.

## ADR-CP01R-002 - Explicit non-indexable robots rule

Status: accepted for CP-01R.

LOCAL and PREVIEW emit `disallow: "/"` and no sitemap. PRODUCTION emits `allow: "/"` and a sitemap only when `NEXT_PUBLIC_SITE_ORIGIN` is explicitly configured. No production domain is invented in the repository.
