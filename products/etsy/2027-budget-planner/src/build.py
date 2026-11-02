"""Build the 2027 Budget Planner printable (US Letter + A4).

Same design system as ../../2027-habit-goal-planner (palette, fonts, header/footer).
Usage: python3 build.py   (outputs to ../)  then python3 thumbnail.py
Fonts: Inter (SIL OFL 1.1), Caladea (SIL OFL 1.1) from system font packages.
All artwork is drawn with HTML/CSS/SVG in this file (no third-party images).
Pages are currency-neutral (no $ sign) so they work in any country.
No financial advice: pages are blank record-keeping forms with field labels only.
"""
import calendar
import pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent
YEAR = 2027
BRAND = "DreamyPixelCo"
TITLE = "2027 Budget Planner"

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

# --- budget-specific styles (same tokens as the habit planner) ---
CSS += """
.ul{border-bottom:0.8pt solid var(--line);height:20pt}
.ink{border-bottom:0.8pt solid var(--ink)}
.led th{height:22pt;background:var(--lav);font-size:7pt;font-weight:600;letter-spacing:.6pt;text-transform:uppercase;padding:4pt 3pt}
.led td{font-size:7.5pt}
.led td.l{text-align:left;padding-left:5pt;color:var(--soft)}
.led tr.tot td{background:var(--sage);font-weight:600;font-size:7pt;letter-spacing:.8pt;text-transform:uppercase}
.sec{display:flex;align-items:center;gap:6pt;margin-bottom:4pt}
.sec .dot{width:8pt;height:8pt;border-radius:50%}
.kpi{flex:1;border:0.8pt solid var(--line);border-radius:7pt;padding:7pt 10pt;display:flex;flex-direction:column;gap:3pt}
.kpi .v{height:18pt;border-bottom:0.8pt solid var(--line)}
.cal2 .mc table td{height:16.6pt}
.circ{aspect-ratio:1;border:0.9pt solid var(--line);border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:Caladea;color:var(--lav2)}
"""


def ledger(cols, n, widths=None, total=None, first_label=None, style=""):
    """A ledger table that stretches to fill its box. cols: header labels."""
    widths = widths or [""] * len(cols)
    head = "<tr>" + "".join(f"<th style='width:{w}'>{c}</th>" if w else f"<th>{c}</th>" for c, w in zip(cols, widths)) + "</tr>"
    rows = ""
    for i in range(n):
        lab = first_label[i] if first_label else ""
        cls = " class='l'" if first_label else ""
        rows += f"<tr><td{cls}>{lab}</td>" + "<td></td>" * (len(cols) - 1) + "</tr>"
    if total:
        rows += f"<tr class='tot'><td>{total}</td>" + "<td></td>" * (len(cols) - 1) + "</tr>"
    return f"<table class='grid led' style='{style}'>{head}{rows}</table>"


def sec(label, color="var(--lav2)"):
    return f"<div class='sec'><span class='dot' style='background:{color}'></span><span class='lbl'>{label}</span></div>"


def month_line(extra=""):
    return f"""<div class="row" style="align-items:center;margin-bottom:9pt"><div class="lbl">Month</div>
<div class="ink" style="width:1.8in;height:14pt"></div>{extra}</div>"""


ITEMS = ["Year at a Glance", "Money Goals", "Annual Overview", "Monthly Budget", "Paycheck Budget",
         "Bill Tracker", "Expense Tracker", "Weekly Spending Log", "Savings Goal Tracker", "Sinking Funds",
         "Debt Payoff Tracker", "No-Spend Challenge", "Monthly Money Review"]


def cover():
    li = "".join(f"<div><span>{i+2:02d}</span>{t}</div>" for i, t in enumerate(ITEMS))
    coin = """<svg width="120" height="34" viewBox="0 0 120 34"><path d="M4 17 H50" stroke="#9bb596" stroke-width="1"/>
<path d="M70 17 H116" stroke="#9bb596" stroke-width="1"/><circle cx="60" cy="17" r="7" fill="#e3ece0" stroke="#9bb596"/>
<circle cx="60" cy="17" r="3.4" fill="none" stroke="#9bb596" stroke-width="0.9"/></svg>"""
    return f"""<section class="page cover"><div class="frame"></div>
<div class="t2">Printable Planner</div>{coin}
<div class="yr">{YEAR}</div><div class="t1">Budget Planner</div>
<div class="t2">Plan it · Track it · Save it</div>
<div class="contents">{li}</div>
<div class="nm">This planner belongs to</div></section>"""


