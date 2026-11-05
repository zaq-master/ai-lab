import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H=2560,1440; BK="/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
F=lambda s:ImageFont.truetype(BK,s,index=0)
im=Image.new("RGBA",(W,H),(12,4,32,255)); d=ImageDraw.Draw(im)
for y in range(H):
    t=y/H; d.line([(0,y),(W,y)],fill=(int(12+40*t),int(4+10*t),int(32+50*t),255))
g=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(g); r=random.Random(5)
for _ in range(90):
    x,y,s=r.randint(0,W),r.randint(0,H),r.randint(10,60); c=r.choice([(255,79,216,160),(61,214,255,160),(255,255,255,120)])
    gd.ellipse([x-s,y-s,x+s,y+s],fill=c)
for i in range(0,W,40):  # equalizer bars
    h=int(120+110*abs(math.sin(i*0.013))*abs(math.cos(i*0.031)))
    gd.rectangle([i,H-h,i+24,H],fill=(255,79,216,90) if (i//40)%2 else (61,214,255,90))
im.alpha_composite(g.filter(ImageFilter.GaussianBlur(6)))
def glow(xy,t,f,fill,gc,b):
    l=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(l).text(xy,t,font=f,fill=gc,anchor="mm",stroke_width=f.size//10,stroke_fill=gc)
    im.alpha_composite(l.filter(ImageFilter.GaussianBlur(b))); ImageDraw.Draw(im).text(xy,t,font=f,fill=fill,anchor="mm",stroke_width=f.size//20,stroke_fill="#14002b")
glow((W//2,H//2-40),"トガ feat. 電脳アリス",F(150),"#ffffff","#ff4fd8",28)
glow((W//2,H//2+110),"当たるまで、やめられない。",F(64),"#ffe3fa","#3dd6ff",14)
im.convert("RGB").save("music/tools/yt_banner.jpg",quality=92)
