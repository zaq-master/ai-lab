"""3D版：e東京喰種を1万人で打ってみた — 計算・セリフ・声・BGM・効果音を作り、assets/ に書き出す。

実行：python3 side/pachi3d/build.py
出力：assets/mix.wav（声＋BGM＋効果音）、assets/data.js（場面の時刻・数字・口パク・1万人のデータ）
その後：cd side/pachi3d && npx hyperframes render
スペックと仮定は side/simvideo/pachi_tg.py と同じ（出典もそちら）。
"""
import json
import math
import os
import wave

import numpy as np
import pyopenjtalk

from yomi import check, to_say, yen_abs, yen_say

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
VOICES = os.path.join(HERE, "..", "simvideo", "voices")
SR, FPS = 48000, 30

# ---------------- シミュレーション ----------------
P_ZORO = P_CHARGE = 1 / 399.9
ZORO = [(0.50, 1500, True), (0.01, 300, True), (0.49, 1500, False)]
ST, P_RUSH = 130, 1 / 95.3
N, SEED, YEN_BALL, RATE, SPINS = 10_000, 20261118, 4, 16, 2000
C = 1 - (1 - P_RUSH) ** ST
rng = np.random.default_rng(SEED)

cat = rng.choice(3, N, p=[z[0] for z in ZORO])
enter = cat < 2
K1 = np.zeros(N, int)
K1[enter] = rng.geometric(1 - C, enter.sum()) - 1
big1 = rng.binomial(K1, 0.03)
pay1 = np.where(cat == 1, 300, 1500) + 3000 * K1 + 3000 * big1
enter_rate = float(enter.mean())
avg_rush = float(pay1[enter].mean())
chain_max = int(K1.max())
chain_cnt = [int(((K1 == k) & enter).sum()) for k in range(8)] + [int(((K1 >= 8) & enter).sum())]
over10k = int((pay1 >= 10000).sum())

p_enter = P_ZORO * (ZORO[0][0] + ZORO[1][0])
to_rush = rng.geometric(p_enter, N)
q50, q90, deep = float(np.percentile(to_rush, 50)), float(np.percentile(to_rush, 90)), int(to_rush.max())
cost_edges = list(range(0, 3001, 250))
cost_cnt = np.histogram(np.minimum(to_rush, 2999), cost_edges)[0].tolist()


def play(days=1, rate=RATE):
    spins = SPINS * days
    nz = rng.binomial(spins, P_ZORO, N)
    nc = rng.binomial(spins, P_CHARGE, N)
    m = np.array([rng.multinomial(k, [z[0] for z in ZORO]) for k in nz])
    R = m[:, 0] + m[:, 1]
    K = np.zeros(N, int)
    pos = R > 0
    K[pos] = rng.negative_binomial(R[pos], 1 - C)
    rb = 3000 * K + 3000 * rng.binomial(K, 0.03)
    balls = 1500 * (m[:, 0] + m[:, 2]) + 300 * m[:, 1] + 300 * nc + rb
    return balls * YEN_BALL - spins / rate * 1000, R


day, R_day = play()
win_day, avg_day, med_day = float((day > 0).mean()), float(day.mean()), float(np.median(day))
best_day, worst_day, norush_day = float(day.max()), float(day.min()), float((R_day == 0).mean())
rates = {r: play(rate=r)[0] for r in (14, 16, 18)}
month, _ = play(days=20)
win_month, avg_month = float((month > 0).mean()), float(month.mean())
border = 1000 / (((sum(z[0] * z[1] for z in ZORO) + 0.51 * 3000 * 1.03 * C / (1 - C)) * P_ZORO + 300 * P_CHARGE) * YEN_BALL)
day_edges = list(range(-100000, 150001, 10000))
day_cnt = np.histogram(np.clip(day, -99999, 149999), day_edges)[0].tolist()


def man(y):
    return f"{'+' if y >= 0 else '−'}{abs(y) / 10000:.1f}万円"


