"""Create deterministic CP-08 social cards and responsive image derivatives."""
from __future__ import annotations

import hashlib
import json
import platform
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageStat, features

ROOT = Path(__file__).resolve().parents[2]
ACCEPTANCE = ROOT / "artifacts/cp06/cp06-asset-acceptance.json"
TOKENS = ROOT / "public/brand/tokens.json"
SITE = ROOT / "content/site/site.json"
LOGO = ROOT / "brand/logo/candidates/NX-C-02.svg"
SOURCE_IMAGE = ROOT / "artifacts/cp06/static/hero-16x9.png"
OUTPUT_DIR = ROOT / "public/release-visuals"
ARTIFACT_DIR = ROOT / "artifacts/cp08"
REGULAR_FONT = Path("C:/Windows/Fonts/segoeui.ttf")
SEMIBOLD_FONT = Path("C:/Windows/Fonts/seguisb.ttf")
MAX_PARITY_ERROR_PERCENT = 3.0

STATIC_SOURCES = {
    "16x9": ("hero16x9", "hero-16x9.png", "context-core-16x9"),
    "4x5": ("hero4x5", "hero-4x5.png", "context-core-4x5"),
    "1x1": ("hero1x1", "hero-1x1.png", "context-core-1x1"),
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def hex_rgb(value: str) -> tuple[int, int, int]:
    value = value.removeprefix("#")
    return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))  # type: ignore[return-value]


def blend(start: tuple[int, int, int], end: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    return tuple(round(a + (b - a) * amount) for a, b in zip(start, end))  # type: ignore[return-value]


def load_theme() -> dict[str, str]:
    colors = read_json(TOKENS)["primitives"]["color"]
    return {
        "background": colors["neutral"]["950"]["dark"],
        "surface": colors["neutral"]["850"]["dark"],
        "text": colors["neutral"]["50"]["dark"],
        "muted": colors["neutral"]["300"]["dark"],
        "cyan": colors["spectral"]["400"]["dark"],
        "violet": colors["violet"]["400"]["dark"],
        "logo": "#10151c",
        "logoPlate": colors["neutral"]["50"]["dark"],
    }


def load_logo() -> tuple[list[list[tuple[float, float]]], str, str]:
    raw = LOGO.read_bytes()
    root = ET.fromstring(raw)
    view_box = root.attrib.get("viewBox", "0 0 120 120").split()
    if view_box != ["0", "0", "120", "120"]:
        raise ValueError("NX-C-02 source viewBox changed")
    paths: list[list[tuple[float, float]]] = []
    fill = ""
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1] != "path":
            continue
        data = element.attrib.get("d", "")
        tokens = re.findall(r"[MLZmlz]|[-+]?(?:\d*\.)?\d+", data)
        points: list[tuple[float, float]] = []
        index = 0
        while index < len(tokens):
            command = tokens[index].upper()
            index += 1
            if command == "Z":
                continue
            if command not in {"M", "L"} or index + 1 >= len(tokens):
                raise ValueError("NX-C-02 path contains unsupported geometry")
            points.append((float(tokens[index]), float(tokens[index + 1])))
            index += 2
        if len(points) < 3:
            raise ValueError("NX-C-02 contains an invalid path")
        paths.append(points)
        fill = fill or element.attrib.get("fill", "")
    if not paths or not fill:
        raise ValueError("NX-C-02 source paths or original fill are missing")
    return paths, fill, hashlib.sha256(raw).hexdigest()


