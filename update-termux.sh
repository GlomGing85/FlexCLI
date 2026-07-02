#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

if ! command -v git >/dev/null 2>&1; then
  echo "git is not installed. Run: pkg install git -y"
  exit 1
fi

cd "$REPO_DIR"

if [ -n "$(git status --porcelain)" ]; then
  echo "Repo has local changes. Commit/stash them first, then rerun update."
  git status --short
  exit 1
fi

echo "[1/3] Pulling latest changes..."
git pull --ff-only

echo "[2/3] Reinstalling dependencies and launcher..."
SKIP_SYSTEM_PACKAGES=1 bash "$REPO_DIR/install-termux.sh"

echo "[3/3] Update complete ✅"
