"""パチンコ実機シミュレーション 第1回：e東京喰種（ビスティ）を1万人で打ってみた。

スペック（公開情報。出典は SPEC["sources"]。メーカー公式PDFは未照合）
  通常時：図柄揃い 1/399.9、喰種チャージ 1/399.9（合算 1/199.9）
  図柄揃い：50% 約1500個→HYPER喰種RUSH ／ 1% 約300個→RUSH ／ 49% 約1500個→通常
  喰種チャージ：約300個→通常（まれにRUSHへ昇格。割合が非公開のため0%として扱う）
  RUSH：ST130回・1/95.3（継続率 約74.6%）、大当たりは 3% 約6000個 ／ 97% 約3000個
仮定（動画内に表示）：等価（1玉4円）、通常時の回転率は1000円あたり16回（損益の分かれ目付近）、1日＝通常時2000回転、
  RUSH中の玉の増減は0として扱う。
実行：python3 side/simvideo/pachi_tg.py → out/pachi_tg.mp4
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from engine import (W, H, FG, SUB, HIT, ACCENT, BLUE, Scene, Host, render, text, ease, font)

SPEC = {
    "name": "e東京喰種",
    "maker": "ビスティ",
    "p_zoro": 1 / 399.9, "p_charge": 1 / 399.9,
    "zoro": [(0.50, 1500, True), (0.01, 300, True), (0.49, 1500, False)],
    "charge_pay": 300,
    "st": 130, "p_rush": 1 / 95.3,
    "rush_pay": [(0.03, 6000), (0.97, 3000)],
    "sources": ["https://nana-press.com/kaiseki/machine/933/",
                "https://nana-press.com/kaiseki/machine/933/30215/",
                "https://p-town.dmm.com/specials/news/8623",
                "https://web-greenbelt.jp/post-95432/"],
}
N, SEED, YEN_BALL, RATE, SPINS = 10_000, 20261118, 4, 16, 2000
rng = np.random.default_rng(SEED)
C = 1 - (1 - SPEC["p_rush"]) ** SPEC["st"]           # RUSHの継続率


def rush_balls(R):
    """R回のRUSHをまとめて消化：(当たり回数, 出玉)"""
    R = np.asarray(R)
    K = np.zeros(R.shape, int)
    pos = R > 0                                        # RUSHが0回の人は当たり0
    K[pos] = rng.negative_binomial(R[pos], 1 - C)
    big = rng.binomial(K, SPEC["rush_pay"][0][0])
    return K, 3000 * K + 3000 * big


# ---- 実験1：図柄揃い1万回 ----
cat = rng.choice(3, N, p=[z[0] for z in SPEC["zoro"]])
enter = cat < 2
K1 = np.zeros(N, int)
K1[enter] = rng.geometric(1 - C, enter.sum()) - 1     # RUSH中に当たった回数
big1 = rng.binomial(K1, 0.03)
pay1 = np.where(cat == 1, 300, 1500) + 3000 * K1 + 3000 * big1
enter_rate = enter.mean()
avg_rush = pay1[enter].mean()
chain_max = int(K1.max())
chain_cnt = [int(((K1 == k) & enter).sum()) for k in range(0, 8)] + [int(((K1 >= 8) & enter).sum())]
over10k = int((pay1 >= 10000).sum())


# ---- 実験2〜4：1万人が打つ ----
def play(days=1, rate=RATE, n=N):
    spins = SPINS * days
    nz = rng.binomial(spins, SPEC["p_zoro"], n)
    nc = rng.binomial(spins, SPEC["p_charge"], n)
    m = np.array([rng.multinomial(k, [z[0] for z in SPEC["zoro"]]) for k in nz])
    R = m[:, 0] + m[:, 1]
    K, rb = rush_balls(R)
    balls = 1500 * (m[:, 0] + m[:, 2]) + 300 * m[:, 1] + SPEC["charge_pay"] * nc + rb
    yen = balls * YEN_BALL - spins / rate * 1000
    return yen, nz + nc, R


day, hits_day, R_day = play()
win_day = (day > 0).mean()
avg_day, med_day = day.mean(), np.median(day)
best_day, worst_day = day.max(), day.min()
norush_day = (R_day == 0).mean()
rates = {r: play(rate=r) for r in (14, 16, 18)}
month, _, _ = play(days=20)
win_month, avg_month = (month > 0).mean(), month.mean()
# RUSHに入るまでの通常回転数（1万人）
p_enter = SPEC["p_zoro"] * (SPEC["zoro"][0][0] + SPEC["zoro"][1][0])
to_rush = rng.geometric(p_enter, N)
to_rush_yen = to_rush / RATE * 1000                    # 出玉を使わずに打った場合の目安
q50, q90 = np.percentile(to_rush, 50), np.percentile(to_rush, 90)
over2000 = (to_rush > 2000).mean()
deep = int(to_rush.max())
border = 1000 / (((sum(z[0] * z[1] for z in SPEC["zoro"]) + (0.51) * (3000 * (1 + 0.03)) * C / (1 - C))
                  * SPEC["p_zoro"] + SPEC["charge_pay"] * SPEC["p_charge"]) * YEN_BALL)


def man(y):                                           # 円 → 「+1.2万円」
    return f"{'+' if y >= 0 else '−'}{abs(y) / 10000:.1f}万円"


def man_say(y):
    return f"{'プラス' if y >= 0 else 'マイナス'}{abs(y) / 10000:.1f}万円"


# ---- 見た目 ----
VIOLET = (176, 140, 255)
CX0, CX1 = 90, 1270                                   # 左側の内容エリア（右はアリス）


def make_bg():
    bg = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(bg)
    for y in range(H):
        k = y / H
        d.line([(0, y), (W, y)], fill=(int(14 + 10 * k), int(18 + 8 * k), int(40 + 22 * k)))
    for x in range(0, W, 48):
        for y in range(0, H, 48):
            d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(40, 52, 92))
    glow = Image.new("RGB", (W, H))
    ImageDraw.Draw(glow).ellipse([1250, 120, 1900, 980], fill=(40, 60, 140))
    return Image.blend(bg, glow.filter(ImageFilter.GaussianBlur(120)), 0.35)


def card(d, box, title=None):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, 28, fill=(22, 30, 58), outline=(70, 88, 150), width=3)
    if title:
        text(d, (x0 + 36, y0 + 26), title, 36, VIOLET)


def chapter(d, s):
    d.rounded_rectangle([60, 40, 60 + 20 + len(s) * 32, 92], 24, fill=(46, 64, 140))
    text(d, (80, 48), s, 30, FG)


def machine(img, x, y, s=1.0, t=0.0):
    """オリジナルの台のイラスト（実在機の画像は使わない）。"""
    d = ImageDraw.Draw(img)
    w, h = int(420 * s), int(640 * s)
    d.rounded_rectangle([x, y, x + w, y + h], int(40 * s), fill=(30, 36, 70), outline=(150, 170, 255), width=6)
    d.rounded_rectangle([x + 24 * s, y + 24 * s, x + w - 24 * s, y + h * 0.62], int(30 * s), fill=(12, 16, 34))
    for i in range(9):
        for j in range(6):
            cx = x + 50 * s + j * 64 * s + (32 * s if i % 2 else 0)
            cy = y + 50 * s + i * 34 * s
            if cx < x + w - 50 * s:
                d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(200, 200, 220))
    lx0, ly0, lx1, ly1 = x + 90 * s, y + 110 * s, x + w - 90 * s, y + 300 * s
    d.rounded_rectangle([lx0, ly0, lx1, ly1], int(16 * s), fill=(40, 30, 90), outline=VIOLET, width=4)
    digits = "777" if (t % 2.4) > 1.6 else "".join(str(int((t * 13 + k * 3) % 9) + 1) for k in range(3))
    text(d, ((lx0 + lx1) / 2, ly0 + 30 * s), digits, int(110 * s), HIT if digits == "777" else FG, anchor="ma")
    d.rounded_rectangle([x + 40 * s, y + h * 0.68, x + w - 40 * s, y + h * 0.80], int(20 * s), fill=(54, 64, 118))
    d.ellipse([x + w - 120 * s, y + h * 0.84, x + w - 40 * s, y + h * 0.96], fill=(90, 100, 160), outline=(170, 180, 230), width=3)
    text(d, (x + 60 * s, y + h * 0.86), "1/399.9", int(40 * s), HIT)


def bars(d, box, vals, labels, colors, fmt, k=1.0, label_size=32):
    x0, y0, x1, y1 = box
    n = len(vals)
    bw = (x1 - x0) / n
    vmax = max(vals) or 1
    for i, v in enumerate(vals):
        h = (y1 - y0 - 70) * v / vmax * k
        bx = x0 + i * bw + bw * 0.15
        if h > 2:
            d.rounded_rectangle([bx, y1 - h, bx + bw * 0.7, y1], 10, fill=colors[i])
        text(d, (bx + bw * 0.35, y1 + 12), labels[i], label_size, SUB, anchor="ma")
        if k > 0.9:
            text(d, (bx + bw * 0.35, y1 - h - 44), fmt(v), 30, FG, anchor="ma")


# ---- 場面 ----
def s_open(img, t, dur):
    machine(img, 160, 210, 1.0, t)
    d = ImageDraw.Draw(img)
    text(d, (700, 260), "パチンコ実機を", 56, SUB)
    text(d, (700, 330), "1万人で", 92, FG, stroke=1)
    text(d, (700, 440), "打ってみた", 92, FG, stroke=1)
    a = ease(t / 1.0)
    text(d, (700, 590), SPEC["name"], int(110 * (0.85 + 0.15 * a)), HIT, stroke=2)


def s_spec(img, t, dur):
    d = ImageDraw.Draw(img)
    chapter(d, "スペック")
    card(d, [CX0, 130, CX1, 830], f"{SPEC['name']}（{SPEC['maker']}）")
    rows = [("当たり確率（合算）", "1/199.9"), ("　うち図柄揃い", "1/399.9"), ("　うち喰種チャージ（約300個）", "1/399.9"),
            ("RUSH突入（図柄揃いの）", "約51%"), ("RUSH", "130回転・1/95.3"), ("RUSH継続率", f"約{C * 100:.0f}%"),
            ("RUSH中の大当たり", "約3000個（3%で約6000個）")]
    for i, (k, v) in enumerate(rows):
        if t > 0.6 * i:
            y = 210 + i * 80
            text(d, (CX0 + 40, y), k, 40, SUB)
            text(d, (CX1 - 40, y - 4), v, 46, FG, anchor="ra")
    text(d, (CX0 + 40, 785), "出典：攻略サイト各種（メーカー公式資料とは未照合）", 26, SUB)


def s_trick(img, t, dur):
    d = ImageDraw.Draw(img)
    chapter(d, "ここがポイント")
    text(d, (680, 200), "当たりの半分は", 60, SUB, anchor="ma")
    text(d, (680, 290), "約300個のチャージ", 84, ACCENT, anchor="ma", stroke=1)
    if t > 3:
        text(d, (680, 470), "RUSHに入るのは", 60, SUB, anchor="ma")
        text(d, (680, 560), f"約 1/{399.9 / 0.51:.0f}", 120, HIT, anchor="ma", stroke=2)


def s_lt(img, t, dur):
    d = ImageDraw.Draw(img)
    chapter(d, "LT（ラッキートリガー）とは")
    card(d, [CX0, 130, CX1, 830])
    steps = [("通常時", "1/199.9で当たり", SUB), ("RUSH", "ここに入ると", HIT), ("LT", "上位の出玉モード", ACCENT)]
    for i, (a, b, c) in enumerate(steps):
        if t > 1.4 * i:
            x = CX0 + 60 + i * 380
            d.rounded_rectangle([x, 300, x + 320, 560], 26, fill=(32, 42, 80), outline=c, width=4)
            text(d, (x + 160, 360), a, 64, c, anchor="ma")
            text(d, (x + 160, 470), b, 34, FG, anchor="ma")
            if i < 2:
                d.polygon([(x + 330, 410), (x + 365, 430), (x + 330, 450)], fill=SUB)
    if t > 5:
        text(d, (680, 640), "この台は RUSH に入れば、そのまま LT", 46, HIT, anchor="ma")
        text(d, (680, 720), "RUSH中の大当たりは すべて約3000個以上", 36, SUB, anchor="ma")


def s_cost(img, t, dur):
    d = ImageDraw.Draw(img)
    chapter(d, "実験2　RUSHまで何回転？")
    card(d, [CX0, 130, CX1, 830], "RUSHに入るまでの通常回転数（1万人）")
    edges = np.arange(0, 3001, 250)
    cnt, _ = np.histogram(np.minimum(to_rush, 2999), edges)
    labels = [f"{e}" for e in edges[:-1]]
    labels[-1] = "2750〜"
    bars(d, [CX0 + 30, 300, CX1 - 30, 720], list(cnt), labels,
         [HIT if e < q50 else (BLUE if e < q90 else ACCENT) for e in edges[:-1]], lambda v: f"{v:,}", ease(t / 2), 24)
    if t > 3:
        text(d, (CX1 - 40, 200), f"半分の人：{q50:.0f}回転まで", 36, HIT, anchor="ra")
        text(d, (CX1 - 40, 245), f"1割の人は {q90:.0f}回転以上", 36, ACCENT, anchor="ra")


def s_cost2(img, t, dur):
    d = ImageDraw.Draw(img)
    chapter(d, "実験2　RUSHまでいくら？")
    card(d, [CX0, 130, CX1, 830], f"1000円で{RATE}回転・出玉を使わずに打った場合の目安")
    rows = [("平均", f"{to_rush.mean():.0f}回転", f"約{to_rush_yen.mean() / 10000:.1f}万円"),
            ("半分の人", f"{q50:.0f}回転", f"約{q50 / RATE * 1000 / 10000:.1f}万円"),
            ("遅いほうの1割", f"{q90:.0f}回転", f"約{q90 / RATE * 1000 / 10000:.1f}万円"),
            ("いちばんハマった人", f"{deep:,}回転", f"約{deep / RATE * 1000 / 10000:.0f}万円")]
    for i, (a, b, c) in enumerate(rows):
        if t > 1.3 * i:
            y = 230 + i * 140
            text(d, (CX0 + 50, y + 12), a, 38, SUB)
            text(d, (CX0 + 760, y), b, 58, FG, anchor="ra")
            text(d, (CX1 - 50, y), c, 60, ACCENT if i == 3 else HIT, anchor="ra")


def s_exp1_run(img, t, dur):
    d = ImageDraw.Draw(img)
    chapter(d, "実験1　図柄揃いを1万回")
    k = ease(t / max(0.5, dur - 1))
    n = int(N * k)
    card(d, [CX0, 130, CX1, 830])
    # 1万人を100x100の点で：RUSHに入った人は光る
    sub = enter[:n]
    cell = 6
    arr = np.full((100, 100, 3), (52, 62, 92), np.uint8)
    flat = arr.reshape(-1, 3)
    flat[:n][sub] = HIT
    flat[:n][~sub] = (90, 100, 140)
    big = np.repeat(np.repeat(arr, cell, 0), cell, 1)
    img.paste(Image.fromarray(big), (CX0 + 50, 180))
    text(d, (CX0 + 720, 220), "図柄揃い", 40, SUB)
    text(d, (CX0 + 720, 270), f"{n:,} 回", 80, FG)
    text(d, (CX0 + 720, 420), "RUSH突入", 40, SUB)
    text(d, (CX0 + 720, 470), f"{int(sub.sum()):,} 回", 80, HIT)
    if n:
        text(d, (CX0 + 720, 580), f"{sub.mean() * 100:.1f}%", 64, HIT)


def s_exp1_chain(img, t, dur):
    d = ImageDraw.Draw(img)
    chapter(d, "実験1　RUSHで何回当たった？")
    card(d, [CX0, 130, CX1, 830], f"RUSHに入った {int(enter.sum()):,} 回の内訳")
    labels = [f"{k}回" for k in range(8)] + ["8回〜"]
    cols = [ACCENT] + [HIT] * 3 + [BLUE] * 5
    bars(d, [CX0 + 30, 260, CX1 - 30, 740], chain_cnt, labels, cols, lambda v: f"{v:,}", ease(t / 2))
    if t > 3:
        text(d, (CX1 - 40, 200), f"最高 {chain_max} 連続", 40, ACCENT, anchor="ra")


def s_exp1_avg(img, t, dur):
    d = ImageDraw.Draw(img)
    chapter(d, "実験1　RUSHの出玉")
    card(d, [CX0, 130, CX1, 830])
    text(d, (680, 220), "RUSHに入ったときの平均出玉", 52, SUB, anchor="ma")
    text(d, (680, 300), f"約 {avg_rush:,.0f} 個", 130, HIT, anchor="ma", stroke=2)
    if t > 3:
        text(d, (680, 520), "1万個を超えたのは", 52, SUB, anchor="ma")
        text(d, (680, 590), f"1万回中 {over10k:,} 回", 90, FG, anchor="ma")


def hist_yen(d, box, yen, k, title):
    x0, y0, x1, y1 = box
    edges = np.arange(-100000, 150001, 10000)
    cnt, _ = np.histogram(np.clip(yen, -99999, 149999), edges)
    bw = (x1 - x0) / len(cnt)
    for i, c in enumerate(cnt):
        h = (y1 - y0 - 40) * c / cnt.max() * k
        lo = edges[i]
        col = BLUE if lo >= 0 else ACCENT
        d.rounded_rectangle([x0 + i * bw + 3, y1 - h, x0 + (i + 1) * bw - 3, y1], 6, fill=col)
    for v in (-100000, -50000, 0, 50000, 100000, 150000):
        x = x0 + (v - edges[0]) / 10000 * bw
        lab = f"{v // 10000:+d}万" if v else "0"
        lab = lab + "以下" if v == edges[0] else (lab + "以上" if v == edges[-1] else lab)
        text(d, (x, y1 + 12), lab, 28, SUB, anchor="ma")
    text(d, (x0, y0 - 50), title, 34, VIOLET)


def s_exp2(img, t, dur):
    d = ImageDraw.Draw(img)
    chapter(d, "実験3　1万人が1日打つ")
    card(d, [CX0, 130, CX1, 830])
    hist_yen(d, [CX0 + 50, 330, CX1 - 50, 720], day, ease(t / 2.5), "1日の収支（1万人）")
    text(d, (CX0 + 50, 170), f"勝った人 {win_day * 100:.1f}%", 64, BLUE if win_day >= 0.5 else ACCENT)
    text(d, (CX1 - 50, 190), f"平均 {man(avg_day)}", 44, FG, anchor="ra")
    text(d, (CX0 + 50, 770), f"仮定：等価・1000円で{RATE}回転・通常時{SPINS}回転", 26, SUB)


def s_exp2_ext(img, t, dur):
    d = ImageDraw.Draw(img)
    chapter(d, "実験3　1万人が1日打つ")
    card(d, [CX0, 130, CX1, 830])
    rows = [("いちばん勝った人", man(best_day), BLUE), ("いちばん負けた人", man(worst_day), ACCENT),
            ("真ん中の人", man(med_day), FG), ("RUSHに1回も入らなかった人", f"{norush_day * 100:.0f}%", ACCENT)]
    for i, (k, v, c) in enumerate(rows):
        if t > 1.2 * i:
            y = 210 + i * 150
            text(d, (CX0 + 50, y), k, 44, SUB)
            text(d, (CX1 - 50, y + 40), v, 80, c, anchor="ra")


def s_exp3(img, t, dur):
    d = ImageDraw.Draw(img)
    chapter(d, "実験4　回転率で変わる？")
    card(d, [CX0, 130, CX1, 830], "1000円あたりの回転数ごとに、1万人が1日")
    for i, r in enumerate((14, 16, 18)):
        if t > 1.5 * i:
            yen = rates[r][0]
            x = CX0 + 80 + i * 380
            text(d, (x + 150, 230), f"{r}回転", 56, FG, anchor="ma")
            text(d, (x + 150, 330), "勝った人", 34, SUB, anchor="ma")
            text(d, (x + 150, 375), f"{(yen > 0).mean() * 100:.1f}%", 80, HIT, anchor="ma")
            text(d, (x + 150, 500), "平均", 34, SUB, anchor="ma")
            text(d, (x + 150, 545), man(yen.mean()), 64, BLUE if yen.mean() >= 0 else ACCENT, anchor="ma")
    if t > 5:
        text(d, (680, 730), f"この計算での損益の分かれ目：約{border:.1f}回転", 40, VIOLET, anchor="ma")


def s_exp4(img, t, dur):
    d = ImageDraw.Draw(img)
    chapter(d, "実験5　1ヶ月（20日）打つ")
    card(d, [CX0, 130, CX1, 830])
    edges = np.arange(-600000, 800001, 50000)
    cnt, _ = np.histogram(np.clip(month, -599999, 799999), edges)
    x0, y0, x1, y1 = CX0 + 50, 330, CX1 - 50, 720
    bw = (x1 - x0) / len(cnt)
    k = ease(t / 2.5)
    for i, c in enumerate(cnt):
        h = (y1 - y0 - 40) * c / cnt.max() * k
        d.rounded_rectangle([x0 + i * bw + 3, y1 - h, x0 + (i + 1) * bw - 3, y1], 6,
                            fill=BLUE if edges[i] >= 0 else ACCENT)
    for v in (-600000, -300000, 0, 300000, 600000, 800000):
        lab = f"{v // 10000:+d}万" if v else "0"
        lab = lab + "以下" if v == -600000 else (lab + "以上" if v == 800000 else lab)
        text(d, (x0 + (v - edges[0]) / 50000 * bw, y1 + 12), lab, 28, SUB, anchor="ma")
    text(d, (CX0 + 50, 170), f"勝った人 {win_month * 100:.1f}%", 64, BLUE if win_month >= 0.5 else ACCENT)
    text(d, (CX1 - 50, 190), f"平均 {man(avg_month)}", 44, FG, anchor="ra")


def s_summary(img, t, dur):
    d = ImageDraw.Draw(img)
    chapter(d, "まとめ")
    card(d, [CX0, 130, CX1, 830])
    rows = [f"当たりの半分はチャージ。RUSHは約1/{399.9 / 0.51:.0f}",
            f"RUSHに入れば平均 約{avg_rush:,.0f}個",
            f"1日の勝率は {win_day * 100:.0f}%（{RATE}回転・等価）",
            "回転率しだいで、平均収支の向きが変わる"]
    for i, s in enumerate(rows):
        if t > 1.6 * i:
            text(d, (CX0 + 50, 210 + i * 140), f"{i + 1}", 60, VIOLET)
            text(d, (CX0 + 130, 218 + i * 140), s, 44, FG)


def s_end(img, t, dur):
    d = ImageDraw.Draw(img)
    card(d, [CX0, 160, CX1, 800])
    lines = ["この動画はAIがシミュレーションして制作しています", "数値は公開情報から。実際の台・お店の条件で変わります",
             "必勝法ではありません。18歳未満は遊技できません", f"条件：1万人・乱数の種 {SEED}"]
    for i, s in enumerate(lines):
        text(d, (680, 250 + i * 120), s, 38 if i < 3 else 30, FG if i < 3 else SUB, anchor="ma")


A = "alice"
SCENES = [
    Scene(f"こんにちは、電脳アリスです。今日は、話題のラッキートリガー機、{SPEC['name']}を、1万人で打ってみます。", s_open, face=("happy", "smile"), voice="alice_happy", pad=0.8),
    Scene("まずはスペックから。当たり確率は合算で、199.9分の1。この台のRUSHは、130回転のあいだ、95.3分の1を引けば続く仕組みで、継続率はおよそ75パーセントです。", s_spec, pad=1.0),
    Scene("ラッキートリガー、略してLTは、RUSHのさらに上に、出玉の多いモードを用意した仕組みです。この台は、RUSHに入れば、そのままLTの状態。RUSH中の大当たりは、すべて約3000個以上です。", s_lt, pad=1.0),
    Scene(f"ここで大事なポイント。当たりの半分は、喰種チャージという、約300個の当たりです。RUSHに入るのは図柄揃いの51パーセントだけなので、通常時からRUSHに入る確率は、およそ{399.9 / 0.51:.0f}分の1になります。", s_trick, face=("wide", "smile"), pad=1.2),
    Scene(f"では実験です。図柄揃いを1万回引いて、RUSHに入るかを見てみます。光った点が、RUSH突入です。結果は、{enter_rate * 100:.1f}パーセント。ほぼスペックどおりですね。", s_exp1_run, pad=1.2),
    Scene(f"RUSHに入ったあと、何回当たったかの内訳です。いちばん多いのは、1回も当たらずに終わるパターン。でも、長く続く人もいて、最高は{chain_max}連続でした。", s_exp1_chain, pad=1.2),
    Scene(f"RUSHに入ったときの平均出玉は、およそ{avg_rush:.0f}個。1万個を超えたのは、1万回のうち{over10k}回でした。", s_exp1_avg, face=("happy", "smile"), pad=1.2),
    Scene(f"では、RUSHに入るまで、何回転かかるのでしょう。1万人に、RUSHに入るまで打ってもらいました。半分の人は{q50:.0f}回転までに入りますが、1割の人は{q90:.0f}回転以上かかっています。", s_cost, pad=1.2),
    Scene(f"お金にすると、1000円で{RATE}回転の場合、平均でおよそ{to_rush_yen.mean() / 10000:.1f}万円。1割の人は{q90 / RATE * 1000 / 10000:.0f}万円以上かかり、いちばんハマった人は{deep}回転、およそ{deep / RATE * 1000 / 10000:.0f}万円でした。途中の当たりの出玉を使わずに打った場合の目安です。", s_cost2, face=("wide", "o"), pad=1.4),
    Scene(f"次は、1万人に1日ずつ打ってもらいます。条件は、等価交換、1000円で{RATE}回転、通常時を{SPINS}回転です。勝った人は、{win_day * 100:.1f}パーセント。平均は{man_say(avg_day)}でした。", s_exp2, pad=1.2),
    Scene(f"いちばん勝った人は{man_say(best_day)}、いちばん負けた人は{man_say(worst_day)}。真ん中の人は{man_say(med_day)}。そして、1日打ってRUSHに1回も入らなかった人が、{norush_day * 100:.0f}パーセントもいました。", s_exp2_ext, face=("wide", "o"), pad=1.2),
    Scene(f"では、回るかどうかで、どれくらい変わるのでしょう。1000円あたり14回転、16回転、18回転で比べます。この計算での損益の分かれ目は、およそ{border:.1f}回転。それより回れば平均はプラス、回らなければマイナスです。", s_exp3, pad=1.4),
    Scene(f"最後に、1ヶ月、20日間打ち続けた場合です。勝った人は{win_month * 100:.1f}パーセント、平均は{man_say(avg_month)}。日数を重ねるほど、運より、回転率の差が効いてきます。", s_exp4, pad=1.4),
    Scene(f"まとめです。当たりの半分はチャージで、RUSHは約{399.9 / 0.51:.0f}分の1。入れば平均{avg_rush:.0f}個。そして、結果を決めるのは、運だけでなく回転率です。", s_summary, face=("happy", "smile"), pad=1.4),
    Scene("この動画は、AIがシミュレーションして作りました。数値は公開情報をもとにしていて、実際のお店の条件で変わります。遊ぶときは、無理のない範囲で。電脳アリスでした。", s_end, face=("happy", "smile"), voice="alice_happy", pad=2.0),
]

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "out", "pachi_tg.mp4")
    host = Host(1290, 230, 900)
    sec = render(SCENES, out, voice=A, host=host, bg=make_bg())
    print(f"ok {sec:.1f}s enter={enter_rate:.3f} avg_rush={avg_rush:.0f} chain_max={chain_max} over10k={over10k} "
          f"win_day={win_day:.3f} avg_day={avg_day:.0f} best={best_day:.0f} worst={worst_day:.0f} med={med_day:.0f} "
          f"norush={norush_day:.3f} border={border:.2f} rates={[(r, round((v[0] > 0).mean(), 3), int(v[0].mean())) for r, v in rates.items()]} "
          f"win_month={win_month:.3f} avg_month={avg_month:.0f} C={C:.4f}")
