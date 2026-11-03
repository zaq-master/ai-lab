# スマホ表示チェック 2026-11-04（カルク）

## やり方
- Playwright（Chromium）の `devices['iPhone 13']`（画面幅390px）で docs/ の公開ページ23枚（index・about・posts 20本・apps/sub-check）をローカルファイルとして開いて自動計測
- 数えたもの：①ページ全体の横スクロール ②表が親より広くて列が隠れている（scrollWidth > clientWidth、または画面の右端をはみ出す） ③ボタン・入力欄が画面の外にはみ出す
- 念のためPC幅（1200px）でも同じ計測をして、悪化がないことを確認

## 結果（問題のあるページ数）
| | 前 | 後 |
|---|---|---|
| iPhone 13（390px） | **16 / 23** | **0 / 23** |
| PC（1200px） | 9 / 23 | 0 / 23 |

①ページ全体の横スクロールは前後とも0件（表は前から表の中だけでスクロールしていた）。問題は「表の右の列がスマホで見えない」こと。

## ページ別（iPhone 13：前 → 後）
| ページ | 前 | 後 |
|---|---|---|
| index.html | OK | OK |
| about.html | OK | OK |
| posts/aircon-danbou-denkidai-calculator.html | OK | OK |
| posts/denki-moufu-kotatsu-denkidai-telework.html | 表3個（最大1109px隠れ） | OK |
| posts/denkidai-calculator.html | 表1個（右144px隠れ）、削除ボタン「×」2個が画面外 | OK |
| posts/desk-qol-guide.html | OK | OK |
| posts/foot-heater-electricity-cost.html | 表2個（最大691px隠れ） | OK |
| posts/fuyu-denkidai-matome.html | 表1個（251px隠れ） | OK |
| posts/heater-denkidai-hikaku.html | 表1個（669px隠れ） | OK |
| posts/hot-carpet-denkidai.html | 表3個（最大571px隠れ） | OK |
| posts/humidifier-electricity-cost-telework.html | 表2個（最大846px隠れ） | OK |
| posts/kashitsu-ryo-calculator.html | OK | OK |
| posts/monitor-light-guide.html | 表1個（238px隠れ） | OK |
| posts/rakuten-marathon-fuyu-kaden-list.html | 表2個（最大707px隠れ） | OK |
| posts/rakuten-marathon-point-calculator.html | 表2個（最大707px隠れ） | OK |
| posts/smart-plug-guide.html | 表1個（324px隠れ） | OK |
| posts/smart-remote-count-shindan.html | 表1個（355px隠れ） | OK |
| posts/smart-remote-guide.html | 表2個（最大369px隠れ） | OK |
| posts/smart-remote-rental-two-aircon.html | 表1個（675px隠れ） | OK |
| posts/telework-ketsuro-taisaku-roten.html | 表3個（最大359px隠れ） | OK |
| posts/usb-c-charger-guide.html | OK | OK |
| posts/winter-heating-shindan.html | 表1個（624px隠れ） | OK |
| apps/sub-check/index.html | OK | OK |

## 原因
共通CSS（templates/base.html）で表のセルが全部 `white-space:nowrap`（折り返し禁止）だったため、長い文章のセルが1行に伸びて表が画面の何倍にも広がっていた。

## 直したこと（記事の文章・数字は変更なし）
1. **templates/base.html（共通CSS）**
   - セルの折り返しを許可（`white-space:normal`、`line-break:strict`）
   - スマホ幅（600px以下）：セルの文字を .82rem・余白 6px 4px に、記事枠の左右余白 20px→12px
   - 表がまだ広いときに「横にスクロールできる」と分かる左右の影（背景グラデーション。広くない表には出ない）。色付きの計算ツール枠（`style="background:#…"` の中）の表には影を付けない
   - `td.nw` は折り返さない（スマホでは1列目だけ折り返し可）
2. **build.py**：表のセルのうち「数字を含む10文字以内」（例：約4.2°C、約1,587円）に `class="nw"` を自動で付ける。「約 / 4.2°C」のような途中改行を防ぐため（関数 `short_cell`）
3. **content/posts/denkidai-calculator.md**：電気代計算ツールだけ、スマホ幅では1家電＝1枚のカード表示（名前＋×／消費電力・時間／1日・1ヶ月）にするスコープ付きCSSを追加。PC幅の見た目は従来どおり。削除ボタンの動作も確認済み

## 確認
- `python3 build.py`：OK（built 20 posts）
- `python3 ops/tests/site_health.py`：公開ページ23／問題0件
- `node ops/tests/*.test.js`（aircon_calc／sub_check_dates／sub_check_sheet）：すべてOK
- 悪化チェック：楽天マラソン計算ツールのショップ名入力欄の幅 56px → 71px（広がった）。PC幅の表の隠れも 9ページ → 0
- スクショ：scratchpad の shots_before/（直す前の問題ページ）、tbl_*.png・calc_after.png・calc_desktop.png（直した後）

## 次の一手
新しい記事を出すたびに同じ計測（mcheck.py 相当）を ops/tests/ に入れて自動チェックにする。
