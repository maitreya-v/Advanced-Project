#!/bin/zsh
set -eu
APP_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$APP_DIR")")"
PYTHON_BIN="$PROJECT_DIR/work/venv/bin/python"
if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN="python3"
fi
cd "$APP_DIR"
export MPLCONFIGDIR="$PROJECT_DIR/work/matplotlib"
OLLAMA_BIN="$PROJECT_DIR/work/runtime/ollama"
if ! "$PYTHON_BIN" -c 'import urllib.request; urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=2)' >/dev/null 2>&1; then
  if [[ -x "$OLLAMA_BIN" ]]; then
    nohup env OLLAMA_MODELS="$PROJECT_DIR/work/runtime/models" OLLAMA_NO_CLOUD=1 OLLAMA_HOST=127.0.0.1:11434 OLLAMA_CONTEXT_LENGTH=8192 OLLAMA_NUM_PARALLEL=1 "$OLLAMA_BIN" serve > "$PROJECT_DIR/work/ollama-launcher.log" 2>&1 < /dev/null &
  fi
fi
if "$PYTHON_BIN" -c 'import urllib.request; urllib.request.urlopen("http://127.0.0.1:8502/_stcore/health", timeout=2)' >/dev/null 2>&1; then
  open http://127.0.0.1:8502
  exit 0
fi
exec "$PYTHON_BIN" -m streamlit run Dashboard.py --server.address 127.0.0.1 --server.port 8502 --browser.gatherUsageStats false
