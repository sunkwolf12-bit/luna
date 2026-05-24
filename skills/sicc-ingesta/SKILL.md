---
name: sicc-ingesta
description: |
  Cargar, corregir y consultar datos del Sistema de Inteligencia y Control
  de Cobranza (SICC) en sicc.protegrt.com. Activar cuando Elena adjunte
  REPORTE_COBRANZA_*.pptx, captura de pantalla del Excel de cobranza, o
  diga "cargame [mes]", "corrige [X] de [mes]", "como va [mes]", "muestrame
  Top5 de [categoria] en [mes]".
allowed-tools: Read, Bash(sicc:*), Bash(python3:*)
---

# sicc-ingesta — operar SICC desde Luna

Habilidad para cargar y mantener la base de datos del Sistema de Inteligencia
y Control de Cobranza (SICC, https://sicc.protegrt.com). Reemplaza al SKILL
viejo `estadistica-mensual-cobranza` y conserva sus reglas de negocio
(consultar `references/reglas-de-negocio.md`).

## 0 · Setup (una sola vez por sesion)

Antes del primer comando comprobar que el CLI y la config esten listos:

```bash
sicc --version       # debe imprimir 0.1.0 o superior
ls ~/.config/sicc/config.toml || echo "FALTA CONFIG"
test -n "$SICC_LUNA_TOKEN" && echo "TOKEN OK" || echo "FALTA TOKEN"
```

Si `sicc` no existe en `PATH`, avisar a Elena: "El CLI `sicc` no esta
instalado en lunita; Claudio debe instalarlo (ver `TODO operativo` mas
abajo)". Sin CLI no puedo ejecutar nada de esta skill.

Si el token no esta, exportarlo desde `/root/sicc/.env` (lo carga Claudio,
no Luna):

```bash
export SICC_LUNA_TOKEN="<valor>"  # uso por sesion; Claudio lo persiste en bashrc
```

## 1 · Triggers y mapeo a comandos

| Lo que dice/manda Elena | Accion |
|---|---|
| Adjunta `REPORTE_COBRANZA_<MES>_<ANIO>.pptx` | Flujo `PPTX -> commit` (seccion 2). |
| Adjunta `ESTADISTICA_<ANIO>.xlsx` canonico | Flujo `XLSX -> commit` (seccion 2-bis). Pre-parse con `reconstruir_datos_gral.py`. |
| Adjunta captura de pantalla del Excel (un solo apartado) | `sicc parse --imagen <ruta> --slot <categoria> --mes M --anio A`. |
| "cargame ENERO" / "sube enero" | Buscar el ultimo PPTX de enero en `~/.openclaw/media/inbound/` y procesarlo. |
| "como va MAYO" / "muestrame mayo" | `sicc show --anio 2026 --mes 5` (T2.6, cuando aterrice). |
| "muestrame Top5 EFECTIVA de mayo" | `sicc show --anio 2026 --mes 5 --categoria efectiva` (T2.6). |
| "corrige RECUPERADA de mayo a 174435" | `sicc update --anio 2026 --mes 5 --concepto RECUPERADA --monto 174435 --razon "Correccion Elena"` (T2.6). |

Si el comando es T2.6 y aun no esta disponible, decirlo claro a Elena
(`sicc show` o `sicc update` no existe todavia, pendiente T2.6).

## 2 · Flujo PPTX -> commit (caso comun)

1. `sicc parse --pptx <ruta> --out /tmp/sicc/<sesion>/candidato_base.json`
   - Genera el JSON candidato con concentrado y `imagenes` (rutas
     extraidas de las slides Top5).
2. Inspeccionar cada imagen del Top5 con `Read <ruta>`. Para cada
   apartado extraer visualmente 5 entradas con `codigo_actor` (o nombre),
   monto y porcentaje. Verificar el TOTAL contra el text box de la slide.
3. **Normalizar tokens de actor** con `scripts/normalize_actor.py` antes
   de armar el JSON. Los PPTX 2026 muestran vendedores solo con numero
   (`6: $356,324`); `normalize_actor_token("6")` devuelve
   `actor_codigo="V6"` automaticamente. NO compensar manualmente.

   ```python
   from normalize_actor import normalize_actor_token
   r = normalize_actor_token("6 GABY")
   # -> actor_codigo="V6", actor_nombre="GABY", warning=None
   ```

   Si `r.warning` no es None, reportar el warning a Elena antes de
   continuar (indica un placeholder ambiguo como `OTROS`).
4. Construir el JSON candidato FINAL combinando lo del parser + lo extraido
   con vision. Aplicar `references/reglas-de-negocio.md` (especialmente la
   consolidacion `TRANSFER. / DEPTOS.`). Guardarlo en
   `/tmp/sicc/<sesion>/candidato_final.json`.
4. `sicc preview --json /tmp/sicc/<sesion>/candidato_final.json`
   - Revisar validaciones con Elena. Si hay validaciones rojas o numeros
     raros, AJUSTAR el JSON antes de commitear.
5. `sicc commit --json /tmp/sicc/<sesion>/candidato_final.json [--force]`
   - `--force` solo si Elena confirma override (mes cerrado, mismo hash,
     etc.).
6. Reportar a Elena en una linea:

   > Cargue MAYO 2026. EFECTIVA $1,030,490.00, RECUPERADA $79,437.00,
   > total $1,184,720.00. Top5 EFECTIVA: 1) Laura V38 $254,xxx (24%), ...

