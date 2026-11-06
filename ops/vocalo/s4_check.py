#!/usr/bin/env python3
"""ボカロXの判定S4（ops/strategy/judge_2026-11-16_v2.md）を x_metrics.csv から計算する。
使い方: python3 ops/vocalo/s4_check.py [--median 50] [--clicks 5]
- 新曲告知は x_metrics.csv に入れない（S4の対象外）
- 投稿から12時間未満で読んだ数字は「早すぎ」として判定から外す（時間がたつほど表示数は増えるため）
"""
import csv, sys, statistics, argparse
from datetime import datetime
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("--median", type=float, default=50)
p.add_argument("--clicks", type=int, default=5)
p.add_argument("--min-hours", type=float, default=12)
a = p.parse_args()

rows = list(csv.DictReader(open(Path(__file__).with_name("x_metrics.csv"), encoding="utf-8")))
fmt = "%Y-%m-%d %H:%M"
ok, early, empty = [], [], []
for r in rows:
    if not r["impressions"].strip():
        empty.append(r["id"]); continue
    try:
        h = (datetime.strptime(r["read_at"].strip(), fmt) - datetime.strptime(r["posted_at"].strip(), fmt)).total_seconds() / 3600
    except ValueError:
        h = None
    r["_h"] = h
    (early if h is not None and h < a.min_hours else ok).append(r)

def num(v):
    try: return int(v)
    except ValueError: return 0

print(f"記録あり {len(ok)}件／早すぎ（{a.min_hours:g}時間未満）{len(early)}件／未記録 {len(empty)}件")
if early: print("  早すぎ:", ", ".join(r["id"] for r in early), "→ 次のPC回で読み直す")
if not ok:
    print("S4判定：データなし → 未計測＝止める側（告知以外の予約は1日1件）"); sys.exit(0)

imps = [num(r["impressions"]) for r in ok]
clicks = sum(num(r["profile_clicks"]) for r in ok)
med = statistics.median(imps)
print(f"表示数の中央値 {med:g}（しきい値 {a.median:g}）／プロフィールクリック合計 {clicks}（しきい値 {a.clicks}）")
for key in ("kind", "head"):
    groups = {}
    for r in ok: groups.setdefault(r[key], []).append(num(r["impressions"]))
    print(f"  {'型' if key=='kind' else '1行目'}別の中央値:", "／".join(f"{k} {statistics.median(v):g}（{len(v)}件）" for k, v in groups.items()))
slots = {}
for r in ok: slots.setdefault(r["posted_at"][-5:], []).append(num(r["impressions"]))
print("  時刻別の中央値:", "／".join(f"{k} {statistics.median(v):g}（{len(v)}件）" for k, v in sorted(slots.items())))
if med < a.median and clicks < a.clicks:
    print("S4判定：止める側 → 告知以外の予約を1日1件に減らす")
else:
    print("S4判定：続ける側 → 1日2件のまま")
if len(ok) < 6: print("※記録が6件未満。判定は参考値（11/16の本判定は11/15分まで）")
