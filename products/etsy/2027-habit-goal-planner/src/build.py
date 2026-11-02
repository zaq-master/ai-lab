"""Build the 2027 Habit & Goal Planner printable (US Letter + A4) and the Etsy thumbnail.

Usage: python3 build.py   (outputs to ../)
Fonts: Inter (SIL OFL 1.1), Caladea (SIL OFL 1.1) from system font packages.
All artwork is drawn with HTML/CSS/SVG in this file (no third-party images).
"""
import calendar
import pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent
YEAR = 2027
BRAND = "DreamyPixelCo"
TITLE = "2027 Habit &amp; Goal Planner"

INTER = "/usr/share/fonts/opentype/inter"
CAL = "/usr/share/fonts/truetype/crosextra"

FONTS = f"""
@font-face{{font-family:'Inter';font-weight:400;src:url('file://{INTER}/Inter-Regular.otf');}}
@font-face{{font-family:'Inter';font-weight:500;src:url('file://{INTER}/Inter-Medium.otf');}}
@font-face{{font-family:'Inter';font-weight:600;src:url('file://{INTER}/Inter-SemiBold.otf');}}
@font-face{{font-family:'Inter';font-weight:300;src:url('file://{INTER}/Inter-Light.otf');}}
@font-face{{font-family:'Caladea';font-weight:400;src:url('file://{CAL}/Caladea-Regular.ttf');}}
@font-face{{font-family:'Caladea';font-style:italic;src:url('file://{CAL}/Caladea-Italic.ttf');}}
@font-face{{font-family:'Caladea';font-weight:700;src:url('file://{CAL}/Caladea-Bold.ttf');}}
"""

# Soft, printer-friendly palette (light tints, dark-grey ink)
CSS = """
:root{--ink:#3d3a4b;--soft:#8a86a0;--line:#cfcbe0;--lav:#e9e3f5;--lav2:#b9a7d6;--blush:#f7e3e5;--sage:#e3ece0;--sage2:#9bb596;}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff;color:var(--ink);font-family:'Inter',sans-serif;font-size:9.5pt;}
.page{width:var(--pw);height:var(--ph);padding:0.5in 0.5in 0.42in;display:flex;flex-direction:column;page-break-after:always;overflow:hidden;position:relative}
.page:last-child{page-break-after:auto}
.hdr{display:flex;align-items:flex-end;justify-content:space-between;border-bottom:1.2pt solid var(--ink);padding-bottom:6pt;margin-bottom:12pt}
.hdr h1{font-family:'Caladea',serif;font-weight:700;font-size:25pt;letter-spacing:.3pt;line-height:1}
.hdr .k{font-size:8pt;letter-spacing:2.2pt;text-transform:uppercase;color:var(--soft);font-weight:500}
.ftr{margin-top:auto;padding-top:8pt;display:flex;justify-content:space-between;font-size:6.8pt;color:var(--soft);letter-spacing:1.2pt;text-transform:uppercase}
.body{flex:1;display:flex;flex-direction:column;min-height:0}
.lbl{font-size:7.5pt;letter-spacing:1.8pt;text-transform:uppercase;font-weight:600;color:var(--ink)}
.sub{font-size:7.5pt;color:var(--soft)}
.box{border:0.8pt solid var(--line);border-radius:7pt;padding:8pt 10pt}
.lines{flex:1;background-image:repeating-linear-gradient(to bottom,transparent 0,transparent 21.5pt,var(--line) 21.5pt,var(--line) 22.3pt)}
.tag{display:inline-block;background:var(--lav);border-radius:20pt;padding:2pt 9pt;font-size:7.3pt;letter-spacing:1.5pt;text-transform:uppercase;font-weight:600}
table{border-collapse:collapse;width:100%}
.grid td,.grid th{border:0.6pt solid var(--line);text-align:center}
.row{display:flex;gap:10pt}
.col{display:flex;flex-direction:column;gap:10pt}
.f1{flex:1;min-height:0}
.cb{display:inline-block;width:8pt;height:8pt;border:0.8pt solid var(--soft);border-radius:2pt;vertical-align:-1pt;margin-right:5pt}
/* cover */
.cover{padding:0.6in;justify-content:center;align-items:center;text-align:center;background:#fff}
.cover .frame{position:absolute;inset:0.42in;border:1pt solid var(--line);border-radius:14pt}
.cover .yr{font-family:'Caladea',serif;font-weight:700;font-size:118pt;line-height:.9;letter-spacing:-2pt}
.cover .t1{font-family:'Caladea',serif;font-style:italic;font-size:30pt;margin-top:8pt}
.cover .t2{font-size:9pt;letter-spacing:4pt;text-transform:uppercase;color:var(--soft);margin-top:14pt}
.cover .contents{margin-top:34pt;display:grid;grid-template-columns:1fr 1fr;gap:5pt 28pt;text-align:left;font-size:9pt}
.cover .contents span{color:var(--soft);margin-right:6pt;font-variant-numeric:tabular-nums}
.cover .nm{margin-top:40pt;width:3.6in;border-bottom:0.8pt solid var(--ink);text-align:left;font-size:7.5pt;letter-spacing:2pt;color:var(--soft);padding-bottom:16pt;text-transform:uppercase}
/* mini calendars */
.cal{display:grid;grid-template-columns:repeat(3,1fr);gap:12pt 14pt;flex:1}
.mc .mn{font-family:'Caladea',serif;font-weight:700;font-size:14pt;margin-bottom:3pt;border-bottom:0.6pt solid var(--line);padding-bottom:2pt}
.mc table td,.mc table th{font-size:8.4pt;text-align:center;height:19pt;width:14.28%}
.mc th{color:var(--soft);font-weight:600;font-size:6.4pt}
.mc td.we{color:var(--lav2)}
/* wheel */
.wheel{display:flex;justify-content:center}
/* pixels */
.px td{height:var(--pxh);font-size:6.2pt}
.px th{font-size:6.6pt;font-weight:600;height:14pt;background:var(--lav)}
.px td.dn{color:var(--soft);width:16pt;border:none}
.px td.na{background:repeating-linear-gradient(45deg,#f1eff6 0,#f1eff6 2pt,#fff 2pt,#fff 4pt)}
.legend{display:flex;gap:10pt;align-items:center;font-size:7.5pt}
.legend i{display:inline-block;width:12pt;height:12pt;border:0.8pt solid var(--line);border-radius:2pt;margin-right:4pt;vertical-align:-3pt}
"""

