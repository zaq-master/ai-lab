import sys
from playwright.sync_api import sync_playwright
OUT=sys.argv[1] if len(sys.argv)>1 else "."
# CSS・はみ出しチェックは 2026-11-10/render.py を流用（シリーズの見た目を統一）
# ルールの出典：楽天市場 お買い物マラソン ガイド（https://event.rakuten.co.jp/campaign/point-up/marathon/guide/ 確認日2026-11-03）
# と content/posts/rakuten-marathon-point-calculator.md。倍率＝条件を満たしたショップ数（最大10倍）、記事の marathonCalc と同じ数え方
CSS="""
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;font-family:'Noto Sans CJK JP',sans-serif;background:#0f1c3f;color:#fff;overflow:hidden}
.w{position:relative;width:1080px;height:1350px;padding:90px 80px;background:linear-gradient(160deg,#0f1c3f 0%,#1b2f66 60%,#24407f 100%)}
.tag{display:inline-block;background:#ff8a3d;color:#0f1c3f;font-weight:900;font-size:34px;padding:10px 26px;border-radius:40px}
.pg{position:absolute;top:90px;right:80px;font-size:30px;color:#9fb3e0;font-weight:700}
h1{font-size:84px;line-height:1.25;font-weight:900;margin-top:50px}
h2{font-size:62px;line-height:1.3;font-weight:900;margin-top:46px}
.or{color:#ffb070}
.card{background:#fff;color:#0f1c3f;border-radius:36px;padding:40px 48px;margin-top:40px}
.sm{font-size:30px;line-height:1.6;color:#c9d6f5}
.foot{position:absolute;left:80px;right:80px;bottom:70px;font-size:24px;color:#9fb3e0;line-height:1.6}
.row{display:flex;justify-content:space-between;align-items:center;font-size:38px;padding:18px 0;border-bottom:3px dashed #d5def2}
.row:last-child{border-bottom:none}
.warn{background:#fff4e8;border-left:12px solid #ff8a3d;border-radius:20px;padding:22px 32px;margin-top:20px;color:#0f1c3f}
.wt{font-size:34px;font-weight:900}
.wd{font-size:27px;line-height:1.5;color:#41507a;margin-top:4px}
.big{background:#fff;color:#0f1c3f;border-radius:36px;padding:40px 48px;margin-top:50px;text-align:center}
.ai{position:absolute;right:40px;bottom:22px;font-size:22px;color:#9fb3e0;background:rgba(255,255,255,.08);padding:4px 14px;border-radius:20px}
.shop{display:flex;align-items:center;gap:22px;background:#fff;color:#0f1c3f;border-radius:24px;padding:20px 28px;margin-top:18px}
.sb{flex:0 0 74px;height:74px;border-radius:18px;background:#ff8a3d;display:flex;align-items:center;justify-content:center;font-size:40px;font-weight:900;color:#0f1c3f}
.sn{flex:1;font-size:36px;font-weight:700}
.sv{font-size:36px;font-weight:900;white-space:nowrap}
.ng .sb{background:#d5def2;color:#7a88ab}.ng .sn,.ng .sv{color:#7a88ab}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:34px}
.g{background:#fff;color:#0f1c3f;border-radius:22px;padding:16px 26px;display:flex;justify-content:space-between;align-items:baseline}
.g span{font-size:34px;font-weight:700}.g b{font-size:46px;font-weight:900;color:#e2561b}
.g.max{grid-column:1/3;background:#ffb070}.g.max b{color:#0f1c3f}
.fx{background:#fff;color:#0f1c3f;border-radius:36px;padding:34px 30px;margin-top:36px;text-align:center;font-size:44px;font-weight:900;line-height:1.45}
.fx .u{color:#e2561b}
.chk{display:flex;gap:20px;align-items:flex-start;background:#fff;color:#0f1c3f;border-radius:24px;padding:20px 28px;margin-top:16px}
.ck{flex:0 0 52px;height:52px;border-radius:12px;border:5px solid #e2561b;display:flex;align-items:center;justify-content:center;font-size:34px;font-weight:900;color:#e2561b}
.ct{font-size:33px;font-weight:900;line-height:1.35}.cd{font-size:26px;color:#41507a;line-height:1.45;margin-top:4px}
"""
NOTE='楽天公式のアカウントではありません（AIがまとめた目安）'
AI='<div class=ai>🤖 AI運営アカウント</div>'
def foot(extra=""):
    return f'<div class=foot>{extra}{NOTE}</div>'+AI
