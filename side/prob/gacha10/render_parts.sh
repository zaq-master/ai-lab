#!/bin/bash
# 10分を約2分ごとに分けて順番に書き出す（終わった分は飛ばす）。最後に ffmpeg でつなぐ。
cd "$(dirname "$0")"; mkdir -p renders
B=(0 122 244 366 488 END)
for i in 0 1 2 3 4; do
  o=renders/p$i.mp4; [ -f "$o.ok" ] && continue
  s=${B[$i]}; e=${B[$((i+1))]}
  if [ "$e" = END ]; then E=""; else E="--end $e"; fi
  echo "== part $i $s-$e $(date +%T)" >> renders/parts.log
  npx --yes hyperframes@0.9.64 render --start $s $E -o $o -q looks --skill hyperframes > renders/p$i.log 2>&1 && touch $o.ok
  echo "   exit $? $(date +%T)" >> renders/parts.log
done
ls renders/p{0,1,2,3,4}.mp4.ok >/dev/null 2>&1 || { echo "未完了あり" >> renders/parts.log; exit 1; }
for i in 0 1 2 3 4; do echo "file 'p$i.mp4'"; done > renders/list.txt
ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i renders/list.txt -c copy renders/joined.mp4 && echo "joined $(date +%T)" >> renders/parts.log
