import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "brand" / "logo" / "candidate-index.json"
EXPECTED = [
    "NX-D-01", "NX-D-02", "NX-D-03",
    "NX-C-01", "NX-C-02", "NX-C-03",
    "NX-B-01", "NX-B-02", "NX-B-03",
]


class LogoLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, "scripts/logo_lab.py"], cwd=ROOT, check=True)

    def test_exact_candidate_batch(self):
        data = json.loads(INDEX.read_text(encoding="utf-8"))
        self.assertEqual(data["candidateIds"], EXPECTED)
        self.assertEqual(len(data["candidates"]), 9)

    def test_masters_are_path_only_and_hash_bound(self):
        data = json.loads(INDEX.read_text(encoding="utf-8"))
        for item in data["candidates"]:
            raw = (ROOT / item["svg"]).read_bytes()
            self.assertEqual(__import__("hashlib").sha256(raw).hexdigest(), item["sha256"])
            source = raw.decode("utf-8")
            self.assertNotIn("<text", source)
            self.assertNotIn("<rect", source)
            self.assertNotIn("<circle", source)
            self.assertNotIn("Gradient", source)
            self.assertIn('viewBox="0 0 120 120"', source)
            self.assertIn("<path", source)

    def test_no_canonical_promotion_and_review_artifacts_exist(self):
        data = json.loads(INDEX.read_text(encoding="utf-8"))
        self.assertFalse(data["canonicalSelection"])
        self.assertFalse(data["runtimeWiring"])
        review = ROOT / "brand" / "logo" / "review"
        for name in ("contact-sheet.svg", "small-size.svg", "theme-lockups.svg", "website-context.svg", "blender-projection-blocked.svg", "blender-mcp-receipt.json"):
            self.assertTrue((review / name).is_file(), name)

    def test_artifact_manifest_is_hash_bound(self):
        manifest = json.loads((ROOT / "brand" / "logo" / "artifact-manifest.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(manifest["artifacts"]), 20)
        for artifact in manifest["artifacts"]:
            raw = (ROOT / artifact["path"]).read_bytes()
            self.assertEqual(__import__("hashlib").sha256(raw).hexdigest(), artifact["sha256"], artifact["path"])


if __name__ == "__main__":
    unittest.main()
