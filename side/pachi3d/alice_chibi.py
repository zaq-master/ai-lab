"""電脳アリス（ちびキャラ版）を SVG で描き、表情ごとの PNG を作る。
2頭身・太い輪郭線・丸い形。特徴（白い長い髪・青いリボン・スペードのヘッドホン）は元のアリスに合わせる。
出力：assets/alice/alice_<目>_<口>.png（600x800、背景透明）
実行：python3 side/pachi3d/alice_chibi.py
"""
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "alice")
L = "#3b3557"           # 輪郭線
SKIN, HAIR, HAIR_S = "#fff3ea", "#f7f8ff", "#cdd3f5"
BLUE, NAVY = "#3d7bff", "#26305e"


def eye(cx, kind):
    if kind == "closed":
        return f'<path d="M{cx-36},318 Q{cx},340 {cx+36},318" stroke="{L}" stroke-width="9" fill="none" stroke-linecap="round"/>'
    if kind == "happy":
        return f'<path d="M{cx-36},330 Q{cx},292 {cx+36},330" stroke="{L}" stroke-width="10" fill="none" stroke-linecap="round"/>'
    rx, ry = (34, 46) if kind != "wide" else (38, 52)
    pupil = 0.55 if kind == "wide" else 1
    return (
        f'<ellipse cx="{cx}" cy="318" rx="{rx}" ry="{ry}" fill="{NAVY}" stroke="{L}" stroke-width="6"/>'
        f'<ellipse cx="{cx}" cy="{318 + ry * 0.35}" rx="{rx * 0.8}" ry="{ry * 0.5}" fill="{BLUE}"/>'
        f'<ellipse cx="{cx}" cy="{318 + ry * 0.45}" rx="{rx * 0.5}" ry="{ry * 0.28}" fill="#8fd0ff"/>'
        f'<ellipse cx="{cx - 12}" cy="{300}" rx="{13 * pupil + 3}" ry="{16 * pupil + 3}" fill="#fff"/>'
        f'<circle cx="{cx + 14}" cy="{338}" r="6" fill="#fff"/>'
    )


def mouth(kind):
    return {
        "smile": f'<path d="M282,392 Q300,408 318,392" stroke="{L}" stroke-width="7" fill="none" stroke-linecap="round"/>',
        "o": f'<ellipse cx="300" cy="398" rx="13" ry="15" fill="#c9465c" stroke="{L}" stroke-width="5"/>',
        "a": f'<path d="M276,386 Q300,380 324,386 Q320,424 300,426 Q280,424 276,386 Z" fill="#c9465c" stroke="{L}" stroke-width="5" stroke-linejoin="round"/>'
             '<path d="M286,410 Q300,402 314,410 Q308,420 300,420 Q292,420 286,410 Z" fill="#ff9aac"/>',
        "grin": f'<path d="M272,384 Q300,428 328,384 Z" fill="#c9465c" stroke="{L}" stroke-width="5" stroke-linejoin="round"/>'
                '<path d="M280,388 L320,388 L316,396 L284,396 Z" fill="#fff"/>',
    }[kind]


