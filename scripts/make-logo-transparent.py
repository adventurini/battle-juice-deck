#!/usr/bin/env python3
"""Remove baked-in black background from Battle Juice logo."""
from collections import deque
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUT = ASSETS / "battle-juice-logo.png"
SOURCE_CANDIDATES = [
    ASSETS / "battle-juice-logo.png",
    Path("/Users/adventurini/.cursor/projects/Users-adventurini-Downloads-invest-2/assets")
    / "MainLogo-d9eda2b0-953b-4745-98dc-7c337baeb722.png",
]


def flood_key_black(img: Image.Image, threshold: int = 55) -> Image.Image:
    img = img.convert("RGBA")
    pixels = img.load()
    w, h = img.size

    def is_bg(r: int, g: int, b: int) -> bool:
        return r <= threshold and g <= threshold and b <= threshold

    def flood(sx: int, sy: int) -> None:
        if not is_bg(*pixels[sx, sy][:3]):
            return
        q: deque[tuple[int, int]] = deque([(sx, sy)])
        seen: set[tuple[int, int]] = set()
        while q:
            x, y = q.popleft()
            if (x, y) in seen or x < 0 or y < 0 or x >= w or y >= h:
                continue
            seen.add((x, y))
            r, g, b, _ = pixels[x, y]
            if not is_bg(r, g, b):
                continue
            pixels[x, y] = (0, 0, 0, 0)
            q.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))

    for sx, sy in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        flood(sx, sy)

    # clean dark JPEG fringe on letter edges
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            if r < 70 and g < 70 and b < 70:
                fade = max(r, g, b) / 70
                pixels[x, y] = (r, g, b, int(255 * fade))

    bbox = img.getbbox()
    return img.crop(bbox) if bbox else img


def main() -> None:
    src = next((p for p in SOURCE_CANDIDATES if p.exists()), OUT)
    img = flood_key_black(Image.open(src))
    img.save(OUT, format="PNG", optimize=True)
    print(f"Wrote transparent logo from {src.name} → {img.size}")


if __name__ == "__main__":
    main()
