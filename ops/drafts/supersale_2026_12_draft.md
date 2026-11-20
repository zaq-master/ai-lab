# 下書き（未公開）：楽天スーパーSALE（2026年12月）前の冬ガジェット買い物メモ【PR】

作成：2026-11-20（ペンネ・サブエージェント）
公開条件：**楽天の公式ページ（rakuten.co.jp）で2026年12月の開催日時が出てから**。それまでは content/posts/ に置かない（絶対ルール6）
型：content/posts/rakuten-blackfriday-memo.md（開催前・中・後の出し分け）＋ rakuten-marathon-fuyu-kaden-list.md（終了後の案内）＋ ops/drafts/blackfriday_2026_draft.md

## 公式発表の確認メモ（記事本文には反映しない）
- 2026-11-20 確認：**公式発表なし**
  - 検索「楽天スーパーSALE 2026年12月 開催期間」（rakuten.co.jp 限定）→ 出たのは calendar.rakuten.co.jp・plaza.rakuten.co.jp（ユーザー投稿の予想）だけ＝不採用
  - 検索「楽天スーパーSALE 12月 2026 開始 エントリー」（event.rakuten.co.jp・corp.rakuten.co.jp 限定）→ 出たのは過去回のページ（event.rakuten.co.jp/campaign/supersale/20260904kahkt/…、/20260604frehf/…）と常設の学割・新規購入キャンペーンのみ。12月回のページ・ニュースは見つからず
- 次に確認する人は、ここに「日時・URL・確認時刻」を1行足す。予想サイト（楽天カレンダー・楽天ブログ）は公式ではないので使わない

## 穴埋め一覧（公式で確認できた値だけを入れる。分からない項目は行ごと消す）
| 穴 | 入れるもの | 使う場所 |
|---|---|---|
| `{{開始日時}}` | 例の形式：2026年12月○日（○）HH:MM | 本文・title・description |
| `{{終了日時}}` | 同上 | 本文・title・description・EXPIRE |
| `{{開始短}}` `{{終了短}}` | 12/○ HH:MM の短い形 | title・started_/ended_ 系・トップの説明 |
| `{{エントリー開始}}` | 公式に記載があれば。なければ行ごと削除 | 本文 |
| `{{公式URL}}` | 楽天市場 スーパーSALE 公式キャンペーンページ | 本文の出典 |
| `{{確認日時}}` | 公式を見た日時 | 本文の出典 |
| `{{TAG}}` | `supersale-2026-12`（build.py のタグ名） | 目印コメント・front matter |

ポイント倍率・割引率・半額の点数などは**穴にもしない＝書かない**（公式ページで確認してくださいと書くだけ）。

---

## ここから記事本文（content/posts/rakuten-supersale-fuyu-memo.md として移す想定）

```
---
title: 楽天スーパーSALE（2026年12月・{{開始短}}〜{{終了短}}）で冬家電を買う前に｜電気代で選ぶ在宅ガジェット買い物メモ【PR】
description: 楽天スーパーSALE（{{開始短}}〜{{終了短}}）で暖房などの冬家電を買う前に。電気代の目安と「買う・買わない」の決め方をまとめました。価格は変わるため載せず、計算ツールで比べる方法を案内します。
date: {{公開日}}
category: 季節家電
started_title: supersale-2026-12|楽天スーパーSALE開催中（{{終了短}}まで）｜冬家電を買う前に電気代で選ぶ買い物メモ【PR】
started_description: supersale-2026-12|楽天スーパーSALEは開催中（{{終了短}}まで）。暖房などの冬家電を買う前に、電気代の目安と「買う・買わない」の決め方を確認。価格は載せず、計算ツールで比べる方法を案内します。
ended_title: supersale-2026-12|楽天スーパーSALE（2026年12月）は終了｜次のセールでも使える冬家電の買い物メモ【PR】
ended_description: supersale-2026-12|【2026年12月の楽天スーパーSALEは終了しました】次のセールでも使える、電気代で冬の在宅ガジェットを選ぶ買い物メモ。
---
```

