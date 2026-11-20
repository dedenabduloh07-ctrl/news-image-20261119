import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("missing entry.png next to main.py", file=sys.stderr)
        return 1
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    dst = os.path.join(outdir, "entry.png")
    shutil.copyfile(src, dst)
    want = os.path.getsize(src)
    got = os.path.getsize(dst)
    if got != want:
        print("size mismatch: expected %d bytes, got %d" % (want, got), file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (dst, got))
    return 0


if __name__ == "__main__":
    sys.exit(main())
