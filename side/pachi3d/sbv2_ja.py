"""Style-Bert-VITS2 で日本語を読み上げる（CPU）。

声のモデル（voices_sbv2/、リポジトリには入れない）
  ami  ：小春音アミ（CV:あみたろ） クレジット必須「Style-BertVITS2モデル: 小春音アミ、あみたろの声素材工房 (https://amitaro.net/)」
  jvnv ：JVNV F1（JP-Extra） CC BY-SA 4.0 クレジット必須「JVNVコーパス（CC BY-SA 4.0）」
読みは Open JTalk（SBV2 内部）＝ yomi.py の点検と同じ読み。
"""
import os
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
VOICES = {
    "ami": ("voices_sbv2/ami/koharune-ami", "koharune-ami.safetensors"),
    "jvnv": ("voices_sbv2/jvnv/jvnv-F1-jp", "jvnv-F1-jp_e160_s14000.safetensors"),
}
BERT = "ku-nlp/deberta-v2-large-japanese-char-wwm"
_models = {}


def _load(name):
    if name in _models:
        return _models[name]
    from style_bert_vits2.constants import Languages
    from style_bert_vits2.nlp import bert_models
    from style_bert_vits2.tts_model import TTSModel
    if not _models:
        bert_models.load_model(Languages.JP, BERT).float()   # 新しい transformers は半精度のまま読むので、CPU用に通常精度へ
        bert_models.load_tokenizer(Languages.JP, BERT)
    d, f = VOICES[name]
    d = os.path.join(HERE, d)
    m = TTSModel(model_path=os.path.join(d, f), config_path=os.path.join(d, "config.json"),
                 style_vec_path=os.path.join(d, "style_vectors.npy"), device="cpu")
    _models[name] = m
    return m


def styles(name):
    return list(_load(name).style2id.keys())


def tts(text, name="ami", style="Neutral", style_weight=1.0, speed=1.0):
    """→ (波形 float32 -1..1, サンプリング周波数)"""
    m = _load(name)
    sr, x = m.infer(text=text, style=style, style_weight=style_weight, length=1.0 / speed)
    x = np.asarray(x, np.float32)
    if np.abs(x).max() > 1.5:                 # int16 で返る場合
        x = x / 32768.0
    return x, sr


def save(path, x, sr):
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "ami"
    print(name, styles(name))


def tts_script(text, name="ami", sr_out=None):
    """語りかけ調の読み上げ：1文ずつ声を作り、文の種類で速さ・声の調子・間を変える。
    - 問いかけ（？）：明るい調子、あとに長めの間（考えてもらう）
    - 数字を含む文：少しゆっくり（大事な数字を聞き取りやすく）
    - 「…」：その場で間を置く
    - ふつうの文：落ち着いた調子
    """
    import re
    parts = [p for p in re.findall(r"[^。？！…]+[。？！…]*", text) if p.strip()]
    out, sr = [], 44100
    for p in parts:
        is_q = "？" in p or "?" in p
        has_num = bool(re.search(r"[0-9０-９]|パーセント|万円|分の", p))
        style = "るんるん" if (is_q or "！" in p) else "Neutral"
        speed = 0.97 if has_num else 1.12
        x, sr = tts(p, name, style, 1.0, speed)
        out.append(x)
        gap = 0.35 if is_q else 0.4 if "…" in p else 0.1
        out.append(np.zeros(int(sr * gap), np.float32))
    y = np.concatenate(out) if out else np.zeros(1, np.float32)
    if sr_out and sr_out != sr:
        y = np.interp(np.arange(int(len(y) * sr_out / sr)) / sr_out, np.arange(len(y)) / sr, y).astype(np.float32)
        sr = sr_out
    return y, sr
