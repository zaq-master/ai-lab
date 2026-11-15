# 2026-11-20「楽天ブラックフライデー開催中｜用途別：買う前に読む記事」 1枚 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py を共用し、セール用にアクセントだけ金色へ差し替え（11/19_bfと同じ配色）
# 元ネタ：content/posts/rakuten-blackfriday-memo.md の「用途別：買う前に読む記事」「買わない判断もOK」だけ。価格・割引率・ポイント倍率は書かない
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,"..","2026-11-11"))
import base
from base import AI
for a,b in [(".tag{display:inline-block;background:#5fd4e8",".tag{display:inline-block;background:#ffd36b"),
            (".ac{color:#7fe3f2}",".ac{color:#ffe08a}"),
            (".warn{background:#e8f8fb;border-left:12px solid #1aa6c0",".warn{background:#fff8e1;border-left:12px solid #e0a800")]:
    assert a in base.CSS,a
    base.CSS=base.CSS.replace(a,b)
base.CSS+=".t td{padding:10px 8px;font-size:28px;line-height:1.3;text-align:left}.t th{padding:12px 8px;font-size:27px;text-align:left}.t td.h{width:44%}"
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
G="#9a5b00"
rows=[("足元の寒さ","足元ヒーターの電気代"),("ひざ・肩を温める","電気毛布とこたつ"),("部屋全体を温める","ホットカーペット・暖房比較"),
      ("乾燥・結露","加湿器の電気代・結露対策"),("消し忘れ・見える化","スマートプラグ・スマートリモコン"),
      ("寝るときの寒さ","寝るときの暖房 電気代くらべ"),("冬の部屋干し","除湿機の電気代"),("外出・通勤の寒さ","電熱ベストとモバイルバッテリー")]
tr="".join(f"<tr><td class=h>{a}</td><td>{b}</td></tr>" for a,b in rows)
S=[f"""<div class=w><span class=tag>保存版｜楽天ブラックフライデー開催中</span>
<h2 style="margin-top:34px;font-size:58px">用途別：<span class=ac>買う前に読む記事</span></h2>
<p class=sm style="margin-top:10px">期間：11/19（木）20:00〜11/25（水）1:59</p>
<div class=card style="margin-top:18px;padding:18px 24px"><table class=t>
<tr><th>こんなとき</th><th>先に読む記事</th></tr>{tr}</table></div>
<div class=warn style="margin-top:18px;padding:16px 30px"><div class=wt>買わない判断もOK</div><div class=wd>今ある暖房で足りているなら、まず空気を回す・温湿度計で室温を見る、から</div></div>
<div class=foot>出典：楽天市場公式サイト内の記事（楽天ママ割、2026年11月時点）。<br>価格・ポイント倍率は書いていません。AIが作成・実機レビューではありません</div>"""+AI+"</div>"]
base.render(S,OUT)
