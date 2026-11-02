#!/usr/bin/env python3
"""Listing preview images (2000x1600, landscape per Etsy image guidance).

Uses real page renders of the Letter PDF (pdftoppm) — no stock photos, no AI images.
Run after build_planner.py.
"""
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "src" / "preview_assets"
ASSETS.mkdir(parents=True, exist_ok=True)
PDF = HERE / "2027-Minimalist-Planner-Letter.pdf"
PAGES = {"cover": 1, "index": 2, "year": 3, "goals": 4, "month": 5, "habit": 6, "week": 30, "notes": 83}

for name, n in PAGES.items():
    subprocess.run(["pdftoppm", "-f", str(n), "-l", str(n), "-r", "110", "-png", "-singlefile",
                    str(PDF), str(ASSETS / name)], check=True)

BASE = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:2000px;height:1600px;overflow:hidden;font-family:'Inter',sans-serif;color:#2f2b28;
  background:#ece4db;position:relative}
.serif{font-family:'Lora',serif}
.pg{position:absolute;background:#fff;box-shadow:0 30px 60px rgba(60,40,30,.18),0 4px 12px rgba(60,40,30,.10)}
.pg img{display:block;width:100%}
.badge{display:inline-block;border:2px solid #2f2b28;border-radius:999px;padding:14px 30px;font-size:30px;
  letter-spacing:.12em;text-transform:uppercase;margin:0 14px 18px 0}
"""

P1 = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE}
.l{{position:absolute;left:120px;top:190px;width:760px}}
.l .k{{font-size:34px;letter-spacing:.35em;text-transform:uppercase;color:#9a6c58}}
.l h1{{font-family:'Lora',serif;font-weight:500;font-size:150px;line-height:1;margin:30px 0 10px}}
.l h2{{font-family:'Lora',serif;font-weight:400;font-size:64px;line-height:1.15;margin-bottom:50px}}
.l p{{font-size:34px;line-height:1.6;color:#6d645d;margin-top:30px}}
</style></head><body>
<div class="l"><div class="k">Digital Download</div><h1>2027</h1>
<h2>Minimalist<br>Planner</h2>
<span class="badge">A4</span><span class="badge">US Letter</span><span class="badge">83 pages</span>
<p>Year · Monthly · Weekly · Habit Tracker<br>Hyperlinked tabs for tablets</p></div>
<div class="pg" style="left:1010px;top:250px;width:760px;transform:rotate(-5deg)"><img src="preview_assets/week.png"></div>
<div class="pg" style="left:1120px;top:170px;width:760px;transform:rotate(3deg)"><img src="preview_assets/month.png"></div>
</body></html>"""

items = [("year", "Year at a Glance"), ("month", "12 Monthly Pages"), ("week", "53 Dated Weekly Pages"),
         ("habit", "12 Habit Trackers"), ("goals", "Goals & Intentions"), ("notes", "Notes · Dot Grid")]
cards = "".join(
    f'<div class="c"><div class="im"><img src="preview_assets/{k}.png"></div><div class="t">{t}</div></div>'
    for k, t in items)
P2 = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE}
body{{background:#f6f1eb}}
body{{display:flex;flex-direction:column;align-items:center;padding-top:50px}}
h1{{font-family:'Lora',serif;font-weight:500;font-size:84px;text-align:center}}
.sub{{text-align:center;font-size:30px;letter-spacing:.3em;text-transform:uppercase;color:#9a6c58;margin-top:20px}}
.g{{display:grid;grid-template-columns:repeat(3,330px);gap:36px 110px;margin-top:50px}}
.c .im{{background:#fff;box-shadow:0 18px 40px rgba(60,40,30,.15)}}
.c img{{display:block;width:100%}}
.c .t{{font-size:27px;text-align:center;margin-top:24px;line-height:1.3}}
.f{{position:absolute;left:0;right:0;bottom:40px;text-align:center}}
</style></head><body>
<h1>What's Inside</h1><div class="sub">2027 · Sunday start · Jan – Dec</div>
<div class="g">{cards}</div>
<div class="f"><span class="badge">Instant PDF download</span><span class="badge">Print at home</span>
<span class="badge">Tablet friendly</span></div>
</body></html>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 2000, "height": 1600})
    for i, html in enumerate([P1, P2], 1):
        f = HERE / "src" / f"preview_{i}.html"
        f.write_text(html, encoding="utf-8")
        pg.goto(f.as_uri())
        pg.wait_for_timeout(300)
        out = HERE / f"preview_{i}.png"
        pg.screenshot(path=str(out))
        print(out.name)
    b.close()
