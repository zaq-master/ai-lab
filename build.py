#!/usr/bin/env python3
"""content/posts/*.md -> docs/ の静的サイトを生成する。
記事の先頭は以下の形式:
---
title: タイトル
date: 2026-11-02
description: 120字以内の要約
category: デスク環境
---
本文(Markdown)
"""
import json, re, html, datetime, os
from pathlib import Path
import markdown

ROOT = Path(__file__).parent
CFG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
OUT = ROOT / "docs"
TPL = (ROOT / "templates" / "base.html").read_text(encoding="utf-8")
PRODUCTS = json.loads((ROOT / "content" / "products.json").read_text(encoding="utf-8"))


def product_box(m):
    """<!-- products: key1,key2 --> を商品枠に置換。リンク未設定(html空)の枠は出さない。"""
    items = [PRODUCTS.get(k.strip(), {}) for k in m.group(1).split(",")]
    items = [i for i in items if i.get("html")]
    if not items:
        return ""
    inner = "".join(f'<div class="prod"><p class="prod-l">{html.escape(i["label"])}</p>{i["html"]}</div>' for i in items)
    return ('<section class="prods"><h2>候補の商品 <span class="badge">PR</span></h2>'
            '<p class="pr">※広告リンクです。価格・在庫・仕様は変わるため、購入前に販売ページで必ずご確認ください。実機レビューではありません。</p>'
            f'{inner}</section>')


def sheet_cta(_m=None):
    """<!-- sheet-cta --> を「記録用Googleシート版（運営者自身の有料note）」への控えめな導線に置換。
    config.json の note_sheet_sales が空の間は何も出さない（note_box と重複するため）、値が入ったら販売ページへ。"""
    url = CFG.get("note_sheet_sales", "").strip()
    note = '<br><small>※運営者（電脳アリス）自身の有料記事の案内です（アフィリエイトではありません）。</small>'
    if url:
        link = f'<a href="{html.escape(url)}" rel="noopener">Googleシート版テンプレ（note）を見る →</a>' + note
    else:
        # 準備中の間は出さない（同じnote第1回への案内は記事末尾の note_box が出すため。2026-11-06 重複解消）
        return ''
    return ('<aside class="sheet-cta" style="margin:12px 0;padding:10px 14px;border:1px dashed var(--line,#ccc);'
            'border-radius:10px;font-size:.9rem">'
            f'<b>この計算を毎月の記録として残すなら</b><br>{link}</aside>')


SHORT_CELL = 10  # 数字を含むこの文字数以下の表セルは折り返さない（「約 / 4.2°C」のような途中改行を防ぐ。スマホ表示対策 2026-11-04）


def short_cell(m):
    """数字を含む短いセル（金額・温度など）に class="nw"（折り返し禁止）を付ける。文章セルはスマホ幅で折り返す。"""
    text = html.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
    if 0 < len(text) <= SHORT_CELL and re.search(r"[0-9０-９]", text):
        return f'<td class="nw"{m.group(1) or ""}>{m.group(2)}</td>'
    return m.group(0)


def jst_today():
    """日本時間の今日（コンテナはUTCのため）。"""
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date()


# 期限つき文言の目印 → 表示する最終日（JST）。過ぎたら「目印コメント＋次の1段落」を次のビルドで自動的に出さない
# （手作業の削除が遅れても、終わったセールの案内が残らないようにする保険。元の .md は消さない）
EXPIRE = {"marathon-2026-11": "2026-11-11T01:59"}  # 公式の終了 11/11(水)01:59（11/8 13時深掘りで楽天公式と照合）


def jst_now():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).replace(tzinfo=None)


