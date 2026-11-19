# オーナーPCで動画を書き出す（GPUで速く）

PCのClaudeデスクトップアプリ →「Code」→ 作業フォルダに「ドキュメント」を選び、下の文を貼って送る。
途中の「実行していいですか？」は許可する。

```
動画の書き出しをこのPCのGPUでやって。
1. Node.js（LTS）とGitが入っていなければ入れて（Windowsは winget、Macは brew）
2. ドキュメントに https://github.com/zaq-master/ai-lab を clone（すでにあれば git pull）
3. side/sim1min で `npx --yes hyperframes@0.9.64 render -o renders/pc.mp4 -q looks` を実行して、かかった時間を教えて
   ・音のファイル assets/mix.wav が無いのは正常（曲の権利のためGitHubに置いていない。音はクラウド側で入れる）。それでエラーになるなら index.html の <audio> の行を一時的に消して書き出して
4. できた renders/pc.mp4 をエクスプローラー（Finder）で開いて場所を見せて
```

できた pc.mp4 は、Claudeアプリのクラウドの会話にファイルとして添付する（クラウド側で声とBGMを入れて仕上げる）。
