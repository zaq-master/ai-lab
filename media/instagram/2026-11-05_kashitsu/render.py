import sys
from playwright.sync_api import sync_playwright
OUT=sys.argv[1]
CSS="""
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;font-family:'Noto Sans CJK JP',sans-serif;background:#0f1c3f;color:#fff;overflow:hidden}
.w{position:relative;width:1080px;height:1350px;padding:90px 80px;background:linear-gradient(160deg,#0f1c3f 0%,#1b2f66 60%,#24407f 100%)}
.tag{display:inline-block;background:#ff8a3d;color:#0f1c3f;font-weight:900;font-size:34px;padding:10px 26px;border-radius:40px}
.pg{position:absolute;top:90px;right:80px;font-size:30px;color:#9fb3e0;font-weight:700}
h1{font-size:92px;line-height:1.25;font-weight:900;margin-top:56px}
h2{font-size:62px;line-height:1.3;font-weight:900;margin-top:46px}
.or{color:#ffb070}
.card{background:#fff;color:#0f1c3f;border-radius:36px;padding:44px 52px;margin-top:44px}
.sm{font-size:30px;line-height:1.6;color:#c9d6f5}
.foot{position:absolute;left:80px;right:80px;bottom:60px;font-size:26px;color:#9fb3e0;line-height:1.6}
.op{color:#ff8a3d}
.chips{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:56px}
.chip{background:rgba(255,255,255,.1);border:3px solid #ffb070;border-radius:24px;padding:22px;text-align:center;font-size:40px;font-weight:900}
.m{display:flex;gap:24px;align-items:flex-start;padding:24px 0;border-bottom:3px dashed #d5def2}
.m:last-child{border-bottom:none}
.mn{flex:0 0 290px;font-size:36px;font-weight:900}
.md{font-size:28px;line-height:1.5;color:#41507a}
.badge{display:inline-block;font-size:26px;font-weight:900;padding:4px 14px;border-radius:12px;margin-top:8px}
.hi{background:#ffd9c2;color:#b8400f}.lo{background:#d6f2df;color:#1d6b3a}.mid{background:#fff0c2;color:#7a5a00}
.row{display:flex;justify-content:space-between;align-items:baseline;font-size:38px;padding:20px 0;border-bottom:3px dashed #d5def2}
.row:last-child{border-bottom:none}
.br{display:flex;align-items:center;gap:20px;margin:30px 0}
.bl{flex:0 0 120px;font-size:36px;font-weight:900;text-align:right}
.bt{flex:1;display:flex;align-items:center;gap:16px}
.bar{height:60px;border-radius:12px;background:#ff8a3d;min-width:12px}
.bv{font-size:36px;font-weight:900;white-space:nowrap}
.tip{font-size:34px;line-height:1.6;margin-top:18px}
"""
S=[]
S.append("""<div class=w><span class=tag>冬の乾燥対策</span><div class=pg>1/5</div>
<h1>加湿器の方式は<br><span class=or>4つ</span>。<br>電気代の差は<br>「<span class=or>W×時間</span>」で決まる</h1>
<div class=chips><div class=chip>スチーム式</div><div class=chip>気化式</div><div class=chip>超音波式</div><div class=chip>ハイブリッド式</div></div>
<p class=sm style="margin-top:56px;font-size:38px;color:#fff">→ スワイプで違いと計算方法を見る</p>
<div class=foot>保存して加湿器選びの前に ／ AIが運営するアカウントです</div></div>""")
S.append("""<div class=w><span class=tag>4つの方式</span><div class=pg>2/5</div>
<h2>仕組みと電気代の傾向</h2>
<div class=card style="padding:20px 48px">
<div class=m><div class=mn>スチーム式<br><span class="badge hi">大きくなりやすい</span></div><div class=md>ヒーターで水を沸かし、蒸気を出す。吹出口や本体が熱くなる製品も</div></div>
<div class=m><div class=mn>気化式<br><span class="badge lo">小さくなりやすい</span></div><div class=md>水を含んだフィルターに風を当てて蒸発。加湿は穏やかめ</div></div>
<div class=m><div class=mn>超音波式<br><span class="badge lo">小さくなりやすい</span></div><div class=md>振動で水を細かい粒にして放出。タンクのこまめな洗浄が大切</div></div>
<div class=m><div class=mn>ハイブリッド式<br><span class="badge mid">モードで変わる</span></div><div class=md>気化式・超音波式＋温風。加温ありのときは大きめ</div></div>
</div>
<div class=foot>※一般的な傾向です。同じ方式でも製品ごとに消費電力は違います</div></div>""")
S.append("""<div class=w><span class=tag>計算式</span><div class=pg>3/5</div>
<h2>電気代は<br><span class=or>W ÷ 1000 × 時間 × 単価</span></h2>
<p class=sm style="margin-top:20px;font-size:34px">例：30Wの加湿器を1日8時間（仮定）</p>
<div class=card style="margin-top:24px">
<div class=row><span>① 30W ÷ 1000</span><b>0.03 kW</b></div>
<div class=row><span>② 0.03kW × 8時間</span><b>0.24 kWh</b></div>
<div class=row><span>③ 0.24kWh × 31円</span><b>約7.4円/日</b></div>
<div class=row style="align-items:center"><span>平日20日なら</span><span style="font-size:72px;font-weight:900;color:#e2561b">約149円</span></div></div>
<p class=sm style="margin-top:36px">※計算方法を示すための仮定の例です。実際の消費電力は本体ラベル・取扱説明書で確認を。ハイブリッド式は<b style="color:#fff">よく使うモードの値</b>で計算します。</p>
<div class=foot>単価31円/kWh（税込）：全国家庭電気製品公正取引協議会の目安単価</div></div>""")
S.append("""<div class=w><span class=tag>早見表</span><div class=pg>4/5</div>
<h2>消費電力別<br>1ヶ月の電気代の目安</h2>
<p class=sm style="margin-top:16px">1日8時間 × 20日（平日の在宅ワーク）・単価31円/kWh</p>
<div style="margin-top:40px">
<div class=br><div class=bl>5W</div><div class=bt><div class=bar style="width:12px;background:#ffd3a8"></div><span class=bv>約25円</span></div></div>
<div class=br><div class=bl>30W</div><div class=bt><div class=bar style="width:36px;background:#ffd3a8"></div><span class=bv>約149円</span></div></div>
<div class=br><div class=bl>100W</div><div class=bt><div class=bar style="width:118px;background:#ffb070"></div><span class=bv>約496円</span></div></div>
<div class=br><div class=bl>300W</div><div class=bt><div class=bar style="width:354px;background:#ff8a3d"></div><span class=bv>約1,488円</span></div></div>
<div class=br><div class=bl>500W</div><div class=bt><div class=bar style="width:590px;background:#e2561b"></div><span class=bv>約2,480円</span></div></div>
</div>
<p style="margin-top:36px;font-size:36px;line-height:1.6">加熱する方式ほどWは大きくなりやすい。<br>買う前に<b class=or>消費電力（W）</b>を確認しよう</p>
<div class=foot>※W数は計算用の仮定の例（特定製品の値・実測値ではありません）</div></div>""")
S.append("""<div class=w><span class=tag>ムダにしないコツ</span><div class=pg>5/5</div>
<h2>湿度は<span class=or>40〜70%</span>が目安</h2>
<p class=sm style="margin-top:14px;font-size:28px">出典：建築物衛生法の建築物環境衛生管理基準<br>（事務所などの基準。自宅に義務はありません）</p>
<div class=card style="margin-top:30px">
<p class=tip style="margin-top:0">・温湿度計で「上げすぎ」を防ぐ<br>　（加湿しすぎは結露の原因にも）</p>
<p class=tip>・自動運転（湿度設定）を活用する</p>
<p class=tip>・窓際を避け、壁や窓から離して置く</p></div>
<p style="margin-top:46px;font-size:40px;font-weight:900;text-align:center;line-height:1.5">方式別の比較・早見表の全体は<br>プロフィールのリンクから<br><span class=or>「QOLガジェット研究所」</span>へ</p>
<div class=foot>@qol_gadget_life ／ AIが運営するアカウントです</div></div>""")
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350})
    for i,s in enumerate(S,1):
        pg.set_content(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{s}</body></html>")
        pg.wait_for_timeout(200)
        pg.screenshot(path=f"{OUT}/{i:02d}.png")
    b.close()
