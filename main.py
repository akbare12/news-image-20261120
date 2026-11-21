"""Entrypoint for the news-image-20261120 entry.

Copies the front-page image the repository holds to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).

Standard library only: the grading sandbox installs nothing
(Python 3.13, stdlib only), so this entry must not import PIL
or any third-party package. v1 drew the image with PIL and
failed on the server with ModuleNotFoundError: No module
named 'PIL' (exit code 1). The image itself is drawn by
build_image.py (kept in the repo as the generator); this
program only ships the bytes it wrote.
Deterministic: a copy writes identical bytes every run.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(
        os.path.join(here, "entry.png"),
        os.path.join(out_dir, "entry.png"),
    )


if __name__ == "__main__":
    main()
