"""サブスク管理＆見直し表 (.xlsx) を生成する。
数式は Excel / Googleスプレッドシート / LibreOffice で共通に動く関数だけを使う
（IF, AND, OR, ISNUMBER, ROUND, SUMIFS, COUNTIFS, SUM, TODAY, EDATE, DATEDIF, INT, IFERROR）。
実行: python3 build_xlsx.py
"""
from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

OUT = Path(__file__).with_name("subscription-manager.xlsx")
ROWS = 50            # 入力行数
FIRST = 5            # 入力シートのデータ開始行
LAST = FIRST + ROWS - 1

FONT = "Meiryo"
NAVY = "1F3A5F"
TEAL = "2A9D8F"
LIGHT = "EEF4F8"
INPUT_FILL = PatternFill("solid", fgColor="FFFDF0")
HEAD_FILL = PatternFill("solid", fgColor=NAVY)
CALC_FILL = PatternFill("solid", fgColor=LIGHT)
thin = Side(style="thin", color="C9D3DD")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

CATEGORIES = ["動画", "音楽", "クラウド・ツール", "ニュース・読書", "健康・フィットネス",
              "学習", "ゲーム", "生活・買い物", "その他"]

# 架空のサンプル（実在サービス・実在価格ではありません）
SAMPLES = [
    ("動画サブスクA", "動画", "月額", 1000, date(2025, 4, 10), 12, "", "クレカ"),
    ("動画サブスクB", "動画", "月額", 800, date(2025, 9, 3), 1, "", "クレカ"),
    ("音楽サブスクC", "音楽", "月額", 1000, date(2024, 6, 21), 25, "", "キャリア決済"),
    ("クラウドストレージD", "クラウド・ツール", "年額", 3600, date(2025, 2, 1), 30, "", "クレカ"),
    ("ニュースアプリE", "ニュース・読書", "月額", 500, date(2025, 11, 15), 0, "使っていない", "クレカ"),
    ("雑誌読み放題F", "ニュース・読書", "月額", 400, date(2025, 7, 28), 2, "", "クレカ"),
    ("フィットネスアプリG", "健康・フィットネス", "月額", 1200, date(2026, 1, 5), 0, "使っていない", "クレカ"),
    ("語学学習H", "学習", "年額", 9600, date(2026, 3, 12), 8, "", "クレカ"),
    ("ゲームサブスクI", "ゲーム", "月額", 700, date(2025, 12, 1), 6, "", "キャリア決済"),
    ("ネットスーパー会員J", "生活・買い物", "年額", 4800, date(2025, 5, 20), 3, "", "クレカ"),
]


def style_header(ws, row, ncols, height=34):
    for c in range(1, ncols + 1):
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


wb = Workbook()

# ---------------- 設定 ----------------
st = wb.active
st.title = "設定"
title(st, "設定", "ここの数字を変えると、入力シートの判定と色分けが変わります。")
st["A4"], st["B4"] = "1回あたり料金がこの金額以上なら「要見直し」", 500
st["A5"], st["B5"] = "更新日の何日前から色を付けるか", 14
st["A6"], st["B6"] = "使用回数の目安（月）がこの回数以下なら「要見直し」", 1
for r in (4, 5, 6):
    st[f"A{r}"].font = Font(name=FONT, size=10)
    st[f"B{r}"].font = Font(name=FONT, size=11, bold=True)
    st[f"B{r}"].fill = INPUT_FILL
    st[f"B{r}"].border = BORDER
st["C4"], st["C5"], st["C6"] = "円", "日", "回"
st["A8"] = "カテゴリ一覧（自由に書き換え・追加OK／A9〜A23）"
st["A8"].font = Font(name=FONT, bold=True, size=10, color=NAVY)
for i in range(15):
    cell = st.cell(row=9 + i, column=1, value=CATEGORIES[i] if i < len(CATEGORIES) else None)
    cell.font = Font(name=FONT, size=10)
    cell.fill = INPUT_FILL
    cell.border = BORDER
st["A25"] = "支払周期"
st["A25"].font = Font(name=FONT, bold=True, size=10, color=NAVY)
st["A26"], st["A27"] = "月額", "年額"
st.column_dimensions["A"].width = 52
st.column_dimensions["B"].width = 10
st.column_dimensions["C"].width = 5

THRESH = "設定!$B$4"
ALERT = "設定!$B$5"
LOWUSE = "設定!$B$6"

