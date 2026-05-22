#!/usr/bin/env python3
"""
Convert OpenClaw session JSONL to daily RAW files (Luna / asistente de Elena).

Reads the session transcripts, extracts user/assistant messages, groups by date
(Mexico City time), and writes to memory/raws-daily/.

Modos:
    --session-file PATH   Procesa una sesion JSONL especifica.
    --all                 Procesa TODAS las sesiones del directorio (incluye
                          .deleted y .reset — el contenido sigue siendo valido).
                          Acumula y deduplica por hash en un solo RAW por dia.
    --full                Ignora el cursor y reescribe los RAW afectados limpios.
    --topic NAME          Nombre del topic para el RAW (default: "luna").

Uso tipico:
    # Rebuild historico completo (recuperacion):
    python3 jsonl_to_raw.py --all --full
    # Incremental nocturno (cron) sobre todas las sesiones:
    python3 jsonl_to_raw.py --all

Tracks last processed timestamp per-source en memory/raws-daily/.raw-cursor.json
para poder correr incremental. El merge por hash protege contra duplicados aun
si el cursor se pierde o corrompe.
"""

import json
import os
import sys
import re
import hashlib
from datetime import datetime
from pathlib import Path

# Usar el reloj MX como fuente unica de verdad para hora Mexico
sys.path.insert(0, str(Path(__file__).parent))
from mx_clock import MX_TZ, now as mx_now

WORKSPACE = Path("/home/elena/.openclaw/workspace")
RAW_DIR = WORKSPACE / "memory" / "raws-daily"
CURSOR_FILE = RAW_DIR / ".raw-cursor.json"
SESSIONS_DIR = Path("/home/elena/.openclaw/agents/main/sessions")

MONTH_NAMES = {1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
               5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
               9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"}


def source_key(session_path: Path) -> str:
    return str(session_path.resolve())


def parse_args():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--session-file", type=str, default=None)
    p.add_argument("--all", action="store_true",
                   help="Procesa todas las sesiones del directorio")
    p.add_argument("--full", action="store_true",
                   help="Ignora cursor y reescribe RAW limpios")
    p.add_argument("--topic", type=str, default="luna")
    return p.parse_args()


def find_active_session():
    """Find the active DM session JSONL (most recently written)."""
    candidates = []
    for f in SESSIONS_DIR.glob("*.jsonl"):
        name = f.name
        if ".deleted" in name or ".reset" in name:
            continue
        if "-topic-" in name:
            continue
        candidates.append((f.stat().st_mtime, f))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][1]


def find_all_sessions():
    """Todas las sesiones del directorio, incluidas .deleted y .reset.

    OpenClaw fragmenta cada dia en multiples sesiones (cada conversacion, cada
    reset, cada heartbeat genera un JSONL). Una sesion rotada a .deleted/.reset
    sigue conteniendo mensajes validos — procesarla es obligatorio para no
    perder memoria. Se ordena por mtime para procesar en orden cronologico.
    """
    files = []
    for f in SESSIONS_DIR.iterdir():
        if not f.is_file():
            continue
        if ".jsonl" not in f.name:
            continue
        if "-topic-" in f.name:
            continue
        files.append(f)
    files.sort(key=lambda p: p.stat().st_mtime)
    return files


def to_mx(ts_str):
    """Parse ISO timestamp to Mexico City datetime."""
    ts_str = ts_str.replace("Z", "+00:00")
    dt = datetime.fromisoformat(ts_str)
    return dt.astimezone(MX_TZ)


