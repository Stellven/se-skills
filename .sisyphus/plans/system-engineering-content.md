# Plan: System Engineering Content Expansion

## TL;DR

> **Quick Summary**: Restructure the documentation to distinguish between **DevOps** (Infrastructure) and **System Engineering** (Holistic/Industrial). Rename existing content to `devops.md` and create a new `system-engineering/` section with core methodologies.
>
> **Deliverables**:
> - `docs/devops.md` (Renamed from old `system-engineering.md`)
> - `docs/system-engineering/` directory with 4 new topic files
> - Updated `mkdocs.yml` navigation
>
> **Estimated Effort**: Quick
> **Parallel Execution**: Sequential (Rename -> Create -> Update Config)
> **Critical Path**: Rename existing file first to prevent data loss.

---

## Context

### Original Request
Analyze project files and build a "System Engineering Skills" directory.

### Metis Gap Analysis
**Crucial Finding**: `docs/system-engineering.md` *already exists* but contains DevOps content (Linux, Networking).
**Correction**:
1. **Rename** existing file to `devops.md` to preserve it.
2. **Create** `docs/system-engineering/` folder for the *new* requested content (Requirements, V-Model, etc.).
3. **Clarify** `reliability.md`: Focus on SRE (SLOs/Error Budgets) as requested, distinct from pure hardware reliability.

---

## Work Objectives

### Core Objective
Establish a dedicated "System Engineering" section without losing existing DevOps context.

### Concrete Deliverables
- [ ] `docs/devops.md` (Preserved content)
- [ ] `docs/system-engineering/index.md`
- [ ] `docs/system-engineering/requirements.md`
- [ ] `docs/system-engineering/lifecycle.md`
- [ ] `docs/system-engineering/verification-validation.md`
- [ ] `docs/system-engineering/reliability.md`
- [ ] Updated `mkdocs.yml`

### Definition of Done
- [ ] `mkdocs build` succeeds.
- [ ] Navigation shows "DevOps" AND "System Engineering" (as a folder).
- [ ] Old content is accessible under "DevOps".

### Must Have
- Clear distinction between "System Design" (Software Arch), "DevOps" (Infra), and "System Engineering" (Holistic).

### Must NOT Have
- Overwriting of existing `system-engineering.md` content.

---

## Verification Strategy

### Test Decision
- **Infrastructure exists**: N/A (Documentation)
- **Automated tests**: None.
- **Agent-Executed QA**: MANDATORY.

### Agent-Executed QA Scenarios

```
Scenario: Verify Content Preservation
  Tool: interactive_bash
  Steps:
    1. ls -l docs/devops.md
    2. Assert: File exists
    3. grep "Linux" docs/devops.md
    4. Assert: Exit code 0 (Content preserved)

Scenario: Verify New Structure
  Tool: interactive_bash
  Steps:
    1. ls -R docs/system-engineering/
    2. Assert: requirements.md exists
    3. Assert: lifecycle.md exists
    4. Assert: reliability.md exists

Scenario: Verify MkDocs Config
  Tool: interactive_bash
  Steps:
    1. cat mkdocs.yml
    2. Assert: Contains "- DevOps: devops.md"
    3. Assert: Contains "- System Engineering:"
    4. mkdocs build
    5. Assert: Build successful
```

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Refactor):
└── Task 1: Rename and Preserve (Blocking)

Wave 2 (Creation):
└── Task 2: Create System Engineering Structure (Parallelizable files)

Wave 3 (Integration):
└── Task 3: Update Navigation & Verify
```

---

## TODOs

- [ ] 1. Safe Rename & Preservation
  **What to do**:
  - Check content of `docs/system-engineering.md`.
  - Rename it to `docs/devops.md`.
  - Update any internal links if necessary (unlikely for simple docs).

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`bash`]

  **Acceptance Criteria**:
  - [ ] `docs/devops.md` exists.
  - [ ] `docs/system-engineering.md` does NOT exist (as a file).

- [ ] 2. Create System Engineering Content
  **What to do**:
  - Create `docs/system-engineering/` directory.
  - Create `index.md`: Overview of SysEng vs SysDesign.
  - Create `requirements.md`: Requirements Engineering (Functional/Non-Functional).
  - Create `lifecycle.md`: SDLC vs V-Model.
  - Create `verification-validation.md`: V&V definitions.
  - Create `reliability.md`: SRE principles (SLAs/SLOs).

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: [`markdown`]

  **Acceptance Criteria**:
  - [ ] All 5 files created with basic structure/headers.

- [ ] 3. Update Configuration & Verify
  **What to do**:
  - Edit `mkdocs.yml`:
    - Add `DevOps: devops.md`.
    - Change `System Engineering` to a list (folder structure).
  - Run verification scenarios.

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`bash`]

  **Acceptance Criteria**:
  - [ ] MkDocs build passes.
  - [ ] Navigation structure is correct.
