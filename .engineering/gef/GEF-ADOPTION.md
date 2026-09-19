# GEF v1.0.0 Adoption - NexLabs Web

## Adoption record

- Project: `KayzenRoot/nexlabs-web`
- Mode: `EXISTING_PROJECT / BROWNFIELD`
- GEF: `v1.0.0` at `866fe3af8cccc65c929aaf6a47a924401fa448b3`
- HIVE: `v1.0.0` at `a53b5b9fcf55c32a5696180fb1b1ef80ccd1edcf`
- Planning source: `KayzenRoot/nexlabs-startup` at `b541e802472a3acc75a3a8ebd3818d33de8a316f`
- Prompt mode: `GEF_V1_HIVE_FIRST`
- Review mode: `DELTA_EXACT_HEAD`
- Assurance: fail closed for missing required evidence

GEF is materialized as a target-project contract. The GEF and HIVE repositories remain external and are not copied into this website.

## Lifecycle

`ANALYZE -> SOURCE CHECK -> WORK ORDER -> CONTEXT LOCK -> PREFLIGHT -> EXECUTOR -> TESTS/EVIDENCE -> PR -> AUDIT -> VERDICT -> CHECKPOINT DELTA -> MERGE -> NEXT`

## Adoption state

The state remains `GEF_V1_ADOPTION_IN_PROGRESS` until the active Work Order evidence is accepted and the protected lifecycle has completed. No green test, PR or HIVE receipt alone promotes the checkpoint.