# ---------------- 入力 ----------------
ws = wb.create_sheet("入力", 0)
title(ws, "サブスク管理＆見直し表",
      "黄色のセルだけ入力。灰色のセルは自動計算です（数式を消さないでください）。サンプル行は架空の例です。")
ws["A3"] = "※ 次回更新日は「契約開始日」と「支払周期」から自動で進みます。"
ws["A3"].font = Font(name=FONT, size=9, color=TEAL)

headers = ["No", "サービス名", "カテゴリ", "支払周期", "料金（円）", "契約開始日",
           "支払方法", "月の利用回数", "使っていない", "月額換算", "年額換算",
           "次回更新日", "更新まで（日）", "1回あたり料金", "判定", "解約時の節約額（年）", "メモ"]
for i, h in enumerate(headers, 1):
    ws.cell(row=4, column=i, value=h)
style_header(ws, 4, len(headers))
widths = [5, 22, 16, 9, 11, 12, 12, 10, 12, 11, 11, 12, 10, 12, 11, 14, 24]
for i, w in enumerate(widths, 1):
    ws.column_dimensions[ws.cell(row=4, column=i).column_letter].width = w

INPUT_COLS = {2, 3, 4, 5, 6, 7, 8, 9, 17}
for r in range(FIRST, LAST + 1):
    n = r - FIRST + 1
    ws.cell(row=r, column=1, value=n)
    # J 月額換算
    ws[f"J{r}"] = f'=IF(OR(B{r}="",E{r}=""),"",IF(D{r}="年額",ROUND(E{r}/12,0),E{r}))'
    # K 年額換算
    ws[f"K{r}"] = f'=IF(OR(B{r}="",E{r}=""),"",IF(D{r}="年額",E{r},E{r}*12))'
    # L 次回更新日（契約開始日から周期ごとに自動で進める）
    step = f'IF(D{r}="年額",12,1)'
    k = f'INT(DATEDIF(F{r},TODAY(),"m")/{step})'
    ws[f"L{r}"] = (f'=IF(OR(B{r}="",F{r}=""),"",IF(F{r}>=TODAY(),F{r},'
                   f'IF(EDATE(F{r},{k}*{step})>=TODAY(),EDATE(F{r},{k}*{step}),'
                   f'EDATE(F{r},({k}+1)*{step}))))')
    # M 更新まで日数
    ws[f"M{r}"] = f'=IF(L{r}="","",L{r}-TODAY())'
    # N 1回あたり料金
    ws[f"N{r}"] = f'=IF(OR(J{r}="",H{r}=""),"",IF(H{r}=0,"未使用",ROUND(J{r}/H{r},0)))'
    # O 判定
    ws[f"O{r}"] = (f'=IF(B{r}="","",IF(OR(I{r}="使っていない",N{r}="未使用"),"解約候補",'
                   f'IF(OR(AND(ISNUMBER(N{r}),N{r}>={THRESH}),AND(ISNUMBER(H{r}),H{r}<={LOWUSE})),"要見直し","継続")))')
    # P 節約額（年）：「使っていない」にした分だけ
    ws[f"P{r}"] = f'=IF(AND(I{r}="使っていない",ISNUMBER(K{r})),K{r},0)'
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=r, column=c)
        cell.border = BORDER
        cell.font = Font(name=FONT, size=10)
        if c in INPUT_COLS:
            cell.fill = INPUT_FILL
        elif c > 1:
            cell.fill = CALC_FILL
        if c in (5, 10, 11, 14, 16):
            cell.number_format = '#,##0;-#,##0;"-"'
        if c in (6, 12):
            cell.number_format = "yyyy/mm/dd"
            cell.alignment = Alignment(horizontal="center")
        if c in (1, 4, 8, 9, 13, 15):
            cell.alignment = Alignment(horizontal="center")

for i, s in enumerate(SAMPLES):
    r = FIRST + i
    name, cat, cyc, price, start, uses, unused, pay = s
    ws[f"B{r}"], ws[f"C{r}"], ws[f"D{r}"], ws[f"E{r}"] = name, cat, cyc, price
    ws[f"F{r}"], ws[f"G{r}"], ws[f"H{r}"] = start, pay, uses
    if unused:
        ws[f"I{r}"] = unused

# 合計行
tr = LAST + 1
ws[f"B{tr}"] = "合計"
for col in ("J", "K", "P"):
    ws[f"{col}{tr}"] = f"=SUM({col}{FIRST}:{col}{LAST})"
