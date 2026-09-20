# 16 - Decisions Ledger

## ADR-NXWEB-001 - Brownfield GEF adoption

Status: accepted for CP-02R execution.

GEF v1.0.0 is materialized as a target-project contract rather than vendored. The active Work Order and Context Lock govern the repair delta.

## ADR-NXWEB-002 - HIVE remains external

Status: accepted for CP-02R execution.

HIVE v1.0.0 remains a separate local-first runtime. The website stores only its read-only launcher, bootstrap bridge, project identity and evidence. HIVE-derived context cannot replace Git-tracked authority.

## ADR-NXWEB-003 - Exact-head governance

Status: accepted for CP-02R execution.

Governance and quality workflows check the exact PR head rather than a synthetic merge ref, and evidence binds the Work Order/Context Lock to that SHA.

## ADR-NXWEB-004 - Protected merge boundary

Status: accepted for CP-02R execution.

Merge, post-merge verification and ruleset required-check migration are separate lifecycle gates. They are not claimed from a green PR run alone.

## ADR-NXWEB-005 - Deterministic HIVE task preparation

Status: accepted for CP-02R corrective execution.

The active Work Order is submitted to HIVE task intake by exact UTF-8 source digest before read-only MCP context retrieval. Existing tasks with the same digest are reused deterministically. MCP remains read-only and cannot create tasks.

## ADR-NXWEB-006 - Web3 strategic direction boundary

Status: accepted as a strategy direction only.

Web3, blockchain and smart-contract engineering may appear in the capability map, but no deployed protocol, audit, token, TVL, customer or on-chain traction claim is authorized by this direction.

## ADR-NXWEB-007 - Workstation capability layers

Status: accepted for CP-03 execution.

The implementation workstation has verified Blender MCP readiness and UGAS core installation, but the UGAS generation provider is not ready because the local ComfyUI/provider endpoint is unavailable. CP-03 records these capability layers truthfully and remains static-only: no provider auto-start, generation, final logo, canonical 3D, Blender asset production or UGAS derivative media is admitted.

## ADR-NXWEB-008 - CP-03 HIVE license truth

Status: accepted for CP-03 execution.

The pinned HIVE repository documentation and `LICENSE` at `a53b5b9fcf55c32a5696180fb1b1ef80ccd1edcf` state that the repository is All Rights Reserved and is not an open-source license. The website may link to and describe the public implementation, but must not publish the stale Apache-2.0 claim from the planning draft.

## ADR-NXWEB-009 - Blender production workstation transition

Status: accepted for governed CP-05 resumption after the protected transition merge.

This workstation is authorized for governed Blender production beginning with CP-05. The authorization is supported by Blender 5.2.1 LTS, MCP add-on 1.7/protocol 7, and passing `get_addon_status` and `get_scene_info` preflight receipts. Blender work remains conditional on an active governed Work Order and a passing live MCP gate; if that gate fails, the affected Work Order stops fail-closed.

UGAS generation remains unauthorized and unready: `UGAS_GENERATION_PROVIDER_READY=false` and `UGAS_GENERATION_AUTHORIZED=false`. This decision does not promote NX-C-02 into runtime, admit CP-06, authorize Three.js/R3F, deployment, release or provider startup.
