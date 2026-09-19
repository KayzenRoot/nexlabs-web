# Deployment

## Selected CP-01 path

CP-01 uses Next.js static export and Cloudflare Workers + Static Assets. The build artifact is `out/`; the Wrangler configuration points its static asset directory there.

```bash
npm ci
npm run build
npx wrangler dev --config wrangler.jsonc
```

For a production-like local check of the generated static artifact, run:

```bash
npm run build
npm run start
```

This serves `out/` with the repository-owned static server at `http://127.0.0.1:3000`. It is intentionally different from `npm run preview`, which starts Wrangler and exercises the Cloudflare Workers + Static Assets boundary.

Remote deployment is intentionally not performed by CP-01. When Cloudflare credentials and a release decision exist, the documented deployment command is:

```bash
npm run build
npx wrangler deploy --config wrangler.jsonc
```

The production domain is not configured. Set `NEXLABS_ENV=PRODUCTION` and `NEXT_PUBLIC_SITE_ORIGIN` only in a release environment after the domain and content gates are approved. Local and preview environments remain non-indexable.

Before any production promotion, run the explicit release gate with the approved HTTPS origin:

```bash
NEXLABS_ENV=PRODUCTION NEXT_PUBLIC_SITE_ORIGIN=https://example.invalid npm run validate:release
```

`example.invalid` is only a reserved syntax-test origin in documentation, not a NexLabs domain. The gate rejects local/preview environments, missing origins, malformed origins, HTTP origins, credentials and origins containing a path, query or hash. It does not run in ordinary PR CI, which remains domain-independent.

Cloudflare's current documentation recommends `vinext` for new Next.js Workers applications, but the guide identifies it as beta. CP-01 therefore keeps the stable static export path as the foundational deployment contract and leaves `vinext` or OpenNext as a future evidence-based migration option.
