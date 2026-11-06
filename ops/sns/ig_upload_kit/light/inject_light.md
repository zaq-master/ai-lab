# IG 受け渡しキット「軽い版」（試作・ネットワーク不使用）

作成：2026-11-06 ハエル（事業4）。きっかけ：監査 ops/audit/2026-11-06_1000_r2_kansa.md「マラソン5枚のbase64（約91万文字）はPC回1回に収まらない」🔴。
方法：画像そのものではなく、**スライドのHTML/CSS＋使う文字だけのフォント（woff2）**を送り、IGのタブの中で
SVG（foreignObject）→ data: URL → Image → canvas(1080×1350) → JPEG → File → DataTransfer → `input[type=file]` に渡す。
※このフォルダは公開しない（docs/ に置かない）。ログイン・投稿はこのキットの範囲外。

## 中身と文字数（マラソン5枚）

| 項目 | 値 |
|---|---|
| フォルダ | `2026-11-05_marathon/`（part1〜4.txt、payload.json、manifest.json） |
| チャンク | **4個**（38,074 / 38,072 / 38,072 / 28,769 文字＝そのまま貼るJS） |
| 注入する文字数の合計 | **142,987文字**（チャンク4個）＋ 確認744＋組み立て2,184文字 ＝ **145,915文字**（現行 910,452文字の約16%） |
| JS実行の回数 | 4（チャンク）＋1（確認）＋1（組み立て）＋（必要なら1：結果読み出し）＝**6〜7回**（現行27回） |
| フォント | Noto Sans CJK JP（OFL）Regular/Bold/Black を、スライドで使う **253文字** だけに切り出し（各 約4.4万文字のbase64） |
| 元画像との違い | 右下の絵文字「🤖」だけ、同じ大きさの自作ロボット図形に置き換え（端末で絵柄が変わるため）。文言「AI運営アカウント」・注意書き・内容は同じ |

作り直し：`python3 ops/sns/ig_upload_kit/light/make_light.py media/instagram/2026-11-05_marathon`（作り直すたびにフォントのバイト列が少し変わりハッシュも変わる。(2) の `E` はスクリプトが自動で書き換える。**作り直したら part1〜4 と E を必ずセットで使う**）

## 全投稿の一覧（2026-11-06 追加）

注入する文字数＝チャンク（partK.txt）の合計＋確認コード＋組み立てコード（2,184）。JS実行回数＝チャンク数＋確認1＋組み立て1（＋必要なら読み出し1）。

| フォルダ | 枚数 | 合計文字数 | JS実行回数 | 重い版（base64）の文字数 | 採否 |
|---|---|---|---|---|---|
| `2026-11-05_marathon` | 5 | **145,915**（part×4） | **6〜7回** | 910,452 | ✅ 採用（11-06 前ラウンド。作り直していない） |
| `2026-11-04_smart-remote` | 1 | **93,289**（part×3） | **5〜6回** | 200,972 | ✅ 採用 |
| `2026-11-05_kashitsu` | 5 | **177,694**（part×5） | **7〜8回** | 876,192 | ✅ 採用 |
| `2026-11-06_heater` | 5 | **167,501**（part×5） | **7〜8回** | 849,048 | ✅ 採用 |

- 元：kashitsu・heater は `media/instagram/<フォルダ>/render.py`、スマートリモコンは `docs/sns/2026-11-04-smart-remote-count.src.html`（1枚ものHTML。make_light.py がHTMLファイルも読めるよう汎用化）
- 3フォルダとも絵文字なし → 置き換えなし（文言・注意書き・AI表示は元のまま）
- 3フォルダは約物の詰め（halt/chws）をフォントに残す設定で作成。これがないと「）。」「）・」の間が広がり、kashitsu 05 で違う画素 0.43% → 入れて 0.004% に（改行位置は入れる前から同じ）
- 不採用（重い版を使う）のフォルダ：なし

## 手順

