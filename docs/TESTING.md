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

The E2E server is a small repository-owned static server so the test does not add a production runtime dependency.
