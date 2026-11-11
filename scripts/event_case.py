#!/usr/bin/env python3
"""Create and validate a deterministic AlphaGBM event evidence package."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


REQUIRED_TOP_LEVEL = {"schema_version", "record_id", "created_at", "event", "evidence", "unknowns"}
REQUIRED_EVENT = {"kind", "occurred_at", "timezone"}
VALID_TYPES = {"FACT", "MANAGEMENT", "MARKET", "MODEL", "INFERENCE", "UNKNOWN"}


def new_case(record_id: str, kind: str, occurred_at: str) -> dict:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return {
        "schema_version": "1.0",
        "record_id": record_id,
        "created_at": now,
        "event": {"kind": kind, "occurred_at": occurred_at, "timezone": "UTC"},
        "evidence": [],
        "assumptions": [],
        "unknowns": ["事件前共识与基准收益待补充"],
        "attribution": {"confidence": "low", "primary_drivers": [], "alternatives": []},
    }


def validate(case: dict) -> list[str]:
    errors = [f"missing top-level field: {key}" for key in sorted(REQUIRED_TOP_LEVEL - case.keys())]
    event = case.get("event")
    if not isinstance(event, dict):
        errors.append("event must be an object")
    else:
        errors.extend(f"missing event field: {key}" for key in sorted(REQUIRED_EVENT - event.keys()))
    if not isinstance(case.get("evidence"), list):
        errors.append("evidence must be a list")
    else:
        for index, item in enumerate(case["evidence"]):
            if not isinstance(item, dict):
                errors.append(f"evidence[{index}] must be an object")
                continue
            if item.get("claim_type") not in VALID_TYPES:
                errors.append(f"evidence[{index}] has invalid claim_type")
            for key in ("claim_id", "statement", "source"):
                if not item.get(key):
                    errors.append(f"evidence[{index}] missing {key}")
            source = item.get("source")
            if source and not isinstance(source, dict):
                errors.append(f"evidence[{index}].source must be an object")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create")
    create.add_argument("output", type=Path)
    create.add_argument("--record-id", required=True)
    create.add_argument("--kind", default="earnings")
    create.add_argument("--occurred-at", required=True)

    check = subparsers.add_parser("check")
    check.add_argument("case", type=Path)
    args = parser.parse_args()

    if args.command == "create":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(new_case(args.record_id, args.kind, args.occurred_at), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"created {args.output}")
        return 0

    case = json.loads(args.case.read_text(encoding="utf-8"))
    errors = validate(case)
    if errors:
        print("Event case failed:")
        print("\n".join(errors))
        return 1
    print("Event case passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