DOW = ["S", "M", "T", "W", "T", "F", "S"]


def page(title, kicker, inner, label):
    return f"""<section class="page"><div class="hdr"><h1>{title}</h1><div class="k">{kicker}</div></div>
<div class="body">{inner}</div>
<div class="ftr"><span>{BRAND} · {TITLE}</span><span>{label}</span></div></section>"""


def cover():
    items = ["Year at a Glance", "Vision &amp; Word of the Year", "Life Balance Wheel", "Top 3 Goals",
             "Goal Action Plan", "Quarterly Goals", "Monthly Habit Tracker", "Weekly Habit Tracker",
             "Year in Pixels", "30-Day Challenge", "Monthly Reflection", "Year-End Review"]
    li = "".join(f"<div><span>{i+2:02d}</span>{t}</div>" for i, t in enumerate(items))
    leaf = """<svg width="120" height="34" viewBox="0 0 120 34"><path d="M4 17 H50" stroke="#b9a7d6" stroke-width="1"/>
<path d="M70 17 H116" stroke="#b9a7d6" stroke-width="1"/><circle cx="60" cy="17" r="6" fill="#f7e3e5" stroke="#b9a7d6"/>
<circle cx="60" cy="17" r="2" fill="#b9a7d6"/></svg>"""
    return f"""<section class="page cover"><div class="frame"></div>
<div class="t2">Printable Planner</div>{leaf}
<div class="yr">{YEAR}</div><div class="t1">Habit &amp; Goal Planner</div>
<div class="t2">Plan it · Track it · Reflect on it</div>
<div class="contents">{li}</div>
<div class="nm">This planner belongs to</div></section>"""


