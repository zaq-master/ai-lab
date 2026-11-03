# 2026-11-11「窓の結露、加湿しすぎ？露点で見分ける」 python3 render.py <出力フォルダ>
import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from base import render,AI
OUT=sys.argv[1] if len(sys.argv)>1 else os.path.dirname(os.path.abspath(__file__))
S=[]
S.append("""<div class=w><span class=tag>保存版｜在宅ワーク部屋の結露</span><div class=pg>1/6</div>
<h1>窓の結露、<br>加湿しすぎ？</h1>
<h2 style="font-size:64px;margin-top:36px"><span class=ac>「露点（ろてん）」</span>で<br>見分ける早見表</h2>
<div class=big><p style="font-size:38px;font-weight:700;color:#41507a;line-height:1.6">湿度の数字だけでなく<br><b style="color:#0b7f95">室温 × 湿度</b> と <b style="color:#0b7f95">窓の冷たさ</b><br>の組み合わせで決まる</p></div>
<p class=sm style="margin-top:40px;font-size:34px;color:#fff">→ スワイプで早見表</p>
<div class=foot>保存して、窓が濡れた朝に見返す用</div>"""+AI+"</div>")
S.append("""<div class=w><span class=tag>結露のしくみ</span><div class=pg>2/6</div>
<h2>露点＝空気を冷やしていくと<br><span class=ac>結露が始まる温度</span></h2>
<div class=card>
<div class=row><span>窓の表面温度 <b>＞</b> 露点</span><b style="color:#0b7f95">結露しない</b></div>
<div class=row><span>窓の表面温度 <b>≦</b> 露点</span><b style="color:#c2410c">結露する</b></div></div>
<div class=warn style="margin-top:36px"><div class=wt>同じ湿度50%でも</div><div class=wd>室温が高いほど露点も高くなり、<br>冷たい窓で結露しやすくなる</div></div>
<div class=warn><div class=wt>露点は室温と湿度から計算できる</div><div class=wd>Tetens（テテンス）の式という公知の近似式を使用</div></div>
<div class=foot>式の出典：Tetens, O. (1930) Zeitschrift für Geophysik 6</div>"""+AI+"</div>")
S.append("""<div class=w><span class=tag>早見表①　露点</span><div class=pg>3/6</div>
<h2>室温と湿度から見る<br><span class=ac>露点</span>（結露が始まる温度）</h2>
<div class=card style="padding:30px 30px"><table>
<tr><th>室温＼湿度</th><th>40%</th><th>50%</th><th>60%</th><th>70%</th></tr>
<tr><td class=h>18℃</td><td>4.2℃</td><td>7.4℃</td><td>10.1℃</td><td>12.5℃</td></tr>
<tr><td class=h>20℃</td><td>6.0℃</td><td>9.3℃</td><td class=hi>12.0℃</td><td>14.4℃</td></tr>
<tr><td class=h style="border-bottom:none">22℃</td><td style="border-bottom:none">7.8℃</td><td style="border-bottom:none">11.1℃</td><td style="border-bottom:none">13.9℃</td><td style="border-bottom:none">16.3℃</td></tr>
</table></div>
<p style="font-size:34px;line-height:1.6;margin-top:36px">例：室温20℃・湿度60%なら露点は<b class=ac>約12℃</b>。<br>窓の内側が12℃以下まで冷えると<br>そこで結露が始まる</p>
<div class=foot>※Tetensの式で計算した目安（小数第1位で四捨五入、値はすべて「約」）</div>"""+AI+"</div>")
S.append("""<div class=w><span class=tag>早見表②　湿度の上限</span><div class=pg>4/6</div>
<h2>窓の表面温度から見る<br>「<span class=ac>この湿度まで</span>」の上限</h2>
<div class=card style="padding:30px 30px"><table>
<tr><th>窓の表面温度</th><th>室温20℃</th><th>室温22℃</th></tr>
<tr><td class=h>5℃</td><td>約37%</td><td>約33%</td></tr>
<tr><td class=h>8℃</td><td>約46%</td><td>約41%</td></tr>
<tr><td class=h>10℃</td><td>約53%</td><td>約46%</td></tr>
<tr><td class=h>12℃</td><td>約60%</td><td>約53%</td></tr>
<tr><td class=h style="border-bottom:none">14℃</td><td style="border-bottom:none">約68%</td><td style="border-bottom:none">約60%</td></tr>
</table></div>
<p style="font-size:33px;line-height:1.55;margin-top:30px">窓が<b class=ac>冷えるほど</b>、結露しない湿度の<br>上限は<b class=ac>下がる</b></p>
<div class=foot>※計算上の目安。窓の表面温度は外気温・窓の種類・カーテンで<br>大きく変わるため、気になる場合は実際に測るのが確実</div>"""+AI+"</div>")
S.append("""<div class=w><span class=tag>調整の順番</span><div class=pg>5/6</div>
<h2 style="font-size:56px">湿度計を見て<br>まず試すこと</h2>
<div class=warn style="margin-top:34px"><div class=wt>70%を超えている</div><div class=wd>→ 加湿器の設定を下げる・運転時間を短く</div></div>
<div class=warn><div class=wt>40〜60%台で窓だけ結露</div><div class=wd>→ 加湿しすぎより「窓が冷たすぎる」ケース。<br>換気、窓まわりの冷え対策を検討</div></div>
<div class=warn><div class=wt>朝だけ結露する</div><div class=wd>→ 夜間の加湿を止める・弱める<br>（夜は室温が下がり露点との差が縮む）</div></div>
<div class=warn><div class=wt>40%を下回る</div><div class=wd>→ 結露より乾燥が問題</div></div>
<div class=foot>目安：建築物衛生法の基準（事務所など）で相対湿度40〜70%。<br>自宅に義務があるわけではありません</div>"""+AI+"</div>")
S.append("""<div class=w><span class=tag>まとめ</span><div class=pg>6/6</div>
<h2 style="font-size:58px">結露は<br><span class=ac>窓の温度 ≦ 露点</span> で起きる</h2>
<div class=card style="margin-top:36px">
<div class=row><span>室温20℃・湿度50%</span><b>露点 約9.3℃</b></div>
<div class=row><span>室温20℃・湿度60%</span><b>露点 約12.0℃</b></div>
<div class=row><span>70%超</span><b>加湿しすぎ</b></div>
<div class=row><span>40〜60%台で結露</span><b>窓の冷えを疑う</b></div></div>
<div class=big style="margin-top:34px;padding:28px 36px"><p style="font-size:32px;font-weight:900;line-height:1.5">露点の式・早見表のくわしい版は<br><span style="color:#0b7f95">「QOLガジェット研究所」で検索</span></p></div>
<div class=foot style="color:#fff;font-size:28px">AIが公開情報をもとに作成・実機レビューではありません<br>（表の数値は計算上の目安）</div>"""+AI+"</div>")
render(S,OUT)
