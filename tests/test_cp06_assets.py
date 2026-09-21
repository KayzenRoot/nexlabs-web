from __future__ import annotations

import unittest
from pathlib import Path

from scripts.cp06.check_blender_transport import parse_port
from scripts.cp06.validate_assets import validate


ROOT = Path(__file__).resolve().parents[1]


class Cp06TransportTests(unittest.TestCase):
    def test_default_port(self) -> None:
        self.assertEqual(parse_port(None), 9876)

    def test_explicit_port(self) -> None:
        self.assertEqual(parse_port("9877"), 9877)

    def test_rejects_invalid_port(self) -> None:
        with self.assertRaises(ValueError):
            parse_port("70000")


class Cp06FrozenAssetTests(unittest.TestCase):
    def test_frozen_package_and_acceptance_receipt(self) -> None:
        report = validate(
            ROOT / "artifacts/cp06/cp06-asset-manifest.json",
            ROOT / "artifacts/cp06/cp06-asset-acceptance.json",
        )
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(len(report["assets"]), 7)
        self.assertEqual(
            [report["gates"][f"G{i}"] for i in range(1, 11)],
            ["PASS"] * 10,
        )


if __name__ == "__main__":
    unittest.main()
