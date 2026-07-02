# FlexCLI

**FlexCLI** is a terminal AI assistant for **Android + Termux** focused on:
- chatting
- coding help
- file and folder operations
- web search
- memory
- skill scaffolding for future extensions

Language: **English** | [Українська](README.ua.md) | [Русский](README.ru.md)

> Current release: **1.0.0-alpha.3**

## Status
FlexCLI is currently an **alpha-stage MVP**.
It already works as a local CLI agent scaffold, but it is still evolving and not production-ready.

At the moment:
- the main docs are multilingual
- the CLI interface itself is still mostly Ukrainian
- runtime language selection is planned for a future release

## Features

### Core
- interactive CLI chat loop
- NVIDIA API integration through an OpenAI-compatible endpoint
- agent loop with tool/function calling
- JSON config
- workspace sandbox
- SQLite-based memory

### Built-in tools
- `list_files`
- `read_file`
- `write_file`
- `edit_file`
- `mkdir`
- `web_search`
- `save_memory`
- `search_memory`
- `create_skill`

### Current CLI commands
- `/help`
- `/config`
- `/mem`
- `/reset`
- `/set model <value>`
- `/set temp <value>`
- `/set search on|off`
- `/set genskills on|off`
- `/exit`

## Repository structure

```text
FlexCLI/
├─ .env.example
├─ .gitignore
├─ LICENSE
├─ CHANGELOG.md
├─ CONTRIBUTING.md
├─ RELEASE.md
├─ README.md
├─ README.ua.md
├─ README.ru.md
├─ install-termux.sh
├─ update-termux.sh
├─ run.sh
├─ pyproject.toml
├─ requirements.txt
├─ .github/
│  ├─ workflows/python-ci.yml
│  ├─ PULL_REQUEST_TEMPLATE.md
│  └─ ISSUE_TEMPLATE/
│     ├─ bug_report.md
│     └─ feature_request.md
└─ flexcli/
   ├─ __init__.py
   ├─ __main__.py
   ├─ agent.py
   ├─ cli.py
   ├─ client.py
   ├─ config.py
   ├─ memory.py
   └─ skills.py
```

After first launch, FlexCLI creates:

```text
~/.flexcli/
├─ .env
├─ config.json
├─ memory.db
├─ generated_skills/
└─ workspace/
```

## Requirements
- Android device
- [Termux](https://termux.dev/)
- Python available in Termux
- NVIDIA API key (`nvapi-...`)

## Installation on Termux

### 1. Clone the repository
```bash
pkg update
pkg install git -y
git clone https://github.com/GlomGing85/FlexCLI.git
cd FlexCLI
```

### 2. Run the installer
```bash
bash install-termux.sh
```

### 3. Add your NVIDIA API key
```bash
nano ~/.flexcli/.env
```

Paste:
```env
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxxxxxx
```

### 4. Start FlexCLI
```bash
flexcli
```

## Updating
If FlexCLI was installed from GitHub:

```bash
cd ~/FlexCLI
bash update-termux.sh
```

## Configuration
Main config file:

```bash
~/.flexcli/config.json
```

Example:

```json
{
  "base_url": "https://integrate.api.nvidia.com/v1",
  "model": "nvidia/llama-3.3-nemotron-super-49b-v1.5",
  "temperature": 0.3,
  "max_tool_rounds": 5,
  "max_history_messages": 12,
  "web_search_enabled": true,
  "confirm_destructive": true,
  "enable_generated_skills": false,
  "workspace_dir": "/data/data/com.termux/files/home/.flexcli/workspace",
  "db_path": "/data/data/com.termux/files/home/.flexcli/memory.db",
  "system_prompt": "You are FlexCLI..."
}
```

### Where to store the API key
FlexCLI can read `.env` from:
- `~/.flexcli/.env`
- `.env` in the repository root
- `.env` in the current working directory

Recommended for Termux:

```bash
~/.flexcli/.env
```

## Memory model
FlexCLI currently uses two simple memory layers:

### Short-term memory
Recent conversation history stored in SQLite.

### Long-term memory
Useful user preferences and persistent notes stored separately.

Good examples of what to store:
- preferred programming language
- preferred response style
- project names
- important paths
- long-term tasks

## Skill generation
The `create_skill` tool currently creates a Python scaffold inside:

```bash
~/.flexcli/generated_skills/
```

This is intentional.
Generated skills are scaffolded safely and are **not auto-executed by default**.

## Roadmap

### Alpha / MVP
- chat
- file tools
- memory
- web search
- config
- skill scaffolding

### Next steps
- streaming output
- `/mode chat|code|research`
- append/delete tools with confirmations
- safer code execution
- autoload for generated skills
- better search and summarization
- CLI language selection

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md).

## License
MIT — see [LICENSE](LICENSE).
