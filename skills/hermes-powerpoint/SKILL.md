---
name: hermes-powerpoint
description: Use the NousResearch/Hermes PowerPoint skill from Codex to turn Markdown, text, or lightweight source documents into editable PPTX slide decks. Use when a user asks to install Hermes PowerPoint in Codex, create a deck from a document, generate a PPTX from notes, or wrap the upstream `powerpoint` skill in a repeatable local workflow.
---

# Hermes PowerPoint Bridge

This skill is a project-local bridge to the upstream NousResearch/Hermes
PowerPoint skill. It does not copy the upstream skill content into this repo.
Install the upstream skill into the active Codex environment, then use it to
generate editable `.pptx` files from source documents.

## Upstream Skill

- Repository: `NousResearch/hermes-agent`
- Skill path: `skills/productivity/powerpoint`
- Local install directory: `$CODEX_HOME/skills/hermes-powerpoint`
- Upstream skill name: `powerpoint`

The upstream `SKILL.md` frontmatter uses `name: powerpoint`, so after Codex is
restarted the direct invocation is usually:

```text
Use $powerpoint to create a PPTX deck from this document.
```

Use this bridge name when you want the repository workflow, installer notes, or
the deterministic fallback script.

## Install

From the repository root:

```bash
python tools/hermes_powerpoint.py --install-skill
```

Restart Codex after installation so the new user skill is discovered.

## Generate With Codex Agent

Use the nested Codex path when you want the agent to explicitly apply the
Hermes PowerPoint skill instructions:

```bash
python tools/hermes_powerpoint.py docs/coding.md \
  --agent \
  --out outputs/presentations/coding.pptx
```

Word input example:

```bash
python tools/hermes_powerpoint.py inputs/presentations/report.docx \
  --agent \
  --out outputs/presentations/report.pptx
```

The wrapper asks Codex to use `$powerpoint`. If the skill is not loaded by name,
the prompt points Codex at `$CODEX_HOME/skills/hermes-powerpoint/SKILL.md`.

## Generate Locally

Use the local path for deterministic smoke tests or environments where you do
not want to launch a nested agent:

```bash
python tools/hermes_powerpoint.py docs/coding.md \
  --out outputs/presentations/coding.pptx
```

The local path uses `python-pptx` and supports PDF, Markdown, plain text, simple
RTF, and Microsoft Word `.docx` / `.docm` extraction. Legacy `.doc` files are
supported on macOS when `textutil` is available; otherwise convert them to
`.docx` first. It is intentionally conservative and does not replace the
upstream skill's richer editing and QA workflow.

## Working Rules

- Keep source documents and generated decks in the workspace.
- Do not upload, email, or externally send generated decks from this skill.
- Prefer the agent path for polished decks and template-sensitive work.
- Use the local path for CI-style validation and quick drafts.
- For finance decks where every number must trace to a workbook, consider the
  upstream Hermes `pptx-author` optional skill instead.