for c in range(1, len(headers) + 1):
    cell = ws.cell(row=tr, column=c)
    cell.font = Font(name=FONT, bold=True, size=10, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor=TEAL)
    cell.border = BORDER
    if c in (10, 11, 16):
        cell.number_format = "#,##0"

# 入力規則（プルダウン）
dv_cat = DataValidation(type="list", formula1="=設定!$A$9:$A$23", allow_blank=True)
dv_cyc = DataValidation(type="list", formula1="=設定!$A$26:$A$27", allow_blank=True)
dv_unused = DataValidation(type="list", formula1='"使っていない"', allow_blank=True)
dv_num = DataValidation(type="whole", operator="greaterThanOrEqual", formula1="0", allow_blank=True)
for dv, col in ((dv_cat, "C"), (dv_cyc, "D"), (dv_unused, "I")):
    ws.add_data_validation(dv)
    dv.add(f"{col}{FIRST}:{col}{LAST}")
ws.add_data_validation(dv_num)
dv_num.add(f"E{FIRST}:E{LAST}")
dv_num.add(f"H{FIRST}:H{LAST}")

# 条件付き書式
rng = f"A{FIRST}:Q{LAST}"
ws.conditional_formatting.add(rng, FormulaRule(
    formula=[f'$O{FIRST}="解約候補"'], fill=PatternFill("solid", bgColor="FDE2E1"),
    font=Font(color="B42318")))
ws.conditional_formatting.add(rng, FormulaRule(
    formula=[f'$O{FIRST}="要見直し"'], fill=PatternFill("solid", bgColor="FFF1D6")))
ws.conditional_formatting.add(f"L{FIRST}:M{LAST}", FormulaRule(
    formula=[f'AND(ISNUMBER($M{FIRST}),$M{FIRST}<={ALERT})'],
    fill=PatternFill("solid", bgColor="FFD54F"), font=Font(bold=True)))

ws.freeze_panes = "C5"
ws.row_dimensions[1].height = 26

R = f"入力!$%s${FIRST}:$%s${LAST}"

# ---------------- 集計 ----------------
sm = wb.create_sheet("集計", 1)
title(sm, "集計ダッシュボード", "すべて自動計算。入力シートを更新すると変わります。")
kpis = [
    ("登録しているサブスク", f'=COUNTIFS({R % ("B", "B")},"?*")', "件"),
    ("毎月の合計（月額換算）", f"=SUM({R % ('J', 'J')})", "円"),
    ("1年間の合計（年額換算）", f"=SUM({R % ('K', 'K')})", "円"),
    ("「使っていない」を解約したら浮く額（年）", f"=SUM({R % ('P', 'P')})", "円"),
    ("解約候補の件数", f'=COUNTIFS({R % ("O", "O")},"解約候補")', "件"),
    ("要見直しの件数", f'=COUNTIFS({R % ("O", "O")},"要見直し")', "件"),
    ("30日以内に更新が来る件数", f'=COUNTIFS({R % ("M", "M")},">=0",{R % ("M", "M")},"<=30")', "件"),
]
for i, (label, f, unit) in enumerate(kpis):
    r = 4 + i
    sm[f"A{r}"], sm[f"B{r}"], sm[f"C{r}"] = label, f, unit
    sm[f"A{r}"].font = Font(name=FONT, size=10)
    sm[f"B{r}"].font = Font(name=FONT, size=13, bold=True,
                            color="B42318" if "浮く" in label else NAVY)
    sm[f"B{r}"].number_format = "#,##0"
    sm[f"B{r}"].fill = CALC_FILL
    for c in "ABC":
        sm[f"{c}{r}"].border = BORDER

hr = 13
for i, h in enumerate(["カテゴリ", "件数", "月額合計", "年額合計", "構成比", "節約できる額（年）"], 1):
    sm.cell(row=hr, column=i, value=h)
style_header(sm, hr, 6, height=24)
for i in range(15):
    r = hr + 1 + i
    sm[f"A{r}"] = f'=IF(設定!A{9 + i}="","",設定!A{9 + i})'
    sm[f"B{r}"] = f'=IF(A{r}="","",COUNTIFS({R % ("C", "C")},A{r}))'
    sm[f"C{r}"] = f'=IF(A{r}="","",SUMIFS({R % ("J", "J")},{R % ("C", "C")},A{r}))'
    sm[f"D{r}"] = f'=IF(A{r}="","",SUMIFS({R % ("K", "K")},{R % ("C", "C")},A{r}))'
    sm[f"E{r}"] = f'=IF(OR(A{r}="",$B$6=0),"",D{r}/$B$6)'
    sm[f"F{r}"] = f'=IF(A{r}="","",SUMIFS({R % ("P", "P")},{R % ("C", "C")},A{r}))'
    for c in "ABCDEF":
        cell = sm[f"{c}{r}"]
        cell.border = BORDER
        cell.font = Font(name=FONT, size=10)
        cell.fill = CALC_FILL
        cell.number_format = "0.0%" if c == "E" else '#,##0;-#,##0;"-"'
