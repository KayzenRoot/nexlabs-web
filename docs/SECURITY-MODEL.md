# Security model

CP-01 minimizes the public attack surface:

- static export only;
- no database, authentication, CMS, contact backend or analytics;
- no secrets in the repository or browser bundle;
- `.env.example` contains names and descriptions only;
- lockfile, npm audit and Dependabot configuration are committed;
- GitHub Actions use read-only repository permissions and pinned action commits;
- a Cloudflare static-asset header policy is versioned in `public/_headers`.
- local and preview robots explicitly disallow crawling; production indexing requires the explicit production environment and origin contract.
- production misconfiguration fails closed: no indexable metadata, canonical origin, sitemap URL or localhost fallback is emitted.

The header policy must be revalidated if a future client island, third-party asset, 3D runtime or dynamic Worker is added. No public security-reporting email is published because no monitored address has been approved.
# CP-02 additions

The theme bootstrap is an inline, same-origin preference read already covered by the existing `script-src 'self' 'unsafe-inline'` policy. CP-02 does not broaden origins, add third-party browser scripts, collect theme telemetry, or add network-capable runtime dependencies. Theme persistence is a single local-storage preference and is not used for fingerprinting.
