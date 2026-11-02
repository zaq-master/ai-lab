# 2027 Habit & Goal Planner（Etsy／DreamyPixelCo 用・未出品）

事業10（Etsyデジタル商品）の試作第1弾。作成：エミリー（2026-11-02）。

## 中身
| ファイル | 内容 |
|---|---|
| `2027-Habit-Goal-Planner_US-Letter.pdf` | 印刷用PDF 13ページ（8.5×11in） |
| `2027-Habit-Goal-Planner_A4.pdf` | 印刷用PDF 13ページ（210×297mm） |
| `thumbnail_2000x1600.png` | Etsy用サムネイル（2000×1600） |
| `listing.md` | 英語の出品文（タイトル・説明・タグ13個・価格案・AI開示） |
| `src/build.py` | PDFの生成スクリプト（HTML→Playwright PDF） |
| `src/thumbnail.py` | サムネイルの生成スクリプト（PDFのページ画像から合成） |

作り直す手順：`cd src && python3 build.py && python3 thumbnail.py`（pdftoppm と Playwright が必要）

## この商品を選んだ理由
数字はすべてRankHero（第三者のEtsyキーワードツール）の値。Etsy公式の数字ではない。
- 「habit tracker」の月間検索数は、2025年12月が16.5万、2026年1月が20.1万で、通常月（9万）の約2倍。年末年始に需要が集中する。中央値は$4.95。（[出典](https://www.rankhero.com/keywords/habit-tracker)）
- 「2027 planner」の月間検索数は、2026年8月が2.2万、9月が3.3万で伸びている。出品数は70,241件。（[出典](https://www.rankhero.com/keywords/2027-planner)）
- 「budget planner」の月間検索数は1月が7.4万で、通常は6万前後。出品数は約25〜29万件で競合が多い。（[出典](https://www.rankhero.com/keywords/budget-planner)）
- 結論：年末〜1月に需要が最も跳ねる habit tracker を主役にし、「2027」と「goal」の検索もタイトルで拾う組み合わせにした。
- 競合の例：TheNeutralPlanner（プランナー素材のショップ）は販売数2,642件、レビュー4.7（351件）、価格はCA$4.46〜11.90（[ショップページ](https://www.etsy.com/ca/shop/TheNeutralPlanner)、2026-11-02に確認）。RankHeroの上位リストにある数字（例：Digicarftの$17.99の商品で「8,587」）は項目名が書かれておらず、販売数かどうか確認できないため使っていない。

## ライセンス
- フォント：Inter（SIL Open Font License 1.1）、Caladea（SIL Open Font License 1.1）。どちらも商用利用可。PDFにはサブセットを埋め込んでいる（OFLで許可されている）。出典はDebianパッケージの fonts-inter と fonts-crosextra-caladea の copyright ファイル。
- 図形・カレンダー・ホイール・サムネイル：すべてHTML/CSS/SVGで自作。写真・ストック素材・他人のイラストは使っていない。
- 2027年のカレンダーはPythonの calendar モジュールで生成している（日曜始まり。2027年1月1日は金曜日）。

## 規約メモ（Etsy、2026-10-22発表の新ルール）
- AIを使ったデジタル商品は、本人が創作に関わっていて、AIの使用を開示すれば出品できる。listing.md の説明文に「ページのデザインとレイアウトはAI（Claude by Anthropic）がコードで生成した」と明記してある（2026-11-02 修正）。Etsy公式ページでの確認は未実施（要確認）。
- AIが作った「手順書」（型紙・レシピ・ガイド）は禁止。このプランナーには使い方ガイドを入れていない。今後も入れない。
- 人の関与がない自動生成の出品（botによる量産）は禁止。量産せず、1点ずつオーナーが確認してから出品する。
- 上記は二次情報（ブログ記事）による。出品前にオーナーがEtsyのSeller Handbookとポリシーページで最終確認すること。

## オーナー作業（出品時、合計15分ほど）
1. DreamyPixelCoにログインし、新しい出品を作る（デジタル商品として登録）
2. listing.md の内容を貼り付け、PDF2つをアップロード。サムネイルと、PDFのページを書き出した画像をプレビューとして載せる
3. 出品料などの手数料と「Who made it」の選択を確認し、公開する

> 生成スクリプト（*.py）は2026-11-03から公開リポジトリの追跡外。新しい環境では `git show 6adcf7a:<パス> > <パス>` で復元して使う（非公開の保管先ができたら移す）。
