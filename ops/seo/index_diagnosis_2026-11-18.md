# Google掲載0件の診断（2026-11-18・カンサ）

調査と報告のみ。build.py・content/・docs/ は変更していない。commit・push なし。

## 結論
- **「Google掲載0件」は、Google本体で確かめた記録が見つからない。** 毎日の計測に使っている検索ツールは `site:` の絞り込みが保証されず、この数字は根拠にならない。
- **無料・アカウント作成なしで残っている手は4つ**（測り方の修正、プロフィールのURL、GitHubの About 欄、更新日の修正）。どれも小さく、Search Console の代わりにはならない。
- **サイト側に、掲載を止める設定ミスは見つからなかった。** いちばん可能性が高い原因は「Googleがサイトをまだ見つけていない」だが、断定はできない。

## ① 確認した事実

### 計測について
| # | 事実 | 根拠 |
|---|---|---|
| 1 | 日報の掲載数は WebSearch の `site:zaq-master.github.io/ai-lab` で測っている | .claude/skills/daily-report/SKILL.md 11行目、ops/metrics.csv（11/13〜11/17 は0） |
| 2 | **WebSearch の `site:` は絞り込みが保証されない。** 指定サイトの結果は `site:squidfunk.github.io/mkdocs-material` 0／14件、`site:squidfunk.github.io mkdocs material setup` 0／19件、`site:docs.python.org asyncio tutorial` 10／15件 | 2026-11-18 に実施した対照テスト（監査の再テスト含む） |
| 3 | 同じツールのドメイン絞り込み（allowed_domains）は効く。squidfunk.github.io は10件出て、zaq-master.github.io は3通りの検索語すべて0件 | 同上。**このツールの検索元がGoogleかは未確認** |
| 4 | 内蔵ブラウザでGoogle本体を検索した結果の記録は、ops/log と ops/drafts に見つからない | 両フォルダを検索。手順の案は ops/strategy/judge_2026-11-16_v2.md 16行目にあるのみ |

### サイトの状態
| # | 事実 | 根拠 |
|---|---|---|
| 5 | 公開ページは配信されている（鍵ファイル・記事とも200、内容もローカルと一致） | GitHub Actions の IndexNow 実行ログ（2026-11-18 03:08 UTC）`key=200 page=200 same=True` |
| 6 | IndexNow の直近19回はすべて 200 OK。ただしGoogleは対象外 | 同ログ、ops/seo/indexnow.md |
| 7 | sitemap は37件で、重複なし、全URLのファイルが実在 | docs/sitemap.xml をスクリプトで点検 |
| 8 | 37ページすべて、canonical が自分自身を指し、robots の meta 指定なし | 同上 |
| 9 | 全ページにトップから1クリックで届く。内部リンク切れ0件 | 同上 |
| 10 | Search Console の確認タグ・確認ファイルは docs/ に無い（未登録と整合） | docs/ を検索 |

### robots.txt について
| # | 事実 | 根拠 |
|---|---|---|
| 11 | `/ai-lab/robots.txt` は無効な場所。**Sitemap 行はGoogleに読まれない** | [Google：robots.txt の仕様](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec)（`/folder/robots.txt` は無効、クローラーはサブディレクトリを確認しない） |
| 12 | 影響は「sitemap が届かない」ことだけ。この robots.txt がクロールを止めることはない | 同上 |
| 13 | Googleにサイトマップを知らせる公式の方法は、Search Console、その API、ルートの robots.txt。RSS/Atom には WebSub もある | [Google：サイトマップの作成と送信](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) |

