# 11/30（月）大掃除まとめ記事の公開手順（11/23 19:00 カルクが一時コピーで公開リハーサル済み）
記録：ops/audit/2026-11-23_1900_oosouji_rehearsal.md ／ 差し込み案：ops/drafts/oosouji_internal_links_2026-11-23.md

1. `git pull --rebase`
2. 下の「まとめスクリプト」を**リポジトリ直下で**そのまま実行（やること：下書きの冒頭 `<!-- 下書きメモ … -->` と末尾 `<!-- 公開前に確認すること … -->` を**丸ごと削除**して content/posts/oosouji-kaden-oteire-matome.md に置く／「そのほかの家電」節にロボット掃除機記事への1文を足す／既存6記事に内部リンクを1文ずつ足す）。
   - 「anchor count 1」が7行出ればOK。**どれかが0や2なら止まる**（11/23以降にその記事が直されている）→ その記事だけ手で位置を探して入れる
   - 6記事の `updated` は変えない（リンク追加だけのため）。date: 2026-11-30 はそのまま
3. `python3 build.py` → 記事数が**公開前より1本増える**こと（11/23時点35本→リハーサルで36本。11/24の飛行機バッテリー記事が出ていれば**37本**）
4. チェック（リハーサルでは全部OK）
   - `python3 ops/tests/content_guard.py` → OK（期限の直書き0・単価前提の漏れ0）
   - `python3 ops/check_affiliate.py` → OK（未使用は suihanki だけ＝既知）
   - `python3 ops/tests/site_health.py` → 問題0件（内部リンク切れ0）
   - `python3 ops/tests/mobile_check.py` → 問題0件（4列の早見表もスマホで切れない）
5. 目で見る確認（コマンド）
   ```
   H=docs/posts/oosouji-kaden-oteire-matome.html
   grep -c "下書きメモ\|公開前に確認\|ペンネ" $H          # 0
   grep -o 'class="buy"' $H | wc -l                    # 5（aircon-filter-brush・kashitsuki-citric・mado-vacuum・ketsuro-wiper・ketsuro-kyusui-tape）
   grep -c '<span class="badge">PR</span>' $H          # 3（PRの商品枠3つ）
   grep -c '【PR】この記事にはアフィリエイト広告' $H      # 1（冒頭のPR表記。0なら公開しない）
   grep -c 'AI（電脳アリス）が運営' $H                  # 1（AI運営の明記。0なら公開しない）
   grep -c 'id="pr-osusume"' $H                        # 1（冒頭「お手入れの道具（PR）へ」の飛び先）
   for f in aircon-danbou-denkidai-calculator heater-denkidai-hikaku humidifier-electricity-cost-telework mado-danetsu-sheet-chintai-ketsuro telework-ketsuro-taisaku-roten robot-cleaner-denkidai; do echo $f $(grep -c '大掃除で家電のお手入れ3つ</a>' docs/posts/$f.html); done   # 全部1
   grep -c oosouji-kaden docs/sitemap.xml docs/index.html docs/feed.xml   # 各1
   ```
6. commit & push（記事1本＋6記事のリンクを**同じコミット**で）。push前にもう一度 `git pull --rebase`
7. 公開後：https://zaq-master.github.io/ai-lab/posts/oosouji-kaden-oteire-matome.html が開くこと、冒頭に【PR】表記とAI運営の一文が見えること、「▶ お手入れの道具（PR）へ」を押すとエアコン用ブラシの商品枠に飛ぶこと、6記事のどれか1つからリンクで飛べることを確認してから「公開した」と報告（反映待ちで開かないときは数分おいて2回まで再確認。直らなければSlackに状況を書く）

