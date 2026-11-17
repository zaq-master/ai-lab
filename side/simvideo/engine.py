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
    def __init__(self, narration, draw, pad=0.6, min_dur=0.0, face=("open", "smile"), voice=None):
        self.narration = narration
        self.draw = draw
        self.pad = pad
        self.min_dur = min_dur
        self.face = face
        self.voice_name = voice


_engines = {}
VOICES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voices")


def tts(s, speed=1.0, voice=None):
    """voice=None は既定の男性声。"alice" / "alice_happy" は tohoku-f01（女性・CC BY 4.0）。"""
    if not voice:
        x, sr = pyopenjtalk.tts(s, speed=speed)
        return x.astype(np.float32), sr
    emo = "happy" if voice.endswith("happy") else "neutral"
    if emo not in _engines:
        _engines[emo] = pyopenjtalk.HTSEngine(os.path.join(VOICES, f"tohoku-f01-{emo}.htsvoice").encode())
    e = _engines[emo]
    e.set_speed(speed * 0.94)          # アリスは少しゆっくり（聞き取りやすさ）
    x = e.synthesize(pyopenjtalk.extract_fullcontext(s))
    return np.asarray(x, np.float32), e.get_sampling_frequency()


class Host:
    """解説役（電脳アリス）。声の大きさで口を動かし、ときどき瞬きする。"""
    def __init__(self, x, y, h, assets=None):
        self.x, self.y, self.h = x, y, h
        self.dir = assets or os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
        self.cache = {}

    def img(self, eyes, mouth):
        k = (eyes, mouth)
        if k not in self.cache:
            im = Image.open(os.path.join(self.dir, f"alice_{eyes}_{mouth}.png")).convert("RGBA")
            w = int(im.width * self.h / im.height)
            self.cache[k] = im.resize((w, self.h), Image.LANCZOS)
        return self.cache[k]

    def draw(self, img, gt, amp, face):
        eyes, idle = face
        mouth = idle
        if amp > 0.55:
            mouth = "a"
        elif amp > 0.2:
            mouth = "o"
        if eyes == "open" and (gt % 3.7) < 0.12:
            eyes = "closed"
        bob = int(6 * np.sin(gt * 1.6))
        im = self.img(eyes, mouth)
        img.paste(im, (self.x, self.y + bob), im)


def sentences(s):
    out, cur = [], ""
    for ch in s:
        cur += ch
        if ch in "。？！":
            out.append(cur)
            cur = ""
    if cur:
        out.append(cur)
    return out


def subtitle(img, s, progress=0.0):
    """画面下に字幕。声の進み具合（0〜1）に合わせて、1文ずつ切り替えて出す。"""
    parts = sentences(s)
    total = sum(len(x) for x in parts)
    acc = 0
    for x in parts:
        acc += len(x)
        if acc / total >= progress:
            s = x
            break
    d = ImageDraw.Draw(img)
    size, maxw = 46, W - 240
    total = d.textlength(s, font=font(size))
    lines = [s]
    if total > maxw:                     # 2行に均等に分ける（句読点で行を始めない）
        cur = ""
        for i, ch in enumerate(s):
            cur += ch
            if d.textlength(cur, font=font(size)) >= total / 2 and (i + 1 < len(s) and s[i + 1] not in "、。」）！？"):
                lines = [cur, s[i + 1:]]
                break
    lines = lines[-2:]
    y = H - 70 - 62 * len(lines)
    d.rectangle([0, y - 20, W, H], fill=(8, 12, 24))
    for i, ln in enumerate(lines):
        text(d, (W // 2, y + 62 * i), ln, size, FG, anchor="ma")


def render(scenes, out_path, footer="AIがシミュレーションして制作", voice=None, host=None, bg=None):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    # 1) 声を作り、場面の長さを決める
    sr = 48000
    tracks, durs = [], []
    for sc in scenes:
        if sc.narration:
            x, sr = tts(sc.narration, voice=sc.voice_name or voice)
        else:
            x = np.zeros(0, np.float32)
        sc.voice = len(x) / sr
        dur = max(sc.voice + sc.pad, sc.min_dur)
        n = int(round(dur * sr))
        buf = np.zeros(n, np.float32)
        buf[: len(x)] = x
        tracks.append(buf)
        durs.append(dur)
        # 1コマごとの声の大きさ（口パク用、0〜1）
        nf = int(round(dur * FPS))
        hop = sr // FPS
        env = np.array([np.abs(buf[i * hop:(i + 1) * hop]).mean() if i * hop < len(buf) else 0 for i in range(nf)])
        sc.env = env / (np.percentile(env, 90) + 1e-9) if env.max() > 0 else env
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
    gt = 0.0
    for sc, dur in zip(scenes, durs):
        nf = int(round(dur * FPS))
        for f in range(nf):
            img = bg.copy() if bg is not None else Image.new("RGB", (W, H), BG)
            sc.draw(img, f / FPS, dur)
            if host is not None:
                host.draw(img, gt, float(sc.env[f]) if f < len(sc.env) else 0.0, sc.face)
            gt += 1 / FPS
            d = ImageDraw.Draw(img)
            text(d, (W - 40, 30), footer, 26, SUB, anchor="ra")
            if sc.narration:
                subtitle(img, sc.narration, (f / FPS) / max(0.1, sc.voice))
            p.stdin.write(img.tobytes())
    p.stdin.close()
    p.wait()
    os.remove(wav_path)
    return sum(durs)
