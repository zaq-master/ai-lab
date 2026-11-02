"""冬の光熱費トラッカー (.xlsx) を生成する。
数式は Excel / Googleスプレッドシート / LibreOffice で共通に動く関数だけを使う
（IF, OR, AND, SUM, SUMIFS, COUNTIFS, EDATE, ROUND, ISNUMBER, IFERROR）。
実行: python3 build_xlsx.py
"""
from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

OUT = Path(__file__).with_name("winter-utility-tracker.xlsx")
MONTHS = 36          # 3年分
FIRST = 6            # 月次記録のデータ開始行
LAST = FIRST + MONTHS - 1
APP_ROWS = 15        # 暖房器具の行数
APP_FIRST = 6
APP_LAST = APP_FIRST + APP_ROWS - 1

FONT = "Meiryo"
NAVY = "1F3A5F"
TEAL = "2A9D8F"
WARM = "E76F51"
LIGHT = "EEF4F8"
INPUT_FILL = PatternFill("solid", fgColor="FFFDF0")
HEAD_FILL = PatternFill("solid", fgColor=NAVY)
CALC_FILL = PatternFill("solid", fgColor=LIGHT)
thin = Side(style="thin", color="C9D3DD")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
YEN = '#,##0;-#,##0;"-"'
PCT = '+0.0%;-0.0%;0.0%'

# ---- 架空のサンプル（実在の世帯・請求額ではありません） ----
# (電気kWh, 電気料金, ガスm3, ガス料金, 灯油L, 灯油代) 2024/11〜2026/10 の24か月
SAMPLE = [
    (310, 10200, 28, 5400, 18, 2300), (420, 13600, 36, 6800, 36, 4600),
    (480, 15500, 41, 7600, 54, 6900), (450, 14600, 39, 7300, 36, 4600),
    (360, 11800, 32, 6200, 18, 2300), (280, 9100, 25, 5000, 0, 0),
    (240, 7900, 20, 4300, 0, 0), (250, 8200, 16, 3700, 0, 0),
    (330, 10600, 12, 3100, 0, 0), (390, 12400, 11, 3000, 0, 0),
    (300, 9700, 13, 3300, 0, 0), (250, 8100, 18, 4000, 0, 0),
    (300, 9600, 27, 5300, 18, 2200), (400, 12700, 34, 6500, 36, 4500),
    (440, 14000, 38, 7100, 36, 4500), (430, 13700, 37, 6900, 36, 4500),
    (350, 11200, 30, 5900, 18, 2200), (270, 8700, 24, 4800, 0, 0),
    (230, 7500, 19, 4100, 0, 0), (240, 7800, 15, 3500, 0, 0),
    (340, 10900, 12, 3100, 0, 0), (400, 12800, 11, 3000, 0, 0),
    (310, 9900, 13, 3300, 0, 0), (250, 8100, 17, 3800, 0, 0),
]
# 暖房器具（架空の例。消費電力は自分の製品の銘板・取扱説明書の値に置き換える）
APPLIANCES = [
    ("エアコン（暖房・例）", 600, 8, 30, "消費電力は運転状況で大きく変わる。目安として使う"),
    ("セラミックヒーター（例）", 1200, 2, 30, "強運転の例"),
    ("こたつ（例）", 300, 4, 30, "温度調節で実際の消費は下がる"),
    ("電気毛布（例）", 50, 7, 30, ""),
    ("ホットカーペット 2畳（例）", 500, 4, 30, ""),
    ("オイルヒーター（例）", 1200, 6, 30, ""),
]


def style_header(ws, row, ncols, height=34, start=1):
    for c in range(start, start + ncols):
        cell = ws.cell(row=row, column=c)
        cell.font = Font(name=FONT, bold=True, color="FFFFFF", size=10)
        cell.fill = HEAD_FILL
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER
    ws.row_dimensions[row].height = height


def title(ws, text, sub):
    ws["A1"] = text
    ws["A1"].font = Font(name=FONT, bold=True, size=16, color=NAVY)
    ws["A2"] = sub
    ws["A2"].font = Font(name=FONT, size=9, color="5B6B7B")
    ws.row_dimensions[1].height = 26


