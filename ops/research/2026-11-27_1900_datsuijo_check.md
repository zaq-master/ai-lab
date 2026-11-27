# 脱衣所ヒーター下書き TODO照合記録（2026-11-27 19:00、ペンネ）

対象：ops/drafts/datsuijo_heater_draft_2026-11-27.md の TODO 4件（eftc単価／DS-FZS1200 弱W数／YKT-S640GM 公式ページ／取説の設置条件）
方法：WebSearch（standard）→ WebFetch。検索結果に出たURLは開けたが、検索に出ないURL（eftc Q&A、パナソニック仕様ページ、アイリスの取説PDF）は取得の許可待ちが時間切れになり開けなかった。
結論：**4件とも確認済みにはできず、TODOは残した**（理由を下書きに追記）。下書きの数値は1つも変えていない。

## 1) eftc 目安単価 31円/kWh・令和4年7月改定
| URL | ページの記載 | 下書きの値 | 判定 |
|---|---|---|---|
| https://www.eftc.or.jp/qa/ | （取得の許可待ちが時間切れで開けず） | 31円/kWh（税込、令和4年7月改定） | 取得できず |
| https://eftc.or.jp/news/pamphlet_pdf/pamphlet1_r0807.pdf | 協議会の紹介のみ。目安単価の記載なし | 同上 | 取得できず（該当記載なし） |
| https://www.eftc.or.jp/news/pamphlet_pdf/pamphlet1_r0705.pdf | 協議会の紹介のみ。目安単価の記載なし | 同上 | 取得できず（該当記載なし） |
| https://www.eftc.or.jp/news/pdf/news165.pdf | 発行日 令和4（2022）年1月5日。目安単価の記載なし | 同上 | 取得できず（該当記載なし） |

## 2) パナソニック DS-FZS1200 弱のW数
| URL | ページの記載 | 下書きの値 | 判定 |
|---|---|---|---|
| https://panasonic.jp/danbo/products/DS-FZS1200/spec.html | （取得の許可待ちが時間切れで開けず） | 強1,170W／弱は未掲載 | 取得できず |
| https://panasonic.jp/danbo/p-db/DS-FZS1200.html | 特長の概要のみ。消費電力の記載なし | 同上 | 取得できず（該当記載なし） |
| https://panasonic.jp/danbo/products/DS-FZS1200.html | 消費電力の記載なし | 同上 | 取得できず（該当記載なし） |
| https://panasonic.jp/danbo/products/DS-FZS1200/feature.html | 「弱」運転の消費電力の記載なし。試験条件は「温風運転「強」、ナノイーX運転。」 | 同上 | 取得できず（弱の記載なし） |
| https://panasonic.jp/catalog/ctlg/danbo/danbo.pdf | 「2025年8月現在」。スリムタイプ欄に「1170 W 温風（「強」運転時）」「1150 W 温風（「強」運転時）」「1170 W／1130 W」があるが、抽出テキストで型番との対応が読めず。弱の値は型番に紐づけて読めない | 同上 | 取得できず（対応が読めない） |

→ 弱の行は追加していない（本文の「弱のW数は記載がなかったため載せていません」の注記のまま）。

## 3) ユアサプライムス YKT-S640GM 公式製品ページ
| URL | ページの記載 | 下書きの値 | 判定 |
|---|---|---|---|
| （公式製品ページ） | 検索2回（型番単独／型番＋640W 400W）で見つからず | — | 取得できず |
| https://newscast.jp/smart/news/2862060 | 消費電力（50Hz/60Hz）強：640W、弱：400W。発表 2025-10-14、ユアサプライムス株式会社。専用の製品ページURLの記載なし（会社サイト https://www.yuasa-p.com 等のみ）。使用場所は「高い位置にコンセントがありがちな脱衣所のほか、トイレ等のパーソナル空間、デスクの上やキッチン等の少し離れたコンセントから電源がとれます」 | 強640W／弱400W | 一致（ただしプレスリリース転載。公式製品ページではない） |

→ 出典表記は「メーカーのプレスリリース（2025年10月発表）」のまま。

## 4) 取扱説明書の設置条件（脱衣所・水がかかる場所）
| 機種 | URL | ページの記載 | 判定 |
|---|---|---|---|
| アイリス JCH-127D-W | https://www.irisohyama.co.jp/products/support/4967576550710 → 取説 https://www.irisohyama.co.jp/products/manual/pdf/288678.pdf | サポートページで品番と取説URLは確認。PDFは許可待ちの時間切れで開けず | 取得できず |
| アイリス ACH-EM12C-C | https://www.irisohyama.co.jp/products/support/4967576702249 → 取説 .../manual/pdf/202474.pdf | 同上 | 取得できず |
| アイリス ACH-LWSW12A-W | https://www.irisohyama.co.jp/products/support/4967576705356 → 取説 .../manual/pdf/202781.pdf | 同上 | 取得できず |
| アイリス ACH-E12C-W | https://www.irisohyama.co.jp/products/support/4967576702294 → 取説 .../manual/pdf/202479.pdf | 同上 | 取得できず |
| パナソニック DS-FZS1200 | — | 公式の取説PDFは見つからず（検索に出た panasonic.jp の取説 1428433791232.pdf は DS-FWX1200 用） | 取得できず |
| ユアサ YKT-S640GM | — | 取説は見つからず。プレスリリースに浴室・水がかかる場所の記載なし | 取得できず |

参考（表に載っていない機種なので本文には使わない）：
- アイリス JCHM-12TD3／JCHM2-12TD3／JCH-12TD3／JCH-12DD3 取説 https://www.irisohyama.co.jp/products/manual/pdf/274266.pdf ：「水まわり、風呂場など湿気の多い場所では絶対に使用しない」「水につけたり、水をかけたりしない」
- パナソニック DS-FWX1200 取説 https://panasonic.jp/p-db/contents/manualdl/1428433791232.pdf ：「温室・浴室など」「高温・多湿・水のかかる」「場所では使わない」

→ 本文の「設置場所の条件は必ず取扱説明書で確認」の一般的な注意のまま。

## 次に開けば片づくURL（許可が通る回で）
- https://www.eftc.or.jp/qa/
- https://panasonic.jp/danbo/products/DS-FZS1200/spec.html
- https://www.irisohyama.co.jp/products/manual/pdf/288678.pdf ／ 202474.pdf ／ 202781.pdf ／ 202479.pdf
