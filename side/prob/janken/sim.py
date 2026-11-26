"""「n人でじゃんけん、1回で決まる確率は？」のシミュレーション（全員ランダムに手を出す前提）。
決まる＝あいこにならない＝出た手がちょうど2種類。乱数の種 20261129、各1万回。
理論値：1回で決まる確率 3×(2^n−2)/3^n、決まるまでの平均回数はその逆数。
おまけ：10人から1人を決めるまでの合計回数（いっぺん vs 5人ずつ2組で代表→決勝）。理論値は漸化式で計算。
実行：python3 sim.py → results.json
"""
import json
import os
from math import comb

import numpy as np

SEED, N = 20261129, 10000
HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(SEED)


def p_dec(n):
    return 3 * (2 ** n - 2) / 3 ** n


def kinds(hands):
    """hands: (回数, 人数) の 0=グー 1=チョキ 2=パー → 出た手の種類の数"""
    return (hands[:, :, None] == np.arange(3)).any(1).sum(1)


def one_winner_rounds(n):
    """n人から勝ち残り1人が決まるまでの回数（1ゲーム）"""
    r = 0
    while n > 1:
        h = rng.integers(0, 3, n); r += 1
        u = np.unique(h)
        if len(u) == 2:   # 2種類 → 勝った手を出した人が残る（グー>チョキ, チョキ>パー, パー>グー）
            a, b = u
            win = a if (a, b) in ((0, 1), (1, 2)) else b
            n = int((h == win).sum())
    return r


E1 = {1: 0.0}
for n in range(2, 11):   # 1人が決まるまでの平均回数（理論）
    pa = 1 - p_dec(n)
    E1[n] = (1 + sum(3 * comb(n, k) / 3 ** n * E1[k] for k in range(1, n))) / (1 - pa)

out = dict(seed=SEED, trials=N, people={}, cond="全員がグー・チョキ・パーを3分の1ずつランダムに出す")
for n in range(2, 11):
    h = rng.integers(0, 3, (N, n))
    k = kinds(h)
    dec = k == 2
    # 決まるまでの回数（1万ゲーム）：1回ごとに p で決まる → 回数を数える
    games = []
    for _ in range(N):
        r = 1
        while kinds(rng.integers(0, 3, (1, n)))[0] != 2:
            r += 1
        games.append(r)
    games = np.array(games)
    d = dict(n=n, p_sim=round(float(dec.mean()), 4), p_theory=round(p_dec(n), 4),
             rounds_sim=round(float(games.mean()), 3), rounds_theory=round(1 / p_dec(n), 3),
             all_same=round(float((k == 1).mean()), 4), three=round(float((k == 3).mean()), 4),
             ways=3 ** n, ways_dec=3 * (2 ** n - 2), ways_same=3, ways_three=3 ** n - 3 - 3 * (2 ** n - 2))
    if n == 5:   # 画面で見せる5人の1万回：手（先頭10回）と決まったかどうか（全部）
        out["five_hands10"] = h[:10].tolist()
        out["five_dec"] = "".join("1" if x else "0" for x in dec)
        out["five_first10"] = int(dec[:10].sum()); out["five_first100"] = int(dec[:100].sum()); out["five_all"] = int(dec.sum())
    if n == 10:
        out["ten_games_first"] = games[:40].tolist()
    out["people"][n] = d
    assert abs(d["p_sim"] - d["p_theory"]) < 0.015, (n, d)
    assert abs(d["rounds_sim"] - d["rounds_theory"]) / d["rounds_theory"] < 0.05, (n, d)
    print(n, d)

# 10人から1人を決める：いっぺん vs 5人ずつ2組（それぞれ1人に）→ 代表2人で決勝。回数は全部足す（同時にやらない前提）
all10 = np.array([one_winner_rounds(10) for _ in range(N)])
split = np.array([one_winner_rounds(5) + one_winner_rounds(5) + one_winner_rounds(2) for _ in range(N)])
out["pick1"] = dict(all10_sim=round(float(all10.mean()), 3), all10_theory=round(E1[10], 3),
                    split_sim=round(float(split.mean()), 3), split_theory=round(2 * E1[5] + E1[2], 3),
                    split_faster=round(float((split < all10).mean()), 4))
assert abs(out["pick1"]["all10_sim"] - E1[10]) / E1[10] < 0.05 and abs(out["pick1"]["split_sim"] - (2 * E1[5] + E1[2])) / (2 * E1[5] + E1[2]) < 0.05
print(out["pick1"])
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), ensure_ascii=False, indent=1)
