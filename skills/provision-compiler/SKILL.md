---
name: provision-compiler
description: 将标准、法规和政策文档编译成条款级 provisions，并保留 citations、locators、review status 和 version metadata。用于 PI agent 需要把 source text 转成结构化 provisions、拆分条款、保留编号，或准备 reviewed knowledge artifacts 的场景。
---

# Provision Compiler

完成 source intake，并确认允许处理 source content 后，使用这个 skill。

## Workflow

1. 确认 source manifest 允许当前处理方式。
2. 保留文档层级：part、chapter、section、clause、annex、table、figure、note。
3. 按逻辑 provision 拆分，不按任意 token chunk 拆分。
4. 尽可能用 document family 和 clause locator 分配稳定 ID。
5. 除非经过人类或批准的 review step，否则 `review_status` 保持 `candidate`。
6. 记录 source locator、version status、effective date 和 extraction notes。
7. 产出符合 `schemas/provision.schema.json` 的 records。

## Quality Gate

- 每条 provision 都有 source ID 和 locator。
- 条件和例外必须靠近对应规范性表述。
- 表格和附录如果抽取置信度低，必须标记。
- Candidate provisions 不得混入 final answers，除非显式允许。

## Output

使用 `schemas/provision.schema.json`。
