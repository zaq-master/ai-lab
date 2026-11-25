# トイレの便座（温水洗浄便座）冬の電気代 記事 公開手順（2026-11-25 ペンネ 作業用コピーで案Cの順に通し確認済み）

**公開日は11/30のAI経営会議で決める**（ops/meetings/prep_2026-11-30_december_slots.md）

| 案 | 公開日 | 実行するコマンド |
|---|---|---|
| 案C（おすすめ） | **12/30（水）11:00** | `python3 ops/drafts/publish_benza_2026-12-30.py` |
| 案A・案B | 12/28（月）11:00 | `python3 ops/drafts/publish_benza_2026-12-30.py --date 2026-12-28` |

- `--date` は 2026-12-28・2026-12-30 だけ受け付ける。記事の `date:` はスクリプトが公開日に書きかえる（下書きは 2026-12-30 のまま）
- 案Cでは 12/28 に鍋（`ops/drafts/nabe_move_to_2026-12-28.patch` を当てたあとの publish_nabe_2026-12-28.py）が先に出る

## 手順
1. `git pull --rebase`
2. 公開前の宿題（スクリプトではやらない）：資源エネルギー庁「無理のない省エネ節約（風呂・トイレ）」を開き、貯湯式の年間 **34.90／26.40／13.80kWh** が同じか確認（違えば下書きの数字と表を直してから実行）
3. 上の表のコマンドを実行。スクリプトがやること：
   - 下書き（ops/drafts/article_benza-denkidai_draft.md）→ content/posts/benza-denkidai.md。front matter の**前**にある下書きメモを消し、先頭を `---` にする。`<!-- products: benza-cover -->` 1個だけ残す
   - 新しい商品枠：ops/make_links.py の KEYWORDS に `"benza-cover": "便座カバー 洗える",`、content/products.json に `"benza-cover": {"label": "洗える便座カバー", "html": ""}` を足し、make_links を実行（ログイン不要）
   - 内部リンク3か所（下）
   - 止まる：公開日より前／二重実行／位置の行が無い・2か所以上／benza-cover が別のキーワードで登録済み／make_links 後もリンクが空（このときは全部元に戻す）
4. `python3 build.py` → `python3 ops/tests/content_guard.py`・`python3 ops/tests/mobile_check.py`・`python3 ops/check_affiliate.py`・`python3 ops/tests/site_health.py`
5. 確認後 commit & push（push前に `git pull --rebase`）。**ops/make_links.py と content/products.json も一緒に commit**

## 期待値（案Cの順の試し。2026-11-25）
- 12/28 鍋まで 45本・175個 → **＋この記事 46本・176個（楽天ボタン+1）**。content_guard OK・check_affiliate OK（未使用の枠0）・site_health 公開49ページ 問題0・mobile_check 49ページ×4画面 問題0
- 案A・Bの12/28の場合は、鍋が12/10に出ているので本数・ボタン数は同じ（46本・176個。年賀状を見送る案Aなら 45本・175個）※案A・Bの順は通しで試していない（数は足し算）

## 内部リンク（リンク追加だけなので `updated` は変えない。他の公開スクリプトの位置の行と重ならない）
- B1 fuyu-denkidai-matome.md：悩み別の早見表「| 部屋が乾燥する | …加湿量 計算ツール… |」の行の直後に1行
- B2 denkidai-calculator.md：「## 関連記事」の「- ホットカーペットを畳数・強弱別に見るなら → …」の直後に1行
- B3 heater-denkidai-hikaku.md：「## 関連ツール・記事」の「- 電力を見える化するなら → [スマートプラグの選び方](smart-plug-guide.html)」の直後に1行
