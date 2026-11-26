# 楽天スーパーSALE（2026年12月）本体ページ再照合（2026-11-26 13時台 JST／カンサ）

## 判定
**本体未確認（楽天公式ドメインの別ページでは確認）。**
event.rakuten.co.jp/campaign/supersale/ の下に 2026年12月回のURL（20261204… の形）は検索に出てこなかった。本体の告知文で12月回の日時が書かれたものも見つからなかった。楽天マートの連動ページ（sm.rakuten.co.jp/promotion/ss.html）は今回も検索に出たが、公開の条件は本体ページなので、下書き（ops/drafts/supersale_2026_12_draft.md）は**公開保留のまま**。監査 NG #16（本体での再照合）は未達。

※メモ：2026-12-04 は**金曜日**（指示文の例「12月4日（木）」は2025年の曜日。下書きに「木」と書かないこと）。

## 検索した語と結果（WebSearch、WebFetch は使っていない）
| # | 検索語（モード／ドメイン限定） | 結果 |
|---|---|---|
| 1 | 楽天スーパーSALE 2026年12月 開催 20:00（standard／event.rakuten.co.jp） | 12月回なし。9月回 /supersale/20260904kahkt/timetable/、3月回 /20260304wofmq/specialcoupon/、常設のスーパーDEAL、モバイル向け /superdeal/campaign/mobiledeal/20261119/、楽天ファミリーの解説記事 |
| 2 | 楽天スーパーセール 12月 2026 event.rakuten.co.jp（standard／限定なし） | 本体は9月回 /20260904kahkt/presale/ のみ。他はまとめ・予想サイト（appllio、gamepedia、goal.com など＝根拠にしない） |
| 3 | 楽天スーパーSALE 12月4日 20:00 12月11日 1:59 2026（extended／event・www・corp.rakuten.co.jp） | 12月回なし。6月回・9月回の timetable、2025年6月回、ショップページ（www.rakuten.co.jp/power-sprt/…＝店舗なので不可）、corp の過去の楽天トラベル告知（2024・2025年）、2026年6月のプレスリリース |
| 4 | event.rakuten.co.jp/campaign/supersale/20261204（standard） | 出たのは 2025年12月回 /20251204gfuuy/ 配下（bookmark・famous-shop・pointup20 等）と常設トップ /campaign/supersale/ のみ。2026年12月回のURLなし |
| 5 | 楽天 スーパーSALE 2026年12月 開催 お知らせ（standard／corp・event・sm.rakuten.co.jp） | 楽天マート連動ページ https://sm.rakuten.co.jp/promotion/ss.html?scid=wi_ich_ss（楽天公式の別ドメイン）。本体側はクリスマス特集2026・お歳暮2026などで、12月スーパーSALEの告知なし。corp に2026年の楽天トラベル スーパーSALE告知もまだ出ていない |

- 常設トップ https://event.rakuten.co.jp/campaign/supersale/ は検索結果に出たが、今の中身（12月回の日時が載っているか）は検索結果からは読めない。WebFetch は前回許可待ちで止まったため使っていない
- まとめ・予想記事（appllio・gamepedia・goal.com・plaza.rakuten.co.jp）は根拠にしていない

## 見つかった公式URL（参考）
- 楽天マート連動（12月回の日程が載っていると03時台に確認済み）：https://sm.rakuten.co.jp/promotion/ss.html
- 本体常設トップ（中身は未確認）：https://event.rakuten.co.jp/campaign/supersale/
- 過去回の形の例：https://event.rakuten.co.jp/campaign/supersale/20251204gfuuy/ ／ /20260904kahkt/

## 日時
本体での原文：**見つからず**（書けない）。

## 下書きの差し替え案
本体確認OKにならなかったので、今回は出さない（下書きは編集していない）。

## 次
11/27〜11/28 の回（マート側エントリーが 11/28 10:00 開始）で同じ検索 #4・#3 をもう一度やる。オーナーPCがつながる回なら、内蔵ブラウザで本体トップ https://event.rakuten.co.jp/campaign/supersale/ を開いて get_page_text で日時を読むのが一番早い。
