# Pre-parse `reconstruir_datos_gral.py` — drift `DATOS GRAL.` mes-vacio

> Hallazgo origen: **F4-HF-001** (`docs/HALLAZGOS_F4.md`).
> Lección dura del bug 2024: Luna llenó los top5 individuales del xlsx
> `ESTADISTICA_2024.xlsx` (hojas `COBRANZA *`) pero olvidó replicar los
> totales mensuales en la hoja resumen `DATOS GRAL.`. Marzo-diciembre 2024
> quedaron con `total=0` al parseo y la ingesta los rechazó por
> `cuadre_efectiva_recuperada_vs_total`. Fix ad-hoc 2026-05-23 (script
> `reconstruir_datos_gral_2024.py`). Industrializado en F4-HF-001.

## 1 · Cuándo ejecutar el pre-parse

Activa el pre-parse SIEMPRE que se cumplan las dos condiciones a la vez:

1. **Hojas fuente con datos**: el xlsx tiene una o más hojas con nombre
   que empieza por `COBRANZA ` (`COBRANZA CORRIENTE`, `COBRANZA EFECTIVA`,
   `COBRANZA RECUPERADA`, `COBRANZA ADELANTADA F.`, `COBRANZA VENCIDA`)
   o `CANCELACIONES`, y al menos una de ellas tiene totales mensuales
   reales en su `col B` (`TOTAL MENSUAL`).

2. **Resumen `DATOS GRAL.` mes-vacio**: la hoja `DATOS GRAL.` tiene al
   menos un mes (filas 4..15) con la celda de la columna correspondiente
   vacia o en cero, mientras la hoja fuente sí trae total para ese mes.

Mapeo concepto -> columna en `DATOS GRAL.` (header en fila 3):

| Concepto SICC      | Hoja fuente              | Col destino |
|--------------------|--------------------------|-------------|
| CORRIENTE          | `COBRANZA CORRIENTE`     | B           |
| CANCELACIONES      | `CANCELACIONES`          | D           |
| EFECTIVA           | `COBRANZA EFECTIVA`      | F           |
| RECUPERADA         | `COBRANZA RECUPERADA`    | H           |
| ANTICIPADA_FUTURA  | `COBRANZA ADELANTADA F.` | J           |
| VENCIDA            | `COBRANZA VENCIDA`       | L           |

`ANTICIPADA_ANTERIOR` (col N) no se reconstruye automáticamente: no tiene
hoja fuente. Si está vacia se queda en cero.

## 2 · Cómo ejecutar

Desde el directorio raíz de la skill (donde está `SKILL.md`):

```bash
python scripts/reconstruir_datos_gral.py \
    --xlsx /home/elena/.openclaw/media/inbound/ESTADISTICA_2024.xlsx \
    --inplace
```

Flags:

- `--inplace`: sobrescribe el original; **deja una copia `.bak.xlsx`
  junto al original antes de guardar**. Idempotente.
- `--out RUTA.xlsx`: salida separada; original intacto. Mutuamente
  exclusivo con `--inplace`.
- `--force`: sobrescribe celdas de `DATOS GRAL.` que ya tengan valor
  no-cero. Sólo si Elena confirma override (default: respetar lo que
  Luna o el operador ya escribieron).
- `--log-level DEBUG|INFO|WARNING|ERROR`: default `INFO`.

Salida esperada (resumen al final):

```
listo. cambios=72 saltadas=0 advertencias=0
```

- `cambios` = celdas escritas.
- `saltadas` = celdas con valor existente, no forzadas.
- `advertencias` = problemas no-fatales (hoja fuente vacia, mes en
  `DATOS GRAL.` con valor pero sin total en la hoja fuente — drift
  inverso que conviene revisar a mano).

## 3 · Verificación post-pre-parse

Antes de continuar al `sicc parse`/migrar histórico:

1. Abrir el xlsx (o `python -c "import openpyxl; wb=...; print(...)"`) y
   confirmar que las celdas B/D/F/H/J/L de las filas 4..15 (meses) en
   `DATOS GRAL.` tienen los totales esperados.
2. La copia de seguridad `.bak.xlsx` queda junto al original; si algo
   sale mal puedes restaurar con `mv X.bak.xlsx X.xlsx`.
3. El xlsx ya quedó consistente: `EFECTIVA + RECUPERADA ~ COBRANZA TOTAL`
   por mes. Si no cuadra al centavo, no es bug del pre-parse — revisa
   el xlsx fuente.

## 4 · Origen y mantenimiento

- **Fuente canónica del script**: `backend/scripts/reconstruir_datos_gral.py`
  en el repo `sunkwolf/sicc`.
- **Copia en la skill**: `skill/sicc-ingesta/scripts/reconstruir_datos_gral.py`.
  Existe para que la skill desplegada en lunita sea autocontenida (no
  depende del checkout del repo backend en `/root/sicc/`).
- **Sincronización**: manual. Si tocas la lógica, modifica el canónico,
  corre los tests (`cd backend && uv run pytest
  tests/test_reconstruir_datos_gral.py -q`, 11/11) y re-copia el archivo
  a la skill (restaurando la cabecera "FUENTE CANONICA").
- **Tests**: `backend/tests/test_reconstruir_datos_gral.py`. Suite
  standalone (xlsx en memoria, sin DB ni red). 11 casos: happy path,
  idempotencia, `--force`, hoja ausente, hoja vacia, `--inplace`,
  `--out`, xlsx sin `DATOS GRAL.`, coherencia inversa.

## 5 · Anti-patrones

- **NO**: editar `DATOS GRAL.` a mano celda por celda. Usa el script,
  garantiza idempotencia y deja log auditable.
- **NO**: copiar el script a otra ubicación sin actualizar la cabecera
  "FUENTE CANONICA". Drift garantizado.
- **NO**: pasar el xlsx directo a `sicc parse` sin verificar el drift
  cuando viene de Luna o de una rehidratación histórica. El bug 2024
  costó una sesión completa de debugging.
