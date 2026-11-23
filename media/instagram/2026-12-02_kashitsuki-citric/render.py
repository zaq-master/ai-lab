# 2026-12-02「年末大掃除：加湿器のクエン酸掃除は方式で違う」 1枚 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py を共用し、アクセントは水色（base.pyのまま）
# 元ネタ：ops/drafts/article_kashitsuki-citric-souji_draft.md の確認済みの内容だけ（シャープ・ダイニチ・パナソニック・象印 EE-RT35/50・アイリスオーヤマ FAQ ID=1714、2026-11-21確認）。価格・型番の推奨はしない
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,"..","2026-11-11"))
import base
from base import AI
base.CSS+=(".foot{font-size:22px}.t td{padding:11px 8px;font-size:27px;line-height:1.35}.t th{padding:10px 6px;font-size:26px}"
           ".t td.h{text-align:left;font-size:28px;line-height:1.3;width:250px}.t td.l{text-align:left}")
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
rows=[("気化式・<br>ハイブリッド式","フィルター・トレイを<b>つけ置き</b>"),
      ("スチーム式","タンク（内容器）に入れて<b>洗浄運転</b><br><span style='font-size:22px;color:#41507a'>象印 EE-RT35/50の取扱説明書の例</span>"),
      ("超音波式","タンクなど<b>外せるプラスチック部品だけ</b><br><span style='font-size:22px;color:#41507a'>内部には使わない（アイリスオーヤマの案内）</span>")]
tr="".join(f"<tr><td class=h>{a}</td><td class=l>{b}</td></tr>" for a,b in rows)
S=[f"""<div class=w><span class=tag>保存版｜年末大掃除・加湿器</span>
<h2 style="margin-top:24px;font-size:54px">加湿器のクエン酸掃除<br><span class=ac>方式で「使う場所」が違う</span></h2>
<div class=card style="margin-top:20px;padding:14px 22px"><table class=t>
<tr><th>方式</th><th>クエン酸を使う場所</th></tr>{tr}</table></div>
<div class=card style="margin-top:14px;padding:16px 28px"><div style="font-size:30px;font-weight:900">量の例（メーカー公式）</div>
<div class=row style="font-size:29px;padding:8px 0"><span>シャープ</span><b>水1Lに約6g</b></div>
<div class=row style="font-size:29px;padding:8px 0"><span>ダイニチ</span><b>水4Lに約25g</b></div>
<div class=row style="font-size:29px;padding:8px 0"><span>パナソニック</span><b>水3Lに20g</b></div>
<p style="font-size:21px;color:#41507a;margin-top:4px;line-height:1.45">他社の機種にそのまま当てはまるとは限りません。取扱説明書の量が最優先</p></div>
<div class=warn style="margin-top:14px;padding:14px 30px"><div class=wt>重曹と混ぜない・塩素系と一緒に使わない</div><div class=wd>運転を止めてプラグを抜いてから。スチーム式は冷めてから</div></div>
<div class=foot>出典：シャープ・ダイニチ・パナソニック・象印・アイリスオーヤマの公式ページ／取扱説明書（2026-11-21確認）／AIが作成・実機レビューではありません</div>"""+AI+"</div>"]
base.render(S,OUT)
