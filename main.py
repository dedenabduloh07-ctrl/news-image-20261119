#!/usr/bin/env python3
"""Sum up 19 November 2026's world news in one image.

The finished front page (1024 x 1024, drawn in advance and stored as
entry.png next to this script) is copied to the output directory
unchanged. No drawing happens at run time, no network is used, and
the result is always the exact same bytes.

The page: a newspaper front page with the masthead "THE WORLD IN ONE
PAGE", dateline "Thursday, 19 November 2026", headline "TRUMP, XI
AND PUTIN HOLD FIRST THREE-WAY SUMMIT", an AI-generated hero
illustration of the three leaders at the Shenzhen summit with the
Chinese, US and Russian flags (disclosed as an AI illustration in its
caption), four story blocks (Summit, ICJ genocide ruling, Riyadh
missile, Anthropic IPO) and an ALSO strip.

Standard library only: this program runs as `python3 -P -s main.py`
in an environment where nothing extra is installed.
"""

import os
import shutil
import sys

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, OUTPUT_NAME)
    shutil.copyfile(source, dest)
    # A partial copy must never pass silently: the output has to be
    # byte-for-byte the page that was checked in.
    src_size = os.path.getsize(source)
    size = os.path.getsize(dest)
    if size != src_size:
        raise SystemExit(
            f"error: copied {size} bytes, expected {src_size}"
        )
    print(f"wrote {dest} ({size} bytes)")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # keep the failure loud and short
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
