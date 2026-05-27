# PI-Agent Runner

`standards-skills run-task` 是一个最小 runner prototype。它不执行重 agent，
只把可确定、可重复的 harness 步骤固化下来：

1. 读取 task packet；
2. 按名称选择现有 skill；
3. 可选运行仓库 schema-aware validation；
4. 写 skill run log；
5. 打印机器可读 summary。

## 示例

```bash
standards-skills run-task \
  --packet examples/task-packet.example.json \
  --validate \
  --output /tmp/standards-skill-run.json
```

## Task Packet

使用 `schemas/task-packet.schema.json`。

```json
{
  "task_id": "task-demo-001",
  "requested_outcome": "Create a citation-backed demo answer packet.",
  "skill_name": "regulatory-answer",
  "source_refs": ["demos/gb-vehicle-safety"],
  "constraints": ["public demo only"],
  "allowed_outputs": ["answer_packet", "skill_run_log"]
}
```

## 设计边界

`--validate` 会调用 `standards-skills validate`，检查 skill metadata，并把
`examples/` 与 `demos/` 中的 artifact 按对应 JSON Schema 校验。对 demo，它还会检查
coverage count 和 citation/source/provision 引用一致性。它是轻量本地质量门，不是模型评测、
法律审查或合规认证。

如果任务依赖来源新鲜度，先运行：

```bash
standards-skills check-sources --as-of 2026-06-27
```

这只检查 watchlist 到期状态，不会自动抓取外部网站。

Runner 必须保持轻量：

- 不集成模型 provider；
- 不隐藏策略逻辑；
- 不自动发布；
- 不抽取 source text。

Provider 调用、文档处理和 GitHub 操作属于独立工具或其他 agent。
这个 runner 只标准化本地 task packet 和 run log 契约。
