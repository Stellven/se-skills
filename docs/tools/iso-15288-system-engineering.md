# ISO 15288 Systems Engineering Skill

The **ISO 15288 Systems Engineering Skill** helps structure systems engineering work using the lifecycle processes from ISO/IEC/IEEE 15288:2023.

## What It Is For

Use this skill when a task needs more than generic system design advice, for example:

- translating stakeholder needs into system requirements
- decomposing a system into architecture and design elements
- planning integration, verification, validation, and transition
- reviewing lifecycle gaps in operations, maintenance, or disposal
- tailoring systems engineering activities for a project or system of systems

## What the Skill Produces

Depending on the request, the skill can help produce:

- stakeholder and system requirement sets
- traceability matrices
- architecture decomposition and interface definitions
- verification and validation plans
- lifecycle review packages
- risk, decision, and configuration-oriented management outputs

## Requirements Management Scripts

The skill now includes deterministic scripts for common requirements work:

- `skills/iso-15288-system-engineering/scripts/requirements_lint.py`
  checks requirement IDs, missing trace fields, missing verification methods, and common ambiguous wording.
- `skills/iso-15288-system-engineering/scripts/traceability_matrix.py`
  converts stakeholder, system, and verification relationships in JSON into a CSV traceability matrix.

Example:

```bash
python skills/iso-15288-system-engineering/scripts/requirements_lint.py requirements.json
python skills/iso-15288-system-engineering/scripts/traceability_matrix.py requirements.json --output matrix.csv
```

## How to Invoke It

Invoke the skill explicitly in a Codex prompt:

```text
Use $iso-15288-system-engineering to turn this product idea into a lifecycle-structured systems engineering package.
```

Example:

```text
Use $iso-15288-system-engineering to derive stakeholder requirements, system requirements, architecture drivers, and a verification approach for an autonomous warehouse robot.
```

## How It Works

The skill first frames the system context, lifecycle stage, stakeholders, and constraints. It then selects the relevant ISO 15288 process path instead of forcing the full standard on every request. The output keeps traceability visible across stakeholder need, requirement, architecture, and V&V activities.

The main skill instructions live in `skills/iso-15288-system-engineering/SKILL.md`. A condensed process reference is available in `skills/iso-15288-system-engineering/references/process-map.md`.

## Notes

- The skill is based on ISO/IEC/IEEE 15288:2023 process thinking.
- It is intended to support engineering work, not replace the full standard text.
- It is most useful for systems work that spans requirements, architecture, realization, and lifecycle management.
