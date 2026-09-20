import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CP05BlenderContractTests(unittest.TestCase):
    def test_source_contract_is_present(self):
        self.assertTrue((ROOT / "scripts/cp05/build_context_core.py").is_file())
        self.assertTrue((ROOT / "scripts/cp05/validate_context_core.py").is_file())
        self.assertEqual(json.loads((ROOT / "scripts/cp05/parameters.json").read_text())["scene_id"], "NL-SCENE-CONTEXT-CORE-01")

    def test_scope_does_not_introduce_deferred_runtime_work(self):
        source = (ROOT / "scripts/cp05/build_context_core.py").read_text(encoding="utf-8")
        self.assertNotIn("bpy.ops.object.modifier_add(type='NODES')", source)
        self.assertNotIn("ugas.generate", source)

    def test_planning_cache_manifest_binds_cp05_sources(self):
        manifest = json.loads((ROOT / ".engineering/planning-snapshots/nexlabs-startup/b541e802472a3acc75a3a8ebd3818d33de8a316f/MANIFEST.json").read_text())
        paths = {entry["sourcePath"] for entry in manifest["files"]}
        self.assertIn("brand-web/BR-05-3D-LANGUAGE.md", paths)
        self.assertIn("brand-web/BR-11-CONTEXT-CORE-WORK-ORDERS.md", paths)


if __name__ == "__main__":
    unittest.main()
