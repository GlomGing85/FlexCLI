#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
PREFIX_BIN="${PREFIX:-/data/data/com.termux/files/usr}/bin"
HOME_DIR="${HOME:-/data/data/com.termux/files/home}"
FLEX_HOME="${FLEXCLI_HOME:-$HOME_DIR/.flexcli}"

if [ "${SKIP_SYSTEM_PACKAGES:-0}" != "1" ] && command -v pkg >/dev/null 2>&1; then
  echo "[1/5] Installing system packages in Termux..."
  pkg update -y
  pkg install -y python git
else
  echo "[1/5] Skipping system packages"
fi

echo "[2/5] Creating virtual environment..."
python -m venv "$REPO_DIR/.venv"

PIP="$REPO_DIR/.venv/bin/pip"
PYTHON="$REPO_DIR/.venv/bin/python"

echo "[3/5] Installing FlexCLI..."
"$PIP" install --upgrade pip setuptools wheel
"$PIP" install -e "$REPO_DIR"

echo "[4/5] Preparing FlexCLI home..."
mkdir -p "$FLEX_HOME"
if [ ! -f "$FLEX_HOME/.env" ]; then
  cp "$REPO_DIR/.env.example" "$FLEX_HOME/.env"
fi
"$PYTHON" -c "from flexcli.config import load_config; load_config()"

echo "[5/5] Installing launcher command..."
cat > "$PREFIX_BIN/flexcli" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
source "$REPO_DIR/.venv/bin/activate"
python -m flexcli "\$@"
EOF
chmod +x "$PREFIX_BIN/flexcli"

cat <<EOF

Done ✅

Next steps:
1. Open your API key file:
   nano "$FLEX_HOME/.env"
2. Paste your key:
   NVIDIA_API_KEY=nvapi-...
3. Start FlexCLI:
   flexcli

Project directory:
  $REPO_DIR
FlexCLI home:
  $FLEX_HOME
EOF
