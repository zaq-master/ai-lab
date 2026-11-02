#!/usr/bin/env python3
"""ops/agents.json からエージェントのアイコン画像（PNG）を ops/avatars/ に作る"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import report_card as rc
import matplotlib.pyplot as plt
rc.font()
A = json.load(open(Path(__file__).parent / "agents.json", encoding="utf-8"))
out = Path(__file__).parent / "avatars"; out.mkdir(exist_ok=True)
for k, a in A.items():
    fig = plt.figure(figsize=(2.56, 2.56), dpi=100); ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.add_patch(plt.Circle((.5, .5), .5, color=a["color"]))
    ax.add_patch(plt.Circle((.5, .5), .43, color="white", alpha=.12))
    ax.text(.5, .54, a["mark"], fontsize=70, color="white", ha="center", va="center", weight="bold")
    ax.text(.5, .17, ("CEO" if k == "ceo" else k), fontsize=16, color="white", ha="center", va="center", alpha=.85)
    fig.savefig(out / f"{k}.png", transparent=True); plt.close(fig)
print("ok", len(A))
