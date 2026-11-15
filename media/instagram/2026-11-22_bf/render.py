# 2026-11-22「楽天ブラックフライデー 残り期間｜買う前の確認ポイント」 1枚 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py を共用し、セール用にアクセントだけ金色へ差し替え（11/19_bf・11/20_bfと同じ配色）
# 元ネタ：content/posts/rakuten-blackfriday-memo.md の「開催日時」「セール前の3ステップ」「用途別の候補」の注意書き「買わない判断もOK」だけ。価格・割引率・ポイント倍率は書かない
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
base.CSS+=".warn{padding:12px 30px;margin-top:12px}.wt{font-size:32px}.wd{font-size:26px;margin-top:2px}.foot{font-size:23px}"
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
G="#9a5b00"
S=[f"""<div class=w><span class=tag>保存版｜楽天ブラックフライデー</span>
<h1 style="font-size:60px;margin-top:26px">残り期間と<br><span class=ac>買う前の確認ポイント</span></h1>
<div class=big style="margin-top:24px;padding:22px 40px"><p style="font-size:30px;font-weight:700;color:#41507a">終了日時</p>
<p style="font-size:52px;font-weight:900;line-height:1.35;margin-top:4px">11/25（水）<b style="color:{G}">1:59</b>まで</p>
<p style="font-size:25px;color:#41507a;margin-top:6px">火曜の夜（日付が変わって水曜1:59）に終了。<br>エントリーや条件は楽天市場の公式ページで確認</p></div>
<div class=warn style="margin-top:16px"><div class=wt>☑ 毎日使う／冬だけ／なくても困らない</div><div class=wd>欲しい物を3つに分けてから決める</div></div>
<div class=warn><div class=wt>☑ 暖房家電は消費電力（W）を確認</div><div class=wd>Wから電気代を計算してから決める</div></div>
<div class=warn><div class=wt>☑ 買いまわりはショップ数と上限を先に</div><div class=wd>条件はお買い物マラソンと違う場合あり。公式を確認</div></div>
<div class=warn><div class=wt>☑ 買わない判断もOK</div><div class=wd>足りているなら、サーキュレーター・温湿度計から</div></div>
<div class=foot>出典：楽天市場 ブラックフライデー公式キャンペーンページ（2026-11-16に期間を確認）。<br>価格・ポイント倍率は書いていません。AIが作成・実機レビューではありません</div>"""+AI+"</div>"]
base.render(S,OUT)
