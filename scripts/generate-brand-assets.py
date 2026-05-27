#!/usr/bin/env python3
"""Generate favicons and OG preview image for the Battle Juice investor deck."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
LOGO = ASSETS / "battle-juice-logo.png"

OG_W, OG_H = 1200, 630
BG = (5, 6, 15)
ACCENT = (255, 59, 48)
TEXT = (238, 241, 255)
TEXT_DIM = (154, 163, 199)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in candidates:
        p = Path(path)
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except OSError:
                continue
    return ImageFont.load_default()


def fit_logo(canvas: Image.Image, logo: Image.Image, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    max_w, max_h = x1 - x0, y1 - y0
    w, h = logo.size
    scale = min(max_w / w, max_h / h)
    nw, nh = int(w * scale), int(h * scale)
    resized = logo.resize((nw, nh), Image.Resampling.LANCZOS)
    ox = x0 + (max_w - nw) // 2
    oy = y0 + (max_h - nh) // 2
    if resized.mode == "RGBA":
        canvas.paste(resized, (ox, oy), resized)
    else:
        canvas.paste(resized, (ox, oy))


def make_favicon(size: int) -> Image.Image:
    logo = Image.open(LOGO).convert("RGBA")
    canvas = Image.new("RGBA", (size, size), BG + (255,))
    pad = max(2, size // 10)
    fit_logo(canvas, logo, (pad, pad, size - pad, size - pad))
    return canvas


def make_og() -> Image.Image:
    logo = Image.open(LOGO).convert("RGBA")
    img = Image.new("RGB", (OG_W, OG_H), BG)
    draw = ImageDraw.Draw(img)

    # subtle gradient bands
    for y in range(OG_H):
        t = y / OG_H
        r = int(BG[0] + 18 * (1 - t))
        g = int(BG[1] + 22 * (1 - t))
        b = int(BG[2] + 55 * (1 - t))
        draw.line([(0, y), (OG_W, y)], fill=(r, g, b))

    draw.rectangle([(0, 0), (6, OG_H)], fill=ACCENT)
    fit_logo(img, logo, (80, 70, OG_W - 80, 300))

    title_font = load_font(52, bold=True)
    sub_font = load_font(28, bold=True)
    body_font = load_font(24)

    title = "Battle Juice — Investor Overview 2026"
    subtitle = "Confidential · Youth-sports hydration"
    body = (
        "Cash-funded brand with early retail sell-through, a live national pipeline, "
        "and lean burn — built for investors evaluating Battle Juice, Inc."
    )

    y = 330
    draw.text((80, y), title, fill=TEXT, font=title_font)
    y += 62
    draw.text((80, y), subtitle, fill=ACCENT, font=sub_font)
    y += 48

    # wrap body text
    words = body.split()
    lines: list[str] = []
    line: list[str] = []
    max_width = OG_W - 160
    for word in words:
        test = " ".join(line + [word])
        bbox = draw.textbbox((0, 0), test, font=body_font)
        if bbox[2] - bbox[0] <= max_width:
            line.append(word)
        else:
            if line:
                lines.append(" ".join(line))
            line = [word]
    if line:
        lines.append(" ".join(line))

    for ln in lines:
        draw.text((80, y), ln, fill=TEXT_DIM, font=body_font)
        y += 34

    return img


def save_ico(sizes: list[int], path: Path) -> None:
    icons = [make_favicon(s).convert("RGBA") for s in sizes]
    icons[0].save(path, format="ICO", sizes=[(s, s) for s in sizes], append_images=icons[1:])


def write_manifest() -> None:
    manifest = """{
  "name": "Battle Juice — Investor Overview",
  "short_name": "Battle Juice",
  "description": "Confidential investor deck for Battle Juice, Inc.",
  "start_url": "./index.html",
  "display": "browser",
  "background_color": "#05060f",
  "theme_color": "#05060f",
  "icons": [
    {"src": "favicon-32.png", "sizes": "32x32", "type": "image/png"},
    {"src": "apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
    {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}
  ]
}
"""
    (ASSETS / "site.webmanifest").write_text(manifest, encoding="utf-8")


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    for size, name in [
        (16, "favicon-16.png"),
        (32, "favicon-32.png"),
        (180, "apple-touch-icon.png"),
        (192, "icon-192.png"),
        (512, "icon-512.png"),
    ]:
        make_favicon(size).save(ASSETS / name, format="PNG", optimize=True)
    save_ico([16, 32, 48], ASSETS / "favicon.ico")
    make_og().save(ASSETS / "og-image.png", format="PNG", optimize=True)
    write_manifest()
    print("Wrote favicons, manifest, and og-image.png to", ASSETS)


if __name__ == "__main__":
    main()
