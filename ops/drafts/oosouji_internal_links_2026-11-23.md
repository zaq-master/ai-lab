# 大掃除まとめ（11/30公開）への内部リンク位置の下書き
作成：2026-11-23 15:00 SEO改善回／リンク先：`oosouji-kaden-oteire-matome.html`（ops/drafts/article_oosouji-matome_draft.md）

**今は入れない**：まとめ記事が未公開のため、今入れるとリンク切れになる。
**11/30の公開回で、まとめ記事を content/posts に置いた同じコミットで下の6か所を入れる**（リンク追加だけなので各記事の `updated` は変えない）。

文言は既存の文の末尾に1文足すだけ。数字・価格・期限は書かない（まとめ記事側に出典つきで載っているため）。

| # | 記事（content/posts/） | 入れる場所（この文の末尾に足す） | 足す文 |
|---|---|---|---|
| 1 | aircon-danbou-denkidai-calculator.md | 「同じエアコンで、ムダなく暖める基本」の箇条「**フィルターを掃除する**：**月1〜2回**が目安（機種ごとの取扱説明書を確認）」 | 。年末にまとめて掃除するときの手順は[大掃除で家電のお手入れ3つ](oosouji-kaden-oteire-matome.html)に整理しています |
| 2 | heater-denkidai-hikaku.md | 153行目の表「フィルターを掃除する」行の直後（表の外、空行のあと） | エアコンのフィルター掃除を年末の大掃除でまとめてやる手順は[大掃除で家電のお手入れ3つ](oosouji-kaden-oteire-matome.html)へ。 |
| 3 | humidifier-electricity-cost-telework.md | 「お手入れは…」節の最後「※クエン酸などの洗浄剤が使えるかどうか…取扱説明書を確認してください。」 | 年末の大掃除で加湿器・エアコン・窓をまとめて手入れするときの早見表は[大掃除で家電のお手入れ3つ](oosouji-kaden-oteire-matome.html)にあります。 |
| 4 | mado-danetsu-sheet-chintai-ketsuro.md | 注意点「結露を放置するとカビの原因になることがあります。窓や窓枠の水滴は拭き取ってください」 | 。毎朝の結露取りの道具3つは[大掃除で家電のお手入れ3つ](oosouji-kaden-oteire-matome.html)で比べています |
| 5 | telework-ketsuro-taisaku-roten.md | 注意点（141行目）の同じ文「…窓や窓枠の水滴は拭き取ってください」 | 4と同じ文 |
| 6 | robot-cleaner-denkidai.md | 「年末の大掃除で使う前に」節の「…手で窓・棚・水まわり」の順にすると、上の表の「片付ける」が先に済みます。」 | 手で掃除する家電（エアコンのフィルター・加湿器・窓の結露）の手順は[大掃除で家電のお手入れ3つ](oosouji-kaden-oteire-matome.html)にまとめています。 |

## 入れない記事（理由）
- danbou-nando-kion-denkidai.md：「フィルター掃除」は一言だけで、文脈が暖房の始め方。リンクを足すと本筋がぶれる
- futon-kansouki-denkidai.md：フィルター掃除はふとん乾燥機自身の話で、まとめ記事の3項目と関係ない
- kashitsu-ryo-calculator.md：お手入れは表の1行のみ。加湿器記事（#3）経由で十分

## 逆方向（まとめ → 既存）
まとめ下書きには既に8本へのリンクあり（denkidai-calculator／aircon-danbou-denkidai-calculator／humidifier-electricity-cost-telework／kashitsu-ryo-calculator／telework-ketsuro-taisaku-roten／mado-danetsu-sheet-chintai-ketsuro／fuyu-denkidai-matome／winter-heating-shindan）。
**robot-cleaner-denkidai.html が無い** → 公開回で「そのほかの家電は『取扱説明書の手順』で」節に「ロボット掃除機を動かす前の床の片付けは[ロボット掃除機の電気代と大掃除前のチェック表](robot-cleaner-denkidai.html)」を1文足す案。

## 公開回のチェック
1. build.py → `python3 ops/tests/mobile_check.py` → `python3 ops/tests/content_guard.py`
2. docs 内で `oosouji-kaden-oteire-matome.html` へのリンクが6記事から出ているか grep（`grep -l oosouji-kaden-oteire-matome docs/posts/*.html`）
