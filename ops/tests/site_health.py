#!/usr/bin/env python3
"""サイトの技術的な健康診断（docs/ 配下の全HTML）。
実行：python3 ops/tests/site_health.py            # 静的チェックのみ
      python3 ops/tests/site_health.py --browser  # + Playwrightで375px幅のはみ出し・コンソールエラー
終了コード：問題0件なら0、あれば1。

チェック項目
- 内部リンク切れ（相対・絶対 base_url 含む）、画像・OGP画像の欠落、img の alt 欠落
- title / meta description の有無・重複・長さ、canonical の有無と正しさ、h1 が1つ、lang="ja"、viewport
- sitemap.xml と公開ページの突き合わせ（漏れ・存在しないURL）
- OGP（og:title・og:description・og:url・og:image・twitter:card）の有無
- RSSフィード（feed.xml）がXMLとして読め、link/guid がすべて実在の公開ページで、全記事を含み、sitemap に入っていないこと
- JSON-LD が JSON として読めるか
- af.moshimo.com のリンクがあるページに「PR」「広告」表記があるか
- SNS画像の元HTML（docs/sns/*.src.html）は検索に出さない（noindex）こと
"""
import json, re, sys, subprocess, threading, functools, http.server, socketserver
from pathlib import Path
from urllib.parse import urlparse, unquote
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
BASE = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))["base_url"].rstrip("/")
BASE_PATH = urlparse(BASE).path  # /ai-lab
SITE = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))["site_name"]

TITLE_MAX = 60      # 日本語タイトルは検索結果で概ね30〜35字前後で切れる。サイト名込みで60字を上限の目安に
DESC_MIN, DESC_MAX = 50, 160

issues = []


def add(kind, page, msg):
    issues.append((kind, page, msg))


def is_aux(rel):
    """SNS画像の元HTMLなど、公開ページ扱いしないもの"""
    return rel.startswith("sns/") or rel.endswith(".src.html")


def url_of(rel):
    """docs 内の相対パス → 公開URL（index.html はディレクトリURL）"""
    if rel == "index.html":
        return BASE + "/"
    if rel.endswith("/index.html"):
        return f"{BASE}/{rel[:-len('index.html')]}"
    return f"{BASE}/{rel}"


def resolve(page_rel, href):
    """リンク先 → docs 内のファイル（外部なら None）"""
    href = href.strip()
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None
    u = urlparse(href)
    if u.scheme in ("http", "https"):
        if not (href + "/").startswith(BASE + "/"):
            return None
        path = u.path[len(BASE_PATH):].lstrip("/")
    elif u.scheme:
        return None
    elif href.startswith("/"):
        if not u.path.startswith(BASE_PATH + "/") and u.path != BASE_PATH:
            return ("ABS", u.path)  # /ai-lab を付けない絶対パスは本番で404
        path = u.path[len(BASE_PATH):].lstrip("/")
    else:
        path = str((Path(page_rel).parent / unquote(u.path)))
    p = (DOCS / path)
    try:
        p = p.resolve()
    except Exception:
        pass
    if p.is_dir() or path.endswith("/") or path == "":
        p = p / "index.html"
    return p


