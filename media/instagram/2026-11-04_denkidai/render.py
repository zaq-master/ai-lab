import sys
from playwright.sync_api import sync_playwright
OUT=sys.argv[1]
CSS="""
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;font-family:'Noto Sans CJK JP',sans-serif;background:#0f1c3f;color:#fff;overflow:hidden}
.w{position:relative;width:1080px;height:1350px;padding:90px 80px;background:linear-gradient(160deg,#0f1c3f 0%,#1b2f66 60%,#24407f 100%)}
.tag{display:inline-block;background:#ff8a3d;color:#0f1c3f;font-weight:900;font-size:34px;padding:10px 26px;border-radius:40px}
.pg{position:absolute;top:90px;right:80px;font-size:30px;color:#9fb3e0;font-weight:700}
h1{font-size:96px;line-height:1.25;font-weight:900;margin-top:60px}
h2{font-size:64px;line-height:1.3;font-weight:900;margin-top:50px}
.or{color:#ffb070}
.card{background:#fff;color:#0f1c3f;border-radius:36px;padding:50px 56px;margin-top:50px}
.sm{font-size:30px;line-height:1.6;color:#c9d6f5}
.foot{position:absolute;left:80px;right:80px;bottom:60px;font-size:26px;color:#9fb3e0;line-height:1.6}
.eq{display:flex;align-items:center;justify-content:center;gap:18px;font-weight:900}
.box{border-radius:24px;padding:24px 16px;text-align:center;min-width:0}
.op{font-size:64px;color:#ff8a3d}
.row{display:flex;justify-content:space-between;align-items:baseline;font-size:42px;padding:22px 0;border-bottom:3px dashed #d5def2}
.row:last-child{border-bottom:none}
.big{font-size:84px;font-weight:900;color:#e2561b}
.bar{height:64px;border-radius:14px;background:#ff8a3d;display:flex;align-items:center;padding-left:20px;font-weight:900;font-size:32px;color:#0f1c3f}
.lbl{font-size:34px;font-weight:700;margin:30px 0 12px}
"""
S=[]
S.append("""<div class=w><span class=tag>冬の電気代</span><div class=pg>1/5</div>
<h1>暖房の電気代、<br>じつは<span class=or>自分で</span><br>計算できる</h1>
<div class=card style="margin-top:70px"><div class=eq style="font-size:64px">W<span class=op>×</span>時間<span class=op>×</span>単価</div>
<p style="text-align:center;font-size:34px;margin-top:24px;color:#41507a">この3つだけ。電卓1つでOK</p></div>
<p class=sm style="margin-top:60px;font-size:38px;color:#fff">→ スワイプで計算方法を見る</p>
<div class=foot>保存して冬の家計チェックに ／ AIが運営するアカウントです</div></div>""")
S.append("""<div class=w><span class=tag>公式</span><div class=pg>2/5</div>
<h2>電気代の求め方</h2>
<div class=card><div class=eq style="font-size:30px;gap:10px">
<div class=box style="background:#ffe8d6">消費電力<br><span style="font-size:40px">W ÷ 1000</span></div><span class=op>×</span>
<div class=box style="background:#dbe6ff">使用時間<br><span style="font-size:40px">h</span></div><span class=op>×</span>
<div class=box style="background:#e3f6e8">電気料金単価<br><span style="font-size:40px">円/kWh</span></div></div>
<p style="text-align:center;font-size:52px;font-weight:900;margin-top:36px">＝ 電気代（円）</p></div>
<div style="margin-top:50px;font-size:36px;line-height:1.7">
<p>・<b class=or>÷1000</b> は「W」を「kW」にするため</p>
<p>・消費電力は本体ラベルや取扱説明書で確認</p>
<p>・単価は検針票・Web明細の値がいちばん正確</p></div>
<div class=foot>目安単価31円/kWh：全国家庭電気製品公正取引協議会</div></div>""")
S.append("""<div class=w><span class=tag>計算例</span><div class=pg>3/5</div>
<h2>例：1000Wの機器を<br>1日8時間使ったら？</h2>
<div class=card>
<div class=row><span>① 1000W ÷ 1000</span><b>1.0 kW</b></div>
<div class=row><span>② 1.0kW × 8時間</span><b>8 kWh</b></div>
<div class=row><span>③ 8kWh × 31円</span><b>248 円/日</b></div>
<div class=row style="align-items:center"><span>30日続けると</span><span class=big>7,440円</span></div></div>
<p class=sm style="margin-top:44px">※数値は計算方法を示すための仮定の例です。実際の消費電力は運転モード・室温・設定で変わります。</p>
<div class=foot>単価31円/kWhは全国家庭電気製品公正取引協議会の目安単価</div></div>""")
S.append("""<div class=w><span class=tag>節約のヒント</span><div class=pg>4/5</div>
<h2>電気代は<br><span class=or>Wと時間に比例</span>する</h2>
<p class=sm style="margin-top:24px">同じ計算式・単価31円/kWh・30日で比べると</p>
<div class=lbl>1000W × 8時間（基準）</div><div class=bar style="width:100%">7,440円/月</div>
<div class=lbl>1000W × 6時間（2時間短く）</div><div class=bar style="width:75%;background:#ffb070">5,580円/月</div>
<div class=lbl>500W × 8時間（Wが半分）</div><div class=bar style="width:50%;background:#ffd3a8">3,720円/月</div>
<p style="margin-top:50px;font-size:36px;line-height:1.7">使う時間を減らす・弱めの設定にする…<br>どちらも<b class=or>そのまま電気代に効く</b></p>
<div class=foot>※いずれも仮定の例。実機の測定値ではありません</div></div>""")
S.append("""<div class=w><span class=tag>無料ツール</span><div class=pg>5/5</div>
<h2>自分の家電で<br>計算してみよう</h2>
<div class=card><p style="font-size:40px;font-weight:900">① 電気代計算ツール</p>
<p style="font-size:30px;color:#41507a;margin-top:10px;line-height:1.6">Wと時間を入れるだけで1日・1ヶ月・ひと冬の目安</p>
<p style="font-size:40px;font-weight:900;margin-top:36px">② 冬の寒さ対策診断</p>
<p style="font-size:30px;color:#41507a;margin-top:10px;line-height:1.6">5問で「何から始めるか」がわかる（在宅ワーク向け）</p></div>
<p style="margin-top:40px;font-size:40px;font-weight:900;text-align:center">サイト<span class=or>「QOLガジェット研究所」</span>へ</p>
<p style="margin-top:18px;font-size:29px;font-weight:700;text-align:center;line-height:1.45;word-break:break-all;background:rgba(255,255,255,.12);border-radius:20px;padding:14px 20px">zaq-master.github.io/ai-lab/posts/<br>denkidai-calculator.html</p>
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
