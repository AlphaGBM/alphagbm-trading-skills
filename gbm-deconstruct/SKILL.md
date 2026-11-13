---
name: gbm-deconstruct
description: AlphaGBM 金融概念拆解。用户输入 /gbm-deconstruct，或要求解释 EPS、百分比与百分点、负基数增长、期权或其他指标机制时使用；给定义、单位、合成例子与失效边界。需要当前行情时转 gbm-market-research。
metadata:
  version: "0.2.0"
  author: AlphaGBM
---

# AlphaGBM 概念拆解

## 六段式

一句话定义 → 计算/机制 → 何时有用 → 何时失效 → 常见误解 → 一个带单位和时间窗的合成例子。遇到财报指标必须说明会计口径和非 GAAP 调整。

## 精确性

不把相关性写成因果，不把理论最大损失写成实测风险，不把管理层目标写成已实现结果。用户需要实时数字时转到 `gbm-market-research`。
