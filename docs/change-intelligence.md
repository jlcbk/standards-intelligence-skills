# 变更情报

Change intelligence 的目标是把来源更新整理成可 review 的 change packet。
除非 packet 里有已 review 的证据，否则它不能声称法律或技术要求已经发生实质变化。

## 基本假设

- Source manifest 是状态、日期、官方 locator 和替代关系的第一层事实来源。
- 一个 document family 可能有多个版本、草案、替代版本或计划修订。
- 公开仓库默认只保存 metadata-level change packet。
- Provision-level diff 应放在私有 BYOD 处理流程中，除非源文本明确可公开再分发。

## 推荐流程

1. 刷新 source manifest metadata。
2. 比较状态、日期、替代关系和官方 locator。
3. 如果有授权文本，按稳定 locator 比较 provisions。
4. 将变化分类为 metadata refresh、new version、replacement、provision change、
   withdrawal 或 unknown。
5. 为低置信度或高影响变化生成 review tasks。
6. 明确保留 unresolved issues。

## Version Graph 字段

Change packet 应保留：

- old/new document ID；
- old/new source ID；
- 关系类型；
- old/new status；
- 已知时记录 old/new effective date；
- 证据 locator。

## Watchlist 字段

后续 watchlist record 建议包含：

- source ID；
- 官方 URL；
- 检查频率；
- last checked time；
- last seen status；
- last seen hash 或 metadata fingerprint；
- next review task。
