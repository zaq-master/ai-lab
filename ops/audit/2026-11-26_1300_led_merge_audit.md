# 2026-11-26 13:00 カンサ監査：LEDイルミ記事の統合（commit 1d5d403、未push）

対象：content/posts/led-illumination-denkidai.md（今日公開済み記事を、退役した監査済み下書き ops/drafts/retired/article_led-illumination-denkidai_draft.md ベースに差し替え）＋内部リンク3本（smart-plug-guide / denkidai-calculator / fuyu-denkidai-matome）＋下書き類の retired 移動。
照合のもと：ops/audit/2026-11-25_1000_illumi_audit.md、ops/audit/2026-11-25_1300_prepublish_recheck.md（日立31円/kWh・楽天 約8W・約16W を公式で照合済み）。

## 結果（OK 13／NG 1＝軽微・修正済み）

| # | 点検項目 | 結果 | 根拠・メモ |
|---|---|---|---|
| 1 | 早見表（6時間）2/5/8/16W の 1日・25日・31日 | OK | 自分で再計算：2W 0.4/9/12、5W 0.9/23/29、8W 1.5/37/46、16W 3.0/74/92 円 → 全一致 |
| 2 | 商品例の kWh と電気代 | OK | 8W×6h×25日＝1.2kWh×31＝37.2→約37円、16W→2.4kWh×31＝74.4→約74円 |
| 3 | つけっぱなし表（24h×25日）と差・「4倍」 | OK | 2W 37（差28）、8W 149（差112）、16W 298（差224）。24/6＝4倍 |
| 4 | 結論・まとめ・description の数字（8W 約37円／約149円）、USB例 5V×0.4A＝2W | OK | 本文の表と一致 |
| 5 | 下書きにない数値・商品名・価格・体験談 | OK | 本文は下書きとほぼ同文。下書きから増えたのは旧記事由来の文3つ（W数不明時はスマートプラグの電力モニター／屋外用か確認／延長コードの容量）だけで、いずれも数値・商品名・体験談なし。旧記事の30W・60W・100W・5時間の表は削除。商品2件（NCIL3154 約8W・最大7セット/56W、scl-rl-2p10m 約16W・IP65）は11/25の照合記録と一致。価格は不掲載 |
| 6 | 単価31円/kWh の出典・支援の1行 | OK | 日立 a115（11/25 照合OK）。支援の1行は下書き（監査済み）と同文、リンク先 #shien-2027 |
| 7 | 【PR】冒頭表記・「おすすめの探し方（PR）」見出し・目次リンク #pr-osusume | OK | 本文とHTMLの両方で確認 |
| 8 | AI作成・実機レビューでない旨 | OK | 冒頭の※注記に「AI（電脳アリス）が作成」「実機レビューではありません」 |
| 9 | 下書きメモ・内部用語の残り（ops/、ペンネ、カンサ、照合、下書き、I1〜I3 等） | OK | 0件。残るコメントは `<!-- products: led-illumination,smart-plug-basic -->` 1個だけ（必要なもの） |
| 10 | 内部リンク3本の文言・位置 | OK | 退役スクリプトの I1〜I3 と一字一句同じ・同じ位置（スマートプラグ＝「向いている家電」の充電器の次、計算ツール＝Q「W数がわからない」の答えの次、冬まとめ＝悩み別表の計算ツール行の次）。文脈も自然 |
| 11 | リンク元の updated | OK | 変更なし（denkidai-calculator 11-20、smart-plug-guide 11-07、fuyu-denkidai-matome 11-21） |
| 12 | docs が最新か・商品枠 | OK | 作業用コピーで build し直しても docs の差分0。led-illumination は make_links.py の KEYWORDS と products.json に登録済み。本物で content_guard OK（37記事）・check_affiliate OK（159個） |
| 13 | 残り9本の公開スクリプト（作業用コピー sim で日付順に --allow-early） | OK | oosouji→kisei→nabe→nenga→yutanpo→samusa→reizouko→gohan→benza 全部「OK」で完走（nabe の N4 は仕様どおり飛ばし→gohan で挿入）。最後に build 46本、content_guard OK（46記事）、check_affiliate OK（176個・未使用枠0）、site_health 49ページ問題0、mobile_check 49×4画面問題0。イルミのリンク3本は各1回のまま |
| 14 | 11/30 手順書の期待値 | **NG（軽微）→修正** | イルミが前倒し公開されたため、11/30大掃除の後は「37本・162個」ではなく **38本・164個**（作業用コピーで実測、現在は37本・159個）。ops/drafts/publish_steps_2026-11-30.md に訂正行を追記。12/8以降の期待値は12/2イルミ込みで計算済みのため不変 |

参考（NGにしない）：商品例の「屋外使用可」は商品ページでは「コントローラーとコンセント部分は防雨対策が必要」付き。本文の注意点に「屋外での使用・防水は取扱説明書に従う」があり、11/25の監査済み下書きと同文なので現状維持。

## 12/2 枠が空いた件：「12/2 にイルミを実行」と書かれている計画ファイル

退役済み（ops/drafts/retired/）とログ・監査記録を除く。
- ops/drafts/publish_steps_2026-11-30.md 18行目「次の公開は 12/2 LEDイルミ」→ 今回、直下に訂正行を追加済み
- ops/meetings/prep_2026-11-30_december_slots.md 14行目（表：LEDイルミ 12/2）、28行目（11/30〜 大掃除・イルミ）、46行目（イルミだけ未登録で12/2スクリプトで追加）→ **11/30会議の資料。46行目は事実と違う（登録済み）**。会議前に更新が必要
- ops/drafts/publish_steps_2026-12-08.md 15・57行目、publish_steps_2026-12-10.md 15行目、publish_steps_2026-12-14.md 3・11行目、publish_steps_2026-12-16.md 17行目、publish_steps_2026-12-21.md 21行目、publish_steps_2026-12-23_gohan.md 3・14行目 → 試しの順番の記録（「12/2 LEDイルミ→…」）。期待値の数字自体は変わらないので実害なし
- ops/drafts/publish_gohan_2026-12-23.py 3行目、publish_yutanpo_2026-12-14.py 3行目、publish_nenga_2026-12-10.py 3行目、publish_benza_2026-12-30.py 3・26行目 → 説明コメントのみ（動作に影響なし）
- ops/drafts/article_gohan-hoon-vs-reitou_draft.md 7行目（下書きメモ、公開時に消える）
- ops/sessions/2026-11-25_1000.md 9・21行目、2026-11-25_1300.md 10・19行目、ops/decisions.md 306行目、ops/ideas.md 191行目、ops/ventures.md 13行目 → 過去の記録・経緯
- ops/backlog.md：12/2・イルミの記載なし

## 次の一手
12/2 の空き枠に何を入れるか（例：スーパーSALE記事 12/4 開始前の前倒し、または在庫の年賀状・便座の前倒し）を決め、11/30会議資料 prep_2026-11-30_december_slots.md の14・28・46行目を直す。
