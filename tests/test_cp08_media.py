from __future__ import annotations

import json
import unittest

from scripts.cp08.validate_media import ROOT, validate_media


class CP08MediaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads((ROOT / "artifacts/cp08/cp08-asset-manifest.json").read_text(encoding="utf-8"))
        cls.report = validate_media()
        cls.records = {record["asset_id"]: record for record in cls.manifest["assets"]}

    def test_all_ten_quality_gates_pass(self) -> None:
        self.assertEqual(self.report["status"], "PASS")
        self.assertEqual([gate["id"] for gate in self.report["gates"]], [f"UG{number}" for number in range(1, 11)])
        self.assertTrue(all(gate["status"] == "PASS" for gate in self.report["gates"]))
        self.assertEqual(self.report["findings"], [])

    def test_assets_use_truthful_nonreleased_br12_records(self) -> None:
        self.assertEqual(len(self.records), 12)
        for record in self.records.values():
            self.assertIn(record["status"], {"PRODUCTION", "OPTIMIZED"})
            self.assertIsNone(record["ugas"]["workflow"])
            self.assertIsNone(record["ugas"]["workflow_version"])
            self.assertEqual(record["rights"]["external_inputs"], [])
            self.assertIsNone(record["approved_by"])
            self.assertIsNone(record["approved_at"])
            self.assertEqual(record["approval_status"], "NOT_INDEPENDENTLY_REVIEWED")

    def test_social_destinations_and_generic_template_are_distinct(self) -> None:
        self.assertEqual(self.records["NL_CP08_OG_DEFAULT"]["destinations"], ["/"])
        self.assertEqual(self.records["NL_CP08_OG_HIVE"]["destinations"], ["/hive"])
        self.assertEqual(self.records["NL_CP08_OG_TECHNOLOGY"]["destinations"], ["/technology"])
        self.assertEqual(self.records["NL_CP08_SOCIAL_GITHUB_REPOSITORY"]["destinations"], ["https://github.com/KayzenRoot/nexlabs-web"])
        self.assertEqual(self.records["NL_CP08_TEMPLATE_GENERIC_SOCIAL"]["destinations"], [])

    def test_source_framing_and_release_boundaries_are_preserved(self) -> None:
        self.assertEqual(self.manifest["releaseStatus"], "NOT_RELEASED")
        self.assertFalse(self.manifest["boundaries"]["ugasProviderStarted"])
        self.assertFalse(self.manifest["boundaries"]["ugasGenerationPerformed"])
        self.assertFalse(self.manifest["boundaries"]["deployed"])
        self.assertFalse(self.manifest["boundaries"]["cp09Started"])
        self.assertEqual(len(self.manifest["compression"]), 6)
        self.assertTrue(all(item["normalizedMeanAbsoluteErrorPercent"] <= 3 for item in self.manifest["compression"]))


if __name__ == "__main__":
    unittest.main()
