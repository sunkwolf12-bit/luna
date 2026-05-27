# SKILL.md — Skill para Procedimientos

## Objetivo
Crear documentos de procedimientos operativos para Proteg-rt usando como plantilla el archivo base `FORMATO_INSTITUCIONAL_PROCEDIMIENTO_2025.docx`.

---

## REGLA CRÍTICA — Códigos oficiales del archivo Excel

**El archivo oficial de códigos es:**
`CHECK_LIST_ACTIVIDADES_GERENTE_COBRANZA_2025_LIMPIO.xlsx` (hoja "ACTIVIDADES TOTALES")

**Los códigos de procedimientos VIENEN SIEMPRE de este archivo. NO inventar claves.**

### Flujo obligatorio para obtener la clave:
1. **Consultar la lista oficial** leyendo el Excel y buscando en la columna **C (CLAVE)** y columna **B (NOMBRE)** un match por nombre o tema.
2. Si hay un match exacto o cercano → usar esa CLAVE.
3. Si **NO existe** clave en el Excel → **notificar a Elena** y proponer crear una clave nueva según el bloque correspondiente:
   - **A** → Pagos (PCA#)
   - **B** → Documentos operativos (PCB#)
   - **C** → Cobradores (PCC#)
   - **D** → Vendedores (PCD#)
   - **E** → Contable/Finanzas (PCE#)
   - **F** → Reportes (PCF#)
4. Solo después de que Elena autorice la nueva clave, usarla.

---

## Flujo completo paso a paso

### 1. Recibir el procedimiento
Elena envía un archivo **Word (.docx)** con el procedimiento (título, fecha de creación, y contenido).

### 2. Extraer metadatos del archivo fuente
- **Nombre del procedimiento:** el título que aparece en el documento (ej. "PROCEDIMIENTO DE SEGUIMIENTO A COBRANZA ATRASADA")
- **Fecha de creación/modificación:** la fecha que aparece en el documento (ej. "25/10/2025")
- **Contenido:** las secciones 1. Objetivo, 2. Alcance, 3. Responsables, 4. Procedimiento

### 3. Buscar la CLAVE en el Excel
Usar el archivo `CHECK_LIST_ACTIVIDADES_GERENTE_COBRANZA_2025_LIMPIO.xlsx` para encontrar la CLAVE que corresponda por nombre/tema.

### 4. Crear el documento institucional

Usar el script `scripts/crear_procedimiento.py`:
```bash
python3 skills/skill-para-procedimientos/scripts/crear_procedimiento.py \
  <archivo_fuente.docx> <CLAVE> "<NOMBRE>" "<FECHA>" "<DEPARTAMENTO>"
```

Ejemplo:
```bash
python3 skills/skill-para-procedimientos/scripts/crear_procedimiento.py \
  /home/elena/.openclaw/media/inbound/procedimiento.docx \
  PCD1 \
  "PROCEDIMIENTO DE SEGUIMIENTO A COBRANZA ATRASADA" \
  "25/10/2025" \
  "Cobranza"
```

Si el script falla o hay que hacer ajustes manuales, seguir las reglas de abajo.

---

## Reglas de modificación del archivo base

### PORTADA
- Reemplazar **"PROCEDIMIENTO EN BLANCO"** por el nombre del procedimiento.
- Este texto está en `word/document.xml` del ZIP del .docx.

### ENCABEZADOS (páginas 1, 2, 3...)
- Reemplazar **"PROCEDIMIENTO EN BLANCO"** por el nombre del procedimiento (**debe coincidir 100% con la portada**).
- **FECHA:** reemplazar `31/08/2025` por la fecha que viene en el procedimiento fuente.
- **CLAVE:** reemplazar el valor vacío por la CLAVE obtenida del Excel.
- **DEPARTAMENTO:** "Cobranza" (o el que corresponda).
- Estos textos están en `word/header2.xml`.

### REGLA: NO modificar nada no autorizado
- No cambiar formato, estilos, márgenes, logos, ni ninguna otra parte del archivo base.
- Solo reemplazar los textos indicados arriba.

---

## Estructura del contenido (CUERPO)

El documento final debe tener este orden exacto:

1. **OBJETIVO** — Texto del objetivo (extraído del archivo fuente, sección "1. Objetivo").
2. **ALCANCE** — Texto del alcance (extraído de "2. Alcance").
3. **DOCUMENTOS DE REFERENCIA** — Si el procedimiento fuente no los menciona, **generarlos** con base en la información del mismo (mencionar CRM, SIGA, archivos Excel, Google Sheets, etc. según lo que aparezca en el DESARROLLO).
4. **DEFINICIONES** — Si el procedimiento fuente no las menciona, **generarlas** con base en la información del mismo (definir términos clave que aparezcan en el procedimiento).
5. **DESARROLLO** — Aquí va el procedimiento completo:
   - Incluir la sección "3. Responsables" y todo el "4. Procedimiento".
   - **REGLA: NO omitir NADA de información del archivo que Elena envía.**
   - TODO el contenido desde "3. Responsables" hasta el final del documento fuente va aquí.

---

## Nombre del archivo de salida

Formato: `(CLAVE)_(NOMBRE_SANITIZADO).docx`

Donde `NOMBRE_SANITIZADO` es el nombre del procedimiento convertido a mayúsculas, sin acentos, espacios reemplazados por guiones bajos.

Ejemplo:
- CLAVE: `PCD1`
- Nombre: `PROCEDIMIENTO DE SEGUIMIENTO A COBRANZA ATRASADA`
- Archivo: `PCD1_PROCEDIMIENTO_DE_SEGUIMIENTO_A_COBRANZA_ATRASADA.docx`

El archivo se guarda en: `workspaces/instructivos/`

---

## Checklist de verificación (antes de entregar)

- [ ] ¿El nombre en PORTADA coincide 100% con el nombre en ENCABEZADOS?
- [ ] ¿La CLAVE coincide con la del Excel?
- [ ] ¿La FECHA es la que viene en el documento fuente?
- [ ] ¿El DESARROLLO incluye TODO el contenido del archivo fuente (sin omitir nada)?
- [ ] ¿DOCUMENTOS DE REFERENCIA y DEFINICIONES están completos (generados si no existían)?
- [ ] ¿El nombre del archivo sigue el formato CLAVE_NOMBRE.docx?
- [ ] ¿No se modificó nada no autorizado del archivo base?
