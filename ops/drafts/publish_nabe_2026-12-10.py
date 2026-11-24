"""12/10（木）11:00 卓上IH vs カセットコンロ（鍋1回いくら？）記事の公開スクリプト（2026-11-25 03:00 ペンネ作成・作業用コピーで通し確認済み）

手順書 ops/drafts/publish_steps_2026-12-10.md の 2〜4・8 をそのままスクリプトにしたもの（作りは publish_gohan_2026-12-02.py／publish_kisei_2026-12-08.py と同じ）。
使い方（リポジトリ直下で）：
  git pull --rebase
  python3 ops/drafts/publish_nabe_2026-12-10.py      # 記事を移す＋下書きメモ2つ削除＋内部リンク3〜4か所（N1〜N4）
  python3 build.py && python3 ops/tests/content_guard.py && python3 ops/tests/mobile_check.py && python3 ops/check_affiliate.py && python3 ops/tests/site_health.py
  → 確認後 commit & push（push前に git pull --rebase）

止まる条件（止まったら何も書きかえない）：
  - 日本時間の今日が 2026-12-10 より前（早すぎる公開を防ぐ。試しのときだけ --allow-early）
  - 記事がもう content/posts にある（二重実行）
  - 下書きの date が 2026-12-10 でない
  - メモ（先頭の「下書きメモ」と末尾の「公開前に確認すること」）を消した後に残るコメントが
    「<!-- products: takujo-ih,cassette-konro -->」1個でない／メモの文字が残っている
  - 【PR】・「おすすめの探し方（PR）」・「AI（電脳アリス）が作成」・実機レビューでない旨 が無い
  - 文中リンク先（3記事）が無い／商品枠 takujo-ih・cassette-konro が KEYWORDS か products.json（リンク入り）に無い
  - 内部リンクの差し込み位置の行が各記事で「行全体が一致してちょうど1行」でない、またはすでにリンク済み
N4（ご飯の保温vs冷凍の記事）は、その記事が content/posts に無ければ N4 だけ飛ばす（12/2 の公開が遅れても止まらない）。
KEYWORDS の追加・make_links の実行は不要（2つの枠とも 11/24 に登録・リンク入り済み）なので、make_links.py・products.json は書きかえない。
リンク追加だけなので、リンク元の各記事の `updated` は変えない。
"""
import datetime, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
P = ROOT / "content/posts"
SRC = ROOT / "ops/drafts/article_nabe-ih-vs-cassette_draft.md"
DST = P / "nabe-ih-vs-cassette-denkidai.md"
SLUG = "nabe-ih-vs-cassette-denkidai"
PUBLISH_DATE = datetime.date(2026, 12, 10)
L = f"[卓上IHとカセットコンロ、鍋1回いくら？]({SLUG}.html)"
PRODUCTS = "<!-- products: takujo-ih,cassette-konro -->"
PRODUCT_KEYS = ["takujo-ih", "cassette-konro"]
LINKED = ["denkidai-calculator", "fuyu-denkidai-matome", "denki-kettle-vs-pot-denkidai"]
MEMO_WORDS = ("下書きメモ", "公開前に確認", "ペンネ", "カンサ", "照合", "2026-11-2", "content/posts", "ops/")
GOHAN = "gohan-hoon-vs-reitou-denkidai.md"

