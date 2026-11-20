#!/usr/bin/env python3
"""News-image-daily entry: the image is entry.png beside this file; copy it to /output/entry.png.

19 November 2026 edition. Runs with no network (Python 3.13, standard library
only). Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
import struct
import sys

MAX_BYTES = 1_048_576
MAX_SIDE = 1024

src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
dst = os.path.join(out_dir, "entry.png")

if not os.path.isfile(src):
    sys.exit(f"entry.png missing beside {__file__}")
with open(src, "rb") as f:
    head = f.read(33)
# Whole PNG: magic bytes plus the IHDR chunk naming its size.
if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
    sys.exit("entry.png is not a PNG")
width, height = struct.unpack(">II", head[16:24])
if width > MAX_SIDE or height > MAX_SIDE:
    sys.exit(f"entry.png is {width}x{height}, over the {MAX_SIDE}x{MAX_SIDE} gate")
if os.path.getsize(src) > MAX_BYTES:
    sys.exit(f"entry.png is over the {MAX_BYTES}-byte gate")

os.makedirs(out_dir, exist_ok=True)
shutil.copyfile(src, dst)
# Verify the copy, not just the source: re-read the destination header and
# confirm its byte size matches, so a truncated write cannot slip through.
with open(dst, "rb") as f:
    dst_head = f.read(33)
if dst_head[:8] != b"\x89PNG\r\n\x1a\n" or dst_head[12:16] != b"IHDR":
    sys.exit("copied entry.png failed header check")
if os.path.getsize(dst) != os.path.getsize(src):
    sys.exit("copied entry.png size differs from source")
# And the dimensions: the copy must still be the gated 1024x1024 image.
with open(dst, "rb") as f:
    dst_head = f.read(33)
dst_w, dst_h = struct.unpack(">II", dst_head[16:24])
if (dst_w, dst_h) != (width, height):
    sys.exit(f"copied entry.png is {dst_w}x{dst_h}, source was {width}x{height}")
print(f"wrote {dst}: {width}x{height} PNG, {os.path.getsize(dst)} bytes")
