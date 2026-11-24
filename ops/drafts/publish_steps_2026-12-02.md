# 12/2（水）11:00 ご飯の保温vs冷凍記事 公開手順（2026-11-24 カルク 試しで通し確認済み）

> **【2026-11-25 03:00 追加】`python3 ops/drafts/publish_gohan_2026-12-02.py` は日本時間の今日が 12/2 より前なら何も書かずに止まる**（早すぎる公開の防止。試しのときだけ `--allow-early`）

1. `git pull --rebase`
2. 下書きを移す：ops/drafts/article_gohan-hoon-vs-reitou_draft.md → content/posts/gohan-hoon-vs-reitou-denkidai.md（date は 2026-12-02 のままでよい）
3. **消すのは先頭の `<!-- 下書きメモ…-->` 1つだけ**（7〜19行目。この下書きに「公開前に確認すること」メモは無い）
   - ⚠️ `<!-- products: suihanki -->`（68行目）は**絶対に消さない**（楽天ボタンの目印）
   - 例：`re.sub(r'<!-- (下書きメモ|公開前に確認).*?-->\n?', '', s, flags=re.S)` → 残るコメント**1個**（products: suihanki）
4. KEYWORDS の追加は**不要**：`suihanki`（"炊飯器 5.5合"）は ops/make_links.py の KEYWORDS と content/products.json の両方に登録済み・リンク入り（11/24確認）。make_links の実行もいらない
5. `python3 build.py` → `python3 ops/tests/content_guard.py`・`python3 ops/tests/mobile_check.py`・`python3 ops/check_affiliate.py`（時間があれば `python3 ops/tests/site_health.py`）
6. 期待値（12/2 11:30 に時計をずらした試し。11/30の大掃除まとめ＋11/24の飛行機記事が入った状態）：
   - 記事 36→**38本**（大掃除まとめ＋この記事）・公開ページ41
   - content_guard OK／mobile_check 41ページ×4画面 問題0件／site_health 問題0件／check_affiliate OK（未使用の枠 0）
   - 楽天ボタン 157→**163**（大掃除まとめで+5、この記事で+1）
     - 注：11/30手順書の「156→161」は飛行機記事の前の数字。飛行機記事にボタンが1個あるため、今は**157→162**が11/30の正しい期待値
   - PR表記（冒頭の【PR】行）・AI運営の明記（「AI（電脳アリス）が作成」＋全記事共通の注意書き）あり
   - サイトマップ・トップ・RSS に各1件、アイキャッチSVG・OGP画像あり
   - 表2つ（機種比較・早見表）は崩れなし。文中リンク3本（denkidai-calculator・denki-kettle-vs-pot-denkidai・fuyu-denkidai-matome）の先あり
   - 目次の飛び先：この記事には `#pr-osusume` などのページ内リンクは無い（確認不要）
   - HTMLに下書きメモの文字（下書きメモ・ペンネ・カンサ・照合・2026-11-2x）**0件**
7. 同時に内部リンク（下の3か所）。**リンク追加だけなので `updated` は変えない**。行番号は11/24時点。ずれていたら「位置の行」の文で検索（3か所とも各記事に1回だけ＝ `grep -cFx` で1を確認済み）
8. 確認後 commit & push（push前に `git pull --rebase`）

## 内部リンクの差し込み位置案（試しのコピーで3か所とも適用→ビルド・4つのチェック問題0・リンク先ありを確認済み）

### G1. fuyu-denkidai-matome.md（冬の電気代まとめ）76行目の表の行の**直後**に1行
位置の行：`| 在宅でお湯を何度も沸かす（ケトルとポット） | [電気ケトルと電気ポットの電気代はどっちが安い？](denki-kettle-vs-pot-denkidai.html) |`
```
| 余ったご飯を保温するか冷凍するか迷う | [ご飯の保温と冷凍→レンジ温め、電気代はどっち？](gohan-hoon-vs-reitou-denkidai.html) |
```

### G2. denki-kettle-vs-pot-denkidai.md（ケトルとポット）「## 関連記事」の最後の箇条（121行目）の**直後**に1行
位置の行：`- 湯たんぽのお湯を沸かす分も含めて一晩の暖房を比べるなら → [寝るときの暖房 一晩の電気代くらべ](neru-danbou-denkidai-calculator.html)`
```
- 炊飯器の「保温」と冷凍ご飯のレンジ温めを比べるなら → [ご飯の保温と冷凍、電気代はどっち？](gohan-hoon-vs-reitou-denkidai.html)
```
※すぐ下のBFの段落（`<!-- blackfriday-2026-11 …-->`）は11/25以降ビルドで自動的に出なくなる。手で消してあっても位置の行は同じ

### G3. denkidai-calculator.md（電気代計算ツール）120行目の「👉 …ケトルとポット…」の**直後**に空行＋1段落
位置の行：`👉 メーカー公表値（象印・タイガー）で1杯・1日・1ヶ月を計算した比較は → [電気ケトルと電気ポット、電気代はどっち？](denki-kettle-vs-pot-denkidai.html)`
```

👉 炊飯器の保温（1時間あたりのWh）と冷凍ご飯のレンジ温めを、何時間から冷凍が得かで比べた計算は → [ご飯の保温と冷凍→レンジ、電気代はどっち？](gohan-hoon-vs-reitou-denkidai.html)
```
（リンク文には金額・時間の数字を入れていない＝元記事の数字が変わってもずれない）

## 下書きで見つけた点
- **不具合（リンク切れ・表の崩れ・メモの消し残し）：0件**。表と本文の金額をすべて31円/kWhで再計算し、すべて本文の数字と一致（直していない）
- 任意：本文の出典が「各社の製品仕様ページ（2026年11月23日確認）」の1行だけで、URLは下書きメモ（消す部分）にしか無い。公開時に残したいなら、メモ11〜14行目のURL（日立は11/23に開いた `kadenfan.hitachi.co.jp/range/recipe/mro-s8e/s/A004.html`）を記事末に「### 出典」として足す。数字は変えない
- 未確認のまま：KS-HF10Bの加熱方式（IHか）、アイリスオーヤマの「保温4時間が目安」。どちらも本文に入っていないので公開に影響なし
