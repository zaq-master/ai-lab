"""モンティ・ホール問題を「そのまま派」「選び直す派」で各1万回ためす（乱数の種 20261128）。
条件：司会は当たりの場所を知っていて、あなたが選ばなかった扉から必ず外れを1つ開ける
（当たりを選んでいた時は、残り2つの外れから半々で選ぶ）。
理論値：そのまま 1/3、選び直す 2/3。計算と一致するかを確かめて results.json に保存。
"""
import json
import os

import numpy as np

SEED, N = 20261128, 10000
HERE = os.path.dirname(os.path.abspath(__file__))


def play(rng, n, switch):
    car = rng.integers(0, 3, n)            # 当たりの扉
    pick = rng.integers(0, 3, n)           # あなたが最初に選ぶ扉
    coin = rng.integers(0, 2, n)           # 司会が外れを2つから選べる時の半々
    opened = np.empty(n, int)
    for i in range(n):
        cand = [d for d in range(3) if d != pick[i] and d != car[i]]
        opened[i] = cand[coin[i] % len(cand)]
        assert opened[i] != car[i] and opened[i] != pick[i]   # 必ず外れ・あなたの扉は開けない
    final = 3 - pick - opened if switch else pick
    return (final == car).astype(int)


def main():
    rng = np.random.default_rng(SEED)
    stay = play(rng, N, False)
    sw = play(rng, N, True)
    out = dict(seed=SEED, n=N, cond="司会は当たりを知っていて、あなたが選ばなかった扉から必ず外れを開ける")
    for name, w, th in (("stay", stay, 1 / 3), ("switch", sw, 2 / 3)):
        p = w.mean(); se = np.sqrt(th * (1 - th) / N)
        assert abs(p - th) < 3 * se, f"{name}: {p} が理論値 {th} から離れすぎ"
        out[name] = dict(rate=round(float(p), 4), wins=int(w.sum()), theory=round(th, 4),
                         at={str(k): int(w[:k].sum()) for k in (1, 10, 100, 1000, N)},
                         bits="".join(map(str, w.tolist())))
        print(name, p, "理論", round(th, 4), {k: int(w[:k].sum()) for k in (1, 10, 100, 1000, N)})
    out["ratio"] = round(out["switch"]["rate"] / out["stay"]["rate"], 3)
    print("ratio", out["ratio"])
    json.dump(out, open(os.path.join(HERE, "results.json"), "w"), ensure_ascii=False)


if __name__ == "__main__":
    main()
