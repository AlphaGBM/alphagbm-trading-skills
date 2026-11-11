import json
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

    def test_round_trip_json(self):
        case = new_case("CASE-003", "guidance", "2026-11-11T08:00:00Z")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            path.write_text(json.dumps(case), encoding="utf-8")
            loaded = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(validate(loaded), [])


if __name__ == "__main__":
    unittest.main()
