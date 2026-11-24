"""12/2（水）11:00 ご飯の保温vs冷凍記事の公開スクリプト（2026-11-24 19:00 ペンネ作成・一時コピーで通し確認済み）
手順書 ops/drafts/publish_steps_2026-12-02.md の 2〜4・7 をそのまま実行する。

使い方（リポジトリ直下で）：
  git pull --rebase
  python3 ops/drafts/publish_gohan_2026-12-02.py      # 記事を移す＋下書きメモ削除＋内部リンク3か所（G1〜G3）
  python3 build.py && python3 ops/tests/content_guard.py && python3 ops/tests/mobile_check.py && python3 ops/check_affiliate.py && python3 ops/tests/site_health.py
  → 確認後 commit & push（push前に git pull --rebase）

止まる条件（何も書かずに終了する）：
- 記事がもう content/posts にある（二重実行）
- メモを消した後に残るコメントが「<!-- products: suihanki -->」1個でない／メモの文字が残っている／date が 2026-12-02 でない
- 商品枠 suihanki が make_links の KEYWORDS か products.json（リンク入り）に無い（手順書4：登録済みのため追加・make_links 実行は不要。無ければ手で確認）
- 内部リンクの差し込み位置の文が各記事で「ちょうど1か所」でない、またはリンク済み
リンクを足すだけなので、リンク先3記事の updated は変えない。
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
P = ROOT / "content/posts"
SRC = ROOT / "ops/drafts/article_gohan-hoon-vs-reitou_draft.md"
DST = P / "gohan-hoon-vs-reitou-denkidai.md"
SLUG = "gohan-hoon-vs-reitou-denkidai"

# (ファイル, 位置の行, 位置の行の直後に足す文)
EDITS = [
    # G1 冬の電気代まとめ：表の行の直後に1行
    ("fuyu-denkidai-matome.md",
     "| 在宅でお湯を何度も沸かす（ケトルとポット） | [電気ケトルと電気ポットの電気代はどっちが安い？](denki-kettle-vs-pot-denkidai.html) |\n",
     "| 余ったご飯を保温するか冷凍するか迷う | [ご飯の保温と冷凍→レンジ温め、電気代はどっち？](gohan-hoon-vs-reitou-denkidai.html) |\n"),
    # G2 ケトルとポット：「## 関連記事」の最後の箇条の直後に1行
    ("denki-kettle-vs-pot-denkidai.md",
     "- 湯たんぽのお湯を沸かす分も含めて一晩の暖房を比べるなら → [寝るときの暖房 一晩の電気代くらべ](neru-danbou-denkidai-calculator.html)\n",
     "- 炊飯器の「保温」と冷凍ご飯のレンジ温めを比べるなら → [ご飯の保温と冷凍、電気代はどっち？](gohan-hoon-vs-reitou-denkidai.html)\n"),
    # G3 電気代計算ツール：「👉 …ケトルとポット…」の直後に空行＋1段落
    ("denkidai-calculator.md",
     "👉 メーカー公表値（象印・タイガー）で1杯・1日・1ヶ月を計算した比較は → [電気ケトルと電気ポット、電気代はどっち？](denki-kettle-vs-pot-denkidai.html)\n",
     "\n👉 炊飯器の保温（1時間あたりのWh）と冷凍ご飯のレンジ温めを、何時間から冷凍が得かで比べた計算は → [ご飯の保温と冷凍→レンジ、電気代はどっち？](gohan-hoon-vs-reitou-denkidai.html)\n"),
]
MEMO_WORDS = ("下書きメモ", "公開前に確認", "ペンネ", "カンサ", "照合", "2026-11-2")


def check_product():
    """手順書4：suihanki は KEYWORDS と products.json（リンク入り）に登録済みのはず。確認だけ"""
    mk = (ROOT / "ops/make_links.py").read_text(encoding="utf-8")
    if not re.search(r'^\s*"suihanki"\s*:', mk, flags=re.M):
        sys.exit("止めた：ops/make_links.py の KEYWORDS に suihanki が無い（手順書では登録済み。KEYWORDS に1行足して make_links を実行してから再実行）")
    prod = json.loads((ROOT / "content/products.json").read_text(encoding="utf-8"))
    if "af.moshimo.com" not in (prod.get("suihanki") or {}).get("html", ""):
        sys.exit("止めた：content/products.json の suihanki にリンクが入っていない（python3 ops/make_links.py を実行してから再実行）")


def main():
    if DST.exists():
        sys.exit("止めた：記事はもう content/posts にあります（二重実行）")
    check_product()
    s = SRC.read_text(encoding="utf-8")
    if not re.search(r"^date: 2026-12-02$", s, flags=re.M):
        sys.exit("止めた：下書きの date が 2026-12-02 ではない")
    s = re.sub(r"<!-- (下書きメモ|公開前に確認).*?-->\n?", "", s, flags=re.S)
    if s.count("<!--") != 1 or s.count("<!-- products: suihanki -->") != 1:
        sys.exit(f"止めた：残ったコメントが想定外（{s.count('<!--')}個。products: suihanki の1個だけのはず）")
    left = [w for w in MEMO_WORDS if w in s]
    if left:
        sys.exit(f"止めた：メモの文字が本文に残っている：{left}")
    if "【PR】" not in s or "AI（電脳アリス）が作成" not in s:
        sys.exit("止めた：PR表記かAI作成の明記が見つからない")
    new = {}
    for f, anchor, add in EDITS:
        t = (P / f).read_text(encoding="utf-8")
        if SLUG in t or t.count(anchor) != 1:
            sys.exit(f"止めた：{f} の差し込み位置が1か所ではない（またはリンク済み）")
        new[f] = t.replace(anchor, anchor + add)
    # 書き込み（2026-11-24 カンサ監査で追加：途中で失敗したら元に戻して止まる＝中途半端な状態を残さない）
    orig = {f: (P / f).read_text(encoding="utf-8") for f in new}
    try:
        for f, t in new.items():
            (P / f).write_text(t, encoding="utf-8")
        DST.write_text(s, encoding="utf-8")
    except Exception as e:
        for f, t in orig.items():
            (P / f).write_text(t, encoding="utf-8")
        DST.unlink(missing_ok=True)
        sys.exit(f"止めた：書き込み中にエラー（元に戻しました）：{e}")
    print("OK：記事1本（gohan-hoon-vs-reitou-denkidai.md）＋内部リンク3か所（G1〜G3）。下書き（ops/drafts）は残しています")


if __name__ == "__main__":
    main()
