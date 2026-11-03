# 2026-11-12「6畳の加湿器、何mL/h必要？」 python3 render.py <出力フォルダ>（見た目は ../2026-11-11/base.py を共用）
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,"..","2026-11-11"))
from base import render,AI
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
def bars(rows,maxv,maxpx):
    h=""
    for lab,v,col in rows:
        px=max(12,round(v/maxv*maxpx))
        h+=f'<div class=br><div class=bl>{lab}</div><div class=bt><div class=bar style="width:{px}px;background:{col}"></div><span class=bv>約{v}</span></div></div>'
    return h
S=[]
S.append("""<div class=w><span class=tag>保存版｜加湿器えらび</span><div class=pg>1/6</div>
<h1>6畳の加湿器、<br>何mL/h<br>あればいい？</h1>
<div class=big><p style="font-size:38px;font-weight:700;color:#41507a;line-height:1.6">「適用畳数」だけでなく<br><b style="color:#0b7f95">部屋の体積・室温・湿度・換気</b><br>から目安を出せる</p></div>
<p class=sm style="margin-top:40px;font-size:34px;color:#fff">→ スワイプで計算の例</p>
<div class=foot>保存して、加湿器を比べるときに</div>"""+AI+"</div>")
S.append("""<div class=w><span class=tag>考え方は2つ</span><div class=pg>2/6</div>
<h2>加湿器に必要な水の量</h2>
<div class=warn style="margin-top:36px"><div class=wt>① 目標の湿度まで上げる分（g）</div><div class=wd>部屋の体積 × 飽和水蒸気量 ×<br>（目標の湿度 − 今の湿度）÷ 100</div></div>
<div class=warn><div class=wt>② 換気で逃げる分を補う量（mL/h）</div><div class=wd>換気回数 × 部屋の体積 × 足りない水分<br>→ 加湿器の「加湿量（mL/h）」と比べるのはこちら</div></div>
<div class=card style="margin-top:30px;padding:30px 44px">
<div class=row style="font-size:31px"><span>1畳</span><b>1.62m²で換算</b></div>
<div class=row style="font-size:31px"><span>換気回数</span><b>0.5回/時</b></div>
<div class=row style="font-size:31px"><span>水1g</span><b>約1mL</b></div></div>
<div class=foot style="font-size:23px">飽和水蒸気量：Tetensの式（1930）から計算／0.5回/時：建築基準法施行令<br>第20条の8（住宅の居室の機械換気の最低値）／1.62m²：不動産の表示に関する公正競争規約施行規則</div>"""+AI+"</div>")
S.append("""<div class=w><span class=tag>計算の例</span><div class=pg>3/6</div>
<h2>6畳・天井2.4m・20℃で<br><span class=ac>湿度30% → 50%</span>にすると</h2>
<div class=card style="margin-top:34px">
<div class=row><span>部屋の体積</span><b>約23.3m³</b></div>
<div class=row><span>20℃の飽和水蒸気量</span><b>約17.3g/m³</b></div>
<div class=row><span>① 50%まで上げる水</span><b>約81g</b></div>
<div class=row style="align-items:center"><span>② 保つための加湿量</span><span style="font-size:68px;font-weight:900;color:#0b7f95">約40mL/h</span></div></div>
<p class=sm style="margin-top:28px;font-size:30px">9.72m²（6畳）× 2.4m ＝ 23.3m³<br>換気0.5回/時、外の気温・湿度は入れない場合</p>
<div class=foot>※ツールの検算用の例で、推奨値ではありません</div>"""+AI+"</div>")
S.append("""<div class=w><span class=tag>冬は外気が乾いている</span><div class=pg>4/6</div>
<h2>外が<span class=ac>5℃・湿度60%</span>だと<br>必要な量は増える</h2>
<p class=sm style="margin-top:20px;font-size:30px">同じ6畳・20℃・目標50%の例（mL/h）</p>
<div style="margin-top:10px">"""+bars([("外気は室内と<br>同じと仮定",40,"#a8e6f0"),("外気5℃・60%",53,"#5fd4e8"),("最初の1時間<br>（①＋②）",134,"#1aa6c0")],134,360)+"""</div>
<div class=warn style="margin-top:26px"><div class=wt>外気を室内と同じと仮定すると少なめに出やすい</div><div class=wd>冬の外気は暖めると室内より乾いていることが多い。<br>天気予報の気温・湿度を入れると実態に近づく</div></div>
<div class=foot>外気の水分量 約4.08g/m³、目標（20℃・50%）約8.64g/m³<br>→ 0.5 × 23.3 ×（8.64 − 4.08）≒ 53mL/h</div>"""+AI+"</div>")
S.append("""<div class=w><span class=tag>比べるときの注意</span><div class=pg>5/6</div>
<h2 style="font-size:56px">カタログの数字と<br>比べる前に</h2>
<div class=warn style="margin-top:34px"><div class=wt>計算結果にゆとりを持たせる</div><div class=wd>カタログの加湿量・適用畳数は決められた測定条件での値。<br>室温や湿度が違えば実際の加湿量も変わる</div></div>
<div class=warn><div class=wt>始めた直後は多めに必要なことも</div><div class=wd>壁紙・木材・布製品が水分を吸うため</div></div>
<div class=warn><div class=wt>目標は40〜70%の範囲で</div><div class=wd>建築物衛生法の基準（事務所など）の目安。<br>上げすぎは窓の結露の原因に</div></div>
<div class=foot>断熱・すき間・人の出入り・洗濯物や調理でも必要量は変わります</div>"""+AI+"</div>")
S.append("""<div class=w><span class=tag>自分の部屋で計算</span><div class=pg>6/6</div>
<h2 style="font-size:58px">うちの部屋は<br>何mL/h？を出してみる</h2>
<div class=card style="margin-top:34px">
<div class=row style="font-size:32px;flex-direction:column;align-items:flex-start;gap:8px"><b style="color:#0b7f95">入れるもの（6つ）</b><span>広さ／天井の高さ／室温／今の湿度／<br>目標の湿度／換気回数</span></div>
<div class=row style="font-size:32px;flex-direction:column;align-items:flex-start;gap:8px"><b style="color:#0b7f95">任意（2つ）</b><span>外の気温／外の湿度（天気予報など）</span></div></div>
<div class=big style="margin-top:30px;padding:28px 36px"><p style="font-size:32px;font-weight:900;line-height:1.5">無料の「加湿量 計算ツール」は<br><span style="color:#0b7f95">「QOLガジェット研究所」で検索</span></p></div>
<div class=foot style="color:#fff;font-size:28px">AIが公開情報をもとに作成・実機レビューではありません<br>（計算による目安）</div>"""+AI+"</div>")
render(S,OUT)
