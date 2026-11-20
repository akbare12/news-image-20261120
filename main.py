"""Entrypoint for the news-image-20261120 entry.

Draws the front page with build_image.py and writes it to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
Deterministic: two runs write identical bytes.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_image import build


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    build(os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
