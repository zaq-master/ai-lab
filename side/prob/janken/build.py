"""確率のお話②「5人でじゃんけん、1回で決まる確率は？」の台本・声・音・データを作る。
数字は results.json（sim.py）からだけ入れる。時刻の表 K はここで1回だけ作り、絵（data.js）と音（mix.wav）が同じ表を使う。
仕様：side/prob/SPEC.md　お手本：side/videos/2026-11-27_kikan/build.py
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
from yomi import check, to_say as _to_say  # noqa: E402

LOCAL = [("2組", "ふたくみ"), ("1組", "ひとくみ")]


def to_say(s):
    for a, b in LOCAL:
        s = s.replace(a, b)
    return _to_say(s)


SR, FPS = 48000, 30
R = json.load(open(os.path.join(HERE, "results.json")))
P = {int(k): v for k, v in R["people"].items()}
pc = lambda x: f"{round(x * 100):.0f}%"
p5 = P[5]["p_sim"]
HN = ["グー", "チョキ", "パー"]
H10 = R["five_hands10"]
# 話の流れが結果と合っているか（合わなければ台本を作らない）
assert len(set(H10[0])) == 2 and len(set(H10[1])) == 3 and len(set(H10[2])) == 1, "実演の3回が 決まる／3種類／全員同じ になっていない"
assert p5 < 0.5 and 0.34 < p5 < 0.40, "「半分より少ない・3回に1回ちょっと」が成り立たない"
assert pc(P[5]["p_sim"]) == pc(P[5]["p_theory"]), "5人の答えが計算と%で一致しない"
assert all(P[n]["p_sim"] > P[n + 1]["p_sim"] for n in range(3, 10)), "人数で下がっていない"
PK = R["pick1"]
assert PK["split_sim"] < PK["all10_sim"], "分けても早くならない"


def cnt(h):
    return {HN[k]: h.count(k) for k in range(3) if h.count(k)}


c1 = cnt(H10[0])
win1 = [HN[a] for a in range(3) for b in range(3) if a in H10[0] and b in H10[0] and (a, b) in ((0, 1), (1, 2), (2, 0))][0]
who1 = "、".join(f"{k}が{v}人" for k, v in c1.items())
same3 = HN[H10[2][0]]
r10 = round(P[10]["rounds_sim"])

S = [
    dict(id="hook", face="surprised", vis="hook", sub="5人でじゃんけん。1回で勝負が決まる確率は、どれくらい？"),
    dict(id="hook2", face="pose_pointing", vis="hook", sub="1万回やって、確かめてみます。"),
    dict(id="demo1", face="base", vis="demo1", sub=f"まず、1回やってみます。{who1}。"),
    dict(id="demo1r", face="pose_excited", vis="demo1", sub=f"{win1}の勝ちで、決まりました！"),
    dict(id="demo2", face="pose_thinking", vis="demo2", sub="2回目。グー、チョキ、パーが、ぜんぶ出ました。これは、あいこです。"),
    dict(id="demo3", face="troubled", vis="demo3", sub=f"3回目は、全員{same3}。これも、あいこ。"),
    dict(id="rule", face="pose_pointing", vis="rule", sub="つまり、出た手がちょうど2種類なら、決まり。1種類か3種類なら、あいこです。"),
    dict(id="guess", face="pose_thinking", vis="guess", sub="では、5人で1回で決まるのは、半分より多い？少ない？ちょっと考えてみてね。"),
    dict(id="ten", face="base", vis="ten", sub=f"まず、10回やってみます。決まったのは、{R['five_first10']}回。"),
    dict(id="hund", face="pose_pointing", vis="hund", sub=f"次は100回。金色が決まった回、灰色があいこです。100回では、{R['five_first100']}回。"),
    dict(id="man", face="pose_excited", vis="man", sub="いよいよ、1万回。点の1つ1つが、じゃんけん1回です。ぜんぶ数えると…"),
    dict(id="ans", face="surprised", vis="ans", sub=f"決まったのは…{pc(p5)}。"),
    dict(id="ans2", face="pose_pointing", vis="ans", sub=f"半分より少なくて、3回に1回ちょっと。計算で出した答えも{pc(P[5]['p_theory'])}で、ぴったり合いました。"),
    dict(id="ppl", face="pose_thinking", vis="ppl", sub="では、人数を変えると？"),
    dict(id="ppl2", face="pose_pointing", vis="ppl",
         sub=f"2人なら{pc(P[2]['p_sim'])}。5人で{pc(P[5]['p_sim'])}。10人だと、たった{pc(P[10]['p_sim'])}。人数が増えるほど、決まりにくくなります。"),
    dict(id="tenr", face="troubled", vis="tenr", sub=f"10人だと、決まるまで、平均で約{r10}回。ずっと、あいこが続くんです。"),
    dict(id="why", face="pose_thinking", vis="why", sub=f"なぜでしょう？5人の手の出し方は、3を5回かけて、{P[5]['ways']}通り。"),
    dict(id="why2", face="pose_pointing", vis="why", sub=f"そのうち、決まるのは、ちょうど2種類の{P[5]['ways_dec']}通りだけ。"),
    dict(id="why3", face="base", vis="why", sub=f"全員同じが{P[5]['ways_same']}通り。3種類ぜんぶ出るのが{P[5]['ways_three']}通り。これが、あいこです。"),
    dict(id="why4", face="pose_pointing", vis="why4", sub="人数が増えると、だれか1人は、ちがう手を出しがち。だから、3種類ぜんぶ出る形が、どんどん増えるんです。"),
    dict(id="tip", face="pose_excited", vis="tip",
         sub=f"大人数なら、分けるのがコツ。10人で1人を選ぶとき、全員いっぺんだと、最後の1人まで平均{round(PK['all10_sim'])}回。"),
    dict(id="tip2", face="happy", vis="tip", sub=f"5人ずつ2組で代表を決めて、決勝をすると、合わせて平均{round(PK['split_sim'])}回です。"),
    dict(id="sum", face="base", vis="sum", sub=f"まとめ。5人のじゃんけんが1回で決まるのは、{pc(p5)}。人数が多いほど、あいこが増えます。"),
    dict(id="end", face="happy", vis="end", sub="これはAIのシミュレーションです。次に確かめてほしいこと、コメントで教えてね！"),
]


def split_parts(text):
    return [p for p in re.findall(r"[^。？！…]+[。？！…]*", text) if p.strip()]


def tts_marks(text):
    """vv_ja.tts_script と同じ読み方で、文ごとの開始時刻（marks）も返す"""
    out, marks, t = [], [], 0.0
    for p in split_parts(text):
        is_q = "？" in p
        has_num = bool(re.search(r"[0-9０-９]|パーセント|万|分の", p))
        bright = is_q or "！" in p
        x, sr = vv_ja.tts(p, "amaama" if bright else "normal", 0.98 if has_num else 1.06, 0.02 if bright else 0.0, 1.3 if bright else 1.12)
        x = np.interp(np.arange(int(len(x) * SR / sr)) / SR, np.arange(len(x)) / sr, x).astype(np.float32)
        marks.append(round(t, 3)); out.append(x); t += len(x) / SR
        gap = 0.45 if is_q else 0.5 if "…" in p else 0.16
        out.append(np.zeros(int(SR * gap), np.float32)); t += gap
    return np.concatenate(out), marks


def load_mp3(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
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
        if len(split_parts(s["say"])) != len(split_parts(s["sub"])):
            raise SystemExit(f"文の数が合わない {s['id']}")
    lead, t, parts = 0.4, 0.4, []
    # 数字・答えの場面は読み終わってから長めに止める（2.5秒以上）。答えの直前は本当の無音
    PAD = {"hook": 0.5, "demo1": 0.9, "demo1r": 0.8, "demo2": 0.7, "demo3": 0.6, "rule": 1.6, "guess": 2.2, "ten": 1.6, "hund": 1.6,
           "man": 1.4, "ans": 2.6, "ans2": 1.0, "ppl2": 1.6, "tenr": 1.6, "why": 1.2, "why2": 1.2, "why3": 1.6, "why4": 1.6,
           "tip": 0.8, "tip2": 2.0, "sum": 1.6, "end": 1.8}
    EXTRA = {"man": 7.5, "ten": 2.2, "hund": 0.0}  # 1万回の点が埋まるのを見せる時間（声のあと）
    for s in S:
        x, marks = tts_marks(s["say"])
        sp = split_parts(s["sub"])
        acc, mk = 0, []
        for i, p in enumerate(sp):
            mk.append([acc, round(t + marks[i], 3)]); acc += len(p)
        pad = PAD.get(s["id"], 0.35) + EXTRA.get(s["id"], 0)
        s["start"], s["voice_len"], s["dur"], s["marks"] = round(t, 3), round(len(x) / SR, 3), round(len(x) / SR + pad, 3), mk
        b = np.zeros(int(s["dur"] * SR), np.float32)
        if s["id"] == "man":   # 「ぜんぶ数えると…」の前に、点が埋まる時間を入れる（声を2つに分ける）
            cut = int((marks[-1]) * SR); b[:cut] = x[:cut]; ins = int(EXTRA["man"] * SR)
            rest = x[cut:]; b[cut + ins: cut + ins + len(rest)] = rest[: len(b) - cut - ins]
            s["marks"][-1][1] = round(s["marks"][-1][1] + EXTRA["man"], 3); s["fill"] = [round(t + marks[-2] + 1.2, 3), round(t + marks[-1] + EXTRA["man"] - 0.3, 3)]
            s["voice_len"] = round(s["voice_len"] + EXTRA["man"], 3)
        elif s["id"] == "ten":  # 「決まったのは」の前に、10回の結果が並ぶ時間を入れる
            cut = int((marks[-1]) * SR); b[:cut] = x[:cut]; ins = int(EXTRA["ten"] * SR)
            rest = x[cut:]; b[cut + ins: cut + ins + len(rest)] = rest[: len(b) - cut - ins]
            s["marks"][-1][1] = round(s["marks"][-1][1] + EXTRA["ten"], 3); s["voice_len"] = round(s["voice_len"] + EXTRA["ten"], 3)
        else:
            b[: len(x)] = x
        parts.append(b); t += s["dur"]
        print(s["id"], s["start"], s["voice_len"], s["dur"], flush=True)
    SC = {s["id"]: s for s in S}

    def at(sid, word):
        s = SC[sid]; i = s["sub"].find(word)
        assert i >= 0, (sid, word)
        m = s["marks"][0]
        for mk in s["marks"]:
            if mk[0] <= i: m = mk
        nx = next((mk for mk in s["marks"] if mk[0] > i), None)
        end = nx[1] - 0.16 if nx else s["start"] + s["voice_len"]
        L = (nx[0] if nx else len(s["sub"])) - m[0]
        return round(m[1] + 0.05 + (end - m[1]) * (i - m[0]) / max(1, L), 3)

    man = SC["man"]
    K = dict(
        h_q=at("hook", "1回で"), h2=at("hook2", "1万回"),
        d1_go=at("demo1", "まず") + 1.0, d1_res=at("demo1r", "の勝ち") - 0.3,
        d2_go=at("demo2", "2回目") + 0.3, d2_res=at("demo2", "これは"), d3_go=SC["demo3"]["start"] + 0.2, d3_res=at("demo3", "これも"),
        rc2=at("rule", "ちょうど2種類"), rc13=at("rule", "1種類か"),
        g_a=at("guess", "半分より多い"), g_b=at("guess", "少ない"),
        ten_go=at("ten", "まず") + 0.9, ten_num=at("ten", "決まったのは") + 0.7,
        hu_go=SC["hund"]["start"] + 0.3, hu_col=at("hund", "金色"), hu_num=at("hund", "100回では") + 0.8,
        m_go=man["fill"][0], m_end=man["fill"][1], m_say=at("man", "ぜんぶ"),
        a_num=at("ans", pc(p5)), a_half=at("ans2", "半分"), a_th=at("ans2", "計算で"),
        p_q=SC["ppl"]["start"] + 0.2, p2=at("ppl2", "2人"), p5=at("ppl2", "5人"), p10=at("ppl2", "10人"), p_all=at("ppl2", "人数が"),
        tr_go=SC["tenr"]["start"] + 0.3, tr_num=at("tenr", "平均"),
        w_tot=at("why", "3を5回"), w_num=at("why", f"{P[5]['ways']}通り"), w_dec=at("why2", "ちょうど"), w_same=at("why3", "全員同じ"), w_three=at("why3", "3種類"), w_aiko=at("why3", "これが"),
        w4_go=SC["why4"]["start"] + 0.3, w4_more=at("why4", "だから"),
        tp_all=at("tip", "全員いっぺん"), tp_split=at("tip2", "5人ずつ"), tp_num=at("tip2", "合わせて"),
        s1=at("sum", "5人の"), s2=at("sum", "人数が"),
    )
    K = {k: round(v, 3) for k, v in K.items()}
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
    # 答えの直前0.6秒は BGM も止める（本当の無音）
    for k in ("a_num",):
        a, b = int((K[k] - 0.6) * SR), int((K[k] - 0.05) * SR); duck[a:b] = 0.0
    mix = vo * 0.95 + mus * duck * 0.6

    def put(tsec, c):
        a = int(tsec * SR)
        if a < len(mix): mix[a:a + len(c)] += c[: len(mix) - a]

    kiran = sum(tone(f, 1.0, 0.07, 0.3) for f in (1318.5, 1760, 2637))
    boo = tone(220, 0.35, 0.09, 0.12) + tone(196, 0.35, 0.06, 0.12)
    pon = lambda f=880: tone(f, 0.18, 0.06, 0.05)
    # 実演：手が1つずつ出る「ポン」＋結果（決まり＝キラン、あいこ＝ブー）
    for go in ("d1_go", "d2_go", "d3_go"):
        for i in range(5): put(K[go] + i * 0.16, pon(660 + 110 * i))
    put(K["d1_res"], kiran); put(K["d2_res"], boo); put(K["d3_res"], boo)
    for i in range(10): put(K["ten_go"] + i * 0.3, pon(1046 if (R["five_dec"][i] == "1") else 523))
    put(K["ten_num"], kiran); put(K["hu_num"], kiran)
    # 1万回：点が埋まる間、だんだん高くなる細かい音
    m0, m1 = K["m_go"], K["m_end"]
    for j in range(40):
        u = j / 40; put(m0 + (m1 - m0) * (1 - (1 - u) ** 2), tone(500 + 900 * u, 0.08, 0.035, 0.03))
    put(K["a_num"], kiran * 1.4)
    for k, n in (("p2", 2), ("p5", 5), ("p10", 10)):   # 割合が高いほど高い音
        put(K[k], tone(440 * 2 ** ((P[n]["p_sim"] - 0.4) * 24 / 12), 0.5, 0.08, 0.15))
    put(K["tr_num"], kiran); put(K["w_dec"], kiran); put(K["w_three"], boo); put(K["tp_split"] + 1.0, kiran)
    n = int(1.5 * SR); mix[-n:] *= np.linspace(1, 0, n)
    mix = np.clip(mix / np.abs(mix).max() * 0.92, -1, 1)
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    with wave.open(os.path.join(HERE, "assets", "mix.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    data = dict(total=round(total, 3), fps=FPS, mouth=mouth, lead=lead, K=K, seed=R["seed"], trials=R["trials"],
                scenes=[{k: s[k] for k in ("id", "sub", "start", "dur", "voice_len", "face", "vis", "marks")} for s in S],
                P={n: {q: P[n][q] for q in ("p_sim", "p_theory", "rounds_sim", "ways", "ways_dec", "ways_same", "ways_three")} for n in P},
                H10=H10, dec=R["five_dec"], first10=R["five_first10"], first100=R["five_first100"], all=R["five_all"],
                pick=PK, r10=r10, win1=win1)
    with open(os.path.join(HERE, "assets", "data.js"), "w") as f:
        f.write("window.DATA=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";")
    print(f"total {total:.2f}s", K)


if __name__ == "__main__":
    main()
