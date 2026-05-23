#!/usr/bin/env python3
"""Consolida entradas Top5 con etiquetas crudas a `TRANSFER. / DEPTOS.`.

Helper local para Luna. Aplica la misma regla que
`backend/app/services/consolidador.py`, util para preview / debugging antes
de mandar el JSON al backend.

Uso:

    python3 consolidar.py /tmp/sicc/<sesion>/candidato_base.json \\
        > /tmp/sicc/<sesion>/candidato_consolidado.json

Acepta el JSON candidato completo en stdin o como primer argumento, y
emite el JSON con:

- Cada Top5 reagrupado: entradas con `actor_nombre` en
  {DEPOSITO, TRANSFERENCIA, TRANSFER, TRANSFER_DEPOSITO} (cualquier
  capitalizacion) se suman en una sola entrada
  `actor_nombre = "TRANSFER. / DEPTOS."` y se re-rankean por monto.
- El resto del JSON se preserva tal cual.

NO contacta al backend. NO valida cuadre. Solo aplica la regla bancaria.
"""

from __future__ import annotations

import json
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any

CANONICO = "TRANSFER. / DEPTOS."
ETIQUETAS_CRUDAS = {"DEPOSITO", "TRANSFERENCIA", "TRANSFER", "TRANSFER_DEPOSITO"}


def _es_etiqueta_cruda(nombre: str | None) -> bool:
    if not nombre:
        return False
    return nombre.strip().upper().replace(" ", "_") in ETIQUETAS_CRUDAS


def _to_dec(v: Any) -> Decimal:
    return Decimal(str(v)) if v is not None else Decimal("0")


def consolidar_top5(entradas: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Reagrupa Top5: suma TRANSFER/DEPOSITO en una entrada `TRANSFER. / DEPTOS.`."""
    canonicos: list[dict[str, Any]] = []
    suma_transfer = Decimal("0")
    pct_transfer = Decimal("0")
    hubo_transfer = False

    for e in entradas:
        if _es_etiqueta_cruda(e.get("actor_nombre")):
            suma_transfer += _to_dec(e.get("monto"))
            pct_transfer += _to_dec(e.get("porcentaje"))
            hubo_transfer = True
        elif e.get("actor_nombre") == CANONICO:
            suma_transfer += _to_dec(e.get("monto"))
            pct_transfer += _to_dec(e.get("porcentaje"))
            hubo_transfer = True
        else:
            canonicos.append({**e, "monto": str(_to_dec(e.get("monto")))})

    if hubo_transfer:
        canonicos.append(
            {
                "actor_codigo": None,
                "actor_nombre": CANONICO,
                "monto": str(suma_transfer),
                "porcentaje": str(pct_transfer),
            }
        )

    canonicos.sort(key=lambda x: _to_dec(x.get("monto")), reverse=True)
    for idx, e in enumerate(canonicos[:5], start=1):
        e["lugar"] = idx
    return canonicos[:5]


def consolidar_candidato(data: dict[str, Any]) -> dict[str, Any]:
    """Aplica `consolidar_top5` a cada categoria del candidato."""
    top5 = data.get("top5") or {}
    if not isinstance(top5, dict):
        return data
    nuevo: dict[str, list[dict[str, Any]]] = {}
    for cat, entradas in top5.items():
        if isinstance(entradas, list):
            nuevo[cat] = consolidar_top5(entradas)
        else:
            nuevo[cat] = entradas  # type: ignore[assignment]
    return {**data, "top5": nuevo}


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[1] not in {"-", "--stdin"}:
        raw = Path(argv[1]).read_text(encoding="utf-8")
    else:
        raw = sys.stdin.read()
    data = json.loads(raw)
    out = consolidar_candidato(data)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(sys.argv))
