#!/usr/bin/env python3
"""Create and validate a deterministic AlphaGBM event evidence package."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


REQUIRED_TOP_LEVEL = {"schema_version", "record_id", "created_at", "event", "evidence", "unknowns"}
REQUIRED_EVENT = {"kind", "occurred_at", "timezone"}
VALID_TYPES = {"FACT", "MANAGEMENT", "MARKET", "MODEL", "INFERENCE", "UNKNOWN"}
REQUIRED_SOURCE = {"publisher", "title", "url", "published_at", "accessed_at", "locator", "source_tier"}


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


def _is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_timestamp(value: object) -> bool:
    if not _is_non_empty_string(value):
        return False
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _valid_url(value: object) -> bool:
    if not _is_non_empty_string(value):
        return False
    parsed = urlparse(str(value))
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def validate(case: object) -> list[str]:
    if not isinstance(case, dict):
        return ["top-level JSON value must be an object"]

    errors = [f"missing top-level field: {key}" for key in sorted(REQUIRED_TOP_LEVEL - case.keys())]
    for key in ("schema_version", "record_id"):
        if key in case and not _is_non_empty_string(case[key]):
            errors.append(f"{key} must be a non-empty string")
    if "created_at" in case and not _valid_timestamp(case["created_at"]):
        errors.append("created_at must be an ISO-8601 timestamp with timezone")

    event = case.get("event")
    if not isinstance(event, dict):
        errors.append("event must be an object")
    else:
        errors.extend(f"missing event field: {key}" for key in sorted(REQUIRED_EVENT - event.keys()))
        if "kind" in event and not _is_non_empty_string(event["kind"]):
            errors.append("event.kind must be a non-empty string")
        if "occurred_at" in event and not _valid_timestamp(event["occurred_at"]):
            errors.append("event.occurred_at must be an ISO-8601 timestamp with timezone")
        if "timezone" in event and not _is_non_empty_string(event["timezone"]):
            errors.append("event.timezone must be a non-empty string")

    for key in ("assumptions", "unknowns"):
        if key in case and (
            not isinstance(case[key], list)
            or any(not _is_non_empty_string(item) for item in case[key])
        ):
            errors.append(f"{key} must be a list of non-empty strings")

    if not isinstance(case.get("evidence"), list):
        errors.append("evidence must be a list")
    else:
        claim_ids: set[str] = set()
        for index, item in enumerate(case["evidence"]):
            if not isinstance(item, dict):
                errors.append(f"evidence[{index}] must be an object")
                continue
            if item.get("claim_type") not in VALID_TYPES:
                errors.append(f"evidence[{index}] has invalid claim_type")
            for key in ("claim_id", "statement", "source"):
                if not item.get(key):
                    errors.append(f"evidence[{index}] missing {key}")
            claim_id = item.get("claim_id")
            if _is_non_empty_string(claim_id):
                if claim_id in claim_ids:
                    errors.append(f"evidence[{index}] duplicates claim_id: {claim_id}")
                claim_ids.add(claim_id)
            elif "claim_id" in item:
                errors.append(f"evidence[{index}].claim_id must be a non-empty string")

            source = item.get("source")
            if source and not isinstance(source, dict):
                errors.append(f"evidence[{index}].source must be an object")
                continue
            if not isinstance(source, dict):
                continue
            missing_source = REQUIRED_SOURCE - source.keys()
            errors.extend(f"evidence[{index}].source missing {key}" for key in sorted(missing_source))
            for key in ("publisher", "title", "locator"):
                if key in source and not _is_non_empty_string(source[key]):
                    errors.append(f"evidence[{index}].source.{key} must be a non-empty string")
            if "url" in source and not _valid_url(source["url"]):
                errors.append(f"evidence[{index}].source.url must be an http(s) URL")
            for key in ("published_at", "accessed_at"):
                if key in source and not _valid_timestamp(source[key]):
                    errors.append(f"evidence[{index}].source.{key} must be an ISO-8601 timestamp with timezone")
            tier = source.get("source_tier")
            if not isinstance(tier, int) or isinstance(tier, bool) or tier not in {1, 2, 3, 4}:
                errors.append(f"evidence[{index}].source.source_tier must be an integer from 1 to 4")
            if item.get("claim_type") == "FACT" and not _is_non_empty_string(item.get("quote_or_data")):
                errors.append(f"evidence[{index}] FACT requires quote_or_data")
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
        payload = json.dumps(new_case(args.record_id, args.kind, args.occurred_at), ensure_ascii=False, indent=2) + "\n"
        try:
            with args.output.open("x", encoding="utf-8") as handle:
                handle.write(payload)
        except FileExistsError:
            print(f"refusing to overwrite existing event case: {args.output}")
            return 1
        print(f"created {args.output}")
        return 0

    try:
        case = json.loads(args.case.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"event case not found: {args.case}")
        return 1
    except (OSError, json.JSONDecodeError) as exc:
        print(f"could not read event case {args.case}: {exc}")
        return 1
    errors = validate(case)
    if errors:
        print("Event case failed:")
        print("\n".join(errors))
        return 1
    print("Event case passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
