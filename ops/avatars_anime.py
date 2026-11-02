#!/usr/bin/env python3
"""エージェント11人のアニメ風アイコン（オリジナル）をSVGで描き、PNG（256px）に書き出す。
出力：ops/avatars/<key>.png と docs/team/<key>.png、一覧 docs/team/all.png
"""
import json, asyncio
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKIN, SKIN_SH = "#ffe3d0", "#f5c9b0"

# key: (背景, 髪色, 髪の影, 目の色, 服の色, 髪型, 小物, 表情)
C = {
    "ceo": ("#e5dbff", "#d0bfff", "#9775fa", "#7048e8", "#5f3dc4", "long", "crown", "smile"),
    "01": ("#d3f9d8", "#2b8a3e", "#1e6b30", "#2b8a3e", "#ffffff", "bob", "pen", "smile"),
    "02": ("#c5f6fa", "#15aabf", "#0c8599", "#0b7285", "#e3fafc", "short", "robot", "neutral"),
    "03": ("#e9ecef", "#212529", "#000000", "#495057", "#343a40", "spiky", "headset", "open"),
    "04": ("#ffdeeb", "#f783ac", "#e64980", "#d6336c", "#fff0f6", "twin", "star", "wink"),
    "05": ("#ebfbee", "#2f4f3a", "#1b3022", "#5c940d", "#f8f0e3", "long", "beret", "smile"),
    "06": ("#fff4e6", "#f08c00", "#d9480f", "#e8590c", "#fff9db", "pony", "band", "smile"),
    "07": ("#dbe4ff", "#364fc7", "#1c2c8c", "#3b5bdb", "#495057", "messy", "goggles", "grin"),
    "08": ("#fff3bf", "#fcc419", "#e67700", "#1c7ed6", "#ff8787", "wavy", "bow", "open"),
    "09": ("#ffe3e3", "#c92a2a", "#8f1d1d", "#e03131", "#212529", "spiky", "cap", "grin"),
    "10": ("#f1f3f5", "#495057", "#212529", "#343a40", "#212529", "slick", "glasses", "stern"),
}


def eyes(col, expr):
    out = []
    for i, x in enumerate((102, 154)):
        if expr == "wink" and i == 1:
            out.append(f'<path d="M{x-14},134 Q{x},124 {x+14},134" stroke="#3b2a24" stroke-width="5" fill="none" stroke-linecap="round"/>')
            continue
        ry = 13 if expr == "stern" else 18
        out.append(f'<ellipse cx="{x}" cy="134" rx="13" ry="{ry}" fill="#fff"/>'
                   f'<ellipse cx="{x}" cy="{136 if ry==18 else 135}" rx="11" ry="{ry-2}" fill="{col}"/>'
                   f'<ellipse cx="{x}" cy="{138}" rx="6" ry="{ry-8}" fill="#1a1a2e"/>'
                   f'<circle cx="{x-4}" cy="{129}" r="4.5" fill="#fff"/><circle cx="{x+5}" cy="{142}" r="2" fill="#fff" opacity=".8"/>'
                   f'<path d="M{x-16},{134-ry+2} Q{x},{134-ry-6} {x+16},{134-ry+3}" stroke="#2b1d18" stroke-width="5" fill="none" stroke-linecap="round"/>')
    brow = {"stern": ('M88,106 L116,112', 'M168,106 L140,112'), "open": ('M90,104 Q102,98 114,104', 'M142,104 Q154,98 166,104')}
    b = brow.get(expr, ('M90,108 Q102,103 114,107', 'M142,107 Q154,103 166,108'))
    out.append(''.join(f'<path d="{p}" stroke="#4a3328" stroke-width="3.5" fill="none" stroke-linecap="round"/>' for p in b))
    return ''.join(out)


def mouth(expr):
    return {
        "smile": '<path d="M118,168 Q128,177 138,168" stroke="#b5463c" stroke-width="3.5" fill="none" stroke-linecap="round"/>',
        "open": '<path d="M117,166 Q128,184 139,166 Z" fill="#c2453b"/><path d="M121,172 Q128,177 135,172" fill="#ff8a80"/>',
        "grin": '<path d="M114,165 Q128,183 142,165 Z" fill="#fff" stroke="#b5463c" stroke-width="3"/>',
        "wink": '<path d="M118,167 Q128,178 138,167" stroke="#b5463c" stroke-width="3.5" fill="none" stroke-linecap="round"/>',
        "neutral": '<path d="M120,170 L136,170" stroke="#b5463c" stroke-width="3.5" stroke-linecap="round"/>',
        "stern": '<path d="M118,172 Q128,168 138,172" stroke="#8a3a32" stroke-width="3.5" fill="none" stroke-linecap="round"/>',
    }[expr]


