# 大掃除まとめ（11/30公開予定）の公開リハーサル（2026-11-23 19:00・カルク）

## 結論
- **このまま11/30に出せる。** 日付を11/30に固定したビルドで「built 36 posts」、content_guard・check_affiliate・site_health・mobile_check の**4つとも問題0件**、内部リンク切れ**0**。
- 内部リンク6か所は、今のファイルで差し込み位置の文が**各1か所だけ**。ずれていたのは **#6（ロボット掃除機）の位置だけ**：元案の文は行の途中で、直後に「水まわりでは使わない」の文が続くため、**段落の末尾**に足す形に案を直した（ops/drafts/oosouji_internal_links_2026-11-23.md）。
- 公開回の手順書：ops/drafts/publish_steps_2026-11-30.md（貼り付けて実行できるスクリプト付き。一時コピーで2回目の実行もやり直して同じ結果を確認済み）。

## やり方
- 本体は触らず、スクラッチ（/tmp/claude-0/oosouji_reh/）に**複製（git clone）**して作業。起点 commit：b3e46d0
  - `git worktree` を使わなかった理由：build.py（145〜147行目）は履歴が浅いと自動で `git fetch --unshallow` する。worktree は本体と .git を共有するので、本体の .git が書き換わってしまう。複製なら本体に影響しない
- 日付固定：build.py に環境変数はないため、ops/audit/2026-11-23_1300_bf_switch_check.md と同じく `build.jst_now`／`build.jst_today` を 2026-11-30 11:30 に差し替えて `build.main()` を呼んだ
- 先に「何も足さずに11/30でビルド」した状態を複製の中だけでコミットし、そこからの差分で確認

## 結果
| 確認 | 結果 |
|---|---|
| ビルド | **built 36 posts**（35→36） |
| content_guard.py | OK（36記事・期限の直書き0・単価前提の漏れ0。①節の31円/kWh前提も通過） |
| check_affiliate.py | OK（ボタン161・未使用は suihanki のみ＝既知） |
| site_health.py | 公開ページ39・**問題0件**（内部リンク切れ0・title/description長さ・sitemap・feed含む） |
| mobile_check.py | 39ページ×4画面・**問題0件**（4列の早見表・表5つともスマホで切れない） |
| 下書きメモ・「公開前に確認すること」コメントの残り | HTMLに**0件**（`<!-- products -->` 3つは残す＝正しい） |
| PR表記 | 冒頭「【PR】この記事にはアフィリエイト広告…」あり・PRバッジつき商品枠3つ・「広告」5か所 |
| 楽天ボタン | **5個**（a_id=5877487）。aircon-filter-brush・mado-vacuum・kashitsuki-citric・ketsuro-wiper・ketsuro-kyusui-tape は make_links.py の KEYWORDS と content/products.json の**両方にあり・html入り** |
| 「kuensan-souji」 | **存在しない**（make_links・products.json・下書きのどこにもない）。下書きでクエン酸の枠は **kashitsuki-citric** を使っており、こちらは登録済み。追加作業なし |
| まとめ記事からの内部リンク | 12本すべてリンク先あり（下書きの8本＋逆方向のロボット掃除機1本＋関連記事欄） |
| 6記事 → まとめ記事 | 6記事とも本文リンク**各1本**（aircon-danbou-denkidai-calculator・heater-denkidai-hikaku・humidifier-electricity-cost-telework・mado-danetsu-sheet-chintai-ketsuro・telework-ketsuro-taisaku-roten・robot-cleaner-denkidai） |
| サイトマップ・トップ・RSS | 各1件掲載。OGP画像（docs/og/oosouji-kaden-oteire-matome.png）とアイキャッチSVGも生成 |

### 差し込み位置の照合（今のファイル）
| # | 記事 | 行 | 一致 |
|---|---|---|---|
| 1 | aircon-danbou-denkidai-calculator.md | 122 | 一致（箇条の末尾に「。…」） |
| 2 | heater-denkidai-hikaku.md | 153 | 一致（表の直後・空行のあと、箇条書きの前に1段落） |
| 3 | humidifier-electricity-cost-telework.md | 174 | 一致 |
| 4 | mado-danetsu-sheet-chintai-ketsuro.md | 102 | 一致 |
| 5 | telework-ketsuro-taisaku-roten.md | 141 | 一致 |
| 6 | robot-cleaner-denkidai.md | 88 | **位置を修正**：文は一致するが行の途中。段落末「…（パナソニック MC-RS1）。」の後ろに足す |

## 気づいた点（直していない・任意）
1. 冒頭の「▶ お手入れの道具（PR）へ」（#pr-osusume）の飛び先は「① エアコン」見出しの直前で、最初の商品枠はそこから約80行下。押しても商品が見えない。下書きの `<div id="pr-osusume"></div>` を `<!-- products: aircon-filter-brush -->` の直前に移せば解消（手順書の「任意」に記載）
2. 11/24に飛行機バッテリー記事が出ると、11/30のビルドは**37本**になる。手順書は「1本増える」で判定するよう書いた
3. 下書きの出典のうち確認日が11/21のまま（ダイニチ・象印・ケルヒャー・ニトムズ）は再照合していない（今回はビルド点検のみ）。公開回に時間があれば照合して確認日を更新

## 後片付け
- 本体の content/・docs/ は**変更なし**。本体で変えたのは ops/drafts/oosouji_internal_links_2026-11-23.md（#6の位置修正＋結果メモ）と、この記録・手順書の新規2ファイルだけ。commit/push なし
- 一時コピー（/tmp/claude-0/oosouji_reh/）は削除済み
