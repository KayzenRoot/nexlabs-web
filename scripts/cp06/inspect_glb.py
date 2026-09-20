"""Small dependency-free GLB inspection receipt for CP-06 exports."""
from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path


def read_json_chunk(path: Path) -> dict:
    raw = path.read_bytes()
    if len(raw) < 20 or raw[:4] != b"glTF":
        raise ValueError("not a GLB file")
    version, length = struct.unpack_from("<II", raw, 4)
    if version != 2 or length != len(raw):
        raise ValueError("invalid GLB header")
    chunk_length, chunk_type = struct.unpack_from("<II", raw, 12)
    if chunk_type != 0x4E4F534A:
        raise ValueError("first GLB chunk is not JSON")
    return json.loads(raw[20 : 20 + chunk_length].decode("utf-8"))


def inspect(path: Path) -> dict[str, object]:
    doc = read_json_chunk(path)
    meshes = doc.get("meshes", [])
    accessors = doc.get("accessors", [])
    triangles = 0
    for mesh in meshes:
        for primitive in mesh.get("primitives", []):
            if "indices" in primitive:
                triangles += int(accessors[primitive["indices"]].get("count", 0)) // 3
            else:
                position = primitive.get("attributes", {}).get("POSITION")
                if position is not None:
                    triangles += int(accessors[position].get("count", 0)) // 3
    nodes = [str(node.get("name", "")) for node in doc.get("nodes", [])]
    animations = [str(animation.get("name", "")) for animation in doc.get("animations", [])]
    return {
        "status": "PASS",
        "path": str(path),
        "bytes": path.stat().st_size,
        "assetVersion": doc.get("asset", {}).get("version"),
        "nodes": len(nodes),
        "meshes": len(meshes),
        "materials": len(doc.get("materials", [])),
        "triangles": triangles,
        "animations": animations,
        "hasExternalBuffers": any("uri" in buffer for buffer in doc.get("buffers", [])),
        "nodeNames": nodes,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()
    print(json.dumps([inspect(Path(item)) for item in args.paths], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
