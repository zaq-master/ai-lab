# 照合メモ：電気毛布と湯たんぽ（お湯・充電式）1晩いくら（ペンネ／2026-11-24 10:00深掘り）

下書き：ops/drafts/article_yutanpo-vs-denki-blanket_draft.md（公開予定の slug 案：yutanpo-vs-denki-blanket、12月中旬。content/posts には未投入）

## 数値ごとの照合（WebFetchで公式ページを取得して原文と照合）
| 数値 | 出典URL | 結果 |
|---|---|---|
| YMK-F43P 定格75W／1時間 強 約57Wh・適温 約30Wh・弱 約13Wh／室温15℃・綿ふとん中5時間平均・JEMA測定・27円/kWh／「強」は予熱専用（寝る30分〜1時間前）、寝るときは適温 | https://yamazenbizcom.jp/client_info/YAMAZEN/itemimage/manual/XP703.pdf | 一致 |
| アイリス EHB-FR1813B-DT 定格60W／1時間の電気代0.7円（20℃環境・「弱」・31円/kWh 令和4年7月改定） | https://www.irisohyama.co.jp/products/electrical-appliances/seasonal-appliances/electric-blanket/threshold-blankets/hang-lay-blankets/ | 一致（kWhは**取得できず**＝ページに記載なし→記事では0.7÷31で逆算と明記） |
| アイリス EBK-1206/1208-ZR 36W/55W（ひざ掛け） | https://www.irisohyama.co.jp/products/electrical-appliances/seasonal-appliances/electric-blanket/for-rug/electric-blankets-rug | 一致（ただし寝具用でないため本記事では不使用） |
| 象印 CK-DH08 0.8L・600W・満水 約8分30秒（室温・水温23℃、定格、当社調べ） | https://www.zojirushi.co.jp/syohin/pot_kettle/kettle/ck-dh/ | 一致 |
| タイガー PCM-A061/A081 0.6/0.8L・1300W・満水 約3分/約4分（水温・室温23度、定格、自社測定法） | https://www.tiger-corporation.com/ja/jpn/product/kettle-pot/pcm-a1/ | 一致 |
| 無印良品 ポリエチレン湯たんぽ・大 2.3L | https://www.muji.com/jp/ja/store/cmdty/detail/4550002545611 | 一致（お湯の温度の指定は**取得できず**＝ページに記載なし） |
| 山善 YTY-S402H 400W・蓄熱 約7分（室温20℃）・あんか約8h/カイロ約4h・1回 約1.5円（31円/kWh） | https://yamazenbizcom.jp/item/R7M13.html | 一致（計算 400×7/60=0.0467kWh×31=1.45円 ✓） |
| スリーアップ EWT-2532 270W・蓄熱 約12分（室温20℃）・布団内約8.5h/身体約2.5h・1回 約1.7円 | https://three-up.co.jp/products/detail/EWT-2532 | 一致（単価は**取得できず**。0.054kWh×31=1.67円で公式と一致） |
| スリーアップ EWT-2145 360W・蓄熱 約15分（室温20℃）・アンカ約8h/カイロ約4h・1回 約2.8円 | https://three-up.co.jp/products/detail/EWT-2145 | 一致（単価は**取得できず**。0.09kWh×31=2.79円で公式と一致） |
| 目安単価31円/kWh | https://kadenfan.hitachi.co.jp/support/rei/q_a/a115.html | 既存記事と同じ前提文をそのまま流用（今回は再取得せず。2026-11-04確認分） |

取得できなかったページ：
- https://www.three-up.co.jp/ （WebFetchの許可待ちでタイムアウト。製品ページは検索結果経由で取得済みのため影響なし）
- 象印FAQ（faqchat.zojirushi.co.jp、robots.txt読めず）→不使用
- 山善 16075.pdf（文字のないPDF）→不使用

## 計算の前提（記事に明記済み）
- お湯の湯たんぽ＝ケトル満水の電力量を量に比例させた計算（1Lあたり 約0.106〜0.108kWh）。水温23℃条件なので冬は増える、と明記
- 充電式＝1晩1回蓄熱
- 他サイトの「◯円節約」は不引用。やけど等は「メーカーの取扱説明書・注意書きに従う」のみ
- 実機レビューでない旨・PR表記・単価前提の定型文あり

## 商品枠
- make_links.py：既存キー "yutanpo"（="湯たんぽ"）は変えず、新キー **"yutanpo-juden": "湯たんぽ 充電式"** を追加。products.json に {"label":"充電式（蓄熱式）湯たんぽ"} を追加→make_links 実行で html 生成（filled 1）
- python3 build.py → built 36 posts（公開記事数36のまま）。commit/push はしていない
- 記事の枠：`<!-- products: denki-moufu,yutanpo,yutanpo-juden -->`（denki-moufu は「電気毛布 ひざ掛け」の検索なので、寝具用なら将来 "denki-moufu-shiki": "電気毛布 敷き 掛け" の新枠も検討）

## 内部リンク案（公開時に差し込む。原文は 2026-11-24 時点で照合済み）
1. content/posts/neru-danbou-denkidai-calculator.md 171行目（Q「湯たんぽがいちばん安いなら…」の回答末尾）
   - 原文末尾：`…の「湯たんぽと電気毛布、どっちが安い？」の節にあります。`
   - 追記案：`…の節にあります。メーカー公表値（電気毛布の温度段階ごとの消費電力量・充電式湯たんぽの蓄熱時間）で1晩を計算した例は[電気毛布と湯たんぽ（お湯・充電式）1晩いくら？](yutanpo-vs-denki-blanket.html)にまとめています。`
2. content/posts/denki-blanket-denkidai-1jikan.md 113行目（「エアコン・こたつと比べると？」の箇条書き）
   - 原文：`- 寝る前に布団だけ温めたいなら、[布団乾燥機の電気代（あたため・乾燥・ダニ対策モード別）](futon-kansouki-denkidai.html)も参考にしてください`
   - この行の直後に追加：`- 寝るときに湯たんぽ（お湯・充電式）と1晩の電気代を比べるなら、[電気毛布と湯たんぽ 1晩いくら？](yutanpo-vs-denki-blanket.html)へ`
- 公開時は content_guard.py・mobile_check.py を通すこと。neru-danbou の front matter `updated` はリンク追加だけなので変えない
