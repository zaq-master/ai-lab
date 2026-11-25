"""12/2（水）11:00 クリスマスのLEDイルミネーション 1か月の電気代 記事の公開スクリプト（2026-11-25 ペンネ作成・作業用コピーで通し確認済み）

手順書 ops/drafts/publish_steps_2026-12-02_illumi.md の 2〜5・8 をそのままスクリプトにしたもの（作りは publish_reizouko_2026-12-21.py と同じ。
ただしこの記事は新しい商品枠 led-illumination を使うので、KEYWORDS と products.json への追加・make_links の実行もこの中で行う）。
使い方（リポジトリ直下で）：
  git pull --rebase
  python3 ops/drafts/publish_illumi_2026-12-02.py   # 記事を移す＋下書きメモ2つ削除＋商品枠の追加＋内部リンク3か所（I1〜I3）
  python3 build.py && python3 ops/tests/content_guard.py && python3 ops/tests/mobile_check.py && python3 ops/check_affiliate.py && python3 ops/tests/site_health.py
  → 確認後 commit & push（push前に git pull --rebase）。ops/make_links.py と content/products.json も変わるので一緒に commit

止まる条件（止まったら何も書きかえない）：
  - 日本時間の今日が 2026-12-02 より前（早すぎる公開を防ぐ。試しのときだけ --allow-early）
  - 記事がもう content/posts にある（二重実行）
  - 下書きの date が 2026-12-02 でない
  - メモ（先頭の「下書きメモ」と末尾の「公開前に確認すること」）を消した後に残るコメントが
    「<!-- products: led-illumination,smart-plug-basic -->」1個でない／メモの文字が残っている
  - 【PR】・「おすすめの探し方（PR）」・「AI（電脳アリス）が作成」・「実機レビューではありません」 が無い
  - 本文に楽天・もしもの直書きURLがある（check_affiliate が止めるため。商品ページのURLは下書きメモにだけ書く）
  - 文中リンク先（3記事）が無い／商品枠 smart-plug-basic が KEYWORDS か products.json（リンク入り）に無い
  - led-illumination が KEYWORDS に別のキーワードで登録済み（勝手に上書きしない）
  - 内部リンクの差し込み位置の行が各記事で「行全体が一致してちょうど1行」でない、またはすでにリンク済み
  - make_links 実行後に led-illumination のリンクが入っていない（このときは全部元に戻す）
リンク追加だけなので、リンク元の各記事の `updated` は変えない。
I1〜I3 の位置の行は、他の7本（oosouji/gohan/kisei/nabe/yutanpo/samusa/reizouko）の位置の行・足す行と重ならないことを grep で確認済み（11/25）。
"""
import datetime, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
P = ROOT / "content/posts"
SRC = ROOT / "ops/drafts/article_led-illumination-denkidai_draft.md"
DST = P / "led-illumination-denkidai.md"
SLUG = "led-illumination-denkidai"
PUBLISH_DATE = datetime.date(2026, 12, 2)
L = f"[クリスマスのLEDイルミネーション、1か月の電気代はいくら？]({SLUG}.html)"
PRODUCTS = "<!-- products: led-illumination,smart-plug-basic -->"
NEW_KEY, NEW_KW, NEW_LABEL = "led-illumination", "LEDイルミネーション 室内 USB", "LEDイルミネーション（室内・USB式）"
OLD_KEYS = ["smart-plug-basic"]
LINKED = ["denkidai-calculator", "fuyu-denkidai-matome", "smart-plug-guide"]
MEMO_WORDS = ("下書きメモ", "公開前に確認", "ペンネ", "カンサ", "照合", "2026-11-2", "content/posts", "ops/", "check_affiliate", "未登録")
DATE_LINE = "date: 2026-12-02"
NEED = ("【PR】", "おすすめの探し方（PR）", 'id="pr-osusume"', "AI（電脳アリス）が作成", "実機レビューではありません")
MK = ROOT / "ops/make_links.py"
PJ = ROOT / "content/products.json"

