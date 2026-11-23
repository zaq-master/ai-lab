# 帰省中の留守宅チェック（スマートプラグ・スマートリモコン）下書きの照合表（2026-11-23 19:00 ペンネ）

対象：ops/drafts/article_kisei-rusu-smartplug_draft.md（公開想定 2026-12-08、content/posts には未投入）
元ネタ：ops/ideas.md「2026-11-23 09:00 リサーチ回」②
方法：WebSearch で公式URLを出す → WebFetch で本文を確認。確認日はすべて 2026-11-23。

## 機能の照合（メーカー公式ページ）

| 機種 | 項目 | 本文の書き方 | 公式ページの記載 | 結果 | URL |
|---|---|---|---|---|---|
| SwitchBot プラグミニ | 外出先からオン・オフ | ○（ハブ不要と記載） | 「ハブ不要で、外出先からでも照明器具のオン/オフが手軽にできるので、消し忘れた際にも役立ちます。」 | 一致 | https://www.switchbot.jp/products/switchbot-plug-mini |
| 同上 | 消費電力 | リアルタイム・過去分 | 「アプリで電気使用量をリアルタイムに確認できます。」「過去の消費電力も確認でき、データのエクスポートも可能です。」 | 一致 | 同上 |
| 同上 | スケジュール・タイマー | スケジュール、「○○分後にオン/オフ」 | 「スケジュールの設定ができます」「「○○分後に電源をオン/オフにする」などのタイマー設定も可能です。」 | 一致 | 同上 |
| 同上 | 定格・Wi-Fi | 1500W・15A、2.4GHzのみ | 定格電力1500W、電流15A（最大）、「2.4GHzのWi-Fiのみ対応します。」 | 一致 | 同上 |
| SwitchBot（暖房器具の注意） | 電熱器を挿さない | 原文を引用、例としてホットカーペット・電気毛布・電気ストーブ・こたつ・ファンヒーター・オイルヒーター | 「原則、熱を発する電熱器のコンセントをSwitchBotプラグミニに挿し込む行為は推奨されていません。」例：ホットカーペット、電気毛布、電気ストーブ、こたつ、各種ファンヒーター、オイルヒーター等。直後に「火災や火傷の原因となりますので…使用は控えてください。」（記事日付 2023-02-15） | 一致 | https://blog.switchbot.jp/usecase/beginners/warning-use-of-switchbot-products/ |
| 同上 | 外出時はプラグを抜く | 原文を引用 | 「就寝時や外出時はプラグをコンセントから抜く」 | 一致 | 同上 |
| TP-Link Tapo P110M | 外出先からオン・オフ | ○「いつでもどこからでも」 | 「Tapoアプリを通じて、いつでもどこからでもプラグのオン/オフを切り替えられます。」 | 一致 | https://www.tapo.com/jp/product/smart-plug/tapo-p110m/ |
| 同上 | 電力モニタリング | 使用状況を確認、電気料金を入れると月の目安 | 電力使用状況を確認でき、電気料金を設定すると毎月の電気料金の目安が分かる（リアルタイム・日別の記載は取得できず→本文に書かない） | 一致 | 同上 |
| 同上 | スケジュール・自動オフ・おでかけモード | 3つとも記載、おでかけモードは原文引用・防犯効果は判断しない | 「指定した時間帯にプラグの電源を無作為にON/OFFし、在宅しているように見せかけることができます。」自動オフ「一定時間経過後…自動的にオフ」 | 一致 | 同上 |
| 同上 | 定格・Wi-Fi | 1500W・15A、2.4GHzのみ | 最大負荷「1500W, 15A, 1/6 HP Motor」、「2.4GHz Wi-Fi Only」 | 一致 | https://www.tapo.com/jp/product/tapo-p110m-smart-plug/v1/1-pack/specs |
| SwitchBot ハブ2 | 外出先から家電操作 | ○ | 「おうちでも外出先でもスマホで家電を一括にコントロールします。」 | 一致 | https://www.switchbot.jp/collections/100p/products/switchbot-hub2 |
| 同上 | リモコン状態の確認・同期 | 外出先でリモコン状態を確認、手元リモコンと同期 | 「外出先でもスマホでエアコンのリモコン状態を確認でき、エアコンの状態をシンクロさせられます。」 | 一致（「実際に止まったか」とは別である旨は既存記事 smart-remote-guide の注意と統一） | 同上 |
| 同上 | 温湿度センサー | 付属ケーブルに搭載 | 「付属のケーブルには温度センサーと湿度センサーが搭載」 | 一致 | 同上 |
| 同上 | 通信障害時 | Bluetoothで操作（近くにいるとき） | 「ルーターやサーバーに通信障害が発生しても、スマホのBluetooth機能を使ってエアコンを操作することが可能です。」 | 一致（「近くにいるとき」はBluetoothの一般的な性質として補足） | 同上 |
| 同上 | Wi-Fi | 2.4GHzのみ | 「※本製品はWi-Fi2.4GHz帯のみ対応。」 | 一致 | 同上 |
| Nature Remo mini 2 | 外出先からエアコン操作 | ○ | 「外出先からスマートフォンでエアコンを操作したり」 | 一致 | https://shop.nature.global/products/nature-remo-mini-2 |
| 同上 | センサー・自動化 | 温度センサー、条件「GPS、曜日・時間、温度」 | センサー「温度」、自動化「GPS、曜日・時間、温度」 | 一致 | 同上 |
| 同上 | Wi-Fi | 2.4GHzのみ | 「IEEE 802.11 b/g/n(2.4GHz)」「※2.4GHzのみ対応」 | 一致 | 同上 |
| Nature Remo Lapis | 消し忘れアラート | 全員外出と判定＋設定時間超えで通知 | 家に誰もいない状態でエアコンが一定時間以上ついていると通知。位置情報で、ホームの全員が外出中と判定され設定時間を超えたらプッシュ通知。ホームロケーション設定が必要 | 一致 | https://nature.global/blog/21891/ |
| 同上 | 通知されない場合 | 原文引用 | 「Wi-Fi環境などネットワークの要因により、Nature Remoがインターネットに接続できない場合など、消し忘れアラートが適切に通知されない可能性があります。」 | 一致 | 同上 |
| 同上 | センサー・Wi-Fi | 「この記事では未確認」と表に明記 | 製品ページ未取得 | 未確認（本文で断定せず） | — |
| Nature（共通） | 障害時 | Wi-Fiやサーバーの障害で一時的に使えない可能性 | Wi-Fiやサーバーの障害で、遠隔操作や自動操作が一時的に使えなくなる可能性 | 一致 | https://nature.global/blog/24692/ |