def inp(cell, fmt=None):
    cell.fill = INPUT_FILL
    cell.border = BORDER
    cell.font = Font(name=FONT, size=11, bold=True)
    if fmt:
        cell.number_format = fmt


wb = Workbook()

# ================= 設定 =================
st = wb.active
st.title = "設定"
title(st, "設定", "黄色のセルを自分の契約・地域に合わせて変えてください。")
rows = [
    ("電気料金の単価（円/kWh）", 31, "円/kWh", "0.0"),
    ("今冬の開始月（この月の1日を入力）", date(2025, 11, 1), "", "yyyy/mm"),
    ("冬の月数（例：11月〜3月なら5）", 5, "か月", "0"),
    ("暖房器具シートの「1か月の日数」の初期値", 30, "日", "0"),
]
for i, (label, val, unit, fmt) in enumerate(rows):
    r = 4 + i
    st[f"A{r}"], st[f"B{r}"], st[f"C{r}"] = label, val, unit
    st[f"A{r}"].font = Font(name=FONT, size=10)
    inp(st[f"B{r}"], fmt)
st["A9"] = ("※ 31円/kWh の出典：全国家庭電気製品公正取引協議会「新電気料金目安単価」（2022年7月改定・税込）。"
            "家電カタログの電気代表示に使われる目安の値で、実際の単価は契約・燃料費調整額・再エネ賦課金・補助金で変わります。")
st["A10"] = "　より正確にしたい場合は、検針票・Webの明細の「電気料金 ÷ 使用量（kWh）」の値を入れてください（「月次記録」シートのN列に毎月の実績単価が出ます）。"
for r in (9, 10):
    st[f"A{r}"].font = Font(name=FONT, size=9, color="5B6B7B")
st.column_dimensions["A"].width = 46
st.column_dimensions["B"].width = 12
st.column_dimensions["C"].width = 8

UNIT = "設定!$B$4"
WSTART = "設定!$B$5"
WLEN = "設定!$B$6"

# ================= 月次記録 =================
ws = wb.create_sheet("月次記録", 0)
title(ws, "月次記録（電気・ガス・灯油）",
      "黄色のセルに検針票・明細の数字を入れるだけ。灰色は自動計算。入っている数字はすべて架空のサンプルです。")
ws["A3"] = "※ 年月はA6に最初の月（1日）を入れると、下は自動で1か月ずつ進みます。前年同月の比較は、12か月前の行に数字があるときに出ます。"
ws["A3"].font = Font(name=FONT, size=9, color=TEAL)

groups = [("A4:A4", ""), ("B4:C4", "電気"), ("D4:E4", "ガス"), ("F4:G4", "灯油"),
          ("H4:K4", "合計と前年同月比"), ("L4:N4", "種類別 前年同月比／実績単価"), ("O4:O4", "")]
for rng, label in groups:
    if ":" in rng and rng.split(":")[0] != rng.split(":")[1]:
        ws.merge_cells(rng)
    c = ws[rng.split(":")[0]]
    c.value = label
    c.font = Font(name=FONT, bold=True, size=10, color="FFFFFF")
    c.fill = PatternFill("solid", fgColor=TEAL)
    c.alignment = Alignment(horizontal="center")
headers = ["年月", "使用量（kWh）", "料金（円）", "使用量（m³）", "料金（円）", "購入量（L）", "代金（円）",
           "合計（円）", "前年同月の合計", "前年差（円）", "前年比",
           "電気 前年比", "ガス 前年比", "電気の実績単価（円/kWh）", "メモ"]
for i, h in enumerate(headers, 1):
    ws.cell(row=5, column=i, value=h)
style_header(ws, 5, len(headers))
widths = [10, 11, 11, 11, 11, 11, 11, 12, 13, 12, 10, 10, 10, 13, 24]
for i, w in enumerate(widths, 1):
    ws.column_dimensions[ws.cell(row=5, column=i).column_letter].width = w

