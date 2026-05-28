# 私有来源测试

真实标准 PDF、授权文本和企业内部材料应放在私有目录中处理，不应提交到公开仓库。
本仓库默认忽略 `private/`、`private-sources/` 和 `private-runs/`。

## 推荐流程

1. 把授权 PDF 放入 `private-sources/`。
2. 用本地工具转换为文本，例如：

```bash
mkdir -p private/gb-pdf-text
pdftotext -layout private-sources/GB_7258-2017.pdf private/gb-pdf-text/GB_7258-2017.txt
```

3. 运行抽取质量检查：

```bash
standards-skills inspect-corpus \
  --text-dir private/gb-pdf-text \
  --output private-runs/corpus-inspection.json \
  --json
```

4. 只把统计、schema、工具或脱敏后的 synthetic artifact 提交到公开仓库。
5. 需要公开展示时，使用 metadata、locator、短引用策略和 paraphrased/synthetic demo。

## 私有条款索引

抽取质量可用后，可以生成不含正文的条款索引：

```bash
standards-skills index-corpus \
  --text-dir private/gb-pdf-text \
  --output private-runs/provision-index.jsonl \
  --json
```

默认输出字段包括：

- `provision_id`；
- `source_file`；
- `clause_number`；
- `locator`；
- `line_number`；
- `source_quality`；
- `text_included=false`。

默认会跳过 `needs_review` 和 `poor` 的文件。确需在私有环境中进一步诊断时，可以加
`--include-needs-review`。确需输出标题文本时，可以加 `--include-heading-text`，但这类
输出应继续留在私有目录中。

为了降低目录、表格和列表项造成的假阳性，默认索引规则会：

- 跳过 `0` 或前导 `0` 编号；
- 每个文件的顶层编号只保留首次出现；
- 每个文件的同一条款编号只保留首次出现；
- 继续保留 `4.1`、`4.1.1` 这类层级编号。

## 报告边界

`inspect-corpus` 只输出文件级统计：

- 行数和非空行数；
- 字符数；
- 疑似条款编号数量；
- 疑似字体映射/乱码字符数量；
- `usable`、`needs_review` 或 `poor` 抽取质量标记。

报告不包含标准正文，不替代 OCR、人工校对、版权审查或合规判断。
