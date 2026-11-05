// 楽天お買い物マラソン 買いまわり計算（content/posts/rakuten-marathon-point-calculator.md）の検算テスト
// 実行：node ops/tests/marathon_calc.test.js
// 記事の /* calc-start */〜/* calc-end */ だけを取り出して検証する（本番と同じコードを試す）
// 追加：2026-11-06 03:00 計算総点検（カルク）
"use strict";
const fs = require("fs");
const path = require("path");
const vm = require("vm");
const assert = require("assert");

const root = path.join(__dirname, "../..");
const md = fs.readFileSync(path.join(root, "content/posts/rakuten-marathon-point-calculator.md"), "utf8");
const m = md.match(/\/\* calc-start \*\/([\s\S]*?)\/\* calc-end \*\//);
if (!m) throw new Error("calc-start〜calc-end が見つかりません");
const ctx = {};
vm.createContext(ctx);
vm.runInContext(m[1] + "\nthis.marathonCalc=marathonCalc;", ctx);
const calc = ctx.marathonCalc;
const OPT = { threshold: 1000, maxRate: 10, cap: 7000 }; // 2026年11月回の公式条件

let pass = 0, fail = 0;
function t(name, fn) {
  try { fn(); pass++; console.log("ok   " + name); }
  catch (e) { fail++; console.log("FAIL " + name + "\n     " + e.message); }
}

t("記事の初期例（8,000円・1,200円・980円）→ 2店舗・2倍・税抜8,362円・特典83pt", () => {
  const r = calc([{ amount: 8000 }, { amount: 1200 }, { amount: 980 }], OPT);
  assert.strictEqual(r.shops, 2); assert.strictEqual(r.rate, 2); assert.strictEqual(r.extraRate, 1);
  // floor(8000×100/110)=7272、floor(1200×100/110)=1090
  assert.strictEqual(r.taxless, 8362); assert.strictEqual(r.points, 83); assert.strictEqual(r.normal, 83);
  assert.deepStrictEqual(Array.from(r.flags), [true, true, false]);
});
t("ちょうど1,000円は対象、999円は対象外", () => {
  const r = calc([{ amount: 1000 }, { amount: 999 }], OPT);
  assert.deepStrictEqual(Array.from(r.flags), [true, false]); assert.strictEqual(r.rate, 1); assert.strictEqual(r.points, 0);
});
t("8%の行は ×100÷108（1,080円→税抜1,000円）", () => {
  const r = calc([{ amount: 1080, tax8: true }, { amount: 1100 }], OPT);
  assert.strictEqual(r.taxless, 2000); assert.strictEqual(r.points, 20);
});
t("11店舗でも10倍まで（特典+9倍）", () => {
  const rows = Array.from({ length: 11 }, () => ({ amount: 1100 }));
  const r = calc(rows, OPT);
  assert.strictEqual(r.shops, 11); assert.strictEqual(r.rate, 10); assert.strictEqual(r.extraRate, 9); assert.strictEqual(r.toNext, 0);
});
t("上限7,000ptで頭打ち（10倍・税抜10万円×9％＝9,000pt→7,000pt）", () => {
  const rows = Array.from({ length: 10 }, () => ({ amount: 11000 })); // 税抜1万円×10
  const r = calc(rows, OPT);
  assert.strictEqual(r.taxless, 100000); assert.strictEqual(r.rawPoints, 9000); assert.strictEqual(r.points, 7000); assert.ok(r.capped);
});
t("早見表：上限に届く税抜合計（2倍70万・3倍35万・5倍17.5万・8倍10万・10倍77,778円）", () => {
  const want = { 2: 700000, 3: 350000, 5: 175000, 8: 100000, 10: 77778 };
  for (const k of Object.keys(want)) {
    const rows = Array.from({ length: +k }, () => ({ amount: 1100 }));
    assert.strictEqual(calc(rows, OPT).capTaxless, want[k], k + "店舗");
  }
  // 記事の早見表の数字と一致しているか
  for (const s of ["700,000円", "350,000円", "175,000円", "100,000円", "約77,778円"]) assert.ok(md.includes(s), "早見表に " + s);
});

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
