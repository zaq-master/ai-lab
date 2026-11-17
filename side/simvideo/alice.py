"""電脳アリス（解説役）を SVG で描き、表情ごとの PNG を作る。
ジャケット絵（music/01_1-319/alice_small.png）の特徴に合わせたオリジナル：
白い長い髪・青い目・スペードのヘッドホン・青いリボン・白黒の襟。
出力：side/simvideo/assets/alice_<目>_<口>.png（720x900、背景透明）
実行：python3 side/simvideo/alice.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets")

SKIN, SKIN_SH, LINE = "#fff1e8", "#f6d6c8", "#5b6b8c"
HAIR, HAIR_SH, HAIR_HI = "#f4f7ff", "#c9d3ee", "#ffffff"
BLUE, BLUE_D, BLUE_L = "#2f6bff", "#1a3fae", "#8fb4ff"


def defs():
    return f'''<defs>
<linearGradient id="hair" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{HAIR}"/><stop offset="1" stop-color="{HAIR_SH}"/></linearGradient>
<linearGradient id="hairback" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#dfe6fa"/><stop offset="1" stop-color="#aebce6"/></linearGradient>
<radialGradient id="iris" cx="0.5" cy="0.62" r="0.6"><stop offset="0" stop-color="#9cdcff"/><stop offset="0.45" stop-color="{BLUE}"/><stop offset="1" stop-color="#0e1f6b"/></radialGradient>
<linearGradient id="cloth" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e2846"/><stop offset="1" stop-color="#0f1428"/></linearGradient>
<linearGradient id="ribbon" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5b8cff"/><stop offset="1" stop-color="{BLUE_D}"/></linearGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
</defs>'''


def back_hair():
    return ('<path d="M150,250 Q130,90 300,80 Q470,90 450,250 L500,640 Q470,700 430,690 L410,520 '
            'L190,520 L170,690 Q130,700 100,640 Z" fill="url(#hairback)" stroke="#9aa8d6" stroke-width="3"/>')


def body():
    return (
        # 首
        f'<path d="M262,420 L338,420 L342,500 Q300,522 258,500 Z" fill="{SKIN_SH}"/>'
        # 服（黒のワンピース＋白い襟）
        '<path d="M120,900 Q126,560 250,505 L350,505 Q474,560 480,900 Z" fill="url(#cloth)" stroke="#0a0f20" stroke-width="3"/>'
        '<path d="M250,505 L300,580 L350,505 Q330,540 300,548 Q270,540 250,505 Z" fill="#f7f9ff" stroke="#b8c2de" stroke-width="3"/>'
        '<path d="M232,512 Q246,560 300,582 Q254,590 214,548 Z" fill="#f7f9ff" stroke="#b8c2de" stroke-width="3"/>'
        '<path d="M368,512 Q354,560 300,582 Q346,590 386,548 Z" fill="#f7f9ff" stroke="#b8c2de" stroke-width="3"/>'
        # 胸元のリボン
        '<path d="M300,590 L226,556 Q212,600 230,632 Z" fill="url(#ribbon)" stroke="#16307f" stroke-width="3"/>'
        '<path d="M300,590 L374,556 Q388,600 370,632 Z" fill="url(#ribbon)" stroke="#16307f" stroke-width="3"/>'
        '<path d="M290,600 L270,700 L292,690 Z M310,600 L330,700 L308,690 Z" fill="url(#ribbon)" stroke="#16307f" stroke-width="3"/>'
        '<circle cx="300" cy="594" r="15" fill="#e8eeff" stroke="#16307f" stroke-width="3"/>'
        '<path d="M300,585 Q292,594 300,603 Q308,594 300,585 Z" fill="#16307f"/>'
        # 服の光るライン（電脳）
        f'<path d="M180,820 L260,740 L260,680 M420,820 L340,740 L340,680" stroke="{BLUE_L}" stroke-width="3" fill="none" opacity=".7"/>'
        f'<circle cx="260" cy="680" r="5" fill="{BLUE_L}"/><circle cx="340" cy="680" r="5" fill="{BLUE_L}"/>'
    )


def face():
    return (f'<path d="M190,250 Q188,410 300,450 Q412,410 410,250 Z" fill="{SKIN}" stroke="{LINE}" stroke-width="2.5"/>'
            f'<ellipse cx="226" cy="368" rx="24" ry="12" fill="#ffb3c1" opacity=".55"/>'
            f'<ellipse cx="374" cy="368" rx="24" ry="12" fill="#ffb3c1" opacity=".55"/>'
            f'<path d="M296,350 L300,358" stroke="#d9a99a" stroke-width="3" stroke-linecap="round"/>')


def eye(cx, kind, right):
    sgn = 1 if right else -1
    if kind == "closed":
        return (f'<path d="M{cx-34},312 Q{cx},330 {cx+34},312" stroke="#2a3150" stroke-width="6" fill="none" stroke-linecap="round"/>'
                f'<path d="M{cx+sgn*34},312 L{cx+sgn*44},304" stroke="#2a3150" stroke-width="5" stroke-linecap="round"/>')
    if kind == "happy":
        return f'<path d="M{cx-32},322 Q{cx},290 {cx+32},322" stroke="#2a3150" stroke-width="7" fill="none" stroke-linecap="round"/>'
    ry = 40 if kind != "wide" else 46
    return (
        f'<ellipse cx="{cx}" cy="312" rx="31" ry="{ry}" fill="#ffffff"/>'
        f'<ellipse cx="{cx}" cy="{316}" rx="27" ry="{ry-4}" fill="url(#iris)"/>'
        f'<ellipse cx="{cx}" cy="{322}" rx="12" ry="{ry-20}" fill="#0b1440"/>'
        f'<ellipse cx="{cx-9}" cy="296" rx="10" ry="12" fill="#fff"/>'
        f'<circle cx="{cx+11}" cy="336" r="5" fill="#fff" opacity=".85"/>'
        f'<path d="M{cx-18},346 Q{cx},354 {cx+18},346" stroke="#c8ecff" stroke-width="3" fill="none" opacity=".8"/>'
        # まつげ（上）
        f'<path d="M{cx-38},{318-ry+4} Q{cx},{300-ry-6} {cx+38},{318-ry+6}" stroke="#2a3150" stroke-width="8" fill="none" stroke-linecap="round"/>'
        f'<path d="M{cx+sgn*36},{318-ry+6} L{cx+sgn*50},{318-ry-4}" stroke="#2a3150" stroke-width="6" stroke-linecap="round"/>'
    )


def brows(kind):
    if kind == "wide":
        return ('<path d="M216,248 Q240,236 264,246" stroke="#b9c2dc" stroke-width="5" fill="none" stroke-linecap="round"/>'
                '<path d="M336,246 Q360,236 384,248" stroke="#b9c2dc" stroke-width="5" fill="none" stroke-linecap="round"/>')
    return ('<path d="M216,258 Q240,250 264,256" stroke="#b9c2dc" stroke-width="5" fill="none" stroke-linecap="round"/>'
            '<path d="M336,256 Q360,250 384,258" stroke="#b9c2dc" stroke-width="5" fill="none" stroke-linecap="round"/>')


def mouth(kind):
    return {
        "smile": '<path d="M282,392 Q300,404 318,392" stroke="#b44d5c" stroke-width="4" fill="none" stroke-linecap="round"/>',
        "a": '<path d="M280,388 Q300,384 320,388 Q316,418 300,420 Q284,418 280,388 Z" fill="#a8364a" stroke="#7d2436" stroke-width="2"/>'
             '<path d="M288,408 Q300,402 312,408 Q306,416 300,416 Q294,416 288,408 Z" fill="#ff8fa3"/>',
        "o": '<ellipse cx="300" cy="398" rx="10" ry="12" fill="#a8364a" stroke="#7d2436" stroke-width="2"/>',
        "grin": '<path d="M278,386 Q300,416 322,386 Z" fill="#a8364a" stroke="#7d2436" stroke-width="2"/>'
                '<path d="M284,388 L316,388 L312,394 L288,394 Z" fill="#fff"/>',
    }[kind]


def front_hair():
    return (
        '<path d="M182,300 Q160,120 300,108 Q440,120 418,300 L404,262 L392,300 L372,214 L350,282 L326,196 L306,270 '
        'L284,192 L262,282 L240,214 L218,296 L206,256 Z" fill="url(#hair)" stroke="#a9b6dc" stroke-width="3" stroke-linejoin="round"/>'
        # 横の髪
        '<path d="M186,280 Q162,380 176,500 Q196,430 206,330 Z" fill="url(#hair)" stroke="#a9b6dc" stroke-width="3"/>'
        '<path d="M414,280 Q438,380 424,500 Q404,430 394,330 Z" fill="url(#hair)" stroke="#a9b6dc" stroke-width="3"/>'
        # つや
        '<path d="M232,170 Q300,140 372,170" stroke="#ffffff" stroke-width="9" fill="none" opacity=".8" stroke-linecap="round"/>'
        '<path d="M250,190 Q300,172 350,190" stroke="#dbe7ff" stroke-width="5" fill="none" opacity=".8" stroke-linecap="round"/>'
    )


def headphones():
    return (
        f'<path d="M160,250 Q170,70 300,66 Q430,70 440,250" stroke="#1b2340" stroke-width="22" fill="none" stroke-linecap="round"/>'
        f'<path d="M168,240 Q178,84 300,80 Q422,84 432,240" stroke="{BLUE}" stroke-width="5" fill="none" opacity=".8"/>'
        '<rect x="134" y="232" width="62" height="104" rx="26" fill="#1b2340" stroke="#0a0f20" stroke-width="3"/>'
        '<rect x="404" y="232" width="62" height="104" rx="26" fill="#1b2340" stroke="#0a0f20" stroke-width="3"/>'
        f'<circle cx="435" cy="284" r="20" fill="{BLUE}" filter="url(#glow)" opacity=".8"/>'
        '<path d="M435,266 Q418,284 428,294 Q434,296 435,290 Q436,296 442,294 Q452,284 435,266 Z M431,294 L439,294 L441,302 L429,302 Z" fill="#ffffff"/>'
        f'<circle cx="165" cy="284" r="18" fill="{BLUE}" filter="url(#glow)" opacity=".7"/>'
        '<circle cx="165" cy="284" r="8" fill="#ffffff"/>'
        # 頭のリボン
        '<path d="M360,112 L410,70 Q430,110 404,140 Z" fill="url(#ribbon)" stroke="#16307f" stroke-width="3"/>'
        '<path d="M360,112 L330,60 Q300,96 330,132 Z" fill="url(#ribbon)" stroke="#16307f" stroke-width="3"/>'
        '<circle cx="358" cy="112" r="11" fill="#e8eeff" stroke="#16307f" stroke-width="3"/>'
    )


def svg(eyes="open", mouth_kind="smile"):
    e = (eye(240, eyes, False) + eye(360, eyes, True))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 900" width="720" height="1080">{defs()}'
            f'{back_hair()}{body()}{face()}{brows(eyes)}{e}{mouth(mouth_kind)}{front_hair()}{headphones()}</svg>')


VARIANTS = [(e, m) for e in ("open", "closed", "happy", "wide") for m in ("smile", "a", "o", "grin")]


def main():
    """SVGを書き出し、Node版 Playwright で PNG にする（Python版は入っていないため）。"""
    import json
    import subprocess
    os.makedirs(OUT, exist_ok=True)
    jobs = []
    for e, m in VARIANTS:
        sp = os.path.join(OUT, f"alice_{e}_{m}.svg")
        open(sp, "w").write(svg(e, m))
        jobs.append([sp, sp[:-4] + ".png"])
    js = ("const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();"
          "const p=await b.newPage({viewport:{width:720,height:1080}});for(const [s,o] of %s){"
          "await p.setContent('<html><body style=\\'margin:0;background:transparent\\'>'+fs.readFileSync(s,'utf8')+'</body></html>');"
          "await p.screenshot({path:o,omitBackground:true});fs.unlinkSync(s);}await b.close();})();" % json.dumps(jobs))
    subprocess.run(["node", "-e", js], check=True)


if __name__ == "__main__":
    main()
    print("ok", len(VARIANTS))
