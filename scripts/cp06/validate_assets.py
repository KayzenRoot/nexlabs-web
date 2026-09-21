"""Validate CP-06 machine-readable asset and gate receipts."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def fail(message: str) -> None:
    raise SystemExit(f"CP06 ASSET VALIDATION FAILED: {message}")


def read(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"JSON root is not an object: {path}")
    return value


def check_file(relative: str, expected_hash: str) -> dict[str, object]:
    path = ROOT / relative
    if not path.is_file() or path.stat().st_size == 0:
        fail(f"missing or empty asset: {relative}")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected_hash:
        fail(f"hash mismatch for {relative}")
    return {"path": relative, "bytes": path.stat().st_size, "sha256": actual}


def validate(
    manifest_path: Path,
    acceptance_path: Path | None = None,
) -> dict[str, object]:
    manifest = read(manifest_path)
    if manifest.get("status") != "PASS":
        fail("manifest status is not PASS")
    if manifest.get("sceneId") != "NL-SCENE-CONTEXT-CORE-01":
        fail("scene identity mismatch")
    if manifest.get("selectedLogo", {}).get("candidateId") != "NX-C-02":
        fail("selected logo is not NX-C-02")
    if manifest.get("outOfScope", {}).get("runtimeThree") is not False or manifest.get("outOfScope", {}).get("ugasGeneration") is not False:
        fail("forbidden scope is claimed")
    gates = manifest.get("gates", {})
    if [gates.get(f"G{i}") for i in range(1, 11)] != ["PASS"] * 10:
        fail("G1-G10 are not all PASS")

    acceptance_path = acceptance_path or (ROOT / "artifacts/cp06/cp06-asset-acceptance.json")
    acceptance = read(acceptance_path)
    if acceptance.get("status") != "READY_FOR_INDEPENDENT_REVIEW":
        fail("asset acceptance is not READY_FOR_INDEPENDENT_REVIEW")
    if acceptance.get("sourceRevision") != manifest.get("sourceRevision"):
        fail("asset acceptance source revision mismatch")
    if acceptance.get("sceneId") != manifest.get("sceneId"):
        fail("asset acceptance scene identity mismatch")
    if acceptance.get("selectedLogo", {}).get("sha256") != manifest.get("selectedLogo", {}).get("sourceSha256"):
        fail("asset acceptance selected-logo hash mismatch")
    acceptance_gates = acceptance.get("gates", {})
    if [acceptance_gates.get(f"G{i}") for i in range(1, 11)] != ["PASS"] * 10:
        fail("asset acceptance G1-G10 are not all PASS")
    required_receipts = {"SSAC", "PFR", "LIPG", "EBL", "glbInspection"}
    receipts = acceptance.get("receipts", {})
    if any(receipts.get(name) != "PASS" for name in required_receipts):
        fail("asset acceptance required receipts are not all PASS")
    if acceptance.get("independentReview", {}).get("status") != "PENDING":
        fail("pre-review acceptance must not claim independent approval")
    boundaries = acceptance.get("boundaries", {})
    for forbidden in ("runtimeThree", "brandMarkChange", "ugasGeneration", "cp07", "deployment"):
        if boundaries.get(forbidden) is not False:
            fail(f"asset acceptance boundary {forbidden} must remain false")

    assets = []
    for tier in ("HIGH", "MED", "LOW"):
        record = manifest.get("exports", {}).get(tier, {})
        acceptance_record = acceptance.get("exports", {}).get(tier, {})
        if acceptance_record.get("path") != record.get("path") or acceptance_record.get("sha256") != record.get("sha256"):
            fail(f"asset acceptance {tier} binding mismatch")
        assets.append(check_file(record.get("path", ""), record.get("sha256", "")))
    for name, record in manifest.get("staticFallback", {}).items():
        acceptance_record = acceptance.get("staticFallback", {}).get(name, {})
        if acceptance_record.get("path") != record.get("path") or acceptance_record.get("sha256") != record.get("sha256"):
            fail(f"asset acceptance static fallback binding mismatch: {name}")
        assets.append(check_file(record.get("path", ""), record.get("sha256", "")))

    return {
        "status": "PASS",
        "manifest": str(manifest_path.relative_to(ROOT)),
        "acceptance": str(acceptance_path.relative_to(ROOT)),
        "assets": assets,
        "gates": gates,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="artifacts/cp06/cp06-asset-manifest.json")
    args = parser.parse_args()
    report = validate(ROOT / args.manifest)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
