# 布団乾燥機の電気代記事：見出し構成と内部リンク案（11/15解禁後の制作回用）
作成：2026-11-13 00:07 自走回（本文は書かない＝停止週。数字は ops/research/futon_dryer_specs_2026-11-12.md の公表値と試算のみ）

## タイトル案（どれか1つ）
1. 布団乾燥機の電気代は1回いくら？メーカー公表値で計算（パナソニック・日立・アイリス）
2. 布団乾燥機を毎日使うと電気代は月いくら？1回5円〜20円台の目安【公表値で試算】

## 見出し
1. 結論：1回あたり約5〜24円（31円/kWh・公表値の上限で計算）※実機レビューではない旨をここで明記
2. 計算のしかた（消費電力W × 時間 ÷ 1000 × 31円）— 電気代計算ツール記事へリンク
3. 機種別の1回・毎日・週3回の表（パナ FD-F06A6／日立 HFK-VH700・HFK-D100／アイリス ツインノズル）
   - 日立は「最大680W」で計算、アイリスは「タイマー60分にした場合」と条件を書く
4. 寝る前の「ふとん暖め」だけなら1回約5円（日立D100 15分）— 電気毛布・こたつ記事と比べる導線
5. ダニ対策コースは1回40〜80円台（効果は書かない、電気代だけ）
6. 部屋干しに使う場合 — 部屋干し・除湿機記事へリンク
7. まとめ＋楽天ボタン（【PR】表記・価格は書かない）

## 内部リンク（既存記事・すべて docs/posts に生成済みを確認）
- denkidai-calculator.html（計算ツール）
- neru-danbou-denkidai-calculator.html（寝るときの暖房）
- denki-moufu-kotatsu-denkidai-telework.html（電気毛布・こたつ）
- fuyu-heyaboshi-joshitsuki-denkidai.html（部屋干し）
- fuyu-denkidai-matome.html（冬の電気代まとめ）← まとめ側からもこの記事へ戻りリンクを足す

## 公開日にやること
- **先に研究メモ末尾「11/15 公開前チェック」（10項目）を見る**（アイリスの型番・ダニ対策の円の範囲・27円/kWhの1行など、この構成案より新しい注意あり。2026-11-14 10:00 監査で追記）
- 型番の販売状況を再確認（VH700は「在庫品限り」表示だった）
- ops/make_links.py の KEYWORDS には `futon-dryer` が登録済み（34行目）→追加不要。記事に枠を置いて build → push
- 内部リンクは他の記事と同じく相対（`denkidai-calculator.html` の形）で書く。`/posts/` で始めると `/ai-lab/` の外に飛ぶ
- 単価は既存の全記事と同じ **31円/kWh**（content/posts 内50か所すべて31円/kWh・他の単価0件を 11/13 04:08 に確認）。試算8件も再計算して一致

## 楽天ボタンのキーワード下書き（11/13 16:00 自走回・提案2）
※ **11/15の制作回で記事と同時に追加**する（11/13 19:00監査で訂正：make_links.py は content/products.json に**既にある枠だけ**リンクを入れる。KEYWORDSに足すだけではボタンは作られない。check_affiliate.py の「unused keys」は products.json の枠のうち記事で使っていないものを数える）。
既存の `futon-dryer`（布団乾燥機）に加えて、見出しの分け方に合わせた2枠：
```python
    "futon-dryer-dani": "布団乾燥機 ダニ対策",
    "futon-dryer-twin": "布団乾燥機 ツインノズル",
```
- 置き場所：見出し7（まとめ）に `<!-- products: futon-dryer,futon-dryer-dani,futon-dryer-twin -->`
- 見出し4（ふとん暖め）の後に `<!-- products: futon-dryer -->` を1つ（電気毛布記事と同じ並び）
- 手順：①KEYWORDSの `"futon-dryer": "布団乾燥機",` の次の行に2行貼る ②content/products.json に枠を2つ足す `"futon-dryer-dani": {"label": "布団乾燥機 ダニ対策", "html": ""}`・`"futon-dryer-twin": {"label": "布団乾燥機 ツインノズル", "html": ""}`（これが無いと make_links.py が何もしない）③ `python3 ops/make_links.py`（「filled 2」と出ること） → `python3 ops/check_affiliate.py` → `python3 build.py` → push
- 検索語は一般名のみ（特定商品名・価格は入れない）。「ダニ対策」（パナ・日立のコース名）「ツインノズル」（アイリスの方式名）は公表値メモ ops/research/futon_dryer_specs_2026-11-12.md にある言葉。ダニ対策は効果を書かず検索語にだけ使う

## 内部リンク元（既存記事 → 新記事へのリンク）※11/14 15:00 SEO改善回で決定。公開日に足すだけ
新記事のファイル名案：`content/posts/futon-kansouki-denkidai.md`（→ `futon-kansouki-denkidai.html`。既存の `*-denkidai` に合わせた）
優先順に3本＋予備1本。どれも「布団乾燥機」で検索してきた人が次に読みたい流れの位置：
1. **neru-danbou-denkidai-calculator.md** 「## 寝る前に布団を温める「布団乾燥機」の電気代」節（113行目〜）の箇条書き最後（「実機で試した記録ではなく…」の次）に1行：
   `- 機種ごと（パナソニック・日立・アイリス）の公表値で1回・毎日の電気代を出した表は[布団乾燥機の電気代は1回いくら？](futon-kansouki-denkidai.html)にまとめています`
2. **fuyu-denkidai-matome.md** 「悩み別・どの記事を読めばいい？」表の「寝るときの暖房の電気代を比べたい」行の直後に1行：
   `| 寝る前に布団を温めたい（布団乾燥機） | [布団乾燥機の電気代（機種別・1回あたり）](futon-kansouki-denkidai.html) |`
   ※構成案どおり、新記事のまとめからもこの記事へ戻りリンク
3. **denki-moufu-kotatsu-denkidai-telework.md** 「## 電気毛布をつけっぱなしで寝たら一晩いくら？」節の箇条書き2つ目（「寝る前に布団を温めておき…」）の文末に追記：
   `寝る前に温める道具として布団乾燥機を使う場合の電気代は[布団乾燥機の電気代](futon-kansouki-denkidai.html)で計算しています。`
- 予備：fuyu-heyaboshi-joshitsuki-denkidai.md「冬の部屋干しで電気代をムダにしないコツ」末尾（見出し6「部屋干しに使う場合」を書いた時だけ）。書かなければ足さない
- 足した後：build → `python3 ops/tests/mobile_check.py` → 生成HTMLで `grep -c futon-kansouki-denkidai.html docs/posts/*.html` が4本（新記事のまとめ戻り含め）以上あるか確認