def draw_logo(canvas: Image.Image, paths: list[list[tuple[float, float]]], fill: str, box: tuple[int, int, int, int]) -> None:
    x, y, width, height = box
    scale = min(width, height) / 120
    inset_x = x + (width - 120 * scale) / 2
    inset_y = y + (height - 120 * scale) / 2
    factor = 3
    layer = Image.new("RGBA", (canvas.width * factor, canvas.height * factor), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for points in paths:
        draw.polygon(
            [((inset_x + px * scale) * factor, (inset_y + py * scale) * factor) for px, py in points],
            fill=fill,
        )
    layer = layer.resize(canvas.size, Image.Resampling.LANCZOS)
    canvas.alpha_composite(layer)


def font(size: int, semibold: bool = False) -> ImageFont.FreeTypeFont:
    path = SEMIBOLD_FONT if semibold else REGULAR_FONT
    if not path.is_file():
        raise FileNotFoundError(f"Canonical Segoe UI font is unavailable: {path.name}")
    return ImageFont.truetype(str(path), size=size)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, typeface: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if current and draw.textbbox((0, 0), candidate, font=typeface)[2] > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def base_card(width: int, height: int, accent: str, theme: dict[str, str]) -> Image.Image:
    top = hex_rgb(theme["background"])
    bottom = hex_rgb("#111820")
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)
    for y in range(height):
        draw.line((0, y, width, y), fill=blend(top, bottom, y / max(1, height - 1)))
    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    ar, ag, ab = hex_rgb(accent)
    glow_draw.ellipse((width * 0.52, height * 0.05, width * 1.12, height * 1.04), fill=(ar, ag, ab, 35))
    image = Image.alpha_composite(image.convert("RGBA"), glow.filter(ImageFilter.GaussianBlur(radius=70)))
    return image


def draw_card(
    *,
    width: int,
    height: int,
    title: str,
    description: str,
    footer: str,
    source_image: Path,
    theme: dict[str, str],
    logo_paths: list[list[tuple[float, float]]],
    logo_fill: str,
    accent: str,
) -> tuple[Image.Image, dict[str, Any]]:
    scale = width / 1200
    canvas = base_card(width, height, accent, theme)
    draw = ImageDraw.Draw(canvas)
    x = round(68 * scale)
    badge = round(48 * scale)
    y_brand = round(48 * scale)
    draw.rounded_rectangle((x, y_brand, x + badge, y_brand + badge), radius=round(12 * scale), fill=theme["logoPlate"])
    draw_logo(canvas, logo_paths, logo_fill, (x + round(8 * scale), y_brand + round(8 * scale), badge - round(16 * scale), badge - round(16 * scale)))
    draw = ImageDraw.Draw(canvas)
    draw.text((x + badge + round(14 * scale), y_brand + round(6 * scale)), "NexLabs", font=font(round(26 * scale), True), fill=theme["text"])

    accent_rgb = hex_rgb(accent)
    eyebrow = read_json(SITE)["hero"]["eyebrow"]
    eyebrow_font = font(round(13 * scale), True)
    eyebrow_y = round(142 * scale)
    draw.text((x, eyebrow_y), eyebrow, font=eyebrow_font, fill=accent_rgb)

    title_font = font(round(46 * scale), True)
    title_y = round(174 * scale)
    title_lines = wrap_text(draw, title, title_font, round(520 * scale))
    title_line_height = round(54 * scale)
    for line_number, line in enumerate(title_lines):
        draw.text((x, title_y + line_number * title_line_height), line, font=title_font, fill=theme["text"])
    description_font = font(round(18 * scale))
    description_y = title_y + len(title_lines) * title_line_height + round(13 * scale)
    description_lines = wrap_text(draw, description, description_font, round(525 * scale))
    description_line_height = round(27 * scale)
    for line_number, line in enumerate(description_lines):
        draw.text((x, description_y + line_number * description_line_height), line, font=description_font, fill=theme["muted"])
    text_bottom = description_y + len(description_lines) * description_line_height

    panel_x, panel_y = round(644 * scale), round(151 * scale)
    panel_w, panel_h = round(516 * scale), round(326 * scale)
    draw.rounded_rectangle(
        (panel_x, panel_y, panel_x + panel_w, panel_y + panel_h),
        radius=round(20 * scale),
        fill=theme["surface"],
        outline="#2a3a48",
        width=max(1, round(scale)),
    )
    with Image.open(source_image) as source:
        source_rgb = source.convert("RGB")
        source_rgb.thumbnail((round(468 * scale), round(264 * scale)), Image.Resampling.LANCZOS)
        mask = Image.new("L", source_rgb.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, source_rgb.width - 1, source_rgb.height - 1), radius=round(12 * scale), fill=255)
        image_x = panel_x + (panel_w - source_rgb.width) // 2
        image_y = panel_y + (panel_h - source_rgb.height) // 2
        canvas.paste(source_rgb, (image_x, image_y), mask)
    draw = ImageDraw.Draw(canvas)
    draw.line((x, height - round(70 * scale), width - x, height - round(70 * scale)), fill="#2a3a48", width=1)
    footer_font = font(round(13 * scale))
    footer_y = height - round(48 * scale)
    draw.text((x, footer_y), footer, font=footer_font, fill=theme["muted"])
    draw.ellipse((width - x - round(8 * scale), footer_y + round(4 * scale), width - x, footer_y + round(12 * scale)), fill=accent_rgb)
    bounds = {
        "safeMarginPx": round(64 * scale),
        "textBounds": {"left": x, "top": eyebrow_y, "right": x + round(525 * scale), "bottom": text_bottom},
        "titleLineCount": len(title_lines),
        "descriptionLineCount": len(description_lines),
        "titleLines": title_lines,
        "descriptionLines": description_lines,
        "sourceImageBox": [image_x, image_y, source_rgb.width, source_rgb.height],
    }
    return canvas.convert("RGB"), bounds


