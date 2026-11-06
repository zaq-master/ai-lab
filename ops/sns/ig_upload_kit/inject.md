# IG 画像受け渡しキット（ネットワーク不使用）

作成：2026-11-06 ハエル（事業4）。
目的：IGの新規投稿画面に、内蔵ブラウザから画像を渡す。ファイル添付の道具がなく、IGはCSPで外部画像を読み込めない（2026-11-06 08:02に未投稿）。
方法：画像のbase64をJSに直接書き込む → Blob/File → DataTransfer → IGの `input[type=file]` に設定 → `input`/`change` イベントを送る。ネットワークは使わない。
（2026-11-02 08:05にタブ内canvas→DataTransferで渡せた実績あり：ops/log/2026-11-02.md）

※このフォルダは公開しない（docs/ には置かない）。投稿・ログインはこのキットの範囲外。

## 中身

| フォルダ | 枚数 | チャンク | base64合計 | 期限 |
|---|---|---|---|---|
| `2026-11-05_marathon/` | 5枚（01〜05） | 各5個（part1〜5） | 910,452文字 | 楽天の期間 11/11 01:59まで（投稿は11/10までに） |
| `2026-11-04_smart-remote/` | 1枚（01） | 6個（part1〜6） | 200,972文字 | なし |
| `2026-11-05_kashitsu/` | 5枚（01〜05） | 4/5/5/6/5個 | 876,192文字 | なし |
| `2026-11-06_heater/` | 5枚（01〜05） | 4/5/4/5/5個 | 849,048文字 | なし |

### JS実行の回数一覧（(a) で1チャンク＝1回。これに (a2) 確認1回＋(b) 設定1回を足す）

| フォルダ | 画像ごとのチャンク数（01〜05） | チャンク合計＝(a)の回数 | base64合計文字数 | 全体の回数（＋確認＋設定） | (a2) に入れる `E` |
|---|---|---|---|---|---|
| `2026-11-05_marathon` | 5/5/5/5/5 | **25回** | 910,452 | 27回 | `{'01':[5,168220],'02':[5,173816],'03':[5,197392],'04':[5,173436],'05':[5,197588]}` |
| `2026-11-04_smart-remote` | 6 | **6回** | 200,972 | 8回 | `{'01':[6,200972]}` |
| `2026-11-05_kashitsu` | 4/5/5/6/5 | **25回** | 876,192 | 27回 | `{'01':[4,154004],'02':[5,163376],'03':[5,164880],'04':[6,203636],'05':[5,190296]}` |
| `2026-11-06_heater` | 4/5/4/5/5 | **23回** | 849,048 | 25回 | `{'01':[4,154128],'02':[5,166004],'03':[4,154620],'04':[5,195976],'05':[5,178320]}` |

- (a2) の `const E={...}` を、そのフォルダの行の `E` に置き換えてから実行する。5枚のフォルダは (b) の `ORDER` はそのまま（`['01','02','03','04','05']`）
- **別のフォルダを続けて入れるときは、先に `window.__ig={}` を実行して前のフォルダのチャンクを消す**（同じ番号 '01' などが混ざるため）

