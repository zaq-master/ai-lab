# IG 軽い版キットの生成（2026-11-06 ハエル・事業4）
# 画像のbase64ではなく「スライドのHTML/CSS＋使う文字だけのフォント」を送り、IGのタブ内で canvas に描いてJPEGにする。
# 実行：python3 ops/sns/ig_upload_kit/light/make_light.py <元> [出力名]
#   <元> = render.py のあるフォルダ（例 media/instagram/2026-11-06_heater）
#        または 1枚もののHTMLファイル（例 docs/sns/2026-11-04-smart-remote-count.src.html。<style> と <body> の中身を使う）
#   [出力名] 省略時はフォルダ名（HTMLファイルのときは必須。例 2026-11-04_smart-remote）
# 出力：ops/sns/ig_upload_kit/light/<出力名>/  part1..N.txt（JSコードそのまま）、payload.json、manifest.json
# ネットワーク不使用。フォントはシステムの Noto Sans CJK JP（OFL）を pyftsubset で切り出し woff2 化。
# ※マラソン（2026-11-05_marathon）は作り直さない（手順書の E とずれるため）。作り直すなら part と E を必ずセットで更新
import sys, os, re, json, base64, hashlib, io, html as H
from fontTools import subset
from fontTools.ttLib import TTCollection
from playwright.sync_api import sync_playwright

SRC = sys.argv[1].rstrip('/')
if SRC.endswith('.html'):
    if len(sys.argv) < 3: raise SystemExit('HTMLファイルのときは出力名を指定する')
    src = open(SRC, encoding='utf-8').read()
    CSS = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', src, re.S))
    body = re.search(r'<body[^>]*>(.*?)</body>', src, re.S).group(1)
    S = ['<div>' + body + '</div>']  # body の中身を1つの div に包む（.b が body の役）
else:
    # render.py の CSS と S（スライドHTML）だけを取り出す（Playwright部分は実行しない）
    code = open(os.path.join(SRC, 'render.py'), encoding='utf-8').read().split('with sync_playwright')[0]
    ns = {'__name__': 'light', 'sys': sys}
    exec(code.replace('from playwright.sync_api import sync_playwright', ''), ns)
    CSS, S = ns['CSS'], ns['S']
NAME = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(SRC)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), NAME)
os.makedirs(OUT, exist_ok=True)
CHUNK = 38000  # 1回のJS実行に入れる文字数の上限（既存キットの40,000以下）

# 絵文字（🤖）は端末で絵柄・幅が変わるので、同じ大きさの自作ロボットSVG（線画）に置き換える。文言「AI運営アカウント」はそのまま
ROBOT = ('<svg width="24" height="22" viewBox="0 0 24 22" style="vertical-align:-3px;margin-right:6px">'
         '<line x1="12" y1="1" x2="12" y2="5" stroke="#9fb3e0" stroke-width="2"/><circle cx="12" cy="2" r="2" fill="#9fb3e0"/>'
         '<rect x="3" y="5" width="18" height="15" rx="4" fill="#9fb3e0"/><circle cx="8.5" cy="12" r="2.2" fill="#1b2f66"/>'
         '<circle cx="15.5" cy="12" r="2.2" fill="#1b2f66"/><rect x="8" y="16" width="8" height="1.8" rx="0.9" fill="#1b2f66"/></svg>')
S = [s.replace('🤖 ', ROBOT).replace('🤖', ROBOT) for s in S]
FAM = 'AliceSub'  # 端末のフォントと混ざらないよう別名にする
CSS2 = re.sub(r'(^|[\s}])body\{', r'\1.b{', CSS)
CSS2 = re.sub(r'font-family:[^;}]+', f"font-family:'{FAM}',serif", CSS2)
CSS2 = re.sub(r'\s*\n\s*', '', CSS2)

# HTML → XHTML（SVGの中は XML なので）。同時に使う文字を集める
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    xs, chars = [], set()
    for s in S:
        pg.set_content(f'<html><body><div class=b>{s}</div></body></html>')
        xs.append(pg.evaluate("()=>new XMLSerializer().serializeToString(document.querySelector('.b').firstElementChild)"))
        chars |= set(pg.evaluate("()=>document.body.innerText+document.body.textContent"))
    b.close()
chars = {c for c in chars if not c.isspace()} | {' '}
for c in list(chars):
    if ord(c) > 0x1F000: raise SystemExit('絵文字が残っている: ' + c)
