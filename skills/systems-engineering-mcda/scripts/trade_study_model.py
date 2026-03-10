#!/usr/bin/env python3
"""Shared parser and scoring logic for systems engineering MCDA trade studies."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path


SUPPORTED_METHODS = {"weighted-sum", "topsis"}


@dataclass(frozen=True)
class Criterion:
    """One scored decision criterion."""

    id: str
    name: str
    weight: float
    direction: str


@dataclass(frozen=True)
class Alternative:
    """One candidate alternative in the trade study."""

    id: str
    name: str
    scores: dict[str, float]


def load_study(path: Path) -> dict:
    """Load a study definition from JSON."""
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


def resolve_method(data: dict, method_override: str | None) -> str:
    """Choose the scoring method from the CLI or JSON payload."""
    method = method_override or str(data.get("method", "weighted-sum")).strip().lower()
    if method not in SUPPORTED_METHODS:
        choices = ", ".join(sorted(SUPPORTED_METHODS))
        raise SystemExit(f"Unsupported method '{method}'. Choose one of: {choices}")
    return method


def parse_study(data: dict) -> tuple[list[Criterion], list[Alternative]]:
    """Validate and normalize the study structure."""
    raw_criteria = data.get("criteria")
    raw_alternatives = data.get("alternatives")

    if not isinstance(raw_criteria, list) or not raw_criteria:
        raise SystemExit("'criteria' must be a non-empty list")
    if not isinstance(raw_alternatives, list) or not raw_alternatives:
        raise SystemExit("'alternatives' must be a non-empty list")

    criteria: list[Criterion] = []
    seen_criteria: set[str] = set()
    total_weight = 0.0
    for entry in raw_criteria:
        if not isinstance(entry, dict):
            raise SystemExit("Every item in 'criteria' must be an object")
        criterion_id = str(entry.get("id", "")).strip()
        name = str(entry.get("name", criterion_id)).strip() or criterion_id
        direction = str(entry.get("direction", "")).strip().lower()
        weight = coerce_number(entry.get("weight"), "criterion weight")

        if not criterion_id:
            raise SystemExit("Each criterion must have a non-empty 'id'")
        if criterion_id in seen_criteria:
            raise SystemExit(f"Duplicate criterion id '{criterion_id}'")
        if direction not in {"max", "min"}:
            raise SystemExit(
                f"Criterion '{criterion_id}' must define direction as 'max' or 'min'"
            )
        if weight < 0:
            raise SystemExit(f"Criterion '{criterion_id}' has a negative weight")

        criteria.append(Criterion(criterion_id, name, weight, direction))
        seen_criteria.add(criterion_id)
        total_weight += weight

    if total_weight <= 0:
        raise SystemExit("Criterion weights must sum to a positive value")
    criteria = [
        Criterion(item.id, item.name, item.weight / total_weight, item.direction)
        for item in criteria
    ]

    alternatives: list[Alternative] = []
    seen_alternatives: set[str] = set()
    required_ids = {criterion.id for criterion in criteria}
    for entry in raw_alternatives:
        if not isinstance(entry, dict):
            raise SystemExit("Every item in 'alternatives' must be an object")
        alternative_id = str(entry.get("id", "")).strip()
        name = str(entry.get("name", alternative_id)).strip() or alternative_id
        scores = entry.get("scores")
        if not alternative_id:
            raise SystemExit("Each alternative must have a non-empty 'id'")
        if alternative_id in seen_alternatives:
            raise SystemExit(f"Duplicate alternative id '{alternative_id}'")
        if not isinstance(scores, dict):
            raise SystemExit(f"Alternative '{alternative_id}' must include a 'scores' object")

        parsed_scores: dict[str, float] = {}
        for criterion_id in required_ids:
            if criterion_id not in scores:
                raise SystemExit(
                    f"Alternative '{alternative_id}' is missing score for '{criterion_id}'"
                )
            parsed_scores[criterion_id] = coerce_number(
                scores[criterion_id],
                f"score for criterion '{criterion_id}' on alternative '{alternative_id}'",
            )

        alternatives.append(Alternative(alternative_id, name, parsed_scores))
        seen_alternatives.add(alternative_id)

    return criteria, alternatives


def coerce_number(value: object, label: str) -> float:
    """Convert a JSON scalar to float or fail with a readable message."""
    try:
        return float(value)
    except (TypeError, ValueError):
        raise SystemExit(f"Invalid numeric value for {label}: {value!r}")


def rank_study(
    criteria: list[Criterion],
    alternatives: list[Alternative],
    method: str,
) -> list[dict]:
    """Rank alternatives using the selected method."""
    if method == "weighted-sum":
        results = weighted_sum(criteria, alternatives)
    elif method == "topsis":
        results = topsis(criteria, alternatives)
    else:
        raise SystemExit(f"Unsupported method '{method}'")

    sorted_results = sorted(
        results,
        key=lambda item: (-item["score"], item["name"], item["id"]),
    )
    for index, result in enumerate(sorted_results, start=1):
        result["rank"] = index
    return sorted_results


def weighted_sum(criteria: list[Criterion], alternatives: list[Alternative]) -> list[dict]:
    """Compute a weighted additive score with min-max normalization."""
    normalized_by_criterion = min_max_normalize(criteria, alternatives)
    results: list[dict] = []

    for alternative in alternatives:
        contributions: dict[str, float] = {}
        score = 0.0
        for criterion in criteria:
            normalized = normalized_by_criterion[criterion.id][alternative.id]
            contribution = normalized * criterion.weight
            contributions[criterion.id] = contribution
            score += contribution
        results.append(
            {
                "id": alternative.id,
                "name": alternative.name,
                "score": score,
                "contributions": contributions,
                "raw_scores": dict(alternative.scores),
            }
        )
    return results


def min_max_normalize(
    criteria: list[Criterion],
    alternatives: list[Alternative],
) -> dict[str, dict[str, float]]:
    """Normalize raw scores to 0..1 for weighted-sum analysis."""
    normalized: dict[str, dict[str, float]] = {}
    for criterion in criteria:
        values = [alternative.scores[criterion.id] for alternative in alternatives]
        minimum = min(values)
        maximum = max(values)

        criterion_values: dict[str, float] = {}
        if math.isclose(maximum, minimum):
            for alternative in alternatives:
                criterion_values[alternative.id] = 1.0
        else:
            spread = maximum - minimum
            for alternative in alternatives:
                raw_value = alternative.scores[criterion.id]
                if criterion.direction == "max":
                    normalized_value = (raw_value - minimum) / spread
                else:
                    normalized_value = (maximum - raw_value) / spread
                criterion_values[alternative.id] = normalized_value
        normalized[criterion.id] = criterion_values
    return normalized


def topsis(criteria: list[Criterion], alternatives: list[Alternative]) -> list[dict]:
    """Compute TOPSIS closeness to the ideal solution."""
    weighted_matrix: dict[str, dict[str, float]] = {criterion.id: {} for criterion in criteria}

    for criterion in criteria:
        squared_sum = sum(alternative.scores[criterion.id] ** 2 for alternative in alternatives)
        denominator = math.sqrt(squared_sum)
        for alternative in alternatives:
            normalized = 0.0 if math.isclose(denominator, 0.0) else (
                alternative.scores[criterion.id] / denominator
            )
            weighted_matrix[criterion.id][alternative.id] = normalized * criterion.weight

    ideal_best: dict[str, float] = {}
    ideal_worst: dict[str, float] = {}
    for criterion in criteria:
        values = list(weighted_matrix[criterion.id].values())
        if criterion.direction == "max":
            ideal_best[criterion.id] = max(values)
            ideal_worst[criterion.id] = min(values)
        else:
            ideal_best[criterion.id] = min(values)
            ideal_worst[criterion.id] = max(values)

    results: list[dict] = []
    for alternative in alternatives:
        distance_to_best = math.sqrt(
            sum(
                (weighted_matrix[criterion.id][alternative.id] - ideal_best[criterion.id]) ** 2
                for criterion in criteria
            )
        )
        distance_to_worst = math.sqrt(
            sum(
                (weighted_matrix[criterion.id][alternative.id] - ideal_worst[criterion.id]) ** 2
                for criterion in criteria
            )
        )
        denominator = distance_to_best + distance_to_worst
        closeness = 1.0 if math.isclose(denominator, 0.0) else distance_to_worst / denominator
        results.append(
            {
                "id": alternative.id,
                "name": alternative.name,
                "score": closeness,
                "contributions": {
                    criterion.id: weighted_matrix[criterion.id][alternative.id]
                    for criterion in criteria
                },
                "raw_scores": dict(alternative.scores),
            }
        )
    return results


def reweight_criteria(
    criteria: list[Criterion],
    target_id: str,
    new_weight: float,
) -> list[Criterion]:
    """Adjust one criterion weight and rebalance the rest proportionally."""
    if not 0.0 <= new_weight <= 1.0:
        raise SystemExit("Adjusted weight must stay within 0.0 and 1.0")

    target = None
    for criterion in criteria:
        if criterion.id == target_id:
            target = criterion
            break
    if target is None:
        raise SystemExit(f"Unknown criterion id '{target_id}'")

    others = [criterion for criterion in criteria if criterion.id != target_id]
    if not others:
        return [Criterion(target.id, target.name, 1.0, target.direction)]

    other_total = sum(criterion.weight for criterion in others)
    remaining = 1.0 - new_weight

    adjusted: list[Criterion] = []
    if math.isclose(other_total, 0.0):
        equal_share = remaining / len(others)
        for criterion in criteria:
            if criterion.id == target_id:
                adjusted.append(
                    Criterion(criterion.id, criterion.name, new_weight, criterion.direction)
                )
            else:
                adjusted.append(
                    Criterion(criterion.id, criterion.name, equal_share, criterion.direction)
                )
        return adjusted

    scale = remaining / other_total
    for criterion in criteria:
        if criterion.id == target_id:
            adjusted.append(Criterion(criterion.id, criterion.name, new_weight, criterion.direction))
        else:
            adjusted.append(
                Criterion(
                    criterion.id,
                    criterion.name,
                    criterion.weight * scale,
                    criterion.direction,
                )
            )
    return adjusted
