# CP-08 derivative media quality gates

Status: **PASS**
Release: **NOT_RELEASED**

| Gate | Description | Status | Severity |
| --- | --- | --- | --- |
| UG1 | Brand compliance | PASS | NONE |
| UG2 | Composition | PASS | NONE |
| UG3 | Artifact inspection | PASS | NONE |
| UG4 | Text/logo integrity | PASS | NONE |
| UG5 | Provenance | PASS | NONE |
| UG6 | Technical resolution | PASS | NONE |
| UG7 | Destination crop | PASS | NONE |
| UG8 | Compression quality | PASS | NONE |
| UG9 | Accessibility/meaning | PASS | NONE |
| UG10 | Release manifest | PASS | NONE |

## UG1 — Brand compliance

- planning source pin verified
- canonical token source verified
- selected NX-C-02 bytes preserved

## UG2 — Composition

- all OG cards use 1200x630 with conservative safe areas
- repository preview uses 1280x640
- text and illustration zones do not overlap

## UG3 — Artifact inspection

- all 12 output records decode and match dimensions, formats, bytes and SHA-256
- nonessential image metadata is absent

## UG4 — Text/logo integrity

- Open Graph and repository card copy matches tracked canonical text
- all cards have truthful text descriptions

## UG5 — Provenance

- all 12 assets have truthful BR-12 records
- UGAS and Blender fields are null where unused
- external inputs and approvals are not invented

## UG6 — Technical resolution

- accepted CP-06 and promoted CP-07 bytes remain identical
- 16:9, 4:5 and 1:1 framing is preserved without upscaling
- six WebP/AVIF variants meet size and visual-parity budgets

## UG7 — Destination crop

- three metadata destinations resolve to committed local PNG files
- repository preview uses the verified repository URL
- generic template has no fabricated destination

## UG8 — Compression quality

- each responsive derivative is smaller than its accepted PNG source
- all visual parity scores are within 3% normalized MAE
- all social cards are at most 512 KiB

## UG9 — Accessibility/meaning

- generic template contains no unresolved tokens or fake social claim
- visuals have provenance alt-purpose descriptions
- site meaning remains in semantic HTML and visuals stay decorative

## UG10 — Release manifest

- manifest status is NOT_RELEASED and asset lifecycle is PRODUCTION/OPTIMIZED only
- no UGAS provider, release, merge, deployment or CP-09 action is recorded
- no CP-09/deployment implementation files are in the change set

No asset is marked RELEASED. No external input, approval identity, approval timestamp, provider startup, generation, deployment, merge or CP-09 action is claimed.
