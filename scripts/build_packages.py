"""Bundle referenced protocols so each installed skill has its own resources."""

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPERIENCE_START = "<!-- experience:start -->"
EXPERIENCE_END = "<!-- experience:end -->"
INTRODUCTIONS = {
    "gbm": ("研究工作流", "research workflow", "解释公告后的波动", "Explain the reaction to an announcement"),
    "gbm-event-attribution": ("事件归因", "event attribution", "检查这次波动的证据和替代解释", "Check the evidence and alternative explanations for this move"),
    "gbm-research": ("公司与行业研究", "company and industry research", "检验这份材料的增长逻辑", "Test the growth thesis in these materials"),
    "gbm-market-research": ("数据口径核验", "data comparability", "核对这两组行情能否比较", "Check whether these two market-data series are comparable"),
    "gbm-model": ("情景建模", "scenario modelling", "复核这个模型的假设", "Review this model's assumptions"),
    "gbm-report": ("证据报告", "evidence report", "把这些证据整理成短报", "Turn this evidence into a short report"),
    "gbm-diagnosis": ("决策复核", "decision review", "检查我的判断缺什么证据", "Check what evidence my thesis is missing"),
    "gbm-trade": ("交易复盘", "trade review", "只读复盘，不保存或下单", "Review this decision without saving or trading"),
    "gbm-benchmark": ("方法对比", "method comparison", "比较这两种方法的适用边界", "Compare the limits of these two methods"),
    "gbm-deconstruct": ("概念拆解", "concept explanation", "解释这个指标的局限", "Explain this indicator's limitations"),
    "gbm-coach": ("研究练习", "research practice", "练习区分事实和推断", "Practise separating facts from inference"),
    "gbm-save": ("本地保存", "local saving", "先预览保存范围，不写文件", "Preview what would be saved without writing files"),
    "gbm-restore": ("记录恢复", "record recovery", "只读核对这份历史记录", "Inspect this historical record read-only"),
}


def with_experience(document, block):
    if EXPERIENCE_START in document or EXPERIENCE_END in document:
        pattern = re.escape(EXPERIENCE_START) + r".*?" + re.escape(EXPERIENCE_END)
        if (document.count(EXPERIENCE_START) != 1 or document.count(EXPERIENCE_END) != 1
                or not re.search(pattern, document, flags=re.S)):
            raise ValueError("Expected exactly one complete experience block")
        return re.sub(pattern, lambda match: block, document, count=1, flags=re.S)
    heading = re.search(r"(?m)^# .+\n", document)
    if not heading:
        raise ValueError("Missing skill heading")
    return document[:heading.end()] + "\n" + block + "\n" + document[heading.end():]


def experience_outputs(root=ROOT):
    template = (root / "_shared/user-experience.md").read_text()
    result = {}
    for skill in sorted(root.glob("gbm*/SKILL.md")):
        title_zh, title_en, request_zh, request_en = INTRODUCTIONS[skill.parent.name]
        intro_zh = f"我是 AlphaGBM 的{title_zh}助手。可说「{request_zh}」；我会先明确结果，再说明依据和缺口。"
        intro_en = f"I’m AlphaGBM’s {title_en} assistant. Try “{request_en}”; I’ll lead with the result, then explain evidence and gaps."
        content = template.replace("{{INTRO_ZH}}", intro_zh).replace("{{INTRO_EN}}", intro_en)
        block = EXPERIENCE_START + "\n" + content.rstrip() + "\n" + EXPERIENCE_END
        result[skill] = with_experience(skill.read_text(), block)
    return result


def outputs(root=ROOT):
    result = {}
    for skill in sorted(root.glob("gbm*/SKILL.md")):
        for filename in re.findall(r"\]\(references/shared/([a-z-]+\.md)\)", skill.read_text()):
            result[skill.parent / "references/shared" / filename] = (root / "_shared" / filename).read_text()
    return result


def check(root=ROOT):
    expected = {**outputs(root), **experience_outputs(root)}
    stale = {path for path, content in expected.items()
             if not path.is_file() or path.read_text() != content}
    stale.update(set(root.glob("gbm*/references/shared/*")) - set(expected))
    return sorted(stale)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    if arguments.check:
        stale = check()
        if stale:
            print("Protocol bundles are missing, stale or unexpected:")
            for path in stale:
                print(path.relative_to(ROOT))
            return 1
    else:
        for path, content in {**outputs(), **experience_outputs()}.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    print("Protocol bundles and skill experience blocks match their canonical sources.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
