"""第1回（5分版）：「1%のガチャ、100連で当たらない人は何人？」

仮の1万人にガチャを引いてもらう。乱数の種は固定＝誰が作っても同じ結果。
ナレーションの数字はすべて計算結果から自動で入れる（手で書かない）。
実行：python3 side/simvideo/ep001_gacha.py  → side/simvideo/out/ep001_gacha.mp4
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw

from engine import (W, H, FG, SUB, HIT, MISS, ACCENT, BLUE, Scene, render, text, ease)

N, P, SEED, YEN = 10_000, 0.01, 20261117, 300
rng = np.random.default_rng(SEED)
# 1万人 × 1000回 を実際に引く（全部の実験はこの同じ結果から数える）
M = rng.random((N, 1000)) < P
first = np.where(M.any(1), M.argmax(1) + 1, 0)
none = first == 0                          # 1000回でも出なかった人は続きを引く
first[none] = 1000 + rng.geometric(P, int(none.sum()))
order = rng.permutation(N)
grid_first = first[order].reshape(100, 100)


def left(t):
    return int((first > t).sum())


L50, L100, L500 = left(50), left(100), left(500)
theory100 = (1 - P) ** 100
n50 = math.ceil(math.log(0.5) / math.log(1 - P))
n90 = math.ceil(math.log(0.1) / math.log(1 - P))
n99 = math.ceil(math.log(0.01) / math.log(1 - P))
hit1, maxp = int((first == 1).sum()), int(first.max())

# 天井200回（200回目で必ず当たる）
CEIL = 200
pulls_ceil = np.minimum(first, CEIL)
avg_free, avg_ceil = first.mean(), pulls_ceil.mean()
worst_free, worst_ceil = int(first.max()) * YEN, CEIL * YEN
n_ceil = int((first >= CEIL).sum())       # 天井まで行った人

# 「次こそ当たる？」：100連はずれた人の、次の100回
unlucky = first > 100
next_rate_unlucky = ((first[unlucky] <= 200).mean())
fresh_rate = (first <= 100).mean()

# 3%のSSRを10連
rng2 = np.random.default_rng(SEED + 1)
ssr = (rng2.random((N, 10)) < 0.03).sum(1)
ssr0 = int((ssr == 0).sum())
ssr2p = int((ssr >= 2).sum())

# 100連で何回当たったか（運のいい人）
wins = M[:, :100].sum(1)                  # 同じ1万人の、最初の100回
w3p = int((wins >= 3).sum())
w5p = int((wins >= 5).sum())
wmax = int(wins.max())

# ---- 描画の部品 ----
CELL, GX, GY = 6, 150, 150
cellmask = np.zeros((CELL, CELL), bool)
cellmask[:5, :5] = True
bigmask = np.tile(cellmask, (100, 100))


def draw_grid(img, lit, dim=None, alpha=1.0):
    colors = np.empty((100, 100, 3), np.uint8)
    colors[:] = MISS
    colors[lit] = HIT
    if dim is not None:
        colors[dim] = (28, 34, 54)
    big = np.repeat(np.repeat(colors, CELL, 0), CELL, 1)
    base = np.array(img.crop((GX, GY, GX + 600, GY + 600)))
    base[bigmask] = (base[bigmask] * (1 - alpha) + big[bigmask] * alpha).astype(np.uint8)
    img.paste(Image.fromarray(base), (GX, GY))


def chapter(img, s):
    text(ImageDraw.Draw(img), (40, 30), s, 30, BLUE)


def stat(d, x, y, label, value, color):
    text(d, (x, y), label, 40, SUB)
    text(d, (x, y + 50), value, 90, color)


def run(a, b, hold=1.0, ch="実験1　100連"):
    def f(img, t, dur):
        k = ease(t / max(0.1, dur - hold))
        n = int(round(a + (b - a) * k))
        draw_grid(img, grid_first <= n)
        chapter(img, ch)
        d = ImageDraw.Draw(img)
        stat(d, 860, 150, "引いた回数", f"{n} 回", FG)
        stat(d, 860, 360, "当たった人", f"{N - left(n):,} 人", HIT)
        stat(d, 860, 570, "まだ当たらない人", f"{left(n):,} 人", ACCENT)
    return f


def center_lines(rows, ch=None):
    """rows: (出す時刻, y, 文字, 大きさ, 色)"""
    def f(img, t, dur):
        d = ImageDraw.Draw(img)
        if ch:
            chapter(img, ch)
        for t0, y, s, size, color in rows:
            if t >= t0:
                text(d, (W // 2, y), s, size, color, anchor="ma", stroke=1 if size >= 90 else 0)
    return f


# ---- 場面 ----
def s_title(img, t, dur):
    d = ImageDraw.Draw(img)
    a = ease(t / 0.8)
    text(d, (W // 2, 230), "当たり確率 1% のガチャ", 64, SUB, anchor="ma")
    text(d, (W // 2, 340), "100連で当たらない人は", 110, FG, anchor="ma", stroke=1)
    text(d, (W // 2, 500), "1万人中 何人？", int(150 * (0.8 + 0.2 * a)), HIT, anchor="ma", stroke=2)


def s_quiz(img, t, dur):
    d = ImageDraw.Draw(img)
    chapter(img, "クイズ")
    text(d, (W // 2, 140), "100連しても当たらない人は？", 70, FG, anchor="ma")
    for i, (k, v) in enumerate([("A", "約100人"), ("B", "約1,000人"), ("C", "約3,700人")]):
        x = 360 + i * 600
        d.rounded_rectangle([x - 240, 300, x + 240, 600], 30, outline=BLUE, width=4)
        text(d, (x, 340), k, 80, BLUE, anchor="ma")
        text(d, (x, 470), v, 64, FG, anchor="ma")
    if t > dur - 3.2:
        n = max(1, math.ceil(dur - 0.2 - t))
        text(d, (W // 2, 650), str(min(3, n)), 120, ACCENT, anchor="ma")


def s_intro(img, t, dur):
    draw_grid(img, grid_first <= 0, alpha=ease(t / 1.5))
    chapter(img, "実験1　100連")
    d = ImageDraw.Draw(img)
    text(d, (860, 230), "仮の1万人を用意", 64, FG)
    text(d, (860, 330), "1つの点 = 1人", 48, SUB)
    text(d, (860, 410), "全員が1%のガチャを", 48, SUB)
    text(d, (860, 475), "100回ずつ引く", 48, SUB)


def s_result(img, t, dur):
    draw_grid(img, grid_first <= 100)
    chapter(img, "実験1　100連")
    d = ImageDraw.Draw(img)
    text(d, (860, 170), "正解は C", 60, BLUE)
    text(d, (860, 250), "100連して当たらなかった人", 52, FG)
    text(d, (860, 330), f"{L100:,} 人", int(170 * (0.85 + 0.15 * ease(t / 0.6))), ACCENT, stroke=2)
    text(d, (860, 550), f"およそ {round(N / L100)} 人に 1 人", 64, FG)


def s_marks(img, t, dur):
    d = ImageDraw.Draw(img)
    chapter(img, "実験2　何回引けば安心？")
    text(d, (W // 2, 140), "何回引けば安心？", 72, FG, anchor="ma")
    rows = [("半分の人が当たる", f"{n50} 回"), ("9割の人が当たる", f"{n90} 回"),
            ("99%の人が当たる", f"{n99} 回"), ("500回でも外れ続けた人", f"{L500} 人")]
    for i, (k, v) in enumerate(rows):
        if t > 1.5 * i:
            y = 280 + i * 140
            text(d, (420, y), k, 60, SUB)
            text(d, (1500, y - 10), v, 90, ACCENT if i == 3 else HIT, anchor="ra")


def s_hist(img, t, dur):
    d = ImageDraw.Draw(img)
    chapter(img, "実験2　何回引けば安心？")
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


def s_ceil(img, t, dur):
    d = ImageDraw.Draw(img)
    chapter(img, f"実験3　天井{CEIL}回があると？")
    text(d, (W // 2, 120), f"1回{YEN}円・1万人が当たるまで引く", 52, SUB, anchor="ma")
    cols = [("天井なし", avg_free * YEN, worst_free, BLUE), (f"天井{CEIL}回", avg_ceil * YEN, worst_ceil, HIT)]
    k = ease(t / 2.0)
    for i, (name, avg, worst, color) in enumerate(cols):
        x = 560 + i * 800
        text(d, (x, 230), name, 64, FG, anchor="ma")
        text(d, (x, 340), "平均", 40, SUB, anchor="ma")
        text(d, (x, 390), f"{int(avg * k):,} 円", 88, color, anchor="ma")
        if t > 3:
            text(d, (x, 540), "いちばん運が悪い人", 40, SUB, anchor="ma")
            text(d, (x, 590), f"{worst:,} 円", 88, ACCENT, anchor="ma")


def s_gambler_final(img, t, dur):
    s_gambler(img, 999, 1)


def s_gambler(img, t, dur):
    k = ease(t / max(0.1, dur - 2))
    n = int(round(100 + 100 * k))
    draw_grid(img, (grid_first <= n) & (grid_first > 100), dim=grid_first <= 100)
    chapter(img, "実験5　「次こそ当たる」は本当？")
    d = ImageDraw.Draw(img)
    text(d, (860, 150), "100連はずれた人だけ", 48, SUB)
    text(d, (860, 210), f"{L100:,} 人", 80, ACCENT)
    text(d, (860, 340), "次の100回で当たった割合", 48, SUB)
    rate = ((first[unlucky] <= n).mean()) * 100
    text(d, (860, 400), f"{rate:.1f} %", 110, HIT)
    if t > dur - 2:
        text(d, (860, 580), f"最初の100回（全員）：{fresh_rate * 100:.1f} %", 44, BLUE)


def s_ssr(img, t, dur):
    d = ImageDraw.Draw(img)
    chapter(img, "実験6　SSR 3% を10連")
    text(d, (W // 2, 120), "SSRの確率3%、10連の中身（1万人）", 56, FG, anchor="ma")
    cnt = [int((ssr == i).sum()) for i in range(4)] + [int((ssr >= 4).sum())]
    labels = ["0枚", "1枚", "2枚", "3枚", "4枚以上"]
    x0, y0, bw, hmax = 330, 760, 260, 470
    k = ease(t / 2.0)
    for i, c in enumerate(cnt):
        h = int(c / max(cnt) * hmax * k)
        x = x0 + i * bw
        d.rectangle([x, y0 - h, x + bw - 50, y0], fill=ACCENT if i == 0 else HIT)
        text(d, (x + (bw - 50) // 2, y0 + 15), labels[i], 40, SUB, anchor="ma")
        if k > 0.95:
            text(d, (x + (bw - 50) // 2, y0 - h - 60), f"{c:,}人", 44, FG, anchor="ma")


def s_lucky(img, t, dur):
    d = ImageDraw.Draw(img)
    chapter(img, "実験4　運のいい人はどれくらい？")
    text(d, (W // 2, 120), "100連で何回当たった？（1万人）", 56, FG, anchor="ma")
    cnt = [int((wins == i).sum()) for i in range(5)] + [int((wins >= 5).sum())]
    labels = ["0回", "1回", "2回", "3回", "4回", "5回以上"]
    x0, y0, bw, hmax = 260, 760, 240, 470
    k = ease(t / 2.0)
    for i, c in enumerate(cnt):
        h = int(c / max(cnt) * hmax * k)
        x = x0 + i * bw
        d.rectangle([x, y0 - h, x + bw - 50, y0], fill=ACCENT if i == 0 else (BLUE if i >= 3 else HIT))
        text(d, (x + (bw - 50) // 2, y0 + 15), labels[i], 40, SUB, anchor="ma")
        if k > 0.95:
            text(d, (x + (bw - 50) // 2, y0 - h - 60), f"{c:,}人", 44, FG, anchor="ma")


def s_menu(img, t, dur):
    d = ImageDraw.Draw(img)
    chapter(img, "今日の実験")
    items = ["100連で当たらない人は何人？", "何回引けば安心？", f"天井{CEIL}回でいくら変わる？",
             "運のいい人はどれくらい？", "「次こそ当たる」は本当？", "SSR 3% の10連の中身"]
    for i, s in enumerate(items):
        if t > 0.9 * i:
            text(d, (360, 170 + i * 105), f"{i + 1}", 60, BLUE)
            text(d, (450, 170 + i * 105), s, 60, FG)


def s_summary(img, t, dur):
    d = ImageDraw.Draw(img)
    chapter(img, "まとめ")
    rows = [f"100連でも 約{round(N / L100)}人に1人は 当たらない",
            "外れ続けても、次が当たりやすくはならない",
            "天井は「平均」より「最悪」を小さくする"]
    for i, s in enumerate(rows):
        if t > 1.8 * i:
            text(d, (220, 230 + i * 170), f"{i + 1}.", 70, BLUE)
            text(d, (330, 230 + i * 170), s, 64, FG)


def s_outro(img, t, dur):
    d = ImageDraw.Draw(img)
    text(d, (W // 2, 300), "確率 1% は", 80, SUB, anchor="ma")
    text(d, (W // 2, 420), "「100回に1回当たる」", 100, FG, anchor="ma")
    text(d, (W // 2, 560), "ではない", 120, ACCENT, anchor="ma", stroke=2)
    text(d, (W // 2, 760), f"条件：1万人・乱数の種 {SEED}・1回{YEN}円と仮定", 32, SUB, anchor="ma")


pct = lambda x: f"{x * 100:.1f}パーセント"

SCENES = [
    Scene("当たり確率1パーセントのガチャ。100回引けば、さすがに当たる気がしますよね。", s_title, pad=0.8),
    Scene("今日は、仮の1万人に、本当にガチャを引いてもらいます。実験は6つ。100連で当たらない人の数から、天井の効果、そして、次こそ当たるは本当なのか、まで確かめます。", s_menu, pad=1.0),
    Scene("まずはクイズです。100連しても当たらない人は、1万人のうち何人でしょう。Aが約100人、Bが約1000人、Cが約3700人。3、2、1。", s_quiz, pad=1.0),
    Scene("では実験です。1つの点が1人。全員が、1パーセントのガチャを100回ずつ引きます。", s_intro),
    Scene("当たった人は光ります。10回、20回。思ったより光りません。", run(0, 30, hold=0.5)),
    Scene(f"50回で、当たった人は{N - L50}人。まだ半分にも届きません。そして、100回目。", run(30, 100, hold=1.2)),
    Scene(f"正解はCです。100回引いても当たらなかった人は、{L100}人。およそ{round(N / L100)}人に1人です。", s_result, pad=1.0),
    Scene(f"なぜでしょう。1回外れる確率は99パーセント。これが100回続く確率は、0.99を100回かけて、およそ{round(theory100 * 100)}パーセント。1万人の実験でも{pct(L100 / N)}で、ほぼ同じになりました。",
          center_lines([(0, 220, "1回外れる確率 = 99%", 80, FG), (3.5, 380, "100回続けて外れる確率", 60, SUB),
                        (3.5, 470, f"0.99 の 100乗 = {theory100 * 100:.1f}%", 110, ACCENT),
                        (8, 680, f"1万人の実験：{L100 / N * 100:.1f}%", 52, BLUE)], "なぜ？"), pad=1.2),
    Scene("1パーセントを100回引けば、確率は足し算で100パーセントになる。そう思いがちですが、当たる確率は足し算では増えません。外れが続く確率が、少しずつ小さくなるだけです。",
          center_lines([(0, 260, "1% × 100回 = 100% ？", 100, SUB), (3.5, 450, "足し算にはならない", 100, ACCENT),
                        (7, 640, "「外れ続ける確率」が少しずつ減るだけ", 56, FG)], "なぜ？"), pad=1.0),
    Scene("では、何回引けば安心なのか。続けて500回まで引いてもらいました。", run(100, 500, hold=1.0, ch="実験2　何回引けば安心？")),
    Scene(f"半分の人が当たるのは{n50}回。9割なら{n90}回、99パーセントなら{n99}回。それでも、500回外れ続けた人が{L500}人いました。", s_marks, pad=1.2),
    Scene(f"初めて当たるまでの回数を並べると、この形になります。いちばん多いのは、なんと1回目で{hit1}人。でも右に長く伸びています。全員が当たるまで引き続けたら、最後の1人は{maxp}回目でした。", s_hist, pad=1.2),
    Scene(f"ここで、天井を考えます。{CEIL}回引けば必ず当たる仕組みです。1回{YEN}円として、1万人が当たるまで引いたときのお金を比べます。天井なしの平均は{int(avg_free * YEN)}円。天井ありの平均は{int(avg_ceil * YEN)}円です。",
          s_ceil, pad=0.8),
    Scene(f"平均はあまり変わりません。違うのは、いちばん運が悪い人です。天井なしでは{worst_free}円。天井があれば、どんなに運が悪くても{worst_ceil}円で止まります。天井まで行った人は{n_ceil}人でした。", s_ceil, pad=1.2),
    Scene(f"今度は逆に、運のいい人を見てみます。1万人が100連して、何回当たったかを数えました。0回が{int((wins == 0).sum())}人、1回がいちばん多く{int((wins == 1).sum())}人。3回以上当たった人は{w3p}人、5回以上は{w5p}人でした。いちばん多い人は{wmax}回です。", s_lucky, pad=1.2),
    Scene(f"同じ確率でも、100連で{wmax}回当たる人と、1回も当たらない人が出ます。この差は、腕でも日頃の行いでもなく、ただの偶然です。", s_lucky, pad=1.2),
    Scene("次は、よく聞く言葉を確かめます。これだけ外れたんだから、次こそ当たるはず。本当でしょうか。100連外れた人だけに、続けて100回引いてもらいます。", s_gambler, pad=0.5),
    Scene(f"結果は{pct(next_rate_unlucky)}。最初の100回の全員の結果、{pct(fresh_rate)}と、ほとんど同じです。ガチャは前の結果を覚えていません。外れ続けても、次が当たりやすくはなりません。", s_gambler_final, pad=1.2),
    Scene(f"最後に、よくあるSSR3パーセントの10連です。1万人が10連を1回ずつ引くと、SSRが1枚も出ない人は{ssr0}人。{pct(ssr0 / N)}。4人に3人は、SSRなしです。2枚以上出た人は{ssr2p}人でした。", s_ssr, pad=1.2),
    Scene(f"まとめです。100連でも、およそ{round(N / L100)}人に1人は当たらない。外れ続けても、次が当たりやすくはならない。そして天井は、平均ではなく、最悪の場合を小さくする仕組みです。", s_summary, pad=1.2),
    Scene("確率1パーセントは、100回に1回当たる、ではありません。この動画は、AIがシミュレーションして作りました。次回もお楽しみに。", s_outro, pad=2.0),
]

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "out", "ep001_gacha.mp4")
    sec = render(SCENES, out)
    print(f"ok {out} {sec:.1f}s L100={L100} L500={L500} avg_free={avg_free:.1f} avg_ceil={avg_ceil:.1f} "
          f"next={next_rate_unlucky:.3f} fresh={fresh_rate:.3f} ssr0={ssr0} ssr2p={ssr2p} n_ceil={n_ceil}")