1. IGで「作成」→「投稿」を押し、「新規投稿を作成」（「コンピューターから選択」がある画面）を出す。**ボタンは押さない**
2. `part1.txt`〜`part4.txt` の中身を、**そのまま1個ずつ**JS実行ツールに貼って実行（4回）。返り値 `partK/4 len=…` を確認
3. (2) 確認コードを実行 → 全部「OK」になるまで、NGのpartだけ流し直す
4. (3) 組み立てコードを実行 → `OK: 5枚を設定`（スマートリモコンは1枚） なら、ページの文字で「切り取り」「次へ」と5枚のサムネを確認
   - 返り値が `[object Promise]` や空だったら、(4) 読み出しコードを実行して結果を見る
5. うまくいかなければ既存の inject.md（監査済みのbase64方式）の手順へ戻る

## (2) 確認コード（貼り漏れ・中身のずれを SHA-256 で検出）

<!-- code:check -->
```js
(async()=>{const E=[[38000,"ba90f8d956a5cda3"],[38000,"0b238e5b250012e8"],[38000,"edf6aa650402caf6"],[28118,"4fbcc002c14c6f3a"]];const p=window.__igl||[];const out=[];let ok=true;for(let k=0;k<E.length;k++){const s=p[k];if(typeof s!=='string'){out.push('part'+(k+1)+': ない NG');ok=false;continue}const h=[...new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s)))].map(b=>b.toString(16).padStart(2,'0')).join('').slice(0,16);const g=s.length===E[k][0]&&h===E[k][1];if(!g)ok=false;out.push('part'+(k+1)+': 長さ '+s.length+' ハッシュ '+h+(g?' OK':' NG（期待 '+E[k][0]+' '+E[k][1]+'）'))}if(p.length>E.length){out.push('余分なpartあり：window.__igl=[] から流し直す');ok=false}window.__iglOK=ok;return (ok?'ALL OK\n':'NGあり\n')+out.join('\n')})()
```

## (2') 確認コード：ほかの投稿（2026-11-06 追加）

手順は上と同じ。(2) の確認コードだけ、下のフォルダ用に差し替える（(3) 組み立て・(4) 読み出しは全フォルダ共通）。
- **同じタブで別の投稿に切り替えるときは、最初に `window.__igl=[];window.__iglOK=false` を実行**して前の中身を消す（消し忘れは確認コードが「余分なpartあり」「NG」で止める）
- 作り直し：`python3 ops/sns/ig_upload_kit/light/make_light.py media/instagram/<フォルダ>`（スマートリモコンは `docs/sns/2026-11-04-smart-remote-count.src.html 2026-11-04_smart-remote`）。下の `E` は自動で書き換わる

### 2026-11-04_smart-remote（part1〜3）

<!-- code:check:2026-11-04_smart-remote -->
```js
(async()=>{const E=[[38000,"e70c6d742af09189"],[38000,"3917e34b2daadd0e"],[14136,"c4b5dde29ab3f39e"]];const p=window.__igl||[];const out=[];let ok=true;for(let k=0;k<E.length;k++){const s=p[k];if(typeof s!=='string'){out.push('part'+(k+1)+': ない NG');ok=false;continue}const h=[...new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s)))].map(b=>b.toString(16).padStart(2,'0')).join('').slice(0,16);const g=s.length===E[k][0]&&h===E[k][1];if(!g)ok=false;out.push('part'+(k+1)+': 長さ '+s.length+' ハッシュ '+h+(g?' OK':' NG（期待 '+E[k][0]+' '+E[k][1]+'）'))}if(p.length>E.length){out.push('余分なpartあり：window.__igl=[] から流し直す');ok=false}window.__iglOK=ok;return (ok?'ALL OK\n':'NGあり\n')+out.join('\n')})()
```

### 2026-11-05_kashitsu（part1〜5）

