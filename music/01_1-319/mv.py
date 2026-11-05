import wave, math, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
W,H,FPS=1080,1920,30
BK="/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
_f={}
def F(s):
    if s not in _f: _f[s]=ImageFont.truetype(BK,s,index=0)
    return _f[s]
w=wave.open('song.wav'); SR=w.getframerate(); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).reshape(-1,2).mean(1)/32768
DUR=len(x)/SR
LY=[(0.5,6.8,"きみを見つけた 金曜の夜","ネオンの海で 息をのんだ"),(6.8,13.2,"話しかけるまで 回した言葉","もう三百回は 超えたかな"),
(13.8,21.4,"目が合うたびに 保留が光る","期待しちゃうよ 赤い色"),(21.4,29.2,"でもいつだって 外れた顔で","笑ってるのは ぼくのほう"),
(30.0,37.3,"319分の1の恋をしてる","当たるまで やめられない"),(37.3,44.6,"ハマるほど 好きになる","このリーチは 本物？"),
(44.6,51.8,"319分の1の恋をしてる","信じてる 次こそはって"),(51.8,59.2,"財布も心も 空っぽでも","もう一回だけ 回すよ")]
art=Image.open('alice_small.png').convert('RGB')
# background: blurred art + dark gradient
bg=art.resize((H,H),Image.LANCZOS).crop(((H-W)//2,0,(H-W)//2+W,H)).filter(ImageFilter.GaussianBlur(40))
bg=ImageEnhance.Brightness(bg).enhance(0.35).convert('RGBA')
icon=art.resize((640,640),Image.LANCZOS).filter(ImageFilter.UnsharpMask(3,120,2))
mask=Image.new('L',(640,640),0); ImageDraw.Draw(mask).ellipse([0,0,639,639],fill=255)
rng=np.random.default_rng(2); P=[(rng.uniform(0,W),rng.uniform(0,H),rng.uniform(20,90),rng.uniform(2,6),rng.choice(['#ff4fd8','#3dd6ff','#ffffff'])) for _ in range(70)]
NB=48; edges=np.geomspace(120,8000,NB+1); win=np.hanning(4096); smooth=np.zeros(NB); bass_s=0
def glow(img,xy,text,font,fill,gc,blur,anchor='mm'):
    lay=Image.new('RGBA',img.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
    d.text(xy,text,font=font,fill=gc,anchor=anchor,stroke_width=max(2,font.size//12),stroke_fill=gc)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))
    ImageDraw.Draw(img).text(xy,text,font=font,fill=fill,anchor=anchor,stroke_width=max(2,font.size//18),stroke_fill='#14002b')
def frame(t):
    global smooth,bass_s
    i=int(t*SR); seg=x[max(0,i-2048):i+2048]
    if len(seg)<4096: seg=np.pad(seg,(0,4096-len(seg)))
    sp=np.abs(np.fft.rfft(seg*win)); fr=np.fft.rfftfreq(4096,1/SR)
    b=np.array([sp[(fr>=edges[k])&(fr<edges[k+1])].mean() for k in range(NB)])
    b=np.clip(np.nan_to_num(np.log1p(b)/5),0,1); smooth=np.maximum(b,smooth*0.82)
    bass=float(smooth[:6].mean()); bass_s=max(bass,bass_s*0.9)
    im=bg.copy(); d=ImageDraw.Draw(im)
    for px,py,r,sp_,c in P:
        y=(py-t*sp_*20)%H; a=int(60+40*math.sin(t*2+px))
        d.ellipse([px-r/6,y-r/6,px+r/6,y+r/6],fill=c)
    # radial bars around icon
    cx,cy,R=W//2,820,360+int(18*bass_s)
    for k in range(NB*2):
        v=smooth[k%NB if k<NB else NB-1-(k-NB)]
        ang=k/(NB*2)*2*math.pi-math.pi/2; L=20+v*170
        c=(255,79,216) if k%2 else (61,214,255)
        d.line([(cx+R*math.cos(ang),cy+R*math.sin(ang)),(cx+(R+L)*math.cos(ang),cy+(R+L)*math.sin(ang))],fill=c,width=10)
    s=int(640*(1+0.05*bass_s)); ic=icon.resize((s,s)); mk=mask.resize((s,s))
    halo=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(halo).ellipse([cx-s/2-20,cy-s/2-20,cx+s/2+20,cy+s/2+20],fill=(255,79,216,int(120+100*bass_s)))
    im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(30)))
    im.paste(ic,(cx-s//2,cy-s//2),mk)
    glow(im,(W//2,200),"319分の1の恋",F(110),'#ffffff','#ff4fd8',16)
    glow(im,(W//2,320),"トガ feat. 電脳アリス",F(52),'#ffffff','#3dd6ff',10)
    for a,b_,l1,l2 in LY:
        if a<=t<b_:
            u=t-a; al=min(1,u/0.35,max(0,(b_-t)/0.3))
            lay=Image.new('RGBA',im.size,(0,0,0,0))
            f1=F(84 if len(l1)<=12 else 74)
            glow(lay,(W//2,1390+int((1-al)*30)),l1,f1,'#ffffff','#ff4fd8',14)
            glow(lay,(W//2,1520+int((1-al)*30)),l2,F(84 if len(l2)<=12 else 74),'#ffe3fa','#3dd6ff',14)
            if al<1: lay.putalpha(Image.eval(lay.getchannel('A'),lambda v:int(v*al)))
            im.alpha_composite(lay)
    ImageDraw.Draw(im).text((W//2,1850),"Music: Suno AI ／ 作詞・制作：トガ（AIと共作）",font=F(30),fill='#cfc6e8',anchor='mm')
    return im.convert('RGB')
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i','song.wav',
  '-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-shortest','short_mv.mp4'],stdin=subprocess.PIPE)
for n in range(int(DUR*FPS)):
    fr=frame(n/FPS); p.stdin.write(fr.tobytes())
    if n in (100,500,1000,1500): fr.save(f'/tmp/claude-0/-home-claude/7414ca55-4d0a-5c65-b43c-fe02402c8213/scratchpad/mv_{n}.png')
p.stdin.close(); p.wait()
