"""mx_clock — fuente única de verdad para hora México Central.

Todo script o proceso que necesite fecha/hora en zona MX debe usar
este módulo en lugar de hacer su propio cálculo. Evita divergencias
entre UTC del servidor y la zona operativa real (America/Mexico_City).

Uso como módulo:
    from mx_clock import now, today, yesterday, iso, day_start, day_end
    print(today())            # date(2026, 4, 14)
    print(iso())              # "2026-04-14T23:45:12-06:00"
    print(yesterday())        # date(2026, 4, 13)

Uso como CLI (espejo de mx-clock.sh):
    python3 mx_clock.py                 # "2026-04-14 23:45:12 MX"
    python3 mx_clock.py --date          # "2026-04-14"
    python3 mx_clock.py --today         # alias de --date
    python3 mx_clock.py --time          # "23:45:12"
    python3 mx_clock.py --iso           # "2026-04-14T23:45:12-06:00"
    python3 mx_clock.py --timestamp     # timestamp Unix
    python3 mx_clock.py --day-start     # inicio del día MX
    python3 mx_clock.py --day-end       # fin del día MX
    python3 mx_clock.py --yesterday     # "2026-04-13"
    python3 mx_clock.py --days-ago 7    # fecha de hace 7 días
    python3 mx_clock.py --tag           # "20260414-234512" (rollback tags, temp dirs)
    python3 mx_clock.py --compact       # alias de --tag

Garantía: todas las funciones usan ZoneInfo("America/Mexico_City").
Si México cambia de DST o de zona, solo se toca este archivo.
"""
from __future__ import annotations

import sys
from datetime import datetime, date, timedelta, time
from zoneinfo import ZoneInfo

MX_TZ = ZoneInfo("America/Mexico_City")


def now() -> datetime:
    """Datetime actual con tzinfo MX."""
    return datetime.now(MX_TZ)


def today() -> date:
    """Fecha MX de hoy."""
    return now().date()


def yesterday() -> date:
    """Fecha MX de ayer (maneja bordes de mes/año correctamente)."""
    return today() - timedelta(days=1)


def tomorrow() -> date:
    """Fecha MX de mañana."""
    return today() + timedelta(days=1)


def iso() -> str:
    """ISO 8601 con offset (ej: '2026-04-14T23:45:12-06:00').

    Sin microsegundos para que sea estable y comparable.
    """
    return now().replace(microsecond=0).isoformat()


def timestamp() -> int:
    """Timestamp Unix (segundos desde epoch)."""
    return int(now().timestamp())


def day_start(d: date | None = None) -> datetime:
    """Inicio del día MX (00:00:00) para la fecha dada o hoy."""
    d = d or today()
    return datetime.combine(d, time.min, tzinfo=MX_TZ)


def day_end(d: date | None = None) -> datetime:
    """Fin del día MX (23:59:59) para la fecha dada o hoy."""
    d = d or today()
    return datetime.combine(d, time(23, 59, 59), tzinfo=MX_TZ)


def format_default() -> str:
    """Formato default que iguala a mx-clock.sh sin argumentos."""
    return now().strftime("%Y-%m-%d %H:%M:%S MX")


def format_date() -> str:
    return today().strftime("%Y-%m-%d")


def format_time() -> str:
    return now().strftime("%H:%M:%S")


def days_ago(n: int) -> date:
    """Fecha MX de hace N días (maneja bordes de mes/año)."""
    return today() - timedelta(days=n)


def tag() -> str:
    """Formato compacto para rollback tags, temp dirs, nombres de archivo.

    Ejemplo: '20260414-234512' — sin símbolos conflictivos para filesystems
    ni separadores ambiguos.
    """
    return now().strftime("%Y%m%d-%H%M%S")


def _cli(argv: list[str]) -> int:
    mode = argv[1] if len(argv) > 1 else "--default"

    if mode in ("--default", ""):
        print(format_default())
    elif mode in ("--date", "--today"):
        print(format_date())
    elif mode == "--time":
        print(format_time())
    elif mode == "--iso":
        print(iso())
    elif mode == "--timestamp":
        print(timestamp())
    elif mode == "--day-start":
        print(day_start().isoformat())
    elif mode == "--day-end":
        print(day_end().isoformat())
    elif mode == "--yesterday":
        print(yesterday().strftime("%Y-%m-%d"))
    elif mode == "--days-ago":
        if len(argv) < 3:
            print("mx_clock.py: --days-ago requiere un número de días", file=sys.stderr)
            return 2
        try:
            n = int(argv[2])
        except ValueError:
            print(f"mx_clock.py: --days-ago espera un entero, recibió '{argv[2]}'", file=sys.stderr)
            return 2
        print(days_ago(n).strftime("%Y-%m-%d"))
    elif mode in ("--tag", "--compact"):
        print(tag())
    elif mode in ("--help", "-h"):
        print(__doc__)
    else:
        print(f"mx_clock.py: modo desconocido '{mode}'", file=sys.stderr)
        print("Usa --help para ver los modos válidos.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_cli(sys.argv))
