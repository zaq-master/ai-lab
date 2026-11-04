import subprocess, math, random, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS,T=1080,1920,30,30.0
BK="/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"; BD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
_fc={}
def F(p,s):
    k=(p,s)
    if k not in _fc: _fc[k]=ImageFont.truetype(p,s,index=0)
    return _fc[k]
rng=random.Random(7)
# ---------- timeline ----------
SEG=[]; t=2.5
def add(kind,dur,res):
    global t; SEG.append((kind,t,t+dur,res)); t+=dur
for _ in range(3): add("spin",1.2,None)
add("reach",2.4,(7,6,7))
for _ in range(2): add("spin",1.2,None)
add("reach",2.4,(3,4,3))
add("hit",2.6,(7,7,7))
HIT=t; JACK_END=HIT+3.6; STAT_END=JACK_END+5.8
for i,s in enumerate(SEG):
    if s[0]=="spin":
        while True:
            r=(rng.randint(1,9),rng.randint(1,9),rng.randint(1,9))
            if r[0]!=r[2]: break
        SEG[i]=(s[0],s[1],s[2],r)
def spins_at(t):
    if t<2.5: return 0
    if t>=HIT: return 244
    return int(243*(t-2.5)/(HIT-2.5))
# ---------- static layers ----------
def bokeh():
    im=Image.new("RGB",(W+200,H+200),"#07060c"); d=ImageDraw.Draw(im)
    cols=["#ff2a6d","#ffd166","#05d9e8","#a06bff","#ff8c42","#ffffff"]
    r=random.Random(3)
    for _ in range(70):
        x,y,rad=r.randint(0,W+200),r.randint(0,H+200),r.randint(20,90)
        c=r.choice(cols); d.ellipse([x-rad,y-rad,x+rad,y+rad],fill=c)
    im=im.filter(ImageFilter.GaussianBlur(40))
    return Image.blend(Image.new("RGB",im.size,"#000"),im,0.55)
BOKEH=bokeh()
LW,LH=960,1240; LX,LY=60,330
DIGCOL={7:"#ff2b2b",3:"#2bd1ff",1:"#ffd84a",5:"#7dff6b",9:"#ff7ad9"}
def dcol(n): return DIGCOL.get(n,"#ffffff")
COLX=[170,480,790]; DY=600
def draw_digit(layer,n,cx,cy,alpha=255,size=330):
    d=ImageDraw.Draw(layer); f=F(BK,size); s=str(n)
    w=d.textlength(s,font=f)
    c=tuple(int(dcol(n)[i:i+2],16) for i in (1,3,5))
    d.text((cx-w/2,cy-size*0.62),s,font=f,fill=c+(alpha,),stroke_width=12,stroke_fill=(0,0,0,alpha))
