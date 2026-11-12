#!/usr/bin/env python3
"""Render a poster to PNG at 2x, cropped to its real content height."""
import os
import pathlib
import struct
import subprocess
import sys
import zlib

CHROME = "/Applications/Chromium.app/Contents/MacOS/Chromium"
WIDTH, SCALE = 1000, 2

def screenshot(page, out, height):
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--default-background-color=00000000",
                    f"--force-device-scale-factor={SCALE}",
                    f"--window-size={WIDTH},{height}",
                    f"--screenshot={out}", f"file://{page}"],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def decode(path):
    data = open(path, "rb").read()
    i, idat, w, h, ctype = 8, b"", None, None, None
    while i < len(data):
        ln = struct.unpack(">I", data[i:i+4])[0]
        typ = data[i+4:i+8]
        if typ == b"IHDR":
            w, h, depth, ctype = struct.unpack(">IIBB", data[i+8:i+18])
            if depth != 8 or ctype not in (2, 6):
                raise SystemExit(f"unsupported PNG depth {depth} ctype {ctype}")
        elif typ == b"IDAT":
            idat += data[i+8:i+8+ln]
        i += 12 + ln
    bpp = 4 if ctype == 6 else 3
    raw = zlib.decompress(idat)
    stride = w * bpp
    rows, prev, pos = [], bytearray(stride), 0
    for _ in range(h):
        f = raw[pos]
        line = bytearray(raw[pos+1:pos+1+stride])
        pos += 1 + stride
        if f == 1:
            for x in range(bpp, stride):
                line[x] = (line[x] + line[x-bpp]) & 0xFF
        elif f == 2:
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 0xFF
        elif f == 3:
            for x in range(stride):
                a = line[x-bpp] if x >= bpp else 0
                line[x] = (line[x] + ((a + prev[x]) >> 1)) & 0xFF
        elif f == 4:
            for x in range(stride):
                a = line[x-bpp] if x >= bpp else 0
                b = prev[x]
                c = prev[x-bpp] if x >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p-a), abs(p-b), abs(p-c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 0xFF
        rows.append(bytes(line))
        prev = line
    return w, h, bpp, rows

def encode(path, w, bpp, rows):
    ctype = 6 if bpp == 4 else 2
    raw = b"".join(b"\x00" + r for r in rows)
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t+d) & 0xFFFFFFFF)
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, len(rows), 8, ctype, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))
    open(path, "wb").write(png)

def main():
    page, out = str(pathlib.Path(sys.argv[1]).resolve()), sys.argv[2]
    theme = sys.argv[3] if len(sys.argv) > 3 else "dark"
    if theme != "dark":
        src = open(page).read().replace('data-theme="dark"', f'data-theme="{theme}"', 1)
        page = page.replace(".html", f"-{theme}.html")
        page = str(pathlib.Path(page).resolve())
        open(page, "w").write(src)
    tall = out + ".tall.png"
    screenshot(page, tall, 6000)
    w, h, bpp, rows = decode(tall)
    bg = rows[0][:bpp]
    last = 0
    for y in range(len(rows)-1, -1, -1):
        row = rows[y]
        if any(row[x:x+bpp] != bg for x in range(0, len(row), bpp)):
            last = y
            break
    crop = min(len(rows), last + 2)
    encode(out, w, bpp, rows[:crop])
    for temp in (tall, page if theme != "dark" else None):
        if temp and os.path.exists(temp):
            os.remove(temp)
    print(f"{out}: {w}x{crop} ({theme})")

if __name__ == "__main__":
    main()
