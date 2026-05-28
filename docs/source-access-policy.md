# 来源访问策略

标准和法规材料经常同时涉及公开 metadata、受限全文、付费标准和企业私有资料。
本仓库默认采用保守公开边界。

## 访问级别

- `public_web`：公开官方网页或通知。
- `public_metadata`：metadata 公开，但全文不在公开仓库再分发。
- `restricted_standard`：付费、授权或访问受控标准。
- `private_document`：企业或用户提供的私有文件。
- `unknown`：访问状态尚未核实。

## 再分发策略

- `public_ok`：内容可以公开保存。
- `metadata_only`：公开仓库只保存 metadata 和 locator。
- `private_processing_only`：只能在私有工作区处理全文。
- `do_not_store`：不持久化内容。
- `unknown`：未 review 前阻止公开发布。

## 默认规则

1. 公开仓库保存 source metadata、locator、hash 和 run log，不保存受限标准全文。
2. 受限标准按 BYOD 模式在私有环境处理。
3. 公开 examples 必须是 synthetic、public-domain 或明确可再分发内容。
4. 每条 source manifest 都必须包含 access 和 redistribution 字段。
5. 如果授权状态不确定，先按 `metadata_only` 或 `private_processing_only` 处理。
6. 私有 PDF、OCR/text extraction output 和真实 review notes 应放在 `private/`、
   `private-sources/` 或 `private-runs/`，不进入公开仓库。
7. 不包含正文的 corpus inspection report 可以公开保存，用于说明抽取质量和测试边界。
