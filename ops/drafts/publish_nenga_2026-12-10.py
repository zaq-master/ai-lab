"""12/10（木）11:00 年賀状を家のプリンターで刷ると1枚いくら？ 記事の公開スクリプト（2026-11-25 ペンネ作成・作業用コピーで案Cの順に通し確認済み）

手順書 ops/drafts/publish_steps_2026-12-10_nenga.md をそのままスクリプトにしたもの（作りは publish_illumi_2026-12-02.py と同じ。
この記事は新しい商品枠 printer-ink を使うので、KEYWORDS と products.json への追加・make_links の実行もこの中で行う）。
公開日は11/30のAI経営会議で決める：案C＝12/10（既定）／案B＝12/9（--date 2026-12-09）／案A＝見送り（実行しない）。
使い方（リポジトリ直下で）：
  git pull --rebase
  python3 ops/drafts/publish_nenga_2026-12-10.py                     # 案C（12/10）
  python3 ops/drafts/publish_nenga_2026-12-10.py --date 2026-12-09   # 案B（12/9）
  python3 build.py && python3 ops/tests/content_guard.py && python3 ops/tests/mobile_check.py && python3 ops/check_affiliate.py && python3 ops/tests/site_health.py
  → 確認後 commit & push（push前に git pull --rebase）。ops/make_links.py と content/products.json も変わるので一緒に commit

止まる条件（止まったら何も書きかえない）：
  - --date が 2026-12-09・2026-12-10 以外（年賀状の目安12/27に間に合う案B・案Cの日付だけ受け付ける）
  - 日本時間の今日が公開日より前（早すぎる公開を防ぐ。試しのときだけ --allow-early）
  - 記事がもう content/posts にある（二重実行）
  - 下書きの front matter に date の行が1つでない（date は公開日に書きかえて移す）
  - メモ（先頭の「下書きメモ」）を消した後に残るコメントが「<!-- products: printer-ink -->」1個でない／メモの文字が残っている
  - 【PR】・「プリンターの探し方（PR）」・「AI（電脳アリス）が」・「実機レビューではありません」 が無い
  - 本文に楽天・もしもの直書きURLがある（check_affiliate が止めるため）
  - 文中リンク先（3記事）が無い
  - printer-ink が KEYWORDS に別のキーワードで登録済み（勝手に上書きしない）
  - 内部リンクの差し込み位置の行が各記事で「行全体が一致してちょうど1行」でない、またはすでにリンク済み
  - make_links 実行後に printer-ink のリンクが入っていない（このときは全部元に戻す）
リンク追加だけなので、リンク元の各記事の `updated` は変えない。
Y1・Y2 のリンク元2記事（telework-gadget-present-erabikata・desk-qol-guide）は、他の公開スクリプト
（oosouji/illumi/kisei/nabe/yutanpo/samusa/reizouko/gohan/benza）がどれも触らない記事であることを確認済み（11/25）。
"""
import datetime, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
P = ROOT / "content/posts"
SRC = ROOT / "ops/drafts/article_nenga-ink-dai_draft.md"
DST = P / "nenga-ink-dai.md"
SLUG = "nenga-ink-dai"
DEFAULT_DATE = datetime.date(2026, 12, 10)          # 案C
ALLOWED_DATES = (datetime.date(2026, 12, 9), datetime.date(2026, 12, 10))  # 案B・案C
L = f"[年賀状を家のプリンターで刷ると1枚いくら？]({SLUG}.html)"
PRODUCTS = "<!-- products: printer-ink -->"
NEW_KEY, NEW_KW, NEW_LABEL = "printer-ink", "プリンター 年賀状", "年賀状が刷れるプリンター"
OLD_KEYS = []
LINKED = ["denkidai-calculator", "telework-gadget-present-erabikata", "desk-qol-guide"]
MEMO_WORDS = ("下書きメモ", "公開前に確認", "ペンネ", "カンサ", "照合", "2026-11-2", "content/posts", "ops/", "check_affiliate", "未登録", "仮置き")
NEED = ("【PR】", "プリンターの探し方（PR）", 'id="pr-osusume"', "AI（電脳アリス）が", "実機レビューではありません")
MK = ROOT / "ops/make_links.py"
PJ = ROOT / "content/products.json"