def year_glance():
    cal = calendar.Calendar(firstweekday=6)  # Sunday start (US)
    blocks = []
    for m in range(1, 13):
        rows = ""
        weeks = cal.monthdayscalendar(YEAR, m)
        while len(weeks) < 6:
            weeks.append([0] * 7)
        for w in weeks:
            rows += "<tr>" + "".join(
                f"<td class='{'we' if i in (0, 6) else ''}'>{d if d else ''}</td>" for i, d in enumerate(w)) + "</tr>"
        head = "<tr>" + "".join(f"<th>{d}</th>" for d in DOW) + "</tr>"
        blocks.append(f"<div class='mc'><div class='mn'>{calendar.month_name[m]}</div><table>{head}{rows}</table></div>")
    inner = f"<div class='cal'>{''.join(blocks)}</div>"
    return page(f"{YEAR} at a Glance", "Year overview", inner, "02")


def vision():
    inner = """
<div class="box" style="text-align:center;padding:14pt"><div class="lbl">My word of the year</div>
<div style="height:40pt;border-bottom:0.8pt solid var(--line);margin:4pt 1.2in 0"></div>
<div class="sub" style="margin-top:6pt">One word to come back to when things get busy</div></div>
<div style="height:10pt"></div>
<div class="row f1">
 <div class="box f1 col" style="gap:4pt"><div class="lbl">By the end of 2027 I want to feel…</div><div class="lines"></div></div>
 <div class="box f1 col" style="gap:4pt"><div class="lbl">Things I'm leaving in 2026</div><div class="lines"></div></div>
</div>
<div style="height:10pt"></div>
<div class="box f1 col" style="gap:4pt;background:linear-gradient(var(--lav),var(--lav)) top/100% 0 no-repeat"><div class="lbl">Vision board — words, sketches, quotes</div>
<div class="f1" style="border:0.8pt dashed var(--line);border-radius:6pt;margin-top:4pt"></div></div>"""
    return page("Vision &amp; Word of the Year", "Set the tone", inner, "03")


