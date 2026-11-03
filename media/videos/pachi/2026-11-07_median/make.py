# 4本目：計算ネタ「当たるまでの回転数のばらつき：半分の人は何回までに当たる？（中央値）」（声なし・文字＋効果、ffmpeg＋PIL）
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
    ctext(d,40,"計算してみた｜何回までに当たる？",F(BK,56),"#FFE45C")
    d.rectangle([0,H-150,W,H],fill="#111")
    ctext(d,H-120,"借金介護士の日常｜数字で見るパチンコ",F(BD,40),"white")
def foot(d,s):
    ctext(d,H-260,s,F(BD,32),"#DDDDDD")
# 数字はすべて下の式で計算（sources.md に検算結果）。p=1/319.7 は計算用の例（特定機種の話ではない）
P=1/319.7; Q=1-P
def need(c): return math.ceil(math.log(1-c)/math.log(Q))   # 累積で c 以上が当たる最小の回転数
N25,N50,N75,N90=need(0.25),need(0.5),need(0.75),need(0.9)   # 92,222,443,735
P_MEAN=round((1-Q**320)*100)                                 # 平均(約320回)までに当たる割合 63
SCN=[(0,3.5),(3.5,9.5),(9.5,15.5),(15.5,22.5),(22.5,28)]
def frame(t):
    if t<SCN[0][1]:
        im=bg(t,"#B3001B","#D4142F"); header(im); d=ImageDraw.Draw(im)
        stamp(im,"半分の人は",F(BK,120),"white",380,pop(t,0.1))
        n=int(N50*min(1,max(0,(t-0.5)/1.4)))
        if t>0.5: stamp(im,f"約{n}回",F(BK,220),"#FFE45C",700,pop(t,0.5,0.3) if t<1.9 else 1+0.04*math.sin(t*12),16,"#5A0000")
        if t>2.1: ctext(d,1330,"…までに当たる計算",F(BK,76),"white",6)
        foot(d,"※大当り確率1/319.7（計算用の例）で計算")
        return im
    if t<SCN[1][1]:
        s=t-SCN[1][0]; im=bg(t,"#14213D","#1D2D50"); header(im); d=ImageDraw.Draw(im)
        ctext(d,250,"今回の前提",F(BK,90),"white",6)
        rows=[("大当り確率","1/319.7（例）"),("当たり方","毎回転 同じ確率"),("数えるもの","初当たりの回転数"),("考えない","お金・出玉")]
        for i,(k,v) in enumerate(rows):
            sc=pop(s,0.3+i*0.6)
            if sc<=0: continue
            y=420+i*170
            d.rounded_rectangle([70,y,W-70,y+145],28,fill="white")
            d.text((110,y+40),k,font=F(BD,50),fill="#333")
            fv=F(BK,60); w=d.textlength(v,font=fv); d.text((W-110-w,y+35),v,font=fv,fill="#D4142F")
        if s>3.0:
            d.rounded_rectangle([70,1150,W-70,1400],28,fill="#FFE45C")
            ctext(d,1180,"平均は 319.7回",F(BD,62),"#333")
            ctext(d,1275,"じゃあ真ん中の人は？",F(BK,72),"#B3001B")
        foot(d,"※特定の機種の数字ではありません。計算のための例")
        return im
    if t<SCN[2][1]:
        s=t-SCN[2][0]; im=bg(t,"#0B3D2E","#0F5240"); header(im); d=ImageDraw.Draw(im)
        ctext(d,250,"100人が打ったら",F(BK,90),"white",6)
        ctext(d,370,"真ん中の人は？",F(BK,90),"#FFE45C",6)
        n=int(N50*min(1,max(0,(s-0.8)/1.2)))
        if s>0.8: stamp(im,f"約{n}回",F(BK,230),"#FFE45C",520,pop(s,0.8,0.3) if s<2.0 else 1,14,"#002B1F")
        if s>2.4:
            x0,x1,y=90,W-90,1130
            d.rounded_rectangle([x0,y,x1,y+90],20,fill="#33554A")
            d.rounded_rectangle([x0,y,x0+(x1-x0)*0.5,y+90],20,fill="#FFE45C")
            d.text((x0+20,y+14),f"{N50}回までに 50%",font=F(BK,46),fill="#002B1F")
            fs=F(BK,46); w=d.textlength("まだ 50%",font=fs); d.text((x1-20-w,y+14),"まだ 50%",font=fs,fill="white")
        if s>3.6: ctext(d,1300,"平均（319.7回）より約100回少ない",F(BK,56),"white",5)
        foot(d,"計算：1−(1−1/319.7)のn乗が50%を超える最小のn＝222")
        return im
    if t<SCN[3][1]:
        s=t-SCN[3][0]; im=bg(t,"#3A0CA3","#4A1BB8"); header(im); d=ImageDraw.Draw(im)
        ctext(d,250,"何回までに当たる？",F(BK,86),"white",6)
        ctext(d,365,"（当たった人の割合）",F(BD,52),"#FFE45C",4)
        data=[("4人に1人",N25),("2人に1人",N50),("4人に3人",N75),("10人に9人",N90)]
        mx=800; bx0=340; bw=W-90-bx0
        for i,(lab0,v) in enumerate(data):
            k=max(0,min(1,(s-0.5-i*0.5)/0.6))
            if k<=0: continue
            y=500+i*170
            d.text((70,y+24),lab0,font=F(BK,50),fill="white")
            col="#FFE45C" if v==N50 else "#FFFFFF"
            d.rounded_rectangle([bx0,y,bx0+bw*(v/mx)*k,y+110],18,fill=col)
            if k>=1:
                fl=F(BK,50); lab=f"{v}回"; w=d.textlength(lab,font=fl)
                bxr=bx0+bw*(v/mx)
                if bxr-bx0>w+40: d.text((bxr-w-20,y+24),lab,font=fl,fill="#1A0050")
                else: d.text((bxr+16,y+24),lab,font=fl,fill="white")
        if s>3.2:
            d.rounded_rectangle([70,1250,W-70,1500],28,fill="white")
            ctext(d,1275,f"約10人に1人は",F(BK,58),"#333")
            ctext(d,1375,f"{N90}回でもまだ当たらない計算",F(BK,58),"#D4142F")
        foot(d,"計算：n回までに当たる割合＝1−(1−1/319.7)のn乗")
        return im
    s=t-SCN[4][0]; im=bg(t,"#222","#2E2E2E"); header(im); d=ImageDraw.Draw(im)
    ctext(d,300,"まとめ",F(BD,60),"#AAAAAA")
    ctext(d,400,"平均の約320回までに当たるのは",F(BK,62),"white",6)
    if s>0.4: stamp(im,f"約{P_MEAN}%",F(BK,190),"#FFE45C",420,pop(s,0.4),12)
    if s>1.4: ctext(d,880,"長いハマりが平均を引き上げている",F(BK,56),"white",5)
    if s>2.4:
        d.rounded_rectangle([70,1080,W-70,1330],28,fill="#3A3A3A")
        ctext(d,1100,"（AIナレーション／キャラのひとこと）",F(BD,40),"#AAAAAA")
        ctext(d,1180,"自分がどっち側かは選べない…",F(BK,60),"#FFE45C",6)
    ctext(d,1480,"遊技は18歳以上・ほどほどに",F(BD,44),"white")
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
