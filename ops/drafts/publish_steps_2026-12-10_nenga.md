# 年賀状を家のプリンターで刷ると1枚いくら？ 記事 公開手順（2026-11-25 ペンネ 作業用コピーで案Cの順に通し確認済み）

**公開日は11/30のAI経営会議で決める**（ops/meetings/prep_2026-11-30_december_slots.md）

| 案 | 公開日 | 実行するコマンド |
|---|---|---|
| 案C（おすすめ） | **12/10（木）11:00** | `python3 ops/drafts/publish_nenga_2026-12-10.py` |
| 案B | 12/9（水）11:00 | `python3 ops/drafts/publish_nenga_2026-12-10.py --date 2026-12-09` |
| 案A | 見送り | 実行しない（12/28以降は元日に届ける目安12/27を過ぎる） |

- `--date` は 2026-12-09・2026-12-10 だけ受け付ける。記事の `date:` はスクリプトが公開日に書きかえる（下書きは 2026-12-10 のまま）

## 手順
1. `git pull --rebase`
2. 公開前の宿題（スクリプトではやらない・**必須**）：キヤノン「年賀状お役立ち機能をご紹介」のページを開き、TS8730 の**印刷面 約11.3円・宛名面 1.2円（税込）**と条件（標準容量・筆まめVer.32・写真用はがきフチなし（はみ出し量小））が同じか確認。特集名（パンくず）が「年賀状2026」のままなら下書きの「昨シーズン向けの特集…2027年向けの特集は見つからず」の文のままでよい。「年賀状2027」に変わっていたら数字・条件を照合し直し、その文と早見表を直してから実行（ops/audit/2026-11-25_1900_nenga_official_check.md の案3）。日本郵便の 12/20 受付開始・12/27 目安（よくある質問 140）も開き直す
3. 上の表のコマンドを実行。スクリプトがやること：
   - 下書き（ops/drafts/article_nenga-ink-dai_draft.md）→ content/posts/nenga-ink-dai.md。先頭の下書きメモを消し、`<!-- products: printer-ink -->` 1個だけ残す
   - 新しい商品枠：ops/make_links.py の KEYWORDS に `"printer-ink": "プリンター 年賀状",`、content/products.json に `"printer-ink": {"label": "年賀状が刷れるプリンター", "html": ""}` を足し、make_links を実行（ログイン不要）
   - 内部リンク2か所（下）
   - 止まる：公開日より前／二重実行／位置の行が無い・2か所以上／printer-ink が別のキーワードで登録済み／make_links 後もリンクが空（このときは全部元に戻す）
4. `python3 build.py` → `python3 ops/tests/content_guard.py`・`python3 ops/tests/mobile_check.py`・`python3 ops/check_affiliate.py`・`python3 ops/tests/site_health.py`
5. 確認後 commit & push（push前に `git pull --rebase`）。**ops/make_links.py と content/products.json も一緒に commit**

## 期待値（案Cの順の試し。2026-11-25）
- 12/8 帰省まで 39本・166個 → **＋この記事 40本・167個（楽天ボタン+1）**。content_guard OK・check_affiliate OK
- 案Bの 12/9 の場合も、この時点の本数・ボタン数は同じ（12/10 鍋の前に入るだけ）
- 冒頭【PR】・見出し「年賀状が刷れるプリンターの探し方 PR」・「AI（電脳アリス）が…まとめた記事」「実機レビューではありません」あり

## 内部リンク（リンク追加だけなので `updated` は変えない。他の公開スクリプトが触らない記事）
- Y1 telework-gadget-present-erabikata.md：まとめの最後の段落「デスクまわりの困りごとをまとめて見直したい場合は、…で整理しています。」の直後に空行＋1段落
- Y2 desk-qol-guide.md：最後の段落「在宅ワークをしている家族や友人に贈るものを探している場合は、…まとめています。」の直後に空行＋1段落
