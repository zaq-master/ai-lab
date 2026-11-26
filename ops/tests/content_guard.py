#!/usr/bin/env python3
"""記事原稿（content/posts/*.md）の書き方の漏れチェック（ローカルファイルのみ・外部通信なし・標準ライブラリのみ）。
実行：python3 ops/tests/content_guard.py             # 問題0件なら終了コード0、あれば行番号付きで出して1
      python3 ops/tests/content_guard.py --selftest  # わざと壊した文で検出できるかの確認（規則を甘くしすぎていないか）
ビルドやCI（.github/workflows/）には組み込んでいない。記事を書いた・直した回で手で実行する。

チェック項目
① 期限の直書き（経緯：ops/audit/2026-11-20_1000_bf_end_test.md）
   build.py の EXPIRE の終了日時（例 11/25・11月25日・1:59）や「開催中」が、期限つきの目印
   （<!-- TAG -->／<!-- started:TAG -->／<!-- ended:TAG --> ＋直後の段落。build.py の strip_expired と同じ範囲）の
   外に書かれていたら警告。終了後もページに残ってしまうため。
   許すもの：HTMLコメントの中／front matter の started_*・ended_*／ended_title・ended_description があるときの
   title・description（期限後に差し替わる）／終了告知（<!-- ended:TAG -->）がある記事か、期限が過ぎたあとの、
   年（2026年）つきの記録として書かれた行（例：マラソン記事の「2026年11月2日〜11月11日(水)01:59」の公式日程表、
   出典の「（2026年11月11日）」）。「1:59」のように複数の期限で同じ時刻は、どれか1つの例外に当たれば許す。
② 電気代の単価前提（経緯と分類基準：ops/audit/2026-11-20_1000_price_check.md）
   「約◯円」「◯円/時間」「◯円/月」など電気代の計算値がある行で、同じ段落・同じ表・同じ見出し節（親の##節を含む）に
   「◯円/kWh」の前提がない行を警告。
   許すもの：前提のある表を参照する「上の表」「上の早見表」「前の節」等の明示／
   「W÷1000×時間×31円」のような単価入りの計算式が同じ段落・節にある／「目安単価31円/kWhを各記事で使っています」等として
   記事全体の前提単価を書いている記事（まとめ記事）／「÷1000×3×31＝約7.0円」のように記事の単価の数字を掛ける計算式／
   冒頭の結論で単価を書いた記事での「◯円前後の差」の言い直し／売上・note価格・ポイントなど電気代でない金額。
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POSTS = ROOT / "content" / "posts"
sys.path.insert(0, str(ROOT))
from build import EXPIRE, STARTS, expired  # noqa: E402  build.py は import しても実行されない（main は __main__ のときだけ）

issues = []


def add(kind, path, line, msg, text):
    issues.append((kind, path, line, msg, text.strip()[:80]))


# ---------- 共通：front matter と本文を行番号つきで分ける ----------
def split_front(raw):
    lines = raw.split("\n")
    if lines and lines[0] == "---":
        for i in range(1, len(lines)):
            if lines[i] == "---":
                return lines[1:i], i + 1  # front の行, 本文が始まる行のindex（0始まり）
    return [], 0


def comment_lines(lines):
    """HTMLコメント（複数行も）に含まれる行の index 集合"""
    out, inside = set(), False
    for i, l in enumerate(lines):
        s = l
        if inside:
            out.add(i)
            if "-->" in s:
                inside = False
                s = s.split("-->", 1)[1]
            else:
                continue
        while "<!--" in s:
            out.add(i)
            rest = s.split("<!--", 1)[1]
            if "-->" in rest:
                s = rest.split("-->", 1)[1]
            else:
                inside = True
                break
    return out


def strip_comments(text):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


# ---------- ① 期限の直書き ----------
def date_patterns(tag):
    """EXPIRE の終了日時から、本文に直書きされがちな形の正規表現を作る"""
    last = EXPIRE[tag]
    d, _, t = last.partition("T")
    y, mo, da = (int(x) for x in d.split("-"))
    pats = [rf"(?<![\d/]){mo}/{da}(?!\d)", rf"(?<!\d){mo}月{da}日", rf"{y}-{mo:02d}-{da:02d}"]
    if t:
        hh, mm = (int(x) for x in t.split(":"))
        pats.append(rf"(?<![\d:]){hh:02d}:{mm:02d}(?!\d)" if hh >= 10 else rf"(?<![\d:])0?{hh}:{mm:02d}(?!\d)")
    return [re.compile(p) for p in pats]


ONGOING = re.compile(r"開催中")
YEAR = re.compile(r"20\d\d年")


def guarded_lines(body_lines):
    """strip_expired と同じ範囲：目印コメントの行＋直後の空行でない行の連続（＝消える／出し分けられる段落）"""
    out = set()
    tags = "|".join(re.escape(t) for t in EXPIRE)
    mark = re.compile(r"<!--\s*(?:started:|ended:)?(?:" + tags + r")[^>]*-->\s*$")
    i = 0
    while i < len(body_lines):
        if mark.search(body_lines[i]):
            out.add(i)
            j = i + 1
            while j < len(body_lines) and body_lines[j].strip():
                out.add(j)
                j += 1
            i = j
        else:
            i += 1
    return out


def check_expiry_text(name, raw, now=None):
    """1記事分の①チェック。見つかった (行番号, 内容, 行) のリストを返す。now＝期限切れ判定の時刻（既定は今・JST）"""
    found = []
    front, start = split_front(raw)
    meta = {}
    for l in front:
        if ":" in l:
            k, v = l.split(":", 1)
            meta[k.strip()] = v.strip()
    has_ended = {t for t in EXPIRE if re.search(r"<!--\s*ended:" + re.escape(t), raw)}
    gone = {t for t in EXPIRE if expired(t, now)}
    pats = {t: date_patterns(t) for t in EXPIRE}

    def hits(text):
        """[(該当しうるタグの集合, 文字列)]。「1:59」のように複数の期限で同じ時刻は、どれか1つの例外に当たれば許す"""
        r = {}
        for t in EXPIRE:
            for p in pats[t]:
                for m in p.finditer(text):
                    r.setdefault(m.group(0), set()).add(t)
        out = [(tags, f"終了日時「{s}」（{'/'.join(sorted(tags))}）") for s, tags in r.items()]
        if ONGOING.search(text):
            out.append((set(EXPIRE), "「開催中」"))
        return out

    # front matter
    for n, l in enumerate(front, start=2):
        k = l.split(":", 1)[0].strip()
        if k.startswith(("started_", "ended_")) or ":" not in l:
            continue  # 開催中だけ／期限後だけ使われる
        if k in ("date", "updated"):
            continue  # 書いた日・直した日（セールの期限ではない。BF終了日に直した記事の updated: 2026-11-25 を誤検知しないように 2026-11-25 追加）
        repl = meta.get(f"ended_{k}", "")
        swap = repl.split("|", 1)[0].strip() if k in ("title", "description") and "|" in repl else ""
        for tags, x in hits(l.split(":", 1)[1]):
            if swap in tags:
                continue  # その期限が過ぎたら ended_* に差し替わる
            found.append((n, x, l))

    body = raw.split("\n")[start:]
    skip = comment_lines(body) | guarded_lines(body)
    in_code = False
    for i, l in enumerate(body):
        if l.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or i in skip:
            continue
        for tags, x in hits(l):
            if YEAR.search(l) and tags & (has_ended | gone) and x != "「開催中」":
                continue  # 終了告知のある記事・期限切れ後の、年つきの記録（公式日程の表・出典の日付など）
            found.append((start + i + 1, x, l))
    return found


# ---------- ② 電気代の単価前提 ----------
NUM = r"[0-9０-９][0-9０-９,，.．]*"
COST = re.compile(
    r"約\s*\**" + NUM + r"(?:\s*[〜~～-]\s*\**(?:約)?" + NUM + r")?\s*\**円"    # 約7.0円／約20〜31円
    r"|" + NUM + r"(?:\s*[〜~～-]\s*" + NUM + r")?\s*円\s*[/／]\s*(?:時間|h|日|月|年|回|冬|シーズン)"  # 13円/月
    r"|" + NUM + r"(?:\s*[〜~～-]\s*" + NUM + r")?\s*円(?:ほど|前後|くらい|程度)"            # 13〜28円ほど
)
PREMISE = re.compile(r"円\s*[/／]\s*k[wW]h|円/1kWh|円（1kWh"
                     r"|[×✕xX＊*]\s*\**\s*[0-9]+(?:\.[0-9]+)?\s*円(?![/／]\s*(?:時間|日|月|回))")  # 「W÷1000×時間×31円」の計算式も単価の明示
ELEC = re.compile(r"電気代|消費電力|kWh|[0-9]\s*W(?![a-zA-Z])|Wh|ワット|充電|電力")
REFER = re.compile(r"上の(?:早見)?表|上の計算|前の節|前節|上の節|上で計算|上の結果|上の例")
WIDE = re.compile(r"各記事で使|この記事の電気代は.{0,20}円\s*[/／]\s*kWh|この記事(?:では|の計算は)?(?:すべて|全て|ぜんぶ)?.{0,20}円\s*[/／]\s*kWh")
NOT_ELEC = re.compile(r"売上|ポイント|¥|￥|送料|税込|以上のショップ|note|続きは|価格|購入金額")
DIFF = re.compile(r"円(?:前後|ほど|くらい|程度)?の差")  # 「1ヶ月100円前後の差なので…」のような、計算済みの値の差の言い直し
HEAD = re.compile(r"^(#{1,6})\s")


def blocks(body):
    """段落・表のまとまり（空行区切り）ごとに [開始, 終了) を返す"""
    out, s = [], None
    for i, l in enumerate(body + [""]):
        if l.strip() and s is None:
            s = i
        elif not l.strip() and s is not None:
            out.append((s, i))
            s = None
    return out


def check_price_premise(name, raw):
    found = []
    _, start = split_front(raw)
    body = strip_comments("\n".join(raw.split("\n")[start:])).split("\n")
    # コメントを消すと行がずれるので、元の行番号を引けるよう行ごとにコメントを消す
    orig = raw.split("\n")[start:]
    cm = comment_lines(orig)
    body = ["" if i in cm and not re.sub(r"<!--.*?-->", "", l).strip() else re.sub(r"<!--.*?-->", "", l) for i, l in enumerate(orig)]

    heads = [(i, len(HEAD.match(l).group(1))) for i, l in enumerate(body) if HEAD.match(l)]
    wide = any(PREMISE.search(l) and WIDE.search(l) for l in body)  # 記事全体の前提単価を明記（まとめ記事など）
    first_h2 = next((i for i, lv in heads if lv == 2), len(body))
    intro_premise = bool(PREMISE.search("\n".join(body[:first_h2])))  # 冒頭の結論で前提単価を書いている
    # 「÷ 1000 × 8 × 31 ＝」のように、記事で使っている単価の数字を掛ける計算式も前提の明示とみなす
    units = {u.rstrip("0").rstrip(".") for u in re.findall(r"([0-9]+(?:\.[0-9]+)?)\s*円\s*[/／]\s*k[wW]h", raw)} | {"31"}
    formula = re.compile(r"(?:÷\s*1,?000|kWh).*×\s*(?:" + "|".join(sorted(map(re.escape, units))) + r")\s*(?:円|[＝=])")

    def section(i, level_max):
        """i 行を含む、level_max 以下の見出しで区切られた節 [s, e)"""
        s = max([h for h, lv in heads if h <= i and lv <= level_max], default=0)
        e = min([h for h, lv in heads if h > i and lv <= level_max], default=len(body))
        return s, e

    blk = blocks(body)
    in_code = False
    for i, l in enumerate(body):
        if l.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or HEAD.match(l) or not COST.search(l):
            continue
        b0, b1 = next((a, b) for a, b in blk if a <= i < b)
        s3, e3 = section(i, 6)   # 直前の見出しの節
        s2, e2 = section(i, 2)   # 親の ## 節
        para = "\n".join(body[b0:b1])
        ctx = "\n".join(body[s2:e2])
        if not (ELEC.search(para) or ELEC.search("\n".join(body[s3:e3]))):
            continue  # 電気代の話でない金額
        if NOT_ELEC.search(l) and not ELEC.search(l):
            continue
        if PREMISE.search(para) or PREMISE.search("\n".join(body[s3:e3])) or PREMISE.search(ctx):
            continue
        if formula.search(l):
            continue
        if DIFF.search(l) and intro_premise:
            continue
        if REFER.search(l) or REFER.search(body[b0]):
            continue  # 前提のある表・計算を明示して参照（表なら見出し行も見る）
        if wide:
            continue
        found.append((start + i + 1, "電気代の計算値に単価（◯円/kWh）の前提が同じ段落・表・節にない", l))
    return found


# ---------- 自己テスト：わざと壊した文で検出できるか ----------
def selftest():
    ok = True

    def expect(label, got, want):
        nonlocal ok
        flag = (len(got) > 0) == want
        ok &= flag
        print(f"  {'OK ' if flag else 'NG '} {label}: 検出{len(got)}件（期待：{'あり' if want else 'なし'}）")

    tag = next(iter(STARTS), next(iter(EXPIRE)))
    d = EXPIRE[tag].split("T")[0]
    mo, da = int(d[5:7]), int(d[8:10])
    hm = EXPIRE[tag].split("T")[1] if "T" in EXPIRE[tag] else ""
    hm_s = hm.lstrip("0") if hm.startswith("0") else hm
    fm = "---\ntitle: t\ndescription: d\n---\n"
    import datetime, functools
    before = datetime.datetime.fromisoformat(EXPIRE[tag] if "T" in EXPIRE[tag] else d + "T12:00") - datetime.timedelta(hours=1)
    after = before + datetime.timedelta(days=2)
    check = functools.partial(check_expiry_text, now=before)  # 日付が過ぎても同じ結果になるよう、期限の1時間前として判定
    print("① 期限の直書き")
    expect("目印の外に終了日（M/D）", check("x", fm + f"\nセール（{mo}/{da} {hm_s}まで）の考え方は…\n"), True)
    expect("目印の外に終了日（M月D日）", check("x", fm + f"\nセール（{mo}月{da}日まで）で買うなら\n"), True)
    expect("目印の外に時刻だけ", check("x", fm + f"\n〜{hm_s}までの注文が対象\n"), bool(hm))
    expect("目印の外に「開催中」", check("x", fm + "\n楽天セールは開催中です。\n"), True)
    expect("年つきでも終了告知なしなら検出", check("x", fm + f"\n2026年{mo}月{da}日まで開催\n"), True)
    expect("年つきの記録は期限切れ後なら許す", check_expiry_text("x", fm + f"\n2026年{mo}月{da}日の公式案内\n", now=after), False)
    expect("期限切れ後でも年なしは検出", check_expiry_text("x", fm + f"\n（{mo}/{da}まで）\n", now=after), True)
    expect("description の直書き（ended_description なし）", check("x", f"---\ntitle: t\ndescription: セール（{mo}/{da}まで）\n---\n本文\n"), True)
    expect("目印の段落の中（2行続き）", check("x", fm + f"\n<!-- {tag}（期限） -->\n開催中（{mo}/{da} {hm_s}まで）\n続きの行 {mo}月{da}日\n"), False)
    expect("目印の段落の後の別段落は検出", check("x", fm + f"\n<!-- {tag} -->\n期限つきの文\n\n{mo}/{da}までの話\n"), True)
    expect("started: の段落・HTMLコメント内", check("x", fm + f"\n<!-- started:{tag} -->\n開催中です（{mo}/{da}まで）\n\n<!-- メモ\n開催中の回のみ {mo}/{da}\n-->\n"), False)
    expect("ended_description で差し替わる description", check("x", f"---\ntitle: t\ndescription: セール（{mo}/{da}まで）\nended_description: {tag}|終了しました\n---\n本文\n"), False)
    expect("似た数字（{0}/{1}0・1{2}）は誤検知しない".format(mo, da, hm_s), check("x", fm + f"\n{mo}/{da}0 と 1{hm_s} と {mo}/{da}5\n" if hm else fm + f"\n{mo}/{da}0\n"), False)

    print("② 電気代の単価前提")
    bad = fm + "\n## 1時間の電気代\n\n消費電力75Wなので、1時間で**約2.3円**です。\n"
    expect("前提なしの計算値（約◯円）", check_price_premise("x", bad), True)
    expect("前提なしの計算値（◯円/月）", check_price_premise("x", fm + "\n## 月の電気代\n\n充電は0.432kWh → **13円/月**\n"), True)
    expect("前提なしの計算値（◯円ほど）", check_price_premise("x", fm + "\n## 乾燥\n\n電気代は乾燥60分で13〜28円ほど。\n"), True)
    expect("前提なしの表", check_price_premise("x", fm + "\n## 早見表\n\n| 器具 | 消費電力 | 1時間の電気代 |\n|---|---|---|\n| A | 75W | 約2.3円 |\n"), True)
    expect("別の##節にだけ前提がある", check_price_premise("x", fm + "\n## A\n\n単価は31円/kWhで計算。\n\n## B\n\n消費電力75Wで**約2.3円**。\n"), True)
    expect("今日の実例（75Wが出続けた場合の上限で約7.0円）", check_price_premise("x", fm + "\n## 自動OFF\n\n75Wが出続けた場合の上限で**約7.0円**。\n"), True)
    expect("同じ行に前提", check_price_premise("x", fm + "\n## A\n\n75Wで**約2.3円**（31円/kWhで計算）。\n"), False)
    expect("同じ節（###の親##）に前提", check_price_premise("x", fm + "\n## A\n\n目安単価31円/kWhで計算します。\n\n### 75W\n\n電気代は**約2.3円**。\n"), False)
    expect("表の注記に前提", check_price_premise("x", fm + "\n## 早見表\n\n| 器具 | 1時間の電気代 |\n|---|---|\n| A 75W | 約2.3円 |\n※電気代は目安単価31円/kWhで計算\n"), False)
    expect("単価の数字を掛ける式（÷1000×3×31＝）", check_price_premise("x", fm + "\n## A\n\n75Wが3時間で 75 ÷ 1000 × 3 × 31 ＝ **約7.0円**\n"), False)
    expect("日数を掛けただけの式は前提にならない", check_price_premise("x", fm + "\n## A\n\n75W × 8時間 ÷ 1000 × 20 ＝ 12kWh、電気代は**約372円**\n"), True)
    expect("冒頭に前提がない記事の「◯円前後の差」", check_price_premise("x", fm + "\n## A\n\n電気代は1ヶ月100円前後の差なので\n"), True)
    expect("電気代でない金額（売上0円・note¥300）", check_price_premise("x", fm + "\n## 実録\n\n売上は約0円、続きは¥300です。\n"), False)
    print("自己テスト：" + ("すべてOK" if ok else "NGあり"))
    return ok


def check_pending_duplicates():
    """③ 公開待ちの下書きとの重複（2026-11-26 追加）
    ops/drafts/publish_*.py の公開予定日より前の date で、同じ記事名の記事が content/posts にあれば NG。
    （11/26 11時の回が、12/2公開予定で監査済みの記事と同じ記事名で別の版を先に出したため）"""
    import re as _re, datetime as _dt
    for s in sorted((ROOT / "ops/drafts").glob("publish_*.py")):
        src = s.read_text(encoding="utf-8")
        m_slug = _re.search(r'^SLUG\s*=\s*"([^"]+)"', src, _re.M) or _re.search(r'^DST\s*=\s*P\s*/\s*"([^"]+)\.md"', src, _re.M)
        dates = [_dt.date(*map(int, d)) for line in _re.findall(r'^(?:PUBLISH_DATE|DEFAULT_DATE|ALLOWED_DATES)\s*=.*$', src, _re.M)
                 for d in _re.findall(r'datetime\.date\((\d+),\s*(\d+),\s*(\d+)\)', line)]
        if not (m_slug and dates):
            continue
        pub = min(dates)  # 案が複数あるときは一番早い公開候補日
        post = POSTS / f"{m_slug.group(1)}.md"
        if not post.exists():
            continue
        m = _re.search(r'^date:\s*(\d{4})-(\d{2})-(\d{2})', post.read_text(encoding="utf-8"), _re.M)
        if m and _dt.date(*map(int, m.groups())) < pub:
            add("公開待ちと重複", post.relative_to(ROOT), 1,
                f"{s.name}（{pub}公開予定）と同じ記事名。新しく書かず下書きを使うか、下書きを ops/drafts/retired/ へ", post.name)


def main():
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    files = sorted(POSTS.glob("*.md"))
    for p in files:
        raw = p.read_text(encoding="utf-8")
        rel = p.relative_to(ROOT)
        for n, msg, text in check_expiry_text(p.name, raw):
            add("期限の直書き", rel, n, msg + "が期限の目印の外にある（終了後もページに残る）", text)
        for n, msg, text in check_price_premise(p.name, raw):
            add("単価前提", rel, n, msg, text)
    check_pending_duplicates()
    if not issues:
        print(f"content_guard: OK（{len(files)}記事・期限の直書き0件・単価前提の漏れ0件）")
        sys.exit(0)
    for kind, path, line, msg, text in issues:
        print(f"[{kind}] {path}:{line}  {msg}\n    → {text}")
    print(f"content_guard: 問題 {len(issues)}件（{len(files)}記事）")
    sys.exit(1)


if __name__ == "__main__":
    main()
