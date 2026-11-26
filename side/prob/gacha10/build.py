"""10分動画「確率1%のガチャ、100回引けば当たる？1万人でためしてみた」の台本・声・音・データを作る。
数字は results.json（sim.py）からだけ入れる。時刻の表 K はここで1回だけ作り、絵（data.js）と音（mix.wav）が同じ表を使う。
実行：python3 build.py [--kana]（--kana は読みの確認だけ） → assets/{mix.wav,data.js}
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
E1, E2, E3, E4, E5 = R["e1"], R["e2"], R["e3"], R["e4"], R["e5"]
pc = lambda x: f"{round(x * 100):.0f}%"

# ---- 話の流れが結果と合っているか（合わなければ止まる） ----
Z, W = pc(E1["zero_rate"]), pc(E1["win_rate"])
assert pc(E1["zero_theory"]) == Z and pc(E1["win_theory"]) == W, "①が計算の答えと同じ%にならない"
assert E1["zero_rate"] > 1 / 3, "「3人に1人より多い」と言えない"
assert E1["p1_bits"][:3] == "000", "1人目の最初の3回が外れではない"
assert E2["half"]["sim"] < 90 and abs(E2["half"]["sim"] - E2["half"]["theory"]) <= 3
assert abs(E2["p90"]["sim"] - 230) <= 12 and abs(E2["p99"]["sim"] - 459) <= 30
assert E2["max"] > 600 and round(E2["mean"]) == 100, "②平均が100回と言えない"
assert pc(E3["win_rate"]) == W, "③が①と同じ%にならない"
assert round(E4["mean"]) < 95 and E4["worst_nocap"] > E4["cap"]
assert E5["mean"] == E5["mean_theory"] and E5["mean"] > 12
assert E5["stage"] == E5["stage_theory"]
OVER = pc(E2["over_mean"])
assert abs(E2["over_mean"] - E1["zero_rate"]) < 0.02
TEN2, TEN5 = E2["ten"], E5["ten"]
man, sen = divmod(round(E3["tried"] / 1000), 10)
TRIED = f"約{man}万{sen}千人" if sen else f"約{man}万人"
ONE_IN = round(1 / E4["reach_rate"])
MAXX = round(E2["max"] / 100)
HALF, P90, P99 = E2["half"]["sim"], E2["p90"]["sim"], E2["p99"]["sim"]
SAFE = P99 // 50 * 50          # 「450回をこえてから」
M4 = round(E4["mean"])

if E1["p1_hits"] == 0:
    o5 = dict(id="o5", face="troubled", sub="0回。1人目は、1回も当たりませんでした。")
else:
    o5 = dict(id="o5", face="happy", sub=f"{E1['p1_hits']}回。{E1['p1_first']}回目に当たりました。")
p2r = f"{E2['first']}回目で当たり！" + ("運がいい人です。" if E2["first"] <= 30 else "けっこうかかりました。" if E2["first"] > 100 else "")
k3 = f"{E5['first']}回でそろいました。" + ("この人は、かなり運がいいです。" if E5["first"] <= 8 else "")

S = [
    # ---- 導入 ----
    dict(id="hook", face="surprised", vis="hook", sub="確率1%のガチャ。100回引けば、当たる？"),
    dict(id="hook2", face="pose_pointing", vis="hook", sub="1万人で、ためしてみました。", pad=0.9),
    dict(id="in1", face="base", vis="in1", sub="1%というのは、100個に1個が当たり、ということ。", pad=0.8),
    dict(id="in2", face="pose_thinking", vis="in2", sub="それを100回引く。だったら、100%当たる。そう思いますよね？", pad=0.8),
    dict(id="in3", face="pose_thinking", vis="in3", sub="ほぼ100%。90%くらい。60%くらい。あなたの予想は、どれですか？", pad=1.6),
    dict(id="in4", face="pose_pointing", vis="in4", sub="今日は、5つの実験で確かめます。", pad=1.6),
    # ---- 実験① ----
    dict(id="c1t", face="pose_excited", vis="c1t", sub="実験1。100回引いたら、当たる？", pad=1.2),
    dict(id="r1", face="base", vis="e1rule", sub="ルールです。金色の玉が、当たり。確率は1%。灰色の玉は、外れです。", pad=0.8),
    dict(id="o1", face="pose_pointing", vis="e1one", sub="まず、1人目。1回ずつ引いてみます。", pad=0.5),
    dict(id="o2", face="base", vis="e1one", sub="外れ。外れ。また外れ。", pad=0.5),
    dict(id="o3", face="pose_thinking", vis="e1one", sub="ここからは、早送りです。", pad=3.4),
    dict(id="o4", face="pose_thinking", vis="e1one", sub="100回引いて、当たりは…", pad=0.3),
    dict(vis="e1one", pad=2.2, **o5),
    dict(id="t10", face="pose_pointing", vis="e1ten", sub="次は、10人。それぞれ100回ずつ引きます。", pad=3.6),
    dict(id="t10r", face="base", vis="e1ten", sub=f"1回でも当たった人は、10人のうち{E1['win10']}人。", pad=1.6),
    dict(id="t100", face="pose_thinking", vis="e1grid", sub="100人では？", pad=2.6),
    dict(id="t100r", face="base", vis="e1grid", sub=f"当たった人は、{E1['win100']}人でした。", pad=1.2),
    dict(id="t1m", face="pose_excited", vis="e1grid", sub="いよいよ、1万人です！点1つが、1人。金色は当たった人、灰色は1回も当たらなかった人です。", pad=2.0),
    dict(id="ansq", face="pose_thinking", vis="e1grid", sub="100回引いて、1回も当たらなかった人は…", pad=0.9),
    dict(id="ans1", face="surprised", vis="e1grid", sub=f"約{Z}。", pad=2.8),
    dict(id="ans2", face="base", vis="e1grid", sub=f"3人に1人より多いんです。当たった人は、約{W}でした。", pad=2.4),
    dict(id="ans3", face="troubled", vis="e1grid", sub="100%には、ほど遠いですね。", pad=1.0),
    dict(id="why0", face="pose_thinking", vis="e1why", sub="なぜでしょう？図で見てみます。", pad=0.5),
    dict(id="why1", face="pose_pointing", vis="e1why", sub="1回引いて、外れる確率は99%。", pad=1.0),
    dict(id="why2", face="base", vis="e1why", sub="2回つづけて外れるのは、その99%の、また99%。", pad=1.0),
    dict(id="why3", face="pose_pointing", vis="e1why", sub="引くたびに、99%を掛けていきます。灰色の棒が、少しずつ縮みます。", pad=2.6),
    dict(id="why4", face="surprised", vis="e1why", sub=f"100回掛けると、残りは約{Z}。これが、1回も当たらない人です。", pad=2.4),
    dict(id="why5", face="base", vis="e1why2", sub="1%を100回足す、のではありません。外れの99%を、100回掛ける。ここが大事です。", pad=2.0),
    # ---- 実験② ----
    dict(id="c2t", face="pose_excited", vis="c2t", sub="実験2。じゃあ、何回引けば安心？", pad=1.2),
    dict(id="p1", face="base", vis="e2one", sub="今度は、当たるまで引きつづけます。まずは1人目。", pad=3.0),
    dict(id="p2", face="happy", vis="e2one", sub=p2r, pad=1.4),
    dict(id="p10", face="pose_pointing", vis="e2ten", sub="次は10人。棒の長さが、引いた回数です。", pad=4.2),
    dict(id="p10r", face="base", vis="e2ten", sub=f"早い人は{min(TEN2)}回。遅い人は{max(TEN2)}回。ばらばらですね。", pad=1.4),
    dict(id="p1m", face="pose_excited", vis="e2grid", sub="では、1万人。全員いっしょに、1回ずつ引いていきます。当たった人から、金色に変わります。", pad=1.0),
    dict(id="halfq", face="pose_thinking", vis="e2grid", sub="半分の人が当たったのは…", pad=0.9),
    dict(id="half", face="surprised", vis="e2grid", sub=f"{HALF}回目。", pad=2.8),
    dict(id="half2", face="base", vis="e2grid", sub="100回より、ずっと早いですね。でも、ここからが長いんです。", pad=0.8),
    dict(id="p90", face="pose_pointing", vis="e2grid", sub=f"10人のうち9人が当たるまで、{P90}回。", pad=2.6),
    dict(id="p99", face="base", vis="e2grid", sub=f"100人のうち99人が当たるまでは、{P99}回。", pad=2.6),
    dict(id="maxq", face="pose_thinking", vis="e2grid", sub="そして、いちばん運の悪かった人は…", pad=0.9),
    dict(id="max", face="surprised", vis="e2grid", sub=f"{E2['max']}回！", pad=2.8),
    dict(id="max2", face="troubled", vis="e2grid", sub=f"1%なのに、100回の約{MAXX}倍です。", pad=1.4),
    dict(id="dist0", face="pose_pointing", vis="e2hist", sub="この1万人を、当たった回数の順に並べ直します。", pad=2.2),
    dict(id="dist1", face="base", vis="e2hist", sub="早く当たる人が、いちばん多い。そして右へ、長く長くつづきます。", pad=1.4),
    dict(id="avg1", face="pose_thinking", vis="e2hist", sub="よく聞く「平均100回」。これは、全員の回数をならした数です。", pad=1.4),
    dict(id="avg2", face="pose_pointing", vis="e2hist", sub=f"でも、半分の人は{HALF}回までに当たっています。", pad=1.6),
    dict(id="avg3", face="base", vis="e2hist", sub="右のほうの運の悪い人たちが、平均を引き上げているんです。", pad=1.8),
    dict(id="avg4", face="troubled", vis="e2hist", sub=f"平均の100回を引いても、当たらない人が約{OVER}。「平均まで引けば安心」ではありません。", pad=2.0),
    dict(id="sum1", face="pose_pointing", vis="sum1", sub=f"ここまでのまとめです。100回引いて当たるのは、約{W}。100人のうち99人が当たるのは、約{SAFE}回をこえてから。", pad=2.0),
    # ---- 実験③ ----
    dict(id="c3t", face="pose_excited", vis="c3t", sub="実験3。200回外れた。そろそろ出る？", pad=1.2),
    dict(id="s1", face="pose_thinking", vis="e3a", sub="200回も外れたら、そろそろ当たりそう。そう感じますよね。", pad=1.2),
    dict(id="s2", face="pose_pointing", vis="e3b", sub=f"そこで、200回つづけて外れた人だけを、1万人集めました。集めるのに、{TRIED}が引きました。", pad=1.4),
    dict(id="s4", face="pose_thinking", vis="e3grid", sub=f"もし「そろそろ出る」なら、当たる人は実験1の{W}より増えるはずです。", pad=1.2),
    dict(id="s3", face="base", vis="e3grid", sub="この1万人が、さらに100回引きます。", pad=4.2),
    dict(id="sq", face="pose_thinking", vis="e3grid", sub="当たった人は…", pad=0.9),
    dict(id="sa", face="surprised", vis="e3grid", sub=f"約{pc(E3['win_rate'])}。", pad=2.8),
    dict(id="sa2", face="base", vis="e3grid", sub="実験1と、同じです。200回外れても、当たりやすくはなりません。", pad=2.2),
    dict(id="swhy1", face="pose_pointing", vis="e3why", sub="理由はかんたん。ガチャは、前の結果を覚えていません。", pad=1.2),
    dict(id="swhy2", face="base", vis="e3why", sub="201回目も、1回目と同じ1%です。", pad=2.0),
    dict(id="s6", face="pose_excited", vis="e3why", sub="「そろそろ出る」は、気のせいなんです！", pad=2.2),
    # ---- 実験④ ----
    dict(id="c4t", face="pose_excited", vis="c4t", sub="実験4。天井があると、どうなる？", pad=1.2),
    dict(id="t1", face="base", vis="e4a", sub="天井とは、決まった回数を引けば、必ずもらえる仕組みです。", pad=0.8),
    dict(id="t1b", face="pose_pointing", vis="e4a", sub="今回は200回。200回引いても出なければ、もらえます。", pad=1.8),
    dict(id="t2", face="base", vis="e4hist", sub="実験2の1万人に、この天井をつけてみます。", pad=1.0),
    dict(id="t3", face="pose_pointing", vis="e4hist", sub="200回より右にいた人たちが…全員、200回で止まります。", pad=2.4),
    dict(id="t4", face="surprised", vis="e4hist", sub=f"いちばん運の悪い人は、{E4['worst_nocap']}回から200回に。", pad=2.4),
    dict(id="t5", face="base", vis="e4hist", sub=f"平均の回数は、100回から約{M4}回に。", pad=2.4),
    dict(id="t6", face="pose_pointing", vis="e4hist", sub=f"天井まで行った人は、約{pc(E4['reach_rate'])}。{ONE_IN}人に1人くらいです。", pad=2.4),
    dict(id="t7", face="base", vis="e4note", sub="天井は、運の悪い人を助ける仕組み。でも、それまでの1回1回は、ずっと1%のままです。", pad=1.8),
    dict(id="sum2", face="pose_pointing", vis="sum2", sub="ここまでのまとめです。「そろそろ出る」はない。天井があれば、いちばん悪い場合の回数が決まる。", pad=2.0),
    # ---- 実験⑤ ----
    dict(id="c5t", face="pose_excited", vis="c5t", sub="実験5。全6種類、そろえるには何回？", pad=1.2),
    dict(id="k1", face="base", vis="e5a", sub="今度のガチャは、全部で6種類。毎回、どれか1つが同じ確率で出ます。", pad=0.8),
    dict(id="k2", face="pose_thinking", vis="e5a", sub="6回引けば、全部そろう？まず1人、やってみます。", pad=5.6),
    dict(id="k3", face="happy", vis="e5a", sub=k3, pad=1.6),
    dict(id="k10", face="pose_pointing", vis="e5ten", sub="次は10人。", pad=3.8),
    dict(id="k10r", face="base", vis="e5ten", sub=f"早い人は{min(TEN5)}回。遅い人は{max(TEN5)}回かかりました。", pad=1.4),
    dict(id="k1m", face="pose_excited", vis="e5hist", sub="では、1万人です！そろった回数のところに、1人ずつ積んでいきます。", pad=3.4),
    dict(id="kq", face="pose_thinking", vis="e5hist", sub="全部そろうまでの平均は…", pad=0.9),
    dict(id="ka", face="surprised", vis="e5hist", sub=f"{E5['mean']}回。", pad=2.8),
    dict(id="ka2", face="base", vis="e5hist", sub=f"6回の2倍以上です。6回ぴったりでそろった人は、{E5['min_count']}人だけ。", pad=2.0),
    dict(id="kmax", face="troubled", vis="e5hist", sub=f"いちばんかかった人は、{E5['max']}回でした。", pad=2.2),
    dict(id="kwhy0", face="pose_thinking", vis="e5why", sub="なぜ、こんなにかかるのでしょう？", pad=0.5),
    dict(id="kwhy1", face="pose_pointing", vis="e5why", sub="1種類目は、何が出ても新しい種類。1回で進みます。", pad=1.0),
    dict(id="kwhy2", face="base", vis="e5why", sub="でも、持っている種類が増えるほど、ダブりやすくなります。", pad=1.6),
    dict(id="kwhy3", face="pose_pointing", vis="e5why", sub="最後の1種類は、6回に1回しか出ません。平均で6回かかります。", pad=1.6),
    dict(id="kwhy4", face="surprised", vis="e5why", sub=f"全部足すと、{E5['mean_theory']}回。最後の1種類が、いちばん遠いんです。", pad=2.4),
    # ---- まとめ ----
    dict(id="e0", face="pose_pointing", vis="end", sub="今日のまとめです。", pad=0.4),
    dict(id="e1", face="base", vis="end", sub=f"1つ。1%を100回引いても、当たるのは約{W}。", pad=1.0),
    dict(id="e2", face="base", vis="end", sub="2つ。「そろそろ出る」は、ありません。", pad=1.0),
    dict(id="e3", face="pose_pointing", vis="end", sub="3つ。回数とお金は、引く前に決めておく。", pad=1.4),
    dict(id="e4", face="pose_thinking", vis="end2", sub="最初の問い。1%を100回引けば、当たる？", pad=0.6),
    dict(id="e5", face="happy", vis="end2", sub="答えは、3人に1人は当たらない、でした。", pad=2.4),
    dict(id="e6", face="happy", vis="end2", sub="次に確かめてほしい確率、コメントで教えてね！", pad=2.2),
]
SPLIT = r"[^。？！…]+[。？！…]*"
# 章（BGM・背景・左の目次に使う）
CH = [("intro", "hook"), ("c1", "c1t"), ("c2", "c2t"), ("c3", "c3t"), ("c4", "c4t"), ("c5", "c5t"), ("end", "e0")]
BGM = {"intro": "nandeshou", "c1": "nandeshou", "c2": "morning", "c3": "morning", "c4": "summer_triangle", "c5": "summer_triangle", "end": "nandeshou"}


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
        gap = 0.4 if is_q else 0.5 if "…" in p else 0.2
        out.append(np.zeros(int(SR * gap), np.float32)); t += gap
    return np.concatenate(out), marks


def load_mp3(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def tone(f, d, a, decay):
    t = np.arange(int(d * SR)) / SR
    return (a * np.sin(2 * np.pi * f * t) * np.exp(-t / decay)).astype(np.float32)


def noise(d, a, decay, seed=1):
    t = np.arange(int(d * SR)) / SR
    n = np.random.default_rng(seed).standard_normal(len(t)).astype(np.float32)
    n = np.convolve(n, np.ones(6) / 6, "same")
    return (a * n * np.exp(-t / decay)).astype(np.float32)


def sweep(d, f0=300, f1=800, a=0.03):
    tt = np.arange(int(d * SR)) / SR
    return (a * np.sin(2 * np.pi * (f0 * tt + (f1 - f0) * tt * tt / (2 * d))) * np.minimum(1, (d - tt) / 0.3) * np.minimum(1, tt / 0.1)).astype(np.float32)


def main():
    for s in S:
        s["say"] = to_say(s["sub"]).replace("「", "").replace("」", "")
        kana, bad = check(s["say"])
        if bad:
            raise SystemExit(f"読みの問題 {s['id']}: {bad} {kana}")
        for p in re.findall(SPLIT, s["sub"]):
            assert len(p) <= 44, (s["id"], p, len(p))
    if "--kana" in sys.argv:
        for s in S:
            print(s["id"], "|", s["sub"], "\n    ", vv_ja._get().create_audio_query(s["say"], 2).kana)
        return
    lead, t, parts = 0.3, 0.3, []
    for s in S:
        x, marks = tts_marks(s["say"])
        sp = [p for p in re.findall(SPLIT, s["sub"]) if p.strip()]
        assert len(sp) == len(marks), s["id"]
        acc, mk = 0, []
        for i, p in enumerate(sp):
            mk.append([acc, round(t + marks[i], 3)]); acc += len(p)
        pad = s.get("pad", 0.4)
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

    st = lambda sid: SC[sid]["start"]
    end = lambda sid: round(SC[sid]["start"] + SC[sid]["voice_len"], 3)
    fin = lambda sid: round(SC[sid]["start"] + SC[sid]["dur"], 3)
    o2m = [m[1] for m in SC["o2"]["marks"]]
    in3m = [m[1] for m in SC["in3"]["marks"]]
    # ---- 時刻の表（絵と音が同じものを使う） ----
    K = dict(
        h_q=at("hook", "100回引けば"), h_1man=at("hook2", "1万人"),
        in1_gold=at("in1", "100個に1個"), in2_100=at("in2", "100回引く"), in2_eq=at("in2", "100%当たる"),
        g1=in3m[0], g2=in3m[1], g3=in3m[2], g_q=in3m[3], in4=at("in4", "5つの"),
        r_gold=at("r1", "金色"), r_p=at("r1", "確率は"), r_gray=at("r1", "灰色"),
        o_d1=o2m[0] + 0.1, o_d2=o2m[1] + 0.1, o_d3=o2m[2] + 0.25, o_ff=end("o3") - 0.2, o_ffend=fin("o3") - 0.4,
        o_sil=end("o4"), o_ans=st("o5") + 0.05,
        t10_go=end("t10") + 0.1, t10_end=fin("t10") - 0.5, t10r=at("t10r", "10人のうち"),
        x100=end("t100") + 0.1, x100r=at("t100r", str(E1["win100"])),
        x1m=at("t1m", "1万人"), x1m_fill=at("t1m", "点1つ"), x1m_done=fin("t1m") - 0.4,
        a_sil=end("ansq"), a1=st("ans1") + 0.05, a_sort=st("ans1") + 1.2, a2=at("ans2", "当たった人は"), a2n=at("ans2", "約"),
        w1=at("why1", "外れる確率"), w2=at("why2", "また99%"), w3=at("why3", "灰色の棒"), w3end=fin("why3") - 0.3,
        w4=at("why4", "残りは"), w4b=at("why4", "これが"), w5a=st("why5") + 0.1, w5b=at("why5", "外れの99%"), w5c=at("why5", "ここが"),
        p1_go=at("p1", "まずは1人目") + 0.5, p2=st("p2") + 0.05,
        p10_go=end("p10") + 0.1, p10_end=fin("p10") - 0.4, p10a=at("p10r", "早い人"), p10b=at("p10r", "遅い人"),
        g2_go=at("p1m", "全員いっしょに"), h_sil=end("halfq"), half=st("half") + 0.05,
        p90_go=st("p90"), p90=end("p90") + 0.3, p99_go=st("p99"), p99=end("p99") + 0.3,
        m_go=st("maxq"), m_sil=end("maxq"), mx=st("max") + 0.05,
        d_fly=at("dist0", "並べ直します") - 0.3, d_tail=at("dist1", "そして右へ"),
        v1=at("avg1", "平均100回"), v2=at("avg2", "半分の人は"), v3=at("avg3", "右のほう"), v3b=at("avg3", "平均を"), v4=at("avg4", "当たらない人"), v4b=at("avg4", "「平均まで"),
        sm1a=at("sum1", "100回引いて"), sm1b=at("sum1", "100人のうち"),
        s1a=st("s1") + 0.1, s1b=at("s1", "そろそろ"),
        s2a=at("s2", "200回つづけて"), s2b=at("s2", "1万人集め"), s2c=at("s2", "集めるのに"),
        s4=at("s4", "実験1の"), s3_go=end("s3") + 0.1, s3_end=fin("s3") - 0.5,
        s_sil=end("sq"), sa=st("sa") + 0.05, sa2=at("sa2", "同じです") - 0.2, sa3=at("sa2", "200回外れても"),
        sw1=at("swhy1", "ガチャは"), sw2=at("swhy2", "201回目"), sw3=at("swhy2", "1回目と同じ"), s6=at("s6", "気のせい"),
        t1=at("t1", "決まった回数"), t1b=at("t1b", "200回引いても"), t1c=at("t1b", "もらえます"),
        t2=at("t2", "この天井"), t3a=st("t3") + 0.1, t3=at("t3", "全員"), t4=at("t4", "から200回") - 0.1, t4a=st("t4") + 0.1,
        t5a=st("t5") + 0.1, t5=at("t5", "約"), t6a=st("t6") + 0.1, t6=at("t6", "約"), t6b=at("t6", f"{ONE_IN}人に"),
        t7a=st("t7") + 0.1, t7b=at("t7", "でも"),
        sm2a=at("sum2", "「そろそろ"), sm2b=at("sum2", "天井があれば"),
        k1a=at("k1", "全部で6種類"), k1b=at("k1", "毎回"), k2q=at("k2", "6回引けば"), k2_go=end("k2") + 0.2, k2_end=fin("k2") - 0.5, k3=st("k3") + 0.05,
        k10_go=end("k10") + 0.1, k10_end=fin("k10") - 0.4, k10a=at("k10r", "早い人"), k10b=at("k10r", "遅い人"),
        k1m_go=at("k1m", "そろった回数"), k1m_end=fin("k1m") - 0.4, k_sil=end("kq"), ka=st("ka") + 0.05,
        ka2=at("ka2", "6回ぴったり"), kmax=at("kmax", str(E5["max"])),
        kw1=at("kwhy1", "1種類目"), kw2=at("kwhy2", "持っている"), kw2end=fin("kwhy2") - 0.3, kw3=at("kwhy3", "最後の"), kw3b=at("kwhy3", "平均で"),
        kw4=at("kwhy4", "全部足すと"), kw4b=at("kwhy4", "最後の1種類"),
        e1=st("e1") + 0.05, e2=st("e2") + 0.05, e3=st("e3") + 0.05, e4=st("e4") + 0.05, e5=at("e5", "3人に1人"), e6=st("e6") + 0.05,
    )
    K = {k: round(float(v), 3) for k, v in K.items()}
    chapters = [dict(id=c, start=SC[sid]["start"]) for c, sid in CH]
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
    # ---- BGM：章で曲を切り替える（1秒で入れ替え） ----
    mus = np.zeros(len(vo), np.float32)
    cache = {}
    for i, c in enumerate(chapters):
        name = BGM[c["id"]]; path = os.path.join(P3, "assets", "bgm", name + ".mp3")
        if not os.path.exists(path): continue
        if name not in cache:
            m = load_mp3(path); cache[name] = m / (np.sqrt((m ** 2).mean()) + 1e-9) * 0.11
        a = int(max(0, c["start"] - 0.5) * SR); b = int((chapters[i + 1]["start"] + 0.5) * SR) if i + 1 < len(chapters) else len(vo)
        if i and BGM[chapters[i - 1]["id"]] == name:      # 同じ曲がつづく章は切らない
            continue
        j = i
        while j + 1 < len(chapters) and BGM[chapters[j + 1]["id"]] == name: j += 1
        b = int((chapters[j + 1]["start"] + 0.5) * SR) if j + 1 < len(chapters) else len(vo)
        seg = np.tile(cache[name], (b - a) // len(cache[name]) + 1)[: b - a].copy()
        f = min(SR, len(seg) // 2); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        mus[a:b] += seg
    duck = np.repeat(np.array([0.45 if m else 1.0 for m in mouth], np.float32), hop)
    duck = np.convolve(np.pad(duck, (0, len(vo) - len(duck)), constant_values=1.0), np.ones(4800) / 4800, "same")
    # 答えの直前は本当の無音（BGMも止める）
    SIL = [("o_sil", "o_ans"), ("a_sil", "a1"), ("h_sil", "half"), ("m_sil", "mx"), ("s_sil", "sa"), ("k_sil", "ka")]
    for a, b in SIL:
        duck[int(K[a] * SR):int((K[b] - 0.05) * SR)] = 0.0
    mix = vo * 0.95 + mus * duck * 0.6
    n = int(1.5 * SR); mix[-n:] *= np.linspace(1, 0, n)

    def put(tm, c):
        a = int(tm * SR)
        if 0 <= a < len(mix): mix[a:a + len(c)] += c[: len(mix) - a]
    kiran = sum(tone(f, 1.0, 0.07, 0.3) for f in (1318.5, 1760, 2637))
    don = tone(196, 0.5, 0.12, 0.15) + noise(0.25, 0.08, 0.05, 5)
    pon = tone(880, 0.25, 0.05, 0.08)
    low = tone(330, 0.25, 0.06, 0.08)
    hi = tone(1046.5, 0.3, 0.07, 0.1)
    HITS = ["a1", "half", "mx", "sa", "ka", "e5"]
    for k in HITS: put(K[k], kiran)
    put(K["o_ans"], low + tone(247, 0.4, 0.06, 0.15))
    for c, sid in CH[1:6]: put(SC[sid]["start"] - 0.25, noise(0.5, 0.06, 0.2, 9)); put(SC[sid]["start"] + 0.05, don)
    for k in ("h_1man", "in2_eq", "g1", "g2", "g3", "r_gold", "r_gray", "in1_gold", "t10r", "x100r", "a2n", "w1", "w2", "w4", "w5a", "w5b", "p10a", "p10b",
              "p90", "p99", "v1", "v2", "v4", "sm1a", "sm1b", "s2b", "s4", "sa2", "sw2", "sw3", "t1c", "t4", "t5", "t6", "sm2a", "sm2b", "k1a",
              "ka2", "kmax", "kw1", "kw3", "kw4", "e1", "e2", "e3", "e6", "p2", "k3", "s6"):
        put(K[k], pon)
    for k in ("o_d1", "o_d2", "o_d3"): put(K[k], low)
    for k, e in (("o_ff", "o_ffend"), ("t10_go", "t10_end"), ("x1m_fill", "x1m_done"), ("p10_go", "p10_end"), ("g2_go", "h_sil"), ("p90_go", "p90"), ("p99_go", "p99"),
                 ("m_go", "m_sil"), ("s3_go", "s3_end"), ("k10_go", "k10_end"), ("k1m_go", "k1m_end"), ("w3", "w3end"), ("kw2", "kw2end")):
        put(K[k], sweep(max(0.4, K[e] - K[k])))
    put(K["x100"], sweep(1.6)); put(K["d_fly"], sweep(1.2, 500, 900)); put(K["t3"], sweep(1.2, 900, 400, 0.04)); put(K["t3"] + 1.2, don)
    # 実験②の1人目：1回ずつの音（最後が当たり）
    n1 = E2["first"]; step = min(0.45, 2.4 / n1)
    for i in range(n1): put(K["p1_go"] + i * step, hi if i == n1 - 1 else low * (1.0 if n1 <= 12 else 0.4))
    # 実験⑤の1人目：1回ずつの音（新しい種類＝高い音、ダブり＝低い音）
    seq = E5["seq0"]; step5 = min(0.7, (K["k2_end"] - K["k2_go"]) / len(seq)); seen = set()
    for i, c in enumerate(seq):
        put(K["k2_go"] + i * step5, low if c in seen else tone(660 + 80 * len(seen), 0.3, 0.07, 0.1)); seen.add(c)
    mix = np.clip(mix / np.abs(mix).max() * 0.92, -1, 1)
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    with wave.open(os.path.join(HERE, "assets", "mix.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    slim = lambda d, drop: {k: v for k, v in d.items() if k not in drop}
    data = dict(total=round(total, 3), fps=FPS, mouth="".join(map(str, mouth)), lead=lead, K=K, chapters=chapters, hits=[K[k] for k in HITS],
                sil=[[K[a], K[b]] for a, b in SIL], step1=step, step5=step5,
                scenes=[{k: s[k] for k in ("id", "sub", "start", "dur", "voice_len", "face", "vis", "marks")} for s in S],
                e1=slim(E1, ()), e2=E2, e3=E3, e4=E4, e5=E5, n=R["n"], seed=R["seed"],
                txt=dict(Z=Z, W=W, OVER=OVER, TRIED=TRIED, ONE_IN=ONE_IN, SAFE=SAFE, M4=M4, W3=pc(E3["win_rate"]), REACH=pc(E4["reach_rate"]), MAXX=MAXX))
    with open(os.path.join(HERE, "assets", "data.js"), "w") as f:
        f.write("window.DATA=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";")
    print(f"total {total:.2f}s")
    for c in chapters: print(c)
    print(K)


if __name__ == "__main__":
    main()
