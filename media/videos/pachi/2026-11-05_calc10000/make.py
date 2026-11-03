# 2本目：計算ネタ「1万円で何回まわる？」（声なし・文字＋効果、ffmpeg＋PIL）
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
    ctext(d,40,"計算してみた｜1万円で何回まわる？",F(BK,56),"#FFE45C")
    d.rectangle([0,H-150,W,H],fill="#111")
    ctext(d,H-120,"借金介護士の日常｜数字で見るパチンコ",F(BD,40),"white")
def foot(d,s):
    ctext(d,H-260,s,F(BD,32),"#DDDDDD")
SCN=[(0,3.5),(3.5,9.5),(9.5,15.5),(15.5,22.5),(22.5,28)]
def frame(t):
    if t<SCN[0][1]:
        im=bg(t,"#B3001B","#D4142F"); header(im); d=ImageDraw.Draw(im)
        stamp(im,"1万円で",F(BK,130),"white",380,pop(t,0.1))
        n=int(180*min(1,max(0,(t-0.5)/1.4)))
        if t>0.5: stamp(im,f"約{n}回",F(BK,220),"#FFE45C",700,pop(t,0.5,0.3) if t<1.9 else 1+0.04*math.sin(t*12),16,"#5A0000")
        if t>2.1: ctext(d,1330,"…で、当たるの？",F(BK,80),"white",6)
        foot(d,"※1000円で18回まわる台で計算")
        return im
    if t<SCN[1][1]:
        s=t-SCN[1][0]; im=bg(t,"#14213D","#1D2D50"); header(im); d=ImageDraw.Draw(im)
        ctext(d,250,"今回の前提",F(BK,90),"white",6)
        rows=[("貸玉","4円（千円=250玉）"),("回転率","千円で18回"),("大当り確率","1/319.7"),("計算するお金","現金投資のみ")]
        for i,(k,v) in enumerate(rows):
            sc=pop(s,0.3+i*0.6)
            if sc<=0: continue
            y=420+i*170
            d.rounded_rectangle([70,y,W-70,y+145],28,fill="white")
            d.text((110,y+40),k,font=F(BD,50),fill="#333")
            fv=F(BK,60); w=d.textlength(v,font=fv); d.text((W-110-w,y+35),v,font=fv,fill="#D4142F")
        if s>3.0:
            d.rounded_rectangle([70,1150,W-70,1400],28,fill="#FFE45C")
            ctext(d,1180,"10,000円 ÷ 1,000円 × 18回",F(BD,58),"#333")
            ctext(d,1280,"＝ 180回",F(BK,80),"#B3001B")
        foot(d,"※1/319.7はミドル帯によくある確率の一例。持ち玉は考えない")
        return im
    if t<SCN[2][1]:
        s=t-SCN[2][0]; im=bg(t,"#0B3D2E","#0F5240"); header(im); d=ImageDraw.Draw(im)
        ctext(d,270,"180回で1回でも",F(BK,96),"white",6)
        ctext(d,400,"当たる確率は？",F(BK,96),"#FFE45C",6)
        n=int(43*min(1,max(0,(s-0.8)/1.2)))
        if s>0.8: stamp(im,f"約{n}%",F(BK,250),"#FFE45C",560,pop(s,0.8,0.3) if s<2.0 else 1,14,"#002B1F")
        if s>2.4:
            # 100%バー
            x0,x1,y=90,W-90,1160
            d.rounded_rectangle([x0,y,x1,y+90],20,fill="#33554A")
            d.rounded_rectangle([x0,y,x0+(x1-x0)*0.431,y+90],20,fill="#FFE45C")
            d.text((x0+20,y+14),"当たる 43%",font=F(BK,48),fill="#002B1F")
            fs=F(BK,48); w=d.textlength("当たらない 57%",font=fs); d.text((x1-20-w,y+14),"当たらない 57%",font=fs,fill="white")
        if s>3.6: ctext(d,1330,"半分以上は1万円で当たらない計算",F(BK,58),"white",5)
        foot(d,"計算：1−(1−1/319.7)の180乗＝約43.1%")
        return im
    if t<SCN[3][1]:
        s=t-SCN[3][0]; im=bg(t,"#3A0CA3","#4A1BB8"); header(im); d=ImageDraw.Draw(im)
        ctext(d,250,"初当たりまで平均いくら？",F(BK,76),"white",6)
        ctext(d,360,"回転率で比べると…",F(BD,56),"#FFE45C",4)
        data=[(16,19981),(18,17761),(20,15985),(22,14532)]
        mx=22000; bx0=330; bw=W-110-bx0
        for i,(r,v) in enumerate(data):
            k=max(0,min(1,(s-0.5-i*0.5)/0.6))
            if k<=0: continue
            y=520+i*190
            d.text((90,y+20),f"千円{r}回",font=F(BK,52),fill="white")
            col="#FFE45C" if r==18 else "#FFFFFF"
            d.rounded_rectangle([bx0,y,bx0+bw*(v/mx)*k,y+110],18,fill=col)
            lab=f"約{v/10000:.1f}万円" if k>=1 else ""
            if lab:
                fl=F(BK,54); w=d.textlength(lab,font=fl); d.text((bx0+bw*(v/mx)-w-20,y+22),lab,font=fl,fill="#1A0050")
        if s>3.2:
            d.rounded_rectangle([70,1310,W-70,1520],28,fill="white")
            ctext(d,1335,"千円18回→16回になると",F(BK,58),"#333")
            ctext(d,1425,"平均 約2,200円アップ",F(BK,66),"#D4142F")
        foot(d,"計算：319.7 ÷ 回転率 × 1,000円（あくまで平均）")
        return im
    s=t-SCN[4][0]; im=bg(t,"#222","#2E2E2E"); header(im); d=ImageDraw.Draw(im)
    ctext(d,300,"ちなみに",F(BD,60),"#AAAAAA")
    ctext(d,400,"1000回ハマる確率",F(BK,80),"white",6)
    if s>0.4: stamp(im,"約4.4%",F(BK,200),"#FF6B6B",450,pop(s,0.4),12)
    if s>1.6: ctext(d,960,"＝ 23人に1人くらい",F(BK,66),"white",5)
    if s>2.6:
        ctext(d,1130,"借金介護士のひとこと",F(BD,48),"#AAAAAA")
        ctext(d,1210,"平均は「平均」でしかない…",F(BK,64),"#FFE45C",6)
    ctext(d,1480,"遊技は18歳以上・ほどほどに",F(BD,44),"white")
    foot(d,"この動画はAIで制作しています")
    return im
T=28
p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
  "-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-c:a","aac","short.mp4"],stdin=subprocess.PIPE)
for i in range(T*FPS):
    t=i/FPS; im=frame(t); p.stdin.write(im.tobytes())
    if i in (80,260,420,640,820): im.save(f"preview_{i}.png")
p.stdin.close(); p.wait()
