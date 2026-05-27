#!/usr/bin/env python3
"""Set absolute Open Graph URLs for GitHub Pages deployment."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE_BASE = "https://battle-juice-deck.vercel.app"
OG_IMAGE = f"{SITE_BASE}/assets/og-image.png"


def page_url(name: str) -> str:
    return f"{SITE_BASE}/" if name == "index.html" else f"{SITE_BASE}/{name}"


def wire(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    url = page_url(path.name)

    html = re.sub(
        r'content="(?:https?://[^"]+)?assets/og-image\.png"',
        f'content="{OG_IMAGE}"',
        html,
    )
    html = re.sub(
        r'<meta property="og:url" content="[^"]*">\n?',
        "",
        html,
    )
    html = html.replace(
        '<meta property="og:type" content="website">',
        f'<meta property="og:type" content="website">\n<meta property="og:url" content="{url}">',
        1,
    )
    path.write_text(html, encoding="utf-8")
    print("Wired", path.name, "→", url)


def main() -> None:
    for path in sorted(ROOT.glob("*.html")):
        wire(path)


if __name__ == "__main__":
    main()
