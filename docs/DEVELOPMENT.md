# Development

## Requirements

- Node.js 24 LTS (`.nvmrc` / `.node-version`)
- npm 11

Install dependencies with the committed lockfile:

```bash
npm ci
```

## Commands

```bash
npm run dev          # local Next.js development server
npm run build        # generate the static out/ artifact
npm run start        # serve out/ locally at http://127.0.0.1:3000
npm run check        # typecheck, lint, tests, validation and build
npm run preview      # static build followed by local Wrangler preview
npm run test:e2e     # production static build plus Playwright smoke tests
```

`npm run start` is the production-like local smoke path for the static export. It uses the repository-owned static server and does not run `next start`, because this application has no Next.js server output. `npm run preview` exercises the Cloudflare/Wrangler runtime boundary separately.

No secret or purchased domain is required for local development.
