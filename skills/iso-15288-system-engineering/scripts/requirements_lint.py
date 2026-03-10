#!/usr/bin/env python3
"""Lint stakeholder and system requirements stored as JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


AMBIGUOUS_TERMS = {
    "adequate",
    "as needed",
    "easy",
    "efficient",
    "fast",
    "flexible",
    "improved",
    "maximize",
    "minimize",
    "optimize",
    "quick",
    "rapid",
    "robust",
    "seamless",
    "simple",
    "sufficient",
    "support",
    "user-friendly",
}
WEAK_PHRASES = {
    "and/or",
    "if possible",
    "where appropriate",
}
SHALL_HINTS = (" shall ", " must ", " should ")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Lint requirements JSON for common quality and traceability issues."
    )
    parser.add_argument("input", help="Path to requirements JSON file")
    return parser.parse_args()


def load_json(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        raise SystemExit(f"Input file not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}")
    if not isinstance(data, dict):
        raise SystemExit("Top-level JSON must be an object")
    return data


def iter_requirements(data: dict) -> list[tuple[str, dict]]:
    items: list[tuple[str, dict]] = []
    for section in ("stakeholder_requirements", "system_requirements"):
        value = data.get(section, [])
        if not isinstance(value, list):
            raise SystemExit(f"'{section}' must be a list")
        for entry in value:
            if not isinstance(entry, dict):
                raise SystemExit(f"Every item in '{section}' must be an object")
            items.append((section, entry))
    return items


def find_ambiguous_terms(text: str) -> list[str]:
    lowered = f" {text.lower()} "
    hits = [term for term in AMBIGUOUS_TERMS if f" {term} " in lowered]
    hits.extend(phrase for phrase in WEAK_PHRASES if phrase in lowered)
    return sorted(set(hits))


def lint_requirement(section: str, req: dict, seen_ids: set[str]) -> list[str]:
    problems: list[str] = []
    req_id = str(req.get("id", "")).strip()
    text = str(req.get("text", "")).strip()

    if not req_id:
        problems.append("missing id")
    elif req_id in seen_ids:
        problems.append(f"duplicate id '{req_id}'")
    else:
        seen_ids.add(req_id)

    if not text:
        problems.append("missing text")
        return problems

    lowered = f" {text.lower()} "
    if not any(hint in lowered for hint in SHALL_HINTS):
        problems.append("text should use normative wording such as 'shall' or 'must'")

    ambiguous = find_ambiguous_terms(text)
    if ambiguous:
        problems.append(f"contains ambiguous terms: {', '.join(ambiguous)}")

    if len(text.split()) < 5:
        problems.append("text is unusually short")

    if section == "system_requirements":
        if not req.get("source_ids"):
            problems.append("missing source_ids trace to stakeholder requirements")
        if not req.get("verification_method"):
            problems.append("missing verification_method")

    return problems


def lint_verification(data: dict, system_ids: set[str]) -> list[str]:
    findings: list[str] = []
    entries = data.get("verification_requirements", [])
    if not isinstance(entries, list):
        raise SystemExit("'verification_requirements' must be a list")

    for entry in entries:
        if not isinstance(entry, dict):
            raise SystemExit("Every item in 'verification_requirements' must be an object")
        ver_id = str(entry.get("id", "")).strip() or "<missing-id>"
        req_ids = entry.get("requirement_ids", [])
        if not isinstance(req_ids, list):
            findings.append(f"{ver_id}: requirement_ids must be a list")
            continue
        for req_id in req_ids:
            if req_id not in system_ids:
                findings.append(f"{ver_id}: traces to unknown system requirement '{req_id}'")
        if not entry.get("method"):
            findings.append(f"{ver_id}: missing verification method")
    return findings


def main() -> int:
    args = parse_args()
    data = load_json(Path(args.input))
    seen_ids: set[str] = set()
    system_ids: set[str] = set()
    findings: list[str] = []

    for section, req in iter_requirements(data):
        req_id = str(req.get("id", "")).strip() or "<missing-id>"
        problems = lint_requirement(section, req, seen_ids)
        if section == "system_requirements" and req_id != "<missing-id>":
            system_ids.add(req_id)
        for problem in problems:
            findings.append(f"{req_id}: {problem}")

    findings.extend(lint_verification(data, system_ids))

    if findings:
        print("# Requirements Lint Report")
        print()
        for finding in findings:
            print(f"- {finding}")
        return 1

    print("Requirements lint passed with no findings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
