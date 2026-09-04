#!/usr/bin/env python3
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required in GitHub Actions", file=sys.stderr)
    raise

repo = os.environ["GITHUB_REPOSITORY"]
token = os.environ["GITHUB_TOKEN"]
labels_path = Path(".github/labels.yml")
labels = yaml.safe_load(labels_path.read_text()) or []

base = f"https://api.github.com/repos/{repo}/labels"
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28",
    "Content-Type": "application/json",
}

def request(method, url, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode()
            return resp.status, json.loads(body) if body else None
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="ignore")
        if e.code == 404:
            return 404, body
        if e.code == 422:
            return 422, body
        raise RuntimeError(f"{method} {url} failed: {e.code} {body}") from e

for item in labels:
    name = item["name"]
    payload = {
        "name": name,
        "color": str(item.get("color", "ededed")).lstrip("#"),
        "description": item.get("description", ""),
    }
    url = f"{base}/{urllib.parse.quote(name, safe='')}"
    status, _ = request("GET", url)
    if status == 404:
        request("POST", base, payload)
        print(f"created {name}")
    else:
        request("PATCH", url, {"new_name": name, "color": payload["color"], "description": payload["description"]})
        print(f"updated {name}")
