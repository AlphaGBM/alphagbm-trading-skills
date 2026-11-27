"""Bundle referenced protocols so each installed skill has its own resources."""

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def outputs(root=ROOT):
    result = {}
    for skill in sorted(root.glob("gbm*/SKILL.md")):
        for filename in re.findall(r"\]\(references/shared/([a-z-]+\.md)\)", skill.read_text()):
            result[skill.parent / "references/shared" / filename] = (root / "_shared" / filename).read_text()
    return result


def check(root=ROOT):
    expected = outputs(root)
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
        for path, content in outputs().items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    print("Referenced protocol bundles match their canonical sources.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
