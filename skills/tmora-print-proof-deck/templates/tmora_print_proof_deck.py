#!/usr/bin/env python3
"""Generate a TMORA print proof PDF deck from a folder of print assets.

Dependencies:
  python3 -m pip install pillow reportlab

Example:
  python3 tmora_print_proof_deck.py \
    --source-root "/path/to/print files" \
    --metadata metadata.example.json \
    --output-dir output/pdf
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


PAGE_W = 990
PAGE_H = 765
MARGIN_X = 70
FOOTER_Y = 44
CARD_SHORT = 116
CARD_LONG = 174

CHARCOAL = "#2A2725"
GOLD = "#B19149"
GOLD_SOFT = "#8F7437"
CREAM = "#F4EFE6"
MUTED = "#BEB5AA"
PAPER = "#FFFFFF"
RECOMMENDED_GREEN = "#5D7F59"

DEFAULT_CODE_ORDER = ["TMORA108", "TMORA109", "TMORA110", "TMORA111", "TMORA112", "TMORA113"]
DEFAULT_BACK_PREFIX_TO_CODE = {
    "01-": "TMORA108",
    "02-": "TMORA109",
    "03-": "TMORA110",
    "04-": "TMORA111",
    "05-": "TMORA112",
    "06-": "TMORA113",
}


@dataclass(frozen=True)
class ProofAsset:
    path: Path
    code: str
    kind: str
    size_label: str
    option_label: str
    width: int
    height: int
    optimized_path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a TMORA print proof PDF deck.")
    parser.add_argument("--source-root", required=True, type=Path, help="Folder containing proof images.")
    parser.add_argument("--output-dir", default=Path("output/pdf"), type=Path, help="Directory for PDF and manifest.")
    parser.add_argument("--tmp-dir", default=Path("tmp/pdfs/tmora-print-proof-deck"), type=Path, help="Intermediate image directory.")
    parser.add_argument("--metadata", type=Path, help="Optional metadata JSON. See metadata.example.json.")
    parser.add_argument("--output-name", default="TMORA_Print_Proofs_and_Options.pdf", help="PDF filename.")
    parser.add_argument("--manifest-name", default="TMORA_Print_Proofs_manifest.csv", help="CSV manifest filename.")
    parser.add_argument("--title", default="Print Proofs and Options", help="Cover title.")
    parser.add_argument("--date", default="", help="Optional cover date text.")
    parser.add_argument("--prepared-by", default="", help="Optional prepared-by text on cover.")
    return parser.parse_args()


def load_metadata(path: Path | None) -> dict:
    if not path:
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def rgb(value: str) -> tuple[float, float, float]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) / 255 for i in (0, 2, 4))


def fill(c: canvas.Canvas, color: str) -> None:
    c.setFillColorRGB(*rgb(color))


def stroke(c: canvas.Canvas, color: str) -> None:
    c.setStrokeColorRGB(*rgb(color))


def register_fonts() -> tuple[str, str, str, str]:
    font_candidates = {
        "regular": [
            Path("/System/Library/Fonts/Supplemental/Georgia.ttf"),
            Path("/Library/Fonts/Georgia.ttf"),
        ],
        "bold": [
            Path("/System/Library/Fonts/Supplemental/Georgia Bold.ttf"),
            Path("/Library/Fonts/Georgia Bold.ttf"),
        ],
        "italic": [
            Path("/System/Library/Fonts/Supplemental/Georgia Italic.ttf"),
            Path("/Library/Fonts/Georgia Italic.ttf"),
        ],
    }

    def first_existing(paths: list[Path]) -> Path | None:
        return next((p for p in paths if p.exists()), None)

    regular = first_existing(font_candidates["regular"])
    bold = first_existing(font_candidates["bold"])
    italic = first_existing(font_candidates["italic"])
    if regular:
        pdfmetrics.registerFont(TTFont("TMORA-Serif", str(regular)))
        serif = "TMORA-Serif"
    else:
        serif = "Times-Roman"
    if bold:
        pdfmetrics.registerFont(TTFont("TMORA-Serif-Bold", str(bold)))
        serif_bold = "TMORA-Serif-Bold"
    else:
        serif_bold = "Times-Bold"
    if italic:
        pdfmetrics.registerFont(TTFont("TMORA-Serif-Italic", str(italic)))
        serif_italic = "TMORA-Serif-Italic"
    else:
        serif_italic = "Times-Italic"
    return serif, serif_bold, serif_italic, "Helvetica"


SERIF, SERIF_BOLD, SERIF_ITALIC, SANS = register_fonts()
SANS_BOLD = "Helvetica-Bold"


def wrap(text: str, font: str, size: float, max_w: float) -> list[str]:
    lines: list[str] = []
    line = ""
    for word in text.split():
        candidate = f"{line} {word}".strip()
        if not line or pdfmetrics.stringWidth(candidate, font, size) <= max_w:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_wrapped(c: canvas.Canvas, text: str, x: float, y: float, max_w: float, font: str, size: float, leading: float, color: str) -> float:
    fill(c, color)
    c.setFont(font, size)
    for line in wrap(text, font, size, max_w):
        c.drawString(x, y, line)
        y -= leading
    return y


def page_base(c: canvas.Canvas, footer_label: str, show_footer: bool = True) -> None:
    fill(c, CHARCOAL)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    if not show_footer:
        return
    stroke(c, GOLD_SOFT)
    c.setLineWidth(0.45)
    c.line(MARGIN_X, FOOTER_Y + 17, PAGE_W - MARGIN_X, FOOTER_Y + 17)
    fill(c, MUTED)
    c.setFont(SANS, 8)
    c.drawString(MARGIN_X, FOOTER_Y, footer_label)


def infer_code(path: Path, code_order: list[str], back_prefix_to_code: dict[str, str]) -> str:
    upper = path.name.upper()
    for code in code_order:
        if code.upper() in upper:
            return code
    lower_name = path.name.lower()
    if "postcard backs" in str(path).lower():
        for prefix, code in back_prefix_to_code.items():
            if lower_name.startswith(prefix.lower()):
                return code
    return path.stem.split("-")[0].upper()


def infer_kind(path: Path) -> str:
    parts = [p.lower() for p in path.parts]
    if "11x17" in parts and "info cards" in parts:
        return "11x17 info card"
    if "11x17" in parts:
        return "11x17 print"
    if "backs-info-card" in parts:
        return "4x6 info back"
    if "backs-postal-landscape" in parts:
        return "4x6 postal back"
    if "postcard fronts" in parts:
        return "4x6 front"
    name = path.name.lower()
    if "postal" in name:
        return "4x6 postal back"
    if "back" in name:
        return "4x6 info back"
    if "4x6" in name:
        return "4x6 front"
    if "11x17" in name:
        return "11x17 print"
    return "print file"


def infer_size(kind: str) -> str:
    if kind.startswith("11x17"):
        return "11x17 in."
    if kind.startswith("4x6"):
        return "4x6 in."
    return ""


def infer_option(path: Path, kind: str) -> str:
    name = path.stem.lower()
    if "option-a" in name or name.endswith("-a"):
        return "A"
    if "option-b" in name or name.endswith("-b"):
        return "B"
    if "postal" in kind:
        return "Postal back"
    if "info back" in kind:
        return "Info back"
    if "info card" in kind:
        return "Info card"
    return "Front"


def optimize(src: Path, tmp_dir: Path) -> tuple[Path, int, int]:
    optimized_dir = tmp_dir / "optimized"
    optimized_dir.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha1(str(src).encode("utf-8")).hexdigest()[:10]
    dst = optimized_dir / f"{src.stem}-{digest}.jpg"
    with Image.open(src) as im:
        if im.mode in ("RGBA", "LA") or "transparency" in im.info:
            bg = Image.new("RGB", im.size, "white")
            rgba = im.convert("RGBA")
            bg.paste(rgba, mask=rgba.split()[-1])
            im = bg
        else:
            im = im.convert("RGB")
        w, h = im.size
        max_dim = 2400
        if max(w, h) > max_dim:
            ratio = max_dim / max(w, h)
            im = im.resize((round(w * ratio), round(h * ratio)), Image.Resampling.LANCZOS)
        im.save(dst, "JPEG", quality=92, optimize=True, progressive=True)
    return dst, w, h


def collect_assets(source_root: Path, tmp_dir: Path, code_order: list[str], back_prefix_to_code: dict[str, str]) -> list[ProofAsset]:
    paths = sorted(p for p in source_root.rglob("*") if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".tif", ".tiff"})
    assets: list[ProofAsset] = []
    for path in paths:
        kind = infer_kind(path)
        optimized, w, h = optimize(path, tmp_dir)
        assets.append(
            ProofAsset(
                path=path,
                code=infer_code(path, code_order, back_prefix_to_code),
                kind=kind,
                size_label=infer_size(kind),
                option_label=infer_option(path, kind),
                width=w,
                height=h,
                optimized_path=optimized,
            )
        )
    return assets


def by_code(assets: list[ProofAsset], code_order: list[str]) -> dict[str, list[ProofAsset]]:
    grouped: dict[str, list[ProofAsset]] = {}
    for asset in assets:
        grouped.setdefault(asset.code, []).append(asset)
    ordered = {code: grouped.get(code, []) for code in code_order}
    for code in sorted(set(grouped) - set(code_order)):
        ordered[code] = grouped[code]
    return ordered


def image_fit(c: canvas.Canvas, asset: ProofAsset, x: float, y: float, w: float, h: float) -> None:
    ratio = min(w / asset.width, h / asset.height)
    draw_w = asset.width * ratio
    draw_h = asset.height * ratio
    draw_x = x + (w - draw_w) / 2
    draw_y = y + (h - draw_h) / 2
    c.drawImage(ImageReader(str(asset.optimized_path)), draw_x, draw_y, draw_w, draw_h, preserveAspectRatio=True, mask="auto")


def recommended_badge(c: canvas.Canvas, x: float, y: float) -> None:
    fill(c, RECOMMENDED_GREEN)
    c.rect(x, y, 86, 16, fill=1, stroke=0)
    fill(c, PAPER)
    c.setFont(SANS_BOLD, 6)
    c.drawCentredString(x + 43, y + 5.2, "RECOMMENDED")


def labeled_image(c: canvas.Canvas, asset: ProofAsset, x: float, y: float, w: float, h: float, label: str, recommended: bool = False) -> None:
    fill(c, GOLD)
    c.setFont(SANS_BOLD, 8.8)
    c.drawString(x, y + h + 10, label.upper())
    image_fit(c, asset, x, y, w, h)
    if recommended:
        recommended_badge(c, x, y - 25)


def card_dims(asset: ProofAsset) -> tuple[float, float]:
    if asset.width > asset.height:
        return CARD_LONG, CARD_SHORT
    return CARD_SHORT, CARD_LONG


def labeled_card(c: canvas.Canvas, asset: ProofAsset, x: float, y: float, label: str, recommended: bool = False) -> None:
    w, h = card_dims(asset)
    labeled_image(c, asset, x, y, w, h, label, recommended=recommended)


def cover(c: canvas.Canvas, title: str, date: str, prepared_by: str) -> None:
    page_base(c, "Print Proofs and Options", show_footer=False)
    fill(c, GOLD)
    c.setFont(SERIF, 58)
    c.drawString(82, 596, "TMORA")
    c.setFont(SERIF, 18)
    c.drawString(84, 570, "The Museum of Russian Art")
    stroke(c, GOLD)
    c.setLineWidth(0.75)
    c.line(84, 530, 262, 530)
    fill(c, CREAM)
    c.setFont(SERIF_BOLD, 27)
    lines = wrap(title, SERIF_BOLD, 27, 360)
    y = 484
    for line in lines:
        c.drawString(84, y, line)
        y -= 35
    fill(c, MUTED)
    c.setFont(SANS, 8.5)
    if date:
        c.drawString(84, 406, date)
    if prepared_by:
        c.drawString(84, 103, "Prepared by")
        draw_wrapped(c, prepared_by, 84, 82, 240, SANS, 8.5, 16, MUTED)


def left_info_panel(c: canvas.Canvas, code: str, files: list[ProofAsset], metadata: dict) -> None:
    item = metadata.get("artworks", {}).get(code, {})
    artist = item.get("artist", code)
    artwork = item.get("artwork", "")
    x = 70
    col_w = 180
    y = 620
    draw_wrapped(c, artist, x, y, col_w, SERIF, 17, 22, CREAM)
    y -= 39
    if artwork:
        y = draw_wrapped(c, artwork, x, y, col_w, SERIF_ITALIC, 10.4, 15, CREAM)
        y -= 12
    stroke(c, GOLD)
    c.setLineWidth(0.7)
    c.line(x, y, x + 112, y)
    y -= 25
    sizes = {a.size_label for a in files if a.size_label}
    size_lines = []
    if "11x17 in." in sizes:
        size_lines.append("Poster: 11x17 in.")
    if "4x6 in." in sizes:
        size_lines.append("Postcard: 4x6 in.")
    fill(c, MUTED)
    c.setFont(SANS, 8.2)
    for line in size_lines:
        c.drawString(x, y, line)
        y -= 14
    y -= 9
    fill(c, GOLD_SOFT)
    c.setFont(SANS, 6.6)
    c.drawString(x, y, f"SKU: {code}")


def front_label(asset: ProofAsset) -> str:
    if asset.option_label in {"A", "B"}:
        return f"{asset.size_label.split()[0]} {asset.option_label}"
    if asset.kind.startswith("11x17"):
        return "11x17"
    if asset.kind.startswith("4x6"):
        return "4x6"
    return asset.kind


def proof_page(c: canvas.Canvas, code: str, files: list[ProofAsset], metadata: dict, recommended_option: str) -> None:
    page_base(c, "Print File Options")
    left_info_panel(c, code, files, metadata)

    fronts_11 = sorted([a for a in files if a.kind == "11x17 print"], key=lambda a: a.option_label)
    fronts_4 = sorted([a for a in files if a.kind == "4x6 front"], key=lambda a: a.option_label)
    info_11 = [a for a in files if a.kind == "11x17 info card"]
    info_backs = [a for a in files if a.kind == "4x6 info back"]
    postal_backs = [a for a in files if a.kind == "4x6 postal back"]

    has_front_options = sum(1 for a in fronts_11 + fronts_4 if a.option_label in {"A", "B"}) > 1
    x = 285
    top_y = 410
    if fronts_11:
        for asset in fronts_11:
            labeled_image(c, asset, x, top_y, 125, 190, front_label(asset), recommended=has_front_options and asset.option_label == recommended_option)
            x += 145
        for asset in info_11:
            labeled_image(c, asset, x, top_y + 30, 180, 120, "11x17 info card")
    else:
        for asset in fronts_4:
            labeled_card(c, asset, x, top_y, front_label(asset), recommended=has_front_options and asset.option_label == recommended_option)
            x += 148

    x = 285
    bottom_y = 120
    if fronts_11 and fronts_4:
        for asset in fronts_4:
            labeled_card(c, asset, x, bottom_y, front_label(asset), recommended=has_front_options and asset.option_label == recommended_option)
            x += 148
    for asset in info_backs:
        labeled_card(c, asset, x, bottom_y, "Back A")
        x += 148
    for asset in postal_backs:
        labeled_card(c, asset, x, bottom_y, "Back B")


def write_manifest(path: Path, assets: list[ProofAsset]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["code", "kind", "size", "option", "pixels", "source_path"])
        for asset in assets:
            writer.writerow([asset.code, asset.kind, asset.size_label, asset.option_label, f"{asset.width}x{asset.height}", str(asset.path)])


def build_deck(args: argparse.Namespace) -> None:
    metadata = load_metadata(args.metadata)
    code_order = metadata.get("code_order", DEFAULT_CODE_ORDER)
    back_prefix_to_code = metadata.get("back_prefix_to_code", DEFAULT_BACK_PREFIX_TO_CODE)
    recommended_option = metadata.get("recommended_option", "B")

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / args.output_name
    manifest_path = output_dir / args.manifest_name

    assets = collect_assets(args.source_root, args.tmp_dir, code_order, back_prefix_to_code)
    grouped = by_code(assets, code_order)
    write_manifest(manifest_path, assets)

    c = canvas.Canvas(str(pdf_path), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    cover(c, args.title, args.date, args.prepared_by)
    c.showPage()
    for code, files in grouped.items():
        if not files:
            continue
        proof_page(c, code, files, metadata, recommended_option)
        c.showPage()
    c.save()

    print(pdf_path)
    print(manifest_path)
    print(f"{len(assets)} assets")


if __name__ == "__main__":
    build_deck(parse_args())
