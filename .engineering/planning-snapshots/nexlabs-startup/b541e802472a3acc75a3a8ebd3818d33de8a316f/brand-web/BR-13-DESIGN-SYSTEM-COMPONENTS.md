# BR-13 — Design System & Component Contract

Status: SYSTEM ARCHITECTURE
Date: 2026-09-19

## 1. Principle
Pages compose approved primitives and sections.
Pages do not invent independent visual systems.

Architecture:
Primitive tokens
→ Semantic tokens
→ UI primitives
→ Brand components
→ Section patterns
→ Pages.

3D remains an enhancement layer with explicit boundaries.

## 2. Component domains

### UI primitives
Button
Link
Icon
Text
Heading
Label
Badge
Divider
Surface
Container
Stack
Cluster
Grid

### Navigation/layout
Header
DesktopNav
MobileNav
Footer
SkipLink
PageShell
Section
SectionHeader

### Brand/content
BrandMark
Wordmark
Eyebrow
HeroCopy
EvidenceCard
PrincipleCard
ProductCard
CapabilityItem
TechnicalCallout
CTAGroup
ExternalEvidenceLink

### Technical/diagram
SystemFlow
ArchitectureDiagram
Metric/FactLine
CodeOrMetadataLabel

### 3D
ThreeBoundary
ThreeCanvas
ContextCore
Static3DFallback
QualityIndicatorDev
ThreeErrorBoundary

### System
ThemeController
MotionPreferenceBridge
AdaptiveFidelityProvider
ExternalLink
Metadata helpers

## 3. Button contract
Variants:
primary
secondary
quiet

States:
default
hover
focus-visible
active
disabled
loading only if an actual asynchronous action exists.

Rules:
- anchor navigation is not disguised as a button component internally when semantic link behavior is correct;
- minimum accessible target;
- visible focus;
- icon-only button requires accessible name;
- no magnetic movement that impairs pointing.

## 4. Link contract
Variants:
inline
navigation
evidence
external.

External links must remain understandable.
Do not add target=_blank indiscriminately.

## 5. Typography
Semantic components map to BR-04 roles.
Heading level is chosen for document structure, not visual size.
Visual style and HTML heading level can be configured independently within safe API constraints.

## 6. Container
Controls:
- content max width;
- reading max width;
- wide/visual max width;
- responsive gutters.

No arbitrary page-specific max-width values unless documented exception.

## 7. Section
Responsibilities:
- vertical rhythm;
- semantic section wrapper;
- optional anchor id;
- standard content width;
- optional visual layer slot.

A Section never requires JavaScript merely to render its content.

## 8. Header
Requirements:
- brand;
- primary navigation;
- GitHub utility;
- Contact;
- accessible mobile trigger;
- keyboard operation;
- stable layout;
- optional surface transition after scroll.

No hero canvas owns the header.

## 9. MobileNav
Requirements:
- focus management;
- escape/close behavior;
- scroll handling without trapping user;
- clear active route;
- reduced-motion behavior;
- no duplicated inaccessible navigation tree.

## 10. EvidenceCard
Purpose:
Show verifiable product/OSS facts.

Inputs may include:
- title;
- description;
- evidence type;
- link;
- metadata.

Must not manufacture metrics.

## 11. ProductCard
V1 primary use: HIVE.
Designed for future reuse without rendering nonexistent products today.

## 12. TechnicalDiagram
HTML/SVG-first when semantic structure benefits accessibility/responsiveness.
3D is not the default for every diagram.

Requirements:
- text remains selectable where practical;
- shape + label, not color alone;
- accessible explanation/caption.

## 13. CTAGroup
Controls primary/secondary action hierarchy.
Maximum emphasis is constrained so sections do not contain three “primary” actions.

## 14. ThreeBoundary
Owns the boundary between semantic page and interactive scene.

Responsibilities:
- static-first placeholder;
- lazy client initialization;
- fallback;
- error isolation;
- reduced-motion mode;
- quality state handoff;
- lifecycle visibility.

Page content must remain valid if ThreeBoundary never hydrates.

## 15. ContextCore
Consumes:
- semantic scene state;
- quality tier;
- motion preference;
- interaction input;
- asset manifest.

Does not own:
- page copy;
- navigation;
- SEO;
- business logic.

## 16. ThreeErrorBoundary
On runtime failure:
- preserve page;
- show intentional static fallback;
- suppress retry loops;
- optionally emit approved diagnostic event.

## 17. ThemeController
Theme options planned:
dark
light
system

Institutional default may be dark-first while respecting explicit user choice.
Persistence mechanism must be small and privacy-appropriate.

Avoid flash of incorrect theme.

## 18. AdaptiveFidelityProvider
Implements BR-10 AFC contract.
3D scenes consume selected tier rather than independently guessing device quality.

## 19. Component state model
Every interactive component documents applicable:
default
hover
focus-visible
active
disabled
loading
error
reduced-motion
dark/light.

Do not implement meaningless states.

## 20. Responsive contract
Components own their responsive behavior.
Pages should not patch component internals with fragile selector overrides.

Use content-driven breakpoints where practical, aligned to system-level breakpoint tokens.

## 21. Accessibility contract
Each component documents:
- semantic element;
- keyboard behavior;
- focus behavior;
- accessible name requirements;
- ARIA only where native semantics are insufficient;
- reduced-motion behavior;
- contrast/state requirements.

No ARIA used as decoration.

## 22. Motion contract
Components consume BR-06 motion tokens.
UI components do not invent bespoke durations/easings.

## 23. Styling contract
Preferred:
- design tokens exposed as CSS custom properties;
- component styles consume semantic/component tokens;
- avoid hardcoded raw palette values;
- no inline arbitrary magic numbers except calculated/runtime values with documented purpose.

Exact styling mechanism freezes with implementation framework validation.

## 24. Composition rule
Prefer composition over giant components with dozens of booleans.
APIs should expose meaningful slots/variants, not page-specific hacks.

## 25. Server/client boundary
Default component is server/static-capable where framework permits.
Client component only when interaction/runtime state requires it.

Do not mark entire page trees client-side merely to animate one element.

## 26. Dependency isolation
Three.js/R3F imports stay within 3D boundary/module tree.
Non-3D components must not accidentally pull 3D runtime into their bundles.

## 27. Documentation
For each production component:
- purpose;
- API;
- variants;
- accessibility;
- examples;
- states;
- dependencies;
- tests.

A lightweight internal component gallery may replace full Storybook if Storybook cost/complexity is unjustified for V1.

## 28. Testing
UI primitives:
unit/component tests where behavior exists.

Interactive components:
keyboard/focus/state tests.

Critical visual components:
visual regression.

3D boundary:
fallback/error/reduced-motion/lazy-load lifecycle tests.

## 29. Anti-patterns
Reject:
- page-specific duplicate buttons;
- one-off colors;
- arbitrary z-index escalation;
- giant all-purpose Card component;
- DOM text inside WebGL when semantic HTML works;
- decorative client components for static content;
- nested animation libraries;
- hidden content waiting forever for JS animation.

## 30. Acceptance
BR-13 freezes when:
- component inventory covers all BR-07 pages;
- UI/3D boundaries are explicit;
- accessibility contract exists;
- responsive behavior ownership is clear;
- tokens feed components;
- client JS is limited to components that need it;
- no page requires an ungoverned design primitive.
