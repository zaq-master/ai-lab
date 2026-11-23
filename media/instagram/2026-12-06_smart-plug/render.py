# 2026-12-06「スマートプラグ、つないでいい家電は？」 1枚 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py を共用し、アクセントは紫系
# 元ネタ：content/posts/smart-plug-guide.md（公開済み）のQ5の◯△✕表・Q2（暖房器具の遠隔オン）・Q4（2.4GHz）だけ。数値・価格・製品名は書かない
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,"..","2026-11-11"))
import base
from base import AI
for a,b in [(".tag{display:inline-block;background:#5fd4e8",".tag{display:inline-block;background:#c3a6ff"),
            (".ac{color:#7fe3f2}",".ac{color:#d6c4ff}"),
            (".warn{background:#e8f8fb;border-left:12px solid #1aa6c0",".warn{background:#f3eeff;border-left:12px solid #7c3aed")]:
    assert a in base.CSS,a
    base.CSS=base.CSS.replace(a,b)
base.CSS+=(".foot{font-size:22px}.t td{padding:8px 8px;font-size:24px;line-height:1.35;text-align:left}.t th{padding:10px 6px;font-size:25px}"
           ".t td.h{font-size:27px;line-height:1.3;width:250px}.t td.m{text-align:center;font-size:27px;width:170px;white-space:nowrap}"
           ".ok{color:#15803d;font-weight:900}.mid{color:#b45309;font-weight:900}.ng{color:#c2410c;font-weight:900;background:#ffe9dc}")
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
rows=[("間接照明・<br>電気スタンド","ok","◯ 向く","スイッチを入れたままなら<br>通電で点くものが多い"),
      ("スマホ・PCの<br>充電器","ok","◯ 向く","夜中の充電を時間で止める"),
      ("加湿器","mid","△ 説明書","通電だけで動かない機種や<br>水切れ時の注意がある"),
      ("電気毛布","mid","△ 説明書","外部での電源操作の注意書き<br>と消費電力を確認"),
      ("電気ストーブ・<br>ヒーター","ng","✕ 遠隔オン<br>は避ける","無人の部屋での運転は危険"),
      ("テレビ・<br>エアコン","ng","✕ 向かない","通電だけでは起動しないことが多い<br>→スマートリモコンの担当")]
tr="".join(f"<tr><td class=h>{a}</td><td class='m {c}'>{m}</td><td>{d}</td></tr>" for a,c,m,d in rows)
S=[f"""<div class=w><span class=tag>保存版｜スマートプラグ</span>
<h2 style="margin-top:28px;font-size:52px">つないでいい家電は？<br><span class=ac>「電気を流す・止める」だけの道具</span></h2>
<div class=card style="margin-top:20px;padding:14px 20px"><table class=t>
<tr><th>家電</th><th>目安</th><th>理由</th></tr>{tr}</table>
<p style="font-size:21px;color:#41507a;margin-top:6px;line-height:1.45">◯△✕は一般的な目安。最終的には家電とプラグ両方の取扱説明書に従う</p></div>
<div class=warn style="margin-top:14px;padding:14px 30px"><div class=wt>設定でつながらない時</div><div class=wd>2.4GHzのみ対応が多い→スマホを2.4GHzのWi-Fiへ</div></div>
<div class=foot>出典：QOLガジェット研究所の記事「スマートプラグでできること・できないこと」<br>製品ごとの仕様は取扱説明書で確認／AIが作成・実機レビューではありません</div>"""+AI+"</div>"]
base.render(S,OUT)
