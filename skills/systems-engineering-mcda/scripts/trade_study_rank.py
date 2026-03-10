#!/usr/bin/env python3
"""Rank systems engineering trade-study alternatives from a JSON model."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from trade_study_model import load_study, parse_study, rank_study, resolve_method


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rank trade-study alternatives with weighted-sum or TOPSIS."
    )
    parser.add_argument("input", help="Path to trade-study JSON file")
    parser.add_argument(
        "--method",
        choices=("weighted-sum", "topsis"),
        help="Override the scoring method from the JSON input",
    )
    parser.add_argument(
        "--output-json",
        help="Optional path to write ranking results as JSON",
    )
    parser.add_argument(
        "--output-csv",
        help="Optional path to write ranking results as CSV",
    )
    return parser.parse_args()


def print_report(method: str, criteria: list, results: list[dict]) -> None:
    """Emit a readable ranking report."""
    print(f"# Trade Study Ranking ({method})")
    print()
    print("## Criteria")
    for criterion in criteria:
        print(
            f"- {criterion.id}: weight={criterion.weight:.3f}, direction={criterion.direction}"
        )
    print()
    print("## Ranking")
    for result in results:
        print(
            f"{result['rank']}. {result['name']} ({result['id']}) "
            f"score={result['score']:.4f}"
        )


def write_json(path: Path, method: str, criteria: list, results: list[dict]) -> None:
    """Write ranking results to JSON."""
    payload = {
        "method": method,
        "criteria": [
            {
                "id": criterion.id,
                "name": criterion.name,
                "weight": round(criterion.weight, 6),
                "direction": criterion.direction,
            }
            for criterion in criteria
        ],
        "results": [
            {
                "rank": result["rank"],
                "id": result["id"],
                "name": result["name"],
                "score": round(result["score"], 6),
                "raw_scores": result["raw_scores"],
                "contributions": {
                    key: round(value, 6) for key, value in result["contributions"].items()
                },
            }
            for result in results
        ],
    }
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def write_csv(path: Path, criteria: list, results: list[dict]) -> None:
    """Write ranking results to CSV."""
    fieldnames = ["rank", "id", "name", "score"]
    fieldnames.extend(f"raw_{criterion.id}" for criterion in criteria)
    fieldnames.extend(f"contribution_{criterion.id}" for criterion in criteria)

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            row = {
                "rank": result["rank"],
                "id": result["id"],
                "name": result["name"],
                "score": f"{result['score']:.6f}",
            }
            for criterion in criteria:
                row[f"raw_{criterion.id}"] = result["raw_scores"][criterion.id]
                row[f"contribution_{criterion.id}"] = (
                    f"{result['contributions'][criterion.id]:.6f}"
                )
            writer.writerow(row)


def main() -> int:
    args = parse_args()
    data = load_study(Path(args.input))
    method = resolve_method(data, args.method)
    criteria, alternatives = parse_study(data)
    results = rank_study(criteria, alternatives, method)

    print_report(method, criteria, results)

    if args.output_json:
        write_json(Path(args.output_json), method, criteria, results)
        print()
        print(f"Wrote JSON results to {args.output_json}")

    if args.output_csv:
        write_csv(Path(args.output_csv), criteria, results)
        print(f"Wrote CSV results to {args.output_csv}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
