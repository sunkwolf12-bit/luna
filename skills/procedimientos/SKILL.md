# SKILL.md — Procedimientos Institucionales

## Objetivo
Recibir un procedimiento de Elena (en archivo Word), identificar la CLAVE según el Excel oficial, y trasladar **todo** el contenido al formato institucional `FORMATO_INSTITUCIONAL_PROCEDIMIENTO_2025.docx`, generando un archivo-final con el formato oficial y nombre correcto.

---

## ARCHIVOS FUENTE (references/)

| Alias | Ruta en workspace | Descripción |
|-------|------------------|-------------|
| `BASE_FORMAT` | `workspaces/instructivos/FORMATO_INSTITUCIONAL_PROCEDIMIENTO_2025.docx` | Formato base institucional (plantilla). |
| `CODES_XLSX` | `workspaces/instructivos/CHECK_LIST_ACTIVIDADES_GERENTE_COBRANZA_2025_LIMPIO.xlsx` | Archivo oficial de códigos (columna "C" = CLAVE). |

---

## PASO 1 — Identificar la CLAVE del procedimiento

1. Abrir `CODES_XLSX` (hoja activa 默认).
2. Buscar en la **columna "C"** (CLAVE DEL PROCEDIMIENTO) o en la columna "B" (NOMBRE) si la columna C no tiene valores.
3. Buscar por **coincidencia parcial** del nombre del procedimiento que Elena envió:
   - Si Elena envió `PROCEDIMIENTO PARA LA ASIGNACIÓN DE COBRANZA QUINCENAL`, busco en las columnas la cadena `"ASIGNACIÓN DE COBRANZA QUINCENAL"` o `"COBRANZA QUINCENAL"`.
4. **Regla estricta**: NO inventar claves. Si el procedimiento NO aparece en la lista → notificar a Elena, esperar autorización antes de avanzar.

**Salida del paso 1**: tener `CLAVE` y `NOMBRE_OFICIAL` del Excel.

---

## PASO 2 — Extraer contenido del documento de Elena

1. El documento de Elena llega como ruta/archivo adjunto en el chat o en `media/inbound/`.
2. Extraer **TODO** el texto del documento (párrafos 0 en adelante).
3. **No resumir, no interpretar, no recategorizar** — copiar textualmente todo lo que dice en cada sección.
4. Si el documento de Elena incluye las secciones 1. OBJETIVO, 2. ALCANCE, etc., esas secciones + su texto se marcan como "contenido_de_elena".
5. Se preservan también los pasos numerados (5.1, 5.2, etc.) tal como vinieron — sin modificar numeración.

**Salida del paso 2**: texto_completo_del_documento (string multi-línea).

---

## PASO 3 — Modificar el formato base

1. Copiar `BASE_FORMAT` a ruta de salida: `workspaces/instructivos/{CLAVE}_{NOMBRE_SINACENTOS}.docx`.
2. **Modificar header2.xml** (solo estas 3 sustituciones):

| Qué buscar | Por qué substituir |
|------------|-------------------|
| `PROCEDIMIENTO EN BLANCO` (cell 0, row 0) | `NOMBRE_DEL_PROCEDIMIENTO` (de la tabla del header — coincide con el título de la portada del documento de Elena) |
| `: 31/08/202` + `5` después | `: {FECHA}` donde FECHA viene del documento de Elena (buscar en el texto: fechas tipo `dd/mm/aaaa` o indicar explícitamente) |
| `CLAVE: ` (cell 2, row 0) + siguiente `<w:t>` vacío | El valor de `CLAVE` del Excel |

3. **Modificar document.xml/body**:
   - Localizar en el body del BASE FORMAT las etiquetas existentes: `OBJETIVO:`, `ALCANCE:`, alguna etiqueta de `DOCUMENTOS DE REFERENCIA` o `DEFINICIONES` o `DESARROLLO`.
   - **Reemplazar el texto de cada etiqueta** (lo que viene después del `:` en la misma línea del base) **por el contenido correspondiente de Elena**.
   - Si la etiqueta del base dice `DESARROLLO` y Elena tiene pasos `5.1`, `5.2`, etc., el contenido替换 (reemplazo) va en esa misma área.
   - **No eliminar las etiquetas** (OBJETIVO:, ALCANCE:, etc.) — se mantienen visibles en el documento final.
   - Si alguna de las 5 secciones no existe en el documento de Elena: dejar vacío el contenido debajo de la etiqueta del base (etiqueta se queda, contenido en blanco).

**Regla de contenido**: copiar el texto de Elena **exactamente** — misma redacción, mismo orden, misma puntuación. No parafrasear, no corregir ortografía interna de Elena.

---

## PASO 4 — Construir el nombre del archivo de salida

`{CLAVE}_{NOMBRE_SINACENTOS_ESPACIOSGUIONES}.docx`

Ejemplo:
- CLAVE = `PCC4`
- NOMBRE = `PROCEDIMIENTO PARA LA ASIGNACIÓN DE COBRANZA QUINCENAL (COBRADORES)`
- Resultado: `PCC4_PROCEDIMIENTO_PARA_LA_ASIGNACION_DE_COBRANZA_QUINCENAL_COBRADORES.docx`

---

## NOMENCLATURA DE CLAVES (bloques del Excel)

| Bloque | Prefijo | Significado |
|--------|---------|-------------|
| A | PCA | Pagos |
| B | PCB | Documentos operativos |
| C | PCC | Cobradores |
| D | PCD | Vendedores |
| E | PCE | Contable/Finanzas |
| F | PCF | Reportes |

---

## REGLAS CRÍTICAS (no negociables)

1. **El nombre del procedimiento en el ENCABEZADO (header2) y en la PORTADA (body) debe ser IDÉNTICO al 100%** — ni un espacio diferente, ni una mayúscula diferente.
2. **La CLAVE viene del Excel, siempre**. Si no existe en el Excel, no avanzar y preguntar.
3. **No modificar nada que Elena no haya autorizado explícitamente** — si hay algo que no se entiende del procedimiento de Elena, preguntar antes de asumir.
4. **Transferir TODO el contenido — no omitir nada** del documento que Elena envió.
5. **Fecha**: usar la fecha que aparezca en el documento de Elena. Si no hay fecha, usar la fecha actual del sistema.
