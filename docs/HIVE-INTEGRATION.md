# HIVE v1.0.0 Integration

NexLabs Web integrates HIVE as a separate local-first runtime at `a53b5b9fcf55c32a5696180fb1b1ef80ccd1edcf`. The HIVE backend, database, Redis, dashboard and Docker Compose files are never copied into this repository.

## Project identity

- name: `NEXLABS-WEB`;
- relative path: `nexlabs-web` below the machine-local `HIVE_PROJECTS_ROOT`;
- API: `http://localhost:8000` by default;
- required state: `READY`, index `COMPLETED`, corpus `CURRENT` or `COMPLETED`.

Run `python scripts/hive_bootstrap.py --relative-path nexlabs-web` after the supported HIVE Compose runtime is healthy. The script resolves exact relative-path identity, fails on a same-name collision, inspects Git, indexes and synchronizes the retrieval corpus.

## MCP

`.codex/config.toml` defines required stdio server `hive` through `python scripts/hive_mcp.py`. The launcher resolves `HIVE_REPO_PATH`, sibling `hive` or sibling `Hive`, then runs `docker compose exec -T api python -m app.mcp_server`.

Only `project.list`, `project.status`, `context.build`, `context.search`, `memory.search`, `memory.get` and `checkpoint.read` are allowed. All are read-only. No provider credential is committed.

## Runtime evidence

HIVE-derived context cannot replace the canonical Project Brain or Git. If Docker or HIVE is unavailable, the Work Order records the exact external blocker and never fabricates registration, index or corpus success.
