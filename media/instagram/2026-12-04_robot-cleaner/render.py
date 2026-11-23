# 2026-12-04「ロボット掃除機の電気代、1回いくら？＋大掃除前の片付け」 1枚 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py を共用し、アクセントは緑系
# 元ネタ：content/posts/robot-cleaner-denkidai.md（公開済み）の早見表・式・片付けチェック表の値だけ（パナソニック・シャープ公表値 2026-11-07確認、取扱説明書 2026-11-08確認、目安単価31円/kWh）。新しい数値・価格は書かない
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,"..","2026-11-11"))
import base
from base import AI
for a,b in [(".tag{display:inline-block;background:#5fd4e8",".tag{display:inline-block;background:#8be0a4"),
            (".ac{color:#7fe3f2}",".ac{color:#a8f0bd}"),
            (".warn{background:#e8f8fb;border-left:12px solid #1aa6c0",".warn{background:#e9f9ee;border-left:12px solid #1f9d55")]:
    assert a in base.CSS,a
    base.CSS=base.CSS.replace(a,b)
base.CSS+=(".foot{font-size:22px}.t td{padding:10px 6px;font-size:28px;line-height:1.3}.t th{padding:10px 6px;font-size:24px}"
           ".t td.h{text-align:left;font-size:25px;line-height:1.3;width:330px}")
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
rows=[("パナソニック MC-RSF600<br>20W×約3時間","約1.9円","約56円","約24円"),
      ("パナソニック MC-RS1<br>33W×3時間","約3.1円","約92円","約40円"),
      ("シャープ RX-V60<br>30W×約2時間","約1.9円","約56円","約24円")]
tr="".join(f"<tr><td class=h>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a,b,c,d in rows)
S=[f"""<div class=w><span class=tag>保存版｜ロボット掃除機の電気代</span>
<h2 style="margin-top:28px;font-size:56px">1回 <span class=ac>約2〜3円</span><br>毎日でも月 <span class=ac>約56〜92円</span></h2>
<div class=fx style="margin-top:22px;padding:22px 24px;font-size:33px">充電時のW × 充電時間 ÷ 1000 × 31円<div style="font-size:23px;color:#41507a;font-weight:700;margin-top:4px">運転時ではなく「充電時」のW数で計算（多めに見た目安）</div></div>
<div class=card style="margin-top:16px;padding:14px 20px"><table class=t>
<tr><th>機種（公表値）</th><th>1回</th><th>毎日<br>30回/月</th><th>週3回<br>13回/月</th></tr>{tr}</table>
<p style="font-size:22px;color:#41507a;margin-top:6px;line-height:1.45">充電台だけ（本体を外した時 約0.6W・パナソニック）は月約13円</p></div>
<div class=warn style="margin-top:14px;padding:14px 30px"><div class=wt>大掃除の前に床を片付ける（取扱説明書）</div><div class=wd>コード・ひも・薄い袋・房付きの敷物・小物<br>充電台の前方約100cm・左右約50cmは物を置かない</div></div>
<div class=foot>出典：パナソニック・シャープ公式仕様／取扱説明書（2026-11-07・08確認）<br>目安単価31円/kWh／おすすめ機種の紹介ではありません<br>AIが作成・実機レビューではありません</div>"""+AI+"</div>"]
base.render(S,OUT)
