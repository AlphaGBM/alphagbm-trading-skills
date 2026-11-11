import tempfile
import unittest
from pathlib import Path

from scripts.privacy_gate import scan


class PrivacyGateTests(unittest.TestCase):
    def test_clean_public_content_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "README.md"
            path.write_text("AlphaGBM\nopensource@alphagbm.com\n", encoding="utf-8")
            self.assertEqual(scan(Path(directory)), [])

    def test_private_key_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.md"
            path.write_text("-----BEGIN " + "PRIVATE KEY-----\n", encoding="utf-8")
            findings = scan(Path(directory))
            self.assertTrue(any("private key" in finding for finding in findings))


if __name__ == "__main__":
    unittest.main()
