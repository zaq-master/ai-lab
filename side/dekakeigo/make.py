"""でか敬語：LINEスタンプ40個とSUZURI用デザインを文字だけで自動生成する。

使い方: python3 side/dekakeigo/make.py
出力:   side/dekakeigo/out/line/   … LINEスタンプ申請用（01〜40.png, main.png, tab.png）＋ line_stickers.zip
        side/dekakeigo/out/suzuri/ … SUZURI用（透過PNG 2400px）
        side/dekakeigo/out/preview.png … 一覧（確認用）

画像生成AIは使わず、フォントで描くだけ（審査・著作権のリスクを下げるため）。
フォント：IPAゴシック（IPAフォントライセンス。描いた画像の販売は可）。
"""
import os
import zipfile
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FONT = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"

# (文字, 色)。改行は "\n"。仕事・家族・友だちのどれでも使える丁寧なひと言
PHRASES = [
    ("承知\nしました", "#1f6feb"), ("ありがとう\nござい\nます", "#e8590c"),
    ("お疲れ\nさまです", "#2f9e44"), ("よろしく\nお願い\nします", "#7048e8"),
    ("了解\nです", "#1f6feb"), ("すみません", "#c2255c"),
    ("今から\n帰ります", "#2f9e44"), ("少し\n遅れます", "#e03131"),
    ("確認\nします", "#1f6feb"), ("確認\nしました", "#1971c2"),
    ("さすが\nです", "#e8590c"), ("助かり\nます", "#2f9e44"),
    ("おはよう\nござい\nます", "#f08c00"), ("おやすみ\nなさい", "#5f3dc4"),
    ("いま\n無理です", "#e03131"), ("あとで\n見ます", "#868e96"),
    ("最高\nです", "#e8590c"), ("なるほど\nです", "#1971c2"),
    ("ご報告\nです", "#0c8599"), ("お願い\nします", "#7048e8"),
    ("大丈夫\nです", "#2f9e44"), ("無理\nしないでね", "#d6336c"),
    ("いいね\nです", "#f08c00"), ("失礼\nします", "#495057"),
    ("お先に\n失礼\nします", "#495057"), ("向かって\nます", "#2f9e44"),
    ("着き\nました", "#1f6feb"), ("ごめん\nなさい", "#c2255c"),
    ("おめでとう\nござい\nます", "#e8590c"), ("楽しみ\nです", "#f08c00"),
    ("寝坊\nしました", "#e03131"), ("帰ったら\n連絡\nします", "#0c8599"),
    ("既読\nです", "#868e96"), ("天才\nですか", "#7048e8"),
    ("尊い\nです", "#d6336c"), ("休み\nたいです", "#5f3dc4"),
    ("ご飯\nいります", "#2f9e44"), ("ご飯\nいりません", "#e03131"),
    ("検討\nします", "#495057"), ("以上\nです", "#1f6feb"),
]
assert len(PHRASES) == 40


def fit_font(draw, text, max_w, max_h, stroke_ratio=0.10):
    """枠に収まる最大の文字サイズを探す。"""
    lo, hi, best = 10, 2000, 10
    while lo <= hi:
        mid = (lo + hi) // 2
        f = ImageFont.truetype(FONT, mid)
        sw = max(2, int(mid * stroke_ratio))
        l, t, r, b = draw.multiline_textbbox((0, 0), text, font=f, spacing=int(mid * 0.08),
                                             align="center", stroke_width=sw)
        if r - l <= max_w and b - t <= max_h:
            best, lo = mid, mid + 1
        else:
            hi = mid - 1
    return best


def render(text, color, w, h, margin, bg=None):
    """白フチ付きの太い文字を描く。IPAゴシックは細字なので同色の内側フチで太らせる。"""
    img = Image.new("RGBA", (w, h), bg or (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    size = fit_font(d, text, w - margin * 2, h - margin * 2)
    f = ImageFont.truetype(FONT, size)
    spacing = int(size * 0.08)
    outer = max(2, int(size * 0.09))   # 白フチ（暗いトーク画面でも読める）
    inner = max(1, int(size * 0.022))  # 文字を太く見せる
    l, t, r, b = d.multiline_textbbox((0, 0), text, font=f, spacing=spacing, align="center",
                                      stroke_width=outer)
    x = (w - (r - l)) / 2 - l
    y = (h - (b - t)) / 2 - t
    d.multiline_text((x, y), text, font=f, fill="white", spacing=spacing, align="center",
                     stroke_width=outer, stroke_fill="white")
    d.multiline_text((x, y), text, font=f, fill=color, spacing=spacing, align="center",
                     stroke_width=inner, stroke_fill=color)
    return img


def main():
    line_dir = os.path.join(OUT, "line")
    suz_dir = os.path.join(OUT, "suzuri")
    os.makedirs(line_dir, exist_ok=True)
    os.makedirs(suz_dir, exist_ok=True)

    # LINEスタンプ：最大370x320・偶数・透過PNG・余白10px程度
    for i, (text, color) in enumerate(PHRASES, 1):
        render(text, color, 370, 320, 12).save(os.path.join(line_dir, f"{i:02d}.png"), optimize=True)
    render("でか\n敬語", "#1f6feb", 240, 240, 12).save(os.path.join(line_dir, "main.png"), optimize=True)
    render("敬語", "#1f6feb", 96, 74, 4).save(os.path.join(line_dir, "tab.png"), optimize=True)

    zpath = os.path.join(OUT, "line_stickers.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(os.listdir(line_dir)):
            z.write(os.path.join(line_dir, name), name)

    # SUZURI：透過PNG 2400x2400（Tシャツ・ステッカー・スマホケース共通で使える大きさ）
    for i, (text, color) in enumerate(PHRASES, 1):
        render(text, color, 2400, 2400, 120).save(os.path.join(suz_dir, f"{i:02d}.png"), optimize=True)

    # 確認用の一覧（灰色背景＝暗い画面での見え方も確認）
    cols, cw, ch = 8, 185, 160
    sheet = Image.new("RGB", (cols * cw, 5 * ch), "#cfd4da")
    for i in range(40):
        im = Image.open(os.path.join(line_dir, f"{i+1:02d}.png")).resize((cw, ch))
        sheet.paste(im, ((i % cols) * cw, (i // cols) * ch), im)
    sheet.save(os.path.join(OUT, "preview.png"))
    print("ok:", zpath)


if __name__ == "__main__":
    main()
