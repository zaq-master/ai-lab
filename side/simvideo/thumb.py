"""サムネイル（1280x720）。python3 thumb.py "上の行" "大きい数字" "下の行" out.png"""
import sys
from PIL import Image, ImageDraw, ImageFont
F = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"
top, big, bottom, out = sys.argv[1:5]
img = Image.new("RGB", (1280, 720), (16, 22, 40))
d = ImageDraw.Draw(img)
import random
r = random.Random(7)
for y in range(0, 720, 16):           # 背景の点（1万人のイメージ）
    for x in range(0, 1280, 16):
        d.rectangle([x, y, x + 10, y + 10], fill=(255, 196, 64) if r.random() < 0.63 else (40, 50, 78))
d.rectangle([0, 0, 1280, 720], fill=None)
ov = Image.new("RGBA", (1280, 720), (10, 14, 28, 200))
img.paste(ov, (0, 0), ov)
def t(y, s, size, fill, sw):
    f = ImageFont.truetype(F, size)
    while d.textlength(s, font=f) > 1200:
        size -= 6; f = ImageFont.truetype(F, size)
    d.text((640, y), s, font=f, fill=fill, anchor="ma", stroke_width=sw, stroke_fill=(10, 14, 28))
t(60, top, 96, (240, 236, 226), 6)
t(230, big, 230, (255, 120, 80), 10)
t(520, bottom, 100, (255, 196, 64), 6)
img.save(out)
