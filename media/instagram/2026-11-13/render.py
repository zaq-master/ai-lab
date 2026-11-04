# 2026-11-13「エアコン暖房の電気代、自分で出す方法」 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py を共用し、暖房テーマ用にアクセントだけオレンジへ差し替え
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,"..","2026-11-11"))
import base
from base import AI
for a,b in [(".tag{display:inline-block;background:#5fd4e8",".tag{display:inline-block;background:#ffb35c"),
            (".ac{color:#7fe3f2}",".ac{color:#ffc27a}"),(".u{color:#0b7f95}",".u{color:#c2410c}"),
            (".warn{background:#e8f8fb;border-left:12px solid #1aa6c0",".warn{background:#fff3e6;border-left:12px solid #f08a24")]:
    assert a in base.CSS,a
    base.CSS=base.CSS.replace(a,b)
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
O="#c2410c"
def bars(rows,maxv,maxpx):
    h=""
    for lab,v,col in rows:
        px=max(12,round(v/maxv*maxpx))
        h+=f'<div class=br><div class=bl>{lab}</div><div class=bt><div class=bar style="width:{px}px;background:{col}"></div><span class=bv>¥{v:,}</span></div></div>'
    return h
S=[]
S.append(f"""<div class=w><span class=tag>保存版｜エアコン暖房の電気代</span><div class=pg>1/6</div>
<h1>エアコン暖房、<br>1ヶ月いくら？<br><span class=ac>自分で出す方法</span></h1>
<div class=big><p style="font-size:38px;font-weight:700;color:#41507a;line-height:1.6">必要なのは<br><b style="color:{O}">暖房の消費電力（W）・時間・単価</b><br>＋「平均で何％で動くか」</p></div>
<p class=sm style="margin-top:40px;font-size:34px;color:#fff">→ スワイプで式と計算例</p>
<div class=foot>保存して、電気代が気になったときに</div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>式は1本</span><div class=pg>2/6</div>
<h2>エアコン暖房の電気代（円）</h2>
<div class=fx style="font-size:44px">消費電力(W) × 平均の％ ÷ 100<br>÷ 1000 × 時間(h)<br>× <span class=u>単価(円/kWh)</span></div>
<div class=warn style="margin-top:30px"><div class=wt>消費電力（W）はどこを見る？</div><div class=wd>カタログ・取扱説明書・メーカー公式サイト・<br>本体や室外機の銘板の「暖房の消費電力」</div></div>
<div class=warn><div class=wt>単価がわからなければ 31円/kWh</div><div class=wd>検針票やWeb明細の単価に変えると実態に近づく</div></div>
<div class=foot style="font-size:23px">31円/kWh：全国家庭電気製品公正取引協議会<br>「新電気料金目安単価」（2022年7月現在）<br>「平均の％」＝入力した消費電力の何％で動き続ける想定か（100％＝そのまま）</div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>計算例（仮の数字）</span><div class=pg>3/6</div>
<h2>消費電力 <span class=ac>500W</span>・1日8時間<br>平均100％・31円/kWh なら</h2>
<div class=card style="margin-top:34px">
<div class=row><span>1時間</span><b>¥15.5</b></div>
<div class=row><span>1日（8時間）</span><b>¥124</b></div>
<div class=row><span>1ヶ月（30日）</span><b>¥3,720</b></div>
<div class=row style="align-items:center"><span>ひと冬（4ヶ月）</span><span style="font-size:68px;font-weight:900;color:{O}">¥14,880</span></div></div>
<p class=sm style="margin-top:28px;font-size:30px">500 ÷ 1000 × 8 × 31 ＝ 124円／日<br>124 × 30日 ＝ 3,720円／月</p>
<div class=foot>※500Wは式を確かめるための計算例です。特定の製品の値ではありません</div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>消費電力は一定じゃない</span><div class=pg>4/6</div>
<h2>部屋が暖まると<br>消費電力は<span class=ac>下がることが多い</span></h2>
<p class=sm style="margin-top:20px;font-size:30px">同じ計算例（500W・8時間・30日）の1ヶ月分で<br>「平均の％」だけを変えると</p>
<div style="margin-top:10px">"""+bars([("平均100％<br>（そのまま）",3720,"#ffb35c"),("平均60％と<br>仮定した場合",2232,"#ffd8a8")],3720,360)+"""</div>
<div class=warn style="margin-top:26px"><div class=wt>実際の％は機種・条件で変わる</div><div class=wd>外気温・設定温度・部屋の広さ・断熱しだい。<br>立ち上がりや寒い日は高くなることも</div></div>
<div class=warn><div class=wt>暖房時の室温は20℃が目安</div><div class=wd>設定温度ではなく、温度計で室温を見る。<br>出典：資源エネルギー庁 省エネポータル「空調」</div></div>
<div class=foot>60％は「％を変えると結果がどう変わるか」を見せるための仮の値です<br>（平均値の目安ではありません）</div>"""+AI+"</div>")
S.append("""<div class=w><span class=tag>もっと正確に知るには</span><div class=pg>5/6</div>
<h2 style="font-size:56px">計算の前に<br>知っておきたい3つ</h2>
<div class=warn style="margin-top:34px"><div class=wt>機種を比べるなら「期間消費電力量」</div><div class=wd>カタログの kWh/年 × 単価 で年間の目安。<br>決められた条件で冷房＋暖房を1年使った値</div></div>
<div class=warn><div class=wt>いちばん正確なのは実測</div><div class=wd>時間ごとの使用量が見られる電力会社のWeb明細で。<br>専用コンセントだとスマートプラグで測れないことも</div></div>
<div class=warn><div class=wt>基本料金などは入っていない</div><div class=wd>燃料費調整額・再エネ賦課金でも変わる。<br>この式は「使った分の電力量料金」の目安</div></div>
<div class=foot>この3つは当サイト記事「エアコン暖房の電気代 計算ツール」の<br>注意書きをまとめたものです</div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>自分のエアコンで計算</span><div class=pg>6/6</div>
<h2 style="font-size:58px">うちのエアコンは<br>ひと冬いくら？</h2>
<div class=card style="margin-top:34px">
<div class=row style="font-size:32px;flex-direction:column;align-items:flex-start;gap:8px"><b style="color:{O}">入れるもの（6つ）</b><span>暖房の消費電力／平均の％／1日の時間／<br>1ヶ月の日数／ひと冬の月数／電気料金単価</span></div>
<div class=row style="font-size:32px;flex-direction:column;align-items:flex-start;gap:8px"><b style="color:{O}">わかること</b><span>1時間・1日・1ヶ月・ひと冬の目安<br>（期間消費電力量から年間の目安も）</span></div></div>
<div class=big style="margin-top:30px;padding:28px 36px"><p style="font-size:32px;font-weight:900;line-height:1.5">無料の「エアコン暖房の電気代 計算ツール」<br><span style="color:{O}">zaq-master.github.io/ai-lab</span><br><span style="font-size:26px;color:#41507a">（キャプションのURLをコピーして開く）</span></p></div>
<div class=foot style="color:#fff;font-size:28px">AIが公開情報をもとに作成・実機レビューではありません<br>（計算による目安）</div>"""+AI+"</div>")
base.render(S,OUT)
