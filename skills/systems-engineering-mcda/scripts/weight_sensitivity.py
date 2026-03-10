#!/usr/bin/env python3
"""Run one-at-a-time weight sensitivity analysis on a trade-study model."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from trade_study_model import (
    load_study,
    parse_study,
    rank_study,
    resolve_method,
    reweight_criteria,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Vary one criterion weight at a time and report ranking instability."
    )
    parser.add_argument("input", help="Path to trade-study JSON file")
    parser.add_argument(
        "--method",
        choices=("weighted-sum", "topsis"),
        help="Override the scoring method from the JSON input",
    )
    parser.add_argument(
        "--delta",
        type=float,
        default=0.1,
        help="Absolute weight change to apply up and down (default: 0.1)",
    )
    parser.add_argument(
        "--output-json",
        help="Optional path to write sensitivity results as JSON",
    )
    return parser.parse_args()


def compute_rank_shift(baseline: list[dict], candidate: list[dict]) -> int:
    """Return the largest absolute rank change across alternatives."""
    baseline_ranks = {item["id"]: item["rank"] for item in baseline}
    candidate_ranks = {item["id"]: item["rank"] for item in candidate}
    return max(
        abs(baseline_ranks[item_id] - candidate_ranks[item_id])
        for item_id in baseline_ranks
    )


def print_report(method: str, baseline: list[dict], scenarios: list[dict]) -> None:
    """Print a readable sensitivity report."""
    baseline_top = baseline[0]
    print(f"# Weight Sensitivity ({method})")
    print()
    print(
        f"Baseline winner: {baseline_top['name']} ({baseline_top['id']}) "
        f"score={baseline_top['score']:.4f}"
    )
    print()
    print("criterion, change, winner, changed, max_rank_shift")
    for scenario in scenarios:
        print(
            f"{scenario['criterion_id']}, {scenario['change']}, "
            f"{scenario['winner_id']}, {scenario['winner_changed']}, "
            f"{scenario['max_rank_shift']}"
        )


def write_json(path: Path, method: str, baseline: list[dict], scenarios: list[dict]) -> None:
    """Persist sensitivity results as JSON."""
    payload = {
        "method": method,
        "baseline": [
            {
                "rank": item["rank"],
                "id": item["id"],
                "name": item["name"],
                "score": round(item["score"], 6),
            }
            for item in baseline
        ],
        "scenarios": scenarios,
    }
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def main() -> int:
    args = parse_args()
    if not 0 < args.delta < 1:
        raise SystemExit("--delta must be between 0 and 1")

    data = load_study(Path(args.input))
    method = resolve_method(data, args.method)
    criteria, alternatives = parse_study(data)
    baseline = rank_study(criteria, alternatives, method)
    baseline_winner = baseline[0]["id"]

    scenarios: list[dict] = []
    for criterion in criteria:
        for label, raw_weight in (
            ("increase", min(1.0, criterion.weight + args.delta)),
            ("decrease", max(0.0, criterion.weight - args.delta)),
        ):
            adjusted_criteria = reweight_criteria(criteria, criterion.id, raw_weight)
            ranked = rank_study(adjusted_criteria, alternatives, method)
            top = ranked[0]
            actual_weight = next(
                item.weight for item in adjusted_criteria if item.id == criterion.id
            )
            scenarios.append(
                {
                    "criterion_id": criterion.id,
                    "change": label,
                    "adjusted_weight": round(actual_weight, 6),
                    "winner_id": top["id"],
                    "winner_name": top["name"],
                    "winner_changed": top["id"] != baseline_winner,
                    "max_rank_shift": compute_rank_shift(baseline, ranked),
                    "ranking": [
                        {
                            "rank": item["rank"],
                            "id": item["id"],
                            "name": item["name"],
                            "score": round(item["score"], 6),
                        }
                        for item in ranked
                    ],
                    "weights": {
                        item.id: round(item.weight, 6) for item in adjusted_criteria
                    },
                }
            )

    print_report(method, baseline, scenarios)

    if args.output_json:
        write_json(Path(args.output_json), method, baseline, scenarios)
        print()
        print(f"Wrote JSON results to {args.output_json}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
