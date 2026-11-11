---
name: alphagbm-save
description: 在用户明确要求后，将研究、事件证据包或交易记录按版本化协议安全写入本地私有目录。
metadata:
  version: "0.1.0"
  author: AlphaGBM
---

# AlphaGBM 保存

## 写入前确认

确认记录类型、目标路径、是否覆盖、隐私级别和是否允许同步。默认只新增版本，不覆盖原始快照；未明确要求时不写入真实账户数据。

## 最小检查

补齐 `record_id`、`schema_version`、创建时间、数据截止时间、来源和未知项；对缺失字段写 `UNKNOWN`，不填猜测值。写入后返回路径、版本和校验摘要。
