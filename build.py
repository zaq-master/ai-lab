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


def parse(p):
    raw = p.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    meta = dict(l.split(":", 1) for l in m.group(1).splitlines() if ":" in l)
    meta = {k.strip(): v.strip() for k, v in meta.items()}
    meta["body"] = markdown.markdown(m.group(2), extensions=["tables", "toc"])
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


def main():
    posts = sorted((parse(p) for p in (ROOT / "content" / "posts").glob("*.md")),
                   key=lambda x: x["date"], reverse=True)
    urls = []
    for x in posts:
        body = (f'<article><p class="meta">{x["date"]}・{html.escape(x.get("category",""))}</p>'
                f'<h1>{html.escape(x["title"])}</h1>'
                '<p class="pr">※本記事はアフィリエイト広告を含みます。内容はAI（電脳アリス）が公開情報をもとに作成しています。</p>'
                f'{x["body"]}</article>')
        urls.append(page(x["title"], x["description"], body, f"posts/{x['slug']}.html", "../"))
    cards = "".join(
        f'<a class="card" href="posts/{x["slug"]}.html"><span class="meta">{x["date"]}・{html.escape(x.get("category",""))}</span>'
        f'<h2>{html.escape(x["title"])}</h2><p>{html.escape(x["description"])}</p></a>' for x in posts)
    hero = (f'<section class="hero"><h1>{CFG["site_name"]}</h1><p>{CFG["tagline"]}</p></section>'
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
        + "".join(f"<url><loc>{u}</loc></url>" for u in urls) + "</urlset>", encoding="utf-8")
    print(f"built {len(posts)} posts")


if __name__ == "__main__":
    main()
