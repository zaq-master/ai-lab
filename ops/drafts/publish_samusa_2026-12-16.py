"""12/16（水）11:00 寒さでスマホの電池が減る記事の公開スクリプト（2026-11-25 03:00 ペンネ作成・一時コピーで通し確認済み）

手順書 ops/drafts/publish_steps_2026-12-16.md をそのままスクリプトにしたもの（作りは publish_kisei_2026-12-08.py と同じ）。
使い方（リポジトリ直下で）：
  git pull --rebase
  python3 ops/drafts/publish_samusa_2026-12-16.py   # 記事を移す＋下書きメモ削除＋内部リンク3か所（S1〜S3）
  python3 build.py && python3 ops/tests/content_guard.py && python3 ops/tests/mobile_check.py && python3 ops/check_affiliate.py && python3 ops/tests/site_health.py
  → 確認後 commit & push（push前に git pull --rebase）
止まる条件（止まったら何も書きかえない）：
  - 記事がもう content/posts にある（二重実行）
  - 日本時間の今日が 2026-12-16 より前（早すぎる公開を防ぐ。試しのときだけ --allow-early）※2026-11-25 カンサ監査で追加
  - 下書きの date が 2026-12-16 でない
  - 下書きメモを消したあとのコメントが「<!-- products: mobile-battery-10000 -->」の1個以外／メモの文字が残っている
  - PR表記・AI作成の明記・実機検証でない旨が見つからない
  - 文中リンク先の記事（2本）が無い／商品枠 mobile-battery-10000 が KEYWORDS か products.json（リンク入り）に無い
  - 差し込み位置の文が各記事で「ちょうど1行」でない・すでにリンク済み
KEYWORDS の追加・make_links の実行は不要（mobile-battery-10000 は登録済み・リンク入り）なので、make_links.py は書きかえない。
リンク追加だけなので、各記事の `updated` は変えない。
公開前の宿題（スクリプトではやらない）：シャープ AQUOS sense8 取扱説明書PDF と Apple の日本語ページ（support.apple.com/ja-jp/118431）を開き、引用の文言が変わっていないか確認。
"""
import datetime, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
P = ROOT / "content/posts"
SRC = ROOT / "ops/drafts/article_smartphone-samusa-battery_draft.md"
DST = P / "smartphone-samusa-battery.md"
SLUG = "smartphone-samusa-battery"
DATE = "2026-12-16"
PUBLISH_DATE = datetime.date(2026, 12, 16)
L = f"[寒い場所でスマホの電池が減るのはなぜ？]({SLUG}.html)"
PRODUCT_KEYS = ["mobile-battery-10000"]
LINKED = ["mobile-battery-jikan-calculator", "hikouki-mobile-battery"]
MEMO_WORDS = ("下書きメモ", "公開前に", "ペンネ", "カンサ", "照合", "content/posts", "ops/", "2026-11-2")

# (ファイル, 位置の行（行全体が一致）, その直後に足す文字列)  ※3か所とも空行＋1段落
EDITS = [
    ("mobile-battery-jikan-calculator.md",  # S1 早見表②の注記の直後（<div id="hikouki"> より前）
     "※W数は例です。機器の消費電力は取扱説明書・商品ページで確認してください。寒い屋外や、出力が上下する機器では短くなることがあります。",
     f"\nスマホ本体の電池が寒さで急に減る理由と、Apple・Google・シャープの公式ページに書かれた動作温度は、{L}にまとめています。"),
    ("hikouki-mobile-battery.md",  # S2 計算ツールへの案内の直後（「## 帰省の前のチェックリスト」より前。12/8 の K3 は表の最後の行なので別の位置）
     "旅先で「このバッテリーでスマホを何回充電できるか」「電熱ベストが何時間もつか」を知りたい人は、[モバイルバッテリーで何時間もつ？計算ツール](mobile-battery-jikan-calculator.html) で、容量と機器のW数を入れて確かめられます。",
     f"\n帰省先の寒い屋外でスマホの電池が急に減ったときは、故障かどうかを見分ける前に{L}で、メーカー公式の動作温度と「暖かい場所に戻すと元に戻る」という説明を確認できます。"),
    ("usb-c-charger-guide.md",  # S3 Q8 の答えの最後（Q9 の見出しより前）
     "飛行機（国内線）でモバイルバッテリーを持っていく場合は、2026年4月24日から1人2個まで・1個160Wh以下になり、機内でバッテリー本体を充電することも禁止されています。くわしくは[飛行機のモバイルバッテリー新ルール](hikouki-mobile-battery.html)をどうぞ。",
     f"\n冬の屋外でスマホが冷えて電池が急に減ったり、充電されなかったりするときは、{L}でメーカー公式の動作温度と対策を確認できます。"),
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
    # 2026-11-25 カンサ監査で追加：build.py は未来の date の記事も公開するため、早く実行すると即公開になる
    if jst_today() < PUBLISH_DATE and "--allow-early" not in sys.argv:
        sys.exit(f"止めた：今日（日本時間 {jst_today()}）は公開日 {PUBLISH_DATE} より前です（試しのときだけ --allow-early）")
    s = SRC.read_text(encoding="utf-8")
    if not re.search(rf"^date: {DATE}$", s, flags=re.M):
        sys.exit(f"止めた：下書きの date が {DATE} ではない")
    s = re.sub(r"<!-- (下書きメモ|公開前に確認).*?-->\n?", "", s, flags=re.S)
    if s.count("<!--") != 1 or s.count("<!-- products: mobile-battery-10000 -->") != 1:
        sys.exit(f"止めた：残ったコメントが想定外（{s.count('<!--')}個。products: mobile-battery-10000 の1個だけのはず）")
    left = [w for w in MEMO_WORDS if w in s]
    if left:
        sys.exit(f"止めた：記事に下書きの文字が残っている：{left}")
    if 'class="badge">PR' not in s or "広告リンク" not in s or "AI（電脳アリス）が作成" not in s or "実機での検証ではなく" not in s:
        sys.exit("止めた：PR表記・AI作成の明記・実機検証でない旨のどれかが見つからない")
    missing = [x for x in LINKED if not (P / f"{x}.md").exists()]
    if missing:
        sys.exit(f"止めた：リンク先の記事が無い {missing}")
    mk = (ROOT / "ops/make_links.py").read_text(encoding="utf-8")
    prods = json.loads((ROOT / "content/products.json").read_text(encoding="utf-8"))
    for k in PRODUCT_KEYS:
        if not re.search(rf'^\s*"{k}"\s*:', mk, flags=re.M) or "af.moshimo.com" not in (prods.get(k) or {}).get("html", ""):
            sys.exit(f"止めた：商品枠 {k} が KEYWORDS か products.json に無い（またはリンク空）")
    # 内部リンク3か所（先に全部確かめてから書く）
    new = {}
    for f, anchor, add in EDITS:
        t = (P / f).read_text(encoding="utf-8")
        if SLUG in t:
            sys.exit(f"止めた：{f} はもうこの記事にリンク済み")
        r = insert_after(t, anchor, add)
        if r is None:
            sys.exit(f"止めた：{f} の位置の行が1か所ではない")
        new[f] = r
    # 書き込み：途中で失敗したら全部元に戻して止まる（中途半端な状態を残さない）。リンク→記事本体の順
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
    print(f"OK：記事1本（{SLUG}.md）＋内部リンク3か所（S1〜S3）。下書き（ops/drafts）は残しています")


if __name__ == "__main__":
    main()
