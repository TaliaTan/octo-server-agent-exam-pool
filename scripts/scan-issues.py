#!/usr/bin/env python3
"""Scan issue changes and print a concise report when changed.

Env:
- GITHUB_REPOSITORY: owner/repo, default TaliaTan/octo-server-agent-exam-pool
- GITHUB_TOKEN: optional; unauthenticated works for public repo but lower rate limit.
- STATE_PATH: default state/github-issue-scan-state.json
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

repo = os.environ.get("GITHUB_REPOSITORY", "TaliaTan/octo-server-agent-exam-pool")
token = os.environ.get("GITHUB_TOKEN")
state_path = Path(os.environ.get("STATE_PATH", "/home/mlclaw/.openclaw/workspace/octo-exam/state/github-issue-scan-state.json"))
url = f"https://api.github.com/repos/{repo}/issues?state=all&per_page=100&sort=updated&direction=desc"
headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
if token:
    headers["Authorization"] = f"Bearer {token}"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=30) as resp:
    remaining = resp.headers.get("X-RateLimit-Remaining")
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
    if prev is None:
        changes.append(f"新增 issue #{num}: {item['title']}\n{item['url']}")
    elif item != prev:
        diffs = []
        for k in ["state", "labels", "comments", "updated_at"]:
            if item.get(k) != prev.get(k):
                diffs.append(f"{k}: {prev.get(k)} -> {item.get(k)}")
        changes.append(f"更新 issue #{num}: {item['title']}\n" + "\n".join(diffs) + f"\n{item['url']}")
    new["issues"][num] = item

state_path.parent.mkdir(parents=True, exist_ok=True)
state_path.write_text(json.dumps(new, ensure_ascii=False, indent=2))

if changes:
    print("需求池有更新：")
    print("\n\n".join(changes[:10]))
    if len(changes) > 10:
        print(f"\n还有 {len(changes)-10} 条更新未展开。")
else:
    # Silent by default; print to stderr for cron logs only.
    print(f"no changes; rate_remaining={remaining}", file=sys.stderr)
