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

