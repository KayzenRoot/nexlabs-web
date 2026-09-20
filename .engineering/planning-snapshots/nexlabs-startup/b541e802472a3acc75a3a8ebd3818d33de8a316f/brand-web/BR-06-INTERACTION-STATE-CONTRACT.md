# BR-06 — Interaction State Contract

Status: PROPOSED
Purpose: future implementation contract for Codex.

## Inputs
- route/page;
- section visibility/progress;
- pointer/touch capability;
- reduced-motion preference;
- 3D capability/readiness;
- quality tier;
- document visibility;
- runtime error state.

## Presentation state

### HERO_SAFE
Semantic hero + static branded composition.
Default before 3D readiness.

### HERO_LIVE
Interactive Context Core enabled.

### HERO_REDUCED
Static/resolved Core, minimal DOM transitions.

### HERO_FALLBACK
Static branded render after unsupported capability/runtime failure.

## Section state
INACTIVE
ENTERING
ACTIVE
LEAVING
PAST

No section is hidden permanently while waiting for ENTERING animation.

## 3D lifecycle
UNLOADED
LOADING
READY
ACTIVE
THROTTLED
PAUSED
FAILED

Transitions must be observable/testable rather than inferred from arbitrary timers.

## Visibility policy
When hero is sufficiently outside viewport:
ACTIVE → THROTTLED or PAUSED.

When document becomes hidden:
expensive animation → PAUSED where technically safe.

## Quality adaptation
Quality may degrade:
HIGH → MEDIUM → LOW → STATIC

Automatic upgrades should be conservative to avoid oscillation.
Never rapidly bounce between quality tiers.

## Analytics/telemetry events — only if analytics is approved
Examples:
hero_3d_ready
hero_3d_failed
hero_quality_selected
reduced_motion_used

Do not collect invasive device fingerprinting data.

## Testing contract
Automated/component tests should verify:
- content visible before 3D;
- failed 3D produces fallback;
- reduced motion avoids complex choreography;
- keyboard navigation unaffected;
- section content never remains hidden due to animation failure;
- lifecycle pauses/throttles when appropriate.
