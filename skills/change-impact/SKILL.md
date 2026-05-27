---
name: change-impact
description: 分析标准、法规、政策通知和文档版本之间的变化。用于 PI agent 需要检测来源变化、比较版本、识别受影响 provisions/topics/entities，或准备 change impact packet 的场景。
---

# Change Impact

当 source、version 或 document family 发生变化时，使用这个 skill。

## Workflow

1. 确认 old/new source manifest records。
2. 读取已有 document family / version graph；没有时先生成 metadata-level 草稿。
3. 先比较 document metadata：issuer、status、publication date、effective date、
   replacement relation 和 official locator。
4. 读取 source watchlist；如果 `check-sources` 显示到期，先生成 metadata refresh review task。
5. 如果有授权文本，先按稳定 locator 比较 provisions，再考虑 semantic similarity。
6. 将变化分类为 added、removed、modified、renumbered、clarified 或 unknown。
7. 识别受影响 topics、entities、controls、evidence 和 answer packets。
8. 为高风险或低置信度变化生成 review tasks。

## Quality Gate

- 没有证据时，不要把变化标记为 substantive。
- 保留 old/new citations。
- 遇到 replacement 和 effective-date 不确定性要升级。
- 如果影响 compliance evidence，要生成 review tasks。

## Output

Version graph 使用 `schemas/document-family.schema.json`，watchlist 使用
`schemas/source-watchlist.schema.json`，具体变化使用 `schemas/change-packet.schema.json`。

公开 metadata-only demo 可以描述 source status、replacement relation、retrieval
或 watchlist 变化，但不要引用标准正文。私有 BYOD 运行可以在授权允许时包含
provision-level diff summaries。
