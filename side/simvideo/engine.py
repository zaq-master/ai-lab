"""シミュレーション動画の共通エンジン（1920x1080・30fps）。

・場面（Scene）ごとに「ナレーション文」と「描画関数 draw(img, t, dur)」を持つ
・声は Open JTalk（pyopenjtalk、無料・端末内）。場面の長さ＝声の長さ＋余白
・映像は PIL で1枚ずつ描き、ffmpeg にそのまま流し込む（中間ファイルなし）
"""
import os
import subprocess
import wave

import numpy as np
import pyopenjtalk
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 30
FONT = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"

# 色（暗い紺の背景に、光る点）
BG = (16, 22, 40)
FG = (240, 236, 226)
SUB = (150, 162, 190)
HIT = (255, 196, 64)
MISS = (52, 62, 92)
ACCENT = (255, 120, 80)
BLUE = (96, 170, 255)

_fonts = {}


def font(size):
    if size not in _fonts:
        _fonts[size] = ImageFont.truetype(FONT, size)
    return _fonts[size]


def text(d, xy, s, size, fill=FG, anchor="la", stroke=0):
    d.text(xy, s, font=font(size), fill=fill, anchor=anchor,
           stroke_width=stroke, stroke_fill=fill)


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


class Scene:
    def __init__(self, narration, draw, pad=0.6, min_dur=0.0):
        self.narration = narration
        self.draw = draw
        self.pad = pad
        self.min_dur = min_dur


def tts(s, speed=1.08):
    x, sr = pyopenjtalk.tts(s, speed=speed)
    return x.astype(np.float32), sr


def subtitle(img, s):
    """画面下に字幕（2行まで自動改行）。"""
    d = ImageDraw.Draw(img)
    size, maxw = 46, W - 240
    lines, cur = [], ""
    for ch in s:
        if d.textlength(cur + ch, font=font(size)) > maxw and ch not in "、。」）！？":
            lines.append(cur)
            cur = ch
        else:
            cur += ch
    lines.append(cur)
    lines = lines[-2:]
    y = H - 70 - 62 * len(lines)
    d.rectangle([0, y - 20, W, H], fill=(8, 12, 24))
    for i, ln in enumerate(lines):
        text(d, (W // 2, y + 62 * i), ln, size, FG, anchor="ma")


def render(scenes, out_path, footer="AIがシミュレーションして制作"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    # 1) 声を作り、場面の長さを決める
    sr = 48000
    tracks, durs = [], []
    for sc in scenes:
        if sc.narration:
            x, sr = tts(sc.narration)
        else:
            x = np.zeros(0, np.float32)
        dur = max(len(x) / sr + sc.pad, sc.min_dur)
        n = int(round(dur * sr))
        buf = np.zeros(n, np.float32)
        buf[: len(x)] = x
        tracks.append(buf)
        durs.append(dur)
    audio = np.concatenate(tracks)
    peak = np.abs(audio).max() or 1
    audio = (audio / peak * 0.85 * 32767).astype(np.int16)
    wav_path = out_path.replace(".mp4", ".wav")
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(audio.tobytes())

    # 2) 映像を描いて ffmpeg へ
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", wav_path,
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-shortest", out_path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for sc, dur in zip(scenes, durs):
        nf = int(round(dur * FPS))
        for f in range(nf):
            img = Image.new("RGB", (W, H), BG)
            sc.draw(img, f / FPS, dur)
            d = ImageDraw.Draw(img)
            text(d, (W - 40, 30), footer, 26, SUB, anchor="ra")
            if sc.narration:
                subtitle(img, sc.narration)
            p.stdin.write(img.tobytes())
    p.stdin.close()
    p.wait()
    os.remove(wav_path)
    return sum(durs)
