from PIL import Image, ImageDraw, ImageFont
W,H=1220,1240
im=Image.new("RGB",(W,H),"#F4F8F6"); d=ImageDraw.Draw(im)
B="/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"; R="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
f=lambda p,s:ImageFont.truetype(p,s,index=0)
def c(y,t,font,fill):
    w=d.textlength(t,font=font); d.text(((W-w)/2,y),t,font=font,fill=fill)
d.rectangle([0,0,W,300],fill="#1E7A5A")
c(60,"Excel・スプレッドシートの",f(B,72),"white")
c(160,"面倒な作業を自動化",f(B,92),"#FFE45C")
# before/after
d.rounded_rectangle([70,360,560,700],30,fill="white",outline="#C9D6D0",width=4)
d.rounded_rectangle([660,360,1150,700],30,fill="white",outline="#1E7A5A",width=6)
c2=lambda x0,x1,y,t,font,fill:d.text((x0+(x1-x0-d.textlength(t,font=font))/2,y),t,font=font,fill=fill)
c2(70,560,390,"今",f(B,56),"#888")
c2(70,560,490,"コピペ・手集計",f(R,48),"#444")
c2(70,560,570,"毎月 数時間",f(B,58),"#D9534F")
d.polygon([(585,500),(635,530),(585,560)],fill="#1E7A5A")
c2(660,1150,390,"自動化後",f(B,56),"#1E7A5A")
c2(660,1150,490,"ボタンを押すだけ",f(R,48),"#444")
c2(660,1150,570,"あっという間",f(B,58),"#1E7A5A")
items=["複数シートの集計・まとめ","請求書・報告書の自動作成","フォーム回答の自動集計","エラーが出る関数の修正"]
y=770
for t in items:
    d.ellipse([150,y+10,200,y+60],fill="#1E7A5A"); d.text((163,y+3),"✓",font=f(B,40),fill="white")
    d.text((230,y),t,font=f(R,52),fill="#222"); y+=95
d.rectangle([0,1150,W,H],fill="#1E7A5A")
c(1165,"関数・マクロ(VBA)・GAS 対応｜5,000円〜",f(B,46),"white")
im.save("service.png")
