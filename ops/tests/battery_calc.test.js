// モバイルバッテリーで何時間もつ？計算ツール（content/posts/mobile-battery-jikan-calculator.md）の検算テスト
// 実行：node ops/tests/battery_calc.test.js
// 記事の <script id="mb-calc-js"> ブロックだけを取り出して検証する（本番と同じコードを試す）
"use strict";
const fs = require("fs");
const path = require("path");
const vm = require("vm");
const assert = require("assert");

const root = path.join(__dirname, "../..");
const md = fs.readFileSync(path.join(root, "content/posts/mobile-battery-jikan-calculator.md"), "utf8");
const m = md.match(/<script id="mb-calc-js">([\s\S]*?)<\/script>/);
if (!m) throw new Error('<script id="mb-calc-js"> が見つかりません');
const ctx = { module: { exports: {} } };
vm.createContext(ctx);
vm.runInContext(m[1], ctx);
const B = ctx.module.exports;

let pass = 0, fail = 0;
function t(name, fn) {
  try { fn(); pass++; console.log("ok   " + name); }
  catch (e) { fail++; console.log("FAIL " + name + "\n     " + e.message); }
}
const near = (a, b, msg) => assert.ok(Math.abs(a - b) < 1e-9, `${msg}: ${a} != ${b}`);

const close = (a, b, msg, eps = 1e-9) => assert.ok(Math.abs(a - b) < eps, `${msg}: ${a} != ${b}`);

