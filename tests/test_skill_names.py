import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAMES = {
    "gbm", "gbm-benchmark", "gbm-coach", "gbm-deconstruct", "gbm-diagnosis",
    "gbm-event-attribution", "gbm-market-research", "gbm-model", "gbm-report",
    "gbm-research", "gbm-restore", "gbm-save", "gbm-trade",
}


class SkillNameTests(unittest.TestCase):
    def skill_files(self):
        return {
            path.parent.name: path
            for path in ROOT.glob("*/SKILL.md")
            if path.parent.name != "skill-template"
        }

    def test_exactly_thirteen_short_named_skills(self):
        self.assertEqual(set(self.skill_files()), NAMES)

    def test_frontmatter_matches_directory_brand_and_version(self):
        version = (ROOT / "_shared/SUITE_VERSION").read_text().strip()
        for name, path in self.skill_files().items():
            with self.subTest(name=name):
                text = path.read_text(encoding="utf-8")
                frontmatter = text.split("---", 2)[1]
                self.assertIn(f"\nname: {name}\n", frontmatter)
                self.assertIn('  author: AlphaGBM', frontmatter)
                self.assertIn(f'  version: "{version}"', frontmatter)
                description = re.search(r"^description: (.+)$", frontmatter, re.M).group(1)
                self.assertIn(f"/{name}", description)
                self.assertIn("AlphaGBM", description)
                self.assertLessEqual(len(description), 1024)

    def test_skill_references_resolve_without_legacy_names(self):
        for name, path in self.skill_files().items():
            with self.subTest(name=name):
                text = path.read_text(encoding="utf-8")
                self.assertNotRegex(text, r"\balphagbm(?:-[a-z-]+)?\b")
                for target in re.findall(r"`(gbm(?:-[a-z-]+)?)`", text):
                    self.assertIn(target, NAMES)
                    self.assertTrue((ROOT / target / "SKILL.md").is_file())

    def test_router_lists_every_child(self):
        text = (ROOT / "gbm/SKILL.md").read_text(encoding="utf-8")
        for name in NAMES - {"gbm"}:
            self.assertIn(f"`{name}`", text)

    def test_readme_has_new_catalog_and_migration_boundary(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for name in NAMES:
            self.assertIn(f"| `{name}` |", text)
        self.assertIn("# AlphaGBM Trading Skills", text)
        self.assertIn("AlphaGBM/alphagbm-trading-skills", text)
        self.assertIn("从 0.1.x 升级", text)
        self.assertIn("不会自动修改", text)


if __name__ == "__main__":
    unittest.main()
