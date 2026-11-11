---
name: alphagbm
description: AlphaGBM 投研与交易工作流总路由。把问题拆成事实、证据、模型、决策和结果，默认只读，不执行交易。
metadata:
  version: "0.1.0"
  author: AlphaGBM
---

# AlphaGBM 总路由

## 何时触发

用户提出研究标的、财报解释、事件归因、估值、交易复盘、持仓记录、交易能力训练或恢复历史上下文时触发。

## 首轮协议

1. 复述目标、标的、市场、时间窗和用户希望的交付物。
2. 先判断是在“向外研究”（`alphagbm-research`）、“解释事件”（`alphagbm-event-attribution`）、“做模型”（`alphagbm-model`）还是“复核自己的决策”（`alphagbm-diagnosis` / `alphagbm-trade`）。
3. 说明数据是否实时、是否一手、是否只读；缺数据就降级，不猜。
4. 输出中分开 `FACT`、`MANAGEMENT`、`MARKET`、`MODEL`、`INFERENCE`、`UNKNOWN`。
5. 任何买卖方向问题先做证据与风险复核，不直接给出下单指令。

## 路由表

| 需求 | Skill |
|---|---|
| 财报、公告、电话会后股价异动 | `alphagbm-event-attribution` |
| 标的/行业/主题研究 | `alphagbm-research` |
| 公开行情或公司基本面数据 | `alphagbm-market-research` |
| 估值、情景、压力测试 | `alphagbm-model` |
| 报告写作与证据索引 | `alphagbm-report` |
| 个人交易计划、持仓、成交复盘 | `alphagbm-trade` |
| 判断是否有证据支持 | `alphagbm-diagnosis` |
| 概念和指标解释 | `alphagbm-deconstruct` |
| 对标和方法比较 | `alphagbm-benchmark` |
| 交易能力练习 | `alphagbm-coach` |
| 保存/恢复记录 | `alphagbm-save` / `alphagbm-restore` |

## 失败处理

如果来源冲突、行情不可得、事件时间不明确或记录缺失，先列出缺口和最小补证动作，不用更强的语气掩盖不确定性。
