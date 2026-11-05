# 2026-11-18「電熱ベスト、10000mAhのモバイルバッテリーで何時間もつ？」 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py を共用し、暖房テーマ用にアクセントだけオレンジへ差し替え（11/16と同じ配色）
# 元ネタ：content/posts/dennetsu-vest-battery-jikan-denkidai.md の数値だけ（MCPC資料・31円/kWh。表のWは計算用の例。新しい数値・製品名・体験談なし）
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
SRC="出典：MCPC「モバイルバッテリーの容量について」<br>（定格容量＝電池容量の約60〜70%）。W（5〜15W）は計算用の例。<br>実機レビューではありません"
S=[]
S.append(f"""<div class=w><span class=tag>保存版｜電熱ベスト×モバイルバッテリー</span><div class=pg>1/{N}</div>
<h1>電熱ベスト、<br>10000mAhで<br><span class=ac>何時間もつ？</span></h1>
<div class=big style="margin-top:44px"><p style="font-size:34px;font-weight:700;color:#41507a">10000mAhのモバイルバッテリーで（目安）</p>
<div class=row style="margin-top:10px"><span style="font-weight:900">10Wで使うと</span><span style="font-size:52px;font-weight:900">約<b style="color:{G}">3.0〜3.5</b>時間</span></div>
<div class=row><span style="font-weight:900">5W（弱）なら</span><span style="font-size:52px;font-weight:900">約<b style="color:{G}">6.0〜7.0</b>時間</span></div></div>
<p class=sm style="margin-top:34px;font-size:34px;color:#fff">→「10時間くらい？」が長すぎる理由へ</p>
<div class=foot>{SRC}</div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>まず単位をそろえる</span><div class=pg>2/{N}</div>
<h2>mAhのままでは<br><span class=ac>割り算できない</span></h2>
<div class=fx style="font-size:40px">Wh ＝ 電圧(V) × 容量(mAh) ÷ 1000</div>
<div class=card style="margin-top:28px"><p style="font-size:33px;line-height:1.6;font-weight:700">10000mAh × 3.7V ÷ 1000 ＝ <b style="color:{G}">37Wh</b><br><span style="font-size:27px;color:#41507a">3.7V＝中のリチウム電池の平均電圧</span></p></div>
<div class=warn style="margin-top:26px"><div class=wt>USB（5V）で数えた定格は6〜7割</div><div class=wd>5Vへの変換ロスなどで、定格容量（5V）は<br>10000mAhの約60〜70%＝<b>6000〜7000mAh</b></div></div>
<div class=big style="margin-top:26px;padding:28px 36px"><p style="font-size:38px;font-weight:900">6000〜7000mAh × 5V ÷ 1000<br>＝ 約<b style="color:{G}">30〜35Wh</b>（使える目安）</p></div>
<div class=foot>出典：MCPC「モバイルバッテリーの容量について」</div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>早見表</span><div class=pg>3/{N}</div>
<h2>容量 × 消費電力で<br><span class=ac>何時間？</span></h2>
<div class=card style="margin-top:30px;padding:24px 26px"><table class=t>
<tr><th>ベスト</th><th>5000mAh</th><th>10000mAh</th><th>20000mAh</th></tr>
<tr><td class=h>5W</td><td>3.0〜3.5</td><td class=hi>6.0〜7.0</td><td>12.0〜14.0</td></tr>
<tr><td class=h>7.5W</td><td>2.0〜2.3</td><td>4.0〜4.7</td><td>8.0〜9.3</td></tr>
<tr><td class=h>10W</td><td>1.5〜1.8</td><td class=hi>3.0〜3.5</td><td>6.0〜7.0</td></tr>
<tr><td class=h>15W</td><td>1.0〜1.2</td><td>2.0〜2.3</td><td>4.0〜4.7</td></tr>
</table><p style="font-size:26px;color:#41507a;margin-top:14px;text-align:right">単位：時間（定格容量×5V＝使えるWhで計算）</p></div>
<div class=warn style="margin-top:24px"><div class=wt>寒い屋外では短くなることも</div><div class=wd>強モードや低温では、表より短くなることがあります</div></div>
<div class=foot>{SRC}</div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>計算式と電気代</span><div class=pg>4/{N}</div>
<h2>自分のベストで<br><span class=ac>計算してみる</span></h2>
<div class=fx style="font-size:40px">使える時間(h)<br>＝ 使えるWh ÷ ベストのW</div>
<div class=warn style="margin-top:24px"><div class=wt>「定格容量（5V）」の表示があれば</div><div class=wd>定格容量(mAh) × 5V ÷ 1000 が、取り出せるWh。<br>いちばん正確です</div></div>
<div class=card style="margin-top:26px;padding:30px 40px"><p style="font-size:32px;font-weight:900">充電1回の電気代（ロス多めに1.5倍）</p>
<div class=row style="font-size:34px"><span>10000mAh</span><span>約<b style="color:{G}">1.7</b>円</span></div>
<div class=row style="font-size:34px"><span>20000mAh</span><span>約<b style="color:{G}">3.4</b>円</span></div></div>
<div class=foot>単価31円/kWh＝全国家庭電気製品公正取引協議会の目安単価<br>（2022年7月現在）。実際の単価は契約プランで変わります</div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>まとめ</span><div class=pg>5/{N}</div>
<h2 style="font-size:58px">買う前・使う前に<br>この3つだけ</h2>
<div class=card style="margin-top:30px">
<div class=row style="font-size:33px"><span>☑ 対応バッテリーを説明書で確認</span></div>
<div class=row style="font-size:33px"><span>☑ モバイルバッテリーはPSEマーク</span></div>
<div class=row style="font-size:33px"><span>☑ 低温やけどの注意書きを読む</span></div></div>
<div class=big style="margin-top:30px;padding:28px 36px"><p style="font-size:32px;font-weight:900;line-height:1.5">計算のくわしい解説はサイト記事で<br><span style="color:{G}">zaq-master.github.io/ai-lab</span><br><span style="font-size:26px;color:#41507a">（キャプションのURLをコピーして開く）</span></p></div>
<div class=foot style="color:#fff;font-size:28px">AIが公開情報をもとに作成・実機レビューではありません</div>"""+AI+"</div>")
base.render(S,OUT)
