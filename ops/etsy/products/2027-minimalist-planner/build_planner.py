#!/usr/bin/env python3
"""2027 Minimalist Printable Planner generator (DreamyPixelCo).

Generates HTML for A4 and US Letter, renders PDFs with Playwright (page.pdf),
and renders listing preview PNGs. All dates come from Python's calendar module.
Fonts: local Inter + Lora only (both SIL OFL). No external images.

Usage: python3 build_planner.py
"""
import calendar
import datetime as dt
from pathlib import Path

from playwright.sync_api import sync_playwright

YEAR = 2027
HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
OUT = HERE
SRC.mkdir(exist_ok=True)

SIZES = {
    "A4": {"w": "210mm", "h": "297mm"},
    "Letter": {"w": "8.5in", "h": "11in"},
}

CAL = calendar.Calendar(firstweekday=calendar.SUNDAY)  # US-style Sunday start
DOW = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
DOW1 = ["S", "M", "T", "W", "T", "F", "S"]
MONTHS = list(calendar.month_name)[1:]
MON3 = list(calendar.month_abbr)[1:]

CSS = """
:root{
  --ink:#2f2b28; --muted:#8a817a; --line:#d9d2cb; --soft:#f4efe9; --accent:#b9806a;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff;color:var(--ink);font-family:'Inter',sans-serif;
  -webkit-print-color-adjust:exact;print-color-adjust:exact}
@page{size:__W__ __H__;margin:0}
.page{width:__W__;height:__H__;padding:12mm 12mm 10mm;display:flex;flex-direction:column;
  page-break-after:always;break-after:page;overflow:hidden;position:relative}
.page:last-child{page-break-after:auto;break-after:auto}
a{color:inherit;text-decoration:none}
.serif{font-family:'Lora',serif}
.nav{display:flex;gap:1.6mm;justify-content:flex-end;font-size:6.6pt;letter-spacing:.06em;
  color:var(--muted);text-transform:uppercase;margin-bottom:5mm}
.nav a{padding:.6mm 1.4mm;border-radius:1mm}
.nav a.on{background:var(--soft);color:var(--ink);font-weight:600}
.head{display:flex;align-items:baseline;justify-content:space-between;border-bottom:.3mm solid var(--ink);
  padding-bottom:2.5mm;margin-bottom:5mm}
.head h1{font-family:'Lora',serif;font-weight:500;font-size:30pt;letter-spacing:-.01em}
.head .sub{font-size:8pt;letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
.foot{margin-top:auto;padding-top:3mm;font-size:6pt;letter-spacing:.15em;color:var(--muted);
  text-transform:uppercase;display:flex;justify-content:space-between}
/* cover */
.cover{justify-content:center;align-items:center;text-align:center;background:var(--soft)}
.cover .yr{font-family:'Lora',serif;font-size:110pt;font-weight:400;letter-spacing:-.02em;line-height:1}
.cover .t{font-size:11pt;letter-spacing:.5em;text-transform:uppercase;margin-top:8mm}
.cover .rule{width:30mm;height:.3mm;background:var(--accent);margin:10mm auto}
.cover .s{font-size:8pt;letter-spacing:.25em;color:var(--muted);text-transform:uppercase}
.cover .foot{position:absolute;left:12mm;right:12mm;bottom:10mm}
/* index */
.toc{display:grid;grid-template-columns:1fr 1fr;gap:3mm 10mm;font-size:10pt}
.toc a{display:flex;justify-content:space-between;border-bottom:.2mm solid var(--line);padding:2.4mm 0}
.toc a span:last-child{color:var(--muted)}
/* year at a glance */
.yag{display:grid;grid-template-columns:repeat(3,1fr);gap:7mm 8mm;flex:1}
.mini h3{font-family:'Lora',serif;font-weight:500;font-size:12pt;margin-bottom:2mm}
.mini table{width:100%;border-collapse:collapse;font-size:7.4pt;text-align:center}
.mini th{color:var(--muted);font-weight:500;padding-bottom:1mm;font-size:6.6pt}
.mini td{padding:.9mm 0}
.mini td.o{color:transparent}
.mini td.we{color:var(--accent)}
/* month */
.mgrid{flex:1;display:grid;grid-template-columns:repeat(7,1fr);grid-template-rows:auto;
  border-top:.2mm solid var(--line);border-left:.2mm solid var(--line)}
.mgrid .dh{font-size:7pt;letter-spacing:.15em;text-transform:uppercase;color:var(--muted);
  padding:2mm 2mm;border-right:.2mm solid var(--line);border-bottom:.2mm solid var(--line);background:var(--soft)}
.mgrid .c{border-right:.2mm solid var(--line);border-bottom:.2mm solid var(--line);padding:1.6mm 2mm;font-size:9pt}
.mgrid .c.o{background:#fbf9f7;color:#c9c1b9}
.mgrid .c.o span{visibility:hidden}
.mside{display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-top:5mm;height:34mm}
.box h4,.wk h4,.hab h4{font-size:7pt;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);
  font-weight:600;margin-bottom:2mm}
.lines{background-image:linear-gradient(to bottom,transparent calc(100% - .2mm),var(--line) calc(100% - .2mm));
  background-size:100% 6.5mm;height:calc(100% - 5mm)}
/* weekly */
.wk{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(4,1fr);gap:4mm 6mm}
.wk .d{border-top:.3mm solid var(--ink);padding-top:1.6mm;display:flex;flex-direction:column}
.wk .d .dn{display:flex;align-items:baseline;gap:2mm;margin-bottom:1mm}
.wk .d .dn b{font-family:'Lora',serif;font-weight:500;font-size:15pt}
.wk .d .dn i{font-style:normal;font-size:7pt;letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
.wk .d .dn em{font-style:normal;font-size:6.5pt;color:var(--accent);margin-left:auto;letter-spacing:.1em;text-transform:uppercase}
.wk .d.out{opacity:.45}
.wk .d .lines{flex:1;height:auto}
.wk .n{background:var(--soft);padding:2.5mm 3mm;display:flex;flex-direction:column}
.wk .n .chk{font-size:8.5pt;line-height:2.15}
.wk .n .chk div::before{content:"";display:inline-block;width:2.6mm;height:2.6mm;border:.25mm solid var(--muted);
  border-radius:.5mm;margin-right:2mm;vertical-align:-.3mm}
/* habit */
.hab{flex:1;display:flex;flex-direction:column}
.hab table{width:100%;border-collapse:collapse;table-layout:fixed}
.hab th{font-size:6pt;font-weight:500;color:var(--muted);padding:1mm 0;text-align:center}
.hab th.hn{text-align:left;width:32mm;font-size:7pt;letter-spacing:.15em;text-transform:uppercase}
.hab th.we{color:var(--accent)}
.hab td{border:.2mm solid var(--line);height:12.5mm}
.hab td.hn{border-left:none;border-right:.3mm solid var(--ink)}
/* goals */
.goals{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr 1fr;gap:6mm}
.goals .box{border-top:.3mm solid var(--ink);padding-top:2mm;display:flex;flex-direction:column}
.goals .box .lines{flex:1;height:auto}
.dots{flex:1;background-image:radial-gradient(circle,#c9c1b9 .28mm,transparent .32mm);background-size:5mm 5mm;
  background-position:center}
"""


