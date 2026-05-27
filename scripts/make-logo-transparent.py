#!/usr/bin/env python3
"""Remove baked-in black background from Battle Juice logo PNG."""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "battle-juice-logo.png"
OUT = ROOT / "assets" / "battle-juice-logo.png"


def key_black(img: Image.Image, threshold: int = 42) -> Image.Image:
    img = img.convert("RGBA")
    pixels = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if r <= threshold and g <= threshold and b <= threshold:
                pixels[x, y] = (r, g, b, 0)
            elif r < 80 and g < 80 and b < 80:
                # soften dark fringe from JPEG compression
                fade = max(r, g, b) / 80
                pixels[x, y] = (r, g, b, int(a * fade))
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    return img


def main() -> None:
    img = Image.open(SRC)
    img = key_black(img)
    img.save(OUT, format="PNG", optimize=True)
    print(f"Wrote transparent logo {img.size} hasAlpha=yes")


if __name__ == "__main__":
    main()