def until_passed(last, now=None):
    """last＝表示する最後の日（YYYY-MM-DD・その日いっぱい）か最後の時刻（YYYY-MM-DDTHH:MM・その分いっぱい）。過ぎたら True"""
    now = now or jst_now()
    if isinstance(now, datetime.date) and not isinstance(now, datetime.datetime):
        now = datetime.datetime.combine(now, datetime.time(23, 59, 59))  # 日付だけ渡されたらその日の終わりで判定（従来どおり）
    if "T" in last:
        end = datetime.datetime.fromisoformat(last) + datetime.timedelta(seconds=59)
    else:
        end = datetime.datetime.combine(datetime.date.fromisoformat(last), datetime.time(23, 59, 59))
    return now > end


def expired(tag, today=None):
    last = EXPIRE.get(tag)
    return bool(last) and until_passed(last, today)


def strip_expired(md, today=None):
    """期限つき文言の出し分け。
    ・<!-- TAG ... -->＋次の段落 … 期限内だけ出す（過ぎたら消す）
    ・<!-- ended:TAG -->＋次の段落 … 期限が過ぎてから出す（「今回のセールは終了」の案内など。期限内は消す）"""
    for tag in EXPIRE:
        gone = expired(tag, today)
        ended = r"<!--\s*ended:" + re.escape(tag) + r"[^>]*-->\n((?:.+\n?)*)\n*"
        md = re.sub(ended, (lambda m: m.group(1) + "\n") if gone else "", md)
        if gone:
            md = re.sub(r"<!--\s*" + re.escape(tag) + r"[^>]*-->\n(?:.+\n?)*\n*", "", md)
    return md


def ended_description(meta, today=None):
    """front matter の ended_description: TAG|文 … 期限が過ぎたら description（一覧カード・検索結果の説明）を差し替える。"""
    v = meta.get("ended_description", "")
    if "|" in v:
        tag, text = v.split("|", 1)
        if expired(tag.strip(), today):
            meta["description"] = text.strip()
    return meta


_UNSHALLOW_TRIED = []


def git_date(p):
    """ファイルの最終コミット日（YYYY-MM-DD）。未コミットの変更があれば今日。取れなければ空文字。"""
    import subprocess
    if not _UNSHALLOW_TRIED:
        # 浅いclone（履歴の一部だけ）だと、古いファイルの更新日が「履歴の端の日付」に化けて
        # 毎回サイトマップの更新日がぶれる（2026-11-07 05:00に発見）。最初の1回だけ全履歴を取りに行く
        _UNSHALLOW_TRIED.append(1)
        try:
            if subprocess.run(["git", "rev-parse", "--is-shallow-repository"], cwd=ROOT,
                              capture_output=True, text=True, timeout=10).stdout.strip() == "true":
                subprocess.run(["git", "fetch", "-q", "--unshallow"], cwd=ROOT, capture_output=True, timeout=60)
        except Exception:
            pass
    try:
        env = {**os.environ, "TZ": "Asia/Tokyo"}  # コミット日は日本時間で数える（UTCだと0〜9時のコミットが前日になる）
        r = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, timeout=10, env=env).stdout.strip()
        if r("status", "--porcelain", "--", str(p)):
            return jst_today().isoformat()
        return r("log", "-1", "--format=%cd", "--date=format-local:%Y-%m-%d", "--", str(p))
    except Exception:
        return ""


def parse(p):
    raw = p.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    meta = dict(l.split(":", 1) for l in m.group(1).splitlines() if ":" in l)
    meta = {k.strip(): v.strip() for k, v in meta.items()}
    meta = ended_description(meta)
    body = markdown.markdown(strip_expired(m.group(2)), extensions=["tables", "toc"])
    body = re.sub(r"<td((?:\s(?![^>]*\bclass=)[^>]*)?)>(.*?)</td>", short_cell, body, flags=re.S)
    body = re.sub(r"<!--\s*sheet-cta\s*-->", sheet_cta, body)
    meta["body"] = re.sub(r"<!--\s*products:\s*(.*?)\s*-->", product_box, body)
    meta["slug"] = p.stem
    # 更新日：front matter の updated → 最終コミット日（未コミットなら今日）→ 公開日。公開日より前にはしない
    meta["modified"] = max(meta.get("updated") or git_date(p) or meta["date"], meta["date"])
    return meta


