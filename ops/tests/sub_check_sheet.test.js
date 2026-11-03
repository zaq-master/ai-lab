// sub-check（docs/apps/sub-check/index.html）の結果画面の導線（サブスク管理表）のテスト
// 実行：node ops/tests/sub_check_sheet.test.js
// HTML の <script id="sc-sheet"> ブロックだけを取り出して検証する（本番と同じコードを試す）
"use strict";
const fs = require("fs");
const path = require("path");
const vm = require("vm");
const assert = require("assert");

const html = fs.readFileSync(path.join(__dirname, "../../docs/apps/sub-check/index.html"), "utf8");
const m = html.match(/<script id="sc-sheet">([\s\S]*?)<\/script>/);
if (!m) throw new Error('<script id="sc-sheet"> が見つかりません');
const ctx = { module: { exports: {} } };
vm.createContext(ctx);
vm.runInContext(m[1], ctx);
const S = ctx.module.exports;
const NOTE = "https://note.com/zaqmaster";

let pass = 0, fail = 0;
function t(name, fn) {
  try { fn(); pass++; console.log("ok   " + name); }
  catch (e) { fail++; console.log("FAIL " + name + "\n     " + e.message); }
}

t("見直し候補が0件なら導線を出さない", () => {
  assert.strictEqual(S.cta(0, "", NOTE), null);
  assert.strictEqual(S.cta(0, "https://note.com/zaqmaster/n/x", NOTE), null);
});

t("販売URLが空の間は「準備中」で note 連載トップへ", () => {
  const c = S.cta(2, "", NOTE);
  assert.strictEqual(c.ready, false);
  assert.strictEqual(c.href, NOTE);
  assert.ok(c.label.includes("準備中"));
});

t("販売URLが入れば販売ページへ", () => {
  const c = S.cta(1, "https://note.com/zaqmaster/n/abc", NOTE);
  assert.strictEqual(c.ready, true);
  assert.strictEqual(c.href, "https://note.com/zaqmaster/n/abc");
});

t("https 以外の値は使わない（準備中扱い）", () => {
  assert.strictEqual(S.cta(1, "javascript:alert(1)", NOTE).href, NOTE);
});

t("広告ではなく自社の有料記事だと明記", () => {
  const d = S.cta(1, "", NOTE).disclosure;
  assert.ok(d.includes("広告ではなく") && d.includes("有料記事"));
});

t("本番の定数：SHEET_SALES_URL は空、NOTE_TOP_URL は config.json の note と同じ", () => {
  assert.strictEqual(ctx.SHEET_SALES_URL, "");
  const cfg = JSON.parse(fs.readFileSync(path.join(__dirname, "../../config.json"), "utf8"));
  assert.strictEqual(ctx.NOTE_TOP_URL, cfg.note);
});

console.log("\n" + pass + " passed, " + fail + " failed");
process.exit(fail ? 1 : 0);
