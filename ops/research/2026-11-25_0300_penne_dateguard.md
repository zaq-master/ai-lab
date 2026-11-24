# 公開スクリプト3本に「公開日前は止まる」確認を追加（2026-11-25 03時台／ペンネ）

元の監査：ops/audit/2026-11-25_0300_scripts_audit.md の要対応3（未修正だったNG）
**結果：3本とも鍋（publish_nabe_2026-12-10.py）と同じ作りで追加し、作業用コピーで確認済み。本番の content/ docs/ は変えていない。commit／push はしていない（司令塔が行う）**

## 直したもの

| ファイル | 内容 |
|---|---|
| ops/drafts/publish_oosouji_2026-11-30.py | `PUBLISH_DATE = datetime.date(2026, 11, 30)`・`jst_today()`（日本時間の日付）を追加。main() の最初で「今日 < 公開日 かつ `--allow-early` なし」なら何も書かずに止まる。説明文にも1行 |
| ops/drafts/publish_gohan_2026-12-02.py | 同じ（12/2） |
| ops/drafts/publish_kisei_2026-12-08.py | 同じ（12/8） |
| ops/drafts/publish_steps_2026-11-30.md／12-02.md／12-08.md | 見出しの直後に1行「日本時間の今日が公開日より前なら何も書かずに止まる（試しのときだけ `--allow-early`）」 |

止める文言は鍋と同じ：`止めた：今日（日本時間 YYYY-MM-DD）は公開日 YYYY-MM-DD より前です（試しのときだけ --allow-early）`

## 確認（作業用コピー：scratchpad/guard/ai-lab）

(a) 今の時計（日本時間 11/25）で6本すべて実行 → **6本とも止まった（終了コード1）**。content/・docs/・ops/make_links.py の全ファイルのハッシュが実行前後で**一致**。

(b) 時計をずらして順に実行（scratchpad/guard/run_guard_chain.sh、時計のずらし方は scratchpad/chain の sitecustomize.py と同じ FAKE_NOW 方式）。各本で「前日23:59 → 止まりハッシュ不変」を確かめてから「当日11:30 → 実行」：

| 公開日 | 記事 | 前日23:59 | 当日 | 記事数 | 楽天ボタン | 点検4種 |
|---|---|---|---|---|---|---|
| 11/30 | 大掃除まとめ | 止まった | OK | 37 | 162 | 問題0 |
| 12/2 | ご飯の保温vs冷凍 | 止まった | OK | 38 | 163 | 問題0 |
| 12/8 | 帰省中の消し忘れ | 止まった | OK | 39 | 165 | 問題0 |
| 12/10 | 鍋 IH vs カセット | 止まった | OK | 40 | 167 | 問題0 |
| 12/14 | 湯たんぽ | 止まった | OK | 41 | 170 | 問題0 |
| 12/16 | スマホ寒さ | 止まった | OK | 42 | 171 | 問題0 |

点検4種＝content_guard／check_affiliate／site_health（最後45ページ問題0）／mobile_check（最後45ページ×4画面 問題0）。最後は未使用の商品枠0。
ログ：scratchpad/guard/chain_log.txt

## メモ
- 作業ツリーにある ops/drafts/article_reizouko-tsumekomi_draft.md の変更と publish_reizouko_2026-12-21.py は別の担当のもの（今回は触っていない・試しにも含めていない）。12/21 のスクリプトには同じ日付の確認がすでに入っている（PUBLISH_DATE 2026-12-21・--allow-early）ことだけ確認した
