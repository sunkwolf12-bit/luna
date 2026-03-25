#!/usr/bin/env python3
"""export_raws.py

Export OpenClaw session JSONL logs into human-readable RAW markdown.

Sources:
- /root/.openclaw/agents/main/sessions/*.jsonl

Outputs:
- workspace/memory/dailies-raw/YYYY-MM-DD.md  (Mexico City date)

Design goals (for Elena):
- RAW is a near-verbatim, readable log.
- It is *not* the daily summary.
- RAW can contain sensitive data; treat as internal source-of-truth and never paste externally.

Usage:
  python3 scripts/export_raws.py all
  python3 scripts/export_raws.py day 2026-03-25
  python3 scripts/export_raws.py day today
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

MX_TZ = ZoneInfo("America/Mexico_City")

SESSIONS_DIR = "/root/.openclaw/agents/main/sessions"
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "memory", "raws-daily")

# Keep it readable; RAW is allowed to be long.
MAX_FIELD_LEN = 20000


def _safe_str(x) -> str:
    if x is None:
        return ""
    if not isinstance(x, str):
        x = str(x)
    if len(x) > MAX_FIELD_LEN:
        return x[:5000] + "\n[... truncado ...]\n" + x[-2000:]
    return x


def _parse_ts(ts: str) -> datetime | None:
    if not ts:
        return None
    try:
        # Handles Z
        ts2 = ts.replace("Z", "+00:00")
        return datetime.fromisoformat(ts2)
    except Exception:
        return None


def _mx_date_str(dt_utc: datetime) -> str:
    return dt_utc.astimezone(MX_TZ).date().isoformat()


def _mx_time_str(dt_utc: datetime) -> str:
    return dt_utc.astimezone(MX_TZ).strftime("%H:%M")


def _iter_jsonl_files() -> list[str]:
    if not os.path.isdir(SESSIONS_DIR):
        raise SystemExit(f"No existe el directorio de sesiones: {SESSIONS_DIR}")
    files = []
    for name in os.listdir(SESSIONS_DIR):
        if not name.endswith(".jsonl"):
            continue
        # ignore locks etc
        if name.endswith(".jsonl.lock"):
            continue
        path = os.path.join(SESSIONS_DIR, name)
        if os.path.isfile(path):
            files.append(path)
    return sorted(files)


def _extract_message_text(message_obj) -> str:
    """message.content can be str or a list of content parts (OpenClaw v3)."""
    if message_obj is None:
        return ""
    content = message_obj.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        # Join text parts; ignore non-text
        parts = []
        for p in content:
            if isinstance(p, dict) and p.get("type") == "text":
                parts.append(p.get("text", ""))
        return "\n".join([x for x in parts if x])
    return _safe_str(content)


def _entry_to_lines(entry: dict) -> list[str] | None:
    """Convert a JSONL entry to readable lines.

    We only keep user/assistant chat messages.
    OpenClaw session logs often store chat under: {type:"message", message:{role, content:[...]}}
    """
    etype = entry.get("type")
    ts = entry.get("timestamp") or entry.get("ts") or entry.get("time")

    if etype != "message":
        return None

    msg = entry.get("message") or {}
    role = msg.get("role") or ""
    if role == "system":
        return None

    content = _safe_str(_extract_message_text(msg))
    if not content.strip():
        return None

    # Omite "basura" típica (heartbeats/crons/logs) para que el RAW sea legible.
    # Nota: el RAW sigue siendo fuente interna; esto solo reduce ruido de automatizaciones.
    noise_patterns = [
        r"^\[cron:[^\]]+\s+heartbeat\]",  # prompts de heartbeat
        r"Heartbeat prompt:\s*Read HEARTBEAT\.md",
        r"^Current time:\s*\w+",  # encabezados de heartbeat
        r"^Return your summary as plain text;",  # instrucciones de heartbeat
        r"^\[cron:[^\]]+\]",  # otros prefijos de cron
    ]
    for pat in noise_patterns:
        if re.search(pat, content, flags=re.IGNORECASE | re.MULTILINE):
            return None

    dt = _parse_ts(ts) if isinstance(ts, str) else None
    time_prefix = ""
    if dt:
        time_prefix = f"[{_mx_time_str(dt)} MX] "

    if role == "user":
        speaker = "Elena"
    elif role == "assistant":
        speaker = "Luna"
    else:
        return None

    # If content includes audio wrapper, keep transcript if present.
    if "Transcript:" in content:
        parts = content.split("Transcript:", 1)
        if len(parts) == 2:
            content = parts[1].strip()

    return [f"**{time_prefix}{speaker}:**", content, ""]


def export_all() -> int:
    os.makedirs(OUT_DIR, exist_ok=True)

    grouped: dict[str, list[str]] = defaultdict(list)

    for path in _iter_jsonl_files():
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except Exception:
                    continue

                ts = entry.get("timestamp") or ""
                dt = _parse_ts(ts) if isinstance(ts, str) else None
                if not dt:
                    continue

                date_key = _mx_date_str(dt)
                lines = _entry_to_lines(entry)
                if not lines:
                    continue
                grouped[date_key].extend(lines)

    written = 0
    for date_key in sorted(grouped.keys()):
        out_path = os.path.join(OUT_DIR, f"{date_key}.md")
        header = [
            f"# RAW — {date_key} (MX)",
            "", 
            "> Fuente: exportado de JSONL de OpenClaw (agente main).", 
            "> Nota: este RAW puede contener datos sensibles. No compartir; solo usar como fuente para reconstruir dailies.",
            "",
        ]
        with open(out_path, "w", encoding="utf-8") as out:
            out.write("\n".join(header + grouped[date_key]).rstrip() + "\n")
        written += 1

    print(f"OK: RAWs escritos por día: {written} → {OUT_DIR}")
    return 0


def export_day(day: str) -> int:
    os.makedirs(OUT_DIR, exist_ok=True)

    if day == "today":
        day = datetime.now(MX_TZ).date().isoformat()

    grouped: list[str] = []

    for path in _iter_jsonl_files():
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except Exception:
                    continue

                ts = entry.get("timestamp") or ""
                dt = _parse_ts(ts) if isinstance(ts, str) else None
                if not dt:
                    continue

                if _mx_date_str(dt) != day:
                    continue

                lines = _entry_to_lines(entry)
                if not lines:
                    continue
                grouped.extend(lines)

    out_path = os.path.join(OUT_DIR, f"{day}.md")
    header = [
        f"# RAW — {day} (MX)",
        "",
        "> Fuente: exportado de JSONL de OpenClaw (agente main).",
        "> Nota: este RAW puede contener datos sensibles. No compartir; solo usar como fuente para reconstruir dailies.",
        "",
    ]
    with open(out_path, "w", encoding="utf-8") as out:
        out.write("\n".join(header + grouped).rstrip() + "\n")

    print(f"OK: RAW escrito: {out_path} (líneas: {len(grouped)})")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0

    cmd = argv[1]
    if cmd == "all":
        return export_all()
    if cmd == "day":
        if len(argv) < 3:
            raise SystemExit("Uso: export_raws.py day YYYY-MM-DD | today")
        return export_day(argv[2])

    raise SystemExit(f"Comando no reconocido: {cmd}")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
