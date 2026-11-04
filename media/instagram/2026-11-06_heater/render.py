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
CSS+="""
.step{font-size:34px;line-height:1.55;margin-top:22px}
.warn{background:#fff4e8;border-left:12px solid #ff8a3d;border-radius:20px;padding:26px 34px;margin-top:22px;color:#0f1c3f}
.wt{font-size:36px;font-weight:900}
.chip{display:flex;align-items:center;justify-content:center;min-height:130px;line-height:1.35}
.wd{font-size:28px;line-height:1.55;color:#41507a;margin-top:6px}
"""
S=[]
S.append("""<div class=w><span class=tag>冬の電気代</span><div class=pg>1/5</div>
<h1 style="font-size:84px">エアコン？<br>ヒーター？<br>電気毛布？</h1>
<h2 style="margin-top:34px;font-size:58px">ひと冬の電気代は<br>“<span class=or>自分のW数</span>”で比べよう</h2>
<div class=chips style="grid-template-columns:1fr 1fr 1fr;margin-top:46px"><div class=chip style="font-size:34px">エアコン</div><div class=chip style="font-size:34px">セラミック<br>ヒーター</div><div class=chip style="font-size:34px">オイル<br>ヒーター</div><div class=chip style="font-size:34px">電気毛布</div><div class=chip style="font-size:34px">こたつ</div><div class=chip style="font-size:34px;border-style:dashed;color:#ffb070">＋あなたの<br>候補</div></div>
<p class=sm style="margin-top:40px;font-size:36px;color:#fff">→ スワイプで計算方法と早見表を見る</p>
<div class=foot>保存して暖房選びの前に ／ AIが運営するアカウントです</div></div>""")
S.append("""<div class=w><span class=tag>計算式</span><div class=pg>2/5</div>
<h2>電気代は<br><span class=or>W ÷ 1000 × 時間 × 単価</span></h2>
<p class=sm style="margin-top:20px;font-size:34px">例：50Wの器具を1日8時間（仮定）</p>
<div class=card style="margin-top:24px">
<div class=row><span>① 50W ÷ 1000 × 31円</span><b>約1.6円/時間</b></div>
<div class=row><span>② × 8時間</span><b>約12円/日</b></div>
<div class=row><span>③ × 平日20日</span><b>約248円/月</b></div>
<div class=row style="align-items:center"><span>ひと冬（80日）</span><span style="font-size:72px;font-weight:900;color:#e2561b">約992円</span></div></div>
<p class=sm style="margin-top:32px">※計算方法を示すための仮定の例です。器具の<b style="color:#fff">種類名ではなくW数</b>で決まります。W数は本体ラベル・取扱説明書・メーカー公式サイトで確認を。</p>
<div class=foot>単価31円/kWh：全国家庭電気製品公正取引協議会の目安単価</div></div>""")
S.append("""<div class=w><span class=tag>早見表</span><div class=pg>3/5</div>
<h2>消費電力別<br>ひと冬の電気代の目安</h2>
<p class=sm style="margin-top:16px">1日8時間 × 80日（11〜2月・月20日）・単価31円/kWh</p>
<div style="margin-top:36px">
<div class=br><div class=bl>10W</div><div class=bt><div class=bar style="width:12px;background:#ffd3a8"></div><span class=bv>約198円</span></div></div>
<div class=br><div class=bl>50W</div><div class=bt><div class=bar style="width:59px;background:#ffd3a8"></div><span class=bv>約992円</span></div></div>
<div class=br><div class=bl>100W</div><div class=bt><div class=bar style="width:118px;background:#ffb070"></div><span class=bv>約1,984円</span></div></div>
<div class=br><div class=bl>300W</div><div class=bt><div class=bar style="width:354px;background:#ff8a3d"></div><span class=bv>約5,952円</span></div></div>
<div class=br><div class=bl>500W</div><div class=bt><div class=bar style="width:500px;background:#e2561b"></div><span class=bv>約9,920円</span></div></div>
</div>
<p style="margin-top:30px;font-size:34px;line-height:1.6">最大W数が8時間出続けた場合の<b class=or>上限の目安</b>。<br>温度調節つきの器具は、実際はこれより<br>低くなることが多いです</p>
<div class=foot>※W数は計算用の仮定の例（特定製品の値・実測値ではありません）</div></div>""")
S.append("""<div class=w><span class=tag>比べるときの注意</span><div class=pg>4/5</div>
<h2>同じ「W」でも<br>読み方が違う</h2>
<div class=warn style="margin-top:36px"><div class=wt>エアコン</div><div class=wd>カタログの暖房消費電力は<b>定格運転時の値</b>。実際は外気温・設定温度・部屋の広さで大きく変わる（暖まった後は下がることが多く、立ち上がりや寒い日は高くなることも）。ひと冬の目安は<b>期間消費電力量（kWh）</b>も参考に</div></div>
<div class=warn><div class=wt>温度調節つきの器具</div><div class=wd>オイルヒーター・こたつ・電気毛布など。表示は最大値のことが多く、設定温度に達すると通電を抑えるため、実際は計算より低くなることがある</div></div>
<div class=warn><div class=wt>暖まり方が違う</div><div class=wd>部屋全体を暖める器具と、体の一部を温める器具は役割が別。「どこを暖めたいか」もあわせて</div></div>
<div class=foot>※電気料金は基本料金・燃料費調整額・再エネ賦課金でも変わります</div></div>""")
S.append("""<div class=w><span class=tag>替えたらいくら？</span><div class=pg>5/5</div>
<h2>差額は<span class=or>W数の差</span>で出せる</h2>
<div class=card style="margin-top:34px">
<p style="font-size:32px;color:#41507a">例：100W → 50Wの器具に替えた場合（仮定）<br>1日8時間 × 80日</p>
<p style="font-size:34px;margin-top:16px;font-weight:700">(100−50) ÷ 1000 × 8 × 80 × 31</p>
<p style="font-size:68px;font-weight:900;color:#e2561b;margin-top:6px">＝ 約992円/ひと冬</p></div>
<p class=sm style="margin-top:22px">※寒くてエアコンの設定温度を上げると、<br>　差額は打ち消されることもあります</p>
<p style="margin-top:40px;font-size:38px;font-weight:900;text-align:center;line-height:1.55">W数を入れるだけで安い順に並ぶ<br><span class=or>無料の比較ツール</span>と、電気毛布・<br>こたつの解説記事は<br>プロフィールのリンクから</p>
<div class=foot>@qol_gadget_life ／ AIが運営するアカウントです</div></div>""")
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350})
    for i,s in enumerate(S,1):
        pg.set_content(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{s}</body></html>")
        pg.wait_for_timeout(200)
        pg.screenshot(path=f"{OUT}/{i:02d}.png")
    b.close()
