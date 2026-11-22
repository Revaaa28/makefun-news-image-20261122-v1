#!/usr/bin/env python3
"""Entry point: validate the pre-rendered entry.png and copy it,
byte-identically, to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).
The image itself is produced by draw.py (deterministic, offline).
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1048576  # 1 MiB
MAX_DIM = 1024
PNG_SIG = b"\x89PNG\r\n\x1a\n"


def main():
    with open(SRC, "rb") as f:
        data = f.read()
    if not data.startswith(PNG_SIG):
        sys.exit("entry.png: bad PNG signature")
    if len(data) > MAX_BYTES:
        sys.exit("entry.png: exceeds 1 MiB")
    # IHDR: width/height are big-endian uint32 at bytes 16..24
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        sys.exit("entry.png: exceeds 1024x1024")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    with open(dst, "rb") as f:
        if f.read() != data:
            sys.exit("copy mismatch")
    print(f"wrote {dst} ({len(data)} bytes, {width}x{height})")


if __name__ == "__main__":
    main()
