"""12/14（月）11:00 電気毛布と湯たんぽ（お湯・充電式）1晩いくら？記事の公開スクリプト（2026-11-25 03:00 ペンネ作成・一時コピーで通し確認済み）

手順書 ops/drafts/publish_steps_2026-12-14.md をそのままスクリプトにしたもの（12/2 ご飯・12/8 帰省と同じ作り）。
使い方（リポジトリ直下で）：
  git pull --rebase
  python3 ops/drafts/publish_yutanpo_2026-12-14.py    # 記事を移す＋内部リンク4か所（Y1〜Y4）
  python3 build.py && python3 ops/tests/content_guard.py && python3 ops/tests/mobile_check.py && python3 ops/check_affiliate.py && python3 ops/tests/site_health.py
  → 確認後 commit & push（push前に git pull --rebase）
止まる条件（止まったら何も書きかえない）：
  - 記事がもう content/posts にある（二重実行）
  - 日本時間の今日が 2026-12-14 より前（早すぎる公開を防ぐ。試しのときだけ --allow-early）
  - 下書きの date が 2026-12-14 でない
  - 下書きメモが残っている／コメントが products の1個以外／PR表記・AI作成の明記・実機レビューでない旨が無い
  - 文中リンク先の記事（6本）が無い／商品枠 denki-moufu・yutanpo・yutanpo-juden が KEYWORDS か products.json（リンク入り）に無い
  - 差し込み位置の文が各記事で「ちょうど1行」でない・すでにリンク済み
KEYWORDS の追加・make_links の実行は不要（3枠とも登録済み・リンク入り。11/24 確認）なので、make_links.py は書きかえない。
リンク追加だけなので、各記事の `updated` は変えない。
差し込み先は寝具・暖房系の4本だけ（ご飯・帰省・大掃除・鍋のスクリプトが触る記事とは重ならない）。
"""
import datetime, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
P = ROOT / "content/posts"
SRC = ROOT / "ops/drafts/article_yutanpo-vs-denki-blanket_draft.md"
PUBLISH_DATE = datetime.date(2026, 12, 14)
SLUG = "yutanpo-vs-denki-blanket"
DST = P / f"{SLUG}.md"
L = f"[電気毛布と湯たんぽ（お湯・充電式）1晩いくら？]({SLUG}.html)"
PRODUCT_KEYS = ["denki-moufu", "yutanpo", "yutanpo-juden"]
LINKED = ["neru-danbou-denkidai-calculator", "denki-blanket-denkidai-1jikan", "denki-kettle-vs-pot-denkidai",
          "futon-kansouki-denkidai", "smart-plug-guide", "fuyu-denkidai-matome"]
MEMO_WORDS = ("下書きメモ", "公開前に確認", "ペンネ", "カンサ", "照合", "content/posts", "ops/")

# (ファイル, 位置の行（行全体が一致）, その直後に足す文字列)
EDITS = [
    ("neru-danbou-denkidai-calculator.md",  # Y1 Q「湯たんぽがいちばん安いなら…」の回答の直後に空行＋1段落
     "A. 上の早見表の前提（単価31円/kWh）では湯たんぽ（約5.9円）が電気毛布8時間（約12.4円）より安くなりますが、お湯の量・沸かし方・電気毛布のW数で順番は変わります。また、湯たんぽは時間とともに冷めていき、電気毛布は設定した温度を保つなど、**温まり方が違う**ため、金額だけでは決められません。2つの計算方法の詳しい比べ方は[電気毛布・こたつの電気代](denki-moufu-kotatsu-denkidai-telework.html)の「湯たんぽと電気毛布、どっちが安い？」の節にあります。",
     f"\n実際の製品のメーカー公表値（電気毛布の温度段階ごとの消費電力量・充電式湯たんぽの蓄熱時間・ケトルの沸とう時間）で1晩を計算した例は、{L}にまとめています。お湯の量・W数の前提がこのツールの初期値と違うため、金額の順番も同じにはなりません。"),
    ("denki-moufu-kotatsu-denkidai-telework.md",  # Y2 「寝るときに使う場合は…」の段落の直後に空行＋1段落（下の products: yutanpo はそのまま）
     "寝るときに使う場合は、[寝るときの暖房 一晩の電気代くらべ](neru-danbou-denkidai-calculator.html)で、W数と時間（湯たんぽはお湯の量）を入れると一晩の電気代を並べて比べられます。",
     f"\n仮定の例ではなく実際の製品の数字（電気毛布2機種・充電式湯たんぽ3機種のメーカー公表値）で比べたいときは、{L}を見てください。"),
    ("denki-blanket-denkidai-1jikan.md",  # Y3 「エアコン・こたつと比べると？」の箇条の最後に1行
     "- 寝る前に布団だけ温めたいなら、[布団乾燥機の電気代（あたため・乾燥・ダニ対策モード別）](futon-kansouki-denkidai.html)も参考にしてください",
     f"- 寝るときの電気毛布を、湯たんぽ（お湯・充電式）と1晩の電気代で比べるなら → {L}"),
    ("futon-kansouki-denkidai.md",  # Y4 「電気毛布・部屋干しとの使い分け」の箇条に1行
     "- 一晩の暖房を並べて比べたいときは[寝るときの暖房 一晩の電気代くらべ（計算ツール）](neru-danbou-denkidai-calculator.html)へ",
     f"- 電気毛布と湯たんぽ（お湯・充電式）を、メーカー公表値で1晩いくらか比べた例は{L}にあります"),
]


