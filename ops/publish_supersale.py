#!/usr/bin/env python3
"""12月の楽天スーパーSALE記事を「公開手順」3〜5番どおりに差し込む（2026-11-28 20:06 自走回で作成）。

使い方：
  python3 ops/publish_supersale.py            # 試し（既定）：作業用コピーで差し込み→build→点検。リポジトリは変えない
  python3 ops/publish_supersale.py --apply    # 本番：このリポジトリに差し込む（commit/push は自分で）

やること：
  1. ops/drafts/supersale_2026_12_draft.md の本文 → content/posts/rakuten-supersale-fuyu-memo.md（{{公開日}}＝今日）
  2. build.py の EXPIRE・STARTS・SALE・SALE_ON をスーパーSALEに差し替え（BFは「# 前回：」に残す）
  3. BF記事の終了後の段落の下に「次はスーパーSALE」の1行（supersale-2026-12 の目印付き＝終了で自動で消える）
止まる条件：本体の公式ページで日時を確認していない（--confirmed を付けない）、{{ が残る、終了時刻を過ぎている。
"""
import argparse, datetime, pathlib, re, shutil, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
TAG, START, END = "supersale-2026-12", "2026-12-04T20:00", "2026-12-11T01:59"
SLUG = "rakuten-supersale-fuyu-memo"
NEXT_LINE = ("次の楽天スーパーSALEは12/4（金）20:00〜。日程と買う前のメモは"
             "[楽天スーパーSALE前の冬ガジェット買い物メモ](rakuten-supersale-fuyu-memo.html)へ。")


def jst_now():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).replace(tzinfo=None)


def body_from_draft(text, today):
    a = text.index("## ここから記事本文")
    b = text.index("## 公開手順")
    body = text[a:b].split("\n", 1)[1]
    body = body.rstrip().removesuffix("---").rstrip() + "\n"   # 本文の後ろの区切り線を外す
    body = body.replace("```\n---", "---", 1)                   # front matter のコードブロック記号を外す
    body = body.replace("---\n```", "---", 1)
    body = body.replace("{{公開日}}", today).lstrip()
    if "{{" in body:
        sys.exit("止めた：本文に {{ が残っている → " + ", ".join(sorted(set(re.findall(r"\{\{[^}]*\}\}", body)))))
    if not body.startswith("---\ntitle:"):
        sys.exit("止めた：front matter の形が想定と違う（先頭が ---/title: でない）")
    return body


def patch_build(s):
    def sub1(pat, rep):
        nonlocal s
        s2, n = re.subn(pat, rep, s, count=1, flags=re.M)
        if n != 1:
            sys.exit(f"止めた：build.py の置き換え先が見つからない：{pat[:40]}")
        s = s2
    if TAG in s:
        sys.exit("止めた：build.py にもう supersale-2026-12 がある（差し込み済み？）")
    sub1(r'^(EXPIRE = \{.*?)\}', r'\1, "%s": "%s"}' % (TAG, END))
    sub1(r'^(STARTS = \{.*?)\}', r'\1, "%s": "%s"}' % (TAG, START))
    sub1(r'^SALE = \(.*?\n.*?\)\n',
         f'SALE = ("posts/{SLUG}.html", "楽天スーパーSALE前の冬ガジェット買い物メモ【PR】",\n'
         f'        "12/4 20:00〜12/11 01:59。電気代で選ぶ暖房・加湿器など", "{END}")\n')
    sub1(r'^SALE_ON = \(.*?\n.*?\)\n',
         f'SALE_ON = ("{TAG}", "楽天スーパーSALE開催中：冬ガジェット買い物メモ【PR】",\n'
         f'           "開催中です（12/11 01:59まで）。電気代で選ぶ暖房・加湿器など")\n')
    sub1(r'^(# 前回：マラソン.*)$',
         r'# 前回：BF（posts/rakuten-blackfriday-memo.html、2026-11-19T20:00〜2026-11-25T01:59）\n\1')
    return s


def patch_bf(s):
    anchor = "下の選び方は次のセールでもそのまま使えます。<br>\nクリスマス・年末の贈り物を選ぶなら[相手の悩み別の早見表](telework-gadget-present-erabikata.html#_2)へ。\n"
    if s.count(anchor) != 1:
        sys.exit("止めた：BF記事の終了後の段落が想定と違う")
    return s.replace(anchor, anchor + f"\n<!-- {TAG} -->\n{NEXT_LINE}\n", 1)


def apply(root, today):
    draft = (root / "ops/drafts/supersale_2026_12_draft.md").read_text()
    post = root / f"content/posts/{SLUG}.md"
    if post.exists():
        sys.exit("止めた：記事がもう content/posts にある")
    post.write_text(body_from_draft(draft, today))
    (root / "build.py").write_text(patch_build((root / "build.py").read_text()))
    bf = root / "content/posts/rakuten-blackfriday-memo.md"
    bf.write_text(patch_bf(bf.read_text()))


def run(root, *cmd):
    r = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
    tail = (r.stdout + r.stderr).strip().splitlines()[-3:]
    print(f"  {'OK ' if r.returncode == 0 else 'NG '} {' '.join(cmd[1:])}：" + " / ".join(tail))
    return r.returncode == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="このリポジトリに差し込む")
    ap.add_argument("--confirmed", action="store_true",
                    help="楽天市場本体の公式ページで 12/4 20:00〜12/11 01:59 を確認した（--apply に必須）")
    a = ap.parse_args()
    now = jst_now()
    if now >= datetime.datetime.fromisoformat(END):
        sys.exit("止めた：スーパーSALEの終了時刻を過ぎている")
    if a.apply and not a.confirmed:
        sys.exit("止めた：--apply には --confirmed（本体の公式ページで日時を確認した）が必要（絶対ルール6）")
    today = now.strftime("%Y-%m-%d")
    if a.apply:
        root = ROOT
    else:
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="ss_try_"))
        root = tmp / "repo"
        subprocess.run(["git", "worktree", "add", "-q", "--detach", str(root)], cwd=ROOT, check=True)
        for f in ["build.py", "content/posts/rakuten-blackfriday-memo.md", "ops/drafts/supersale_2026_12_draft.md"]:
            shutil.copy(ROOT / f, root / f)   # まだ commit していない手元の変更も試しに含める
    print(("本番" if a.apply else "試し") + f"：{root}")
    apply(root, today)
    ok = all([run(root, sys.executable, "build.py"),
              run(root, sys.executable, "ops/check_affiliate.py"),
              run(root, sys.executable, "ops/tests/mobile_check.py"),
              run(root, sys.executable, "ops/tests/content_guard.py")])
    page = root / f"docs/posts/{SLUG}.html"
    ok = ok and page.exists() and "{{" not in page.read_text()
    print("  ページ生成：" + ("OK" if page.exists() else "なし"))
    if not a.apply:
        subprocess.run(["git", "worktree", "remove", "--force", str(root)], cwd=ROOT)
        shutil.rmtree(tmp, ignore_errors=True)
    print("結果：" + ("合格" if ok else "不合格（直してから公開）"))
    if a.apply and ok:
        print("次：git pull --rebase → git add -A → commit → push → 1〜2分後にページが開くか確認")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
