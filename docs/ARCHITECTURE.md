# Architecture

CP-01 establishes a static-first Next.js App Router application for `KayzenRoot/nexlabs-web`.

## Runtime shape

- Next.js + React + TypeScript provide routing, metadata and component boundaries.
- `output: "export"` produces a portable `out/` directory with no server, database, authentication or runtime secret requirement.
- Cloudflare Workers + Static Assets is the preferred deployment boundary. Wrangler serves the generated `out/` directory.
- Local production-like serving also reads only the generated `out/` directory through `scripts/serve-static.mjs`; there is no Next.js server runtime for the static export.
- The root layout is a server component. Future interactive features must be isolated as client islands.
- Content is version-controlled JSON validated at build time and imported through typed TypeScript contracts.

## Planned boundaries

The repository reserves `components/brand`, `components/layout`, `components/sections`, `components/ui`, `components/diagrams`, `components/three`, `three/`, `design/`, `public/models/`, `public/images/`, and test-category directories for later CP packages. CP-01 creates only the files needed to prove the contract.

## Static-first contract

The semantic home shell, navigation and factual content are present in generated HTML. JavaScript is not required for the current content. 3D, animation and richer theme controls remain future optional enhancements.
