import numpy as np, wave, json
SR=44100; BPM=165; S16=60/BPM/4
N=lambda n:{'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}[n[0]]+12*(int(n[1])+1)
# (kana, note or None for rest, 16ths)
L={
'A':[('さ','E5',1),('ん','E5',1),('びゃ','D5',1),('く','E5',1),('じゅ','G5',1),('う','G5',1),('きゅ','A5',1),('う','G5',1),('ぶ','E5',1),('ん','E5',1),('の','D5',1),('い','C5',1),('ち','D5',1),(None,None,1),('の','E5',2),('こ','G5',2),('い','A5',4),('を','G5',2),('し','E5',2),('て','D5',2),('る','E5',4)],
'B':[('あ','C5',2),('た','D5',2),('る','E5',2),('ま','G5',2),('で','A5',4),(None,None,2),('や','A5',2),('め','G5',2),('ら','E5',2),('れ','D5',2),('な','E5',2),('い','C5',6),(None,None,2)],
'C':[('は','E5',2),('ま','G5',2),('る','A5',2),('ほ','C6',2),('ど','B5',4),(None,None,2),('す','A5',2),('き','G5',2),('に','A5',2),('な','G5',2),('る','E5',6),(None,None,4)],
'D':[('こ','G5',2),('の','A5',2),('り','C6',2),('ー','C6',2),('ち','D6',2),('は','C6',2),(None,None,2),('ほ','A5',2),('ん','G5',2),('も','A5',2),('の','C6',10),(None,None,2)],
'F':[('し','C5',2),('ん','D5',2),('じ','E5',2),('て','G5',2),('る','A5',4),(None,None,2),('つ','A5',2),('ぎ','G5',2),('こ','A5',2),('そ','G5',2),('は','E5',2),('っ','E5',1),('て','C5',5),(None,None,2)],
'G':[('さ','E5',1),('い','E5',1),('ふ','D5',1),('も','E5',1),('こ','G5',1),('こ','G5',1),('ろ','A5',1),('も','G5',1),(None,None,4),('か','A5',2),('ら','G5',2),('っ','A5',1),('ぽ','C6',3),('で','B5',2),('も','A5',6),(None,None,4)],
'H':[('も','G5',2),('う','A5',2),('い','C6',2),('っ','C6',1),('か','D6',1),('い','E6',2),('だ','D6',2),('け','C6',4),(None,None,2),('ま','A5',2),('わ','G5',2),('す','A5',2),('よ','C6',8)],
}
for k,v in L.items(): assert sum(x[2] for x in v)==32,(k,sum(x[2] for x in v))
ORDER=['A','B','C','D','A','F','G','H']
CH=['F','G','Em','Am','F','G','C','C','F','G','Em','Am','Dm','G','C','C']
CHN={'C':[48,52,55],'Dm':[50,53,57],'Em':[52,55,59],'F':[53,57,60],'G':[55,59,62],'Am':[57,60,64]}
json.dump({'bpm':BPM,'key':'C','chords':CH,'melody':[L[k] for k in ORDER]},open('chorus.json','w'),ensure_ascii=False,indent=1)
INTRO=2  # bars of intro
bars=16+INTRO; dur=bars*16*S16+1.5; A=np.zeros(int(SR*dur))
def put(sig,t,g=1):
    i=int(t*SR); j=min(len(A),i+len(sig)); A[i:j]+=sig[:j-i]*g
f=lambda m:440*2**((m-69)/12)
def saw(fr,d,det=0.0):
    t=np.arange(int(SR*d))/SR; return 2*((t*fr*(1+det))%1)-1
def env(n,a=0.01,r=0.08):
    e=np.ones(n); ai=int(a*SR); ri=int(r*SR); e[:ai]=np.linspace(0,1,ai)
    if ri<n: e[-ri:]*=np.linspace(1,0,ri)
    return e
def lp(x,k=8): return np.convolve(x,np.ones(k)/k,'same')
t0=INTRO*16*S16
# lead (vocal guide)
t=t0
for line in ORDER:
    for kana,note,n in L[line]:
        d=n*S16
        if note:
            fr=f(N(note)); tt=np.arange(int(SR*d*0.95))/SR
            vib=1+0.006*np.sin(2*np.pi*5.5*tt)*np.clip((tt-0.15)*4,0,1)
            ph=np.cumsum(fr*vib)/SR
            s=(np.sign(np.sin(2*np.pi*ph))*0.5+(2*(ph%1)-1)*0.5)
            put(lp(s,6)*env(len(s),0.008,0.04),t,0.22)
        t+=d
# chords, bass
for b in range(bars):
    c=CH[(b-INTRO)%16] if b>=INTRO else CH[b]
    tb=b*16*S16
    for m in CHN[c]:
        s=(saw(f(m),16*S16)+saw(f(m),16*S16,0.004))*0.5; put(lp(s,20)*env(len(s),0.05,0.2),tb,0.06)
    for k in range(8):
        s=saw(f(CHN[c][0]-12),2*S16*0.9); put(lp(s,30)*env(len(s),0.005,0.03),tb+k*2*S16,0.18)
# drums
nr=np.random.default_rng(0)
def kick():
    tt=np.arange(int(SR*0.25))/SR; return np.sin(2*np.pi*(50*tt+60*(1-np.exp(-tt*30))/30*30))*np.exp(-tt*12)
def snare():
    n=int(SR*0.18); tt=np.arange(n)/SR; return (nr.normal(0,1,n)*0.7+np.sin(2*np.pi*190*tt)*0.5)*np.exp(-tt*22)
def hat():
    n=int(SR*0.05); x=nr.normal(0,1,n); x=x-lp(x,3); return x*np.exp(-np.arange(n)/SR*80)
for b in range(bars):
    tb=b*16*S16
    for q in range(4):
        put(kick(),tb+q*4*S16,0.9)
        if q in (1,3): put(snare(),tb+q*4*S16,0.45)
    for e in range(8): put(hat(),tb+e*2*S16,0.12 if e%2 else 0.07)
put(np.sin(2*np.pi*f(84)*np.arange(int(SR))/SR)*0,0)
A=A/np.max(np.abs(A))*0.9
st=(np.stack([A,A],1)*32767).astype(np.int16)
with wave.open('demo.wav','wb') as w: w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(st.tobytes())
