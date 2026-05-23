# Formato del PPTX `REPORTE_COBRANZA_<MES>_<ANIO>.pptx`

Descripcion de la estructura esperada de los reportes que Elena envia cada
mes, basada en `REPORTE_COBRANZA_JUNIO_2025.pptx` (verificado 2026-05-23,
10 slides).

El parser `sicc parse --pptx` (T2.5) ya implementa esta extraccion; este
documento es para que Luna entienda que sale del parser y donde apoyarse
con vision para completar el Top5.

## 1 · Estructura general

El archivo tiene tipicamente **10 slides**:

| # | Tipo | Titulo | Contenido |
|---|---|---|---|
| 1 | Portada | `REPORTE COBRANZA <MES> <ANIO>` | Imagen ornamental; no aporta datos. |
| 2 | Grafica | `Grafica General` | Resumen visual; el parser puede ignorarla. |
| 3 | Top5 | `Cobranza Corriente` | Imagen del apartado + text box `TOTAL $X,XXX,XXX`. |
| 4 | Top5 | `Cancelaciones` | idem. |
| 5 | Top5 | `Cobranza Vencida` | idem. |
| 6 | Top5 | `Cobranza Efectiva` | idem (aplica consolidacion `TRANSFER. / DEPTOS.`). |
| 7 | Concentrado | `COBRANZA TOTAL` | Es el `total_general` del mes (suma EFECTIVA + RECUPERADA). |
| 8 | Top5 | `Cobranza Recuperada` | idem (aplica consolidacion). |
| 9 | Top5 | `Cobranza Adelantada` | idem (aplica consolidacion). Corresponde a `ANTICIPADA_FUTURA`. |
| 10 | Proyeccion | `Proyeccion <MES_SIGUIENTE> <ANIO>` | Sin imagen; text boxes con conceptos + montos esperados. |

> Numeros redondeados a entero pesos en los slides; el JSON candidato usa
> decimal con 2 posiciones.

## 2 · Mapeo titulo PPTX -> concepto SICC

| Titulo slide | `slot` parser | Concepto SICC (concentrado) |
|---|---|---|
| `Cobranza Corriente` | `corriente` | `CORRIENTE` |
| `Cancelaciones` | `cancelaciones` | `CANCELACIONES` |
| `Cobranza Vencida` | `vencida` | `VENCIDA` |
| `Cobranza Efectiva` | `efectiva` | `EFECTIVA` |
| `Cobranza Recuperada` | `recuperada` | `RECUPERADA` |
| `Cobranza Adelantada` | `adelantada` | `ANTICIPADA_FUTURA` |
| `COBRANZA TOTAL` | (no Top5) | Da el `total_general` del mes. |

> `ANTICIPADA_ANTERIOR` casi nunca aparece en el PPTX; si falta, ponerlo
> en `0.00`.

## 3 · Extraccion de cada slide Top5

Por cada slide tipo Top5 el parser hace dos cosas:

1. **Texto**: lee el text box `TOTAL $1,553,183` con regex
   `TOTAL\s*\$?([\d,.]+)` y lo deposita como `total_apartado` para esa
   categoria.
2. **Imagen**: extrae la imagen embebida (shape type 13) a
   `/tmp/sicc/<sesion>/slide_<n>_<categoria>.png` y la lista en el campo
   `imagenes` del JSON candidato.

**Luna NO lee las imagenes con OCR**; las lee con vision multimodal via
`Read <ruta>`. De cada imagen extraer 5 entradas con:

- Codigo de vendedor (`V\d+`) **si aparece**, sino nombre del cobrador.
- Monto en pesos.
- Porcentaje (lo que muestre el slide; si no, calcular `monto /
  total_apartado`).

## 4 · Slide Proyeccion (ultima)

Slide sin imagen, solo text boxes con conceptos y montos para el mes
siguiente. El parser intenta extraerlos por patrones; si la disposicion
varia (ej. tabla en lugar de text boxes sueltos), Luna puede completarlo
manualmente leyendo el slide con `Read` despues de exportar la slide a
PNG con `python3 -m pptx`/LibreOffice.

Formato esperado en JSON candidato:

```json
"proyeccion": [
  {"concepto": "CORRIENTE",     "monto": "1103443.00", "porcentaje": "1.0000"},
  {"concepto": "CANCELACIONES", "monto": "110344.00",  "porcentaje": "0.1000"},
  {"concepto": "EFECTIVA",      "monto": "827583.00",  "porcentaje": "0.7500"},
  {"concepto": "VENCIDA",       "monto": "165517.00",  "porcentaje": "0.1500"}
]
```

## 5 · Casos borde

- **Slide titulo diferente**: si Elena cambia capitalizacion o sufijos,
  el parser hace match con regex insensible a mayusculas y elimina
  acentos. Si aun asi falla, slide queda como `desconocido` y Luna debe
  asignarlo manualmente en el JSON.
- **Mes con CANCELACIONES = 0**: poner `0.00`, no omitir.
- **`COBRANZA TOTAL` ausente**: calcular `EFECTIVA + RECUPERADA` y usar
  ese valor como `total_general`. Documentar el calculo en el commit log.
- **Imagen ilegible/borrosa**: pedir a Elena el original o el Excel
  fuente. NO inventar Top5.

## 6 · Verificacion antes de preview

Despues del parser y antes de `sicc preview`:

- `EFECTIVA + RECUPERADA ~ total_general` con tolerancia +/- $0.01.
- Cada Top5 con 5 entradas (warning si menos).
- Suma de porcentajes Top5 <= 100% por categoria.
- Ninguna entrada con etiqueta cruda `DEPOSITO|TRANSFER|TRANSFERENCIA`
  suelta — todas consolidadas en `TRANSFER. / DEPTOS.`.
- Concentrado completo (7 conceptos; `ANTICIPADA_ANTERIOR` puede ser 0).
