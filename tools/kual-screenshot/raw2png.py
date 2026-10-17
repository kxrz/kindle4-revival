#!/usr/bin/env python3
"""Convert framebuffer dumps (*.raw + *.info) from the Screenshot extension to PNG.

Usage: python3 raw2png.py /Volumes/Kindle/screenshots/*.raw [--out DIR] [--invert|--no-invert]

Only the standard library is used. 8 bpp (grayscale) and 4 bpp framebuffers
are supported. By default the image is inverted when it comes out mostly
dark, since an e-reader screen is mostly white.
"""
import argparse, os, re, struct, zlib


def read_info(path):
    info = {}
    with open(path) as f:
        for line in f:
            k, _, v = line.strip().partition("=")
            info[k] = v
    return info


def png(path, width, height, rows):
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    raw = b"".join(b"\x00" + r for r in rows)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0)))
        f.write(chunk(b"IDAT", zlib.compress(raw, 9)))
        f.write(chunk(b"IEND", b""))


def convert(raw_path, out_dir, invert):
    info = read_info(raw_path[:-4] + ".info")
    data = open(raw_path, "rb").read()
    bpp = int(info.get("bits_per_pixel") or 8)
    m = re.search(r"(\d+)x(\d+)", info.get("modes", ""))
    vx, vy = (int(x) for x in info.get("virtual_size", "600,800").split(","))
    width, height = (int(m.group(1)), int(m.group(2))) if m else (vx, min(vy, 800))
    stride = int(info.get("stride") or vx * bpp // 8)
    rows = []
    for y in range(height):
        line = data[y * stride: y * stride + stride]
        if bpp == 8:
            row = line[:width]
        elif bpp == 4:
            row = bytes(v for b in line for v in ((b >> 4) * 17, (b & 15) * 17))[:width]
        else:
            raise SystemExit(f"{raw_path}: unsupported {bpp} bpp")
        rows.append(row)
    mean = sum(sum(r) for r in rows) / (width * height)
    if invert is None:
        invert = mean < 128
    if invert:
        rows = [bytes(255 - v for v in r) for r in rows]
    out = os.path.join(out_dir or os.path.dirname(raw_path), os.path.basename(raw_path)[:-4] + ".png")
    png(out, width, height, rows)
    print(f"{out}  {width}x{height} {bpp}bpp{' inverted' if invert else ''}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("raw", nargs="+")
    ap.add_argument("--out")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--invert", dest="invert", action="store_true", default=None)
    g.add_argument("--no-invert", dest="invert", action="store_false")
    a = ap.parse_args()
    for r in a.raw:
        convert(r, a.out, a.invert)
