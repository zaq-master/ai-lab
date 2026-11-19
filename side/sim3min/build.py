"""3分動画「やめ方を変えたら、パチンコは勝てるの？」の台本・声・音・データを作る。
数字はすべて results.json（sim.py の結果）から入れる。企画書：side/pachi3d/plans/2026-11-20_yamekata.md
実行：python3 side/sim3min/build.py → assets/{mix.wav,data.js}
"""
import json
import os
import subprocess
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
P3 = os.path.join(HERE, "..", "pachi3d")
sys.path.insert(0, P3)
import vv_ja  # noqa: E402
from yomi import check, to_say  # noqa: E402

SR, FPS = 48000, 30
R = json.load(open(os.path.join(HERE, "results.json")))
P = R["plans"]
K = ["close", "win2", "rush1", "lose1"]
COL = {"close": "#ff6b6b", "win2": "#4da3ff", "rush1": "#3ccf7a", "lose1": "#ffc928"}
SHORT = {"close": "18時まで打つ", "win2": "2万円で帰る", "rush1": "RUSH1回で帰る", "lose1": "財布1万円だけ"}
pc = lambda x: f"{round(x * 100):.0f}%"
man = lambda y: f"約{abs(y) / 10000:.1f}万円"
hr = lambda y: f"{round(abs(y), -1):.0f}円"
rs = {int(k): v for k, v in R["rate_scan"].items()}
# 損得ゼロの回転率：16回転と17回転の30日平均を直線でつないで0になる所（この計算の設定での値）
border = 16 + (-rs[16]["mean"]) / (rs[17]["mean"] - rs[16]["mean"])
hours = [P[k]["yen_per_hour"] for k in K]
d1, mo = {k: P[k]["day1"] for k in K}, {k: P[k]["month"] for k in K}

S = [
    dict(id="hook", face="surprised", vis="hook",
         sub="「勝ったらすぐ帰る」って、本当に得なんでしょうか？"),
    dict(id="hook2", face="pose_pointing", vis="hook",
         sub="負ける前にやめれば、勝てる。よく聞きますよね。今日はこれを、1万人で確かめます。"),
    dict(id="plans", face="pose_pointing", vis="plans",
         sub="用意したやめ方は4つ。18時まで打つ。2万円勝ったら帰る。RUSHが1回終わったら帰る。そして、財布に1万円だけ持っていく。"),
    dict(id="guess", face="pose_thinking", vis="plans",
         sub="どれがいちばん得だと思いますか？コメントで予想してから、続きを見てね。"),
    dict(id="rule", face="base", vis="rule",
         sub="台は、e東京喰種のスペック。1000円で16回転する台を、等価で、朝10時から18時まで。財布は5万円までです。"),
    dict(id="rule2", face="pose_pointing", vis="rule",
         sub="これを、作戦ごとに1万人ずつ、30日間。作戦を比べるための、ちょっと極端な条件です。"),
    dict(id="d1", face="pose_thinking", vis="d1",
         sub="まずは、1日だけ。勝った人の割合は…"),
    dict(id="d1r", face="pose_excited", vis="d1",
         sub=f"18時まで打つ人は{pc(d1['close']['win'])}。2万円で帰る人は{pc(d1['win2']['win'])}。RUSH1回で帰る人は{pc(d1['rush1']['win'])}。早く帰るほど、勝つ人が増えました！"),
    dict(id="d1w", face="surprised", vis="d1",
         sub=f"でも、財布1万円だけの人は、たった{pc(d1['lose1']['win'])}。勝っても18時まで打つので、ほとんどの人が、玉を全部使い切ってしまうんです。"),
    dict(id="broke", face="troubled", vis="broke",
         sub=f"それと、もうひとつ。18時まで打った人の、{pc(P['close']['day1_broke'])}が、財布の5万円を、全部なくしています。"),
    dict(id="mo", face="pose_thinking", vis="mo",
         sub="じゃあ、これを30日続けたら、どうなるでしょう？"),
    dict(id="mow", face="pose_pointing", vis="mo",
         sub=f"30日トータルでプラスだった人は、どの作戦も{pc(min(mo[k]['win'] for k in K))}から{pc(max(mo[k]['win'] for k in K))}。1日目の差が、ぐっと縮まりました。"),
    dict(id="mom", face="pose_excited", vis="mom",
         sub=f"30日の平均は…18時まで打つ人が、マイナス{man(mo['close']['mean'])}。2万円で帰る人が{man(mo['win2']['mean'])}。RUSH1回は{man(mo['rush1']['mean'])}。財布1万円は{man(mo['lose1']['mean'])}。"),
    dict(id="q", face="pose_thinking", vis="mom",
         sub="やっぱり、早く帰る作戦が強い…？実は、ちょっと違うんです。"),
    dict(id="hour", face="pose_pointing", vis="hour",
         sub=f"1時間あたりの損を計算すると…4つとも、{hr(max(hours))}から{hr(min(hours))}。ほとんど同じなんです！"),
    dict(id="why", face="base", vis="why",
         sub="損が少なかったのは、作戦がうまいからじゃなくて、遊んだ時間が短かったから。"),
    dict(id="why2", face="pose_pointing", vis="why",
         sub="台は、前の結果を覚えていません。だから、どこでやめても、1時間あたりの損は変わらないんです。"),
    dict(id="rate", face="surprised", vis="rate",
         sub=f"では、お金を大きく変えるのは何か。それは、1000円で何回まわるか、です。"),
    dict(id="rate2", face="pose_pointing", vis="rate",
         sub=f"この計算での損得ゼロは、約{border:.1f}回転。16回転だと、30日でマイナス{man(rs[16]['mean'])}。15回転だと、マイナス{man(rs[15]['mean'])}。1回転の差で、倍以上になります。"),
    dict(id="sum", face="base", vis="sum",
         sub="まとめです。やめ方で変わるのは、勝つ人の割合と、遊ぶ時間。1時間あたりの損は、変わりません。遊ぶお金と時間は、先に決めておこうね。"),
    dict(id="end", face="happy", vis="end",
         sub="これはAIのシミュレーションで、必勝法ではありません。次に確かめてほしい言い伝え、コメントで教えてね！"),
]


