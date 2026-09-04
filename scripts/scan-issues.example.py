#!/usr/bin/env python3
"""Example scanner skeleton for exam issue pool.

真实运行时需要环境变量：
- GITHUB_TOKEN：只限本需求池仓库的 fine-grained PAT
- GITHUB_REPOSITORY：例如 TaliaTan/octo-server-agent-exam-pool

本脚本是模板，不会默认发 Octo 群消息。
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

repo = os.environ.get("GITHUB_REPOSITORY", "TaliaTan/octo-server-agent-exam-pool")
token = os.environ.get("GITHUB_TOKEN")
state_path = Path("state/github-issue-scan-state.json")

if not token:
    print("missing GITHUB_TOKEN", file=sys.stderr)
    sys.exit(2)

req = urllib.request.Request(
    f"https://api.github.com/repos/{repo}/issues?state=all&per_page=100&sort=updated&direction=desc",
    headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    },
)
with urllib.request.urlopen(req, timeout=30) as resp:
    issues = json.load(resp)

old = json.loads(state_path.read_text()) if state_path.exists() else {"issues": {}}
new = {"repo": repo, "issues": {}}
changes = []

for issue in issues:
    if "pull_request" in issue:
        continue
    num = str(issue["number"])
    labels = sorted([l["name"] for l in issue.get("labels", [])])
    item = {
        "updated_at": issue["updated_at"],
        "state": issue["state"],
        "labels": labels,
        "comments": issue.get("comments", 0),
        "title": issue["title"],
        "url": issue["html_url"],
    }
    prev = old.get("issues", {}).get(num)
    if prev and item != prev:
        changes.append({"number": num, "before": prev, "after": item})
    elif not prev:
        changes.append({"number": num, "before": None, "after": item})
    new["issues"][num] = item

state_path.parent.mkdir(parents=True, exist_ok=True)
state_path.write_text(json.dumps(new, ensure_ascii=False, indent=2))

# 考试规则：无变化保持静默。
if changes:
    print(json.dumps(changes, ensure_ascii=False, indent=2))
