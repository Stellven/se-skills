# SE Skills

A documentation site for Software Engineering skills.

## Prerequisites

- Python 3.8+

## Setup

1.  Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Run the development server:
    ```bash
    mkdocs serve
    ```

4.  Open `http://127.0.0.1:8000` in your browser.

## Structure

- `docs/`: Markdown documentation files
- `mkdocs.yml`: Configuration file

## Hermes PowerPoint Skill

Full usage guide: `docs/tools/hermes-powerpoint.md`.

Install the NousResearch/Hermes PowerPoint skill into the active Codex
environment:

```bash
python tools/hermes_powerpoint.py --install-skill
```

Restart Codex after installing the skill. Then generate a PPTX from a document
with the Codex agent path:

```bash
python tools/hermes_powerpoint.py docs/coding.md --agent --out outputs/presentations/coding.pptx
```

For a deterministic local draft without launching a nested Codex run:

```bash
python tools/hermes_powerpoint.py docs/coding.md --out outputs/presentations/coding.pptx
```

The input can be PDF, Markdown, plain text, simple RTF, or Microsoft Word
`.docx` / `.docm`. Legacy `.doc` works on macOS when `textutil` is available;
otherwise convert it to `.docx` first.

Word input example:

```bash
python tools/hermes_powerpoint.py inputs/presentations/report.docx --agent --out outputs/presentations/report.pptx
```
