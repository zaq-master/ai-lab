# 2026-11-21「電気ブランケットの電気代は1時間いくら？」 1枚 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py を共用し、ブラックフライデー期間中なのでアクセントは金色（11/19_bf・11/20_bfと同じ配色）
# 元ネタ：content/posts/denki-blanket-denkidai-1jikan.md の早見表・計算式・「強/弱」の公表例だけ。価格・割引率・ポイント倍率は書かない
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
base.CSS+=".foot{font-size:23px}.t td{padding:12px 6px;font-size:31px}.t th{padding:12px 6px;font-size:26px}.t td.h{text-align:left;font-size:25px;line-height:1.3}"
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
rows=[("山善 YKTPD-15<br>着る・USB","15W","約0.5円","約3.7円","約74円"),
      ("アイリス EBK-1206-ZR<br>ひざ掛け","36W","約1.1円","約8.9円","約179円"),
      ("アイリス EBK-1208-ZR<br>ひざ掛け","55W","約1.7円","約14円","約273円"),
      ("山善 YMK-F43P<br>掛敷・参考","75W","約2.3円","約19円","約372円")]
tr="".join(f"<tr><td class=h>{a}</td><td><b>{w}</b></td><td>{h}</td><td>{d}</td><td>{m}</td></tr>" for a,w,h,d,m in rows)
S=[f"""<div class=w><span class=tag>保存版｜電気代早見表</span><span class=sm style="margin-left:18px;font-size:26px">楽天BF期間中（〜11/25（水）1:59）</span>
<h2 style="margin-top:30px;font-size:62px">電気ブランケットの電気代<br><span class=ac>1時間 約0.5〜2.3円</span></h2>
<p class=sm style="margin-top:12px">W ÷ 1000 × 時間 × 31円（目安単価/kWh）で計算</p>
<div class=card style="margin-top:20px;padding:16px 20px"><table class=t>
<tr><th>機種</th><th>公表W</th><th>1時間</th><th>8時間</th><th>1ヶ月</th></tr>{tr}</table>
<p style="font-size:22px;color:#41507a;margin-top:8px;line-height:1.5">1ヶ月＝1日8時間×平日20日。表示のWが出続けた場合の上限の目安</p></div>
<div class=warn style="margin-top:18px;padding:16px 30px"><div class=wt>「弱」は「強」の4分の1以下の例も</div><div class=wd>YMK-F43P取説：強 約57Wh／弱 約13Wh（1時間）</div></div>
<div class=foot>消費電力：各メーカー公式ページ・取扱説明書（2026-11-16確認）／単価：全国家庭電気製品公正取引協議会の目安単価（2022年7月現在）／AIが作成・実機レビューではありません</div>"""+AI+"</div>"]
base.render(S,OUT)
