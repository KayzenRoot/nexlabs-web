# BR-10 — Performance & Accessibility Budgets

Status: PROPOSED ENGINEERING BUDGETS
Date: 2026-09-19
Scope: institutional website + interactive Context Core

## 1. Performance principle
**Static value first. Interactive depth second.**

A visitor must receive brand, headline, navigation, primary CTA and an intentional hero visual before interactive 3D becomes a requirement.

Performance budgets are release gates, not aspirational documentation.

## 2. Core Web Vitals targets
Production field target at the 75th percentile where measurable:
- LCP: <= 2.5 s
- INP: <= 200 ms
- CLS: <= 0.1

Internal stretch targets on controlled reference runs:
- LCP: <= 2.0 s
- CLS: <= 0.05

Field data, when available, takes precedence over flattering lab-only results.

## 3. Initial route budgets
These are compressed-transfer engineering targets and may be refined after prototype evidence.

### Non-3D routes
Target initial JS required for page usability:
<= 120 KiB compressed where practical.

### Home before 3D enhancement
Target initial JS required for usable semantic hero/navigation:
<= 150 KiB compressed where practical.

### 3D runtime
Three/R3F/scene runtime must be lazy and separately chunked.
It must not be required for initial textual content or CTA functionality.

No single total-JS number is used to hide the difference between critical and deferred code.

## 4. CSS
Critical/global CSS should remain compact.
Target initial compressed CSS:
<= 50 KiB unless measured evidence justifies more.

Avoid shipping unused component-library styles.

## 5. Fonts
Preferred:
- one variable primary family if it meets brand needs;
- one technical mono only if justified.

Target:
- <= 2 critical font files on first meaningful view;
- preload only truly critical font resources;
- use font-display behavior that preserves immediate text;
- subset carefully without breaking required language/glyph coverage.

## 6. Images
Use responsive image sizes.
Prefer modern formats such as AVIF/WebP where supported by toolchain.
Do not ship desktop hero resolution to small mobile viewports.

Static hero fallback target:
<= 250 KiB compressed for typical viewport where visual quality permits.
Larger variants may exist for high-density/large displays but should be selected responsively.

## 7. 3D asset budgets

### Hero asset package targets
WEB-HIGH:
target <= 3.5 MiB transferred total for hero 3D package.

WEB-MED:
target <= 2.0 MiB.

WEB-LOW:
target <= 1.0 MiB.

STATIC:
target <= 250 KiB typical responsive fallback.

These include model/required texture payload for the hero, not unrelated site assets.

No individual production web asset may approach provider file limits without explicit review.

## 8. Geometry budgets
Initial scene targets after optimization:

WEB-HIGH:
- visible triangles: <= 300k preferred;
- draw calls: <= 100 preferred.

WEB-MED:
- visible triangles: <= 150k preferred;
- draw calls: <= 70 preferred.

WEB-LOW:
- visible triangles: <= 75k preferred;
- draw calls: <= 45 preferred.

Instancing is preferred for repeated elements.
Silhouette and semantic hierarchy matter more than raw triangle count.

## 9. Texture budgets
WEB-HIGH:
- maximum common texture dimension: 2048 unless explicit exception;
- compressed GPU-friendly delivery where compatible.

WEB-MED/LOW:
- prefer 1024 or smaller for most scene textures;
- procedural/material simplification preferred over unnecessary maps.

No blanket 4K texture policy.

## 10. DPR
Do not blindly render at devicePixelRatio.

Initial caps:
HIGH: <= 2.0
MEDIUM: <= 1.5
LOW: <= 1.0–1.25

Controller may reduce DPR dynamically within stable bounds.

## 11. Frame targets
Interactive target:
- 60 fps on capable reference hardware;
- stable >= 45 fps may be acceptable for balanced tier;
- if sustained performance drops below acceptable threshold, degrade quality.

More important than a single FPS sample:
- stable frame time;
- low long-task interference;
- no oscillating quality changes;
- responsive UI.

