# Execution Workstation Policy

Status: ACTIVE
Date: 2026-09-19

## Current workstation mode
The implementation desktop has verified capability layers for static development and Blender MCP integration, but it is not a ready UGAS generation workstation.

Canonical capability state:

- `BLENDER_MCP_READY=true`: Blender 5.2.1 LTS, uv/uvx and the MCP add-on were installed and the end-to-end MCP smoke test passed.
- `UGAS_CORE_INSTALLED=true`: UGAS 0.25.9 is installed and the canonical `nexlabs-web` inspection passed.
- `UGAS_GENERATION_PROVIDER_READY=false`: the local ComfyUI/provider endpoint at `127.0.0.1:8188` is unavailable.

Until the provider is explicitly prepared and approved:

- do not auto-start a provider or start real generation merely to make `ugas doctor` green;
- do not require UGAS generation for an implementation package;
- do not block engineering work on final graphical assets;
- use neutral generic placeholders, simple CSS/SVG geometry, or text-only placeholders where a visual slot must exist;
- keep visual/3D interfaces modular so approved assets can be replaced later without architecture refactoring;
- do not treat temporary graphics as canonical brand assets;
- do not select or freeze a final logo from generic placeholders;
- do not create substitute "final" 3D models outside the approved Blender/UGAS workstation.

## Allowed work in this mode
Continue normally with:
- repository engineering;
- design-token architecture;
- layout/component engineering;
- responsive behavior;
- accessibility;
- content/pages;
- metadata/SEO;
- tests;
- performance;
- security;
- Cloudflare/deployment preparation;
- generic placeholder contracts for future media.

## Deferred work
Hold until the founder explicitly announces that the UGAS/Blender workstation is available:
- UGAS generation/production;
- final graphical identity production;
- final logo production/evaluation that depends on graphics tooling;
- Context Core canonical 3D production;
- high-fidelity motion/3D asset integration.

Blender MCP readiness is an integration capability only; it does not authorize Blender asset production in CP-03.

## Handoff rule
Every placeholder intended for future replacement must have a clear semantic role and stable interface/slot.

When the founder enables the UGAS/Blender workstation, resume the deferred graphical pipeline from the canonical BR specifications rather than redesigning the application architecture.
## CP-03 design-system boundary

The active workstation mode remains static-first. CP-03 may implement provisional CSS/SVG/text placeholders and stable media interfaces, but must not produce final logo identity, UGAS derivative media, Blender assets, canonical 3D, or Three.js/R3F dependencies. `docs/WORKSTATION-MODE.md` is the repository policy source for this constraint.
