# BR-04 — Visual System: Color, Type & Graphic Language

Status: PROPOSED
Date: 2026-09-19

## 1. Theme architecture
Decision direction:
- Brand/institutional website: DARK-FIRST.
- Design system: DARK + LIGHT token architecture from day one.
- Future products may select theme by product needs.
- No component may depend on a decorative gradient for legibility.

## 2. Color architecture

### Neutral foundation — Mineral
Use perceptually controlled near-neutrals rather than pure black everywhere.

Roles:
- mineral-void: deepest page field;
- mineral-base: primary surface;
- mineral-raised: cards/panels;
- mineral-edge: subtle separation;
- mineral-text: primary text;
- mineral-muted: secondary text.

Exact color values are NOT frozen until contrast and display testing.

### Brand signal — Spectral Cyan
Lead candidate family: cool cyan/blue spectral energy.

Purpose:
- active routes;
- primary interactive focus;
- 3D signal energy;
- selective brand highlights.

Constraint:
Do not flood backgrounds with saturated cyan.

### Secondary signal — Ion Violet
Lead complementary family: controlled violet/indigo.

Purpose:
- secondary system states;
- depth transitions;
- selective spectral gradients;
- 3D energy separation.

### Rare accent — Plasma Warm
A very limited warm signal may be explored for contrast/state emphasis.

It must not turn the identity into orange-vs-blue cinematic cliché.

## 3. Gradient rule
Gradients belong primarily to ENERGY and DEPTH, not to typography decoration.

Approved conceptual uses:
- emissive path transitions;
- volumetric/spectral 3D effects;
- subtle active-state accents.

Avoid:
- gradient on every button;
- rainbow AI branding;
- large text made readable only through gradient.

## 4. Semantic color layer
Functional tokens are independent from brand accents:
- success;
- warning;
- danger;
- info;
- focus;
- disabled.

Accessibility wins over aesthetic purity for functional states.

## 5. Contrast
Target WCAG 2.2 AA as baseline for standard web content.
Critical text/navigation should seek stronger contrast where practical.
Decorative 3D color never substitutes semantic UI cues.

## 6. Typography architecture

### Display / Brand
Direction: modern grotesk/geometric sans with precision, not sci-fi novelty.

Requirements:
- zero-cost commercial/web licensing;
- excellent Latin support;
- variable font preferred;
- strong large-display shapes;
- readable lowercase;
- clean numerals;
- good web performance.

### UI / Body
Prefer either:
A. one high-quality variable family across display/body, using optical/weight hierarchy; or
B. tightly paired display + utilitarian UI family if testing proves meaningful improvement.

### Mono
A zero-cost technical monospace may be used selectively for:
- code;
- labels;
- coordinates;
- system metadata;
- technical diagrams.

Never use mono for entire paragraphs as “developer aesthetic”.

## 7. Type scale
Use fluid responsive typography via clamp() rather than breakpoint jumps.

Planned semantic roles:
- display-xl;
- display-lg;
- heading-1;
- heading-2;
- heading-3;
- body-lg;
- body;
- body-sm;
- label;
- code/meta.

Exact rem/clamp values are decided with real homepage compositions.

## 8. Typography behavior
Headlines: compact, controlled line length, strong rhythm.
Body: high legibility and comfortable measure.
Technical labels: restrained uppercase/mono only where semantic.
Avoid extreme tracking and ultra-thin weights on dark backgrounds.

## 9. Grid
Desktop foundation: 12-column responsive grid.
Tablet: adaptive 8-column behavior where useful.
Mobile: 4-column foundation.

Grid is a layout system, not visible decoration.
3D may break the grid compositionally while content anchors remain aligned.

## 10. Spacing
Adopt a tokenized spacing scale with a small primitive unit and semantic aliases.
Avoid arbitrary one-off margins during implementation.

Semantic spacing:
- section;
- cluster;
- component;
- inline;
- micro.

## 11. Shape language
Primary UI shapes:
- precise geometry;
- restrained corner radius;
- occasional cut/structural detail derived from logo grammar.

Avoid universal pill-shaped UI and oversized bubbly cards.

3D geometry may be richer, but UI remains disciplined.

## 12. Borders & depth
Use contrast, spacing and surface luminance before adding borders.
When borders are needed, they are low-noise technical separators.
Shadows are subtle and physically plausible; dark UI does not need glowing outlines everywhere.

## 13. Iconography
Direction:
- simple line/structural icons;
- consistent optical weight;
- geometric relation to brand grammar;
- no emoji as production navigation icons;
- use an OSS icon library initially only if its license and visual fit are approved.

Custom icons reserved for brand/product concepts where generic symbols fail.

## 14. Graphic language
Supporting motifs:
- topology traces;
- controlled routing lines;
- layer cuts;
- node fields;
- spatial coordinates;
- context bands;
- sparse technical annotations.

Each motif must have a role. Decorative density is capped.

## 15. Diagrams
NexLabs technical diagrams should share the brand system:
- mineral neutral surfaces;
- spectral signal paths;
- strong labels;
- consistent node/edge grammar;
- accessible color + shape encoding;
- exportable to web, docs and decks.

## 16. Imagery
Primary identity should not depend on stock photography.
Preferred:
- owned 3D renders;
- product UI;
- technical diagrams;
- generated/owned visual assets with documented provenance where needed.

Human photography can be introduced later when authentic founder/team imagery exists.

## 17. Design-token model
Implementation should separate:
Primitive tokens → semantic tokens → component tokens.

Example conceptual chain:
spectral-cyan-* → color-action-primary → button-primary-background.

This prevents raw brand colors from leaking across components.

## 18. Motion tokens
Plan semantic motion tokens:
- instant;
- fast;
- standard;
- deliberate;
- cinematic.

Also:
- easing-enter;
- easing-exit;
- easing-system;
- reduced-motion alternatives.

Exact durations are BR-06 decisions.

## 19. Light theme
Light mode should feel like the same laboratory under analytical illumination:
- mineral-white/soft neutral foundation;
- dark structural typography;
- spectral accents preserved;
- 3D scenes relit/reframed when required.

Do not simply invert dark colors.

## 20. Current art direction
Dark Mineral Laboratory
+ Mineral neutral foundation
+ Spectral Cyan primary signal
+ Ion Violet secondary signal
+ rare Plasma Warm accent
+ precise grotesk typography
+ restrained technical mono
+ topology/routing graphic grammar

## 21. Freeze requirements
BR-04 freezes after:
- actual candidate palettes pass contrast tests;
- typography licenses verified;
- display/body tests on real compositions;
- dark/light semantic tokens demonstrated;
- logo finalists remain strong in the palette;
- 3D materials and UI colors coexist without visual conflict.
