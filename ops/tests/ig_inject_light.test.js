// IG受け渡しキット「軽い版」（ops/sns/ig_upload_kit/light/inject_light.md）のテスト
// 実行：node ops/tests/ig_inject_light.test.js
// inject_light.md の <!-- code:… --> と part*.txt をそのまま、IGに近い厳しいCSPの模擬ページ（https://mock.ig.test/、page.route で作る）に流す。
// ネットワークは使わない（模擬ページ以外のリクエストは全部止めて数える）。本物のIGには接続しない。
// 追加：2026-11-06 ハエル（事業4）
"use strict";
const fs = require("fs");
const path = require("path");
const assert = require("assert");
const { chromium } = require("playwright");

const LIGHT = path.join(__dirname, "../sns/ig_upload_kit/light");
// 全フォルダ（2026-11-06 拡張）。aiMask=右下のAI表示（🤖を図形に置き換えた所）を差の計算から外すか
const FOLDERS = [
  { name: "2026-11-05_marathon", check: "check", aiMask: true },
  { name: "2026-11-04_smart-remote", check: "check:2026-11-04_smart-remote", aiMask: false },
  { name: "2026-11-05_kashitsu", check: "check:2026-11-05_kashitsu", aiMask: false },
  { name: "2026-11-06_heater", check: "check:2026-11-06_heater", aiMask: false },
];
const md = fs.readFileSync(path.join(LIGHT, "inject_light.md"), "utf8");
const code = (id) => {
  const m = md.match(new RegExp("<!-- code:" + id + " -->\\s*```js\\n([\\s\\S]*?)\\n```"));
  if (!m) throw new Error("inject_light.md に code:" + id + " がない");
  return m[1];
};

const CSP = "default-src 'none'; connect-src 'none'; img-src blob: data:; font-src 'none'; media-src 'none'; frame-src 'none'; worker-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'";
const MOCK = `<!doctype html><meta charset="utf-8"><body>
<button id="create">作成</button><div id="menu" hidden><button id="post">投稿</button></div>
<script>
window.__csp=[];document.addEventListener('securitypolicyviolation',e=>window.__csp.push(e.violatedDirective+' '+e.blockedURI.slice(0,40)));
async function report(src,files){const out=[];for(const f of files){const buf=new Uint8Array(await f.arrayBuffer());const bmp=await createImageBitmap(f);
 out.push({name:f.name,size:f.size,type:f.type,w:bmp.width,h:bmp.height,soi:buf[0]===0xFF&&buf[1]===0xD8,b64:btoa(Array.from(buf,c=>String.fromCharCode(c)).join(''))})}
 window.__result={src,files:out}}
document.getElementById('create').onclick=()=>{document.getElementById('menu').hidden=false};
document.getElementById('post').onclick=()=>{const d=document.createElement('div');d.setAttribute('role','dialog');
 d.innerHTML='<h2>新規投稿を作成</h2><button>コンピューターから選択</button><form><input type="file" accept="image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime" multiple style="display:none"></form>';
 document.body.appendChild(d);d.querySelector('input').addEventListener('change',e=>report('change',[...e.target.files]))};
</script>`;

