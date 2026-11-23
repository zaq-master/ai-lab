# ご飯の保温 vs 冷凍レンジ 下書きの照合（2026-11-23 19:00 ペンネ）

対象：ops/drafts/article_gohan-hoon-vs-reitou_draft.md（公開想定 12/2〜12/3、content/posts には未投入）

## 数値の照合（WebSearch → WebFetch、メーカー公式ページ）

| 項目 | 下書きの値 | 公式ページの値 | 結果 | URL |
|---|---|---|---|---|
| SR-A110D 炊飯時消費電力量 | 161Wh/回（エコ炊飯） | 161Wh/回（エコ炊飯） | 一致 | https://panasonic.jp/suihan/products/SR-A110D/spec.html |
| SR-A110D 保温時消費電力量 | 20.0Wh/h | 20.0Wh/h | 一致 | 同上 |
| SR-A110D 容量・加熱方式 | 5.5合・ヒーター式 | 1.0L（1.0〜5.5合）・ヒーター式 | 一致 | 同上 |
| SR-A110D 年間消費電力量 | （本文では不使用） | 86.1kWh/年 | 一致（メモのみ） | 同上 |
| KS-HF10B 炊飯時消費電力量 | 171.3Wh/回（エコ炊飯コース） | 171.3Wh/回（エコ炊飯コース） | 一致 | https://jp.sharp/ricecooker/products/kshf10b/spec/ |
| KS-HF10B 保温時消費電力量 | 18.8Wh/h | 18.8Wh/時間 | 一致 | 同上 |
| KS-HF10B 容量 | 5.5合 | 最大1.0L（1〜5.5合） | 一致 | 同上 |
| KS-HF10B 加熱方式（IH） | 本文に書かない | ページ説明文の「IHジャー炊飯器」のみ（仕様表の項目では確認できず） | 取得できず（本文から削除のまま） | 同上 |
| NE-FL1C 消費電力（レンジ） | 1400W | 1400W | 一致 | https://panasonic.jp/range/products/NE-FL1C/spec.html |
| NE-FL1C 1000Wの継続時間 | 最大1分30秒→600Wに切換 | 最大1分30秒、自動で600Wに切換（自動メニューで働く） | 一致 | 同上 |
| 日立 MRO-S8E 冷凍ごはん | 1個（約150g）約3分 | 1個（約150g）約3分（オートメニュー「あたため4」） | 一致 | https://kadenfan.hitachi.co.jp/range/recipe/mro-s8e/s/A004.html?id=_01 |
| 電力料金目安単価 | 31円/kWh | 31円/kWh（税込、令和4年7月22日改定） | 一致 | https://www.eftc.or.jp/qa/ （Q7） |

不一致：0件。未確認の数値は本文に使っていない（アイリスオーヤマ「保温4時間」、冷凍庫の電気代、価格、味の比較は不使用のまま）。

## 計算の検算（python、31円/kWh）

| 計算 | 結果 | 本文 | 判定 |
|---|---|---|---|
| 161Wh × 31円 | 4.99円 | 約5.0円 | 一致 |
| 171.3Wh × 31円 | 5.31円 | 約5.3円 | 一致 |
| 20.0Wh/h | 0.620円 | 約0.62円 | 一致 |
| 18.8Wh/h | 0.583円 | 約0.58円 | 一致 |
| 保温2/4/6/8/12時間（20.0Wh/h） | 1.24/2.48/3.72/4.96/7.44円 | 約1.2/2.5/3.7/5.0/7.4円 | 一致 |
| 1400W×3分＝70Wh | 2.17円 | 約2.2円 | 一致 |
| レンジ2杯/3杯 | 4.34/6.51円 | 約4.3/6.5円 | 一致 |
| 分かれ目 70Wh÷20.0Wh/h | 3.5時間 | 約3.5時間（約3〜4時間） | 一致 |

## その他の確認

| 項目 | 結果 |
|---|---|
| 楽天ボタン枠 suihanki | ops/make_links.py の KEYWORDS にあり（"炊飯器 5.5合"）、content/products.json にも html 入りで登録済み → 追加不要 |
| 内部リンク denkidai-calculator | content/posts/denkidai-calculator.md 実在 |
| 内部リンク denki-kettle-vs-pot-denkidai | content/posts/denki-kettle-vs-pot-denkidai.md 実在 |
| 内部リンク fuyu-denkidai-matome | content/posts/fuyu-denkidai-matome.md 実在 |
| PR表記 | 本文冒頭に「【PR】この記事にはアフィリエイト広告（楽天市場へのリンク）が含まれます。」あり |
| 実機レビューではない明記 | あり |
| AI運営の明記 | 本文になかったため、冒頭の注意書きを「この記事はAI（電脳アリス）が作成したもので、実機で測ったレビューではありません」に修正（build.py のフッターにもAI運営表記あり） |

## 下書きに入れた修正
- date：2026-12-07 → 2026-12-02（公開日に合わせて再調整可）
- 冒頭の注意書きに「AI（電脳アリス）が作成」を追記
- 表の出典確認日：11月21日 → 11月23日
- 冒頭メモに今回の照合結果を1行追記

## 公開回でやること
ops/drafts/article_gohan-hoon-vs-reitou_draft.md を content/posts/gohan-hoon-vs-reitou-denkidai.md に移し、date を公開日に → build.py → mobile_check.py・content_guard.py → pull --rebase → push。
