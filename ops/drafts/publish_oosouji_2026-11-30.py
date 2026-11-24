"""11/30（月）11:00 大掃除まとめ記事の公開スクリプト（2026-11-24 18:00 作成・一時コピーで通し確認済み）

使い方（リポジトリ直下で）：
  git pull --rebase
  python3 ops/drafts/publish_oosouji_2026-11-30.py      # 記事を移す＋内部リンク6か所＋逆方向1か所
  python3 build.py && python3 ops/tests/content_guard.py && python3 ops/tests/mobile_check.py && python3 ops/check_affiliate.py
差し込み位置の文が「ちょうど1か所」でなければ何も書かずに止まる（二重実行・文の変更を防ぐ）。
日本時間の今日が 2026-11-30 より前なら何も書かずに止まる（早すぎる公開の防止。試しのときだけ --allow-early。2026-11-25 03:00 監査対応）。
"""
import datetime, pathlib, re, sys

PUBLISH_DATE = datetime.date(2026, 11, 30)
ROOT = pathlib.Path(__file__).resolve().parents[2]
P = ROOT / "content/posts"
SRC = ROOT / "ops/drafts/article_oosouji-matome_draft.md"
DST = P / "oosouji-kaden-oteire-matome.md"
L = "[大掃除で家電のお手入れ3つ](oosouji-kaden-oteire-matome.html)"
KETSURO = f"。毎朝の結露取りの道具3つは{L}で比べています"

# (ファイル, 探す文, 置きかえ後)
EDITS = [
    ("aircon-danbou-denkidai-calculator.md",
     "- **フィルターを掃除する**：**月1〜2回**が目安（機種ごとの取扱説明書を確認）\n",
     f"- **フィルターを掃除する**：**月1〜2回**が目安（機種ごとの取扱説明書を確認）。年末にまとめて掃除するときの手順は{L}に整理しています\n"),
    ("heater-denkidai-hikaku.md",
     "| フィルターを掃除する | エアコンのフィルターは**月1〜2回**（機種ごとの取扱説明書を確認） | 資源エネルギー庁 |\n\n",
     f"| フィルターを掃除する | エアコンのフィルターは**月1〜2回**（機種ごとの取扱説明書を確認） | 資源エネルギー庁 |\n\nエアコンのフィルター掃除を年末の大掃除でまとめてやる手順は{L}へ。\n\n"),
    ("humidifier-electricity-cost-telework.md",
     "使う前に取扱説明書を確認してください。\n",
     f"使う前に取扱説明書を確認してください。年末の大掃除で加湿器・エアコン・窓をまとめて手入れするときの早見表は{L}にあります。\n"),
    ("mado-danetsu-sheet-chintai-ketsuro.md",
     "窓や窓枠の水滴は拭き取ってください\n", f"窓や窓枠の水滴は拭き取ってください{KETSURO}\n"),
    ("telework-ketsuro-taisaku-roten.md",
     "窓や窓枠の水滴は拭き取ってください\n", f"窓や窓枠の水滴は拭き取ってください{KETSURO}\n"),
    ("robot-cleaner-denkidai.md",
     "（パナソニック MC-RS1）。\n",
     f"（パナソニック MC-RS1）。手で掃除する家電（エアコンのフィルター・加湿器・窓の結露）の手順は{L}にまとめています。\n"),
]
REVERSE = ("お手入れは各製品の取扱説明書の手順で行ってください。\n",
           "お手入れは各製品の取扱説明書の手順で行ってください。ロボット掃除機を動かす前の床の片付けは[ロボット掃除機の電気代と大掃除前のチェック表](robot-cleaner-denkidai.html)へ。\n")


def jst_today():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date()


def main():
    if jst_today() < PUBLISH_DATE and "--allow-early" not in sys.argv:
        sys.exit(f"止めた：今日（日本時間 {jst_today()}）は公開日 {PUBLISH_DATE} より前です（試しのときだけ --allow-early）")
    if DST.exists():
        sys.exit("止めた：記事はもう content/posts にあります（二重実行）")
    s = SRC.read_text(encoding="utf-8")
    s = re.sub(r"<!-- (下書きメモ|公開前に確認).*?-->\n?", "", s, flags=re.S)
    if s.count(REVERSE[0]) != 1:
        sys.exit("止めた：まとめ記事の逆方向リンクの位置が1か所ではない")
    s = s.replace(*REVERSE)
    if s.count("<!--") != 3 or s.count("<!-- products:") != 3:
        sys.exit(f"止めた：残ったコメントが想定外（{s.count('<!--')}個、products は3個のはず）")
    new = {}
    for f, old, rep in EDITS:
        t = (P / f).read_text(encoding="utf-8")
        if "oosouji-kaden-oteire-matome" in t or t.count(old) != 1:
            sys.exit(f"止めた：{f} の差し込み位置が1か所ではない（またはリンク済み）")
        new[f] = t.replace(old, rep)
    DST.write_text(s, encoding="utf-8")
    for f, t in new.items():
        (P / f).write_text(t, encoding="utf-8")
    print("OK：記事1本＋内部リンク6か所＋逆方向1か所。下書き（ops/drafts）は残しています")


if __name__ == "__main__":
    main()
