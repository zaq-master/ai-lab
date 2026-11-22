# 2026-11-27「電気ケトルと電気ポット、電気代はどっち？」 1枚 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py を共用し、アクセントはピンク系
# 元ネタ：content/posts/denki-kettle-vs-pot-denkidai.md のメーカー公表値（象印・タイガー、2026-11-16確認）と31円/kWhの計算だけ。価格は書かない
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,"..","2026-11-11"))
import base
from base import AI
for a,b in [(".tag{display:inline-block;background:#5fd4e8",".tag{display:inline-block;background:#ff9ec4"),
            (".ac{color:#7fe3f2}",".ac{color:#ffb8d4}"),
            (".warn{background:#e8f8fb;border-left:12px solid #1aa6c0",".warn{background:#fff0f6;border-left:12px solid #d6457f")]:
    assert a in base.CSS,a
    base.CSS=base.CSS.replace(a,b)
base.CSS+=".foot{font-size:22px}.t td{padding:12px 6px;font-size:30px}.t th{padding:11px 6px;font-size:25px}.t td.h{font-size:28px}"
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
rows=[("3杯","約2.0円","約60円"),("5杯","約3.4円","約101円"),("10杯","約6.7円","約202円")]
tr="".join(f"<tr><td class=h>{a}</td><td>{b}</td><td>{c}</td></tr>" for a,b,c in rows)
tr+="<tr><td class=h style='font-size:24px;line-height:1.3'>ポット2.2L<br>1日保温</td><td class=hi>約20〜31円</td><td class=hi>約605〜921円</td></tr>"
S=[f"""<div class=w><span class=tag>保存版｜お湯の電気代</span>
<h2 style="margin-top:30px;font-size:56px">ケトル1杯 <span class=ac>約0.6〜0.7円</span><br>ポット1日保温 <span class=ac>約20〜31円</span></h2>
<p class=sm style="margin-top:10px">メーカー公表値で計算｜1日30杯前後まではケトルが安い計算</p>
<div class=card style="margin-top:18px;padding:16px 20px"><table class=t>
<tr><th>1日に飲む量</th><th>ケトル<br>1日</th><th>ケトル<br>30日</th></tr>{tr}</table>
<p style="font-size:21px;color:#41507a;margin-top:8px;line-height:1.5">ケトル：1300W・カップ1杯（約140mL）60秒の公表値。ポット：1日あたりの消費電力量0.65〜0.99kWhの公表値（湯沸かし2回・再沸とう1回・保温23時間の条件）</p></div>
<div class=warn style="margin-top:16px;padding:14px 30px"><div class=wt>冬は水温が低く、ケトルは時間がかかる</div><div class=wd>沸とう時間の公表値は水温23℃の条件。多めに沸かして余らせると、その分はムダに</div></div>
<div class=foot>数値：象印・タイガー公式ページ（2026-11-16確認）／単価31円/kWh：全国家庭電気製品公正取引協議会の目安単価（2022年7月現在）／AIが作成・実機レビューではありません</div>"""+AI+"</div>"]
base.render(S,OUT)