A = f"$A${FIRST}:$A${LAST}"
INPUT_COLS = {2, 3, 4, 5, 6, 7, 15}
for r in range(FIRST, LAST + 1):
    if r == FIRST:
        ws[f"A{r}"] = date(2024, 11, 1)
    else:
        ws[f"A{r}"] = f"=IF(A{r-1}=\"\",\"\",EDATE(A{r-1},1))"
    has = f'COUNT(B{r}:G{r})>0'
    ws[f"H{r}"] = f'=IF({has},SUM(C{r},E{r},G{r}),"")'
    prev = f'EDATE(A{r},-12)'
    prev_has = f'COUNTIFS({A},{prev},$H${FIRST}:$H${LAST},">0")>0'
    ws[f"I{r}"] = f'=IF(A{r}="","",IF({prev_has},SUMIFS($H${FIRST}:$H${LAST},{A},{prev}),""))'
    ws[f"J{r}"] = f'=IF(AND(ISNUMBER(H{r}),ISNUMBER(I{r})),H{r}-I{r},"")'
    ws[f"K{r}"] = f'=IF(AND(ISNUMBER(H{r}),ISNUMBER(I{r})),IF(I{r}=0,"",H{r}/I{r}-1),"")'
    for col, src in (("L", "C"), ("M", "E")):
        p = f'SUMIFS(${src}${FIRST}:${src}${LAST},{A},{prev})'
        ws[f"{col}{r}"] = (f'=IF(OR(A{r}="",NOT(ISNUMBER({src}{r}))),"",'
                           f'IF({p}=0,"",{src}{r}/{p}-1))')
    ws[f"N{r}"] = f'=IF(AND(ISNUMBER(B{r}),ISNUMBER(C{r})),IF(B{r}=0,"",ROUND(C{r}/B{r},1)),"")'
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=r, column=c)
        cell.border = BORDER
        cell.font = Font(name=FONT, size=10)
        if c in INPUT_COLS or (c == 1 and r == FIRST):
            cell.fill = INPUT_FILL
        else:
            cell.fill = CALC_FILL
        if c == 1:
            cell.number_format = "yyyy/mm"
            cell.alignment = Alignment(horizontal="center")
        elif c in (11, 12, 13):
            cell.number_format = PCT
            cell.alignment = Alignment(horizontal="center")
        elif c == 14:
            cell.number_format = "0.0"
        elif c != 15:
            cell.number_format = YEN

for i, s in enumerate(SAMPLE):
    r = FIRST + i
    for col, v in zip("BCDEFG", s):
        ws[f"{col}{r}"] = v

tr = LAST + 1
ws[f"A{tr}"] = "合計"
for col in "BCDEFGH":
    ws[f"{col}{tr}"] = f"=SUM({col}{FIRST}:{col}{LAST})"
for c in range(1, len(headers) + 1):
    cell = ws.cell(row=tr, column=c)
    cell.font = Font(name=FONT, bold=True, size=10, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor=TEAL)
    cell.border = BORDER
    cell.number_format = "#,##0"

dv_num = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True)
ws.add_data_validation(dv_num)
dv_num.add(f"B{FIRST}:G{LAST}")

# 前年より増えた月を赤、減った月を緑
for rng, col in ((f"K{FIRST}:K{LAST}", "K"), (f"L{FIRST}:L{LAST}", "L"), (f"M{FIRST}:M{LAST}", "M")):
    ws.conditional_formatting.add(rng, FormulaRule(
        formula=[f'AND(ISNUMBER({col}{FIRST}),{col}{FIRST}>=0.1)'],
        fill=PatternFill("solid", bgColor="FDE2E1"), font=Font(color="B42318", bold=True)))
    ws.conditional_formatting.add(rng, FormulaRule(
        formula=[f'AND(ISNUMBER({col}{FIRST}),{col}{FIRST}<0)'],
        fill=PatternFill("solid", bgColor="DFF3EA"), font=Font(color="1B7F4B")))
# 今冬の行をうっすら強調
ws.conditional_formatting.add(f"A{FIRST}:A{LAST}", FormulaRule(
    formula=[f'AND(ISNUMBER($A{FIRST}),$A{FIRST}>={WSTART},$A{FIRST}<EDATE({WSTART},{WLEN}))'],
    fill=PatternFill("solid", bgColor="FFE3D3"), font=Font(bold=True, color=WARM)))
ws.freeze_panes = "B6"

