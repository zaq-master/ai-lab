#!/usr/bin/env python3
"""エージェントの名前・アイコンで Slack に投稿する（Slackアプリ「AI-Lab Team」のBotトークンを使う）。
トークンは環境変数 SLACK_BOT_TOKEN から読む（Slack の非公開チャンネル #secrets-bot C0CE28MG71T に保管。リポジトリには絶対に書かない）。
使い方:
  SLACK_BOT_TOKEN=... python3 ops/slack_post.py <agent_key> "<本文>"          # agent_key: ceo, 01〜10
  SLACK_BOT_TOKEN=... python3 ops/slack_post.py <agent_key> "<本文>" --channel C0XXXX
  SLACK_BOT_TOKEN=... python3 ops/slack_post.py <agent_key> "<本文>" --image ops/out/biz01.png   # 画像を直接アップロード
"""
import json, os, sys, argparse, urllib.request, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AGENTS = json.load(open(ROOT / "agents.json", encoding="utf-8"))
ICON = "https://zaq-master.github.io/ai-lab/team/{}.png"


def api(method, token, data=None, raw=None, headers=None):
    h = {"Authorization": f"Bearer {token}"}
    if raw is None:
        h["Content-Type"] = "application/json; charset=utf-8"
        raw = json.dumps(data or {}).encode()
    h.update(headers or {})
    req = urllib.request.Request(f"https://slack.com/api/{method}", data=raw, headers=h)
    return json.load(urllib.request.urlopen(req, timeout=30))


def upload(token, path, channel, comment, thread_ts=None):
    b = Path(path).read_bytes()
    r = api("files.getUploadURLExternal", token,
            raw=urllib.parse.urlencode({"filename": Path(path).name, "length": len(b)}).encode(),
            headers={"Content-Type": "application/x-www-form-urlencoded"})
    if not r.get("ok"):
        return r
    urllib.request.urlopen(urllib.request.Request(r["upload_url"], data=b, method="POST"), timeout=60)
    c = api("files.completeUploadExternal", token, {"files": [{"id": r["file_id"], "title": Path(path).name}]})
    if not c.get("ok"):
        return c
    return {"file_id": r["file_id"]}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("agent"); ap.add_argument("text")
    ap.add_argument("--channel"); ap.add_argument("--image"); ap.add_argument("--thread")
    a = ap.parse_args()
    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        sys.exit("SLACK_BOT_TOKEN がありません（#secrets-bot から取得）")
    ag = AGENTS[a.agent]
    ch = a.channel or ag["channel"]
    body = {"channel": ch, "text": a.text, "username": f"{ag['name']}（{ag['role']}）",
            "icon_url": ICON.format(a.agent), "unfurl_links": True}
    if a.image:
        import time
        u = upload(token, a.image, ch, a.text, a.thread)
        if "file_id" not in u:
            print(json.dumps(u)); sys.exit(1)
        time.sleep(3)  # アップロード処理の完了待ち
        body["blocks"] = [{"type": "section", "text": {"type": "mrkdwn", "text": a.text}},
                          {"type": "image", "slack_file": {"id": u["file_id"]}, "alt_text": Path(a.image).stem}]
    if a.thread:
        body["thread_ts"] = a.thread
    r = api("chat.postMessage", token, body)
    print(json.dumps({"ok": r.get("ok"), "error": r.get("error"), "ts": r.get("ts")}, ensure_ascii=False))
