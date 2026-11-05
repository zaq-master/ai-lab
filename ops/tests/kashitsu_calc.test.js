// 部屋の加湿量 計算ツール（content/posts/kashitsu-ryo-calculator.md）と結露記事の露点表の検算テスト
// 実行：node ops/tests/kashitsu_calc.test.js
// 記事の es()・asat() の式をそのまま取り出して、記事本文の計算例・露点表と照合する
// 追加：2026-11-06 03:00 計算総点検（カルク）
"use strict";
const fs = require("fs");
const path = require("path");
const vm = require("vm");
const assert = require("assert");

const root = path.join(__dirname, "../..");
const md = fs.readFileSync(path.join(root, "content/posts/kashitsu-ryo-calculator.md"), "utf8");
const fEs = md.match(/function es\(t\)\{[^\n]*\}/), fAs = md.match(/function asat\(t\)\{[^\n]*\}/);
if (!fEs || !fAs) throw new Error("es() / asat() が見つかりません");
const ctx = {};
vm.createContext(ctx);
vm.runInContext(fEs[0] + "\n" + fAs[0] + "\nthis.es=es;this.asat=asat;", ctx);
const { es, asat } = ctx;

let pass = 0, fail = 0;
function t(name, fn) {
  try { fn(); pass++; console.log("ok   " + name); }
  catch (e) { fail++; console.log("FAIL " + name + "\n     " + e.message); }
}
const r0 = (v) => Math.round(v);
const r1 = (v) => Math.round(v * 10) / 10;

// 記事の計算例：6畳（9.72m²）・天井2.4m・20℃・30%→50%・換気0.5回/時
const vol = 6 * 1.62 * 2.4;
t("体積 23.3m³・20℃の飽和水蒸気量 約17.3g/m³", () => {
  assert.strictEqual(r1(vol), 23.3); assert.strictEqual(r1(asat(20)), 17.3);
});
t("必要な水分量 約81g・換気分 約40mL/h（外気空欄）", () => {
  const d = asat(20) * 20 / 100;
  assert.strictEqual(r0(vol * d), 81); assert.strictEqual(r0(0.5 * vol * d), 40);
});
t("外気5℃・60%：外気4.08g/m³・目標8.64g/m³・換気分 約53mL/h・最初の1時間 約134mL/h", () => {
  const ao = asat(5) * 0.6, tgt = asat(20) * 0.5, keep = 0.5 * vol * (tgt - ao), need = vol * asat(20) * 0.2;
  assert.strictEqual(Math.round(asat(5) * 100) / 100, 6.80);
  assert.strictEqual(Math.round(ao * 100) / 100, 4.08); assert.strictEqual(Math.round(tgt * 100) / 100, 8.64);
  assert.strictEqual(r0(keep), 53); assert.strictEqual(r0(need + keep), 134);
});

// 結露記事（telework-ketsuro-taisaku-roten.md）の露点表は同じTetensの式
const ket = fs.readFileSync(path.join(root, "content/posts/telework-ketsuro-taisaku-roten.md"), "utf8");
function dew(t, rh) { const A = Math.log10(es(t) * rh / 100 / 6.1078); return 237.3 * A / (7.5 - A); }
t("結露記事 早見表①：露点（18/20/22℃ × 40〜70%）が本文と一致", () => {
  for (const T of [18, 20, 22]) {
    const row = [40, 50, 60, 70].map((h) => "約" + dew(T, h).toFixed(1) + "℃").join(" | ");
    assert.ok(ket.includes(`| ${T}℃ | ${row} |`), `${T}℃の行：${row}`);
  }
});
t("結露記事 早見表②：窓の表面温度ごとの湿度の上限が本文と一致", () => {
  for (const w of [5, 8, 10, 12, 14]) {
    const a = r0(es(w) / es(20) * 100), b = r0(es(w) / es(22) * 100);
    assert.ok(ket.includes(`| ${w}℃ | 約${a}% | 約${b}% |`), `${w}℃：約${a}% / 約${b}%`);
  }
});

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