def nav(active):
    links = ['<a href="#index"{}>Index</a>'.format(' class="on"' if active == "index" else ""),
             '<a href="#year"{}>Year</a>'.format(' class="on"' if active == "year" else "")]
    for i, m in enumerate(MON3, 1):
        on = ' class="on"' if active == i else ""
        links.append(f'<a href="#m{i}"{on}>{m}</a>')
    return '<nav class="nav">' + "".join(links) + "</nav>"


def foot(label):
    return f'<div class="foot"><span>DreamyPixelCo · {YEAR} Planner</span><span>{label}</span></div>'


def mini_month(m):
    rows = []
    for wk in CAL.monthdatescalendar(YEAR, m):
        cells = []
        for d in wk:
            cls = []
            if d.month != m:
                cls.append("o")
            elif d.weekday() in (5, 6):
                cls.append("we")
            cells.append(f'<td class="{" ".join(cls)}">{d.day}</td>')
        rows.append("<tr>" + "".join(cells) + "</tr>")
    while len(rows) < 6:
        rows.append("<tr>" + "<td>&nbsp;</td>" * 7 + "</tr>")
    head = "".join(f"<th>{x}</th>" for x in DOW1)
    return (f'<div class="mini"><h3><a href="#m{m}">{MONTHS[m-1]}</a></h3>'
            f"<table><tr>{head}</tr>{''.join(rows)}</table></div>")


