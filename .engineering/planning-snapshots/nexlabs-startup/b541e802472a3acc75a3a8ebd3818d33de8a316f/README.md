# CP-03 Planning Source Cache

Status: `IMMUTABLE_SOURCE_CACHE`

This directory mirrors the minimum NexLabs Brand/Web planning inputs required to admit and execute CP-03 without requiring the executor to authenticate to the private parent repository at runtime.

## Authority

Authoritative origin:

- repository: `KayzenRoot/nexlabs-startup`
- commit: `b541e802472a3acc75a3a8ebd3818d33de8a316f`

The cached files are **not a new authority** and must not be edited as planning decisions. Their source paths and Git blob SHAs are recorded in `MANIFEST.json`.

If the authoritative planning commit changes, this cache is stale and must be regenerated rather than patched manually.

## Execution use

CP-03 executors should read the local cached paths listed by the manifest after reading the canonical target-repository hierarchy:

Checkpoint -> Decisions -> Scope -> Definition of Done -> Architecture -> Requirements -> CP-03 planning cache.

Git-tracked target-project authority still wins within its domain. HIVE may index this cache but cannot overwrite it.
