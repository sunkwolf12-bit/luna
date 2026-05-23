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
3. Construir el JSON candidato FINAL combinando lo del parser + lo extraido
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

## 5 · TODO operativo (Claudio configura, Luna no)

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

## 6 · Referencias

- `references/reglas-de-negocio.md` — Reglas heredadas del SKILL
  `estadistica-mensual-cobranza` (consolidacion bancaria, criterio dual
  vendedor/cobrado, exclusiones, ADR-004).
- `references/catalogo-actores.md` — Snapshot de actores activos del seed
  F1 (vendedores V1-V114 + cobradores puros). Fuente real es la tabla
  `actores` del backend; preferir `sicc actores list` cuando T2.6
  aterrice.
- `references/formato-pptx.md` — Estructura esperada de las slides del
  `REPORTE_COBRANZA_*.pptx` y como extraer cada categoria.

## 7 · Restricciones (heredadas del SKILL viejo)

- **Honestidad brutal**: si un monto no es legible, no adivinar. Pedir
  aclaracion.
- **Privacidad**: no persistir nombres completos de clientes ni folios en
  memoria larga ni en commits. Solo nombres de vendedores/cobradores y
  totales.
- **Sin emojis** en mensajes operativos (consistente con el estilo de
  Claudio).