# (ファイル, 位置の行（行全体が一致）, "after"=その行の直後／"before"=その行の直前, 足す文字列, 必須か)
EDITS = [
    # Y1 在宅ワークの人へのプレゼント：まとめの最後の段落（デスク環境・冬の電気代への案内）の直後に空行＋1段落
    ("telework-gadget-present-erabikata.md",
     "デスクまわりの困りごとをまとめて見直したい場合は、[在宅ワークのデスク環境を快適にするガジェット7カテゴリ](desk-qol-guide.html)もどうぞ。冬の暖房の電気代は[冬の電気代まとめ](fuyu-denkidai-matome.html)で整理しています。",
     "after",
     f"\n年末に年賀状を家のプリンターで刷る場合の費用（インク代＋はがき代）の出し方は、{L}にまとめています。",
     True),
    # Y2 デスク環境7カテゴリ：記事の最後の段落（プレゼント記事への案内）の直後に空行＋1段落
    ("desk-qol-guide.md",
     "在宅ワークをしている家族や友人に贈るものを探している場合は、[在宅ワークの人へのプレゼント、ガジェットの選び方](telework-gadget-present-erabikata.html)で、困りごと別に選び方と「買う前に確かめる6項目」をまとめています。",
     "after",
     f"\nデスクのプリンターで年賀状を刷るときの1枚あたりの費用は、{L}で計算式と早見表にしています。",
     True),
]


def jst_today():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date()


def publish_date():
    if "--date" not in sys.argv:
        return DEFAULT_DATE
    i = sys.argv.index("--date")
    try:
        d = datetime.date.fromisoformat(sys.argv[i + 1])
    except (IndexError, ValueError):
        sys.exit("止めた：--date は 2026-12-09 の形で書く")
    if d not in ALLOWED_DATES:
        sys.exit(f"止めた：--date {d} は受け付けない（案B＝2026-12-09／案C＝2026-12-10 のどちらか。年賀状は12/27の目安より前に出す）")
    return d


def insert(text, anchor, where, add):
    lines = text.split("\n")
    idx = [i for i, x in enumerate(lines) if x == anchor]
    if len(idx) != 1:
        return None
    at = idx[0] + 1 if where == "after" else idx[0]
    lines[at:at] = add.split("\n")
    return "\n".join(lines)


def add_keyword(mk):
    """KEYWORDS の閉じ括弧の直前に1行足した make_links.py の文字列を返す（もう同じ行があれば None）"""
    m = re.search(rf'^\s*"{re.escape(NEW_KEY)}"\s*:\s*"(.*?)"', mk, flags=re.M)
    if m:
        if m.group(1) != NEW_KW:
            sys.exit(f"止めた：KEYWORDS に {NEW_KEY} が別のキーワード「{m.group(1)}」で登録済み（上書きしない。手で確認）")
        return None
    lines = mk.split("\n")
    try:
        start = lines.index("KEYWORDS = {")
        end = lines.index("}", start)
    except ValueError:
        sys.exit("止めた：make_links.py の KEYWORDS = { … } の形が見つからない（手で1行足す）")
    lines[end:end] = [f'    "{NEW_KEY}": "{NEW_KW}",']
    return "\n".join(lines)


