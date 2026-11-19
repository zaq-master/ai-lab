"""リアルなパチンコの1日を1万人分シミュレーションする共通エンジン（今後の動画はすべてこれを使う）。

再現すること（2026-11-18 オーナー指示「シミュレーション条件も具体的かつリアルに」）
- お金：1玉4円で借りる（1000円＝250玉）。財布の上限を超えたら終わり
- 交換率：等価（4円）／28玉（約3.57円）／30玉（約3.33円）など。最後に持ち玉を交換して収支を出す
- 回転率：1000円あたり◯回転（＝1回転に使う玉 250/回転率）。人ごと・台ごとに少しばらつく
- 時間：通常時は1時間あたり約240回転が上限（玉の打ち出し1分100発＋演出・保留の時間）
        大当たり消化・RUSH中の時間もかかる → 閉店時間で打ち切り
- 持ち玉：当たった玉は持ち玉になり、次は持ち玉から打つ（現金は持ち玉が尽きてから）
- 出玉：払い出しから「打ちながら消化する分」を引いた実質の出玉（net_ratio）
- RUSH中：電サポ中も玉は少しずつ減る（rush_ball_per_spin、マイナス）
- やめる作戦：閉店まで／勝ったら帰る／負け額の上限／RUSH終了でやめる 等（stop 関数）

使い方：
    from pachisim import ST_MACHINE_TOKYOGHOUL, Conditions, simulate
    r = simulate(ST_MACHINE_TOKYOGHOUL, Conditions(rate=17, exchange_yen=4.0, hours=8), n=10000, seed=1)
    r["yen"]  # 1人ずつの収支（円）
"""
from dataclasses import dataclass, field

import numpy as np


@dataclass
class Machine:
    """ST（一定回転のRUSH）型の台。数字は公開スペックから入れ、出典を sources に残す"""
    name: str
    p_normal: float                    # 通常時、図柄揃いの確率
    normal_hits: list                  # 通常時の当たり振り分け [(割合, 払い出し個数, RUSHに入るか)]
    p_charge: float = 0.0              # 小当たり・チャージ等の確率（RUSHに入らない少量の当たり）
    charge_pay: int = 0
    st_spins: int = 130                # RUSHの回転数
    p_rush: float = 1 / 95.3           # RUSH中の当たり確率
    rush_hits: list = field(default_factory=lambda: [(1.0, 3000)])  # RUSH中の振り分け [(割合, 払い出し)]
    net_ratio: float = 0.933           # 払い出しのうち実際に増える割合。1R＝払い出し150個−打ち込み10個＝140個（140/150）。2026-11-19 確認
    rush_ball_per_spin: float = -0.3   # RUSH中1回転あたりの玉の増減（電サポ中の目減り）
    sec_per_rush_spin: float = 3.0     # RUSH中1回転にかかる秒数
    sec_per_1000_balls: float = 75.0   # 大当たり消化：1000個払い出すのにかかる秒数
    sources: list = field(default_factory=list)


@dataclass
class Conditions:
    rate: float = 17.0                 # 1000円あたりの回転数（ホールの一般的な目安：16〜20）
    rate_spread: float = 0.8           # 台ごとの回転率のばらつき（標準偏差、回転/1000円）
    exchange_yen: float = 4.0          # 1玉あたりの交換額（等価4.0／28玉≒3.57／30玉≒3.33）
    hours: float = 8.0                 # 打つ時間（例：10時〜18時）
    spins_per_hour: float = 240.0      # 通常時の1時間あたりの回転数の上限
    budget_yen: float = 50000.0        # 財布の上限（これ以上は使わない）
    stop_win_yen: float = None         # この金額以上勝っていたら、RUSH終了時に帰る（None＝帰らない）
    stop_after_rush: bool = False      # 1回RUSHが終わったら帰る
    finish_rush: bool = True           # 時間を過ぎてもRUSH・大当たり中は最後まで打つ（False＝閉店で打ち切り）
    hashidama: bool = True             # 交換できない端玉（exchange_unit未満）は0円として扱う
    exchange_unit: int = 1             # 特殊景品1個あたりの玉数の刻み（例：等価で25玉＝100円）


