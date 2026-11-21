# 下書き（✅ 2026-11-21 22:10 build.py に適用済み）：BF終了後のトップ「セールの合間」案内枠

作成：2026-11-21 20:10（自走回・提案2の後半）
目的：11/25 01:59 にBF枠がトップから消えたあと、次のセール記事を出すまでトップの「期間限定」欄が空になるのを防ぐ。
**日付・「12月に開催」などは書かない**（楽天の公式発表がまだのため＝絶対ルール6）。

## 表示される文言
- バッジ：買い物メモ
- 見出し：セールの合間の冬ガジェット買い物メモ【PR】
- 説明：ブラックフライデーは終了。次の大型セールの日程は楽天市場の公式発表のあとに載せます。今のうちに電気代で候補を決めておけます
- リンク先：BF特集ページ（終了後は「次のセールでも使える」表示に自動で切り替わる）

## 試しビルドの結果（別コピーで実施、本番は未変更）
| 時刻 | トップの特集欄 |
|---|---|
| 11/24 23:00 | BF開催中の枠（今までどおり） |
| 11/25 02:30 | 「セールの合間」枠に自動で切替 |
| 2027/1/1 | 枠なし（保険の最終日 12/31 を過ぎたため） |

## 適用のしかた（build.py に下の差分を当てる）
- 当てる回：11/25 01:59 より前ならいつでも（開催中の表示には影響しない）
- スーパーSALE記事を公開するときは、SALE/SALE_ON を差し替えれば AFTER は出なくなる（SALE の期限が未来になるため）。AFTER の行はその時に消してよい

```diff
diff --git a/build.py b/build.py
index ef70ac3..b8f0d0e 100644
--- a/build.py
+++ b/build.py
@@ -390,6 +390,10 @@ SALE = ("posts/rakuten-blackfriday-memo.html", "楽天ブラックフライデ
 # 開催中（STARTS の開始〜SALE の最終時刻）だけ SALE の見出し・説明をこちらに差し替える（タグ, 見出し, 説明）
 SALE_ON = ("blackfriday-2026-11", "楽天ブラックフライデー開催中：冬ガジェット買い物メモ【PR】",
            "開催中です（11/25 01:59まで）。電気代で選ぶ暖房・加湿器など")
+# BF終了後〜次のセール記事を公開するまで、トップに出す「合間」の案内（日付は書かない。最後の要素＝保険の表示最終日）
+AFTER = ("posts/rakuten-blackfriday-memo.html", "セールの合間の冬ガジェット買い物メモ【PR】",
+         "ブラックフライデーは終了。次の大型セールの日程は楽天市場の公式発表のあとに載せます。今のうちに電気代で候補を決めておけます",
+         "2026-12-31")
 # 前回：マラソン（posts/rakuten-marathon-fuyu-kaden-list.html、〜2026-11-11T01:59）
 # 4つ目の要素（任意）＝表示する最終日（JST、この日まで先頭に出す。過ぎたら次のビルドで自動的に消える）
 TOOLS = [
@@ -476,6 +480,9 @@ def hub_block():
         head, sub = SALE_ON[1:3] if ongoing(SALE_ON[0]) else SALE[1:3]
         hub = (f'<a class="hub-main" href="{SALE[0]}"><span class="badge">期間限定</span><b>{html.escape(head)}</b>'
                f'<span>{html.escape(sub)} →</span></a><div style="height:10px"></div>') + hub
+    elif ok(AFTER[0]) and until_passed(SALE[3]) and live(AFTER):
+        hub = (f'<a class="hub-main" href="{AFTER[0]}"><span class="badge">買い物メモ</span><b>{html.escape(AFTER[1])}</b>'
+               f'<span>{html.escape(AFTER[2])} →</span></a><div style="height:10px"></div>') + hub
     if not (hub or tools):
         return ""
     return (f'<section class="hub" aria-label="特集と無料ツール">{hub}'
```
