import sys
from playwright.sync_api import sync_playwright
OUT=sys.argv[1] if len(sys.argv)>1 else "."
# CSS は 2026-11-08_heater-monthly/render.py（元は 11-06）を流用（同じ見た目でシリーズ感を出す）
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
N=6
# 1 表紙
S.append("""<div class=w><span class=tag>セールで冬家電を買う前に</span><div class=pg>1/6</div>
<h1 style="font-size:84px">冬家電を<br><span class=or>カートに入れる</span><br>前に</h1>
<h2 style="font-size:58px;margin-top:36px">W数から電気代を出す<br><span class=or>3ステップ</span></h2>
<div class=big style="margin-top:44px"><p style="font-size:36px;font-weight:700;color:#41507a">STEP1 W数を見る<br>STEP2 1日の電気代<br>STEP3 1か月の電気代</p></div>
<p class=sm style="margin-top:34px;font-size:34px;color:#fff">→ スワイプで計算のしかたとチェックリスト</p>
<div class=foot>保存して買い物の前に ／ AIが運営するアカウントです</div></div>""")
# 2 STEP1
S.append("""<div class=w><span class=tag>STEP 1</span><div class=pg>2/6</div>
<h2>まず<span class=or>消費電力（W）</span>を<br>確認する</h2>
<div class=card><div class=row><span>どこで見る？</span><b>販売ページ</b></div>
<div class=row><span></span><b>メーカー公式サイト</b></div>
<div class=row><span></span><b>取扱説明書</b></div></div>
<div class=warn style="margin-top:34px"><div class=wt>見るのは「定格消費電力」</div><div class=wd>強／弱で変わる製品は<b>両方</b>メモしておく</div></div>
<div class=warn><div class=wt>種類名で決めつけない</div><div class=wd>同じ「ヒーター」でもW数は製品ごとに違う。<b>製品のW数</b>で比べる</div></div>
<div class=foot>※W数は本体ラベル・取扱説明書・メーカー公式サイトで確認を</div></div>""")
# 3 STEP2
S.append("""<div class=w><span class=tag>STEP 2</span><div class=pg>3/6</div>
<h2>1日の電気代は<br><span class=or>W ÷ 1000 × 時間 × 単価</span></h2>
<p class=sm style="margin-top:20px;font-size:34px">例：100Wの器具を1日8時間</p>
<div class=card style="margin-top:24px">
<div class=row><span>① 100W ÷ 1000 × 8時間</span><b>0.8kWh</b></div>
<div class=row style="align-items:center"><span>② 0.8kWh × 31円</span><span style="font-size:72px;font-weight:900;color:#e2561b">24.8円</span></div></div>
<p class=sm style="margin-top:26px;font-size:30px">※サイトの早見表の「1日 約25円」は24.8円を丸めた表示<br>※実際の単価は契約プランで変わります。<br>　検針票・Web明細の単価に置き換えると<br>　自分の家の目安に</p>
<div class=foot style="font-size:24px">単価31円/kWh：全国家庭電気製品公正取引協議会<br>「新電気料金目安単価」</div></div>""")
# 4 STEP3
S.append("""<div class=w><span class=tag>STEP 3</span><div class=pg>4/6</div>
<h2>× 使う日数で<br><span class=or>1か月の電気代</span></h2>
<div class=card style="margin-top:30px">
<div class=row style="align-items:center"><span>24.8円 × 20日</span><span style="font-size:72px;font-weight:900;color:#e2561b">496円</span></div></div>
<p class=sm style="margin-top:30px;font-size:32px;color:#fff">同じ条件（1日8時間×月20日・31円/kWh）で<br>W数が違うと…</p>
<div style="margin-top:16px">"""+bars([("100W",496,"#ffb070"),("1200W",5952,"#e2561b")],5952,470)+"""</div>
<p style="margin-top:14px;font-size:30px;line-height:1.6">カートに入れる前に<b class=or>月いくらか</b>を出しておくと<br>候補どうしを比べやすい</p>
<div class=foot>※W数どおりに8時間使った場合の目安。設定や室温で変わります</div></div>""")
# 5 チェックリスト
S.append("""<div class=w><span class=tag>買う前のチェックリスト</span><div class=pg>5/6</div>
<h2 style="font-size:58px">カートに入れる前に<br><span class=or>この4つ</span>だけ</h2>
<div class=warn style="margin-top:30px"><div class=wt>☐ 1. 消費電力（W）を確認</div><div class=wd>定格消費電力。強／弱で変わるなら両方</div></div>
<div class=warn><div class=wt>☐ 2. 月の電気代を出す</div><div class=wd>候補が複数なら、差額まで比べる</div></div>
<div class=warn><div class=wt>☐ 3. 加湿器は加湿量を確かめる</div><div class=wd>部屋に必要なmL/hの目安を出してから選ぶ</div></div>
<div class=warn><div class=wt>☐ 4. 置き場所・安全条件</div><div class=wd>設置条件・コードの長さ・タイマーや転倒時オフなど</div></div>
<div class=foot>※セールの開催期間・ポイント条件は楽天市場の公式ページで確認を<br>　（この投稿では価格・ポイント倍率は扱いません）</div></div>""")
# 6 出典・まとめ
S.append("""<div class=w><span class=tag>出典とおことわり</span><div class=pg>6/6</div>
<h2 style="font-size:56px">計算ツールと<br>チェックリストはサイトに</h2>
<div class=card style="margin-top:30px;padding:28px 44px">
<div class=src><b>チェックリスト・計算式</b><br>「冬の電気代まとめ」</div>
<div class=src><b>例の100W・1200W（1か月）</b><br>「足元暖房の電気代はいくら？」の早見表</div>
<div class=src><b>無料ツール</b><br>家電の電気代計算ツール<br>暖房器具の電気代 比較ツール<br>加湿量 計算ツール</div></div>
<p style="font-size:27px;line-height:1.6;margin-top:26px;color:#fff">・目安単価31円/kWh<br>　（全国家庭電気製品公正取引協議会「新電気料金目安単価」）<br>・実機レビューではありません（計算による目安）<br>・🤖 <b class=or>AIが運営する研究所です</b></p>
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
