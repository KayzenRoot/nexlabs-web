# Execution Workstation Policy

Status: ACTIVE - BLENDER PRODUCTION AUTHORIZED FOR GOVERNED WORK
Date: 2026-09-20

## Current workstation mode
The implementation desktop has verified capability layers for static development and Blender MCP integration. This transition explicitly authorizes governed Blender production; it does not authorize UGAS generation.

Canonical capability state:

- `BLENDER_MCP_READY=true`: Blender 5.2.1 LTS, uv/uvx and the MCP add-on were installed and the end-to-end MCP smoke test passed.
- `BLENDER_PRODUCTION_AUTHORIZED=true`: governed Blender asset production is authorized only with an active Work Order requiring Blender and a passing live MCP preflight.
- `UGAS_CORE_INSTALLED=true`: UGAS 0.25.9 is installed and the canonical `nexlabs-web` inspection passed.
- `UGAS_GENERATION_PROVIDER_READY=false`: the local ComfyUI/provider endpoint at `127.0.0.1:8188` is unavailable.
- `UGAS_GENERATION_AUTHORIZED=false`: UGAS generation and provider startup remain unauthorized and fail-closed.

Until the provider is explicitly prepared and approved:

- do not auto-start a provider or start real generation merely to make `ugas doctor` green;
- do not require UGAS generation for an implementation package;
- do not block ordinary engineering work on final graphical assets;
- keep visual/3D interfaces modular so approved assets can be replaced later without architecture refactoring;
- do not treat temporary graphics as canonical brand assets;
- do not select or freeze a final logo from generic placeholders;
- do not create final logo/runtime assets or start UGAS generation under this transition.

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

## Governed Blender boundary

The direct execution of the CP-05 workstation transition package is the explicit owner authorization for Blender production. Blender production remains conditional on an active governed Work Order and successful live MCP preflight. If MCP preflight fails, the affected Work Order stops fail-closed and no fabricated asset is substituted.

## Deferred / separately governed work
Hold until a separate gate and Work Order authorize it:
- UGAS generation/production;
- any new Blender mutation/rebuild beyond the already approved CP-06 frozen asset package;
- BrandMark/header/favicon promotion when not explicitly admitted by the active Work Order;
- deployment or release.

## Web runtime consumption boundary

The CP-06 HIGH/MED/LOW/STATIC asset package is already approved and hash-bound. CP-07 web runtime consumption of those frozen assets through Three.js/React Three Fiber does not require Blender MCP to be live, provided the active Work Order does not mutate or rebuild Blender-authored source assets.

Three.js/R3F runtime work still requires its own active governed Work Order and Context Lock. If a runtime task discovers that Blender asset mutation is actually required, stop only that Blender-dependent boundary and require a fresh live MCP preflight before mutation. UGAS generation remains separately unauthorized.

## Handoff rule
Every placeholder intended for future replacement must have a clear semantic role and stable interface/slot.

When the founder enables the UGAS/Blender workstation, resume the deferred graphical pipeline from the canonical BR specifications rather than redesigning the application architecture.
## CP-03 design-system boundary

The active workstation mode remains static-first for web/runtime work. CP-03 may implement provisional CSS/SVG/text placeholders and stable media interfaces, but must not produce final logo identity, UGAS derivative media, runtime 3D or Three.js/R3F dependencies. `docs/WORKSTATION-MODE.md` is the repository policy source for this constraint.