def back_hair(style, h, s):
    return {
        "long": f'<path d="M58,120 Q56,40 128,38 Q200,40 198,120 L204,236 L52,236 Z" fill="{s}"/>',
        "wavy": f'<path d="M56,120 Q54,38 128,36 Q202,38 200,120 Q214,160 200,190 Q214,215 196,236 L60,236 Q42,215 56,190 Q42,160 56,120 Z" fill="{s}"/>',
        "bob": f'<path d="M58,118 Q56,42 128,40 Q200,42 198,118 L200,176 Q190,186 176,180 L80,180 Q66,186 56,176 Z" fill="{s}"/>',
        "twin": f'<ellipse cx="46" cy="160" rx="24" ry="56" fill="{s}"/><ellipse cx="210" cy="160" rx="24" ry="56" fill="{s}"/><path d="M60,118 Q58,42 128,40 Q198,42 196,118 Z" fill="{s}"/>',
        "pony": f'<path d="M180,70 Q236,80 226,170 Q214,140 196,120 Z" fill="{s}"/><path d="M60,118 Q58,42 128,40 Q198,42 196,118 Z" fill="{s}"/>',
    }.get(style, f'<path d="M62,118 Q60,44 128,42 Q196,44 194,118 Z" fill="{s}"/>')


def front_hair(style, h):
    if style in ("spiky", "messy"):
        top = '<path d="M70,70 L84,30 L102,58 L118,22 L134,56 L156,26 L162,60 L188,40 L184,80 Z" fill="%s"/>' % h
        return top + f'<path d="M64,124 Q62,56 128,52 Q194,56 192,124 L182,98 L172,118 L160,90 L146,114 L134,86 L120,112 L104,88 L92,116 L80,96 Z" fill="{h}"/>'
    if style == "slick":
        return f'<path d="M64,118 Q60,52 128,48 Q196,52 192,118 Q186,84 160,76 Q120,70 96,82 Q72,92 64,118 Z" fill="{h}"/>'
    bangs = f'<path d="M62,126 Q60,50 128,46 Q196,50 194,126 L184,100 L172,116 L162,92 L146,112 L136,88 L122,110 L108,90 L96,114 L84,96 L74,118 Z" fill="{h}"/>'
    side = f'<path d="M62,120 Q58,150 66,176 L74,130 Z" fill="{h}"/><path d="M194,120 Q198,150 190,176 L182,130 Z" fill="{h}"/>' if style in ("long", "wavy", "bob", "twin") else ''
    return bangs + side + '<path d="M96,70 Q120,58 150,66" stroke="#fff" stroke-width="5" opacity=".35" fill="none" stroke-linecap="round"/>'


def accessory(a, h, eye):
    return {
        "crown": '<path d="M98,52 L106,28 L118,46 L128,22 L138,46 L150,28 L158,52 Z" fill="#fcc419" stroke="#e67700" stroke-width="2"/><circle cx="128" cy="40" r="4" fill="#e64980"/><rect x="186" y="128" width="8" height="18" rx="3" fill="#7048e8"/><circle cx="190" cy="126" r="3" fill="#66d9e8"/>',
        "pen": '<g transform="rotate(-35 196 96)"><rect x="190" y="60" width="9" height="56" rx="2" fill="#fab005"/><path d="M190,116 L194.5,128 L199,116 Z" fill="#495057"/><rect x="190" y="60" width="9" height="8" fill="#e64980"/></g>',
        "robot": '<line x1="128" y1="48" x2="128" y2="20" stroke="#868e96" stroke-width="4"/><circle cx="128" cy="18" r="7" fill="#ff6b6b"/><circle cx="102" cy="136" r="19" fill="none" stroke="#343a40" stroke-width="3.5"/><circle cx="154" cy="136" r="19" fill="none" stroke="#343a40" stroke-width="3.5"/><line x1="121" y1="134" x2="135" y2="134" stroke="#343a40" stroke-width="3.5"/>',
        "headset": '<path d="M62,130 Q60,40 128,38 Q196,40 194,130" stroke="#212529" stroke-width="8" fill="none"/><rect x="50" y="118" width="18" height="34" rx="8" fill="#ff922b"/><rect x="188" y="118" width="18" height="34" rx="8" fill="#ff922b"/><path d="M60,150 Q70,186 110,182" stroke="#212529" stroke-width="4" fill="none"/><circle cx="112" cy="182" r="6" fill="#212529"/>',
        "star": '<path d="M174,70 L179,82 L192,83 L182,91 L186,104 L174,96 L162,104 L166,91 L156,83 L169,82 Z" fill="#fcc419" stroke="#f08c00" stroke-width="2"/>',
        "beret": f'<ellipse cx="124" cy="52" rx="62" ry="20" fill="#c92a2a"/><path d="M70,58 Q128,8 182,52" fill="#c92a2a"/><circle cx="128" cy="26" r="5" fill="#a61e1e"/>',
        "band": '<path d="M66,92 Q128,56 190,92" stroke="#fff" stroke-width="9" fill="none"/><circle cx="182" cy="86" r="9" fill="#ff6b6b"/>',
        "goggles": '<rect x="74" y="62" width="108" height="16" rx="8" fill="#495057"/><circle cx="104" cy="70" r="15" fill="#99e9f2" stroke="#495057" stroke-width="5"/><circle cx="152" cy="70" r="15" fill="#99e9f2" stroke="#495057" stroke-width="5"/>',
        "bow": '<path d="M150,52 L184,36 L182,72 Z M150,52 L120,36 L124,70 Z" fill="#ff6b6b"/><circle cx="152" cy="53" r="8" fill="#e03131"/>',
        "cap": f'<path d="M66,84 Q66,34 128,32 Q190,34 190,84 Z" fill="#212529"/><path d="M60,84 L196,84 Q200,94 190,94 L66,94 Q56,94 60,84 Z" fill="#212529"/><text x="128" y="72" font-size="22" text-anchor="middle" fill="#fff" font-family="sans-serif" font-weight="bold">REC</text><circle cx="96" cy="64" r="5" fill="#fa5252"/>',
        "glasses": '<rect x="84" y="122" width="38" height="26" rx="4" fill="none" stroke="#212529" stroke-width="4"/><rect x="134" y="122" width="38" height="26" rx="4" fill="none" stroke="#212529" stroke-width="4"/><line x1="122" y1="132" x2="134" y2="132" stroke="#212529" stroke-width="4"/>',
    }[a]