### 外部リンクについて
| # | 事実 | 根拠 |
|---|---|---|
| 14 | noteからのリンクは記録上**8本以上**（第1〜3回に6本、第4回に1本、第6回に1本）。依頼文の6本より多い | ops/log/2026-11-08.md 90行目、2026-11-09.md 13行目・66行目 |
| 15 | GitHub の README のサイトへのリンクは `rel="nofollow"` 付き | github.com/zaq-master/ai-lab のHTML |
| 16 | nofollow のリンクは、Googleが原則たどらない | [Google：外部リンクの rel 属性](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links) |
| 17 | GitHub の About 欄（homepage・説明・topics）は**空のまま**。11/3 に提案済みで未実行 | `gh api repos/zaq-master/ai-lab`、ops/seo/discovery_options.md #1 |
| 18 | IG・noteプロフィールへのサイトURL追加は backlog で「未」のまま | ops/backlog.md 58行目 |
| 19 | 最も古い記事の公開日は 11/2 で、今日で16日。Googleは新しいサイトに気づくまで「数週間かかることがある」としている | content/posts の date、[Google：Googleに載せる方法](https://developers.google.com/search/docs/fundamentals/get-on-google) |

### 更新日について
| # | 事実 | 根拠 |
|---|---|---|
| 20 | 11記事の更新日が、リンク追加だけのコミットで新しくなった可能性がある。Googleは lastmod に「重要な更新」の日付を求めている | commit 371d2f6（10記事は+2〜3行）、build.py 174行目、上記サイトマップの公式ページ |

### 未確認
- ルートの `https://zaq-master.github.io/robots.txt` の有無と応答（この環境から接続不可）
- 公開ページのHTTPヘッダー（X-Robots-Tag の有無）
- noteのリンクに nofollow が付いているか、note記事がGoogleに載っているか（note.com に接続不可）
- GitHub の About 欄の homepage リンクの rel 属性
- Google本体での実際の掲載数、Googleのクロール履歴（Search Console が必要）

## ② 原因の候補（可能性の高い順、いずれも断定不可）
1. **Googleがサイトをまだ見つけていない、または巡回待ち（最有力）**
   sitemap がGoogleに届く経路がなく、確認できた外部リンクは少ない。公開16日は、公式の「数週間」の範囲内。
2. **すでに一部は載っているが、測れていない（否定できない）**
   これまでの「0件」は、Google本体の結果ではない。
3. **見つかったが、掲載が見送られている（判定不可）**
   新しいサイトで、短期間に34記事を公開し、広告リンクも多い。Search Console の「クロール済み - インデックス未登録」を見ないと分からない。
4. **技術的なブロック（可能性は低い）**
   ビルド出力に問題はなく、公開ページも200を返す。上記の未確認2点だけが残る。

## ③ 今すぐできる修正案（優先順）

### 1. 掲載数の測り方を直す（クラウドの回で可、10分）
**.claude/skills/daily-report/SKILL.md 11行目**を次に置き換える。
```
- インデックス状況：WebSearch の site: は効かないので使わない。PC回の内蔵ブラウザでGoogleに `site:zaq-master.github.io/ai-lab` を1回検索する（CAPTCHAが出たら中止）。測れない回は ops/metrics.csv の site_index_seen を空欄にする（0と書かない）
- 補助：WebSearch の allowed_domains に zaq-master.github.io を指定した検索の結果はログにだけ書く（Googleの件数として扱わない）
```

### 2. 未投稿のnote原稿の表現を直す（絶対ルール6、投稿前に必須）
対象：ops/note/2026-11-13_vol08.md 81行目、ops/note/2026-11-23_vol_paid.md 75行目・292行目。

「Googleの掲載は0件」を、次のように改める。
> Googleに載っているかは、まだ正しく確認できていません（使っている検索ツールでは、このサイトは見つかっていません）

公開済みの回は、手順3の結果が出てから訂正の要否を判断する。

### 3. 次のPC回でGoogle本体を確認し、プロフィールにURLを入れる（5分）
- Googleで `site:zaq-master.github.io/ai-lab` を1回検索し、件数をログに書く（CAPTCHAが出たら中止）
- IG・noteプロフィールに `https://zaq-master.github.io/ai-lab/` を入れる（絶対ルール9で許可済み、AI運営の明記は残す）

### 4. GitHub の About 欄を埋める（1分、効果は小）
```
gh api -X PATCH repos/zaq-master/ai-lab \
  -f homepage='https://zaq-master.github.io/ai-lab/' \
  -f description='QOLガジェット研究所：暮らしの電気代計算ツールと比較記事（AI運営）'
```
このトークンは admin 権限あり。この環境のプロキシで書き込めるかは未確認。

### 5. リンク追加だけの記事の更新日を戻す（別担当の作業が終わってから）
commit 371d2f6 で変更した `content/posts/` の11記事のうち、`updated` がまだ無く（denki-moufu-kotatsu-denkidai-telework と dennetsu-vest-battery-jikan-denkidai は設定済み）、以後に本文の更新がないものの front matter に、`updated: <最後に本文を更新した日>` を追加する。build.py の変更は不要（174行目が `updated` を優先する）。

### 6. 古い記述を訂正する
- ops/seo/discovery_options.md 3行目・15行目：「robots.txt の Sitemap 行で代替済み」は誤り（事実11）
- ops/research/2026-11-17_seo_check.md 19行目：「sitemapの場所を正しく指している」に「ただしこの場所の robots.txt はGoogleに読まれない」と追記

### 使えない・今はやらない手
| 手 | 判定 | 理由 |
|---|---|---|
| Indexing API | 使えない | 求人と動画ライブ配信のページ専用（[公式](https://developers.google.com/search/apis/indexing-api/v3/quickstart)） |
| sitemap ping | 使えない | 廃止済み（discovery_options.md #8） |
| `zaq-master.github.io` リポジトリを作り、ルートに robots.txt を置く | 今はやらない | 新規リポジトリの作成はオーナー判断。Googleがこのホストを訪れないと読まれない |
| WebSub | 今はやらない | ハブの利用規約への同意はオーナー判断（discovery_options.md #4）。掲載への効果も不明 |
| はてなブックマーク等の自作自演 | やらない | アカウント作成が必要で、ルールの趣旨にも反する |

## ④ オーナーにしか頼めないこと（1つだけ）
**Search Console に `https://zaq-master.github.io/ai-lab/` を「URLプレフィックス」で登録し、確認用のHTMLタグ1行をSlackに貼ってください。Googleへのサイトマップ送信と、載らない本当の理由の確認は、ここでしかできないためです（約10分、無料、Googleの規約同意が必要）。**

補足：公式ヘルプには、サブフォルダのURLを直接確認できるとは明記されていない。登録画面の指示に従い、確認に失敗したら、その画面の内容をSlackで知らせてもらう。
