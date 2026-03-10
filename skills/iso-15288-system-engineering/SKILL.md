---
name: iso-15288-system-engineering
description: Apply ISO/IEC/IEEE 15288:2023 system life cycle processes to systems engineering work. Use when Codex needs to structure stakeholder needs, system requirements, architecture, design decomposition, integration, verification, validation, transition, operation, maintenance, disposal, technical management, agreement activities, or lifecycle tailoring for a system or system-of-systems task.
---

# ISO 15288 System Engineering

Use this skill to turn vague system problems into lifecycle-structured engineering outputs. Base the work on ISO/IEC/IEEE 15288:2023 process thinking and use ISO/IEC/IEEE 24748-2:2024 as application guidance when tailoring.

## Quick Start

1. Identify the system of interest, lifecycle stage, stakeholders, and success criteria.
2. Decide which 15288 process group is dominant: agreement, organizational project-enabling, technical management, or technical.
3. Tailor the minimum process set needed for the request instead of forcing the full standard.
4. Produce concrete outputs: requirement sets, architecture views, verification matrices, risk logs, plans, or lifecycle decisions.
5. Keep traceability explicit from stakeholder need to requirement, architecture element, verification method, and validation outcome.

## Workflow

### 1. Frame the engineering context

Capture:

- system of interest and boundaries
- mission, business objective, or operational problem
- lifecycle stage: concept, development, production, utilization, support, or retirement
- stakeholders, constraints, assumptions, and critical risks
- whether the request is for a system, subsystem, service, or system of systems

If the request is underspecified, state assumptions before decomposing the work.

### 2. Select the process path

Use the dominant path below and pull in adjacent processes only when needed:

- Requirements and problem framing: stakeholder needs and requirements definition, system requirements definition
- Solution shaping: architecture definition, design definition, system analysis
- Delivery readiness: implementation, integration, verification, validation, transition
- In-service change: operation, maintenance, disposal
- Project control: planning, assessment and control, risk, decision management, configuration, information, measurement, quality
- Commercial boundary: acquisition or supply
- Organizational capability: lifecycle model management, infrastructure, portfolio, human resources, quality, knowledge

For the full process map and expected outputs, read `references/process-map.md`.

### 3. Produce lifecycle-consistent outputs

Match the output to the user request:

- For strategy or concept work, produce mission context, stakeholders, use scenarios, constraints, and candidate concepts.
- For requirements work, separate stakeholder needs from system requirements and assign identifiers, rationale, source, and verification method.
- For architecture work, define logical and physical decomposition, interfaces, allocations, quality attribute tradeoffs, and key decisions.
- For execution planning, produce lifecycle plans, milestones, entry/exit criteria, and risk-driven reviews.
- For V&V work, distinguish verification against requirements from validation against stakeholder intent.
- For operations or sustainment work, cover deployment, support concept, maintenance triggers, incident feedback, and retirement criteria.

Prefer tables and matrices when they improve traceability.

### 4. Tailor instead of copying the standard

Tailor by:

- removing irrelevant lifecycle processes
- scaling artifacts to system size and criticality
- choosing review depth based on risk and novelty
- making recursive decomposition explicit for subsystems
- noting where agile, DevOps, MBSE, or hardware-heavy delivery changes the implementation, not the intent

Do not claim that 15288 prescribes a single lifecycle model. It does not.

## Output Patterns

### Requirements package

Produce:

- context and scope
- stakeholder concerns
- stakeholder requirements
- system requirements
- traceability matrix
- verification approach summary

### Architecture package

Produce:

- architectural drivers
- candidate viewpoints
- decomposition and interfaces
- technology and make/buy decisions
- risks and tradeoffs
- verification and validation implications

### Lifecycle review package

Produce:

- selected process set
- major artifacts and owners
- entrance and exit criteria
- top risks and mitigations
- open decisions
- next review recommendation

## Working Rules

- Keep stakeholder needs, system requirements, design decisions, and test evidence distinct.
- Prefer measurable requirements and explicit interfaces.
- Call out missing operational, maintenance, safety, security, or disposal considerations.
- When inferring artifacts not given by the user, label them as proposed rather than authoritative.
- Summarize the standard; do not present invented clause citations or unverifiable quotes.

## Resources

- `scripts/requirements_lint.py`: check requirement quality, IDs, trace fields, and common ambiguity patterns from JSON input
- `scripts/traceability_matrix.py`: generate a CSV traceability matrix from stakeholder, system, and verification records in JSON
- `references/process-map.md`: condensed 15288:2023 process groups, usage guidance, and artifact checklist

## Script Usage

Use scripts when the task is deterministic and repetitive:

- Lint requirement quality:
  `python skills/iso-15288-system-engineering/scripts/requirements_lint.py requirements.json`
- Generate a traceability matrix:
  `python skills/iso-15288-system-engineering/scripts/traceability_matrix.py requirements.json --output matrix.csv`

Expected JSON shape:

```json
{
  "stakeholder_requirements": [
    {
      "id": "STK-001",
      "text": "The operator shall configure the robot in less than 10 minutes.",
      "source": "Operations team"
    }
  ],
  "system_requirements": [
    {
      "id": "SYS-001",
      "text": "The system shall complete initial setup within 600 seconds.",
      "source_ids": ["STK-001"],
      "verification_method": "test"
    }
  ],
  "verification_requirements": [
    {
      "id": "VER-001",
      "requirement_ids": ["SYS-001"],
      "method": "test",
      "evidence": "setup-timer-test"
    }
  ]
}
```
