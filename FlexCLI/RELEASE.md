# Release Checklist

Use this checklist before creating a GitHub release.

## Pre-release
- [ ] Update `CHANGELOG.md`
- [ ] Review `README.md`
- [ ] Run `python -m compileall flexcli`
- [ ] Verify `install-termux.sh`
- [ ] Verify `update-termux.sh`
- [ ] Confirm `.env` is not committed
- [ ] Confirm local secrets are not in repo

## Versioning
- [ ] Pick version number
- [ ] Create git tag
- [ ] Push tag to GitHub

Example:

```bash
git tag v1.0.0-alpha.1
git push origin v1.0.0-alpha.1
```

## GitHub Release notes template

Title:

```text
FlexCLI v1.0.0-alpha.1
```

Suggested notes:
- First public alpha of FlexCLI
- Android + Termux install flow included
- NVIDIA API integration included
- Core tools, memory, config, and workspace scaffold included
- Safe starter implementation for generated skills

## After release
- [ ] Test fresh install from GitHub
- [ ] Test update flow on an existing install
- [ ] Note regressions for next alpha
