from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.error
from pathlib import Path
from typing import Any

try:
    from .hive_bootstrap import request, resolve_registered_project
except ImportError:  # pragma: no cover - direct script execution
    from hive_bootstrap import request, resolve_registered_project

ROOT = Path(__file__).resolve().parents[1]
GEF_CURRENT = ".engineering/gef/GEF-CURRENT.json"
WORK_ORDER_DIR = ".engineering/work-orders"
SAFE_WORK_ORDER_ID = re.compile(r"^[A-Za-z0-9._-]+$")


class PreparationError(RuntimeError):
    """The deterministic HIVE preparation boundary cannot be satisfied."""


def git_output(*arguments: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), *arguments],
            capture_output=True,
            check=True,
            text=True,
            timeout=10,
            shell=False,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise PreparationError(f"Git command failed: git {' '.join(arguments)}") from exc
    return result.stdout.strip()


def resolve_git_state() -> dict[str, Any]:
    status = git_output("status", "--porcelain=v1", "--untracked-files=all")
    if status:
        raise PreparationError("working tree is not clean; refuse HIVE task preparation")
    branch = git_output("branch", "--show-current")
    if not branch:
        raise PreparationError("detached HEAD is not accepted for HIVE preparation")
    head = git_output("rev-parse", "HEAD")
    return {"branch": branch, "head": head, "working_tree_clean": True}


