"""「確率1%のガチャ」を1万人でためす（乱数の種 20261201）。架空のガチャ。実在のゲームではない。
実験① 1万人が100回ずつ引く → 1回も当たらない人の割合（計算の答え 0.99^100）
実験② 1万人が当たるまで引く → 当たるまでの回数（半分・9割・99%の人が当たる回数、平均、いちばん運の悪い人）
実験③ 200回つづけて外れた人を1万人集め、次の100回で当たる割合（計算の答えは①と同じ）
実験④ 天井（200回引いても出なければ、もらえる）→ 実験②の同じ1万人で、引く回数は min(回数, 200)
実験⑤ 全6種類（どれも同じ確率）を1万人がそろうまで引く → 平均（計算の答え 6×(1+1/2+…+1/6)=14.7）
計算の答えと合うかを確かめて results.json に保存。
"""
import json
import math
import os

import numpy as np

SEED, N, P = 20261201, 10000, 0.01
HERE = os.path.dirname(os.path.abspath(__file__))
Q = 1 - P


def near(x, th, se, name, k=3.5):
    assert abs(x - th) < k * se, f"{name}: {x} が計算の答え {th} から離れすぎ（許容 {k * se:.4f}）"


def main():
    rng = np.random.default_rng(SEED)
    out = dict(seed=SEED, n=N, p=P)

    # ---- 実験① 100回ずつ ----
    draws = rng.random((N, 100)) < P                       # [人, 回] 当たりか
    cnt = draws.sum(1)
    win = cnt > 0
    th0 = Q ** 100
    zero = float((~win).mean())
    near(zero, th0, math.sqrt(th0 * (1 - th0) / N), "①0回の人")
    first = np.where(draws[0])[0]
    out["e1"] = dict(zero=int((~win).sum()), win=int(win.sum()), zero_rate=round(zero, 4), win_rate=round(1 - zero, 4),
                     zero_theory=round(th0, 4), win_theory=round(1 - th0, 4),
                     p1_bits="".join("1" if b else "0" for b in draws[0]), p1_hits=int(cnt[0]),
                     p1_first=int(first[0]) + 1 if len(first) else 0,
                     win10=int(win[:10].sum()), win100=int(win[:100].sum()),
                     ten_bits=["".join("1" if b else "0" for b in draws[i]) for i in range(10)],
                     bits="".join("1" if b else "0" for b in win), most=int(cnt.max()),
                     multi=int((cnt >= 2).sum()),
                     pow=[round(Q ** k, 4) for k in range(0, 101)])

    # ---- 実験② 当たるまで ----
    x = rng.geometric(P, N)                                 # 当たった回（1〜）
    qs = {}
    for name, f in (("half", 0.5), ("p90", 0.9), ("p99", 0.99)):
        th = math.ceil(math.log(1 - f) / math.log(Q))       # その回までに f 以上の人が当たる最初の回
        sim = int(np.sort(x)[int(math.ceil(f * N)) - 1])    # f の人数に届いた回
        se = math.sqrt(f * (1 - f) / N) / (P * (1 - f))     # 回数のばらつきの目安
        near(sim, th, se + 1, "②" + name)
        qs[name] = dict(sim=sim, theory=th, share=round(float((x <= sim).mean()), 4))
    mean = float(x.mean())
    near(mean, 1 / P, math.sqrt(Q) / P / math.sqrt(N), "②平均")
    over_mean = float((x > 100).mean())
    out["e2"] = dict(x=x.tolist(), mean=round(mean, 1), mean_theory=100, max=int(x.max()), min=int(x.min()),
                     first=int(x[0]), ten=x[:10].tolist(), **qs,
                     within100=round(float((x <= 100).mean()), 4), over_mean=round(over_mean, 4),
                     first1=int((x == 1).sum()))

    # ---- 実験③ 200回外れた人を1万人集める ----
    got, tried = [], 0
    while sum(len(g) for g in got) < N:
        y = rng.geometric(P, 20000); tried += len(y)
        got.append(y[y > 200])
    allg = np.concatenate(got)
    # ちょうど1万人目が見つかった時点までに、ためした人数
    y_all_tried = tried - 20000 + int(np.where(np.cumsum(y > 200) == N - (len(allg) - len(got[-1])))[0][0]) + 1
    g = allg[:N]
    more = g - 200                                          # 200回外れたあと、当たるまでの追加の回数
    w3 = more <= 100
    r3 = float(w3.mean())
    near(r3, 1 - th0, math.sqrt(th0 * (1 - th0) / N), "③次の100回")
    near(N / y_all_tried, Q ** 200, 0.004, "③200回外れる割合")
    out["e3"] = dict(tried=y_all_tried, win=int(w3.sum()), win_rate=round(r3, 4), win_theory=round(1 - th0, 4),
                     miss200_theory=round(Q ** 200, 4), more=np.minimum(more, 101).tolist())

    # ---- 実験④ 天井200（200回引いても出なければ、もらえる）。実験②と同じ1万人 ----
    capped = np.minimum(x, 200)
    reach = x > 200
    m4 = float(capped.mean())
    th4 = (1 - Q ** 200) / P
    near(m4, th4, capped.std() / math.sqrt(N), "④平均")
    near(float(reach.mean()), Q ** 200, math.sqrt(Q ** 200 * (1 - Q ** 200) / N), "④天井に届く人")
    out["e4"] = dict(cap=200, mean=round(m4, 1), mean_theory=round(th4, 1), reach=int(reach.sum()),
                     reach_rate=round(float(reach.mean()), 4), reach_theory=round(Q ** 200, 4),
                     worst=int(capped.max()), worst_nocap=int(x.max()), mean_nocap=round(mean, 1))

    # ---- 実験⑤ 全6種類 ----
    K = 6
    t5 = np.zeros(N, int); stage = np.zeros((N, K))
    seq0 = None
    for i in range(N):
        seen, n, last, s = set(), 0, 0, []
        while len(seen) < K:
            c = int(rng.integers(0, K)); n += 1; s.append(c)
            if c not in seen:
                stage[i, len(seen)] = n - last; last = n; seen.add(c)
        t5[i] = n
        if i == 0: seq0 = s
    th5 = K * sum(1 / k for k in range(1, K + 1))
    var5 = sum((1 - (K - k) / K) / ((K - k) / K) ** 2 for k in range(K))
    near(float(t5.mean()), th5, math.sqrt(var5 / N), "⑤平均")
    sm = stage.mean(0)
    for k in range(K):
        near(float(sm[k]), K / (K - k), 0.25, f"⑤{k + 1}種類目")
    out["e5"] = dict(k=K, t=t5.tolist(), mean=round(float(t5.mean()), 1), mean_theory=round(th5, 1), max=int(t5.max()),
                     min=int(t5.min()), min_count=int((t5 == t5.min()).sum()), median=int(np.median(t5)),
                     seq0=seq0, first=int(t5[0]), ten=t5[:10].tolist(),
                     stage=[round(float(v), 1) for v in sm], stage_theory=[round(K / (K - k), 1) for k in range(K)],
                     p90=int(np.sort(t5)[int(0.9 * N) - 1]), mode=int(np.bincount(t5).argmax()))
    json.dump(out, open(os.path.join(HERE, "results.json"), "w"), ensure_ascii=False)
    for k in ("e1", "e2", "e3", "e4", "e5"):
        print(k, {a: b for a, b in out[k].items() if not isinstance(b, (list, str)) or len(b) <= 10})


if __name__ == "__main__":
    main()
