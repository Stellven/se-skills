# Repository Guidelines

## Project Structure & Module Organization
This repository is a MkDocs-based documentation site for software engineering topics. Author source content in `docs/`, with top-level pages such as `docs/coding.md`, `docs/system-design.md`, and tool-specific content under `docs/tools/`. Site configuration lives in `mkdocs.yml`. Python helper logic lives in `tools/`; at present, `tools/prompts.py` is the only checked-in module. `site/` contains generated output and should be treated as build artifacts, not hand-edited source. Planning drafts live under `.sisyphus/`.

## Build, Test, and Development Commands
Set up a virtual environment and install dependencies before editing:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Use `mkdocs serve` to run the local docs server at `http://127.0.0.1:8000`. Use `mkdocs build` to regenerate the static site into `site/`. If you touch Python helpers, run `python -m py_compile tools/*.py` for a fast syntax check.

## Coding Style & Naming Conventions
Write documentation in clear, instructional Markdown with short sections and descriptive headings. Keep filenames lowercase with hyphens only when adding nested pages; current top-level docs use simple names like `system-engineering.md`. In Python, follow PEP 8: 4-space indentation, snake_case for variables/functions, and module-level constants in UPPER_SNAKE_CASE, as shown in `tools/prompts.py`.

## Testing Guidelines
There is no automated test suite in this workspace yet. Treat `mkdocs build` as the baseline validation step for all content changes. For documentation updates, verify links, headings, and code fences render correctly in `mkdocs serve`. For Python changes, combine `python -m py_compile tools/*.py` with a focused manual run of the affected command if the implementation exists in the repo.

## Commit & Pull Request Guidelines
Git history is not available in this workspace, so follow a simple, consistent convention: use imperative commit subjects such as `docs: expand system design page` or `tools: refine architect prompts`. Keep commits scoped to one concern. Pull requests should include a short summary, affected paths, manual verification steps, and screenshots only when UI or rendered-doc output changed materially.

## Configuration & Content Notes
Dependencies are declared in `requirements.txt`; update that file when adding MkDocs plugins or Python packages. The docs mention `tools/architect.py`, but it is not currently present, so confirm tool references against the actual repository state before documenting new workflows.