text = ''.join(sorted(chars))

def sub(ttc, weight):
    f = TTCollection(ttc)[0]  # 0 = Noto Sans CJK JP
    miss = [c for c in text if ord(c) not in f.getBestCmap()]
    if miss: raise SystemExit(f'{ttc} に無い文字: {miss}')
    opt = subset.Options(); opt.flavor = 'woff2'; opt.hinting = False; opt.desubroutinize = False
    opt.layout_features = ['palt', 'kern', 'liga', 'halt', 'chws', 'vhal', 'vchw']  # halt/chws：「）。」などの約物を詰める（Chromium の text-spacing-trim が使う。11-06 追加、マラソンは追加前）; opt.name_IDs = []; opt.notdef_outline = True
    s = subset.Subsetter(opt); s.populate(text=text); s.subset(f)
    bio = io.BytesIO(); f.flavor = 'woff2'; f.save(bio)
    return base64.b64encode(bio.getvalue()).decode()

D = '/usr/share/fonts/opentype/noto/'
fonts = {'400': sub(D + 'NotoSansCJK-Regular.ttc', 400), '700': sub(D + 'NotoSansCJK-Bold.ttc', 700),
         '900': sub(D + 'NotoSansCJK-Black.ttc', 900)}
payload = json.dumps({'v': 1, 'name': NAME, 'css': CSS2, 'fonts': fonts, 'slides': xs}, ensure_ascii=False, separators=(',', ':'))
json.dump(json.loads(payload), open(os.path.join(OUT, 'payload.json'), 'w', encoding='utf-8'), ensure_ascii=False)

# JSのシングルクォート文字列に入れるため、\ と ' と改行をエスケープ（チャンクごとに。エスケープの途中で切らない）
def esc(t): return t.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
slices = [payload[i:i + CHUNK] for i in range(0, len(payload), CHUNK)]
man = {'name': NAME, 'chars': len(text), 'payload_chars': len(payload), 'parts': []}
for f in os.listdir(OUT):
    if re.match(r'part\d+\.txt$', f): os.remove(os.path.join(OUT, f))
for k, sl in enumerate(slices, 1):
    h = hashlib.sha256(sl.encode('utf-8')).hexdigest()[:16]  # 確認側：crypto.subtle.digest('SHA-256', TextEncoder(文字列)) の先頭16桁
    js = f"window.__igl=window.__igl||[];__igl[{k - 1}]='{esc(sl)}';'part{k}/{len(slices)} len='+__igl[{k - 1}].length"
    open(os.path.join(OUT, f'part{k}.txt'), 'w', encoding='utf-8').write(js)
    man['parts'].append({'k': k, 'len': len(sl), 'sha256_16': h, 'js_chars': len(js)})
man['E'] = [[p['len'], p['sha256_16']] for p in man['parts']]
open(os.path.join(OUT, 'manifest.json'), 'w', encoding='utf-8').write(json.dumps(man, ensure_ascii=False, indent=1))
print(json.dumps({k: v for k, v in man.items() if k != 'parts'}, ensure_ascii=False),
      'parts=', [p['js_chars'] for p in man['parts']], 'total_js=', sum(p['js_chars'] for p in man['parts']),
      'fonts_b64=', {k: len(v) for k, v in fonts.items()}, 'slides=', sum(map(len, xs)))
# inject_light.md の確認コードの E を自動で合わせる（<!-- code:check:<出力名> --> の中だけ。マラソンは従来の <!-- code:check -->）
MD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inject_light.md')
if os.path.exists(MD):
    s = open(MD, encoding='utf-8').read()
    tag = 'check' if NAME == '2026-11-05_marathon' else 'check:' + NAME
    m = re.search(r'<!-- code:' + re.escape(tag) + r' -->\s*```js\n.*?\n```', s, re.S)
    if m:
        blk = re.sub(r'const E=\[\[.*?\]\];', lambda x: 'const E=' + json.dumps(man['E'], separators=(',', ':')) + ';', m.group(0), count=1)
        if blk != m.group(0): open(MD, 'w', encoding='utf-8').write(s[:m.start()] + blk + s[m.end():]); print('inject_light.md の E を更新:', tag)
    else: print('inject_light.md に <!-- code:' + tag + ' --> が無い（確認コードを追加して E=' + json.dumps(man['E']) + ' を入れる）')
