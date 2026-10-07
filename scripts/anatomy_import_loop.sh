#!/usr/bin/env bash
# Unattended hourly importer for GPT anatomical motion sheets.
# Launched detached (nohup) so it keeps importing new waves while GPT generates
# for 10+ hours. Idempotent; refreshes existing GIFs; never rebuilds the APK.
# Stop early with:  kill "$(cat build/anatomy_import.pid)"
set -uo pipefail

ROOT="/Users/restartday/Documents/健身"
PY="/opt/homebrew/Caskroom/miniforge/base/bin/python3"
LOG="$ROOT/build/anatomy_import.log"
MAX_RUNS=14          # ~14 hourly passes, then self-exits
INTERVAL=3600

cd "$ROOT" || exit 1
mkdir -p "$ROOT/build"
echo $$ > "$ROOT/build/anatomy_import.pid"

for run in $(seq 1 "$MAX_RUNS"); do
  {
    echo "===== run ${run}/${MAX_RUNS}  $(date '+%Y-%m-%d %H:%M:%S') ====="
    "$PY" scripts/import_anatomy_sheets.py
    "$PY" scripts/validate_exercise_gifs.py app/src/main/res/raw 2>&1 | tail -1
    echo
  } >> "$LOG" 2>&1
  [ "$run" -lt "$MAX_RUNS" ] && sleep "$INTERVAL"
done

echo "loop finished $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG"
rm -f "$ROOT/build/anatomy_import.pid"