# (ファイル, 位置の行（行全体が一致）, "after"=その行の直後／"before"=その行の直前, 足す文字列, 必須か)
EDITS = [
    # N1 冬の電気代まとめ：悩み別の早見表。「実際に何kWh…」の行の直前に1行（表の行なので空行なし）
    #   → 12/2 のご飯の行（G1：ケトルの行の直後）・12/8 の帰省の行（K4：エアコンの行の直後）とは位置の行が別。
    #     仕上がりの順：エアコン／帰省／ケトル／ご飯／鍋（N1）／スマートプラグ
    ("fuyu-denkidai-matome.md",
     "| 実際に何kWh使ったか知りたい | [スマートプラグの選び方](smart-plug-guide.html) |",
     "before",
     f"| 年末年始の鍋、卓上IHとカセットコンロの1回分を出したい | {L} |",
     True),
    # N2 電気代計算ツール：「## 関連記事」の最後の箇条の直後に1行（G3 は120行目の「👉 …ケトル…」で別の場所）
    ("denkidai-calculator.md",
     "- エアコンをスマホで操作して切り忘れを防ぐ → [賃貸でエアコン2台をスマホ操作](smart-remote-rental-two-aircon.html)",
     "after",
     f"- 卓上IHで鍋をするときの火力（W）別・時間別の電気代を見るなら → {L}",
     True),
    # N3 ケトルとポット：「## 関連記事」の1つ目（計算ツール）の直後に1行
    #   （G2 は最後の箇条＝湯たんぽの行の直後に足すので、位置の行が別。順番も崩れない）
    ("denki-kettle-vs-pot-denkidai.md",
     "- W数と時間を入れて計算するなら → [家電の電気代計算ツール](denkidai-calculator.html)",
     "after",
     f"- 冬の鍋で卓上IHとカセットコンロの1回分を比べるなら → {L}",
     True),
    # N4 ご飯の保温vs冷凍（12/2公開）：まとめの最後の段落の直後に空行＋1段落。記事が無ければ飛ばす
    (GOHAN,
     "お湯を沸かす家電でも同じように「時間でかかるか、回数でかかるか」で差が出ます。[電気ケトルと電気ポットの電気代比較](denki-kettle-vs-pot-denkidai.html) もあわせてどうぞ。冬の家電全体の電気代は [冬の電気代まとめ](fuyu-denkidai-matome.html) にまとめています。",
     "after",
     f"\n年末年始の鍋を卓上IHとカセットコンロのどちらでするか迷ったら、火力（W）と時間で1回分を出す{L}もどうぞ。",
     False),
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


def main():
    if jst_today() < PUBLISH_DATE and "--allow-early" not in sys.argv:
        sys.exit(f"止めた：今日（日本時間 {jst_today()}）は公開日 {PUBLISH_DATE} より前です（試しのときだけ --allow-early）")
    if DST.exists():
        sys.exit("止めた：記事はもう content/posts にあります（二重実行）")
    s = SRC.read_text(encoding="utf-8")
    if not re.search(r"^date: 2026-12-10$", s, flags=re.M):
        sys.exit("止めた：下書きの date が 2026-12-10 ではない")
    # 下書きメモ（先頭）と「公開前に確認すること」（末尾）の2つを消す。products の目印は残す
    s = re.sub(r"\n?<!-- (下書きメモ|公開前に確認).*?-->\n?", "\n", s, flags=re.S)
    s = re.sub(r"\n{3,}", "\n\n", s).rstrip("\n") + "\n"
    s = s.replace("---\n\n**【PR】", "---\n**【PR】", 1)  # front matter 直後の空行を元どおり詰める
    if s.count("<!--") != 1 or s.count(PRODUCTS) != 1:
        sys.exit(f"止めた：残ったコメントが想定外（{s.count('<!--')}個。products の1個だけのはず）")
    left = [w for w in MEMO_WORDS if w in s]
    if left:
        sys.exit(f"止めた：メモの文字が本文に残っている：{left}")
    for need in ("【PR】", "おすすめの探し方（PR）", 'id="pr-osusume"', "AI（電脳アリス）が作成", "実機で測ったレビューではありません"):
        if need not in s:
            sys.exit(f"止めた：記事に「{need}」が見つからない（PR表記・AI作成の明記）")
    missing = [x for x in LINKED if not (P / f"{x}.md").exists()]
    if missing:
        sys.exit(f"止めた：文中リンク先の記事が無い {missing}")
    mk = (ROOT / "ops/make_links.py").read_text(encoding="utf-8")
    prods = json.loads((ROOT / "content/products.json").read_text(encoding="utf-8"))
    for k in PRODUCT_KEYS:
        if not re.search(rf'^\s*"{re.escape(k)}"\s*:', mk, flags=re.M) or "af.moshimo.com" not in (prods.get(k) or {}).get("html", ""):
            sys.exit(f"止めた：商品枠 {k} が KEYWORDS か products.json に無い（またはリンク空）。KEYWORDS を確認して python3 ops/make_links.py を実行してから再実行")
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
        for f, t in new.items():
            (P / f).write_text(t, encoding="utf-8")
        DST.write_text(s, encoding="utf-8")
    except Exception as e:
        for f, t in orig.items():
            (P / f).write_text(t, encoding="utf-8")
        DST.unlink(missing_ok=True)
        sys.exit(f"止めた：書き込み中にエラー（元に戻しました）：{e}")
    msg = f"OK：記事1本（{DST.name}）＋内部リンク{len(new)}か所（{'・'.join(new)}）。下書き（ops/drafts）は残しています"
    if skipped:
        msg += f"\n注意：{'・'.join(skipped)} が無いので N4 は飛ばしました（ご飯記事を公開した後に手順書の N4 を手で足す）"
    print(msg)


if __name__ == "__main__":
    main()