# ---------------- セリフ（字幕＝sub、声＝say） ----------------
R784 = round(399.9 / 0.51)
S = [
    dict(id="hook", face="wide",
         sub=f"RUSHに入るまで、平均いくらかかるか知っていますか？1日打って、勝てる人は何%？今日は全部、1万人で確かめます。"),
    dict(id="open", face="happy", voice="happy",
         sub="こんにちは、電脳アリスです。今日は、話題のラッキートリガー機「e東京喰種」を、コンピューターの中の1万人に打ってもらいます。"),
    dict(id="spec", sub="まずはスペック。当たりは合算で1/199.9。RUSHは130回転のあいだに1/95.3を引けば続く仕組みで、継続率は約75%です。"),
    dict(id="lt", sub="ラッキートリガー、略してLTは、RUSHのさらに上に、出玉の多いモードを用意した仕組み。この台は、RUSHに入れば、そのままLTの状態です。RUSH中の大当たりは、すべて約3000個以上。"),
    dict(id="trick", face="wide",
         sub=f"ここが大事なポイント。当たりの半分は、約300個の「喰種チャージ」です。RUSHに入るのは図柄揃いの51%だけなので、通常時からRUSHに入る確率は、約1/{R784}になります。"),
    dict(id="exp1", sub=f"では実験。図柄揃いを1万回引いて、RUSHに入るかを見てみます。光った人がRUSH突入。結果は{enter_rate * 100:.1f}%。ほぼスペックどおりですね。"),
    dict(id="chain", sub=f"RUSHに入ったあと、何回当たったか。いちばん多いのは、1回も当たらずに終わるパターン。でも長く続く人もいて、最高は{chain_max}連続でした。"),
    dict(id="avg", face="happy",
         sub=f"RUSHに入ったときの平均出玉は、約{avg_rush:,.0f}個。1万個を超えたのは、1万回のうち{over10k:,}回でした。",
         say=f"ラッシュに入ったときの平均デダマは、約{round(avg_rush, -1):.0f}個。いちまんこを超えたのは、いちまんかいのうち{over10k}回でした。"),
    dict(id="cost", sub=f"では、RUSHに入るまで何回転かかるのか。半分の人は{q50:.0f}回転までに入りますが、遅いほうの1割は{q90:.0f}回転以上かかりました。"),
    dict(id="cost2", face="wide",
         sub=f"お金にすると、1000円で{RATE}回転なら、平均で約{to_rush.mean() / RATE * 1000 / 10000:.1f}万円。いちばんハマった人は{deep:,}回転、約{deep / RATE * 1000 / 10000:.0f}万円でした。途中の出玉を使わずに打った場合の目安です。",
         say=f"お金にすると、千円で{RATE}回転なら、平均で約{yen_abs(to_rush.mean() / RATE * 1000)}。いちばんハマった人は{deep}回転、約{yen_abs(deep / RATE * 1000)}でした。途中の出玉を使わずに打った場合の目安です。"),
    dict(id="day", sub=f"次は、1万人に1日ずつ打ってもらいます。条件は等価交換、1000円で{RATE}回転、通常時2000回転。勝った人は{win_day * 100:.1f}%、平均は{man(avg_day)}でした。",
         say=f"次は、いちまんにんに、いちにちずつ打ってもらいます。条件は、とうかこうかん、千円で{RATE}回転、通常時二千回転。勝った人は{win_day * 100:.1f}パーセント、平均は{yen_say(avg_day)}でした。"),
    dict(id="dayext", face="wide",
         sub=f"いちばん勝った人は{man(best_day)}、いちばん負けた人は{man(worst_day)}。真ん中の人は{man(med_day)}。そして1日打ってRUSHに1回も入れなかった人が、{norush_day * 100:.0f}%いました。",
         say=f"いちばん勝った人は{yen_say(best_day)}、いちばん負けた人は{yen_say(worst_day)}。真ん中の人は{yen_say(med_day)}。そして、いちにち打ってラッシュに一回も入れなかった人が、{norush_day * 100:.0f}パーセントいました。"),
    dict(id="rates", sub=f"回るかどうかで、どれだけ変わるのか。1000円あたり14回転、16回転、18回転で比べます。この計算での損益の分かれ目は約{border:.1f}回転。それより回れば平均はプラス、回らなければマイナスです。",
         say=f"回るかどうかで、どれだけ変わるのか。千円あたり、14回転、16回転、18回転で比べます。この計算での、そんえきの分かれ目は、やく{border:.1f}回転。それより回れば平均はプラス、回らなければマイナスです。"),
    dict(id="month", sub=f"最後に、1ヶ月、20日間打ち続けた場合。勝った人は{win_month * 100:.1f}%、平均は{man(avg_month)}。日数を重ねるほど、運よりも回転率の差が効いてきます。",
         say=f"最後に、いっかげつ、はつかかん打ち続けた場合。勝った人は{win_month * 100:.1f}パーセント、平均は{yen_say(avg_month)}。日数を重ねるほど、運よりも、かいてんりつの差が効いてきます。"),
    dict(id="summary", face="happy",
         sub=f"まとめです。当たりの半分はチャージで、RUSHは約1/{R784}。入れば平均約{avg_rush:,.0f}個。そして、結果を決めるのは運だけでなく回転率です。",
         say=f"まとめです。当たりの半分はチャージで、ラッシュは、約{R784}分の1。入れば、平均約{round(avg_rush, -1):.0f}個。そして、結果を決めるのは、運だけでなく、かいてんりつです。"),
    dict(id="end", face="happy", voice="happy",
         sub="この動画は、AIがシミュレーションして作りました。数字は公開情報をもとにしていて、実際のお店の条件で変わります。遊ぶときは無理のない範囲で。電脳アリスでした。"),
]