# ================= 暖房器具の電気代 =================
ap = wb.create_sheet("暖房器具の電気代", 1)
title(ap, "暖房器具ごとの電気代",
      "消費電力（W）は製品の銘板・取扱説明書の値を入れてください。入っている器具と数字は架空の例です。")
ap["A3"] = "計算式：消費電力(W) ÷ 1000 × 使用時間(h) × 電気単価(円/kWh)。単価は「設定」シートの値（初期値31円/kWh）。"
ap["A4"] = "※ エアコンは室温・外気温で消費電力が大きく変わるため、ここでの数字は目安です。カタログの「期間消費電力量（kWh/年）」×単価で年額の目安も出せます。"
for r in (3, 4):
    ap[f"A{r}"].font = Font(name=FONT, size=9, color=TEAL)
ah = ["器具名", "消費電力（W）", "1日の使用時間（h）", "1か月の使用日数", "1時間あたり（円）",
      "1日あたり（円）", "1か月あたり（円）", "冬の期間合計（円）", "メモ"]
for i, h in enumerate(ah, 1):
    ap.cell(row=5, column=i, value=h)
style_header(ap, 5, len(ah))
for col, w in zip("ABCDEFGHI", (26, 11, 11, 11, 11, 11, 12, 13, 36)):
    ap.column_dimensions[col].width = w
for r in range(APP_FIRST, APP_LAST + 1):
    ap[f"E{r}"] = f'=IF(OR(A{r}="",B{r}=""),"",ROUND(B{r}/1000*{UNIT},1))'
    ap[f"F{r}"] = f'=IF(OR(E{r}="",C{r}=""),"",ROUND(B{r}/1000*C{r}*{UNIT},0))'
    ap[f"G{r}"] = f'=IF(F{r}="","",ROUND(F{r}*IF(D{r}="",設定!$B$7,D{r}),0))'
    ap[f"H{r}"] = f'=IF(G{r}="","",G{r}*{WLEN})'
    for c in range(1, 10):
        cell = ap.cell(row=r, column=c)
        cell.border = BORDER
        cell.font = Font(name=FONT, size=10)
        cell.fill = INPUT_FILL if c in (1, 2, 3, 4, 9) else CALC_FILL
        if c == 5:
            cell.number_format = "#,##0.0"
        elif c in (2, 6, 7, 8):
            cell.number_format = YEN
for i, (name, w, h, d, memo) in enumerate(APPLIANCES):
    r = APP_FIRST + i
    ap[f"A{r}"], ap[f"B{r}"], ap[f"C{r}"], ap[f"D{r}"], ap[f"I{r}"] = name, w, h, d, memo
atr = APP_LAST + 1
ap[f"A{atr}"] = "合計"
for col in "FGH":
    ap[f"{col}{atr}"] = f"=SUM({col}{APP_FIRST}:{col}{APP_LAST})"
for c in range(1, 10):
    cell = ap.cell(row=atr, column=c)
    cell.font = Font(name=FONT, bold=True, size=10, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor=TEAL)
    cell.border = BORDER
    cell.number_format = "#,##0"
dv_w = DataValidation(type="decimal", operator="between", formula1="0", formula2="5000", allow_blank=True)
dv_h = DataValidation(type="decimal", operator="between", formula1="0", formula2="24", allow_blank=True)
dv_d = DataValidation(type="whole", operator="between", formula1="0", formula2="31", allow_blank=True)
for dv, col in ((dv_w, "B"), (dv_h, "C"), (dv_d, "D")):
    ap.add_data_validation(dv)
    dv.add(f"{col}{APP_FIRST}:{col}{APP_LAST}")
ap.conditional_formatting.add(f"G{APP_FIRST}:G{APP_LAST}", FormulaRule(
    formula=[f'AND(ISNUMBER(G{APP_FIRST}),G{APP_FIRST}=MAX($G${APP_FIRST}:$G${APP_LAST}))'],
    fill=PatternFill("solid", bgColor="FDE2E1"), font=Font(color="B42318", bold=True)))
bc = BarChart()
bc.type = "bar"
bc.title = "器具ごとの1か月の電気代（円）"
bc.legend = None
bc.add_data(Reference(ap, min_col=7, min_row=5, max_row=5 + len(APPLIANCES)), titles_from_data=True)
bc.set_categories(Reference(ap, min_col=1, min_row=6, max_row=5 + len(APPLIANCES)))
bc.height, bc.width = 7.5, 16
ap.add_chart(bc, "A24")

