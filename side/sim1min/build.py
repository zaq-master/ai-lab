"""1分動画：「ハマってる台は『そろそろ当たる』のか？」— 1万人で検証。

A組：500回転ハマっている台に座る ／ B組：当たった直後の台に座る。
どちらも1/399.9（e東京喰種の図柄揃いと同じ確率）で300回転だけ打つ。台は前の結果を覚えていないので、理論上どちらも同じ。
実行：python3 side/sim1min/build.py → assets/{mix.wav,data.js}
"""
import json
import os
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
P3 = os.path.join(HERE, "..", "pachi3d")
sys.path.insert(0, P3)
import sbv2_ja  # noqa: E402
from yomi import check, to_say  # noqa: E402

SR, FPS = 48000, 30
P, SPINS, N, SEED = 1 / 399.9, 300, 5000, 20261119
rng = np.random.default_rng(SEED)
# 各人が300回転のうち初めて当たった回転（当たらなければ0）
def first_hit():
    g = rng.geometric(P, N)
    return np.where(g <= SPINS, g, 0)

A, B = first_hit(), first_hit()          # A＝ハマり台、B＝当たった直後の台（中身の確率は同じ）
ra, rb = float((A > 0).mean()), float((B > 0).mean())
theory = 1 - (1 - P) ** SPINS
pct = lambda x: f"{x * 100:.1f}%"

S = [
    dict(id="hook", face="surprised", sub="500回転もハマってる台。そろそろ当たりそうな気、しませんか？"),
    dict(id="setup", face="pose_pointing", sub="じゃあ、確かめてみましょう。1万人を2組に分けます。A組はハマってる台、B組は当たった直後の台です。"),
    dict(id="rule", face="base", sub="当たり確率は、どちらも1/399.9。300回転だけ打って、当たった人の数をくらべます。"),
    dict(id="race", face="pose_thinking", sub="当たった人は、金色の玉になってタンクにたまります。さあ、どっちが多くなると思いますか？"),
    dict(id="result", face="pose_excited",
         sub=f"結果は…A組{pct(ra)}。B組{pct(rb)}。ほとんど、同じなんです。"),
    dict(id="why", face="pose_pointing", sub="実は、台は前の結果を覚えていません。次の1回転も、ずっと1/399.9のままなんです。"),
    dict(id="end", face="happy", sub="そろそろ当たるっていうのは、気のせいだったんですね。次に試してほしいこと、コメントで教えてね！"),
]


def tts(say):
    x, _ = sbv2_ja.tts_script(say, "ami", sr_out=SR)   # 語りかけ調（文ごとに調子・速さ・間を変える）
    return x


def load_mp3(path):
    import subprocess
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def tone(f, d, a, decay):
    t = np.arange(int(d * SR)) / SR
    return a * np.sin(2 * np.pi * f * t) * np.exp(-t / decay)


def main():
    for s in S:
        s["say"] = to_say(s["sub"])
        kana, bad = check(s["say"])
        if bad:
            raise SystemExit(f"読みの問題 {s['id']}: {bad} {kana}")
    lead, t, parts = 0.5, 0.5, []
    for s in S:
        x = tts(s["say"])
        pad = {"race": 3.5, "result": 0.6, "end": 1.2}.get(s["id"], 0.3)   # レースは声のあとも玉がたまる時間を取る
        s["start"], s["voice_len"], s["dur"] = round(t, 3), round(len(x) / SR, 3), round(len(x) / SR + pad, 3)
        b = np.zeros(int(s["dur"] * SR), np.float32); b[: len(x)] = x
        parts.append(b); t += s["dur"]
    vo = np.concatenate([np.zeros(int(lead * SR), np.float32)] + parts)
    total = len(vo) / SR
    hop = SR // FPS
    env = np.array([np.abs(vo[i * hop:(i + 1) * hop]).mean() for i in range(int(total * FPS))])
    mouth = np.where(env > np.percentile(env[env > 1e-4], 85) * 0.22, 1, 0).tolist()
    bgm = os.path.join(P3, "assets", "bgm", "nandeshou.mp3")
    mus = load_mp3(bgm) if os.path.exists(bgm) else np.zeros(1, np.float32)
    mus = np.tile(mus, len(vo) // len(mus) + 1)[: len(vo)]
    mus = mus / (np.sqrt((mus ** 2).mean()) + 1e-9) * 0.11
    duck = np.repeat(np.array([0.45 if m else 1.0 for m in mouth], np.float32), hop)
    duck = np.convolve(np.pad(duck, (0, len(vo) - len(duck)), constant_values=1.0), np.ones(4800) / 4800, "same")
    mix = vo * 0.95 + mus * duck * 0.6
    # レース中：当たりが出るたびに小さな「チン」（A・Bの当たりを時間に並べる）
    race = next(s for s in S if s["id"] == "race")
    rs, rd = race["start"] + 1.0, race["dur"] - 1.5
    for arr, f in ((A, 1568), (B, 1760)):
        for k in np.sort(arr[arr > 0])[::12]:
            a = int((rs + rd * k / SPINS) * SR)
            c = tone(f, 0.12, 0.05, 0.04); mix[a:a + len(c)] += c[: len(mix) - a]
    res = next(s for s in S if s["id"] == "result")
    a = int((res["start"] + res["voice_len"] * 0.45) * SR)
    c = sum(tone(f, 1.2, 0.09, 0.35) for f in (1318.5, 1760, 2637)); mix[a:a + len(c)] += c[: len(mix) - a]
    mix = np.clip(mix / np.abs(mix).max() * 0.92, -1, 1)
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    with wave.open(os.path.join(HERE, "assets", "mix.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    data = dict(total=round(total, 3), fps=FPS, mouth=mouth, lead=lead, spins=SPINS,
                scenes=[{k: s[k] for k in ("id", "sub", "start", "dur", "voice_len", "face")} for s in S],
                stats=dict(ra=ra, rb=rb, theory=theory, n=N, race_start=rs, race_dur=rd),
                A=A.tolist(), B=B.tolist())
    with open(os.path.join(HERE, "assets", "data.js"), "w") as f:
        f.write("window.DATA=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";")
    print(f"total {total:.1f}s  A={pct(ra)} B={pct(rb)} theory={pct(theory)}", [(s["id"], s["start"]) for s in S])


if __name__ == "__main__":
    main()
