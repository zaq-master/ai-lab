# 2026-11-15「USB-C充電器、何W買えばいい？買う前の4チェック」 python3 render.py <出力フォルダ>
# 見た目は ../2026-11-11/base.py を共用し、充電テーマ用にアクセントだけ黄緑へ差し替え
# 元ネタ：content/posts/usb-c-charger-guide.md の内容だけ（新しい数値・製品名なし）
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,"..","2026-11-11"))
import base
from base import AI
for a,b in [(".tag{display:inline-block;background:#5fd4e8",".tag{display:inline-block;background:#a8e063"),
            (".ac{color:#7fe3f2}",".ac{color:#c4f07f}"),(".u{color:#0b7f95}",".u{color:#3f7d12}"),
            (".warn{background:#e8f8fb;border-left:12px solid #1aa6c0",".warn{background:#f1fae6;border-left:12px solid #5fa82a")]:
    assert a in base.CSS,a
    base.CSS=base.CSS.replace(a,b)
OUT=sys.argv[1] if len(sys.argv)>1 else HERE
G="#3f7d12"
S=[]
S.append(f"""<div class=w><span class=tag>保存版｜USB-C充電器の選び方</span><div class=pg>1/6</div>
<h1>USB-C充電器、<br>何W買えばいい？<br><span class=ac>買う前の4チェック</span></h1>
<div class=big><p style="font-size:38px;font-weight:700;color:#41507a;line-height:1.7">① いちばん電力を使う機器で<b style="color:{G}">W数</b><br>② 複数ポートは<b style="color:{G}">配分表</b><br>③ <b style="color:{G}">USB PD</b>対応・持ち歩くなら<b style="color:{G}">GaN</b><br>④ <b style="color:{G}">ケーブル</b>の対応W数も</p></div>
<p class=sm style="margin-top:40px;font-size:34px;color:#fff">→ スワイプで1つずつ</p>
<div class=foot>保存して、充電器を買う前に見返してください</div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>チェック① W数</span><div class=pg>2/6</div>
<h2>いちばん電力を使う<br>機器に<span class=ac>合わせる</span></h2>
<div class=card style="margin-top:34px;padding:30px 36px"><table>
<tr><th>機器の例</th><th>目安の出力</th></tr>
<tr><td class=h>スマホ</td><td>20〜30W</td></tr>
<tr><td class=h>タブレット</td><td>30〜45W</td></tr>
<tr><td class=h>薄型ノートPC</td><td>45〜65W</td></tr>
<tr><td class=h>高性能ノートPC</td><td>65〜100W以上</td></tr>
</table></div>
<div class=warn style="margin-top:30px"><div class=wt>足りないと…</div><div class=wd>「充電が遅い」「使いながらだと減っていく」</div></div>
<div class=foot>あくまで目安です。正確な数値は、使っている機器の<br>公式サイトや付属充電器の表示で確認してください</div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>チェック② 複数ポート</span><div class=pg>3/6</div>
<h2>「合計」と「1ポートあたり」<br><span class=ac>両方</span>見る</h2>
<div class=warn style="margin-top:36px"><div class=wt>合計出力</div><div class=wd>全ポートを同時に使ったときの上限</div></div>
<div class=warn><div class=wt>1ポートあたりの最大出力</div><div class=wd>1台だけつないだときに出せる上限</div></div>
<div class=card style="margin-top:34px"><p style="font-size:34px;line-height:1.6;font-weight:700">たとえば「合計65W」でも、<br>2台同時につなぐと配分が変わり、<br><b style="color:{G}">ノートPC側が想定より少なくなる</b><br>ことがあります</p></div>
<div class=foot>商品ページの「ポートごとの出力配分表」を必ず確認</div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>チェック③ 規格と中身</span><div class=pg>4/6</div>
<h2>迷ったら<span class=ac>USB PD</span>対応<br>持ち歩くなら<span class=ac>GaN</span></h2>
<div class=card style="margin-top:36px"><p style="font-size:40px;font-weight:900;color:{G}">USB PD（USB Power Delivery）</p>
<p style="font-size:31px;line-height:1.6;color:#41507a;margin-top:10px">ノートPCやiPhone・Androidの多くが<br>この規格で急速充電。<br>「PD対応」と書かれたものなら大きく外しにくい</p></div>
<div class=card style="margin-top:30px"><p style="font-size:40px;font-weight:900;color:{G}">GaN（窒化ガリウム）</p>
<p style="font-size:31px;line-height:1.6;color:#41507a;margin-top:10px">充電器の中に使われる半導体の素材。<br><b>小さく・発熱しにくく</b>作りやすいので、<br>同じW数でもコンパクトな製品が増えている</p></div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>チェック④ ケーブルと安全</span><div class=pg>5/6</div>
<h2>充電器が高出力でも<br><span class=ac>ケーブルしだい</span></h2>
<div class=warn style="margin-top:36px"><div class=wt>60Wを超える充電には</div><div class=wd>「100W（5A）対応」と書かれたケーブルが必要</div></div>
<div class=warn><div class=wt>対応W数が書いてあるものを</div><div class=wd>安すぎるノーブランド品は避ける</div></div>
<div class=warn><div class=wt>PSEマークを確認</div><div class=wd>日本で販売される電源機器には表示が必要</div></div>
<div class=warn><div class=wt>保護機能の記載</div><div class=wd>過電流・過熱保護などが書いてあるか</div></div>"""+AI+"</div>")
S.append(f"""<div class=w><span class=tag>まとめ</span><div class=pg>6/6</div>
<h2 style="font-size:58px">買う前に<br>この4つだけ</h2>
<div class=card style="margin-top:30px">
<div class=row style="font-size:34px"><span>☑ いちばん電力を使う機器でW数</span></div>
<div class=row style="font-size:34px"><span>☑ 複数ポートは配分表を見る</span></div>
<div class=row style="font-size:34px"><span>☑ USB PD対応・持ち歩くならGaN</span></div>
<div class=row style="font-size:34px"><span>☑ ケーブルの対応W数も合わせる</span></div></div>
<div class=big style="margin-top:30px;padding:28px 36px"><p style="font-size:32px;font-weight:900;line-height:1.5">くわしい解説はサイト記事で<br><span style="color:{G}">zaq-master.github.io/ai-lab</span><br><span style="font-size:26px;color:#41507a">（キャプションのURLをコピーして開く）</span></p></div>
<div class=foot style="color:#fff;font-size:28px">AIが公開情報をもとに作成・実機レビューではありません</div>"""+AI+"</div>")
base.render(S,OUT)
