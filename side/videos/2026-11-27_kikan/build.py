"""3分動画「1回だけ打つ人と、1年打つ人。勝ってる人の割合は？」の台本・声・音・データを作る。
数字は results_16.json / results_16.8.json（sim.py）からだけ入れる。企画書：PLAN.md
時刻の表（K）は ここで1回だけ作り、絵（data.js）と音（mix.wav）の両方が同じ表を使う。
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
P3 = os.path.join(HERE, "..", "..", "pachi3d")
sys.path.insert(0, P3)
import vv_ja  # noqa: E402
from yomi import check, to_say  # noqa: E402

SR, FPS = 48000, 30
A = json.load(open(os.path.join(HERE, "results_16.json")))
Z = json.load(open(os.path.join(HERE, "results_16.8.json")))
C, CZ = A["check"], Z["check"]
PER = ["1回", "1ヶ月", "3ヶ月", "半年", "1年", "2年", "5年"]
pc = lambda x: f"{round(x * 100):.0f}%"
man = lambda y: f"約{abs(y) / 10000:.1f}万円"
yen100 = lambda y: f"約{round(abs(y), -2):,.0f}円"
y1 = C["1年"]
# 話の流れが結果と合っているか（合わなければ台本を作らない）
assert C["1回"]["win"] < C["1ヶ月"]["win"], "1ヶ月で増えていない"
assert C["5年"]["win"] < C["半年"]["win"] < C["3ヶ月"]["win"] + 0.01, "ゆっくり減っていない"
FIVE_BELOW_ONE = C["5年"]["win"] < C["1回"]["win"]
assert CZ["5年"]["win"] > CZ["半年"]["win"] - 0.01, "取り分ゼロの台で下がっている"
assert -y1["p10"] > y1["p90"], "負ける側のほうが大きい、が成り立たない"
T = A["traj10"]; n_up = sum(1 for p in range(10) if T[103][p] > 0)
peak = max(C["1ヶ月"]["win"], C["3ヶ月"]["win"])

S = [
    dict(id="hook", face="surprised", vis="hook", sub="パチンコで勝ってる人、まわりにいますよね？"),
    dict(id="hook2", face="pose_pointing", vis="hook",
         sub="じゃあ、打つ期間が長くなると、勝ってる人は増える？減る？1万人で、5年分ためします。"),
    dict(id="rule", face="base", vis="rule",
         sub="台は、e東京喰種のスペック。1000円で16回転、等価。週に2回、1回最大4時間、財布は2万円までです。"),
    dict(id="rule2", face="pose_pointing", vis="rule", sub="全員まったく同じルールで、変えるのは、打った期間だけです。"),
    dict(id="guess", face="pose_thinking", vis="guess", sub="1回だけと、5年間。プラスの人が多いのは、どっちだと思いますか？"),
    dict(id="d1", face="pose_thinking", vis="d1", sub="まずは、1回だけ。プラスで帰れた人は…"),
    dict(id="d1r", face="surprised", vis="d1",
         sub=f"{pc(C['1回']['win'])}。5人に1人だけ。平均の収支はマイナス{yen100(C['1回']['mean'])}なのに、真ん中の人は、2万円をほぼ全部なくしています。4時間打つつもりでも、{"4回に3回" if 0.7 < A["day_broke_mean"] < 0.8 else pc(A["day_broke_mean"])}は、財布が先に空になるんです。"),
    dict(id="m1", face="pose_thinking", vis="m1", sub="じゃあ、1ヶ月から3ヶ月、続けたら？"),
    dict(id="m1r", face="pose_excited", vis="m1", sub=f"約{pc(peak)}。プラスの人が、むしろ増えました！"),
    dict(id="why1", face="pose_pointing", vis="why1",
         sub=f"理由は2つ。1回で負けるのは最大2万円なのに、勝つときは、上位1割の人で{man(C['1回']['p90'])}以上。それに、何回か足すと、運の偏りがならされるから。"),
    dict(id="line", face="pose_pointing", vis="line",
         sub=f"では、もっと続けると…半年で{pc(C['半年']['win'])}。1年で{pc(y1['win'])}。2年で{pc(C['2年']['win'])}。5年で{pc(C['5年']['win'])}。"
             + ("1回だけのときより、少なくなりました。" if FIVE_BELOW_ONE else "1回だけのときと、ほぼ同じまで戻りました。" if C["5年"]["win"] - C["1回"]["win"] < 0.02 else "ゆっくり、減り続けます。")),
    dict(id="house", face="base", vis="house",
         sub=f"下がっていく理由は、お店の取り分。1時間あたり平均{round(abs(y1['yen_per_hour']), -1):.0f}円ずつ削られて、1年、約{round(y1['hours'], -1):.0f}時間遊ぶと、平均マイナス{man(y1['mean'])}です。"),
    dict(id="zero", face="pose_pointing", vis="zero",
         sub=f"仮に、お店の取り分がゼロの台だったら？プラスの人は減らずに、1年で{pc(CZ['1年']['win'])}、5年で{pc(CZ['5年']['win'])}。"),
    dict(id="compare", face="surprised", vis="compare",
         sub=f"でも、1年後のプラスの人は、{pc(y1['win'])}と{pc(CZ['1年']['win'])}。これだと見分けにくい。差がはっきり出るのは金額で、真ん中の人は、マイナス{man(y1['median'])}と、マイナス{man(CZ['1年']['median'])}です。"),
    dict(id="money", face="troubled", vis="money",
         sub=f"16回転の台の1年後は、下位1割の人がマイナス{man(y1['p10'])}以下。上位1割はプラス{man(y1['p90'])}以上。負ける側のほうが、大きいんです。"),
    dict(id="ten", face="pose_pointing", vis="ten",
         sub=f"10人だけ、1年の動きを見ると…{"半分以上" if n_up < 5 else "多く"}の人は、じわじわ下がっていきます。でも、ときどき、ドンと上がる人がいるんです。"),
    dict(id="hist", face="pose_thinking", vis="hist",
         sub="1年後の1万人を並べると、山はマイナス側。プラス側には、細く長いすそ。負けた人はやめて話さなくなるので、勝った話ばかり聞こえるんです。"),
    dict(id="sum", face="base", vis="sum",
         sub="まとめです。プラスの人の割合は、損の大きさを表しません。勝ってる人がいても、甘い台とは限りません。長く続けるほど、お店の取り分が積み重なります。"),
    dict(id="end", face="happy", vis="end",
         sub="これはAIのシミュレーションで、必勝法ではありません。遊ぶお金と時間は、先に決めておこうね。次のネタ、コメントで教えてね！"),
]


def tts_marks(text):
    """vv_ja.tts_script と同じ読み方で、文ごとの開始時刻（marks）も返す"""
    parts = [p for p in re.findall(r"[^。？！…]+[。？！…]*", text) if p.strip()]
    out, marks, pos, t = [], [], 0, 0.0
    for p in parts:
        is_q = "？" in p
        has_num = bool(re.search(r"[0-9０-９]|パーセント|万円|分の", p))
        bright = is_q or "！" in p
        x, sr = vv_ja.tts(p, "amaama" if bright else "normal", 1.0 if has_num else 1.12, 0.02 if bright else 0.0, 1.3 if bright else 1.1)
        x = np.interp(np.arange(int(len(x) * SR / sr)) / SR, np.arange(len(x)) / sr, x).astype(np.float32)
        marks.append([pos, round(t, 3)]); out.append(x); t += len(x) / SR
        gap = 0.35 if is_q else 0.4 if "…" in p else 0.1
        out.append(np.zeros(int(SR * gap), np.float32)); t += gap
        pos += len(p)
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
    lead, t, parts = 0.4, 0.4, []
    # 結論の直前は本当の無音（声のあと pad）。数字の場面は読み終わってから長めに止める
    PAD = {"d1": 0.9, "d1r": 0.8, "m1": 0.6, "m1r": 0.9, "line": 0.9, "zero": 0.8, "compare": 0.8, "money": 0.8, "ten": 0.5, "end": 1.0}
    for s in S:
        x, marks = tts_marks(s["say"])
        # marks は say（読み）の文字位置。表示の sub と文の数は同じなので、文の順で sub の位置に直す
        sp = [p for p in re.findall(r"[^。？！…]+[。？！…]*", s["sub"]) if p.strip()]
        acc, mk = 0, []
        for i, p in enumerate(sp):
            mk.append([acc, round(t + (marks[i][1] if i < len(marks) else marks[-1][1]), 3)]); acc += len(p)
        pad = PAD.get(s["id"], 0.22)
        s["start"], s["voice_len"], s["dur"], s["marks"] = round(t, 3), round(len(x) / SR, 3), round(len(x) / SR + pad, 3), mk
        b = np.zeros(int(s["dur"] * SR), np.float32); b[: len(x)] = x
        parts.append(b); t += s["dur"]
        print(s["id"], s["start"], s["voice_len"], flush=True)
    SC = {s["id"]: s for s in S}

    def at(sid, word):
        s = SC[sid]; i = max(0, s["sub"].find(word)); m = s["marks"][0]
        for mk in s["marks"]:
            if mk[0] <= i: m = mk
        nx = next((mk for mk in s["marks"] if mk[0] > i), [len(s["sub"]), s["start"] + s["voice_len"]])
        return round(m[1] + (nx[1] - m[1]) * (i - m[0]) / max(1, nx[0] - m[0]), 3)

    # ---- 時刻の表（絵と音が同じものを使う） ----
    K = dict(
        h2=at("hook2", "1万人"), r_rule=at("rule", "台"), r_rate=at("rule", "1000円"), r_week=at("rule", "週に"), r_wallet=at("rule", "財布"), r_same=at("rule2", "全員"),
        d1_num=at("d1r", pc(C["1回"]["win"])), d1_mean=at("d1r", "平均"), d1_med=at("d1r", "真ん中"), d1_broke=at("d1r", "4時間"),
        m1_num=at("m1r", "約"), why_lose=at("why1", "1回で"), why_win=at("why1", "上位"), why_sum=at("why1", "それに"),
        l_start=at("line", "では"), l6=at("line", "半年"), l1y=at("line", "1年で"), l2y=at("line", "2年で"), l5y=at("line", "5年で"),
        hour=at("house", "1時間"), h_year=at("house", "1年"), z_q=at("zero", "仮に"), z_num=at("zero", "プラスの人"),
        c_num=at("compare", "1年後"), c_med=at("compare", "真ん中"), c_money=at("compare", "差が"),
        mo_p10=at("money", "下位"), mo_med=at("money", "下位") + 0.6, mo_p90=at("money", "上位"),
        ten_up=at("ten", "ときどき"), hist_tail=at("hist", "プラス側"), hist_you=at("hist", "負けた人"),
        s1=at("sum", "プラスの人"), s2=at("sum", "勝ってる人"), s3=at("sum", "長く"),
    )
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
    # 結論の数字の直前0.6秒は、BGMも止める（本当の無音）
    for k in ("d1_num", "m1_num", "l5y", "c_num"):
        a, b = int((K[k] - 0.6) * SR), int(K[k] * SR); duck[a:b] = 0.0
    mix = vo * 0.95 + mus * duck * 0.6
    n = int(1.5 * SR); mix[-n:] *= np.linspace(1, 0, n)
    # 効果音：数字が出る瞬間に「キラン」、折れ線の点に値の高さの音（％が高いほど高い）
    for k in ("d1_num", "m1_num", "l5y", "c_num", "mo_p10"):
        a = int(K[k] * SR); c = sum(tone(f, 1.0, 0.07, 0.3) for f in (1318.5, 1760, 2637)); mix[a:a + len(c)] += c[: len(mix) - a]
    for k, per in (("l6", "半年"), ("l1y", "1年"), ("l2y", "2年"), ("l5y", "5年")):
        a = int(K[k] * SR); f = 440 * 2 ** ((C[per]["win"] - 0.3) * 20 / 12)
        c = tone(f, 0.5, 0.08, 0.15); mix[a:a + len(c)] += c[: len(mix) - a]
    mix = np.clip(mix / np.abs(mix).max() * 0.92, -1, 1)
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    with wave.open(os.path.join(HERE, "assets", "mix.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    data = dict(total=round(total, 3), fps=FPS, mouth=mouth, lead=lead, K=K, PER=PER, days=A["days"],
                scenes=[{k: s[k] for k in ("id", "sub", "start", "dur", "voice_len", "face", "vis", "marks")} for s in S],
                C={k: {q: C[k][q] for q in ("win", "mean", "median", "p10", "p90")} for k in PER},
                CZ={k: {q: CZ[k][q] for q in ("win", "mean", "median", "p10", "p90")} for k in PER},
                S16=dict(win=[round(x, 4) for x in A["series"]["win"]]), SZ=dict(win=[round(x, 4) for x in Z["series"]["win"]]),
                perhour=y1["yen_per_hour"], hours=y1["hours"], d1_p90=C["1回"]["p90"], traj=A["traj10"], hist=A["year_hist"], edges=A["year_edges"],
                cond=A["cond"], n=A["n"], broke=A["day_broke_mean"], dayhours=A["day_hours_mean"])
    with open(os.path.join(HERE, "assets", "data.js"), "w") as f:
        f.write("window.DATA=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";")
    print(f"total {total:.1f}s", K)


if __name__ == "__main__":
    main()
