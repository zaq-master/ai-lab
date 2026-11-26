"""サムネ（1080x1920）：大きな問い＋手の絵＋アリス"""
import os
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__))
W, HH = 1080, 1920
im = Image.new("RGB", (W, HH))
d = ImageDraw.Draw(im)
for y in range(HH):
    k = y / HH; d.line([(0, y), (W, y)], fill=(int(45 - 25 * k), int(53 - 30 * k), int(119 - 60 * k)))
F = lambda s: ImageFont.truetype(os.path.join(H, "assets/fonts/MPLUSRounded1c-ExtraBold.ttf"), s)
def txt(x, y, s, size, fill, stroke=14):
    f = F(size); w = d.textlength(s, font=f)
    d.text((x - w / 2 + 8, y + 8), s, font=f, fill=(20, 24, 58), stroke_width=stroke, stroke_fill=(20, 24, 58))
    d.text((x - w / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(28, 33, 80))
txt(540, 120, "5人でじゃんけん", 120, (255, 255, 255))
# 手（Noto Color Emoji は109pxで描いて拡大）
ef = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
for i, ch in enumerate(["✊", "✌", "✋", "✌", "✊"]):
    c = Image.new("RGBA", (136, 128)); ImageDraw.Draw(c).text((0, 0), ch, font=ef, embedded_color=True)
    c = c.resize((170, 160)); cx = 105 + i * 217; cy = 400 + (30 if i % 2 else 0)
    d.ellipse([cx - 100, cy - 100, cx + 100, cy + 100], fill=(255, 255, 255), outline=(28, 33, 80), width=10)
    im.paste(c, (cx - 85, cy - 82), c)
txt(540, 600, "1回で決まる", 150, (255, 201, 40), 16)
txt(540, 790, "確率は？", 190, (255, 201, 40), 18)
txt(540, 1050, "半分より上？下？", 84, (255, 255, 255))
d.rounded_rectangle([140, 1190, 940, 1300], 30, fill=(255, 61, 127))
f = F(70); w = d.textlength("1万回ためした", font=f); d.text((540 - w / 2, 1245), "1万回ためした", font=f, fill=(255, 255, 255), anchor="lm")
al = Image.open(os.path.join(H, "assets/alice/pose_pointing_768.png")).convert("RGBA")
al = al.resize((int(al.width * 760 / al.height), 760))
im.paste(al, (W - al.width - 20, HH - 600), al)
d.text((30, 1860), "AIのシミュレーション", font=F(36), fill=(220, 224, 245))
im.save(os.path.join(H, "thumb.png"))
