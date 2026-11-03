from PIL import Image, ImageDraw, ImageFont
S=800; im=Image.new("RGB",(S,S),"#1E7A5A"); d=ImageDraw.Draw(im)
B="/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
# spreadsheet card
x0,y0,x1,y1=170,150,630,520
d.rounded_rectangle([x0,y0,x1,y1],28,fill="white")
d.rounded_rectangle([x0,y0,x1,y0+70],28,fill="#D8EFE5"); d.rectangle([x0,y0+40,x1,y0+70],fill="#D8EFE5")
for i in range(1,4): d.line([(x0+i*(x1-x0)/4,y0),(x0+i*(x1-x0)/4,y1)],fill="#C5D9D0",width=4)
for j in range(1,5): d.line([(x0,y0+70+j*60),(x1,y0+70+j*60)],fill="#C5D9D0",width=4)
# play/auto button
cx,cy,r=560,470,95
d.ellipse([cx-r,cy-r,cx+r,cy+r],fill="#FFE45C",outline="#1E7A5A",width=10)
d.polygon([(cx-30,cy-45),(cx-30,cy+45),(cx+45,cy)],fill="#1E7A5A")
f=ImageFont.truetype(B,96,index=0); t="自動化"
w=d.textlength(t,font=f); d.text(((S-w)/2,585),t,font=f,fill="white")
im.save("icon.png")
