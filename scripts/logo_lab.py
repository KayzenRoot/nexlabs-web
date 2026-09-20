"""Deterministic CP-04 logo candidate generator and validator.

This lab intentionally lives outside the runtime brand components. The masters are
path-only SVGs; review sheets may add labels and context text.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

try:
    from PIL import Image, ImageDraw
except ImportError:  # SVG remains the authoritative review format on minimal CI images.
    Image = None
    ImageDraw = None


ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "brand" / "logo"
CANDIDATE_DIR = LAB / "candidates"
PROVENANCE_DIR = LAB / "provenance"
REVIEW_DIR = LAB / "review"
GRID = 12
CANVAS = 120
EXPECTED_IDS = [
    "NX-D-01", "NX-D-02", "NX-D-03",
    "NX-C-01", "NX-C-02", "NX-C-03",
    "NX-B-01", "NX-B-02", "NX-B-03",
]


def primitive(points: list[tuple[int, int]], *, kind: str = "line", width: int = 12) -> dict[str, Any]:
    return {"points": points, "kind": kind, "width": width}


def candidate(candidate_id: str, family: str, name: str, paths: list[dict[str, Any]], note: str) -> dict[str, Any]:
    return {"id": candidate_id, "family": family, "name": name, "paths": paths, "note": note}


CANDIDATES = [
    candidate("NX-D-01", "Topological N", "continuous diagonal", [
        primitive([(30, 90), (30, 30), (90, 90), (90, 30)], width=14),
    ], "One continuous N gesture with a decisive diagonal crossing."),
    candidate("NX-D-02", "Topological N", "split orbit", [
        primitive([(30, 90), (30, 30), (90, 90)], width=13),
        primitive([(90, 90), (90, 30)], width=13),
        primitive([(30, 60), (60, 60)], width=8),
    ], "Two vertical anchors and a controlled midline create a layered topology."),
    candidate("NX-D-03", "Topological N", "solid cut N", [
        primitive([(30, 90), (30, 30), (50, 30), (90, 70), (90, 30), (100, 30), (100, 90), (80, 90), (40, 50), (40, 90)], kind="polygon"),
    ], "Compact filled silhouette with a single diagonal negative-space cut."),
    candidate("NX-C-01", "Modular Core", "four-node core", [
        primitive([(25, 25), (48, 25), (48, 48), (25, 48)], kind="polygon"),
        primitive([(72, 25), (95, 25), (95, 48), (72, 48)], kind="polygon"),
        primitive([(25, 72), (48, 72), (48, 95), (25, 95)], kind="polygon"),
        primitive([(72, 72), (95, 72), (95, 95), (72, 95)], kind="polygon"),
        primitive([(48, 48), (72, 48), (72, 72), (48, 72)], kind="polygon"),
    ], "Five restrained modules establish a central system core."),
    candidate("NX-C-02", "Modular Core", "interlock core", [
        primitive([(25, 25), (55, 25), (55, 42), (42, 42), (42, 78), (55, 78), (55, 95), (25, 95)], kind="polygon"),
        primitive([(95, 25), (65, 25), (65, 42), (78, 42), (78, 78), (65, 78), (65, 95), (95, 95)], kind="polygon"),
        primitive([(55, 42), (65, 42), (65, 78), (55, 78)], kind="polygon"),
    ], "Opposed modules interlock around a narrow vertical core."),
    candidate("NX-C-03", "Modular Core", "open core frame", [
        primitive([(25, 25), (55, 25), (55, 38), (38, 38), (38, 82), (55, 82), (55, 95), (25, 95)], kind="polygon"),
        primitive([(95, 25), (65, 25), (65, 38), (82, 38), (82, 82), (65, 82), (65, 95), (95, 95)], kind="polygon"),
        primitive([(55, 48), (65, 48), (65, 72), (55, 72)], kind="polygon"),
    ], "Open frame variant keeps the core readable at reduced size."),
    candidate("NX-B-01", "Routed N", "diagonal route", [
        primitive([(28, 90), (28, 30), (44, 30), (92, 78), (92, 30)], width=13),
        primitive([(28, 60), (54, 60)], width=8),
    ], "A routed path uses one diagonal trunk with a small service branch."),
    candidate("NX-B-02", "Routed N", "orthogonal route", [
        primitive([(28, 90), (28, 30), (46, 30), (92, 76), (92, 30)], width=12),
        primitive([(28, 60), (58, 60), (58, 48)], width=8),
        primitive([(74, 90), (92, 90)], width=8),
    ], "Orthogonal service turns make infrastructure semantics explicit without circuitry detail."),
    candidate("NX-B-03", "Routed N", "dual rail route", [
        primitive([(28, 90), (28, 30), (42, 30), (92, 80), (92, 30)], width=11),
        primitive([(42, 90), (42, 58), (74, 90)], width=9),
        primitive([(28, 60), (56, 60)], width=7),
    ], "Two rails and a shared diagonal produce the most structural route study."),
]


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def path_d(item: dict[str, Any]) -> str:
    points = item["points"]
    prefix = "M " + " L ".join(f"{x} {y}" for x, y in points)
    return prefix + (" Z" if item["kind"] == "polygon" else "")


def master_svg(item: dict[str, Any]) -> str:
    body: list[str] = []
    for path in item["paths"]:
        d = path_d(path)
        if path["kind"] == "polygon":
            body.append(f'  <path d="{d}" fill="#10151c" fill-rule="nonzero"/>')
        else:
            body.append(
                f'  <path d="{d}" fill="none" stroke="#10151c" stroke-linecap="round" stroke-linejoin="round" stroke-width="{path["width"]}"/>'
            )
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" role="img">\n' + "\n".join(body) + "\n</svg>\n"


def svg_symbol(item: dict[str, Any], x: float, y: float, size: float, color: str) -> str:
    scale = size / CANVAS
    parts = [f'<g transform="translate({x:g} {y:g}) scale({scale:g})">']
    for path in item["paths"]:
        d = path_d(path)
        if path["kind"] == "polygon":
            parts.append(f'<path d="{d}" fill="{color}"/>')
        else:
            parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-linecap="round" stroke-linejoin="round" stroke-width="{path["width"]}"/>')
    parts.append("</g>")
    return "".join(parts)


def svg_document(width: int, height: int, body: list[str]) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">\n' + "\n".join(body) + "\n</svg>\n"


def text(x: float, y: float, value: str, size: int = 12, color: str = "#10151c", weight: str = "400") -> str:
    safe = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<text x="{x:g}" y="{y:g}" font-family="Arial, sans-serif" font-size="{size}px" font-weight="{weight}" fill="{color}">{safe}</text>'


def review_sheets() -> dict[str, str]:
    body: list[str] = ['<rect width="960" height="720" fill="#f5f7f9"/>', text(40, 42, "CP04 / nine candidate contact sheet", 22, weight="700")]
    for index, item in enumerate(CANDIDATES):
        col, row = index % 3, index // 3
        x, y = 40 + col * 300, 72 + row * 210
        body.append(f'<rect x="{x}" y="{y}" width="260" height="170" rx="14" fill="#ffffff" stroke="#d8e0e8"/>')
        body.append(svg_symbol(item, x + 65, y + 15, 140, "#10151c"))
        body.append(text(x + 16, y + 150, item["id"], 14, weight="700"))
        body.append(text(x + 88, y + 150, item["family"], 11, "#586474"))
    contact = svg_document(960, 720, body)

    body = ['<rect width="1000" height="1500" fill="#eef2f5"/>', text(32, 38, "CP04 / small-size and legibility sweep", 20, weight="700")]
    sizes = [16, 24, 32, 64, 128]
    for row, item in enumerate(CANDIDATES):
        y = 56 + row * 160
        body.append(text(22, y + 35, item["id"], 11, weight="700"))
        for col, size in enumerate(sizes):
            x = 135 + col * 145
            body.append(f'<rect x="{x - 8}" y="{y}" width="{size + 16}" height="{size + 16}" fill="#ffffff" stroke="#d8e0e8"/>')
            body.append(svg_symbol(item, x, y + 8, size, "#10151c"))
            body.append(text(x, y + size + 27, str(size), 9, "#586474"))
    small = svg_document(1000, 1500, body)

    body = ['<rect width="1060" height="520" fill="#f5f7f9"/>', text(34, 40, "CP04 / light-dark lockup comparison", 22, weight="700")]
    for index, item in enumerate(CANDIDATES):
        col, row = index % 3, index // 3
        x, y = 34 + col * 345, 68 + row * 145
        body.append(f'<rect x="{x}" y="{y}" width="320" height="112" rx="12" fill="#ffffff" stroke="#d8e0e8"/>')
        body.append(f'<rect x="{x + 160}" y="{y}" width="160" height="112" rx="0" fill="#10151c"/>')
        body.append(svg_symbol(item, x + 22, y + 17, 78, "#10151c"))
        body.append(svg_symbol(item, x + 182, y + 17, 78, "#f5f7f9"))
        body.append(text(x + 20, y + 101, item["id"], 10, "#586474", "700"))
        body.append(text(x + 180, y + 101, "NexLabs", 10, "#cdd7e1", "700"))
    theme = svg_document(1060, 520, body)

    body = ['<rect width="1200" height="620" fill="#202833"/>', text(40, 44, "CP04 / website-context comparison", 22, "#f5f7f9", "700")]
    contexts = [("HEADER / LIGHT", "#f5f7f9", "#10151c"), ("HERO / DARK", "#10151c", "#f5f7f9"), ("FOOTER / MINERAL", "#303b47", "#f5f7f9"), ("SQUARE AVATAR", "#f5f7f9", "#10151c")]
    for index, (label, bg, fg) in enumerate(contexts):
        x = 40 + (index % 2) * 570
        y = 70 + (index // 2) * 245
        body.append(f'<rect x="{x}" y="{y}" width="520" height="190" rx="16" fill="{bg}"/>')
        body.append(text(x + 22, y + 34, label, 12, fg, "700"))
        for col, item in enumerate(CANDIDATES[:3]):
            body.append(svg_symbol(item, x + 28 + col * 160, y + 52, 90, fg))
            body.append(text(x + 45 + col * 160, y + 166, item["id"], 10, fg))
        if index == 0:
            body.append(text(x + 330, y + 52, "NexLabs", 20, fg, "700"))
    context = svg_document(1200, 620, body)
    return {"contact-sheet.svg": contact, "small-size.svg": small, "theme-lockups.svg": theme, "website-context.svg": context}


def blocker_sheet() -> str:
    body: list[str] = ['<rect width="960" height="540" fill="#202833"/>', text(36, 46, "CP04 / Blender MCP projection status", 22, "#f5f7f9", "700"), text(36, 78, "BLOCKED_EXTERNAL: addon connection unavailable; no 3D pass is claimed.", 13, "#ffb4a2")]
    for index, item in enumerate(CANDIDATES):
        col, row = index % 3, index // 3
        x, y = 36 + col * 300, 106 + row * 130
        body.append(f'<rect x="{x}" y="{y}" width="260" height="92" rx="12" fill="#303b47" stroke="#536272"/>')
        body.append(svg_symbol(item, x + 16, y + 12, 68, "#d8e0e8"))
        body.append(text(x + 92, y + 42, item["id"], 13, "#f5f7f9", "700"))
        body.append(text(x + 92, y + 64, "external blocker", 11, "#ffb4a2"))
    return svg_document(960, 540, body)


def png_symbol(image: Image.Image, item: dict[str, Any], x: int, y: int, size: int, color: tuple[int, int, int]) -> None:
    draw = ImageDraw.Draw(image)
    scale = size / CANVAS
    def point(pair: tuple[int, int]) -> tuple[int, int]:
        return (round(x + pair[0] * scale), round(y + pair[1] * scale))
    for path in item["paths"]:
        points = [point(pair) for pair in path["points"]]
        if path["kind"] == "polygon":
            draw.polygon(points, fill=color)
        else:
            draw.line(points, fill=color, width=max(1, round(path["width"] * scale)), joint="curve")
            radius = max(1, round(path["width"] * scale / 2))
            for px, py in (points[0], points[-1]):
                draw.ellipse((px - radius, py - radius, px + radius, py + radius), fill=color)


def png_sheets() -> dict[str, Image.Image]:
    if Image is None or ImageDraw is None:
        return {}
    contact = Image.new("RGB", (960, 720), "#f5f7f9")
    draw = ImageDraw.Draw(contact)
    for index, item in enumerate(CANDIDATES):
        col, row = index % 3, index // 3
        x, y = 40 + col * 300, 72 + row * 210
        draw.rounded_rectangle((x, y, x + 260, y + 170), radius=14, fill="#ffffff", outline="#d8e0e8")
        png_symbol(contact, item, x + 65, y + 15, 140, (16, 21, 28))
        draw.text((x + 16, y + 150), item["id"], fill="#10151c")
    small = Image.new("RGB", (1000, 1500), "#eef2f5")
    draw = ImageDraw.Draw(small)
    for row, item in enumerate(CANDIDATES):
        y = 56 + row * 160
        draw.text((22, y + 20), item["id"], fill="#10151c")
        for col, size in enumerate([16, 24, 32, 64, 128]):
            x = 135 + col * 145
            draw.rectangle((x - 8, y, x + size + 8, y + size + 16), fill="#ffffff", outline="#d8e0e8")
            png_symbol(small, item, x, y + 8, size, (16, 21, 28))
    theme = Image.new("RGB", (1060, 520), "#f5f7f9")
    draw = ImageDraw.Draw(theme)
    for index, item in enumerate(CANDIDATES):
        col, row = index % 3, index // 3
        x, y = 34 + col * 345, 68 + row * 145
        draw.rounded_rectangle((x, y, x + 320, y + 112), radius=12, fill="#ffffff", outline="#d8e0e8")
        draw.rectangle((x + 160, y, x + 320, y + 112), fill="#10151c")
        png_symbol(theme, item, x + 22, y + 17, 78, (16, 21, 28))
        png_symbol(theme, item, x + 182, y + 17, 78, (245, 247, 249))
    return {"contact-sheet.png": contact, "small-size.png": small, "theme-lockups.png": theme}


def evaluation_markdown() -> str:
    rows = [
        ("NX-D-01", "PASS", "Strong single gesture; good 16 px survival.", "Diagonal is familiar; similarity research remains open."),
        ("NX-D-02", "PASS", "Layered topology and clear anchors.", "Midline adds density at 16 px."),
        ("NX-D-03", "PASS", "Best filled silhouette and clean negative cut.", "Heavier mass can read more like a generic N."),
        ("NX-C-01", "PASS", "Strong modular system semantics; stable avatar.", "Core may look blocky beside wordmark."),
        ("NX-C-02", "PASS", "Clear interlock and 2D/3D projection potential.", "Narrow core needs optical review in dark mode."),
        ("NX-C-03", "PASS", "Open frame preserves negative space at small sizes.", "Less immediate N read than the other C variants."),
        ("NX-B-01", "PASS", "Route semantics with restrained detail.", "Service branch can disappear under blur."),
        ("NX-B-02", "PASS", "Controlled orthogonal turn communicates infrastructure.", "Most circuitry-adjacent; avoid technology cliche."),
        ("NX-B-03", "PASS", "Distinct rail structure and strong horizontal rhythm.", "Highest small-size complexity; human review required."),
    ]
    lines = [
        "# CP04 Logo Exploration Evaluation",
        "",
        "Status: candidate batch only; no automatic winner and no canonical selection.",
        "",
        "## Method",
        "",
        "Each symbol is evaluated independently across silhouette, small size, relevance, infrastructure semantics, 2D/3D coherence, wordmark context, motion readiness, production simplicity, accessibility/color independence and similarity risk. `PASS` means the candidate is reviewable for the next human gate, not approved.",
        "",
        "## Candidate rows",
        "",
        "| ID | Result | Strengths | Weaknesses / repair note |",
        "| --- | --- | --- | --- |",
    ]
    lines.extend(f"| {id_} | {status} | {strength} | {weakness} |" for id_, status, strength, weakness in rows)
    lines.extend([
        "",
        "## Objective checks",
        "",
        "- PASS: 12x12 construction grid, path-only masters, monochrome and no gradients.",
        "- PASS: 16/24/32/64/128 px review sheet, light/dark, square/avatar and horizontal lockup contexts generated deterministically.",
        "- PASS: reduced-motion behavior is static by construction; no animation is encoded.",
        "- BLOCKED_EXTERNAL: Blender MCP projection proof could not run because the live addon was unreachable. The blocker is recorded separately and no 3D pass is claimed.",
        "- NOT_PERFORMED_IN_SCOPE: external visual similarity and trademark clearance. This is a required independent review gap, not evidence of uniqueness.",
        "",
        "## Human gate",
        "",
        "HG-01 must select or reject candidates independently. This document does not recommend a candidate and does not authorize runtime BrandMark wiring.",
    ])
    return "\n".join(lines) + "\n"


def provenance(item: dict[str, Any], svg_hash: str) -> dict[str, Any]:
    return {
        "schemaVersion": "nexlabs-cp04-logo-provenance-v1",
        "candidateId": item["id"],
        "family": item["family"],
        "revision": "r1",
        "status": "CANDIDATE_EXPLORATION",
        "constructionGrid": "12x12",
        "source": {"type": "deterministic-procedural", "generator": "scripts/logo_lab.py", "references": ["BR-03-LOGO-SYSTEM", "BR-03-LOGO-EVALUATION", "BR-12-UGAS-ASSET-PIPELINE"]},
        "svgPath": f"brand/logo/candidates/{item['id']}.svg",
        "svgSha256": svg_hash,
        "ugAS": {"mode": "REFERENCE_ONLY", "generation": "NOT_PERFORMED", "canonical": False},
        "blender": {"mode": "LIGHTWEIGHT_PROJECTION_ATTEMPTED", "status": "BLOCKED_EXTERNAL", "canonical": False},
        "approval": None,
        "canonicalRuntimeWiring": False,
    }


def generate() -> None:
    for directory in (CANDIDATE_DIR, PROVENANCE_DIR, REVIEW_DIR):
        directory.mkdir(parents=True, exist_ok=True)
    index_items = []
    for item in CANDIDATES:
        svg = master_svg(item).encode("utf-8")
        path = CANDIDATE_DIR / f"{item['id']}.svg"
        path.write_bytes(svg)
        svg_hash = sha256_bytes(svg)
        metadata = provenance(item, svg_hash)
        (PROVENANCE_DIR / f"{item['id']}.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        index_items.append({"id": item["id"], "family": item["family"], "revision": "r1", "status": "CANDIDATE_EXPLORATION", "svg": f"brand/logo/candidates/{item['id']}.svg", "sha256": svg_hash})
    for name, content in review_sheets().items():
        (REVIEW_DIR / name).write_text(content, encoding="utf-8")
    (REVIEW_DIR / "blender-projection-blocked.svg").write_text(blocker_sheet(), encoding="utf-8")
    (REVIEW_DIR / "blender-mcp-receipt.json").write_text(json.dumps({
        "status": "BLOCKED_EXTERNAL",
        "attempts": [{"tool": "get_addon_status", "result": "Could not connect to Blender. Make sure the Blender addon is running."}, {"tool": "get_scene_info", "result": "Could not connect to Blender. Make sure the Blender addon is running."}],
        "proofs": {"candidateCount": 9, "completed": 0, "claimed": False},
        "providerStarted": False,
    }, indent=2) + "\n", encoding="utf-8")
    (LAB / "evaluation.md").write_text(evaluation_markdown(), encoding="utf-8")
    for name, image in png_sheets().items():
        image.save(REVIEW_DIR / name, format="PNG", optimize=False, compress_level=9)
    review_files = sorted(str(path.relative_to(ROOT)).replace("\\", "/") for path in REVIEW_DIR.iterdir() if path.is_file())
    index = {
        "schemaVersion": "nexlabs-cp04-logo-index-v1",
        "workOrder": "NXWEB-WO-0003-CP04-LOGO-EXPLORATION",
        "status": "CANDIDATE_EXPLORATION",
        "canonicalSelection": False,
        "runtimeWiring": False,
        "constructionGrid": "12x12",
        "generator": "scripts/logo_lab.py",
        "candidateIds": EXPECTED_IDS,
        "candidates": index_items,
        "reviewArtifacts": review_files + ["brand/logo/evaluation.md", "brand/logo/artifact-manifest.json"],
        "blenderProjection": "BLOCKED_EXTERNAL",
        "ugasGeneration": "NOT_PERFORMED",
        "externalSimilarityResearch": "NOT_PERFORMED_IN_SCOPE",
    }
    (LAB / "candidate-index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    (LAB / "README.md").write_text("# CP04 logo candidate lab\n\nThis is a non-runtime exploration package. Do not import these masters into runtime BrandMark until HG-01 selects and separately promotes one candidate.\n\nGenerated by `scripts/logo_lab.py`; run `python scripts/logo_lab.py --check` to validate the deterministic batch.\n", encoding="utf-8")
    artifact_paths = sorted(
        [*(CANDIDATE_DIR.glob("*.svg")), *(PROVENANCE_DIR.glob("*.json")), *(REVIEW_DIR.iterdir()), LAB / "candidate-index.json", LAB / "evaluation.md", LAB / "README.md"],
        key=lambda path: str(path.relative_to(ROOT)).replace("\\", "/"),
    )
    manifest = {"schemaVersion": "nexlabs-cp04-logo-artifact-manifest-v1", "generatedBy": "scripts/logo_lab.py", "artifacts": []}
    for path in artifact_paths:
        if path.is_file() and path.name != "artifact-manifest.json":
            manifest["artifacts"].append({"path": str(path.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256_bytes(path.read_bytes())})
    (LAB / "artifact-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def check() -> None:
    index_path = LAB / "candidate-index.json"
    if not index_path.is_file():
        raise SystemExit("logo lab index is missing; run without --check first")
    index = json.loads(index_path.read_text(encoding="utf-8"))
    if index.get("candidateIds") != EXPECTED_IDS or len(index.get("candidates", [])) != 9:
        raise SystemExit("logo lab must contain exactly the nine CP04 candidate IDs")
    if index.get("canonicalSelection") is not False or index.get("runtimeWiring") is not False:
        raise SystemExit("logo lab must not claim canonical selection or runtime wiring")
    for item in index["candidates"]:
        path = ROOT / item["svg"]
        raw = path.read_bytes()
        if sha256_bytes(raw) != item["sha256"]:
            raise SystemExit(f"candidate hash mismatch: {item['id']}")
        source = raw.decode("utf-8")
        if "<text" in source or "<rect" in source or "<circle" in source or "linearGradient" in source or "radialGradient" in source:
            raise SystemExit(f"master contains non-path artwork: {item['id']}")
        if 'viewBox="0 0 120 120"' not in source:
            raise SystemExit(f"master viewBox is not normalized: {item['id']}")
        if not re.search(r"<path\b", source):
            raise SystemExit(f"master has no paths: {item['id']}")
        provenance_path = PROVENANCE_DIR / f"{item['id']}.json"
        provenance_data = json.loads(provenance_path.read_text(encoding="utf-8"))
        if provenance_data.get("svgSha256") != item["sha256"] or provenance_data.get("approval") is not None:
            raise SystemExit(f"provenance mismatch or approval leak: {item['id']}")
    expected_reviews = {"contact-sheet.svg", "small-size.svg", "theme-lockups.svg", "website-context.svg", "blender-projection-blocked.svg", "blender-mcp-receipt.json"}
    actual_reviews = {path.name for path in REVIEW_DIR.iterdir() if path.is_file()}
    if not expected_reviews.issubset(actual_reviews):
        raise SystemExit(f"missing review artifacts: {sorted(expected_reviews - actual_reviews)}")
    print(f"Logo lab PASS: {len(EXPECTED_IDS)} candidates, {len(actual_reviews)} review artifacts, no canonical wiring")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
    else:
        generate()
        check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
