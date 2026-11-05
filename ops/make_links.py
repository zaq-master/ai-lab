#!/usr/bin/env python3
"""もしも「どこでもリンク」（楽天）を検索キーワードから生成し、content/products.json の html に入れる。
もしもへのログインは不要（a_id は固定）。新しい商品枠を作ったら KEYWORDS に1行足して実行するだけ。
  python3 ops/make_links.py
"""
import json, html
from pathlib import Path
from urllib.parse import quote

A_ID = "5877487"            # もしも：QOLガジェット研究所（楽天市場 promotion 54）
P = "p_id=54&pc_id=54&pl_id=616"
KEYWORDS = {
    "smart-plug-monitor": "スマートプラグ 電力モニター",
    "smart-plug-basic": "スマートプラグ タイマー",
    "smart-remote-std": "スマートリモコン",
    "smart-remote-sensor": "スマートリモコン 温湿度センサー",
    "charger-65w": "USB-C 充電器 65W PD",
    "charger-30w": "USB-C 充電器 30W PD",
    "cable-c2c": "USB-C ケーブル 100W 5A",
    "monitor-light": "モニターライト",
    "monitor-arm": "モニターアーム",
    "foot-heater": "足元ヒーター デスク下",
    "humidifier-vaporize": "加湿器 気化式",
    "humidifier-steam": "加湿器 スチーム式",
    "denki-moufu": "電気毛布 ひざ掛け",
    "thermo-hygrometer": "温湿度計 デジタル",
    "kotatsu-hitori": "こたつ 一人用",
    "ceramic-heater": "セラミックヒーター",
    "circulator": "サーキュレーター",
    "hot-carpet": "ホットカーペット",
    "yutanpo": "湯たんぽ",
    "datsuijo-heater": "脱衣所 ヒーター",
    "window-danetsu-sheet": "窓 断熱シート 貼ってはがせる",
    "monitor-light-curved": "モニターライト 曲面モニター対応",
    "monitor-light-remote": "モニターライト リモコン付き",
    "cable-tray": "ケーブルトレー デスク 配線",
    "footrest": "フットレスト デスク",
    "heated-vest": "電熱ベスト USB",
    "mobile-battery-10000": "モバイルバッテリー 10000mAh PSE",
    "joshitsuki-compressor": "除湿機 コンプレッサー",
    "joshitsuki-desiccant": "除湿機 デシカント",
    "joshitsuki-hybrid": "除湿機 ハイブリッド",
}


def link(keyword):
    target = f"https://search.rakuten.co.jp/search/mall/{quote(keyword)}/"
    href = f"https://af.moshimo.com/af/c/click?a_id={A_ID}&{P}&url={quote(target, safe='')}"
    return (f'<a class="buy" href="{href}" rel="nofollow sponsored noopener" target="_blank" '
            f'referrerpolicy="no-referrer-when-downgrade">楽天市場で「{html.escape(keyword)}」を探す →</a>'
            f'<img src="https://i.moshimo.com/af/i/impression?a_id={A_ID}&{P}" width="1" height="1" style="border:none" alt="" loading="lazy">')


if __name__ == "__main__":
    p = Path(__file__).resolve().parent.parent / "content" / "products.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    n = 0
    for k, kw in KEYWORDS.items():
        if k in d and not d[k].get("html"):
            d[k]["html"] = link(kw); n += 1
    missing = [k for k in d if k != "_help" and not d[k].get("html")]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"filled {n}; still empty: {missing}")
