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
