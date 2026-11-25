"""12/30（水）11:00 トイレの便座（温水洗浄便座）冬の電気代 記事の公開スクリプト（2026-11-25 ペンネ作成・作業用コピーで案Cの順に通し確認済み）

手順書 ops/drafts/publish_steps_2026-12-30_benza.md をそのままスクリプトにしたもの（作りは publish_illumi_2026-12-02.py・publish_nenga_2026-12-10.py と同じ。
この記事は新しい商品枠 benza-cover を使うので、KEYWORDS と products.json への追加・make_links の実行もこの中で行う）。
公開日は11/30のAI経営会議で決める：案C＝12/30（既定）／案A・案B＝12/28（--date 2026-12-28）。
使い方（リポジトリ直下で）：
  git pull --rebase
  python3 ops/drafts/publish_benza_2026-12-30.py                     # 案C（12/30）
  python3 ops/drafts/publish_benza_2026-12-30.py --date 2026-12-28   # 案A・案B（12/28）
  python3 build.py && python3 ops/tests/content_guard.py && python3 ops/tests/mobile_check.py && python3 ops/check_affiliate.py && python3 ops/tests/site_health.py
  → 確認後 commit & push（push前に git pull --rebase）。ops/make_links.py と content/products.json も変わるので一緒に commit

止まる条件（止まったら何も書きかえない）：
  - --date が 2026-12-28・2026-12-30 以外
  - 日本時間の今日が公開日より前（早すぎる公開を防ぐ。試しのときだけ --allow-early）
  - 記事がもう content/posts にある（二重実行）
  - 下書きの front matter に date の行が1つでない（date は公開日に書きかえて移す）
  - メモ（front matter の前にある「下書きメモ」）を消した後、先頭が --- でない／残るコメントが「<!-- products: benza-cover -->」1個でない／メモの文字が残っている
  - 【PR】・「おすすめの探し方（PR）」・「AI（電脳アリス）が」・「実機で測った記録ではありません」 が無い
  - 本文に楽天・もしもの直書きURLがある（check_affiliate が止めるため）
  - 文中リンク先（4記事）が無い
  - benza-cover が KEYWORDS に別のキーワードで登録済み（勝手に上書きしない）
  - 内部リンクの差し込み位置の行が各記事で「行全体が一致してちょうど1行」でない、またはすでにリンク済み
  - make_links 実行後に benza-cover のリンクが入っていない（このときは全部元に戻す）
リンク追加だけなので、リンク元の各記事の `updated` は変えない。
B1〜B3 の位置の行は、他の公開スクリプト（oosouji/illumi/kisei/nabe/yutanpo/samusa/reizouko/gohan/nenga）の位置の行・足す行と重ならないことを確認済み（11/25）。
"""
import datetime, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
P = ROOT / "content/posts"
SRC = ROOT / "ops/drafts/article_benza-denkidai_draft.md"
DST = P / "benza-denkidai.md"
SLUG = "benza-denkidai"
DEFAULT_DATE = datetime.date(2026, 12, 30)          # 案C
ALLOWED_DATES = (datetime.date(2026, 12, 28), datetime.date(2026, 12, 30))  # 案A・B／案C
L = f"[トイレの便座（温水洗浄便座）冬の電気代、ふた・温度設定でいくら変わる？]({SLUG}.html)"
PRODUCTS = "<!-- products: benza-cover -->"
NEW_KEY, NEW_KW, NEW_LABEL = "benza-cover", "便座カバー 洗える", "洗える便座カバー"
OLD_KEYS = []
LINKED = ["denkidai-calculator", "fuyu-denkidai-matome", "heater-denkidai-hikaku", "winter-heating-shindan"]
MEMO_WORDS = ("下書きメモ", "公開前に確認", "ペンネ", "カンサ", "照合", "2026-11-2", "content/posts", "ops/", "check_affiliate", "未登録", "仮置き")
NEED = ("【PR】", "おすすめの探し方（PR）", 'id="pr-osusume"', "AI（電脳アリス）が", "実機で測った記録ではありません")
MK = ROOT / "ops/make_links.py"
PJ = ROOT / "content/products.json"

# (ファイル, 位置の行（行全体が一致）, "after"=その行の直後／"before"=その行の直前, 足す文字列, 必須か)
EDITS = [
    # B1 冬の電気代まとめ：悩み別の早見表「部屋が乾燥する」の行の直後に1行（表の行なので空行なし）
    #   （I3＝電気代をすぐ知りたいの直後、R1＝除湿機の直後、K4＝エアコンの直後、G1＝ケトルの直後、N1＝スマートプラグの直前 とは別の行）
    ("fuyu-denkidai-matome.md",
     "| 部屋が乾燥する | [加湿器の電気代](humidifier-electricity-cost-telework.html)／[加湿量 計算ツール](kashitsu-ryo-calculator.html) |",
     "after",
     f"| トイレの便座の電気代を減らしたい | {L} |",
     True),
    # B2 電気代計算ツール：「## 関連記事」のホットカーペットの行の直後に1行
    #   （N2 鍋＝関連記事の最後の行の直後、I2・R2＝よくある質問、G3＝ケトルの計算例 とは別の場所）
    ("denkidai-calculator.md",
     "- ホットカーペットを畳数・強弱別に見るなら → [ホットカーペットの電気代 早見表](hot-carpet-denkidai.html)",
     "after",
     f"- トイレの温水洗浄便座（ふた・温度設定）で年間の電気代がどれだけ変わるかは → {L}",
     True),
    # B3 暖房器具の比較ツール：「## 関連ツール・記事」のスマートプラグの行の直後に1行
    #   （大掃除＝「フィルターを掃除する」の表の行 とは別の場所）
    ("heater-denkidai-hikaku.md",
     "- 電力を見える化するなら → [スマートプラグの選び方](smart-plug-guide.html)",
     "after",
     f"- 冬に電気が増えやすいトイレの便座（ふた・温度設定）の電気代は → {L}",
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
        sys.exit("止めた：--date は 2026-12-28 の形で書く")
    if d not in ALLOWED_DATES:
        sys.exit(f"止めた：--date {d} は受け付けない（案A・案B＝2026-12-28／案C＝2026-12-30 のどちらか）")
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
    # 下書きメモ（front matter の前）を消す。products の目印は残す
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
