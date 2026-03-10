# Plan: System Architect Agent Skill

## TL;DR

> **Quick Summary**: Create a Python CLI tool (`tools/architect.py`) that acts as an AI System Architect. It takes a natural language description and generates a complete architectural design package (Requirements, Architecture, API Specs) using Google's Gemini API.
>
> **Deliverables**:
> - `tools/architect.py`: The CLI agent.
> - `requirements.txt`: Updated dependencies.
> - `docs/tools/architect.md`: Documentation for the tool.
> - `design/`: Directory for generated outputs.
>
> **Estimated Effort**: Medium
> **Parallel Execution**: Sequential (Dependencies -> Tool -> Docs)
> **Critical Path**: Setup Env -> Implement CLI -> Verify

---

## Context

### Original Request
Operationalize "System Architecture / Design" methodologies into an executable agent skill using Python and Gemini.

### Interview Summary
**Key Decisions**:
- **Format**: Python CLI (`typer`) using `google-generativeai`.
- **Provider**: Google Gemini (requires `GOOGLE_API_KEY`).
- **Output**: Modular Markdown files in `design/{project_name}/`.
- **Depth**: Conceptual design + Mermaid diagrams + API sketches.

### Metis Review
**Incorporated Guardrails**:
- **Validation**: Strict checks for `GOOGLE_API_KEY`.
- **Output**: Modular generation (Analyze -> Architect -> Detail).
- **Versioning**: Output to named subfolders to prevent overwriting.
- **Safety**: No implementation code generation, only design artifacts.

---

## Work Objectives

### Core Objective
Enable users to generate comprehensive system designs from a single text prompt.

### Concrete Deliverables
- [ ] `tools/architect.py` (CLI entry point)
- [ ] `tools/prompts.py` (System prompts for each stage)
- [ ] `mkdocs.yml` updated with "Tools" section
- [ ] `docs/tools/architect.md` user guide

### Definition of Done
- [ ] `python tools/architect.py --help` runs without error.
- [ ] Tool successfully generates `requirements.md`, `architecture.md`, and `api.md` from a test prompt.
- [ ] Generated Markdown contains valid Mermaid diagram syntax.
- [ ] MkDocs site builds and displays the new tool documentation.

### Must Have
- Chain-of-Thought reasoning for architectural choices.
- Separation of Functional vs Non-Functional requirements.
- Mermaid JS diagrams for components.

### Must NOT Have
- Automatic code generation (implementation).
- Hardcoded API keys.

---

## Verification Strategy

### Test Decision
- **Infrastructure exists**: No (creating new tool).
- **Automated tests**: None (Manual Agent-Executed QA).
- **Agent-Executed QA**: MANDATORY.

### Agent-Executed QA Scenarios

```
Scenario: CLI Help Check
  Tool: interactive_bash (tmux)
  Preconditions: Virtualenv activated, dependencies installed
  Steps:
    1. tmux new-session: python tools/architect.py --help
    2. Assert: stdout contains "Usage: architect.py"
    3. Assert: stdout contains "--name"
    4. Assert: exit code 0
  Expected Result: Help message displayed correctly
  Evidence: Terminal output

Scenario: Generate Design (Dry Run / Test)
  Tool: interactive_bash (tmux)
  Preconditions: GOOGLE_API_KEY set (or mocked), Virtualenv activated
  Steps:
    1. tmux new-session: python tools/architect.py plan "A simple todo list CLI" --name test-todo
    2. Wait for: "Generating requirements..."
    3. Wait for: "Generating architecture..."
    4. Wait for: "Done"
    5. ls design/test-todo/
    6. Assert: requirements.md exists
    7. Assert: architecture.md exists
    8. grep "```mermaid" design/test-todo/architecture.md
    9. Assert: exit code 0 (pattern found)
  Expected Result: Design artifacts generated with correct structure
  Evidence: File listing and grep output
```

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Setup):
└── Task 1: Environment & Dependencies

Wave 2 (Implementation):
├── Task 2: Prompt Engineering (prompts.py)
└── Task 3: CLI Implementation (architect.py)

Wave 3 (Integration):
├── Task 4: Documentation (MkDocs)
└── Task 5: Verification (QA)
```

---

## TODOs

- [ ] 1. Environment & Dependencies Setup

  **What to do**:
  - Update `requirements.txt` with `google-generativeai`, `typer`, `rich`, `pydantic`.
  - Create `tools/` directory.
  - Create `design/` directory.

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`bash`]

  **Parallelization**:
  - **Can Run In Parallel**: NO (Blocks everything)
  - **Parallel Group**: Wave 1

  **Acceptance Criteria**:
  - [ ] `pip install -r requirements.txt` succeeds
  - [ ] `ls tools/` shows directory exists

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: Dependency Check
    Tool: interactive_bash
    Steps:
      1. pip install -r requirements.txt
      2. python -c "import google.generativeai; import typer; print('OK')"
      3. Assert: stdout equals "OK"
  ```

- [ ] 2. Implement System Prompts (`tools/prompts.py`)

  **What to do**:
  - Create `tools/prompts.py`.
  - Define 3 prompt templates:
    1. `REQUIREMENTS_PROMPT`: Extract FR/NFRs.
    2. `ARCHITECTURE_PROMPT`: Select patterns + C4 Component diagram (Mermaid).
    3. `API_PROMPT`: Define API endpoints and Data models.

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: [`python`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2

  **References**:
  - `docs/system-design.md` - Match the style defined there.

  **Acceptance Criteria**:
  - [ ] File contains `REQUIREMENTS_PROMPT`, `ARCHITECTURE_PROMPT`, `API_PROMPT` variables.
  - [ ] Prompts explicitly request Markdown format.

- [ ] 3. Implement CLI Tool (`tools/architect.py`)

  **What to do**:
  - Create `tools/architect.py` using `typer`.
  - Implement `plan` command:
    - Input: `description`, `--name`.
    - Check `GOOGLE_API_KEY`.
    - Init `GenerativeModel('gemini-1.5-flash')`.
    - Chain calls: Prompts -> Gemini -> File Write.
    - Use `rich` for status spinners.

  **Recommended Agent Profile**:
  - **Category**: `ultrabrain`
  - **Skills**: [`python`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2
  - **Blocked By**: Task 1

  **Acceptance Criteria**:
  - [ ] Script runs with `--help`.
  - [ ] Script fails gracefully if API key missing.
  - [ ] Script creates output directory if missing.

- [ ] 4. Documentation & Integration

  **What to do**:
  - Update `mkdocs.yml`: Add "Tools" -> "System Architect" to nav.
  - Create `docs/tools/architect.md`:
    - Explain how to use the tool.
    - Prerequisites (API Key).
    - Example output.

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: [`markdown`]

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3
  - **Blocked By**: Task 3

  **Acceptance Criteria**:
  - [ ] `mkdocs build` succeeds.
  - [ ] `docs/tools/architect.md` exists.

- [ ] 5. Final Verification (QA)

  **What to do**:
  - Run the tool end-to-end with a real (or mock) prompt.
  - Verify all outputs.

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`bash`]

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3

  **Acceptance Criteria**:
  - [ ] All QA scenarios pass.