def week_starts():
    """Sundays starting each week that contains any day of YEAR."""
    d = dt.date(YEAR, 1, 1)
    d -= dt.timedelta(days=(d.weekday() + 1) % 7)  # back to Sunday
    out = []
    while d.year <= YEAR:
        out.append(d)
        d += dt.timedelta(days=7)
    return out


def build_html(size):
    W, H = SIZES[size]["w"], SIZES[size]["h"]
    weeks = week_starts()
    pages = []

    # Cover
    pages.append(f'''<section class="page cover" id="cover">
      <div class="t">Planner</div><div class="yr">{YEAR}</div>
      <div class="rule"></div><div class="s">Minimalist · Printable · {size}</div>
      <div class="foot"><span>DreamyPixelCo</span><span>Personal use only</span></div></section>''')

    # Index
    toc = [("Year at a Glance", "#year"), ("Goals & Intentions", "#goals")]
    toc += [(f"{MONTHS[m-1]} — Month + Habits", f"#m{m}") for m in range(1, 13)]
    toc += [("Weekly Pages (Week 1)", "#w1"), ("Notes", "#notes")]
    toc_html = "".join(f'<a href="{h}"><span>{t}</span><span>→</span></a>' for t, h in toc)
    pages.append(f'''<section class="page" id="index">{nav("index")}
      <div class="head"><h1>Index</h1><span class="sub">{YEAR}</span></div>
      <div class="toc">{toc_html}</div>
      <div style="margin-top:10mm;font-size:8pt;color:var(--muted);line-height:1.7">
      Tip: tap the tabs at the top of each page to jump between sections in GoodNotes, Notability or any PDF reader.
      Weeks start on Sunday.</div>{foot("Index")}</section>''')

    # Year at a glance
    pages.append(f'''<section class="page" id="year">{nav("year")}
      <div class="head"><h1>Year at a Glance</h1><span class="sub">{YEAR}</span></div>
      <div class="yag">{"".join(mini_month(m) for m in range(1, 13))}</div>{foot("Year")}</section>''')

    # Goals
    boxes = ["Health", "Work & Money", "Relationships", "Learning", "Home", "Just for Me"]
    gb = "".join(f'<div class="box"><h4>{b}</h4><div class="lines"></div></div>' for b in boxes)
    pages.append(f'''<section class="page" id="goals">{nav("goals")}
      <div class="head"><h1>Goals &amp; Intentions</h1><span class="sub">{YEAR}</span></div>
      <div class="goals">{gb}</div>{foot("Goals")}</section>''')

    for m in range(1, 13):
        # Monthly
        cells = "".join(f'<div class="dh">{d}</div>' for d in DOW)
        mweeks = CAL.monthdatescalendar(YEAR, m)
        for wk in mweeks:
            for d in wk:
                if d.month == m:
                    cells += f'<div class="c"><span>{d.day}</span></div>'
                else:
                    cells += f'<div class="c o"><span>{d.day}</span></div>'
        rows = len(mweeks)
        pages.append(f'''<section class="page" id="m{m}">{nav(m)}
          <div class="head"><h1>{MONTHS[m-1]}</h1><span class="sub">{YEAR} · {m:02d}</span></div>
          <div class="mgrid" style="grid-template-rows:auto repeat({rows},1fr)">{cells}</div>
          <div class="mside"><div class="box"><h4>Focus</h4><div class="lines"></div></div>
          <div class="box"><h4>Notes</h4><div class="lines"></div></div></div>{foot(MONTHS[m-1])}</section>''')

        # Habit tracker
        ndays = calendar.monthrange(YEAR, m)[1]
        th = '<th class="hn">Habit</th>'
        for day in range(1, ndays + 1):
            wd = dt.date(YEAR, m, day).weekday()
            cls = ' class="we"' if wd in (5, 6) else ""
            th += f"<th{cls}>{day}<br>{DOW1[(wd + 1) % 7]}</th>"
        trs = "".join('<tr><td class="hn"></td>' + "<td></td>" * ndays + "</tr>" for _ in range(16))
        pages.append(f'''<section class="page" id="h{m}">{nav(m)}
          <div class="head"><h1>Habit Tracker</h1><span class="sub">{MONTHS[m-1]} {YEAR}</span></div>
          <div class="hab"><table><tr>{th}</tr>{trs}</table></div>{foot(MONTHS[m-1] + " Habits")}</section>''')

    # Weekly pages
    for i, s in enumerate(weeks, 1):
        days = [s + dt.timedelta(days=k) for k in range(7)]
        e = days[-1]
        rng = f"{MON3[s.month-1]} {s.day}" + (f", {s.year}" if s.year != YEAR else "")
        rng += f" – {MON3[e.month-1]} {e.day}" + (f", {e.year}" if e.year != YEAR else "")
        act = days[3].month if days[3].year == YEAR else (1 if s.year < YEAR else 12)
        blocks = ""
        for d in days:
            out = " out" if d.year != YEAR else ""
            mtag = f"<em>{MON3[d.month-1]}</em>" if d.day == 1 or d == days[0] else ""
            blocks += (f'<div class="d{out}"><div class="dn"><b>{d.day}</b><i>{DOW[(d.weekday()+1)%7]}</i>{mtag}</div>'
                       f'<div class="lines"></div></div>')
        blocks += ('<div class="n"><h4>Top 3 this week</h4><div class="chk"><div></div><div></div><div></div></div>'
                   '<h4 style="margin-top:2mm">Notes</h4><div class="lines" style="flex:1;height:auto"></div></div>')
        pages.append(f'''<section class="page" id="w{i}">{nav(act)}
          <div class="head"><h1>Week {i:02d}</h1><span class="sub">{rng}</span></div>
          <div class="wk">{blocks}</div>{foot(f"Week {i}")}</section>''')

    # Notes
    pages.append(f'''<section class="page" id="notes">{nav("notes")}
      <div class="head"><h1>Notes</h1><span class="sub">Lined</span></div>
      <div class="lines" style="flex:1;height:auto;background-size:100% 8mm"></div>{foot("Notes")}</section>''')
    pages.append(f'''<section class="page">{nav("notes")}
      <div class="head"><h1>Notes</h1><span class="sub">Dot grid</span></div>
      <div class="dots"></div>{foot("Notes")}</section>''')

    css = CSS.replace("__W__", W).replace("__H__", H)
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<title>{YEAR} Minimalist Planner ({size})</title><style>{css}</style></head>'
            f'<body>{"".join(pages)}</body></html>'), len(pages)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for size in SIZES:
            html, n = build_html(size)
            src = SRC / f"planner_{size}.html"
            src.write_text(html, encoding="utf-8")
            page.goto(src.as_uri())
            page.wait_for_timeout(300)
            pdf = OUT / f"2027-Minimalist-Planner-{size}.pdf"
            page.pdf(path=str(pdf), width=SIZES[size]["w"], height=SIZES[size]["h"],
                     print_background=True, prefer_css_page_size=True)
            print(f"{pdf.name}: {n} pages, {pdf.stat().st_size/1024:.0f} KB")
        browser.close()


if __name__ == "__main__":
    main()
