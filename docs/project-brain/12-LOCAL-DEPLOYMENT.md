# 12 - Local Deployment

## Website

```text
npm ci
npm run build
npm run start
```

The website produces `out/` and does not start a server-side application runtime.

## HIVE

HIVE is a sibling external checkout. Configure the machine-local `HIVE_PROJECTS_ROOT` so it contains the `nexlabs-web` checkout, start HIVE with its supported Docker Compose procedure, then run:

```text
python scripts/hive_bootstrap.py --relative-path nexlabs-web
python scripts/hive_prepare.py --relative-path nexlabs-web
```

The preparation command must pass before read-only MCP retrieval: it returns the HIVE project/task/head binding and reuses the active Work Order by exact source digest. The committed launcher uses `HIVE_REPO_PATH` when supplied, then sibling `hive` or `Hive` directories. No absolute path is committed.
