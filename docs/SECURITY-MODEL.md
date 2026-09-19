# Security model

CP-01 minimizes the public attack surface:

- static export only;
- no database, authentication, CMS, contact backend or analytics;
- no secrets in the repository or browser bundle;
- `.env.example` contains names and descriptions only;
- lockfile, npm audit and Dependabot configuration are committed;
- GitHub Actions use read-only repository permissions and pinned action commits;
- a Cloudflare static-asset header policy is versioned in `public/_headers`.

The header policy must be revalidated if a future client island, third-party asset, 3D runtime or dynamic Worker is added. No public security-reporting email is published because no monitored address has been approved.
