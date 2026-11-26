"""確率のお話③「くじ引きは、先に引いた人が得？」の台本・声・音・データを作る。
数字は results.json（sim.py）からだけ入れる。
時刻の表（K）はここで1回だけ作り、絵（data.js）と音（mix.wav）の両方が同じ表を使う。
実行：python3 sim.py && python3 build.py → assets/{mix.wav,data.js}
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

SR, FPS = 48000, 30
R = json.load(open(os.path.join(HERE, "results.json")))
W = R["first_winner"]
pc = lambda x: f"{round(x * 100):.0f}%"
c10, c100 = R["cnt1_first10"], R["cnt1_first100"]
assert R["cnt1"][0] + sum(R["cnt1"][1:]) == R["n"]
ZERO10 = min(c10) == 0
P3MIN, P3MAX = min(R["pct3"]), max(R["pct3"])
assert pc(P3MIN) == pc(P3MAX) == "30%", "3本のとき、どれも約30%とは言えない"
assert all(abs(p - 0.1) < 0.008 for p in R["pct1"]), "どれも約10%とは言えない"

# 読みの直し（分数は「〜ぶんの〜」、早い者勝ち、上がる分 など）
SAY = [("早い者勝ち", "はやいものがち"), ("上がる分", "上がるぶん"), ("取られる分", "取られるぶん"), ("見た後", "見たあと")]


def to_say(s):
    for a, b in SAY:
        s = s.replace(a, b)
    s = re.sub(r"(\d+)分の(\d+)", r"\1ぶんの\2", s)
    return _to_say(s)


S = [
    dict(id="hook", face="surprised", vis="hook", sub="くじ引きって、先に引いた人が得なの？"),
    dict(id="hook2", face="pose_pointing", vis="hook", sub="それとも、残り物には福がある？1万回ためして、確かめます。"),
    dict(id="rule", face="base", vis="rule", sub="くじは10本。当たりは1本だけです。"),
    dict(id="rule2", face="pose_pointing", vis="rule", sub="10人が順番に、1本ずつ引きます。引いたくじは、戻しません。ズルもなしです。"),
    dict(id="rule3", face="pose_thinking", vis="rule", sub="そして確率は、前の人の結果を、見る前に考えます。"),
    dict(id="demo", face="base", vis="demo", sub="まずは1回、やってみます。1番目の人から、順番に引いて、開けていきます。"),
    dict(id="demo_r", face="happy", vis="demo", sub=f"今回は、{W}番目の人が当たりでした。"),
    dict(id="guess", face="pose_thinking", vis="guess", sub="これを何回もやったら、どうなるでしょう？先に引く人が得？後の人が得？それとも、同じ？"),
    dict(id="e10", face="pose_pointing", vis="exp", sub="まずは10回。当たった人の色の点を、1回に1つ置きます。"),
    dict(id="e10b", face="pose_thinking", vis="exp", sub=("10回だと、1回も当たらない人もいて、ばらばらです。" if ZERO10 else "10回だと、まだばらばらです。")),
    dict(id="e100", face="pose_pointing", vis="exp", sub="100回にすると…"),
    dict(id="e100b", face="pose_thinking", vis="exp", sub="まだ、でこぼこですね。"),
    dict(id="e1m", face="pose_pointing", vis="exp1m", sub="では、1万回。点も、1万個です。"),
    dict(id="e1m2", face="pose_thinking", vis="exp1m", sub="色ごとに、集めてみると…"),
    dict(id="answer", face="surprised", vis="exp1m", sub="何番目の人も、ほぼ同じ。どれも約10%です！"),
    dict(id="why", face="pose_pointing", vis="why", sub="なぜでしょう？1番目の人は、10本から1本。10分の1です。"),
    dict(id="why2", face="base", vis="why", sub="2番目の人は、まず1番目が外れて、10分の9。次に、残り9本から当たりで、9分の1。"),
    dict(id="why3", face="pose_excited", vis="why", sub="かけると、9が消えて、10分の1！"),
    dict(id="why4", face="pose_pointing", vis="why", sub="3番目も、かけると9と8が消えて、やっぱり10分の1です。"),
    dict(id="deal", face="base", vis="deal", sub="別の見方もあります。10本を先に10人へ配って、一斉に開けるのと同じこと。"),
    dict(id="deal2", face="pose_pointing", vis="deal", sub="当たりがだれの手にあるかは、10人とも同じですよね。"),
    dict(id="feel", face="pose_thinking", vis="feel", sub="でも、前の人が外れたら、後の人は有利になるのでは？"),
    dict(id="feel2", face="pose_pointing", vis="feel", sub=f"はい。3人が外れたのを見た後なら、4番目は7本から1本。約{pc(R['cond4'])}に上がります。"),
    dict(id="feel3", face="troubled", vis="feel", sub="でも、引く前に考えると、先に当たりを取られる回もあります。"),
    dict(id="feel4", face="base", vis="feel", sub="上がる分と、取られる分で、ちょうど10%のままなんです。"),
    dict(id="three", face="surprised", vis="three", sub=f"当たりが3本なら？1万回ためすと、どの順番も約{pc(P3MIN)}。やっぱり同じでした。"),
    dict(id="sum", face="base", vis="sum", sub="答えです。戻さない、ズルなしのくじなら、先に引いても後に引いても、当たる確率は同じ。"),
    dict(id="sum2", face="happy", vis="sum", sub="残り物には福がある、も、早い者勝ち、も、当たる確率については、気のせいでした。"),
    dict(id="end", face="happy", vis="end", sub="これはAIのシミュレーションです。次に確かめてほしい言い伝え、コメントで教えてね！"),
]
SPLIT = r"[^。？！…]+[。？！…]*"

# 絵の動きの長さ（index.html と同じ値を data.js で渡す）
DEMO_STEP, E10_STEP, E100_DUR, FILL_DUR, SORT_DUR = 0.85, 0.42, 4.0, 4.2, 2.4


def tts_marks(text):
    """vv_ja.tts_script と同じ読み方で、文ごとの開始時刻（marks）も返す"""
    parts = [p for p in re.findall(SPLIT, text) if p.strip()]
    out, marks, pos, t = [], [], 0, 0.0
    for p in parts:
        is_q = "？" in p
        has_num = bool(re.search(r"[0-9０-９]|パーセント|ぶんの", p))
        bright = is_q or "！" in p
        q = vv_ja._get().create_audio_query(p, 0 if bright else 2)
        q.speed_scale, q.pitch_scale, q.intonation_scale = (1.0 if has_num else 1.1), (0.02 if bright else 0.0), (1.3 if bright else 1.1)
        q.pre_phoneme_length, q.post_phoneme_length = 0.05, 0.05
        import io
        w = vv_ja._get().synthesis(q, 0 if bright else 2)
        with wave.open(io.BytesIO(w)) as f:
            x = np.frombuffer(f.readframes(f.getnframes()), np.int16).astype(np.float32) / 32768; sr = f.getframerate()
        x = np.interp(np.arange(int(len(x) * SR / sr)) / SR, np.arange(len(x)) / sr, x).astype(np.float32)
        marks.append([pos, round(t, 3)]); out.append(x); t += len(x) / SR
        gap = 0.35 if is_q else 0.45 if "…" in p else 0.12
        out.append(np.zeros(int(SR * gap), np.float32)); t += gap
        pos += len(p)
    return np.concatenate(out), marks


def load_mp3(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def tone(f, d, a, decay):
    t = np.arange(int(d * SR)) / SR
    return a * np.sin(2 * np.pi * f * t) * np.exp(-t / decay)


def at_in(s, word):
    i = s["sub"].find(word)
    assert i >= 0, (s["id"], word)
    m = s["marks"][0]
    for mk in s["marks"]:
        if mk[0] <= i: m = mk
    nx = next((mk for mk in s["marks"] if mk[0] > i), [len(s["sub"]), s["start"] + s["voice_len"]])
    return round(m[1] + (nx[1] - m[1]) * (i - m[0]) / max(1, nx[0] - m[0]), 3)


def main():
    for s in S:
        s["say"] = "".join(to_say(p) for p in re.findall(SPLIT, s["sub"]))
        kana, bad = check(s["say"])
        k2 = "".join(vv_ja._get().create_audio_query(p, 2).kana for p in re.findall(SPLIT, s["say"]) if p.strip())
        if "フンノ" in k2 or "プンノ" in k2 or "シャガチ" in k2:
            bad.append("分数・早い者勝ちの読み")
        print(s["id"], k2, flush=True)
        if bad:
            raise SystemExit(f"読みの問題 {s['id']}: {bad} {kana}")
    lead, t, parts = 0.5, 0.5, []
    # 声のあとの間。絵の動きが終わるまで待つ所は、必要な時刻から計算する
    PAD = {"hook2": 0.5, "rule3": 0.5, "demo_r": 1.0, "guess": 1.6, "e10b": 0.5, "e100b": 0.5, "answer": 2.9, "why3": 1.0, "why4": 1.2,
           "deal": 0.6, "deal2": 0.8, "feel2": 1.0, "feel4": 1.2, "three": 2.6, "sum": 0.8, "sum2": 1.0, "end": 1.6}
    NEED = {  # 場面の終わりまでに必要な絶対時刻
        "demo": lambda s: at_in(s, "1番目の人から") + 10 * DEMO_STEP + 0.6,
        "e10": lambda s: at_in(s, "当たった人") + 10 * E10_STEP + 0.6,
        "e100": lambda s: at_in(s, "100回") + 0.5 + E100_DUR + 0.5,
        "e1m": lambda s: at_in(s, "1万個") + FILL_DUR + 0.4,
        "e1m2": lambda s: at_in(s, "集めて") + SORT_DUR + 1.3,   # 並べ終わり→本当の無音→答え
    }
    for s in S:
        x, marks = tts_marks(s["say"])
        sp = [p for p in re.findall(SPLIT, s["sub"]) if p.strip()]
        acc, mk = 0, []
        for i, p in enumerate(sp):
            mk.append([acc, round(t + marks[min(i, len(marks) - 1)][1], 3)]); acc += len(p)
        s["start"], s["voice_len"], s["marks"] = round(t, 3), round(len(x) / SR, 3), mk
        pad = PAD.get(s["id"], 0.25)
        if s["id"] in NEED:
            pad = max(pad, NEED[s["id"]](s) - (t + len(x) / SR))
        s["dur"] = round(len(x) / SR + pad, 3)
        b = np.zeros(int(round(s["dur"] * SR)), np.float32); b[: len(x)] = x
        parts.append(b); t += len(b) / SR
        print(s["id"], s["start"], s["voice_len"], round(pad, 2), flush=True)
    SC = {s["id"]: s for s in S}
    at = lambda sid, w: at_in(SC[sid], w)

    K = dict(
        h_q=at("hook2", "それとも"), h_n=at("hook2", "1万回"),
        r_ten=at("rule", "くじは"), r_one=at("rule", "当たりは"), r_order=at("rule2", "10人"), r_back=at("rule2", "引いたくじ"), r_fair=at("rule2", "ズル"), r_before=at("rule3", "そして"),
        d_go=at("demo", "1番目の人から"), d_res=at("demo_r", "今回"),
        g_a=at("guess", "先に"), g_b=at("guess", "後の人"), g_c=at("guess", "それとも"),
        e10=at("e10", "当たった人"), e10b=SC["e10b"]["start"], e100=at("e100", "100回") + 0.5, e1m=at("e1m", "1万個"), sort=at("e1m2", "集めて"),
        ans=at("answer", "どれも"), ans0=SC["answer"]["start"],
        w1=at("why", "1番目"), w2a=at("why2", "まず"), w2b=at("why2", "次に"), w2c=SC["why3"]["start"], w2eq=at("why3", "10分の1"),
        w3=at("why4", "3番目"), w3c=at("why4", "かけると"), w3eq=at("why4", "やっぱり"),
        dl_give=at("deal", "10本を"), dl_open=at("deal", "一斉"), dl_same=at("deal2", "10人とも"),
        f_seen=at("feel2", "3人"), f_up=at("feel2", "約"), f_before=at("feel3", "先に"), f_keep=at("feel4", "ちょうど"),
        th_go=at("three", "1万回"), th_num=at("three", "どの順番"),
        s1=at("sum", "戻さない"), s1b=at("sum", "先に引いても"), s2a=at("sum2", "残り物"), s2b=at("sum2", "早い者勝ち"), s2c=at("sum2", "気のせい"),
    )
    vo = np.concatenate([np.zeros(int(lead * SR), np.float32)] + parts)
    total = len(vo) / SR
    assert 170 <= total < 179.5, f"長さ {total:.1f}秒"
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
    # 答えの直前0.8秒は、BGMも止める（本当の無音）
    a, b = int((K["ans0"] - 0.8) * SR), int(K["ans0"] * SR); duck[a:b] = 0.0
    mix = vo * 0.95 + mus * duck * 0.6

    def add(tt, c):
        a = int(tt * SR)
        if 0 <= a < len(mix): mix[a:a + len(c)] += c[: len(mix) - a]
    chime = sum(tone(f, 1.0, 0.07, 0.3) for f in (1318.5, 1760, 2637))
    # くじを開ける音：はずれ＝低い「ポン」、当たり＝キラン
    order = R["first_round"]
    for i in range(10):
        tt = K["d_go"] + i * DEMO_STEP + 0.45
        add(tt, chime if order[i] == 0 else tone(330, 0.25, 0.08, 0.06))
    # 点が積もる音（10回・100回）。高さは列の番号（1番目が低い）
    win1 = R["win1"]
    for i in range(10):
        add(K["e10"] + i * E10_STEP + 0.3, tone(523 * 2 ** (win1[i] / 12), 0.2, 0.06, 0.05))
    for i in range(10, 100):
        u = (i - 10) / 90; tt = K["e100"] + E100_DUR * (1 - (1 - u) ** 1.6)
        if i % 3 == 0: add(tt + 0.3, tone(523 * 2 ** (win1[i] / 12), 0.12, 0.035, 0.03))
    # 1万個：さらさら音
    n = int(FILL_DUR * SR); rs = np.random.default_rng(1)
    add(K["e1m"], (rs.standard_normal(n) * 0.02 * np.sin(np.linspace(0, np.pi, n))).astype(np.float32))
    n = int(SORT_DUR * SR)
    sw = np.convolve(rs.standard_normal(n), np.ones(30) / 30, "same") * 0.06 * np.sin(np.linspace(0, np.pi, n))
    add(K["sort"], sw.astype(np.float32))
    for k in ("ans", "w2eq", "w3eq", "dl_open", "f_up", "th_num", "s1b"):
        add(K[k], chime)
    mix = np.clip(mix / np.abs(mix).max() * 0.92, -1, 1)
    n = int(1.5 * SR); mix[-n:] *= np.linspace(1, 0, n)
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    with wave.open(os.path.join(HERE, "assets", "mix.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    data = dict(total=round(total, 3), fps=FPS, mouth=mouth, lead=lead, K=K,
                scenes=[{k: s[k] for k in ("id", "sub", "start", "dur", "voice_len", "face", "vis", "marks")} for s in S],
                step=dict(demo=DEMO_STEP, e10=E10_STEP, e100=E100_DUR, fill=FILL_DUR, sort=SORT_DUR),
                R={k: R[k] for k in ("seed", "n", "first_round", "first_winner", "win1", "cnt1", "pct1", "pct3", "cnt3", "cond4", "theory_cond4", "left4", "win4_after3miss")})
    with open(os.path.join(HERE, "assets", "data.js"), "w") as f:
        f.write("window.DATA=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";")
    print(f"total {total:.2f}s", K)


if __name__ == "__main__":
    main()
