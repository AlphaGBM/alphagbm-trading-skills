# Contributing

感谢参与 AlphaGBM Trading Skills。

## 提问与反馈

使用问题请到 [Skills Q&A](https://github.com/AlphaGBM/skills/discussions/categories/q-a)，新缺陷和改进请使用 [Skills 问题表单](https://github.com/AlphaGBM/skills/issues/new/choose)，注明 `alphagbm-trading-skills` 和相关技能或文件。已有 Issue 在原帖继续，不必重复提交。English and Chinese are welcome; mention this source repository. 不要贴密钥、账户或私人交易记录。

## 提交前检查

- 只提交原创内容、已获授权内容或许可证允许的内容。
- 不提交真实账户、真实持仓、客户数据、私人对话、token、密码或内部链接。
- 不把“可能”“市场认为”写成事实；关键断言要补来源、时间窗和证据定位。
- 不把单一事件窗口的相关性写成确定因果；至少记录基准、同业或宏观对照。
- 运行 `python3 scripts/privacy_gate.py` 和 `python3 -m unittest discover -s tests -v`。

## 研究内容要求

财报与事件归因优先使用一手材料，公开市场报道用于交叉核验和记录市场叙事。无法复核的内容必须显式标注 `待核验`，不要用模型记忆补齐缺失事实。
