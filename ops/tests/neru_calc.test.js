// 寝るときの暖房 一晩の電気代くらべ（content/posts/neru-danbou-denkidai-calculator.md）の検算テスト
// 実行：node ops/tests/neru_calc.test.js
// 記事の <script id="nr-calc-js"> ブロックだけを取り出して検証する（本番と同じコードを試す）
"use strict";
const fs = require("fs");
const path = require("path");
const vm = require("vm");
const assert = require("assert");

const root = path.join(__dirname, "../..");
const md = fs.readFileSync(path.join(root, "content/posts/neru-danbou-denkidai-calculator.md"), "utf8");
const m = md.match(/<script id="nr-calc-js">([\s\S]*?)<\/script>/);
if (!m) throw new Error('<script id="nr-calc-js"> が見つかりません');
const ctx = { module: { exports: {} } };
vm.createContext(ctx);
vm.runInContext(m[1], ctx);
const N = ctx.module.exports;

let pass = 0, fail = 0;
function t(name, fn) {
  try { fn(); pass++; console.log("ok   " + name); }
  catch (e) { fail++; console.log("FAIL " + name + "\n     " + e.message); }
}
const near = (a, b, msg) => assert.ok(Math.abs(a - b) < 1e-9, `${msg}: ${a} != ${b}`);

// 電気の暖房：W÷1000×時間×単価
t("電気毛布50W・8時間・31円・30日 → 一晩12.4円／1か月372円", () => {
  const r = N.device(50, 8, 31, 30);
  near(r.kwh, 0.4, "kWh"); near(r.night, 12.4, "night"); near(r.month, 372, "month");
});
t("エアコン400W・8時間・31円・30日 → 一晩99.2円／1か月2,976円", () => {
  const r = N.device(400, 8, 31, 30);
  near(r.night, 99.2, "night"); near(r.month, 2976, "month");
});
t("オイルヒーター600W・8時間・27.5円・31日 → 一晩132円／1か月4,092円", () => {
  const r = N.device(600, 8, 27.5, 31);
  near(r.night, 132, "night"); near(r.month, 4092, "month");
});
t("使用時間は24時間で頭打ち", () => near(N.device(1000, 30, 31, 1).night, 744, "night"));
t("空欄・マイナス・文字は0扱い（NaNにならない）", () => {
  for (const r of [N.device("", 8, 31, 30), N.device(-50, 8, 31, 30), N.device("abc", 8, 31, 30)]) {
    near(r.night, 0, "night"); near(r.month, 0, "month");
  }
});

// 湯たんぽ：L×4.186×ΔT÷3600÷効率×回数
t("比熱は4.186 kJ/(kg・℃)", () => near(N.C, 4.186, "C"));
t("2L・15→80℃・効率80％・1回・31円・30日（手計算）", () => {
  const kwh = 2 * 4.186 * 65 / 3600 / 0.8; // 0.18895…kWh
  const r = N.kettle(2, 15, 80, 80, 1, 31, 30);
  near(r.kwh, kwh, "kWh"); near(r.night, kwh * 31, "night"); near(r.month, kwh * 31 * 30, "month");
  assert.ok(Math.abs(r.night - 5.857) < 0.001, "一晩 約5.86円");
});
t("効率100％・1L・0→100℃ → 4.186×100/3600 kWh", () => near(N.kettle(1, 0, 100, 100, 1, 31, 30).kwh, 418.6 / 3600, "kWh"));
t("回数2回で2倍", () => near(N.kettle(2, 15, 80, 80, 2, 31, 30).night, 2 * N.kettle(2, 15, 80, 80, 1, 31, 30).night, "night"));
t("お湯の温度が水温以下・効率0・量が空欄 → 0", () => {
  near(N.kettle(2, 80, 15, 80, 1, 31, 30).night, 0, "逆転");
  near(N.kettle(2, 15, 80, 0, 1, 31, 30).night, 0, "効率0");
  near(N.kettle("", 15, 80, 80, 1, 31, 30).night, 0, "量空欄");
});
t("効率は100％で頭打ち", () => near(N.kettle(1, 0, 100, 150, 1, 31, 30).kwh, 418.6 / 3600, "kWh"));
t("文字列入力（フォームの値）でも同じ結果", () => near(N.kettle("2", "15", "80", "80", "1", "31", "30").night, N.kettle(2, 15, 80, 80, 1, 31, 30).night, "night"));

t("rank：0円の行を除き、一晩の安い順に並ぶ", () => {
  const r = N.rank([{ name: "a", night: 99 }, { name: "b", night: 0 }, { name: "c", night: 5.8 }, { name: "d", night: 12.4 }]);
  assert.deepStrictEqual(Array.from(r, x => x.name), ["c", "d", "a"]);
});

// ページの作り（既存ツールと同じ導線・表記）
t("PR表記・商品枠・次の一手・31円の出典と確認日・例/仮定の明記", () => {
  assert.ok(md.includes('<span class="badge">PR</span>'), "PRバッジ");
  assert.ok(/<!-- products: [^>]*denki-moufu/.test(md), "商品枠");
  assert.ok(md.includes('class="tool-next"') && md.includes('href="#tool-prods"'), "結果直後の導線");
  assert.ok(md.includes('<div id="tool-prods"></div>'), "導線の飛び先");
  assert.ok(md.indexOf('<!-- products:') < md.indexOf("## 使い方"), "商品枠がツール直後にある");
  assert.ok(md.includes("全国家庭電気製品公正取引協議会") && md.includes("2026-11-03確認"), "出典と確認日");
  assert.ok(md.includes("実機レビューではありません"), "実機レビューでない明記");
  assert.ok(md.includes("（例）") && md.includes("（仮定）"), "例・仮定の明記");
  assert.ok(md.includes('id="nr-share"') && md.includes("twitter.com/intent/tweet"), "X共有リンク");
  assert.ok(md.includes("取扱説明書"), "取扱説明書の確認");
  assert.ok(!/マラソン/.test(md), "期間つきの楽天マラソン文言を入れない");
});
t("関連記事への内部リンクがリンク先に存在する", () => {
  for (const h of md.match(/\]\(([a-z0-9-]+\.html)\)/g).map(s => s.slice(2, -1))) {
    assert.ok(fs.existsSync(path.join(root, "content/posts", h.replace(".html", ".md"))), h);
  }
});
t("build.py の TOOLS に登録されている", () => {
  const b = fs.readFileSync(path.join(root, "build.py"), "utf8");
  assert.ok(b.includes('"posts/neru-danbou-denkidai-calculator.html"'));
});

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
