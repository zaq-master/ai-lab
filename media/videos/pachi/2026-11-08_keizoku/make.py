# 5本目（11/8想定）：計算ネタ「継続率80%、平均5連なのに何連で終わる人が多い？」（声なし・文字＋効果、ffmpeg＋PIL）
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
    ctext(d,40,"計算してみた｜継続率80%の本当",F(BK,56),"#FFE45C")
    d.rectangle([0,H-150,W,H],fill="#111")
    ctext(d,H-120,"借金介護士の日常｜数字で見るパチンコ",F(BD,40),"white")
def foot(d,s):
    ctext(d,H-260,s,F(BD,32),"#DDDDDD")
# 数字はすべて下の式で計算（sources.md に検算結果）。継続率80%・90%は計算用の例（特定機種の話ではない）
# 連の数え方：初当たりを1連目とし、そのあと毎回 r で次も当たる（単純化）。N連以上になる割合＝r^(N-1)
R=0.8
MEAN=round(1/(1-R))                          # 5
P_LE4=round((1-R**4)*100)                    # 4連以内で終わる 59
P_GE10=round(R**9*100)                       # 10連以上 13
DIST=[("1連(単発)",(1-R)),("2連",R*(1-R)),("3連",R**2*(1-R)),("4連",R**3*(1-R)),("5連以上",R**4)]  # 20,16,12.8,10.2,41
R2=0.9; MEAN2=round(1/(1-R2)); P2_LE9=round((1-R2**9)*100); P2_GE10=round(R2**9*100)   # 10, 61, 39
SCN=[(0,3.5),(3.5,9.5),(9.5,16),(16,22.5),(22.5,28)]
def frame(t):
    if t<SCN[0][1]:
        im=bg(t,"#B3001B","#D4142F"); header(im); d=ImageDraw.Draw(im)
        stamp(im,"継続率80%でも",F(BK,110),"white",380,pop(t,0.1))
        n=int(P_LE4*min(1,max(0,(t-0.5)/1.4)))
        if t>0.5: stamp(im,f"約{n}%",F(BK,230),"#FFE45C",700,pop(t,0.5,0.3) if t<1.9 else 1+0.04*math.sin(t*12),16,"#5A0000")
        if t>2.1: ctext(d,1330,"の人は4連以内で終わる計算",F(BK,70),"white",6)
        foot(d,"※継続率80%（計算用の例）で計算")
        return im
    if t<SCN[1][1]:
        s=t-SCN[1][0]; im=bg(t,"#14213D","#1D2D50"); header(im); d=ImageDraw.Draw(im)
        ctext(d,250,"今回の前提",F(BK,90),"white",6)
        rows=[("継続率","80%（例）"),("数え方","初当たり＝1連目"),("毎回","同じ80%で次へ"),("考えない","お金・出玉")]
        for i,(k,v) in enumerate(rows):
            sc=pop(s,0.3+i*0.6)
            if sc<=0: continue
            y=420+i*170
            d.rounded_rectangle([70,y,W-70,y+145],28,fill="white")
            d.text((110,y+40),k,font=F(BD,50),fill="#333")
            fv=F(BK,58); w=d.textlength(v,font=fv); d.text((W-110-w,y+37),v,font=fv,fill="#D4142F")
        if s>3.0:
            d.rounded_rectangle([70,1150,W-70,1400],28,fill="#FFE45C")
            ctext(d,1180,f"平均は {MEAN}連",F(BD,62),"#333")
            ctext(d,1275,"じゃあ実際は何連が多い？",F(BK,68),"#B3001B")
        foot(d,"※特定の機種の数字ではありません。計算のための例")
        return im
    if t<SCN[2][1]:
        s=t-SCN[2][0]; im=bg(t,"#3A0CA3","#4A1BB8"); header(im); d=ImageDraw.Draw(im)
        ctext(d,250,"何連で終わる？",F(BK,90),"white",6)
        ctext(d,365,"（100人が初当たりしたら）",F(BD,50),"#FFE45C",4)
        mx=0.45; bx0=330; bw=W-90-bx0
        for i,(lab0,v) in enumerate(DIST):
            k=max(0,min(1,(s-0.5-i*0.45)/0.5))
            if k<=0: continue
            y=480+i*150
            d.text((60,y+22),lab0,font=F(BK,46),fill="white")
            col="#FFE45C" if i<4 else "#FFFFFF"
            d.rounded_rectangle([bx0,y,bx0+bw*(v/mx)*k,y+100],18,fill=col)
            if k>=1:
                fl=F(BK,46); lab=f"約{v*100:.0f}人"; w=d.textlength(lab,font=fl)
                bxr=bx0+bw*(v/mx)
                if bxr-bx0>w+40: d.text((bxr-w-20,y+22),lab,font=fl,fill="#1A0050")
                else: d.text((bxr+16,y+22),lab,font=fl,fill="white")
        if s>3.4:
            d.rounded_rectangle([70,1270,W-70,1520],28,fill="white")
            ctext(d,1295,"黄色（4連以内）を足すと",F(BK,56),"#333")
            ctext(d,1395,f"約{P_LE4}人＝平均5連に届かない",F(BK,58),"#D4142F")
        foot(d,"計算：N連以上になる割合＝0.8の(N−1)乗")
        return im
    if t<SCN[3][1]:
        s=t-SCN[3][0]; im=bg(t,"#0B3D2E","#0F5240"); header(im); d=ImageDraw.Draw(im)
        ctext(d,250,"継続率90%（例）だと？",F(BK,84),"white",6)
        rows=[("平均",f"{MEAN2}連"),("9連以内で終わる",f"約{P2_LE9}%"),("10連以上",f"約{P2_GE10}%")]
        for i,(k,v) in enumerate(rows):
            if pop(s,0.4+i*0.7)<=0: continue
            y=430+i*190
            d.rounded_rectangle([70,y,W-70,y+160],28,fill="white")
            d.text((110,y+48),k,font=F(BD,54),fill="#333")
            fv=F(BK,72); w=d.textlength(v,font=fv); d.text((W-110-w,y+35),v,font=fv,fill="#0F5240")
        if s>3.0:
            d.rounded_rectangle([70,1080,W-70,1330],28,fill="#FFE45C")
            ctext(d,1105,"90%でも 平均に届かない人が",F(BK,56),"#333")
            ctext(d,1200,"半分より多い計算",F(BK,72),"#B3001B")
        foot(d,"計算：9連以内で終わる割合＝1−0.9の9乗")
        return im
    s=t-SCN[4][0]; im=bg(t,"#222","#2E2E2E"); header(im); d=ImageDraw.Draw(im)
    ctext(d,300,"まとめ",F(BD,60),"#AAAAAA")
    ctext(d,400,"継続率80%で10連以上いくのは",F(BK,60),"white",6)
    if s>0.4: stamp(im,f"約{P_GE10}%",F(BK,190),"#FFE45C",420,pop(s,0.4),12)
    if s>1.4: ctext(d,880,"たまの大連チャンが平均を引き上げている",F(BK,52),"white",5)
    if s>2.4:
        d.rounded_rectangle([70,1080,W-70,1330],28,fill="#3A3A3A")
        ctext(d,1100,"（AIナレーション／キャラのひとこと）",F(BD,40),"#AAAAAA")
        ctext(d,1180,"「平均5連」は よくある数字じゃなかった…",F(BK,50),"#FFE45C",6)
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
