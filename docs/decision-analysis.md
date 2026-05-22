# Decision Analysis Skills (MCDA)

Multi-Criteria Decision Analysis (MCDA / MCDM) is a mature and crucial domain within System Engineering. It provides structured methodologies for Trade Studies, architecture selection, technology evaluation, and investment planning when dealing with multiple, often conflicting, objectives and diverse stakeholders.

## Core Concepts

MCDA focuses on evaluating and prioritizing a set of **Alternatives** ($A_1, A_2 ... A_n$) against multiple **Criteria** ($C_1, C_2 ... C_m$).

**Key Objectives of MCDA:**
- **Ranking**: Ordering alternatives from best to worst.
- **Selection**: Identifying the single optimal alternative.
- **Trade-off Analysis**: Balancing conflicting criteria (e.g., Cost vs. Performance).

## Common MCDA Methods

MCDA methodologies in system engineering generally fall into these major categories:

### 1. Analytic Hierarchy Process (AHP)
AHP is one of the most widely used methods in systems engineering, developed by Thomas Saaty.
- **Concept**: Decomposes the decision into a hierarchy (Goal -> Criteria -> Sub-criteria -> Alternatives).
- **Process**: Uses pairwise comparisons to establish weights and evaluate alternatives.
- **Pros**: Clear structure; intuitive for domain experts to participate in.
- **Cons**: High degree of subjectivity in pairwise scoring.

### 2. MAUT / MAVT (Multi-Attribute Utility/Value Theory)
- **Concept**: Converts different criteria into a unified utility or value function: $U(a) = \sum w_i u_i(a)$
- **Characteristics**: Rigorous theoretical foundation; capable of incorporating risk preferences.
- **Use Cases**: Defense systems engineering, aerospace project evaluation.

### 3. TOPSIS (Distance-Based)
Technique for Order Preference by Similarity to Ideal Solution.
- **Concept**: The best alternative should be closest to the ideal solution and farthest from the negative-ideal solution.
- **Process**: Normalizes the decision matrix, applies weights, calculates ideal solutions, and measures geometric distances.
- **Prevalence**: Highly common in engineering evaluations.

### 4. ELECTRE & PROMETHEE (Outranking)
- **Concept**: Determines if one alternative "outranks" (is preferred over) another based on concordance and discordance indices.
- **Pros**: Suitable for complex decisions; doesn't require complete compensation (poor performance in one criteria isn't totally offset by excellence in another).
- **Cons**: Algorithmically complex.

### 5. VIKOR (Optimization/Compromise)
- **Concept**: Seeks a compromise solution that is closest to the ideal.
- **Use Cases**: Supply chain optimization, resource planning, and engineering design where conflicting criteria require a negotiated solution.

## The Trade Study Process

In System Engineering, MCDA is typically executed as a **Trade Study**. A standard workflow (common in NASA/DoD) looks like this:

1. **Define Criteria**: Establish technical, cost, risk, schedule, and scalability metrics.
2. **Weight Criteria**: Assign relative importance to each metric.
3. **Evaluate Alternatives**: Score each candidate solution against the criteria.
4. **Aggregate Score**: Combine scores using an MCDA method.
5. **Sensitivity Analysis**: Test how changes in weights or scores affect the final ranking.

## Software Tools

System Engineers often leverage specialized tools to process complex MCDA matrices:
- **Commercial Software**: DecisionPlus (AHP/SMART), DecideIT (MAVT), Expert Choice.
- **Python Libraries**: `scikit-criteria`, `pyDecision`, `pymcdm`.

## AI Agents & System Engineering

In modern MBSE (Model-Based Systems Engineering) and the development of AI Agent Systems (like SysML v2 + Agent Skills), MCDA principles are vital.

An AI system should possess **MCDA Skills** to function as an **Autonomous System Trade Study Agent**, capable of autonomously performing criteria weighting, alternative evaluation, and sensitivity analysis during architectural design loops.
