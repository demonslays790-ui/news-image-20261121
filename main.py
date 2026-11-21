#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261121 entry.

The repository holds the finished front-page image in ``entry.png`` (drawn by
``generate_image.py``). The grader runs this program with no network and reads
exactly one file, so the program copies the image, byte for byte, to
``/output/entry.png`` (or to ``$MAKEFUN_OUTPUT_DIR`` when that is set, which
is how it is run outside the grader's container).
"""

import os
import shutil
import stat
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    with open(source, "rb") as handle:
        data = handle.read()
    if not data.startswith(PNG_SIGNATURE):
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1
    if len(data) > 1048576:
        print("entry.png exceeds the 1 MiB gate limit", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as handle:
        handle.write(data)
    # The grader collects the output as a different user: leave it readable.
    os.chmod(target, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    print(f"wrote {target} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
