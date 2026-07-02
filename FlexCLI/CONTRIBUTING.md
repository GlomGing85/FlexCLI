# Contributing to FlexCLI

Thanks for your interest in FlexCLI.

## Ground rules
- Keep the core simple.
- Prefer safe defaults.
- Protect the workspace sandbox.
- Do not introduce risky auto-execution behavior without clear confirmation paths.
- Keep Android + Termux support first-class.

## Development setup

```bash
git clone https://github.com/<YOUR_GITHUB_USERNAME>/FlexCLI.git
cd FlexCLI
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m flexcli
```

## Recommended workflow
1. Create a branch.
2. Make focused changes.
3. Run a quick compile check:

```bash
python -m compileall flexcli
```

4. Update docs if behavior changed.
5. Open a pull request with a short summary.

## Commit style
Simple, clear messages are enough, for example:
- `feat: add /version command`
- `fix: protect workspace path resolution`
- `docs: improve Termux install guide`

## Areas that need help
- streaming output
- mode system (`chat`, `code`, `research`)
- safer destructive actions with confirmation layer
- plugin autoload for generated skills
- better search and summarization
- testing

## Security notes
Please do not add features that let generated code auto-run without an explicit trust model or confirmation step.
