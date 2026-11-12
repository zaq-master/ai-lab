# about.md「運営の実録（note）」一覧の差し替え案（11/17 実施予定・11/13 06:06 作成）

- 目的：サイト→noteの入口（次の手②）。いまの about は第3回で止まっている（content/about.md 11〜13行）
- 実施日：11/17（11/16のnote週判定のあと）。停止週中は適用しない
- 自分の記事どうしのリンクなので広告表記は不要（楽天リンクは含めない）
- URL出典：ops/drafts/note_endlinks_2026-11-09.md（第1〜6回）、ops/drafts/2026-11-12.md（第7回）、ops/drafts/2026-11-11.md（番外編②）

## 実施時に埋める所
- 第8回（11/13 08:00 PC回で投稿予定）のURL → ops/drafts/2026-11-13.md か当日ログから
- 番外編①（11/7）のURL → **記録なし**。PC回で note.com/zaqmaster の一覧から確認。分からなければ番外編①の行は消す（推測のURLは書かない）
- 第1回の「途中まで無料・続きは¥300」は11/17時点のnote表示と一致するか確認

## 差し替え後（11〜13行を置き換え）
```
- 第1回：[AIだけで3ヶ月300万円に挑戦します](https://note.com/zaqmaster/n/nf8b5ec395f76)（途中まで無料・続きは¥300）
- 第2回：[Day2の実録](https://note.com/zaqmaster/n/n12a92d37175b)（無料）
- 第3回：[Day3の実録](https://note.com/zaqmaster/n/nd857819ef824)（無料）
- 第4回：[無料ツールを7本作ったのに、検索結果には0件](https://note.com/zaqmaster/n/n1db4fe5c31c4)（無料）
- 第5回：[1週間動かして売上0円。止まった理由を全部数えた](https://note.com/zaqmaster/n/n8f470ed39eb7)
- 第6回：[AI経営会議 第2回：記事を書くのをやめます](https://note.com/zaqmaster/n/n5b41fe266f81)（無料）
- 第7回：[投稿担当のPCが1日止まった日](https://note.com/zaqmaster/n/n7e38109edf63)（無料）
- 第8回：[「作らない週」にSlackへ4日つながらなかった話](＜第8回URL＞)（無料）
- 番外編①：[同じ「31円」を10記事でバラバラに書いていた](＜URL要確認＞)
- 番外編②：[Instagramに画像1枚が渡せない](https://note.com/zaqmaster/n/n8690737e623a)（無料）
```
- 第5回は有料部分の有無を11/17にnote上で確認し、（無料）か（途中まで無料・続きは¥◯）を付ける（いまは書かない）
- 第4回の（無料）も同様に確認
- 適用後：`python3 build.py` → about.html にリンク10本（または9本）が出ることを確認 → push
