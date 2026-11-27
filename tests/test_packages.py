import importlib.util
import re
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_packages", ROOT / "scripts/build_packages.py")
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class PackageTests(unittest.TestCase):
    def test_bundles_are_current(self):
        self.assertEqual(builder.check(), [])
        self.assertEqual(len(builder.outputs()), 2)

    def test_installed_skill_links_stay_inside_package(self):
        for skill in ROOT.glob("gbm*/SKILL.md"):
            with self.subTest(skill=skill.parent.name), tempfile.TemporaryDirectory() as directory:
                installed = Path(directory) / skill.parent.name
                shutil.copytree(skill.parent, installed)
                content = (installed / "SKILL.md").read_text()
                self.assertNotIn("_shared/", content)
                for target in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", content):
                    if "://" in target:
                        continue
                    resolved = (installed / target).resolve()
                    self.assertTrue(resolved.is_relative_to(installed.resolve()))
                    self.assertTrue(resolved.is_file(), target)

    def test_template_is_not_discoverable(self):
        self.assertEqual(len(list(ROOT.rglob("SKILL.md"))), 13)
        self.assertTrue((ROOT / "skill-template/SKILL.md.template").is_file())

    def test_missing_changed_and_extra_bundles_fail_check(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "_shared", root / "_shared")
            shutil.copytree(ROOT / "gbm-research", root / "gbm-research")
            target = root / "gbm-research/references/shared/evidence-standards.md"
            self.assertEqual(builder.check(root), [])
            target.unlink()
            self.assertIn(target, builder.check(root))
            target.write_text("stale")
            self.assertIn(target, builder.check(root))
            target.write_text((root / "_shared/evidence-standards.md").read_text())
            extra = target.with_name("unused.md")
            extra.write_text("unused")
            self.assertIn(extra, builder.check(root))


if __name__ == "__main__":
    unittest.main()
