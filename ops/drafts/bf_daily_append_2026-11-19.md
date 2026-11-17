# BF更新メモ 初日分 下書き（11/19 20:00以降の回で5分で貼る）

1. **貼り付け先**：content/posts/rakuten-blackfriday-memo.md 末尾の `<!-- draft-template ... -->` コメントの閉じ `-->` のすぐ下（初回なので下の「貼り付けブロック」をまるごと。空行を入れない）
2. **手順**：下のチェック項目を公式ページで確認 → `【要確認】` 行を確認できた事実1行に置き換えて貼る → `python3 build.py` → 表示確認（下の grep 3つ＋mobile_check）→ `git pull --rebase && git add -A && git commit && git push` → 1〜2分後に公開ページで表示を確認
3. **ルール**：楽天公式（event.rakuten.co.jp／www.rakuten.co.jp）で確認できた事実だけ。価格・割引率・還元率・倍率・上限額・クーポン額は書かない。【PR】表記と「運営はAI」の明記は記事冒頭にあるので追加不要（消さない）

---

## 作成時点（2026-11-17）の状況
- 確認済みの事実（2026-11-16 に公式キャンペーンページで照合済み・記事にも掲載済み）：
  - 期間：2026年11月19日（木）20:00〜11月25日（水）1:59
  - エントリー開始：11月12日（木）10:00
  - 出典：https://event.rakuten.co.jp/campaign/point-up/blackfriday/
- 2026-11-17 の再確認：公式ページの取得が許可待ちのまま時間切れとなり、**未確認**（新しい事実は足していない）
- 手順書（bf_daily_append_howto.md）では初回追記を 11/20 としている（11/19 の 08:00・11:00 は開始前のため）。この下書きは **11/19 20:00 以降の最初の回**（11/19 21:00・22:00、または 11/20 の担当回）で使う。その日に記事内に同じ日付があれば何もしない

## 当日、公式ページで確認してから書く（チェック項目）
確認先：公式キャンペーンページ https://event.rakuten.co.jp/campaign/point-up/blackfriday/ と、そこからリンクされた楽天公式の企画ページのみ

- [ ] ページが開催中の表示になっているか（期間の表記が 11/19 20:00〜11/25 1:59 のままか）→ 変わっていたら記事の「開催日時」も直す必要があるので、追記せず Slack で報告
- [ ] ページに載っている**企画の名前**（例：クーポン・タイムセール等の枠名。名前だけ、ページの文言どおり）
- [ ] その企画の**日時・時間帯**（ページに書かれている場合のみ）
- [ ] その企画に**エントリーが必要か**（ページに書かれている場合のみ）
- [ ] 当日のクーポン内容・割引額・倍率 → **書かない**（確認できても書かない）
- [ ] 確認した時刻（HH:MM）を控える

いずれも確認できなければ、**その回は追記しない**（「特になし」「準備中」も書かない）。ログに「BF更新メモ：公式で新しい事実を確認できず、追記なし」を1行。

## 貼り付けブロック（初回・空行なしでこのまま貼る）
`11/DD（曜）` は貼る日に合わせる（11/19なら「11/19（木）」、11/20なら「11/20（金）」）。`【要確認】` の行は必ず置き換える。

```
<!-- blackfriday-2026-11 期間中の更新メモ -->
## 期間中の更新メモ（楽天公式で確認できたことだけ）
- **11/DD（曜）**：
  【要確認】公式ページで確認した事実を1行（例の形：「公式ページに『◯◯』の企画が掲載（◯/◯ ◯:◯◯〜、エントリー必要）」。数字は日時のみ）
  出典：[楽天市場 ブラックフライデー 公式キャンペーンページ](https://event.rakuten.co.jp/campaign/point-up/blackfriday/)（11/DD HH:MM 確認）
```

- 企画ページ側で確認した場合は、出典のページ名とURLをその企画ページ（event.rakuten.co.jp／www.rakuten.co.jp 配下）に差し替える
- 1件は「日付／事実1行／出典」の3行だけ。評価（お得・おすすめ）や体験談は書かない

## 表示確認（push前）
```
python3 build.py
grep -c "draft-template" docs/posts/rakuten-blackfriday-memo.html     # 0
grep -n "期間中の更新メモ" docs/posts/rakuten-blackfriday-memo.html     # 見出しが出る
grep -c "開催中です" docs/posts/rakuten-blackfriday-memo.html           # 1以上（11/19 20:00以降のbuild）
grep -c "【要確認】\|11/DD\|HH:MM" docs/posts/rakuten-blackfriday-memo.html   # 0（穴埋めの置き忘れがないこと。1以上ならpushしない）
python3 ops/tests/mobile_check.py
git pull --rebase && git add -A && git commit -m "HH:MM BF更新メモ 11/DD" && git push
```
- push後1〜2分で https://zaq-master.github.io/ai-lab/posts/rakuten-blackfriday-memo.html を開き、追記と「開催中です」が出ていることを確認してから報告
- ops/log/当日.md に「BF更新メモ追記：<事実の要約>（出典URL）」を1行
