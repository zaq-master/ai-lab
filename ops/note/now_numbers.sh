#!/bin/sh
# note原稿の【差替】欄に入れる「今の数字」を出す（投稿するPC回の最初に実行）
# 使い方: sh ops/note/now_numbers.sh
cd "$(dirname "$0")/../.." || exit 1
echo "日時（JST）: $(TZ=Asia/Tokyo date '+%-m月%-d日 %H:%M')"
echo "運営日数: $(( ( $(date +%s) - $(TZ=Asia/Tokyo date -d 2026-11-02 +%s) ) / 86400 + 1 ))日目"
echo "サイトの記事: $(ls content/posts/*.md | wc -l)本"
echo "楽天ボタン（サイト全体）: $(cat docs/posts/*.html | grep -o 'af.moshimo.com' | wc -l)個"
echo "BFメモ記事のボタン: $(grep -o 'af.moshimo.com' docs/posts/rakuten-blackfriday-memo.html | wc -l)個"
echo "BF終了まで: 11月25日(水) 1:59（これを過ぎたら番外編③は出さない）"
