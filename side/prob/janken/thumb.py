"""サムネ（横 1280x720）：大きな問い＋手の絵＋アリス"""
import os
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__))
W, HH = 1280, 720
im = Image.new("RGB", (W, HH))
d = ImageDraw.Draw(im)
for y in range(HH):
    k = y / HH; d.line([(0, y), (W, y)], fill=(int(45 - 25 * k), int(53 - 30 * k), int(119 - 60 * k)))
F = lambda s: ImageFont.truetype(os.path.join(H, "assets/fonts/MPLUSRounded1c-ExtraBold.ttf"), s)


def txt(x, y, s, size, fill, stroke=12):
    f = F(size)
    d.text((x + 6, y + 6), s, font=f, fill=(20, 24, 58), stroke_width=stroke, stroke_fill=(20, 24, 58))
    d.text((x, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(28, 33, 80))


txt(50, 30, "5人でじゃんけん", 84, (255, 255, 255))
ef = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
for i, ch in enumerate(["✊", "✌", "✋", "✌", "✊"]):
    c = Image.new("RGBA", (136, 128)); ImageDraw.Draw(c).text((0, 0), ch, font=ef, embedded_color=True)
    c = c.resize((112, 105)); cx = 110 + i * 150; cy = 215 + (18 if i % 2 else 0)
    d.ellipse([cx - 66, cy - 66, cx + 66, cy + 66], fill=(255, 255, 255), outline=(28, 33, 80), width=7)
    im.paste(c, (cx - 56, cy - 54), c)
txt(50, 310, "1回で決まる", 118, (255, 201, 40), 14)
txt(50, 455, "確率は？", 150, (255, 201, 40), 16)
d.rounded_rectangle([60, 640, 520, 705], 24, fill=(255, 61, 127))
f = F(42); d.text((290, 672), "1万回ためした", font=f, fill=(255, 255, 255), anchor="mm")
al = Image.open(os.path.join(H, "assets/alice/pose_pointing_768.png")).convert("RGBA")
al = al.resize((int(al.width * 760 / al.height), 760))
im.paste(al, (W - al.width + 40, 40), al)
d.text((540, 658), "AIのシミュレーション", font=F(28), fill=(220, 224, 245))
im.save(os.path.join(H, "thumb.png"))
