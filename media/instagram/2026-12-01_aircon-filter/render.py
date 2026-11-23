# 2026-12-01「年末大掃除：エアコン、自分でやってよい範囲」 1枚 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py を共用し、アクセントは黄色系
# 元ネタ：ops/drafts/article_aircon-filter-souji_draft.md の確認済みの内容だけ（三菱電機 霧ヶ峰資料PDF 2023-12-05・パナソニック公式 170106、2026-11-21確認）。価格・製品名は書かない
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,"..","2026-11-11"))
import base
from base import AI
for a,b in [(".tag{display:inline-block;background:#5fd4e8",".tag{display:inline-block;background:#ffd36b"),
            (".ac{color:#7fe3f2}",".ac{color:#ffe08f}"),
            (".warn{background:#e8f8fb;border-left:12px solid #1aa6c0",".warn{background:#fff8e1;border-left:12px solid #d99a00")]:
    assert a in base.CSS,a
    base.CSS=base.CSS.replace(a,b)
base.CSS+=(".foot{font-size:22px}.t td{padding:8px 8px;font-size:29px}.t th{padding:10px 6px;font-size:26px}"
           ".t td.h{text-align:left;font-size:29px;line-height:1.3}.ok{color:#15803d;font-weight:900}.ng{color:#c2410c;font-weight:900;background:#ffe9dc}")
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
rows=[("フィルターのホコリ取り（掃除機）",1),("汚れがひどい時だけ水洗い→陰干し",1),("外から見える部分の拭き掃除",1),
      ("室外機のまわりの片付け",1),("内部の洗浄（市販スプレー・除菌剤）",0),("分解する・電気部品を外す",0),("本体に消臭剤・抗菌剤を吹きかける",0)]
tr="".join(f"<tr><td class=h>{t}</td><td class={'ok' if o else 'ng'}>{'○ してよい' if o else '× しない'}</td></tr>" for t,o in rows)
S=[f"""<div class=w><span class=tag>保存版｜年末大掃除・エアコン</span>
<h2 style="margin-top:28px;font-size:54px">エアコンの大掃除<br><span class=ac>自分でやるのはどこまで？</span></h2>
<p class=sm style="margin-top:10px;font-size:28px;line-height:1.5">フィルター約半年そのまま→消費電力 <b class=ac>約12%悪化</b><br>（三菱電機調べ・冷房／暖房の別は記載なし）</p>
<div class=card style="margin-top:16px;padding:14px 22px"><table class=t>
<tr><th>場所・作業</th><th style="width:210px">自分で？</th></tr>{tr}</table>
<p style="font-size:21px;color:#41507a;margin-top:6px;line-height:1.45">内部の汚れ・カビが見えたら、メーカーやクリーニング業者に相談</p></div>
<div class=warn style="margin-top:14px;padding:14px 30px"><div class=wt>ブラシの扱いはメーカーで違う</div><div class=wd>パナソニック＝古い歯ブラシ×・専用ブラシが望ましい<br>三菱電機＝ブラシ・たわしは使わない</div></div>
<div class=foot>出典：三菱電機 霧ヶ峰の資料（2023年12月）／パナソニック公式（2026-11-21確認）／機種で違うため取扱説明書を優先／AIが作成・実機レビューではありません</div>"""+AI+"</div>"]
base.render(S,OUT)
