# BR-06 — Motion & Interaction System

Status: SYSTEM ARCHITECTURE
Date: 2026-09-19

## 1. Motion thesis
**Motion represents computation changing state.**

NexLabs motion vocabulary:
- assemble;
- route;
- index;
- retrieve;
- synchronize;
- compress;
- resolve;
- stabilize.

Avoid motion whose only purpose is “make it move”.

## 2. Motion character
Desired:
- precise;
- fluid but controlled;
- spatially coherent;
- restrained at idle;
- fast for UI feedback;
- deliberate for system transformations;
- cinematic only for brand moments.

Avoid:
- elastic/cartoon bounce;
- constant floating of all elements;
- excessive springiness;
- random parallax;
- long blocking intros;
- motion that delays navigation.

## 3. Semantic motion tiers

### M0 — Instant
State acknowledgement with no perceptible choreography.
Use: toggles, immediate accessibility states, critical UI feedback.

### M1 — Fast
Microinteraction.
Use: hover, focus, small state changes.

### M2 — Standard
Component transition.
Use: nav, card reveal, content state.

### M3 — System
Meaningful transformation.
Use: routing, assembly, Context Core state transitions.

### M4 — Cinematic
Rare brand sequence.
Use: motion logo, launch media, optional first hero reveal where non-blocking.

Exact durations are not frozen until prototypes, but M4 never blocks access to page content.

## 4. Easing grammar
Plan three core easing families:
- precision: quick controlled response;
- resolve: smooth deceleration into stable state;
- system: multi-stage transformation where physical/semantic continuity matters.

Avoid a different easing curve for every component.

## 5. Page-entry behavior
At navigation/page load:
1. semantic HTML and critical UI appear without waiting for 3D;
2. static hero composition is available;
3. noncritical motion/runtime initializes;
4. 3D transitions from safe state only when ready.

No full-screen branded loading gate for ordinary visits.

## 6. Scroll philosophy
Native scrolling remains intact.
Scroll provides progress/state input; it is not hijacked.

Allowed:
- section activation;
- bounded camera interpolation;
- progressive reveal;
- semantic Context Core state changes;
- subtle depth shifts.

Avoid:
- forced scroll snapping for the whole site;
- scroll-jacking;
- long pinned scenes that trap the user;
- mapping every pixel of scroll to expensive 3D updates without need.

## 7. Pointer interaction
Pointer can influence:
- shallow parallax;
- signal attraction;
- bounded camera target;
- hover inspection.

Rules:
- amplitude capped;
- composition returns smoothly to canonical state;
- interaction optional;
- no critical feature requires pointer;
- touch devices receive an intentional alternative.

## 8. Focus and keyboard
Keyboard focus is a first-class visual state.
Motion on focus must not obscure focus indication.
Canvas/3D must not trap keyboard navigation.

## 9. Context Core choreography

### DORMANT → INTAKE
Peripheral fragments become active; core remains stable.

### INTAKE → INDEX
Fragments align toward structured routes/layers.

### INDEX → RETRIEVE
Only relevant routes illuminate; unnecessary signals quiet.

### RETRIEVE → ASSEMBLE
Selected data matter converges into context shells.

### ASSEMBLE → RESOLVE
Structure simplifies visually as coherence increases.

### RESOLVE → IDLE
Motion amplitude falls. Stable system breathes minimally.

Important paradox:
More processing should ultimately produce **more visual order**, not more visual noise.

## 10. Logo motion
Concept:
distributed geometry → routed alignment → topology resolves → NexLabs mark → stable wordmark.

Variants:
- micro;
- standard;
- cinematic.

Static logo appears immediately when animation is skipped.

## 11. Typography motion
Text animation is subordinate to readability.

Preferred:
- opacity + small controlled translation;
- masked reveal only for rare display moments;
- stagger used sparingly.

Avoid:
- character scrambling;
- fake terminal typing for ordinary prose;
- repeated letter-by-letter effects;
- blur so heavy it harms readability.

## 12. Navigation
Header behavior:
- immediately usable;
- may transition from transparent/quiet to mineral surface after scroll;
- logo remains stable;
- active state clear;
- mobile menu uses short controlled transition.

## 13. CTA interactions
Primary CTA communicates action through:
- state/color/surface response;
- subtle signal movement;
- focus ring.

No magnetic button behavior strong enough to move away from the user's pointer.

## 14. Section transitions
Use one of a small set:
- signal handoff;
- layer reveal;
- topology continuation;
- quiet dissolve/translate.

Sections should feel connected by one computational system rather than independent demo reels.

## 15. Reduced motion
When reduced motion is requested:
- remove parallax;
- remove nonessential camera travel;
- collapse complex state sequences;
- replace logo motion with static identity;
- use instant/short opacity state changes where appropriate;
- retain all information and functionality.

## 16. Touch/mobile
No hover-dependent meaning.
Touch targets meet accessibility sizing guidance.
3D responds only when interaction adds value; scrolling remains primary.
Motion complexity is reduced based on capability/performance, not merely screen width.

## 17. Audio
Institutional website defaults to silent.
No autoplay audio.
Future sonic identity may exist as an optional brand asset but is outside core website requirements unless explicitly approved.

## 18. State synchronization
Where feasible, web motion should use explicit semantic state rather than scattered independent animation timers.

Conceptual model:
PAGE_STATE
+ SECTION_STATE
+ THREE_STATE
+ MOTION_PREFERENCE
+ QUALITY_TIER
→ PRESENTATION_STATE

## 19. Failure safety
Animation library/runtime failure must not hide content.
Initial CSS/HTML states must be readable without JavaScript where technically practical for core institutional content.

## 20. Performance
Prefer transform/opacity for DOM motion.
Avoid layout thrashing.
3D animation loop should pause/throttle when not visible where practical.
Do not keep expensive hero effects active below the fold without reason.

## 21. Motion QA
Test:
- 60 Hz and higher-refresh displays;
- constrained mobile/laptop;
- reduced motion;
- touch;
- keyboard-only;
- tab visibility/backgrounding;
- slow initialization;
- 3D failure/fallback;
- route/navigation transitions.

## 22. Freeze criteria
BR-06 freezes when:
- semantic motion vocabulary is approved;
- Context Core choreography is implementable;
- logo-motion concept aligns with BR-03;
- scroll/pointer boundaries are explicit;
- reduced-motion behavior is complete;
- motion tokens can be finalized after prototype timing tests;
- no interaction pattern compromises native navigation/accessibility.
