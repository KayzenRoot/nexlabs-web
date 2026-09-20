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

    def test_final_closure_keeps_review_and_hive_lineage_typed(self):
        current = json.loads((ROOT / ".engineering/gef/GEF-CURRENT.json").read_text())
        lock = json.loads((ROOT / ".engineering/context-locks/NXWEB-LOCK-0004-CP05-BLENDER-CONTEXT-CORE-FOUNDATION.json").read_text())
        evidence = json.loads((ROOT / ".engineering/evidence/NXWEB-WO-0004-CP05-BLENDER-CONTEXT-CORE-FOUNDATION.json").read_text())
        self.assertEqual(current["productStage"], "CP05_COMPLETE")
        self.assertIsNone(current["activeWorkOrder"])
        self.assertEqual(lock["status"], "CLOSED")
        self.assertEqual(lock["candidateHead"], "de5a35db79521fca740f909982cc69ffd2033dc3")
        self.assertEqual(lock["reviewedCandidateHead"], "da97a702797078ff1de119065e4fc80e943d1984")
        self.assertEqual(lock["sceneMutationHead"], "da97a702797078ff1de119065e4fc80e943d1984")
        self.assertEqual(evidence["verdict"], "APPROVED")
        self.assertFalse(evidence["blender"]["preflight"]["sceneMutationBeforeGate"])
        self.assertTrue(evidence["blender"]["production"]["sceneMutationPerformed"])
        self.assertTrue(evidence["blender"]["production"]["mutationAfterPolicyAndMcpGate"])
        self.assertEqual(evidence["hosted"]["checks"]["status"], "PENDING_VERIFY_EXTERNALLY")


if __name__ == "__main__":
    unittest.main()
