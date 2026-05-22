#!/bin/bash
set -euo pipefail
# Batch export RAWs for Luna (Elena's assistant).
#
# Procesa TODAS las sesiones de OpenClaw, no solo la mas reciente: OpenClaw
# fragmenta cada dia en decenas de sesiones (cada conversacion, reset y
# heartbeat genera un JSONL). El modo --all de jsonl_to_raw.py recorre todas,
# acumula y deduplica por hash en un solo RAW por dia.
#
# Modo incremental por default (cursor per-source + dedup por hash).
# Rebuild historico completo via --full.

SCRIPT="/home/elena/.openclaw/workspace/scripts/jsonl_to_raw.py"
RAW_DIR="/home/elena/.openclaw/workspace/memory/raws-daily"
FULL_MODE=0

if [[ "${1:-}" == "--full" ]]; then
  FULL_MODE=1
fi

backup_raw_dir() {
  local stamp backup
  stamp=$(date +%Y%m%d-%H%M%S)
  backup="/home/elena/.openclaw/workspace/backups/raws-daily-pre-full-$stamp"
  mkdir -p "$(dirname "$backup")"
  if [ -d "$RAW_DIR" ]; then
    cp -a "$RAW_DIR" "$backup"
    echo "Backup before --full: $backup"
  fi
}

if [[ "$FULL_MODE" -eq 1 ]]; then
  backup_raw_dir
  python3 "$SCRIPT" --all --full --topic luna
else
  python3 "$SCRIPT" --all --topic luna
fi

echo ""
if [[ "$FULL_MODE" -eq 1 ]]; then
  echo "RAW rebuild completo (--full) terminado"
else
  echo "RAW export incremental terminado"
fi

echo "RAW files present:"
find "$RAW_DIR" -maxdepth 1 -name 'luna-*.md' 2>/dev/null | wc -l
du -sh "$RAW_DIR" 2>/dev/null || echo "(raws-daily dir empty or missing)"
