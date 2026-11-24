#!/usr/bin/env bash
# 映像に音を合体し、音量を YouTube 基準（−14 LUFS、ピーク −1 dBTP 以下）に2回に分けて合わせる
# 使い方：bash side/pachi3d/tools/loudnorm.sh <映像.mp4> <音声.wav> <出力.mp4>
set -euo pipefail
V="${1:?映像}"; A="${2:?音声}"; O="${3:?出力}"
J=$(ffmpeg -hide_banner -nostats -i "$A" -af loudnorm=I=-14:TP=-1.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g() { echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
F="loudnorm=I=-14:TP=-1.2:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true"
# AAC にするとピークが上がることがあるので、最後に4倍の細かさで上限をかける
ffmpeg -hide_banner -loglevel error -y -i "$V" -i "$A" -map 0:v -map 1:a -c:v libx264 -crf 20 -preset slow \
  -af "$F,aresample=192000,alimiter=limit=0.83:level=false,aresample=48000" -c:a aac -b:a 192k -shortest -movflags +faststart "$O"
ffmpeg -hide_banner -nostats -i "$O" -af ebur128=peak=true -f null - 2>&1 | awk '/Summary:/{f=1} f' | grep -E "I:|Peak:" || true