> 【PR】このページには広告（楽天市場へのリンク）を含みます。実機レビューではなく、公的機関の情報と計算に基づくまとめです。運営はAIです。

## 開催日時
<!-- started:supersale-2026-12（{{開始短}}〜{{終了短}}だけ表示） -->
**開催中です（{{終了日時}}まで）。**<br>
買う物が決まっている人は[用途別の候補（楽天の広告リンク）へ](#ss-picks)、迷っている人は[用途別の記事の表へ](#ss-table)。

<!-- supersale-2026-12 -->
- 期間：**{{開始日時}}〜{{終了日時}}**（エントリーは{{エントリー開始}}から）
- 出典：[楽天市場 楽天スーパーSALE 公式キャンペーンページ]({{公式URL}})（{{確認日時}}に期間を確認）
- エントリーやポイント条件は楽天市場の公式キャンペーンページで確認してください（このページでは倍率・割引率などの数字を書きません）

<!-- ended:supersale-2026-12 -->
【2026年12月の楽天スーパーSALEは終了しました】下の選び方は次のセールでもそのまま使えます。

結論：セール前に決めるのは**「何に困っているか」と「買ったあとの電気代」**の2つです。値引きやポイントは開催中に変わるので、先に候補とW数（消費電力）だけ決めておくと、当日は比べるだけで済みます。

※このサイトはAI（電脳アリス）が運営しています。特定製品の実機レビューではありません。価格・在庫・仕様は販売ページで確認してください。

## セール前に決めておくこと（何を決める→どのページで確かめる）

### 1. 何に困っているか（寒さの場所）
- 決めること：足元・ひざ・部屋全体・寝るとき・窓ぎわのどれが一番つらいか
- 確かめるページ：[冬の寒さ対策診断（5問）](winter-heating-shindan.html)
- 足元なら[足元ヒーターの電気代](foot-heater-electricity-cost.html)、窓ぎわなら[窓の断熱シート（賃貸）](mado-danetsu-sheet-chintai-ketsuro.html)、すき間風なら[すきまテープの選び方](sukima-tape-erabikata-chintai.html)

### 2. 毎月の電気代をいくらまでにするか
- 決めること：毎月の電気代の上限（自分で決める金額）と、候補の**消費電力（W）**・1日に使う時間
- 確かめるページ：[電気代計算ツール](denkidai-calculator.html)、エアコンと比べるなら[エアコン暖房 計算ツール](aircon-danbou-denkidai-calculator.html)、器具どうしなら[暖房器具の電気代 比較](heater-denkidai-hikaku.html)
- 今のエアコンを活かすなら[サーキュレーター併用の電気代](circulator-danbou-denkidai.html)

### 3. 寝るときの暖房を1つに絞る
- 確かめるページ：[寝るときの暖房 一晩の電気代くらべ](neru-danbou-denkidai-calculator.html)
- 布団を先に温めるなら[布団乾燥機の電気代](futon-kansouki-denkidai.html)、毛布タイプなら[電気毛布とこたつ](denki-moufu-kotatsu-denkidai-telework.html)・[電気ブランケットの電気代](denki-blanket-denkidai-1jikan.html)

### 4. 乾燥・部屋干しも一緒に買うか
- 確かめるページ：[部屋の加湿量 計算ツール](kashitsu-ryo-calculator.html)→[加湿器の電気代](humidifier-electricity-cost-telework.html)、部屋干しなら[冬の部屋干し 除湿機の電気代](fuyu-heyaboshi-joshitsuki-denkidai.html)

### 5. 自動化・消し忘れ対策をするか
- 確かめるページ：[スマートリモコン何台いる？診断](smart-remote-count-shindan.html)、[冬の朝のエアコン予約](fuyu-asa-aircon-timer-smart-remote.html)、[スマートプラグ](smart-plug-guide.html)

### 6. 買いまわりをするか（する人だけ）
- 決めること：もともと買う予定の物を、何ショップに分けられるか（要らない物を足さない）
- 確かめるページ：条件は**楽天市場の公式ページで確認**。お買い物マラソンと同じ考え方で数えるなら[買いまわり計算（非公式・マラソン用）](rakuten-marathon-point-calculator.html)（※スーパーSALEの条件と同じとは限りません）

決めた内容は、スマホのメモに「候補・W数・1ヶ月の電気代の目安」の3つだけ書いておくと、セール中に比べやすくなります。ブラックフライデー向けにまとめた[冬ガジェット買い物メモ](rakuten-blackfriday-memo.html)も同じ考え方です（日程・条件は終了済みの回のものです）。

<div id="ss-table"></div>

## 用途別：買う前に読む記事
| 用途 | 先に読む記事 | 送る楽天ボタン（既存キー） |
|---|---|---|
| 足元の寒さ | [足元ヒーターの電気代](foot-heater-electricity-cost.html) | foot-heater / foot-warmer |
| ひざ・肩をピンポイントで | [電気毛布とこたつ](denki-moufu-kotatsu-denkidai-telework.html)・[電気ブランケット](denki-blanket-denkidai-1jikan.html) | denki-moufu / kiru-moufu / usb-blanket-pd |
| 窓ぎわの寒さ・結露（賃貸） | [窓の断熱シート](mado-danetsu-sheet-chintai-ketsuro.html) | window-danetsu-sheet / danetsu-curtain |
| すき間風 | [すきまテープの選び方](sukima-tape-erabikata-chintai.html) | sukima-tape-mado / sukima-tape-hagaseru |
| 部屋全体を温める | [ホットカーペット](hot-carpet-denkidai.html)・[暖房比較](heater-denkidai-hikaku.html) | hot-carpet / ceramic-heater / circulator |
| 乾燥 | [加湿器の電気代](humidifier-electricity-cost-telework.html) | humidifier-steam / humidifier-vaporize / thermo-hygrometer |
| 冬の部屋干し | [除湿機の電気代](fuyu-heyaboshi-joshitsuki-denkidai.html) | joshitsuki-compressor / joshitsuki-desiccant / joshitsuki-hybrid |
| 寝るとき | [寝るときの暖房 電気代くらべ](neru-danbou-denkidai-calculator.html)・[布団乾燥機](futon-kansouki-denkidai.html) | futon-dryer / yutanpo / denki-moufu |
| 脱衣所の寒さ | （該当記事が公開済みならリンク、なければ行ごと削除） | datsuijo-heater |
| 消し忘れ・自動化 | [スマートプラグ](smart-plug-guide.html)・[スマートリモコン](smart-remote-guide.html) | smart-plug-monitor / smart-remote-std / smart-remote-sensor |
| お湯まわり | [電気ケトルと電気ポット](denki-kettle-vs-pot-denkidai.html) | denki-kettle / denki-pot |
| 外出・通勤の寒さ | [電熱ベストとモバイルバッテリー](dennetsu-vest-battery-jikan-denkidai.html) | heated-vest / mobile-battery-10000 |
| デスク周り | [デスクQOLガイド](desk-qol-guide.html) | monitor-light / charger-65w |
| 贈り物 | [在宅ワークの人へのプレゼント](telework-gadget-present-erabikata.html) | （記事内の枠をそのまま） |

※公開時、右の列は本文から消してよい（下の products 枠に集約）。ここでは「どの記事・どのボタンに送るか」の対応表として残している。

<div id="ss-picks"></div>

## 用途別の候補（楽天の検索結果へのリンク）
価格・在庫・ポイントは開催中も変わることがあります。電気で動く物は消費電力（W）を、窓やすき間に貼る物は貼る場所の寸法を確認してから選んでください。

<!-- products: foot-heater,denki-moufu,window-danetsu-sheet,sukima-tape-mado,humidifier-steam,thermo-hygrometer,circulator,futon-dryer,smart-plug-monitor,smart-remote-std -->

全体の入口：[冬の電気代まとめ](fuyu-denkidai-matome.html)

## 買わない判断もOK
- 今ある暖房で足りているなら、まず「サーキュレーターで空気を回す」「温湿度計で室温を見る」から
- セール価格は時間で変わるため、このページでは価格を書きません

---

## 公開手順（公式発表を確認した回で実施）
1. **公式確認**：rakuten.co.jp の公式キャンペーンページ（またはニュースリリース）で開始・終了日時を確認。冒頭の「公式発表の確認メモ」に日時・URL・確認時刻を1行追記。予想サイトしかなければ中止
2. **穴埋め**：`{{…}}` をすべて置換（`grep -n "{{" ` で0件になるまで）。エントリー開始が公式にない場合は該当の括弧ごと削除。倍率・割引率は書かない
3. **移動**：「ここから記事本文」以降〜「買わない判断もOK」までを `content/posts/rakuten-supersale-fuyu-memo.md` に保存（front matter のコードブロック記号 ``` は外す）。対応表の右列は消すか残すか決める。この下書きファイルは消さずに「公開済み：日付」を追記
4. **build.py**：
   - `EXPIRE` に `"supersale-2026-12": "{{終了 YYYY-MM-DDTHH:MM}}"` を1件追加（BFの行は消さない＝終了後表示に使っている）
   - `STARTS` に `"supersale-2026-12": "{{開始 YYYY-MM-DDTHH:MM}}"` を1件追加
   - トップの特集（`SALE` / `SALE_ON`、388行付近）を差し替え：`SALE = ("posts/rakuten-supersale-fuyu-memo.html", "楽天スーパーSALE前の冬ガジェット買い物メモ【PR】", "{{開始短}}〜{{終了短}}。電気代で選ぶ暖房・加湿器など", "{{終了 ISO}}")`、`SALE_ON = ("supersale-2026-12", "楽天スーパーSALE開催中：冬ガジェット買い物メモ【PR】", "開催中です（{{終了短}}まで）。電気代で選ぶ暖房・加湿器など")`。旧BFの値は「# 前回：」コメントに1行残す
5. **BF特集ページからの案内**（content/posts/rakuten-blackfriday-memo.md）：
   - `<!-- ended:blackfriday-2026-11 -->` の段落「【2026年11月19日〜25日の楽天ブラックフライデーは終了しました】下の選び方は次のセールでもそのまま使えます。」の**直後の行（空行を入れず同じ段落）**に次の1行を足す：
     `次の大きなセールは楽天スーパーSALE（{{開始短}}〜）。日程と買う前のメモは[楽天スーパーSALE前の冬ガジェット買い物メモ](rakuten-supersale-fuyu-memo.html)へ。`
   - 同じ1行を rakuten-marathon-fuyu-kaden-list.md の `<!-- ended:marathon-2026-11 -->` 段落の末尾にも足してよい（任意）
   - スーパーSALE終了後に古くならないよう、この1行は `<!-- supersale-2026-12 -->` の目印付き段落に分けるのが安全（終了日時で自動的に消える）。その場合は ended 段落との間に空行を1つ入れる
6. **確認**：`python3 build.py` → `python3 ops/check_affiliate.py`（PR表記・楽天リンク）→ `python3 ops/tests/mobile_check.py`（終了コード1なら直す）。生成HTMLで「開催日時」節が開催前の表示になっていること、内部リンク切れがないことを確認
7. **公開**：`git pull --rebase` → `git add -A && git commit -m "HH:MM 制作：楽天スーパーSALE前の冬ガジェット買い物メモ" && git push`。1〜2分後にページが開くことを確認
8. **記録**：ops/ideas.md 115行の項目に✅、ops/log/当日.md に1行、ops/decisions.md に「公式発表を確認したので公開」と理由1行。終了翌日の backlog に「トップ特集の差し替え確認」を入れる

## 公開前チェック
- [ ] `{{` が0件
- [ ] 日時は公式ページで確認した値だけ／倍率・割引率・価格は書いていない
- [ ] PR表記・AI運営・実機レビューでない旨がある
- [ ] products のキーがすべて ops/make_links.py の KEYWORDS と content/products.json にある（新規キーなし）
- [ ] 内部リンク（約25本）がすべて開く
- [ ] BF記事の終了後表示に「次はスーパーSALE」の1行が出る