// 監査 2026-11-05_1900_r1 致命1：MCPCの60〜70％は mAh どうしの比（3.7V基準→5V基準）。電力量Whには掛けない
t("電圧は3.7V（電池）と5V（USB）", () => { near(B.V_CELL, 3.7, "cell"); near(B.V_USB, 5, "usb"); });
t("電池容量10000mAh・10W・60〜70％ → 電池37Wh／使える30〜35Wh／3.0〜3.5時間", () => {
  const r = B.calc("cell", 10000, 10, 60, 70, 31, 1.5);
  close(r.cellWh, 37, "cellWh"); close(r.useLo, 30, "useLo"); close(r.useHi, 35, "useHi");
  close(r.hLo, 3.0, "hLo"); close(r.hHi, 3.5, "hHi");
});
t("旧前提（37Wh×60〜70％＝22.2〜25.9Wh）の値にならない", () => {
  const r = B.calc("cell", 10000, 10, 60, 70, 31, 1.5);
  assert.ok(Math.abs(r.useLo - 22.2) > 1 && Math.abs(r.useHi - 25.9) > 1);
});
t("充電1回：37Wh×1.5÷1000×31円 ＝ 約1.72円", () => {
  const r = B.calc("cell", 10000, 10, 60, 70, 31, 1.5);
  close(r.chargeKwh, 0.0555, "kWh"); close(r.chargeYen, 1.7205, "yen");
});
t("20000mAh：使える60〜70Wh、5Wで12〜14時間、充電1回 約3.44円", () => {
  const r = B.calc("cell", 20000, 5, 60, 70, 31, 1.5);
  close(r.useLo, 60, "useLo"); close(r.useHi, 70, "useHi");
  close(r.hLo, 12, "hLo"); close(r.hHi, 14, "hHi"); close(r.chargeYen, 3.441, "yen", 1e-6);
});
t("10000mAh：5W → 6.0〜7.0時間、15W → 2.0〜2.3時間（監査の例）", () => {
  const a = B.calc("cell", 10000, 5, 60, 70, 31, 1.5), b = B.calc("cell", 10000, 15, 60, 70, 31, 1.5);
  close(a.hLo, 6, "5W lo"); close(a.hHi, 7, "5W hi");
  close(b.hLo, 2, "15W lo"); assert.strictEqual(Math.round(b.hHi * 10) / 10, 2.3);
});
t("定格容量（5V）6000mAh・10W → 30Wh・3時間ちょうど（割合はかけない）", () => {
  const r = B.calc("rated", 6000, 10, 60, 70, 31, 1.5);
  close(r.useLo, 30, "useLo"); close(r.useHi, 30, "useHi"); close(r.hLo, 3, "hLo"); close(r.hHi, 3, "hHi");
});
t("定格6000mAh の電気代は電池容量を 6000÷0.6＝10000mAh と逆算 → 37Wh・約1.72円", () => {
  const r = B.calc("rated", 6000, 10, 60, 70, 31, 1.5);
  close(r.cellWh, 37, "cellWh"); close(r.chargeYen, 1.7205, "yen");
});
t("電池容量10000mAh と 定格6000mAh（＝60％）は使える量の下限が一致", () => {
  close(B.calc("cell", 10000, 10, 60, 70, 31, 1.5).useLo, B.calc("rated", 6000, 10, 60, 70, 31, 1.5).useLo, "30Wh");
});
t("10W×8時間＝80Wh は1台（30〜35Wh）で足りない → 注意・約3台分", () => {
  const r = B.calc("cell", 10000, 10, 60, 70, 31, 1.5, 8);
  close(r.needWh, 80, "needWh"); assert.strictEqual(r.short, true); assert.strictEqual(r.units, 3);
});
t("10W×3時間＝30Wh は足りる（注意なし）／時間空欄なら注意なし", () => {
  assert.strictEqual(B.calc("cell", 10000, 10, 60, 70, 31, 1.5, 3).short, false);
  assert.strictEqual(B.calc("cell", 10000, 10, 60, 70, 31, 1.5, "").short, false);
  assert.strictEqual(B.calc("cell", 10000, 10, 60, 70, 31, 1.5).short, false);
});
t("割合の下限と上限が逆でも入れ替えて計算", () => {
  const a = B.calc("cell", 10000, 10, 70, 60, 31, 1.5), b = B.calc("cell", 10000, 10, 60, 70, 31, 1.5);
  near(a.hLo, b.hLo, "hLo"); near(a.hHi, b.hHi, "hHi");
});
t("割合は100％で頭打ち、充電ロスは1倍未満にしない", () => {
  const r = B.calc("cell", 10000, 10, 150, 150, 31, 0.5);
  close(r.useLo, 50, "useLo"); close(r.chargeKwh, 0.037, "kWh");
});
t("W空欄・0 → 時間0（NaN・Infinityにならない）", () => {
  for (const w of ["", 0, -5, "abc"]) {
    const r = B.calc("cell", 10000, w, 60, 70, 31, 1.5, 8);
    near(r.hLo, 0, "hLo"); near(r.hHi, 0, "hHi"); assert.strictEqual(r.short, false);
  }
});
t("容量空欄・マイナス → すべて0", () => {
  for (const mah of ["", -100]) for (const type of ["cell", "rated"]) {
    const r = B.calc(type, mah, 10, 60, 70, 31, 1.5, 8);
    near(r.cellWh, 0, "cellWh"); near(r.chargeYen, 0, "yen"); near(r.useLo, 0, "useLo"); assert.strictEqual(r.short, false);
  }
});
t("時間の表示：3.0 → 3時間0分、3.5 → 3時間30分、2.333… → 2時間20分", () => {
  assert.strictEqual(B.hm(3), "3時間0分"); assert.strictEqual(B.hm(3.5), "3時間30分"); assert.strictEqual(B.hm(35 / 15), "2時間20分");
});
t("記事の文面：旧前提の数値が残っておらず、新しい例と式が書かれている", () => {
  const text = md.replace(/<script[\s\S]*?<\/script>/g, "");
  assert.ok(!/22\.2|25\.9|22〜26|2時間13分|2時間35分|2\.2〜2\.6|取り出せる割合/.test(text), "旧前提の数値・言い回し");
  assert.ok(text.includes("約30〜35Wh") && text.includes("約3.0〜3.5時間") && text.includes("約1.7円"), "新しい例");
  assert.ok(text.includes("×5V÷1000") && text.includes("mAhどうしの比") && text.includes("80Wh"), "式とmAh比・80Whの注意");
  assert.ok(md.includes('<span class="badge">PR</span>') && md.includes("AI（電脳アリス）"), "PR表記・AI明記");
});

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