<!-- code:check:2026-11-05_kashitsu -->
```js
(async()=>{const E=[[38000,"b0c47d066add4432"],[38000,"aedb142fef2eb511"],[38000,"ad31e2e64a4049aa"],[38000,"86727af0135a8fce"],[22105,"69bc56d6a376b0ae"]];const p=window.__igl||[];const out=[];let ok=true;for(let k=0;k<E.length;k++){const s=p[k];if(typeof s!=='string'){out.push('part'+(k+1)+': ない NG');ok=false;continue}const h=[...new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s)))].map(b=>b.toString(16).padStart(2,'0')).join('').slice(0,16);const g=s.length===E[k][0]&&h===E[k][1];if(!g)ok=false;out.push('part'+(k+1)+': 長さ '+s.length+' ハッシュ '+h+(g?' OK':' NG（期待 '+E[k][0]+' '+E[k][1]+'）'))}if(p.length>E.length){out.push('余分なpartあり：window.__igl=[] から流し直す');ok=false}window.__iglOK=ok;return (ok?'ALL OK\n':'NGあり\n')+out.join('\n')})()
```

### 2026-11-06_heater（part1〜5）

<!-- code:check:2026-11-06_heater -->
```js
(async()=>{const E=[[38000,"af8ccc39604556f1"],[38000,"edaf8768dfa6c88d"],[38000,"a3d7d99b0dcece41"],[38000,"dd8015ef344f1b13"],[11912,"7a74a88c60dca0e8"]];const p=window.__igl||[];const out=[];let ok=true;for(let k=0;k<E.length;k++){const s=p[k];if(typeof s!=='string'){out.push('part'+(k+1)+': ない NG');ok=false;continue}const h=[...new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s)))].map(b=>b.toString(16).padStart(2,'0')).join('').slice(0,16);const g=s.length===E[k][0]&&h===E[k][1];if(!g)ok=false;out.push('part'+(k+1)+': 長さ '+s.length+' ハッシュ '+h+(g?' OK':' NG（期待 '+E[k][0]+' '+E[k][1]+'）'))}if(p.length>E.length){out.push('余分なpartあり：window.__igl=[] から流し直す');ok=false}window.__iglOK=ok;return (ok?'ALL OK\n':'NGあり\n')+out.join('\n')})()
```

## (3) 組み立て → JPEG 5枚 → input に設定

<!-- code:build -->
```js
(async()=>{const R=m=>(window.__iglResult=m);try{
if(!window.__iglOK)return R('NG: 先に (2) 確認コードで ALL OK にする');
const P=JSON.parse((window.__igl||[]).join(''));
const ff=Object.entries(P.fonts).map(([w,b])=>"@font-face{font-family:'AliceSub';font-weight:"+w+";src:url(data:font/woff2;base64,"+b+") format('woff2')}").join('');
const files=[];
for(let i=0;i<P.slides.length;i++){
 const svg='<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350"><foreignObject x="0" y="0" width="1080" height="1350"><div xmlns="http://www.w3.org/1999/xhtml" class="b"><style>'+ff+P.css+'</style>'+P.slides[i]+'</div></foreignObject></svg>';
 const img=new Image();img.decoding='sync';
 await new Promise((ok,ng)=>{img.onload=ok;img.onerror=()=>ng(new Error('SVGの読み込み失敗（CSPのimg-srcでdata:が禁止の可能性）'));img.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svg)});
 try{await img.decode()}catch(e){}
 await new Promise(r=>setTimeout(r,150));
 const c=document.createElement('canvas');c.width=1080;c.height=1350;const x=c.getContext('2d');
 x.fillStyle='#0f1c3f';x.fillRect(0,0,1080,1350);x.drawImage(img,0,0,1080,1350);
 const blob=await new Promise((ok,ng)=>{try{c.toBlob(b=>b?ok(b):ng(new Error('toBlobが空')),'image/jpeg',0.92)}catch(e){ng(e)}});
 const nn=String(i+1).padStart(2,'0');
 files.push(new File([blob],nn+'.jpg',{type:'image/jpeg',lastModified:Date.now()}));
}
window.__igFiles=files;
const all=[...document.querySelectorAll('input[type=file]')];
const okI=all.filter(i=>!i.disabled&&(!i.accept||/image|jpe?g|\*/i.test(i.accept)));
const input=okI.find(i=>i.closest('[role=dialog]'))||okI[0];
if(!input)return R('NG: input[type=file] が見つからない（数='+all.length+'）→ inject.md の (c)。画像は window.__igFiles に '+files.length+'枚できている');
const dt=new DataTransfer();files.forEach(f=>dt.items.add(f));input.files=dt.files;
input.dispatchEvent(new Event('input',{bubbles:true}));input.dispatchEvent(new Event('change',{bubbles:true}));
return R('OK: '+input.files.length+'枚を設定（'+files.map(f=>f.name+' '+f.size+'B').join(', ')+'） multiple='+input.multiple);
}catch(e){return R('NG: '+e.name+': '+e.message+(e.name==='SecurityError'?'（canvasが汚染扱い＝この方式はこのブラウザでは不可 → inject.md へ）':''))}})()
```

