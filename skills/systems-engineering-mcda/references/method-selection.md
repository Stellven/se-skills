# Systems Engineering MCDA Method Selection

## Method chooser

| Method | Use when | Strengths | Watchouts |
| --- | --- | --- | --- |
| Weighted sum / SMART | Need a practical trade study with explicit weights and normalized data | Fast, explainable, easy to audit | Fully compensatory; normalization choice matters |
| TOPSIS | Want "closest to ideal, farthest from worst" logic | Intuitive for engineering comparisons | Sensitive to scaling and correlated criteria |
| AHP | Need expert pairwise comparisons for criteria or subcriteria | Good for weight elicitation and hierarchy | Subjective; consistency must be checked |
| MAUT / MAVT | Need utility/value functions, thresholds, or risk attitude | Strong theoretical basis | More modeling effort |
| ELECTRE / PROMETHEE | Need outranking and limited compensation | Handles veto-like behavior | Harder to explain and parameterize |
| VIKOR | Need a compromise solution near the ideal | Useful for negotiated decisions | Interpretation can be non-obvious |

## Recommended default path

For most systems engineering trade studies:

1. Frame the decision and remove infeasible alternatives.
2. Define criteria and weights.
3. Use weighted sum as the baseline.
4. Re-run with TOPSIS if stakeholders care about closeness to an ideal profile.
5. Run sensitivity analysis on the baseline weights.

Escalate to AHP, MAUT/MAVT, or outranking methods only when the decision characteristics justify the extra complexity.

## Criteria design rules

- Keep criteria mutually distinct.
- Separate benefits from costs, risks, and schedule drivers.
- Use measurable evidence where possible.
- Define the direction of preference for every criterion.
- Record whether a score is measured, estimated, or expert-judged.
- Treat hard thresholds as gates, not just low scores.

## Weighting guidance

- Normalize weights so they sum to 1.0.
- Use AHP or workshop ranking only when experts can explain the source of preference.
- If weights are politically negotiated, note that the result is value-laden rather than purely technical.
- Test the recommendation with at least one-at-a-time weight variation.

## Sensitivity interpretation

Treat the decision as unstable when:

- the top-ranked alternative changes under small weight shifts
- alternatives cluster with near-identical scores
- one criterion dominates because of an arbitrary scale choice
- missing data or assumed values drive the winner

When instability appears, recommend one of:

- collect better evidence
- simplify or redefine overlapping criteria
- separate hard constraints from preferences
- move to scenario-based analysis instead of a single ranking

## Trade study package template

Use this output shape in reports and reviews:

1. Decision statement and scope
2. Alternatives considered and exclusions
3. Criteria table with definitions, weights, and data sources
4. Method selection rationale
5. Ranked results
6. Sensitivity findings
7. Recommendation, caveats, and follow-up actions

## MBSE alignment

In MBSE-heavy work, connect:

- stakeholder needs and requirements
- measures of effectiveness and performance
- candidate architectures or concepts
- parametric trade study calculations
- decision rationale and downstream verification impact

This prevents the MCDA result from becoming a disconnected spreadsheet exercise.
