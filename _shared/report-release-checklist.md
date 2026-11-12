# 报告发布门禁

发布前逐项填值，不能把未执行的检查写成通过：

```yaml
source_located: yes|no|partial
direct_link_checked: yes|no
privacy_scan_ran: yes|no
synthetic_data_labeled: yes|no|not_applicable
release_status: draft|internal_review|ready
```

## 解释

- `source_located`：关键原文能按页码、段落、表行或录音时间戳找回。
- `direct_link_checked`：链接直达最终文档；搜索结果页、聚合页和失效跳转不算。
- `privacy_scan_ran`：实际运行了仓库根目录 `python3 scripts/privacy_gate.py`，没有运行就写 `no`。
- `synthetic_data_labeled`：合成案例在标题、数据表和结论中都标记，不让读者误解为真实行情。

任一关键项为 `no` 时，`release_status` 不能为 `ready`。`partial` 只能交内部审阅，并在正文列出缺口。
