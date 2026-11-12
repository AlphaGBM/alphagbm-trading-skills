# 共享记录字段

```yaml
schema_version: "1.0"
record_id: ""
created_at: ""
updated_at: ""
instrument:
  symbol: ""
  market: ""
  currency: ""
event:
  kind: "earnings|guidance|filing|macro|corporate_action|other"
  occurred_at: ""
  timezone: ""
evidence: []
assumptions: []
unknowns: []
publication_checks:
  source_located: "yes|no|partial"
  direct_link_checked: "yes|no"
  privacy_scan_ran: "yes|no"
  synthetic_data_labeled: "yes|no|not_applicable"
decision:
  action: "observe|research|hold|exit|other"
  rationale: ""
  invalidation: []
  risk_notes: []
outcome:
  status: "open|closed|not_applicable"
  observed_at: ""
  notes: ""
```

不要求每次填满所有字段，但不得把未知字段伪装成空字符串意义上的已知事实。

`unknowns` 和 `assumptions` 是非空字符串列表。`evidence` 中每个 `claim_id` 必须唯一；每条证据都要有可定位来源。`FACT` 还必须有 `quote_or_data`，来源至少包含 `publisher`、`title`、`url`、`published_at`、`accessed_at`、`locator` 和 1–4 的 `source_tier`。计算结果用 `MODEL`，市场观点用 `MARKET`，不可混写。