def check_pages():
    pages = sorted(DOCS.rglob("*.html"))
    titles, descs = {}, {}
    public = []
    for f in pages:
        rel = f.relative_to(DOCS).as_posix()
        soup = BeautifulSoup(f.read_text(encoding="utf-8"), "html.parser")
        if is_aux(rel):
            rb = soup.find("meta", attrs={"name": "robots"})
            if not rb or "noindex" not in rb.get("content", ""):
                add("noindex", rel, "SNS画像の元HTMLに noindex がない（検索に低品質ページとして出る）")
            continue
        public.append(rel)
        # 基本タグ
        h = soup.find("html")
        if not h or h.get("lang") != "ja":
            add("lang", rel, 'html lang="ja" がない')
        vp = soup.find("meta", attrs={"name": "viewport"})
        if not vp or "width=device-width" not in vp.get("content", ""):
            add("viewport", rel, "viewport がない")
        t = soup.title.get_text(strip=True) if soup.title else ""
        if not t:
            add("title", rel, "title がない")
        else:
            titles.setdefault(t, []).append(rel)
            if t.count(SITE) > 1:
                add("title", rel, f"title にサイト名が重複: {t}")
            if len(t) > TITLE_MAX:
                add("title-len", rel, f"title が長い（{len(t)}字）")
        d = soup.find("meta", attrs={"name": "description"})
        d = d.get("content", "").strip() if d else ""
        if not d:
            add("desc", rel, "meta description がない")
        else:
            descs.setdefault(d, []).append(rel)
            if not (DESC_MIN <= len(d) <= DESC_MAX):
                add("desc-len", rel, f"description の長さ {len(d)}字（目安 {DESC_MIN}〜{DESC_MAX}）")
        c = soup.find("link", rel="canonical")
        want = url_of(rel)
        if not c:
            add("canonical", rel, "canonical がない")
        elif c.get("href") != want:
            add("canonical", rel, f"canonical が {c.get('href')}（期待 {want}）")
        # OGP の有無（SNSで共有したときのカード）：全公開ページに必須
        for p in ("og:title", "og:description", "og:url", "og:image"):
            m = soup.find("meta", property=p)
            if not m or not m.get("content", "").strip():
                add("ogp", rel, f"{p} がない")
        tc = soup.find("meta", attrs={"name": "twitter:card"})
        if not tc or not tc.get("content", "").strip():
            add("ogp", rel, "twitter:card がない")
        ogu = soup.find("meta", property="og:url")
        if ogu and ogu.get("content") != want:
            add("og:url", rel, f"og:url が {ogu.get('content')}（期待 {want}）")
        n_h1 = len(soup.find_all("h1"))
        if n_h1 != 1:
            add("h1", rel, f"h1 が {n_h1} 個")
        # JSON-LD
        for s in soup.find_all("script", type="application/ld+json"):
            try:
                json.loads(s.string or "")
            except Exception as e:
                add("jsonld", rel, f"JSON-LD が壊れている: {e}")
        # OGP画像
        for m in soup.find_all("meta", attrs={"property": "og:image"}) + soup.find_all("meta", attrs={"name": "twitter:image"}):
            tgt = resolve(rel, m.get("content", ""))
            if tgt is None or (isinstance(tgt, Path) and not tgt.exists()):
                add("ogimage", rel, f"OGP画像がない: {m.get('content')}")
        # 画像
        for img in soup.find_all("img"):
            src = img.get("src", "")
            if img.get("alt") is None:
                add("alt", rel, f"alt がない: {src[:80]}")
            tgt = resolve(rel, src)
            if isinstance(tgt, tuple):
                add("img", rel, f"/ai-lab なしの絶対パス: {src}")
            elif isinstance(tgt, Path) and not tgt.exists():
                add("img", rel, f"画像が見つからない: {src}")
        # 内部リンク
        for a in soup.find_all("a", href=True):
            tgt = resolve(rel, a["href"])
            if isinstance(tgt, tuple):
                add("link", rel, f"/ai-lab なしの絶対パス: {a['href']}")
            elif isinstance(tgt, Path) and not tgt.exists():
                add("link", rel, f"リンク切れ: {a['href']}")
        # ステマ規制：広告リンクのあるページに PR/広告 表記
        txt = soup.get_text()
        if soup.find("a", href=re.compile(r"af\.moshimo\.com")) or "af.moshimo.com" in str(soup.find_all("script")):
            if not re.search(r"PR|広告", txt):
                add("pr", rel, "広告リンクがあるのに PR/広告 表記がない")
    for t, rs in titles.items():
        if len(rs) > 1:
            add("title-dup", ", ".join(rs), f"title が重複: {t}")
    for d, rs in descs.items():
        if len(rs) > 1:
            add("desc-dup", ", ".join(rs), f"description が重複: {d[:40]}…")
    return public


def check_sitemap(public):
    sm = DOCS / "sitemap.xml"
    if not sm.exists():
        add("sitemap", "sitemap.xml", "sitemap.xml がない")
        return
    locs = re.findall(r"<loc>(.*?)</loc>", sm.read_text(encoding="utf-8"))
    want = {url_of(r) for r in public}
    for u in locs:
        if u not in want:
            add("sitemap", "sitemap.xml", f"公開ページに無い/正規URLでないURL: {u}")
    for u in sorted(want - set(locs)):
        add("sitemap", "sitemap.xml", f"sitemap に無い: {u}")
    if len(locs) != len(set(locs)):
        add("sitemap", "sitemap.xml", "URLが重複している")


