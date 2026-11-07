#!/usr/bin/env python3
"""楽天ボタン・PR表記の点検（12:00回）。python3 build.py の後に python3 ops/check_affiliate.py。問題0件なら最後に OK。"""
import json,re,glob,sys,os
os.chdir(os.path.dirname(os.path.abspath(__file__))+"/..")
sys.dont_write_bytecode=True
from urllib.parse import unquote
sys.path.insert(0,'ops'); from make_links import KEYWORDS
P=json.load(open('content/products.json'))
prob=[];used=set();nbtn=0
for f in sorted(glob.glob('content/posts/*.md')):
    t=open(f).read()
    for m in re.finditer(r"<!--\s*products:\s*(.*?)\s*-->",t):
        for k in [x.strip() for x in m.group(1).split(',')]:
            used.add(k)
            if k not in P: prob.append((f,k,'枠が products.json に無い'))
            elif not P[k].get('html'): prob.append((f,k,'リンク空(非表示)'))
            else: nbtn+=1
    if True:
        for u in re.findall(r'https?://[^\s"\)]*(?:moshimo|hb\.afl\.rakuten|item\.rakuten|search\.rakuten)[^\s"\)]*',t): prob.append((f,u[:80],'本文に直書きリンク'))
for k,v in P.items():
    if k=='_help':continue
    h=v.get('html','')
    if h:
        if 'a_id=5877487' not in h: prob.append(('products',k,'a_id違い'))
        m=re.search(r'search/mall/(.*?)/',unquote(unquote(h)))
        kw=m.group(1) if m else None
        if k in KEYWORDS and kw!=KEYWORDS[k]: prob.append(('products',k,f'キーワード不一致 {kw}'))
        if 'sponsored' not in h: prob.append(('products',k,'sponsored無し'))
print('posts',len(glob.glob('content/posts/*.md')),'buttons',nbtn,'keys',len(P)-1,'used',len(used))
print('unused keys',sorted(set(P)-used-{'_help'}))
for p in prob: print(p)
# built pages
for f in sorted(glob.glob('docs/**/*.html',recursive=True)+glob.glob('*.html')):
    t=open(f).read()
    if 'af.moshimo.com' in t and not re.search(r'PR|広告',t): print('PR表記なし',f)
print('OK' if not prob else f'NG {len(prob)}件')
