# 発見経路の候補（2026-11-03 調査・ビルド｜事業9）

前提：Googleインデックス 0 件。IndexNow（Bing・Yandex等向け）は導入済み、robots.txt に Sitemap 記載済み。
今回 RSS（https://zaq-master.github.io/ai-lab/feed.xml）を追加。ここは**調査だけ**で、どれも未実行。

| # | 候補 | 誰が・どうやる | アカウント作成 | お金 | 規約同意 | 効果の見込み（根拠） |
|---|---|---|---|---|---|---|
| 1 | GitHubリポジトリ About 欄の Website／説明／Topics | **AIが `gh api -X PATCH repos/zaq-master/ai-lab -f homepage=... -f description=...` でできる**（2026-11-03 確認：このトークンは repo の admin 権限あり、現状 homepage・description・topics とも空）。オーナーがGitHub画面の⚙で設定しても可 | 不要（既存アカウント） | 0円 | 不要（既存のGitHub規約の範囲） | 小〜中。GitHubのページはクロールされやすく、サイトへの外部リンクが1本増える。リンクの nofollow 有無は未確認。README（今回更新）にもサイトURLあり |
| 2 | Google Search Console に登録＋sitemap送信 | オーナーのGoogleアカウントでログイン→URLプレフィックスで登録→所有確認用HTMLファイルをAIが docs/ に置く | 既存Googleアカウントなら新規作成は不要。ただし**オーナーのログインが必要** | 0円 | 必要（Search Console 利用規約） | **大**。Googleは sitemap の ping エンドポイントを廃止し、robots.txt か Search Console での送信を案内（出典1）。インデックス状況の確認もここでしかできない → いちばん効く |
| 3 | Bing Webmaster Tools | オーナーがMicrosoft/Googleアカウントでログイン。Search Console からのサイト取り込みで確認を省略できる（出典2） | ログインが必要（作成は既存アカウントなら不要） | 0円 | 必要 | 中。IndexNow 済みのため上積みは小さめ。Bing経由の検索（ChatGPT検索等も Bing の索引を使うとされる）の状況確認用 |
| 4 | WebSub（Google運営の公開ハブ pubsubhubbub.appspot.com）に feed 更新を通知 | AIが push 後に `hub.mode=publish&hub.url=<feed>` をPOSTするだけ（出典3）。RSSに `<atom:link rel="hub">` を足すとより正式 | 不要（ページに記載なし） | 0円 | **要確認**：ページに Google の利用規約へのリンクがあり「同意しないなら別のハブを使って」とある（出典3）→ 規約同意に当たるのでオーナー判断 | 小。フィード購読者側（Feedly等）への即時通知が主。Google検索のインデックスへの効果は公式に保証なし |
| 5 | Feedly・Inoreader 等のRSSリーダー | **発行側の登録は不要**。RSSを出していれば読者が購読できる（今回対応済み）。運営側が自分で購読してもSEO効果はほぼ無い | 読者側のみ | 0円 | 読者側のみ | 小。読者が増えたときの再訪経路。X・note・READMEにRSSのURLを載せると効く |
| 6 | はてなブックマーク | ブックマークするには はてなID（ログイン）が必要（出典4）。**自分で自分の記事をブクマするのは自作自演寄りでルールの趣旨に反する**ので、記事に「はてブ」ボタンを置いて読者に任せる形だけが可 | 必要（新規作成はルール7で不可） | 0円 | 必要 | 小〜中（ホットエントリ入りすれば大きいが、狙って作れない）。ボタン設置だけならアカウント不要 |
| 7 | note・X・Instagram のプロフィール／記事からサイトへのリンク | 既存アカウント。PC回で実施（プロフィール変更は許可済み） | 不要 | 0円 | 不要（既存） | 小〜中。人の流入の経路。記事末尾にサイトの関連ツールへのリンクを入れる |
| 8 | Googleの sitemap ping（`google.com/ping?sitemap=`） | — | — | — | — | **使えない**：2023年6月に廃止告知（出典1）。robots.txt の Sitemap 行で代替済み |

## おすすめの順番
1. **#1（AIで今すぐ・承認不要の範囲）**：司令塔の判断でGitHub About に homepage・説明（「AI運営」を明記）・topics を設定。
2. **#2（オーナー5分）**：Search Console の登録と sitemap 送信。インデックス0件の原因切り分けにも必須。
3. #3 は #2 のあとに取り込みで。#4 は規約の扱いをオーナーに確認してから。

## 出典
1. Google Search Central Blog「Sitemaps ping endpoint is going away」（2023-06）https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping
2. Bing Webmaster Blog「Import sites from Search Console to Bing Webmaster Tools」（2019-09）https://blogs.bing.com/webmaster/september-2019/Import-sites-from-Search-Console-to-Bing-Webmaster-Tools
3. Google PubSubHubbub Hub https://pubsubhubbub.appspot.com/
4. はてなブックマーク（窓の杜の紹介ページ）https://forest.watch.impress.co.jp/library/software/hatenabm/
- GitHub の権限は `gh api repos/zaq-master/ai-lab` の `permissions.admin=true` で確認（2026-11-03）。API：GitHub REST「Update a repository」（homepage・description）
