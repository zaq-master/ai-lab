# 2026-11-19「楽天ブラックフライデー 今夜20時から｜セール前の3ステップ」 1枚 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py を共用し、セール用にアクセントだけ金色へ差し替え
# 元ネタ：content/posts/rakuten-blackfriday-memo.md の内容だけ（日程と出典・3ステップ）。価格・割引率・ポイント倍率は書かない
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
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
G="#9a5b00"
S=[f"""<div class=w><span class=tag>保存版｜楽天ブラックフライデー</span>
<h1 style="font-size:72px;margin-top:34px">セール前に決める<br><span class=ac>3ステップ</span></h1>
<div class=big style="margin-top:26px;padding:24px 40px"><p style="font-size:30px;font-weight:700;color:#41507a">開催期間</p>
<p style="font-size:44px;font-weight:900;line-height:1.4;margin-top:6px">11/19（木）<b style="color:{G}">20:00</b><br>〜 11/25（水）<b style="color:{G}">1:59</b></p>
<p style="font-size:24px;color:#41507a;margin-top:10px">エントリーは11/12（木）10:00から。条件は楽天市場の公式ページで確認</p></div>
<div class=warn style="margin-top:22px"><div class=wt>① 欲しい物を3つに分ける</div><div class=wd>毎日使う／冬だけ使う／なくても困らない</div></div>
<div class=warn><div class=wt>② 暖房家電は「W」を見て計算</div><div class=wd>消費電力（W）から電気代を出してから決める</div></div>
<div class=warn><div class=wt>③ 買いまわりは先に計算</div><div class=wd>ショップ数と上限を先に。条件はマラソンと違う場合あり</div></div>
<div class=foot>出典：楽天市場公式サイト内の記事（楽天ママ割、2026年11月時点）。<br>価格・ポイント倍率は書いていません。AIが作成・実機レビューではありません</div>"""+AI+"</div>"]
base.CSS+=".warn{padding:18px 30px;margin-top:16px}"
base.render(S,OUT)
