"""3分動画「やめ方で勝てる？」の計算。結果は results.json（動画の数字はここからだけ取る）。
条件は plans/2026-11-20_yamekata.md の確認表で確定したもの。
実行：python3 side/sim3min/sim.py
"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "pachi3d"))
from pachisim import ST_MACHINE_TOKYOGHOUL as M, Conditions, simulate, describe

N, DAYS, SEED = 10000, 30, 20261120
BASE = dict(rate=16.0, exchange_yen=4.0, hours=8.0, budget_yen=50000)
PLANS = {
    "close":  ("18時まで打つ", {}),
    "win2":   ("2万円勝ったら帰る", dict(stop_win_yen=20000)),
    "rush1":  ("RUSHが1回終わったら帰る", dict(stop_after_rush=True)),
    "lose1":  ("財布に1万円だけ（勝っても18時まで打つ）", dict(budget_yen=10000)),
}

def stats(y):
    return dict(win=float((y > 0).mean()), mean=float(y.mean()), median=float(np.median(y)),
                p10=float(np.percentile(y, 10)), p90=float(np.percentile(y, 90)),
                se=float(y.std() / np.sqrt(len(y))))

out = dict(n=N, days=DAYS, seed=SEED, base=BASE, machine=M.name, sources=M.sources, plans={}, rate_scan={})
t0 = time.time()
for key, (label, extra) in PLANS.items():
    c = Conditions(**{**BASE, **extra})
    total = np.zeros(N); day1 = None; spins = np.zeros(N); hours = np.zeros(N)
    for d in range(DAYS):
        r = simulate(M, c, n=N, seed=SEED + 1000 * d + list(PLANS).index(key) * 97)
        if d == 0:
            day1 = r
        total += r["yen"]; spins += r["spins"]; hours += r["hours_played"]
    out["plans"][key] = dict(label=label, cond=describe(c), day1=stats(day1["yen"]), month=stats(total),
                             day1_hours=float(day1["hours_played"].mean()), day1_spins=float(day1["spins"].mean()),
                             day1_broke=float(day1["broke"].mean()), month_spins=float(spins.mean()),
                             month_hours=float(hours.mean()),
                             yen_per_1000spins=float(total.mean() / spins.mean() * 1000),   # 通常時の回転だけを数える
                             yen_per_hour=float(total.mean() / hours.mean()),
                             day1_p10=float(np.percentile(day1["yen"], 10)), day1_p90=float(np.percentile(day1["yen"], 90)))
    print(key, json.dumps(out["plans"][key], ensure_ascii=False), f"{time.time()-t0:.0f}s", flush=True)
# 回転率の比較（18時まで打つ・30日）。16回転は上の「18時まで打つ」と同じ数字を使う（画面に2つの数字を出さない）
for rate in (15, 16, 17, 18):
    if rate == 16:
        out["rate_scan"][rate] = out["plans"]["close"]["month"]; continue
    c = Conditions(**{**BASE, "rate": float(rate)})
    total = np.zeros(N); hours = np.zeros(N)
    for d in range(DAYS):
        r = simulate(M, c, n=N, seed=SEED + 1000 * d)
        total += r["yen"]; hours += r["hours_played"]
    out["rate_scan"][rate] = {**stats(total), "yen_per_hour": float(total.mean() / hours.mean())}
    print(rate, out["rate_scan"][rate], f"{time.time()-t0:.0f}s", flush=True)
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), ensure_ascii=False, indent=1)
