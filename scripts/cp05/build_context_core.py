"""Deterministic CP-05 Context Core builder for Blender 5.2+.

Run from the repository root with Blender:
  blender.exe --background --python scripts/cp05/build_context_core.py -- --repo-root .
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import sys
from pathlib import Path

import bpy
from mathutils import Vector


PRIMITIVE_TYPES = ("CORE", "SHELL", "ROUTE", "NODE", "LATTICE", "CELL", "BAND", "FRAGMENT", "GATE", "FIELD")
MATERIAL_FAMILIES = (
    ("Mineral", (0.025, 0.035, 0.05, 1.0), 0.58, 0.0, "Dark structural body"),
    ("Ceramic", (0.23, 0.28, 0.34, 1.0), 0.28, 0.0, "Precision surface"),
    ("Optical", (0.08, 0.14, 0.2, 1.0), 0.18, 0.0, "Selective structural transparency"),
    ("Signal_Cyan", (0.02, 0.52, 0.82, 1.0), 0.24, 3.5, "Primary system signal"),
    ("Signal_Violet", (0.34, 0.12, 0.72, 1.0), 0.3, 2.8, "Secondary system signal"),
    ("Signal_Warm", (0.86, 0.29, 0.08, 1.0), 0.36, 1.8, "Rare state accent"),
    ("Data", (0.1, 0.64, 0.72, 1.0), 0.42, 1.4, "Instanced data matter"),
)


def repo_root() -> Path:
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    for index, value in enumerate(args):
        if value == "--repo-root" and index + 1 < len(args):
            return Path(args[index + 1]).resolve()
    return Path.cwd().resolve()


ROOT = repo_root()
ARTIFACTS = ROOT / "artifacts" / "cp05"
LOCAL = ROOT / ".local" / "cp05"
PARAMETERS_PATH = ROOT / "scripts" / "cp05" / "parameters.json"


def load_parameters() -> dict:
    return json.loads(PARAMETERS_PATH.read_text(encoding="utf-8"))


def link_to(obj: bpy.types.Object, collection: bpy.types.Collection) -> None:
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    collection.objects.link(obj)


def collection(name: str, parent: bpy.types.Collection) -> bpy.types.Collection:
    value = bpy.data.collections.new(name)
    parent.children.link(value)
    return value


def material(name: str, color: tuple[float, float, float, float], roughness: float, emission: float, family: str) -> bpy.types.Material:
    value = bpy.data.materials.new(f"NL_MAT_{name}_A")
    value.use_nodes = True
    value["family"] = name
    value["description"] = family
    value["web_approximation"] = "Principled BSDF with bounded color/emission; no runtime dependency"
    nodes = value.node_tree.nodes
    shader = next(node for node in nodes if node.type == "BSDF_PRINCIPLED")
    shader.inputs["Base Color"].default_value = color
    shader.inputs["Roughness"].default_value = roughness
    if "Metallic" in shader.inputs:
        shader.inputs["Metallic"].default_value = 0.18 if name == "Mineral" else 0.0
    if "Emission Color" in shader.inputs:
        shader.inputs["Emission Color"].default_value = color
    elif "Emission" in shader.inputs:
        shader.inputs["Emission"].default_value = color
    if "Emission Strength" in shader.inputs:
        shader.inputs["Emission Strength"].default_value = emission
    if name == "Optical":
        value.surface_render_method = "DITHERED"
        if "Alpha" in shader.inputs:
            shader.inputs["Alpha"].default_value = 0.42
    return value


def assign(obj: bpy.types.Object, mat: bpy.types.Material) -> None:
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def tag(obj: bpy.types.Object, primitive: str, parameters: dict, seed: int | None = None) -> None:
    obj["cp05_primitive"] = primitive
    obj["cp05_parameters"] = json.dumps(parameters, sort_keys=True, separators=(",", ":"))
    if seed is not None:
        obj["cp05_seed"] = seed


def curve_object(name: str, points: list[tuple[float, float, float]], bevel: float, mat: bpy.types.Material, target: bpy.types.Collection) -> bpy.types.Object:
    data = bpy.data.curves.new(name, type="CURVE")
    data.dimensions = "3D"
    data.bevel_depth = bevel
    data.bevel_resolution = 3
    spline = data.splines.new("BEZIER")
    spline.bezier_points.add(len(points) - 1)
    for point, coordinate in zip(spline.bezier_points, points):
        point.co = coordinate
        point.handle_left_type = "AUTO"
        point.handle_right_type = "AUTO"
    obj = bpy.data.objects.new(name, data)
    target.objects.link(obj)
    assign(obj, mat)
    return obj


def add_cube(name: str, location: tuple[float, float, float], scale: tuple[float, float, float], mat: bpy.types.Material, target: bpy.types.Collection) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bevel = obj.modifiers.new("NL_Bevel", "BEVEL")
    bevel.width = min(scale) * 0.22
    bevel.segments = 3
    link_to(obj, target)
    assign(obj, mat)
    return obj


def add_ico(name: str, location: tuple[float, float, float], radius: float, mat: bpy.types.Material, target: bpy.types.Collection, subdivisions: int = 2) -> bpy.types.Object:
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, radius=radius, location=location)
    obj = bpy.context.object
    obj.name = name
    link_to(obj, target)
    assign(obj, mat)
    return obj


def look_at(obj: bpy.types.Object, target: tuple[float, float, float]) -> None:
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def rounded(values: tuple[float, ...]) -> list[float]:
    return [round(float(value), 5) for value in values]


def object_record(obj: bpy.types.Object) -> dict:
    return {
        "name": obj.name,
        "type": obj.type,
        "primitive": obj.get("cp05_primitive"),
        "location": rounded(obj.location),
        "rotation": rounded(obj.rotation_euler),
        "scale": rounded(obj.scale),
        "dimensions": rounded(obj.dimensions),
        "seed": obj.get("cp05_seed"),
    }


def fingerprint(payload: dict) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build() -> None:
    parameters = load_parameters()
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    LOCAL.mkdir(parents=True, exist_ok=True)
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for datablocks in (bpy.data.collections, bpy.data.curves, bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for datablock in list(datablocks):
            if datablock.users == 0:
                datablocks.remove(datablock)

    scene = bpy.context.scene
    scene.name = parameters["scene_id"]
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"
    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except TypeError:
        scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = parameters["render"]["width"]
    scene.render.resolution_y = parameters["render"]["height"]
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.color_depth = "8"
    scene.render.fps = 24
    scene.world.color = (0.004, 0.006, 0.012)
    scene["cp05_scene_id"] = parameters["scene_id"]
    scene["cp05_seed"] = parameters["seed"]
    scene["cp05_scope"] = "WO-B3D-001..006; static foundation only"

    root = collection("NL_CONTEXT_CORE", scene.collection)
    groups = {name: collection(name, root) for name in ("CORE", "SHELLS", "ROUTES", "NODES", "DATA", "LIGHTS", "CAMERAS", "HELPERS", "EXPORT", "RENDER_ONLY")}
    mats = {name: material(name, color, roughness, emission, family) for name, color, roughness, emission, family in MATERIAL_FAMILIES}

    core = add_ico("NL_CORE_Context_A", (0.0, 0.0, 0.2), 0.82, mats["Ceramic"], groups["CORE"], 3)
    tag(core, "CORE", {"radius": 0.82, "state": "resolved"})
    bpy.ops.mesh.primitive_torus_add(major_radius=1.22, minor_radius=0.055, major_segments=64, minor_segments=12, location=(0, 0, 0.2), rotation=(math.radians(68), 0, math.radians(18)))
    shell = bpy.context.object
    shell.name = "NL_SHELL_Context_A"
    link_to(shell, groups["SHELLS"])
    assign(shell, mats["Mineral"])
    tag(shell, "SHELL", {"major_radius": 1.22, "minor_radius": 0.055, "layer": 1})
    bpy.ops.mesh.primitive_torus_add(major_radius=1.65, minor_radius=0.035, major_segments=64, minor_segments=10, location=(0, 0, 0.2), rotation=(math.radians(22), math.radians(52), 0))
    shell2 = bpy.context.object
    shell2.name = "NL_SHELL_Context_B"
    link_to(shell2, groups["SHELLS"])
    assign(shell2, mats["Optical"])
    tag(shell2, "SHELL", {"major_radius": 1.65, "minor_radius": 0.035, "layer": 2})

    route_points = [(0.0, 0.0, 0.24), (0.7, -0.5, 0.6), (1.9, -1.2, 0.9), (3.4, -1.6, 1.0)]
    route = curve_object("NL_ROUTE_Primary_01", route_points, 0.035, mats["Signal_Cyan"], groups["ROUTES"])
    tag(route, "ROUTE", {"bevel": 0.035, "points": route_points}, parameters["route_seed"])
    for index in range(parameters["route_count"]):
        angle = (2 * math.pi * index) / parameters["route_count"]
        end = (3.1 * math.cos(angle), 3.1 * math.sin(angle), 0.35 + 0.3 * math.sin(angle * 2))
        points = [(0.0, 0.0, 0.3), (0.8 * math.cos(angle + 0.35), 0.8 * math.sin(angle + 0.35), 0.8), (1.8 * math.cos(angle), 1.8 * math.sin(angle), 0.5), end]
        obj = curve_object(f"NL_ROUTE_Field_{index + 1:02d}", points, 0.018, mats["Signal_Violet" if index % 2 else "Signal_Cyan"], groups["ROUTES"])
        tag(obj, "ROUTE", {"bevel": 0.018, "index": index}, parameters["route_seed"] + index)

    for index in range(parameters["node_count"]):
        angle = 2 * math.pi * index / parameters["node_count"]
        radius = 1.65 + 0.12 * (index % 3)
        obj = add_ico(f"NL_NODE_Anchor_{index + 1:02d}", (radius * math.cos(angle), radius * math.sin(angle), 0.24 + 0.35 * math.sin(angle)), 0.085, mats["Data"], groups["NODES"], 2)
        tag(obj, "NODE", {"radius": radius, "index": index}, parameters["data_seed"] + index)

    lattice = add_cube("NL_LATTICE_Context_A", (0.0, 0.0, 0.25), (2.05, 0.025, 0.025), mats["Mineral"], groups["HELPERS"])
    tag(lattice, "LATTICE", {"span": 4.1, "thickness": 0.05})
    lattice.rotation_euler[2] = math.radians(45)
    cell = add_cube("NL_CELL_Module_A", (0.0, 0.0, 0.22), (0.48, 0.48, 0.1), mats["Ceramic"], groups["CORE"])
    tag(cell, "CELL", {"width": 0.96, "depth": 0.96})
    band = curve_object("NL_BAND_Stream_A", [(-2.2, -1.0, 0.0), (-0.8, -1.65, 0.1), (0.8, -1.65, 0.1), (2.2, -1.0, 0.0)], 0.07, mats["Signal_Warm"], groups["ROUTES"])
    tag(band, "BAND", {"bevel": 0.07, "state": "rare_accent"})
    fragment = add_ico("NL_FRAGMENT_Data_A", (2.3, 1.2, 1.0), 0.16, mats["Data"], groups["DATA"], 1)
    tag(fragment, "FRAGMENT", {"radius": 0.16, "prototype": True}, parameters["data_seed"])
    gate = add_cube("NL_GATE_Transition_A", (-1.55, 0.35, 0.75), (0.08, 0.5, 0.75), mats["Mineral"], groups["CORE"])
    tag(gate, "GATE", {"height": 1.5, "width": 0.16})
    field = add_cube("NL_FIELD_Outer_A", (0.0, 0.0, -0.25), (4.4, 4.4, 0.03), mats["Mineral"], groups["RENDER_ONLY"])
    tag(field, "FIELD", {"extent": 8.8, "density_control": 0.32})

    rng = random.Random(parameters["data_seed"])
    for index in range(parameters["fragment_count"]):
        angle = rng.random() * math.tau
        radius = 2.35 + rng.random() * 1.65
        position = (radius * math.cos(angle), radius * math.sin(angle), 0.15 + rng.uniform(-0.45, 1.25))
        obj = add_ico(f"NL_DATA_Fragment_{index + 1:03d}", position, 0.035 + rng.random() * 0.045, mats["Data"], groups["DATA"], 1)
        tag(obj, "FRAGMENT", {"radius_min": 0.035, "radius_max": 0.08, "distribution_radius": [2.35, 4.0]}, parameters["data_seed"] + index)

    cameras = {}
    for name, location, lens in (
        ("NL_CAM_Hero_A", (7.4, -7.4, 5.2), 52),
        ("NL_CAM_Projection_A", (0.0, -9.0, 2.7), 58),
        ("NL_CAM_Macro_A", (3.5, -3.7, 2.4), 72),
        ("NL_CAM_Review_A", (9.0, 0.0, 6.8), 50),
    ):
        camera_data = bpy.data.cameras.new(name)
        camera_data.lens = lens
        camera_data.sensor_width = 36
        obj = bpy.data.objects.new(name, camera_data)
        groups["CAMERAS"].objects.link(obj)
        obj.location = location
        look_at(obj, (0.0, 0.0, 0.3))
        cameras[name] = obj
        tag(obj, "CAMERA", {"lens": lens, "target": [0.0, 0.0, 0.3]})
    scene.camera = cameras["NL_CAM_Hero_A"]

    for name, location, energy, size, color in (
        ("NL_LIGHT_Key_Sculpt", (4.5, -4.0, 6.5), 950, 4.0, (0.72, 0.84, 1.0)),
        ("NL_LIGHT_Rim_Structure", (-4.0, 2.5, 4.8), 1100, 3.0, (0.36, 0.52, 1.0)),
        ("NL_LIGHT_Environment", (0.0, 0.0, 7.0), 500, 5.0, (0.25, 0.31, 0.42)),
        ("NL_LIGHT_Signal_Emission", (0.0, 0.0, 2.5), 140, 2.0, (0.1, 0.55, 0.9)),
    ):
        data = bpy.data.lights.new(name, type="AREA")
        data.energy = energy
        data.shape = "DISK"
        data.size = size
        data.color = color
        obj = bpy.data.objects.new(name, data)
        groups["LIGHTS"].objects.link(obj)
        obj.location = location
        look_at(obj, (0.0, 0.0, 0.3))
        tag(obj, "LIGHT", {"energy": energy, "size": size})

    primitive_objects = [obj for obj in bpy.data.objects if obj.get("cp05_primitive") in PRIMITIVE_TYPES]
    primitive_rows = [{"primitive": name, "objectCount": sum(1 for obj in primitive_objects if obj.get("cp05_primitive") == name)} for name in PRIMITIVE_TYPES]
    material_rows = [{"name": mat.name, "family": mat.get("family"), "webApproximation": mat.get("web_approximation")} for mat in sorted(mats.values(), key=lambda item: item.name)]
    scene_payload = {
        "sceneId": parameters["scene_id"],
        "blenderVersion": bpy.app.version_string,
        "seed": parameters["seed"],
        "collections": sorted(collection.name for collection in bpy.data.collections if collection.name.startswith("NL_")),
        "objects": sorted((object_record(obj) for obj in bpy.data.objects if obj.get("cp05_primitive") or obj.type in {"CAMERA", "LIGHT"}), key=lambda item: item["name"]),
        "primitiveSummary": primitive_rows,
        "materialSummary": material_rows,
        "cameras": sorted(name for name in cameras),
        "lights": sorted(obj.name for obj in bpy.data.objects if obj.type == "LIGHT"),
        "complexity": {"objectCount": len(bpy.data.objects), "meshCount": len(bpy.data.meshes), "materialCount": len(mats), "fragmentCount": parameters["fragment_count"], "nodeCount": parameters["node_count"], "routeCount": parameters["route_count"]},
    }
    scene_payload["sceneFingerprint"] = fingerprint(scene_payload)
    blend_path = LOCAL / "context_core_master.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))

    render_dir = ARTIFACTS / "renders"
    render_dir.mkdir(parents=True, exist_ok=True)
    scene.render.filepath = str(render_dir / "context-core-neutral.png")
    signal_materials = [mats[name] for name in ("Signal_Cyan", "Signal_Violet", "Signal_Warm", "Data")]
    saved_colors = []
    for mat in signal_materials:
        shader = next(node for node in mat.node_tree.nodes if node.type == "BSDF_PRINCIPLED")
        saved_colors.append((mat, shader.inputs["Base Color"].default_value[:], shader.inputs.get("Emission Strength").default_value if shader.inputs.get("Emission Strength") else 0.0))
        shader.inputs["Base Color"].default_value = (0.18, 0.2, 0.24, 1.0)
        if shader.inputs.get("Emission Strength"):
            shader.inputs["Emission Strength"].default_value = 0.0
    bpy.ops.render.render(write_still=True)
    for mat, color, emission in saved_colors:
        shader = next(node for node in mat.node_tree.nodes if node.type == "BSDF_PRINCIPLED")
        shader.inputs["Base Color"].default_value = color
        if shader.inputs.get("Emission Strength"):
            shader.inputs["Emission Strength"].default_value = emission
    scene.camera = cameras["NL_CAM_Hero_A"]
    scene.render.filepath = str(render_dir / "context-core-branded.png")
    bpy.ops.render.render(write_still=True)
    scene.camera = cameras["NL_CAM_Macro_A"]
    scene.render.filepath = str(render_dir / "context-core-macro.png")
    bpy.ops.render.render(write_still=True)
    scene.camera = cameras["NL_CAM_Hero_A"]
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))

    blend_hash = hashlib.sha256(blend_path.read_bytes()).hexdigest()
    write_json(ARTIFACTS / "scene-manifest.json", {"schemaVersion": "nexlabs-web-cp05-scene-manifest-v1", "sceneId": parameters["scene_id"], "scope": "WO-B3D-001..006", "builder": "scripts/cp05/build_context_core.py", "masterBlend": {"path": ".local/cp05/context_core_master.blend", "role": "local ignored Blender master", "bytes": blend_path.stat().st_size, "sha256": blend_hash}, "scene": scene_payload, "renders": [{"path": f"artifacts/cp05/renders/{name}", "role": role} for name, role in (("context-core-neutral.png", "monochrome material-neutral pass"), ("context-core-branded.png", "restrained Dark Mineral Laboratory pass"), ("context-core-macro.png", "macro material/detail pass"))]})
    write_json(ARTIFACTS / "primitive-manifest.json", {"schemaVersion": "nexlabs-web-cp05-primitives-v1", "sceneId": parameters["scene_id"], "seed": parameters["seed"], "primitives": primitive_rows, "objects": sorted((object_record(obj) for obj in primitive_objects), key=lambda item: item["name"])})
    write_json(ARTIFACTS / "material-manifest.json", {"schemaVersion": "nexlabs-web-cp05-materials-v1", "families": material_rows, "webBoundary": "No runtime 3D or Three.js/R3F is introduced by CP-05."})
    write_json(ARTIFACTS / "provenance.json", {"schemaVersion": "nexlabs-web-cp05-provenance-v1", "assetId": "NL_CONTEXT_CORE_CP05", "version": "v001", "status": "CANDIDATE", "purpose": "Deterministic Blender Context Core foundation source and review evidence", "source": {"type": "procedural", "references": ["scripts/cp05/build_context_core.py", "scripts/cp05/parameters.json", "BR-05-3D-LANGUAGE.md", "BR-11-CONTEXT-CORE-WORK-ORDERS.md"]}, "blender": {"sourceFile": ".local/cp05/context_core_master.blend", "sceneFingerprint": scene_payload["sceneFingerprint"]}, "planning": {"BR05BlobSha": "d1144daeeb6193249c354198baaadc39fc322231", "BR11BlobSha": "1593b20ffccd8b4af4f39c2cd38a1a690fb221ce", "BR12SchemaBlobSha": "6feebc0df320d0194abd305cc6e3659d17553542"}, "selectedLogoDependency": {"candidateId": "NX-C-02", "revision": "r1", "sha256": "16daeac469520dbae6ba224dbd87bc8f07510c734940d35412248f32d2364165", "metadataOnly": True}, "outputs": [{"path": f"artifacts/cp05/renders/{name}", "format": "png", "sha256": hashlib.sha256((render_dir / name).read_bytes()).hexdigest()} for name in ("context-core-neutral.png", "context-core-branded.png", "context-core-macro.png")], "ugas": {"providerStarted": False, "generationAuthorized": False, "notes": "UGAS V1 remains outside this CP-05 production scope."}, "approval": None})
    print(json.dumps({"status": "PASS", "sceneFingerprint": scene_payload["sceneFingerprint"], "blend": ".local/cp05/context_core_master.blend", "primitiveCount": len(primitive_rows), "materialCount": len(material_rows), "fragmentCount": parameters["fragment_count"], "renderCount": 3}, sort_keys=True))


if __name__ == "__main__":
    build()