def svg(k):
    bg, h, s, eye, cloth, style, acc, expr = C[k]
    over = acc in ("crown", "beret", "cap", "band", "goggles", "star", "bow", "headset", "robot")
    body = (f'<path d="M40,256 Q44,200 96,192 L160,192 Q212,200 216,256 Z" fill="{cloth}"/>'
            f'<path d="M110,184 L146,184 L144,204 Q128,214 112,204 Z" fill="{SKIN_SH}"/>'
            f'<path d="M102,194 L128,224 L154,194" stroke="{h if k!="10" else "#c92a2a"}" stroke-width="6" fill="none"/>')
    face = (f'<ellipse cx="128" cy="128" rx="62" ry="64" fill="{SKIN}"/>'
            f'<ellipse cx="66" cy="136" rx="8" ry="12" fill="{SKIN}"/><ellipse cx="190" cy="136" rx="8" ry="12" fill="{SKIN}"/>'
            '<ellipse cx="94" cy="158" rx="11" ry="6" fill="#ffa8a8" opacity=".55"/><ellipse cx="162" cy="158" rx="11" ry="6" fill="#ffa8a8" opacity=".55"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">'
            f'<defs><clipPath id="c"><circle cx="128" cy="128" r="128"/></clipPath></defs><g clip-path="url(#c)">'
            f'<rect width="256" height="256" fill="{bg}"/>{back_hair(style, h, s)}{body}{face}'
            f'{eyes(eye, expr)}{mouth(expr)}{front_hair(style, h)}{accessory(acc, h, eye) if over or acc in ("pen","glasses") else ""}'
            '</g></svg>')


async def render():
    from playwright.async_api import async_playwright
    out1, out2 = ROOT / "avatars", ROOT.parent / "docs" / "team"
    out1.mkdir(exist_ok=True); out2.mkdir(parents=True, exist_ok=True)
    A = json.load(open(ROOT / "agents.json", encoding="utf-8"))
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 256, "height": 256})
        for k in C:
            await pg.set_content(f'<html><body style="margin:0;background:transparent">{svg(k)}</body></html>')
            png = await pg.screenshot(omit_background=True, clip={"x": 0, "y": 0, "width": 256, "height": 256})
            (out1 / f"{k}.png").write_bytes(png); (out2 / f"{k}.png").write_bytes(png)
        cells = "".join(f'<div style="text-align:center;font:600 15px sans-serif;color:#343a40">{svg(k)}<br>{A[k]["name"]}<br><span style="font-weight:400;font-size:12px;color:#868e96">{A[k]["role"]}</span></div>' for k in C)
        await pg.set_viewport_size({"width": 1660, "height": 640})
        await pg.set_content(f'<html><body style="margin:0;background:#f6f7fb;font-family:Noto Sans CJK JP,sans-serif"><div style="display:grid;grid-template-columns:repeat(6,1fr);gap:12px;padding:16px">{cells}</div></body></html>')
        (out2 / "all.png").write_bytes(await pg.screenshot(full_page=True))
        await b.close()


if __name__ == "__main__":
    asyncio.run(render()); print("ok")
