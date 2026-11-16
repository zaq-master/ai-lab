# 2026-11-25「冬の部屋干し、除湿機の電気代」 1枚 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py を共用し、アクセントは緑系（BF明け。金色は使わない）
# 元ネタ：content/posts/fuyu-heyaboshi-joshitsuki-denkidai.md の早見表（計算用の例のW数）・計算式・方式の傾向だけ。価格・乾く時間は書かない
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
base.CSS+=".foot{font-size:23px}.t td{padding:13px 6px;font-size:32px}.t th{padding:12px 6px;font-size:26px}"
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
rows=[("150W","約4.7円","約28円","約419円"),
      ("250W","約7.8円","約47円","約698円"),
      ("450W","約14円","約84円","約1,256円"),
      ("600W","約19円","約112円","約1,674円")]
tr="".join(f"<tr><td class=h>{w}</td><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for w,a,b,c in rows)
S=[f"""<div class=w><span class=tag>保存版｜部屋干しの電気代</span>
<h2 style="margin-top:30px;font-size:58px">除湿機で部屋干し<br><span class=ac>6時間 約28〜112円</span></h2>
<p class=sm style="margin-top:10px">150〜600Wの計算例｜W ÷ 1000 × 時間 × 31円</p>
<div class=card style="margin-top:20px;padding:16px 20px"><table class=t>
<tr><th>消費電力<br>（計算例）</th><th>1時間</th><th>6時間</th><th>6時間<br>×月15回</th></tr>{tr}</table>
<p style="font-size:22px;color:#41507a;margin-top:8px;line-height:1.5">W数は計算用の例で、特定の製品の値ではありません。乾く時間は条件で変わります</p></div>
<div class=warn style="margin-top:18px;padding:16px 30px"><div class=wt>冬はデシカント式が得意とされる一方…</div><div class=wd>ヒーターを使うぶん消費電力は大きめになりやすい（一般的な傾向）。よく使うモードのWを確認</div></div>
<div class=foot>単価：全国家庭電気製品公正取引協議会の目安単価（2022年7月現在）／方式の説明：パナソニック公式サイト（2026-11-05確認）／AIが作成・実機レビューではありません</div>"""+AI+"</div>"]
base.render(S,OUT)
