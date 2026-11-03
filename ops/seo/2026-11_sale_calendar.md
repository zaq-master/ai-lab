# 楽天 11〜12月 大型セール日程と、セール前の更新案（2026-11-03 13:00 カンサ調べ）

確認方法：WebSearch／WebFetch で楽天の公式ページ（corp.rakuten.co.jp・event.rakuten.co.jp）だけを確認。2026-11-03時点。
※WebFetchは要約経由の読み取りのため、記事に日付を書く前に PC回で公式ページを目視で再確認すること。

## 2026年（今年）
| イベント | 状態 | 日時 | 出典 |
|---|---|---|---|
| 楽天お買い物マラソン（11月） | **公式ページに掲載あり** | エントリー 11/2(月)10:00〜／ポイントアップ期間 **11/4(水)20:00〜11/11(水)01:59** | https://event.rakuten.co.jp/campaign/point-up/marathon/ |
| 楽天ブラックフライデー | **未発表** | 公式ページは「終了しました／来年の開催もおたのしみに」のまま（2025年分の表示）。2026年の告知はなし | https://event.rakuten.co.jp/campaign/point-up/blackfriday/ |
| 楽天お買い物マラソン（12月） | **未発表** | 公式発表を確認できず | — |
| 楽天スーパーSALE（12月） | **未発表** | 公式ページは「終了しました」、開催期間はプレースホルダー（0000-00-00）のまま | https://event.rakuten.co.jp/campaign/supersale/ |

参考：公式「ジャンル祭」（新しいセールイベント）のお知らせ 2026-10-02 https://corp.rakuten.co.jp/news/update/2026/1002_01.html （11〜12月の開催日は未確認）

## 過去の公式実績（参考。2026年の日付として書かないこと）
| 年 | イベント | 日時 | 出典 |
|---|---|---|---|
| 2025 | ブラックフライデー（楽天市場） | **11/20(木)20:00〜11/27(木)01:59**（エントリー開始 11/12(水)10:00） | https://corp.rakuten.co.jp/news/update/2025/1112_01.html |
| 2024 | ブラックフライデー（楽天市場） | **11/21(木)20:00〜11/27(水)01:59** | https://corp.rakuten.co.jp/news/update/2024/1121_02.html （同年 1118_01 もあり） |
| 2019〜2023 | ブラックフライデー | 2023: 11/21〜27／2022: 11/22〜27／2021: 11/18〜23／2020: 11/19〜24／2019: 11/28〜30（時刻なし） | 楽天市場公式コラム https://event.rakuten.co.jp/family/story/article/2023/rakuten-black-friday/ ※同コラムは2024年を「11/20」としており、プレスの11/21と食い違う→プレスを優先 |
| 2025 | 楽天スーパーSALE（12月） | 公式特集ページのメタ情報：2025-11-28 10:00〜**2025-12-11 01:59**（予告・エントリー期間を含む値と思われる。セール本体の開始時刻は公式本文で確認できず） | https://event.rakuten.co.jp/campaign/supersale/20251204gfuuy/special/live/ |
| 2025 | （別イベント）楽天トラベル スーパーSALE | 12/4(木)20:00〜12/20(土)23:59 | https://corp.rakuten.co.jp/news/update/2025/1128_03.html |
| 2024 | 楽天スーパーSALE（12月） | 公式ページで日時を確認できず（楽天トラベル側は 12/4(水)〜 https://corp.rakuten.co.jp/news/update/2024/1202_02.html ） | — |
| 2024・2025 | お買い物マラソン（12月） | 公式ページで日時を確認できず | — |

読み取れる傾向（推定・未確定）：ブラックフライデーは過去6年すべて11月第3〜4週（18日〜28日の範囲）。12月スーパーSALEは月初〜11日ごろ。→ 2026年は **11/17までに準備完了** を目標にし、日付は公式発表を見てから書く。

## 結論：記事を出すべきか
- **出す。ただし新規記事ではなく既存ページの強化で**（ideas.md 2026-11-03 案3と同じ方針）。
- 一番近い確定イベントは **明日 11/4(水)20:00 開始のお買い物マラソン**。ここに間に合う作業を優先。
- 日付入りの「セール記事」は、公式発表（BF・12月SS）を確認した回で1行追記するだけにする。推定日付は書かない。

## 冬家電と結びつく既存の商品枠
| 枠（products.json） | 置いてあるページ | セールとの相性 |
|---|---|---|
| kotatsu-hitori（こたつ 一人用） | denki-moufu-kotatsu-denkidai-telework | 季節の大物。11:00で早見表を拡充済み |
| denki-moufu（電気毛布 ひざ掛け） | denki-moufu-kotatsu-denkidai-telework, heater-denkidai-hikaku | 冬の定番 |
| foot-heater（足元ヒーター） | denkidai-calculator, foot-heater-electricity-cost, fuyu-denkidai-matome, heater-denkidai-hikaku, winter-heating-shindan | 枠数が最多＝露出が一番多い |
| humidifier-vaporize / humidifier-steam | humidifier-electricity-cost-telework, kashitsu-ryo-calculator | 乾燥シーズン |
| thermo-hygrometer（温湿度計） | kashitsu-ryo-calculator, telework-ketsuro-taisaku-roten | 低単価の小物＝買いまわりのついで買い向き |
| smart-plug-monitor / smart-remote-sensor | 多数 | 冬の電気代対策の小物 |
| **セラミックヒーター** | **枠なし**（heater-denkidai-hikaku のタイトルに「セラミックヒーター」があるのに枠がない） | 空白 |
| ハブ fuyu-denkidai-matome | foot-heater, smart-plug-monitor の2枠のみ | こたつ・電気毛布・加湿器・温湿度計の枠がない |

## セール前日に更新すると売上に近いこと（3つ）
1. **ハブ（fuyu-denkidai-matome）に「セール前チェックリスト」節＋冬家電の枠をまとめて置く**（11/4 20:00 のマラソン開始前＝今日中が理想）。中身は「W数を確認→計算ツールで月額→候補を楽天で探す」の3手順と、既存枠 kotatsu-hitori・denki-moufu・humidifier-vaporize・thermo-hygrometer を追加。日付は「公式ページで確認してください」＋上の公式URLのみ。SNS・noteの入口がこのハブに統一済みなので、流入が一番集まる場所に枠を足すのが最短。
2. **heater-denkidai-hikaku にセラミックヒーター枠を新設し、kotatsu-hitori も追加**。タイトルで「セラミックヒーター・こたつ」を名乗っているのに該当枠がない＝検索流入の購買意図を取りこぼしている。make_links.py の KEYWORDS に「セラミックヒーター」を1行追加→build。スペック・価格は書かない（PR表記は自動で付く）。
3. **温湿度計・スマートプラグなど低単価の小物を「買いまわりのついでに」導線として、加湿量ツールと結露記事の枠の直前に1行案内を足す**。お買い物マラソンはショップ数でポイント倍率が上がる仕組み（公式の説明ページ https://event.rakuten.co.jp/campaign/point-up/marathon/ ）なので、大物（こたつ・加湿器）と一緒に買われやすい小物の枠を目立たせる。「◯倍」等の倍率や価格は書かない（変わるため・事実確認できないため）。

あわせて：BF・12月SSの公式発表をチェックする作業を backlog に入れる（09:00リサーチ回で週2回、corp.rakuten.co.jp/news/update/2026/ と上の公式ページを確認）。
