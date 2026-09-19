from __future__ import annotations

import unittest

from scripts.hive_bootstrap import resolve_registered_project


class HiveProjectResolutionTests(unittest.TestCase):
    def test_exact_relative_path_wins(self) -> None:
        projects = [{"project_id": "wrong", "name": "NEXLABS-WEB", "relative_path": "archive/web"}, {"project_id": "right", "name": "Renamed", "relative_path": "nexlabs-web"}]
        result = resolve_registered_project(projects, name="NEXLABS-WEB", relative_path="nexlabs-web")
        self.assertEqual(result["project_id"], "right")

    def test_same_name_different_path_fails_closed(self) -> None:
        projects = [{"project_id": "other", "name": "NEXLABS-WEB", "relative_path": "other/web"}]
        with self.assertRaisesRegex(RuntimeError, "different path"):
            resolve_registered_project(projects, name="NEXLABS-WEB", relative_path="nexlabs-web")

    def test_missing_project_returns_none(self) -> None:
        self.assertIsNone(resolve_registered_project([], name="NEXLABS-WEB", relative_path="nexlabs-web"))