def load_mp3(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def tone(f, d, a, decay):
    t = np.arange(int(d * SR)) / SR
    return a * np.sin(2 * np.pi * f * t) * np.exp(-t / decay)


def main():
    assert d1['close']['win'] < d1['win2']['win'] < d1['rush1']['win'] and rs[15]['mean'] / rs[16]['mean'] > 2
    for s in S:
        s["say"] = to_say(s["sub"])
        kana, bad = check(s["say"])
        if bad:
            raise SystemExit(f"読みの問題 {s['id']}: {bad} {kana}")
    lead, t, parts = 0.4, 0.4, []
    for s in S:
        x, _ = vv_ja.tts_script(s["say"], sr_out=SR)
        pad = {"d1": 0.6, "mom": 0.5, "hour": 0.6, "end": 1.5}.get(s["id"], 0.35)
        s["start"], s["voice_len"], s["dur"] = round(t, 3), round(len(x) / SR, 3), round(len(x) / SR + pad, 3)
        b = np.zeros(int(s["dur"] * SR), np.float32); b[: len(x)] = x
        parts.append(b); t += s["dur"]
        print(s["id"], s["start"], s["voice_len"], flush=True)
    vo = np.concatenate([np.zeros(int(lead * SR), np.float32)] + parts)
    total = len(vo) / SR
    hop = SR // FPS
    env = np.array([np.abs(vo[i * hop:(i + 1) * hop]).mean() for i in range(int(total * FPS))])
    ref = np.percentile(env[env > 1e-4], 85)
    sm = np.convolve(env, np.ones(3) / 3, "same")
    lv = np.where(sm > ref * 0.55, 2, np.where(sm > ref * 0.2, 1, 0))
    for i in range(1, len(lv) - 1):
        if lv[i] != lv[i - 1] and lv[i] != lv[i + 1]:
            lv[i] = lv[i - 1]
    mouth = lv.tolist()
    mus = load_mp3(os.path.join(P3, "assets", "bgm", "nandeshou.mp3"))
    mus = np.tile(mus, len(vo) // len(mus) + 1)[: len(vo)]
    mus = mus / (np.sqrt((mus ** 2).mean()) + 1e-9) * 0.11
    duck = np.repeat(np.array([0.45 if m else 1.0 for m in mouth], np.float32), hop)
    duck = np.convolve(np.pad(duck, (0, len(vo) - len(duck)), constant_values=1.0), np.ones(4800) / 4800, "same")
    mix = vo * 0.95 + mus * duck * 0.6
    fade = np.ones(len(mix), np.float32); n = int(1.5 * SR); fade[-n:] = np.linspace(1, 0, n)
    mix *= fade
    # 結果が出る瞬間に「キラン」
    for sid, at in (("d1r", 0.0), ("mom", 0.25), ("hour", 0.45), ("rate2", 0.3)):
        s = next(x for x in S if x["id"] == sid)
        a = int((s["start"] + s["voice_len"] * at) * SR)
        c = sum(tone(f, 1.0, 0.07, 0.3) for f in (1318.5, 1760, 2637)); mix[a:a + len(c)] += c[: len(mix) - a]
    mix = np.clip(mix / np.abs(mix).max() * 0.92, -1, 1)
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    with wave.open(os.path.join(HERE, "assets", "mix.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    data = dict(total=round(total, 3), fps=FPS, mouth=mouth, lead=lead, K=K, COL=COL, SHORT=SHORT,
                scenes=[{k: s[k] for k in ("id", "sub", "start", "dur", "voice_len", "face", "vis")} for s in S],
                P={k: dict(d1win=d1[k]["win"], d1mean=d1[k]["mean"], d1median=d1[k]["median"], d1p90=P[k]["day1_p90"],
                           broke=P[k]["day1_broke"], mowin=mo[k]["win"], momean=mo[k]["mean"], hours=P[k]["month_hours"],
                           perhour=P[k]["yen_per_hour"]) for k in K},
                rate={k: rs[k]["mean"] for k in (15, 16)}, border=border, cond=P["close"]["cond"])
    with open(os.path.join(HERE, "assets", "data.js"), "w") as f:
        f.write("window.DATA=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";")
    print(f"total {total:.1f}s border {border:.2f}")


if __name__ == "__main__":
    main()
