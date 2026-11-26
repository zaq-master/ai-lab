"""確率のお話③「くじ引きは、先に引いた人が得？」の計算 → results.json
10本のくじ（当たり1本、または3本）を10人が順番に1本ずつ引く（戻さない・ズルなし）。
この「10人のくじ引き」を1万回くり返し、何番目の人が当たったかを数える。
理論値（計算の答え）：当たり1本なら全員 1/10、当たり3本なら全員 3/10。
実行：python3 sim.py
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SEED, N, K = 20261130, 10000, 10
rng = np.random.default_rng(SEED)

# 当たり1本：1回ごとに10本を並べ替え（＝引く順番）、当たりの位置を記録（0〜9 → 1〜10番目）
perm1 = np.array([rng.permutation(K) for _ in range(N)])        # perm1[r, j] = j番目の人が引いたくじの番号（0が当たり）
win1 = (perm1 == 0).argmax(axis=1)                               # 当たった人（0始まり）
cnt1 = np.bincount(win1, minlength=K)
# 当たり3本：くじ0,1,2 が当たり
perm3 = np.array([rng.permutation(K) for _ in range(N)])
hit3 = perm3 < 3                                                 # hit3[r, j] = j番目の人が当たったか
cnt3 = hit3.sum(axis=0)

# 「前の3人が外れたのを見た後」の4番目（当たり1本）
left = win1 >= 3                                                 # 4番目まで当たりが残っていた回
cond4 = float((win1[left] == 3).mean())

res = dict(
    seed=SEED, n=N, k=K,
    first_round=[int(x) for x in perm1[0]], first_winner=int(win1[0]) + 1,
    win1=[int(x) for x in win1],                                  # 1万回分、当たった人（0始まり）
    cnt1=[int(x) for x in cnt1], pct1=[round(float(x) / N, 4) for x in cnt1],
    cnt1_first10=[int(x) for x in np.bincount(win1[:10], minlength=K)],
    cnt1_first100=[int(x) for x in np.bincount(win1[:100], minlength=K)],
    cnt3=[int(x) for x in cnt3], pct3=[round(float(x) / N, 4) for x in cnt3],
    theory1=0.1, theory3=0.3,
    left4=int(left.sum()), win4_after3miss=int((win1[left] == 3).sum()), cond4=round(cond4, 4), theory_cond4=round(1 / 7, 4),
)
# 理論値との一致を確認（1万回なら差はほぼ±1%以内）
assert max(abs(p - 0.1) for p in res["pct1"]) < 0.012, res["pct1"]
assert max(abs(p - 0.3) for p in res["pct3"]) < 0.02, res["pct3"]
assert abs(cond4 - 1 / 7) < 0.015, cond4
assert cnt1.sum() == N and cnt3.sum() == 3 * N
json.dump(res, open(os.path.join(HERE, "results.json"), "w"), ensure_ascii=False)
print("1本:", res["pct1"]); print("3本:", res["pct3"])
print("最初の1回:", res["first_round"], "当たり", res["first_winner"], "番目")
print("10回:", res["cnt1_first10"], "100回:", res["cnt1_first100"])
print("3人外れの後の4番目:", res["left4"], res["win4_after3miss"], res["cond4"], "理論", res["theory_cond4"])
