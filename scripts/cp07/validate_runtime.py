"""Validate CP-07 promoted assets and static/runtime boundaries."""
from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "artifacts/cp07/cp07-runtime-manifest.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def glb_json(path: Path) -> dict:
    raw = path.read_bytes()
    if raw[:4] != b"glTF":
        raise AssertionError(f"not a GLB: {path}")
    chunk_length, chunk_type = struct.unpack_from("<II", raw, 12)
    if chunk_type != 0x4E4F534A:
        raise AssertionError(f"missing GLB JSON chunk: {path}")
    return json.loads(raw[20 : 20 + chunk_length].decode("utf-8"))


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["status"] == "PROMOTED_SOURCE_PACKAGE"
    assert manifest["semanticClips"] == ["DORMANT", "INTAKE", "INDEX", "RETRIEVE", "ASSEMBLE", "RESOLVE", "IDLE"]

    for tier, asset in manifest["assets"].items():
        promoted = ROOT / asset["path"]
        source = ROOT / asset["sourcePath"]
        assert promoted.is_file() and source.is_file(), tier
        assert promoted.stat().st_size == asset["bytes"], tier
        assert sha256(promoted) == asset["sourceSha256"], tier
        assert promoted.read_bytes() == source.read_bytes(), tier
        doc = glb_json(promoted)
        assert doc.get("asset", {}).get("version") == "2.0", tier
        assert not any("uri" in buffer for buffer in doc.get("buffers", [])), tier
        clip_names = {str(animation.get("name", "")) for animation in doc.get("animations", [])}
        suffix = "MED" if tier == "MEDIUM" else tier
        expected = {f"NL_ANIM_{name.title()}_{suffix}" for name in manifest["semanticClips"]}
        assert expected.issubset(clip_names), f"{tier} clips"

    for fallback in manifest["staticFallbacks"].values():
        promoted = ROOT / fallback["path"]
        source = ROOT / fallback["sourcePath"]
        assert promoted.is_file() and source.is_file()
        assert promoted.stat().st_size == fallback["bytes"]
        assert sha256(promoted) == fallback["sourceSha256"]
        assert promoted.read_bytes() == source.read_bytes()

    boundary = (ROOT / "components/three/ThreeBoundary.tsx").read_text(encoding="utf-8")
    assert "StaticContextCore" in boundary and "dynamic(" in boundary
    assert "ssr: false" in boundary and "IntersectionObserver" not in boundary
    for path in (ROOT / "app").rglob("*.tsx"):
        if path.name == "page.tsx" and path.parent == ROOT / "app":
            continue
        text = path.read_text(encoding="utf-8")
        assert "@react-three/fiber" not in text and 'from "three"' not in text, path

    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    assert package["dependencies"]["three"] == "0.181.2"
    assert package["dependencies"]["@react-three/fiber"] == "9.3.0"
    print("CP-07 runtime validation: PASS")
    print("Promoted assets: HIGH/MEDIUM/LOW + STATIC landscape/portrait/square")
    print("Static-first boundary: PASS")
    print("Clip parity and dependency isolation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
