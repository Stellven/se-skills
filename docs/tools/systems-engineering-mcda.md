# Systems Engineering MCDA Skill

The **Systems Engineering MCDA Skill** supports multi-criteria decision analysis for system trade studies, architecture selection, technology evaluation, and other option-comparison work.

## What It Is For

Use this skill when a task needs a structured comparison across competing alternatives, for example:

- evaluating candidate system architectures
- running a concept or technology trade study
- comparing cost, performance, risk, and schedule across options
- selecting a method such as weighted scoring, TOPSIS, AHP, or MAUT/MAVT
- checking whether a recommendation is stable under weight changes

## What the Skill Produces

Depending on the request, the skill can produce:

- a decision statement and scope definition
- alternatives and exclusion rules
- criteria tables with weights and rationale
- ranked trade-study outputs
- sensitivity analysis findings
- recommendation packages with caveats and next actions

## Built-in Scripts

The skill includes deterministic Python scripts for common numeric trade-study work:

- `skills/systems-engineering-mcda/scripts/trade_study_rank.py`
  ranks alternatives using `weighted-sum` or `topsis`
- `skills/systems-engineering-mcda/scripts/weight_sensitivity.py`
  varies one criterion weight at a time and reports ranking instability

Example:

```bash
python skills/systems-engineering-mcda/scripts/trade_study_rank.py decision.json --method weighted-sum
python skills/systems-engineering-mcda/scripts/weight_sensitivity.py decision.json --method weighted-sum --delta 0.1
```

## How to Invoke It

Invoke the skill explicitly in a Codex prompt:

```text
Use $systems-engineering-mcda to evaluate these system alternatives with explicit criteria, weights, and sensitivity analysis.
```

Example:

```text
Use $systems-engineering-mcda to compare three autonomy stack options for an unmanned vehicle, weight performance, lifecycle cost, technical risk, and schedule, then recommend one with sensitivity analysis.
```

## How It Works

The skill frames the decision, separates hard constraints from scored criteria, selects an MCDA method, and then produces a traceable ranking and recommendation. It defaults to practical trade-study approaches first and escalates to more advanced methods only when the decision context requires them.

The main skill instructions live in `skills/systems-engineering-mcda/SKILL.md`. Method-selection guidance is in `skills/systems-engineering-mcda/references/method-selection.md`.

## Notes

- The skill is derived from a systems-engineering MCDA workflow, including trade study, ranking, and sensitivity analysis practices.
- It supports engineering judgment; it does not replace stakeholder alignment or data quality review.
- It is most effective when criteria, weights, and evidence sources are explicit.
