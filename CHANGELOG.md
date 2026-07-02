# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by Keep a Changelog, and this project loosely follows Semantic Versioning.

## [1.0.0-alpha.3] - 2026-07-02

### Fixed
- Removed the `duckduckgo-search` dependency from installation.
- Replaced the external web-search package with a lightweight built-in HTML search implementation.
- Avoided the Rust/maturin/primp build failure on Termux during installation.
- Reduced install friction and unnecessary compiler-heavy dependency pulls on Android.
- Simplified the README install steps to avoid recommending a full `pkg upgrade` during first-time setup.

### Notes
- This release is focused on making first-time Termux installation succeed more reliably.
- Web search remains basic and may evolve in future releases.

## [1.0.0-alpha.2] - 2026-07-02

### Changed
- Repository structure cleaned up so project files live in the repository root.
- Main `README.md` rewritten for public GitHub usage in English.
- Added `README.ua.md` and `README.ru.md` for Ukrainian and Russian documentation.
- Removed internal-oriented wording from public-facing docs.

### Notes
- This release focuses on documentation and repository usability.
- CLI runtime language selection is planned for a future release.

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
