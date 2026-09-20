# CP04 Logo Exploration Evaluation

Status: candidate batch only; no automatic winner and no canonical selection.

## Method

Each symbol is evaluated independently across silhouette, small size, relevance, infrastructure semantics, 2D/3D coherence, wordmark context, motion readiness, production simplicity, accessibility/color independence and similarity risk. `PASS` means the candidate is reviewable for the next human gate, not approved.

## Candidate rows

| ID | Candidate result | Website contexts | Horizontal lockup | Blur/squint | Strengths | Weaknesses / repair note |
| --- | --- | --- | --- | --- | --- | --- |
| NX-D-01 | PASS | PASS (4/4) | PASS (light + dark) | PASS (945 px) | Strong single gesture; good 16 px survival. | Diagonal is familiar; similarity research remains open. |
| NX-D-02 | PASS | PASS (4/4) | PASS (light + dark) | PASS (801 px) | Layered topology and clear anchors. | Midline adds density at 16 px. |
| NX-D-03 | PASS | PASS (4/4) | PASS (light + dark) | PASS (792 px) | Best filled silhouette and clean negative cut. | Heavier mass can read more like a generic N. |
| NX-C-01 | PASS | PASS (4/4) | PASS (light + dark) | PASS (882 px) | Strong modular system semantics; stable avatar. | Core may look blocky beside wordmark. |
| NX-C-02 | PASS | PASS (4/4) | PASS (light + dark) | PASS (1080 px) | Clear interlock and 2D/3D projection potential. | Narrow core needs optical review in dark mode. |
| NX-C-03 | PASS | PASS (4/4) | PASS (light + dark) | PASS (1044 px) | Open frame preserves negative space at small sizes. | Less immediate N read than the other C variants. |
| NX-B-01 | PASS | PASS (4/4) | PASS (light + dark) | PASS (792 px) | Route semantics with a connected service spur and clearer route continuity. | The spur junction adds a small amount of detail; similarity research remains open. |
| NX-B-02 | PASS | PASS (4/4) | PASS (light + dark) | PASS (882 px) | Controlled orthogonal turn communicates infrastructure. | Most circuitry-adjacent; avoid technology cliche. |
| NX-B-03 | PASS | PASS (4/4) | PASS (light + dark) | PASS (972 px) | Distinct rail structure and strong horizontal rhythm. | Highest small-size complexity; human review required. |

## Objective checks

- PASS: 12x12 construction grid, path-only masters, monochrome and no gradients.
- PASS: all nine IDs are present in HEADER/LIGHT, HERO/DARK, FOOTER/MINERAL and SQUARE/AVATAR website-context rows.
- PASS: all nine IDs have a true symbol + NexLabs horizontal lockup in both LIGHT and DARK variants.
- PASS: blur/squint uses a 48px raster, GaussianBlur radius 1.5, 16px LANCZOS reduction and deterministic threshold (retained pixels >= 6 and peak >= 16).
- PASS: 16/24/32/64/128 px review sheet and all coverage records were generated deterministically.
- PASS: reduced-motion behavior is static by construction; no animation is encoded.
- BLOCKED_EXTERNAL: Blender MCP projection proof could not run because the live addon was unreachable. The blocker is recorded separately and no 3D pass is claimed.
- NOT_PERFORMED_IN_SCOPE: external visual similarity and trademark clearance. This is a required independent review gap, not evidence of uniqueness.

## Human gate

HG-01 must select or reject candidates independently. This document does not recommend a candidate and does not authorize runtime BrandMark wiring.