## 2-bis · Flujo XLSX canonico -> commit (pre-parse obligatorio)

Cuando Elena adjunta el xlsx anual canonico (`ESTADISTICA_<ANIO>.xlsx`) o
cuando se rehidrata un anio historico desde Excel, ejecutar SIEMPRE el
pre-parse antes del flujo de ingesta:

1. **Detectar drift de `DATOS GRAL.` mes-vacio** (regla operativa
   documentada en `references/reconstruir-datos-gral.md`). Abrir el xlsx
   y comprobar:
   - Existen hojas `COBRANZA *` (CORRIENTE, EFECTIVA, RECUPERADA, etc.)
     con totales en col B (`TOTAL MENSUAL`).
   - La hoja `DATOS GRAL.` tiene meses con totales en cero (o celdas
     vacias) en las columnas B/D/F/H/J/L mientras las hojas `COBRANZA *`
     sí tienen totales para esos meses.
   - Si ambas condiciones se cumplen -> drift confirmado (Luna llenó
     top5 individuales pero olvidó replicar el resumen). Aplica el
     pre-parse.

2. **Pre-parse: reconstruir DATOS GRAL.** Ejecutar desde el directorio
   de la skill (`scripts/` esta junto a `SKILL.md`):

   ```bash
   python scripts/reconstruir_datos_gral.py \
       --xlsx /home/elena/.openclaw/media/inbound/ESTADISTICA_2024.xlsx \
       --inplace
   ```

   - `--inplace` deja una copia de seguridad `.bak.xlsx` antes de
     sobrescribir el original. Idempotente: si DATOS GRAL. ya esta
     completo, no cambia nada (advertencias informativas).
   - `--out RUTA.xlsx` si Elena prefiere mantener el original intacto.
   - `--force` solo cuando Elena confirme override (sobrescribe celdas
     no-cero existentes). Por defecto las celdas con valor se respetan.
   - Salida `cambios=N saltadas=N advertencias=N` resume lo aplicado.

3. **Continuar con el flujo normal de ingesta**: el xlsx ya tiene los
   totales por mes en `DATOS GRAL.`, asi que `sicc parse --xlsx ...`
   (T2.6) o el bridge `migrar_<anio>.py` los leera correctamente. Sin
   este paso, los meses afectados quedan con `total=0` y la ingesta los
   rechaza por validacion `cuadre_efectiva_recuperada_vs_total`.

> **Fuente canonica del script**: `backend/scripts/reconstruir_datos_gral.py`
> en el repo. La copia en `skill/sicc-ingesta/scripts/` se sincroniza
> manualmente y existe para que la skill desplegada en lunita sea
> autocontenida (no depende del checkout del repo backend). Si tocas la
> logica, modifica el canonico y vuelve a copiar — la cabecera del
> archivo en la skill lo recuerda. Tests viven en
> `backend/tests/test_reconstruir_datos_gral.py` (11/11 verdes).

## 3 · Reglas criticas (resumen — detalle en `references/reglas-de-negocio.md`)

- Consolidar `DEPOSITO` / `TRANSFER` / `TRANSFERENCIA` / `TRANSFER_DEPOSITO`
  en una sola entidad `TRANSFER. / DEPTOS.`. Si el parser las separa,
  sumarlas antes del preview.
- Si un actor del Top5 es desconocido (no aparece en
  `references/catalogo-actores.md` ni en `sicc actores list`), NO inventar
  codigo. Preguntar a Elena: "Top5 trae a `Pedro` con $X, no esta en
  catalogo. Es alta nueva, typo, o lo dejamos como esta?".
- Cuadre obligatorio: `EFECTIVA + RECUPERADA ~ total_general` (tolerancia
  +/- $0.01). Si no cuadra, hay error de transcripcion: revisar las
  cifras crudas antes de insistir.
