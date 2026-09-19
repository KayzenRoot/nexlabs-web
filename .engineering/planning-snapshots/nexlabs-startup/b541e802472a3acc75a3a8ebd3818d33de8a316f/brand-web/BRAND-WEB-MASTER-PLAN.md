# NexLabs Brand & Institutional Web Program — Master Plan v0.1

Status: PLANNING
Target outcome: production institutional website deployed and operational on a zero-cost hosting tier, with founder-provided custom domain after brand/site acceptance.
Execution: Codex + Blender MCP after planning freeze
Cash constraint: BRL 0
Source of factual company claims: STARTUP-MASTER.md

## Objective
Create a distinctive, application-grade global identity and institutional web presence for NexLabs Technology, with an optimized interactive 3D visual system. The result must strengthen credibility with startup programs, open-source users, developers, accelerators and future investors without overstating company status or traction.

## Execution boundary
This repository plans and governs the work. Codex will implement production code and orchestrate Blender MCP during the execution phase. No implementation prompt is issued until the planning STOP CONDITION is satisfied.

## Program map
### BR-01 Strategy & Brand DNA
Positioning, audiences, brand promise, personality, voice, differentiation, visual territories, anti-patterns.

### BR-02 Naming Architecture & Messaging
Canonical naming, descriptors, tagline system, elevator pitches, headlines, product naming relationship, application-safe claims.

### BR-03 Logo System
Symbol exploration, wordmark, lockups, responsive marks, monochrome, favicon, geometry, clear space, minimum sizes, misuse rules.

### BR-04 Color, Type & Graphic Language
Color tokens, contrast/accessibility, typography, grid, iconography, shapes, diagrams, textures, technical motifs.

### BR-05 NexLabs 3D Language
Hero object/system, geometry grammar, materials, lighting, camera, particles, procedural systems, reusable scene components, LOD strategy.

### BR-06 Motion & Interaction
Motion principles, transitions, scroll behavior, hover/interaction, 3D choreography, reduced-motion behavior.

### BR-07 UX / Information Architecture
Personas, journeys, sitemap, page goals, CTAs, navigation, application-reviewer journey, OSS/developer journey.

### BR-08 Website Content
English-first canonical copy, About, HIVE, Technology, Open Source, Contact, legal/status-safe wording, metadata.

### BR-09 Web Technical Architecture
Framework, rendering strategy, 3D runtime, asset pipeline, content model, SEO, analytics, forms, security, deployment, environments.

### BR-10 Performance & Accessibility
Performance budgets, Web Vitals targets, GLB/texture budgets, adaptive quality, mobile/fallback modes, reduced motion, WCAG targets.

### BR-11 Blender MCP Production Specification
Scene naming, collections, geometry, materials, procedural nodes, cameras, animation clips, export profiles, compression, validation.

### BR-12 UGAS Asset Pipeline
Asset briefs, generation/reference workflow, provenance, review, optimization, export and versioning.

### BR-13 Design System & Component Contract
Tokens, primitives, components, states, responsive behavior, 3D canvas contracts, error/fallback states.

### BR-14 Trust / Program Readiness
Company facts, OSS evidence, GitHub links, contact identity, privacy/security pages, no fabricated social proof.

### BR-15 QA / Observability / Security
Browser/device matrix, visual regression, accessibility tests, performance tests, runtime errors, CSP/security headers, analytics privacy.

### BR-16 Deployment & Release
Zero-cost hosting path, DNS/domain decision, preview/prod, CI/CD, rollback, cache strategy, release checklist.

Deployment candidates: Vercel free tier and Cloudflare free-tier stack. Final provider is selected only after BR-09/10 requirements are compared against current provider limits. Domain purchase is founder-controlled and deferred until naming/brand direction and domain availability are validated.

### BR-17 Codex Execution Package
Repository bootstrap, implementation work orders, Blender MCP prompts/specs, dependency policy, acceptance tests and evidence bundle.

### BR-18 Final Acceptance
Cross-device audit, factual audit, visual QA, performance evidence, accessibility evidence, program-readiness review, production-domain verification and operational handoff.

## Mandatory principles
- English-first global presentation.
- Product company, not agency aesthetics.
- Distinctive NexLabs identity; no cloning competitors.
- 3D is functional brand language, not decorative bloat.
- Progressive enhancement.
- Fast usable first paint independent of 3D.
- Mobile is first-class.
- Reduced-motion and static fallback.
- Every external factual claim traceable to Startup Master/evidence.
- Zero paid dependency unless explicitly approved.
- Production assets optimized for web.
- Design must remain credible without animation.

## STOP CONDITION before Codex implementation
All BR-01 through BR-16 are approved/frozen; sitemap and copy are stable; visual direction and logo concept are selected; 3D scene contracts and budgets exist; technical architecture and deployment are decided; acceptance criteria are measurable; no HIGH/CRITICAL planning ambiguity remains.

Only then generate BR-17 Codex execution work orders.
