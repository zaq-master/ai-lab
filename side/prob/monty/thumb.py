"""サムネ（1080x1920）：大きな問い＋扉の絵＋アリス。実行：python3 thumb.py → thumb.png"""
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1920
im = Image.new('RGB', (W, H), '#171b42'); d = ImageDraw.Draw(im)
for r in range(900, 0, -6):
    c = int(30 + (900 - r) / 900 * 25); d.ellipse((540 - r * 1.2, 600 - r, 540 + r * 1.2, 600 + r), fill=(c, c + 8, min(255, c * 3)))
F = lambda s: ImageFont.truetype('assets/fonts/MPLUSRounded1c-ExtraBold.ttf', s)
def text(y, s, size, fill, stroke=14):
    f = F(size); w = d.textlength(s, font=f)
    d.text(((W - w) / 2 + 8, y + 8), s, font=f, fill='#0e1130', stroke_width=stroke, stroke_fill='#0e1130')
    d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill='#1c2150')
text(70, '3つの扉', 150, 'white'); text(250, '選び直す？', 190, '#ffc928')
DW, DH, y = 270, 400, 660
for i, x in enumerate([45, 405, 765]):
    d.rounded_rectangle((x, y, x + DW, y + DH), 20, fill='#2a2340', outline='#f1e2c0', width=12)
    if i == 2:
        d.polygon([(x, y), (x + 40, y - 20), (x + 40, y + DH + 20), (x, y + DH)], fill='#b9783e')
        f = F(60); s = '外れ'; w = d.textlength(s, font=f); d.text((x + DW / 2 - w / 2 + 15, y + DH / 2 - 40), s, font=f, fill='#8d93ad')
    else:
        d.rounded_rectangle((x + 12, y + 12, x + DW - 12, y + DH - 12), 14, fill='#c98a4b', outline='#8c5426', width=8)
        d.ellipse((x + DW / 2 - 50, y + 50, x + DW / 2 + 50, y + 150), fill='#fff3dc'); f = F(70); s = str(i + 1); w = d.textlength(s, font=f); d.text((x + DW / 2 - w / 2, y + 55), s, font=f, fill='#7a4a1c')
        d.ellipse((x + DW - 50, y + 220, x + DW - 30, y + 240), fill='#ffe08a')
    if i == 0:
        d.rounded_rectangle((x - 6, y - 6, x + DW + 6, y + DH + 6), 26, outline='#ff5a4e', width=12)
        f = F(54); s = 'あなた'; w = d.textlength(s, font=f); d.rounded_rectangle((x + DW / 2 - w / 2 - 26, y - 96, x + DW / 2 + w / 2 + 26, y - 22), 38, fill='#e03131'); d.text((x + DW / 2 - w / 2, y - 94), s, font=f, fill='white')
    if i == 1:
        d.rounded_rectangle((x - 6, y - 6, x + DW + 6, y + DH + 6), 26, outline='#4da3ff', width=12)
        f = F(200); w = d.textlength('？', font=f); d.text((x + DW / 2 - w / 2, y + 160), '？', font=f, fill='#ffc928', stroke_width=12, stroke_fill='#1c2150')
text(1110, '1万回ためした', 110, 'white', 12)
a = Image.open('assets/alice/pose_pointing_768.png').convert('RGBA').resize((600, 800))
im.paste(a, (430, 1260), a)
im.save('thumb.png')
