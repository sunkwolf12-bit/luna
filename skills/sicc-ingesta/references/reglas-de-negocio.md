# Reglas de negocio — estadistica mensual de cobranza

Extracto sintetizado del SKILL viejo `estadistica-mensual-cobranza` (que vive
en `/home/elena/.openclaw/workspace/skills/estadistica-mensual-cobranza/`),
ajustado al stack SICC. Esta es la **fuente de verdad operativa** para
preparar el JSON candidato antes de `sicc preview`.

## 1 · Conceptos del concentrado

El concentrado mensual tiene 7 conceptos. El backend usa el enum
`concepto_concentrado`:

| Concepto | Que representa | Base 100% |
|---|---|---|
| `CORRIENTE` | Universo total del mes que se debia cobrar (recibos vigentes). | Si — sirve de base para los demas %. |
| `CANCELACIONES` | Recibos cancelados (revertidos) — no se cobraron. | No. % se calcula sobre `CORRIENTE`. |
| `EFECTIVA` | Cobranza realizada dentro del mes corriente. | No. |
| `RECUPERADA` | Cobranza realizada de meses anteriores (vencida que se recupero). | No. |
| `ANTICIPADA_FUTURA` | Pagos adelantados de meses futuros. | No. |
| `VENCIDA` | Lo que quedo vencido al cierre. | No. |
| `ANTICIPADA_ANTERIOR` | Saldo anticipado de meses previos aplicado este mes. | No. |

> Nota: el SKILL viejo y el PPTX llaman "Total Mensual" a la suma del
> universo del mes (la columna del apartado sin filtrar por status). Eso es
> `CORRIENTE` en el modelo SICC.

## 2 · Regla TRANSFER. / DEPTOS. (consolidacion bancaria)

Para los apartados basados en **COBRADO** (`EFECTIVA`, `RECUPERADA`,
`ANTICIPADA_FUTURA`, "TOTAL_GRAL" del Excel viejo), todos los pagos NO en
efectivo se consolidan en una sola entidad:

- Etiquetas crudas en la fuente: `DEPOSITO`, `TRANSFERENCIA`,
  `TRANSFER_DEPOSITO`, `TRANSFER` (cualquier capitalizacion).
- Etiqueta canonica en el sistema: **`TRANSFER. / DEPTOS.`** (existe como
  `actor` tipo `cobrador_puro` en la DB).
- Accion: sumar los montos y meter una sola entrada al Top5 con
  `actor_nombre = "TRANSFER. / DEPTOS."`.

El backend (`services/consolidador.py`) tambien aplica esta regla; el
script local `scripts/consolidar.py` la replica en cliente para preview /
debugging.

## 3 · Criterio de agrupacion del Top5 por categoria

Heredado del SKILL viejo:

| Categoria (slide PPTX) | Criterio Top5 | Notas |
|---|---|---|
| Cobranza Corriente | Vendedor (codigo o nombre) | Codigo `V\d+`. |
| Cancelaciones | Vendedor (codigo o nombre) | Codigo `V\d+`. |
| Cobranza Vencida / Atrasada | Ubicacion / Ruta | El SKILL viejo agrupaba por ruta; SICC usa por vendedor codigo. **Verificar con Elena** caso por caso. |
| Cobranza Efectiva | COBRADO (persona que cobro) | Aplicar consolidacion `TRANSFER. / DEPTOS.`. |
| Cobranza Recuperada | COBRADO | Aplicar consolidacion. |
| Cobranza Adelantada Futura | COBRADO | Aplicar consolidacion. |
| Cobranza Total / Pagada | COBRADO | Aplicar consolidacion. SICC no almacena este Top5 separado; se considera derivado de los anteriores. |

## 4 · Calculo de porcentajes

- **`%` del concentrado**: cada concepto vs `CORRIENTE`.
  `porcentaje = monto / corriente`.
- **`%` dentro del Top5**: cada entrada vs el TOTAL del apartado.
  `porcentaje = monto / total_apartado`.

Los porcentajes en el JSON candidato se expresan como decimal con 4
posiciones (`0.6634` = 66.34%).

## 5 · Exclusiones y casos borde

- **Cancelaciones**: revierten la cobranza, no la suman. Aparecen como su
  propio concepto pero NO se descuentan de `EFECTIVA`/`RECUPERADA` en el
  Top5; son listado aparte.
- **`ANTICIPADA_ANTERIOR`** del concentrado puede ser `0.00` muchos meses;
  esta bien.
- Si un slide trae menos de 5 entradas reales, dejar las que haya. El
  backend lo permite con advertencia (validacion #4).

## 6 · ADR-004 — V5 no se usa

Codigo de vendedor `V5` es historico erroneo. **Nunca** aparece en seeds
ni se acepta en ingesta. Si una imagen Top5 menciona `V5`, asumir typo
(probablemente `V55` o `V56`) y pedir confirmacion a Elena antes de
commitear.

## 7 · Resolucion de actor en backend

El backend resuelve `actor_codigo` primero, luego `actor_nombre` (fallback)
contra la tabla `actores`. Si no encuentra y el JSON no trae
`alta_automatica=true`, rechaza con 422.

Listado canonico: ver `catalogo-actores.md` o pedir al backend con
`sicc actores list` (T2.6). El backend siempre gana sobre el snapshot
local — el snapshot ayuda solo en caso de no tener conectividad para
preview.

## 8 · Validaciones del backend (resumen)

Las 10 validaciones que rechaza/advierte el backend estan en SPEC §4.5.
Las criticas para Luna:

1. Cuadre `EFECTIVA + RECUPERADA ~ total_general` (+/- $0.01) — rechaza.
2. Sin etiquetas crudas `DEPOSITO|TRANSFER|TRANSFERENCIA` sueltas —
   rechaza, exige consolidacion.
3. Suma de % Top5 <= 100% — rechaza.
5. Mes `cerrado` — rechaza sin `--force` + razon.
6. `hash_fuente` duplicado — 409 sin `--force`.
8. Actor desconocido — rechaza sin `alta_automatica=true`.

## 9 · Privacidad

- **No persistir** nombres completos de asegurados ni folios de poliza en
  memoria larga ni en commits. Las cifras del concentrado y Top5 (con
  codigos de vendedor o nombres de cobradores) SI van; los datos de
  clientes finales NO.
