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
npm run check        # typecheck, lint, tests, validation and build
npm run preview      # static build followed by local Wrangler preview
npm run test:e2e     # production static build plus Playwright smoke tests
```

No secret or purchased domain is required for local development.