def spin_col(layer,cx,t,speed=2600,seed=0):
    off=(t*speed+seed*137)%330
    base=int((t*speed+seed*137)//330)
    for k in range(-2,3):
        n=(base-k)%9+1
        y=DY+k*330+off-165
        for g in range(3):
            draw_digit(layer,n,cx,y-g*45,alpha=170-g*55)
# particles
PR=random.Random(11)
PARTS=[(PR.uniform(-1,1)*900,PR.uniform(-1.6,-0.3)*1400,PR.choice(["#ffd700","#ff3d6e","#3dfcff","#ffffff","#9dff3d"]),PR.randint(8,22)) for _ in range(220)]
def lcd(t):
    """returns LCD image and shake strength"""
    im=Image.new("RGBA",(LW,LH),(10,12,30,255)); d=ImageDraw.Draw(im)
    shake=1.0
    # idle bg gradient lines
    for i in range(0,LH,60):
        a=int(25+20*math.sin(t*3+i*0.02)); d.rectangle([0,i,LW,i+30],fill=(40,30,90,a))
    seg=None
    for s in SEG:
        if s[1]<=t<s[2]: seg=s
    if t<2.5:
        for i,cx in enumerate(COLX): spin_col(im,cx,t,seed=i)
    elif seg:
        kind,a,b,res=seg; u=t-a
        if kind=="spin":
            stops=[0.55,0.85,0.70]  # L, R, C order
            for i,cx in enumerate(COLX):
                if u<stops[i]: spin_col(im,cx,t,seed=i)
                else:
                    bounce=max(0,1-(u-stops[i])/0.12)*25
                    draw_digit(im,res[i],cx,DY+bounce)
        else:
            # reach / hit
            Ls,Rs=0.4,0.65; cstop=b-a-0.55
            reach_on=u>Rs
            if reach_on:
                p=0.5+0.5*math.sin(u*14)
                ov=Image.new("RGBA",(LW,LH),(200,0,20,int(60+80*p))); im.alpha_composite(ov)
                d=ImageDraw.Draw(im)
                # cut-in
                x=max(80,LW-(u-Rs)*3000)
                d.rectangle([0,90,LW,300],fill=(0,0,0,200))
                f=F(BK,170); d.text((x,95),"リーチ!!",font=f,fill="#ffe94a",stroke_width=10,stroke_fill="#b00000")
                shake=2.2
            for i,cx in [(0,COLX[0]),(2,COLX[2])]:
                st=Ls if i==0 else Rs
                if u<st: spin_col(im,cx,t,seed=i)
                else: draw_digit(im,res[i],cx,DY+max(0,1-(u-st)/0.12)*25)
            if u<cstop:
                sp=2600 if not reach_on else max(380,2600-(u-Rs)*1500)
                spin_col(im,COLX[1],t,speed=sp,seed=5)
            else:
                draw_digit(im,res[1],COLX[1],DY)
                if kind=="reach" and u>cstop+0.05:
                    d=ImageDraw.Draw(im); f=F(BK,120)
                    d.text((LW/2-d.textlength("ハズレ…",font=f)/2,950),"ハズレ…",font=f,fill="#bbbbbb",stroke_width=8,stroke_fill="#000")
                    shake=1.5
    elif HIT<=t<JACK_END:
        u=t-HIT
        hue=(u*2)%1
        import colorsys
        for i in range(0,LH,40):
            r,g,b=colorsys.hsv_to_rgb((hue+i/LH)%1,0.85,1)
            d.rectangle([0,i,LW,i+40],fill=(int(r*255),int(g*255),int(b*255),255))
        for i,cx in enumerate(COLX): draw_digit(im,7,cx,DY-60+math.sin(u*10+i)*25)
        d=ImageDraw.Draw(im)
        sc=min(1,u/0.25); f=F(BK,int(230*(0.6+0.4*sc+0.08*math.sin(u*16))))
        s="大当り"; w=d.textlength(s,font=f); d.text((LW/2-w/2,830),s,font=f,fill="#ffffff",stroke_width=16,stroke_fill="#c40000")
        for vx,vy,c,sz in PARTS:
            x=LW/2+vx*u; y=LH*0.55+vy*u+900*u*u
            if 0<x<LW and 0<y<LH: d.ellipse([x-sz,y-sz,x+sz,y+sz],fill=c)
        if u<0.18: im.alpha_composite(Image.new("RGBA",(LW,LH),(255,255,255,int(255*(1-u/0.18)))))
        shake=3.0 if u<1.0 else 1.4
    else:
        for i,cx in enumerate(COLX): spin_col(im,cx,t,speed=900,seed=i)
        im.alpha_composite(Image.new("RGBA",(LW,LH),(0,0,0,150)))
    # HUD counters
    d=ImageDraw.Draw(im)
    n=spins_at(t); yen=round(n*1000/18)
    d.rounded_rectangle([20,LH-150,LW-20,LH-20],20,fill=(0,0,0,170))
    d.text((50,LH-135),f"回転数 {n:>3}",font=F(BK,62),fill="#ffffff")
    d.text((520,LH-135),f"投資 ¥{yen:,}",font=F(BK,62),fill="#ffd84a")
    return im,shake
# ---------- telop ----------
def telop(img,text,y,size,fill="#ffffff",edge="#000000",inner=None,scale=1.0):
    if scale<=0: return
    f=F(BK,max(10,int(size*scale))); d=ImageDraw.Draw(img)
    w=d.textlength(text,font=f); x=(W-w)/2
    d.text((x,y),text,font=f,fill=edge,stroke_width=int(22*scale),stroke_fill=edge)
    if inner: d.text((x,y),text,font=f,fill=fill,stroke_width=int(9*scale),stroke_fill=inner)
    else: d.text((x,y),text,font=f,fill=fill)
def pop(t,s,d=0.25):
    x=(t-s)/d
    if x<0: return 0
    if x>=1: return 1
    return 0.3+0.7*x+0.25*math.sin(x*math.pi)
SUBS=[(2.6,6.1,"とりあえず18,000円ぶん回してみる"),(6.1,8.5,"お、リーチ…"),(8.5,10.9,"知ってた"),(10.9,13.4,"また7じゃない…"),(13.4,HIT,"頼む頼む頼む"),
      (HIT+0.6,JACK_END,"244回転（13,556円）で当たり！")]
def frame(t):
    # shake via smooth noise
    L,sh=lcd(t)
    amp=6*sh
    ox=amp*(math.sin(t*7.3)+0.5*math.sin(t*17.1)); oy=amp*(math.cos(t*6.1)+0.5*math.sin(t*13.7))
    rot=0.4*math.sin(t*1.3)*sh
    bg=BOKEH.crop((int(100+30*math.sin(t*.3)),int(100+30*math.cos(t*.25)),int(100+30*math.sin(t*.3))+W,int(100+30*math.cos(t*.25))+H)).copy()
    # machine body
    body=Image.new("RGBA",(LW+80,LH+80),(0,0,0,0)); bd=ImageDraw.Draw(body)
    bd.rounded_rectangle([0,0,LW+79,LH+79],40,fill=(30,30,36,255))
    # LED frame cycling
    import colorsys
    for i in range(0,LW+80,40):
        r,g,b=colorsys.hsv_to_rgb((i/(LW+80)+t*0.7)%1,1,1); c=(int(r*255),int(g*255),int(b*255),255)
        bd.rectangle([i,4,i+28,18],fill=c); bd.rectangle([i,LH+62,i+28,LH+76],fill=c)
    body.alpha_composite(L,(40,40))
    # glass reflection
    refl=Image.new("RGBA",body.size,(0,0,0,0)); rd=ImageDraw.Draw(refl)
    rx=int(((t*120)%(LW*2))-LW/2); rd.polygon([(rx,0),(rx+160,0),(rx-240,LH+80),(rx-400,LH+80)],fill=(255,255,255,22))
    body.alpha_composite(refl)
    body=body.rotate(rot,resample=Image.BICUBIC,expand=False)
    glow=body.filter(ImageFilter.GaussianBlur(30)) if False else None
    bg.paste(body,(int(LX-40+ox),int(LY-40+oy)),body)
    img=bg
    # telops
    if t<2.5:
        telop(img,"1万8千円で",110,96,"#ffffff",inner="#d10000",scale=pop(t,0.05))
        telop(img,"当たる確率は？",220,120,"#ffe94a",inner="#d10000",scale=pop(t,0.35))
    elif t<JACK_END:
        telop(img,"大当り確率 1/319.7 の台",150,64,"#ffffff",inner="#1f3bd1")
    for a,b,s in SUBS:
        if a<=t<b: telop(img,s,1640,68 if len(s)<15 else 58,"#ffffff",inner="#222222",scale=pop(t,a,0.15))
    if JACK_END<=t<STAT_END:
        u=t-JACK_END; d=ImageDraw.Draw(img)
        d.rounded_rectangle([60,560,W-60,1420],40,fill=(255,255,255))
        tf=lambda y,s,sz,c: d.text(((W-d.textlength(s,font=F(BK,sz)))/2,y),s,font=F(BK,sz),fill=c)
        tf(620,"でも計算すると…",58,"#555")
        tf(720,"1万8千円（324回転）で",64,"#222")
        tf(810,"1回も当たらない確率",76,"#222")
        n=min(36,int(36*max(0,u-0.6)/1.0))
        if u>0.6: telop(img,f"約{n}%",930,230,"#ff2b2b",edge="#000000",inner="#ffffff",scale=pop(u,0.6,0.25))
        if u>2.4: tf(1250,"＝ 3回に1回は ノーヒット",60,"#d10000")
    if t>=STAT_END:
        u=t-STAT_END
        telop(img,"借金介護士のひとこと",420,56,"#dddddd",inner="#333")
        telop(img,"3回に1回…",560,130,"#ffffff",inner="#000",scale=pop(u,0.1))
        if u>0.9: telop(img,"ぼくの食費が消える",760,100,"#ffe94a",inner="#b00000",scale=pop(u,0.9))
        if u>2.2: telop(img,"不労所得…欲しい…",1000,110,"#ff7a7a",inner="#000",scale=pop(u,2.2))
    d=ImageDraw.Draw(img); f=F(BD,28)  # 2行にして左右の見切れを防ぐ（11/5 01:00修正）
    for yy_,s in ((1848,"※確率シミュレーション（実機映像ではありません）"),(1882,"AI制作／遊技は18歳以上")):
        d.text(((W-d.textlength(s,font=f))/2,yy_),s,font=f,fill="#bbbbbb")
    a=np.asarray(img,dtype=np.int16)
    a=a+np.random.randint(-7,8,(H,W,1),dtype=np.int16)
    yy=np.linspace(-1,1,H)[:,None]; xx=np.linspace(-1,1,W)[None,:]
    return np.clip(a*VIG,0,255).astype(np.uint8)
yy=np.linspace(-1,1,H)[:,None]; xx=np.linspace(-1,1,W)[None,:]
VIG=(1-0.35*(xx**2+yy**2))[...,None]
# ---------- audio ----------
SR=44100; N=int(SR*T); A=np.zeros(N)
def at(s): return int(s*SR)
def put(sig,s,g=1.0):
    i=at(s); j=min(N,i+len(sig)); A[i:j]+=sig[:j-i]*g
def tone(f,d,dec=6,kind="sin"):
    tt=np.arange(int(SR*d))/SR; w=np.sin(2*np.pi*f*tt) if kind=="sin" else np.sign(np.sin(2*np.pi*f*tt))
    return w*np.exp(-dec*tt)
nr=np.random.default_rng(1)
amb=nr.normal(0,1,N); amb=np.convolve(amb,np.ones(40)/40,"same")*0.25
A+=amb
for _ in range(900):  # ball rattle clicks
    put(nr.normal(0,1,300)*np.exp(-np.arange(300)/40),nr.uniform(0,T),0.08)
put(tone(55,1.2,3)+nr.normal(0,1,int(SR*1.2))*np.exp(-np.arange(int(SR*1.2))/SR*5)*0.5,0.0,0.9)
def ticks(a,b,rate=22):
    k=a
    while k<b: put(tone(1800,0.02,200,"sq"),k,0.12); k+=1/rate
for kind,a,b,res in SEG:
    if kind=="spin":
        ticks(a,a+0.55); [put(tone(140,0.25,18),a+s,0.6) for s in (0.55,0.70,0.85)]
    else:
        ticks(a,a+0.65); put(tone(140,0.25,18),a+0.4,0.6); put(tone(140,0.25,18),a+0.65,0.6)
        d=b-a-0.55-0.65; tt=np.arange(int(SR*d))/SR
        sw=np.sin(2*np.pi*(400*tt+300*tt**2))*0.35; put(sw,a+0.65)
        put(np.sin(2*np.pi*880*tt)*(np.sin(2*np.pi*6*tt)>0)*0.12,a+0.65)
        put(tone(140,0.3,15),b-0.55,0.8)
        if kind=="reach": put(np.concatenate([tone(f,0.18,8,"sq") for f in (440,392,330)])*0.25,b-0.5)
for i,f in enumerate([523,659,784,1047,1319]): put(tone(f,0.6,4,"sq")*0.22,HIT+i*0.09)
put(tone(50,1.5,2.5),HIT,1.0)
for k in range(40): put(tone(nr.uniform(2000,5000),0.15,25),HIT+0.3+k*0.07,0.15)
for k in range(30): put(tone(1200,0.03,120),JACK_END+0.6+k*0.033,0.15)
put(tone(80,0.8,5),JACK_END+0.6,0.7)
for i,f in enumerate([392,370,349,330]): put(tone(f,0.45 if i<3 else 1.0,3,"sq")*0.2,STAT_END+2.2+i*0.35)
A=A/np.max(np.abs(A))*0.85
st=(np.stack([A,A],1)*32767).astype(np.int16)
with wave.open("sfx.wav","wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i","sfx.wav",
  "-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-shortest","short.mp4"],stdin=subprocess.PIPE)
for i in range(int(T*FPS)):
    fr=frame(i/FPS); p.stdin.write(fr.tobytes())
    if i in (40,240,420,500,560,690,860): Image.fromarray(fr).save(f"/tmp/claude-0/-home-claude/7414ca55-4d0a-5c65-b43c-fe02402c8213/scratchpad/p_{i}.png")
p.stdin.close(); p.wait(); print("HIT",HIT,"JACK_END",JACK_END,"STAT_END",STAT_END)
