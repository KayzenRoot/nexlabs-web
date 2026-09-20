"""Validate CP-05 manifests and the local Blender master without absolute-path evidence."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import bpy


def root() -> Path:
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    for index, value in enumerate(args):
        if value == "--repo-root" and index + 1 < len(args):
            return Path(args[index + 1]).resolve()
    return Path.cwd().resolve()


ROOT = root()
ARTIFACTS = ROOT / "artifacts" / "cp05"
LOCAL = ROOT / ".local" / "cp05"
EXPECTED_PRIMITIVES = {"CORE", "SHELL", "ROUTE", "NODE", "LATTICE", "CELL", "BAND", "FRAGMENT", "GATE", "FIELD"}
EXPECTED_MATERIALS = {"Mineral", "Ceramic", "Optical", "Signal_Cyan", "Signal_Violet", "Signal_Warm", "Data"}


def fail(message: str) -> None:
    raise SystemExit(f"CP05 VALIDATION FAILED: {message}")


def read_json(name: str) -> dict:
    try:
        value = json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid {name}: {exc}")
    if not isinstance(value, dict):
        fail(f"{name} root is not an object")
    return value


def main() -> None:
    scene_manifest = read_json("scene-manifest.json")
    primitive_manifest = read_json("primitive-manifest.json")
    material_manifest = read_json("material-manifest.json")
    provenance = read_json("provenance.json")
    if scene_manifest.get("sceneId") != "NL-SCENE-CONTEXT-CORE-01":
        fail("scene identity mismatch")
    if set(item.get("primitive") for item in primitive_manifest.get("primitives", [])) != EXPECTED_PRIMITIVES:
        fail("primitive coverage is not exactly the ten CP-05 primitives")
    material_families = {str(item.get("family")) for item in material_manifest.get("families", [])}
    if material_families != EXPECTED_MATERIALS:
        fail("material coverage is not exactly the seven CP-05 families")
    if provenance.get("status") != "CANDIDATE" or provenance.get("selectedLogoDependency", {}).get("metadataOnly") is not True:
        fail("provenance boundary is not candidate/metadata-only")
    blend_path = LOCAL / "context_core_master.blend"
    if not blend_path.is_file() or blend_path.stat().st_size < 1000:
        fail("local .blend master is missing or implausibly small")
    if scene_manifest.get("masterBlend", {}).get("sha256") != hashlib.sha256(blend_path.read_bytes()).hexdigest():
        fail("local .blend hash does not match scene manifest")
    required_objects = {"NL_CORE_Context_A", "NL_SHELL_Context_A", "NL_ROUTE_Primary_01", "NL_NODE_Anchor_01", "NL_LATTICE_Context_A", "NL_CELL_Module_A", "NL_BAND_Stream_A", "NL_FRAGMENT_Data_A", "NL_GATE_Transition_A", "NL_FIELD_Outer_A"}
    object_names = {obj.name for obj in bpy.data.objects}
    if not required_objects.issubset(object_names):
        fail(f"required source objects missing: {sorted(required_objects - object_names)}")
    if len([obj for obj in bpy.data.objects if obj.get("cp05_primitive") == "FRAGMENT"]) < 36:
        fail("deterministic fragment count is below the configured minimum")
    if len([obj for obj in bpy.data.objects if obj.type == "CAMERA"]) != 4:
        fail("camera foundation must contain four cameras")
    if len([obj for obj in bpy.data.objects if obj.type == "LIGHT"]) != 4:
        fail("lighting foundation must contain four lights")
    render_paths = [ROOT / item["path"] for item in scene_manifest.get("renders", [])]
    if len(render_paths) != 3 or any(not path.is_file() or path.stat().st_size < 1000 for path in render_paths):
        fail("review render package is incomplete")
    report = {"schemaVersion": "nexlabs-web-cp05-validation-v1", "status": "PASS", "sceneId": scene_manifest["sceneId"], "blendBytes": blend_path.stat().st_size, "blendSha256": hashlib.sha256(blend_path.read_bytes()).hexdigest(), "objects": len(bpy.data.objects), "materials": len(bpy.data.materials), "primitives": sorted(EXPECTED_PRIMITIVES), "materialFamilies": sorted(EXPECTED_MATERIALS), "cameras": 4, "lights": 4, "renders": [item["path"] for item in scene_manifest["renders"]], "boundaries": {"animation": False, "logoIntegration": False, "glbLodExport": False, "runtimeThree": False, "ugasGeneration": False, "cp06": False}}
    (ARTIFACTS / "validation-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
