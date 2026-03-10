#!/usr/bin/env python3
"""Generate a CSV traceability matrix from requirements JSON."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a stakeholder-to-system-to-verification traceability matrix."
    )
    parser.add_argument("input", help="Path to requirements JSON file")
    parser.add_argument(
        "--output",
        default="traceability-matrix.csv",
        help="Output CSV path (default: traceability-matrix.csv)",
    )
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


def build_index(items: list[dict]) -> dict[str, dict]:
    index: dict[str, dict] = {}
    for item in items:
        item_id = str(item.get("id", "")).strip()
        if item_id:
            index[item_id] = item
    return index


def main() -> int:
    args = parse_args()
    data = load_json(Path(args.input))

    stakeholder_reqs = data.get("stakeholder_requirements", [])
    system_reqs = data.get("system_requirements", [])
    verification_reqs = data.get("verification_requirements", [])

    if not all(isinstance(section, list) for section in (stakeholder_reqs, system_reqs, verification_reqs)):
        raise SystemExit("stakeholder_requirements, system_requirements, and verification_requirements must be lists")

    stakeholder_index = build_index(stakeholder_reqs)
    verification_by_requirement: dict[str, list[dict]] = {}
    for verification in verification_reqs:
        for requirement_id in verification.get("requirement_ids", []):
            verification_by_requirement.setdefault(str(requirement_id), []).append(verification)

    output_path = Path(args.output)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "stakeholder_requirement_id",
                "stakeholder_requirement_text",
                "system_requirement_id",
                "system_requirement_text",
                "verification_method",
                "verification_id",
                "verification_evidence",
            ]
        )

        for system_req in system_reqs:
            system_id = str(system_req.get("id", "")).strip()
            system_text = str(system_req.get("text", "")).strip()
            source_ids = system_req.get("source_ids", []) or [""]
            verifications = verification_by_requirement.get(system_id, [{}])

            for source_id in source_ids:
                stakeholder_req = stakeholder_index.get(str(source_id), {})
                stakeholder_text = str(stakeholder_req.get("text", "")).strip()
                for verification in verifications:
                    writer.writerow(
                        [
                            source_id,
                            stakeholder_text,
                            system_id,
                            system_text,
                            verification.get("method", system_req.get("verification_method", "")),
                            verification.get("id", ""),
                            verification.get("evidence", ""),
                        ]
                    )

    print(f"Wrote traceability matrix to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
