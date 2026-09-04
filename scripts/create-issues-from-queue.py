#!/usr/bin/env python3
"""Create GitHub issues from .agent/issue-queue/*.json.

This lets the bot use deploy-key git push only. GitHub Actions' GITHUB_TOKEN
performs the actual Issues API write inside this repository.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

repo = os.environ["GITHUB_REPOSITORY"]
token = os.environ["GITHUB_TOKEN"]
queue_dir = Path(".agent/issue-queue")
base = f"https://api.github.com/repos/{repo}"
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28",
    "Content-Type": "application/json",
}

def request(method, url, payload=None):
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode()
            return resp.status, json.loads(body) if body else None
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="ignore")
        raise RuntimeError(f"{method} {url} failed: {e.code} {body}") from e

def issue_exists(queue_id):
    # Search existing issues by hidden marker. This prevents duplicate creation if
    # a workflow is re-run for the same queue file.
    query = urllib.parse.urlencode({"q": f"repo:{repo} {queue_id} in:body type:issue"})
    _, data = request("GET", f"https://api.github.com/search/issues?{query}")
    items = data.get("items", []) if isinstance(data, dict) else []
    return items[0]["html_url"] if items else None

if not queue_dir.exists():
    print("no queue dir")
    sys.exit(0)

files = sorted(queue_dir.glob("*.json"))
if not files:
    print("no queued issues")
    sys.exit(0)

for path in files:
    item = json.loads(path.read_text())
    queue_id = item.get("id") or path.stem
    marker = f"<!-- octo-agent-issue-id:{queue_id} -->"
    existing = issue_exists(queue_id)
    if existing:
        print(f"skip existing {queue_id}: {existing}")
        continue

    title = item["title"]
    body = item.get("body", "").rstrip() + "\n\n" + marker + "\n"
    labels = item.get("labels", [])
    assignees = item.get("assignees", [])
    payload = {"title": title, "body": body, "labels": labels, "assignees": assignees}
    _, created = request("POST", f"{base}/issues", payload)
    print(f"created {queue_id}: {created.get('html_url')}")
