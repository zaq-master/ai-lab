# 内部リンク点検 2026-11-05（ペンネ）

数え方：content/posts/*.md の本文に書かれた「他の記事へのリンク」を、リンク元の記事数で数えた（同じ記事から複数回は1本）。build.py が自動で付ける「あわせて読みたい」は含めない。

## 記事ごとの被リンク数（前→後）

| 記事 | 前 | 後 | 追加したリンク元 |
|---|---|---|---|
| dennetsu-vest-battery-jikan-denkidai（電熱ベスト×モバイルバッテリー） | **0** | **4** | fuyu-denkidai-matome（早見表の行＋悩み3の紹介）、denki-moufu-kotatsu-denkidai-telework（作業スタイル別）、usb-c-charger-guide（まとめ）、desk-qol-guide（冬の足元が寒い） |
| monitor-light-guide | 2 | 3 | humidifier-electricity-cost-telework（まとめ） |
| desk-qol-guide | 3 | 4 | humidifier-electricity-cost-telework（まとめ） |
| usb-c-charger-guide | 3 | 4 | fuyu-denkidai-matome（電熱ベスト紹介文の中で充電器の選び方） |
| hot-carpet-denkidai | 3 | 4 | denki-moufu-kotatsu-denkidai-telework（座卓で作業する人） |
| smart-remote-guide | 7 | 8 | telework-ketsuro-taisaku-roten（湿度の記録） |
| smart-plug-guide | 11 | 11 | 追加なし（すでに十分） |
| fuyu-asa-aircon-timer-smart-remote | 4 | 4 | — |
| smart-remote-count-shindan | 4 | 4 | — |
| humidifier-electricity-cost-telework | 5 | 5 | — |
| neru-danbou-denkidai-calculator | 5 | 5 | — |
| telework-ketsuro-taisaku-roten | 5 | 5 | — |
| kashitsu-ryo-calculator | 6 | 6 | — |
| smart-remote-rental-two-aircon | 7 | 7 | — |
| aircon-danbou-denkidai-calculator | 8 | 8 | — |
| denki-moufu-kotatsu-denkidai-telework | 9 | 9 | — |
| winter-heating-shindan | 10 | 10 | — |
| foot-heater-electricity-cost | 11 | 11 | — |
| heater-denkidai-hikaku | 12 | 12 | — |
| rakuten-marathon-fuyu-kaden-list | 14 | 14 | — |
| rakuten-marathon-point-calculator | 15 | 15 | — |
| denkidai-calculator | 15 | 16 ※ | ※別担当が作成中の新記事 mobile-battery-jikan-calculator からのリンク |
| fuyu-denkidai-matome | 18 | 18 | — |

※電熱ベスト記事の「後」は自分の追加4本。点検の途中で別担当の新記事 mobile-battery-jikan-calculator（未コミット）が現れ、そこからのリンクも入ると5本になる。

結果：23記事すべてが被リンク3本以上（0本・1本の記事はなし）。

## 方針
- 内容が本当につながる場所にだけ、1文＋リンクを足した（例：電気毛布の記事の「デスクを離れて家事もする」→電熱ベスト）
- 新しい数値・価格は書いていない（電熱ベストの「約22〜26Wh」「約2円以下」は元記事の計算結果の引用）
- 新記事 mobile-battery-jikan-calculator は被リンク0本。作成した担当が公開したら、電熱ベスト記事・まとめ記事からリンクを足す

## 確認
- `python3 build.py` → built 24 posts（成功）
- `python3 ops/tests/mobile_check.py` → ページ27／画面4種／問題0件
