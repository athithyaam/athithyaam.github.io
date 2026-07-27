#!/usr/bin/env python3
"""
Generate a per-post Open Graph preview image.

Usage:
  python3 _scripts/generate_og_image.py <slug> "<Post Title>" "<Category>"

Writes assets/images/og/<slug>.png (1200x630). Requires Google Chrome
installed locally (used headlessly to render the HTML template to PNG).

After generating, add this to the post's front matter:
  header:
    teaser: "/assets/images/og/<slug>.png"
"""
import html
import subprocess
import sys
import tempfile
from pathlib import Path

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "_scripts" / "og-post-template.html"
OUT_DIR = ROOT / "assets" / "images" / "og"


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    slug = sys.argv[1]
    title = sys.argv[2]
    category = sys.argv[3] if len(sys.argv) > 3 else "Blog Post"

    template = TEMPLATE.read_text()
    rendered = template.replace("__TITLE__", html.escape(title)).replace(
        "__CATEGORY__", html.escape(category)
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"{slug}.png"

    with tempfile.NamedTemporaryFile(
        suffix=".html", mode="w", delete=False
    ) as tmp:
        tmp.write(rendered)
        tmp_path = tmp.name

    subprocess.run(
        [
            CHROME,
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            "--window-size=1200,630",
            "--virtual-time-budget=5000",
            "--run-all-compositor-stages-before-draw",
            f"--screenshot={out_path}",
            f"file://{tmp_path}",
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print(f"Wrote {out_path.relative_to(ROOT)}")
    print(f'Add to post front matter:\n  header:\n    teaser: "/assets/images/og/{slug}.png"')


if __name__ == "__main__":
    main()
