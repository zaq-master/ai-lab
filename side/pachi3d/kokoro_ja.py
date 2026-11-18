"""Kokoro（Apache-2.0）の日本語音声で読み上げる。

日本語の読み（カナ）は Open JTalk で作り（yomi.py の点検と同じ読み）、
misaki の「カナ→発音記号」の表に渡して Kokoro に読ませる。
（misaki 標準の辞書 unidic はこの環境で入らないため、その部分だけ Open JTalk に置き換える）
モデル：~/.cache/hyperframes/tts（`npx hyperframes tts` が取ってきたもの）
"""
import os
from types import SimpleNamespace

import numpy as np
import pyopenjtalk

CACHE = os.path.expanduser("~/.cache/hyperframes/tts")
_k = None
_g2p = None


class _OJTTagger:
    """fugashi の Tagger の代わり：Open JTalk の単語分けと読みを返す。"""
    def __call__(self, text):
        out = []
        for w in pyopenjtalk.run_frontend(text):
            s, pron = w["string"], w["pron"].replace("’", "")
            if w["pos"] == "記号":
                pron = s
            out.append(SimpleNamespace(surface=s, feature=SimpleNamespace(pron=pron, kana=pron),
                                       char_type=3 if w["pos"] == "記号" else 6, is_unk=False))
        return out


def g2p(text):
    global _g2p
    if _g2p is None:
        import sys
        import types
        sys.modules.setdefault("fugashi", types.SimpleNamespace(Tagger=lambda *a, **k: _OJTTagger()))
        from misaki import ja
        _g2p = ja.JAG2P()
        _g2p.tagger = _OJTTagger()
    return _g2p(text)


def tts(text, voice="jf_alpha", speed=1.0):
    """text（読み上げ用の文）→ (波形 float32 -1..1, サンプリング周波数)"""
    global _k
    if _k is None:
        from kokoro_onnx import Kokoro
        _k = Kokoro(os.path.join(CACHE, "models", "kokoro-v1.0.onnx"), os.path.join(CACHE, "voices", "voices-v1.0.bin"))
    ph = g2p(text)
    x, sr = _k.create(ph, voice=voice, speed=speed, lang="ja", is_phonemes=True)
    return np.asarray(x, np.float32), sr


if __name__ == "__main__":
    import sys
    import wave
    t = sys.argv[1] if len(sys.argv) > 1 else "こんにちは、電脳アリスです。今日は、話題のラッキートリガー機を、いちまんにんで打ってみます。"
    print(g2p(t))
    x, sr = tts(t)
    print(len(x) / sr, "sec")
    with wave.open(sys.argv[2] if len(sys.argv) > 2 else "kokoro_ja_test.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
