# 2026-11-19「エアコン暖房×サーキュレーター：電気代の計算例と置き方」 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py を共用し、暖房テーマ用にアクセントだけオレンジへ差し替え（11/16・11/18と同じ配色）
# 元ネタ：content/posts/circulator-danbou-denkidai.md の数値・説明だけ（31円/kWh。表のWは計算用の例。効果の数値・製品名・体験談なし）
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
base.CSS+=".t td{padding:22px 4px;font-size:33px}.t th{padding:16px 4px;font-size:29px}.t td.h{font-size:34px}"
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
G="#c2410c"
N=5
SRC="単価31円/kWh＝全国家庭電気製品公正取引協議会の目安単価<br>（2022年7月現在）。W数は計算用の例。実機レビューではありません"
S=[]
S.append(f"""<div class=w><span class=tag>保存版｜エアコン暖房×サーキュレーター</span><div class=pg>1/{N}</div>
<h1>暖房に<br>サーキュレーター、<br><span class=ac>電気代はいくら？</span></h1>
<div class=big style="margin-top:44px"><p style="font-size:34px;font-weight:700;color:#41507a">サーキュレーター分の電気代（計算例）</p>
<div class=row style="margin-top:10px"><span style="font-weight:900">20Wを1時間</span><span style="font-size:52px;font-weight:900">約<b style="color:{G}">0.62</b>円</span></div>
<div class=row><span style="font-weight:900">8時間×30日</span><span style="font-size:52px;font-weight:900">約<b style="color:{G}">149</b>円</span></div></div>
<p class=sm style="margin-top:34px;font-size:34px;color:#fff">→ 計算式・早見表・置き方の考え方へ</p>
<div class=foot>{SRC}</div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>なぜ足すの？</span><div class=pg>2/{N}</div>
<h2>暖かい空気は<br><span class=ac>上にたまりやすい</span></h2>
<div class=card style="margin-top:34px"><p style="font-size:34px;line-height:1.6;font-weight:700">顔のあたりは暖かいのに<br>足元が冷える…<br><span style="font-size:29px;color:#41507a">暖かい空気は軽く、天井付近にたまりやすいため</span></p></div>
<div class=warn style="margin-top:28px"><div class=wt>サーキュレーター＝空気を混ぜる役</div><div class=wd>資源エネルギー庁の省エネポータルでも、<br>暖まった空気を循環させる工夫が紹介されています</div></div>
<div class=warn style="margin-top:22px"><div class=wt>効き方は家ごとに違う</div><div class=wd>部屋の形・天井の高さ・断熱・エアコンの位置で変わります。<br>「必ず暖かくなる」とは言い切れません</div></div>
<div class=foot>出典：資源エネルギー庁 省エネポータル「空調」（要約）</div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>早見表</span><div class=pg>3/{N}</div>
<h2>サーキュレーターの<br><span class=ac>電気代 計算例</span></h2>
<div class=card style="margin-top:30px;padding:24px 26px"><table class=t>
<tr><th>消費電力</th><th>1時間</th><th>1日8時間</th><th>8時間×30日</th></tr>
<tr><td class=h>10W</td><td>約0.31円</td><td>約2.5円</td><td>約74円</td></tr>
<tr><td class=h>20W</td><td>約0.62円</td><td>約5.0円</td><td class=hi>約149円</td></tr>
<tr><td class=h>30W</td><td>約0.93円</td><td>約7.4円</td><td>約223円</td></tr>
<tr><td class=h>40W</td><td>約1.2円</td><td>約9.9円</td><td>約298円</td></tr>
</table><p style="font-size:26px;color:#41507a;margin-top:14px;text-align:right">同じ風量で連続運転した場合の目安</p></div>
<div class=fx style="font-size:38px;margin-top:26px">電気代（円）＝ W ÷ 1000<br>× 時間(h) × 31円</div>
<div class=foot>{SRC}</div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>置き方の考え方（目安）</span><div class=pg>4/{N}</div>
<h2>まずは<br><span class=ac>取扱説明書を優先</span></h2>
<div class=warn style="margin-top:30px"><div class=wt>① 上向き（天井方向）に送る</div><div class=wd>天井付近の暖かい空気を動かして混ぜる</div></div>
<div class=warn><div class=wt>② 風が届きにくい場所から中央へ</div><div class=wd>部屋全体の空気を回す。いくつか試して比べる</div></div>
<div class=warn><div class=wt>③ 体に直接当てない</div><div class=wd>風が当たると寒く感じることも。弱めの風量から</div></div>
<div class=big style="margin-top:28px;padding:28px 36px"><p style="font-size:33px;font-weight:900;line-height:1.5">確かめ方：温度計を<span style="color:{G}">足元</span>と<span style="color:{G}">顔の高さ</span>に<br><span style="font-size:28px;color:#41507a">使う前と後で、上下の差を見る</span></p></div>
<div class=foot>よく紹介される考え方の整理。正解は部屋ごとに違います</div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>まとめ</span><div class=pg>5/{N}</div>
<h2 style="font-size:58px">併用の電気代は<br>この順で出す</h2>
<div class=card style="margin-top:30px">
<div class=row style="font-size:33px"><span>① エアコン暖房の電気代を出す</span></div>
<div class=row style="font-size:33px"><span>② サーキュレーターの電気代を出す</span></div>
<div class=row style="font-size:33px"><span>③ 2つを足す＝併用の目安</span></div></div>
<p class=sm style="margin-top:22px;font-size:29px">W数は商品ページ・本体ラベル・取扱説明書で確認</p>
<div class=big style="margin-top:24px;padding:28px 36px"><p style="font-size:32px;font-weight:900;line-height:1.5">計算ツール付きの解説はサイト記事で<br><span style="color:{G}">zaq-master.github.io/ai-lab</span><br><span style="font-size:26px;color:#41507a">（キャプションのURLをコピーして開く）</span></p></div>
<div class=foot style="color:#fff;font-size:28px">AIが公開情報をもとに作成・実機レビューではありません</div>"""+AI+"</div>")
base.render(S,OUT)