def year_glance():
    cal = calendar.Calendar(firstweekday=6)  # Sunday start (US)
    blocks = []
    for m in range(1, 13):
        weeks = cal.monthdayscalendar(YEAR, m)
        while len(weeks) < 6:
            weeks.append([0] * 7)
        rows = "".join("<tr>" + "".join(
            f"<td class='{'we' if i in (0, 6) else ''}'>{d if d else ''}</td>" for i, d in enumerate(w)) + "</tr>" for w in weeks)
        head = "<tr>" + "".join(f"<th>{d}</th>" for d in DOW) + "</tr>"
        blocks.append(f"<div class='mc'><div class='mn'>{calendar.month_name[m]}</div><table>{head}{rows}</table></div>")
    key = """<div class="legend" style="margin-top:8pt"><span class="lbl">Key</span>
<span><i style="background:#e3ece0"></i>Payday</span><span><i style="background:#f7e3e5"></i>Bill due</span>
<span><i style="background:#e9e3f5"></i>Savings day</span><span><i style="background:#fdf3d8"></i>____________</span></div>"""
    inner = f"<div class='cal cal2'>{''.join(blocks)}</div>{key}"
    return page(f"{YEAR} at a Glance", "Paydays &amp; due dates", inner, "02")


def money_goals():
    def g(n):
        return f"""<div class="box f1 col" style="gap:6pt"><div style="display:flex;align-items:center;gap:8pt">
<div style="width:22pt;height:22pt;border-radius:50%;background:var(--sage);display:flex;align-items:center;justify-content:center;font-family:Caladea;font-weight:700;font-size:12pt">{n}</div>
<div class="f1 ink" style="height:18pt"></div></div>
<div class="row"><div class="kpi"><div class="lbl">Target amount</div><div class="v"></div></div>
<div class="kpi"><div class="lbl">Target date</div><div class="v"></div></div>
<div class="kpi"><div class="lbl">Per month</div><div class="v"></div></div></div>
<div class="f1 col" style="gap:2pt"><div class="lbl">Why it matters to me</div><div class="lines"></div></div></div>"""
    inner = f"""<div class="box" style="text-align:center;padding:10pt"><div class="lbl">My money word of the year</div>
<div style="height:28pt;border-bottom:0.8pt solid var(--line);margin:2pt 1.4in 0"></div></div>
<div style="height:10pt"></div><div class='col f1'>{g(1)}{g(2)}{g(3)}</div>"""
    return page("Money Goals", f"Focus for {YEAR}", inner, "03")


def annual_overview():
    cols = ["Month", "Income", "Expenses", "Saved", "Debt paid", "Left over"]
    inner = f"""<div class="sub" style="margin-bottom:6pt">Fill in one row at the end of each month from your Monthly Budget page.</div>
<div class="f1">{ledger(cols, 12, ["18%"] + [""] * 5, total="Total", first_label=[calendar.month_name[m] for m in range(1, 13)])}</div>
<div style="height:10pt"></div>
<div class="row" style="height:1.7in"><div class="box f1 col"><div class="lbl">Best month &amp; why</div><div class="lines"></div></div>
<div class="box f1 col"><div class="lbl">Notes for next year</div><div class="lines"></div></div></div>"""
    return page("Annual Overview", f"{YEAR} money at a glance", inner, "04")


def monthly_budget():
    w = ["", "22%", "22%"]

    def block(title, n, color):
        cols = [title, "Planned", "Actual"]
        return f"<div class='f1 col' style='gap:0'>{sec(title, color)}<div class='f1'>{ledger(cols, n, w, total='Total')}</div></div>"
    kpis = """<div class="row" style="margin-bottom:10pt"><div class="kpi"><div class="lbl">Total income</div><div class="v"></div></div>
<div class="kpi"><div class="lbl">Total expenses</div><div class="v"></div></div>
<div class="kpi"><div class="lbl">Total savings</div><div class="v"></div></div>
<div class="kpi" style="background:var(--sage)"><div class="lbl">Left over</div><div class="v" style="border-color:var(--sage2)"></div></div></div>"""
    inner = f"""{month_line()}{kpis}
<div class="row f1"><div class="col f1" style="gap:10pt">{block('Income', 5, 'var(--sage2)')}{block('Savings', 5, 'var(--lav2)')}</div>
<div class="col f1" style="gap:10pt;flex:1.25">{block('Fixed expenses', 9, '#e2aab1')}{block('Variable expenses', 8, '#e2aab1')}</div></div>"""
    return page("Monthly Budget", "Undated · reuse monthly", inner, "05")


def paycheck():
    def one(label):
        return f"""<div class="box f1 col" style="gap:6pt"><div style="display:flex;gap:10pt;align-items:center"><span class="tag" style="background:var(--sage)">{label}</span>
<span class="sub">Pay date&nbsp;____________</span><span class="sub" style="margin-left:auto">Amount&nbsp;________________</span></div>
<div class="f1">{ledger(['Bill / expense', 'Due', 'Amount', 'Paid'], 9, ['', '14%', '20%', '10%'])}</div>
<div class="row"><div class="kpi"><div class="lbl">Total out</div><div class="v"></div></div>
<div class="kpi"><div class="lbl">To savings</div><div class="v"></div></div>
<div class="kpi" style="background:var(--sage)"><div class="lbl">Left over</div><div class="v" style="border-color:var(--sage2)"></div></div></div></div>"""
    inner = f"<div class='col f1'>{one('Paycheck 1')}{one('Paycheck 2')}</div>"
    return page("Paycheck Budget", "Two paychecks per page", inner, "06")


