# 9本目（11/12想定）：計算ネタ「当たった回数では 甘い台と辛い台を見分けられない」（声なし・文字＋効果、ffmpeg＋PIL）
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
    ctext(d,40,"計算してみた｜台の見分け",F(BK,50),"#FFE45C")
    d.rectangle([0,H-150,W,H],fill="#111")
    ctext(d,H-120,"借金介護士の日常｜数字で見るパチンコ",F(BD,40),"white")
def foot(d,s):
    ctext(d,H-260,s,F(BD,32),"#DDDDDD")
# 数字はすべて下の式で計算（sources.md と check.log に検算結果）。1/199.8・1/319.7は計算用の例（特定機種の話ではない）
# 前提：1回転ごとの当たり確率は毎回同じ。2台は無関係（独立）。比べるのは同じ回転数での当たり回数だけ（お金・出玉・回転率は考えない）
import numpy as np
from scipy.stats import binom
PA,PB=1/199.8,1/319.7
def cmp(n):
    k=np.arange(n+1); A=binom.pmf(k,n,PA); B=binom.pmf(k,n,PB); cA=np.cumsum(A)
    gt=(B[1:]*cA[:-1]).sum(); eq=(A*B).sum()
    return gt,eq                                  # 辛い台の当たりが多い確率／同じ確率