## 12. Adaptive Fidelity Controller — AFC

### Inputs
- reduced-motion preference;
- viewport;
- effective DPR;
- WebGL/WebGPU capability only as actually used;
- initialization success;
- measured frame-time window;
- document visibility;
- scene visibility;
- memory/performance signals only when reliable and privacy-safe.

Do not use invasive fingerprinting.
Do not maintain a hardcoded consumer-GPU ranking as the primary mechanism.

### Outputs
HIGH
MEDIUM
LOW
STATIC

### Adjustable dimensions
- DPR;
- particle count;
- instance density;
- post-processing;
- transmission/refraction complexity;
- shadow quality;
- shader complexity variants;
- LOD;
- animation update frequency.

## 13. AFC hysteresis
Quality changes must have hysteresis/cooldowns.

Example behavior:
HIGH under sustained stress → MEDIUM.
MEDIUM under sustained stress → LOW.
LOW under sustained stress or initialization failure → STATIC.

Upgrade only after a significantly longer stable period than downgrade.
Never oscillate rapidly between tiers.

## 14. Static-first boot
Sequence:
1. HTML/CSS content;
2. static hero fallback;
3. deferred 3D runtime;
4. load appropriate asset tier;
5. initialize off critical path;
6. crossfade/replace static composition only when live scene is ready.

If any step fails, keep static state.

## 15. Main-thread protection
- avoid large synchronous initialization;
- split noncritical work;
- defer scene setup;
- pause/throttle offscreen animation;
- avoid React rerenders on every animation frame;
- keep high-frequency scene state outside unnecessary UI reconciliation.

## 16. Accessibility baseline
Target WCAG 2.2 AA for institutional website.

Required:
- semantic landmarks;
- logical heading order;
- keyboard operation;
- visible focus;
- sufficient contrast;
- alt text where images convey information;
- decorative assets excluded from accessibility tree appropriately;
- touch target sizing;
- form labels if forms exist;
- skip navigation mechanism;
- reduced-motion support;
- zoom/reflow resilience;
- no information conveyed by color alone.

## 17. Canvas/3D accessibility
3D is enhancement.
Equivalent meaning exists in semantic content.
Decorative canvas should not become noisy screen-reader content.
Interactive 3D controls, if any become meaningful, require accessible equivalents.

## 18. Motion safety
Respect prefers-reduced-motion.
No flashing patterns beyond safe accessibility thresholds.
No forced camera motion required for comprehension.

## 19. Contrast
All text/UI combinations validated programmatically where feasible and visually.
Brand emissive colors are not automatically valid text colors.

## 20. Responsive testing matrix
At minimum:
- small phone;
- modern mainstream phone;
- tablet;
- typical 1366/1440-class laptop;
- 1080p desktop;
- high-DPI desktop.

Browsers:
- Chromium family;
- Safari/WebKit;
- Firefox.

Include iOS Safari because 3D/mobile behavior can differ materially.

## 21. Network testing
Lab profiles should include:
- fast broadband;
- constrained mobile;
- high latency;
- cache-cold first visit;
- cache-warm repeat visit.

The page must remain useful while 3D is still downloading.

## 22. Automated release gates
Planned:
- Lighthouse/appropriate lab audits;
- bundle-size budget;
- asset-size budget;
- accessibility automated scan;
- visual regression;
- link validation;
- production smoke tests.

Automated accessibility does not replace manual keyboard/screen-reader review.

## 23. Performance evidence
Store release evidence for major launches:
- build sizes;
- route bundles;
- hero asset manifest;
- representative Lighthouse results;
- 3D scene metrics;
- accessibility audit notes;
- known exceptions with rationale.

## 24. Acceptance
BR-10 freezes when:
- budgets are approved;
- prototype proves realistic payload/scene targets;
- AFC state machine is implementable;
- static-first boot is demonstrated;
- reduced-motion path is complete;
- reference-device matrix exists;
- automated performance/accessibility gates can be encoded in CI.
