from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

try:
    from .hive_bootstrap import request, resolve_registered_project
except ImportError:  # pragma: no cover - direct script execution
    from hive_bootstrap import request, resolve_registered_project

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORK_ORDER = ".engineering/work-orders/NXWEB-WO-0001-CP02-GEF-HIVE-ADOPTION.md"


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


def select_reusable_task(tasks: list[dict[str, Any]], digest: str) -> dict[str, Any] | None:
    matches = [task for task in tasks if task.get("original_blob_sha256") == digest]
    if not matches:
        return None
    return sorted(matches, key=lambda task: str(task.get("task_id", "")))[0]


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
    work_order: str,
) -> dict[str, Any]:
    git_state = resolve_git_state()
    _, raw = work_order_bytes(work_order)
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
    if not project_id:
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
    task = select_reusable_task(tasks, digest)
    reused = task is not None
    if task is None:
        title = f"{work_order.rsplit('/', 1)[-1]} @ {git_state['head'][:12]}"
        task = request(
            base_url,
            "POST",
            f"/api/v1/projects/{project_id}/tasks/text",
            build_task_payload(raw, title=title),
        )
        if task.get("original_blob_sha256") != digest:
            raise PreparationError("HIVE task digest does not match the Work Order source")
    if task.get("project_id") != project_id or not task.get("task_id"):
        raise PreparationError("HIVE task is not project-scoped or has no task_id")

    return {
        "project_id": project_id,
        "task_id": task["task_id"],
        "task_reused": reused,
        "work_order": work_order,
        "work_order_sha256": digest,
        "git": git_state,
        "hive": {
            "api": base_url,
            "name": inspected.get("name"),
            "relative_path": inspected.get("relative_path"),
            "state": inspected.get("state"),
            "index_status": index.get("status"),
            "corpus_status": corpus.get("status"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a deterministic NexLabs Work Order task in HIVE")
    parser.add_argument("--base-url", default=os.getenv("HIVE_API_URL", "http://localhost:8000"))
    parser.add_argument("--name", default="NEXLABS-WEB")
    parser.add_argument("--relative-path", default="nexlabs-web")
    parser.add_argument("--work-order", default=DEFAULT_WORK_ORDER)
    args = parser.parse_args()
    print(json.dumps(prepare(**vars(args)), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (PreparationError, urllib.error.URLError, RuntimeError) as exc:
        print(f"HIVE preparation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
