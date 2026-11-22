"""完成した動画を採点するための材料を作る（品質審査担当ミルが使う）。

やること（無料・端末の中だけ：ffmpeg と PIL）
1. 機械で測れる所を測る：長さ・画面の大きさ・音の大きさ（LUFS）・音の最大値・無音の区間・画面が止まった区間・場面の切り替わりの数・真っ黒な区間
2. 一定の間隔で画面を切り出して、1枚の一覧画像（コンタクトシート）にする → ミルが Read で見て、見やすさ・豪華さを採点する
3. 機械の決まりに引っかかった所（必ず直す所）を一覧にする

使い方：
    python3 side/pachi3d/video_review.py media/videos/sim/<フォルダ>/short.mp4 [--out <フォルダ>] [--every 5]
出力（--out。標準は動画と同じフォルダの review/）：
    metrics.json … 測った数字と、引っかかった決まり
    sheet_1.png … 画面の一覧（1枚に 4列×5行＝20コマ。足りなければ sheet_2.png …）
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# 機械の決まり（引っかかったら、点数に関係なく直す）
RULES = {
    "lufs_min": -17.0,        # YouTube は約 -14 LUFS にそろえる（大きい音は下げるが、小さい音は上げない）。小さすぎると聞こえにくい
    "lufs_max": -11.0,        # 大きすぎると YouTube に下げられ、音が割れやすい
    "true_peak_max": -1.0,    # 音の最大値（dBTP）。これより大きいと割れやすい
    "silence_max_sec": 2.5,   # 途中で、これより長い無音があってはいけない（最初と最後の1秒はのぞく）
    "freeze_max_sec": 4.0,    # 画面が、これより長く止まって見えてはいけない
    "black_max_sec": 1.0,     # 真っ黒な画面が、これより長く続いてはいけない
    "scenes_per_min_min": 4,  # 1分あたりの場面の切り替わりが、これより少ないと単調
}
FONT_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
]


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def probe(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate", "-of", "json", str(path)])
    data = json.loads(out.stdout or "{}")
    video = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
    has_audio = any(s.get("codec_type") == "audio" for s in data.get("streams", []))
    return {
        "duration": float(data.get("format", {}).get("duration", 0)),
        "width": video.get("width"),
        "height": video.get("height"),
        "fps": video.get("r_frame_rate"),
        "has_audio": has_audio,
    }


def loudness(path):
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
    summary = err[err.rfind("Summary:"):] if "Summary:" in err else err
    lufs = re.search(r"I:\s+(-?[\d.]+) LUFS", summary)
    peak = re.search(r"Peak:\s+(-?[\d.]+) dBFS", summary)
    return (float(lufs.group(1)) if lufs else None, float(peak.group(1)) if peak else None)


def ranges(stderr, start_key, end_key):
    starts = [float(x) for x in re.findall(start_key + r"\s*:?\s*(-?[\d.]+)", stderr)]
    ends = [float(x) for x in re.findall(end_key + r"\s*:?\s*(-?[\d.]+)", stderr)]
    return [(s, e) for s, e in zip(starts, ends)]


def silences(path):
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "silencedetect=noise=-45dB:d=1.0", "-f", "null", "-"]).stderr
    return ranges(err, "silence_start", "silence_end")


def freezes(path):
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-vf", "freezedetect=n=0.003:d=2", "-an", "-f", "null", "-"]).stderr
    return ranges(err, "lavfi.freezedetect.freeze_start", "lavfi.freezedetect.freeze_end")


def blacks(path):
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-vf", "blackdetect=d=0.5:pix_th=0.08", "-an", "-f", "null", "-"]).stderr
    return [(float(a), float(b)) for a, b in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", err)]


def scene_changes(path):
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-vf", "select='gt(scene,0.3)',showinfo", "-an", "-f", "null", "-"]).stderr
    return [float(x) for x in re.findall(r"pts_time:([\d.]+)", err)]


def font(size):
    for candidate in FONT_CANDIDATES:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def contact_sheets(path, out_dir, duration, every, cols=4, rows=5):
    frames_dir = out_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    times = [round(t, 2) for t in frange(0.5, max(duration - 0.3, 0.6), every)]
    thumbs = []
    for t in times:
        frame = frames_dir / f"f_{t:07.2f}.png"
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(t), "-i", str(path), "-frames:v", "1", "-vf", "scale=360:-2", str(frame)])
        if frame.exists():
            thumbs.append((t, Image.open(frame).convert("RGB")))
    sheets = []
    per = cols * rows
    label_font = font(22)
    for index in range(0, len(thumbs), per):
        chunk = thumbs[index:index + per]
        w, h = chunk[0][1].size
        sheet = Image.new("RGB", (cols * w, rows * (h + 30)), "white")
        draw = ImageDraw.Draw(sheet)
        for i, (t, img) in enumerate(chunk):
            x, y = (i % cols) * w, (i // cols) * (h + 30)
            sheet.paste(img, (x, y + 30))
            draw.text((x + 6, y + 2), f"{int(t // 60)}:{t % 60:05.2f}", fill="black", font=label_font)
        name = out_dir / f"sheet_{index // per + 1}.png"
        sheet.save(name)
        sheets.append(str(name))
    return sheets


def frange(start, stop, step):
    t = start
    while t < stop:
        yield t
        t += step


def review(path, out_dir, every):
    info = probe(path)
    duration = info["duration"]
    lufs, peak = loudness(path) if info["has_audio"] else (None, None)
    silent = [(s, e) for s, e in silences(path) if s > 1.0 and e < duration - 1.0] if info["has_audio"] else []
    frozen = freezes(path)
    black = blacks(path)
    scenes = scene_changes(path)
    per_min = len(scenes) / (duration / 60) if duration else 0
    problems = []
    if not info["has_audio"]:
        problems.append("音が入っていません")
    if lufs is not None and not (RULES["lufs_min"] <= lufs <= RULES["lufs_max"]):
        problems.append(f"音の大きさが {lufs:.1f} LUFS（{RULES['lufs_min']}〜{RULES['lufs_max']} にする。目安は -14）")
    if peak is not None and peak > RULES["true_peak_max"]:
        problems.append(f"音の最大値が {peak:.1f} dB（{RULES['true_peak_max']} 以下にしないと割れやすい）")
    for s, e in silent:
        if e - s > RULES["silence_max_sec"]:
            problems.append(f"{s:.1f}〜{e:.1f}秒が無音（{e - s:.1f}秒）")
    for s, e in frozen:
        if e - s > RULES["freeze_max_sec"]:
            problems.append(f"{s:.1f}〜{e:.1f}秒、画面が止まって見える（{e - s:.1f}秒）")
    for s, e in black:
        if e - s > RULES["black_max_sec"]:
            problems.append(f"{s:.1f}〜{e:.1f}秒が真っ黒")
    if per_min < RULES["scenes_per_min_min"]:
        problems.append(f"場面の切り替わりが1分あたり {per_min:.1f} 回（{RULES['scenes_per_min_min']} 回より少なく、単調に見えやすい）")
    out_dir.mkdir(parents=True, exist_ok=True)
    sheets = contact_sheets(path, out_dir, duration, every)
    metrics = {
        "video": str(path),
        **info,
        "lufs": lufs,
        "true_peak": peak,
        "silences": silent,
        "freezes": frozen,
        "blacks": black,
        "scene_changes": len(scenes),
        "scene_changes_per_min": round(per_min, 1),
        "rules": RULES,
        "problems": problems,
        "sheets": sheets,
        "sheet_every_sec": every,
    }
    (out_dir / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    return metrics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--out")
    parser.add_argument("--every", type=float, default=None, help="何秒ごとに画面を切り出すか（標準：ショート3秒・ロング15秒）")
    args = parser.parse_args()
    path = Path(args.video)
    if not path.exists():
        sys.exit(f"動画が見つかりません：{path}")
    out_dir = Path(args.out) if args.out else path.parent / "review"
    every = args.every
    if every is None:
        every = 3.0 if probe(path)["duration"] <= 180 else 15.0
    m = review(path, out_dir, every)
    print(f"長さ {m['duration']:.1f}秒／{m['width']}x{m['height']}／音 {m['lufs']} LUFS・最大 {m['true_peak']} dB／場面の切り替わり {m['scene_changes']}回（1分あたり {m['scene_changes_per_min']}）")
    print("機械の決まりに引っかかった所：" + ("なし" if not m["problems"] else ""))
    for p in m["problems"]:
        print(f"  ✖ {p}")
    print("画面の一覧：" + "、".join(m["sheets"]))


if __name__ == "__main__":
    main()
