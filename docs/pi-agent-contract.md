# PI-Agent 契约

PI agent 是一个薄调度层。它负责协调任务，但不应该把策略和领域 workflow 隐藏在
临时 prompt 里。

## 必须遵守的循环

每个任务都应按以下流程运行：

1. 识别用户真正要的 outcome。
2. 从 `skills/index.json` 选择一个 primary skill。
3. 加载对应的 `SKILL.md`。
4. 只读取任务需要的额外 references 或 source files。
5. 产出符合 schema 的 artifacts。
6. 运行 validation。
7. 写 run log。
8. 如果任务暴露了可复用改进点，提出 skill 更新。

## 输入

PI agent 应传入一个 task packet：

```json
{
  "task_id": "human-or-system-task-id",
  "requested_outcome": "plain-language outcome",
  "source_refs": [],
  "constraints": [],
  "allowed_outputs": []
}
```

## 输出

每次运行至少应产出以下一种 artifact：

- `source_manifest`
- `provision`
- `answer_packet`
- `change_packet`
- `compliance_checklist`
- `skill_run_log`

## 护栏

- 不要把 candidate 内容当成 reviewed 或 verified。
- 不要在公开 artifacts 中再分发受限标准正文。
- 如果问题依赖来源文本，不要在没有 citation 的情况下回答。
- 不要混用 draft、superseded、effective 版本而不说明。
- 不要把解释性建议说成 primary law 或 primary standard text。

## GitHub Handoff 格式

需要 GitHub 操作时，PI agent 应给 GitHub operator 一个明确请求：

```text
Please create/update repo <name>.
Push artifact <attachment or branch>.
Open issue/PR with title <title>.
Use this summary and validation log: <summary>.
```
