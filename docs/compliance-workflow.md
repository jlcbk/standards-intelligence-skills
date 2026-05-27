# 合规工作流

Compliance workflow 把 reviewed provisions 转成可以分配、举证、检查和审计的工作项。

## Checklist Item 结构

每个 checklist item 应保留：

- requirement summary；
- cited provision IDs；
- 要执行的 control/check；
- 需要收集的具体 evidence；
- owner role；
- status；
- 未解决的适用性问题；
- acceptance criteria。

## 状态模型

建议 item status：

- `todo`：尚未开始。
- `in_progress`：正在收集证据。
- `reviewed`：证据已被流程检查。
- `blocked`：缺来源文本、缺证据或缺决定。
- `not_applicable`：已说明理由并排除适用。

## 公开 Demo 边界

公开 demo checklist 只能用 synthetic provisions 展示 workflow 形态。
它不能声称某个车辆、产品或流程符合真实标准。
真实合规使用必须有授权 source text 和人类 review。

## Promotion Rule

只有满足以下条件，才能把 checklist 从 draft 提升为 approved：

1. 每个 item 都引用 reviewed 或 verified provisions；
2. 每个 item 都有具体证据，或有明确的不适用理由；
3. unresolved issues 已关闭，或由负责人明确接受。