- 入らなかったときのドラッグ＆ドロップ版は inject.md の (d)（`window.__igFiles` をそのまま使える）

## (4) 結果の読み出し（ツールが Promise の結果を返さないとき）

<!-- code:result -->
```js
String(window.__iglResult)
```

## テスト結果（本物のIGには接続していない）

テスト：`node ops/tests/ig_inject_light.test.js`（Playwright＋ローカルChromium。ページは page.route で作った https の模擬ページで、ネットワークは使わない）

<!-- test-result -->
2026-11-06 実行：**ALL PASS（7項目）**
- 模擬ページのCSP：`default-src 'none'; connect-src 'none'; img-src blob: data:; font-src 'none'; …; script-src 'unsafe-inline'`。CSP違反 0件、模擬ページ以外への通信 0件
- 5枚とも 1080×1350 の JPEG（141〜192KB）として `input[type=file] multiple` の change に届いた。canvas の汚染エラー（SecurityError）なし
- 確認コード：part2 を1文字変えると「part2 NG」、part4 を流さないと「part4: ない NG」。NGのときは組み立てが止まる
- 元画像との差（右下のAI表示の所を除く）：平均差 0.88〜1.24（0〜255）、大きく違う画素 0.002〜0.004%
- 目視（Read）：01・03 を元画像と並べて確認。文字の欠け・はみ出し・改行位置のずれなし。違いは右下の🤖→ロボット図形のみ。全5枚は `2026-11-05_marathon/preview/` に保存
- 対照実験：フォントを抜いて組み立てると数字・英字が明朝体に変わる（＝埋め込みフォントが実際に使われていることを確認）

2026-11-06 追加（全4フォルダに拡張）：`node ops/tests/ig_inject_light.test.js` → **ALL PASS（25項目＝6項目×4フォルダ＋通信0件）**
- smart-remote 1枚・kashitsu 5枚・heater 5枚とも 1080×1350 JPEG で input の change に届いた。CSP違反 0件
- 元画像との差：smart-remote 平均 1.46／違う画素 0.001%、kashitsu 0.85〜1.33／0.002〜0.055%、heater 1.01〜1.43／0.002〜0.030%（3フォルダは右下も除外せず全面で比較）
- 目視（Read、元と並べて）：smart-remote 01、kashitsu 03・04・05、heater 04。文字の欠け・はみ出し・改行位置のずれなし。全枚は各フォルダの `preview/`

## 未確認事項

- 本物のIGのCSPで `img-src` に `data:` が許されているか（模擬ページは `img-src blob: data:` で検証）。禁止なら (3) が「SVGの読み込み失敗」で止まる → 既存 inject.md へ
- 内蔵ブラウザ（Claudeデスクトップ）のJS実行ツールが async の結果を返すか → 返さなければ (4)
- 1回の貼り付け 約3.8万文字が内蔵ブラウザのツールで通るか（既存キットの4万字と同じ水準）
- テストはこのサーバーのChromium（Linux）。オーナーPCのChromium系で同じ見た目になるかは未確認（フォントは埋め込みなので端末のフォントには依存しない設計）
