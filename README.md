# octo-server Agent Exam Pool

这是 AINOL Agent 实操考核用的需求池仓库，用于归档 octo-server 产品管家 Agent 在 Octo 群内收集到的 Bug、Feature、Question、Docs、Ops 类反馈。

> 注意：本仓库不是 `Mininglamp-OSS/octo-server` 官方 issue tracker。目标仓库在考试中只读，本仓库仅作为考试需求池和 PM 链路载体。

## Agent 工作流

1. 在 Octo 群中接收反馈或需求。
2. 判断类型：bug / feature / question / docs / ops。
3. 信息不足时先追问；信息足够时创建 GitHub issue。
4. 根据类型、优先级、状态打 labels。
5. Feature 类需求补 PRD，只写 What，不写 How。
6. 定时扫描 issues/comments/labels/state 变化。
7. 有真实变化才回 Octo 群，并 @ 对应人和 @ 主考；无变化保持静默。

## 红线

- 不写目标仓库 `Mininglamp-OSS/octo-server`。
- 不把 token、cookie、GitHub PAT、Octo 凭证写进仓库或发到群里。
- 不编造源码引用。
- PRD 不写技术实现细节。
- GitHub 限流时停止并等待 reset / Retry-After。

## Label 体系

### 类型

- `type/bug`
- `type/feature`
- `type/question`
- `type/docs`
- `type/ops`

### 优先级

- `priority/P0`
- `priority/P1`
- `priority/P2`
- `priority/P3`

### 状态

- `status/new`
- `status/triaged`
- `status/need-info`
- `status/prd-ready`
- `status/in-review`
- `status/rework`
- `status/accepted`
- `status/wontfix`
- `status/closed`

### PM 链路

- `pm/prd-needed`
- `pm/review-needed`
- `pm/reviewed`

### 来源

- `source/octo-group`
