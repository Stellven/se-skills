# System Architect Agent

The **System Architect Agent** is a CLI tool that uses AI to generate comprehensive system design documents from a simple description.

## Features

- **Requirements Analysis**: Extracts Functional and Non-Functional Requirements.
- **Architecture Design**: Selects patterns and generates C4 Component Diagrams (Mermaid JS).
- **API Specification**: Defines API endpoints and Data Models.

## Prerequisites

You need a Google Gemini API Key.

1.  Get an API key from [Google AI Studio](https://aistudio.google.com/).
2.  Set it as an environment variable:

```bash
export GOOGLE_API_KEY="your_api_key_here"
```

## Usage

Run the tool from the project root:

```bash
python tools/architect.py plan "A real-time chat application with group messaging and file sharing" --name chat-app
```

### Arguments

- `description`: A natural language description of the system you want to build.
- `--name / -n`: The name of the project (used for the output directory).

## Output

The tool generates a folder in `design/{name}/` containing:

- `requirements.md`: Analysis of FRs, NFRs, and Entities.
- `architecture.md`: High-level design with Mermaid diagrams.
- `api_spec.md`: API endpoints and database schema.

## Example

```bash
python tools/architect.py plan "A todo list CLI" --name todo-cli
```

Output:
- `design/todo-cli/requirements.md`
- `design/todo-cli/architecture.md`
- `design/todo-cli/api_spec.md`
