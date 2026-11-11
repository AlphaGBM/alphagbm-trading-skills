#!/usr/bin/env python3
"""Reject likely secrets, personal contact details, and private paths."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TEXT_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".json", ".py", ".sh", ".toml", ".html"}
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache"}
PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "api token": re.compile(r"(?i)\b(?:api[_-]?key|api[_-]?token|access[_-]?token|secret[_-]?key)\s*[:=]\s*[\"']?[A-Za-z0-9_./+=-]{16,}"),
    "authorization header": re.compile(r"(?i)authorization\s*:\s*bearer\s+[A-Za-z0-9._-]{16,}"),
    "email address": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "private path": re.compile(r"/(?:Users|home)/[^\s/]+/"),
    "phone number": re.compile(r"(?<!\d)(?:\+?\d[\s-]?){10,14}(?!\d)"),
}
ALLOWED_EMAIL_DOMAINS = {"alphagbm.com"}


def iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def scan(root: Path) -> list[str]:
    findings: list[str] = []
    for path in iter_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                value = match.group(0)
                if label == "email address" and value.rsplit("@", 1)[-1].lower() in ALLOWED_EMAIL_DOMAINS:
                    continue
                line = text.count("\n", 0, match.start()) + 1
                findings.append(f"{path}:{line}: {label}: {value[:80]}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    findings = scan(Path(args.root).resolve())
    if findings:
        print("Privacy gate failed:")
        print("\n".join(findings))
        return 1
    print("Privacy gate passed: no likely secrets or personal contact data found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
