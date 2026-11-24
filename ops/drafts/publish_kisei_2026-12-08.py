"""12/8（火）11:00 帰省中の消し忘れ（スマートプラグ）記事の公開スクリプト（2026-11-24 19:00 ペンネ作成・一時コピーで通し確認済み）

手順書 ops/drafts/publish_steps_2026-12-08.md をそのままスクリプトにしたもの。
使い方（リポジトリ直下で）：
  git pull --rebase
  python3 ops/drafts/publish_kisei_2026-12-08.py     # 記事を移す＋内部リンク4か所（K1〜K4）
  python3 build.py && python3 ops/tests/content_guard.py && python3 ops/tests/mobile_check.py && python3 ops/check_affiliate.py && python3 ops/tests/site_health.py
止まる条件（止まったら何も書きかえない）：
  - 日本時間の今日が 2026-12-08 より前（早すぎる公開を防ぐ。試しのときだけ --allow-early。2026-11-25 03:00 監査対応）
  - 記事がもう content/posts にある（二重実行）
  - 差し込み位置の文が「ちょうど1行」でない・すでにリンク済み
  - 下書きメモを消したあとのコメントが products の1個以外
  - 文中リンク先の記事（7本）が無い／商品枠 smart-plug-monitor・smart-remote-std が KEYWORDS か products.json に無い
KEYWORDS の追加・make_links の実行は不要（手順書4。2つの枠とも登録済み・リンク入り）なので、このスクリプトは make_links.py を書きかえない。
リンク追加だけなので、各記事の `updated` は変えない。
公開前の宿題（スクリプトではやらない）：SwitchBot「暖房器具への使用について」と Nature「消し忘れアラート」の公式ページを開き、引用の文言が変わっていないか確認。
"""
import datetime, json, pathlib, re, sys

PUBLISH_DATE = datetime.date(2026, 12, 8)
ROOT = pathlib.Path(__file__).resolve().parents[2]
P = ROOT / "content/posts"
SRC = ROOT / "ops/drafts/article_kisei-rusu-smartplug_draft.md"
DST = P / "kisei-rusu-smartplug.md"
SLUG = "kisei-rusu-smartplug"
L = f"[帰省中の電気の消し忘れをスマホで確認]({SLUG}.html)"
PRODUCT_KEYS = ["smart-plug-monitor", "smart-remote-std"]
LINKED = ["smart-plug-guide", "smart-remote-guide", "smart-remote-count-shindan", "fuyu-asa-aircon-timer-smart-remote",
          "denkidai-calculator", "hikouki-mobile-battery", "fuyu-denkidai-matome"]

# (ファイル, 位置の行（行全体が一致）, その直後に足す文字列)
EDITS = [
    ("smart-plug-guide.md",  # K1
     "判断に迷ったら、**暖房器具はスマートプラグにつながない**のがいちばん安全です。",
     f"\n年末年始の帰省などで何日も家を空ける前のチェック（暖房器具はプラグを抜く・照明はスマートプラグ・エアコンはスマートリモコン）は、{L}に早見表でまとめています。"),
    ("smart-remote-guide.md",  # K2
     "外から操作したときは「本当についたか」が分からないことがあります。温度センサー付きなら、アプリで室温の変化を見て確かめやすくなります。",
     f"\n帰省などで何日も家を空ける前に、家にいるうちに「アプリからオフ→エアコンが止まる」を試しておく手順は、{L}の出発前チェックにまとめています。"),
    ("hikouki-mobile-battery.md",  # K3（表の直後なので空行を必ず入れる）
     "| 航空会社 | 国際線・他社の便は、各社の公式ページで最新ルールを確認 |",
     f"\n家を出る前の照明・エアコンの消し忘れ対策（暖房器具はプラグを抜く）は、{L}にチェックリストでまとめています。"),
    ("fuyu-denkidai-matome.md",  # K4（表の行なので空行なし）
     "| エアコンの切り忘れ・帰宅前の暖房 | [スマートリモコンの選び方](smart-remote-guide.html) ほか |",
     f"| 帰省で家を空ける前に消し忘れを防ぎたい | {L} |"),
]


def insert_after(text, anchor, add):
    lines = text.split("\n")
    idx = [i for i, x in enumerate(lines) if x == anchor]
    if len(idx) != 1:
        return None
    lines[idx[0] + 1:idx[0] + 1] = add.split("\n")
    return "\n".join(lines)


def jst_today():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date()


def main():
    if jst_today() < PUBLISH_DATE and "--allow-early" not in sys.argv:
        sys.exit(f"止めた：今日（日本時間 {jst_today()}）は公開日 {PUBLISH_DATE} より前です（試しのときだけ --allow-early）")
    if DST.exists():
        sys.exit("止めた：記事はもう content/posts にあります（二重実行）")
    # 下書き：先頭の下書きメモだけ消す（products の目印は残す）
    s = SRC.read_text(encoding="utf-8")
    if not re.search(r"^date: 2026-12-08$", s, flags=re.M):  # 2026-11-24 カンサ監査で追加（ご飯側と同じ確認）
        sys.exit("止めた：下書きの date が 2026-12-08 ではない")
    s = re.sub(r"<!-- (下書きメモ|公開前に確認).*?-->\n?", "", s, flags=re.S)
    if s.count("<!--") != 1 or s.count("<!-- products: smart-plug-monitor,smart-remote-std -->") != 1:
        sys.exit(f"止めた：残ったコメントが想定外（{s.count('<!--')}個。products の1個だけのはず）")
    for w in ("下書きメモ", "ペンネ", "照合表", "content/posts", "ops/"):
        if w in s:
            sys.exit(f"止めた：記事に下書きの文字「{w}」が残っている")
    if "【PR】" not in s or "おすすめの探し方（PR）" not in s or "AI（電脳アリス）が運営" not in s:
        sys.exit("止めた：PR表記かAI運営の明記が見つからない")
    # 文中リンク先・商品枠の確認
    missing = [x for x in LINKED if not (P / f"{x}.md").exists()]
    if missing:
        sys.exit(f"止めた：リンク先の記事が無い {missing}")
    kw = (ROOT / "ops/make_links.py").read_text(encoding="utf-8")
    prods = json.loads((ROOT / "content/products.json").read_text(encoding="utf-8"))
    for k in PRODUCT_KEYS:
        if f'"{k}"' not in kw or not prods.get(k, {}).get("html"):
            sys.exit(f"止めた：商品枠 {k} が KEYWORDS か products.json に無い（またはリンク空）")
    # 内部リンク4か所（先に全部確かめてから書く）
    new = {}
    for f, anchor, add in EDITS:
        t = (P / f).read_text(encoding="utf-8")
        if SLUG in t:
            sys.exit(f"止めた：{f} はもうこの記事にリンク済み")
        r = insert_after(t, anchor, add)
        if r is None:
            sys.exit(f"止めた：{f} の位置の行が1か所ではない")
        new[f] = r
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
    print("OK：記事1本（kisei-rusu-smartplug.md）＋内部リンク4か所（K1〜K4）。下書き（ops/drafts）は残しています")


if __name__ == "__main__":
    main()
