# お買い物マラソン 買いまわりポイント計算ツール 検算（2026-11-03 19:00 カルク）

対象：content/posts/rakuten-marathon-point-calculator.md（公開ページ docs/posts/rakuten-marathon-point-calculator.html）
方法（スクリプト：ops/audit/2026-11-03_1900_marathon_calc_test.js、`node <それ> docs/posts/rakuten-marathon-point-calculator.html`）：公開HTMLの `/* calc-start */〜/* calc-end */` の関数 marathonCalc をそのまま node で読み込み、境界値を検算。
条件：1ショップ1,000円（税込）以上／最大10倍／買いまわり分上限7,000P（2026年11月回 公式 https://event.rakuten.co.jp/campaign/point-up/marathon/ ・ガイド https://event.rakuten.co.jp/campaign/point-up/marathon/guide/ 確認日2026-11-03）

計算式：倍率＝min(条件を満たした店舗数, 10)。特典P＝floor(対象店舗の税抜合計×(倍率−1)/100)、上限7,000で頭打ち。税抜＝floor(税込×100/110)（8%行は/108）。

| ケース | 結果 | 判定 |
|---|---|---|
| 0店舗（空） | shops=0 rate=0 税抜=0 計算=0 表示=0 上限=false 次=1倍 | OK |
| 0店舗（999円のみ） | shops=0 rate=0 税抜=0 計算=0 表示=0 上限=false 次=1倍 | OK |
| 1店舗 ちょうど1,000円 | shops=1 rate=1 税抜=909 計算=0 表示=0 上限=false 次=2倍 | OK |
| 1店舗 999円＋1,000円 | shops=1 rate=1 税抜=909 計算=0 表示=0 上限=false 次=2倍 | OK |
| 2店舗 1,000円×2 | shops=2 rate=2 税抜=1818 計算=18 表示=18 上限=false 次=3倍 | OK |
| 3店舗 8,000/1,200/980(例) | shops=2 rate=2 税抜=8362 計算=83 表示=83 上限=false 次=3倍 | OK |
| 8%行 1,080円 | shops=2 rate=2 税抜=2000 計算=20 表示=20 上限=false 次=3倍 | OK |
| 10店舗 各11,000円（上限未満） | shops=10 rate=10 税抜=100000 計算=9000 表示=7000 上限=true 次=- | OK |
| 10店舗 税抜77,700円（上限の手前） | shops=10 rate=10 税抜=77700 計算=6993 表示=6993 上限=false 次=- | OK |
| 11店舗→10倍止まり | shops=11 rate=10 税抜=11000 計算=990 表示=990 上限=false 次=- | OK |
| 上限ちょうど 9倍分=7000 (税抜77,778) | shops=10 rate=10 税抜=77778 計算=7000 表示=7000 上限=true 次=- | OK |
| 上限超え 2店舗 税抜80万 | shops=2 rate=2 税抜=800000 計算=8000 表示=7000 上限=true 次=3倍 | OK |
| capTaxless 10店舗 | shops=10 rate=10 税抜=10000 計算=900 表示=900 上限=false 次=- | OK |

結果：13ケースすべてOK（FAIL 0）。

見つけて直した不具合：初版は税抜を `税込/1.1` で計算しており、浮動小数点の誤差で 1,100円→999円（本来1,000円）と1円少なくなり、上限ちょうど（税抜77,778円）で6,999Pになっていた。整数演算 `税込×100/110` に修正済み。

前提・限界（記事内にも明記）：
- 1,000円未満のショップの購入に特典倍率が付くかは公式ガイドで確認できなかったため、ツールでは0として計算（保守的）
- 注文ごとの端数処理は公式に記載がなく、合計に対して1回だけ切り捨て（実際と数ポイントずれる可能性）
- SPU・ショップ独自キャンペーン・クーポンは扱わない
- python3 build.py 成功、python3 ops/tests/site_health.py（--browser 含む）問題0件
