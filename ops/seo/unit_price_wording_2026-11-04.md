# 単価31円の出典表記：未投稿ストックの要修正一覧（2026-11-04）

## 統一した表記（content/posts/ の10記事に反映済み）
- 本文：**目安単価31円/kWh**（全国家庭電気製品公正取引協議会「新電気料金目安単価」、2022年7月現在）
- 出典行：単価の出典：全国家庭電気製品公正取引協議会が示す「新電気料金目安単価」（約31円/kWh、2022年7月現在）。メーカーの案内ページ：日立の家電品 よくあるご質問「[冷蔵庫の電気代、消費電力量の目安を教えてください。](https://kadenfan.hitachi.co.jp/support/rei/q_a/a115.html)」（2026-11-04確認）
- 根拠：日立ページ本文「1kＷhあたりの電気量目安単価は、約31円です。（2022年7月現在）」「※全国家庭電気製品公正取引協議会が「新電気料金目安単価」として示された単価…」。「税込」の記載はない（協議会サイトはこの環境から未確認）→「税込」は付けない
- 計算値は変更なし

## 未投稿ストックで直す必要がある箇所（今回は未修正・動画は再レンダーしていない）
render.py／composition.html は、直したあとに画像・動画の作り直しが必要（作り直さないなら投稿時にキャプション側で正しい表記を出す）。

| ファイル | 行 | 直す内容 |
|---|---|---|
| media/instagram/2026-11-04_denkidai/caption.md | 21 | 「税込」を外す |
| media/instagram/2026-11-04_denkidai/render.py | 43 | 「税込」を外す |
| media/instagram/2026-11-04_denkidai/render.py | 52 | 「税込」を外す |
| media/instagram/2026-11-05_kashitsu/caption.md | 34 | 「税込」を外す |
| media/instagram/2026-11-05_kashitsu/render.py | 58 | 「税込」を外す |
| media/instagram/2026-11-06_heater/caption.md | 39 | 「税込」を外す |
| media/instagram/2026-11-06_heater/render.py | 57 | 「税込」を外す |
| media/instagram/2026-11-08_heater-monthly/meta.md | 16 | 呼び名「新電力料金」→「新電気料金」／「税込」を外す |
| media/instagram/2026-11-08_heater-monthly/meta.md | 41 | 呼び名「新電力料金」→「新電気料金」／「税込」を外す |
| media/instagram/2026-11-08_heater-monthly/render.py | 56 | 呼び名「新電力料金」→「新電気料金」／「税込」を外す |
| media/instagram/2026-11-08_heater-monthly/render.py | 86 | 呼び名「新電力料金」→「新電気料金」 |
| media/instagram/2026-11-09/meta.md | 12 | 呼び名「新電力料金」→「新電気料金」／「税込」を外す |
| media/instagram/2026-11-09/meta.md | 43 | 呼び名「新電力料金」→「新電気料金」／「税込」を外す |
| media/instagram/2026-11-09/render.py | 64 | 呼び名「新電力料金」→「新電気料金」／「税込」を外す |
| media/instagram/2026-11-09/render.py | 89 | 呼び名「新電力料金」→「新電気料金」 |
| media/instagram/2026-11-10/meta.md | 12 | 呼び名「新電力料金」→「新電気料金」／「税込」を外す |
| media/instagram/2026-11-10/render.py | 58 | 「税込」を外す |
| media/instagram/2026-11-10/render.py | 59 | 呼び名「新電力料金」→「新電気料金」 |
| media/instagram/2026-11-13/render.py | 32 | 呼び名「新電力料金」→「新電気料金」／「税込」を外す |
| media/videos/2026-11-04_denkidai/meta.md | 12 | 「税込」を外す |
| media/videos/2026-11-06_heater/composition.html | 114 | 呼び名「新電力料金」→「新電気料金」 |
| media/videos/2026-11-06_heater/meta.md | 14 | 呼び名「新電力料金」→「新電気料金」 |
| media/videos/2026-11-06_heater/script.md | 13 | 呼び名「新電力料金」→「新電気料金」 |
| media/videos/2026-11-07_calculator/composition.html | 110 | 呼び名「新電力料金」→「新電気料金」 |
| media/videos/2026-11-07_calculator/meta.md | 35 | 呼び名「新電力料金」→「新電気料金」 |
| media/videos/2026-11-08_kotatsu/composition.html | 100 | 呼び名「新電力料金」→「新電気料金」 |
| media/videos/2026-11-08_kotatsu/meta.md | 20 | 呼び名「新電力料金」→「新電気料金」 |
| media/videos/2026-11-12_neru-danbou/composition.html | 118 | 呼び名「新電力料金」→「新電気料金」／「税込」を外す／日付→「2022年7月現在」 |
| media/videos/2026-11-12_neru-danbou/meta.md | 13 | 呼び名「新電力料金」→「新電気料金」／「税込」を外す／日付→「2022年7月現在」 |
| ops/drafts/ig_stock_2026-11-08.md | 36 | 呼び名「新電力料金」→「新電気料金」／「税込」を外す |
| ops/drafts/ig_stock_2026-11-09.md | 41 | 呼び名「新電力料金」→「新電気料金」／「税込」を外す |
| ops/drafts/ig_stock_2026-11-10.md | 44 | 呼び名「新電力料金」→「新電気料金」／「税込」を外す |
| ops/drafts/ig_stock_2026-11-13.md | 52 | 呼び名「新電力料金」→「新電気料金」／「税込」を外す |
| ops/drafts/ig_stock_2026-11-14.md | 58 | 呼び名「新電力料金」→「新電気料金」／「税込」を外す |
| ops/drafts/x_candidates_neru_2026-11-04.md | 10 | 呼び名「新電力料金」→「新電気料金」／「税込」を外す／日付→「2022年7月現在」 |
| ops/drafts/x_candidates_neru_2026-11-04.md | 60 | 呼び名「新電力料金」→「新電気料金」／「税込」を外す／日付→「2022年7月現在」 |