const results = [];
async function t(name, fn) {
  try { await fn(); results.push("PASS " + name); } catch (e) { results.push("FAIL " + name + " : " + e.message); }
}

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext();
  let external = [];
  await ctx.route("**/*", (r) => {
    const u = r.request().url();
    if (u === "https://mock.ig.test/") return r.fulfill({ status: 200, headers: { "content-type": "text/html; charset=utf-8", "content-security-policy": CSP }, body: MOCK });
    external.push(u); return r.abort();
  });
  const open = async () => {
    const page = await ctx.newPage();
    await page.goto("https://mock.ig.test/");
    await page.click("#create"); await page.click("#post");
    return page;
  };

  for (const F of FOLDERS) {
  const man = JSON.parse(fs.readFileSync(path.join(LIGHT, F.name, "manifest.json"), "utf8"));
  const parts = man.parts.map((p) => fs.readFileSync(path.join(LIGHT, F.name, `part${p.k}.txt`), "utf8"));
  const nS = JSON.parse(fs.readFileSync(path.join(LIGHT, F.name, "payload.json"), "utf8")).slides.length;
  const ORIG = path.join(__dirname, "../../docs/sns/ig", F.name);
  const PREVIEW = path.join(LIGHT, F.name, "preview");
  await t(F.name + " md の E が manifest.json と一致", async () => {
    const m = code(F.check).match(/const E=(\[\[.*?\]\]);/);
    assert.deepStrictEqual(JSON.parse(m[1]), man.E);
  });

  await t(F.name + " 注入文字数が20万文字以下", async () => {
    const total = parts.reduce((a, s) => a + s.length, 0) + code(F.check).length + code("build").length;
    console.log("注入合計 =", total, "文字（チャンク", parts.map((s) => s.length).join("/"), "＋確認", code(F.check).length, "＋組立", code("build").length, "）");
    assert.ok(total <= 200000, String(total));
    parts.forEach((s) => assert.ok(s.length <= 40000, "1チャンク40,000以下"));
  });

  let got;
  await t(F.name + " 厳しいCSPの模擬ページで全枚数が1080×1350のJPEGとして input に渡る", async () => {
    const page = await open();
    for (const [k, s] of parts.entries()) {
      const r = await page.evaluate(s);
      assert.ok(r.startsWith(`part${k + 1}/${parts.length} len=`), r);
    }
    const c = await page.evaluate(code(F.check));
    assert.ok(c.startsWith("ALL OK"), c);
    const b = await page.evaluate(code("build"));
    console.log("組立の返り値:", b);
    assert.ok(b.startsWith(`OK: ${nS}枚`), b);
    assert.strictEqual(await page.evaluate(code("result")), b);
    await page.waitForFunction(() => window.__result, null, { timeout: 15000 });
    got = await page.evaluate(() => window.__result);
    assert.strictEqual(got.src, "change");
    assert.strictEqual(got.files.length, nS);
    got.files.forEach((f, i) => {
      assert.strictEqual(f.name, String(i + 1).padStart(2, "0") + ".jpg");
      assert.strictEqual(f.type, "image/jpeg"); assert.ok(f.soi, "JPEGの先頭");
      assert.strictEqual(f.w, 1080); assert.strictEqual(f.h, 1350);
    });
    const csp = await page.evaluate(() => window.__csp);
    console.log("CSP違反:", csp.length ? csp.join(" | ") : "なし");
    fs.mkdirSync(PREVIEW, { recursive: true });
    got.files.forEach((f) => fs.writeFileSync(path.join(PREVIEW, f.name), Buffer.from(f.b64, "base64")));
    await page.close();
  });

  await t(F.name + " チャンクの中身が1文字ずれたら確認コードがNGを出し、組立も止まる", async () => {
    const page = await open();
    for (const [k, s] of parts.entries()) {
      const bad = k === 1 ? s.replace(/(__igl\[1\]=')(.)/, (m, a, ch) => a + (ch === "A" ? "B" : "A")) : s;
      assert.notStrictEqual(k === 1 ? bad : s, k === 1 ? s : null);
      await page.evaluate(bad);
    }
    const c = await page.evaluate(code(F.check));
    assert.ok(c.startsWith("NGあり") && /part2: .* NG/.test(c) && /part1: .* OK/.test(c), c);
    const b = await page.evaluate(code("build"));
    assert.ok(b.startsWith("NG: 先に (2)"), b);
    await page.close();
  });

  await t(F.name + " partが1個足りなければ確認コードがNG", async () => {
    const page = await open();
    for (const s of parts.slice(0, -1)) await page.evaluate(s);
    const c = await page.evaluate(code(F.check));
    assert.ok(new RegExp(`part${parts.length}: ない NG`).test(c), c);
    await page.close();
  });

  await t(F.name + " 元画像（docs/sns/ig/…/0N.png）との差が小さい", async () => {
    assert.ok(got, "前のテストの画像がない");
    const page = await browser.newPage();
    for (const f of got.files) {
      const nn = f.name.slice(0, 2);
      const png = fs.readFileSync(path.join(ORIG, nn + ".png")).toString("base64");
      const r = await page.evaluate(async ([a, b, mask]) => {
        const load = (u) => new Promise((ok) => { const i = new Image(); i.onload = () => ok(i); i.src = u; });
        const [A, B] = await Promise.all([load("data:image/png;base64," + a), load("data:image/jpeg;base64," + b)]);
        const px = (img) => { const c = document.createElement("canvas"); c.width = 1080; c.height = 1350; const x = c.getContext("2d"); x.drawImage(img, 0, 0); return x.getImageData(0, 0, 1080, 1350).data; };
        const p = px(A), q = px(B); let sum = 0, big = 0; const n = p.length / 4;
        // 右下のAI表示（絵文字を図形に置き換えた所）は除外して数える
        for (let i = 0; i < n; i++) { const X = i % 1080, Y = (i / 1080) | 0; if (mask && X > 760 && Y > 1300) continue;
          const d = (Math.abs(p[i * 4] - q[i * 4]) + Math.abs(p[i * 4 + 1] - q[i * 4 + 1]) + Math.abs(p[i * 4 + 2] - q[i * 4 + 2])) / 3; sum += d; if (d > 64) big++; }
        return { mean: sum / n, bigPct: (100 * big) / n };
      }, [png, f.b64, F.aiMask]);
      console.log(nn, "平均差", r.mean.toFixed(2), "大きく違う画素", r.bigPct.toFixed(3) + "%");
      assert.ok(r.mean < 4 && r.bigPct < 1.0, nn + " 差が大きい " + JSON.stringify(r));
    }
    await page.close();
  });

  }

  await t("模擬ページ以外への通信が0件", async () => { assert.deepStrictEqual(external, []); });

  await browser.close();
  console.log(results.join("\n"));
  const fail = results.filter((r) => r.startsWith("FAIL")).length;
  console.log(fail ? `${fail} FAIL` : `ALL PASS（${results.length}項目）`);
  process.exit(fail ? 1 : 0);
})();
