# ISO/IEC/IEEE 15288 Process Map

This reference is a condensed working map for applying ISO/IEC/IEEE 15288:2023. It is not a substitute for the standard text. Use it to choose processes, shape outputs, and keep lifecycle logic coherent.

## Reference Baseline

- Current standard: ISO/IEC/IEEE 15288:2023, edition 2, published May 2023
- Companion guidance: ISO/IEC/IEEE 24748-2:2024 for applying 15288
- Core idea: apply processes iteratively, concurrently, and recursively across the system hierarchy and lifecycle

## Process Groups

### Agreement Processes

Use when the work crosses an acquisition or supplier boundary.

- Acquisition: define need, solicit, select, govern, and accept supplied capability
- Supply: respond, commit, deliver, and support contractual obligations

Typical outputs:

- acquisition strategy
- statement of work or equivalent scope
- supplier commitments
- acceptance criteria
- delivery and acceptance records

### Organizational Project-Enabling Processes

Use when the request is about enterprise capability rather than one project.

- lifecycle model management
- infrastructure management
- portfolio management
- human resource management
- quality management
- knowledge management

Typical outputs:

- standard lifecycle model or policy
- capability roadmap
- shared methods, tools, and environments
- competency plans
- organizational lessons learned

### Technical Management Processes

Use when planning, controlling, or assuring engineering work.

- project planning
- project assessment and control
- decision management
- risk management
- configuration management
- information management
- measurement
- quality assurance

Typical outputs:

- integrated project plan
- milestone criteria
- risk register
- decision log
- configuration baseline
- information model or artifact register
- measures dashboard
- audit or quality findings

### Technical Processes

Use when defining, realizing, using, supporting, or retiring the system.

- business or mission analysis
- stakeholder needs and requirements definition
- system requirements definition
- architecture definition
- design definition
- system analysis
- implementation
- integration
- verification
- transition
- validation
- operation
- maintenance
- disposal

Typical outputs:

- mission context and concept of operations
- stakeholder requirements set
- system requirements specification
- architecture description and views
- design decomposition and interface definitions
- trade studies
- build or realization records
- integration plan and results
- verification matrix and evidence
- transition or deployment package
- validation scenarios and results
- operational procedures and support concept
- maintenance plan and change feedback
- retirement or disposal plan

## Minimal Tailoring Heuristics

### Small internal tool or service

Usually prioritize:

- stakeholder needs and requirements definition
- system requirements definition
- architecture definition
- implementation
- integration
- verification
- validation
- project planning
- risk management
- configuration management

### Safety-, mission-, or compliance-critical system

Expand with:

- explicit business or mission analysis
- stronger decision, information, and quality management
- formal transition and operations planning
- maintenance and disposal planning from the start
- deeper bidirectional traceability and review gates

### System of systems

Emphasize:

- boundary definition
- interface and interoperability management
- delegated authority and supplier coordination
- recursive decomposition and local autonomy assumptions

## Artifact Quality Checks

Before finalizing outputs, check:

- every requirement has a source and verification method
- every architectural element traces back to a requirement or constraint
- every verification activity maps to a requirement
- validation shows stakeholder value, not just requirement conformance
- operations, maintenance, and retirement are not omitted when lifecycle impact matters

## Suggested Response Shapes

- For analysis requests: use lifecycle stage, process selection, assumptions, recommended artifacts, and next actions.
- For document drafting: use numbered sections aligned to the chosen process set.
- For reviews: identify missing processes, weak traceability, lifecycle gaps, and unmanaged risk.
