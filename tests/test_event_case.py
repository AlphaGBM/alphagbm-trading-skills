import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.event_case import new_case, validate


class EventCaseTests(unittest.TestCase):
    def test_new_case_has_required_contract(self):
        case = new_case("CASE-001", "earnings", "2026-11-11T08:00:00Z")
        self.assertEqual(validate(case), [])

    def test_invalid_evidence_is_rejected(self):
        case = new_case("CASE-002", "filing", "2026-11-11T08:00:00Z")
        case["evidence"].append({"claim_type": "FACT"})
        self.assertTrue(validate(case))

    def test_complete_fact_is_accepted(self):
        case = new_case("CASE-004", "earnings", "2026-11-11T08:00:00Z")
        case["evidence"].append(
            {
                "claim_id": "C-001",
                "claim_type": "FACT",
                "statement": "Revenue was 22 million.",
                "quote_or_data": "Revenue: 22 million",
                "source": {
                    "publisher": "Synthetic Company",
                    "title": "Quarterly release",
                    "url": "https://example.invalid/release",
                    "published_at": "2026-11-11T08:00:00Z",
                    "accessed_at": "2026-11-11T09:00:00Z",
                    "locator": "page 1, table 1",
                    "source_tier": 1,
                },
            }
        )
        self.assertEqual(validate(case), [])

    def test_duplicate_claim_ids_and_invalid_unknowns_are_rejected(self):
        case = new_case("CASE-005", "filing", "2026-11-11T08:00:00Z")
        case["unknowns"] = [{"question": "missing"}]
        case["evidence"] = [
            {"claim_id": "C-001", "claim_type": "UNKNOWN", "statement": "x", "source": {}},
            {"claim_id": "C-001", "claim_type": "UNKNOWN", "statement": "y", "source": {}},
        ]
        errors = validate(case)
        self.assertTrue(any("duplicates claim_id" in error for error in errors))
        self.assertTrue(any("unknowns must be" in error for error in errors))

    def test_invalid_timestamp_and_top_level_array_are_rejected_cleanly(self):
        case = new_case("CASE-006", "filing", "not-a-date")
        self.assertTrue(any("occurred_at" in error for error in validate(case)))
        self.assertEqual(validate([]), ["top-level JSON value must be an object"])

    def test_create_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            command = [sys.executable, "scripts/event_case.py", "create", str(path), "--record-id", "A", "--occurred-at", "2026-11-11T08:00:00Z"]
            first = subprocess.run(command, capture_output=True, text=True, check=False)
            before = path.read_bytes()
            second = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(first.returncode, 0)
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual(path.read_bytes(), before)

    def test_round_trip_json(self):
        case = new_case("CASE-003", "guidance", "2026-11-11T08:00:00Z")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            path.write_text(json.dumps(case), encoding="utf-8")
            loaded = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(validate(loaded), [])


if __name__ == "__main__":
    unittest.main()