def wheel():
    import math
    areas = ["Health", "Career", "Money", "Relationships", "Fun", "Growth", "Home", "Mind"]
    n, cx, cy, R = len(areas), 210, 210, 160
    svg = [f'<svg viewBox="0 0 420 420" style="width:4.3in;height:4.3in">']
    for i in range(n):
        a0 = -math.pi / 2 + i * 2 * math.pi / n
        a1 = a0 + 2 * math.pi / n
        x0, y0 = cx + R * math.cos(a0), cy + R * math.sin(a0)
        x1, y1 = cx + R * math.cos(a1), cy + R * math.sin(a1)
        fill = ["#f4f1fa", "#fbf1f2", "#f2f6f0", "#fff"][i % 4]
        svg.append(f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{R},{R} 0 0,1 {x1:.1f},{y1:.1f} Z" fill="{fill}" stroke="#cfcbe0" stroke-width="0.8"/>')
    for k in range(1, 11):
        dash = 'stroke-dasharray="2 2"' if k < 10 else ""
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="{R*k/10:.1f}" fill="none" stroke="#cfcbe0" stroke-width="{0.9 if k==10 else 0.45}" {dash}/>')
    for i, a in enumerate(areas):
        am = -math.pi / 2 + (i + .5) * 2 * math.pi / n
        x, y = cx + (R + 24) * math.cos(am), cy + (R + 24) * math.sin(am)
        svg.append(f'<text x="{x:.1f}" y="{y+3:.1f}" text-anchor="middle" font-family="Inter" font-size="10.5" font-weight="600" fill="#3d3a4b">{a}</text>')
    svg.append("</svg>")
    rows = "".join(f"<tr><td style='text-align:left;padding:5pt 6pt;width:28%;font-weight:600'>{a}</td><td style='width:12%'>&nbsp;/10</td><td style='width:12%'>&nbsp;/10</td><td></td></tr>" for a in areas)
    inner = f"""<div class="sub" style="margin-bottom:6pt">Shade each slice from the centre (1) to the edge (10) to show how satisfied you feel today. Repeat in December.</div>
<div class="wheel">{''.join(svg)}</div>
<table class="grid" style="margin-top:10pt;font-size:8pt"><tr style="background:var(--lav)"><th style="padding:4pt">Area</th><th>Jan</th><th>Dec</th><th>One small change</th></tr>{rows}</table>
<div class="box f1 col" style="margin-top:10pt"><div class="lbl">Notes &amp; insights</div><div class="lines"></div></div>"""
    return page("Life Balance Wheel", "Where am I now?", inner, "04")


def top_goals():
    def g(n):
        return f"""<div class="box f1 col" style="gap:5pt"><div style="display:flex;align-items:center;gap:8pt">
<div style="width:22pt;height:22pt;border-radius:50%;background:var(--lav);display:flex;align-items:center;justify-content:center;font-family:Caladea;font-weight:700;font-size:12pt">{n}</div>
<div class="f1" style="border-bottom:0.8pt solid var(--ink);height:18pt"></div><div class="sub">Due&nbsp;____/____</div></div>
<div class="row f1"><div class="f1 col" style="gap:2pt"><div class="lbl">Why it matters</div><div class="lines"></div></div>
<div class="f1 col" style="gap:2pt"><div class="lbl">First 3 steps</div>
<div style="padding-top:5pt;line-height:22.3pt"><span class="cb"></span>____________________<br><span class="cb"></span>____________________<br><span class="cb"></span>____________________</div></div></div></div>"""
    inner = f"<div class='col f1'>{g(1)}{g(2)}{g(3)}</div>"
    return page(f"My Top 3 Goals", "Focus for 2027", inner, "05")


def action_plan():
    ms = "".join(f"<tr><td style='height:24pt;width:6%;color:var(--soft)'>{i}</td><td></td><td style='width:16%'></td><td style='width:9%'><span class='cb' style='margin:0'></span></td></tr>" for i in range(1, 11))
    inner = f"""<div class="row"><div class="box f1"><div class="lbl">Goal</div><div style="height:22pt;border-bottom:0.8pt solid var(--line)"></div></div>
<div class="box" style="width:1.8in"><div class="lbl">Target date</div><div style="height:22pt;border-bottom:0.8pt solid var(--line)"></div></div></div>
<div style="height:10pt"></div>
<div class="row"><div class="box f1"><div class="lbl">How I'll measure it</div><div style="height:38pt" class="lines"></div></div>
<div class="box f1"><div class="lbl">Possible obstacles &amp; my plan</div><div style="height:38pt" class="lines"></div></div></div>
<div style="height:10pt"></div>
<div class="lbl" style="margin-bottom:4pt">Milestones</div>
<table class="grid" style="font-size:8pt"><tr style="background:var(--lav)"><th style="padding:4pt">#</th><th>Milestone / action</th><th>By when</th><th>Done</th></tr>{ms}</table>
<div style="height:10pt"></div>
<div class="row f1"><div class="box f1 col"><div class="lbl">Reward when I finish</div><div class="lines"></div></div>
<div class="box f1 col"><div class="lbl">Who can support me</div><div class="lines"></div></div></div>"""
    return page("Goal Action Plan", "Break it down", inner, "06")


def quarterly():
    q = [("Q1", "Jan · Feb · Mar"), ("Q2", "Apr · May · Jun"), ("Q3", "Jul · Aug · Sep"), ("Q4", "Oct · Nov · Dec")]
    cells = "".join(f"""<div class="box col" style="gap:4pt"><div style="display:flex;justify-content:space-between;align-items:center">
<span class="tag">{a}</span><span class="sub">{b}</span></div><div class="lbl" style="margin-top:2pt">Focus</div>
<div style="height:18pt;border-bottom:0.8pt solid var(--line)"></div><div class="lbl" style="margin-top:4pt">Goals</div>
<div><div style="display:flex;align-items:flex-end;height:21pt"><span class="cb"></span><div class="f1" style="border-bottom:0.8pt solid var(--line);height:14pt"></div></div><div style="display:flex;align-items:flex-end;height:21pt"><span class="cb"></span><div class="f1" style="border-bottom:0.8pt solid var(--line);height:14pt"></div></div><div style="display:flex;align-items:flex-end;height:21pt"><span class="cb"></span><div class="f1" style="border-bottom:0.8pt solid var(--line);height:14pt"></div></div><div style="display:flex;align-items:flex-end;height:21pt"><span class="cb"></span><div class="f1" style="border-bottom:0.8pt solid var(--line);height:14pt"></div></div></div>
<div class="lbl" style="margin-top:6pt">Habit to build</div><div style="height:18pt;border-bottom:0.8pt solid var(--line)"></div>
<div class="lbl" style="margin-top:6pt">Notes</div><div class="lines f1"></div></div>""" for a, b in q)
    inner = f"<div class='f1' style='display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:10pt'>{cells}</div>"
    return page("Quarterly Goals", "90-day focus", inner, "07")


def monthly_tracker():
    nh = 8
    head = "<tr><th style='width:22pt;background:var(--lav);font-size:7pt'>Day</th>" + "".join(
        f"<th style='height:62pt;background:#fff;vertical-align:bottom;padding-bottom:3pt;font-size:6.5pt;color:var(--soft)'>habit {i}</th>" for i in range(1, nh + 1)) + "<th style='width:46pt;background:var(--lav);font-size:7pt'>Mood</th></tr>"
    rows = "".join("<tr>" + f"<td style='font-size:7.5pt;font-weight:600'>{d}</td>" + "<td></td>" * nh + "<td></td></tr>" for d in range(1, 32))
    total = "<tr><td style='font-size:6.5pt;font-weight:600;background:var(--sage)'>Total</td>" + "<td style='background:var(--sage)'></td>" * nh + "<td style='background:var(--sage)'></td></tr>"
    inner = f"""<div class="row" style="align-items:center;margin-bottom:8pt"><div class="lbl">Month</div><div style="width:1.8in;border-bottom:0.8pt solid var(--ink);height:14pt"></div>
<div class="sub" style="margin-left:auto">Write each habit in the top boxes · tick or colour a cell for every day you do it</div></div>
<table class="grid f1" style="height:100%"><tbody style="height:100%">{head}{rows}{total}</tbody></table>"""
    return page("Monthly Habit Tracker", "Undated · reuse monthly", inner, "08")


def weekly_tracker():
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    def wk(label):
        head = "<tr><th style='text-align:left;padding:4pt 6pt;background:var(--lav);font-size:7.5pt'>Habit</th>" + "".join(f"<th style='width:9%;background:var(--lav);font-size:7.5pt'>{d}</th>" for d in days) + "<th style='width:8%;background:var(--lav);font-size:7.5pt'>✓</th></tr>"
        rows = "".join("<tr>" + "<td></td>" + "".join("<td><span style='display:inline-block;width:10pt;height:10pt;border-radius:50%;border:0.8pt solid var(--line)'></span></td>" for _ in days) + "<td></td></tr>" for _ in range(9))
        return f"""<div class="box f1 col" style="gap:5pt"><div style="display:flex;gap:8pt;align-items:center"><span class="tag">{label}</span>
<span class="sub">Week of&nbsp;______________</span></div><table class="grid f1" style="height:100%">{head}{rows}</table>
<div style="display:flex;gap:8pt;align-items:flex-end"><div class="lbl">Win of the week</div><div class="f1" style="border-bottom:0.8pt solid var(--line);height:14pt"></div></div></div>"""
    inner = f"<div class='col f1'>{wk('Week A')}{wk('Week B')}</div>"
    return page("Weekly Habit Tracker", "Two weeks per page", inner, "09")


def pixels():
    head = "<tr><th style='border:none;background:#fff'></th>" + "".join(f"<th>{calendar.month_abbr[m][0]}</th>" for m in range(1, 13)) + "</tr>"
    rows = ""
    for d in range(1, 32):
        rows += f"<tr><td class='dn'>{d}</td>"
        for m in range(1, 13):
            ok = d <= calendar.monthrange(YEAR, m)[1]
            rows += "<td></td>" if ok else "<td class='na'></td>"
        rows += "</tr>"
    legend = "".join(f"<span><i style='background:{c}'></i>____________</span>" for c in ["#fff", "#e9e3f5", "#f7e3e5", "#e3ece0", "#fdf3d8"])
    inner = f"""<div class="row" style="align-items:center;margin-bottom:8pt"><div class="lbl">Tracking</div><div style="width:2.2in;border-bottom:0.8pt solid var(--ink);height:14pt"></div>
<div class="sub" style="margin-left:auto">Mood, a habit, sleep, steps — one colour per day</div></div>
<table class="grid px f1" style="height:100%">{head}{rows}</table>
<div class="legend" style="margin-top:8pt"><span class="lbl">Key</span>{legend}</div>"""
    return page(f"{YEAR} in Pixels", "365-day tracker", inner, "10")


def challenge():
    cells = "".join(f"<div style='aspect-ratio:1;border:0.9pt solid var(--line);border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:Caladea;font-size:14pt;color:var(--lav2)'>{i}</div>" for i in range(1, 31))
    inner = f"""<div class="row"><div class="box f1"><div class="lbl">The challenge</div><div style="height:22pt;border-bottom:0.8pt solid var(--line)"></div></div>
<div class="box" style="width:2.2in"><div class="lbl">Start date</div><div style="height:22pt;border-bottom:0.8pt solid var(--line)"></div></div></div>
<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:12pt 16pt;padding:16pt 0.35in">{cells}</div>
<div class="row f1"><div class="box f1 col"><div class="lbl">Why I'm doing this</div><div class="lines"></div></div>
<div class="box f1 col"><div class="lbl">How it went</div><div class="lines"></div></div></div>"""
    return page("30-Day Challenge", "One habit · 30 days", inner, "11")


def reflection():
    inner = """<div class="row" style="align-items:center;margin-bottom:10pt"><div class="lbl">Month</div><div style="width:1.8in;border-bottom:0.8pt solid var(--ink);height:14pt"></div>
<div class="lbl" style="margin-left:auto">Overall</div><div>☆ ☆ ☆ ☆ ☆</div></div>
<div class="row f1"><div class="box f1 col"><div class="lbl">Wins &amp; highlights</div><div class="lines"></div></div>
<div class="box f1 col"><div class="lbl">What didn't go to plan</div><div class="lines"></div></div></div>
<div style="height:10pt"></div>
<div class="row f1"><div class="box f1 col"><div class="lbl">Habits that stuck</div><div class="lines"></div></div>
<div class="box f1 col"><div class="lbl">I'm grateful for</div><div class="lines"></div></div></div>
<div style="height:10pt"></div>
<div class="box col" style="height:1.5in"><div class="lbl">Next month I will…</div><div class="lines"></div></div>"""
    return page("Monthly Reflection", "Look back · move forward", inner, "12")


def year_end():
    qs = ["My proudest moment of 2027", "Goals I reached", "Habits that changed my life", "Lessons I learned",
          "What I'd do differently", "Words for 2028"]
    cells = "".join(f"<div class='box col'><div class='lbl'>{q}</div><div class='lines'></div></div>" for q in qs)
    inner = f"<div class='f1' style='display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(3,1fr);gap:10pt'>{cells}</div>"
    return page("Year-End Review", "December check-in", inner, "13")


def build_html(size):
    if size == "letter":
        pw, ph, pxh = "8.5in", "11in", "17.6pt"
    else:
        pw, ph, pxh = "210mm", "297mm", "19.2pt"
    pages = [cover(), year_glance(), vision(), wheel(), top_goals(), action_plan(), quarterly(),
             monthly_tracker(), weekly_tracker(), pixels(), challenge(), reflection(), year_end()]
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}{CSS}
:root{{--pw:{pw};--ph:{ph};--pxh:{pxh}}} @page{{size:{pw} {ph};margin:0}}</style></head><body>{''.join(pages)}</body></html>"""


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        for size, fmt, name in [("letter", "Letter", "US-Letter"), ("a4", "A4", "A4")]:
            html = HERE / f"planner_{size}.html"
            html.write_text(build_html(size), encoding="utf-8")
            pg.goto(html.as_uri())
            pg.wait_for_timeout(400)
            pg.pdf(path=str(OUT / f"2027-Habit-Goal-Planner_{name}.pdf"), format=fmt,
                   print_background=True, prefer_css_page_size=True)
        b.close()


if __name__ == "__main__":
    main()
