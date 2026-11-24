#!/usr/bin/env bash
# 書き出した動画の点検（納品前に必ず）：bash side/pachi3d/tools/qc.sh <動画.mp4> [出力フォルダ]
# 長さ・解像度・fps／音量（−14 LUFS±1・ピーク −1 dBTP 以下）／真っ黒なコマ／コマ一覧を少しずらして2回分
set -euo pipefail
IN="${1:?動画のパスを指定}"; OUT="${2:-$(dirname "$IN")/qc}"; mkdir -p "$OUT"
echo "== 長さ・解像度・fps"
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -show_entries format=duration -of default=nw=1 "$IN"
echo "== 音量（目標 I=-14±1 LUFS、Peak <= -1 dBTP）"
ffmpeg -hide_banner -nostats -i "$IN" -af ebur128=peak=true -f null - 2>&1 | awk '/Summary:/{f=1} f' | grep -E "I:|Peak:|LRA:" || true
echo "== 真っ黒なコマ（0.1秒以上）"
B=$(ffmpeg -hide_banner -nostats -i "$IN" -vf blackdetect=d=0.1:pix_th=0.05 -an -f null - 2>&1 | grep -c black_start || true)
echo "黒い区間: ${B} か所"
echo "== コマ一覧（2秒ごと、0秒始まりと1秒ずらしの2枚）"
ffmpeg -hide_banner -loglevel error -y -i "$IN" -vf "fps=1/2,scale=216:-1,tile=10x10" -frames:v 1 "$OUT/sheet_a.jpg"
ffmpeg -hide_banner -loglevel error -y -ss 1 -i "$IN" -vf "fps=1/2,scale=216:-1,tile=10x10" -frames:v 1 "$OUT/sheet_b.jpg"
echo "→ $OUT/sheet_a.jpg と $OUT/sheet_b.jpg を両方見る"
