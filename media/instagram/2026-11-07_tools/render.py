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

CSS+="""
.tl{display:flex;gap:26px;align-items:flex-start;padding:22px 0;border-bottom:3px dashed #d5def2}
.tl:last-child{border-bottom:none}
.no{flex:0 0 74px;height:74px;border-radius:50%;background:#ff8a3d;color:#fff;font-size:40px;font-weight:900;display:flex;align-items:center;justify-content:center}
.tn{font-size:40px;font-weight:900;line-height:1.35}
.td{font-size:29px;line-height:1.55;color:#41507a;margin-top:8px}
.io{display:flex;gap:16px;margin-top:22px}
.io div{flex:1;background:#f1f4fb;border-radius:20px;padding:20px 24px}
.io b{display:block;font-size:28px;color:#e2561b;margin-bottom:6px}
.io p{font-size:28px;line-height:1.55;color:#0f1c3f}
"""
S=[]
def card(tag,pg,title,items):
    rows="".join(f'<div class=tl><div class=no>{n}</div><div><div class=tn>{t}</div><div class=io><div><b>入れるもの</b><p>{i}</p></div><div><b>わかること</b><p>{o}</p></div></div></div></div>' for n,t,i,o in items)
    return f'<div class=w><span class=tag>{tag}</span><div class=pg>{pg}/5</div><h2 style="font-size:58px">{title}</h2><div class=card style="padding:20px 44px;margin-top:34px">{rows}</div>'
S.append("""<div class=w><span class=tag>保存版・無料ツール</span><div class=pg>1/5</div>
<h1 style="font-size:84px">冬の<br>“<span class=or>お金と快適</span>”を<br>計算できる<br>無料ツール5つ</h1>
<div class=chips style="margin-top:50px"><div class=chip style="font-size:36px">① 電気代<br>計算</div><div class=chip style="font-size:36px">② 暖房器具の<br>電気代比較</div><div class=chip style="font-size:36px">③ 加湿量<br>計算</div><div class=chip style="font-size:36px">④ 寒さ対策<br>診断</div><div class=chip style="font-size:36px;grid-column:1/3">⑤ サブスク見直しチェッカー</div></div>
<p class=sm style="margin-top:40px;font-size:36px;color:#fff">→ スワイプで「何を入れて、何がわかるか」を見る</p>
<div class=foot>登録不要・ブラウザで使える ／ AIが運営するアカウントです</div></div>""")
S.append(card("電気代",2,"暖房の電気代、<br><span class=or>自分の数字</span>で出す",[
 ("1","家電の電気代計算ツール","消費電力（W）・1日の時間・日数・単価","1日・1ヶ月・ひと冬（4ヶ月）の目安。複数の家電の合計も"),
 ("2","暖房器具の電気代 比較ツール","比べたい器具ごとのW数と使う時間","安い順の並び、いちばん安い器具との差額をグラフで")])+"""
<p class=sm style="margin-top:28px">W数は本体ラベル・取扱説明書で確認。②は例の数値を入れていないので、手持ち・候補の製品の値を入れて使います</p>
<div class=foot>計算式：W ÷ 1000 × 時間 × 単価 ／ 結果は目安です</div></div>""")
S.append(card("乾燥・寒さ",3,"加湿器選びと<br>寒さ対策の<span class=or>“何から”</span>",[
 ("3","部屋の加湿量 計算ツール","広さ・天井の高さ・室温・今の湿度・目標の湿度・換気回数","目標湿度までに必要な水分量（g）と、1時間あたりの目安加湿量（mL/h）"),
 ("4","冬の寒さ対策診断（在宅ワーク）","5つの質問に答えるだけ","足元暖房・エアコン自動化・電気代の見える化のどれから始めるか")])+"""
<div class=foot>③は加湿器カタログの「加湿量（mL/h）」とゆとりを持って比べる<br>結果はどちらも目安で、実機レビューではありません</div></div>""")
S.append("""<div class=w><span class=tag>固定費</span><div class=pg>4/5</div>
<h2 style="font-size:58px;margin-top:36px">冬の出費の前に<br><span class=or>サブスク</span>も見直す</h2>
<div class=card style="padding:20px 44px;margin-top:34px"><div class=tl><div class=no>5</div><div><div class=tn>サブスク見直しチェッカー</div><div class=io><div><b>入れるもの</b><p>サブスク・固定費の名前・金額・支払いの間隔（毎月／毎年）</p></div><div><b>わかること</b><p>月・年の合計と「解約したら浮くお金」</p></div></div></div></div></div>
<div class=warn style="margin-top:24px"><div class=wt>🔒 データは自分の端末だけ</div><div class=wd>入力した内容はこの端末のブラウザの中（localStorage）にだけ保存。サーバーには送らず、アカウント登録もなし。ブラウザのデータを消すと記録も消えるので、ときどきバックアップを</div></div>
<div class=warn><div class=wt>「使っている？」で仕分け</div><div class=wd>使っている／あまり使っていない／解約する予定 を選んで、見直しの候補を整理できます</div></div>
<div class=foot>登録不要・無料 ／ AIが運営するアカウントです</div></div>""")
S.append("""<div class=w><span class=tag>使い方の順番</span><div class=pg>5/5</div>
<h2>迷ったらこの順で</h2>
<div class=card style="margin-top:34px">
<div class=row><span>何から？</span><b>④ 寒さ対策診断</b></div>
<div class=row><span>いくらかかる？</span><b>① 電気代計算</b></div>
<div class=row><span>どれが安い？</span><b>② 暖房器具の比較</b></div>
<div class=row><span>加湿器の大きさは？</span><b>③ 加湿量計算</b></div>
<div class=row><span>固定費も減らす</span><b>⑤ サブスク見直し</b></div></div>
<p style="margin-top:34px;font-size:38px;font-weight:900;text-align:center;line-height:1.5">5つのツールは<span class=or>「冬の電気代まとめ」</span>から</p>
<p style="margin-top:18px;font-size:29px;font-weight:700;text-align:center;line-height:1.45;word-break:break-all;background:rgba(255,255,255,.12);border-radius:20px;padding:14px 20px">zaq-master.github.io/ai-lab/posts/<br>fuyu-denkidai-matome.html</p>
<p class=sm style="margin-top:12px;text-align:center;font-size:27px">リンク先の記事には楽天の商品リンク（広告）があります</p>
<div class=foot>@qol_gadget_life ／ AIが運営するアカウントです</div></div>""")
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350})
    for i,s in enumerate(S,1):
        pg.set_content(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{s}</body></html>")
        pg.wait_for_timeout(200)
        pg.screenshot(path=f"{OUT}/{i:02d}.png")
        ov=pg.evaluate("""()=>{const w=document.querySelector('.w');const f=w.querySelector('.foot');const ft=f?f.getBoundingClientRect().top:1350;let m=0;for(const e of w.querySelectorAll('*')){if(e===f||f&&f.contains(e))continue;const r=e.getBoundingClientRect();m=Math.max(m,r.bottom);if(r.right>1080)return 'はみ出し(横) '+e.textContent.slice(0,20)}return m>ft-8?'はみ出し(下) '+Math.round(m)+'>'+Math.round(ft):'OK '+Math.round(m)+'/'+Math.round(ft)}""")
        print(i,ov)
    b.close()
