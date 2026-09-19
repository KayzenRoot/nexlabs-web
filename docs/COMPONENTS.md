# Component contracts

Components are small, semantic, and composable. Visual hierarchy is controlled by HTML headings and landmarks rather than giant boolean APIs.

## Navigation

`DesktopNav` renders the server-side primary links. `MobileNav` is the only client navigation surface: its trigger exposes `aria-expanded`/`aria-controls`, Escape closes it, focus moves into the close control and returns to the trigger, touch targets are at least 44px, and links close the panel. The menu is not duplicated as an inaccessible second desktop navigation.

## Content and actions

`Action` distinguishes internal links from external links and adds a screen-reader new-tab notice for external destinations. `Heading`, `Text`, `Label`, `Container`, `Stack`, `Cluster`, `Surface`, and `Section` keep semantics independent from visual styling. `EvidenceCard` and `PrincipleCard` accept factual or explicitly framed content.

## Media and diagrams

`VisualSlot` and `HeroVisualSlot` reserve stable media geometry and expose an accessible description unless marked decorative. `TechnicalDiagram` uses native SVG title/description, text labels, geometry, and captions; meaning is not conveyed by color alone. Its diagram is illustrative, not a claim about a finished product architecture.