def svg(eyes="open", m="smile"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 800" width="600" height="800">
<defs><linearGradient id="h" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{HAIR}"/><stop offset="1" stop-color="{HAIR_S}"/></linearGradient></defs>
<!-- 後ろ髪 -->
<path d="M110,300 Q100,90 300,80 Q500,90 490,300 Q520,520 470,640 Q430,660 400,630 L200,630 Q170,660 130,640 Q80,520 110,300 Z" fill="url(#h)" stroke="{L}" stroke-width="7"/>
<!-- 体 -->
<path d="M190,800 Q190,600 250,560 L350,560 Q410,600 410,800 Z" fill="{NAVY}" stroke="{L}" stroke-width="7"/>
<path d="M250,560 L300,630 L350,560 Q330,600 300,606 Q270,600 250,560 Z" fill="#fff" stroke="{L}" stroke-width="6"/>
<path d="M300,640 L245,610 Q232,650 250,675 Z M300,640 L355,610 Q368,650 350,675 Z" fill="{BLUE}" stroke="{L}" stroke-width="6" stroke-linejoin="round"/>
<circle cx="300" cy="642" r="16" fill="#fff" stroke="{L}" stroke-width="6"/>
<!-- 腕 -->
<path d="M200,640 Q160,700 190,760" stroke="{L}" stroke-width="40" fill="none" stroke-linecap="round"/>
<path d="M200,640 Q160,700 190,760" stroke="{NAVY}" stroke-width="28" fill="none" stroke-linecap="round"/>
<path d="M400,640 Q440,700 410,760" stroke="{L}" stroke-width="40" fill="none" stroke-linecap="round"/>
<path d="M400,640 Q440,700 410,760" stroke="{NAVY}" stroke-width="28" fill="none" stroke-linecap="round"/>
<!-- 顔 -->
<path d="M140,300 Q140,500 300,520 Q460,500 460,300 Q460,140 300,135 Q140,140 140,300 Z" fill="{SKIN}" stroke="{L}" stroke-width="7"/>
<ellipse cx="205" cy="390" rx="30" ry="17" fill="#ffadbe" opacity=".75"/>
<ellipse cx="395" cy="390" rx="30" ry="17" fill="#ffadbe" opacity=".75"/>
{eye(225, eyes)}{eye(375, eyes)}
{mouth(m)}
<!-- 前髪（丸い房） -->
<path d="M130,290 Q120,120 300,110 Q480,120 470,290 Q440,230 410,250 Q395,190 350,215 Q330,170 300,210 Q270,170 250,215 Q205,190 190,250 Q160,230 130,290 Z" fill="url(#h)" stroke="{L}" stroke-width="7" stroke-linejoin="round"/>
<path d="M210,150 Q300,118 390,150" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" opacity=".9"/>
<!-- 横の髪 -->
<path d="M138,290 Q118,420 150,520 Q175,450 170,330 Z" fill="url(#h)" stroke="{L}" stroke-width="6"/>
<path d="M462,290 Q482,420 450,520 Q425,450 430,330 Z" fill="url(#h)" stroke="{L}" stroke-width="6"/>
<!-- ヘッドホン -->
<path d="M120,280 Q120,60 300,56 Q480,60 480,280" stroke="{L}" stroke-width="30" fill="none" stroke-linecap="round"/>
<path d="M120,280 Q120,60 300,56 Q480,60 480,280" stroke="{NAVY}" stroke-width="18" fill="none" stroke-linecap="round"/>
<rect x="88" y="250" width="70" height="110" rx="34" fill="{NAVY}" stroke="{L}" stroke-width="7"/>
<rect x="442" y="250" width="70" height="110" rx="34" fill="{NAVY}" stroke="{L}" stroke-width="7"/>
<circle cx="477" cy="305" r="22" fill="{BLUE}"/>
<path d="M477,288 Q460,305 470,315 Q476,317 477,311 Q478,317 484,315 Q494,305 477,288 Z M473,315 L481,315 L483,323 L471,323 Z" fill="#fff"/>
<circle cx="123" cy="305" r="20" fill="{BLUE}"/><circle cx="123" cy="305" r="8" fill="#fff"/>
<!-- リボン -->
<path d="M380,110 L440,70 Q462,118 430,148 Z" fill="{BLUE}" stroke="{L}" stroke-width="6" stroke-linejoin="round"/>
<path d="M380,110 L350,52 Q314,94 348,134 Z" fill="{BLUE}" stroke="{L}" stroke-width="6" stroke-linejoin="round"/>
<circle cx="378" cy="108" r="14" fill="#fff" stroke="{L}" stroke-width="6"/>
</svg>'''


VARIANTS = [(e, m) for e in ("open", "closed", "happy", "wide") for m in ("smile", "a", "o", "grin")]


def main():
    os.makedirs(OUT, exist_ok=True)
    jobs = []
    for e, m in VARIANTS:
        sp = os.path.join(OUT, f"alice_{e}_{m}.svg")
        open(sp, "w").write(svg(e, m))
        jobs.append([sp, sp[:-4] + ".png"])
    js = ("const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();"
          "const p=await b.newPage({viewport:{width:600,height:800}});for(const [s,o] of %s){"
          "await p.setContent('<html><body style=\"margin:0;background:transparent\">'+fs.readFileSync(s,'utf8')+'</body></html>');"
          "await p.screenshot({path:o,omitBackground:true});fs.unlinkSync(s);}await b.close();})();" % json.dumps(jobs))
    subprocess.run(["node", "-e", js], check=True)


if __name__ == "__main__":
    main()
    print("ok", len(VARIANTS))
