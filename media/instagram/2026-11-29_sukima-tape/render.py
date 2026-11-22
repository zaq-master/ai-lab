# 2026-11-29「すきまテープの選び方」 1枚 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py を共用（水色のまま）
# 元ネタ：content/posts/sukima-tape-erabikata-chintai.md の場所別早見表（すき間の目安はニトムズ「エプトシーラー」の案内）と、ふさがない場所（国土交通省・東京都の資料）だけ
# 何℃上がる・電気代・価格は記事に無いので書かない
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,"..","2026-11-11"))
import base
from base import AI
base.CSS+=".foot{font-size:23px}.t td{padding:12px 6px;font-size:28px}.t th{padding:11px 6px;font-size:26px}.t td.h{text-align:left;font-size:28px;line-height:1.3}"
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
rows=[("玄関ドア","ゴムの気密パッキン","2〜3.5mm"),("室内のドア","ゴムの気密パッキン","2.5〜4mm"),
      ("ふすま・障子","スポンジ","—"),("窓サッシ・網戸","毛（植毛）","—")]
tr="".join(f"<tr><td class=h>{a}</td><td><b>{b}</b></td><td>{c}</td></tr>" for a,b,c in rows)
S=[f"""<div class=w><span class=tag>保存版｜すき間風対策</span>
<h2 style="margin-top:30px;font-size:58px">すきまテープは<br><span class=ac>貼る場所</span>と<span class=ac>すき間の幅</span>で選ぶ</h2>
<p class=sm style="margin-top:10px">賃貸は「はがせる」表示＋目立たない所で試す</p>
<div class=card style="margin-top:18px;padding:16px 20px"><table class=t>
<tr><th>場所</th><th>向くタイプ</th><th>すき間の目安</th></tr>{tr}</table>
<p style="font-size:22px;color:#41507a;margin-top:8px;line-height:1.5">すき間の目安は、あるメーカーのゴム製パッキンの案内<br>製品ごとに違うので、パッケージの「適合すき間」を確認</p></div>
<div class=warn style="margin-top:16px;padding:14px 30px"><div class=wt>ふさがない：ドア下のすき間・換気口</div><div class=wd>24時間換気の空気の通り道。石油・ガスのストーブを使う部屋はこまめに換気</div></div>
<div class=foot>タイプ・すき間の目安：ニトムズ・セメダイン公式ページ／換気：国土交通省 シックハウス対策の資料・東京都保健医療局／何℃上がるか・電気代は書いていません／AIが作成・実機レビューではありません</div>"""+AI+"</div>"]
base.render(S,OUT)
