# 11/24（火）飛行機のモバイルバッテリー記事の公開手順（11/23 05:06 自走回で試し公開して確認済み）
1. `git pull --rebase`
2. ops/drafts/article_hikouki-mobile-battery_draft.md の冒頭 `<!-- 下書きメモ … -->` を**丸ごと削除**して content/posts/hikouki-mobile-battery.md に置く（date: 2026-11-24 はそのままでよい）
3. `python3 build.py` → 「built 36 posts」になること
4. `python3 ops/tests/content_guard.py`（OK・36記事）／`python3 ops/tests/mobile_check.py`（問題0件）
5. 確認（05:06の試しで全部OK）：HTMLに「下書きメモ」0件／PRバッジあり／商品枠 mobile-battery-10000（もしもリンク1件）／サイトマップ・トップに掲載／内部リンク6本（暖房・電熱ベスト・電池計算・BFメモ・すき間テープ・USB-C）すべてリンク先あり／目次の飛び先2つ（#battery-erabikata・#wh-keisan）あり
6. commit & push → ops/drafts/hikouki_battery_internal_links_2026-11-24.md の4か所（電池計算・USB-C・電熱ベスト・BFメモ）を貼る。差し込み位置の行は11/23 05:06時点でも各記事に1か所だけ（確認済み）
※ 新記事は今週2本枠の1本目（暖房記事は先週11/23 01:06公開＝先週の週末分扱いかは会議の「月曜〜日曜で数える」決定に従う）
