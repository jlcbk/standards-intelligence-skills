---
name: source-intake
description: 登记标准、法规、政策通知和私有文档来源。用于 PI agent 需要新增或 review 来源、判断公开/私有处理边界、记录 provenance、hash/locator metadata，或在条款编译前准备 source manifest 的场景。
---

# Source Intake

使用这个 skill，在任何抽取或问答发生前先创建安全、可追溯的 source record。

## Workflow

1. 识别来源 owner、issuer、jurisdiction、document type、title、publication date、
   effective date 和 official locator。
2. 按 `docs/source-access-policy.md` 分类访问权限。
3. 分配稳定的 `source_id`。
4. 记录 retrieval metadata：URL/path、retrieved time、hash、byte size 和 extractor notes。
5. 在存储任何内容前确定 `redistribution_policy`。
6. 产出符合 `schemas/source-manifest.schema.json` 的 records。
7. 如果访问状态 unknown 或 restricted，公开 artifacts 只保存 metadata。

## Quality Gate

- 每个 source 都有 issuer 和 locator。
- 每个 source 都有 `access_level` 和 `redistribution_policy`。
- Restricted sources 不把全文放到公开路径。
- Run log 记录谁做了访问决策以及原因。

## Output

输出 JSONL records，例如：

```json
{
  "source_id": "src-demo-001",
  "title": "Synthetic vehicle safety notice",
  "source_type": "policy_notice",
  "issuer": "Example Authority",
  "jurisdiction": "EX",
  "access_level": "public_web",
  "redistribution_policy": "public_ok",
  "locator": {"url": "https://example.invalid/notice"},
  "retrieved_at": "2026-05-27T00:00:00Z"
}
```
