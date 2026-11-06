# 10本目（11/13想定）：計算ネタ「台を移っても 当たる確率は変わらない（合計回転数が同じなら同じ）」（声なし・文字＋効果、ffmpeg＋PIL）
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
    ctext(d,40,"計算してみた｜台移動",F(BK,50),"#FFE45C")
    d.rectangle([0,H-150,W,H],fill="#111")
    ctext(d,H-120,"借金介護士の日常｜数字で見るパチンコ",F(BD,40),"white")
def foot(d,s):
    ctext(d,H-260,s,F(BD,32),"#DDDDDD")
# 数字はすべて下の式で計算（sources.md と check.log に検算結果）。1/319.7は計算用の例（特定機種の話ではない）
# 前提：どの台も同じ確率1/319.7（同じ種類の台の例）。1回転ごとの抽選は独立で、台を移っても変わらない。合計500回で比べる（お金・出玉・回転率は考えない）
P=1/319.7; N=500
PLANS=[(1,500),(2,250),(5,100),(10,50)]
def hit(k,m): return 1-((1-P)**m)**k            # k台×m回で1回以上当たる確率
ROWS=[(f"{k}台×{m}回",hit(k,m)) for k,m in PLANS]  # すべて 79.1%
HIT=round(hit(1,N)*100)                            # 79
MISS=round((1-P)**N*100)                         # 21
AVG=N*P                                          # 1.56
SCN=[(0,4),(4,9.5),(9.5,17),(17,22.5),(22.5,28)]
def frame(t):
    if t<SCN[0][1]:
        im=bg(t,"#B3001B","#D4142F"); header(im); d=ImageDraw.Draw(im)
        stamp(im,"台を移れば当たる？",F(BK,100),"white",330,pop(t,0.1))
        if t>0.6: ctext(d,640,"合計500回で 1回以上当たる確率",F(BK,58),"#FFE45C",6)
        if t>1.6:
            n=int(HIT*min(1,max(0,(t-1.6)/1.0)))
            stamp(im,f"約{n}%",F(BK,230),"#FFE45C",720,pop(t,1.6,0.3) if t<2.8 else 1+0.04*math.sin(t*12),16,"#5A0000")
        if t>2.9: ctext(d,1330,"1台でも 10台に分けても 同じ",F(BK,64),"white",6)
        foot(d,"※確率1/319.7（計算用の例）")
        return im
    if t<SCN[1][1]:
        s=t-SCN[1][0]; im=bg(t,"#14213D","#1D2D50"); header(im); d=ImageDraw.Draw(im)
        ctext(d,250,"今回の前提",F(BK,90),"white",6)
        rows=[("どの台も","1/319.7（例）"),("合計","500回まわす"),("比べるもの","1回以上当たる確率")]
        for i,(k,v) in enumerate(rows):
            if pop(s,0.3+i*0.6)<=0: continue
            y=430+i*180
            d.rounded_rectangle([70,y,W-70,y+150],28,fill="white")
            d.text((110,y+44),k,font=F(BD,50),fill="#333")
            fv=F(BK,58); w=d.textlength(v,font=fv); d.text((W-110-w,y+40),v,font=fv,fill="#D4142F")
        if s>2.6:
            d.rounded_rectangle([70,1030,W-70,1280],28,fill="#FFE45C")
            ctext(d,1060,"1台で500回 と 台を移りながら500回",F(BD,50),"#333")
            ctext(d,1155,"当たりやすさは ちがう？",F(BK,60),"#B3001B")
        foot(d,"※特定の機種の数字ではありません。計算のための例")
        return im
    if t<SCN[2][1]:
        s=t-SCN[2][0]; im=bg(t,"#3A0CA3","#4A1BB8"); header(im); d=ImageDraw.Draw(im)
        ctext(d,250,"1回以上 当たる確率",F(BK,76),"white",6)
        ctext(d,365,"（合計500回の分け方ごと）",F(BD,50),"#FFE45C",4)
        mx=1.0; bx0=330; bw=W-230-bx0
        for i,(lab0,v) in enumerate(ROWS):
            k=max(0,min(1,(s-0.5-i*0.4)/0.4))
            if k<=0: continue
            y=480+i*150
            d.text((40,y+18),lab0,font=F(BK,44),fill="white")
            d.rounded_rectangle([bx0,y,bx0+max(8,bw*(v/mx)*k),y+100],18,fill="#FFE45C")
            if k>=1: d.text((bx0+max(8,bw*(v/mx))+16,y+20),f"約{v*100:.0f}%",font=F(BK,46),fill="white")
        if s>3.4:
            d.rounded_rectangle([70,1290,W-70,1520],28,fill="white")
            ctext(d,1310,"どう分けても",F(BK,56),"#333")
            ctext(d,1405,"ぜんぶ 約%d%%"%HIT,F(BK,64),"#D4142F")
        foot(d,"計算：1−(1−1/319.7)の500乗")
        return im
    if t<SCN[3][1]:
        s=t-SCN[3][0]; im=bg(t,"#0B3D2E","#0F5240"); header(im); d=ImageDraw.Draw(im)
        ctext(d,250,"なぜ 同じになる？",F(BK,84),"white",6)
        rows=[("1回の抽選","どの台でも 1/319.7"),("500回 全部ハズレ",f"約{MISS}%"),("平均の当たり回数",f"約{AVG:.1f}回")]
        for i,(k,v) in enumerate(rows):
            if pop(s,0.4+i*0.7)<=0: continue
            y=430+i*190
            d.rounded_rectangle([70,y,W-70,y+160],28,fill="white")
            d.text((110,y+50),k,font=F(BD,46),fill="#333")
            fv=F(BK,54); w=d.textlength(v,font=fv); d.text((W-110-w,y+46),v,font=fv,fill="#0F5240")
        if s>2.9:
            d.rounded_rectangle([70,1080,W-70,1330],28,fill="#FFE45C")
            ctext(d,1105,"ハズレの掛け算は 何台に分けても",F(BK,50),"#333")
            ctext(d,1200,"同じ500回分",F(BK,62),"#B3001B")
        foot(d,"※どの台も同じ確率で毎回抽選する、とした場合の計算")
        return im
    s=t-SCN[4][0]; im=bg(t,"#222","#2E2E2E"); header(im); d=ImageDraw.Draw(im)
    ctext(d,300,"まとめ",F(BD,60),"#AAAAAA")
    ctext(d,400,"同じ確率の台なら 移っても",F(BK,60),"white",6)
    if s>0.4: stamp(im,"当たりやすさは同じ",F(BK,100),"#FFE45C",430,pop(s,0.4),12)
    if s>1.4: ctext(d,880,"変わるのは “まわした合計回数” だけ",F(BK,48),"white",5)
    if s>2.4:
        d.rounded_rectangle([70,1080,W-70,1330],28,fill="#3A3A3A")
        ctext(d,1100,"（AIナレーション／キャラのひとこと）",F(BD,40),"#AAAAAA")
        ctext(d,1180,"台を変えても 流れは変わらない…",F(BK,50),"#FFE45C",6)
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
