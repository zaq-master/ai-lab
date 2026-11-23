# 2026-12-03「年末大掃除：窓の結露を毎朝ラクに取る道具」 1枚 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py を共用し、アクセントはライム系
# 元ネタ：ops/drafts/article_ketsuro-tori-dougu_draft.md の確認済みの内容だけ（ケルヒャー公式FAQ・製品ページ、ニトムズ製品ページ、2026-11-21確認）。ワイパーは公式仕様を確認できていないため数値なし。価格は書かない
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,"..","2026-11-11"))
import base
from base import AI
for a,b in [(".tag{display:inline-block;background:#5fd4e8",".tag{display:inline-block;background:#c6f06b"),
            (".ac{color:#7fe3f2}",".ac{color:#d4f78f}"),
            (".warn{background:#e8f8fb;border-left:12px solid #1aa6c0",".warn{background:#f4fbe4;border-left:12px solid #5f9e10")]:
    assert a in base.CSS,a
    base.CSS=base.CSS.replace(a,b)
base.CSS+=(".foot{font-size:22px}.t td{padding:11px 8px;font-size:26px;line-height:1.35}.t th{padding:10px 6px;font-size:25px}"
           ".t td.h{text-align:left;font-size:27px;line-height:1.3;width:230px}.t td.l{text-align:left}")
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
rows=[("窓用<br>バキューム","なでて水を吸いタンクへ<br>たまったら捨てる＋充電","大きい窓・<br>窓が多い家"),
      ("結露取り<br>ワイパー","なでて水を集める<br>受け皿・タオルの水を捨てる","窓が1〜2枚・<br>充電いらず"),
      ("結露<br>吸水テープ","貼るだけ。吸える量に上限あり","拭けない朝の<br>保険")]
tr="".join(f"<tr><td class=h>{a}</td><td class=l>{b}</td><td style='font-size:24px'>{c}</td></tr>" for a,b,c in rows)
S=[f"""<div class=w><span class=tag>保存版｜年末大掃除・窓の結露</span>
<h2 style="margin-top:28px;font-size:54px">毎朝の結露取り<br><span class=ac>3つの道具の向き不向き</span></h2>
<div class=card style="margin-top:20px;padding:14px 20px"><table class=t>
<tr><th>道具</th><th>毎朝の手間</th><th style="width:220px">向く窓・人</th></tr>{tr}</table>
<p style="font-size:21px;color:#41507a;margin-top:6px;line-height:1.45">おすすめは組み合わせ：ワイパーかバキュームで取る＋垂れた分をテープで受ける</p></div>
<div class=card style="margin-top:14px;padding:14px 28px"><div style="font-size:28px;font-weight:900">公式で確認できた仕様の例</div>
<div class=row style="font-size:26px;padding:8px 0"><span>ケルヒャー WV 1 White</span><b>稼働25分・タンク100ml</b></div>
<div class=row style="font-size:26px;padding:8px 0"><span>ニトムズ 強力結露吸水テープ</span><b>1mあたり約130g</b></div></div>
<div class=warn style="margin-top:14px;padding:14px 30px"><div class=wt>バキュームの注意（ケルヒャー公式FAQ）</div><div class=wd>くもり止め加工の鏡は傷のおそれ<br>すりガラスは水分が残ることがある</div></div>
<div class=foot>出典：ケルヒャー公式FAQ・製品ページ／ニトムズ製品ページ（2026-11-21確認）<br>ワイパーは公式の仕様を確認できず数値なし／AIが作成・実機レビューではありません</div>"""+AI+"</div>"]
base.render(S,OUT)
