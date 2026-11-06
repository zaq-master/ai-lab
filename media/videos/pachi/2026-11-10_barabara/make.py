# 7本目（11/10想定）：計算ネタ「1000回まわした当たり回数はバラバラ」（二項分布）（声なし・文字＋効果、ffmpeg＋PIL）
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
    ctext(d,40,"計算してみた｜同じ確率でもバラバラ",F(BK,50),"#FFE45C")
    d.rectangle([0,H-150,W,H],fill="#111")
    ctext(d,H-120,"借金介護士の日常｜数字で見るパチンコ",F(BD,40),"white")
def foot(d,s):
    ctext(d,H-260,s,F(BD,32),"#DDDDDD")
# 数字はすべて下の式で計算（sources.md に検算結果）。1/319.7は計算用の例（特定機種の話ではない）
# 前提：1回転ごとの当たり確率は毎回同じ、1000回まわす（お金・出玉・回転率は考えない）
from math import comb
P=1/319.7; N=1000
PR=[comb(N,k)*P**k*(1-P)**(N-k) for k in range(N+1)]
ROWS=[("0回",PR[0]),("1回",PR[1]),("2回",PR[2]),("3回",PR[3]),("4回",PR[4]),("5回以上",sum(PR[5:]))]
ZERO=round(PR[0]*100)          # 4
MEAN=round(N*P,1)              # 3.1
EXACT3=round(PR[3]*100)        # 22
LE2=round(sum(PR[:3])*100)     # 39
SCN=[(0,4),(4,9.5),(9.5,17),(17,22.5),(22.5,28)]
def frame(t):
    if t<SCN[0][1]:
        im=bg(t,"#B3001B","#D4142F"); header(im); d=ImageDraw.Draw(im)
        stamp(im,"1000回まわして",F(BK,104),"white",330,pop(t,0.1))
        if t>0.6: ctext(d,640,"当たり0回の人は？",F(BK,76),"#FFE45C",6)
        if t>1.6:
            n=int(ZERO*min(1,max(0,(t-1.6)/1.0)))
            stamp(im,f"約{n}%",F(BK,230),"#FFE45C",720,pop(t,1.6,0.3) if t<2.8 else 1+0.04*math.sin(t*12),16,"#5A0000")
        if t>2.9: ctext(d,1330,"同じ確率でも結果はバラバラ",F(BK,68),"white",6)
        foot(d,"※大当り確率1/319.7（計算用の例）で計算")
        return im
    if t<SCN[1][1]:
        s=t-SCN[1][0]; im=bg(t,"#14213D","#1D2D50"); header(im); d=ImageDraw.Draw(im)
        ctext(d,250,"今回の前提",F(BK,90),"white",6)
        rows=[("大当り確率","1/319.7（例）"),("まわす回数","1000回"),("考えない","お金・出玉")]
        for i,(k,v) in enumerate(rows):
            if pop(s,0.3+i*0.6)<=0: continue
            y=430+i*180
            d.rounded_rectangle([70,y,W-70,y+150],28,fill="white")
            d.text((110,y+44),k,font=F(BD,50),fill="#333")
            fv=F(BK,58); w=d.textlength(v,font=fv); d.text((W-110-w,y+40),v,font=fv,fill="#D4142F")
        if s>2.6:
            d.rounded_rectangle([70,1030,W-70,1280],28,fill="#FFE45C")
            ctext(d,1060,"100人が同じ条件で打ったら",F(BD,58),"#333")
            ctext(d,1155,"当たり回数はどう散らばる？",F(BK,62),"#B3001B")
        foot(d,"※特定の機種の数字ではありません。計算のための例")
        return im
    if t<SCN[2][1]:
        s=t-SCN[2][0]; im=bg(t,"#3A0CA3","#4A1BB8"); header(im); d=ImageDraw.Draw(im)
        ctext(d,250,"1000回での当たり回数",F(BK,80),"white",6)
        ctext(d,365,"（100人中 何人くらい？）",F(BD,50),"#FFE45C",4)
        mx=0.27; bx0=330; bw=W-230-bx0
        for i,(lab0,v) in enumerate(ROWS):
            k=max(0,min(1,(s-0.5-i*0.4)/0.4))
            if k<=0: continue
            y=480+i*130
            d.text((50,y+18),lab0,font=F(BK,46),fill="white")
            d.rounded_rectangle([bx0,y,bx0+bw*(v/mx)*k,y+90],18,fill="#FFE45C")
            if k>=1: d.text((bx0+bw*(v/mx)+16,y+16),f"約{v*100:.0f}人",font=F(BK,46),fill="white")
        if s>3.4:
            d.rounded_rectangle([70,1290,W-70,1520],28,fill="white")
            ctext(d,1310,"0回の人も 5回以上の人も",F(BK,56),"#333")
            ctext(d,1405,"同じ確率で打っている",F(BK,64),"#D4142F")
        foot(d,"計算：二項分布（1000回・1回ごと1/319.7）")
        return im
    if t<SCN[3][1]:
        s=t-SCN[3][0]; im=bg(t,"#0B3D2E","#0F5240"); header(im); d=ImageDraw.Draw(im)
        ctext(d,250,"平均どおりになる？",F(BK,84),"white",6)
        rows=[("平均の当たり",f"約{MEAN}回"),("ちょうど3回",f"約{EXACT3}%だけ"),("2回以下",f"約{LE2}%")]
        for i,(k,v) in enumerate(rows):
            if pop(s,0.4+i*0.7)<=0: continue
            y=430+i*190
            d.rounded_rectangle([70,y,W-70,y+160],28,fill="white")
            d.text((110,y+50),k,font=F(BD,50),fill="#333")
            fv=F(BK,60); w=d.textlength(v,font=fv); d.text((W-110-w,y+42),v,font=fv,fill="#0F5240")
        if s>2.9:
            d.rounded_rectangle([70,1080,W-70,1330],28,fill="#FFE45C")
            ctext(d,1105,"1000回くらいでは",F(BK,58),"#333")
            ctext(d,1200,"運の幅がとても大きい",F(BK,68),"#B3001B")
        foot(d,"※毎回同じ確率で抽選する、とした場合の計算")
        return im
    s=t-SCN[4][0]; im=bg(t,"#222","#2E2E2E"); header(im); d=ImageDraw.Draw(im)
    ctext(d,300,"まとめ",F(BD,60),"#AAAAAA")
    ctext(d,400,"同じ確率・同じ1000回でも",F(BK,60),"white",6)
    if s>0.4: stamp(im,"0回〜5回以上",F(BK,120),"#FFE45C",430,pop(s,0.4),12)
    if s>1.4: ctext(d,880,"結果の差は「台の良し悪し」とは限らない",F(BK,46),"white",5)
    if s>2.4:
        d.rounded_rectangle([70,1080,W-70,1330],28,fill="#3A3A3A")
        ctext(d,1100,"（AIナレーション／キャラのひとこと）",F(BD,40),"#AAAAAA")
        ctext(d,1180,"「次で取り返す」に根拠はない…",F(BK,54),"#FFE45C",6)
    ctext(d,1370,"遊技は18歳以上・ほどほどに",F(BD,44),"white")
    d.rounded_rectangle([60,1450,W-60,1590],24,fill="#000000",outline="#FFFFFF",width=3)
    ctext(d,1465,"のめり込みの相談：リカバリーサポート・ネットワーク",F(BD,36),"white")
    ctext(d,1515,"050-3541-6420",F(BK,52),"#FFE45C")
    foot(d,"この動画はAIで制作しています")
    return im
# AI制作の常時表示（2026-11-04 監査指摘：途中から見た人にも分かるよう全編に表示。上部の黒帯の直下・左上）
def ai_badge(im):
    d=ImageDraw.Draw(im); f=F(BK,34); s="AI制作"
    w=d.textlength(s,font=f); x0,y0=24,204
    d.rounded_rectangle([x0,y0,x0+w+36,y0+54],14,fill="#000000",outline="#FFE45C",width=3)
    d.text((x0+18,y0+5),s,font=f,fill="white")
T=28
p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
  "-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-c:a","aac","short.mp4"],stdin=subprocess.PIPE)
for i in range(T*FPS):
    t=i/FPS; im=frame(t); ai_badge(im); p.stdin.write(im.tobytes())
p.stdin.close(); p.wait()