TITLE_MAX = 60  # <title> の目安上限（site_health.py と同じ）。超える長い記事タイトルはサイト名を付けない


def page_url(path):
    """公開URL。トップと各ディレクトリの index.html は末尾スラッシュのURLを正規URLにする（canonical・sitemap共通）"""
    if path == "index.html":
        return CFG["base_url"] + "/"
    if path.endswith("/index.html"):
        return f"{CFG['base_url']}/{path[:-len('index.html')]}"
    return f"{CFG['base_url']}/{path}"


FEED_URL = CFG["base_url"] + "/feed.xml"  # RSS 2.0（全記事・新しい順）。sitemap には入れない


def rss_feed(posts):
    """docs/feed.xml（RSS 2.0）。pubDate は公開日の 00:00 JST（記事は日付単位で管理しているため時刻は持たない）。
    RSSリーダー（Feedly等）やフィードを巡回するサービスからの発見経路用。"""
    import email.utils
    from xml.sax.saxutils import escape
    jst = datetime.timezone(datetime.timedelta(hours=9))
    rfc = lambda d: email.utils.format_datetime(datetime.datetime.fromisoformat(d).replace(tzinfo=jst))
    items = "".join(
        f'<item><title>{escape(x["title"])}</title><link>{CFG["base_url"]}/posts/{x["slug"]}.html</link>'
        f'<description>{escape(x["description"])}</description>'
        + (f'<category>{escape(x["category"])}</category>' if x.get("category") else "")
        + f'<pubDate>{rfc(x["date"])}</pubDate>'
        f'<guid isPermaLink="true">{CFG["base_url"]}/posts/{x["slug"]}.html</guid></item>' for x in posts)
    last = rfc(max((x["modified"] for x in posts), default=jst_today().isoformat()))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>'
           f'<title>{escape(CFG["site_name"])}</title><link>{CFG["base_url"]}/</link>'
           f'<description>{escape(CFG["tagline"] + "（AI・電脳アリスが運営）")}</description>'
           f'<language>ja</language><lastBuildDate>{last}</lastBuildDate>'
           f'<atom:link href="{FEED_URL}" rel="self" type="application/rss+xml"/>'
           f'{items}</channel></rss>\n')
    (OUT / "feed.xml").write_text(xml, encoding="utf-8")


def page(title, desc, body, path, prefix, ogtype="website", image="", jsonld=None):
    url = page_url(path)
    full = title if title == CFG["site_name"] else f"{title}｜{CFG['site_name']}"
    if len(full) > TITLE_MAX:
        full = title
    out = TPL
    ogimg = (f'<meta property="og:image" content="{image}">\n<meta property="og:image:width" content="1200">\n'
             f'<meta property="og:image:height" content="630">\n<meta name="twitter:image" content="{image}">\n') if image else ""
    ld = "".join('<script type="application/ld+json">'
                 + json.dumps(d, ensure_ascii=False).replace("</", "<\\/") + "</script>\n" for d in (jsonld or []))
    for k, v in {
        "{{ogtype}}": ogtype,
        "{{ogimage}}": ogimg,
        "{{twcard}}": "summary_large_image" if image else "summary",
        "{{jsonld}}": ld,
        "{{fulltitle}}": html.escape(full),
        "{{title}}": html.escape(title),
        "{{desc}}": html.escape(desc),
        "{{url}}": url,
        "{{feed}}": FEED_URL,
        "{{body}}": body,
        "{{p}}": prefix,
        "{{site}}": CFG["site_name"],
        "{{author}}": CFG["author"],
        "{{x}}": CFG["x"],
        "{{ig}}": CFG["instagram"],
        "{{note}}": CFG["note"],
        "{{year}}": str(jst_today().year),
    }.items():
        out = out.replace(k, v)
    f = OUT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(out, encoding="utf-8")
    return url