def bill_tracker():
    months = [calendar.month_abbr[m][0] for m in range(1, 13)]
    cols = ["Bill", "Due", "Amount"] + months
    widths = ["24%", "7%", "11%"] + [""] * 12
    inner = f"""<div class="sub" style="margin-bottom:6pt">Write each regular bill once · tick the month when it's paid</div>
<div class="f1">{ledger(cols, 18, widths)}</div>
<div style="height:10pt"></div>
<div class="row" style="height:1.3in"><div class="box f1 col"><div class="lbl">Annual / one-off bills</div><div class="lines"></div></div>
<div class="box f1 col"><div class="lbl">Subscriptions to review</div><div class="lines"></div></div></div>"""
    return page("Bill Tracker", "12 months · one page", inner, "07")


def expense_tracker():
    cols = ["Date", "Description", "Category", "Method", "Amount"]
    inner = f"""{month_line('<div class="sub" style="margin-left:auto">Budget&nbsp;____________&nbsp;&nbsp;·&nbsp;&nbsp;Spent&nbsp;____________</div>')}
<div class="f1">{ledger(cols, 28, ['10%', '', '20%', '14%', '16%'], total='Total')}</div>"""
    return page("Expense Tracker", "Every purchase, one line", inner, "08")


def weekly_log():
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    def wk(label):
        return f"""<div class="box f1 col" style="gap:5pt"><div style="display:flex;gap:8pt;align-items:center"><span class="tag">{label}</span>
<span class="sub">Week of&nbsp;______________</span><span class="sub" style="margin-left:auto">Budget&nbsp;__________</span></div>
<div class="f1">{ledger(['Day', 'What I spent on', 'Need / want', 'Amount'], 7, ['10%', '', '17%', '17%'], total='Week total', first_label=days)}</div></div>"""
    inner = f"<div class='col f1'>{wk('Week A')}{wk('Week B')}</div>"
    return page("Weekly Spending Log", "Two weeks per page", inner, "09")


def savings():
    def one(label, color):
        cells = "".join(f"<div class='circ' style='font-size:8pt'>{i}</div>" for i in range(1, 41))
        return f"""<div class="box f1 col" style="gap:6pt"><div style="display:flex;gap:10pt;align-items:center"><span class="tag" style="background:{color}">{label}</span>
<span class="lbl">Saving for</span><div class="f1 ink" style="height:14pt"></div></div>
<div class="row"><div class="kpi"><div class="lbl">Goal amount</div><div class="v"></div></div>
<div class="kpi"><div class="lbl">Each circle =</div><div class="v"></div></div>
<div class="kpi"><div class="lbl">Goal date</div><div class="v"></div></div></div>
<div class="f1" style="display:grid;grid-template-columns:repeat(10,1fr);gap:6pt 10pt;padding:4pt 0.25in;align-content:center">{cells}</div>
<div class="sub" style="text-align:center">Colour one circle each time you add to this goal</div></div>"""
    inner = f"<div class='col f1'>{one('Goal A', 'var(--sage)')}{one('Goal B', 'var(--blush)')}</div>"
    return page("Savings Goal Tracker", "Colour in as you save", inner, "10")


def sinking():
    def card():
        return f"""<div class="box col" style="gap:5pt;min-height:0"><div style="display:flex;gap:6pt;align-items:flex-end"><span class="lbl">Fund</span><div class="f1 ink" style="height:14pt"></div></div>
<div style="display:flex;gap:6pt;align-items:flex-end"><span class="lbl">Goal</span><div class="f1 ul" style="height:14pt"></div><span class="lbl">By</span><div class="ul" style="width:0.8in;height:14pt"></div></div>
<div class="f1">{ledger(['Date', 'Added', 'Balance'], 7, ['30%', '', ''])}</div></div>"""
    inner = f"""<div class="sub" style="margin-bottom:6pt">Money set aside for costs you know are coming — gifts, car, holidays, insurance</div>
<div class='f1' style='display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(3,1fr);gap:10pt;min-height:0'>{''.join(card() for _ in range(6))}</div>"""
    return page("Sinking Funds", "Six funds per page", inner, "11")