S=[]
# 1 表紙＋図解
S.append("""<div class=w><span class=tag>保存版｜お買い物マラソン</span><div class=pg>1/5</div>
<h1>買いまわりは<br><span class=or>"1店1,000円以上"</span>で<br>1倍ずつ増える</h1>
<div style="margin-top:30px">
<div class=shop><div class=sb>✓</div><div class=sn>ショップA</div><div class=sv>8,000円 → 1店</div></div>
<div class=shop><div class=sb>✓</div><div class=sn>ショップB</div><div class=sv>1,200円 → 2店</div></div>
<div class="shop ng"><div class=sb>×</div><div class=sn>ショップC</div><div class=sv>980円 → 数えない</div></div>
</div>
<p style="font-size:40px;font-weight:900;margin-top:28px">→ この例は<span class=or>2店＝2倍</span></p>
"""+foot('金額は計算用の例。1,000円は税込・クーポン適用後・送料など除く<br>ポイントアップ期間：11/4(水)20:00〜11/11(水)01:59（公式ページの記載）<br>')+"</div>")
# 2 早見
g="".join(f'<div class=g><span>{n}店</span><b>{n}倍</b></div>' for n in range(1,10))
S.append("""<div class=w><span class=tag>店舗数と倍率の早見</span><div class=pg>2/5</div>
<h2 style="font-size:56px">条件を満たした<br><span class=or>ショップの数＝倍率</span></h2>
<div class=grid>"""+g+"""<div class="g max"><span>10店以上</span><b>10倍（最大）</b></div></div>
<p class=sm style="margin-top:22px;font-size:28px">1店は通常の1倍だけ（買いまわりの上乗せなし）<br>倍率は買う順番に関係なく、同じショップは何回買っても1店</p>
"""+foot('最大10倍＝通常ポイント1倍＋特典ポイント9倍<br>')+"</div>")
# 3 上限
S.append("""<div class=w><span class=tag>上限に注意</span><div class=pg>3/5</div>
<h2>買いまわり分の上限は<br><span class=or>7,000ポイント</span></h2>
<div class=fx>買いまわり分 ＝<br>対象ショップの<span class=u>税抜合計</span><br>×（倍率 − 1）％</div>
<div class=card style="margin-top:30px;padding:24px 44px">
<div class=row><span>5店（+4倍）</span><b>税抜 175,000円で上限</b></div>
<div class=row><span>8店（+7倍）</span><b>税抜 100,000円で上限</b></div>
<div class=row><span>10店（+9倍）</span><b>税抜 約77,778円で上限</b></div></div>
<p style="font-size:30px;line-height:1.5;margin-top:24px">上限を超えて買っても買いまわり分は増えない。<br><b class=or>もともと買う予定の物をまとめる</b>のが基本</p>
"""+foot('特典ポイントは期間限定ポイント。付与は12/15(火)頃（公式ページの記載）<br>計算は目安（端数処理で前後します）<br>')+"</div>")
# 4 公式確認
def ck(t,d): return f'<div class=chk><div class=ck>✓</div><div><div class=ct>{t}</div><div class=cd>{d}</div></div></div>'
S.append("""<div class=w><span class=tag>買う前に</span><div class=pg>4/5</div>
<h2 style="font-size:58px">必ず<span class=or>公式ページ</span>で<br>条件確認＋エントリー</h2>
<div style="margin-top:26px">"""+
ck("エントリーが必要","期間中のエントリーで、エントリー前の購入も対象")+
ck("1,000円は「商品代金」で判定","税込・クーポン適用後。送料・ラッピング代などは含まない")+
ck("キャンセル・返品に注意","店舗数や倍率が変わることがある")+
ck("条件は開催回ごとに変わることも","この投稿は2026年11月回の内容（確認日11/3）")+
"""</div>
"""+foot('楽天市場「お買い物マラソン」公式ガイドで最新の条件を確認してください<br>')+"</div>")
# 5 CTA
S.append("""<div class=w><span class=tag>自分の買い物で計算</span><div class=pg>5/5</div>
<h2 style="font-size:58px">何店で何倍？<br>あと何店で次の倍率？</h2>
<div class=big style="margin-top:40px"><p style="font-size:36px;font-weight:700;color:#41507a;line-height:1.6">ショップごとの金額を入れるだけの<br><b style="color:#0f1c3f">買いまわりポイント計算ツール</b>は<br>サイト「QOLガジェット研究所」へ</p>
<p style="font-size:44px;font-weight:900;color:#e2561b;margin-top:24px">zaq-master.github.io/ai-lab</p>
<p style="font-size:26px;color:#41507a;margin-top:10px">（ブラウザのアドレス欄に入力）</p></div>
<p class=sm style="margin-top:34px;font-size:30px">保存して、カートに入れる前に見返してください</p>
"""+foot('ツールの結果は目安。実際の付与は楽天の判定によります<br>')+"</div>")
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350})
    for i,s in enumerate(S,1):
        pg.set_content(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{s}</body></html>")
        pg.wait_for_timeout(200)
        over=pg.evaluate("""()=>{const f=document.querySelector('.foot');const lim=f?f.getBoundingClientRect().top:1350;let bad=[];document.querySelectorAll('.w > *:not(.foot):not(.pg):not(.ai)').forEach(e=>{const r=e.getBoundingClientRect();if(r.bottom>lim-8||r.right>1000)bad.push(e.className+':'+Math.round(r.bottom)+'/'+Math.round(r.right))});document.querySelectorAll('.w *').forEach(e=>{if(e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).overflow!='visible')bad.push('scroll:'+e.className)});return bad.join(' ')+' lim='+Math.round(lim)}""")
        print(f"{i:02d}",over)
        pg.screenshot(path=f"{OUT}/{i:02d}.png")
    b.close()