def main():
    pd = publish_date()
    if jst_today() < pd and "--allow-early" not in sys.argv:
        sys.exit(f"止めた：今日（日本時間 {jst_today()}）は公開日 {pd} より前です（試しのときだけ --allow-early）")
    if DST.exists():
        sys.exit("止めた：記事はもう content/posts にあります（二重実行）")
    s = SRC.read_text(encoding="utf-8")
    # 下書きメモを消す。products の目印は残す
    s = re.sub(r"\n?<!--\s*(下書きメモ|公開前に確認).*?-->\n?", "\n", s, flags=re.S)
    s = re.sub(r"\n{3,}", "\n\n", s).strip("\n") + "\n"
    s = s.replace("---\n\n**【PR】", "---\n**【PR】", 1)  # front matter 直後の空行を元どおり詰める
    if not s.startswith("---\n"):
        sys.exit("止めた：メモを消したあと、ファイルの先頭が front matter の --- になっていない")
    fm_end = s.index("\n---\n", 4)
    fm = s[:fm_end]
    if len(re.findall(r"^date: \d{4}-\d{2}-\d{2}$", fm, flags=re.M)) != 1:
        sys.exit("止めた：下書きの front matter に date の行が1つではない")
    s = re.sub(r"^date: \d{4}-\d{2}-\d{2}$", f"date: {pd}", fm, count=1, flags=re.M) + s[fm_end:]
    if s.count("<!--") != 1 or s.count(PRODUCTS) != 1:
        sys.exit(f"止めた：残ったコメントが想定外（{s.count('<!--')}個。products の1個だけのはず）")
    left = [w for w in MEMO_WORDS if w in s]
    if left:
        sys.exit(f"止めた：メモの文字が本文に残っている：{left}")
    for need in NEED:
        if need not in s:
            sys.exit(f"止めた：記事に「{need}」が見つからない（PR表記・AI作成の明記）")
    if re.search(r"https?://[^\s\"\)]*(moshimo|hb\.afl\.rakuten|item\.rakuten|search\.rakuten)", s):
        sys.exit("止めた：本文に楽天・もしもの直書きURLがある")
    missing = [x for x in LINKED if not (P / f"{x}.md").exists()]
    if missing:
        sys.exit(f"止めた：文中リンク先の記事が無い {missing}")
    mk = MK.read_text(encoding="utf-8")
    pj_text = PJ.read_text(encoding="utf-8")
    prods = json.loads(pj_text)
    for k in OLD_KEYS:
        if not re.search(rf'^\s*"{re.escape(k)}"\s*:', mk, flags=re.M) or "af.moshimo.com" not in (prods.get(k) or {}).get("html", ""):
            sys.exit(f"止めた：商品枠 {k} が KEYWORDS か products.json に無い（またはリンク空）")
    new_mk = add_keyword(mk)
    need_pj = NEW_KEY not in prods
    # 内部リンク（先に全部確かめてから書く）
    new, skipped = {}, []
    for f, anchor, where, add, required in EDITS:
        if not (P / f).exists():
            if required:
                sys.exit(f"止めた：リンク元の記事 {f} が無い")
            skipped.append(f)
            continue
        t = (P / f).read_text(encoding="utf-8")
        if SLUG in t:
            sys.exit(f"止めた：{f} はもうこの記事にリンク済み")
        r = insert(t, anchor, where, add)
        if r is None:
            sys.exit(f"止めた：{f} の位置の行が1か所ではない（文が変わった可能性。手順書の「位置の行」で検索）")
        new[f] = r
    # 書き込み（途中で失敗したら元に戻して止まる＝中途半端な状態を残さない）
    orig = {f: (P / f).read_text(encoding="utf-8") for f in new}
    try:
        if new_mk is not None:
            MK.write_text(new_mk, encoding="utf-8")
        if need_pj:
            prods[NEW_KEY] = {"label": NEW_LABEL, "html": ""}
            PJ.write_text(json.dumps(prods, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        out = subprocess.run([sys.executable, str(MK)], cwd=ROOT, capture_output=True, text=True)
        if out.returncode != 0:
            raise RuntimeError(f"make_links.py が失敗：{out.stderr.strip()[-300:]}")
        h = (json.loads(PJ.read_text(encoding="utf-8")).get(NEW_KEY) or {}).get("html", "")
        if "af.moshimo.com" not in h or "a_id=5877487" not in h:
            raise RuntimeError(f"make_links 実行後も {NEW_KEY} にリンクが入っていない")
        for f, t in new.items():
            (P / f).write_text(t, encoding="utf-8")
        DST.write_text(s, encoding="utf-8")
    except BaseException as e:
        MK.write_text(mk, encoding="utf-8")
        PJ.write_text(pj_text, encoding="utf-8")
        for f, t in orig.items():
            (P / f).write_text(t, encoding="utf-8")
        DST.unlink(missing_ok=True)
        sys.exit(f"止めた：書き込み中にエラー（make_links.py・products.json・記事を元に戻しました）：{e}")
    msg = (f"OK：記事1本（{DST.name}・date {pd}）＋商品枠 {NEW_KEY}（KEYWORDS{'追加' if new_mk else 'は登録済み'}・products.json"
           f"{'追加' if need_pj else 'は登録済み'}・make_links 実行：{out.stdout.strip()}）"
           f"＋内部リンク{len(new)}か所（{'・'.join(new)}）。下書き（ops/drafts）は残しています")
    if skipped:
        msg += f"\n注意：{'・'.join(skipped)} が無いので飛ばしました"
    print(msg)


if __name__ == "__main__":
    main()
