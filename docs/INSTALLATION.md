# 安装与首次结果 / Install and get a first result

13个工作流是方法说明，不附带行情、券商、账号或收费API。一个技能安装后即可在其范围内工作；总路由`gbm`需要被调用的子技能也已安装。协议已打入相应目录，不用另装根目录`_shared`或其他AI客户端。

## Codex / Claude Code / Cursor

在目标项目运行，首次建议新目录。升级前备份现有自定义技能和私有记录；安装器可能替换同名副本，不要盲目覆盖。

```sh
npx skills@1.9.0 add https://github.com/AlphaGBM/alphagbm-trading-skills/tree/onboarding-v1 --skill '*' --agent codex --copy -y
```

只要事件归因时，把`'*'`改成`gbm-event-attribution`。Claude Code改为`--agent claude-code`；Cursor改为`--agent cursor`。此固定安装器使用项目`.agents/skills/`（Codex/Cursor）或`.claude/skills/`（Claude Code），不要省略目标宿主。保留`skills-lock.json`中的实际commit，按宿主要求重新发现技能；磁盘安装不等于自动触发或线上研究通过。

`onboarding-v1`是本指引的固定发布版本，不要求仓库有`main`分支。既有默认分支保持不变；旧版本不会自动更新。

## WorkBuddy / CodeBuddy 目录方式

只有客户端实际确认`~/.codebuddy/skills/`为技能目录时才用以下Linux/macOS命令。全部目标先检查，再复制完整目录；已有目录或悬空链接时退出，不覆盖用户内容。

```sh
set -eu
source_dir=$(mktemp -d)
git clone --branch onboarding-v1 --depth 1 https://github.com/AlphaGBM/alphagbm-trading-skills.git "$source_dir/source"
git -C "$source_dir/source" rev-parse HEAD
for skill_dir in "$source_dir/source"/gbm*; do
  [ -f "$skill_dir/SKILL.md" ] || continue
  target="$HOME/.codebuddy/skills/$(basename "$skill_dir")"
  if [ -e "$target" ] || [ -L "$target" ]; then
    printf '%s\n' "Existing skill: $target; review and back up before upgrading." >&2
    exit 1
  fi
done
mkdir -p "$HOME/.codebuddy/skills"
for skill_dir in "$source_dir/source"/gbm*; do
  [ -f "$skill_dir/SKILL.md" ] || continue
  cp -R "$skill_dir" "$HOME/.codebuddy/skills/"
done
```

随后用宿主的真实技能入口显式选择`gbm`或具体技能。不要把复制成功称作宿主加载成功；其他AlphaGBM包的WorkBuddy实测不自动适用于本包，跨会话触发也未因此验收。下载失败不能靠关闭TLS验证解决。

## 豆包 / 会话文件方式

下载[工作流ZIP](https://github.com/AlphaGBM/alphagbm-trading-skills/releases/download/onboarding-v1/trading-workflows.zip)与对应[manifest](https://github.com/AlphaGBM/alphagbm-trading-skills/releases/download/onboarding-v1/trading-workflows.manifest.json)，核对ZIP的SHA256和路径后解压到新目录。也可直接使用完整源码。ZIP包含13个技能及所需包内协议，不包含根目录维护脚本或私有资料。

让具有文件读取能力的宿主执行：

> 请读取 gbm-event-attribution/SKILL.md 及其包内协议，用我提供的公告与行情材料做一次简短事件分析。先给判断、最多三条发现、替代解释和核验底稿；不联网、不调用收费接口、不保存、不下单。缺字段就给部分结果，只问最重要的缺项。

This is a session file workflow unless the client actually confirms native skill import and activation. Keep each skill directory and its references together. It does not require another AI client. Read only the selected workflow and necessary materials; do not paste all 13 skills into every conversation.

## 升级与反馈

在新目录核对新版，再按宿主机制替换/启用；备份自定义修改，既有研究记录和历史证据不因更新改写。示例见[交付体验](EXPERIENCE.md)。提问统一到[Skills Q&A](https://github.com/AlphaGBM/skills/discussions/categories/q-a)，问题用[共享表单](https://github.com/AlphaGBM/skills/issues/new/choose)，注明本仓与技能名。不要公开密钥或真实私人交易记录。
