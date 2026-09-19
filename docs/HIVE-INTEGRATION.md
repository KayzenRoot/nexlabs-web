# HIVE v1.0.0 Integration

NexLabs Web integrates HIVE as a separate local-first runtime at `a53b5b9fcf55c32a5696180fb1b1ef80ccd1edcf`. The HIVE backend, database, Redis, dashboard and Docker Compose files are never copied into this repository.

## Project identity

- name: `NEXLABS-WEB`;
- relative path: `nexlabs-web` below the machine-local `HIVE_PROJECTS_ROOT`;
- API: `http://localhost:8000` by default;
- required state: `READY`, index `COMPLETED`, corpus `CURRENT` or `COMPLETED`.

Run `python scripts/hive_bootstrap.py --relative-path nexlabs-web` after the supported HIVE Compose runtime is healthy. The script resolves exact relative-path identity, fails on a same-name collision, inspects Git, indexes and synchronizes the retrieval corpus.

## Deterministic task preparation

Before using the read-only MCP surface, run:

```text
python scripts/hive_prepare.py --relative-path nexlabs-web
```

The preparation bridge fails closed on a dirty or mismatched checkout, refreshes project inspection/index/corpus, computes the SHA-256 digest of the active Work Order's exact UTF-8 bytes, reuses a task with that digest when present, or submits one Markdown task through `POST /api/v1/projects/{project_id}/tasks/text`. Its JSON output binds `project_id`, `task_id`, Work Order digest and Git HEAD for subsequent MCP calls. It never creates tasks through MCP and never writes canonical project state.

## MCP

`.codex/config.toml` defines required stdio server `hive` through `python scripts/hive_mcp.py`. The launcher resolves `HIVE_REPO_PATH`, sibling `hive` or sibling `Hive`, then runs `docker compose exec -T api python -m app.mcp_server`.

Only `project.list`, `project.status`, `context.build`, `context.search`, `memory.search`, `memory.get` and `checkpoint.read` are allowed. All are read-only. No provider credential is committed.

## Runtime evidence

HIVE-derived context cannot replace the canonical Project Brain or Git. If Docker or HIVE is unavailable, the Work Order records the exact external blocker and never fabricates registration, index or corpus success.
