# 2026-12-05「在宅ワークの人へのプレゼント、相手の環境で選ぶ」 1枚 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py を共用し、アクセントはピンク系（クリスマス）
# 元ネタ：content/posts/telework-gadget-present-erabikata.md（公開済み）の「相手の環境で確認すること別」の早見表・6項目・のし/ラッピングの節だけ。数値・価格・製品名・セール情報は書かない
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,"..","2026-11-11"))
import base
from base import AI
for a,b in [(".tag{display:inline-block;background:#5fd4e8",".tag{display:inline-block;background:#ff9ec4"),
            (".ac{color:#7fe3f2}",".ac{color:#ffc2dc}"),
            (".warn{background:#e8f8fb;border-left:12px solid #1aa6c0",".warn{background:#fdeef4;border-left:12px solid #d63384")]:
    assert a in base.CSS,a
    base.CSS=base.CSS.replace(a,b)
base.CSS+=(".foot{font-size:22px}.t td{padding:10px 8px;font-size:26px;line-height:1.35;text-align:left}.t th{padding:10px 6px;font-size:25px}"
           ".t td.h{font-size:26px;line-height:1.3;width:330px}")
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
rows=[("<b>何も分からない</b>","温湿度計・電気ひざ掛け<br>（コンセントの位置だけ確認）"),
      ("USB-Cで充電でき<br>付属充電器のW数も分かる","USB-C充電器＋<br>対応W数のケーブル"),
      ("<b>平面</b>のモニターを<br>使っている","モニターライト<br>（上の縁の厚みを確認）"),
      ("<b>ノートPCだけ</b>で作業","温湿度計・電気ひざ掛け<br>（モニターライトは付かないことも）"),
      ("<b>賃貸</b>・借りている机","クランプ式のケーブルトレー<br>（ねじ止めは避ける）")]
tr="".join(f"<tr><td class=h>{a}</td><td>{b}</td></tr>" for a,b in rows)
S=[f"""<div class=w><span class=tag>保存版｜在宅ワークの人へのプレゼント</span>
<h2 style="margin-top:28px;font-size:54px">ガジェットは<br><span class=ac>相手の環境が分かった分だけ</span>選ぶ</h2>
<div class=card style="margin-top:20px;padding:14px 20px"><table class=t>
<tr><th>確認できたこと</th><th>選びやすいもの</th></tr>{tr}</table></div>
<div class=warn style="margin-top:14px;padding:14px 30px"><div class=wt>のし・ラッピング・届く日</div><div class=wd>ショップや商品ごとに違う。販売ページの<br>「ギフト」「お届け目安」で確認、12月は余裕をもって</div></div>
<div class=foot>出典：QOLガジェット研究所の記事<br>「在宅ワークの人へのプレゼント、ガジェットの選び方」<br>価格は書いていません／AIが作成・実機レビューではありません</div>"""+AI+"</div>"]
base.render(S,OUT)
