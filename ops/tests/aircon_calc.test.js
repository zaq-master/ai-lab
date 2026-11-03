// エアコン暖房の電気代計算（content/posts/aircon-danbou-denkidai-calculator.md）の検算テスト
// 実行：node ops/tests/aircon_calc.test.js
// 記事の <script id="ac-calc-js"> ブロックだけを取り出して検証する（本番と同じコードを試す）
"use strict";
const fs = require("fs");
const path = require("path");
const vm = require("vm");
const assert = require("assert");

const root = path.join(__dirname, "../..");
const md = fs.readFileSync(path.join(root, "content/posts/aircon-danbou-denkidai-calculator.md"), "utf8");
const m = md.match(/<script id="ac-calc-js">([\s\S]*?)<\/script>/);
if (!m) throw new Error('<script id="ac-calc-js"> が見つかりません');
const ctx = { module: { exports: {} } };
vm.createContext(ctx);
vm.runInContext(m[1], ctx);
const A = ctx.module.exports;

let pass = 0, fail = 0;
function t(name, fn) {
  try { fn(); pass++; console.log("ok   " + name); }
  catch (e) { fail++; console.log("FAIL " + name + "\n     " + e.message); }
}
const near = (a, b, msg) => assert.ok(Math.abs(a - b) < 1e-9, `${msg}: ${a} != ${b}`);

// 手計算：W×(％/100)/1000×時間×単価
t("600W・1時間・31円 → 1時間 18.6円", () => {
  const r = A.calc(600, 100, 1, 30, 4, 31);
  near(r.hour, 18.6, "hour"); near(r.day, 18.6, "day");
});
t("600W・8時間・30日・4ヶ月・31円 → 1日148.8円／1ヶ月4,464円／ひと冬17,856円", () => {
  const r = A.calc(600, 100, 8, 30, 4, 31);
  near(r.day, 148.8, "day"); near(r.month, 4464, "month"); near(r.season, 17856, "season"); near(r.kwhDay, 4.8, "kWh/day");
});
t("1000W・平均50％・8時間・31円 → 500W相当で1日124円", () => {
  const r = A.calc(1000, 50, 8, 30, 4, 31);
  near(r.day, 124, "day"); near(r.month, 3720, "month");
});
t("450W・24時間・31日・単価27.5円 → 1日297円／1ヶ月9,207円", () => {
  const r = A.calc(450, 100, 24, 31, 1, 27.5);
  near(r.day, 297, "day"); near(r.month, 9207, "month"); near(r.season, 9207, "season(1ヶ月)");
});
t("文字列入力（フォームの値）でも同じ結果", () => {
  const r = A.calc("600", "100", "8", "30", "4", "31");
  near(r.season, 17856, "season");
});
t("空欄・マイナス・文字は0扱いで結果0（NaNにならない）", () => {
  for (const r of [A.calc("", 100, 8, 30, 4, 31), A.calc(-600, 100, 8, 30, 4, 31), A.calc("abc", 100, 8, 30, 4, 31)]) {
    near(r.hour, 0, "hour"); near(r.season, 0, "season");
  }
});
t("1日の時間は24時間で頭打ち", () => {
  near(A.calc(1000, 100, 30, 1, 1, 31).day, 744, "day");
});
t("期間消費電力量800kWh・31円 → 年24,800円／月平均約2,066.67円", () => {
  const y = A.year(800, 31);
  near(y.year, 24800, "year"); near(y.monthAvg, 24800 / 12, "monthAvg");
});
t("期間消費電力量が空欄 → 0", () => near(A.year("", 31).year, 0, "year"));

// ページの作り（既存ツールと同じ導線・表記）
t("PR表記・商品枠・次の一手・31円の出典と確認日がある", () => {
  assert.ok(md.includes('<span class="badge">PR</span>'), "PRバッジ");
  assert.ok(/<!-- products: [^>]*circulator/.test(md), "商品枠");
  assert.ok(md.includes('class="tool-next"') && md.includes('href="#tool-prods"'), "結果直後の導線");
  assert.ok(md.includes('<div id="tool-prods"></div>'), "導線の飛び先");
  assert.ok(md.includes("全国家庭電気製品公正取引協議会") && md.includes("2026-11-03確認"), "出典と確認日");
  assert.ok(md.includes("実機レビューではありません"), "実機レビューでない明記");
});
t("build.py の TOOLS に登録されている", () => {
  const b = fs.readFileSync(path.join(root, "build.py"), "utf8");
  assert.ok(b.includes('"posts/aircon-danbou-denkidai-calculator.html"'));
});

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