# ---------------- 声 ----------------
_eng = {}


ENGINE = os.environ.get("VOICE", "kokoro")      # kokoro（Apache-2.0）／ hts（東北大 tohoku-f01）


def tts(say, emo):
    if ENGINE == "kokoro":
        from kokoro_ja import tts as ktts
        x, sr = ktts(say, voice="jf_alpha", speed=1.0)
        if sr != SR:                                   # 24kHz → 48kHz
            t_old = np.arange(len(x)) / sr
            t_new = np.arange(int(len(x) * SR / sr)) / SR
            x = np.interp(t_new, t_old, x).astype(np.float32)
        return x
    if emo not in _eng:
        _eng[emo] = pyopenjtalk.HTSEngine(os.path.join(VOICES, f"tohoku-f01-{emo}.htsvoice").encode())
    e = _eng[emo]
    e.set_speed(0.95)
    x = np.asarray(e.synthesize(pyopenjtalk.extract_fullcontext(say)), np.float32)
    return x / 32768.0


def tone(f, dur, amp, sr=SR, attack=0.01, decay=None):
    t = np.arange(int(dur * sr)) / sr
    env = np.minimum(1, t / attack) * (np.exp(-t / decay) if decay else 1)
    return amp * np.sin(2 * np.pi * f * t) * env


