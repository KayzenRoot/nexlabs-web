from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import scripts.hive_prepare as hp


class HivePrepareTests(unittest.TestCase):
    def test_source_digest_matches_exact_bytes(self) -> None:
        raw = b"# Work Order\r\n"
        self.assertEqual(hp.source_digest(raw), hashlib.sha256(raw).hexdigest())

    def test_dirty_git_fails_closed(self) -> None:
        with patch("scripts.hive_prepare.git_output", return_value=" M tracked.txt"):
            with self.assertRaisesRegex(hp.PreparationError, "working tree is not clean"):
                hp.resolve_git_state()

    def test_active_work_order_is_resolved_from_gef_current(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            current = root / ".engineering" / "gef" / "GEF-CURRENT.json"
            current.parent.mkdir(parents=True)
            current.write_text(
                json.dumps({"activeWorkOrder": "NXWEB-WO-0002-CP03-PAGES"}),
                encoding="utf-8",
            )
            with patch("scripts.hive_prepare.ROOT", root):
                self.assertEqual(
                    hp.resolve_work_order(None),
                    ".engineering/work-orders/NXWEB-WO-0002-CP03-PAGES.md",
                )

    def test_missing_active_work_order_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            current = root / ".engineering" / "gef" / "GEF-CURRENT.json"
            current.parent.mkdir(parents=True)
            current.write_text(json.dumps({"activeWorkOrder": None}), encoding="utf-8")
            with patch("scripts.hive_prepare.ROOT", root):
                with self.assertRaisesRegex(hp.PreparationError, "no active Work Order"):
                    hp.resolve_work_order(None)

    def test_reuses_ready_task_for_matching_digest(self) -> None:
        tasks = [
            {
                "task_id": "b",
                "project_id": "project",
                "original_blob_sha256": "digest",
                "intake_status": "READY",
                "extracted_text_available": True,
            },
            {
                "task_id": "a",
                "project_id": "project",
                "original_blob_sha256": "digest",
                "intake_status": "READY",
                "extracted_text_available": True,
            },
        ]
        self.assertEqual(
            hp.select_reusable_task(tasks, project_id="project", digest="digest"),
            tasks[1],
        )

    def test_matching_unready_task_fails_closed(self) -> None:
        tasks = [
            {
                "task_id": "a",
                "project_id": "project",
                "original_blob_sha256": "digest",
                "intake_status": "EXTRACTION_FAILED",
                "extracted_text_available": False,
            }
        ]
        with self.assertRaisesRegex(hp.PreparationError, "extraction is not READY"):
            hp.select_reusable_task(tasks, project_id="project", digest="digest")

    def test_non_matching_digest_does_not_reuse_task(self) -> None:
        self.assertIsNone(
            hp.select_reusable_task(
                [{"task_id": "a", "project_id": "project", "original_blob_sha256": "other"}],
                project_id="project",
                digest="digest",
            )
        )

    def test_payload_preserves_utf8_source_bytes(self) -> None:
        raw = "# Work Order\n\nWeb3 — specialization".encode("utf-8")
        payload = hp.build_task_payload(raw, title="WO")
        self.assertEqual(payload["format"], "markdown")
        self.assertEqual(payload["text"].encode("utf-8"), raw)

    def test_prepare_rejects_stale_inspected_head(self) -> None:
        responses = {
            ("GET", "/api/v1/health"): {"status": "ok"},
            ("GET", "/api/v1/projects"): [
                {"project_id": "p1", "name": "NEXLABS-WEB", "relative_path": "nexlabs-web"}
            ],
            ("POST", "/api/v1/projects/p1/inspect"): {
                "project_id": "p1",
                "name": "NEXLABS-WEB",
                "relative_path": "nexlabs-web",
                "state": "READY",
                "git_head_sha": "old",
                "working_tree_clean": True,
            },
        }

        def fake_request(_base: str, method: str, path: str, payload=None):
            return responses[(method, path)]

        with (
            patch("scripts.hive_prepare.resolve_git_state", return_value={"branch": "main", "head": "new", "working_tree_clean": True}),
            patch("scripts.hive_prepare.resolve_work_order", return_value=".engineering/work-orders/WO.md"),
            patch("scripts.hive_prepare.work_order_bytes", return_value=(Path("WO.md"), b"work")),
            patch("scripts.hive_prepare.request", side_effect=fake_request),
        ):
            with self.assertRaisesRegex(hp.PreparationError, "does not match Git HEAD"):
                hp.prepare(base_url="http://hive", name="NEXLABS-WEB", relative_path="nexlabs-web", work_order=None)

    def test_prepare_creates_task_and_returns_bound_receipt(self) -> None:
        digest = hashlib.sha256(b"work").hexdigest()

        def fake_request(_base: str, method: str, path: str, payload=None):
            if (method, path) == ("GET", "/api/v1/health"):
                return {"status": "ok"}
            if (method, path) == ("GET", "/api/v1/projects"):
                return [{"project_id": "p1", "name": "NEXLABS-WEB", "relative_path": "nexlabs-web"}]
            if (method, path) == ("POST", "/api/v1/projects/p1/inspect"):
                return {
                    "project_id": "p1",
                    "name": "NEXLABS-WEB",
                    "relative_path": "nexlabs-web",
                    "state": "READY",
                    "git_head_sha": "head",
                    "working_tree_clean": True,
                }
            if (method, path) == ("POST", "/api/v1/projects/p1/index"):
                return {"status": "COMPLETED"}
            if (method, path) == ("POST", "/api/v1/projects/p1/retrieval/corpus/sync"):
                return {"status": "CURRENT"}
            if (method, path) == ("GET", "/api/v1/projects/p1/tasks?limit=200"):
                return []
            if (method, path) == ("POST", "/api/v1/projects/p1/tasks/text"):
                self.assertEqual(payload["format"], "markdown")
                return {
                    "task_id": "t1",
                    "project_id": "p1",
                    "original_blob_sha256": digest,
                    "intake_status": "READY",
                    "extracted_text_available": True,
                }
            raise AssertionError((method, path))

        with (
            patch("scripts.hive_prepare.resolve_git_state", return_value={"branch": "main", "head": "head", "working_tree_clean": True}),
            patch("scripts.hive_prepare.resolve_work_order", return_value=".engineering/work-orders/NXWEB-WO-0002.md"),
            patch("scripts.hive_prepare.work_order_bytes", return_value=(Path("NXWEB-WO-0002.md"), b"work")),
            patch("scripts.hive_prepare.request", side_effect=fake_request),
        ):
            receipt = hp.prepare(
                base_url="http://hive",
                name="NEXLABS-WEB",
                relative_path="nexlabs-web",
                work_order=None,
            )

        self.assertEqual(receipt["project_id"], "p1")
        self.assertEqual(receipt["task_id"], "t1")
        self.assertEqual(receipt["work_order_id"], "NXWEB-WO-0002")
        self.assertEqual(receipt["git_head_sha"], "head")
        self.assertEqual(receipt["index_status"], "COMPLETED")
        self.assertEqual(receipt["corpus_status"], "CURRENT")
        self.assertEqual(receipt["hive_version_expected"], "1.0.0")
        self.assertNotIn(str(Path.cwd()), json.dumps(receipt))

    def test_task_creation_failure_blocks_preparation(self) -> None:
        digest = hashlib.sha256(b"work").hexdigest()

        def fake_request(_base: str, method: str, path: str, payload=None):
            if (method, path) == ("GET", "/api/v1/health"):
                return {"status": "ok"}
            if (method, path) == ("GET", "/api/v1/projects"):
                return [{"project_id": "p1", "name": "NEXLABS-WEB", "relative_path": "nexlabs-web"}]
            if (method, path) == ("POST", "/api/v1/projects/p1/inspect"):
                return {
                    "name": "NEXLABS-WEB",
                    "relative_path": "nexlabs-web",
                    "state": "READY",
                    "git_head_sha": "head",
                    "working_tree_clean": True,
                }
            if (method, path) == ("POST", "/api/v1/projects/p1/index"):
                return {"status": "COMPLETED"}
            if (method, path) == ("POST", "/api/v1/projects/p1/retrieval/corpus/sync"):
                return {"status": "CURRENT"}
            if (method, path) == ("GET", "/api/v1/projects/p1/tasks?limit=200"):
                return []
            if (method, path) == ("POST", "/api/v1/projects/p1/tasks/text"):
                return {
                    "task_id": "t1",
                    "project_id": "p1",
                    "original_blob_sha256": digest,
                    "intake_status": "EXTRACTION_FAILED",
                    "extracted_text_available": False,
                }
            raise AssertionError((method, path))

        with (
            patch("scripts.hive_prepare.resolve_git_state", return_value={"branch": "main", "head": "head", "working_tree_clean": True}),
            patch("scripts.hive_prepare.resolve_work_order", return_value=".engineering/work-orders/WO.md"),
            patch("scripts.hive_prepare.work_order_bytes", return_value=(Path("WO.md"), b"work")),
            patch("scripts.hive_prepare.request", side_effect=fake_request),
        ):
            with self.assertRaisesRegex(hp.PreparationError, "not READY"):
                hp.prepare(base_url="http://hive", name="NEXLABS-WEB", relative_path="nexlabs-web", work_order=None)


if __name__ == "__main__":
    unittest.main()