sm.column_dimensions["A"].width = 40
for c, w in zip("BCDEF", (14, 12, 12, 10, 16)):
    sm.column_dimensions[c].width = w

chart = BarChart()
chart.type = "bar"
chart.title = "カテゴリ別 月額合計（円）"
chart.legend = None
chart.y_axis.title = None
data = Reference(sm, min_col=3, min_row=hr, max_row=hr + len(CATEGORIES))
cats = Reference(sm, min_col=1, min_row=hr + 1, max_row=hr + len(CATEGORIES))
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
chart.height, chart.width = 8, 14
sm.add_chart(chart, "H4")

# ---------------- 使い方 ----------------
hw = wb.create_sheet("使い方", 0)
title(hw, "使い方（3ステップ・約10分）", "このテンプレートはAI（Claude）が設計・作成しました。サンプル行は架空のサービスです。")
lines = [
    ("STEP 1　サンプルを消す", "「入力」シートのサンプル（B〜I列・Q列の黄色セル）を選んで Delete。灰色の列（数式）は消さない。"),
    ("STEP 2　契約中のサブスクを書き出す", "カード明細・キャリア決済の明細・アプリストアの「サブスクリプション」画面を見ながら、黄色セルを埋める。"),
    ("", "・料金は1回の支払額（年払いなら年額をそのまま）。月額／年額は「支払周期」で選ぶ。"),
    ("", "・契約開始日を入れると、次回更新日が自動で計算され、毎日最新の日付に進む。"),
    ("", "・月の利用回数はざっくりでOK（例：週1回なら4）。0回なら自動で「解約候補」。"),
    ("STEP 3　見直す", "「判定」列が赤＝解約候補、オレンジ＝要見直し。更新日が近いものは黄色く光る。"),
    ("", "・本当に使っていないものは「使っていない」を選ぶと、浮く金額が「集計」シートに出る。"),
    ("", "・判定の基準（1回あたり何円以上で見直しか等）は「設定」シートで変えられる。"),
    ("Googleスプレッドシートで使う", "Googleドライブにこの.xlsxをアップロード →「Googleスプレッドシートで開く」→「ファイル＞Googleスプレッドシートとして保存」。"),
    ("Excelで使う", "そのまま開くだけ。Excel 2010以降・Microsoft 365・Excel for Mac・LibreOffice Calcで動作する関数だけを使っています。"),
    ("おすすめの使い方", "月に1回（給料日など）開いて「30日以内に更新が来る件数」を確認。解約は各サービスの公式手続きで。"),
    ("注意", "判定は目安です。解約するかどうかはご自身で判断してください。解約手続きや返金の可否は各サービスの規約をご確認ください。"),
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
hw["A18"] = "色の意味"
hw["A18"].font = Font(name=FONT, bold=True, size=10, color=NAVY)
legend = [("黄色セル", "あなたが入力する場所", "FFFDF0"), ("灰色セル", "自動計算（触らない）", LIGHT),
          ("赤い行", "解約候補（使っていない／利用0回）", "FDE2E1"), ("オレンジの行", "要見直し（1回あたりが高い／ほぼ使っていない）", "FFF1D6"),
          ("黄色く光る日付", "更新日が近い（設定シートの日数以内）", "FFD54F")]
for i, (a, b, color) in enumerate(legend):
    r = 19 + i
    hw[f"A{r}"], hw[f"B{r}"] = a, b
    hw[f"A{r}"].fill = PatternFill("solid", fgColor=color)
    for c in "AB":
        hw[f"{c}{r}"].font = Font(name=FONT, size=10)
        hw[f"{c}{r}"].border = BORDER
hw["A25"] = "作成：電脳アリス／QOLガジェット研究所（AI運営）　https://zaq-master.github.io/ai-lab"
hw["A25"].font = Font(name=FONT, size=9, color="5B6B7B")

wb.active = wb.sheetnames.index("使い方")
for s in wb.worksheets:
    s.sheet_view.showGridLines = s.title == "入力"
wb.save(OUT)
print("saved", OUT)
