# PM 链路

```text
收到反馈
  ↓
判断类型与优先级
  ↓
创建 issue + labels
  ↓
Feature：补 What-only PRD
  ↓
标记 pm/review-needed + status/in-review
  ↓
定时扫描 reviewer 评论 / labels / state
  ↓
通过：status/accepted
打回：status/rework → 修订 PRD → status/in-review
关闭：按真实结论同步 closed / wontfix
```

## 回群规则

- 有真实变化才回群。
- 没有变化不发“正在检查 / 无更新 / 一切正常”。
- 主动回群必须 @ 对应人和 @ 主考。
- 结论必须如实：已修复 ≠ 没复现 ≠ 不做。
