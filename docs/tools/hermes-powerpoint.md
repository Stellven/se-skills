# Hermes PowerPoint Skill

The **Hermes PowerPoint Skill** turns a source document into an editable
PowerPoint `.pptx` deck. It can run in two modes:

- **Agent mode**: launches Codex and asks it to use the installed
  NousResearch/Hermes `powerpoint` skill.
- **Local mode**: generates a deterministic draft deck directly with Python.

Use agent mode for polished decks. Use local mode for quick drafts, smoke
tests, or automation where you do not want to launch a nested Codex process.

## Quick Start

From the repository root:

```bash
python tools/hermes_powerpoint.py inputs/presentations/report.docx \
  --agent \
  --out outputs/presentations/report.pptx
```

For a quick local draft:

```bash
python tools/hermes_powerpoint.py inputs/presentations/report.docx \
  --out outputs/presentations/report.pptx
```

## Recommended Folders

Put source files under:

```text
inputs/presentations/
```

Put generated decks under:

```text
outputs/presentations/
```

Example:

```text
se-skills/
  inputs/
    presentations/
      ai-daily-report.docx
  outputs/
    presentations/
      ai-daily-report.pptx
```

`outputs/` is ignored by Git, so generated decks do not accidentally become
source-controlled build artifacts.

## Supported Input Formats

| Format | Support | Notes |
|---|---|---|
| `.docx` | Supported | Recommended Word input format. Preserves titles, headings, lists, and tables as deck structure. |
| `.docm` | Supported | Read as a modern Word document. Macros are not executed. |
| `.doc` | Limited | Legacy Word format. Works on macOS when `textutil` is available; otherwise convert to `.docx`. |
| `.md` | Supported | Headings become slide sections; bullets become slide bullets. |
| `.txt` | Supported | Long lines are converted into slide bullets. |
| `.rtf` | Basic support | Best-effort text extraction. Use `.docx` for better structure. |
| `.pdf` | Supported | Text-based PDFs are extracted with `pypdf`; major figures are rendered with `PyMuPDF`; scanned PDFs need OCR first. |

## Install Dependencies

Create and activate the project virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

The local generator uses:

- `python-pptx` to create PowerPoint files
- `python-docx` to read Microsoft Word `.docx` / `.docm` files
- `pypdf` to extract text from text-based PDF files
- `PyMuPDF` to render major PDF figures into slide images

## Install The Hermes Skill

The upstream skill comes from:

- repository: `NousResearch/hermes-agent`
- path: `skills/productivity/powerpoint`
- installed local directory: `$CODEX_HOME/skills/hermes-powerpoint`

Run this from the repository root:

```bash
python tools/hermes_powerpoint.py --install-skill
```

Restart Codex after installation. The upstream skill declares its name as
`powerpoint`, so direct prompts can use:

```text
Use $powerpoint to create a PPTX deck from this document.
```

## Generate With Agent Mode

Agent mode starts a nested `codex exec` run. The prompt asks Codex to use the
Hermes `powerpoint` skill and points it at the input and output files.

```bash
python tools/hermes_powerpoint.py inputs/presentations/report.docx \
  --agent \
  --out outputs/presentations/report.pptx
```

Use this mode when:

- you want the Hermes skill instructions applied explicitly
- the source document needs interpretation, summarization, or cleanup
- you want a more presentation-aware result than the local fallback

## Generate With Local Mode

Local mode does not launch Codex. It reads the source document and creates a
structured draft deck directly.

```bash
python tools/hermes_powerpoint.py inputs/presentations/report.docx \
  --out outputs/presentations/report.pptx
```

Use this mode when:

- you want a fast draft
- you are testing document parsing
- you are running automation or CI-style checks

## Common Options

| Option | Purpose | Example |
|---|---|---|
| `--out` | Output `.pptx` path | `--out outputs/presentations/report.pptx` |
| `--agent` | Use nested Codex agent mode | `--agent` |
| `--title` | Override inferred deck title | `--title "AI Market Update"` |
| `--max-slides` | Limit total slide count | `--max-slides 8` |
| `--theme` | Choose local visual theme | `--theme teal` |
| `--install-skill` | Install upstream Hermes skill | `--install-skill` |

Available local themes:

- `executive`
- `teal`
- `charcoal`

Examples:

```bash
python tools/hermes_powerpoint.py inputs/presentations/report.docx \
  --agent \
  --title "AI Daily Brief" \
  --max-slides 8 \
  --out outputs/presentations/ai-daily-brief.pptx
```

```bash
python tools/hermes_powerpoint.py inputs/presentations/notes.md \
  --theme charcoal \
  --max-slides 6 \
  --out outputs/presentations/notes.pptx
```

## How Content Becomes Slides

The local generator uses these rules:

- Word `Title` or Markdown `#` becomes the deck title.
- Word `Heading 1` / `Heading 2` or Markdown headings become slide titles.
- Word lists and Markdown bullets become slide bullets.
- Word tables become slide sections named `Table 1`, `Table 2`, and so on.
- Long plain-text lines become bullets.
- The deck includes a title slide, content slides, and a closing slide.

Agent mode can go beyond these deterministic rules because Codex can interpret
the document and apply the full upstream PowerPoint skill guidance.

## How The Wrapper Works Internally

`tools/hermes_powerpoint.py` provides three responsibilities:

- install the upstream skill through Codex's `skill-installer`
- launch `codex exec` with a prompt that asks for `$powerpoint`
- create a deterministic PPTX locally with `python-pptx` when `--agent` is not used
- extract Word document structure with `python-docx`

The local generator creates a title slide, content slides from document
headings and bullets, and a closing slide. It is meant to validate the document
to deck path; use the agent mode for higher-polish decks.

## Troubleshooting

### `python-docx is required for Word inputs`

Install dependencies:

```bash
pip install -r requirements.txt
```

### `.doc` file cannot be read

Convert the file to `.docx`, then run the tool again. Legacy `.doc` support
depends on macOS `textutil`.

### Agent mode says the skill is not loaded

Run:

```bash
python tools/hermes_powerpoint.py --install-skill
```

Then restart Codex. The upstream skill name is `powerpoint`, so direct prompts
can use `$powerpoint`.

### Generated deck is too long

Use:

```bash
--max-slides 8
```

### I only need a fast draft

Omit `--agent`:

```bash
python tools/hermes_powerpoint.py inputs/presentations/report.docx \
  --out outputs/presentations/report.pptx
```

## Notes

- The repository does not vendor the upstream proprietary skill contents.
- Generated decks should stay under `outputs/presentations/` unless a user
  provides another output path.
- For finance-heavy decks backed by workbook cells, use Hermes `pptx-author`
  instead of the general `powerpoint` skill.
