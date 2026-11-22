# 2026-11-28「布団乾燥機の電気代は1回いくら？」 1枚 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py を共用し、アクセントは紫系
# 元ネタ：content/posts/futon-kansouki-denkidai.md の結論の幅（メーカー公表W数で計算）と「W数別の早見表」だけ。価格・効果の大きさは書かない
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,"..","2026-11-11"))
import base
from base import AI
for a,b in [(".tag{display:inline-block;background:#5fd4e8",".tag{display:inline-block;background:#c3a6ff"),
            (".ac{color:#7fe3f2}",".ac{color:#d4c0ff}"),
            (".warn{background:#e8f8fb;border-left:12px solid #1aa6c0",".warn{background:#f4efff;border-left:12px solid #7c4dd6")]:
    assert a in base.CSS,a
    base.CSS=base.CSS.replace(a,b)
base.CSS+=".foot{font-size:23px}.t td{padding:12px 6px;font-size:31px}.t th{padding:11px 6px;font-size:27px}"
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
rows=[("300W","約3.1円","約9.3円","約18.6円"),("500W","約5.2円","約15.5円","約31.0円"),
      ("700W","約7.2円","約21.7円","約43.4円"),("900W","約9.3円","約27.9円","約55.8円")]
tr="".join(f"<tr><td class=h>{w}</td><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for w,a,b,c in rows)
S=[f"""<div class=w><span class=tag>保存版｜布団乾燥機の電気代</span>
<h2 style="margin-top:30px;font-size:58px">寝る前のあたため20分<br><span class=ac>1回 約4〜10円</span></h2>
<p class=sm style="margin-top:10px">メーカー4社の公表W数（420〜905W）で計算<br>毎晩使っても1か月 約130〜280円</p>
<div class=card style="margin-top:18px;padding:16px 20px"><p style="font-size:27px;font-weight:900;margin:4px 0 8px">手持ちのW数で見る早見表（1回あたり）</p><table class=t>
<tr><th>消費電力</th><th>20分</th><th>60分</th><th>120分</th></tr>{tr}</table>
<p style="font-size:22px;color:#41507a;margin-top:8px;line-height:1.5">表示のW数のまま動き続けた場合の上限寄りの概算。実際はヒーターが入ったり切れたりして少なくなることがあります</p></div>
<div class=warn style="margin-top:16px;padding:14px 30px"><div class=wt>ダニ対策モードは長い（80〜120分）</div><div class=wd>1回 約21〜37円（公表W数で計算）。「W×モードの分数」で比べるのが確実</div></div>
<div class=foot>W数・運転時間：アイリスオーヤマ・象印・日立・パナソニック公式ページ（2026-11-16確認）／単価31円/kWh：全国家庭電気製品公正取引協議会の目安単価／AIが作成・実機レビューではありません</div>"""+AI+"</div>"]
base.render(S,OUT)
