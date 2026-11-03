#!/usr/bin/env python3
"""スマホ・PC表示チェック（docs/ の全公開ページ、ローカルファイルのみ・外部通信なし）。
実行：python3 ops/tests/mobile_check.py          # 問題0件なら終了コード0、あれば1
      python3 ops/tests/mobile_check.py --json   # 結果をJSONで出す

チェック項目（iPhone 13 と PC 1280px の両方）
① ページの横スクロール（本文が画面からはみ出す）
② 表の列が隠れる（表の中身が表の枠より広い／表が画面の右にはみ出す）
③ ボタン・入力欄・購入ボタンが画面の外にはみ出す
④ ダークモード（color_scheme=dark）で、白っぽい背景の枠の中の文字が読みにくい
   （文字色と実際の背景色の明暗差がWCAG基準 4.5:1（大きい文字は3:1）未満）
外部URL（Google Fonts・アフィリエイト画像など）への通信は遮断して調べる。
"""
import glob, json, os, sys, time
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DOCS = os.path.join(ROOT, "docs")

LAYOUT_JS = r"""() => {
const vw = document.documentElement.clientWidth;
const r = {sw: document.documentElement.scrollWidth, vw, tables: [], out: []};
r.hscroll = r.sw > vw + 1;
document.querySelectorAll('table').forEach((t, i) => {
  const rect = t.getBoundingClientRect();
  const hidden = Math.max(t.scrollWidth - t.clientWidth, 0);
  if (hidden > 2 || rect.right > vw + 1)
    r.tables.push({i, hidden, right: Math.round(rect.right), head: ((t.querySelector('th,td') || {}).innerText || '').slice(0, 20)});
});
document.querySelectorAll('button,input,select,textarea,a.buy,.buy').forEach(e => {
  const b = e.getBoundingClientRect();
  if (b.width === 0 || e.type === 'hidden') return;
  if (b.right > vw + 1 || b.left < -1)
    r.out.push({tag: e.tagName, txt: (e.innerText || e.value || e.placeholder || '').slice(0, 20), right: Math.round(b.right)});
});
return r;}"""

# ④：直下に文字を持つ見えている要素ごとに、実際の背景色（親をたどって合成）と文字色の明暗差を計算。
# 対象は「白っぽい背景（相対輝度0.5以上）の上の文字」＝ダークモードで白い枠の中にある文字。
CONTRAST_JS = r"""() => {
const parse = s => { const m = s.match(/rgba?\(([^)]+)\)/); if (!m) return [0,0,0,0];
  const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1]; };
const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
const over = (top, bot) => { const a = top[3]; return [0,1,2].map(i => top[i] * a + bot[i] * (1 - a)).concat([1]); };
const bgOf = el => { const layers = [];
  for (let e = el; e; e = e.parentElement) { const c = parse(getComputedStyle(e).backgroundColor); if (c[3] > 0) { layers.push(c); if (c[3] >= 1) break; } }
  let col = parse(getComputedStyle(document.body).backgroundColor); if (col[3] < 1) col = [255,255,255,1];
  if (layers.length && layers[layers.length - 1][3] >= 1) col = layers.pop();
  while (layers.length) col = over(layers.pop(), col); return col; };
const bad = [];
document.querySelectorAll('body *').forEach(el => {
  if (['SCRIPT','STYLE','NOSCRIPT','SVG','svg'].includes(el.tagName)) return;
  const txt = Array.from(el.childNodes).filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim();
  if (!txt) return;
  const cs = getComputedStyle(el);
  if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) === 0) return;
  const rect = el.getBoundingClientRect(); if (rect.width === 0 || rect.height === 0) return;
  const bg = bgOf(el); const lb = lum(bg); if (lb < 0.5) return;
  const fg = over(parse(cs.color), bg); const lf = lum(fg);
  const ratio = (Math.max(lb, lf) + 0.05) / (Math.min(lb, lf) + 0.05);
  const size = parseFloat(cs.fontSize), weight = parseInt(cs.fontWeight) || 400;
  const need = (size >= 24 || (size >= 18.66 && weight >= 700)) ? 3 : 4.5;
  if (ratio < need) bad.push({tag: el.tagName, txt: txt.slice(0, 20), ratio: Math.round(ratio * 100) / 100, color: cs.color, bg: 'rgb(' + bg.slice(0,3).map(Math.round).join(',') + ')'});
});
return bad;}"""


def pages():
    ps = [os.path.join(DOCS, "index.html"), os.path.join(DOCS, "about.html")]
    ps += sorted(glob.glob(os.path.join(DOCS, "posts", "*.html")))
    ps += sorted(glob.glob(os.path.join(DOCS, "apps", "**", "*.html"), recursive=True))
    return [p for p in ps if os.path.exists(p)]


def block_external(route):
    if route.request.url.startswith("file://"):
        route.continue_()
    else:
        route.abort()


def run():
    t0 = time.time()
    files = pages()
    problems = []  # (画面, ページ, 種類, 詳細)
    with sync_playwright() as p:
        br = p.chromium.launch()
        setups = [
            ("iPhone13", dict(**p.devices["iPhone 13"], color_scheme="light")),
            ("PC1280", dict(viewport={"width": 1280, "height": 900}, color_scheme="light")),
            ("iPhone13-dark", dict(**p.devices["iPhone 13"], color_scheme="dark")),
            ("PC1280-dark", dict(viewport={"width": 1280, "height": 900}, color_scheme="dark")),
        ]
        for label, opts in setups:
            ctx = br.new_context(**opts)
            ctx.route("**/*", block_external)
            pg = ctx.new_page()
            dark = label.endswith("dark")
            for f in files:
                name = os.path.relpath(f, DOCS)
                pg.goto("file://" + f, wait_until="load", timeout=20000)
                pg.wait_for_timeout(100)
                if dark:
                    for b in pg.evaluate(CONTRAST_JS):
                        problems.append((label, name, "④ダーク文字", b))
                else:
                    d = pg.evaluate(LAYOUT_JS)
                    if d["hscroll"]:
                        problems.append((label, name, "①横スクロール", {"scrollWidth": d["sw"], "画面幅": d["vw"]}))
                    for t in d["tables"]:
                        problems.append((label, name, "②表の列が隠れる", t))
                    for o in d["out"]:
                        problems.append((label, name, "③はみ出し", o))
            ctx.close()
        br.close()
    return files, problems, time.time() - t0


def main():
    files, problems, sec = run()
    if "--json" in sys.argv:
        print(json.dumps([dict(screen=a, page=b, kind=c, detail=d) for a, b, c, d in problems], ensure_ascii=False, indent=1))
    else:
        for a, b, c, d in problems:
            print(f"[{a}] {b} {c}: {json.dumps(d, ensure_ascii=False)}")
        kinds = {}
        for _, _, c, _ in problems:
            kinds[c] = kinds.get(c, 0) + 1
        summary = "、".join(f"{k} {v}件" for k, v in sorted(kinds.items())) or "なし"
        print(f"ページ {len(files)}／画面 4種／問題 {len(problems)}件（{summary}）／{sec:.1f}秒")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