def resolve_work_order(explicit: str | None) -> str:
    if explicit:
        relative = explicit
    else:
        current_path = ROOT / GEF_CURRENT
        try:
            current = json.loads(current_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise PreparationError("GEF current state is unavailable or invalid") from exc
        active = current.get("activeWorkOrder")
        if not isinstance(active, str) or not active.strip():
            raise PreparationError("GEF has no active Work Order; admit one before HIVE preparation")
        active = active.strip()
        if SAFE_WORK_ORDER_ID.fullmatch(active) is None:
            raise PreparationError("active Work Order identity is unsafe")
        relative = f"{WORK_ORDER_DIR}/{active}.md"

    candidate = Path(relative)
    if candidate.is_absolute() or any(part in {"", ".", ".."} for part in candidate.parts):
        raise PreparationError("Work Order path is unsafe")
    return candidate.as_posix()


def work_order_bytes(relative_path: str) -> tuple[Path, bytes]:
    path = (ROOT / relative_path).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise PreparationError("Work Order path escapes the repository") from exc
    if not path.is_file():
        raise PreparationError(f"Work Order not found: {relative_path}")
    raw = path.read_bytes()
    if not raw:
        raise PreparationError("Work Order is empty")
    return path, raw


def source_digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _task_ready(task: dict[str, Any], *, project_id: str, digest: str) -> bool:
    return (
        task.get("project_id") == project_id
        and isinstance(task.get("task_id"), str)
        and bool(task.get("task_id"))
        and task.get("original_blob_sha256") == digest
        and task.get("intake_status") == "READY"
        and task.get("extracted_text_available") is True
    )


def select_reusable_task(
    tasks: list[dict[str, Any]], *, project_id: str, digest: str
) -> dict[str, Any] | None:
    matching = [
        task
        for task in tasks
        if task.get("project_id") == project_id and task.get("original_blob_sha256") == digest
    ]
    if not matching:
        return None
    ready = [task for task in matching if _task_ready(task, project_id=project_id, digest=digest)]
    if not ready:
        raise PreparationError("matching HIVE task exists but extraction is not READY")
    return sorted(ready, key=lambda task: str(task.get("task_id", "")))[0]


def ensure_task_ready(task: dict[str, Any], *, project_id: str, digest: str) -> None:
    if not _task_ready(task, project_id=project_id, digest=digest):
        raise PreparationError("HIVE task is not READY, extracted, digest-bound and project-scoped")


def build_task_payload(raw: bytes, *, title: str) -> dict[str, Any]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PreparationError("Work Order must be UTF-8") from exc
    return {"title": title, "text": text, "format": "markdown"}


def prepare(
    *,
    base_url: str,
    name: str,
    relative_path: str,
    work_order: str | None,
) -> dict[str, Any]:
    git_state = resolve_git_state()
    work_order_relative = resolve_work_order(work_order)
    work_order_path, raw = work_order_bytes(work_order_relative)
    digest = source_digest(raw)

    health = request(base_url, "GET", "/api/v1/health")
    if health.get("status") != "ok":
        raise PreparationError(f"HIVE health is not ok: {health}")

    projects = request(base_url, "GET", "/api/v1/projects")
    if not isinstance(projects, list):
        raise PreparationError("HIVE project list returned an unexpected payload")
    project = resolve_registered_project(projects, name=name, relative_path=relative_path)
    if project is None:
        raise PreparationError("NEXLABS-WEB is not registered; run hive_bootstrap first")

    project_id = project.get("project_id")
    if not isinstance(project_id, str) or not project_id:
        raise PreparationError("HIVE project has no project_id")

    inspected = request(base_url, "POST", f"/api/v1/projects/{project_id}/inspect")
    if inspected.get("state") != "READY":
        raise PreparationError(f"HIVE project is not READY: {inspected}")
    if inspected.get("relative_path") != relative_path:
        raise PreparationError("HIVE project relative path mismatch")
    if inspected.get("git_head_sha") != git_state["head"]:
        raise PreparationError(
            f"HIVE source head {inspected.get('git_head_sha')} does not match Git HEAD {git_state['head']}"
        )
    if inspected.get("working_tree_clean") is not True:
        raise PreparationError("HIVE reports a dirty working tree")

    index = request(base_url, "POST", f"/api/v1/projects/{project_id}/index")
    if index.get("status") != "COMPLETED":
        raise PreparationError(f"HIVE repository index did not complete: {index}")

    corpus = request(base_url, "POST", f"/api/v1/projects/{project_id}/retrieval/corpus/sync")
    if corpus.get("status") not in {"COMPLETED", "CURRENT"}:
        raise PreparationError(f"HIVE retrieval corpus is not current: {corpus}")

    tasks = request(base_url, "GET", f"/api/v1/projects/{project_id}/tasks?limit=200")
    if not isinstance(tasks, list):
        raise PreparationError("HIVE task list returned an unexpected payload")

    task = select_reusable_task(tasks, project_id=project_id, digest=digest)
    reused = task is not None

    if task is None:
        task = request(
            base_url,
            "POST",
            f"/api/v1/projects/{project_id}/tasks/text",
            build_task_payload(raw, title=work_order_path.stem),
        )

    if not isinstance(task, dict):
        raise PreparationError("HIVE task intake returned an unexpected payload")
    ensure_task_ready(task, project_id=project_id, digest=digest)

    return {
        "project_id": project_id,
        "project_name": inspected.get("name"),
        "project_relative_path": inspected.get("relative_path"),
        "project_state": inspected.get("state"),
        "task_id": task["task_id"],
        "task_reused": reused,
        "task_intake_status": task.get("intake_status"),
        "task_extracted_text_available": task.get("extracted_text_available"),
        "work_order_id": work_order_path.stem,
        "work_order": work_order_relative,
        "work_order_sha256": digest,
        "git_branch": git_state["branch"],
        "git_head_sha": git_state["head"],
        "index_status": index.get("status"),
        "corpus_status": corpus.get("status"),
        "hive_api": base_url,
        "hive_version_expected": "1.0.0",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare the active GEF Work Order as a deterministic HIVE task")
    parser.add_argument("--base-url", default=os.getenv("HIVE_API_URL", "http://localhost:8000"))
    parser.add_argument("--name", default="NEXLABS-WEB")
    parser.add_argument(
        "--relative-path",
        default=os.getenv("HIVE_NEXLABS_WEB_RELATIVE_PATH") or Path.cwd().name,
        help="POSIX-relative path below HIVE_PROJECTS_ROOT",
    )
    parser.add_argument(
        "--work-order",
        default=None,
        help="Optional explicit tracked Work Order path. By default the active Work Order is resolved from GEF-CURRENT.json.",
    )
    args = parser.parse_args()
    print(json.dumps(prepare(**vars(args)), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (PreparationError, urllib.error.URLError, RuntimeError) as exc:
        print(f"HIVE preparation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
