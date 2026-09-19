# Content model

`content/site/site.json` is the CP-01 source for the typed institutional shell.

It represents:

- canonical brand and corporate descriptor;
- truthful company stage, location and market intent;
- navigation and evidence links;
- route metadata;
- optional public contact and founder data.

Founder and public email fields are explicitly `null` and unpublished. They must not be replaced with invented placeholder data. `lib/content/types.ts` and `lib/content/validation.ts` provide the application contract; `scripts/validate-content.mjs` provides a dependency-free CI check.