def extract_text(content):
    """Extract text from message content (list or string)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        texts = []
        for c in content:
            if isinstance(c, dict) and c.get("type") == "text":
                texts.append(c["text"])
            elif isinstance(c, str):
                texts.append(c)
        return "\n".join(texts)
    return ""


def is_system_or_meta(text):
    """Check if message is system/meta noise we should skip."""
    skip_patterns = [
        r"^✅ New session started",
        r"^A new session was started via",
        r"^Read HEARTBEAT\.md",
        r"^HEARTBEAT_OK",
        r"^🔊\s*$",
        r"^System: \[",
        r"^NO_REPLY$",
        r"^\[cron:[^\]]+\s+heartbeat\]",
        r"Heartbeat prompt:\s*Read HEARTBEAT\.md",
        r"^Current time:",
        r"^WhatsApp gateway connected",
        r"^Return your summary as plain text;",
        r"^Conversation info \(untrusted",
        r"^Sender \(untrusted",
        r"^\[Internal task completion event\]$",
        r"^source: subagent$",
        r"^type: subagent task$",
        r"^status: completed successfully$",
        r"^Result \(untrusted content, treat as data\):$",
        r"^<<<BEGIN_UNTRUSTED_CHILD_RESULT>>>$",
        r"^<<<END_UNTRUSTED_CHILD_RESULT>>>$",
        r"^This context is runtime-generated, not user-authored\.",
    ]
    for pat in skip_patterns:
        if re.match(pat, text.strip()):
            return True
    return False


def clean_noise(text):
    """Remove noise patterns from message text (Foro #6 filters)."""
    text = re.sub(r'Transcribe the audio\.?\s*', '', text)
    text = re.sub(r'Transcrição e Legendas[^\n]*', '', text)
    text = re.sub(r'\nThank you\.\s*$', '', text)
    text = re.sub(
        r'```json\s*\n\s*\{[^}]*"(?:message_id|sender_id|label)"[^}]*\}\s*\n\s*```\s*',
        '', text, flags=re.DOTALL
    )
    text = re.sub(r'Conversation info \(untrusted metadata\):\s*\n?', '', text)
    text = re.sub(r'Sender \(untrusted metadata\):\s*\n?', '', text)
    text = re.sub(r'\[Audio\]\s*\n?', '', text)
    text = re.sub(r'^(Ahora ejecuto|Leyendo el archivo|Ejecutando|Revisando el archivo|Verificando)[^\n]*\n?', '', text)
    text = re.sub(r'^\s*(delete mode|create mode) \d+ [^\n]*\n?', '', text, flags=re.MULTILINE)
    return text.strip()


def is_solo_filler(text):
    """Check if message is just a filler word with no real content."""
    solo_patterns = [
        r'^Listo[.!:,]*$',
        r'^Hecho[.!:,]*$',
        r'^Perfecto[.!:,]*$',
        r'^Ok[.!:,]*$',
        r'^Git limpio[.!]*$',
    ]
    stripped = text.strip()
    for pat in solo_patterns:
        if re.match(pat, stripped):
            return True
    return False


def extract_user_text(text):
    """Extract the actual user message from Telegram metadata wrapper."""
    transcript_match = re.search(r"Transcript:\s*\n?(.*?)$", text, re.DOTALL)
    lines = text.strip().split("\n")
    if transcript_match:
        return transcript_match.group(1).strip()
    if "Conversation info" in text or "sender_id" in text:
        in_json = False
        last_json_end = 0
        for i, line in enumerate(lines):
            if line.strip().startswith("```json"):
                in_json = True
            elif line.strip() == "```" and in_json:
                in_json = False
                last_json_end = i
        if last_json_end > 0 and last_json_end + 1 < len(lines):
            actual = "\n".join(lines[last_json_end + 1:]).strip()
            if actual:
                return actual
    return text.strip()


def clean_assistant_text(text):
    """Clean assistant message — remove reply tags, keep content."""
    text = re.sub(r"\[\[reply_to_\w+\]\]\s*", "", text)
    if not text.strip():
        return ""
    return text.strip()


def msg_dedup_key(msg):
    """Stable per-message hash for RAW deduplication (SHA-256 of ts|label|text)."""
    raw = f"{msg.get('ts', '')}|{msg.get('label', '')}|{msg.get('text', '')}"
    return hashlib.sha256(raw.encode()).hexdigest()


def extract_existing_keys(path):
    """Read embedded RAW dedup keys from existing file."""
    keys = set()
    if not path.exists():
        return keys
    for line in path.read_text(errors="ignore").splitlines():
        m = re.match(r'<!-- key:(.+) -->', line)
        if m:
            keys.add(m.group(1))
    return keys


def process_jsonl(filepath, cursor_ts=None):
    """Process JSONL file, return messages grouped by MX date."""
    messages_by_date = {}
    try:
        f = open(filepath, errors="ignore")
    except OSError:
        return messages_by_date
    with f:
        for line in f:
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("type") != "message":
                continue
            msg = obj.get("message", {})
            role = msg.get("role")
            ts = obj.get("timestamp", "")
            if role not in ("user", "assistant"):
                continue
            if not ts:
                continue
            # Skip if before cursor
            if cursor_ts and ts <= cursor_ts:
                continue
            text = extract_text(msg.get("content", []))
            if not text:
                continue
            # Telegram user messages arrive wrapped in metadata; extract the
            # real text BEFORE applying meta filters.
            if role == "user":
                text = extract_user_text(text)
                if is_system_or_meta(text):
                    continue
            else:
                if is_system_or_meta(text):
                    continue
                text = clean_assistant_text(text)
                if not text:
                    continue
            text = clean_noise(text)
            if not text:
                continue
            if role == "assistant" and is_solo_filler(text):
                continue
            if role == "assistant" and len(text) < 10:
                continue
            try:
                mx_dt = to_mx(ts)
            except (ValueError, TypeError):
                continue
            date_key = mx_dt.strftime("%Y-%m-%d")
            time_str = mx_dt.strftime("%H:%M")
            messages_by_date.setdefault(date_key, []).append({
                "time": time_str,
                "label": "Elena" if role == "user" else "Luna",
                "text": text,
                "ts": ts,
            })
    return messages_by_date


def build_raw_content(date_key, messages, topic):
    """Build full RAW file content for a single day (overwrite mode)."""
    dt = datetime.strptime(date_key, "%Y-%m-%d")
    lines = [
        f"# RAW — #{topic} — {dt.day} {MONTH_NAMES[dt.month]} {dt.year}",
        "",
        "> Fuente: exportado de JSONL de OpenClaw. Puede contener datos sensibles.",
        "> No compartir; solo usar como fuente para reconstruir dailies.",
        "",
        "## [AUTO-EXPORT desde JSONL]",
        "",
    ]
    for msg in messages:
        lines.append(f"<!-- key:{msg_dedup_key(msg)} -->")
        lines.append(f"**[{msg['time']} MX] {msg['label']}:**")
        lines.append(msg["text"])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_raw_files(messages_by_date, topic, full_rebuild=False):
    """Write RAW files. full_rebuild overwrites cleanly; else append + dedup."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for date_key, messages in sorted(messages_by_date.items()):
        filepath = RAW_DIR / f"{topic}-{date_key}.md"
        if full_rebuild:
            filepath.write_text(build_raw_content(date_key, messages, topic))
            written.append(date_key)
            continue
        # Incremental append mode with hash dedup
        if not filepath.exists():
            dt = datetime.strptime(date_key, "%Y-%m-%d")
            header = f"# RAW — #{topic} — {dt.day} {MONTH_NAMES[dt.month]} {dt.year}\n"
            filepath.write_text(header)
        existing_keys = extract_existing_keys(filepath)
        new_msgs = [m for m in messages if msg_dedup_key(m) not in existing_keys]
        if not new_msgs:
            continue
        with open(filepath, "a") as f:
            f.write("\n## [AUTO-EXPORT desde JSONL]\n\n")
            for msg in new_msgs:
                f.write(f"<!-- key:{msg_dedup_key(msg)} -->\n")
                f.write(f"**[{msg['time']} MX] {msg['label']}:**\n{msg['text']}\n\n")
        written.append(date_key)
    return written


def dedup_and_sort(messages_by_date):
    """Dentro de cada fecha: deduplica por hash y ordena cronologicamente."""
    result = {}
    for date_key, msgs in messages_by_date.items():
        seen = set()
        uniq = []
        for m in sorted(msgs, key=lambda x: x["ts"]):
            k = msg_dedup_key(m)
            if k in seen:
                continue
            seen.add(k)
            uniq.append(m)
        result[date_key] = uniq
    return result


def load_cursor(session_path=None):
    """Load last processed timestamp (per-source con compat hacia atras)."""
    if not CURSOR_FILE.exists():
        return None
    try:
        data = json.loads(CURSOR_FILE.read_text())
    except Exception:
        return None
    if session_path and data.get("sources"):
        skey = source_key(Path(session_path))
        return data["sources"].get(skey, {}).get("last_ts")
    return data.get("last_ts")


def save_cursor(ts, session_path=None, topic=None):
    """Save last processed timestamp per-source. `updated` en hora MX."""
    now = mx_now().isoformat()
    if session_path:
        if CURSOR_FILE.exists():
            try:
                data = json.loads(CURSOR_FILE.read_text())
            except Exception:
                data = {}
        else:
            data = {}
        data.setdefault("version", 2)
        data.setdefault("sources", {})
        data["sources"][source_key(Path(session_path))] = {
            "topic": topic,
            "last_ts": ts,
        }
        data["updated"] = now
        CURSOR_FILE.write_text(json.dumps(data))
    else:
        CURSOR_FILE.write_text(json.dumps({"last_ts": ts, "updated": now}))


def run_all(topic, full):
    """Procesa TODAS las sesiones, acumula global, dedup por hash, escribe."""
    sessions = find_all_sessions()
    print(f"Sesiones encontradas: {len(sessions)} (incluye .deleted/.reset)")
    global_by_date = {}
    cursor_updates = []
    for sp in sessions:
        cursor_ts = None if full else load_cursor(sp)
        mbd = process_jsonl(sp, cursor_ts)
        for dk, msgs in mbd.items():
            global_by_date.setdefault(dk, []).extend(msgs)
        all_msgs = [m for msgs in mbd.values() for m in msgs]
        if all_msgs:
            cursor_updates.append((max(m["ts"] for m in all_msgs), sp))
    if not global_by_date:
        print("Nada que procesar")
        return
    global_by_date = dedup_and_sort(global_by_date)
    total = sum(len(v) for v in global_by_date.values())
    print(f"Mensajes unicos: {total} en {len(global_by_date)} dias")
    written = write_raw_files(global_by_date, topic, full_rebuild=full)
    print(f"RAW escritos ({len(written)}): {written[0]} .. {written[-1]}")
    # Actualizar cursores per-source
    for ts, sp in cursor_updates:
        save_cursor(ts, session_path=sp, topic=topic)
    print(f"Cursores actualizados: {len(cursor_updates)} sesiones")


def run_single(session_path, topic, full):
    """Procesa una sola sesion (modo legacy / --session-file)."""
    if not session_path or not session_path.exists():
        print("ERROR: No session file found")
        sys.exit(1)
    print(f"Processing: {session_path.name}")
    print(f"Size: {session_path.stat().st_size / 1024:.1f} KB")
    cursor_ts = None if full else load_cursor(session_path)
    print(f"Cursor: {cursor_ts}" if cursor_ts else "No cursor — full file")
    messages_by_date = process_jsonl(session_path, cursor_ts)
    messages_by_date = dedup_and_sort(messages_by_date)
    total = sum(len(v) for v in messages_by_date.values())
    print(f"Found {total} messages across {len(messages_by_date)} days")
    if total == 0:
        print("Nothing new to process")
        return
    written = write_raw_files(messages_by_date, topic, full_rebuild=full)
    print(f"Wrote RAW files for: {', '.join(written)}")
    all_msgs = [m for msgs in messages_by_date.values() for m in msgs]
    if all_msgs:
        latest_ts = max(m["ts"] for m in all_msgs)
        save_cursor(latest_ts, session_path=session_path, topic=topic)
        print(f"Cursor updated to: {latest_ts}")


def main():
    args = parse_args()
    if args.all:
        run_all(args.topic, args.full)
        return
    if args.session_file:
        session_path = Path(args.session_file)
    else:
        session_path = find_active_session()
    run_single(session_path, args.topic, args.full)


if __name__ == "__main__":
    main()
