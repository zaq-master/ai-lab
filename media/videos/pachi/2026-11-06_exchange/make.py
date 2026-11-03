# 3本目：計算ネタ「交換率で同じ出玉がいくらになる？」（声なし・文字＋効果、ffmpeg＋PIL）
import subprocess, math
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1080,1920,30
BK="/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"; BD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
_fc={}
def F(p,s):
    k=(p,s)
    if k not in _fc: _fc[k]=ImageFont.truetype(p,s,index=0)
    return _fc[k]
def bg(t,c1,c2):
    im=Image.new("RGB",(W,H),c1); d=ImageDraw.Draw(im)
    cx,cy=W/2,H*0.42
    for i in range(24):
        a=i*math.pi/12+t*0.4
        d.polygon([(cx,cy),(cx+3000*math.cos(a),cy+3000*math.sin(a)),(cx+3000*math.cos(a+0.13),cy+3000*math.sin(a+0.13))],fill=c2)
    return im
def ctext(d,y,s,font,fill,stroke=0,sc="#000"):
    w=d.textlength(s,font=font); d.text(((W-w)/2,y),s,font=font,fill=fill,stroke_width=stroke,stroke_fill=sc)
def pop(t,start,dur=0.35):
    x=max(0,min(1,(t-start)/dur))
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
    ctext(d,40,"計算してみた｜交換率で出玉はいくら？",F(BK,56),"#FFE45C")
    d.rectangle([0,H-150,W,H],fill="#111")
    ctext(d,H-120,"借金介護士の日常｜数字で見るパチンコ",F(BD,40),"white")
def foot(d,s):
    ctext(d,H-260,s,F(BD,32),"#DDDDDD")
