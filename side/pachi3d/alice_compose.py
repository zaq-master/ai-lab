"""Canvaで作ったアリス3枚（ふつう・話す・まばたき）から、動画用の表情パーツを作る。

3枚は髪や服が少しずつ違うので、そのまま差し替えると体がピクピク動く。
そこで「ふつう」を土台にし、顔の位置を合わせたうえで、口（話す）と目（まばたき）の部分だけを
ぼかした境目で貼り合わせる。白い背景は透明にする。
出力：assets/alice_hq/{base,talk,blink}.png（同じ大きさ・同じ位置）
"""
import os

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "assets", "src")
OUT = os.path.join(HERE, "assets", "alice_hq")

FACE = (518, 330, 1018, 890)          # 顔のあたり（x0, y0, x1, y1）
EYES = (560, 472, 976, 592)           # 目の帯
MOUTH = (668, 630, 868, 760)          # 口のまわり


def load(n):
    return cv2.imread(os.path.join(SRC, f"alice_{n}_export.png"), cv2.IMREAD_COLOR)


def align(base, img, skip=None):
    """顔のあたりだけで、ずれ（拡大・回転・移動）を合わせる。skip（表情が違う部分）は使わない。"""
    x0, y0, x1, y1 = FACE
    a = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY).astype(np.float32)
    b = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    mask = np.zeros_like(a, np.uint8)
    mask[y0:y1, x0:x1] = 255
    if skip:
        sx0, sy0, sx1, sy1 = skip
        mask[sy0:sy1, sx0:sx1] = 0
    warp = np.eye(2, 3, dtype=np.float32)
    crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 300, 1e-6)
    _, warp = cv2.findTransformECC(cv2.GaussianBlur(a, (0, 0), 2), cv2.GaussianBlur(b, (0, 0), 2), warp,
                                   cv2.MOTION_AFFINE, crit, mask, 5)
    h, w = base.shape[:2]
    return cv2.warpAffine(img, warp, (w, h), flags=cv2.INTER_CUBIC + cv2.WARP_INVERSE_MAP,
                          borderMode=cv2.BORDER_REPLICATE), warp


def feather(shape, box, blur=25):
    m = np.zeros(shape[:2], np.float32)
    x0, y0, x1, y1 = box
    cv2.ellipse(m, ((x0 + x1) // 2, (y0 + y1) // 2), ((x1 - x0) // 2, (y1 - y0) // 2), 0, 0, 360, 1, -1)
    return cv2.GaussianBlur(m, (0, 0), blur)[..., None]


def cutout(img):
    """白い背景を透明に（外側からつながった白だけを消す。目の白目などは残す）。"""
    h, w = img.shape[:2]
    white = (img.min(axis=2) > 238).astype(np.uint8)
    ff = white.copy()
    mask = np.zeros((h + 2, w + 2), np.uint8)
    for seed in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        if ff[seed[1], seed[0]]:
            cv2.floodFill(ff, mask, seed, 2)
    bg = (ff == 2).astype(np.float32)
    alpha = 1 - cv2.GaussianBlur(bg, (0, 0), 1.2)
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    rgba[..., 3] = np.clip(alpha * 255, 0, 255).astype(np.uint8)
    return rgba


def main():
    os.makedirs(OUT, exist_ok=True)
    base = load("base")
    talk, wt = align(base, load("talk"), MOUTH)
    blink, wb = align(base, load("blink"), (500, 420, 1040, 620))
    print("talk warp", np.round(wt, 3).tolist())
    print("blink warp", np.round(wb, 3).tolist())
    b = base.astype(np.float32)
    mt = feather(base.shape, MOUTH, 18)
    me = feather(base.shape, EYES, 14)
    out_talk = b * (1 - mt) + talk.astype(np.float32) * mt
    out_blink = b * (1 - me) + blink.astype(np.float32) * me
    for name, im in [("base", base), ("talk", out_talk.astype(np.uint8)), ("blink", out_blink.astype(np.uint8))]:
        cv2.imwrite(os.path.join(OUT, f"{name}.png"), cutout(im))
    print("ok")


if __name__ == "__main__":
    main()
