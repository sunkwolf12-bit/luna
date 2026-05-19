#!/usr/bin/env python3
"""
export_raws.py - CLI wrapper for nightly RAW export.

Usage:
    python3 scripts/export_raws.py day today     # export today's RAW only
    python3 scripts/export_raws.py day YYYY-MM-DD  # export specific date
    python3 scripts/export_raws.py full          # full rebuild (all sessions)
"""

import subprocess
import sys
from pathlib import Path

WORKSPACE = Path("/home/elena/.openclaw/workspace")
SCRIPT_JSONL = WORKSPACE / "scripts" / "jsonl_to_raw.py"


def cmd_day(target_date=None):
    """Export RAW for a specific day (default: today in MX time)."""
    args = ["python3", str(SCRIPT_JSONL)]
    result = subprocess.run(args, capture_output=True, text=True)
    return result


def cmd_full():
    """Full rebuild - process entire session history from scratch."""
    result = subprocess.run(
        ["python3", str(SCRIPT_JSONL), "--full"],
        capture_output=True, text=True
    )
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: export_raws.py day [YYYY-MM-DD|today]")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "day":
        target = sys.argv[2] if len(sys.argv) > 2 else "today"
        if target == "today":
            sys.path.insert(0, str(Path(__file__).parent))
            from mx_clock import now as mx_now
            target = mx_now().strftime("%Y-%m-%d")
        print(f"Exporting RAW for {target}")
        result = cmd_day(target)
    elif mode == "full":
        print("Full rebuild mode")
        result = cmd_full()
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)

    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr, file=sys.stderr)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()