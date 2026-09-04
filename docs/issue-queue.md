# Agent Issue Queue

本仓库支持一种最小权限建 issue 方式：Agent 不需要 GitHub PAT，也不直接调用 Issues API。

流程：

1. Agent 在 `.agent/issue-queue/<id>.json` 写入 issue 请求。
2. Agent 用 Deploy Key push 到本仓库。
3. GitHub Actions 使用仓库内置 `GITHUB_TOKEN` 创建 issue。
4. workflow 会用隐藏 marker `<!-- octo-agent-issue-id:<id> -->` 去重，避免重跑重复建单。

JSON 示例：

```json
{
  "id": "20260904-001",
  "title": "[Bug] 群消息搜索返回不可见消息",
  "labels": ["type/bug", "priority/P1", "status/new", "source/octo-group"],
  "body": "## 用户原话\n> ...\n\n## 现象\n...\n"
}
```

限制：

- workflow 只负责创建 issue，不会删除 queue 文件。
- 重复运行通过 body marker 去重。
- 需要仓库 Actions 可用，且 workflow permissions 允许 `issues: write`。
