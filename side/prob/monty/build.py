"""3分動画「3つの扉、選び直すべき？1万回ためしてみた」（モンティ・ホール問題）の台本・声・音・データを作る。
数字は results.json（sim.py）からだけ入れる。時刻の表 K はここで1回だけ作り、絵（data.js）と音（mix.wav）が同じ表を使う。
実行：python3 build.py → assets/{mix.wav,data.js}
"""
import json
import os
import re
import subprocess
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
P3 = "/home/user/ai-lab/side/pachi3d"
sys.path.insert(0, P3)
import vv_ja  # noqa: E402
from yomi import check, to_say  # noqa: E402

SR, FPS = 48000, 30
R = json.load(open(os.path.join(HERE, "results.json")))
ST, SW = R["stay"], R["switch"]
pc = lambda x: f"{round(x * 100):.0f}%"
assert 1.9 <= R["ratio"] <= 2.2, "約2倍と言えない"
hit = lambda b: "当たり" if b else "外れ"
s1, w1 = ST["at"]["1"], SW["at"]["1"]
s10, w10 = ST["at"]["10"], SW["at"]["10"]
s100, w100 = ST["at"]["100"], SW["at"]["100"]
assert w100 - s100 >= 15, "100回で差が見えるとは言えない"
one = ("1回目は、どちらも当たり。" if s1 and w1 else "1回目は、どちらも外れ。" if not s1 and not w1
       else f"そのまま派は{hit(s1)}。選び直す派は{hit(w1)}。")

S = [
    dict(id="hook", face="surprised", vis="hook", sub="3つの扉、選び直すべき？"),
    dict(id="hook2", face="pose_pointing", vis="hook", sub="1万回ずつ、ためしてみました。"),
    dict(id="rule1", face="base", vis="rule", sub="ルールは簡単。3つの扉のどれか1つに、金の宝箱。残り2つは外れです。"),
    dict(id="rule2", face="pose_pointing", vis="rule", sub="まず、あなたが1つ選びます。"),
    dict(id="rule3", face="base", vis="rule", sub="司会の私は、当たりの場所を知っています。そして、残りの扉から、外れを1つ開けます。"),
    dict(id="rule4", face="pose_pointing", vis="rule", sub="ここが大事。私は必ず、外れを開けます。"),
    dict(id="ask", face="pose_thinking", vis="rule", sub="さあ、このまま？それとも、選び直す？"),
    dict(id="guess", face="pose_thinking", vis="guess", sub="そのまま、選び直す、どっちでも同じ。あなたはどれだと思いますか？"),
    dict(id="guess2", face="base", vis="guess", sub="残りは2枚だから、半分半分。そう思った人も、多いはずです。"),
    dict(id="ex1", face="pose_pointing", vis="exp", sub="では、ためしてみます。左は、ずっとそのまま派。右は、必ず選び直す派。金色が当たり、灰色が外れです。"),
    dict(id="x1", face="pose_thinking", vis="exp", sub="まずは1回。"),
    dict(id="x1r", face="base", vis="exp", sub=one + "1回だけでは、まだ分かりませんね。"),
    dict(id="x10", face="pose_thinking", vis="exp", sub="次は10回。"),
    dict(id="x10r", face="base", vis="exp", sub=f"当たりは、そのまま派が{s10}回。選び直す派が{w10}回。"),
    dict(id="x100", face="pose_thinking", vis="exp", sub="100回では？"),
    dict(id="x100r", face="pose_pointing", vis="exp", sub=f"{s100}回と{w100}回。差が見えてきました。"),
    dict(id="x1m", face="pose_excited", vis="exp", sub="いよいよ、1万回です！割合の数字を見てください。最初はゆれますが、だんだん落ち着きます。"),
    dict(id="ansq", face="pose_thinking", vis="exp", sub="結果は…"),
    dict(id="ans1", face="surprised", vis="exp", sub=f"選び直す派は、約{pc(SW['rate'])}。"),
    dict(id="ans2", face="pose_excited", vis="exp", sub=f"そのまま派は、約{pc(ST['rate'])}。選び直すと、当たりが約2倍です！"),
    dict(id="why0", face="pose_thinking", vis="why", sub="なぜでしょう？図で見てみます。"),
    dict(id="why1", face="pose_pointing", vis="why", sub="最初にあなたが選んだ扉。当たりの確率は、3分の1です。"),
    dict(id="why2", face="pose_pointing", vis="why", sub="残りの2枚をまとめると、3分の2。"),
    dict(id="why3", face="base", vis="why", sub="私は、外れを知っていて開けます。すると、この3分の2が、まるごと残りの1枚に乗るんです。"),
    dict(id="h100a", face="pose_pointing", vis="h100", sub="扉が100枚なら、もっと分かりやすいです。"),
    dict(id="h100b", face="base", vis="h100", sub="あなたが1枚選んで、私が外れを98枚開けます。"),
    dict(id="h100c", face="surprised", vis="h100", sub="残ったこの1枚、あやしくないですか？あなたの1枚が当たりなのは、100枚に1枚だけです。"),
    dict(id="life", face="base", vis="life", sub="後から新しい情報が出たら、選び直すと得なこともあります。ただし今回は、司会が答えを知っている時のお話です。"),
    dict(id="end", face="happy", vis="end", sub="答えは、選び直す。当たりが約2倍になります。これはAIのシミュレーションです。次に確かめてほしいこと、コメントで教えてね！"),
]
SPLIT = r"[^。？！…]+[。？！…]*"


