"""YouTubeショート（縦1080x1920）：「1万人がRUSHまで打ったら平均いくら？」

計算は pachisim.py（リアルな1日）。数字はすべて計算結果から台本・画面・説明欄・サムネに入れる（手書きしない）。
声は VOICEVOX:四国めたん（vv_ja.py）。読みは yomi.py で点検してから声を作る。
実行：python3 side/pachi3d/shorts/build_short.py
出力：shorts/assets/{mix.wav,data.js}、shorts/description.txt、index.html の長さを更新
"""
import json
import os
import re
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import vv_ja  # noqa: E402
from pachisim import ST_MACHINE_TOKYOGHOUL as M, Conditions, describe, simulate  # noqa: E402
from yomi import check, to_say  # noqa: E402

SR, FPS, N, SEED = 48000, 30, 10000, 20261118
COND = Conditions()                       # 標準条件：1000円17回転（±0.8）・等価・8時間・財布5万円・持ち玉遊技・閉店まで
R = simulate(M, COND, n=N, seed=SEED)
cash, ok = R["first_rush_cash"], R["first_rush_cash"] >= 0
yen = R["yen"]
in_pct, out_pct = round(ok.mean() * 100), 100 - round(ok.mean() * 100)
mean_y, half_y = float(cash[ok].mean()), float(np.median(cash[ok]))
one_in = round(1 / (M.p_normal * sum(h[0] for h in M.normal_hits if h[2])))
man = lambda y: f"{y / 10000:.1f}万円"
budget = f"{int(COND.budget_yen / 10000)}万円"
rate = f"{COND.rate:g}"

S = [
    dict(id="hook", face="surprised", sub="1万人がRUSHを目指して打ったら、平均いくらかかると思いますか？"),
    dict(id="guess", face="pose_thinking", sub="なんとなく、1万円くらいで入りそう…ですよね？"),
    dict(id="rule", face="pose_pointing", sub=f"台はe東京喰種。1000円で{rate}回る台を、等価交換で{COND.hours:g}時間。財布は{budget}までです。"),
    dict(id="race", face="base", sub="光った点が、RUSHに入った人。お金を使うほど、増えていきます。"),
    dict(id="mean", face="pose_excited", sub=f"結果は…RUSHに入れた人の平均は、約{man(mean_y)}。"),
    dict(id="half", face="base", sub=f"真ん中の人は、約{man(half_y)}でした。"),
    dict(id="miss", face="surprised", sub=f"でも実は、約{out_pct}%の人は、{budget}を使い切っても、入れなかったんです。"),
    dict(id="why", face="pose_pointing", sub=f"RUSHに行ける当たりは、約{one_in}回転に1回。台は前の結果を覚えていないので、運の差がそのまま出るんです。"),
    dict(id="end", face="happy", sub="平均だけ見ると、安く見えちゃいますよね。次に試してほしいこと、コメントで教えてね！"),
]
PAD = {"race": 2.2, "mean": 0.7, "half": 0.5, "miss": 0.9, "end": 3.2}


def tone(f, d, a, decay):
    t = np.arange(int(d * SR)) / SR
    return (a * np.sin(2 * np.pi * f * t) * np.exp(-t / decay)).astype(np.float32)


def add(mix, sec, x):
    a = int(sec * SR)
    if a < len(mix):
        mix[a:a + len(x)] += x[: len(mix) - a]


