---
name: regulatory-answer
description: 用带 citation 的 answer packet 回答标准、法规、政策通知、条款、适用性、日期、例外和合规影响问题。用于 PI agent 需要生成可追溯答案、版本安全说明和 unresolved issues 的场景。
---

# Regulatory Answer

使用这个 skill，从结构化 provisions 和 source manifests 回答用户或 workflow 问题。

## Workflow

1. 先把问题重述为带 scope 的查询：jurisdiction、document family、
   product/process、date 和 version constraints。
2. 优先搜索 reviewed 或 verified provisions。
3. 只有在明确允许时才使用 candidate provisions，并把答案标记为 provisional。
4. 区分 primary source text、interpretation 和 workflow recommendation。
5. 生成 answer packet，包含 citations、conditions、exceptions、version status、
   confidence 和 unresolved issues。
6. 如果来源覆盖不完整，说明缺什么，不要猜。

## Quality Gate

- 每个规范性回答至少有一个 citation。
- 版本状态必须明确。
- 条件和例外不得遗漏。
- 答案不得声称法律意见或认证签字。

## Output

使用 `schemas/answer-packet.schema.json`。