- `V5` NO se usa nunca (ADR-004, ver reglas-de-negocio).
- Honestidad brutal: si una cifra es ilegible o incoherente, no adivinar.
  Pedir aclaracion a Elena.

## 4 · Manejo de errores del backend

| Codigo HTTP / salida CLI | Que paso | Que hacer |
|---|---|---|
| 401 / `SiccAuthError` (exit 2) | Token invalido o ausente. | Revisar `SICC_LUNA_TOKEN`. Avisar a Claudio si rota. |
| 409 / `SiccConflictError` (exit 3) | Mismo `hash_fuente` ya cargado, o mes cerrado. | Confirmar con Elena. Re-correr con `--force` solo si lo autoriza. |
| 422 / `SiccValidationError` (exit 4) | Una o varias validaciones fallaron. | Leer la salida (cuadre, Top5, actor desconocido). Ajustar JSON o pedir alta. |
| 5xx / `SiccServerError` (exit 5) | Backend caido o error inesperado. | Reportar a Claudio. No reintentar a ciegas. |

Casos puntuales 422:

- **Cuadre roto**: revisar `EFECTIVA` y `RECUPERADA` vs `total_general`.
- **Actor desconocido** y Elena confirma alta nueva: agregar
  `"alta_automatica": true` al actor en el JSON y reintentar
  `sicc preview` -> `sicc commit`.
- **Mes ya cerrado** y Elena confirma override: agregar `--force` al
  commit y registrar la razon de override en el commit message del log.

## 5 · Despues de cerrar un mes

Cuando Elena confirme que un mes esta listo para cierre formal:

1. `sicc cerrar --anio <A> --mes <M> --yes`
   - El backend cierra el mes (status -> CERRADO) y dispara automaticamente
     `REFRESH MATERIALIZED VIEW CONCURRENTLY mv_tendencia_anual` para que
     el dashboard de tendencia anual incluya el nuevo mes (MD-002, F2
     closeout).
2. Si el refresh automatico falla (DB caida, lock conflictivo) o si Elena
   tipea valores manualmente y la MV queda desactualizada por otra razon,
   forzar el refresh manualmente:

   ```bash
   sicc admin mv-refresh
   ```

   El comando llama `POST /api/v1/admin/mv/refresh`. Rate-limited a 1/min.

## 6 · TODO operativo (Claudio configura, Luna no)

- **CLI `sicc` instalado en lunita para el usuario `elena`**: a la fecha
  (2026-05-23) Python en lunita es 3.10 y el CLI requiere 3.12+. Claudio
  debe instalar Python 3.12 (via deadsnakes o uv) y luego
  `pip install --user -e /root/sicc/cli` como `elena`, o un wrapper
  `~/.local/bin/sicc` que invoque al venv. Hasta entonces esta skill no
  puede ejecutarse.
- **Token Luna**: `SICC_LUNA_TOKEN` debe estar exportado en el bashrc de
  `elena` (Claudio lo lee de `/root/sicc/.env`).
- **Config**: `~/.config/sicc/config.toml` creado automaticamente al
  primer `sicc --version`. Default `api_base` ya apunta a
  `https://sicc.protegrt.com/api/v1`.

## 7 · Referencias

- `references/reglas-de-negocio.md` — Reglas heredadas del SKILL
  `estadistica-mensual-cobranza` (consolidacion bancaria, criterio dual
  vendedor/cobrado, exclusiones, ADR-004).
- `references/catalogo-actores.md` — Snapshot de actores activos del seed
  F1 (vendedores V1-V114 + cobradores puros). Fuente real es la tabla
  `actores` del backend; preferir `sicc actores list` cuando T2.6
  aterrice.
- `references/formato-pptx.md` — Estructura esperada de las slides del
  `REPORTE_COBRANZA_*.pptx` y como extraer cada categoria.
- `references/reconstruir-datos-gral.md` — Regla de deteccion del drift
  `DATOS GRAL. mes-vacio post-load Luna` y uso del pre-parse
  `scripts/reconstruir_datos_gral.py` (F4-HF-001).

## 8 · Restricciones (heredadas del SKILL viejo)

- **Honestidad brutal**: si un monto no es legible, no adivinar. Pedir
  aclaracion.
- **Privacidad**: no persistir nombres completos de clientes ni folios en
  memoria larga ni en commits. Solo nombres de vendedores/cobradores y
  totales.
- **Sin emojis** en mensajes operativos (consistente con el estilo de
  Claudio).
