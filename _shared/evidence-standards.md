# AlphaGBM 证据标准

## 断言分层

每个关键句先标记类型，再写结论：

- `FACT`：来源直接陈述或可由原始数据复算的事实。
- `MANAGEMENT`：管理层在公告、演示或电话会中的表述；不得直接等同于事实。
- `MARKET`：公开市场参与者、媒体或分析师的观点；说明是谁、何时、基于什么。
- `MODEL`：由数据和假设计算得到的结果；列出公式、输入、版本和敏感性。
- `INFERENCE`：agent 的推断；必须写出证据链、替代解释和可证伪条件。
- `UNKNOWN`：尚未取得足够证据，保留问题而不是猜测。

## 最小证据卡

```yaml
claim_id: C-001
claim_type: FACT
statement: ""
source:
  publisher: ""
  title: ""
  url: ""
  published_at: ""
  accessed_at: ""
  locator: "page 4 / paragraph 2 / table row"
  source_tier: 1
quote_or_data: ""
supports: []
contradicts: []
confidence: high
notes: ""
```

## 引用规则

- 关键事实必须可从原文定位；只有搜索摘要时标记 `UNKNOWN`。
- 电话会内容应注明是官方录音/逐字稿还是第三方转录。
- 公开报道应保留发布日期，避免把后见之明写入事件时点。
- 同一断言有冲突来源时并列展示，不静默选择更顺眼的一条。
- 引用不等于认同；来源的观点、利益关系和方法限制要单独说明。