不一致：0件。

## 開けなかったページ（本文の根拠に使っていない）
- SwitchBot サポート「SwitchBotプラグミニの安全上と使用上のご注意」https://support.switch-bot.com/hc/ja/articles/7615665255959 （client_error）
- Nature サポート「Nature Remo Lapisの消し忘れアラート機能を知りたい・設定したい」https://support.nature.global/hc/ja/articles/40480463148313 （client_error）
- Tapo P110M の暖房器具に関する注意：製品・仕様ページには記載なし → 本文は「取扱説明書で確認」とだけ書いた

## 書かなかったもの（ルール6）
- 価格・セール日程・電気代の金額（content_guard の電気代チェックに掛からない書き方）
- 防犯効果（おでかけモードはメーカーの説明の引用のみ。Q&Aで「判断していない」と明記）
- 冷蔵庫の可否（公式記載なし→取説で確認）
- 体験談・レビュー

## 既存サイトとの整合
- 暖房器具の遠隔オンは避ける：smart-plug-guide Q2・Q5、smart-remote-guide「ヒーターも外から操作していい？」と同じ方針
- 赤外線は一方通行で状態が分からないことがある：smart-remote-guide「注意点」と同じ
- 内容のかぶり回避：選び方・仕組みは既存2記事にリンクで任せ、本記事は「帰省前の5つのチェック」の順に構成

## 商品枠・内部リンクの確認
- 商品枠：`smart-plug-monitor`・`smart-remote-std`（ops/make_links.py 13・15行、content/products.json に存在。編集なし）。指示にあった「smart-plug」「smart-remote」という名前のキーは存在しない（同系統は smart-plug-basic・smart-remote-sensor も有り）
- 内部リンク（content/posts に実在）：smart-plug-guide・smart-remote-guide・fuyu-asa-aircon-timer-smart-remote・smart-remote-count-shindan・denkidai-calculator・fuyu-denkidai-matome
- **hikouki-mobile-battery は現時点で content/posts に無い**（ops/drafts のみ・11/24公開予定）→ 12/8公開時に存在を確認、無ければその1行を削除
- content_guard.py：一時コピーで実行し OK（期限の直書き0件・単価前提の漏れ0件）。コピーは削除済み

## 公開時（12/8）にやること
1. 上の公式URLを再度開き、文言が変わっていないか確認（特に SwitchBot 注意喚起記事・Nature 消し忘れアラート）
2. 逆向きの内部リンク：smart-plug-guide・smart-remote-guide のまとめ付近と hikouki-mobile-battery（公開後）の「帰省前のチェック」から1行ずつ
3. build → mobile_check.py → content_guard.py → commit & push
