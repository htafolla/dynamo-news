#!/bin/bash
# Dynamo News - Daily Report Runner (Production)
# Runs at 04:00 and 13:00 CST
# Usage: DYNAMO_NEWS_ROOT=/path/to/dynamo-news ./scripts/run_daily_report.sh

set -euo pipefail

ROOT="${DYNAMO_NEWS_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
LOG_DIR="$ROOT/logs"

mkdir -p "$LOG_DIR"

echo "=== Dynamo News: $(date) ===" >> "$LOG_DIR/daily.log"

cd "$ROOT"

if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found" | tee -a "$LOG_DIR/daily.log"
    exit 1
fi

export DYNAMO_NEWS_ROOT="$ROOT"
export PYTHONPATH="$ROOT:$PYTHONPATH"
export HERMES_RUNTIME=1

python3 dynamo_news/daily_correlator.py >> "$LOG_DIR/daily.log" 2>&1

echo "Done at $(date)" >> "$LOG_DIR/daily.log"
