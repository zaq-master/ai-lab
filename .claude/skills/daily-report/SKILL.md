---
name: daily-report
description: 21:00の日報回で数字を集めて ops/metrics.csv に記録し、Slackに日報を出す手順。17:00の分析回でも数字集めに使う。
---
# 日報の型

## 数字集め（ブラウザ不要のものだけ）
- 記事数：`ls content/posts | wc -l`
- 売上：Stripe（読み取り、acct_1SRwxtFamAPaDCXY、livemode=true）の当日 charges の合計
- note・X・IG・もしもの数字は、直近のPC回のログ（ops/log）に書かれた値を使う。なければ空欄にし「未計測」と書く。推測で埋めない
- インデックス状況：WebSearch で `site:zaq-master.github.io/ai-lab` の件数

## 記録
ops/metrics.csv に1行追記（列：date,posts_site,posts_note,posts_x,posts_ig,followers_x,followers_ig,followers_note,sales_jpy,sales_total_jpy）
  - 2026-11-06〜 後ろに15列追加（site_index_seen〜measured_at、意味は ops/strategy/judge_2026-11-16_v2.md 3節）。**空欄＝未計測、0＝測って0**。PC回の値は当日の ops/drafts/YYYY-MM-DD.md の「数字」欄から写す。stripe_charges は日報回が毎日入れる

## 分析（3行で）
- 昨日比で何が動いたか
- 売上を一番止めているボトルネックは何か（1つだけ）
- 明日それを動かす作業は何か → ops/backlog.md の1位に入れる

## 画像
`python3 ops/report_card.py daily` → `python3 ops/slack_post.py ceo "<日報本文>" --image ops/out/daily.png`（トークンの取り方は CLAUDE.md の Slack報告のルール）

## Slack投稿（#daily-report C0CDF2L2N2K、電脳アリスとして）
CLAUDE.md の日報フォーマットどおり。オーナーへの依頼は「何を・なぜ・何分で」を1行。依頼が前日と同じなら「（継続）」と付ける
