import sys
from playwright.sync_api import sync_playwright
OUT=sys.argv[1] if len(sys.argv)>1 else "."
# CSS は 2026-11-06_heater/render.py を流用（同じ見た目でシリーズ感を出す）
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
.row{display:flex;justify-content:space-between;align-items:baseline;font-size:38px;padding:20px 0;border-bottom:3px dashed #d5def2}
.row:last-child{border-bottom:none}
.br{display:flex;align-items:center;gap:20px;margin:26px 0}
.bl{flex:0 0 150px;font-size:38px;font-weight:900;text-align:right}
.bt{flex:1;display:flex;align-items:center;gap:16px}
.bar{height:58px;border-radius:12px;background:#ff8a3d;min-width:12px}
.bv{font-size:40px;font-weight:900;white-space:nowrap}
.warn{background:#fff4e8;border-left:12px solid #ff8a3d;border-radius:20px;padding:26px 34px;margin-top:22px;color:#0f1c3f}
.wt{font-size:36px;font-weight:900}
.wd{font-size:28px;line-height:1.55;color:#41507a;margin-top:6px}
.big{background:#fff;color:#0f1c3f;border-radius:36px;padding:40px 48px;margin-top:50px;text-align:center}
.src{font-size:27px;line-height:1.5;color:#41507a;padding:14px 0;border-bottom:3px dashed #d5def2}
.src:last-child{border-bottom:none}
.src b{color:#0f1c3f}
"""
def bars(rows,maxv,maxpx):
    h=""
    for w,v,col in rows:
        px=max(12,round(v/maxv*maxpx))
        h+=f'<div class=br><div class=bl>{w}</div><div class=bt><div class=bar style="width:{px}px;background:{col}"></div><span class=bv>約{v:,}円</span></div></div>'
    return h
S=[]
# 1 表紙
S.append("""<div class=w><span class=tag>暖房の電気代 早見表</span><div class=pg>1/6</div>
<h1 style="font-size:88px">暖房器具の<br>電気代、<br><span class=or>1か月</span>で<br>いくら？</h1>
<div class=big><p style="font-size:34px;font-weight:700;color:#41507a">たとえば 100W を1日8時間×20日</p>
<p style="font-size:96px;font-weight:900;color:#e2561b;line-height:1.3">約496円<span style="font-size:44px">/月</span></p>
<p style="font-size:28px;line-height:1.5;color:#41507a">100W×8時間＝0.8kWh × 31円 ＝ 24.8円/日<br>→ ×20日 ＝ 496円/月（単価31円/kWhの目安）</p></div>
<p class=sm style="margin-top:40px;font-size:36px;color:#fff">→ スワイプで 10W〜1200W の早見表</p>
<div class=foot>保存して暖房選びの前に ／ AIが運営するアカウントです</div></div>""")
# 2 計算式
S.append("""<div class=w><span class=tag>計算式</span><div class=pg>2/6</div>
<h2>月の電気代は<br><span class=or>W ÷ 1000 × 時間 × 単価</span><br>× 日数</h2>
<p class=sm style="margin-top:20px;font-size:34px">例：100Wの器具を1日8時間・平日20日</p>
<div class=card style="margin-top:24px">
<div class=row><span>① 100W × 8時間</span><b>0.8kWh/日</b></div>
<div class=row><span>② 0.8kWh × 31円</span><b>24.8円/日</b></div>
<div class=row style="align-items:center"><span>③ 24.8円 × 20日</span><span style="font-size:72px;font-weight:900;color:#e2561b">496円</span></div></div>
<p class=sm style="margin-top:20px;font-size:28px">※3・4枚目の早見表は1円未満を四捨五入した表示<br>※サイトの早見表の「約3.1円/時間・約25円/日」も丸めた表示<br>※早見表の条件は<b style="color:#fff">1日8時間×月20日</b>（在宅ワークの平日）<br>※W数は本体ラベル・取扱説明書・メーカー公式サイトで確認を</p>
<div class=foot style="font-size:24px">単価31円/kWh：全国家庭電気製品公正取引協議会<br>「新電気料金目安単価」</div></div>""")
# 3 早見表 小さめ
S.append("""<div class=w><span class=tag>早見表①</span><div class=pg>3/6</div>
<h2>10W〜100Wの<br>1か月の電気代</h2>
<p class=sm style="margin-top:16px">1日8時間 × 月20日・単価31円/kWh</p>
<div style="margin-top:30px">"""+bars([("10W",50,"#ffd3a8"),("30W",149,"#ffd3a8"),("50W",248,"#ffb070"),("80W",397,"#ffb070"),("100W",496,"#ff8a3d")],496,520)+"""</div>
<p style="margin-top:26px;font-size:34px;line-height:1.6">電気毛布・ひざ掛けヒーターなど<br><b class=or>体に巻く・掛けるタイプ</b>は<br>消費電力が小さめの傾向</p>
<div class=foot>※W数は計算用の例（特定製品の値・実測値ではありません）</div></div>""")
# 4 早見表 大きめ
S.append("""<div class=w><span class=tag>早見表②</span><div class=pg>4/6</div>
<h2>200W〜1200Wの<br>1か月の電気代</h2>
<p class=sm style="margin-top:16px">1日8時間 × 月20日・単価31円/kWh</p>
<div style="margin-top:22px">"""+bars([("200W",992,"#ffd3a8"),("300W",1488,"#ffd3a8"),("400W",1984,"#ffb070"),("500W",2480,"#ffb070"),("800W",3968,"#ff8a3d"),("1200W",5952,"#e2561b")],5952,470)+"""</div>
<p style="margin-top:20px;font-size:32px;line-height:1.6">セラミックヒーター・電気ストーブは<br><b class=or>数百W〜1000W超</b>が多いタイプ</p>
<div class=foot>※表示はW数どおりに8時間使った場合の目安</div></div>""")
# 5 読み方の注意
S.append("""<div class=w><span class=tag>表の読み方</span><div class=pg>5/6</div>
<h2>実際は<span class=or>設定や室温</span>で<br>変わる</h2>
<p class=sm style="margin-top:14px;font-size:32px">表は目安。強運転が続けば<b style="color:#fff">高くなることも</b></p>
<div class=warn style="margin-top:26px"><div class=wt>温度調節つきの器具</div><div class=wd>オイルヒーター・こたつ・電気毛布など。表示は最大値のことが多く、設定温度に達すると通電を抑えるため、実際は<b>表より低くなる</b>ことが多い</div></div>
<div class=warn><div class=wt>エアコン</div><div class=wd>カタログの暖房消費電力は<b>定格運転時の値</b>。外気温・設定温度・部屋の広さで大きく変わる。ひと冬の目安は<b>期間消費電力量（kWh）</b>も参考に</div></div>
<div class=warn><div class=wt>請求額とは別もの</div><div class=wd>表は「使った分の電力量料金」の目安。電気料金は<b>基本料金・燃料費調整額・再エネ賦課金</b>などでも変わる</div></div>
<div class=foot>※使う日数や時間が違うなら、比較ツールで自分の条件に変えて計算できます</div></div>""")
# 6 出典・まとめ
S.append("""<div class=w><span class=tag>出典とおことわり</span><div class=pg>6/6</div>
<h2 style="font-size:56px">数字はぜんぶ<br>サイトの早見表から</h2>
<div class=card style="margin-top:30px;padding:28px 44px">
<div class=src><b>10・30・50・80・100・300・500W</b><br>「電気毛布・こたつの電気代はいくら？<br>在宅ワークで1日8時間使った場合」</div>
<div class=src><b>200・400・800・1200W／例の100W</b><br>「足元暖房の電気代はいくら？<br>在宅ワーク向けに…計算式で比較」</div>
<div class=src><b>計算式・注意点</b><br>「暖房器具の電気代 比較ツール」「冬の電気代まとめ」</div></div>
<p style="font-size:27px;line-height:1.6;margin-top:26px;color:#fff">・計算は目安単価31円/kWh<br>　（全国家庭電気製品公正取引協議会「新電気料金目安単価」）<br>・実機レビューではありません（計算による目安）<br>・🤖 このアカウントは<b class=or>AI運営</b>です</p>
<div class=foot style="font-size:30px;color:#fff;font-weight:700">QOLガジェット研究所<br><span style="color:#ffb070">zaq-master.github.io/ai-lab</span></div></div>""")
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350})
    for i,s in enumerate(S,1):
        pg.set_content(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{s}</body></html>")
        pg.wait_for_timeout(200)
        # はみ出しチェック：.w 内の要素が下端（foot の上）を越えていないか
        over=pg.evaluate("""()=>{const f=document.querySelector('.foot');const lim=f?f.getBoundingClientRect().top:1350;let bad=[];document.querySelectorAll('.w > *:not(.foot):not(.pg)').forEach(e=>{const r=e.getBoundingClientRect();if(r.bottom>lim-8||r.right>1000)bad.push(e.className+':'+Math.round(r.bottom)+'/'+Math.round(r.right))});return bad.join(' ')+' lim='+Math.round(lim)}""")
        print(i,over)
        pg.screenshot(path=f"{OUT}/{i:02d}.png")
    b.close()
