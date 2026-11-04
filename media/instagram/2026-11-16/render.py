# 2026-11-16「ホットカーペットの電気代、1時間いくら？畳数別・強弱別」 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py を共用し、暖房テーマ用にアクセントだけオレンジへ差し替え
# 元ネタ：content/posts/hot-carpet-denkidai.md の数値だけ（パナソニック公表値・31円/kWh。新しい数値・体験談なし）
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,"..","2026-11-11"))
import base
from base import AI
for a,b in [(".tag{display:inline-block;background:#5fd4e8",".tag{display:inline-block;background:#ffb26b"),
            (".ac{color:#7fe3f2}",".ac{color:#ffc58a}"),(".u{color:#0b7f95}",".u{color:#c2410c}"),
            (".warn{background:#e8f8fb;border-left:12px solid #1aa6c0",".warn{background:#fff3e8;border-left:12px solid #f08a3c")]:
    assert a in base.CSS,a
    base.CSS=base.CSS.replace(a,b)
base.CSS+=".t td{padding:11px 6px}.t th{padding:14px 6px}"
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
G="#c2410c"
SRC="出典：パナソニック公表値（室温15℃の標準消費電力量）／単価31円/kWh＝<br>全国家庭電気製品公正取引協議会の目安単価（2022年7月現在）"
S=[]
S.append(f"""<div class=w><span class=tag>保存版｜ホットカーペットの電気代</span><div class=pg>1/6</div>
<h1>ホットカーペット、<br>1時間<span class=ac>いくら？</span></h1>
<div class=big><p style="font-size:34px;font-weight:700;color:#41507a">1時間の電気代（目安）</p>
<p style="font-size:66px;font-weight:900;margin-top:10px">約<b style="color:{G}">3.7</b>円〜約<b style="color:{G}">14.6</b>円</p>
<p style="font-size:30px;color:#41507a;margin-top:8px">1畳・中 〜 3畳・高</p></div>
<p class=sm style="margin-top:36px;font-size:34px;color:#fff">→ 畳数別・強弱別の早見表へ</p>
<div class=foot>{SRC}</div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>計算式</span><div class=pg>2/6</div>
<h2>「定格W」ではなく<br><span class=ac>消費電力量（Wh）</span>で計算</h2>
<div class=fx>消費電力量(Wh) ÷ 1000<br>× 時間(h) × 31円</div>
<div class=warn style="margin-top:34px"><div class=wt>例：パナソニック DC-2NK（2畳）</div><div class=wd>定格消費電力 <b>490W</b><br>1時間の標準消費電力量（中）<b>230Wh</b></div></div>
<div class=card style="margin-top:30px"><p style="font-size:32px;line-height:1.6;font-weight:700">温度センサーで通電を調整するので、<br><b style="color:{G}">定格Wで計算すると高めに出ます</b></p></div>
<div class=foot>{SRC}</div>"""+AI+"</div>")
rows=[("1畳","高","5.1"),("1畳","中","3.7"),("1.5畳","高","7.9"),("1.5畳","中","5.7"),("2畳","高","10.4"),("2畳","中","7.1"),("3畳","高","14.6"),("3畳","中","10.4")]
tr="".join(f"<tr><td class=h>{a}</td><td>{b}</td><td>約{c}円</td></tr>" for a,b,c in rows)
S.append(f"""<div class=w><span class=tag>早見表① 1時間</span><div class=pg>3/6</div>
<h2>畳数・温度別 <span class=ac>1時間</span></h2>
<div class=card style="margin-top:30px;padding:24px 36px"><table class=t style="font-size:35px">
<tr><th>畳数</th><th>温度</th><th>1時間</th></tr>{tr}</table></div>
<div class=foot>「弱」は公表値が無いため金額なし。{SRC}</div>"""+AI+"</div>")
rows2=[("1畳・高","614","1,228"),("1畳・中","446","893"),("1.5畳・高","949","1,897"),("1.5畳・中","688","1,376"),("2畳・高","1,246","2,492"),("2畳・中","856","1,711"),("3畳・高","1,748","3,497"),("3畳・中","1,246","2,492")]
tr2="".join(f"<tr><td class=h>{a}</td><td>約{b}円</td><td>約{c}円</td></tr>" for a,b,c in rows2)
S.append(f"""<div class=w><span class=tag>早見表② 1ヶ月（30日）</span><div class=pg>4/6</div>
<h2><span class=ac>1ヶ月</span>の電気代の目安</h2>
<div class=card style="margin-top:30px;padding:24px 30px"><table class=t style="font-size:33px">
<tr><th>畳数・温度</th><th>4時間/日</th><th>8時間/日</th></tr>{tr2}</table></div>
<div class=foot>1ヶ月＝30日で計算（1円未満四捨五入）。{SRC}</div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>電気代を抑える使い方</span><div class=pg>5/6</div>
<h2>効くのは<span class=ac>面積</span>と<span class=ac>温度</span></h2>
<div class=warn style="margin-top:30px"><div class=wt>面切り替えで座る場所だけ</div><div class=wd>3畳・高は1畳・中のおよそ4倍</div></div>
<div class=warn><div class=wt>「高」→「中」で約3割下がる</div><div class=wd>2畳なら1時間 約10.4円 → 約7.1円</div></div>
<div class=warn><div class=wt>断熱シート・ラグ</div><div class=wd>床への放熱を抑える（使えるかは取扱説明書で確認）</div></div>
<div class=warn><div class=wt>タイマー・切り忘れ防止</div><div class=wd>付いている機種なら活用</div></div>
<div class=foot>パナソニックの解説記事の案内を整理。基本料金・燃料費調整額・<br>再エネ賦課金は含まない「使った分」の目安です</div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>まとめ</span><div class=pg>6/6</div>
<h2 style="font-size:58px">ホットカーペットは<br>この3つだけ</h2>
<div class=card style="margin-top:30px">
<div class=row style="font-size:34px"><span>☑ 計算は消費電力量(Wh)で</span></div>
<div class=row style="font-size:34px"><span>☑ 2畳・中・8時間で月 約1,711円</span></div>
<div class=row style="font-size:34px"><span>☑ 必要な面だけ・中以下で</span></div></div>
<div class=big style="margin-top:30px;padding:28px 36px"><p style="font-size:32px;font-weight:900;line-height:1.5">畳数別の早見表はサイト記事で<br><span style="color:{G}">zaq-master.github.io/ai-lab</span><br><span style="font-size:26px;color:#41507a">（キャプションのURLをコピーして開く）</span></p></div>
<div class=foot style="color:#fff;font-size:28px">AIが公開情報をもとに作成・実機レビューではありません</div>"""+AI+"</div>")
base.render(S,OUT)
