// IG画像受け渡しキット（ops/sns/ig_upload_kit/inject.md）のテスト
// 実行：node ops/tests/ig_inject.test.js
// inject.md の <!-- code:… --> のコードをそのまま取り出し、ローカルの模擬ページ（IGの新規投稿画面に似せたもの）に流す。
// ネットワークは使わない（page.setContent のみ）。本物のIGには接続しない。
// 追加：2026-11-06 ハエル（事業4）
"use strict";
const fs = require("fs");
const path = require("path");
const assert = require("assert");
const { chromium } = require("playwright");

const KIT = path.join(__dirname, "../sns/ig_upload_kit");
const md = fs.readFileSync(path.join(KIT, "inject.md"), "utf8");
function code(id) {
  const m = md.match(new RegExp("<!-- code:" + id + " -->\\s*```js\\n([\\s\\S]*?)\\n```"));
  if (!m) throw new Error("inject.md に code:" + id + " がない");
  return m[1];
}
const fnv = (u8) => { let h = 0x811c9dc5; for (const b of u8) { h ^= b; h = Math.imul(h, 0x01000193) >>> 0; } return h; };
function load(folder) {
  const man = JSON.parse(fs.readFileSync(path.join(KIT, folder, "manifest.json"), "utf8"));
  return man.files.map((f) => ({
    ...f,
    jpg: fs.readFileSync(path.join(KIT, folder, f.name)),
    parts: Array.from({ length: f.parts }, (_, k) => fs.readFileSync(path.join(KIT, folder, `${f.nn}_part${k + 1}.txt`), "utf8")),
  }));
}
const push = (nn, k, data) => code("push").split("NN").join(nn).split("K").join(String(k)).replace("DATA", () => data);
const append = (nn, k, data) => code("append").split("NN").join(nn).split("K").join(String(k)).replace("DATA", () => data);

// 模擬ページ：「作成」→「投稿」で dialog と input[type=file] が現れる（IGと同じく最初は input が無い）
const MOCK = `<!doctype html><meta charset="utf-8"><body>
<button id="create">作成</button><div id="menu" hidden><button id="post">投稿</button></div>
<pre id="result"></pre>
<script>
const fnv=u8=>{let h=0x811c9dc5;for(const b of u8){h^=b;h=Math.imul(h,0x01000193)>>>0}return h};
async function report(src,files){
  const out=[];
  for(const f of files){
    const buf=new Uint8Array(await f.arrayBuffer());
    const bmp=await createImageBitmap(f);
    out.push({name:f.name,size:f.size,type:f.type,w:bmp.width,h:bmp.height,fnv:fnv(buf)});
  }
  window.__result={src,files:out};
  document.getElementById('result').textContent=JSON.stringify(window.__result);
}
document.getElementById('create').onclick=()=>{document.getElementById('menu').hidden=false};
document.getElementById('post').onclick=()=>{
  const d=document.createElement('div');d.setAttribute('role','dialog');
  d.innerHTML='<h2>新規投稿を作成</h2><div id="zone"><span>写真や動画をここにドラッグ</span></div><button>コンピューターから選択</button>'+
   '<form><input type="file" accept="image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime" multiple style="display:none"></form>';
  document.body.appendChild(d);
  d.querySelector('input').addEventListener('change',e=>report('change',[...e.target.files]));
  const z=d.querySelector('#zone');
  z.addEventListener('dragover',e=>e.preventDefault());
  z.addEventListener('drop',e=>{e.preventDefault();report('drop',[...e.dataTransfer.files])});
};
</script>`;

async function freshPage(browser) {
  const page = await browser.newPage();
  await page.setContent(MOCK);
  return page;
}
async function waitResult(page) {
  await page.waitForFunction(() => window.__result, null, { timeout: 15000 });
  const r = await page.evaluate(() => window.__result);
  await page.evaluate(() => { window.__result = null; });
  return r;
}
function verify(r, files, src) {
  assert.strictEqual(r.src, src);
  assert.strictEqual(r.files.length, files.length, "枚数");
  r.files.forEach((got, i) => {
    const f = files[i];
    assert.strictEqual(got.name, f.nn + ".jpg");
    assert.strictEqual(got.type, "image/jpeg");
    assert.strictEqual(got.size, f.jpg.length, f.nn + " サイズ");
    assert.strictEqual(got.fnv, fnv(f.jpg), f.nn + " 中身（ハッシュ）");
    assert.strictEqual(got.w, 1080); assert.strictEqual(got.h, 1350);
  });
}

