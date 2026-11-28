import importlib.util
from pathlib import Path
import tempfile
import shutil
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("experience_builder", ROOT / "scripts/build_packages.py")
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class ExperienceTests(unittest.TestCase):
    def test_all_thirteen_skills_have_scoped_inline_experience(self):
        expected = builder.experience_outputs()
        self.assertEqual(len(expected), 13)
        for path, document in expected.items():
            with self.subTest(skill=path.parent.name):
                self.assertEqual(path.read_text(), document)
                self.assertEqual(document.count(builder.EXPERIENCE_START), 1)
                self.assertEqual(document.count(builder.EXPERIENCE_END), 1)
                block = document.split(builder.EXPERIENCE_START)[1].split(builder.EXPERIENCE_END)[0]
                self.assertIn(builder.INTRODUCTIONS[path.parent.name][0], block)
                self.assertIn(builder.INTRODUCTIONS[path.parent.name][1], block)
                self.assertNotIn("{{", block)
                self.assertNotIn("_shared/", block)

    def test_formats_language_permission_and_evidence_take_priority(self):
        policy = (ROOT / "_shared/user-experience.md").read_text()
        for requirement in ("explicit user preference first", "ignoring tickers", "else English",
                            "once per visible conversation across", "JSON-only, code-only, verbatim",
                            "preserve original evidence", "at most three columns",
                            "save/restore tasks report actual action status", "at most two heading levels",
                            "do not repeat installation/demo", "FACT, MANAGEMENT, MARKET, MODEL",
                            "persisted seen flag", "Paid/private"):
            self.assertIn(requirement, policy)

    def test_replacement_preserves_custom_body_and_is_idempotent(self):
        document = (ROOT / "gbm-event-attribution/SKILL.md").read_text()
        before, tail = document.split(builder.EXPERIENCE_START)
        previous, after = tail.split(builder.EXPERIENCE_END)
        block = builder.EXPERIENCE_START + "\nreplacement\n" + builder.EXPERIENCE_END
        rendered = builder.with_experience(document, block)
        self.assertEqual(rendered, before + block + after)
        self.assertEqual(builder.with_experience(rendered, block), rendered)
        with self.assertRaises(ValueError):
            builder.with_experience(document + builder.EXPERIENCE_START, block)
        with self.assertRaises(ValueError):
            builder.with_experience(builder.EXPERIENCE_END + builder.EXPERIENCE_START, block)
        with self.assertRaises(ValueError):
            builder.with_experience("no heading", block)

    def test_stale_skill_experience_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "_shared", root / "_shared")
            shutil.copytree(ROOT / "gbm-research", root / "gbm-research")
            skill = root / "gbm-research/SKILL.md"
            skill.write_text(skill.read_text().replace("Mobile first:", "Stale policy:"))
            self.assertIn(skill, builder.check(root))


if __name__ == "__main__":
    unittest.main()
