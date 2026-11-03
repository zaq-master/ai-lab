#!/usr/bin/env python3
"""Slack報告用のダッシュボード画像（PNG）を作る。
使い方:
  python3 ops/report_card.py daily  -> ops/out/daily.png（日報：KPI＋推移グラフ＋10事業の状態）
  python3 ops/report_card.py biz <番号> "<見出し>" "<状態>" "<成果1|成果2|...>" "<次の一手>" -> ops/out/biz<番号>.png
日本語フォントがない環境では Noto Sans JP を自動で取得する。
"""
import csv, sys, re, os, subprocess, urllib.request
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib import font_manager as fm

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "ops" / "out"
OUT.mkdir(parents=True, exist_ok=True)

BG, CARD, FG, SUB, LINE = "#f6f7fb", "#ffffff", "#1d2330", "#6b7385", "#e3e6ee"
ACC = ["#3b5bdb", "#0ca678", "#f08c00", "#e64980", "#7048e8", "#1098ad"]
STATUS = {"稼働中": "#0ca678", "準備中": "#f08c00", "原稿あり": "#f08c00", "ログイン待ち": "#e03131", "未着手": "#adb5bd", "稼働": "#0ca678",
          "🟢": "#0ca678", "🟡": "#f08c00", "🔴": "#e03131", "順調": "#0ca678", "様子見": "#f08c00", "止まっ": "#e03131"}
# 日本語フォントに絵文字が無く豆腐（□）になるため、描画する文字列からは取り除く（色は STATUS で付ける）
EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0E\uFE0F\u200D]")


def clean(t):
    return re.sub(r"\s{2,}", " ", EMOJI.sub("", str(t))).strip()


def status_key(st):
    return next((k for k in STATUS if k in st), "未着手")


def font():
    cands = [f for f in fm.findSystemFonts() if re.search(r"NotoSansCJK|NotoSansJP|IPAexGothic|ipag", f, re.I)]
    # findSystemFonts の順番は毎回変わるため、太字が出る Noto Sans CJK（Regular）を優先して固定する
    pri = lambda f: next((i for i, k in enumerate(["NotoSansCJK-Regular", "NotoSansCJK", "NotoSansJP", "IPAexGothic"]) if k.lower() in f.lower()), 9)
    cands.sort(key=lambda f: (pri(f), f))
    if not cands:
        p = Path("/tmp/NotoSansJP.ttf")
        if not p.exists():
            urllib.request.urlretrieve(
                "https://github.com/google/fonts/raw/main/ofl/notosansjp/NotoSansJP%5Bwght%5D.ttf", p)
        cands = [str(p)]
    fm.fontManager.addfont(cands[0])
    plt.rcParams["font.family"] = fm.FontProperties(fname=cands[0]).get_name()


def metrics():
    rows = list(csv.DictReader(open(ROOT / "ops" / "metrics.csv", encoding="utf-8")))
    num = lambda v: int(v) if str(v).strip().lstrip("-").isdigit() else 0
    return [{k: (num(v) if k != "date" else v) for k, v in r.items()} for r in rows]


def ventures():
    t = (ROOT / "ops" / "ventures.md").read_text(encoding="utf-8")
    out = []
    for l in t.splitlines():
        c = [x.strip() for x in l.strip("|").split("|")]
        if len(c) >= 3 and c[0].isdigit():
            out.append((c[0], re.sub(r"（.*?）", "", c[1])[:16], c[2]))
    return out


def card(ax, x, y, w, h, title, value, sub, color):
    ax.add_patch(plt.Rectangle((x, y), w, h, color=CARD, ec=LINE, lw=1.2, zorder=1))
    ax.add_patch(plt.Rectangle((x, y + h - 0.012), w, 0.012, color=color, zorder=2))
    ax.text(x + 0.02, y + h - 0.05, title, fontsize=11, color=SUB, va="top")
    ax.text(x + 0.02, y + 0.06, value, fontsize=26, color=FG, weight="bold", va="bottom")
    ax.text(x + 0.02, y + 0.025, sub, fontsize=9, color=SUB, va="bottom")