def jst_today():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date()


def insert_after(text, anchor, add):
    lines = text.split("\n")
    idx = [i for i, x in enumerate(lines) if x == anchor]
    if len(idx) != 1:
        return None
    lines[idx[0] + 1:idx[0] + 1] = add.split("\n")
    return "\n".join(lines)


def main():
    if DST.exists():
        sys.exit("止めた：記事はもう content/posts にあります（二重実行）")
    if jst_today() < PUBLISH_DATE and "--allow-early" not in sys.argv:
        sys.exit(f"止めた：今日（日本時間 {jst_today()}）は公開日 {PUBLISH_DATE} より前です（試しのときだけ --allow-early）")
    s = SRC.read_text(encoding="utf-8")
    if not s.startswith("---\n"):
        sys.exit("止めた：下書きの先頭が front matter（---）ではない")
    if not re.search(r"^date: 2026-12-14$", s, flags=re.M):
        sys.exit("止めた：下書きの date が 2026-12-14 ではない")
    # この下書きには先頭メモが無いが、後から足された場合に備えて同じ消し方をしておく
    s = re.sub(r"<!-- (下書きメモ|公開前に確認).*?-->\n?", "", s, flags=re.S)
    if s.count("<!--") != 1 or s.count("<!-- products: denki-moufu,yutanpo,yutanpo-juden -->") != 1:
        sys.exit(f"止めた：残ったコメントが想定外（{s.count('<!--')}個。products の1個だけのはず）")
    left = [w for w in MEMO_WORDS if w in s]
    if left:
        sys.exit(f"止めた：メモの文字が本文に残っている：{left}")
    if "【PR】" not in s or "おすすめの探し方（PR）" not in s or "AI（電脳アリス）が作成" not in s or "実機レビューではありません" not in s:
        sys.exit("止めた：PR表記・AI作成の明記・実機レビューでない旨のどれかが見つからない")
    missing = [x for x in LINKED if not (P / f"{x}.md").exists()]
    if missing:
        sys.exit(f"止めた：リンク先の記事が無い {missing}")
    kw = (ROOT / "ops/make_links.py").read_text(encoding="utf-8")
    prods = json.loads((ROOT / "content/products.json").read_text(encoding="utf-8"))
    for k in PRODUCT_KEYS:
        if not re.search(rf'^\s*"{re.escape(k)}"\s*:', kw, flags=re.M) or "af.moshimo.com" not in (prods.get(k) or {}).get("html", ""):
            sys.exit(f"止めた：商品枠 {k} が KEYWORDS か products.json に無い（またはリンク空）。python3 ops/make_links.py を確認")
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
    # 書き込み（途中で失敗したら元に戻して止まる＝中途半端な状態を残さない。リンク→記事本体の順）
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
    print(f"OK：記事1本（{SLUG}.md）＋内部リンク4か所（Y1〜Y4）。下書き（ops/drafts）は残しています")


if __name__ == "__main__":
    main()