# ================= 冬のまとめ =================
sm = wb.create_sheet("冬のまとめ", 0)
title(sm, "冬のまとめ", "すべて自動計算。「設定」シートの今冬の開始月・月数で集計します。")
M = lambda c: f"月次記録!${c}${FIRST}:${c}${LAST}"  # noqa: E731
rng_now = f'{M("A")},">="&{WSTART},{M("A")},"<"&EDATE({WSTART},{WLEN})'
rng_prev = f'{M("A")},">="&EDATE({WSTART},-12),{M("A")},"<"&EDATE({WSTART},{WLEN}-12)'
hdr = ["", "今冬", "前の冬", "前年差（円）", "前年比"]
for i, h in enumerate(hdr, 1):
    sm.cell(row=4, column=i, value=h)
style_header(sm, 4, 5, height=24)
items = [("電気代", "C"), ("ガス代", "E"), ("灯油代", "G"), ("光熱費 合計", "H"), ("電気 使用量（kWh）", "B"),
         ("ガス 使用量（m³）", "D"), ("灯油 購入量（L）", "F")]
for i, (label, col) in enumerate(items):
    r = 5 + i
    sm[f"A{r}"] = label
    sm[f"B{r}"] = f"=SUMIFS({M(col)},{rng_now})"
    sm[f"C{r}"] = f"=SUMIFS({M(col)},{rng_prev})"
    sm[f"D{r}"] = f"=B{r}-C{r}"
    sm[f"E{r}"] = f'=IF(C{r}=0,"",B{r}/C{r}-1)'
    for c in "ABCDE":
        cell = sm[f"{c}{r}"]
        cell.border = BORDER
        cell.font = Font(name=FONT, size=11, bold=(label == "光熱費 合計"))
        if c != "A":
            cell.fill = CALC_FILL
            cell.number_format = PCT if c == "E" else YEN
sm["A13"] = "今冬の期間"
sm["B13"] = f'={WSTART}'
sm["C13"] = f'=EDATE({WSTART},{WLEN}-1)'
sm["B13"].number_format = sm["C13"].number_format = "yyyy/mm"
sm["A14"] = "今冬で記録済みの月数"
sm["B14"] = f'=COUNTIFS({rng_now},{M("H")},">0")'
sm["A15"] = "今冬の1か月平均（円）"
sm["B15"] = '=IF(B14=0,"",ROUND(B8/B14,0))'
sm["B15"].number_format = YEN
sm["A16"] = "※ 今冬がまだ途中のときは、前の冬（全月）と比べると少なく見えます。月ごとの比較は「月次記録」シートのK列を見てください。"
sm["A16"].font = Font(name=FONT, size=9, color="5B6B7B")
for r in (13, 14, 15):
    sm[f"A{r}"].font = Font(name=FONT, size=10)
    for c in "BC":
        sm[f"{c}{r}"].font = Font(name=FONT, size=11, bold=True, color=NAVY)
sm.conditional_formatting.add("E5:E11", FormulaRule(
    formula=['AND(ISNUMBER(E5),E5>=0.1)'], font=Font(color="B42318", bold=True)))
sm.conditional_formatting.add("E5:E11", FormulaRule(
    formula=['AND(ISNUMBER(E5),E5<0)'], font=Font(color="1B7F4B", bold=True)))
sm.column_dimensions["A"].width = 24
for c in "BCDE":
    sm.column_dimensions[c].width = 14

lc = LineChart()
lc.title = "毎月の光熱費 合計と前年同月（円）"
lc.add_data(Reference(ws, min_col=8, min_row=5, max_row=FIRST + len(SAMPLE) - 1), titles_from_data=True)
lc.add_data(Reference(ws, min_col=9, min_row=5, max_row=FIRST + len(SAMPLE) - 1), titles_from_data=True)
lc.set_categories(Reference(ws, min_col=1, min_row=FIRST, max_row=FIRST + len(SAMPLE) - 1))
lc.x_axis.number_format = "yyyy/mm"
lc.height, lc.width = 8, 18
sm.add_chart(lc, "G4")

