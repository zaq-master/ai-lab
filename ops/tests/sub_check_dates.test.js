// sub-check（docs/apps/sub-check/index.html）の支払日計算と .ics 書き出しのテスト
// 実行：node ops/tests/sub_check_dates.test.js
// HTML の <script id="sc-dates"> ブロックだけを取り出して検証する（本番と同じコードを試す）
"use strict";
const fs = require("fs");
const path = require("path");
const vm = require("vm");
const assert = require("assert");

const html = fs.readFileSync(path.join(__dirname, "../../docs/apps/sub-check/index.html"), "utf8");
const m = html.match(/<script id="sc-dates">([\s\S]*?)<\/script>/);
if (!m) throw new Error('<script id="sc-dates"> が見つかりません');
const ctx = { module: { exports: {} } };
vm.createContext(ctx);
vm.runInContext(m[1], ctx);
const D = ctx.module.exports;

const iso = (d) => d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
const from = (s) => { const [y, mo, d] = s.split("-").map(Number); return new Date(y, mo - 1, d); };
const list = (next, cycle, start, n) => D.upcoming(next, cycle, from(start), n).map(iso);

let pass = 0, fail = 0;
function t(name, fn) {
  try { fn(); pass++; console.log("ok   " + name); }
  catch (e) { fail++; console.log("FAIL " + name + "\n     " + e.message); }
}
const eq = (a, b) => assert.deepStrictEqual(JSON.parse(JSON.stringify(a)), b); // vm 側の配列を普通の配列に直して比べる

t("31日開始・月額（平年）：2/28、4/30…と月末に丸め、31日に戻る", () => eq(list("2027-01-31", "m", "2027-01-01", 12), [
  "2027-01-31", "2027-02-28", "2027-03-31", "2027-04-30", "2027-05-31", "2027-06-30",
  "2027-07-31", "2027-08-31", "2027-09-30", "2027-10-31", "2027-11-30", "2027-12-31"]));

t("31日開始・月額（うるう年）：2/29", () => eq(list("2028-01-31", "m", "2028-01-01", 3), ["2028-01-31", "2028-02-29", "2028-03-31"]));

t("30日開始・月額：2月だけ28日、31日の月も30日のまま", () => eq(list("2027-01-30", "m", "2027-01-01", 12), [
  "2027-01-30", "2027-02-28", "2027-03-30", "2027-04-30", "2027-05-30", "2027-06-30",
  "2027-07-30", "2027-08-30", "2027-09-30", "2027-10-30", "2027-11-30", "2027-12-30"]));

t("29日開始・月額：平年2/28、うるう年2/29、ほかは29日", () => {
  eq(list("2027-01-29", "m", "2027-01-01", 3), ["2027-01-29", "2027-02-28", "2027-03-29"]);
  eq(list("2028-01-29", "m", "2028-01-01", 3), ["2028-01-29", "2028-02-29", "2028-03-29"]);
});

t("28日以下は従来どおり毎月同じ日", () => eq(list("2027-01-15", "m", "2027-01-01", 3), ["2027-01-15", "2027-02-15", "2027-03-15"]));

t("年額 2/29開始：平年は2/28、うるう年は2/29に戻る", () => eq(list("2028-02-29", "y", "2028-01-01", 5),
  ["2028-02-29", "2029-02-28", "2030-02-28", "2031-02-28", "2032-02-29"]));

t("自動繰り越し：過去の1/31を入れても、丸めた日に引きずられない", () => {
  eq(list("2026-01-31", "m", "2026-11-02", 3), ["2026-11-30", "2026-12-31", "2027-01-31"]);
  eq(list("2026-01-31", "m", "2027-03-01", 2), ["2027-03-31", "2027-04-30"]);
  eq(list("2026-01-31", "m", "2027-02-28", 1), ["2027-02-28"]); // 当日は「今日」として残る
});

t("自動繰り越し：年額2/29を何年も前に入れても正しい", () => {
  eq(list("2020-02-29", "y", "2026-11-02", 2), ["2027-02-28", "2028-02-29"]);
});

t("未来の日付はそのまま／不正な日付は空", () => {
  eq(list("2027-05-31", "m", "2026-11-02", 1), ["2027-05-31"]);
  eq(list("", "m", "2026-11-02", 1), []);
  eq(list("2026-13-01", "m", "2026-11-02", 1), []);
});

t("一気に1200ヶ月先でも結果が出る（ループの上限で止まらない）", () => {
  eq(list("1990-01-31", "m", "2090-02-01", 1), ["2090-02-28"]);
});

t(".ics：31日払いは12件の個別予定・RRULEなし・UIDが重複しない", () => {
  const lines = D.icsEvents({ id: "abc", next: "2027-01-31", cycle: "m" }, "テスト", from("2027-01-01"), "20270101T000000Z");
  const starts = lines.filter((l) => l.startsWith("DTSTART")).map((l) => l.split(":")[1]);
  eq(starts, ["20270131", "20270228", "20270331", "20270430", "20270531", "20270630",
    "20270731", "20270831", "20270930", "20271031", "20271130", "20271231"]);
  assert.ok(!lines.some((l) => l.startsWith("RRULE")), "RRULE が入っている");
  const uids = lines.filter((l) => l.startsWith("UID"));
  eq(new Set(uids).size, 12);
  eq(lines.filter((l) => l === "BEGIN:VALARM").length, 12);
});

t(".ics：DTEND は翌日（2/28 → 3/1、12/31 → 翌1/1）", () => {
  const lines = D.icsEvents({ id: "x", next: "2027-01-31", cycle: "m" }, "t", from("2027-01-01"), "s");
  const ends = lines.filter((l) => l.startsWith("DTEND")).map((l) => l.split(":")[1]);
  assert.ok(ends.includes("20270301"));
  assert.ok(ends.includes("20280101"));
});

t(".ics：年額2/29は4年分の個別予定", () => {
  const lines = D.icsEvents({ id: "y", next: "2028-02-29", cycle: "y" }, "t", from("2028-01-01"), "s");
  eq(lines.filter((l) => l.startsWith("DTSTART")).map((l) => l.split(":")[1]), ["20280229", "20290228", "20300228", "20310228"]);
  assert.ok(!lines.some((l) => l.startsWith("RRULE")));
});

t(".ics：28日以下・通常の年額は従来どおり RRULE 1件", () => {
  const a = D.icsEvents({ id: "a", next: "2027-01-15", cycle: "m" }, "t", from("2027-01-01"), "s");
  eq(a.filter((l) => l.startsWith("RRULE")), ["RRULE:FREQ=MONTHLY"]);
  eq(a.filter((l) => l === "BEGIN:VEVENT").length, 1);
  const b = D.icsEvents({ id: "b", next: "2027-03-31", cycle: "y" }, "t", from("2027-01-01"), "s");
  eq(b.filter((l) => l.startsWith("RRULE")), ["RRULE:FREQ=YEARLY"]);
});

console.log("\n" + pass + " passed, " + fail + " failed");
process.exit(fail ? 1 : 0);
