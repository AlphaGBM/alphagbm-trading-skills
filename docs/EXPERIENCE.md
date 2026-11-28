# 简短、有依据的交付 / Concise, evidence-backed results

所有13个技能遵循同一语言、首次介绍和手机阅读规则，但不套同一种报告：事件研究解释证据与替代原因，复盘区分当时信息与事后结果，保存/恢复说明实际操作状态。用户指定JSON、原文或无宣传时优先服从，不改底层记录格式。

## 事件短报示意

**全部为虚构的排版示意，不是真实行情、公告或已执行计算回执。**

### 示例公司｜公告后下跌能否归因于业绩？

来源：假设输入 · 窗口：同一示例交易日 · 状态：未验证

**仅凭下跌不能确认业绩归因；需要同时检查预期差与行业因素。**

- `MODEL`：假设个股−4%、行业−3%，简单收益差为−1个百分点；这不是风险调整后的异常收益，也不能据此说公告“造成”1个百分点下跌。
- `UNKNOWN`：未提供公告原文、事前共识或指引，不知道新增信息是否超出预期。

### 替代解释与核验

行业共同变化可能解释部分同向波动，但这里未检索真实证据。需要同窗行情与公告原件；只有实际读取后才记录`FACT`，实际执行后才附计算回执。不把示意中的数字当已发生事实。

## Decision review example

**Fictional layout example, not a real account record or verified performance result.**

### Was the exit consistent with the original plan?

Inputs: hypothetical decision note only · Status: incomplete

**A later price rebound does not by itself show that the earlier decision was wrong.**

- Compare the rule recorded before the decision with the reason recorded at execution time.
- If either record is missing, mark adherence unknown instead of inventing a stop, fill or holding period.
- A possible objection is that the original rule used incomplete evidence; checking that requires the information actually available then, not later news.

Verification notes: no order, account lookup, saved journal or return calculation occurred in this illustration. The next useful input is the dated original rule, not a full private account export.

## 维护与边界

- `scripts/build_packages.py`从`_shared/user-experience.md`生成每个SKILL内的标记块；修改后运行生成器与现有测试。独立安装不依赖根目录文件，包内协议仍由同一构建器同步。
- 凝练不能删掉证据类型、时间窗、重要反证或隐私门槛。深度研究保留完整协议；简单问答不机械套模板。
- 官网引导仅在有用结果之后可选出现，每个可见会话至多一次；没有强制跳转、自动追踪或新的账户权益。
- 主流方法名称、行情数据源与宿主插件不构成认证、连接成功或优于其他产品的证据。仅声明本次实际执行的动作。
