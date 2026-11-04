# 楽天リンク枠 → 掲載ページ対応表（2026-11-03 10:15 作成。content/posts の <!-- products: --> から集計。枠を増やしたら作り直す）
もしもの管理画面（週1回オーナーログイン時）でクリック・成果を「リンク先URL（楽天の検索キーワード）」別に見て、下の表でどのページ経由かを推定する。
枠が1ページだけ＝ページが確定。複数ページの枠は按分不可（推定）。

| 枠 | 楽天検索キーワード | 掲載ページ数 | 掲載ページ |
|---|---|---|---|
| smart-plug-monitor | スマートプラグ 電力モニター | 8 | denki-moufu-kotatsu-denkidai-telework, denkidai-calculator, foot-heater-electricity-cost, fuyu-denkidai-matome, heater-denkidai-hikaku, humidifier-electricity-cost-telework, smart-plug-guide, winter-heating-shindan |
| smart-plug-basic | スマートプラグ タイマー | 1 | smart-plug-guide |
| smart-remote-std | スマートリモコン | 3 | smart-remote-count-shindan, smart-remote-guide, smart-remote-rental-two-aircon |
| smart-remote-sensor | スマートリモコン 温湿度センサー | 6 | humidifier-electricity-cost-telework, smart-remote-count-shindan, smart-remote-guide, smart-remote-rental-two-aircon, telework-ketsuro-taisaku-roten, winter-heating-shindan |
| charger-65w | USB-C 充電器 65W PD | 2 | desk-qol-guide, usb-c-charger-guide |
| charger-30w | USB-C 充電器 30W PD | 1 | usb-c-charger-guide |
| cable-c2c | USB-C ケーブル 100W 5A | 1 | usb-c-charger-guide |
| monitor-light | モニターライト | 2 | desk-qol-guide, monitor-light-guide |
| monitor-arm | モニターアーム | 1 | desk-qol-guide |
| foot-heater | 足元ヒーター デスク下 | 5 | denkidai-calculator, foot-heater-electricity-cost, fuyu-denkidai-matome, heater-denkidai-hikaku, winter-heating-shindan |
| humidifier-vaporize | 加湿器 気化式 | 2 | humidifier-electricity-cost-telework, kashitsu-ryo-calculator |
| humidifier-steam | 加湿器 スチーム式 | 2 | humidifier-electricity-cost-telework, kashitsu-ryo-calculator |
| denki-moufu | 電気毛布 ひざ掛け | 2 | denki-moufu-kotatsu-denkidai-telework, heater-denkidai-hikaku |
| thermo-hygrometer | 温湿度計 デジタル | 3 | kashitsu-ryo-calculator, telework-ketsuro-taisaku-roten, heater-denkidai-hikaku（11/3 18:00追加） |
| kotatsu-hitori | こたつ 一人用 | 1 | denki-moufu-kotatsu-denkidai-telework（11/3 12:00追加） |
| circulator | サーキュレーター | 1 | heater-denkidai-hikaku（11/3 18:00追加） |

## 期限つき文言（11/11 04:00の自走回で外す＝マラソン終了01:59の直後）
- 2026-11-04 11:00 追加：`<!-- marathon-2026-11（11/12に削除） -->` の次の1段落（マラソン期間11/4 20:00〜11/11 01:59、チェックリスト・ポイント計算ツールへのリンク）。対象9記事＝hot-carpet-denkidai, fuyu-asa-aircon-timer-smart-remote, heater-denkidai-hikaku, humidifier-electricity-cost-telework, telework-ketsuro-taisaku-roten, winter-heating-shindan, aircon-danbou-denkidai-calculator, neru-danbou-denkidai-calculator, kashitsu-ryo-calculator。`grep -l "marathon-2026-11" content/posts/*.md` で探して削除
- 既存の同趣旨の1段落（コメント目印なし）：foot-heater-electricity-cost, denki-moufu-kotatsu-denkidai-telework, smart-plug-guide（「2026年11月回のポイントアップ期間は」で検索）
- 2026-11-04 16:00 追加：トップの特集欄に期間限定バナー（build.py の `SALE`、チェックリストへ。最終表示日 2026-11-11＝11/12最初のビルドで自動的に消える。11/11 04:00の削除作業で `SALE` ごと消してもよい）。denki-moufu-kotatsu-denkidai-telework・foot-heater-electricity-cost・smart-plug-guide のマラソン文にチェックリストへのリンクを追加（期間文言つき、11/11 04:00に一緒に削除）