def output_details(path: Path) -> dict[str, Any]:
    with Image.open(path) as image:
        image.load()
        return {
            "path": relative(path),
            "format": image.format,
            "width": image.width,
            "height": image.height,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }


def image_source(path: Path) -> dict[str, Any]:
    with Image.open(path) as image:
        return {"path": relative(path), "sha256": sha256(path), "bytes": path.stat().st_size, "width": image.width, "height": image.height}


def asset_record(
    asset_id: str,
    status: str,
    purpose: str,
    destinations: list[str],
    references: list[dict[str, Any]],
    output: dict[str, Any],
    notes: list[str],
    *,
    alt_text: str,
    composition: dict[str, Any] | None = None,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "asset_id": asset_id,
        "version": "v001",
        "status": status,
        "purpose": purpose,
        "brand_spec_revision": "KayzenRoot/nexlabs-startup@b541e802472a3acc75a3a8ebd3818d33de8a316f",
        "source": {"type": "procedural", "references": references},
        "ugas": {"workflow": None, "workflow_version": None, "notes": "UGAS was not used; deterministic local composition/encoding only."},
        "blender": {"source_file": None, "source_revision": None},
        "rights": {
            "provenance_reviewed": True,
            "external_inputs": [],
            "notes": "Derived only from tracked, approved NexLabs source assets and canonical repository copy/tokens.",
        },
        "outputs": [output],
        "destinations": destinations,
        "alt_text": alt_text,
        "approved_by": None,
        "approved_at": None,
        "approval_status": "NOT_INDEPENDENTLY_REVIEWED",
        "review_state": "CP08_IN_PROGRESS",
        "notes": notes,
    }
    if composition:
        record["composition"] = composition
    return record


def save_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_social_template(theme: dict[str, str], logo_fill: str) -> Path:
    template_dir = ARTIFACT_DIR / "templates"
    template_dir.mkdir(parents=True, exist_ok=True)
    path = template_dir / "social-card.svg"
    logo_file = ET.parse(LOGO).getroot()
    paths = "\n".join(
        f'<path d="{element.attrib["d"]}" fill="{logo_fill}" fill-rule="{element.attrib.get("fill-rule", "nonzero")}"/>'
        for element in logo_file.iter()
        if element.tag.rsplit("}", 1)[-1] == "path"
    )
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" role="img" aria-label="NexLabs reusable social card layout">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{theme["background"]}"/><stop offset="1" stop-color="#111820"/></linearGradient>
    <radialGradient id="glow"><stop stop-color="{theme["cyan"]}" stop-opacity=".20"/><stop offset="1" stop-color="{theme["cyan"]}" stop-opacity="0"/></radialGradient>
    <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="{theme["muted"]}" stroke-opacity=".08"/></pattern>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/><rect width="1200" height="630" fill="url(#grid)"/>
  <ellipse cx="970" cy="315" rx="360" ry="310" fill="url(#glow)"/>
  <rect x="68" y="48" width="48" height="48" rx="12" fill="{theme["logoPlate"]}"/>
  <g transform="translate(76 56) scale(.35)">{paths}</g>
  <text x="130" y="82" fill="{theme["text"]}" font-family="Segoe UI, sans-serif" font-size="26" font-weight="600">NexLabs</text>
  <path d="M68 530H1132" stroke="{theme["muted"]}" stroke-opacity=".32"/>
  <rect x="660" y="145" width="500" height="330" rx="20" fill="{theme["surface"]}" fill-opacity=".48" stroke="{theme["muted"]}" stroke-opacity=".22"/>
