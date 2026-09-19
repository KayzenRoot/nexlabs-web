# NexLabs design system

CP-02 establishes the semantic shell consumed by later page work. It is deliberately static-first and provisional while the final logo, visual identity, UGAS, Blender output, and canonical 3D direction remain outside this workstation's active mode.

## Contract

- `design/tokens/source.json` is the source of truth; generated artifacts are checked for deterministic drift.
- Components consume semantic or component custom properties. Page code does not own raw palette values.
- Dark is the default candidate, with explicit light and system modes. The pre-hydration theme bootstrap is intentionally tiny and uses the existing inline-script CSP allowance.
- Native system typography is used. No remote font or third-party browser script is loaded.
- The layout contract includes content, reading, and wide containers; desktop 12-column intent, tablet 8-column intent, and mobile 4-column intent are expressed through responsive CSS grids.
- Motion is tokenized and reduced motion is a hard override. The shell remains useful when JavaScript is unavailable.

## Implemented surface

The reusable layer includes actions, typography, layout primitives, Wordmark/replaceable BrandMark, HeroCopy, EvidenceCard, PrincipleCard, CTAGroup, VisualSlot/HeroVisualSlot, technical diagram, DesktopNav, accessible MobileNav, SkipLink, PageShell-like sections, Footer, and ThemeController.

`VisualSlot` is the approved replacement boundary for future media. It has stable layout, label/description, decorative mode, and no dependency on an asset or product claim.

## Boundaries

This checkpoint does not create final logo candidates, final 3D, UGAS, Blender MCP artifacts, Three.js/R3F dependencies, backend/auth/database, analytics, contact capture, or production-domain configuration.