- 各フォルダ：`NN.jpg`（1080×1350 JPEG、約113〜149KB、文字が読めることを確認済み）、`NN_partK.txt`（base64、1個40,000文字以下）、`manifest.json`（品質・バイト数・チャンク数）
- 作り直し：`python3 ops/sns/ig_upload_kit/make_kit.py docs/sns/ig/<フォルダ>`
- 注意（量）：マラソン5枚＝約91万文字をJS実行ツールに渡すことになる。1回40,000文字以下×25回（スマートリモコンは6回）。時間がかかるので、PC回の最初にやる。1回のツール呼び出しで長すぎて失敗したら、そのチャンクを半分に分けて「(a') 追記版」で2回に分けて送る

---

## (a) チャンクを1個ずつ流す（1チャンク＝1回のJS実行）

`NN`＝画像番号（'01'など）、`K`＝partの番号、`DATA`＝`NN_partK.txt` の中身そのまま（改行なし）。
**partの番号から1を引いた位置**に入れる（同じものを2回流しても重複しない）。

<!-- code:push -->
```js
window.__ig=window.__ig||{};(__ig['NN']=__ig['NN']||[])[K-1]='DATA';'NN part'+K+' len='+__ig['NN'][K-1].length
```

例：`01_part1.txt` → `...(__ig['01']=__ig['01']||[])[1-1]='/9j/4AAQ...';'01 part'+1+' len='+...`
返り値が `len=40000`（最後のpartは端数）になればOK。

### (a') 長すぎて失敗したときの追記版（1チャンクを2回以上に分ける）

<!-- code:append -->
```js
window.__ig=window.__ig||{};(__ig['NN']=__ig['NN']||[]);__ig['NN'][K-1]=(__ig['NN'][K-1]||'')+'DATA';'NN part'+K+' len='+__ig['NN'][K-1].length
```
- 前半→後半の順に流す。途中でやり直すときは先に `__ig['NN'][K-1]=''` を実行して空にする

### (a2) 全部そろったかの確認（貼り付け漏れチェック）

<!-- code:check-chunks -->
```js
(()=>{const E={'01':[5,168220],'02':[5,173816],'03':[5,197392],'04':[5,173436],'05':[5,197588]};const ig=window.__ig||{};return Object.keys(E).map(nn=>{const p=ig[nn]||[];let miss=[];for(let k=0;k<E[nn][0];k++)if(typeof p[k]!=='string'||!p[k].length)miss.push(k+1);const len=p.join('').length;return nn+': '+(miss.length?'足りないpart '+miss.join(','):'part OK')+' / 長さ '+len+(len===E[nn][1]?' OK':' ≠ '+E[nn][1]+' NG')}).join('\n')})()
```
- スマートリモコン（1枚）のときは `E={'01':[6,200972]}` に置き換える
- 全行が「part OK / 長さ … OK」になるまで、足りないpartを (a) で流し直す

---

## (b) 結合 → File → DataTransfer → IGの input に設定

IGで「作成」→「投稿」（または「新規投稿」）を押し、「新規投稿を作成」の画面（「コンピューターから選択」ボタンがある画面）を出してから実行する。
**「コンピューターから選択」ボタンは押さない**（OSのファイル選択ダイアログが開いて操作できなくなるため）。

<!-- code:inject -->
```js
(()=>{
const ORDER=['01','02','03','04','05']; // スマートリモコンは ['01']
const ig=window.__ig||{}; const files=[];
for(const nn of ORDER){
  const p=ig[nn]; if(!p||!p.length) return 'NG: '+nn+' のチャンクがない';
  for(let k=0;k<p.length;k++) if(typeof p[k]!=='string') return 'NG: '+nn+' part'+(k+1)+' が抜けている';
  let bin; try{ bin=atob(p.join('')); }catch(e){ return 'NG: '+nn+' のbase64が壊れている（貼り付けミス）: '+e.message; }
  const u8=new Uint8Array(bin.length); for(let i=0;i<bin.length;i++) u8[i]=bin.charCodeAt(i);
  if(u8[0]!==0xFF||u8[1]!==0xD8||u8[u8.length-2]!==0xFF||u8[u8.length-1]!==0xD9) return 'NG: '+nn+' がJPEGとして不完全';
  files.push(new File([new Blob([u8],{type:'image/jpeg'})], nn+'.jpg', {type:'image/jpeg', lastModified:Date.now()}));
}
window.__igFiles=files;
const all=[...document.querySelectorAll('input[type=file]')];
const ok=all.filter(i=>!i.disabled&&(!i.accept||/image|jpe?g|\*/i.test(i.accept)));
const input=ok.find(i=>i.closest('[role=dialog]'))||ok[0];
if(!input) return 'NG: input[type=file] が見つからない（数='+all.length+'）→ (c) で確認';
const dt=new DataTransfer(); files.forEach(f=>dt.items.add(f));
input.files=dt.files;
input.dispatchEvent(new Event('input',{bubbles:true}));
input.dispatchEvent(new Event('change',{bubbles:true}));
return 'OK: '+input.files.length+'枚を設定（'+files.map(f=>f.name+' '+f.size+'B').join(', ')+'） multiple='+input.multiple+' accept='+(input.accept||'(なし)')+(files.length>1&&!input.multiple?' ※multipleなし：1枚目だけになる可能性':'');
})()
```

- 実行後、ページの文字（get_page_text 等）で「切り取り」「次へ」が出ていれば画像が渡っている。5枚がサムネイル列に並んでいるか確認する
- 1枚しか入らなかったら：IGの画面左下の「複数を選択」（重なった四角のアイコン）→「＋」を押してから、同じ手順を2枚目以降だけでやる（`ORDER` を `['02','03','04','05']` に変えて再実行）

---

## (c) 失敗したときの確認・探し方

### (c1) input の数・accept・multiple を見る

<!-- code:diag -->
```js
(()=>{const a=[...document.querySelectorAll('input[type=file]')];return 'input数='+a.length+'\n'+a.map((i,n)=>n+': accept='+(i.accept||'(なし)')+' multiple='+i.multiple+' disabled='+i.disabled+' 画面内dialog='+!!i.closest('[role=dialog]')+' 今のファイル数='+(i.files?i.files.length:0)).join('\n')+'\n__ig='+Object.keys(window.__ig||{}).join(',')+' __igFiles='+((window.__igFiles||[]).length)})()
```

### (c2) 見つからないとき（input数=0）

IGは「新規投稿を作成」画面を開くまで input を作らないことがある。
1. 左のメニュー（または上部）の **「作成」**（＋アイコン）を押す
2. 出てきたメニューの **「投稿」**（画面により「新規投稿」）を押す
3. 「新規投稿を作成」「写真や動画をここにドラッグ」「コンピューターから選択」が出たら、**ボタンは押さずに** (c1) をもう一度実行
4. それでも0なら、shadow DOM や iframe の中を探す：

<!-- code:deep-find -->
```js
(()=>{const out=[];const walk=(root,path)=>{root.querySelectorAll('*').forEach(el=>{if(el.tagName==='INPUT'&&el.type==='file')out.push(path+' accept='+(el.accept||'')+' multiple='+el.multiple);if(el.shadowRoot)walk(el.shadowRoot,path+'>shadow');if(el.tagName==='IFRAME'){try{walk(el.contentDocument,path+'>iframe')}catch(e){out.push(path+'>iframe(読めない)')}}})};walk(document,'doc');return out.length?out.join('\n'):'どこにも無い'})()
```

### (d) input に入れても反応しないとき：ドラッグ＆ドロップで渡す

「写真や動画をここにドラッグ」の枠に、ドロップイベントで同じファイルを渡す（(b) の後なら `window.__igFiles` が残っている）。

<!-- code:drop -->
```js
(()=>{const files=window.__igFiles||[];if(!files.length)return 'NG: 先に (b) を実行して __igFiles を作る';
const dlg=document.querySelector('[role=dialog]')||document.body;
const zone=[...dlg.querySelectorAll('div,section,form')].reverse().find(el=>/ドラッグ|drag/i.test(el.textContent||''))||dlg;
const dt=new DataTransfer();files.forEach(f=>dt.items.add(f));
for(const t of ['dragenter','dragover','drop']) zone.dispatchEvent(new DragEvent(t,{bubbles:true,cancelable:true,dataTransfer:dt}));
return 'drop送信: '+files.length+'枚 → '+zone.tagName+' 「'+(zone.textContent||'').slice(0,30)+'」'})()
```

止まったら：そこで見送り、Slackに「(b)/(c)/(d) のどこで、返り値は何だったか」を書く（runbook の分岐B）。

---

## テスト結果（本物のIGには接続していない）

テスト：`node ops/tests/ig_inject.test.js`（Playwright＋ローカルChromium、ネットワーク不使用。このファイルの `<!-- code:… -->` のコードをそのまま取り出して、模擬ページに流す）

<!-- test-result -->
2026-11-06 実行：**ALL PASS（6項目）**（加湿器・暖房の2フォルダを追加）
- PASS マラソン5枚：最初は input 数0 → 「作成」→「投稿」後に1個（multiple=true）を発見 → 25回のチャンク投入 → check-chunks 全OK → inject「OK: 5枚を設定」→ change で受け取った5枚が元のJPEGと同じバイト数・同じハッシュ、1080×1350でデコードできた
- PASS ドロップ方式（d）：同じ5枚が drop イベントで同じバイトのまま渡った
- PASS 抜け・壊れ検出：part抜け・1文字欠けを check-chunks が検出し、inject は送らずNGを返した
- PASS スマートリモコン1枚：追記版（1チャンクを半分ずつ、計12回）→ 1枚が同じバイト・1080×1350で渡った
- PASS 加湿器5枚：25回のチャンク投入→ base64が元JPEGと一致 → change で5枚とも同じバイト・1080×1350でデコード
- PASS 暖房5枚：23回のチャンク投入→ 同上
- 未確認（本物のIGでしか分からないこと）：IGの画面が `input.files` の差し替えに反応するか、IGの input に multiple があるか、JS実行ツールが1回40,000文字を受け付けるか
