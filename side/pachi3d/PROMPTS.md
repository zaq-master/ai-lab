# ハイクオリティ3D動画のためのプロンプト集（2026-11-18）

オーナーが外部ツールで作る素材（①アリスの絵 ②BGM）と、AI（Claude）に毎回渡す制作指示（③）。
作った素材は `side/pachi3d/assets/src/` に置けば、AIが動画に組み込む。

---

## ① 電脳アリスのキャラクター素材（画像生成AI用）

使うツール：ChatGPT（画像生成）／Midjourney（niji）など、**商用利用が認められているプラン**のもの。
必ず `music/01_1-319/alice_small.png`（今のアリスの絵）を**参照画像として添付**して、同じキャラに寄せる。

### ①-1 キャラ設定画（最初に1枚）
```
Character design sheet of an original anime VTuber girl named "Dennou Alice" (cyber Alice).
Use the attached image as the character reference and keep the same design.
- long straight silver-white hair with soft lavender shading, blunt bangs
- large sparkling sapphire-blue eyes with detailed highlights
- black-and-navy gothic lolita dress with a white sailor collar and a big blue ribbon on the chest
- navy headphones with glowing blue spade (♠) emblems on the ear cups, small blue ribbon on the head
- subtle cyber details: thin glowing blue circuit lines on the dress, playing-card motifs
- cute, friendly, intelligent expression, age-ambiguous young adult, modest outfit
Full body front view + back view + 3/4 view, standing pose, clean lineart, cel shading,
high detail, pure white background, consistent proportions, 16:9, high resolution.
```

### ①-2 表情差分（口パク・まばたき用。**同じ構図で**何枚も出す）
```
Same character as the reference image, upper body (waist up), front view, facing the camera,
same pose, same framing, same lighting, plain white background, high resolution.
Expression: [ここを差し替え]
```
差し替える表情（この10枚があれば、話す・笑う・驚くが全部できる）：
1. `neutral, mouth closed, gentle smile`（ふつう・口閉じ）
2. `talking, mouth slightly open`（話す・口小）
3. `talking, mouth wide open "a" shape`（話す・口大）
4. `eyes closed, mouth closed, calm`（まばたき）
5. `big happy smile, eyes closed in ^^ shape`（笑顔）
6. `surprised, eyes wide, small round open mouth`（驚き）
7. `thinking, finger on chin, eyes looking up`（考える）
8. `pointing to the left with the right hand, confident smile`（左の画面を指さす）
9. `troubled, sweat drop, awkward smile`（困った）
10. `excited, both fists up, sparkling eyes`（盛り上がる）

> 1・2・3・4 は**顔の位置が1ピクセルもずれない**のが理想。ずれる場合はAIが位置合わせする。

### ①-3（もっと上を目指すなら）3Dモデル
- **VRoid Studio（無料）** で①-1の設定画を見ながら作り、**VRM形式で書き出す**。
  目・口・まばたきの動きが最初から入っているので、AIが3Dの中で歩かせたり、指さしたり、表情を変えたりできる。
- 書き出し設定：ポリゴン数「中」、テクスチャ 2048px。利用条件は「本人のみ・商用可」。

---

## ② BGM（Suno用。オーナー契約のProで作れば商用可）
```
Instrumental only, no vocals. Bright, playful chiptune-pop for a Japanese educational
YouTube variety show about probability and pachinko simulations.
96 BPM, catchy synth lead, light 8-bit arpeggios, soft drums, positive and curious mood,
loopable, no sudden drops, background music under narration.
```
- 2〜3曲作り、正式な Download で落として `side/pachi3d/assets/src/bgm_*.mp3` に置く。
- 盛り上がり用（大当たり・結果発表）にもう1曲：上の文の `positive and curious mood` を `triumphant, festive, exciting` に変える。

---

## ③ 制作指示（毎回、AIにそのまま渡す）
```
電脳アリスが解説する「パチンコ実機を1万人でシミュレーション」の動画を作って。
対象機種：[機種名]

【品質の目標】
人気YouTuberのシミュレーション動画に負けない見た目。明るくポップな3D、
キャラが表情豊かに動き、テロップ・効果音・BGMでテンポよく見せる。

【必ず守ること】
- 数字はすべて実際のシミュレーション結果から自動で入れる（手書きしない）
- スペックは公開情報で確認し、出典を残す。確認できない数字は使わない
- ネットの写真・実機画像・メーカー画像・アニメの絵は使わない（台はオリジナルの3D）
- 「勝てる」とあおらない。最後に「AI制作」「必勝法ではない」「18歳未満は遊技できない」
- 読み上げは全文をカナで点検し、誤読ゼロにしてから声を作る

【見た目は毎回その回の内容にちなむ（2026-11-18 オーナー指示）】
- 背景・色・3Dの舞台・小道具・テロップの飾り・BGM・効果音・切り替えの演出まで「全部」をその回の題材に合わせる。
  毎回同じ空と雲・同じ床の使い回しにしない（雲と木の床は第1回だけ）。
- 例：海の台なら海中と泡、和風の台なら和室・提灯・桜、宇宙ものなら星空とネオン、ガチャの回ならカプセル機。
  実機・メーカー・アニメの絵は使わず、題材の「雰囲気」をオリジナルで作る。
- 臨機応変に、その回でいちばん驚く見せ方を1つ入れる（例：1万人が出玉の山に埋もれる、RUSHの連チャンを塔の高さで見せる）。

【語り方（2026-11-18 オーナー指示：確率シミュレーション大学のように聞き手に優しく語りかける）】
- 語りかける：「〜ですよね？」「実はこれ、〜なんです」「じゃあ、どうなると思いますか？」
- 1文に1つのこと。短く区切る
- 問いかけのあとに間（考えてもらう）、答えの前に「…」でためる
- 大事な数字はゆっくり（sbv2_ja.tts_script が自動で：数字の文は遅め、問いかけ・驚きは明るい調子）
- 締めはコメント誘導（「次に試してほしいこと、コメントで教えてね！」）
- 尺は40〜60秒。冒頭2秒で問いかけ

【シミュレーション条件】side/pachi3d/pachisim.py（リアルな1日）を使い、回転率・交換率・時間・財布・持ち玉・やめる作戦を必ず画面と説明欄に出す（詳細は pachi-sim-video スキル 2.5）

【構成】side/pachi3d/STRUCTURE.md の順番で作る（問いかけ→予想→ルール→実験→結果→理由→締め）

【作り方】
- まず10秒のテスト動画（いちばん見せたい場面）を作って送る（トークン節約。2026-11-18 オーナー指示）。OKが出てから本編（約5分）
- アリスは side/pachi3d/assets/src/ の素材を使う（無ければ今のちびキャラ）
- BGMは assets/src/bgm_*.mp3、無ければ自作
- 声は VOICEVOX が使えればそれ、無ければ今の声
- 新しく使えそうな無料・高品質の道具があれば、自分で探して試す

【構成】
予告（10秒）→ あいさつ → スペック → 仕組みの説明 → 実験4〜5個 → まとめ → 注意書き
各実験：問いかけ →（3Dで）1万人が打つ → 結果の数字がドンと出る → アリスがひと言
```

---

## ④ 置き場所
```
side/pachi3d/assets/src/
  alice_sheet.png           ①-1 設定画
  alice_01_neutral.png …    ①-2 表情差分（番号は上の一覧と同じ）
  alice.vrm                 ①-3 3Dモデル（あれば）
  bgm_main.mp3 / bgm_hype.mp3   ② BGM
```
