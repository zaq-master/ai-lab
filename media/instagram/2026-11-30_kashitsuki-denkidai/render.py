# 2026-11-30「加湿器の電気代」 1枚 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py を共用し、アクセントは緑系
# 元ネタ：content/posts/humidifier-electricity-cost-telework.md の消費電力別早見表（計算用の例のW数）と方式の傾向だけ。価格・製品名は書かない
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,"..","2026-11-11"))
import base
from base import AI
for a,b in [(".tag{display:inline-block;background:#5fd4e8",".tag{display:inline-block;background:#8be0a4"),
            (".ac{color:#7fe3f2}",".ac{color:#9ff0b6}"),
            (".warn{background:#e8f8fb;border-left:12px solid #1aa6c0",".warn{background:#ecfbf0;border-left:12px solid #2f9e57")]:
    assert a in base.CSS,a
    base.CSS=base.CSS.replace(a,b)
base.CSS+=".foot{font-size:23px}.t td{padding:10px 6px;font-size:30px}.t th{padding:11px 6px;font-size:26px}"
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
rows=[("5W","約0.2円","約1.2円","約37円"),("15W","約0.5円","約3.7円","約112円"),("30W","約0.9円","約7.4円","約223円"),
      ("100W","約3.1円","約25円","約744円"),("300W","約9.3円","約74円","約2,232円"),("500W","約16円","約124円","約3,720円")]
tr="".join(f"<tr><td class=h>{w}</td><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for w,a,b,c in rows)
S=[f"""<div class=w><span class=tag>保存版｜加湿器の電気代</span>
<h2 style="margin-top:30px;font-size:56px">加湿器の電気代は<br><span class=ac>方式よりW数</span>で決まる</h2>
<p class=sm style="margin-top:10px">5〜500Wの計算例｜W ÷ 1000 × 時間 × 31円</p>
<div class=card style="margin-top:16px;padding:14px 20px"><table class=t>
<tr><th>消費電力<br>（計算例）</th><th>1時間</th><th>1日8時間</th><th>8時間<br>×30日</th></tr>{tr}</table>
<p style="font-size:21px;color:#41507a;margin-top:6px;line-height:1.45">W数は計算用の例で、特定の製品の値ではありません。本体ラベル・取扱説明書の値で確認</p></div>
<div class=warn style="margin-top:14px;padding:14px 30px"><div class=wt>ヒーターで温める方式は大きくなりやすい</div><div class=wd>スチーム式・加温するハイブリッド式は大きめ、気化式・超音波式は小さめになりやすい（一般的な傾向）</div></div>
<div class=foot>単価：全国家庭電気製品公正取引協議会の目安単価（2022年7月現在）／方式の傾向：一般的な目安で製品ごとに違います／AIが作成・実機レビューではありません</div>"""+AI+"</div>"]
base.render(S,OUT)
