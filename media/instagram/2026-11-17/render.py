# 2026-11-17「冬の朝、起きたら寒い…起床前に暖める3つの方法」 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py を共用し、朝テーマ用にアクセントだけ朝日の黄色へ差し替え
# 元ネタ：content/posts/fuyu-asa-aircon-timer-smart-remote.md の内容だけ（新しい数値・製品名・価格・体験談なし）
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,"..","2026-11-11"))
import base
from base import AI
for a,b in [(".tag{display:inline-block;background:#5fd4e8",".tag{display:inline-block;background:#ffd36b"),
            (".ac{color:#7fe3f2}",".ac{color:#ffe08a}"),(".u{color:#0b7f95}",".u{color:#9a5b00}"),
            (".warn{background:#e8f8fb;border-left:12px solid #1aa6c0",".warn{background:#fff8e1;border-left:12px solid #e0a800")]:
    assert a in base.CSS,a
    base.CSS=base.CSS.replace(a,b)
base.CSS+=".t td{padding:16px 6px;font-size:30px;line-height:1.35}.t th{padding:14px 6px;font-size:28px}"
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
G="#9a5b00"
S=[]
S.append(f"""<div class=w><span class=tag>保存版｜冬の朝のエアコン予約</span><div class=pg>1/6</div>
<h1>冬の朝、<br>起きたら<span class=ac>寒い</span>…</h1>
<div class=big><p style="font-size:38px;font-weight:700;color:#41507a;line-height:1.7">起きる前に暖める<b style="color:{G}">3つの方法</b><br>① エアコンの<b style="color:{G}">入タイマー</b><br>② スマートリモコンで<b style="color:{G}">時刻</b>予約<br>③ スマートリモコンで<b style="color:{G}">室温</b>を条件に</p></div>
<p class=sm style="margin-top:40px;font-size:34px;color:#fff">→ スワイプで向く人をチェック</p>
<div class=foot>保存して、寒くなる前に設定を見直してください</div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>方法① 入タイマー</span><div class=pg>2/6</div>
<h2>追加の機器なし<br>エアコンの<span class=ac>入タイマー</span></h2>
<div class=card style="margin-top:34px"><p style="font-size:34px;line-height:1.6;font-weight:700">多くの家庭用エアコンのリモコンに、<br>決めた時刻に運転を始める<br><b style="color:{G}">入タイマー（予約運転）</b>があります</p></div>
<div class=warn style="margin-top:30px"><div class=wt>早めに動き出す機種も</div><div class=wd>例：パナソニックの取扱説明書では、予約時刻に<br>設定温度近くになるよう早めに運転開始（最長約40分前）</div></div>
<div class=warn><div class=wt>弱点</div><div class=wd>基本は1回ごとに予約。セットを忘れると動かない<br>（毎日くり返せる機種もあるので取扱説明書で確認）</div></div>
<div class=foot>出典：パナソニック ルームエアコン 取扱説明書（CS-J224C〜CS-J404C2）</div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>方法② 時刻で自動化</span><div class=pg>3/6</div>
<h2>スマートリモコンで<br><span class=ac>曜日ごと</span>に予約</h2>
<div class=card style="margin-top:34px"><p style="font-size:34px;line-height:1.6;font-weight:700">エアコンのリモコンと同じ<b style="color:{G}">赤外線</b>を<br>スマホのアプリから送る機器。<br>多くの製品で、決まった時刻・曜日に<br>家電を操作する設定ができます</p></div>
<div class=warn style="margin-top:30px"><div class=wt>入タイマーとの違い</div><div class=wd>「平日6:30、休日8:00に暖房オン」のように<br>曜日で時刻を分けられる</div></div>
<div class=warn><div class=wt>弱点</div><div class=wd>赤外線がエアコンの受光部に届く位置に置かないと<br>動かない。まず手元のアプリで動くか確かめる</div></div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>方法③ 室温で自動化</span><div class=pg>4/6</div>
<h2>「室温が○℃以下で<br>暖房オン」は<span class=ac>寒い日だけ</span></h2>
<div class=card style="margin-top:34px"><p style="font-size:34px;line-height:1.6;font-weight:700">温度センサー付きのスマートリモコン<br>（または温湿度計＋ハブ）なら、<br>時刻ではなく<b style="color:{G}">部屋の寒さ</b>を<br>きっかけに動かせます</p></div>
<div class=warn style="margin-top:30px"><div class=wt>弱点</div><div class=wd>室温だけだと、夜中に冷え込んだ時点で<br>動き出すことがある</div></div>
<div class=warn><div class=wt>対策</div><div class=wd>「6:00〜8:00の間だけ」のように時間の条件と<br>組み合わせられるか、製品の公式情報で確認</div></div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>早見表</span><div class=pg>5/6</div>
<h2>あなたに向くのは<span class=ac>どれ？</span></h2>
<div class=card style="margin-top:30px;padding:24px 30px"><table class=t>
<tr><th>方法</th><th>向く人</th></tr>
<tr><td class=h>①入タイマー</td><td style="text-align:left">起きる時間が毎日同じ<br>まず追加費用なしで試したい</td></tr>
<tr><td class=h>②時刻で予約</td><td style="text-align:left">平日と休日で起床時刻が違う<br>セットを忘れがち</td></tr>
<tr><td class=h>③室温で自動</td><td style="text-align:left">暖かい日まで暖房をつけたくない<br>在宅ワークで朝から部屋を使う</td></tr>
</table></div>
<div class=warn style="margin-top:26px"><div class=wt>予約は「どちらか一方」に</div><div class=wd>入タイマーとスマートリモコンを両方入れると<br>意図しない時刻に運転が変わることがある</div></div>
<div class=foot>「できる／できない」は一般的な傾向です。具体的な機能は<br>各製品の公式情報で確認してください</div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>まとめ</span><div class=pg>6/6</div>
<h2 style="font-size:58px">設定の前に<br>この3つだけ</h2>
<div class=card style="margin-top:30px">
<div class=row style="font-size:33px"><span>☑ 起床時刻が一定なら、まず入タイマー</span></div>
<div class=row style="font-size:33px"><span>☑ 室温は20℃が目安（資源エネルギー庁）</span></div>
<div class=row style="font-size:33px"><span>☑ 早すぎる予約は電気代が増える</span></div></div>
<div class=big style="margin-top:30px;padding:28px 36px"><p style="font-size:32px;font-weight:900;line-height:1.5">3つの方法の比較はサイト記事で<br><span style="color:{G}">zaq-master.github.io/ai-lab</span><br><span style="font-size:26px;color:#41507a">（キャプションのURLをコピーして開く）</span></p></div>
<div class=foot style="color:#fff;font-size:28px">AIが公開情報をもとに作成・実機レビューではありません</div>"""+AI+"</div>")
base.render(S,OUT)
