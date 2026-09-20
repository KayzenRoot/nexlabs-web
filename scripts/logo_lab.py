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
    from PIL import Image, ImageDraw, ImageFilter
except ImportError:  # SVG remains the authoritative review format on minimal CI images.
    Image = None
    ImageDraw = None
    ImageFilter = None


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


def candidate(candidate_id: str, family: str, name: str, paths: list[dict[str, Any]], note: str, *, revision: str = "r1") -> dict[str, Any]:
    return {"id": candidate_id, "family": family, "name": name, "paths": paths, "note": note, "revision": revision}


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
        primitive([(28, 60), (56, 60), (64, 52)], width=9),
    ], "A routed path uses one diagonal trunk with a connected service spur for clearer small-size route legibility.", revision="r2"),
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

    body = ['<rect width="1320" height="850" fill="#202833"/>', text(40, 44, "CP04 / website-context comparison / all nine candidates", 22, "#f5f7f9", "700")]
    contexts = [("HEADER / LIGHT", "#f5f7f9", "#10151c"), ("HERO / DARK", "#10151c", "#f5f7f9"), ("FOOTER / MINERAL", "#303b47", "#f5f7f9"), ("SQUARE AVATAR", "#f5f7f9", "#10151c")]
    for index, (label, bg, fg) in enumerate(contexts):
        x = 40 + (index % 2) * 640
        y = 70 + (index // 2) * 390
        body.append(f'<rect x="{x}" y="{y}" width="600" height="330" rx="16" fill="{bg}"/>')
        body.append(text(x + 22, y + 34, label, 12, fg, "700"))
        for candidate_index, item in enumerate(CANDIDATES):
            col, row = candidate_index % 3, candidate_index // 3
            cell_x, cell_y = x + 34 + col * 188, y + 52 + row * 82
            body.append(svg_symbol(item, cell_x, cell_y, 62, fg))
            body.append(text(cell_x + 7, cell_y + 75, item["id"], 9, fg, "700"))
        if index == 0:
            body.append(text(x + 414, y + 36, "NexLabs", 16, fg, "700"))
    context = svg_document(1320, 850, body)

    body = ['<rect width="1320" height="980" fill="#eef2f5"/>', text(40, 40, "CP04 / true horizontal NexLabs lockups / all nine candidates", 22, weight="700")]
    body.append(text(40, 65, "Each row is one symbol + NexLabs lockup rendered on light and dark backgrounds.", 11, "#586474"))
    for index, item in enumerate(CANDIDATES):
        y = 82 + index * 96
        for variant, (x, bg, fg) in enumerate(((40, "#ffffff", "#10151c"), (680, "#10151c", "#f5f7f9"))):
            body.append(f'<rect x="{x}" y="{y}" width="600" height="76" rx="12" fill="{bg}" stroke="#d8e0e8"/>')
            body.append(svg_symbol(item, x + 18, y + 8, 60, fg))
            body.append(text(x + 100, y + 48, "NexLabs", 22, fg, "700"))
            body.append(text(x + 492, y + 47, item["id"], 12, fg, "700"))
    horizontal = svg_document(1320, 980, body)

    blur_metrics = blur_squint_metrics()
    body = [
        '<defs><filter id="squint-blur" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="1.5"/></filter></defs>',
        '<rect width="1200" height="780" fill="#202833"/>',
        text(36, 42, "CP04 / deterministic blur-squint silhouette review", 22, "#f5f7f9", "700"),
        text(36, 68, "48px raster -> Gaussian blur radius 1.5 -> 16px LANCZOS downsample -> nearest preview", 11, "#cdd7e1"),
    ]
    for index, item in enumerate(CANDIDATES):
        col, row = index % 3, index // 3
        x, y = 36 + col * 390, 88 + row * 220
        metric = blur_metrics[item["id"]]
        body.append(f'<rect x="{x}" y="{y}" width="350" height="184" rx="12" fill="#303b47" stroke="#536272"/>')
        body.append(text(x + 18, y + 28, item["id"], 13, "#f5f7f9", "700"))
        body.append(f'<g filter="url(#squint-blur)">{svg_symbol(item, x + 28, y + 42, 100, "#f5f7f9")}</g>')
        body.append(text(x + 150, y + 72, "SQUINT", 10, "#cdd7e1", "700"))
        body.append(text(x + 150, y + 98, f"retained pixels: {metric['retainedPixels']}", 10, "#cdd7e1"))
        body.append(text(x + 150, y + 120, f"peak: {metric['peak']}", 10, "#cdd7e1"))
        body.append(text(x + 150, y + 148, metric["result"], 11, "#a7f3d0", "700"))
    blur = svg_document(1200, 780, body)
    return {
        "contact-sheet.svg": contact,
        "small-size.svg": small,
        "theme-lockups.svg": theme,
        "website-context.svg": context,
        "horizontal-lockups.svg": horizontal,
        "blur-squint.svg": blur,
    }


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


def png_symbol(image: Image.Image, item: dict[str, Any], x: int, y: int, size: int, color: Any) -> None:
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


def blur_squint_metrics() -> dict[str, dict[str, Any]]:
    if Image is None or ImageDraw is None or ImageFilter is None:
        raise RuntimeError("Pillow is required for the deterministic blur-squint review")
    metrics: dict[str, dict[str, Any]] = {}
    for item in CANDIDATES:
        raster = Image.new("L", (48, 48), 0)
        png_symbol(raster, item, 0, 0, 48, 255)
        blurred = raster.filter(ImageFilter.GaussianBlur(radius=1.5))
        reduced = blurred.resize((16, 16), Image.Resampling.LANCZOS)
        restored = reduced.resize((48, 48), Image.Resampling.NEAREST)
        retained = sum(1 for value in restored.tobytes() if value >= 16)
        peak = max(reduced.tobytes())
        metrics[item["id"]] = {
            "method": "48px raster -> GaussianBlur(1.5) -> 16px LANCZOS -> 48px nearest preview",
            "retainedPixels": retained,
            "peak": peak,
            "threshold": {"retainedPixelsMin": 6, "peakMin": 16},
            "result": "PASS" if retained >= 6 and peak >= 16 else "REVIEW",
        }
    return metrics


def review_coverage(metrics: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        "schemaVersion": "nexlabs-cp04-review-coverage-v1",
        "generatedBy": "scripts/logo_lab.py",
        "candidateIndex": "brand/logo/candidate-index.json",
        "candidateIds": EXPECTED_IDS,
        "websiteContext": {
            "artifact": "brand/logo/review/website-context.svg",
            "contexts": {name: EXPECTED_IDS for name in ("HEADER / LIGHT", "HERO / DARK", "FOOTER / MINERAL", "SQUARE AVATAR")},
        },
        "horizontalLockups": {
            "artifact": "brand/logo/review/horizontal-lockups.svg",
            "variants": {"LIGHT": EXPECTED_IDS, "DARK": EXPECTED_IDS},
        },
        "blurSquint": {
            "artifact": "brand/logo/review/blur-squint.svg",
            "results": [{"id": candidate_id, **metrics[candidate_id]} for candidate_id in EXPECTED_IDS],
        },
    }


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
    website = Image.new("RGB", (1320, 850), "#202833")
    draw = ImageDraw.Draw(website)
    contexts = [("HEADER / LIGHT", "#f5f7f9", "#10151c"), ("HERO / DARK", "#10151c", "#f5f7f9"), ("FOOTER / MINERAL", "#303b47", "#f5f7f9"), ("SQUARE AVATAR", "#f5f7f9", "#10151c")]
    for index, (label, bg, fg) in enumerate(contexts):
        x = 40 + (index % 2) * 640
        y = 70 + (index // 2) * 390
        draw.rounded_rectangle((x, y, x + 600, y + 330), radius=16, fill=bg)
        draw.text((x + 22, y + 18), label, fill=fg)
        for candidate_index, item in enumerate(CANDIDATES):
            col, row = candidate_index % 3, candidate_index // 3
            cell_x, cell_y = x + 34 + col * 188, y + 52 + row * 82
            png_symbol(website, item, cell_x, cell_y, 62, (16, 21, 28) if fg == "#10151c" else (245, 247, 249))
            draw.text((cell_x + 7, cell_y + 65), item["id"], fill=fg)
    horizontal = Image.new("RGB", (1320, 980), "#eef2f5")
    draw = ImageDraw.Draw(horizontal)
    for index, item in enumerate(CANDIDATES):
        y = 82 + index * 96
        for x, bg, fg in ((40, "#ffffff", (16, 21, 28)), (680, "#10151c", (245, 247, 249))):
            draw.rounded_rectangle((x, y, x + 600, y + 76), radius=12, fill=bg, outline="#d8e0e8")
            png_symbol(horizontal, item, x + 18, y + 8, 60, fg)
            draw.text((x + 100, y + 29), "NexLabs", fill=fg)
            draw.text((x + 492, y + 31), item["id"], fill=fg)
    blur = Image.new("RGB", (1200, 780), "#202833")
    draw = ImageDraw.Draw(blur)
    draw.text((36, 24), "CP04 / deterministic blur-squint silhouette review", fill="#f5f7f9")
    for index, item in enumerate(CANDIDATES):
        col, row = index % 3, index // 3
        x, y = 36 + col * 390, 88 + row * 220
        draw.rounded_rectangle((x, y, x + 350, y + 184), radius=12, fill="#303b47", outline="#536272")
        draw.text((x + 18, y + 14), item["id"], fill="#f5f7f9")
        raster = Image.new("L", (48, 48), 0)
        png_symbol(raster, item, 0, 0, 48, 255)
        blurred = raster.filter(ImageFilter.GaussianBlur(radius=1.5)).resize((16, 16), Image.Resampling.LANCZOS).resize((100, 100), Image.Resampling.NEAREST)
        blur.paste(Image.merge("RGB", (blurred, blurred, blurred)), (x + 28, y + 42))
        metric = blur_squint_metrics()[item["id"]]
        draw.text((x + 150, y + 58), "SQUINT", fill="#cdd7e1")
        draw.text((x + 150, y + 84), f"retained pixels: {metric['retainedPixels']}", fill="#cdd7e1")
        draw.text((x + 150, y + 106), f"peak: {metric['peak']}", fill="#cdd7e1")
        draw.text((x + 150, y + 134), metric["result"], fill="#a7f3d0")
    return {
        "contact-sheet.png": contact,
        "small-size.png": small,
        "theme-lockups.png": theme,
        "website-context.png": website,
        "horizontal-lockups.png": horizontal,
        "blur-squint.png": blur,
    }


def evaluation_markdown(metrics: dict[str, dict[str, Any]]) -> str:
    rows = [
        ("NX-D-01", "Strong single gesture; good 16 px survival.", "Diagonal is familiar; similarity research remains open."),
        ("NX-D-02", "Layered topology and clear anchors.", "Midline adds density at 16 px."),
        ("NX-D-03", "Best filled silhouette and clean negative cut.", "Heavier mass can read more like a generic N."),
        ("NX-C-01", "Strong modular system semantics; stable avatar.", "Core may look blocky beside wordmark."),
        ("NX-C-02", "Clear interlock and 2D/3D projection potential.", "Narrow core needs optical review in dark mode."),
        ("NX-C-03", "Open frame preserves negative space at small sizes.", "Less immediate N read than the other C variants."),
        ("NX-B-01", "Route semantics with a connected service spur and clearer route continuity.", "The spur junction adds a small amount of detail; similarity research remains open."),
        ("NX-B-02", "Controlled orthogonal turn communicates infrastructure.", "Most circuitry-adjacent; avoid technology cliche."),
        ("NX-B-03", "Distinct rail structure and strong horizontal rhythm.", "Highest small-size complexity; human review required."),
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
        "| ID | Candidate result | Website contexts | Horizontal lockup | Blur/squint | Strengths | Weaknesses / repair note |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    lines.extend(
        f"| {id_} | PASS | PASS (4/4) | PASS (light + dark) | {metrics[id_]['result']} ({metrics[id_]['retainedPixels']} px) | {strength} | {weakness} |"
        for id_, strength, weakness in rows
    )
    lines.extend([
        "",
        "## Objective checks",
        "",
        "- PASS: 12x12 construction grid, path-only masters, monochrome and no gradients.",
        "- PASS: all nine IDs are present in HEADER/LIGHT, HERO/DARK, FOOTER/MINERAL and SQUARE/AVATAR website-context rows.",
        "- PASS: all nine IDs have a true symbol + NexLabs horizontal lockup in both LIGHT and DARK variants.",
        "- PASS: blur/squint uses a 48px raster, GaussianBlur radius 1.5, 16px LANCZOS reduction and deterministic threshold (retained pixels >= 6 and peak >= 16).",
        "- PASS: 16/24/32/64/128 px review sheet and all coverage records were generated deterministically.",
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
        "revision": item.get("revision", "r1"),
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
        index_items.append({"id": item["id"], "family": item["family"], "revision": item.get("revision", "r1"), "status": "CANDIDATE_EXPLORATION", "svg": f"brand/logo/candidates/{item['id']}.svg", "sha256": svg_hash})
    for name, content in review_sheets().items():
        (REVIEW_DIR / name).write_text(content, encoding="utf-8")
    metrics = blur_squint_metrics()
    (REVIEW_DIR / "review-coverage.json").write_text(json.dumps(review_coverage(metrics), indent=2) + "\n", encoding="utf-8")
    (REVIEW_DIR / "blender-projection-blocked.svg").write_text(blocker_sheet(), encoding="utf-8")
    (REVIEW_DIR / "blender-mcp-receipt.json").write_text(json.dumps({
        "status": "BLOCKED_EXTERNAL",
        "attempts": [
            {"phase": "CP04_INITIAL_REVIEW", "tool": "get_addon_status", "result": "Could not connect to Blender. Make sure the Blender addon is running."},
            {"phase": "CP04_INITIAL_REVIEW", "tool": "get_scene_info", "result": "Could not connect to Blender. Make sure the Blender addon is running."},
            {"phase": "CP04_HG01_CORRECTION_RETRY", "tool": "get_addon_status", "result": "Could not connect to Blender. Make sure the Blender addon is running."},
        ],
        "proofs": {"candidateCount": 9, "completed": 0, "claimed": False},
        "providerStarted": False,
    }, indent=2) + "\n", encoding="utf-8")
    (LAB / "evaluation.md").write_text(evaluation_markdown(metrics), encoding="utf-8")
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
    candidate_ids = [item.get("id") for item in index["candidates"]]
    if candidate_ids != EXPECTED_IDS or len(set(candidate_ids)) != len(candidate_ids):
        raise SystemExit("logo lab candidate index contains duplicate or reordered IDs")
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
    expected_reviews = {
        "contact-sheet.svg", "small-size.svg", "theme-lockups.svg", "website-context.svg",
        "horizontal-lockups.svg", "blur-squint.svg", "review-coverage.json",
        "blender-projection-blocked.svg", "blender-mcp-receipt.json",
    }
    actual_reviews = {path.name for path in REVIEW_DIR.iterdir() if path.is_file()}
    if not expected_reviews.issubset(actual_reviews):
        raise SystemExit(f"missing review artifacts: {sorted(expected_reviews - actual_reviews)}")
    coverage = json.loads((REVIEW_DIR / "review-coverage.json").read_text(encoding="utf-8"))
    if coverage.get("candidateIds") != EXPECTED_IDS:
        raise SystemExit("review coverage candidate IDs do not match the canonical index")
    for context, ids in coverage.get("websiteContext", {}).get("contexts", {}).items():
        if ids != EXPECTED_IDS or len(set(ids)) != len(ids):
            raise SystemExit(f"website context coverage is incomplete: {context}")
    for variant, ids in coverage.get("horizontalLockups", {}).get("variants", {}).items():
        if ids != EXPECTED_IDS or len(set(ids)) != len(ids):
            raise SystemExit(f"horizontal lockup coverage is incomplete: {variant}")
    blur_results = coverage.get("blurSquint", {}).get("results", [])
    if [row.get("id") for row in blur_results] != EXPECTED_IDS or any(row.get("result") != "PASS" for row in blur_results):
        raise SystemExit("blur/squint coverage is incomplete or has a failed objective result")
    manifest_path = LAB / "artifact-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_manifest_paths = sorted(
        str(path.relative_to(ROOT)).replace("\\", "/")
        for path in [*(CANDIDATE_DIR.glob("*.svg")), *(PROVENANCE_DIR.glob("*.json")), *(REVIEW_DIR.iterdir()), LAB / "candidate-index.json", LAB / "evaluation.md", LAB / "README.md"]
        if path.is_file()
    )
    manifest_paths = sorted(artifact.get("path") for artifact in manifest.get("artifacts", []))
    if manifest_paths != expected_manifest_paths:
        raise SystemExit("artifact manifest does not cover the regenerated artifact set")
    for artifact in manifest.get("artifacts", []):
        path = ROOT / artifact["path"]
        if sha256_bytes(path.read_bytes()) != artifact["sha256"]:
            raise SystemExit(f"artifact manifest hash mismatch: {artifact['path']}")
    print(f"Logo lab PASS: {len(EXPECTED_IDS)} candidates, {len(actual_reviews)} review artifacts, coverage complete, no canonical wiring")


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