def daily():
    m = metrics()
    last, prev = m[-1], (m[-2] if len(m) > 1 else None)
    d = lambda k: "" if not prev else f"前日比 {last[k] - prev[k]:+d}"
    fig = plt.figure(figsize=(12, 7.2), dpi=110, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.text(0.03, 0.95, f"日報  {last['date']}", fontsize=20, weight="bold", color=FG, va="top")
    ax.text(0.03, 0.895, "電脳アリス × QOLガジェット ／ AIが3ヶ月で300万円に挑む", fontsize=11, color=SUB, va="top")
    goal = 3_000_000
    pct = last["sales_total_jpy"] / goal
    kp = [("売上（今日）", f"¥{last['sales_jpy']:,}", d("sales_jpy"), ACC[0]),
          ("累計売上", f"¥{last['sales_total_jpy']:,}", f"目標の {pct:.2%}", ACC[3]),
          ("サイト記事", f"{last['posts_site']}本", d("posts_site"), ACC[1]),
          ("フォロワー合計", f"{last['followers_x'] + last['followers_ig'] + last['followers_note']}",
           f"X {last['followers_x']} / IG {last['followers_ig']} / note {last['followers_note']}", ACC[2])]
    for i, (t, v, s, c) in enumerate(kp):
        card(ax, 0.03 + i * 0.24, 0.66, 0.22, 0.19, t, v, s, c)
    # 300万円への進捗バー
    ax.add_patch(plt.Rectangle((0.03, 0.6), 0.94, 0.025, color=LINE))
    ax.add_patch(plt.Rectangle((0.03, 0.6), max(0.004, 0.94 * min(pct, 1)), 0.025, color=ACC[3]))
    ax.text(0.97, 0.635, f"300万円まで ¥{goal - last['sales_total_jpy']:,}", fontsize=10, color=SUB, ha="right", va="bottom")
    # 推移グラフ
    g = fig.add_axes([0.06, 0.08, 0.5, 0.42], facecolor=CARD)
    xs = [r["date"][5:] for r in m]
    g.plot(xs, [r["posts_site"] for r in m], marker="o", color=ACC[1], label="記事数")
    g.plot(xs, [r["posts_note"] for r in m], marker="o", color=ACC[4], label="note")
    g.plot(xs, [r["posts_x"] + r["posts_ig"] for r in m], marker="o", color=ACC[2], label="SNS投稿")
    g2 = g.twinx(); sales = [r["sales_jpy"] for r in m]; g2.bar(xs, sales, color=ACC[0], alpha=0.25, label="売上")
    g2.set_ylim(0, max(sales + [1000]) * 1.2); g2.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"¥{int(v):,}")); g2.tick_params(labelsize=8); g.set_ylim(bottom=0)
    g.set_title("推移（線＝コンテンツ数／棒＝売上）", fontsize=11, color=FG, loc="left")
    g.legend(loc="upper left", fontsize=9, frameon=False); g.tick_params(labelsize=9)
    for s in ("top",): g.spines[s].set_visible(False); g2.spines[s].set_visible(False)
    # 10事業の状態
    ax.text(0.61, 0.52, "事業の状態", fontsize=12, weight="bold", color=FG)
    for i, (n, name, st) in enumerate(ventures()[:11]):
        y = 0.47 - i * 0.04
        key = status_key(st)
        ax.add_patch(plt.Circle((0.62, y + 0.008), 0.007, color=STATUS[key]))
        ax.text(0.635, y, f"{n}. {clean(name)}", fontsize=10, color=FG)
        ax.text(0.97, y, clean(st)[:14], fontsize=9, color=SUB, ha="right")
    p = OUT / "daily.png"; fig.savefig(p, facecolor=BG); print(p)


def biz(no, title, status, results, nxt):
    key = status_key(status)
    title, status, nxt = clean(title), clean(status), clean(nxt)
    results = "|".join(clean(x) for x in results.split("|"))
    fig = plt.figure(figsize=(10, 5.2), dpi=110, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    c = ACC[int(no) % len(ACC)]
    ax.add_patch(plt.Rectangle((0, 0.9), 1, 0.1, color=c))
    ax.text(0.03, 0.95, f"{int(no):02d}  {title}", fontsize=18, weight="bold", color="white", va="center")
    ax.add_patch(plt.Rectangle((0.03, 0.76), 0.3, 0.08, color=STATUS[key]))
    ax.text(0.045, 0.8, f"状態：{status}"[:18], fontsize=12, color="white", va="center", weight="bold")
    ax.text(0.03, 0.68, "今回の成果", fontsize=13, weight="bold", color=FG)
    for i, r in enumerate([x for x in results.split("|") if x][:5]):
        ax.text(0.05, 0.6 - i * 0.075, f"● {r}"[:46], fontsize=11.5, color=FG)
    ax.add_patch(plt.Rectangle((0.03, 0.05), 0.94, 0.13, color=CARD, ec=c, lw=2))
    ax.text(0.05, 0.115, f"▶ 次の一手：{nxt}"[:48], fontsize=12.5, color=FG, va="center", weight="bold")
    p = OUT / f"biz{int(no):02d}.png"; fig.savefig(p, facecolor=BG); print(p)


if __name__ == "__main__":
    font()
    if sys.argv[1] == "daily":
        daily()
    else:
        biz(*sys.argv[2:7])
