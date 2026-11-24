# 12/14（月）11:00 電気毛布と湯たんぽ（お湯・充電式）1晩いくら？ 公開手順（2026-11-25 03:00 ペンネ 試しで通し確認済み）

**1コマンド版**：`python3 ops/drafts/publish_yutanpo_2026-12-14.py`（下の2〜4・7をそのまま実行。12/2ご飯・12/8帰省と同じ作り）

1. `git pull --rebase`
2. 下書きを移す：ops/drafts/article_yutanpo-vs-denki-blanket_draft.md → content/posts/yutanpo-vs-denki-blanket.md（date は 2026-12-14 のまま）
3. **この下書きに下書きメモは無い**（front matter から始まる）。消すものは無し
   - ⚠️ `<!-- products: denki-moufu,yutanpo,yutanpo-juden -->`（早見表の直後）は**絶対に消さない**（楽天ボタンの目印。残るコメントはこの1個だけ）
4. KEYWORDS の追加は**不要**：denki-moufu・yutanpo・yutanpo-juden の3枠とも ops/make_links.py の KEYWORDS と content/products.json（リンク入り）に登録済み（yutanpo-juden は 11/24 追加）。make_links の実行もいらない
5. `python3 build.py` → `python3 ops/tests/content_guard.py`・`python3 ops/tests/mobile_check.py`・`python3 ops/check_affiliate.py`・`python3 ops/tests/site_health.py`
6. 期待値（12/14 11:30 に時計をずらした試し。11/30大掃除→12/2ご飯→12/8帰省→（12/10鍋）→この記事の順）：
   | 状態 | 記事 | 楽天ボタン | 公開ページ |
   |---|---|---|---|
   | 12/8 帰省まで | 39 | 165 | 42 |
   | ＋この記事（鍋なし） | **40** | **168** | 43 |
   | 12/10 鍋も公開済みの場合 | 40 | 167 | 43 |
   | ＋この記事（鍋あり） | **41** | **170** | 44 |
   - この記事のボタンは**3個**（電気毛布・湯たんぽ・充電式湯たんぽ）
   - content_guard OK／mobile_check 問題0件（4画面）／site_health 問題0件／check_affiliate OK（鍋なしなら未使用の枠 cassette-konro・takujo-ih の2つ＝鍋記事用。鍋ありなら0）
   - 【PR】1・「AI（電脳アリス）が作成」1・実機レビューでない旨あり・`#pr-osusume` の飛び先あり・表6つ
   - サイトマップ・トップ・RSS に各1件、アイキャッチSVG（docs/posts/yutanpo-vs-denki-blanket.svg）・OGP画像（docs/og/yutanpo-vs-denki-blanket.png）あり
   - 文中リンク6本（neru-danbou-denkidai-calculator・denki-blanket-denkidai-1jikan・denki-kettle-vs-pot-denkidai・futon-kansouki-denkidai・smart-plug-guide・fuyu-denkidai-matome）の先あり
   - HTMLに 下書きメモ・ペンネ・カンサ・照合・ops/・content/posts が0件（「2026-11-24」は記事本文の確認日なので出てよい）
7. 同時に内部リンク4か所（下）。**リンク追加だけなので `updated` は変えない**
8. 確認後 commit & push（push前に `git pull --rebase`）

## 止まる条件（止まったら何も書きかえない）
- 記事がもう content/posts にある（二重実行）
- 日本時間の今日が 12/14 より前（試しのときだけ `--allow-early`）
- 下書きの date が 2026-12-14 でない／コメントが products の1個以外／PR・AI作成・実機レビューでない旨が無い
- 文中リンク先6本のどれかが無い／3枠のどれかが KEYWORDS か products.json（リンク入り）に無い
- 差し込み位置の行が「ちょうど1行」でない、またはリンク済み
- 書き込み途中のエラー → 全部元に戻して止まる（試しで、2回目の書き込みをわざと失敗させ、content/posts の全ファイルが元とハッシュ一致を確認）

## 内部リンク Y1〜Y4（寝具・暖房系だけ。大掃除・ご飯・帰省・鍋・スマホ寒さのスクリプトが触る記事とは重ならない）
位置の行は 2026-11-25 時点で各記事に1行だけ（行全体一致）。

### Y1. neru-danbou-denkidai-calculator.md（寝るときの暖房 計算ツール）Q「湯たんぽがいちばん安いなら…」の回答（`A. 上の早見表の前提（単価31円/kWh）では湯たんぽ（約5.9円）が…の節にあります。`）の**直後**に空行＋1段落
```

実際の製品のメーカー公表値（電気毛布の温度段階ごとの消費電力量・充電式湯たんぽの蓄熱時間・ケトルの沸とう時間）で1晩を計算した例は、[電気毛布と湯たんぽ（お湯・充電式）1晩いくら？](yutanpo-vs-denki-blanket.html)にまとめています。お湯の量・W数の前提がこのツールの初期値と違うため、金額の順番も同じにはなりません。
```
（11/24 カンサ監査 A17「前提が違うので金額も違うと一言添える」に対応）

### Y2. denki-moufu-kotatsu-denkidai-telework.md（電気毛布・こたつ）「寝るときに使う場合は、[寝るときの暖房 一晩の電気代くらべ]…比べられます。」の**直後**に空行＋1段落（その下の `<!-- products: yutanpo -->` はそのまま）
```

仮定の例ではなく実際の製品の数字（電気毛布2機種・充電式湯たんぽ3機種のメーカー公表値）で比べたいときは、[電気毛布と湯たんぽ（お湯・充電式）1晩いくら？](yutanpo-vs-denki-blanket.html)を見てください。
```

### Y3. denki-blanket-denkidai-1jikan.md（電気ブランケット）「エアコン・こたつと比べると？」の箇条の最後（`- 寝る前に布団だけ温めたいなら、[布団乾燥機の電気代…]も参考にしてください`）の**直後**に1行
```
- 寝るときの電気毛布を、湯たんぽ（お湯・充電式）と1晩の電気代で比べるなら → [電気毛布と湯たんぽ（お湯・充電式）1晩いくら？](yutanpo-vs-denki-blanket.html)
```

### Y4. futon-kansouki-denkidai.md（布団乾燥機）「電気毛布・部屋干しとの使い分け」の `- 一晩の暖房を並べて比べたいときは[寝るときの暖房 一晩の電気代くらべ（計算ツール）]…へ` の**直後**に1行
```
- 電気毛布と湯たんぽ（お湯・充電式）を、メーカー公表値で1晩いくらか比べた例は[電気毛布と湯たんぽ（お湯・充電式）1晩いくら？](yutanpo-vs-denki-blanket.html)にあります
```

## 既存記事との役割分け（重複対策・11/25に下書きへ反映済み）
- 計算ツール（neru-danbou）＝自分のW数・お湯の量を入れる／電気毛布・こたつ（denki-moufu-kotatsu）＝仮定のW数で計算方法／電気ブランケット＝ひざ掛け・着る毛布のW数別
- この記事＝**実在の製品のメーカー公表値だけ**で1晩を計算（電気毛布の温度段階別Wh、充電式湯たんぽ3機種は他記事に無い）
- タイトル・説明文を「実際の製品のメーカー公表値」に寄せ、冒頭に「この記事の役割」段落（ツール・電気ブランケットへのリンク、ツール初期値5.9円と前提が違う旨）を追加

## 12/14の回の宿題（スクリプトではやらない）
- 公式ページの数値が変わっていないかの再確認（11/25は WebFetch が許可待ちで開けず。11/24 のペンネ照合＋カンサ監査の2回で一致確認済み）。変わっていたら公開を止めて直す