def bgm(total):
    """やわらかいシンセのコード進行＋軽いビート（プログラムで作曲、著作権の心配なし）。"""
    n = int(total * SR)
    out = np.zeros(n, np.float32)
    bpm, bar = 96, 4 * 60 / 96
    chords = [[57, 60, 64, 69], [53, 57, 60, 65], [55, 59, 62, 67], [52, 55, 59, 64]]   # Am F G Em
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    t0, i = 0.0, 0
    while t0 < total:
        ch = chords[i % 4]
        seg = min(bar, total - t0)
        a = int(t0 * SR)
        for m in ch:
            s = tone(hz(m), seg, 0.035, attack=0.3) + tone(hz(m) * 1.003, seg, 0.02, attack=0.3)
            out[a:a + len(s)] += s[: n - a]
        # アルペジオ
        for k in range(8):
            ts = t0 + k * bar / 8
            if ts >= total:
                break
            s = tone(hz(ch[k % 4] + 12), 0.25, 0.03, decay=0.12)
            b = int(ts * SR)
            out[b:b + len(s)] += s[: n - b]
        # キック・ハット
        for k in range(4):
            ts = t0 + k * 60 / bpm
            b = int(ts * SR)
            if ts < total:
                tt = np.arange(int(0.18 * SR)) / SR
                kick = 0.22 * np.sin(2 * np.pi * (50 + 80 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 18)
                out[b:b + len(kick)] += kick[: n - b]
                hb = int((ts + 30 / bpm) * SR)
                hat = 0.025 * rng.standard_normal(int(0.04 * SR)) * np.exp(-np.arange(int(0.04 * SR)) / SR * 90)
                out[hb:hb + len(hat)] += hat[: max(0, n - hb)]
        t0 += bar
        i += 1
    return out


BGM_DIR = os.path.join(ASSETS, "bgm")
# 場面 → 曲（オーナー提供。OpenTracks：商用の背景音楽として利用可・表記不要。作曲者ごとの条件はオーナー確認）
BGM_PLAN = [("hook", "summer_triangle.mp3"), ("spec", "nandeshou.mp3"), ("exp1", "honey_lemon.mp3"), ("summary", "morning.mp3")]


def load_mp3(path):
    import subprocess
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def bgm_tracks(total):
    n = int(total * SR)
    out = np.zeros(n, np.float32)
    starts = {s["id"]: s["start"] for s in S}
    plan = [(starts[sid] if sid != "hook" else 0.0, f) for sid, f in BGM_PLAN]
    xf = int(1.5 * SR)                                  # 曲のつなぎ目は1.5秒で重ねる
    for i, (t0, f) in enumerate(plan):
        t1 = plan[i + 1][0] if i + 1 < len(plan) else total
        a, b = int(t0 * SR), min(n, int(t1 * SR) + xf)
        x = load_mp3(os.path.join(BGM_DIR, f))
        x = x / (np.sqrt((x ** 2).mean()) + 1e-9) * 0.12  # 曲ごとの音量をそろえる
        seg = np.tile(x, (b - a) // len(x) + 1)[: b - a]
        env = np.ones(b - a, np.float32)
        k = min(xf, len(env) // 2)
        if i > 0:
            env[:k] = np.linspace(0, 1, k)
        if i + 1 < len(plan):
            env[-k:] = np.linspace(1, 0, k)
        out[a:b] += seg * env
    return out


def whoosh():
    d = 0.6
    t = np.arange(int(d * SR)) / SR
    noise = rng.standard_normal(len(t)).astype(np.float32)
    k = np.exp(-((t - 0.25) / 0.15) ** 2)
    sm = np.convolve(noise, np.ones(30) / 30, "same")
    return 0.25 * sm * k


def chime():
    return sum(tone(f, 1.2, 0.08, decay=0.35) for f in (1318.5, 1760, 2637))


def main():
    os.makedirs(ASSETS, exist_ok=True)
    # 読みの点検（全部通るまで声を作らない）
    problems = []
    for s in S:
        s["say"] = to_say(s.get("say") or s["sub"])
        kana, bad = check(s["say"])
        s["kana"] = kana
        if bad:
            problems.append((s["id"], bad, kana))
    if problems:
        for p in problems:
            print("読みの問題:", p)
        raise SystemExit(1)

    voice, t, mouth = [], 0.0, []
    for s in S:
        x = tts(s["say"], s.get("voice", "neutral"))
        pad = 1.4
        s["start"], s["voice_len"] = round(t, 3), round(len(x) / SR, 3)
        s["dur"] = round(len(x) / SR + pad, 3)
        buf = np.zeros(int(round(s["dur"] * SR)), np.float32)
        buf[: len(x)] = x
        voice.append(buf)
        t += s["dur"]
    lead = 1.0                                         # 冒頭1秒は音楽だけ
    for s in S:
        s["start"] = round(s["start"] + lead, 3)
    vo = np.concatenate([np.zeros(int(lead * SR), np.float32)] + voice)
    total = len(vo) / SR + 1.5
    vo = np.pad(vo, (0, int(total * SR) - len(vo)))

    # 口パク（1コマごとの声の大きさ → 0閉じ／1小／2大）
    hop = SR // FPS
    env = np.array([np.abs(vo[i * hop:(i + 1) * hop]).mean() for i in range(int(total * FPS))])
    ref = np.percentile(env[env > 1e-4], 85) if (env > 1e-4).any() else 1
    mouth = np.where(env > ref * 0.6, 2, np.where(env > ref * 0.22, 1, 0)).tolist()

    # BGM：OpenTracks（旧DOVA-SYNDROME）の曲を場面ごとに切り替える（曲はリポジトリに入れない）
    music = bgm_tracks(total) if os.path.isdir(BGM_DIR) else bgm(total)
    duck = np.repeat(np.array([0.45 if m else 1.0 for m in mouth], np.float32), hop)
    duck = np.convolve(np.pad(duck, (0, len(music) - len(duck)), constant_values=1.0), np.ones(4800) / 4800, "same")
    mix = vo * 0.95 + music * duck * 0.55
    for s in S:                                        # 場面の切り替わりで「シュッ」
        a = int((s["start"] - 0.25) * SR)
        w = whoosh()
        mix[a:a + len(w)] += w[: len(mix) - a]
    ex = next(x for x in S if x["id"] == "exp1")
    fx = {"trick": 6.0, "exp1": round(ex["dur"] - 3.0, 2), "avg": 1.0, "day": 9.0, "dayext": 1.0, "rates": 6.0, "month": 5.0}
    for sid, at in fx.items():
        s = next(x for x in S if x["id"] == sid)       # 大事な数字が出る瞬間に「キラン」（画面の紙吹雪と同じ時刻）
        a = int((s["start"] + at) * SR)
        c = chime()
        mix[a:a + len(c)] += c[: len(mix) - a]
    mix = np.clip(mix / max(1e-9, np.abs(mix).max()) * 0.92, -1, 1)
    with wave.open(os.path.join(ASSETS, "mix.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())

    data = dict(
        total=round(total, 3), fps=FPS, mouth=mouth, fx=fx,
        scenes=[{k: s[k] for k in ("id", "sub", "start", "dur", "voice_len")} | {"face": s.get("face", "open")} for s in S],
        stats=dict(enter_rate=enter_rate, avg_rush=avg_rush, chain_max=chain_max, chain_cnt=chain_cnt, over10k=over10k,
                   q50=q50, q90=q90, deep=deep, cost_cnt=cost_cnt, cost_edges=cost_edges, rate=RATE,
                   win_day=win_day, avg_day=avg_day, med_day=med_day, best_day=best_day, worst_day=worst_day,
                   norush_day=norush_day, border=border, day_cnt=day_cnt, day_edges=day_edges,
                   rates={str(r): [float((v > 0).mean()), float(v.mean())] for r, v in rates.items()},
                   win_month=win_month, avg_month=avg_month, r784=R784, C=C, seed=SEED,
                   cost_mean=float(to_rush.mean())),
        enter=enter.astype(int).tolist(),
        daywin=(day > 0).astype(int).tolist(),
        monthwin=(month > 0).astype(int).tolist(),
    )
    with open(os.path.join(ASSETS, "data.js"), "w") as f:
        f.write("window.DATA=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";")
    for s in S:
        print(f'{s["id"]:8s} {s["start"]:7.2f}s +{s["dur"]:5.2f}  {s["kana"][:60]}')
    print(f"total {total:.1f}s")


if __name__ == "__main__":
    main()
