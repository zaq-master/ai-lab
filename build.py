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
import json, re, html, datetime
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


def parse(p):
    raw = p.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    meta = dict(l.split(":", 1) for l in m.group(1).splitlines() if ":" in l)
    meta = {k.strip(): v.strip() for k, v in meta.items()}
    body = markdown.markdown(m.group(2), extensions=["tables", "toc"])
    meta["body"] = re.sub(r"<!--\s*products:\s*(.*?)\s*-->", product_box, body)
    meta["slug"] = p.stem
    return meta


def page(title, desc, body, path, prefix):
    url = f"{CFG['base_url']}/{path}"
    out = TPL
    for k, v in {
        "{{title}}": html.escape(title),
        "{{desc}}": html.escape(desc),
        "{{url}}": url,
        "{{body}}": body,
        "{{p}}": prefix,
        "{{site}}": CFG["site_name"],
        "{{author}}": CFG["author"],
        "{{x}}": CFG["x"],
        "{{ig}}": CFG["instagram"],
        "{{note}}": CFG["note"],
        "{{year}}": str(datetime.date.today().year),
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


def related(x, posts, n=3):
    """同カテゴリ優先で関連記事を最大n本（内部リンク・回遊用）"""
    others = [y for y in posts if y["slug"] != x["slug"]]
    others.sort(key=lambda y: y["date"], reverse=True)
    others.sort(key=lambda y: y.get("category") != x.get("category"))
    items = "".join(f'<li><a href="{y["slug"]}.html">{html.escape(y["title"])}</a></li>' for y in others[:n])
    return (f'<section class="related"><h2>あわせて読みたい</h2><ul>{items}</ul>'
            '<p class="meta">このサイトはAI（電脳アリス）が運営しています。運営の実録は<a href="../about.html">このサイトについて</a>と'
            f'<a href="{CFG["note"]}" rel="noopener">note</a>で公開中'
            f'（第1回：<a href="{CFG["note_vol1"]}" rel="noopener">AIだけで3ヶ月300万円に挑戦します</a>／一部有料）。</p></section>')


# トップの導線ブロック（冬の電気代ハブ＋無料ツール一覧）。リンク先が docs/ に無いものは出さない。
HUB = ("posts/fuyu-denkidai-matome.html", "冬の電気代まとめ",
       "暖房・加湿・エアコン自動化の電気代を、悩み別に記事とツールで整理")
TOOLS = [
    ("posts/denkidai-calculator.html", "電気代計算", "W数と時間で1日・1ヶ月・ひと冬の目安"),
    ("posts/heater-denkidai-hikaku.html", "暖房器具の電気代比較", "エアコン・ヒーター・こたつを並べて計算"),
    ("posts/kashitsu-ryo-calculator.html", "加湿量計算", "部屋に合う加湿器のmL/hを計算"),
    ("posts/winter-heating-shindan.html", "冬の寒さ対策診断", "5問で最初に試す対策がわかる"),
    ("posts/smart-remote-count-shindan.html", "スマートリモコン台数診断", "6問で必要台数がわかる"),
    ("apps/sub-check/index.html", "サブスク見直しチェッカー", "月額・年額を一覧にして固定費を見直す"),
]


def hub_block():
    ok = lambda p: (OUT / p).exists()
    tools = "".join(f'<li><a href="{p}"><b>{html.escape(n)}</b><span>{html.escape(d)}</span></a></li>'
                    for p, n, d in TOOLS if ok(p))
    hub = (f'<a class="hub-main" href="{HUB[0]}"><span class="badge">特集</span><b>{HUB[1]}</b>'
           f'<span>{HUB[2]} →</span></a>') if ok(HUB[0]) else ""
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
                f'{x["body"]}{related(x, posts)}</article>')
        urls.append(page(x["title"], x["description"], body, f"posts/{x['slug']}.html", "../"))
    cards = "".join(
        f'<a class="card" href="posts/{x["slug"]}.html"><img class="eye" src="posts/{x["slug"]}.svg" alt="" width="1200" height="630" loading="lazy"><span class="meta">{x["date"]}・{html.escape(x.get("category",""))}</span>'
        f'<h2>{html.escape(x["title"])}</h2><p>{html.escape(x["description"])}</p></a>' for x in posts)
    hero = (f'<section class="hero"><h1>{CFG["site_name"]}</h1><p>{CFG["tagline"]}</p></section>'
            f'{hub_block()}'
            f'<section class="list">{cards or "<p>記事を準備中です。</p>"}</section>')
    urls.append(page(CFG["site_name"], CFG["tagline"], hero, "index.html", ""))
    for name in ["about"]:
        src = (ROOT / "content" / f"{name}.md").read_text(encoding="utf-8")
        t = src.splitlines()[0].lstrip("# ")
        urls.append(page(t, t, f"<article>{markdown.markdown(src)}</article>", f"{name}.html", ""))
    (OUT / ".nojekyll").write_text("")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {CFG['base_url']}/sitemap.xml\n")
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(f"<url><loc>{u}</loc><lastmod>{datetime.date.today().isoformat()}</lastmod></url>" for u in urls) + "</urlset>", encoding="utf-8")
    print(f"built {len(posts)} posts")


if __name__ == "__main__":
    main()