def check_feed(public):
    """docs/feed.xml（RSS 2.0）：XMLとして読めるか、link/guid がすべて実在の公開ページか、全記事が入っているか、
    sitemap に入っていないか、トップに <link rel="alternate"> があるか"""
    import xml.etree.ElementTree as ET
    fd = DOCS / "feed.xml"
    if not fd.exists():
        add("feed", "feed.xml", "feed.xml がない")
        return
    try:
        root = ET.parse(fd).getroot()
    except ET.ParseError as e:
        add("feed", "feed.xml", f"XMLとして読めない: {e}")
        return
    ch = root.find("channel")
    if root.tag != "rss" or ch is None:
        add("feed", "feed.xml", "RSS 2.0 の rss/channel がない")
        return
    want = {url_of(r) for r in public}
    seen = set()
    for it in ch.findall("item"):
        for tag in ("title", "link", "description", "pubDate", "guid"):
            if not (it.findtext(tag) or "").strip():
                add("feed", "feed.xml", f"item に {tag} がない: {it.findtext('link')}")
        for tag in ("link", "guid"):
            u = (it.findtext(tag) or "").strip()
            if u and u not in want:
                add("feed", "feed.xml", f"{tag} が実在の公開ページでない: {u}")
        seen.add((it.findtext("link") or "").strip())
    for r in public:
        if r.startswith("posts/") and url_of(r) not in seen:
            add("feed", "feed.xml", f"記事がフィードに無い: {url_of(r)}")
    sm = DOCS / "sitemap.xml"
    if sm.exists() and "feed.xml" in sm.read_text(encoding="utf-8"):
        add("feed", "sitemap.xml", "フィードが sitemap に入っている")
    top = (DOCS / "index.html").read_text(encoding="utf-8") if (DOCS / "index.html").exists() else ""
    if f'href="{BASE}/feed.xml"' not in top or "application/rss+xml" not in top:
        add("feed", "index.html", 'トップに <link rel="alternate" type="application/rss+xml"> がない')


# 主要ツールページ（JSが動くページ）
BROWSER_PAGES = ["index.html", "apps/sub-check/index.html", "posts/denkidai-calculator.html",
                 "posts/heater-denkidai-hikaku.html", "posts/neru-danbou-denkidai-calculator.html",
                 "posts/kashitsu-ryo-calculator.html",
                 "posts/winter-heating-shindan.html", "posts/smart-remote-count-shindan.html",
                 "posts/fuyu-denkidai-matome.html"]

JS = r"""
const { chromium } = require('playwright');
(async () => {
  const [port, ...pages] = process.argv.slice(1);
  const b = await chromium.launch();
  const out = [];
  for (const p of pages) {
    const ctx = await b.newContext({ viewport: { width: 375, height: 800 }, deviceScaleFactor: 1 });
    const pg = await ctx.newPage();
    const errs = [];
    pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    pg.on('pageerror', e => errs.push('pageerror: ' + e.message));
    // 外部（フォント・アフィリエイト）は環境で繋がらないため止めて、ページ自身のエラーだけを見る
    await pg.route('**/*', r => r.request().url().startsWith('http://127.0.0.1') ? r.continue() : r.abort());
    await pg.goto(`http://127.0.0.1:${port}/${p}`, { waitUntil: 'load' });
    await pg.waitForTimeout(300);
    const ov = await pg.evaluate(() => {
      const W = document.documentElement.clientWidth;
      const wide = [];
      for (const el of document.querySelectorAll('body *')) {
        const r = el.getBoundingClientRect();
        if (r.width && r.right > W + 1) {
          let a = el.parentElement, clipped = false;  // overflow:auto の箱の中（表など）は許容
          while (a && a !== document.body) { const s = getComputedStyle(a).overflowX; if (s === 'auto' || s === 'scroll' || s === 'hidden') { clipped = true; break; } a = a.parentElement; }
          if (!clipped) wide.push(el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : '') + '(' + Math.round(r.right) + ')');
        }
      }
      return { sw: document.documentElement.scrollWidth, W, wide: wide.slice(0, 5) };
    });
    out.push({ page: p, errs: errs.filter(e => !/ERR_FAILED|net::|Failed to load resource/.test(e)), ...ov });
    await ctx.close();
  }
  await b.close();
  console.log(JSON.stringify(out));
})();
"""


def check_browser():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    handler = functools.partial(Quiet, directory=str(DOCS))
    srv = socketserver.TCPServer(("127.0.0.1", 0), handler)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        pages = [p for p in BROWSER_PAGES if (DOCS / p).exists()]
        r = subprocess.run(["node", "-e", JS, str(port), *pages], capture_output=True, text=True, timeout=180, cwd=ROOT)
        if r.returncode != 0:
            add("browser", "-", f"Playwright 実行失敗: {r.stderr.strip()[:200]}")
            return
        for x in json.loads(r.stdout.strip().splitlines()[-1]):
            if x["sw"] > x["W"]:
                add("overflow", x["page"], f"375px幅で横スクロール（scrollWidth {x['sw']}px）: {', '.join(x['wide'])}")
            for e in x["errs"]:
                add("console", x["page"], f"コンソールエラー: {e[:160]}")
    finally:
        srv.shutdown()


def main():
    public = check_pages()
    check_sitemap(public)
    check_feed(public)
    if "--browser" in sys.argv:
        check_browser()
    kinds = {}
    for k, p, m in issues:
        kinds[k] = kinds.get(k, 0) + 1
        print(f"[{k}] {p}: {m}")
    print(f"\n公開ページ {len(public)} / 問題 {len(issues)} 件 " + json.dumps(kinds, ensure_ascii=False))
    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()
