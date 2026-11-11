---
name: alphagbm-restore
description: 从 AlphaGBM 本地记录恢复研究或决策上下文，保留旧版本和当时信息集。
metadata:
  version: "0.1.0"
  author: AlphaGBM
---

# AlphaGBM 恢复

## 恢复顺序

读取索引 → 选择记录版本 → 展示创建时间和数据截止时间 → 分离当时事实与后来新增信息 → 列出未解决问题 → 等用户确认后继续推理。

## 防止后见之明

旧报告的结论、来源和未知项不可静默改写。若要更新，创建新版本并说明新增证据、被推翻的判断及原因。
