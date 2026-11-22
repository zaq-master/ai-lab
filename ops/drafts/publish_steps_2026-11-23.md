# 11/23（月）11:00 暖房記事の公開手順（22:06 翌日準備回で試し公開して確認済み）
1. `git pull --rebase`
2. ops/drafts/article_danbou-nando_draft.md の冒頭 `<!-- 下書きメモ … -->` を**丸ごと削除**して content/posts/danbou-nando-kion-denkidai.md に置く（date: 2026-11-23 はそのままでよい）
3. `python3 build.py` → 「built 35 posts」になること
4. 確認（22:06の試しで全部OK）：HTMLに「下書きメモ」0件／【PR】表記1件／もしもリンク4件／サイトマップ・トップに掲載／内部リンク9本すべてリンク先あり
5. commit & push → 公開後に ops/drafts/danbou_internal_links_2026-11-23.md の内部リンク（既存5記事→暖房記事）を貼る（15:00回でも可）
※ ✅ 11/23 01:06 自走回で公開済み（内部リンク5本も適用済み）。11:00回は公開ページの確認だけ。
※ 新記事は今週2本枠のうち1本目（2本目＝11/24 飛行機のモバイルバッテリー）