def bgm(n):
    """自作のBGM（夜の街っぽい短調のアルペジオ）。外部の曲は使わない"""
    y = np.zeros(n, np.float32)
    step = int(SR * 60 / 104 / 2)
    chords = [(220.0, 261.63, 329.63), (174.61, 220.0, 261.63), (130.81, 196.0, 261.63), (196.0, 246.94, 293.66)]
    for i in range(n // step):
        c = chords[(i // 8) % 4]
        x = tone(c[[0, 1, 2, 1][i % 4]] * 2, 0.45, 0.16, 0.16)
        a = i * step
        y[a:a + len(x)] += x[: n - a]
        if i % 8 == 0:
            b = tone(c[0] / 2, 1.6, 0.3, 0.7)
            y[a:a + len(b)] += b[: n - a]
    return y


def main():
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    for s in S:
        s["say"] = to_say(s["sub"])
        s["kana"], bad = check(s["say"])
        print(f"[{s['id']}] {s['kana']}")
        if bad:
            raise SystemExit(f"読みの問題 {s['id']}: {bad}")
    if "--kana" in sys.argv:
        return
    lead, t, parts = 0.5, 0.5, []
    for s in S:
        x, _ = vv_ja.tts_script(s["say"], sr_out=SR)
        s["start"], s["voice_len"], s["dur"] = round(t, 3), round(len(x) / SR, 3), round(len(x) / SR + PAD.get(s["id"], 0.3), 3)
        b = np.zeros(int(round(s["dur"] * SR)), np.float32); b[: len(x)] = x
        parts.append(b); t += len(b) / SR
    vo = np.concatenate([np.zeros(int(lead * SR), np.float32)] + parts)
    total = len(vo) / SR
    hop = SR // FPS
    env = np.array([np.abs(vo[i * hop:(i + 1) * hop]).mean() for i in range(int(total * FPS))])
    mouth = np.where(env > np.percentile(env[env > 1e-4], 85) * 0.22, 1, 0).tolist()
    mus = bgm(len(vo)); mus = mus / (np.sqrt((mus ** 2).mean()) + 1e-9) * 0.07
    duck = np.repeat(np.array([0.45 if m else 1.0 for m in mouth], np.float32), hop)
    duck = np.convolve(np.pad(duck, (0, len(vo) - len(duck)), constant_values=1.0), np.ones(4800) / 4800, "same")
    mix = vo * 0.95 + mus * duck
    sc = {s["id"]: s for s in S}
    race_s, race_d = sc["race"]["start"] + 0.3, sc["race"]["dur"] - 0.6
    for k in np.sort(cash[ok])[::120]:                # RUSHに入った人が増えるたびに小さな音
        add(mix, race_s + race_d * k / COND.budget_yen, tone(1568, 0.1, 0.035, 0.03))
    for sid, at in (("mean", 0.62), ("half", 0.55), ("miss", 0.5)):
        s = sc[sid]
        add(mix, s["start"] + s["voice_len"] * at, sum(tone(f, 1.1, 0.07, 0.3) for f in (1318.5, 1760, 2637)))
    mix = np.clip(mix / np.abs(mix).max() * 0.92, -1, 1)
    with wave.open(os.path.join(HERE, "assets", "mix.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    stats = dict(n=N, entered=int(ok.sum()), missed=int((~ok).sum()), in_pct=in_pct, out_pct=out_pct, mean=mean_y, half=half_y,
                 mean_txt=man(mean_y), half_txt=man(half_y), budget=COND.budget_yen, budget_txt=budget, race_s=race_s, race_d=race_d,
                 cond=describe(COND) + "・閉店まで（財布が尽きたら終了）")
    data = dict(total=round(total, 3), fps=FPS, mouth=mouth, lead=lead, stats=stats,
                scenes=[{k: s[k] for k in ("id", "sub", "start", "dur", "voice_len", "face")} for s in S],
                cash=[int(v) for v in cash])
    with open(os.path.join(HERE, "assets", "data.js"), "w", encoding="utf8") as f:
        f.write("window.DATA=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";")
    p = os.path.join(HERE, "index.html")
    h = open(p, encoding="utf8").read()
    h = re.sub(r'data-duration="[\d.]+"', f'data-duration="{total:.3f}"', h)
    open(p, "w", encoding="utf8").write(h)
    desc = f"""【タイトル案】
1万人がRUSHまで打ったら平均いくら？【e東京喰種】#shorts

【説明欄】
e東京喰種でRUSHに入るまでにかかる現金を、コンピューターの中の1万人で試しました。
RUSHに入れた人（{in_pct}%）の平均は約{man(mean_y)}、真ん中の人は約{man(half_y)}。ただし約{out_pct}%の人は財布の{budget}を使い切ってもRUSHに入れませんでした（平均には含みません）。
解説：電脳アリス（AI）。この動画はAIがシミュレーションして制作しています。実機レビューではありません。

■条件
{stats['cond']}
台ごとの回転率のばらつき：±{COND.rate_spread:g}回転／1時間の上限約{COND.spins_per_hour:g}回転／試行：{N:,}人

■1日の結果（同じ条件・閉店まで）
勝った人 {(yen > 0).mean() * 100:.1f}%／平均収支 {yen.mean():+,.0f}円／真ん中の人の収支 {np.median(yen):+,.0f}円／財布を使い切った人 {(R['cash'] >= COND.budget_yen).mean() * 100:.1f}%

■スペックの出典（公開情報。メーカー公式資料とは未照合）
図柄揃い約1/399.9・チャージ約1/399.9・RUSH突入約51%・ST130回・RUSH中約1/95.3・継続率約75%
{chr(10).join(M.sources)}

実際の台・お店の条件で結果は変わります。必勝法ではありません。18歳未満は遊技できません。

BGM：自作
音声：VOICEVOX:四国めたん
キャラクター画像：Canvaで生成（オリジナル）

#パチンコ #東京喰種 #シミュレーション #確率 #電脳アリス

【投稿のときの設定（YouTubeアプリ）】
- 「改変または合成されたコンテンツ」＝はい（AIで作ったため）
- 年齢制限：なし（あおる表現は入れていない）
"""
    open(os.path.join(HERE, "description.txt"), "w", encoding="utf8").write(desc)
    print(f"total {total:.2f}s", stats["cond"], f"in={in_pct}% mean={mean_y:.0f} half={half_y:.0f} missed={int((~ok).sum())}")


if __name__ == "__main__":
    main()