(async () => {
  const log = [];
  const ok = (m) => { log.push("PASS " + m); console.log("PASS", m); };
  const browser = await chromium.launch();
  try {
    const mara = load("2026-11-05_marathon");
    const remo = load("2026-11-04_smart-remote");

    // 1) マラソン5枚：input が無い→作成→投稿→チャンク投入→確認→inject
    let page = await freshPage(browser);
    assert.match(await page.evaluate(code("diag")), /input数=0/);
    assert.match(await page.evaluate(code("inject")), /^NG: 01 のチャンクがない/);
    await page.click("#create"); await page.click("#post");
    assert.match(await page.evaluate(code("diag")), /input数=1[\s\S]*multiple=true/);
    assert.match(await page.evaluate(code("deep-find")), /doc accept=image\/jpeg/);
    let calls = 0;
    for (const f of mara) for (const [k, d] of f.parts.entries()) {
      assert.ok(d.length <= 40000);
      const ret = await page.evaluate(push(f.nn, k + 1, d)); calls++;
      assert.strictEqual(ret, `${f.nn} part${k + 1} len=${d.length}`);
    }
    // 同じチャンクを2回流しても壊れない
    await page.evaluate(push("03", 2, mara[2].parts[1]));
    const chk = await page.evaluate(code("check-chunks"));
    assert.strictEqual((chk.match(/part OK \/ 長さ \d+ OK/g) || []).length, 5, chk);
    const inj = await page.evaluate(code("inject"));
    assert.match(inj, /^OK: 5枚を設定/, inj);
    verify(await waitResult(page), mara, "change");
    ok(`マラソン5枚：${calls}回のチャンク投入→change で5枚とも同じバイト・1080×1350でデコード（${inj.slice(0, 60)}…）`);

    // 2) ドロップ方式（(b) 後の __igFiles を再利用）
    const drop = await page.evaluate(code("drop"));
    assert.match(drop, /^drop送信: 5枚/, drop);
    verify(await waitResult(page), mara, "drop");
    ok("ドロップ方式（d）でも5枚が同じバイトで渡る");
    await page.close();

    // 3) 抜け・壊れの検出
    page = await freshPage(browser);
    await page.click("#create"); await page.click("#post");
    for (const f of mara) for (const [k, d] of f.parts.entries()) if (!(f.nn === "04" && k === 2)) await page.evaluate(push(f.nn, k + 1, d));
    assert.match(await page.evaluate(code("check-chunks")), /04: 足りないpart 3/);
    assert.match(await page.evaluate(code("inject")), /^NG: 04 part3 が抜けている/);
    await page.evaluate(push("04", 3, mara[3].parts[2].slice(0, 39999))); // 1文字欠け
    assert.match(await page.evaluate(code("check-chunks")), /04: part OK \/ 長さ \d+ ≠ 173436 NG/);
    ok("partの抜け・1文字欠けを確認コードで検出、injectは送らずNGを返す");
    await page.close();

    // 4) 追記版（1チャンクを2回に分割）＋スマートリモコン1枚
    page = await freshPage(browser);
    await page.click("#create"); await page.click("#post");
    const r = remo[0];
    for (const [k, d] of r.parts.entries()) {
      const h = Math.floor(d.length / 2);
      await page.evaluate(append("01", k + 1, d.slice(0, h)));
      assert.strictEqual(await page.evaluate(append("01", k + 1, d.slice(h))), `01 part${k + 1} len=${d.length}`);
    }
    const chk2 = await page.evaluate(code("check-chunks").replace(/const E=\{[^}]*\}/, "const E={'01':[6,200972]}"));
    assert.match(chk2, /^01: part OK \/ 長さ 200972 OK$/, chk2);
    const inj2 = await page.evaluate(code("inject").replace("const ORDER=['01','02','03','04','05']", "const ORDER=['01']"));
    assert.match(inj2, /^OK: 1枚を設定/, inj2);
    verify(await waitResult(page), remo, "change");
    ok("スマートリモコン1枚：追記版（半分ずつ12回）→change で同じバイト・1080×1350");
    await page.close();

    // 5) 加湿器・暖房（各5枚）：manifest から E と ORDER を作り、チャンク投入→確認→inject→デコード確認
    for (const folder of ["2026-11-05_kashitsu", "2026-11-06_heater"]) {
      const fs5 = load(folder);
      page = await freshPage(browser);
      await page.click("#create"); await page.click("#post");
      let n = 0;
      for (const f of fs5) {
        assert.strictEqual(f.parts.join("").length, f.b64_len, folder + "/" + f.nn + " b64長");
        assert.strictEqual(Buffer.from(f.parts.join(""), "base64").equals(f.jpg), true, folder + "/" + f.nn + " base64→jpg一致");
        for (const [k, d] of f.parts.entries()) {
          assert.ok(d.length <= 40000);
          assert.strictEqual(await page.evaluate(push(f.nn, k + 1, d)), `${f.nn} part${k + 1} len=${d.length}`); n++;
        }
      }
      const E = "const E={" + fs5.map((f) => `'${f.nn}':[${f.parts.length},${f.b64_len}]`).join(",") + "}";
      const c = await page.evaluate(code("check-chunks").replace(/const E=\{[^}]*\}/, () => E));
      assert.strictEqual((c.match(/part OK \/ 長さ \d+ OK/g) || []).length, fs5.length, c);
      const ORDER = "const ORDER=[" + fs5.map((f) => `'${f.nn}'`).join(",") + "]";
      const inj5 = await page.evaluate(code("inject").replace("const ORDER=['01','02','03','04','05']", () => ORDER));
      assert.match(inj5, new RegExp("^OK: " + fs5.length + "枚を設定"), inj5);
      verify(await waitResult(page), fs5, "change");
      ok(`${folder} ${fs5.length}枚：${n}回のチャンク投入→change で同じバイト・1080×1350でデコード`);
      await page.close();
    }
  } finally {
    await browser.close();
  }
  console.log(`\nALL PASS (${log.length})`);
})().catch((e) => { console.error("FAIL", e); process.exit(1); });
