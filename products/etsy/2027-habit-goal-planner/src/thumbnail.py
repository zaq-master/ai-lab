"""Etsy listing thumbnail (2000x1600 PNG) built from the real planner pages.
Usage: python3 thumbnail.py   (needs ../2027-Habit-Goal-Planner_US-Letter.pdf; uses pdftoppm)
"""
import pathlib
import subprocess
import tempfile
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent
PDF = OUT / "2027-Habit-Goal-Planner_US-Letter.pdf"
INTER = "/usr/share/fonts/opentype/inter"
CAL = "/usr/share/fonts/truetype/crosextra"


def main():
    tmp = pathlib.Path(tempfile.mkdtemp())
    pages = {}
    for n in (1, 2, 5, 8, 10):
        subprocess.run(["pdftoppm", "-r", "130", "-png", "-f", str(n), "-l", str(n), "-singlefile",
                        str(PDF), str(tmp / f"p{n}")], check=True)
        pages[n] = (tmp / f"p{n}.png").as_uri()

    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:'Inter';font-weight:500;src:url('file://{INTER}/Inter-Medium.otf')}}
@font-face{{font-family:'Inter';font-weight:700;src:url('file://{INTER}/Inter-Bold.otf')}}
@font-face{{font-family:'Caladea';font-weight:700;src:url('file://{CAL}/Caladea-Bold.ttf')}}
@font-face{{font-family:'Caladea';font-style:italic;src:url('file://{CAL}/Caladea-Italic.ttf')}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:2000px;height:1600px;overflow:hidden;font-family:Inter;color:#3d3a4b;
 background:radial-gradient(circle at 78% 30%,#f7e3e5 0,transparent 45%),radial-gradient(circle at 70% 90%,#e3ece0 0,transparent 40%),#efeaf7;position:relative}}
.left{{position:absolute;left:110px;top:150px;width:760px}}
.k{{font-size:30px;letter-spacing:9px;text-transform:uppercase;font-weight:500;color:#8a86a0}}
.yr{{font-family:Caladea;font-weight:700;font-size:270px;line-height:.9;margin-top:24px;letter-spacing:-6px}}
.t{{font-family:Caladea;font-style:italic;font-size:92px;line-height:1.05;margin-top:10px}}
.pills{{margin-top:56px;display:flex;flex-wrap:wrap;gap:18px}}
.pill{{background:#fff;border-radius:60px;padding:18px 34px;font-size:32px;font-weight:700;box-shadow:0 4px 14px rgba(61,58,75,.08)}}
.pill b{{color:#9a86c4}}
.foot{{position:absolute;left:110px;bottom:120px;font-size:30px;font-weight:500;color:#6c6884;line-height:1.6}}
.pg{{position:absolute;width:640px;background:#fff;border-radius:10px;box-shadow:0 30px 60px rgba(61,58,75,.22)}}
.pg img{{width:100%;display:block;border-radius:10px}}
</style></head><body>
<div class="pg" style="left:1010px;top:250px;transform:rotate(-9deg)"><img src="{pages[8]}"></div>
<div class="pg" style="left:1260px;top:210px;transform:rotate(6deg)"><img src="{pages[10]}"></div>
<div class="pg" style="left:1150px;top:360px;transform:rotate(-1deg);width:690px"><img src="{pages[1]}"></div>
<div class="left">
 <div class="k">Printable PDF</div>
 <div class="yr">2027</div>
 <div class="t">Habit &amp; Goal<br>Planner</div>
 <div class="pills"><div class="pill"><b>13</b> pages</div><div class="pill">US Letter <b>+</b> A4</div>
 <div class="pill">Habit trackers</div><div class="pill">Goal setting</div><div class="pill">Year in Pixels</div></div>
</div>
<div class="foot">Instant download · Print at home<br>Digital file only — no physical item shipped</div>
</body></html>"""
    f = tmp / "thumb.html"
    f.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 2000, "height": 1600})
        pg.goto(f.as_uri())
        pg.wait_for_timeout(500)
        pg.screenshot(path=str(OUT / "thumbnail_2000x1600.png"))
        b.close()


if __name__ == "__main__":
    main()
