# GB 车辆安全 Demo

这个 demo 用来跑通第一条垂直 workflow：

```text
source-intake -> provision-compiler -> regulatory-answer -> coverage report
```

Demo 使用两条官方 source metadata：

- GB 7258-2017：`机动车运行安全技术条件`
- GB 1589-2016：`汽车、挂车及汽车列车外廓尺寸、轴荷及质量限值`

官方 metadata 来源于全国标准信息公共服务平台：

- <https://std.samr.gov.cn/gb/search/gbDetailed?id=71F772D81CEDD3A7E05397BE0A0AB82A>
- <https://std.samr.gov.cn/gb/search/gbDetailed?id=71F772D8118AD3A7E05397BE0A0AB82A>

## 边界

这个 package 不保存 PDF 文件，也不保存大段标准原文。这里的 provisions 和 answer packets
都是 synthetic/paraphrased demo artifacts，只用于测试仓库 workflow 和 schema 形态。
它们不是权威合规内容。

适合用于：

- 测试 skill selection；
- 测试 JSON/JSONL artifact validation；
- 演示 citation-shaped answer packets；
- 证明公开 metadata 和私有/BYOD 全文处理可以安全共存。

不适合用于：

- 法律意见；
- 车辆合规决策；
- 认证结论；
- 声称 GB 7258 或 GB 1589 的精确要求。
