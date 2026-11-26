"""説明欄 description.txt を作る（数字は results.json、章の時刻は assets/data.js から）。実行：python3 make_desc.py"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "results.json")))
D = json.loads(open(os.path.join(HERE, "assets", "data.js")).read()[len("window.DATA="):-1])
E1, E2, E3, E4, E5 = (R[k] for k in ("e1", "e2", "e3", "e4", "e5"))
p = lambda x: f"{x * 100:.1f}%"
NAME = {"intro": "1%を100回引けば当たる？（予想してみよう）", "c1": "実験① 100回引いたら、当たる？", "c2": "実験② じゃあ、何回引けば安心？",
        "c3": "実験③ 200回外れた。そろそろ出る？", "c4": "実験④ 天井があると、どうなる？", "c5": "実験⑤ 全6種類、そろえるには何回？", "end": "今日のまとめ"}
mmss = lambda t: f"{int(t) // 60}:{int(t) % 60:02d}"
chap = "\n".join(f"{mmss(0 if c['id'] == 'intro' else c['start'])} {NAME[c['id']]}" for c in D["chapters"])
txt = f"""確率1%のガチャ、100回引けば当たる？1万人でためしてみた【確率のお話】

「当たりは1%。100回引けば、1回は当たるはず」…本当でしょうか？
架空の「確率1%のガチャ」を、1万人で5つの実験にかけて確かめました。数字はすべてシミュレーションの結果です。

■目次
{chap}

■結果（各1万人）
・実験①：100回引いて、1回も当たらなかった人 {E1['zero']:,}人（{p(E1['zero_rate'])}）／当たった人 {E1['win']:,}人（{p(E1['win_rate'])}）
　計算の答え：0.99を100回掛けると {p(E1['zero_theory'])}（当たるのは {p(E1['win_theory'])}）
・実験②：当たるまで引いた回数　半分の人が当たるまで {E2['half']['sim']}回（計算 {E2['half']['theory']}回）／10人のうち9人 {E2['p90']['sim']}回（計算 {E2['p90']['theory']}回）／100人のうち99人 {E2['p99']['sim']}回（計算 {E2['p99']['theory']}回）
　平均 {E2['mean']}回（計算 100回）／いちばん運の悪かった人 {E2['max']}回／100回引いても当たらない人 {p(E2['over_mean'])}
・実験③：200回つづけて外れた人を1万人集めて（{E3['tried']:,}人が引いた）、さらに100回 → 当たった人 {E3['win']:,}人（{p(E3['win_rate'])}、計算 {p(E3['win_theory'])}）＝実験①とほぼ同じ（どちらも約63%）
・実験④：天井200回（200回引いても出なければもらえる）を実験②の1万人につけると、平均 {E2['mean']}回 → {E4['mean']}回（計算 {E4['mean_theory']}回）、いちばん悪い人 {E4['worst_nocap']}回 → {E4['worst']}回、天井まで行った人 {E4['reach']:,}人（{p(E4['reach_rate'])}、計算 {p(E4['reach_theory'])}）
・実験⑤：全6種類（どれも同じ確率）がそろうまで　平均 {E5['mean']}回（計算 {E5['mean_theory']}回）／10人のうち9人は {E5['p90']}回まで／6回ぴったり {E5['min_count']}人／いちばんかかった人 {E5['max']}回

■条件
・架空のガチャです（特定のゲーム・商品とは関係ありません）。当たりの確率は毎回1%で、前の結果に左右されません
・実験④の天井は「200回引いても出なければ、もらえる」としました。実験⑤は毎回6種類のどれか1つが同じ確率で出ます
・Python（numpy）でのシミュレーション、各1万人、乱数の種 {R['seed']}
・「約◯%」「約◯回」は四捨五入した数字です。実際のガチャの確率や天井の決まりは、それぞれの表示を確かめてください

解説：電脳アリス（AI）。AIがシミュレーションして制作
VOICEVOX:四国めたん
BGM：OpenTracks（旧DOVA-SYNDROME）
キャラクター画像：Canvaで生成（オリジナル）

#確率 #ガチャ #シミュレーション #電脳アリス #AI

---
【投稿設定】
・改変または合成されたコンテンツ：はい
・タイトル案：確率1%のガチャ、100回引けば当たる？1万人でためしてみた
・サムネ：thumb.png（1280×720）
"""
open(os.path.join(HERE, "description.txt"), "w").write(txt)
print(txt)