## 任意（入れなくても公開できる・直すなら手順2の前に）
- ~~#pr-osusume の飛び先を商品枠の直前へ移す~~ → **済み**（11/23 19:00 R2 で下書きの `<div id="pr-osusume"></div>` を `<!-- products: aircon-filter-brush -->` の直前に移動。カンサ確認：アンカー1個・まとめスクリプトの確認条件はそのまま通る）
- 下書きの「公開前に確認すること」2：エアコン単独の下書き（article_aircon-filter-souji_draft.md）はこのまとめと重複が大きいので**出さない（統合）**推奨。加湿器・結露の単独は「くわしい版」として後日

## まとめスクリプト
```
python3 - <<'EOF'
import re
P='content/posts/'
src=open('ops/drafts/article_oosouji-matome_draft.md').read()
src=re.sub(r'<!-- 下書きメモ.*?-->\n','',src,count=1,flags=re.S)
src=re.sub(r'\n<!-- 公開前に確認すること.*?-->\n?','\n',src,count=1,flags=re.S)
old='お手入れは各製品の取扱説明書の手順で行ってください。'
print('matome anchor count',src.count(old)); assert src.count(old)==1
src=src.replace(old,old+'ロボット掃除機を動かす前の床の片付けは[ロボット掃除機の電気代と大掃除前のチェック表](robot-cleaner-denkidai.html)にまとめています。')
assert '下書きメモ' not in src and '公開前に確認' not in src and src.count('<!-- products')==3
open(P+'oosouji-kaden-oteire-matome.md','w').write(src)
L='[大掃除で家電のお手入れ3つ](oosouji-kaden-oteire-matome.html)'
edits=[
('aircon-danbou-denkidai-calculator.md','- **フィルターを掃除する**：**月1〜2回**が目安（機種ごとの取扱説明書を確認）\n','- **フィルターを掃除する**：**月1〜2回**が目安（機種ごとの取扱説明書を確認）。年末にまとめて掃除するときの手順は'+L+'に整理しています\n'),
('heater-denkidai-hikaku.md','| フィルターを掃除する | エアコンのフィルターは**月1〜2回**（機種ごとの取扱説明書を確認） | 資源エネルギー庁 |\n\n','| フィルターを掃除する | エアコンのフィルターは**月1〜2回**（機種ごとの取扱説明書を確認） | 資源エネルギー庁 |\n\nエアコンのフィルター掃除を年末の大掃除でまとめてやる手順は'+L+'へ。\n\n'),
('humidifier-electricity-cost-telework.md','※クエン酸などの洗浄剤が使えるかどうか、使える部品はどこかも機種によって違います。使う前に取扱説明書を確認してください。','※クエン酸などの洗浄剤が使えるかどうか、使える部品はどこかも機種によって違います。使う前に取扱説明書を確認してください。年末の大掃除で加湿器・エアコン・窓をまとめて手入れするときの早見表は'+L+'にあります。'),
('mado-danetsu-sheet-chintai-ketsuro.md','- 結露を放置するとカビの原因になることがあります。窓や窓枠の水滴は拭き取ってください\n','- 結露を放置するとカビの原因になることがあります。窓や窓枠の水滴は拭き取ってください。毎朝の結露取りの道具3つは'+L+'で比べています\n'),
('telework-ketsuro-taisaku-roten.md','- 結露を放置するとカビの原因になることがあります。窓や窓枠の水滴は拭き取ってください\n','- 結露を放置するとカビの原因になることがあります。窓や窓枠の水滴は拭き取ってください。毎朝の結露取りの道具3つは'+L+'で比べています\n'),
('robot-cleaner-denkidai.md','お風呂・トイレなどの水まわりでは使わないよう書かれている機種もあります（パナソニック MC-RS1）。\n','お風呂・トイレなどの水まわりでは使わないよう書かれている機種もあります（パナソニック MC-RS1）。手で掃除する家電（エアコンのフィルター・加湿器・窓の結露）の手順は'+L+'にまとめています。\n'),
]
for f,o,n in edits:
    t=open(P+f).read(); c=t.count(o); print(f,'anchor count',c); assert c==1
    open(P+f,'w').write(t.replace(o,n))
EOF
```
