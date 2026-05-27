# 架构

本仓库把 agent 做薄，把可复用能力沉淀到稳定资产中。

## 分层

1. **PI-agent 调度层**
   - 接收任务。
   - 选择并加载 skill。
   - 调用工具或脚本。
   - 保存 artifact 和 run log。

2. **Skills**
   - 描述一个可复用 workflow。
   - 包含触发条件、输入、输出、边界和质量门。
   - 不把大量参考资料塞进 prompt。

3. **Schemas**
   - 定义后续 agent 和工具可以信任的持久化产物。
   - 让输出可 diff、可 review、可被 CI 检查。

4. **Examples**
   - 提供最小 synthetic fixture。
   - 不包含受限标准正文。

5. **Validation**
   - 检查 skill metadata、schema 文件和 JSON/JSONL artifacts。
   - 按 `schemas/*.schema.json` 对 examples/demos 做 schema-aware validation。
   - 对 demo 做 artifact integrity checks，例如 coverage count 和 citation 引用一致性。
   - 防止产物契约悄悄漂移。

## 为什么不做重 Agent

`standards-llm-wiki` 证明了这个领域需要 provenance、版本安全、条款级建模和 eval。
这些应该是长期资产，而不是塞进一个常驻大 agent 的临时上下文里。

目标运行模型是：

```text
task -> PI agent -> skill -> code/schema/data -> validated artifact -> run log
```

只要遵守 `docs/pi-agent-contract.md`，PI agent 本身可以替换。
