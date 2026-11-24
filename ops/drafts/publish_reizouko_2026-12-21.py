"""12/21（月）11:00 冷蔵庫の詰め込みすぎと電気代 記事の公開スクリプト（2026-11-25 03:00 ペンネ作成・作業用コピーで通し確認済み）

手順書 ops/drafts/publish_steps_2026-12-21.md の 2〜4・8 をそのままスクリプトにしたもの（作りは publish_nabe_2026-12-10.py と同じ）。
使い方（リポジトリ直下で）：
  git pull --rebase
  python3 ops/drafts/publish_reizouko_2026-12-21.py   # 記事を移す＋下書きメモ2つ削除＋内部リンク3か所（R1〜R3）
  python3 build.py && python3 ops/tests/content_guard.py && python3 ops/tests/mobile_check.py && python3 ops/check_affiliate.py && python3 ops/tests/site_health.py
  → 確認後 commit & push（push前に git pull --rebase）

止まる条件（止まったら何も書きかえない）：
  - 日本時間の今日が 2026-12-21 より前（早すぎる公開を防ぐ。試しのときだけ --allow-early）
  - 記事がもう content/posts にある（二重実行）
  - 下書きの date が 2026-12-21 でない
  - メモ（先頭の「下書きメモ」と末尾の「公開前に確認すること」）を消した後に残るコメントが
    「<!-- products: smart-plug-monitor -->」1個でない／メモの文字が残っている
  - 【PR】・「おすすめの探し方（PR）」・「AI（電脳アリス）が作成」・「実機レビューではありません」 が無い
  - 文中リンク先（4記事）が無い／商品枠 smart-plug-monitor が KEYWORDS か products.json（リンク入り）に無い
  - 内部リンクの差し込み位置の行が各記事で「行全体が一致してちょうど1行」でない、またはすでにリンク済み
KEYWORDS の追加・make_links の実行は不要（smart-plug-monitor は登録・リンク入り済み）なので、make_links.py・products.json は書きかえない。
リンク追加だけなので、リンク元の各記事の `updated` は変えない。
R1〜R3 の位置の行は、既存6本（oosouji/gohan/kisei/nabe/yutanpo/samusa）の位置の行・足す行と重ならないことを grep で確認済み（11/25）。
"""
import datetime, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
P = ROOT / "content/posts"
SRC = ROOT / "ops/drafts/article_reizouko-tsumekomi_draft.md"
DST = P / "reizouko-tsumekomi-denkidai.md"
SLUG = "reizouko-tsumekomi-denkidai"
PUBLISH_DATE = datetime.date(2026, 12, 21)
L = f"[冷蔵庫の詰め込みすぎで電気代はいくら変わる？]({SLUG}.html)"
PRODUCTS = "<!-- products: smart-plug-monitor -->"
PRODUCT_KEYS = ["smart-plug-monitor"]
LINKED = ["denkidai-calculator", "fuyu-denkidai-matome", "denki-kettle-vs-pot-denkidai", "smart-plug-guide"]
MEMO_WORDS = ("下書きメモ", "公開前に確認", "ペンネ", "カンサ", "照合", "2026-11-24", "content/posts", "ops/", "reizouko-ondokei", "未登録")
DATE_LINE = "date: 2026-12-21"
NEED = ("【PR】", "おすすめの探し方（PR）", 'id="pr-osusume"', "AI（電脳アリス）が作成", "実機レビューではありません")

# (ファイル, 位置の行（行全体が一致）, "after"=その行の直後／"before"=その行の直前, 足す文字列, 必須か)
EDITS = [
    # R1 冬の電気代まとめ：悩み別の早見表。「冬の部屋干しで除湿機を使う」の行の直後に1行（表の行なので空行なし）
    #   → 他の回の位置の行（エアコン＝K4／ケトル＝G1／スマートプラグ＝N1）とは別の行。
    #     仕上がりの順：除湿機／冷蔵庫（R1）／エアコン／帰省／ケトル／ご飯／鍋／スマートプラグ
    ("fuyu-denkidai-matome.md",
     "| 冬の部屋干しで除湿機を使う | [除湿機の電気代（方式別・1回あたりの計算例）](fuyu-heyaboshi-joshitsuki-denkidai.html) |",
     "after",
     f"| 年末の買いだめで冷蔵庫がパンパン | {L} |",
     True),
    # R2 電気代計算ツール：よくある質問「待機電力やつけっぱなしの家電も計算できる？」の答えの直後に空行＋1段落
    #   （G3＝👉ケトルの行、N2＝関連記事の最後の行 とは別の場所）
    ("denkidai-calculator.md",
     "A. 計算式は同じです。待機時の消費電力（W）が仕様表に書かれていれば、その値と「24時間」を入れると1日の目安が出ます。冷蔵庫や電気ポットのように電力が上下する家電は、カタログの**年間消費電力量（kWh/年）**÷365×単価のほうが実際に近くなります。",
     "after",
     f"\n冷蔵庫の使い方（詰め込み・設定温度・壁との間隔）で年間いくら変わるかは、資源エネルギー庁の数値で計算した{L}にまとめています。",
     True),
    # R3 ケトルとポット：「## 関連記事」の3つ目（スマートプラグ）の直後に1行
    #   （N3＝1つ目の直後、G2＝最後の湯たんぽの行の直後 とは別の行）
    ("denki-kettle-vs-pot-denkidai.md",
     "- 家電の電力を測るなら → [スマートプラグの選び方](smart-plug-guide.html)",
     "after",
     f"- 同じ台所の冷蔵庫、詰め込みすぎ・設定温度で年間いくら変わるかは → {L}",
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
        msg += f"\n注意：{'・'.join(skipped)} が無いので飛ばしました"
    print(msg)


if __name__ == "__main__":
    main()