# ================= 使い方 =================
hw = wb.create_sheet("使い方", 0)
title(hw, "使い方（3ステップ）", "このテンプレートはAI（Claude）が設計・作成しました。入っている数字はすべて架空のサンプルです。")
lines = [
    ("STEP 1　サンプルを消す", "「月次記録」のB〜G列、「暖房器具の電気代」のA〜D列の黄色セルを選んで Delete。灰色の列（数式）は消さない。"),
    ("STEP 2　最初の月を決める", "「月次記録」A6に記録を始める月の1日（例：2025/11/1）を入れる。下の行は自動で1か月ずつ進む（3年分）。"),
    ("", "・前年同月比を出したい場合は、去年の検針票・Webの明細（電力会社・ガス会社の会員ページ）から1年前の分も入れる。"),
    ("STEP 3　毎月入れる", "検針票・明細を見て、電気（kWh・円）、ガス（m³・円）、灯油（L・円）を入れる。使っていない燃料は空欄でOK。"),
    ("", "・前年同月より10%以上増えた月は赤、減った月は緑になる。"),
    ("暖房器具の電気代", "器具名と消費電力（W：本体の銘板や取扱説明書）・1日の使用時間を入れると、1時間・1日・1か月・冬の合計の電気代が出る。"),
    ("設定", "電気単価（初期値31円/kWh＝家電の電気代表示に使われる目安）、今冬の開始月・月数を変えられる。自分の明細の単価を入れるとより正確。"),
    ("Googleスプレッドシートで使う", "Googleドライブにこの.xlsxをアップロード →「Googleスプレッドシートで開く」→「ファイル＞Googleスプレッドシートとして保存」。"),
    ("Excelで使う", "そのまま開くだけ。Excel 2010以降・Microsoft 365・Excel for Mac・LibreOffice Calcで動く関数だけを使っています。"),
    ("注意", "電気代の計算は目安です。実際の請求額は契約プラン・基本料金・燃料費調整額・再エネ賦課金・政府の補助などで変わります。"),
]
for i, (a, b) in enumerate(lines):
    r = 4 + i
    hw[f"A{r}"], hw[f"B{r}"] = a, b
    hw[f"A{r}"].font = Font(name=FONT, bold=True, size=10, color=NAVY)
    hw[f"B{r}"].font = Font(name=FONT, size=10)
    hw[f"B{r}"].alignment = Alignment(wrap_text=True, vertical="top")
    hw[f"A{r}"].alignment = Alignment(vertical="top")
    hw.row_dimensions[r].height = 30
hw.column_dimensions["A"].width = 30
hw.column_dimensions["B"].width = 100
hw["A16"] = "色の意味"
hw["A16"].font = Font(name=FONT, bold=True, size=10, color=NAVY)
legend = [("黄色セル", "あなたが入力する場所", "FFFDF0"), ("灰色セル", "自動計算（触らない）", LIGHT),
          ("赤", "前年同月より10%以上増えた／いちばん電気代が高い器具", "FDE2E1"),
          ("緑", "前年同月より減った", "DFF3EA"), ("オレンジの年月", "今冬（設定シートの期間）", "FFE3D3")]
for i, (a, b, color) in enumerate(legend):
    r = 17 + i
    hw[f"A{r}"], hw[f"B{r}"] = a, b
    hw[f"A{r}"].fill = PatternFill("solid", fgColor=color)
    for c in "AB":
        hw[f"{c}{r}"].font = Font(name=FONT, size=10)
        hw[f"{c}{r}"].border = BORDER
hw["A23"] = "電気単価31円/kWhの出典：全国家庭電気製品公正取引協議会「新電気料金目安単価」（2022年7月）"
hw["A24"] = "作成：電脳アリス／QOLガジェット研究所（AI運営）　https://zaq-master.github.io/ai-lab"
for r in (23, 24):
    hw[f"A{r}"].font = Font(name=FONT, size=9, color="5B6B7B")

wb.active = wb.sheetnames.index("使い方")
for s in wb.worksheets:
    s.sheet_view.showGridLines = s.title in ("月次記録", "暖房器具の電気代")
wb.save(OUT)
print("saved", OUT)
