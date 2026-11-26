"""サムネ（1280x720）：大きな問い「1%×100回＝当たる？」＋アリス。実行：python3 thumb.py → thumb.png
背景の点は results.json の実験①（1万人）の本物の結果（金＝当たった人、灰＝1回も当たらなかった人）"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1280, 720
R = json.load(open(os.path.join(HERE, "results.json")))["e1"]
im = Image.new("RGB", (W, H), "#171b42"); d = ImageDraw.Draw(im)
for r in range(700, 0, -6):
    c = (700 - r) / 700; d.ellipse((520 - r * 1.4, 330 - r, 520 + r * 1.4, 330 + r), fill=(int(23 + 22 * c), int(27 + 58 * c), int(66 + 77 * c)))
# 右奥に1万人の点（うすく）
cell = 6
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
for i, b in enumerate(R["bits"]):
    x, y = 660 + (i % 100) * cell, 60 + (i // 100) * cell
    od.ellipse((x, y, x + cell - 1.5, y + cell - 1.5), fill=(255, 201, 40, 150) if b == "1" else (160, 166, 192, 110))
im.paste(ov, (0, 0), ov)
F = lambda s: ImageFont.truetype(os.path.join(HERE, "assets/fonts/MPLUSRounded1c-ExtraBold.ttf"), s)


def text(x, y, s, size, fill, stroke=12):
    f = F(size)
    d.text((x + 7, y + 7), s, font=f, fill="#0e1130", stroke_width=stroke, stroke_fill="#0e1130")
    d.text((x, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill="#1c2150")
    return x + d.textlength(s, font=f)


text(50, 26, "確率1%のガチャ", 66, "white", 9)
x = text(46, 110, "1%", 190, "#ffc928", 14)
text(x + 6, 158, "×100回", 128, "white", 14)
x = text(46, 335, "＝当たる", 150, "white", 14)
text(x - 14, 322, "？", 170, "#ffc928", 14)
# ふせん「1万人でためした」
st = Image.new("RGBA", (500, 108), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
sd.rounded_rectangle((4, 4, 496, 104), 24, fill="#fff3b0", outline="white", width=6)
f = F(56); sd.text((26, 14), "1万人", font=f, fill="#d9480f"); sd.text((26 + sd.textlength("1万人", font=f), 14), "でためした", font=f, fill="#1c2150")
st = st.rotate(3, expand=True, resample=Image.BICUBIC); im.paste(st, (60, 560), st)
a = Image.open(os.path.join(HERE, "assets/alice/surprised_768.png")).convert("RGBA").resize((540, 720))
# 白いふち
al = a.split()[3]; edge = Image.new("RGBA", a.size, (255, 255, 255, 255))
for dx, dy in ((-5, 0), (5, 0), (0, -5), (0, 5), (-4, -4), (4, 4), (-4, 4), (4, -4)):
    im.paste(edge, (840 + dx, 60 + dy), al)
im.paste(a, (840, 60), a)
im.save(os.path.join(HERE, "thumb.png"))
print("thumb.png")
