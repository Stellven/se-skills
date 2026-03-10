---
name: systems-engineering-mcda
description: Evaluate competing system concepts with multi-criteria decision analysis in systems engineering. Use when Codex needs to run a trade study, compare architectures or technology options, weight decision criteria, rank alternatives, justify trade-offs, choose between weighted scoring, TOPSIS, AHP, MAUT/MAVT, or outranking-style approaches, or perform sensitivity analysis for a system or subsystem decision.
---

# Systems Engineering MCDA

Use this skill to turn a vague "which option should we choose?" request into a traceable trade study with explicit criteria, weights, assumptions, rankings, and sensitivity checks.

## Quick Start

1. Define the decision statement, system boundary, stakeholders, and hard constraints.
2. List feasible alternatives and screen out any option that fails mandatory constraints.
3. Build a criteria set with direction (`max` or `min`), units, evidence source, and weight rationale.
4. Choose the method:
   - weighted sum / SMART for most practical trade studies
   - TOPSIS when distance to an ideal and worst case matters
   - AHP for expert pairwise weighting
   - MAUT / MAVT when utility curves or risk attitude matter
   - ELECTRE / PROMETHEE / VIKOR when non-compensatory or compromise logic is required
5. Score the alternatives, inspect the ranking, and run sensitivity analysis before recommending a winner.
6. State the recommendation, instability points, data gaps, and next actions.

## Workflow

### 1. Frame the decision

Capture:

- decision question and scope
- system or subsystem boundary
- lifecycle stage and planning horizon
- decision makers and affected stakeholders
- hard constraints, assumptions, and exclusions
- evidence quality for each alternative

Keep elimination criteria separate from scored criteria. If an alternative violates a mandatory threshold, reject it before ranking.

### 2. Structure the criteria

Use a compact criteria set. In most trade studies, 4-9 top-level criteria is enough.

For each criterion, record:

- identifier and name
- direction: maximize benefit or minimize cost/risk/time
- unit or scoring scale
- weight
- scoring basis and evidence source
- any threshold or gating rule

Avoid double counting. If "performance" already includes range and throughput, do not score them again unless the hierarchy is explicit.

### 3. Select the method

Use the lightest method that can defend the decision:

- Weighted sum / SMART:
  Default for most system trade studies with explicit weights and normalized scores.
- TOPSIS:
  Use when stakeholders want "closest to ideal, farthest from worst" logic.
- AHP:
  Use when expert workshops can provide pairwise comparisons for criteria or subcriteria. Use AHP to derive weights, then rank with weighted sum or TOPSIS.
- MAUT / MAVT:
  Use when value is nonlinear, uncertainty or utility functions matter, or risk attitude must be modeled explicitly.
- ELECTRE / PROMETHEE / VIKOR:
  Use when poor performance in one criterion should not be fully compensated by strength elsewhere, or when a compromise solution is the goal.

For method selection details, read `references/method-selection.md`.

### 4. Build the scoring model

Normalize mixed units before aggregation. Keep the evidence basis consistent across alternatives.

Working rules:

- Mark subjective judgments clearly.
- Record missing or estimated data explicitly.
- Prefer traceable scales over ad hoc "gut feel" numbers.
- Keep two decimal places unless the underlying data supports more precision.
- If the user gives qualitative inputs only, propose a defensible ordinal or 1-5 rubric before scoring.

### 5. Rank and stress-test the result

Use the bundled scripts for deterministic analysis when the decision can be expressed as criteria, weights, and numeric scores:

- `scripts/trade_study_rank.py`: rank alternatives with `weighted-sum` or `topsis`
- `scripts/weight_sensitivity.py`: vary one criterion weight at a time and detect ranking instability

If the user needs AHP pairwise weighting, MAUT utility curves, or outranking logic, use this skill's workflow and references to structure the analysis manually instead of pretending the scripts cover those methods.

### 6. Produce the recommendation

Return a decision package with:

- decision statement
- method and why it fits
- alternatives considered
- criteria table with weights and rationale
- ranking table
- top trade-offs and dominant drivers
- sensitivity findings
- recommendation with caveats
- risks, missing data, and next actions

Prefer tables. If the ranking changes under small weight adjustments, call the decision unstable and recommend further evidence gathering before commitment.

## Output Pattern

Use this structure unless the user asks for another format:

1. Decision context
2. Alternatives and exclusions
3. Criteria, weights, and scoring basis
4. Method and assumptions
5. Ranking results
6. Sensitivity analysis
7. Recommendation and residual risk

## MBSE Notes

When the request touches MBSE or SysML, keep traceability explicit:

- stakeholder need or requirement
- evaluation criterion or measure of effectiveness
- alternative architecture or concept
- trade study model or parametric calculation
- decision outcome and rationale

Do not present the trade study as isolated from requirements, risk, and verification concerns.

## Resources

- `references/method-selection.md`: method chooser, scoring guidance, and decision-package template
- `scripts/trade_study_model.py`: shared parser and scoring engine for the CLI tools
- `scripts/trade_study_rank.py`: deterministic ranking for weighted sum and TOPSIS
- `scripts/weight_sensitivity.py`: one-at-a-time weight perturbation analysis

## Script Usage

Rank a study:

```bash
python skills/systems-engineering-mcda/scripts/trade_study_rank.py decision.json --method weighted-sum
python skills/systems-engineering-mcda/scripts/trade_study_rank.py decision.json --method topsis --output-csv ranking.csv
```

Run sensitivity analysis:

```bash
python skills/systems-engineering-mcda/scripts/weight_sensitivity.py decision.json --method weighted-sum --delta 0.1
```

Expected JSON shape:

```json
{
  "method": "weighted-sum",
  "criteria": [
    {
      "id": "performance",
      "name": "Mission performance",
      "weight": 0.35,
      "direction": "max"
    },
    {
      "id": "cost",
      "name": "Lifecycle cost",
      "weight": 0.25,
      "direction": "min"
    },
    {
      "id": "risk",
      "name": "Technical risk",
      "weight": 0.2,
      "direction": "min"
    }
  ],
  "alternatives": [
    {
      "id": "A",
      "name": "Option A",
      "scores": {
        "performance": 82,
        "cost": 115,
        "risk": 0.32
      }
    },
    {
      "id": "B",
      "name": "Option B",
      "scores": {
        "performance": 77,
        "cost": 95,
        "risk": 0.25
      }
    }
  ]
}
```

If the input is incomplete, fill the gaps transparently and mark the output as a proposed study model rather than an authoritative decision.
