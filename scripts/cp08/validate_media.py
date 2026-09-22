"""Validate CP-08 derivative media, BR-12 provenance and UG1–UG10 gates."""
from __future__ import annotations

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Callable

from PIL import Image, ImageChops, ImageStat

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "artifacts/cp08/cp08-asset-manifest.json"
REPORT_JSON = ROOT / "artifacts/cp08/cp08-gate-report.json"
REPORT_MD = ROOT / "artifacts/cp08/cp08-gate-report.md"
BASE = "d971047d25dc01e7338aba369ea1bd7cf7452490"
MAX_PARITY_ERROR_PERCENT = 3.0
OG_OUTPUTS = {
    "NL_CP08_OG_DEFAULT": ("/", "public/release-visuals/og/nexlabs.png"),
    "NL_CP08_OG_HIVE": ("/hive", "public/release-visuals/og/hive.png"),
    "NL_CP08_OG_TECHNOLOGY": ("/technology", "public/release-visuals/og/technology.png"),
}
SOCIAL_ASSET = "NL_CP08_SOCIAL_GITHUB_REPOSITORY"
PLACEHOLDER_PATTERN = re.compile(r"\b(?:TODO|TBD|PLACEHOLDER|FAKE|EXAMPLE\.INVALID)\b|\{\{", re.IGNORECASE)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked_path(relative: str) -> Path:
    candidate = (ROOT / relative).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"path escapes repository: {relative}") from exc
    return candidate


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def add_gate(report: list[dict[str, Any]], gate_id: str, title: str, action: Callable[[], list[str]]) -> None:
    try:
        details = action()
        report.append({"id": gate_id, "title": title, "status": "PASS", "severity": "NONE", "evidence": details, "findings": []})
    except (AssertionError, OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        report.append({"id": gate_id, "title": title, "status": "FAIL", "severity": "HIGH", "evidence": [], "findings": [str(exc)]})


def validate_media() -> dict[str, Any]:
    manifest = load_json(MANIFEST_PATH)
    acceptance = load_json(ROOT / "artifacts/cp06/cp06-asset-acceptance.json")
    site = load_json(ROOT / "content/site/site.json")
    records = manifest.get("assets", [])
    by_id = {record.get("asset_id"): record for record in records}
    gates: list[dict[str, Any]] = []

    def brand() -> list[str]:
        tokens = load_json(ROOT / "public/brand/tokens.json")
        logo = checked_path("brand/logo/candidates/NX-C-02.svg")
        assert manifest.get("planningSource") == "KayzenRoot/nexlabs-startup@b541e802472a3acc75a3a8ebd3818d33de8a316f", "brand source revision mismatch"
        assert manifest.get("sourceInputs"), "source input ledger is empty"
        logo_ref = next(item for item in manifest["sourceInputs"] if item["path"] == "brand/logo/candidates/NX-C-02.svg")
        assert sha256(logo) == logo_ref["sha256"] == "16daeac469520dbae6ba224dbd87bc8f07510c734940d35412248f32d2364165", "selected NX-C-02 source hash mismatch"
        assert tokens["status"] == "provisional-engineering", "design token state changed without review"
        assert manifest["boundaries"]["identityChanged"] is False, "identity change is not admitted"
        return ["planning source pin verified", "canonical token source verified", "selected NX-C-02 bytes preserved"]

    def composition() -> list[str]:
        for asset_id, (route, path) in OG_OUTPUTS.items():
            output = by_id[asset_id]["outputs"][0]
            composition_info = by_id[asset_id]["composition"]
            assert output["path"] == path and (output["width"], output["height"]) == (1200, 630), f"{asset_id} destination/canvas mismatch"
            bounds = composition_info["textBounds"]
            margin = composition_info["safeMarginPx"]
            assert bounds["left"] >= margin and bounds["top"] >= margin, f"{asset_id} text crosses top/left safe margin"
            assert bounds["right"] <= output["width"] - margin and bounds["bottom"] <= output["height"] - margin, f"{asset_id} text crosses right/bottom safe margin"
            image_x, image_y, image_w, image_h = composition_info["sourceImageBox"]
            assert image_x + image_w <= output["width"] - margin and image_y + image_h <= output["height"] - margin, f"{asset_id} art crosses safe margin"
            assert bounds["right"] < image_x, f"{asset_id} text and artwork overlap"
            assert composition_info["titleLineCount"] <= 2 and composition_info["descriptionLineCount"] <= 4, f"{asset_id} copy is too dense"
        social = by_id[SOCIAL_ASSET]["outputs"][0]
        assert (social["width"], social["height"]) == (1280, 640), "GitHub social preview dimensions mismatch"
        return ["all OG cards use 1200x630 with conservative safe areas", "repository preview uses 1280x640", "text and illustration zones do not overlap"]

    def artifact_inspection() -> list[str]:
        assert len(records) == 12, f"expected 12 tracked production/optimized records, found {len(records)}"
        for record in records:
            assert record.get("status") in {"PRODUCTION", "OPTIMIZED"}, f"invalid lifecycle status for {record.get('asset_id')}"
            assert record.get("outputs"), f"missing outputs for {record.get('asset_id')}"
            for output in record["outputs"]:
                path = checked_path(output["path"])
                assert path.is_file() and path.stat().st_size == output["bytes"], f"missing/size mismatch: {output['path']}"
                assert sha256(path) == output["sha256"], f"hash mismatch: {output['path']}"
                if output["format"] == "SVG":
                    ET.parse(path)
                else:
                    with Image.open(path) as image:
                        image.load()
                        assert image.format == output["format"], f"format mismatch: {output['path']}"
                        assert image.size == (output["width"], output["height"]), f"dimension mismatch: {output['path']}"
                        assert not any(key in image.info for key in ("exif", "icc_profile", "xmp", "comment")), f"nonessential metadata remains: {output['path']}"
        return ["all 12 output records decode and match dimensions, formats, bytes and SHA-256", "nonessential image metadata is absent"]

    def text_integrity() -> list[str]:
        route_assets = manifest["canonicalDestinations"]
        for route, (asset_id, path) in zip(("/", "/hive", "/technology"), OG_OUTPUTS.items()):
            route_data = next(item for item in site["routes"] if item["path"] == route)
            assert route_assets[route]["title"] == route_data["title"] and route_assets[route]["description"] == route_data["description"], f"canonical copy mismatch: {route}"
            composition_info = by_id[asset_id]["composition"]
            visible = composition_info["visibleText"]
            assert " ".join(composition_info["titleLines"]) == route_data["title"], f"title line integrity mismatch: {route}"
            assert " ".join(composition_info["descriptionLines"]) == route_data["description"], f"description line integrity mismatch: {route}"
            assert visible["title"] == route_data["title"] and visible["description"] == route_data["description"], f"embedded metadata copy mismatch: {route}"
            assert by_id[asset_id]["alt_text"] == f"{route_data['title']}. {route_data['description']}", f"alt-purpose record mismatch: {route}"
        social = by_id[SOCIAL_ASSET]
        assert social["composition"]["visibleText"]["title"] == site["hero"]["heading"], "GitHub card title is not canonical"
        assert social["alt_text"].startswith(site["hero"]["heading"]), "GitHub social alt-purpose text missing"
        return ["Open Graph and repository card copy matches tracked canonical text", "all cards have truthful text descriptions"]

    def provenance() -> list[str]:
        for record in records:
            for field in ("asset_id", "version", "purpose", "brand_spec_revision", "source", "ugas", "blender", "rights", "outputs", "destinations", "approved_by", "approved_at", "alt_text"):
                assert field in record, f"BR-12 field {field} missing from {record.get('asset_id')}"
            assert record["source"].get("type") == "procedural" and record["source"].get("references"), f"source lineage missing: {record['asset_id']}"
            assert record["ugas"].get("workflow") is None and record["ugas"].get("workflow_version") is None, f"UGAS lineage must remain null: {record['asset_id']}"
            assert "not used" in record["ugas"].get("notes", "").lower(), f"no-generation note missing: {record['asset_id']}"
            assert record["rights"].get("external_inputs") == [] and record.get("external_inputs", []) == [], f"unapproved external input: {record['asset_id']}"
            assert record["rights"].get("provenance_reviewed") is True, f"provenance review marker missing: {record['asset_id']}"
            assert record["approved_by"] is None and record["approved_at"] is None, f"invented approval attribution: {record['asset_id']}"
            assert record.get("approval_status") == "NOT_INDEPENDENTLY_REVIEWED", f"approval state overstated: {record['asset_id']}"
            for reference in record["source"]["references"]:
                source = checked_path(reference["path"])
                assert source.is_file() and sha256(source) == reference["sha256"], f"source reference hash mismatch: {reference['path']}"
        return ["all 12 assets have truthful BR-12 records", "UGAS and Blender fields are null where unused", "external inputs and approvals are not invented"]

    def resolution_and_sources() -> list[str]:
        for key in ("hero16x9", "hero4x5", "hero1x1"):
            ref = acceptance["staticFallback"][key]
            source = checked_path(ref["path"])
            public_path = ROOT / "public/images/context-core" / Path(ref["path"]).name
            assert source.stat().st_size > 0 and sha256(source) == ref["sha256"], f"CP-06 accepted source hash mismatch: {key}"
            assert public_path.is_file() and public_path.read_bytes() == source.read_bytes(), f"CP-07 source copy changed: {key}"
        optimized = [asset for asset in records if asset["asset_id"].startswith("NL_CP08_HERO_")]
        assert len(optimized) == 6, f"expected six responsive format variants, found {len(optimized)}"
        expected_ratios = {"16X9": 16 / 9, "4X5": 4 / 5, "1X1": 1.0}
        for record in optimized:
            output = record["outputs"][0]
            composition_info = record["composition"]
            width, height = composition_info["sourceDimensions"]
            assert composition_info["outputDimensions"] == [width, height] and composition_info["upscaled"] is False, f"responsive framing/upscale mismatch: {record['asset_id']}"
            ratio = record["asset_id"].split("_")[3]
            assert abs(width / height - expected_ratios[ratio]) < 0.01, f"framing ratio mismatch: {record['asset_id']}"
            source = checked_path(next(ref["path"] for ref in record["source"]["references"] if ref["path"].startswith("artifacts/cp06/static/")))
            with Image.open(source) as original, Image.open(checked_path(output["path"])) as derivative:
                difference = ImageStat.Stat(ImageChops.difference(original.convert("RGB"), derivative.convert("RGB"))).mean
                error = sum(difference) / (3 * 255) * 100
                assert error <= MAX_PARITY_ERROR_PERCENT, f"visual parity error {error:.3f}% exceeds budget: {record['asset_id']}"
                assert derivative.width <= original.width and derivative.height <= original.height, f"upscaled responsive derivative: {record['asset_id']}"
            assert output["bytes"] < source.stat().st_size, f"optimized output did not reduce bytes: {record['asset_id']}"
        return ["accepted CP-06 and promoted CP-07 bytes remain identical", "16:9, 4:5 and 1:1 framing is preserved without upscaling", "six WebP/AVIF variants meet size and visual-parity budgets"]

    def destinations() -> list[str]:
        metadata = (ROOT / "lib/metadata/index.ts").read_text(encoding="utf-8")
        for asset_id, (route, public_path) in OG_OUTPUTS.items():
            assert re.search(rf'"{re.escape(route)}"\s*:\s*"{re.escape(public_path.removeprefix("public"))}"', metadata), f"metadata does not map {route} to its committed local image"
            assert checked_path(public_path).is_file(), f"metadata target missing: {public_path}"
            assert by_id[asset_id]["destinations"] == [route], f"unverified OG destination: {route}"
        github = by_id[SOCIAL_ASSET]
        assert github["destinations"] == ["https://github.com/KayzenRoot/nexlabs-web"], "GitHub preview destination mismatch"
        generic = by_id["NL_CP08_TEMPLATE_GENERIC_SOCIAL"]
        assert generic["destinations"] == [], "generic template must not claim a destination"
        return ["three metadata destinations resolve to committed local PNG files", "repository preview uses the verified repository URL", "generic template has no fabricated destination"]

    def compression() -> list[str]:
        rows = manifest.get("compression", [])
        assert len(rows) == 6, f"expected six size measurements, found {len(rows)}"
        for row in rows:
            assert row["outputBytes"] < row["sourceBytes"] and row["sizeChangePercent"] < 0, f"size regression: {row['outputPath']}"
            assert row["normalizedMeanAbsoluteErrorPercent"] <= MAX_PARITY_ERROR_PERCENT, f"visual quality exceeds budget: {row['outputPath']}"
            assert sha256(checked_path(row["outputPath"])) == row["outputSha256"], f"compression report hash mismatch: {row['outputPath']}"
        cards = [by_id[asset_id]["outputs"][0] for asset_id in (*OG_OUTPUTS.keys(), SOCIAL_ASSET)]
        assert all(item["bytes"] <= 512 * 1024 for item in cards), "social image exceeds 512 KiB budget"
        return ["each responsive derivative is smaller than its accepted PNG source", "all visual parity scores are within 3% normalized MAE", "all social cards are at most 512 KiB"]

    def meaning_and_template() -> list[str]:
        template = checked_path("artifacts/cp08/templates/social-card.svg").read_text(encoding="utf-8")
        assert not PLACEHOLDER_PATTERN.search(template), "generic SVG contains unresolved placeholder text"
        assert "NexLabs" in template and "{{" not in template, "generic brand frame or reusable layout is missing"
        assert all(record.get("alt_text") for record in records), "a visual asset lacks an alt-purpose description"
        for record in records:
            composition_info = record.get("composition", {})
            visible = composition_info.get("visibleText", {})
            for text in visible.values():
                assert not PLACEHOLDER_PATTERN.search(str(text)), f"placeholder/fabricated text in {record['asset_id']}"
        boundary = (ROOT / "components/three/StaticContextCore.tsx").read_text(encoding="utf-8")
        assert "alt=\"\"" in boundary and "aria-hidden=\"true\"" in boundary, "responsive image is no longer decorative in the UI"
        page_source = (ROOT / "app/page.tsx").read_text(encoding="utf-8")
        home_source = (ROOT / "components/sections/HomeShell.tsx").read_text(encoding="utf-8")
        visual_source = (ROOT / "components/media/VisualSlot.tsx").read_text(encoding="utf-8")
        assert "HomeShell" in page_source and "HeroVisualSlot" in home_source and "ThreeBoundary" in visual_source, "static visual is not paired with the live semantic page"
        return ["generic template contains no unresolved tokens or fake social claim", "visuals have provenance alt-purpose descriptions", "site meaning remains in semantic HTML and visuals stay decorative"]

    def release_manifest() -> list[str]:
        assert manifest.get("schemaVersion") == "nexlabs-web-cp08-asset-manifest-v1", "CP-08 manifest schema mismatch"
        assert manifest.get("status") == "PRODUCTION_AND_OPTIMIZED_NOT_RELEASED" and manifest.get("releaseStatus") == "NOT_RELEASED", "release state overstated"
        assert all(record["status"] in {"PRODUCTION", "OPTIMIZED"} for record in records), "asset was marked RELEASED or has an invalid state"
        boundaries = manifest["boundaries"]
        assert boundaries == {"ugasProviderStarted": False, "ugasGenerationPerformed": False, "externalInputs": [], "identityChanged": False, "released": False, "deployed": False, "merged": False, "cp09Started": False}, "forbidden scope boundary changed"
        tracked_changes = set()
        import subprocess
        for args in (("diff", "--name-only", BASE, "HEAD"), ("diff", "--name-only"), ("ls-files", "--others", "--exclude-standard")):
            tracked_changes.update(filter(None, subprocess.check_output(["git", *args], cwd=ROOT, text=True).splitlines()))
        forbidden = [name for name in tracked_changes if re.search(r"(?:^|/)(?:cp09|deployment|deploy|wrangler|dns)(?:/|\.|$)", name, re.IGNORECASE)]
        assert not forbidden, f"out-of-scope CP-09/deployment files detected: {forbidden}"
        assert manifest.get("generationMode") == "DETERMINISTIC_NO_GENERATION" and manifest.get("sourceDocumentSha256") == "b89cc978f695cd990ae3d4d8a473af5df53b47ea161411d7432e782c65718990", "no-generation/source authority mismatch"
        return ["manifest status is NOT_RELEASED and asset lifecycle is PRODUCTION/OPTIMIZED only", "no UGAS provider, release, merge, deployment or CP-09 action is recorded", "no CP-09/deployment implementation files are in the change set"]

    add_gate(gates, "UG1", "Brand compliance", brand)
    add_gate(gates, "UG2", "Composition", composition)
    add_gate(gates, "UG3", "Artifact inspection", artifact_inspection)
    add_gate(gates, "UG4", "Text/logo integrity", text_integrity)
    add_gate(gates, "UG5", "Provenance", provenance)
    add_gate(gates, "UG6", "Technical resolution", resolution_and_sources)
    add_gate(gates, "UG7", "Destination crop", destinations)
    add_gate(gates, "UG8", "Compression quality", compression)
    add_gate(gates, "UG9", "Accessibility/meaning", meaning_and_template)
    add_gate(gates, "UG10", "Release manifest", release_manifest)
    findings = [finding for gate in gates for finding in gate["findings"]]
    return {
        "schemaVersion": "nexlabs-web-cp08-gate-report-v1",
        "status": "PASS" if not findings else "FAIL",
        "verdict": "PASS" if not findings else "FAIL",
        "candidateHead": None,
        "manifestSha256": sha256(MANIFEST_PATH),
        "releaseStatus": manifest.get("releaseStatus"),
        "gates": gates,
        "findings": findings,
    }


def write_report(report: dict[str, Any]) -> None:
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    lines = [
        "# CP-08 derivative media quality gates",
        "",
        f"Status: **{report['status']}**",
        f"Release: **{report['releaseStatus']}**",
        "",
        "| Gate | Description | Status | Severity |",
        "| --- | --- | --- | --- |",
    ]
    for gate in report["gates"]:
        lines.append(f"| {gate['id']} | {gate['title']} | {gate['status']} | {gate['severity']} |")
    for gate in report["gates"]:
        lines.extend(["", f"## {gate['id']} — {gate['title']}", ""])
        lines.extend(f"- {detail}" for detail in gate["evidence"])
        lines.extend(f"- Finding: {finding}" for finding in gate["findings"])
    lines.extend(["", "No asset is marked RELEASED. No external input, approval identity, approval timestamp, provider startup, generation, deployment, merge or CP-09 action is claimed.", ""])
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> int:
    report = validate_media()
    write_report(report)
    print(f"CP-08 media validation: {report['status']}")
    for gate in report["gates"]:
        print(f"{gate['id']} {gate['title']}: {gate['status']}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