def tts_marks(text):
    """vv_ja.tts_script と同じ読み方で、文ごとの開始時刻（marks）も返す"""
    parts = [p for p in re.findall(SPLIT, text) if p.strip()]
    out, marks, t = [], [], 0.0
    for p in parts:
        is_q = "？" in p
        has_num = bool(re.search(r"[0-9０-９]|パーセント|万円|分の", p))
        bright = is_q or "！" in p
        x, sr = vv_ja.tts(p, "amaama" if bright else "normal", 1.0 if has_num else 1.08, 0.02 if bright else 0.0, 1.3 if bright else 1.15)
        x = np.interp(np.arange(int(len(x) * SR / sr)) / SR, np.arange(len(x)) / sr, x).astype(np.float32)
        marks.append(round(t, 3)); out.append(x); t += len(x) / SR
        gap = 0.4 if is_q else 0.5 if "…" in p else 0.18
        out.append(np.zeros(int(SR * gap), np.float32)); t += gap
    return np.concatenate(out), marks


def load_mp3(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def tone(f, d, a, decay):
    t = np.arange(int(d * SR)) / SR
    return a * np.sin(2 * np.pi * f * t) * np.exp(-t / decay)


def noise(d, a, decay, seed=1):
    t = np.arange(int(d * SR)) / SR
    n = np.random.default_rng(seed).standard_normal(len(t)).astype(np.float32)
    n = np.convolve(n, np.ones(6) / 6, "same")
    return a * n * np.exp(-t / decay)


# 場面ごとの「声のあとの間」（秒）。絵が動く時間・答えを止めて見せる時間
PAD = {"hook": 0.5, "hook2": 1.0, "rule1": 0.6, "rule2": 0.9, "rule3": 1.5, "rule4": 1.0, "ask": 1.6, "guess": 0.8, "guess2": 1.0,
       "ex1": 0.8, "x1": 1.8, "x1r": 0.8, "x10": 2.4, "x10r": 1.2, "x100": 2.6, "x100r": 1.2, "x1m": 2.6, "ansq": 0.8,
       "ans1": 1.6, "ans2": 2.8, "why0": 0.4, "why1": 1.2, "why2": 1.4, "why3": 2.0, "h100a": 1.4, "h100b": 3.4, "h100c": 1.6,
       "life": 1.2, "end": 1.8}


def main():
    for s in S:
        s["say"] = to_say(s["sub"])
        kana, bad = check(s["say"])
        if bad:
            raise SystemExit(f"読みの問題 {s['id']}: {bad} {kana}")
    lead, t, parts = 0.3, 0.3, []
    for s in S:
        x, marks = tts_marks(s["say"])
        sp = [p for p in re.findall(SPLIT, s["sub"]) if p.strip()]
        assert len(sp) == len(marks), s["id"]
        acc, mk = 0, []
        for i, p in enumerate(sp):
            mk.append([acc, round(t + marks[i], 3)]); acc += len(p)
        pad = PAD.get(s["id"], 0.3)
        s["start"], s["voice_len"], s["dur"], s["marks"] = round(t, 3), round(len(x) / SR, 3), round(len(x) / SR + pad, 3), mk
        b = np.zeros(int(round(s["dur"] * SR)), np.float32); b[: len(x)] = x
        parts.append(b); t += len(b) / SR
        print(f"{s['id']:7s} {s['start']:7.2f} {s['voice_len']:5.2f}", flush=True)
    SC = {s["id"]: s for s in S}

    def at(sid, word):
        s = SC[sid]; i = s["sub"].find(word)
        assert i >= 0, (sid, word)
        m = s["marks"][0]
        for mk in s["marks"]:
            if mk[0] <= i: m = mk
        nx = next((mk for mk in s["marks"] if mk[0] > i), [len(s["sub"]), s["start"] + s["voice_len"]])
        return round(m[1] + (nx[1] - m[1]) * (i - m[0]) / max(1, nx[0] - m[0]), 3)

    end = lambda sid: round(SC[sid]["start"] + SC[sid]["voice_len"], 3)
    # ---- 時刻の表（絵と音が同じものを使う） ----
    K = dict(
        h_doors=0.3, h_1man=at("hook2", "1万回"),
        r_doors=at("rule1", "3つの扉"), r_gold=at("rule1", "金の宝箱"), r_miss=at("rule1", "残り"),
        r_pick=at("rule2", "選びます"), r_know=at("rule3", "当たりの場所"), r_open=at("rule3", "外れを1つ"),
        r_must=at("rule4", "私は必ず"), a_stay=at("ask", "このまま"), a_sw=at("ask", "選び直す"),
        g1=at("guess", "そのまま"), g2=at("guess", "選び直す"), g3=at("guess", "どっちでも"), g_half=at("guess2", "半分半分"),
        e_left=at("ex1", "左は"), e_right=at("ex1", "右は"), e_col=at("ex1", "金色"),
        x1=end("x1") + 0.15, x10=end("x10") + 0.1, x100=end("x100") + 0.1,
        x1m=at("x1m", "1万回"),
        silence=end("ansq"), ans1=at("ans1", "約"), ans2=at("ans2", "約"), ans_x2=at("ans2", "約2倍"),
        w_pick=at("why1", "最初に"), w_13=at("why1", "3分の1"), w_23=at("why2", "3分の2"), w_open=at("why3", "私は"), w_move=at("why3", "すると"),
        h_grid=SC["h100a"]["start"] + 0.2, h_pick=at("h100b", "1枚選んで"), h_open=at("h100b", "外れを98枚"),
        h_sus=at("h100c", "残った"), h_1in100=at("h100c", "あなたの1枚"),
        l_info=at("life", "後から"), l_but=at("life", "ただし"),
        e_ans=at("end", "答えは"), e_x2=at("end", "当たりが"), e_ai=at("end", "これは"), e_cm=at("end", "次に"),
    )
    # 1万回の点は「1万回です」から、声が終わって間の終わり0.3秒前までに埋める
    K["x1m_fill"] = round(K["x1m"] + 1.0, 3)
    K["x1m_done"] = round(SC["x1m"]["start"] + SC["x1m"]["dur"] - 0.3, 3)
    K["sort"] = round(SC["ans2"]["start"] + SC["ans2"]["dur"] - 2.6, 3)
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
    bgm = os.path.join(P3, "assets", "bgm", "nandeshou.mp3")
    mus = load_mp3(bgm) if os.path.exists(bgm) else np.zeros(SR, np.float32)
    mus = np.tile(mus, len(vo) // len(mus) + 1)[: len(vo)]
    mus = mus / (np.sqrt((mus ** 2).mean()) + 1e-9) * 0.11
    duck = np.repeat(np.array([0.45 if m else 1.0 for m in mouth], np.float32), hop)
    duck = np.convolve(np.pad(duck, (0, len(vo) - len(duck)), constant_values=1.0), np.ones(4800) / 4800, "same")
    # 答えの直前は本当の無音（BGMも止める）
    a, b = int(K["silence"] * SR), int(SC["ans1"]["start"] * SR); duck[a:b] = 0.0
    mix = vo * 0.95 + mus * duck * 0.6
    n = int(1.5 * SR); mix[-n:] *= np.linspace(1, 0, n)

    def put(tm, c):
        a = int(tm * SR)
        if 0 <= a < len(mix): mix[a:a + len(c)] += c[: len(mix) - a]
    kiran = sum(tone(f, 1.0, 0.07, 0.3) for f in (1318.5, 1760, 2637))
    door = noise(0.35, 0.12, 0.08, 3) + tone(110, 0.35, 0.10, 0.1)
    for k in ("ans1", "ans2", "e_ans"): put(K[k], kiran)
    for k in ("r_open", "w_open"): put(K[k], door)
    put(K["r_gold"], tone(1568, 0.6, 0.06, 0.2))
    # 点が出る音：当たり＝高い音、外れ＝低い音（1回・10回は1つずつ）
    for side, bits in ((0, ST["bits"]), (1, SW["bits"])):
        put(K["x1"] + side * 0.35, tone(1046.5 if bits[0] == "1" else 330, 0.3, 0.08, 0.1))
        for i in range(1, 10):
            put(K["x10"] + (i - 1) * 0.14 + side * 0.05, tone(1046.5 if bits[i] == "1" else 330, 0.2, 0.05, 0.06))
    # 100回・1万回は「ざーっ」と上がる音
    for k, d in (("x100", 1.6), ("x1m_fill", K["x1m_done"] - K["x1m_fill"])):
        tt = np.arange(int(d * SR)) / SR
        sw = 0.03 * np.sin(2 * np.pi * (300 * tt + 500 * tt * tt / d)) * np.minimum(1, (d - tt) / 0.3)
        put(K[k], sw.astype(np.float32))
    # 98枚が開く音：小さなコツコツ
    for i in range(98):
        put(K["h_open"] + 0.9 + i * 0.022, tone(700 + (i % 7) * 40, 0.05, 0.02, 0.015))
    mix = np.clip(mix / np.abs(mix).max() * 0.92, -1, 1)
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    with wave.open(os.path.join(HERE, "assets", "mix.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    data = dict(total=round(total, 3), fps=FPS, mouth=mouth, lead=lead, K=K,
                scenes=[{k: s[k] for k in ("id", "sub", "start", "dur", "voice_len", "face", "vis", "marks")} for s in S],
                stay=dict(rate=ST["rate"], theory=ST["theory"], bits=ST["bits"], wins=ST["wins"]),
                sw=dict(rate=SW["rate"], theory=SW["theory"], bits=SW["bits"], wins=SW["wins"]),
                ratio=R["ratio"], n=R["n"], seed=R["seed"])
    with open(os.path.join(HERE, "assets", "data.js"), "w") as f:
        f.write("window.DATA=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";")
    for s in S:
        print(s["id"], vv_ja._get().create_audio_query(s["say"], 2).kana)
    print(f"total {total:.2f}s")
    print(K)


if __name__ == "__main__":
    main()
