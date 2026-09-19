# Deployment

## Selected CP-01 path

CP-01 uses Next.js static export and Cloudflare Workers + Static Assets. The build artifact is `out/`; the Wrangler configuration points its static asset directory there.

```bash
npm ci
npm run build
npx wrangler dev --config wrangler.jsonc
```

Remote deployment is intentionally not performed by CP-01. When Cloudflare credentials and a release decision exist, the documented deployment command is:

```bash
npm run build
npx wrangler deploy --config wrangler.jsonc
```

The production domain is not configured. Set `NEXLABS_ENV=PRODUCTION` and `NEXT_PUBLIC_SITE_ORIGIN` only in a release environment after the domain and content gates are approved. Local and preview environments remain non-indexable.

Cloudflare's current documentation recommends `vinext` for new Next.js Workers applications, but the guide identifies it as beta. CP-01 therefore keeps the stable static export path as the foundational deployment contract and leaves `vinext` or OpenNext as a future evidence-based migration option.
