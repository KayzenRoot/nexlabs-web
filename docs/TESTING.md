# Testing

The CP-01 test foundation contains:

- Vitest unit tests for content, metadata and environment rules.
- React Testing Library component tests for the semantic shell and keyboard skip-link behavior.
- Playwright Chromium tests for the generated home page and static 404 response.
- Node validation scripts for content, internal/external links, asset manifest shape and static output reporting.

Run the core suite with:

```bash
npm run test
npm run test:e2e
npm run validate
```

The E2E server is a small repository-owned static server so the test does not add a production runtime dependency. `npm run start` uses the same server for the local production-like smoke check on port 3000; Playwright uses port 3100 to avoid collisions.

The robots contract is covered by unit tests: LOCAL and PREVIEW explicitly disallow `/`, while PRODUCTION allows `/` and emits a sitemap only when an explicit origin is configured.
