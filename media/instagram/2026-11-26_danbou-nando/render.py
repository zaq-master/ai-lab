# 2026-11-26「暖房は何℃からつける？」 1枚 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py を共用し、アクセントはオレンジ系
# 元ネタ：content/posts/danbou-nando-kion-denkidai.md の室温20℃（資源エネルギー庁）・ウェザーニューズ調査の割合・100Wあたりの早見表だけ
# 特定機種のW数・価格は書かない
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,"..","2026-11-11"))
import base
from base import AI
for a,b in [(".tag{display:inline-block;background:#5fd4e8",".tag{display:inline-block;background:#ffb27a"),
            (".ac{color:#7fe3f2}",".ac{color:#ffc79e}"),
            (".warn{background:#e8f8fb;border-left:12px solid #1aa6c0",".warn{background:#fff3ea;border-left:12px solid #e8772e")]:
    assert a in base.CSS,a
    base.CSS=base.CSS.replace(a,b)
base.CSS+=".foot{font-size:23px}.t td{padding:10px 6px;font-size:31px}.t th{padding:12px 6px;font-size:26px}.t td.h{text-align:left;font-size:28px;line-height:1.3}"
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
rows=[("1時間","約3.1円"),("1日8時間","約24.8円"),("8時間×7日<br><span style='font-size:23px'>（1週間早めた分）</span>","約174円"),("8時間×30日<br><span style='font-size:23px'>（1ヶ月早めた分）</span>","約744円")]
tr="".join(f"<tr><td class=h>{a}</td><td style='font-size:36px;font-weight:900'>{b}</td></tr>" for a,b in rows)
S=[f"""<div class=w><span class=tag>保存版｜暖房のつけ始め</span>
<h2 style="margin-top:30px;font-size:58px">暖房は外の気温より<br><span class=ac>室温20℃</span>で決める</h2>
<p class=sm style="margin-top:10px">朝の室温が20℃を下回る日が続いたら始めどき</p>
<div class=card style="margin-top:20px;padding:16px 20px"><p style="font-size:28px;font-weight:900;margin:4px 0 8px">エアコン暖房の電気代｜消費電力100Wあたり</p><table class=t>
<tr><th>使い方</th><th>電気代の目安</th></tr>{tr}</table>
<p style="font-size:22px;color:#41507a;margin-top:8px;line-height:1.5">W ÷ 1000 × 時間 × 31円。自分のエアコンのW数 ÷ 100 を掛けて使う（W数は機種・外の気温で変わります）</p></div>
<div class=warn style="margin-top:18px;padding:16px 30px"><div class=wt>外の気温は「室温を測り始める合図」に</div><div class=wd>暖房を使った人は 気温12℃で24%・7℃で53%（調査の割合で、推奨温度ではありません）</div></div>
<div class=foot>室温20℃：資源エネルギー庁 省エネポータル／割合：ウェザーニューズの調査／単価31円/kWh：全国家庭電気製品公正取引協議会の目安単価（2022年7月現在）／AIが作成・実機レビューではありません</div>"""+AI+"</div>"]
base.render(S,OUT)
