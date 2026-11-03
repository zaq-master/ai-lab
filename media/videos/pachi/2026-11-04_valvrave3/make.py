import subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1080,1920,30
BK="/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"; BD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
F=lambda p,s:ImageFont.truetype(p,s,index=0)
def bg(t,c1,c2):
    im=Image.new("RGB",(W,H),c1); d=ImageDraw.Draw(im)
    # rotating rays
    cx,cy=W/2,H*0.42
    for i in range(24):
        a=i*math.pi/12+t*0.4
        pts=[(cx,cy),(cx+3000*math.cos(a),cy+3000*math.sin(a)),(cx+3000*math.cos(a+0.13),cy+3000*math.sin(a+0.13))]
        d.polygon(pts,fill=c2)
    return im
def ctext(d,y,s,font,fill,stroke=0,sc="#000"):
    w=d.textlength(s,font=font); d.text(((W-w)/2,y),s,font=font,fill=fill,stroke_width=stroke,stroke_fill=sc)
def pop(t,start,dur=0.35):
    x=max(0,min(1,(t-start)/dur)); 
    return 0 if x<=0 else (1+0.25*math.sin(x*math.pi)) if x<1 else 1
def stamp(im,s,font,fill,y,scale,stroke=10,sc="#000"):
    if scale<=0: return
    tmp=Image.new("RGBA",(W,600),(0,0,0,0)); d=ImageDraw.Draw(tmp)
    w=d.textlength(s,font=font); d.text(((W-w)/2,50),s,font=font,fill=fill,stroke_width=stroke,stroke_fill=sc)
    tw,th=int(W*scale),int(600*scale); tmp=tmp.resize((tw,th))
    im.paste(tmp,(int((W-tw)/2),int(y-(th-600)/2)),tmp)
def header(im):
    d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,190],fill="#111")
    ctext(d,40,"Pフィーバー革命機ヴァルヴレイヴ3",F(BK,58),"#FFE45C")
    d.rectangle([0,H-150,W,H],fill="#111")
    ctext(d,H-120,"借金介護士の日常｜数字で見るパチンコ",F(BD,40),"white")
def foot(d,s):
    ctext(d,H-260,s,F(BD,32),"#DDDDDD")
SCN=[(0,3.5),(3.5,10.5),(10.5,17.5),(17.5,23.5),(23.5,29)]
def frame(t):
    if t<SCN[0][1]:
        im=bg(t,"#B3001B","#D4142F"); header(im); d=ImageDraw.Draw(im)
        stamp(im,"RUSH継続率",F(BK,110),"white",420,pop(t,0.1))
        n=min(90,int(90*max(0,(t-0.5))/1.6)) if t>0.5 else 0
        stamp(im,f"約{n}%",F(BK,300),"#FFE45C",700,pop(t,0.5,0.3) if t<2.1 else 1+0.04*math.sin(t*12),16,"#5A0000")
        if t>2.2: ctext(d,1330,"…数字で見るとどうなる？",F(BK,70),"white",6)
        return im
    if t<SCN[1][1]:
        s=t-SCN[1][0]; im=bg(t,"#14213D","#1D2D50"); header(im); d=ImageDraw.Draw(im)
        ctext(d,260,"まずスペック",F(BK,90),"white",6)
        rows=[("大当り確率","1/319.7"),("RUSH突入率","約59%"),("RUSH中の確率","1/45.5"),("RUSH継続率","約90%"),("10R出玉","約1500個")]
        for i,(k,v) in enumerate(rows):
            sc=pop(s,0.3+i*0.8)
            if sc<=0: continue
            y=430+i*190
            d.rounded_rectangle([80,y,W-80,y+160],30,fill="white")
            d.text((120,y+40),k,font=F(BD,58),fill="#333")
            fv=F(BK,80); w=d.textlength(v,font=fv); d.text((W-120-w,y+25),v,font=fv,fill="#D4142F")
        foot(d,"※RUSH突入率はヘソ当たり時。数値は各機種情報サイト調べ")
        return im
    if t<SCN[2][1]:
        s=t-SCN[2][0]; im=bg(t,"#0B3D2E","#0F5240"); header(im); d=ImageDraw.Draw(im)
        ctext(d,280,"初当たりまで",F(BK,100),"white",6)
        ctext(d,410,"平均いくら？",F(BK,100),"#FFE45C",6)
        if s>1.0:
            d.rounded_rectangle([80,600,W-80,820],30,fill="#FFFFFF")
            ctext(d,630,"1000円で18回まわる台なら",F(BD,56),"#333")
            ctext(d,720,"319.7 ÷ 18 × 1000円",F(BD,56),"#666")
        n=int(17800*min(1,max(0,(s-2.0)/1.5)))
        if s>2.0: stamp(im,f"約{n:,}円",F(BK,190),"#FFE45C",900,pop(s,2.0,0.3) if s<3.5 else 1,14,"#002B1F")
        if s>4.2: ctext(d,1400,"※あくまで平均。ハマれば青天井",F(BK,56),"white",5)
        return im
    if t<SCN[3][1]:
        s=t-SCN[3][0]; im=bg(t,"#3A0CA3","#4A1BB8"); header(im); d=ImageDraw.Draw(im)
        ctext(d,300,"RUSHに入れば",F(BK,100),"white",6)
        stamp(im,"平均10連",F(BK,230),"#FFE45C",420,pop(s,0.5),14,"#1A0050")
        if s>2.0:
            d.rounded_rectangle([80,1050,W-80,1350],30,fill="white")
            ctext(d,1080,"ただし…",F(BK,60),"#333")
            ctext(d,1170,"RUSHに入る確率は 約59%",F(BK,66),"#D4142F")
            ctext(d,1260,"10連以上できるのは 約39%",F(BD,52),"#333")
        foot(d,"継続率90%で計算（0.9の9乗＝約39%）")
        return im
    s=t-SCN[4][0]; im=bg(t,"#222","#2E2E2E"); header(im); d=ImageDraw.Draw(im)
    ctext(d,330,"借金介護士のひとこと",F(BD,60),"#AAAAAA")
    stamp(im,"1万8千円…",F(BK,150),"white",430,pop(s,0.3),10)
    if s>1.2: ctext(d,850,"それ、ぼくの今月の食費です",F(BK,72),"#FFE45C",6)
    if s>2.6: stamp(im,"今日も計算だけで満足…",F(BK,96),"#FF6B6B",1000,pop(s,2.6),8)
    ctext(d,1480,"遊技は18歳以上・ほどほどに",F(BD,44),"white")
    foot(d,"この動画はAIで制作しています")
    return im
# AI制作の常時表示（2026-11-04 監査指摘：途中から見た人にも分かるよう全編に表示。上部の黒帯の直下・左上）
def ai_badge(im):
    d=ImageDraw.Draw(im); f=F(BK,34); s="AI制作"
    w=d.textlength(s,font=f); x0,y0=24,204
    d.rounded_rectangle([x0,y0,x0+w+36,y0+54],14,fill="#000000",outline="#FFE45C",width=3)
    d.text((x0+18,y0+5),s,font=f,fill="white")
T=29
p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
  "-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-c:a","aac","short.mp4"],stdin=subprocess.PIPE)
for i in range(T*FPS):
    t=i/FPS; im=frame(t); ai_badge(im); p.stdin.write(im.tobytes())
    if i in (60,200,400,600,800): im.save(f"preview_{i}.png")
p.stdin.close(); p.wait()
