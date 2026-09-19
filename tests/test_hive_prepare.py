import hashlib
import unittest

from scripts.hive_prepare import build_task_payload, select_reusable_task, source_digest


class HivePrepareTests(unittest.TestCase):
    def test_source_digest_matches_exact_bytes(self) -> None:
        raw = b"# Work Order\r\n"
        self.assertEqual(source_digest(raw), hashlib.sha256(raw).hexdigest())

    def test_reuses_the_deterministic_task_for_matching_digest(self) -> None:
        tasks = [
            {"task_id": "b", "original_blob_sha256": "digest"},
            {"task_id": "a", "original_blob_sha256": "digest"},
            {"task_id": "c", "original_blob_sha256": "other"},
        ]
        self.assertEqual(select_reusable_task(tasks, "digest"), tasks[1])

    def test_non_matching_digest_does_not_reuse_task(self) -> None:
        self.assertIsNone(select_reusable_task([], "digest"))
        self.assertIsNone(select_reusable_task([{"task_id": "a", "original_blob_sha256": "other"}], "digest"))

    def test_payload_preserves_utf8_source_bytes(self) -> None:
        raw = "# Work Order\n\nWeb3 — specialization".encode("utf-8")
        payload = build_task_payload(raw, title="WO")
        self.assertEqual(payload["format"], "markdown")
        self.assertEqual(payload["text"].encode("utf-8"), raw)


if __name__ == "__main__":
    unittest.main()
