"""3分動画「1回だけ打つ人と、何年も打つ人。プラスの人の割合は？」の計算 → results_<rate>.json
同じ1万人が、同じルール（週2回・1回最大4時間・財布2万円まで・持ち玉で遊技・RUSH中は最後まで）で打ち続け、
打った回数（期間）ごとの「通算でプラスの人の割合」と金額を数える。比べるのは期間だけ（公平さのため）。
回転率が違っても、同じ回は同じ乱数の種を使う（＝同じ運で、台の差だけを比べる）。
実行：python3 sim.py 16
"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pachi3d"))
from pachisim import ST_MACHINE_TOKYOGHOUL as M, Conditions, simulate, describe

RATE = float(sys.argv[1]) if len(sys.argv) > 1 else 16.0
N, DAYS, SEED = 10000, 520, 20261127          # 週2回×52週×5年
CHECK = {"1回": 1, "1ヶ月": 8, "3ヶ月": 26, "半年": 52, "1年": 104, "2年": 208, "5年": 520}
c = Conditions(rate=RATE, exchange_yen=4.0, hours=4.0, budget_yen=20000)
cum = np.zeros(N); hours = np.zeros(N); series = dict(win=[], median=[], p10=[], p90=[], mean=[])
traj = []; day_win = []; day_hours = []; day_broke = []
out = dict(n=N, days=DAYS, seed=SEED, rate=RATE, cond=describe(c), machine=M.name, sources=M.sources, check={})
t0 = time.time()
for d in range(1, DAYS + 1):
    r = simulate(M, c, n=N, seed=SEED + d * 1009)
    cum += r["yen"]; hours += r["hours_played"]
    day_win.append(float((r["yen"] > 0).mean())); day_hours.append(float(r["hours_played"].mean())); day_broke.append(float(r["broke"].mean()))
    for k, v in (("win", (cum > 0).mean()), ("median", np.median(cum)), ("p10", np.percentile(cum, 10)), ("p90", np.percentile(cum, 90)), ("mean", cum.mean())):
        series[k].append(float(v))
    if d <= 104: traj.append(cum[:10].round().tolist())
    if d in CHECK.values():
        k = [k for k, v in CHECK.items() if v == d][0]
        out["check"][k] = dict(days=d, win=float((cum > 0).mean()), mean=float(cum.mean()), median=float(np.median(cum)),
                               p10=float(np.percentile(cum, 10)), p90=float(np.percentile(cum, 90)), best=float(cum.max()),
                               worst=float(cum.min()), se=float(cum.std() / np.sqrt(N)),
                               yen_per_hour=float(cum.mean() / hours.mean()), hours=float(hours.mean()))
        if d == 104: out["year_hist"], out["year_edges"] = [x.tolist() for x in np.histogram(cum, bins=40)]
        print(RATE, k, json.dumps(out["check"][k], ensure_ascii=False), f"{time.time()-t0:.0f}s", flush=True)
out.update(series=series, traj10=traj, day_win_mean=float(np.mean(day_win)), day_hours_mean=float(np.mean(day_hours)),
           day_broke_mean=float(np.mean(day_broke)))
json.dump(out, open(os.path.join(HERE, f"results_{RATE:g}.json"), "w"), ensure_ascii=False)
