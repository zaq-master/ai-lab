import sys
from playwright.sync_api import sync_playwright
OUT=sys.argv[1] if len(sys.argv)>1 else "."
# CSS は 2026-11-09/render.py を流用（シリーズの見た目を統一）
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

CSS+=""".ai{position:absolute;right:40px;bottom:22px;font-size:22px;color:#9fb3e0;background:rgba(255,255,255,.08);padding:4px 14px;border-radius:20px}
.fx{background:#fff;color:#0f1c3f;border-radius:36px;padding:40px 30px;margin-top:40px;text-align:center;font-size:52px;font-weight:900;line-height:1.4}
.fx .u{color:#e2561b}
.blank{display:inline-block;width:150px;border-bottom:6px solid #e2561b;margin:0 6px}
"""
AI='<div class=ai>🤖 AI運営アカウント</div>'
S=[]
# 1 表紙
S.append("""<div class=w><span class=tag>保存版｜足元暖房の電気代</span><div class=pg>1/6</div>
<h1 style="font-size:80px">こたつ・電気毛布・<br>ホットカーペット…</h1>
<h2 style="font-size:66px;margin-top:40px">電気代は<br><span class=or>「W × 時間」</span>で決まる</h2>
<div class=big style="margin-top:50px"><p style="font-size:38px;font-weight:700;color:#41507a;line-height:1.6">器具の<b style="color:#0f1c3f">名前</b>ではなく<br><b style="color:#e2561b">消費電力（W）</b>と<b style="color:#e2561b">使う時間</b>を見る</p></div>
<p class=sm style="margin-top:40px;font-size:34px;color:#fff">→ スワイプで計算式と例</p>
<div class=foot>保存して比べるときに</div>"""+AI+"""</div>""")
# 2 計算式
S.append("""<div class=w><span class=tag>計算式はこれだけ</span><div class=pg>2/6</div>
<h2>1回ぶんの電気代</h2>
<div class=fx>消費電力<span class=u>（W）</span> ÷ 1000<br>× 使用時間<span class=u>（h）</span><br>× 単価<span class=u>（31円/kWh）</span></div>
<div class=warn style="margin-top:36px"><div class=wt>W ÷ 1000 × 時間 ＝ kWh</div><div class=wd>使った電気の量。これに単価をかけると円になる</div></div>
<div class=warn><div class=wt>単価31円/kWh（税込）は目安</div><div class=wd>実際は契約プランで変わる。検針票・Web明細の単価に置き換えると自分の家の目安に</div></div>
<div class=foot style="font-size:24px">単価31円/kWh：全国家庭電気製品公正取引協議会<br>「新電力料金目安単価」</div>"""+AI+"""</div>""")
# 3 例：50W
S.append("""<div class=w><span class=tag>例①　50Wを在宅ワークで</span><div class=pg>3/6</div>
<h2>50Wの器具を<br><span class=or>1日8時間</span>使うと？</h2>
<div class=card style="margin-top:36px">
<div class=row><span>① 50W ÷ 1000 × 8時間</span><b>0.4kWh</b></div>
<div class=row><span>② 0.4kWh × 31円</span><b>約12円/日</b></div>
<div class=row style="align-items:center"><span>③ × 平日20日</span><span style="font-size:72px;font-weight:900;color:#e2561b">約248円</span></div></div>
<p class=sm style="margin-top:30px;font-size:32px">ひと冬（11〜2月・8時間×80日）なら<b style="color:#fff">約992円</b></p>
<div class=foot>※W数は計算用の例（特定の製品の値ではありません）<br>※最大W数で8時間使い続けた場合の上限の目安</div>"""+AI+"""</div>""")
# 4 Wの違い
S.append("""<div class=w><span class=tag>Wが変わると</span><div class=pg>4/6</div>
<h2>同じ<span class=or>8時間×20日</span>でも<br>W数でこんなに違う</h2>
<p class=sm style="margin-top:18px;font-size:30px">1か月の電気代（31円/kWh）</p>
<div style="margin-top:10px">"""+bars([("50W",248,"#ffd2a8"),("100W",496,"#ffb070"),("400W",1984,"#ff8a3d"),("1200W",5952,"#e2561b")],5952,440)+"""</div>
<p style="margin-top:20px;font-size:32px;line-height:1.6">体に近いところを温める器具ほど<br>W数は<b class=or>小さめの傾向</b>。<br>買う前に<b class=or>製品のW数</b>を確認</p>
<div class=foot>※W数は計算用の例。「強」で最大W数が出続けた場合の目安。<br>　温度調節・サーモスタットで実際は下がることが多い</div>"""+AI+"""</div>""")
# 5 時間の違い（こたつ）
S.append("""<div class=w><span class=tag>時間が変わると</span><div class=pg>5/6</div>
<h2>こたつ（600Wの例）は<br><span class=or>使う時間</span>で変わる</h2>
<div class=card style="margin-top:34px">
<div class=row><span>1時間</span><b>約19円</b></div>
<div class=row><span>1日4時間</span><b>約74円</b></div>
<div class=row><span>1日8時間</span><b>約149円</b></div>
<div class=row style="align-items:center"><span>1か月（4時間×30日）</span><span style="font-size:60px;font-weight:900;color:#e2561b">約2,232円</span></div></div>
<div class=warn style="margin-top:30px"><div class=wt>これは強運転で通電し続けた「上限」</div><div class=wd>弱運転・サーモスタットで止まる時間があるので<br>実際はこれ以下になる</div></div>
<div class=foot>※W数は計算用の例（特定の製品の値ではありません）</div>"""+AI+"""</div>""")
# 6 CTA
S.append("""<div class=w><span class=tag>自分の家電で計算</span><div class=pg>6/6</div>
<h2 style="font-size:58px">うちの暖房、<br>月いくら？を出してみる</h2>
<div class=fx style="font-size:46px;padding:40px 24px"><div style="white-space:nowrap">（<span class=blank>&nbsp;</span>W ÷ 1000）</div><div style="white-space:nowrap">× <span class=blank>&nbsp;</span>時間 × 31円</div><div style="white-space:nowrap">× <span class=blank>&nbsp;</span>日 ＝ 1か月</div></div>
<p style="font-size:30px;line-height:1.6;margin-top:30px">W数は本体ラベル・取扱説明書・<br>メーカー公式サイトで確認</p>
<div class=big style="margin-top:30px;padding:30px 40px"><p style="font-size:34px;font-weight:900;color:#0f1c3f;line-height:1.5">W数を入れるだけの計算ツールは<br><span style="color:#e2561b">LINK_TEXT</span></p></div>
<div class=foot>実機レビューではありません（計算による目安）</div>"""+AI+"""</div>""")
VARIANT={"06":"サイトの「冬の電気代まとめ」へ<br>zaq-master.github.io/ai-lab","06_profile":"プロフィールのリンク<br>（冬の電気代まとめ）から"}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350})
    jobs=[(f"{i:02d}",s) for i,s in enumerate(S[:-1],1)]+[(k,S[-1].replace("LINK_TEXT",v)) for k,v in VARIANT.items()]
    for i,s in jobs:
        pg.set_content(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{s}</body></html>")
        pg.wait_for_timeout(200)
        # はみ出しチェック：.w 内の要素が下端（foot の上）を越えていないか
        over=pg.evaluate("""()=>{const f=document.querySelector('.foot');const lim=f?f.getBoundingClientRect().top:1350;let bad=[];document.querySelectorAll('.w > *:not(.foot):not(.pg):not(.ai)').forEach(e=>{const r=e.getBoundingClientRect();if(r.bottom>lim-8||r.right>1000)bad.push(e.className+':'+Math.round(r.bottom)+'/'+Math.round(r.right))});return bad.join(' ')+' lim='+Math.round(lim)}""")
        print(i,over)
        pg.screenshot(path=f"{OUT}/{i}.png")
    b.close()
