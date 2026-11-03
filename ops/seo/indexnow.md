# IndexNow（Google以外の検索エンジンへの更新通知）2026-11-03 導入
- 仕組み：main に docs/** の変更が push されると `.github/workflows/indexnow.yml` が起動 → 約2分待って鍵ファイルが200で取れるのを確認 → docs/sitemap.xml の全URLを https://api.indexnow.org/IndexNow にPOST（Bing・Yandex・Naver・Seznam等で共有）。Actions タブから手動実行（workflow_dispatch）も可。
- 鍵：config.json の `indexnow_key`。build.py が毎回 docs/<key>.txt（中身は鍵だけ）を書き出す。仕様上公開してよいファイル。鍵を変えるときは config.json だけ変えて build。
- サブパス対応：鍵を /ai-lab/ に置き keyLocation で指定。仕様では「鍵の場所が送信できるURLの範囲を決める」ので、/ai-lab/ 配下のURLだけ送る（ワークフローで絞り込み済み）。
- 確認方法：GitHub の Actions → IndexNow → 最新の実行ログの `IndexNow response:` 行。200=受理、202=受理・鍵検証待ち（正常）、403=鍵が取れない/不一致、422=URLが範囲外かkeyLocation不正、429=送りすぎ。
- 注意：同じURLを短時間に何度も送らない（変更があったときだけ）。Google は IndexNow 非対応なので Search Console（オーナー作業）は別途必要。
- Bing Webmaster Tools は使わない（アカウント作成・規約同意になるため、絶対ルール7）。
- 出典：https://www.indexnow.org/documentation ／ https://yandex.com/support/webmaster/en/indexnow/reference.md
