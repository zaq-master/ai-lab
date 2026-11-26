"""サムネ（横 1280x720）：大きな問い＋扉の絵＋アリス。実行：python3 thumb.py → thumb.png"""
from PIL import Image, ImageDraw, ImageFont
W, H = 1280, 720
im = Image.new('RGB', (W, H), '#171b42'); d = ImageDraw.Draw(im)
for r in range(800, 0, -6):
    c = int(30 + (800 - r) / 800 * 25); d.ellipse((900 - r * 1.3, 330 - r, 900 + r * 1.3, 330 + r), fill=(c, c + 8, min(255, c * 3)))
F = lambda s: ImageFont.truetype('assets/fonts/MPLUSRounded1c-ExtraBold.ttf', s)
def text(x, y, s, size, fill, stroke=10, center=False):
    f = F(size); w = d.textlength(s, font=f); x = x - w / 2 if center else x
    d.text((x + 6, y + 6), s, font=f, fill='#0e1130', stroke_width=stroke, stroke_fill='#0e1130')
    d.text((x, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill='#1c2150')
# 左：大きな問い
text(40, 30, '3つの扉', 120, 'white'); text(30, 175, '選び直す？', 140, '#ffc928', 12)
# 右：扉
DW, DH, y = 170, 250, 110
for i, x in enumerate([710, 900, 1090]):
    d.rounded_rectangle((x, y, x + DW, y + DH), 14, fill='#2a2340', outline='#f1e2c0', width=8)
    if i == 2:
        d.polygon([(x, y), (x + 26, y - 14), (x + 26, y + DH + 14), (x, y + DH)], fill='#b9783e')
        f = F(42); s = '外れ'; w = d.textlength(s, font=f); d.text((x + DW / 2 - w / 2 + 10, y + DH / 2 - 26), s, font=f, fill='#8d93ad')
    else:
        d.rounded_rectangle((x + 8, y + 8, x + DW - 8, y + DH - 8), 10, fill='#c98a4b', outline='#8c5426', width=6)
        d.ellipse((x + DW / 2 - 32, y + 30, x + DW / 2 + 32, y + 94), fill='#fff3dc'); f = F(46); s = str(i + 1); w = d.textlength(s, font=f); d.text((x + DW / 2 - w / 2, y + 32), s, font=f, fill='#7a4a1c')
        d.ellipse((x + DW - 34, y + 140, x + DW - 20, y + 154), fill='#ffe08a')
    if i == 0:
        d.rounded_rectangle((x - 5, y - 5, x + DW + 5, y + DH + 5), 18, outline='#ff5a4e', width=9)
        f = F(36); s = 'あなた'; w = d.textlength(s, font=f); d.rounded_rectangle((x + DW / 2 - w / 2 - 18, y - 66, x + DW / 2 + w / 2 + 18, y - 16), 26, fill='#e03131'); d.text((x + DW / 2 - w / 2, y - 66), s, font=f, fill='white')
    if i == 1:
        d.rounded_rectangle((x - 5, y - 5, x + DW + 5, y + DH + 5), 18, outline='#4da3ff', width=9)
        f = F(130); w = d.textlength('？', font=f); d.text((x + DW / 2 - w / 2, y + 100), '？', font=f, fill='#ffc928', stroke_width=9, stroke_fill='#1c2150')
text(900 + DW / 2 - 85 + 60, 420, '各1万回ためした', 70, 'white', 9, center=True)
a = Image.open('assets/alice/pose_pointing_768.png').convert('RGBA').resize((330, 440))
im.paste(a, (150, 370), a)
im.save('thumb.png')
