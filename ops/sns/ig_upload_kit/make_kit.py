#!/usr/bin/env python3
"""IG受け渡しキット生成：PNG→1080x1350 JPEG（約150KB以下）→base64→約40,000文字ごとのチャンク。
使い方: python3 ops/sns/ig_upload_kit/make_kit.py docs/sns/ig/2026-11-05_marathon [...]
出力: ops/sns/ig_upload_kit/<フォルダ名>/NN.jpg, NN_partK.txt, manifest.json（ネットワーク不使用）"""
import base64, io, json, sys, os
from PIL import Image

KIT = os.path.dirname(os.path.abspath(__file__))
TARGET = 150 * 1024
CHUNK = 40000

def to_jpeg(path):
    im = Image.open(path).convert("RGB")
    if im.size != (1080, 1350):
        im = im.resize((1080, 1350), Image.LANCZOS)
    best = None
    for q in range(92, 59, -2):  # 品質を下げすぎると文字がにじむので下限60
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=q, optimize=True, progressive=False, subsampling=0 if q >= 85 else 2)
        best = (q, buf.getvalue())
        if len(best[1]) <= TARGET:
            break
    return best

def main(dirs):
    for d in dirs:
        name = os.path.basename(os.path.normpath(d))
        out = os.path.join(KIT, name); os.makedirs(out, exist_ok=True)
        for f in os.listdir(out):
            if f.endswith(".txt") or f.endswith(".jpg"):
                os.remove(os.path.join(out, f))
        files = []
        for png in sorted(p for p in os.listdir(d) if p.endswith(".png")):
            nn = png[:-4]
            q, data = to_jpeg(os.path.join(d, png))
            open(os.path.join(out, nn + ".jpg"), "wb").write(data)
            b64 = base64.b64encode(data).decode()
            parts = [b64[i:i+CHUNK] for i in range(0, len(b64), CHUNK)]
            for k, p in enumerate(parts, 1):
                open(os.path.join(out, f"{nn}_part{k}.txt"), "w").write(p)
            files.append({"nn": nn, "name": nn + ".jpg", "quality": q, "bytes": len(data),
                          "b64_len": len(b64), "parts": len(parts)})
            print(f"{name}/{nn}: q={q} {len(data)/1024:.1f}KB parts={len(parts)}")
        json.dump({"folder": name, "width": 1080, "height": 1350, "chunk": CHUNK, "files": files},
                  open(os.path.join(out, "manifest.json"), "w"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main(sys.argv[1:] or ["docs/sns/ig/2026-11-05_marathon", "docs/sns/ig/2026-11-04_smart-remote"])
