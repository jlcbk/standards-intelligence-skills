# Standards Intelligence Skills

`standards-intelligence-skills` 是一个面向标准/法规智能处理的轻量级
skill pack。它的目标不是再做一个很重的常驻 agent，而是把能力拆成：
薄的 PI agent 调度层 + 可复用 skills + 可验证 schemas + 可持续沉淀的数据产物。

这个项目继承 `standards-llm-wiki` 的核心经验：标准/法规场景真正有价值的不是
“把 PDF 丢给大模型聊天”，而是条款级结构化、来源可追溯、版本安全、答案可验证、
流程可复用。

## 核心思路

这个仓库采用 “fat skills, thin harness” 结构：

- **薄 PI agent**：只负责接收任务、选择 skill、调用工具、写 run log。
- **厚 skills**：把领域流程、边界、输入输出和质量门写进 `skills/*/SKILL.md`。
- **厚数据**：把 source manifest、provision、answer packet、change packet、
  checklist、run log 等产物保存为 JSON/JSONL。
- **厚代码**：把重复验证、转换和检查沉淀到 CLI/脚本中，避免每次靠 prompt 重写。

## 当前能力

当前版本提供五类核心 workflow：

1. `source-intake`：登记来源，并明确访问权限和公开再分发边界。
2. `provision-compiler`：把文档整理成条款级 provision。
3. `regulatory-answer`：生成带引用、带版本安全说明的 answer packet。
4. `change-impact`：把来源或版本变化整理成 change packet。
5. `compliance-checklist`：把条款映射成控制项、证据和负责人。

当前持久化产物包括 source manifest、provision、answer packet、change packet、
document family、source watchlist、coverage report、compliance checklist、task packet、
private corpus inspection report 和 skill run log。

本仓库不会放受限标准 PDF 原文，也不会放大段标准正文。公开示例使用官方 metadata
和 synthetic/paraphrased demo artifacts。

## 仓库结构

```text
skills/       可复用 PI-agent skills
schemas/      JSON Schema 产物契约
examples/     小型 synthetic 示例
demos/        端到端 demo 包，保留安全来源边界
docs/         架构、PI-agent 契约、策略和路线图
src/          小型 stdlib CLI
tests/        验证测试
```

## 快速开始

```bash
python3.10 -m venv .venv
. .venv/bin/activate
pip install -e .
standards-skills list
standards-skills validate
standards-skills check-sources --as-of 2026-05-27
standards-skills inspect-corpus --text-dir private/gb-pdf-text --json
standards-skills index-corpus --text-dir private/gb-pdf-text --output private-runs/provision-index.jsonl
standards-skills run-task --packet examples/task-packet.example.json --validate
python -m unittest discover -s tests
```

不安装包也可以直接运行：

```bash
PYTHONPATH=src python -m standards_intelligence_skills.cli list
PYTHONPATH=src python -m standards_intelligence_skills.cli validate
```

`standards-skills validate` 会做 schema-aware validation：检查 skill metadata、
schema 文件基本形态，并把 `examples/` 与 `demos/` 中的 JSON/JSONL artifact 按
`schemas/*.schema.json` 校验。当前实现覆盖本仓库使用的 JSON Schema 子集：
`type`、`required`、`properties`、`items`、`enum` 和 `additionalProperties`。
对 demo 还会做 artifact integrity checks：coverage count 必须匹配 JSONL 行数，
answer/checklist citation 必须引用存在的 provision/source，provision 的 `source_id`
也必须存在于 source manifest。

`standards-skills check-sources` 会读取 demo 的 source watchlist，并按指定日期判断
metadata source 是否到期需要复核。默认只报告；如果要在 CI 中卡住到期项，可以加
`--fail-on-due`。

`standards-skills inspect-corpus` 用于私有 BYOD 文本抽取质量检查。它只输出统计和质量标记，
不输出标准正文。

`standards-skills index-corpus` 用于私有 BYOD 条款索引。默认只输出条款编号、源文件、
行号和 locator，不输出条款正文或 heading text。

## PI Agent 使用方式

1. 读取任务，并从 `skills/index.json` 选择一个主要 skill。
2. 加载对应的 `SKILL.md`。
3. 产出符合 `schemas/*.schema.json` 的结构化 artifact。
4. 运行 `standards-skills validate`。
5. 使用 `standards-skills new-run-log` 或 `standards-skills run-task` 写 run log。
6. 如果任务暴露了可复用经验，更新对应 skill 或 schema。

更多说明：

- [docs/pi-agent-contract.md](docs/pi-agent-contract.md)
- [docs/pi-agent-runner.md](docs/pi-agent-runner.md)
- [docs/private-source-testing.md](docs/private-source-testing.md)

## Demo

第一个 demo 是 [demos/gb-vehicle-safety](demos/gb-vehicle-safety)。

它登记了 GB 7258-2017 和 GB 1589-2016 的官方 metadata，并用
synthetic document families、source watchlists、provisions 和 answer packets 跑通工作流。这个 demo
不存储标准 PDF 原文，也不声称提供权威合规结论。

## 安全边界

本项目是研究和工作流辅助工具，不是法律意见、认证结论或标准全文公开分发平台。
默认规则是：公开仓库只保存 metadata、locator、schema、demo 和可审计 workflow；
受限标准或企业内部资料应在私有 BYOD 环境中处理。

详见 [docs/source-access-policy.md](docs/source-access-policy.md)。

## 许可证

MIT，详见 [LICENSE](LICENSE)。
