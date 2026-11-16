# 2026-11-24「賃貸の窓の寒さ・結露対策」 1枚 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py をそのまま共用（水色アクセント。BF明けなので金色は使わない）
# 元ネタ：content/posts/mado-danetsu-sheet-chintai-ketsuro.md の「約6割」（政府広報オンライン）・早見表・貼れないガラスの例だけ。
# 何℃上がる／電気代がいくら下がる、価格は記事に無いので書かない
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,"..","2026-11-11"))
import base
from base import AI
base.CSS+=".foot{font-size:23px}.t td{padding:13px 8px;font-size:30px}.t th{padding:12px 8px;font-size:27px}.t td.h{text-align:left;font-size:28px;line-height:1.3}.ok{color:#0b7f95;font-size:34px}.ng{color:#c2410c;font-size:34px}"
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
rows=[("厚手で床まで届くカーテン","<span class=ok>◎</span>","付け替えるだけ"),
      ("すき間テープ<br>（はがせるタイプ）","<span class=ok>○</span>","はがせるタイプを選ぶ"),
      ("窓用断熱シート<br>（貼ってはがせる）","<span class=ok>○</span>","貼れるガラスか確認"),
      ("内窓（二重窓）","<span class=ng>✕</span>","工事が必要・要許可")]
tr="".join(f"<tr><td class=h>{a}</td><td><b>{b}</b></td><td style='font-size:26px'>{c}</td></tr>" for a,b,c in rows)
S=[f"""<div class=w><span class=tag>保存版｜賃貸の窓対策</span>
<h2 style="margin-top:30px;font-size:60px">冬の熱の<span class=ac>約6割</span>は<br>窓などから逃げる</h2>
<p class=sm style="margin-top:10px">工事なし・元に戻せる順に試す</p>
<div class=card style="margin-top:20px;padding:16px 20px"><table class=t>
<tr><th>方法</th><th>原状回復</th><th>確認すること</th></tr>{tr}</table></div>
<div class=warn style="margin-top:18px;padding:16px 30px"><div class=wt>貼る前に：貼れないガラスの例</div><div class=wd>ザラザラ面・凹凸面・網入りガラス・ペアガラス・Low-E複層ガラス（ある製品の販売ページの例。製品ごとに確認）</div></div>
<div class=foot>約6割：政府広報オンライン（資源エネルギー庁 取材協力）／貼れないガラス：カインズ公式通販の商品ページ／何℃上がるか・電気代は条件で変わるため書いていません／AIが作成・実機レビューではありません</div>"""+AI+"</div>"]
base.render(S,OUT)
