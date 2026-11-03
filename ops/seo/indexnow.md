# IndexNow（Google以外の検索エンジンへの更新通知）2026-11-03 導入・同日改修（監査 ops/audit/2026-11-03_1300_r2.md 中1・軽1〜3）
- 仕組み：main に docs/** の変更が push されると `.github/workflows/indexnow.yml` が起動 → `github.event.before..github.sha` の差分で変わった docs/*.html だけを公開URLに変換（build.py の page_url と同じ規則。docs/index.html→/ai-lab/）し、sitemap.xml に載っているURLだけに絞って https://api.indexnow.org/IndexNow にPOST（Bing・Yandex・Naver・Seznam等で共有）。
- 公式FAQ「変わっていないURLは送り直さない」に従う。0件なら送らず正常終了。全件送信は Actions タブからの手動実行（workflow_dispatch）と、before が全ゼロ（比較元なし）のときだけ。force push 等で差分が取れないときは警告を出して送らない。
- 配信待ち：送るページの1つ目を公開側から取得し、ローカルの docs/ と一致する（今回のコミットが反映された）まで最大約7分待つ。鍵ファイルも同時に確認。間に合わなければ警告を出して送信する。
- 鍵：config.json の `indexnow_key`。build.py が毎回 docs/<key>.txt（中身は鍵だけ）を書き出す。仕様上公開してよいファイル。鍵を変えるときは config.json だけ変えて build。
- サブパス対応：鍵を /ai-lab/ に置き keyLocation で指定。仕様では「鍵の場所が送信できるURLの範囲を決める」ので、/ai-lab/ 配下のURLだけ送る。
- 確認方法：GitHub の Actions → IndexNow → 実行ログの `mode=diff urls=N`（送ったURL一覧も出る）と `IndexNow response:` 行。200=受理、202=受理・鍵検証待ち（正常、初回は202で成功済み）、403=鍵が取れない/不一致、422=URLが範囲外かkeyLocation不正 → この2つ等はジョブ失敗。429（送りすぎ）と5xxは警告だけでジョブは緑のまま（オーナーへ失敗メールを飛ばさない）。
- 安全：actions/checkout は v4.2.2 のコミットSHAで固定、persist-credentials: false、権限は contents: read のみ。Google は IndexNow 非対応なので Search Console（オーナー作業）は別途必要。
- Bing Webmaster Tools は使わない（アカウント作成・規約同意になるため、絶対ルール7）。
- 出典：https://www.indexnow.org/documentation ／ https://www.indexnow.org/faq ／ https://yandex.com/support/webmaster/en/indexnow/reference.md