NS=[300,1000,3000,10000]
R={n:cmp(n) for n in NS}
ROWS=[(f"{n:,}回",sum(R[n])) for n in NS]          # 49.6/31.5/14.8/2.1%
H300=round(sum(R[300])*100)                       # 50
G1,E1=R[1000]
M_A=round(1000*PA); M_B=round(1000*PB,0)          # 5 / 3
GT1=round(G1*100); EQ1=round(E1*100); GE1=round((G1+E1)*100)   # 20 / 12 / 31
RATIO=319.7/199.8                                 # 1.6
SCN=[(0,4),(4,9.5),(9.5,17),(17,22.5),(22.5,28)]
def frame(t):
    if t<SCN[0][1]:
        im=bg(t,"#B3001B","#D4142F"); header(im); d=ImageDraw.Draw(im)
        stamp(im,"甘い台 vs 辛い台",F(BK,104),"white",330,pop(t,0.1))
        if t>0.6: ctext(d,640,"300回で 辛い台が“同点以上”の確率",F(BK,58),"#FFE45C",6)
        if t>1.6:
            n=int(H300*min(1,max(0,(t-1.6)/1.0)))
            stamp(im,f"約{n}%",F(BK,230),"#FFE45C",720,pop(t,1.6,0.3) if t<2.8 else 1+0.04*math.sin(t*12),16,"#5A0000")
        if t>2.9: ctext(d,1330,"当たりやすさは 1.6倍ちがうのに",F(BK,64),"white",6)
        foot(d,"※確率1/199.8・1/319.7（どちらも計算用の例）")
        return im
    if t<SCN[1][1]:
        s=t-SCN[1][0]; im=bg(t,"#14213D","#1D2D50"); header(im); d=ImageDraw.Draw(im)
        ctext(d,250,"今回の前提",F(BK,90),"white",6)
        rows=[("甘い台","1/199.8（例）"),("辛い台","1/319.7（例）"),("比べるもの","当たった回数")]
        for i,(k,v) in enumerate(rows):
            if pop(s,0.3+i*0.6)<=0: continue
            y=430+i*180
            d.rounded_rectangle([70,y,W-70,y+150],28,fill="white")
            d.text((110,y+44),k,font=F(BD,50),fill="#333")
            fv=F(BK,58); w=d.textlength(v,font=fv); d.text((W-110-w,y+40),v,font=fv,fill="#D4142F")
        if s>2.6:
            d.rounded_rectangle([70,1030,W-70,1280],28,fill="#FFE45C")
            ctext(d,1060,"同じ回数まわして 当たり回数を比べる",F(BD,50),"#333")
            ctext(d,1155,f"本当は甘い台が{RATIO:.1f}倍 当たりやすい",F(BK,56),"#B3001B")
        foot(d,"※特定の機種の数字ではありません。計算のための例")
        return im
    if t<SCN[2][1]:
        s=t-SCN[2][0]; im=bg(t,"#3A0CA3","#4A1BB8"); header(im); d=ImageDraw.Draw(im)
        ctext(d,250,"辛い台が 同点以上になる確率",F(BK,70),"white",6)
        ctext(d,365,"（まわした回数ごと）",F(BD,50),"#FFE45C",4)
        mx=1.0; bx0=300; bw=W-260-bx0
        for i,(lab0,v) in enumerate(ROWS):
            k=max(0,min(1,(s-0.5-i*0.4)/0.4))
            if k<=0: continue
            y=480+i*150
            d.text((40,y+18),lab0,font=F(BK,46),fill="white")
            d.rounded_rectangle([bx0,y,bx0+max(8,bw*(v/mx)*k),y+100],18,fill="#FFE45C")
            if k>=1: d.text((bx0+max(8,bw*(v/mx))+16,y+20),f"約{v*100:.0f}%",font=F(BK,46),fill="white")
        if s>3.4:
            d.rounded_rectangle([70,1290,W-70,1520],28,fill="white")
            ctext(d,1310,"数百〜数千回では",F(BK,56),"#333")
            ctext(d,1405,"逆転・引き分けがよく起きる",F(BK,60),"#D4142F")
        foot(d,"計算：当たり回数を二項分布で計算し2台を比較")
        return im
    if t<SCN[3][1]:
        s=t-SCN[3][0]; im=bg(t,"#0B3D2E","#0F5240"); header(im); d=ImageDraw.Draw(im)
        ctext(d,250,"1000回ずつ まわすと？",F(BK,84),"white",6)
        rows=[("平均",f"甘い約{M_A}回 対 辛い約{M_B:.0f}回"),("辛い台の方が多い",f"約{GT1}%"),("同じ回数",f"約{EQ1}%")]
        for i,(k,v) in enumerate(rows):
            if pop(s,0.4+i*0.7)<=0: continue
            y=430+i*190
            d.rounded_rectangle([70,y,W-70,y+160],28,fill="white")
            d.text((110,y+50),k,font=F(BD,48),fill="#333")
            fv=F(BK,56); w=d.textlength(v,font=fv); d.text((W-110-w,y+44),v,font=fv,fill="#0F5240")
        if s>2.9:
            d.rounded_rectangle([70,1080,W-70,1330],28,fill="#FFE45C")
            ctext(d,1105,f"約{GE1}%＝3回に1回くらいは",F(BK,56),"#333")
            ctext(d,1200,"甘い台が勝てない",F(BK,62),"#B3001B")
        foot(d,"※毎回同じ確率で抽選する、とした場合の計算")
        return im
    s=t-SCN[4][0]; im=bg(t,"#222","#2E2E2E"); header(im); d=ImageDraw.Draw(im)
    ctext(d,300,"まとめ",F(BD,60),"#AAAAAA")
    ctext(d,400,"少ない回数の当たり数では",F(BK,60),"white",6)
    if s>0.4: stamp(im,"台の差は見えない",F(BK,108),"#FFE45C",430,pop(s,0.4),12)
    if s>1.4: ctext(d,880,"1万回でも 約2%は辛い台が同点以上",F(BK,48),"white",5)
    if s>2.4:
        d.rounded_rectangle([70,1080,W-70,1330],28,fill="#3A3A3A")
        ctext(d,1100,"（AIナレーション／キャラのひとこと）",F(BD,40),"#AAAAAA")
        ctext(d,1180,"昨日よく当たった台 ≠ 甘い台…",F(BK,50),"#FFE45C",6)
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