def debt():
    over = ledger(["Debt", "Balance", "Rate", "Min. payment", "Due", "Order"], 7, ["", "16%", "10%", "16%", "8%", "9%"], total="Total")
    seg = "".join(f"<div style='flex:1;border:0.8pt solid var(--line);height:20pt;display:flex;align-items:center;justify-content:center;font-size:6.6pt;color:var(--soft)'>{p}%</div>" for p in range(10, 101, 10))
    log = ledger(["Date", "Payment", "Balance"], 12, ["30%", "", ""])
    inner = f"""{sec('All debts', '#e2aab1')}<div style="height:2.5in">{over}</div>
<div style="height:10pt"></div>
<div class="box col" style="gap:6pt;flex:1;min-height:0"><div style="display:flex;gap:8pt;align-items:flex-end"><span class="lbl">Payment log for</span><div class="f1 ink" style="height:14pt"></div>
<span class="lbl">Starting balance</span><div class="ul" style="width:1.2in;height:14pt"></div></div>
<div style="display:flex;gap:0">{seg}</div>
<div class="row f1"><div class="f1">{log}</div><div class="f1">{log}</div></div></div>"""
    return page("Debt Payoff Tracker", "Watch the balance fall", inner, "12")


def no_spend():
    cells = "".join(f"<div class='circ' style='font-size:14pt'>{i}</div>" for i in range(1, 31))
    inner = f"""<div class="row"><div class="box f1"><div class="lbl">Month / dates</div><div class="ul"></div></div>
<div class="box f1"><div class="lbl">Still allowed (essentials)</div><div class="ul"></div></div></div>
<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:12pt 16pt;padding:16pt 0.35in">{cells}</div>
<div class="sub" style="text-align:center;margin-top:-6pt;margin-bottom:10pt">Colour a circle for every day with no extra spending</div>
<div class="row f1"><div class="box f1 col"><div class="lbl">Things I didn't buy</div><div class="lines"></div></div>
<div class="box f1 col"><div class="lbl">What I did instead</div><div class="lines"></div></div></div>"""
    return page("No-Spend Challenge", "30 days", inner, "13")


def review():
    inner = f"""{month_line('<div class="lbl" style="margin-left:auto">Overall</div><div>☆ ☆ ☆ ☆ ☆</div>')}
<div class="row"><div class="kpi"><div class="lbl">Income</div><div class="v"></div></div>
<div class="kpi"><div class="lbl">Spent</div><div class="v"></div></div>
<div class="kpi"><div class="lbl">Saved</div><div class="v"></div></div>
<div class="kpi"><div class="lbl">Debt paid</div><div class="v"></div></div></div>
<div style="height:10pt"></div>
<div class="row f1"><div class="box f1 col"><div class="lbl">Money wins</div><div class="lines"></div></div>
<div class="box f1 col"><div class="lbl">Where I overspent</div><div class="lines"></div></div></div>
<div style="height:10pt"></div>
<div class="row f1"><div class="box f1 col"><div class="lbl">Biggest expenses</div><div class="lines"></div></div>
<div class="box f1 col"><div class="lbl">Bills or prices that changed</div><div class="lines"></div></div></div>
<div style="height:10pt"></div>
<div class="box col" style="height:1.4in"><div class="lbl">Next month I will…</div><div class="lines"></div></div>"""
    return page("Monthly Money Review", "Look back · plan ahead", inner, "14")


def build_html(size):
    if size == "letter":
        pw, ph, pxh = "8.5in", "11in", "17.6pt"
    else:
        pw, ph, pxh = "210mm", "297mm", "19.2pt"
    pages = [cover(), year_glance(), money_goals(), annual_overview(), monthly_budget(), paycheck(),
             bill_tracker(), expense_tracker(), weekly_log(), savings(), sinking(), debt(), no_spend(), review()]
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}{CSS}
:root{{--pw:{pw};--ph:{ph};--pxh:{pxh}}} @page{{size:{pw} {ph};margin:0}}</style></head><body>{''.join(pages)}</body></html>"""


# Spread ledger rows evenly over the space their box has (CSS tables give the spare height to text rows).
FILL_JS = """() => document.querySelectorAll('table.led').forEach(t => {
  const H = t.parentElement.clientHeight, rows = [...t.rows], head = rows[0].offsetHeight;
  const h = Math.floor((H - head - 2) / (rows.length - 1) * 10) / 10;
  rows.slice(1).forEach(r => r.style.height = h + 'px');
})"""


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        for size, fmt, name in [("letter", "Letter", "US-Letter"), ("a4", "A4", "A4")]:
            html = HERE / f"planner_{size}.html"
            html.write_text(build_html(size), encoding="utf-8")
            pg.goto(html.as_uri())
            pg.wait_for_timeout(400)
            pg.evaluate(FILL_JS)
            pg.pdf(path=str(OUT / f"2027-Budget-Planner_{name}.pdf"), format=fmt,
                   print_background=True, prefer_css_page_size=True)
        b.close()


if __name__ == "__main__":
    main()