PALETTES = [("#3b5bdb", "#15aabf"), ("#7048e8", "#e64980"), ("#0ca678", "#3bc9db"),
            ("#f76707", "#fab005"), ("#1c7ed6", "#7048e8"), ("#e8590c", "#d6336c")]


def eyecatch(x):
    """記事ごとのアイキャッチSVGを生成（自作・著作権フリー）"""
    a, b = PALETTES[sum(map(ord, x["slug"])) % len(PALETTES)]
    t = x["title"].split("｜")[0]
    lines = [t[i:i + 16] for i in range(0, len(t), 16)][:3]
    tx = "".join(f'<text x="60" y="{230 + i * 70 - (len(lines) - 1) * 35}" font-size="52" font-weight="700" fill="#fff">{html.escape(l)}</text>'
                 for i, l in enumerate(lines))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" font-family="Noto Sans JP,Hiragino Sans,Meiryo,sans-serif">'
           f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs>'
           '<rect width="1200" height="630" fill="url(#g)"/>'
           '<circle cx="1080" cy="90" r="160" fill="#fff" opacity=".08"/><circle cx="1140" cy="560" r="220" fill="#fff" opacity=".06"/>'
           f'<rect x="60" y="70" rx="22" width="{60 + 26 * len(x.get("category", ""))}" height="44" fill="#fff" opacity=".22"/>'
           f'<text x="90" y="101" font-size="26" fill="#fff">{html.escape(x.get("category", ""))}</text>'
           f'{tx}<text x="60" y="570" font-size="28" fill="#fff" opacity=".9">QOLガジェット研究所 ／ 電脳アリス</text></svg>')
    f = OUT / "posts" / f"{x['slug']}.svg"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(svg, encoding="utf-8")


FONT = Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc")
ORG = {"@type": "Organization", "name": "QOLガジェット研究所（AI運営）", "url": CFG["base_url"] + "/"}


# OGPタイトルの改行用：語のかたまり（漢字・カタカナ・英数字の連続＋後ろのひらがな＋閉じ記号）を割らない
_OG_TOKEN = re.compile(
    r"[「『（(【]*"
    r"(?:[\u4e00-\u9fff\u3005\u30a1-\u30fa\u30fc-\u30ffA-Za-z0-9.%¥+\-/()〜~]+[\u3041-\u309f]*|[\u3041-\u309f]+|.)"
    r"[、。，．）」』】！？!?・ー)]*")


def og_lines(text, width, maxw):
    """text を幅 maxw 以内の行に分ける。語の途中では切らず、1語が1行より長いときだけ文字単位で切る。
    行が6割を超えていて、直前が「、・？！」で終わっていれば、そこで早めに改行する（読みやすさ優先）。"""
    lines, cur = [], ""
    for tok in _OG_TOKEN.findall(text):
        if cur and width(cur + tok) > maxw:
            lines.append(cur); cur = ""
        elif cur and cur[-1] in "、・？！?!" and width(cur) > maxw * 0.6 and width(cur + tok) > maxw * 0.85:
            lines.append(cur); cur = ""
        while width(tok) > maxw:  # 1語が長すぎる場合の保険
            i = 1
            while width(tok[:i + 1]) <= maxw:
                i += 1
            lines.append(tok[:i]); tok = tok[i:]
        cur += tok
    return lines + [cur] if cur else lines


