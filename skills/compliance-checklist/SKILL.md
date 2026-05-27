---
name: compliance-checklist
description: 将 reviewed provisions 和 requirements 转成 compliance checklist items、controls、evidence requests、owners、due dates 和 review status。用于 PI agent 需要把标准智能结果连接到实际合规工作流的场景。
---

# Compliance Checklist

使用这个 skill，把 reviewed provisions 转成可执行的合规工作项。

## Workflow

1. 默认只从 reviewed 或 verified provisions 开始，除非用户明确要求 draft checklist。
2. 抽取 requirement 字段：subject、action、object、condition、exception、
   evidence、frequency 和 responsible role。
3. 将每个 requirement 映射到一个或多个 controls。
4. 定义所需 evidence 和 acceptance criteria。
5. 跟踪 owner、due date、status 和 unresolved questions。
6. 每个 checklist item 都保留 provision citations。

## Quality Gate

- 每个 checklist item 都能追溯到 provision。
- Evidence requirements 必须具体、可检查。
- 适用性模糊时必须标记为 review。
- Draft checklist 不得声称最终合规。

## Output

使用 `schemas/compliance-checklist.schema.json`。

公开 demo 可以使用 synthetic workflow examples。生产或私有 BYOD 运行中，
checklist items 必须由 reviewed/verified provisions 支撑，并且在负责人批准前不得声称最终合规。
