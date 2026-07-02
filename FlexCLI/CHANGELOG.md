# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by Keep a Changelog, and this project loosely follows Semantic Versioning.

## [1.0.0-alpha.1] - 2026-07-01

### Added
- Initial FlexCLI MVP structure for Android + Termux.
- NVIDIA OpenAI-compatible client integration.
- CLI chat loop with agent tool-calling flow.
- SQLite-based short-term and long-term memory.
- Workspace sandbox for file operations.
- Core tools: list, read, write, edit files, mkdir, web search, memory search/save, create_skill.
- Termux install, run, and update scripts.
- GitHub Actions CI workflow for package compile check.
- GitHub-ready docs: README, CONTRIBUTING, release checklist, license.

### Notes
- This is an alpha starter release focused on architecture and install flow.
- Generated skills are scaffolded safely and are not auto-executed by default.
