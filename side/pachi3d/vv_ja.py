"""VOICEVOX（四国めたん）で読み上げる。オーナーが規約に同意済み（2026-11-18）。
クレジット必須：「VOICEVOX:四国めたん」（説明欄と動画の最後）。

準備（新しい環境では毎回。GitHubのAPIは使えないので版を直接指定してダウンロード）：
  mkdir -p ~/vv && cd ~/vv
  curl -sSLO https://github.com/VOICEVOX/voicevox_core/releases/download/0.16.0/voicevox_core-0.16.0-cp310-abi3-manylinux_2_34_x86_64.whl
  curl -sSLO https://github.com/VOICEVOX/onnxruntime-builder/releases/download/voicevox_onnxruntime-1.17.3/voicevox_onnxruntime-linux-x64-1.17.3.tgz
  curl -sSLO https://github.com/VOICEVOX/voicevox_vvm/releases/download/0.16.0/0.vvm   # 四国めたん・ずんだもん等
  pip install voicevox_core-0.16.0-*.whl && tar xzf voicevox_onnxruntime-linux-x64-1.17.3.tgz
辞書は pyopenjtalk に入っている open_jtalk_dic_utf_8-1.11 を使う。
声・モデルファイルはコミットしない。
"""
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from yomi import to_say  # noqa: E402

VV = os.environ.get("VV_DIR", os.path.expanduser("~/vv"))
if not os.path.isdir(VV):
    VV = "/home/user/vv"
STYLE = {"normal": 2, "amaama": 0, "tsuntsun": 6}   # 四国めたん
SR = 24000
_syn = None


def _get():
    global _syn
    if _syn is None:
        import pyopenjtalk
        from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile
        ort = Onnxruntime.load_once(filename=os.path.join(
            VV, "voicevox_onnxruntime-linux-x64-1.17.3/lib/libvoicevox_onnxruntime.so.1.17.3"))
        dic = os.path.join(os.path.dirname(pyopenjtalk.__file__), "open_jtalk_dic_utf_8-1.11")
        _syn = Synthesizer(ort, OpenJtalk(dic))
        with VoiceModelFile.open(os.path.join(VV, "0.vvm")) as m:
            _syn.load_voice_model(m)
    return _syn


def tts(text, style="normal", speed=1.1, pitch=0.0, intonation=1.15):
    """1文を合成して (float32波形, 24000)。読みは yomi.to_say を通した文で作る。"""
    import io
    import wave
    syn = _get()
    sid = STYLE.get(style, style)
    q = syn.create_audio_query(to_say(text), sid)
    q.speed_scale, q.pitch_scale, q.intonation_scale = speed, pitch, intonation
    q.pre_phoneme_length, q.post_phoneme_length = 0.05, 0.05
    w = syn.synthesis(q, sid)
    with wave.open(io.BytesIO(w)) as f:
        x = np.frombuffer(f.readframes(f.getnframes()), np.int16).astype(np.float32) / 32768
        return x, f.getframerate()


def tts_script(text, sr_out=None):
    """語りかけ調：問いかけ・！は「あまあま」で明るく、数字の文はゆっくり、…と？のあとは間。"""
    parts = [p for p in re.findall(r"[^。？！…]+[。？！…]*", text) if p.strip()]
    out, sr = [], SR
    for p in parts:
        is_q = "？" in p or "?" in p
        has_num = bool(re.search(r"[0-9０-９]|パーセント|万円|分の", p))
        bright = is_q or "！" in p
        x, sr = tts(p, "amaama" if bright else "normal", 1.0 if has_num else 1.12,
                    0.02 if bright else 0.0, 1.3 if bright else 1.1)
        out.append(x)
        gap = 0.35 if is_q else 0.4 if "…" in p else 0.1
        out.append(np.zeros(int(sr * gap), np.float32))
    y = np.concatenate(out) if out else np.zeros(1, np.float32)
    if sr_out and sr_out != sr:
        y = np.interp(np.arange(int(len(y) * sr_out / sr)) / sr_out, np.arange(len(y)) / sr, y).astype(np.float32)
        sr = sr_out
    return y, sr


if __name__ == "__main__":
    import soundfile as sf
    s = sys.argv[1] if len(sys.argv) > 1 else "500回転もハマってる台。そろそろ当たりそうな気、しませんか？結果は…A組52.4%。B組53.9%。ほとんど、同じなんです。"
    y, sr = tts_script(s)
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "renders", "voice_metan.wav")
    sf.write(out, y, sr)
    print(out, round(len(y) / sr, 1), "s")
