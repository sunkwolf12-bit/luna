#!/bin/bash
set -euo pipefail
# Batch export RAWs for Luna (Elena's assistant).
# Incremental mode by default. Full rebuild via --full.
# Luna currently uses only DM (no topics); if topics are added later,
# the same pattern from Claudy applies (topic-N → name mapping).

SCRIPT="/home/elena/.openclaw/workspace/scripts/jsonl_to_raw.py"
SESSIONS_DIR="/home/elena/.openclaw/agents/main/sessions"
FULL_MODE=0
count=0

if [[ "${1:-}" == "--full" ]]; then
  FULL_MODE=1
fi

latest_for_pattern() {
  local pattern="$1"
  local latest=""
  local latest_mtime=0
  for f in $pattern; do
    [ -f "$f" ] || continue
    local sz
    sz=$(stat -c%s "$f" 2>/dev/null || echo 0)
    [ "$sz" -lt 3000 ] && continue
    # Skip .deleted and .reset sessions
    [[ "$f" == *.deleted* ]] && continue
    [[ "$f" == *.reset* ]] && continue
    local mtime
    mtime=$(stat -c%Y "$f" 2>/dev/null || echo 0)
    if [ "$mtime" -gt "$latest_mtime" ]; then
      latest="$f"
      latest_mtime="$mtime"
    fi
  done
  if [ -n "$latest" ]; then
    echo "$latest"
  fi
}

process_one() {
  local topic="$1"
  local file="$2"
  [ -f "$file" ] || return 0
  echo "Processing: $topic <- $(du -h "$file" | cut -f1) $(basename "$file")"
  if [[ "$FULL_MODE" -eq 1 ]]; then
    python3 "$SCRIPT" --session-file "$file" --topic "$topic" --full
  else
    python3 "$SCRIPT" --session-file "$file" --topic "$topic"
  fi
  count=$((count + 1))
}

# Luna's DM session: most recent non-topic, non-deleted, non-reset jsonl
DM_FILE=$(latest_for_pattern "$SESSIONS_DIR/*.jsonl")

process_one luna "$DM_FILE"

echo ""
if [[ "$FULL_MODE" -eq 1 ]]; then
  echo "Processed $count JSONL files in FULL rebuild mode"
else
  echo "Processed $count JSONL files in incremental mode"
fi

echo "RAW files present:"
find /home/elena/.openclaw/workspace/memory/raws-daily -maxdepth 1 -name '*.md' 2>/dev/null | wc -l
du -sh /home/elena/.openclaw/workspace/memory/raws-daily/ 2>/dev/null || echo "(dailies-raw dir empty or missing)"
