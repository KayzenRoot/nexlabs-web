# BR-12 — Asset Provenance Schema

Status: PROPOSED
Purpose: trace public NexLabs media from source to release.

## Minimal record
```yaml
asset_id: NL_...
version: v001
status: EXPLORE|CANDIDATE|APPROVED_SOURCE|PRODUCTION|OPTIMIZED|RELEASED|SUPERSEDED
purpose: ...
brand_spec_revision: ...
source:
  type: blender|ugas|procedural|manual|external
  references: []
ugas:
  workflow: null
  workflow_version: null
  notes: null
blender:
  source_file: null
  source_revision: null
rights:
  provenance_reviewed: false
  external_inputs: []
  notes: null
outputs:
  - path: ...
    format: ...
    width: null
    height: null
    bytes: null
    sha256: ...
destinations: []
approved_by: null
approved_at: null
notes: []
```

## Rules
- fields not applicable remain null/empty rather than invented;
- no API keys, prompts containing secrets or credentials;
- external inputs require provenance/license note;
- released assets require hash;
- superseded assets retain history;
- approval identity/timestamp are recorded only when actual workflow supports them.

## Release validation
A public asset fails release validation when:
- status is not RELEASED/approved for the destination;
- required output is missing;
- hash mismatch;
- provenance-required external input is unresolved;
- brand revision is incompatible with current release;
- destination crop/format is not approved.

## Goal
A future maintainer should be able to answer:
“What created this public image, which brand rules governed it, what source files were used, and is this the exact approved binary?”
