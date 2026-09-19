# 04 - Architecture

## Website

Next.js App Router with TypeScript and static export. `out/` is served through Cloudflare Workers + Static Assets or the repository-owned static server. The root layout and content shell remain server-first; theme and mobile navigation are small client islands.

## Governance

GEF is materialized under `.engineering/` and the canonical Project Brain under this directory. HIVE remains a separate Docker Compose runtime. `scripts/hive_bootstrap.py` uses the HIVE HTTP API for health, registry resolution, inspection, indexing and retrieval corpus synchronization. `scripts/hive_mcp.py` launches only the bounded read-only HIVE MCP server through Docker Compose.

## Authority flow

```text
Git + Project Brain -> Work Order/Context Lock -> HIVE-derived context -> implementation evidence -> exact-head review
```

HIVE cannot overwrite canonical Git sources. The website repository never imports HIVE runtime packages.
