"""第1回：「1%のガチャ、100連で当たらない人は何人？」

仮の1万人に、当たり確率1%のガチャを引いてもらう（乱数の種は固定＝誰が作っても同じ結果）。
ナレーションの数字はすべて、このシミュレーションの結果から自動で入れる。
実行：python3 side/simvideo/ep001_gacha.py  → side/simvideo/out/ep001_gacha.mp4
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw

from engine import (W, H, BG, FG, SUB, HIT, MISS, ACCENT, BLUE, Scene, render, text, ease)

N, P, SEED = 10_000, 0.01, 20261117
rng = np.random.default_rng(SEED)
first = rng.geometric(P, N)          # 各人が初めて当たった回数
rng_order = rng.permutation(N)       # 点の並びをばらす

def left(t):                          # t回引いて、まだ当たっていない人数
    return int((first > t).sum())

L100, L230, L459, L500 = left(100), left(230), left(459), left(500)
theory100 = (1 - P) ** 100
n90 = math.ceil(math.log(0.1) / math.log(1 - P))
n99 = math.ceil(math.log(0.01) / math.log(1 - P))
hit1 = int((first == 1).sum())
maxp = int(first.max())

# ---- 1万個の点 ----
CELL, GX, GY = 6, 150, 130
cell = np.zeros((CELL, CELL), bool)
cell[:5, :5] = True
grid_first = first[rng_order].reshape(100, 100)


def draw_grid(img, pulls, alpha=1.0):
    lit = grid_first <= pulls
    colors = np.empty((100, 100, 3), np.uint8)
    colors[:] = MISS
    colors[lit] = HIT
    big = np.repeat(np.repeat(colors, CELL, 0), CELL, 1)
    mask = np.tile(cell, (100, 100))
    base = np.array(img.crop((GX, GY, GX + 600, GY + 600)))
    out = base.copy()
    out[mask] = (base[mask] * (1 - alpha) + big[mask] * alpha).astype(np.uint8)
    img.paste(Image.fromarray(out), (GX, GY))


def panel(img, pulls):
    d = ImageDraw.Draw(img)
    x = 860
    text(d, (x, 150), "引いた回数", 40, SUB)
    text(d, (x, 200), f"{pulls} 回", 120, FG)
    text(d, (x, 380), "当たった人", 40, SUB)
    text(d, (x, 430), f"{N - left(pulls):,} 人", 90, HIT)
    text(d, (x, 580), "まだ当たらない人", 40, SUB)
    text(d, (x, 630), f"{left(pulls):,} 人", 90, ACCENT)


# ---- 場面 ----
def s_title(img, t, dur):
    d = ImageDraw.Draw(img)
    a = ease(t / 0.8)
    text(d, (W // 2, 250), "当たり確率 1% のガチャ", 64, SUB, anchor="ma")
    text(d, (W // 2, 360), "100連で当たらない人は", 110, FG, anchor="ma", stroke=1)
    text(d, (W // 2, 520), "1万人中 何人？", int(150 * (0.8 + 0.2 * a)), HIT, anchor="ma", stroke=2)


def s_intro(img, t, dur):
    draw_grid(img, 0, ease(t / 1.5))
    d = ImageDraw.Draw(img)
    text(d, (860, 250), "仮の1万人を用意", 64, FG)
    text(d, (860, 350), "1つの点 = 1人", 48, SUB)
    text(d, (860, 430), "全員が1%のガチャを", 48, SUB)
    text(d, (860, 495), "100回ずつ引く", 48, SUB)


def make_run(a, b, hold=1.0):
    def f(img, t, dur):
        k = ease(t / max(0.1, dur - hold))
        pulls = int(round(a + (b - a) * k))
        draw_grid(img, pulls)
        panel(img, pulls)
    return f


def s_result(img, t, dur):
    draw_grid(img, 100)
    d = ImageDraw.Draw(img)
    text(d, (860, 170), "100連して", 52, SUB)
    text(d, (860, 240), "当たらなかった人", 60, FG)
    text(d, (860, 340), f"{L100:,} 人", int(170 * (0.85 + 0.15 * ease(t / 0.6))), ACCENT, stroke=2)
    text(d, (860, 560), f"およそ {round(N / L100)} 人に 1 人", 64, FG)


def s_why(img, t, dur):
    d = ImageDraw.Draw(img)
    text(d, (W // 2, 170), "なぜ？", 64, SUB, anchor="ma")
    text(d, (W // 2, 290), "1回外れる確率 = 99%", 80, FG, anchor="ma")
    if t > 2.5:
        text(d, (W // 2, 430), "100回続けて外れる確率", 64, SUB, anchor="ma")
        text(d, (W // 2, 520), f"0.99 の 100乗 = {theory100 * 100:.1f}%", 110, ACCENT, anchor="ma", stroke=1)
    if t > 6:
        text(d, (W // 2, 700), f"シミュレーション：{L100 / N * 100:.1f}%（ほぼ一致）", 48, BLUE, anchor="ma")


def s_marks(img, t, dur):
    d = ImageDraw.Draw(img)
    text(d, (W // 2, 140), "何回引けば安心？", 72, FG, anchor="ma")
    rows = [("半分の人が当たる", "69 回"), ("9割の人が当たる", f"{n90} 回"),
            ("99%の人が当たる", f"{n99} 回"), ("500回でも外れ続けた人", f"{L500} 人")]
    for i, (k, v) in enumerate(rows):
        if t > 1.2 * i:
            y = 290 + i * 150
            text(d, (420, y), k, 60, SUB)
            text(d, (1500, y - 10), v, 90, ACCENT if i == 3 else HIT, anchor="ra")


def s_hist(img, t, dur):
    d = ImageDraw.Draw(img)
    text(d, (W // 2, 110), "初めて当たるまでの回数（1万人）", 56, FG, anchor="ma")
    bins = np.arange(0, 520, 20)
    cnt, _ = np.histogram(np.minimum(first, 509), bins)
    x0, y0, bw, hmax = 260, 800, 54, 560
    k = ease(t / 2.5)
    for i, c in enumerate(cnt):
        h = int(c / cnt.max() * hmax * k)
        d.rectangle([x0 + i * bw, y0 - h, x0 + i * bw + bw - 8, y0], fill=HIT if i < 5 else BLUE)
    for v in (0, 100, 200, 300, 400, 500):
        text(d, (x0 + v / 20 * bw, y0 + 15), f"{v}", 36, SUB, anchor="ma")
    text(d, (x0 + 26 * bw, y0 + 15), "回", 36, SUB)
    if t > 3:
        text(d, (1150, 260), f"最後の1人：{maxp} 回目", 56, ACCENT)


def s_outro(img, t, dur):
    d = ImageDraw.Draw(img)
    text(d, (W // 2, 300), "確率 1% は", 80, SUB, anchor="ma")
    text(d, (W // 2, 420), "「100回に1回当たる」", 100, FG, anchor="ma")
    text(d, (W // 2, 560), "ではない", 120, ACCENT, anchor="ma", stroke=2)
    text(d, (W // 2, 780), f"条件：1万人・全員が当たるまで・乱数の種 {SEED}", 32, SUB, anchor="ma")


SCENES = [
    Scene("当たり確率1パーセントのガチャ。100回引けば、さすがに当たる気がしますよね。", s_title, pad=0.8),
    Scene("では本当に試してみましょう。仮の1万人に、100回ずつ引いてもらいます。1つの点が1人です。", s_intro),
    Scene("当たった人は光ります。10回、20回。思ったより光りません。", make_run(0, 30, hold=0.5)),
    Scene("50回で、やっと4割ほど。そして、100回目。", make_run(30, 100, hold=1.2)),
    Scene(f"100回引いても当たらなかった人は、{L100}人。およそ{round(N / L100)}人に1人です。", s_result, pad=1.0),
    Scene(f"1回外れる確率は99パーセント。これが100回続く確率は、0.99の100乗で、およそ{round(theory100 * 100)}パーセント。シミュレーションとほぼ同じです。", s_why, pad=1.0),
    Scene("では、何回引けば安心なのか。続けて500回まで引いてもらいました。", make_run(100, 500, hold=1.0)),
    Scene(f"半分の人が当たるのは69回。9割なら{n90}回、99パーセントなら{n99}回。それでも500回外れ続けた人が、{L500}人いました。", s_marks, pad=1.0),
    Scene(f"これが、初めて当たるまでの回数の分布です。いちばん多いのは1回目で、{hit1}人。でも右に長く伸びています。全員が当たるまで引き続けたら、最後の1人は{maxp}回目でした。", s_hist, pad=1.0),
    Scene("確率1パーセントは、100回に1回当たる、ではありません。この動画は、AIがシミュレーションして作りました。", s_outro, pad=1.5),
]

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "out", "ep001_gacha.mp4")
    sec = render(SCENES, out)
    print(f"ok {out} {sec:.1f}s  L100={L100} L500={L500} hit1={hit1} max={maxp}")
