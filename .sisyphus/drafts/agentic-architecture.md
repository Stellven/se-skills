# Draft: Agentic System Architecture Workflow

## Goal
Operationalize "System Architecture / Design" as an automated agent workflow.

## Core Concept: "The Architect Agent"
Transform the abstract "System Design" process into a concrete, executable pipeline.

### Workflow Stages (The "Skill")
1.  **Requirement Extraction**
    - Input: Raw user prompt/PRD.
    - Action: Identify Functional Requirements (FR) and Non-Functional Requirements (NFR).
    - Output: Structured JSON (e.g., `{"fr": [...], "nfr": {"scalability": "high", "latency": "low"}}`).

2.  **Pattern Selection (Strategy)**
    - Input: Requirements.
    - Action: Select architectural pattern (Microservices, Event-Driven, Monolith, Serverless).
    - Constraint: Must justify choice based on NFRs (e.g., "Chosen Event-Driven for high scalability").

3.  **Component Design (Structure)**
    - Action: Define core services/modules.
    - Output: Component diagram (Mermaid `graph TD`).

4.  **Data & Interface Design (Detail)**
    - Action: Define database schemas and API contracts.
    - Output: ER Diagram (Mermaid `erDiagram`) and Interface definitions.

5.  **Critique & Refinement (Verification)**
    - Action: "Devil's Advocate" pass. Challenge the design against constraints (CAP theorem, cost, complexity).
    - Output: Refined design + Risk Assessment.

## Technical Implementation (Confirmed)
- **Format**: Python CLI Script (`tools/architect.py`).
- **Dependencies**: `google-generativeai` (Gemini SDK), `typer` (CLI), `rich` (UI), `pydantic` (Schema validation).
- **Environment**: Requires `GOOGLE_API_KEY`.
- **Output**: Modular Spec Folder (`design/requirements.md`, `design/architecture.md`, `design/components.md`).
- **Depth**: Conceptual Design (High-level components, data flow).

## Workflow Steps (The "Skill")
1.  **Capture**: User inputs project description via CLI prompt.
2.  **Analyze (Gemini)**: Extract FR/NFR into structured JSON.
3.  **Design (Gemini)**: Propose 3 architectural options, ask user to select one (or auto-select best).
4.  **Detail (Gemini)**: Generate component diagrams (Mermaid) and API contracts based on selection.
5.  **Critique (Gemini)**: act as "Senior Architect" to review the design for flaws.
6.  **Write**: Save all artifacts to `design/` folder.

## Integration Plan
- Add `tools/` directory to `se-skills`.
- Update `requirements.txt` with new dependencies.
- Add `docs/tools/architect.md` to documentation site explaining how to use it.

