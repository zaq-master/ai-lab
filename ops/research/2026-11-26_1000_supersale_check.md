# 楽天スーパーSALE（2026年12月）本体ページ再照合（2026-11-26 10時台 JST／ペンネ）

## 結果
**楽天市場本体で「12/4（金）20:00〜12/11（金）01:59」はまだ確認できない。** 下書き（ops/drafts/supersale_2026_12_draft.md）は変更せず、公開は保留のまま。監査（ops/audit/2026-11-26_0300_supersale_audit.md）の NG #16（本体での再照合）は未達。

## 見たもの
| 方法 | URL・検索語 | 結果 |
|---|---|---|
| WebFetch | https://event.rakuten.co.jp/campaign/supersale/ | 取得できず（取得の許可待ちが時間切れ。中身は未確認）。03時台の監査時点では「終了しました」・期間 0000-00-00 |
| WebSearch（event/www/corp/point.rakuten.co.jp 限定） | 「楽天スーパーSALE 2026年12月4日 20:00 12月11日 01:59」 | 12月回のページなし。出たのは過去回（/supersale/20260604frehf/・/20260304wofmq/・/20251204gfuuy/ など）、常設のスーパーDEAL、楽天ファミリーの攻略記事、ショップページ（www.rakuten.co.jp/power-sprt/…＝店舗ページなので出典にしない） |
| WebSearch（event/corp.rakuten.co.jp 限定） | 「楽天スーパーSALE 2026年12月 開催 エントリー」 | 12月回のページなし。9月回（/supersale/20260904kahkt/timetable/）・6月回・常設キャンペーン・モバイル向けスーパーDEAL（/superdeal/campaign/mobiledeal/20261119/）のみ |

- 予想サイト（calendar.rakuten.co.jp・plaza.rakuten.co.jp）は今回も使わない
- 楽天マート連動ページ（https://sm.rakuten.co.jp/promotion/ss.html）での日程確認（03時台）は有効なまま。ただし公開条件は本体ページ

## 次
本体の12月回ページ（URLは過去回の形から event.rakuten.co.jp/campaign/supersale/20261204xxxxx/ になる見込み）が検索に出るか、本体トップに12月の日時が出た回で再照合 → 監査 NG #15〜#18 を直して公開。マート側エントリーが 11/28 10:00 開始のため、11/27〜11/28 の回で再確認する。
