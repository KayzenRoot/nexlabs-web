# BR-10 — Adaptive Fidelity Controller Contract

Status: PROPOSED
Internal name: AFC
Purpose: preserve the NexLabs visual experience across heterogeneous hardware without sacrificing usability.

## State
STATIC
LOW
MEDIUM
HIGH

Initial selection is conservative.
Runtime evidence may downgrade.
Upgrade is slower and more conservative than downgrade.

## Priority order
1. User accessibility preference.
2. Successful content/UI delivery.
3. Stable interaction.
4. Visual quality.
5. Decorative effects.

## Hard overrides
prefers-reduced-motion:
Use REDUCED presentation; complex choreography disabled. 3D may be static or minimally animated depending on final accessibility testing.

3D initialization failure:
STATIC.

Repeated runtime failure:
STATIC for session; do not retry-loop.

Document hidden:
PAUSED/THROTTLED.

Hero sufficiently offscreen:
PAUSED/THROTTLED.

## Measurement window
Do not react to a single slow frame.
Use a rolling/sustained frame-time window after warm-up.
Ignore known initialization/transitional spikes where appropriate.

Exact thresholds freeze during prototype profiling.

## Downgrade ladder
HIGH → MEDIUM:
reduce expensive post effects, particle density, DPR, shadow/material complexity.

MEDIUM → LOW:
lower DPR/LOD further, simplify materials, remove nonessential particles/effects.

LOW → STATIC:
replace live scene with intentional static branded asset when sustained runtime quality is unacceptable.

## Upgrade policy
Upgrade only if:
- current tier is stable for an extended period;
- page/hero is active;
- no accessibility override;
- no recent downgrade;
- resource loading is complete.

One tier at a time.

## Quality manifest
Each scene declares what HIGH/MEDIUM/LOW means.
The controller chooses tier; the scene owns its tier-specific configuration.

Example conceptual contract:
```
ContextCoreQuality = {
  high: { ... },
  medium: { ... },
  low: { ... },
  static: { ... }
}
```

## No fingerprinting
Do not send raw GPU renderer strings, hardware identifiers or fingerprint-like capability sets to analytics.

Local capability information may be used transiently for rendering decisions when technically necessary.

## Debug mode
Development/preview should expose:
- selected tier;
- reason;
- frame-time summary;
- DPR;
- draw calls;
- triangles;
- asset variant;
- downgrade/upgrade events.

Production debug UI remains disabled.

## Test cases
- strong desktop → HIGH stable;
- moderate laptop → MEDIUM/HIGH based on evidence;
- constrained phone → LOW or STATIC;
- reduced motion → reduced presentation;
- WebGL failure → STATIC;
- tab hidden → pause/throttle;
- thermal/performance degradation → eventual downgrade;
- transient frame spike → no immediate tier collapse;
- repeated poor frames → controlled downgrade;
- recovery → delayed conservative upgrade.

## Success condition
A visitor should perceive an intentional NexLabs experience at every tier. LOW and STATIC are designed states, not degraded accidents.
