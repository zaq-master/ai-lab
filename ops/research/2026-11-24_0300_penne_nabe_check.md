# 卓上IH vs カセットコンロ 下書きの照合（2026-11-24 03:00 ペンネ）

対象：ops/drafts/article_nabe-ih-vs-cassette_draft.md（12/10公開候補、content/posts には未投入）
方法：WebSearch → WebFetch でメーカー公式ページを開いて値を確認（確認日 2026-11-24）

## 数値の照合（開けたページ）

| 項目 | 公式ページの値 | 本文 | URL |
|---|---|---|---|
| アイリス 1口IHコンロ IHK-TA1／IHK-T391／IHK-T37／IHK-T35 消費電力 | 1400W（IHK-T35は「最大1400W」） | 1400W | https://www.irisohyama.co.jp/products/electrical-appliances/cooking-appliances/ih-cooking-heater/1-ih-cooking-heater/1-ih-cooking-heater-tabletop-1400 |
| 同 加熱調理（火力） | 6段階：1400W／1000W／700W／500W／200W相当／80W相当 | 早見表に使用 | 同上 |
| 同 電源 | AC100V 50/60Hz | 本文では不使用 | 同上 |
| アイリス IHコンロ鍋セット（IHKP-T39124・IHKP-T3724・IHKP-3524） | 1400W（3524は最大1400W）、同じ6段階、付属鍋 直径24cm | 本文では鍋の条件のみ使用 | https://www.irisohyama.co.jp/products/electrical-appliances/cooking-appliances/ih-cooking-heater/1-ih-cooking-heater/ih-stove-pot-set-1400w/ |
| 同 使える鍋 | 加熱調理 直径12〜24cm、対応材質：鉄・鉄鋳物・鉄ほうろう・ステンレス・多層鋼（土鍋の記載なし） | 注意点に使用 | 同上 |
| パナソニック KZ-PH34 消費電力 | 75W相当～1400W | 75W相当～1400W | https://panasonic.jp/ih/p-db/KZ-PH34_spec.html |
| 同 火力 | 加熱コース7段階（各段のW数は記載なし） | 「記載なし」と明記 | 同上 |
| アイリス カセットコンロ 省エネタイプ IGC-S1 | 最大発熱量2.9kW（2,500kcal/h）、ガス消費量 約211g/時（周囲温度20℃）、連続燃焼時間 約1時間11分（同社ボンベ・未使用品を最大火力で全て使用した実測値・気温20〜25℃）、鍋底直径15cm以上26cm未満 | 表・注意点に使用 | https://www.irisohyama.co.jp/products/tool-diy-material/tool-diy-material-other/smoke-reduction-cassette-stove/cassette-stove |
| アイリス カセットコンロ スリムタイプ IGC-E1 | 3.5kW（3,000kcal/h）、約254g/時（20℃）、約1時間（条件同じ） | 表に使用 | https://www.irisohyama.co.jp/products/tool-diy-material/tool-diy-material-other/smoke-reduction-cassette-stove/cassette-stove-slim |
| アイリス カセットボンベ IGB-250A/B 内容量 | 250g/本、ブタンガス | 250g | https://www.irisohyama.co.jp/products/tool-diy-material/tool-diy-material-other/smoke-reduction-cassette-stove/cassette-cylinder |

参考（検算）：250g÷211g/時＝約71分、250g÷254g/時＝約59分 → 公表の連続燃焼時間（約1時間11分・約1時間）と矛盾なし。カセットコンロのページ自体にはボンベのg数の記載なし（250gはボンベのページの値）。

## 開けなかった・確認できなかったもの（本文に使っていない）

| 項目 | 状況 |
|---|---|
| イワタニ カセットフー各機種（iwatani.co.jp/jpn/consumer/products/cg/stove/cb-sl-1/・cb-epr-3/・cb-bs-1/・cb-ex-2025/function/） | 取得エラー（WebFetch client_error、curl はプロキシ403）→ **未確認**、値は書いていない |
| 31円/kWh（kadenfan.hitachi.co.jp/support/rei/q_a/a115.html・eftc.or.jp/qa/） | 今回は開けず **再確認できていない**。11/23 19:00 の照合（ops/research/2026-11-23_1900_penne_gohan_check.md）で公取協Q&A「31円/kWh、税込、令和4年7月22日改定」を確認済み。出典の書き方は既存記事どおり |
| 弱火での燃焼時間、熱効率（IH・ガス） | 公表値を確認できず → 書かない |
| ボンベ・卓上IHの価格、他サイトの「1回◯円」 | 方針により書かない・引用しない |

## 計算の検算（python、31円/kWh）

| 計算 | 結果 | 本文 |
|---|---|---|
| 1400W 15分／30分／1時間 | 10.85／21.7／43.4円 | 約10.9／21.7／43.4円 |
| 1000W 同 | 7.75／15.5／31.0円 | 約7.8／15.5／31.0円 |
| 700W 同 | 5.42／10.85／21.7円 | 約5.4／10.9／21.7円 |
| 500W 同 | 3.88／7.75／15.5円 | 約3.9／7.8／15.5円 |
| 200W 同 | 1.55／3.1／6.2円 | 約1.6／3.1／6.2円 |
| 80W 同 | 0.62／1.24／2.48円 | 約0.6／1.2／2.5円 |
| 強火1400W 10分＋500W 50分 | 233.3Wh＋416.7Wh＝650Wh → 20.15円 | 約0.65kWh・約20円 |

content_guard の単価前提チェック・期限チェックを下書き単体に当てて問題0件（2026-11-24）。
