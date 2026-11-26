# YouTubeショートの投稿手順（PC回：02:00・08:00）

> **2026-11-26 停止**：オーナー指示「動画は手動でYouTubeにアップする」。AIはこの手順を実行しない（記録として残す）。


オーナー決定（2026-11-18）：PCの内蔵ブラウザから投稿・**毎日18:00に予約公開**・チャンネル「トガ feat. 電脳アリス」（@toga_alice）
投稿待ちの一覧：`side/pachi3d/upload_queue.md`（上から1本ずつ）

## 1回の作業（約5分・1日1本まで）
1. built-in-browser スキルを読む。内蔵ブラウザに届かなければ「PCオフで未投稿」と報告して終了
2. https://studio.youtube.com を開き、右上が @toga_alice か確認（違えばアカウント切替。ログインが切れていたら作業せず、オーナーに再ログインを依頼）
3. 「作成」→「動画をアップロード」
4. ファイルの入れ方（PCに動画が無いので、公開URLから読み込む）：ページ上で次のJSを実行してファイル欄に入れる
   ```js
   const r = await fetch("<動画のURL>"); const b = await r.blob();
   const f = new File([b], "short.mp4", { type: "video/mp4" });
   const inp = document.querySelector('input[type=file]'); const dt = new DataTransfer(); dt.items.add(f);
   inp.files = dt.files; inp.dispatchEvent(new Event("change", { bubbles: true }));
   ```
   （fetchが失敗する場合は、動画URLを新しいタブで開いて保存→ファイル選択から入れる）
5. 詳細：タイトル・説明欄は queue の description.txt をそのまま。「いいえ、子ども向けではありません」
6. 「改変または合成されたコンテンツ」＝**はい**（AIで作ったため）
7. サムネ：ショートでサムネ欄が出れば thumb.png を同じ方法で入れる（出なければ飛ばす）
8. 公開設定：「スケジュール」→ **その日の18:00**（18:00を過ぎていたら翌日18:00）
9. 予約が終わったら、動画のURL（https://youtube.com/shorts/…）を upload_queue.md の該当行に書き、状態を「予約済み 11/◯ 18:00」に。ops/vocalo/x_queue.md の同じ動画の「【動画URL】」も置き換える
10. Xの告知は公開後（18:00以降の回）に投稿する

## 失敗したとき
- 2回まで同じ手順をやり直す。だめなら状態に「失敗：理由」と書き、オーナーに報告
- 画面の文言が変わっていて分からないときは、無理に押さず報告

## 守ること
- 1日1本まで（毎日の新作を優先）。同じ動画を2回上げない（upload_queue.md の状態を必ず見る）
- 説明欄の「AI制作」「必勝法ではありません」「18歳未満は遊技できません」を消さない
