#!/usr/bin/env python3
"""曲ごとのジャケット(3000x3000)とYouTubeサムネ(1280x720)を作る。
  python3 music/tools/cover.py <アート画像> "<曲名>" [--sub "サブ文字"] [--out 出力フォルダ]
アート画像はCanvaやSunoのジャケット画像（正方形推奨）。名義は「トガ feat. 電脳アリス」。
"""
import argparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
BK="/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
F=lambda s:ImageFont.truetype(BK,s,index=0)
ARTIST="トガ feat. 電脳アリス"
def fit(d,text,maxw,start):
    s=start
    while d.textlength(text,font=F(s))>maxw and s>20: s-=4
    return F(s)
def glow_text(base,xy,text,font,fill,glow,blur):
    lay=Image.new("RGBA",base.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
    d.text(xy,text,font=font,fill=glow,stroke_width=int(font.size*0.08),stroke_fill=glow)
    lay=lay.filter(ImageFilter.GaussianBlur(blur)); base.alpha_composite(lay); base.alpha_composite(lay)
    d=ImageDraw.Draw(base)
    d.text(xy,text,font=font,fill=fill,stroke_width=int(font.size*0.05),stroke_fill="#14002b")
def jacket(art,title,sub,out):
    S=3000; im=art.convert("RGBA").resize((S,S),Image.LANCZOS)
    g=Image.new("RGBA",(S,S),(0,0,0,0)); gd=ImageDraw.Draw(g)
    for y in range(900): gd.line([(0,y),(S,y)],fill=(10,0,30,int(170*(1-y/900))))
    im.alpha_composite(g); d=ImageDraw.Draw(im)
    f=fit(d,title,S-300,380); w=d.textlength(title,font=f)
    glow_text(im,((S-w)/2,140),title,f,"#ffffff","#ff4fd8",40)
    a=F(120); w=d.textlength(ARTIST,font=a); glow_text(im,((S-w)/2,S-330),ARTIST,a,"#ffffff","#3dd6ff",25)
    if sub:
        sf=F(100); w=d.textlength(sub,font=sf); d.text(((S-w)/2,140+f.size*1.35),sub,font=sf,fill="#ffe3fa",stroke_width=8,stroke_fill="#14002b")
    im.convert("RGB").save(f"{out}/jacket.jpg",quality=92)
def thumb(art,title,sub,out):
    W,H=1280,720; bg=art.convert("RGBA").resize((W,W),Image.LANCZOS).crop((0,(W-H)//2,W,(W+H)//2))
    bg=ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(18))).enhance(0.55)
    sq=art.convert("RGBA").resize((660,660),Image.LANCZOS)
    m=Image.new("L",(660,660),0); ImageDraw.Draw(m).rounded_rectangle([0,0,659,659],40,fill=255)
    sh=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([600,40,1280,710],40,fill=(255,79,216,200))
    bg.alpha_composite(sh.filter(ImageFilter.GaussianBlur(25)))
    bg.paste(sq,(600,30),m); d=ImageDraw.Draw(bg)
    words=title if len(title)<=7 else None
    lines=[title] if words else [title[:len(title)//2+1],title[len(title)//2+1:]]
    y=150
    for ln in lines:
        f=fit(d,ln,560,170); glow_text(bg,(40,y),ln,f,"#ffffff","#ff4fd8",18); y+=f.size*1.2
    if sub: d.text((44,y+10),sub,font=F(44),fill="#ffe3fa",stroke_width=5,stroke_fill="#14002b")
    glow_text(bg,(44,600),ARTIST,F(64),"#ffffff","#3dd6ff",12)
    bg.convert("RGB").save(f"{out}/thumb.jpg",quality=92)
if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("art"); p.add_argument("title"); p.add_argument("--sub",default=""); p.add_argument("--out",default=".")
    a=p.parse_args(); art=Image.open(a.art)
    w,h=art.size; s=min(w,h); art=art.crop(((w-s)//2,(h-s)//2,(w-s)//2+s,(h-s)//2+s))
    jacket(art,a.title,a.sub,a.out); thumb(art,a.title,a.sub,a.out); print("ok")
