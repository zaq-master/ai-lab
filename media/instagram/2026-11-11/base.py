# 11/11・11/12 共通の見た目（2026-11-10/render.py のCSSを流用し、湿度テーマ用に水色アクセントへ）
import sys
from playwright.sync_api import sync_playwright
CSS="""
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;font-family:'Noto Sans CJK JP',sans-serif;background:#0f1c3f;color:#fff;overflow:hidden}
.w{position:relative;width:1080px;height:1350px;padding:90px 80px;background:linear-gradient(160deg,#0f1c3f 0%,#1b2f66 60%,#24407f 100%)}
.tag{display:inline-block;background:#5fd4e8;color:#0f1c3f;font-weight:900;font-size:34px;padding:10px 26px;border-radius:40px}
.pg{position:absolute;top:90px;right:80px;font-size:30px;color:#9fb3e0;font-weight:700}
h1{font-size:88px;line-height:1.25;font-weight:900;margin-top:56px}
h2{font-size:60px;line-height:1.3;font-weight:900;margin-top:46px}
.ac{color:#7fe3f2}
.card{background:#fff;color:#0f1c3f;border-radius:36px;padding:40px 48px;margin-top:40px}
.sm{font-size:30px;line-height:1.6;color:#c9d6f5}
.foot{position:absolute;left:80px;right:80px;bottom:60px;font-size:25px;color:#9fb3e0;line-height:1.6}
.row{display:flex;justify-content:space-between;align-items:baseline;font-size:36px;padding:18px 0;border-bottom:3px dashed #d5def2}
.row:last-child{border-bottom:none}
.warn{background:#e8f8fb;border-left:12px solid #1aa6c0;border-radius:20px;padding:24px 32px;margin-top:22px;color:#0f1c3f}
.wt{font-size:35px;font-weight:900}
.wd{font-size:28px;line-height:1.55;color:#41507a;margin-top:6px}
.big{background:#fff;color:#0f1c3f;border-radius:36px;padding:40px 48px;margin-top:50px;text-align:center}
.fx{background:#fff;color:#0f1c3f;border-radius:36px;padding:38px 30px;margin-top:40px;text-align:center;font-size:48px;font-weight:900;line-height:1.45}
.u{color:#0b7f95}
table{width:100%;border-collapse:collapse;font-size:38px;text-align:center}
th{background:#0f1c3f;color:#fff;font-weight:900;padding:18px 6px;font-size:32px}
td{color:#0f1c3f;padding:20px 6px;border-bottom:3px solid #d5def2;font-weight:700}
td.h{font-weight:900;background:#eef3fb}
td.hi{background:#ffe1cc;color:#c2410c;font-weight:900}
.ai{position:absolute;right:40px;bottom:22px;font-size:22px;color:#9fb3e0;background:rgba(255,255,255,.08);padding:4px 14px;border-radius:20px}
.br{display:flex;align-items:center;gap:20px;margin:24px 0}
.bl{flex:0 0 250px;font-size:32px;font-weight:900;text-align:right;line-height:1.3}
.bt{flex:1;display:flex;align-items:center;gap:16px}
.bar{height:58px;border-radius:12px;min-width:12px}
.bv{font-size:40px;font-weight:900;white-space:nowrap}
"""
AI='<div class=ai>🤖 AI運営アカウント</div>'
def render(S,out):
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350})
        for i,s in enumerate(S,1):
            name=f"{i:02d}"
            pg.set_content(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{s}</body></html>")
            pg.wait_for_timeout(200)
            over=pg.evaluate("""()=>{const f=document.querySelector('.foot');const lim=f?f.getBoundingClientRect().top:1350;let bad=[];document.querySelectorAll('.w > *:not(.foot):not(.pg):not(.ai)').forEach(e=>{const r=e.getBoundingClientRect();if(r.bottom>lim-8||r.right>1000)bad.push(e.className+e.tagName+':'+Math.round(r.bottom)+'/'+Math.round(r.right))});return bad.join(' ')+' lim='+Math.round(lim)}""")
            print(name,over)
            pg.screenshot(path=f"{out}/{name}.png")
        b.close()
