# 寒さでスマホの電池が減る記事：12/16公開の準備（2026-11-25 03:00 ペンネ）

成果物：
- 公開スクリプト ops/drafts/publish_samusa_2026-12-16.py（作りは帰省スクリプトと同じ：二重実行・date・コメント数・PR/AI表記・商品枠・位置の行を全部確かめてから書く／失敗したら全部元に戻す）
- 手順書 ops/drafts/publish_steps_2026-12-16.md
- 下書き修正 ops/drafts/article_smartphone-samusa-battery_draft.md：date 2026-12-XX→**2026-12-16**／先頭コメントを「<!-- 下書きメモ」で始まる形に（スクリプトで自動削除）／「AIが作成」→「AI（電脳アリス）が作成」／出典の確認日に「Apple・Googleは11月25日にも再確認」を追記

## 出典の再照合（11/25、WebSearch→WebFetch）
| 出典 | 11/25の結果 | 判定 |
|---|---|---|
| Apple ja-jp/118431 | 日本語ページは取得許可が時間切れで開けず。英語版 support.apple.com/118431 を取得：0〜35℃、保管 -20〜45℃、低温で "temporarily shorten battery life and could cause your device to turn off"、温度が戻れば戻る、"might not charge or could stop charging"、駐車中の車内 | 内容一致（日本語の文言は11/24照合のまま） |
| Pixel 温度を確認する 15679416?hl=ja | 「0°C / 32°F を下回ると、突然シャットダウン」「冷たい外気…エアコンの吹き出し口」「徐々に温める」 | 一致 |
| Pixel バッテリーについて 15738128 | 英語表示で取得："shorter battery runtime or a decreased ability to deliver power in extreme temperatures" | 内容一致（日本語の文言は11/24照合のまま） |
| Pixel 9a 安全ガイド 15475035 | 英語版（product-documentation）："works best in ambient temperatures between … (0° and 35° C)"、保管 "-20° and 45° C"。日本語指定はヘブライ語で表示された | 一致 |
| シャープ SH-M26 取扱説明書PDF | WebFetch は許可時間切れ、curl は通信制限（403）で取得できず | **11/25未確認**（11/24の照合を使用。手順書5に公開前の宿題として記載） |

本文の数値・引用は変更なし（全部、11/24か11/25の公式原文で確認済み）。Xperia・体験談・「◯％減る」等は引き続き書かない。

## 楽天ボタン
- 既存の `mobile-battery-10000`（モバイルバッテリー 10000mAh PSE）1つだけ。KEYWORDS・products.json 登録済み・リンク入り → make_links 不要
- 新しい枠の案（メモだけ。本番の make_links.py は変更していない）：`"smartphone-glove": "スマホ対応 手袋"`。寒い屋外でスマホを出す場面に合うが、記事本文に手袋の話がないため今回は入れない。入れるなら本文に「（本サイトの提案）」の1段落と一緒に

## 内部リンク（原文の行で確認、3か所）
S1 mobile-battery-jikan-calculator.md 130行目／S2 hikouki-mobile-battery.md 84行目／S3 usb-c-charger-guide.md 156行目（Q8）。文言は手順書に。
- 衝突確認：大掃除・ご飯・帰省・鍋（12/10）・湯たんぽ（12/14）のスクリプトの差し込み先と行が重ならない。飛行機記事は帰省K3（95行目の表）と同じファイルだが別の行で、両方入ることを確認
- 電熱ベスト記事（dennetsu-vest）にも合う行（68行目「寒い屋外や強モードでは…」）があるが、暖房系の担当と重なる可能性があるため使わなかった

## 試し（作業用コピー、時計を各日11:30 JSTにずらしてビルド）
| 段階 | 記事 | 楽天ボタン | 公開ページ | content_guard／check_affiliate／site_health |
|---|---|---|---|---|
| 今（11/30の時計） | 36 | 157 | 39 | OK／OK／0件 |
| ＋大掃除 11/30 | 37 | 162 | 40 | OK／OK／0件 |
| ＋ご飯 12/2 | 38 | 163 | 41 | OK／OK／0件 |
| ＋帰省 12/8 | 39 | 165 | 42 | OK／OK／0件 |
| ＋この記事 12/16 | **40** | **166** | 43 | OK／OK／0件、mobile_check 43ページ×4画面 **問題0** |
| （別試し）鍋・湯たんぽも入れた全部入り | 42 | 171 | 45 | OK／OK／0件、mobile_check 問題2件＝**湯たんぽ記事の表2つが iPhone13 幅で列が隠れる**（この記事とは無関係。湯たんぽ担当へ要連絡） |
- 生成HTML：下書きの文字0件、サイトマップ・トップ・RSS各1件、アイキャッチSVG・OGP画像あり、リンク先すべて実在
- 二重実行：「止めた：記事はもう content/posts にあります」で終了コード1
- date 違い：「止めた：下書きの date が 2026-12-16 ではない」で終了コード1
- 書き込み途中の失敗（2回目の書き込みでわざとエラー）：全部元に戻り、content/ のハッシュ一致
- 本番の content/・docs/ は変更なし。commit/push はしていない
