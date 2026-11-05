# Google未掲載の原因点検（サイト側の不具合チェック）2026-11-05

担当：カンサ（戦略参謀・監査）
方法：`python3 build.py` を実行（成功、「built 22 posts」）→ docs/ の全HTML 36件・sitemap.xml・robots.txt をスクリプトで機械的に点検。
公開中のサイトへの接続はこの環境から拒否された（zaq-master.github.io への接続がプロキシで拒否、GitHub Pages 設定APIも 403）。そのため、**配信中の実物と GitHub Pages の設定は確認できていない**。以下はビルド出力だけで分かること。

## 結論
**載らなくなるサイト側の不具合（noindex・canonicalの誤り・robots.txtでのブロック・サイトマップの誤り）は見つからなかった。**
公開4日で掲載0件なのは、「Googleがまだこのサイトを見つけていない／巡回待ち」の可能性が高い。サブパス（/ai-lab/）で公開しているため、robots.txt に書いたサイトマップの場所が Google に届かない（下の「中」）。

## 致命（掲載を止めるもの）
- なし
  - 記事22本・トップ・about・無料ツール1本：`<meta name="robots">` なし（＝掲載禁止の指定なし）
  - 記事中の `nofollow` は楽天の広告リンク（`rel="nofollow sponsored noopener"`）だけ。ページ全体の指定ではなく、正しい使い方
  - robots.txt（docs/robots.txt、build.py 431行）：`User-agent: * / Allow: /` でブロックなし

## 中
1. **robots.txt の Sitemap 行が Google に読まれない**
   - 根拠：Google が読む robots.txt はドメイン直下（`https://zaq-master.github.io/robots.txt`）だけ。このサイトは `/ai-lab/` の下なので、docs/robots.txt（＝`/ai-lab/robots.txt`）は無視される。中の Sitemap 行（`https://zaq-master.github.io/ai-lab/sitemap.xml`）も Google には届かない
   - 影響：Search Console でサイトマップを送れない今、Google がサイトを知る経路は「外部からのリンク」だけ。IndexNow（.github/workflows/indexnow.yml）は Bing などには届くが Google は対象外
   - 対処（提案）：オーナーの Search Console 登録（URLプレフィックス `https://zaq-master.github.io/ai-lab/`、HTMLファイル確認方式なら docs/ に置くだけ）が最短。それまでは X・note・Instagram プロフィールからサイトへのリンクを増やす。ユーザーサイト用リポジトリ（zaq-master.github.io）を作って直下に robots.txt を置く方法もあるが、リポジトリ作成＝アカウント操作なのでオーナー判断
2. **配信中の実物を未確認**
   - GitHub Pages が main の docs/ を配信しているか、公開URLが200で返るかは、この環境から見られなかった。次のPC回（内蔵ブラウザ）で `https://zaq-master.github.io/ai-lab/robots.txt` と `/sitemap.xml` が開くかを1回確認したい
   - 補足：この作業時点でローカルのリポジトリは「ブランチなし（detached HEAD）」状態だった。push の運用に影響しないか司令塔側で確認を

## 軽
1. **トップの無料ツールへのリンクが正規URLとずれていた → 直した**
   - 根拠：docs/index.html が `apps/sub-check/index.html` にリンク、ページの canonical と sitemap は `https://zaq-master.github.io/ai-lab/apps/sub-check/`（末尾スラッシュ）
   - 修正：build.py 309行 `"apps/sub-check/index.html"` → `"apps/sub-check/"` の1か所。再ビルドし、docs/index.html のリンクが `href="apps/sub-check/"` になり、リンク切れ0件のままなのを確認
2. **本文が短めの記事が4本**（タグを除いた文字数、スクリプト計測）
   - monitor-light-guide 約1,406字／desk-qol-guide 約1,467字／smart-remote-count-shindan 約1,554字／usb-c-charger-guide 約1,743字
   - 掲載を止める不具合ではないが、「中身が薄い」と見られると後回しにされやすい。SEO改善回（15:00）で拡充候補
3. **docs/sns/*.src.html（11件）が公開フォルダにある**
   - SNS画像の元HTML。build.py 418〜422行で全件に `noindex` を自動で付けており、sitemap にも入っておらず、サイト内からリンクもない → 害なし。ファイル名に未来日付（2026-11-14-*）があるが検索には出ない

## 問題なしを確認した項目
- canonical：全25ページ（トップ・about・記事22・ツール1）にあり、すべて `https://zaq-master.github.io/ai-lab/...` の絶対URLで自己参照。トップは末尾スラッシュ、ツールはディレクトリ末尾スラッシュ（sitemap と一致）。重複なし
- title・description：全25ページにあり、重複0件
- lang：全25ページ `<html lang="ja">`、doctype あり、viewport あり
- sitemap.xml：URL 25件＝公開ページ25件と一致（漏れ・余計なページ・重複なし）。全URLが実在ファイルに対応。lastmod は `YYYY-MM-DD` 形式（2026-11-04／11-05）
- 内部リンク切れ：0件（相対リンク・自サイト絶対URLの両方。画像・SVG含む）。ルート絶対パス（`/...`、サブパスで切れるもの）は0件
- 孤立ページ：トップから全25ページに到達できる（到達できないのは noindex の sns/*.src.html だけ）
- 下書き・テスト：content/posts に draft 指定なし、docs/posts は記事22本＋アイキャッチSVG22枚のみ
- docs/.nojekyll あり。docs/eba3c8….txt は IndexNow の鍵ファイル（ops/seo/indexnow.md の仕組み）

## 直したもの（一覧）
| ファイル | 行 | 変更 |
|---|---|---|
| build.py | 309 | 無料ツールのリンク先 `apps/sub-check/index.html` → `apps/sub-check/`（canonical と統一） |
| docs/index.html | — | 上の再ビルドで反映（他の docs/ 差分は build.py による日付の自動更新のみ） |
