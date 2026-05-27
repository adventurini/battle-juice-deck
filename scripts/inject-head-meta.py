#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DESC = (
    "Confidential investor overview for Battle Juice, Inc. — a cash-funded "
    "youth-sports hydration brand with early retail sell-through, a live national "
    "pipeline, and lean burn."
)
OG_ALT = (
    "Battle Juice investor deck — confidential overview of a cash-funded "
    "youth-sports hydration brand with early retail sell-through and national pipeline."
)

META_TEMPLATE = """
<meta name="description" content="{desc}">
<link rel="icon" href="assets/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="assets/favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="assets/apple-touch-icon.png">
<meta name="theme-color" content="#05060f">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Battle Juice">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{og_alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="assets/og-image.png">
"""


def inject(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    if "og:image" in html:
        return
    m = re.search(r"<title>([^<]+)</title>", html)
    if not m:
        return
    title = m.group(1).strip()
    block = META_TEMPLATE.format(desc=DESC, title=title, og_alt=OG_ALT)
    html, n = re.subn(
        r'(<meta name="viewport" content="[^"]+">)',
        r"\1" + block,
        html,
        count=1,
    )
    if n:
        path.write_text(html, encoding="utf-8")
        print("Updated", path.name)


def main() -> None:
    for path in sorted(ROOT.glob("*.html")):
        inject(path)


if __name__ == "__main__":
    main()
