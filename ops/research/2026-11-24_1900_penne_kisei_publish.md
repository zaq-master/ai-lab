# 12/8 帰省の留守宅チェック記事 公開スクリプト（2026-11-24 19:00 ペンネ）

## 成果物
- ops/drafts/publish_kisei_2026-12-08.py（publish_steps_2026-12-08.md の手順2〜4・8をスクリプト化）
  - 下書き → content/posts/kisei-rusu-smartplug.md（date 2026-12-08 のまま）。先頭の下書きメモ1つだけ消す → 残るコメントが `<!-- products: smart-plug-monitor,smart-remote-std -->` の1個でなければ止める
  - 内部リンク K1 smart-plug-guide／K2 smart-remote-guide／K3 hikouki-mobile-battery（表の後に空行＋段落）／K4 fuyu-denkidai-matome（表の行）。位置の行が「行全体で一致・ちょうど1行」でなければ止める。すでにリンク済みでも止める。4か所とも確かめてから書く（途中で止まったら何も変わらない）
  - 二重実行（記事がもう content/posts にある）で止める
  - 追加の安全確認：記事に下書きの文字（下書きメモ・ペンネ・照合表・content/posts・ops/）が無いこと、【PR】・「おすすめの探し方（PR）」・「AI（電脳アリス）が運営」があること、文中リンク先7記事があること、商品枠2つが KEYWORDS と products.json（リンク入り）にあること
  - KEYWORDS 追加・make_links 実行は**しない**（手順書4のとおり不要。smart-plug-monitor・smart-remote-std とも登録済み・リンク入りを11/24に確認）
  - `updated` は変えない（リンク追加だけのため）
- 本体の content/・docs/ は変更していない。commit/push なし

## 試し（scratchpad に cp -a、build.jst_now／jst_today を 2026-12-08 11:30 に固定して build.main()）
| 状態 | 記事 | 公開ページ | 楽天ボタン | content_guard | check_affiliate | site_health | mobile_check |
|---|---|---|---|---|---|---|---|
| 何もしない（12/8時点の基準） | 36 | — | 157 | — | — | — | — |
| 大掃除→ご飯（実スクリプト publish_gohan_2026-12-02.py）→この記事 | **39** | **42** | **165** | OK | OK | 問題0 | 42ページ×4画面 問題0 |
| 大掃除→ご飯（手順書どおり手で適用）→この記事 | 39 | 42 | 165 | OK | OK | 問題0 | 問題0 |
| この記事だけ（大掃除・ご飯なし） | 37 | 40 | 159 | OK | OK | 問題0 | 40ページ×4画面 問題0 |
- 手順書7の期待値（39本・42ページ・163→165・各チェック0件）と一致
- check_affiliate の「未使用の枠」3つ（cassette-konro・takujo-ih・yutanpo-juden）は、まだ公開していない他の下書き用の枠で、この記事とは無関係（エラーではない）
- 公開HTML：下書きの文字0件／`id="pr-osusume"` 1個／表3つ／楽天ボタン2個／【PR】・AI運営の明記あり／サイトマップ・トップ・RSSに載る／アイキャッチSVG・OGP画像（og/kisei-rusu-smartplug.png）あり／文中リンク先7記事すべてあり／K1〜K4の4記事からリンクあり
- 止まる動作：2回目の実行 →「二重実行」で止まる（exit 1）。記事だけ消して再実行 →「smart-plug-guide.md はもうリンク済み」で止まり、記事は作られない

## 12/2 ご飯記事との衝突（結論：衝突しない）
- 重なるのは fuyu-denkidai-matome.md の早見表だけ。K4 は75行目（エアコンの切り忘れ）の後、G1 は76行目（ケトルとポット）の後で、**位置の行が別**。どちらのスクリプトも「行の後に足す」だけなので、もう一方の位置の行は消えず、1か所のまま
- 実スクリプトで「ご飯→この記事」「この記事→ご飯」の両方の順で試し、どちらも止まらずに適用できた。仕上がりは表の順に「エアコン／帰省（K4）／ケトル／ご飯（G1）」
- それ以外のファイル（G2 ケトル記事・G3 電気代計算ツール、大掃除の6記事）と K1〜K3 は重ならない
- 手順書8の「行番号は11/24時点」の注意どおり、11/30・12/2の公開後は行番号がずれるが、スクリプトは文で探すので影響なし

## 公開日（12/8 11:00）に人がやること
1. `git pull --rebase` → `python3 ops/drafts/publish_kisei_2026-12-08.py`
2. SwitchBot「暖房器具への使用について」と Nature「消し忘れアラート」の公式ページを開き、引用の文言が変わっていないか確認（スクリプトではやらない。11/24の試しでも未確認）
3. `python3 build.py` → content_guard・mobile_check・check_affiliate・site_health → 期待値は上の表（39本・165個・問題0）
4. commit & push（push前に `git pull --rebase`）
