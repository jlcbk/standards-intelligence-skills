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

## 报告边界

`inspect-corpus` 只输出文件级统计：

- 行数和非空行数；
- 字符数；
- 疑似条款编号数量；
- 疑似字体映射/乱码字符数量；
- `usable`、`needs_review` 或 `poor` 抽取质量标记。

报告不包含标准正文，不替代 OCR、人工校对、版权审查或合规判断。
