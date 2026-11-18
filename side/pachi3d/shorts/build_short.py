"""YouTubeショート（縦1080x1920・約30秒）：「RUSHまで平均いくら？」1万人の結果だけを見せる。

本編と同じシミュレーション（build.py）の数字を使う。読みの点検（yomi.py）を通してから声を作る。
実行：python3 side/pachi3d/shorts/build_short.py → shorts/assets/{mix.wav,data.js}
"""
import json
import os
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import build as B  # noqa: E402  （本編のシミュレーション結果）
from yomi import check, to_say  # noqa: E402
from kokoro_ja import tts as _ktts  # noqa: E402

VOICE = os.environ.get("VOICE", "ami")            # ami（小春音アミ・るんるん）／kokoro


def tts(say):
    if VOICE == "kokoro":
        return _ktts(say)
    import sbv2_ja
    return sbv2_ja.tts(say, "ami", "るんるん" if VOICE == "ami" else "Neutral")

SR, FPS = 48000, 30
yen = lambda spins: spins / B.RATE * 1000
man = lambda y: f"{y / 10000:.1f}万円"
mean_y, half_y, deep_y = yen(B.to_rush.mean()), yen(B.q50), yen(B.deep)

S = [
    dict(id="hook", face="surprised", sub="1万人がRUSHまで打ったら、平均いくらかかると思う？"),
    dict(id="setup", face="pose_pointing", sub=f"話題の「e東京喰種」で、1000円{B.RATE}回転として試してみました。"),
    dict(id="mean", face="pose_excited", sub=f"平均は、約{man(mean_y)}。"),
    dict(id="half", face="base", sub=f"半分の人は、約{man(half_y)}までにRUSHに入りました。"),
    dict(id="deep", face="surprised", sub=f"でも、いちばんハマった人は、なんと約{deep_y / 10000:.0f}万円。"),
    dict(id="end", face="happy", sub="運の差、大きすぎ…。次に試してほしいこと、コメントで教えてね！"),
]


def main():
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    for s in S:
        s["say"] = to_say(s["sub"])
        kana, bad = check(s["say"])
        if bad:
            raise SystemExit(f"読みの問題 {s['id']}: {bad} / {kana}")
    parts, t = [], 0.6
    for s in S:
        x, sr = tts(s["say"])
        if sr != SR:
            x = np.interp(np.arange(int(len(x) * SR / sr)) / SR, np.arange(len(x)) / sr, x).astype(np.float32)
        pad = 0.55 if s["id"] != "end" else 1.2
        s["start"], s["voice_len"], s["dur"] = round(t, 3), round(len(x) / SR, 3), round(len(x) / SR + pad, 3)
        buf = np.zeros(int(s["dur"] * SR), np.float32)
        buf[: len(x)] = x
        parts.append(buf)
        t += s["dur"]
    vo = np.concatenate([np.zeros(int(0.6 * SR), np.float32)] + parts)
    total = len(vo) / SR
    hop = SR // FPS
    env = np.array([np.abs(vo[i * hop:(i + 1) * hop]).mean() for i in range(int(total * FPS))])
    ref = np.percentile(env[env > 1e-4], 85)
    mouth = np.where(env > ref * 0.22, 1, 0).tolist()
    # BGM（本編と同じ OpenTracks の曲。声の間は小さく）
    bgm_path = os.path.join(ROOT, "assets", "bgm", "honey_lemon.mp3")
    music = B.load_mp3(bgm_path)[: len(vo)] if os.path.exists(bgm_path) else np.zeros(len(vo), np.float32)
    music = np.pad(music, (0, len(vo) - len(music)))
    music = music / (np.sqrt((music ** 2).mean()) + 1e-9) * 0.12
    duck = np.repeat(np.array([0.45 if m else 1.0 for m in mouth], np.float32), hop)
    duck = np.convolve(np.pad(duck, (0, len(vo) - len(duck)), constant_values=1.0), np.ones(4800) / 4800, "same")
    mix = vo * 0.95 + music * duck * 0.6
    for sid in ("mean", "deep"):                       # 数字が出る瞬間に「キラン」
        s = next(x for x in S if x["id"] == sid)
        a = int((s["start"] + s["voice_len"] * 0.55) * SR)
        c = B.chime()
        mix[a:a + len(c)] += c[: len(mix) - a]
    mix = np.clip(mix / np.abs(mix).max() * 0.92, -1, 1)
    with wave.open(os.path.join(HERE, "assets", "mix.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())
    order = np.argsort(B.to_rush)                      # 早くRUSHに入った人から順に光らせる
    data = dict(total=round(total, 3), fps=FPS, mouth=mouth, lead=0.6,
                scenes=[{k: s[k] for k in ("id", "sub", "start", "dur", "voice_len", "face")} for s in S],
                stats=dict(mean=mean_y, half=half_y, deep=deep_y, deep_spins=int(B.deep), rate=B.RATE,
                           mean_spins=float(B.to_rush.mean()), half_spins=float(B.q50)),
                rank=np.argsort(order).tolist(), spins=B.to_rush.astype(int).tolist())
    with open(os.path.join(HERE, "assets", "data.js"), "w") as f:
        f.write("window.DATA=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";")
    print(f"total {total:.1f}s", [(s["id"], s["start"]) for s in S])


if __name__ == "__main__":
    main()