# (ファイル, 位置の行（行全体が一致）, "after"=その行の直後／"before"=その行の直前, 足す文字列, 必須か)
EDITS = [
    # I1 スマートプラグの選び方：「## 向いている家電」の最後の箇条（充電器）の直後に1行
    #   （K1 帰省＝「判断に迷ったら…」の段落の直後、とは別の節）
    ("smart-plug-guide.md",
     "- 充電器（夜中の充電しすぎ対策のタイマーとして）",
     "after",
     f"- コンセント式のLEDイルミネーション（消し忘れ防止のタイマーとして。電源が入ったときに自動で点くかは製品ごとに確認。1か月の電気代の出し方は{L}）",
     True),
    # I2 電気代計算ツール：よくある質問「消費電力（W）がわからないときは？」の答えの直後に空行＋1段落
    #   （G3 ご飯＝「👉 …ケトル…」の直後、R2 冷蔵庫＝次の質問「待機電力…」の答えの直後、N2 鍋＝関連記事の最後 とは別の場所）
    ("denkidai-calculator.md",
     "A. 本体の銘板ラベル、取扱説明書、メーカー公式サイトの仕様表に「消費電力」として書かれています。「強」「弱」で値が分かれている製品は、よく使うモードの値をツールに入れてください。わからない数字を推測で入れると、結果も目安としてずれます。",
     "after",
     f"\nUSB式の小さな電飾のように「5V ◯A」としか書かれていない製品は、5×電流（A）がW数の目安です。クリスマスのイルミネーションを点灯時間・日数別に計算した例は{L}にまとめています。",
     True),
    # I3 冬の電気代まとめ：悩み別の早見表。「自分の暖房の電気代をすぐ知りたい」の行の直後に1行（表の行なので空行なし）
    #   （R1＝除湿機の直後、K4＝エアコンの直後、G1＝ケトルの直後、N1＝スマートプラグの直前 とは別の行）
    ("fuyu-denkidai-matome.md",
     "| 自分の暖房の電気代をすぐ知りたい | [家電の電気代計算ツール](denkidai-calculator.html) |",
     "after",
     f"| クリスマスのイルミネーションの電気代を知りたい | {L} |",
     True),
]


def jst_today():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date()


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
    if jst_today() < PUBLISH_DATE and "--allow-early" not in sys.argv:
        sys.exit(f"止めた：今日（日本時間 {jst_today()}）は公開日 {PUBLISH_DATE} より前です（試しのときだけ --allow-early）")
    if DST.exists():
        sys.exit("止めた：記事はもう content/posts にあります（二重実行）")
    s = SRC.read_text(encoding="utf-8")
    if not re.search(rf"^{DATE_LINE}$", s, flags=re.M):
        sys.exit(f"止めた：下書きの date が {PUBLISH_DATE} ではない")
    # 下書きメモ（先頭）と「公開前に確認すること」（末尾）の2つを消す。products の目印は残す
    s = re.sub(r"\n?<!-- (下書きメモ|公開前に確認).*?-->\n?", "\n", s, flags=re.S)
    s = re.sub(r"\n{3,}", "\n\n", s).rstrip("\n") + "\n"
    s = s.replace("---\n\n**【PR】", "---\n**【PR】", 1)  # front matter 直後の空行を元どおり詰める
    if s.count("<!--") != 1 or s.count(PRODUCTS) != 1:
        sys.exit(f"止めた：残ったコメントが想定外（{s.count('<!--')}個。products の1個だけのはず）")
    left = [w for w in MEMO_WORDS if w in s]
    if left:
        sys.exit(f"止めた：メモの文字が本文に残っている：{left}")
    for need in NEED:
        if need not in s:
            sys.exit(f"止めた：記事に「{need}」が見つからない（PR表記・AI作成の明記）")
    if re.search(r"https?://[^\s\"\)]*(moshimo|hb\.afl\.rakuten|item\.rakuten|search\.rakuten)", s):
        sys.exit("止めた：本文に楽天・もしもの直書きURLがある（商品ページのURLは下書きメモにだけ書く）")
    missing = [x for x in LINKED if not (P / f"{x}.md").exists()]
    if missing:
        sys.exit(f"止めた：文中リンク先の記事が無い {missing}")
    mk = MK.read_text(encoding="utf-8")
    pj_text = PJ.read_text(encoding="utf-8")
    prods = json.loads(pj_text)
    for k in OLD_KEYS:
        if not re.search(rf'^\s*"{re.escape(k)}"\s*:', mk, flags=re.M) or "af.moshimo.com" not in (prods.get(k) or {}).get("html", ""):
            sys.exit(f"止めた：商品枠 {k} が KEYWORDS か products.json に無い（またはリンク空）。KEYWORDS を確認して python3 ops/make_links.py を実行してから再実行")
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
    # 書き込み（途中で失敗したら元に戻して止まる＝中途半端な状態を残さない。2026-11-24 カンサ監査の作り）
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
    msg = (f"OK：記事1本（{DST.name}）＋商品枠 {NEW_KEY}（KEYWORDS{'追加' if new_mk else 'は登録済み'}・products.json"
           f"{'追加' if need_pj else 'は登録済み'}・make_links 実行：{out.stdout.strip()}）"
           f"＋内部リンク{len(new)}か所（{'・'.join(new)}）。下書き（ops/drafts）は残しています")
    if skipped:
        msg += f"\n注意：{'・'.join(skipped)} が無いので飛ばしました"
    print(msg)


if __name__ == "__main__":
    main()
