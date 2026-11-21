# 未確認の再確認 2026-11-21 13時（ペンネ）

対象：ops/drafts/article_kashitsuki-citric-souji_draft.md／ops/drafts/article_ketsuro-tori-dougu_draft.md
方法：WebSearch で公式URLを出してから WebFetch で本文を読んだ。PDFの直接ダウンロード（curl）は接続拒否（403）で、画像での目視はできていない。

## A. 加湿器のクエン酸掃除

| 項目 | 下書き | 公式の記述とURL | 結果 |
|---|---|---|---|
| ダイニチ取扱説明書の洗浄剤の表（メモ3） | 本文は「水4Lに約25g」（公式記事40125）。PDFは「クエン酸150g／重曹25g」とも読めて保留 | PDF 3冊（[HD-RXT525ほか](https://www.dainichi-net.co.jp/uploads/2025img/hd-rxt525_rxt725_rxt925.pdf)・[HD-LX1025ほか](https://www.dainichi-net.co.jp/uploads/2025img/hd-lx1025_1225.pdf)・[HD-LX1022ほか](https://www.dainichi-net.co.jp/uploads/manual/humidifier/hd-lx1022_1222.pdf)）はテキストだとどれも「クエン酸 4.0Lあたり約150g／重曹 約25g（大さじ２杯半）」。一方、同じ表を本文に載せた[ダイニチ公式記事 38300](https://www.dainichi-net.co.jp/products/mainichi-plus/38300/)は「クエン酸 ぬるま湯4.0Lあたり約25ｇ（大さじ2杯半）※1／重曹 約150ｇ※1」。[旧取扱説明書 HD-152](https://www.dainichi-net.co.jp/uploads/manual/humidifier/hd152.pdf)は文章で「クエン酸 8.0Lあたり約50g（大さじ５杯）」（＝4Lで25g）。[公式のクエン酸セット](https://webshop.dainichi-net.co.jp/c/814186/814187/citricacid-web21068)も1袋100g | **解消**：PDFは抽出時に量の列が入れ替わっているだけと判断。本文の25gは正しい。メモ3を【済】にした（PDFの画像での目視は今回もできていない） |
| 「濃度が高いと部品破損」の対象 | 監査で「重曹だけ」に直した文 | 38300の表では ※1「濃度が高いと部品破損の原因になります。」がクエン酸・重曹の**両方**に付く。HD-152もクエン酸に※1 | **修正**：注意の行を「クエン酸・重曹とも濃度が高いと部品破損の原因」に直し、出典に38300を追加 |
| ダイニチの量の大さじ表記 | Q&Aは「水4Lに約25g」 | 38300「約25ｇ（大さじ2杯半）」 | **追記**：Q&Aに「（大さじ2杯半）」を足した |
| シャープ care_06（メモ5） | 1Lに約6g・約2時間・40℃以下、重曹1Lに約36g・約60分、混ぜない | [care_06](https://jp.sharp/support/advice/air_purifier/care_06.html)「1Lあたり約6g（大さじ2/3杯）」「2時間」「40℃以下」、重曹「水1Lあたり約36g（大さじ4杯）」「約60分」、「クエン酸と重曹は混ぜて使わないでください。」 | **一致** |
| シャープ kild50（メモ5） | 1か月に1回程度 | [kild50](https://jp.sharp/support/air_purifier/mt_doc/kild50/filter_humi_care_kild50.html)「1カ月に1回程度」・約6g/L・約2時間 | **一致** |
| アイリスオーヤマ FAQ ID=430（メモ2） | 本文では使っていない | ID=430 は取得許可がタイムアウトして開けず。参考に[公式コラム](https://www.irisohyama.co.jp/plusoneday/electronics/29)を確認（「水3Lに対してクエン酸20g」、スチーム式は約1時間運転、超音波式はクエン酸の記載なし） | **未確認のまま**（本文に影響なし。コラムの値も本文に足していない） |
| 象印 FAQ（メモ4） | 本文は EE-RT35/50 取扱説明書の値に限定 | [象印FAQ](https://faq-support.zojirushi.co.jp/kb/article/%E5%8A%A0%E6%B9%BF%E5%99%A8(%E3%82%B9%E3%83%81%E3%83%BC%E3%83%A0%E5%BC%8F)%E3%81%A7%E3%82%AF%E3%82%A8%E3%83%B3%E9%85%B8%E6%B4%97%E6%B5%84%E3%81%AE%E3%81%8A%E6%89%8B%E5%85%A5%E3%82%8C%E6%96%B9%E6%B3%95%E3%82%92%E6%95%99%E3%81%88%E3%81%A6%E3%81%8F%E3%81%A0%E3%81%95%E3%81%84%E3%80%82/)は回答本文が空で取得できず（ページ側の処理で本文を出すため） | **未確認のまま**（本文は機種を限定済みなので公開に支障なし） |

## B. 窓の結露取り道具

| 項目 | 下書き | 公式の記述とURL | 結果 |
|---|---|---|---|
| WV 1 プラス LR／プレミアム LR が現行か（メモ2） | 表に約25分・約100分（FAQ） | [ケルヒャー公式FAQ](https://www.kaercher.com/jp/service/faq/product/window-vacs.html)「約25分間連続」「充電時間が約100分」、「WV 50 plusとWV 75 plusの後継品です」。販売終了の記載なし。日本の製品ページは検索で見つからず（[WV 1 16330040](https://www.kaercher.com/jp/home-garden/window-vacs/wv-1-16330040.html)は約25分・150分・100ml） | **一部解消**：FAQの値は一致・販売終了の記載なし。製品ページがないため、商品ボタンでこの型番を勧めない旨をメモに追記 |
| 結露取りワイパーの公式仕様（メモ3） | 数値なし | 山崎産業の公式仕様ページは検索で出ず（価格比較・通販・紹介記事のみ） | **確認できず**（数値なしのままで公開に支障なし） |
| ニトムズ 強力結露吸水テープ 10m（メモ4） | 30mm×10m・厚さ約4.5mm・1mあたり約130g、交換時期は「製品の表示に従う」 | [10m製品ページ](https://www.nitoms.com/products/madoeco_condensation_tape_10m/)「約4.5mm× 30mm× 10m」「最大吸水量約130g（1mあたり）」。交換時期・貼れない場所・注意は[10m](https://www.nitoms.com/products/madoeco_condensation_tape_10m/)・[2WAY](https://www.nitoms.com/products/madoeco_condensation_tape_2way/)・[FAQ](https://www.nitoms.com/faq/category/eco/)のどれにも記載なし | **一致**（記載がないことも確認。本文のままでよい） |

## まとめ
- 解消（一致・修正を含む）：ダイニチPDFの表、濃度の注意の対象、大さじ表記、シャープ2ページ、ケルヒャーFAQの値、ニトムズ10m＝**6件**
- 残った未確認：アイリスFAQ ID=430、象印FAQ、ワイパーの公式仕様＝**3件**（どれも本文の数値には使っていない）
- 下書き2本とも、本文に出典のない数値はない。公開してよい状態（公開回で商品枠を追加 → build → content_guard・mobile_check）
