# 楽天ブラックフライデー2026 公式発表チェック（2026-11-08 03時台 JST、担当：カンサ）

## 結論
- **未発表**（楽天公式ドメインで2026年の開催日程を確認できる情報は見つからなかった）
- 前回（ops/research/rakuten_bf_check_2026-11-07_19.md、11/7 19:11）から**変化なし**
- → ops/drafts/blackfriday_2026_draft.md は**触らない**。日付・倍率はどこにも書かない

## 今回の調べ方と制約
- WebSearch（楽天ドメインに絞る）を3回：「楽天 ブラックフライデー 2026 開催」「楽天市場 ブラックフライデー エントリー 2026年11月」「楽天ブラックフライデー 2026 開催決定 お知らせ」
- **公式ページの本文は今回読めなかった**：WebFetch は許可待ちで止まり、curl は通信の中継（プロキシ）で拒否（403）された。対象：
  - https://event.rakuten.co.jp/campaign/point-up/blackfriday/
  - https://corp.rakuten.co.jp/news/update/
  - https://event.rakuten.co.jp/campaign/point-up/blackfriday/guide/
  - https://event.rakuten.co.jp/young/campaign/point2/
  - https://event.rakuten.co.jp/campaign/point-up/marathon/
- そのため今回の判断は「検索結果に2026年の公式告知ページが出てこない」ことと、前回（11/7 19時）に本文を読んだ結果に基づく

## 検索で出た楽天公式ドメインのページ（タイトルのみ確認）
| URL | 検索結果のタイトル | 扱い |
|---|---|---|
| https://event.rakuten.co.jp/campaign/point-up/blackfriday/guide/ | 【楽天市場】ガイドトップ│BLACK FRIDAYガイド | 年の記載なし。本文未確認 → 発表とは扱わない |
| https://event.rakuten.co.jp/young/campaign/point2/ | 【楽天市場】楽天学割｜楽天ブラックフライデー ポイント2倍キャンペーン | 前回確認時は2025年分の内容。本文未確認 → 発表とは扱わない |
| https://event.rakuten.co.jp/auto/mycar/program/blackfriday/ | 【楽天市場】マイカー割×ブラックフライデー｜…ポイント3倍 | 年・期間不明。本文未確認 → 発表とは扱わない |
| https://event.rakuten.co.jp/mc/dyson/blackfriday202511/ | 【楽天市場】Dyson ブラックフライデー… | URLが「202511」＝2025年分 |
| https://event.rakuten.co.jp/campaign/point-up/blackfriday/20241121qnvfu/over50off/ | 【楽天市場】ブラックフライデー│24時間限定！50％以上割引SALE | URLが「20241121」＝2024年分 |
| https://event.rakuten.co.jp/xmas/special/point/ | 【楽天市場】クリスマス特集2026｜エントリー＆対象ショップ買いまわりで最大30,000ポイント当たる！ | ブラックフライデーではない（参考：2026年のクリスマス特集ページはある。中身・期間は未確認） |
| https://event.rakuten.co.jp/campaign/point-up/marathon/ | 【楽天市場】お買い物マラソン│買えば買うほどポイントアップ！ | 11月マラソン（期間は前回確認：11/4 20:00〜11/11 01:59） |
| https://www.rakuten.co.jp/kurouto-shop/contents/black_friday-cp/ | 楽天市場 | 出店ショップのページ。楽天の公式発表ではない |

## 不採用（事実として扱わない）
- calendar.rakuten.co.jp（楽天カレンダー）：ユーザー投稿の「開催予想日程」
  - https://calendar.rakuten.co.jp/evt?ct=2&eid=593527 ほか
- plaza.rakuten.co.jp（楽天ブログ）：個人ブログの予想・攻略記事
  - https://plaza.rakuten.co.jp/raku10p/diary/202611020000/ ／ https://plaza.rakuten.co.jp/rocca1/diary/201911160000/ ほか
- いずれも楽天のドメインだが、楽天の公式発表ではないため除外

## 次の確認
- 公式ページの本文が読めるのは、オーナーPCの内蔵ブラウザ（PC回）か、WebFetchの許可が出た回。次は**11/11 01:59のマラソン終了前後**に https://event.rakuten.co.jp/campaign/point-up/blackfriday/ を確認（2025年はエントリー開始11/12＝前回の公式ページ記載。今年も同じ流れかは**推測**）