def simulate(m: Machine, c: Conditions, n=10000, seed=0):
    rng = np.random.default_rng(seed)
    C = 1 - (1 - m.p_rush) ** m.st_spins            # RUSH継続率（参考）
    rush_p = np.array([h[0] for h in m.rush_hits]); rush_pay = np.array([h[1] for h in m.rush_hits])
    nh_p = np.array([h[0] for h in m.normal_hits]); nh_pay = np.array([h[1] for h in m.normal_hits]); nh_in = np.array([h[2] for h in m.normal_hits])
    out = dict(yen=np.zeros(n), cash=np.zeros(n), balls_end=np.zeros(n), spins=np.zeros(n, int), hits=np.zeros(n, int),
               rush_entries=np.zeros(n, int), max_chain=np.zeros(n, int), hours_played=np.zeros(n),
               first_rush_cash=np.full(n, -1.0), first_rush_spin=np.full(n, -1, int),
               big_hits=np.zeros(n, int), charge_hits=np.zeros(n, int), broke=np.zeros(n, bool))   # 初めてRUSHに入った時点の現金・回転数（入れなければ-1）
    total_sec = c.hours * 3600
    for i in range(n):
        rate = max(8.0, rng.normal(c.rate, c.rate_spread))
        balls_per_spin = 250.0 / rate
        sec_per_spin = 3600.0 / c.spins_per_hour
        t = 0.0; balls = 0.0; cash = 0.0; spins = 0; hits = 0; entries = 0; maxc = 0; big = 0; chg = 0; broke = False
        while t < total_sec:
            # 玉が足りなければ現金で借りる（1000円ずつ）
            if balls < balls_per_spin:
                if cash + 1000 > c.budget_yen:
                    broke = True
                    break
                cash += 1000; balls += 250
            balls -= balls_per_spin; spins += 1; t += sec_per_spin
            u = rng.random()                                   # 1回の抽選で 大当たり／小当たり／ハズレ を排他的に決める
            hit_normal = u < m.p_normal
            hit_charge = (not hit_normal) and u < m.p_normal + m.p_charge
            if hit_charge:
                balls += m.charge_pay * m.net_ratio; t += m.charge_pay / 1000 * m.sec_per_1000_balls; hits += 1; chg += 1
            if not hit_normal:
                continue
            k = rng.choice(len(nh_p), p=nh_p)
            balls += nh_pay[k] * m.net_ratio; t += nh_pay[k] / 1000 * m.sec_per_1000_balls; hits += 1; big += 1
            if not nh_in[k]:
                continue
            # RUSH：ST回転のうちに当たれば継続
            if entries == 0:
                out["first_rush_cash"][i] = cash; out["first_rush_spin"][i] = spins
            entries += 1; chain = 0
            while True:
                g = rng.geometric(m.p_rush)
                used = min(g, m.st_spins)
                balls += used * m.rush_ball_per_spin; t += used * m.sec_per_rush_spin
                if g > m.st_spins or (t >= total_sec and not c.finish_rush):
                    break
                j = rng.choice(len(rush_p), p=rush_p)
                balls += rush_pay[j] * m.net_ratio; t += rush_pay[j] / 1000 * m.sec_per_1000_balls
                chain += 1; hits += 1; big += 1
            maxc = max(maxc, chain)
            now = balls * c.exchange_yen - cash
            if c.stop_after_rush or (c.stop_win_yen is not None and now >= c.stop_win_yen):
                break
        paid = (balls // c.exchange_unit) * c.exchange_unit if c.hashidama else balls
        out["yen"][i] = paid * c.exchange_yen - cash
        out["big_hits"][i] = big; out["charge_hits"][i] = chg; out["broke"][i] = broke
        out["cash"][i] = cash; out["balls_end"][i] = balls; out["spins"][i] = spins; out["hits"][i] = hits
        out["rush_entries"][i] = entries; out["max_chain"][i] = maxc; out["hours_played"][i] = t / 3600   # RUSHを最後まで打った分も含む
    out["rush_continue_rate"] = C
    return out


def describe(c: Conditions):
    """動画の画面・説明欄に出す条件の文（必ず表示する）"""
    ex = {4.0: "等価（1玉4円）", 3.57: "28玉交換（1玉約3.57円）", 3.33: "30玉交換（1玉約3.33円）"}.get(round(c.exchange_yen, 2), f"1玉{c.exchange_yen}円")
    s = f"1000円あたり{c.rate:g}回転・{ex}・{c.hours:g}時間・財布{int(c.budget_yen / 10000)}万円まで・持ち玉で遊技"
    if c.stop_after_rush:
        s += "・RUSH終了でやめる"
    if c.stop_win_yen is not None:
        s += f"・{int(c.stop_win_yen / 10000)}万円勝ったら帰る"
    return s


# 公開スペック（攻略サイト等。メーカー公式資料とは未照合）
# 2026-11-18 再確認：1geki.jp/pachinko/e_tokyoghoul/ と pachiseven.jp/machines/7159 で一致
ST_MACHINE_TOKYOGHOUL = Machine(
    name="e東京喰種",
    p_normal=1 / 399.9,
    normal_hits=[(0.50, 1500, True), (0.01, 300, True), (0.49, 1500, False)],
    p_charge=1 / 399.9, charge_pay=300,
    st_spins=130, p_rush=1 / 95.3,
    rush_hits=[(0.03, 6000), (0.97, 3000)],
    sources=["https://1geki.jp/pachinko/e_tokyoghoul/", "https://pachiseven.jp/machines/7159"],
)


if __name__ == "__main__":
    import time
    t0 = time.time()
    c = Conditions(rate=17, exchange_yen=4.0, hours=8, budget_yen=50000)
    r = simulate(ST_MACHINE_TOKYOGHOUL, c, n=2000, seed=1)
    y = r["yen"]
    print(describe(c))
    print(f"勝率 {(y > 0).mean()*100:.1f}%  平均 {y.mean():+.0f}円  中央値 {np.median(y):+.0f}円  "
          f"平均回転 {r['spins'].mean():.0f}  RUSH平均 {r['rush_entries'].mean():.2f}回  遊技時間 {r['hours_played'].mean():.1f}h  "
          f"財布切れ {r['broke'].mean()*100:.1f}%  {time.time()-t0:.1f}s")