</svg>
'''
    path.write_text(content, encoding="utf-8", newline="\n")
    return path


def create_contact_sheet(card_paths: list[Path], labels: list[str], theme: dict[str, str]) -> Path:
    sheet_dir = ARTIFACT_DIR / "contact-sheets"
    sheet_dir.mkdir(parents=True, exist_ok=True)
    width, height = 1080, 720
    canvas = Image.new("RGB", (width, height), hex_rgb(theme["background"]))
    draw = ImageDraw.Draw(canvas)
    draw.text((32, 24), "NexLabs release visuals", font=font(27, True), fill=theme["text"])
    positions = [(32, 82), (552, 82), (32, 400), (552, 400)]
    for path, label, (x, y) in zip(card_paths, labels, positions):
        with Image.open(path) as image:
            preview = image.convert("RGB")
            preview.thumbnail((496, 279), Image.Resampling.LANCZOS)
            canvas.paste(preview, (x, y))
        draw = ImageDraw.Draw(canvas)
        draw.text((x, y + 286), label, font=font(15, True), fill=theme["muted"])
    path = sheet_dir / "cp08-contact-sheet.png"
    canvas.save(path, format="PNG", optimize=True, compress_level=9)
    return path


def main() -> int:
    acceptance = read_json(ACCEPTANCE)
    site = read_json(SITE)
    theme = load_theme()
    logo_paths, logo_fill, logo_sha = load_logo()
    source_by_id = {entry["path"]: entry for entry in [image_source(SOURCE_IMAGE)]}
    source_by_id[relative(TOKENS)] = {"path": relative(TOKENS), "sha256": sha256(TOKENS), "bytes": TOKENS.stat().st_size}
    source_by_id[relative(SITE)] = {"path": relative(SITE), "sha256": sha256(SITE), "bytes": SITE.stat().st_size}
    source_by_id[relative(LOGO)] = {"path": relative(LOGO), "sha256": logo_sha, "bytes": LOGO.stat().st_size}
    source_by_id[relative(ACCEPTANCE)] = {"path": relative(ACCEPTANCE), "sha256": sha256(ACCEPTANCE), "bytes": ACCEPTANCE.stat().st_size}
    source_by_id["artifacts/cp07/cp07-runtime-manifest.json"] = {
        "path": "artifacts/cp07/cp07-runtime-manifest.json",
        "sha256": sha256(ROOT / "artifacts/cp07/cp07-runtime-manifest.json"),
        "bytes": (ROOT / "artifacts/cp07/cp07-runtime-manifest.json").stat().st_size,
    }

    for key, filename, _ in STATIC_SOURCES.values():
        accepted = acceptance["staticFallback"][key]
        path = ROOT / accepted["path"]
        if sha256(path) != accepted["sha256"]:
            raise ValueError(f"accepted CP-06 source changed: {accepted['path']}")
        public_copy = ROOT / "public/images/context-core" / filename
        if public_copy.read_bytes() != path.read_bytes():
            raise ValueError(f"CP-07 promoted source differs from accepted CP-06 bytes: {public_copy}")
        source_by_id[relative(path)] = image_source(path)
        source_by_id[relative(public_copy)] = image_source(public_copy)

    card_specs = [
        ("default", "/", "nexlabs.png", theme["cyan"]),
        ("hive", "/hive", "hive.png", theme["violet"]),
        ("technology", "/technology", "technology.png", theme["cyan"]),
    ]
    og_dir = OUTPUT_DIR / "og"
    og_dir.mkdir(parents=True, exist_ok=True)
    asset_records: list[dict[str, Any]] = []
    cards: list[Path] = []
    card_labels: list[str] = []
    for name, route, filename, accent in card_specs:
        route_data = next(item for item in site["routes"] if item["path"] == route)
        target = og_dir / filename
        image, composition = draw_card(
            width=1200,
            height=630,
            title=route_data["title"],
            description=route_data["description"],
            footer=site["identity"]["corporateName"],
            source_image=SOURCE_IMAGE,
            theme=theme,
            logo_paths=logo_paths,
            logo_fill=logo_fill,
            accent=accent,
        )
        image.save(target, format="PNG", optimize=True, compress_level=9)
        refs = [source_by_id[relative(SOURCE_IMAGE)], source_by_id[relative(TOKENS)], source_by_id[relative(SITE)], source_by_id[relative(LOGO)]]
        asset_records.append(asset_record(
            f"NL_CP08_OG_{name.upper()}",
            "PRODUCTION",
            f"Open Graph visual for the existing {route} destination.",
            [route],
            refs,
            output_details(target),
            ["Canonical title and description are rendered without copy edits.", "Social card is supporting media; equivalent page content remains available as HTML."],
            alt_text=f"{route_data['title']}. {route_data['description']}",
            composition={**composition, "visibleText": {"eyebrow": site["hero"]["eyebrow"], "title": route_data["title"], "description": route_data["description"], "footer": site["identity"]["corporateName"]}},
        ))
        cards.append(target)
        card_labels.append(f"{route} | {route_data['title']}")

    repo_route = "https://github.com/KayzenRoot/nexlabs-web"
    default_route = next(item for item in site["routes"] if item["path"] == "/")
    repo_preview = OUTPUT_DIR / "social-preview/github-repository.png"
    repo_preview.parent.mkdir(parents=True, exist_ok=True)
    repo_image, repo_composition = draw_card(
        width=1280,
        height=640,
        title=site["hero"]["heading"],
        description=default_route["description"],
        footer="github.com/KayzenRoot/nexlabs-web",
        source_image=SOURCE_IMAGE,
        theme=theme,
        logo_paths=logo_paths,
        logo_fill=logo_fill,
        accent=theme["violet"],
    )
    repo_image.save(repo_preview, format="PNG", optimize=True, compress_level=9)
    asset_records.append(asset_record(
        "NL_CP08_SOCIAL_GITHUB_REPOSITORY",
        "PRODUCTION",
        "GitHub repository social-preview image; asset is prepared but not uploaded as a release action.",
        [repo_route],
        [source_by_id[relative(SOURCE_IMAGE)], source_by_id[relative(TOKENS)], source_by_id[relative(SITE)], source_by_id[relative(LOGO)]],
        output_details(repo_preview),
        ["Uses the canonical homepage heading and description.", "No fabricated social account, handle or proof is included."],
        alt_text=f"{site['hero']['heading']} {default_route['description']}",
        composition={**repo_composition, "visibleText": {"title": site["hero"]["heading"], "description": default_route["description"], "footer": "github.com/KayzenRoot/nexlabs-web"}},
    ))
    cards.append(repo_preview)
    card_labels.append("GitHub repository | " + repo_route.removeprefix("https://"))

    compression_rows: list[dict[str, Any]] = []
    hero_dir = OUTPUT_DIR / "hero"
    hero_dir.mkdir(parents=True, exist_ok=True)
    for ratio, (acceptance_key, filename, stem) in STATIC_SOURCES.items():
        accepted = acceptance["staticFallback"][acceptance_key]
        source = ROOT / accepted["path"]
        with Image.open(source) as original:
            if original.width / original.height not in (1.0, 4 / 5, 16 / 9) and abs(original.width / original.height - {"16x9": 16 / 9, "4x5": 4 / 5, "1x1": 1.0}[ratio]) > 0.01:
                raise ValueError(f"source ratio mismatch for {ratio}: {original.size}")
            source_image = original.convert("RGB")
            original_size = source_image.size
            original_bytes = source.stat().st_size
            variants = []
            if features.check("webp"):
                webp_path = hero_dir / f"{stem}.webp"
                source_image.save(webp_path, format="WEBP", quality=88, method=6, exact=True)
                variants.append((webp_path, "WEBP", {"quality": 88, "method": 6, "exact": True}))
            if features.check("avif"):
                avif_path = hero_dir / f"{stem}.avif"
                source_image.save(avif_path, format="AVIF", quality=58, speed=6)
                variants.append((avif_path, "AVIF", {"quality": 58, "speed": 6}))
            if not variants:
                raise RuntimeError("Neither deterministic WebP nor AVIF encoding is available")
            source_rgb = source_image.convert("RGB")
        source_ref = source_by_id[relative(source)]
        public_ref = source_by_id[relative(ROOT / "public/images/context-core" / filename)]
        for variant_path, variant_format, settings in variants:
            with Image.open(variant_path) as encoded:
                encoded.load()
                if encoded.size != original_size or encoded.format != variant_format:
                    raise ValueError(f"encoded hero size/format mismatch: {variant_path}")
                parity = ImageStat.Stat(ImageChops.difference(source_rgb, encoded.convert("RGB"))).mean
                normalized_mae = round(sum(parity) / (3 * 255) * 100, 4)
                if normalized_mae > MAX_PARITY_ERROR_PERCENT:
                    raise ValueError(f"visual parity error exceeds budget for {variant_path}: {normalized_mae}%")
                if any(key in encoded.info for key in ("exif", "icc_profile", "xmp", "comment")):
                    raise ValueError(f"nonessential metadata was not stripped: {variant_path}")
            details = output_details(variant_path)
            if details["bytes"] >= original_bytes:
                raise ValueError(f"optimized hero is not smaller than accepted PNG: {variant_path}")
            compression = {
                "sourcePath": relative(source),
                "sourceBytes": original_bytes,
                "sourceSha256": accepted["sha256"],
                "outputPath": details["path"],
                "outputBytes": details["bytes"],
                "outputSha256": details["sha256"],
                "format": variant_format,
                "settings": settings,
                "normalizedMeanAbsoluteErrorPercent": normalized_mae,
                "sizeChangePercent": round((details["bytes"] - original_bytes) / original_bytes * 100, 2),
                "dimensions": list(original_size),
            }
            compression_rows.append(compression)
            asset_records.append(asset_record(
                f"NL_CP08_HERO_{ratio.upper()}_{variant_format}",
                "OPTIMIZED",
                f"Responsive static Context Core hero delivery derivative ({ratio}, {variant_format}).",
                ["homepage hero responsive static fallback"],
                [source_ref, public_ref, source_by_id[relative(ACCEPTANCE)], source_by_id["artifacts/cp07/cp07-runtime-manifest.json"]],
                details,
                [f"Deterministic Pillow {variant_format} encoding with {settings}.", "Source framing and pixel dimensions are preserved; no upscaling; accepted PNG sources remain unchanged."],
                alt_text="Decorative responsive still from the Context Core visual system; all explanatory website content remains in HTML.",
                composition={"sourceDimensions": list(original_size), "outputDimensions": [details["width"], details["height"]], "upscaled": False, "visualParityNormalizedMaePercent": normalized_mae, "visualParityMaximumPercent": MAX_PARITY_ERROR_PERCENT},
            ))

    template = write_social_template(theme, logo_fill)
    template_details: dict[str, Any] = {
        "path": relative(template), "format": "SVG", "width": 1200, "height": 630,
        "bytes": template.stat().st_size, "sha256": sha256(template),
    }
    asset_records.append(asset_record(
        "NL_CP08_TEMPLATE_GENERIC_SOCIAL",
        "PRODUCTION",
        "Reusable NexLabs social-card layout for future verified destinations.",
        [],
        [source_by_id[relative(TOKENS)], source_by_id[relative(LOGO)]],
        template_details,
        ["Generic layout only; no destination-specific campaign, account, handle or social-proof copy."],
        alt_text="Reusable NexLabs social-card layout for a future verified destination.",
    ))

    contact_sheet = create_contact_sheet(cards, card_labels, theme)
    contact_details = output_details(contact_sheet)
    contact_refs = [output_details(path) for path in cards]
    asset_records.append(asset_record(
        "NL_CP08_CONTACT_SHEET",
        "OPTIMIZED",
        "Human inspection contact sheet for the three Open Graph cards and repository preview.",
        [],
        [{"path": row["path"], "sha256": row["sha256"], "bytes": row["bytes"]} for row in contact_refs],
        contact_details,
        ["Review aid only; not a user-facing information channel."],
        alt_text="Contact sheet for human inspection of three Open Graph cards and one GitHub repository preview.",
    ))

    route_assets = {
        route: {
            "path": f"/release-visuals/og/{filename}",
            "title": next(item["title"] for item in site["routes"] if item["path"] == route),
            "description": next(item["description"] for item in site["routes"] if item["path"] == route),
        }
        for _, route, filename, _ in card_specs
    }
    size_report = ARTIFACT_DIR / "cp08-size-report.md"
    table_rows = [
        "| Variant | Source bytes | Output bytes | Change | Output SHA-256 |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for row in compression_rows:
        table_rows.append(f"| {row['outputPath']} | {row['sourceBytes']} | {row['outputBytes']} | {row['sizeChangePercent']}% | `{row['outputSha256']}` |")
    size_report.write_text("# CP-08 image optimization\n\n" + "\n".join(table_rows) + "\n", encoding="utf-8", newline="\n")

    manifest = {
        "schemaVersion": "nexlabs-web-cp08-asset-manifest-v1",
        "workOrder": "NXWEB-WO-0007-CP08-UGAS-DERIVATIVE-MEDIA-RELEASE-VISUALS",
        "status": "PRODUCTION_AND_OPTIMIZED_NOT_RELEASED",
        "releaseStatus": "NOT_RELEASED",
        "generationMode": "DETERMINISTIC_NO_GENERATION",
        "sourceCommit": "d971047d25dc01e7338aba369ea1bd7cf7452490",
        "sourceDocumentSha256": "b89cc978f695cd990ae3d4d8a473af5df53b47ea161411d7432e782c65718990",
        "planningSource": "KayzenRoot/nexlabs-startup@b541e802472a3acc75a3a8ebd3818d33de8a316f",
        "tools": {
            "python": platform.python_version(),
            "pillow": Image.__version__ if hasattr(Image, "__version__") else __import__("PIL").__version__,
            "fontFamily": "Segoe UI",
            "fontRegularSha256": sha256(REGULAR_FONT),
            "fontSemiboldSha256": sha256(SEMIBOLD_FONT),
            "webpAvailable": features.check("webp"),
            "avifAvailable": features.check("avif"),
        },
        "sourceInputs": sorted(source_by_id.values(), key=lambda item: item["path"]),
        "canonicalDestinations": route_assets,
        "assets": asset_records,
        "compression": compression_rows,
        "reports": {
            "contactSheet": relative(contact_sheet),
            "sizeReport": relative(size_report),
            "gateReport": "artifacts/cp08/cp08-gate-report.json",
            "humanGateReport": "artifacts/cp08/cp08-gate-report.md",
        },
        "boundaries": {
            "ugasProviderStarted": False,
            "ugasGenerationPerformed": False,
            "externalInputs": [],
            "identityChanged": False,
            "released": False,
            "deployed": False,
            "merged": False,
            "cp09Started": False,
        },
    }
    save_json(ARTIFACT_DIR / "cp08-asset-manifest.json", manifest)
    print(json.dumps({"assets": len(asset_records), "manifest": relative(ARTIFACT_DIR / "cp08-asset-manifest.json"), "contactSheet": relative(contact_sheet), "responsiveVariants": len(compression_rows)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