SCN=[(0,3.5),(3.5,9.5),(9.5,16.5),(16.5,22.5),(22.5,28)]
DATA=[("25玉（等価）",25,20000),("28玉",28,17857),("30玉",30,16667),("33玉",33,15152)]
def frame(t):
    if t<SCN[0][1]:
        im=bg(t,"#B3001B","#D4142F"); header(im); d=ImageDraw.Draw(im)
        stamp(im,"同じ5,000玉でも",F(BK,110),"white",380,pop(t,0.1))
        n=int(4800*min(1,max(0,(t-0.5)/1.4)))
        if t>0.5: stamp(im,f"約{n:,}円差",F(BK,150),"#FFE45C",700,pop(t,0.5,0.3) if t<1.9 else 1+0.04*math.sin(t*12),16,"#5A0000")
        if t>2.1: ctext(d,1330,"…交換率って何？",F(BK,80),"white",6)
        foot(d,"※4円パチンコ・等価と33玉交換の比較（例）")
        return im
    if t<SCN[1][1]:
        s=t-SCN[1][0]; im=bg(t,"#14213D","#1D2D50"); header(im); d=ImageDraw.Draw(im)
        ctext(d,250,"今回の前提",F(BK,90),"white",6)
        rows=[("貸玉","4円（千円=250玉）"),("出玉","5,000玉"),("交換率","100円分＝◯玉"),("考えない","端数・手数料")]
        for i,(k,v) in enumerate(rows):
            sc=pop(s,0.3+i*0.6)
            if sc<=0: continue
            y=420+i*170
            d.rounded_rectangle([70,y,W-70,y+145],28,fill="white")
            d.text((110,y+40),k,font=F(BD,50),fill="#333")
            fv=F(BK,60); w=d.textlength(v,font=fv); d.text((W-110-w,y+35),v,font=fv,fill="#D4142F")
        if s>3.0:
            d.rounded_rectangle([70,1150,W-70,1400],28,fill="#FFE45C")
            ctext(d,1180,"5,000玉 ÷ 交換玉数 × 100円",F(BD,58),"#333")
            ctext(d,1280,"＝ 出玉の価値",F(BK,80),"#B3001B")
        foot(d,"※交換率はお店ごとに違います。数字は計算の例")
        return im
    if t<SCN[2][1]:
        s=t-SCN[2][0]; im=bg(t,"#0B3D2E","#0F5240"); header(im); d=ImageDraw.Draw(im)
        ctext(d,250,"5,000玉の価値は？",F(BK,90),"white",6)
        ctext(d,370,"100円に必要な玉数で比べると",F(BD,52),"#FFE45C",4)
        mx=21000; bx0=380; bw=W-90-bx0
        for i,(lab0,n,v) in enumerate(DATA):
            k=max(0,min(1,(s-0.5-i*0.6)/0.6))
            if k<=0: continue
            y=520+i*190
            d.text((70,y+28),lab0,font=F(BK,46 if i==0 else 54),fill="white")
            col="#FFE45C" if i==0 else "#FFFFFF"
            d.rounded_rectangle([bx0,y,bx0+bw*(v/mx)*k,y+110],18,fill=col)
            if k>=1:
                fl=F(BK,54); lab=f"約{v:,}円"; w=d.textlength(lab,font=fl); d.text((bx0+bw*(v/mx)-w-20,y+22),lab,font=fl,fill="#002B1F")
        if s>3.4:
            d.rounded_rectangle([70,1310,W-70,1520],28,fill="white")
            ctext(d,1335,"等価と33玉交換の差",F(BK,58),"#333")
            ctext(d,1425,"約4,800円",F(BK,66),"#D4142F")
        foot(d,"計算：5,000 ÷ 交換玉数 × 100円（端数は四捨五入）")
        return im
    if t<SCN[3][1]:
        s=t-SCN[3][0]; im=bg(t,"#3A0CA3","#4A1BB8"); header(im); d=ImageDraw.Draw(im)
        ctext(d,250,"1玉の値段で見ると",F(BK,86),"white",6)
        boxes=[("借りるとき","4.00円","#FFFFFF"),("28玉交換で戻すと","約3.57円","#FFE45C")]
        for i,(k,v,c) in enumerate(boxes):
            sc=pop(s,0.4+i*0.9)
            if sc<=0: continue
            y=420+i*300
            d.rounded_rectangle([90,y,W-90,y+250],30,fill="#1A0050")
            ctext(d,y+25,k,F(BD,54),"white")
            ctext(d,y+105,v,F(BK,110),c)
        if s>2.4: stamp(im,"1玉 約0.43円の差",F(BK,90),"#FF6B6B",1020,pop(s,2.4),10)
        if s>3.4:
            d.rounded_rectangle([70,1330,W-70,1530],28,fill="white")
            ctext(d,1355,"1,000玉なら",F(BD,54),"#333")
            ctext(d,1430,"約430円の差",F(BK,66),"#D4142F")
        foot(d,"計算：100円 ÷ 28玉 ＝ 約3.57円（4円との差 約0.43円）")
        return im
    s=t-SCN[4][0]; im=bg(t,"#222","#2E2E2E"); header(im); d=ImageDraw.Draw(im)
    ctext(d,300,"まとめ",F(BD,60),"#AAAAAA")
    ctext(d,400,"同じ出玉でも",F(BK,84),"white",6)
    if s>0.4: stamp(im,"交換率で変わる",F(BK,120),"#FFE45C",450,pop(s,0.4),12)
    if s>1.4: ctext(d,900,"交換率はお店の掲示で確認",F(BK,60),"white",5)
    if s>2.4:
        d.rounded_rectangle([70,1080,W-70,1330],28,fill="#3A3A3A")
        ctext(d,1100,"（AIナレーション／キャラのひとこと）",F(BD,40),"#AAAAAA")
        ctext(d,1180,"小さい差も、積もれば大きい…",F(BK,60),"#FFE45C",6)
    ctext(d,1480,"遊技は18歳以上・ほどほどに",F(BD,44),"white")
    foot(d,"この動画はAIで制作しています")
    return im
T=28
p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
  "-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-c:a","aac","short.mp4"],stdin=subprocess.PIPE)
for i in range(T*FPS):
    t=i/FPS; im=frame(t); p.stdin.write(im.tobytes())
    if i in (80,270,470,660,820): im.save(f"preview_{i}.png")
p.stdin.close(); p.wait()