def og_png(slug, title, category=""):
    """SNS共有用の1200×630 PNG（docs/og/<slug>.png）。PILか日本語フォントが無ければ作らず空文字を返す。"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        big, mid = (ImageFont.truetype(str(FONT), n, index=0) for n in (60, 30))
    except Exception:
        return ""
    a, b = PALETTES[sum(map(ord, slug)) % len(PALETTES)]
    ca, cb = (tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for c in (a, b))
    im = Image.new("RGB", (1200, 630))
    d = ImageDraw.Draw(im)
    for y in range(630):  # 縦グラデーション
        t = y / 629
        d.line([(0, y), (1200, y)], fill=tuple(round(ca[i] + (cb[i] - ca[i]) * t) for i in range(3)))
    text = title.split("｜")[0]
    for size in (60, 54, 48):  # 3行に収まらなければ文字を小さくする
        big = ImageFont.truetype(str(FONT), size, index=0)
        lines = og_lines(text, lambda t: d.textlength(t, font=big), 1080)
        if len(lines) <= 3:
            break
    lines, step = lines[:3], round(size * 1.4)
    y0 = 315 - len(lines) * step // 2
    for i, l in enumerate(lines):
        d.text((60, y0 + i * step), l, font=big, fill="white")
    if category:
        d.rounded_rectangle([60, 70, 100 + d.textlength(category, font=mid), 122], radius=24, fill=tuple(min(255, c + 40) for c in ca))
        d.text((80, 76), category, font=mid, fill="white")
    d.text((60, 545), "QOLガジェット研究所 ／ 電脳アリス（AI運営）", font=mid, fill="white")
    f = OUT / "og" / f"{slug}.png"
    f.parent.mkdir(parents=True, exist_ok=True)
    im.save(f, optimize=True)
    return f"{CFG['base_url']}/og/{slug}.png"


def article_ld(x, url, image):
    art = {"@context": "https://schema.org", "@type": "Article", "headline": x["title"][:110],
           "description": x["description"], "datePublished": x["date"],
           "dateModified": x["modified"], "mainEntityOfPage": url,
           "author": ORG, "publisher": ORG, "inLanguage": "ja"}
    if image:
        art["image"] = image
    crumbs = [("トップ", CFG["base_url"] + "/"), (x["title"], url)]  # カテゴリページは無いので2階層
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]}
    return [art, bc]


def wants_note_box(x):
    """末尾に「運営の実録（有料note第1回）」枠を出す記事：無料ツール一覧（TOOLS）に載っている記事と、タイトルに「電気代」を含む記事。"""
    return f'posts/{x["slug"]}.html' in {t[0] for t in TOOLS} or "電気代" in x["title"]


def own_note_link(x):
    """本文に自分でnote記事へのリンク（> の1行など）を入れた記事。共通のnote枠・1行案内は重なるので出さない（2026-11-10 16:00、無料回リンクの試行5記事）。"""
    return "note.com/zaqmaster/n/" in x["body"]


def note_box():
    """有料note第1回（config.json の note_vol1）への共通の1枠。自社の有料記事でアフィリエイトではないためPR表記はせず、有料であることを明記する。"""
    return ('<aside class="note-box" aria-label="運営の実録（note）">'
            '<p><b>このサイトはAIが運営しています。</b>運営の実録（売上・失敗も公開）はnoteで → '
            f'<a href="{html.escape(CFG["note_vol1"])}" rel="noopener">第1回「AIだけで3ヶ月300万円に挑戦します」</a>'
            '（<b>有料¥300</b>・途中まで無料で読めます）</p>'
            '<p class="meta">※運営者（電脳アリス）自身の有料記事の案内です（アフィリエイト・広告ではありません）。</p></aside>')


def related(x, posts, n=3):
    """同カテゴリ優先で関連記事を最大n本（内部リンク・回遊用）。note枠を出す記事では、下の1行の案内は枠と重なるので省く。"""
    others = [y for y in posts if y["slug"] != x["slug"]]
    others.sort(key=lambda y: y["date"], reverse=True)
    others.sort(key=lambda y: y.get("category") != x.get("category"))
    items = "".join(f'<li><a href="{y["slug"]}.html">{html.escape(y["title"])}</a></li>' for y in others[:n])
    if wants_note_box(x) or own_note_link(x):
        return f'<section class="related"><h2>あわせて読みたい</h2><ul>{items}</ul></section>'
    return (f'<section class="related"><h2>あわせて読みたい</h2><ul>{items}</ul>'
            '<p class="meta">このサイトはAI（電脳アリス）が運営しています。運営の実録は<a href="../about.html">このサイトについて</a>と'
            f'<a href="{CFG["note"]}" rel="noopener">note</a>で公開中'
            f'（第1回：<a href="{CFG["note_vol1"]}" rel="noopener">AIだけで3ヶ月300万円に挑戦します</a>／途中まで無料・続きは¥300）。</p></section>')


# トップの導線ブロック（冬の電気代ハブ＋無料ツール一覧）。リンク先が docs/ に無いものは出さない。
HUB = ("posts/fuyu-denkidai-matome.html", "冬の電気代まとめ",
       "暖房・加湿・エアコン自動化の電気代を、悩み別に記事とツールで整理")
# 期間限定の特集（4つ目＝表示する最終日 JST。過ぎたら次のビルドで自動的に消える）
SALE = ("posts/rakuten-marathon-fuyu-kaden-list.html", "楽天お買い物マラソン前の冬家電チェックリスト【PR】",
        "11/4 20:00〜11/11 01:59。電気代で選ぶ暖房・加湿器など", "2026-11-11T01:59")
# 4つ目の要素（任意）＝表示する最終日（JST、この日まで先頭に出す。過ぎたら次のビルドで自動的に消える）
TOOLS = [
    ("posts/rakuten-marathon-point-calculator.html", "楽天お買い物マラソン 買いまわり計算（非公式）",
     "何店舗で何倍か・あと何店舗かの目安。条件は楽天公式で確認", "2026-11-11T01:59"),
    ("posts/denkidai-calculator.html", "電気代計算", "W数と時間で1日・1ヶ月・ひと冬の目安"),
    ("posts/aircon-danbou-denkidai-calculator.html", "エアコン暖房の電気代計算", "W数と時間で1時間・1日・1ヶ月・ひと冬の目安"),
    ("posts/heater-denkidai-hikaku.html", "暖房器具の電気代比較", "エアコン・ヒーター・こたつを並べて計算"),
    ("posts/neru-danbou-denkidai-calculator.html", "寝るときの暖房 電気代くらべ", "電気毛布・湯たんぽ・エアコンの一晩と1か月の目安"),
    ("posts/mobile-battery-jikan-calculator.html", "モバイルバッテリー何時間もつ？計算", "mAhとW数で使える時間と充電1回の電気代"),
    ("posts/kashitsu-ryo-calculator.html", "加湿量計算", "部屋に合う加湿器のmL/hを計算"),
    ("posts/winter-heating-shindan.html", "冬の寒さ対策診断", "5問で最初に試す対策がわかる"),
    ("posts/smart-remote-count-shindan.html", "スマートリモコン台数診断", "6問で必要台数がわかる"),
    ("apps/sub-check/", "サブスク見直しチェッカー", "月額・年額を一覧にして固定費を見直す"),
]


APP_CATEGORY = {"sub-check": "FinanceApplication"}  # schema.org の applicationCategory（無ければ UtilitiesApplication）
APP_MARK = ("<!-- og:auto（build.py が生成。手で編集しない） -->", "<!-- /og:auto -->")


def app_meta(f):
    """手書きの無料ツール（docs/apps/<名前>/index.html）に、他ページと同じ形式の OGP・twitter・JSON-LD を差し込む。
    title / description は HTML 自身から読み、マーカーの間だけを毎回作り直す（本文・スクリプトは触らない）。"""
    s = f.read_text(encoding="utf-8")
    name = f.parent.name
    rel = f.relative_to(OUT).as_posix()
    url = page_url(rel)
    mt = re.search(r"<title>(.*?)</title>", s, re.S)
    md = re.search(r'<meta name="description" content="([^"]*)"', s)
    if not (mt and md):
        return
    full = html.unescape(mt.group(1).strip())
    title = full.split("｜")[0]
    desc = html.unescape(md.group(1))
    img = og_png(f"app-{name}", title, "無料ツール")
    ogimg = (f'<meta property="og:image" content="{img}">\n<meta property="og:image:width" content="1200">\n'
             f'<meta property="og:image:height" content="630">\n<meta name="twitter:image" content="{img}">\n') if img else ""
    e = lambda v: html.escape(v, quote=True)
    ld = [{"@context": "https://schema.org", "@type": "WebApplication", "name": title, "url": url,
           "description": desc, "applicationCategory": APP_CATEGORY.get(name, "UtilitiesApplication"),
           "operatingSystem": "Web", "inLanguage": "ja", "isAccessibleForFree": True,
           "offers": {"@type": "Offer", "price": "0", "priceCurrency": "JPY"},
           "publisher": ORG},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "トップ", "item": CFG["base_url"] + "/"},
              {"@type": "ListItem", "position": 2, "name": title, "item": url}]}]
    block = (f'{APP_MARK[0]}\n<meta property="og:title" content="{e(title)}">\n'
             f'<meta property="og:description" content="{e(desc)}">\n<meta property="og:url" content="{url}">\n'
             f'<meta property="og:type" content="website">\n<meta property="og:site_name" content="{e(CFG["site_name"])}">\n'
             f'<meta property="og:locale" content="ja_JP">\n{ogimg}'
             f'<meta name="twitter:card" content="{"summary_large_image" if img else "summary"}">\n'
             f'<meta name="twitter:site" content="@qol_gadget_life">\n'
             + "".join('<script type="application/ld+json">'
                       + json.dumps(d, ensure_ascii=False).replace("</", "<\\/") + "</script>\n" for d in ld)
             + APP_MARK[1])
    if APP_MARK[0] in s:
        s2 = re.sub(re.escape(APP_MARK[0]) + r".*?" + re.escape(APP_MARK[1]), lambda _: block, s, count=1, flags=re.S)
    else:  # 初回：canonical の直後（無ければ </title> の直後）に入れる
        anchor = re.search(r'<link rel="canonical"[^>]*>', s) or re.search(r"</title>", s)
        s2 = s[:anchor.end()] + "\n" + block + s[anchor.end():]
    if s2 != s:
        f.write_text(s2, encoding="utf-8")


def hub_block():
    ok = lambda p: (OUT / p).exists()
    live = lambda t: len(t) < 4 or not until_passed(t[3])
    tools = "".join(f'<li><a href="{t[0]}"><b>{html.escape(t[1])}</b><span>{html.escape(t[2])}</span></a></li>'
                    for t in TOOLS if ok(t[0]) and live(t))
    hub = (f'<a class="hub-main" href="{HUB[0]}"><span class="badge">特集</span><b>{HUB[1]}</b>'
           f'<span>{HUB[2]} →</span></a>') if ok(HUB[0]) else ""
    if ok(SALE[0]) and live(SALE):
        hub = (f'<a class="hub-main" href="{SALE[0]}"><span class="badge">期間限定</span><b>{html.escape(SALE[1])}</b>'
               f'<span>{html.escape(SALE[2])} →</span></a><div style="height:10px"></div>') + hub
    if not (hub or tools):
        return ""
    return (f'<section class="hub" aria-label="特集と無料ツール">{hub}'
            + (f'<h2>無料ツール</h2><ul class="tools">{tools}</ul>' if tools else "") + '</section>')


def main():
    posts = sorted((parse(p) for p in (ROOT / "content" / "posts").glob("*.md")),
                   key=lambda x: x["date"], reverse=True)
    urls = []
    for x in posts:
        eyecatch(x)
        body = (f'<article><img class="eye" src="{x["slug"]}.svg" alt="{html.escape(x["title"])}" width="1200" height="630"><p class="meta">{x["date"]}・{html.escape(x.get("category",""))}</p>'
                f'<h1>{html.escape(x["title"])}</h1>'
                '<p class="pr">※本記事はアフィリエイト広告を含みます。内容はAI（電脳アリス）が公開情報をもとに作成しています。</p>'
                f'{x["body"]}{note_box() if wants_note_box(x) and not own_note_link(x) else ""}{related(x, posts)}</article>')
        path = f"posts/{x['slug']}.html"
        img = og_png(x["slug"], x["title"], x.get("category", ""))
        urls.append((page(x["title"], x["description"], body, path, "../", "article", img,
                          article_ld(x, f"{CFG['base_url']}/{path}", img)), x["modified"]))
    cards = "".join(
        f'<a class="card" href="posts/{x["slug"]}.html"><img class="eye" src="posts/{x["slug"]}.svg" alt="" width="1200" height="630" loading="lazy"><span class="meta">{x["date"]}・{html.escape(x.get("category",""))}</span>'
        f'<h2>{html.escape(x["title"])}</h2><p>{html.escape(x["description"])}</p></a>' for x in posts)
    hero = (f'<section class="hero"><h1>{CFG["site_name"]}</h1><p>{CFG["tagline"]}</p></section>'
            f'{hub_block()}'
            f'<section class="list">{cards or "<p>記事を準備中です。</p>"}</section>')
    site_img = og_png("index", CFG["tagline"], CFG["site_name"])
    site_desc = (CFG["tagline"] + "電気代計算・暖房器具の比較・加湿量計算などの無料ツールと、"
                 "在宅ワークのQOLを上げるガジェットの比較記事を公開しています（AI運営）。")
    site_ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": CFG["site_name"],
                "url": CFG["base_url"] + "/", "inLanguage": "ja", "publisher": ORG}]
    newest = max((d for _, d in urls), default=jst_today().isoformat())
    urls.append((page(CFG["site_name"], site_desc, hero, "index.html", "", "website", site_img, site_ld), newest))
    for name in ["about"]:
        src = (ROOT / "content" / f"{name}.md").read_text(encoding="utf-8")
        t = src.splitlines()[0].lstrip("# ")
        # description：見出し・リンク記法を除いた本文の冒頭（タイトルの繰り返しにしない）
        plain = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", "".join(l for l in src.splitlines()[1:] if not l.startswith("#")))
        d = re.sub(r"[*_`]", "", plain).strip()
        d = d if len(d) <= 120 else d[:119] + "…"
        urls.append((page(t, d, f"<article>{markdown.markdown(src)}</article>", f"{name}.html", "", "website", site_img),
                     git_date(ROOT / "content" / f"{name}.md") or newest))
    # 無料ツール（docs/apps/<名前>/index.html、手書きのHTML）も sitemap に載せる
    for f in sorted((OUT / "apps").glob("*/index.html")):
        rel = f.relative_to(OUT).as_posix()
        app_meta(f)
        urls.append((page_url(rel), git_date(f) or newest))
    # SNS画像の元HTML・IG素材ページ（docs/sns/**/*.html）は検索に出さない（sitemapにも入れない）
    for f in sorted((OUT / "sns").rglob("*.html")):
        s = f.read_text(encoding="utf-8")
        if 'name="robots"' not in s:
            s2 = re.sub(r"(<head[^>]*>)", r'\1<meta name="robots" content="noindex">', s, count=1)
            if s2 != s:
                f.write_text(s2, encoding="utf-8")
    (OUT / ".nojekyll").write_text("")
    # IndexNow の鍵ファイル（docs/<key>.txt、中身は鍵だけ）。仕様上公開ファイル。ops/seo/indexnow.md 参照
    key = CFG.get("indexnow_key", "").strip()
    if re.fullmatch(r"[A-Za-z0-9-]{8,128}", key):
        (OUT / f"{key}.txt").write_text(key, encoding="utf-8")
    rss_feed(posts)
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {CFG['base_url']}/sitemap.xml\n")
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(f"<url><loc>{u}</loc><lastmod>{d}</lastmod></url>" for u, d in urls) + "</urlset>", encoding="utf-8")
    print(f"built {len(posts)} posts")


if __name__ == "__main__":
    main()
