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

### ⚠️ CRÍTICO — Triple limpieza de SDT (placeholders + dataBindings + core.xml)

El archivo base usa **Building Blocks de Word** (galería/docPart) para título y subtítulo en portada y encabezados. Estos SDT tienen **tres** mecanismos que pueden devolver el texto "PROCEDIMIENTO EN BLANCO":

| # | Mecanismo | Qué hace | Fix |
|---|-----------|----------|-----|
| 1 | `<w:placeholder>` | Word carga el texto desde su galería interna | Eliminar TODOS los `<w:placeholder>...</w:placeholder>` |
| 2 | `<w:dataBinding>` | Word jala el valor desde `docProps/core.xml` → `<dc:subject>` | Eliminar TODOS los `<w:dataBinding.../>` de todos los XML |
| 3 | `<dc:subject>` en `docProps/core.xml` | Contiene el texto viejo que alimenta al dataBinding | Reemplazar por el nombre real del procedimiento |

**Fix obligatorio (en este orden):**
1. Reemplazar `<dc:subject>PROCEDIMIENTO EN BLANCO</dc:subject>` por el nombre real en `docProps/core.xml`
2. Eliminar `<w:dataBinding.../>` de TODOS los XML del ZIP (regex: `<w:dataBinding[^>]*/>`)
3. Eliminar `<w:placeholder>.*</w:placeholder>` de TODOS los XML del ZIP
4. Eliminar `<w:showingPlcHdr/>` de TODOS los XML del ZIP

**⚠️ La regex de dataBinding DEBE usar `[^>]` (no `[^/>]`)** porque los atributos xpath contienen `/`:
```
❌ <w:dataBinding[^/>]*/>  — falla con xpath="/ns1:coreProperties[1]/ns0:subject[1]"
✅ <w:dataBinding[^>]*/>   — correcto
```

### PORTADA
- Reemplazar **"PROCEDIMIENTO EN BLANCO"** por el nombre del procedimiento.
- Este texto está en `word/document.xml` del ZIP del .docx.

### ENCABEZADOS (páginas 1, 2, 3...)
- Reemplazar **"PROCEDIMIENTO EN BLANCO"** por el nombre del procedimiento (**debe coincidir 100% con la portada**).
- **FECHA:** reemplazar `31/08/2025` por la fecha que viene en el procedimiento fuente.
- **CLAVE:** insertar el código justo **después de "CLAVE: " en la misma celda** del header2 (regex: capturar `(<w:t...>CLAVE:\s*)(</w:t>)` e insertar la clave entre ambos grupos). **NO insertar en la celda vMerge de la fila siguiente** — esa es la celda del título, no la de CLAVE.
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

### 🖼️ REGLA — Imágenes y Tablas (28/may/2026)

**Si el documento fuente contiene imágenes o tablas, se DEBEN conservar en el documento institucional final.**

El script `crear_procedimiento.py` ya maneja esto automáticamente:
- **Tablas (`<w:tbl>`):** se copian completas con todo su formato y celdas.
- **Imágenes:** se copian los archivos de imagen del .docx fuente al .docx de salida, y se remapean los rId para que Word las muestre correctamente.
- **SDT / controles:** se conservan si forman parte del contenido del DESARROLLO.

**Qué hace el script internamente:**
1. Copia todos los elementos `<w:p>` (párrafos), `<w:tbl>` (tablas) y `<w:sdt>` del body del documento fuente.
2. Detecta imágenes mediante los `r:embed` en los párrafos.
3. Copia los archivos de imagen de `word/media/` del fuente al output.
4. Remapea los rId de las imágenes para no colisionar con los de la plantilla base.
5. Agrega las relaciones (`_rels`) y los `Content_Types` necesarios.

**Verificación post-generación con imágenes:**
- Abrir el .docx y confirmar que las imágenes se ven.
- Verificar que las tablas conservan su estructura.

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

## Verificación post-generación (OBLIGATORIA)

Después de generar cada documento, ejecutar esta verificación:

```python
import zipfile
p = 'workspaces/instructivos/<archivo>.docx'
with zipfile.ZipFile(p) as z:
    doc = z.read('word/document.xml')
    h2 = z.read('word/header2.xml')
    core = z.read('docProps/core.xml')

# Checks obligatorios (todos deben ser 0)
print(f'BLANCO en doc: {doc.count(b"PROCEDIMIENTO EN BLANCO")}')       # debe ser 0
print(f'BLANCO en h2:  {h2.count(b"PROCEDIMIENTO EN BLANCO")}')        # debe ser 0
print(f'BLANCO en core: {core.count(b"PROCEDIMIENTO EN BLANCO")}')     # debe ser 0
print(f'dataBindings:  {doc.count(b"<w:dataBinding") + h2.count(b"<w:dataBinding")}')  # debe ser 0
print(f'CLAVE en h2:   {b"CLAVE: PCE1" in h2}')  # debe ser True (con la clave correcta)
```

## Checklist de verificación (antes de entregar)

- [ ] ¿El nombre en PORTADA coincide 100% con el nombre en ENCABEZADOS?
- [ ] ¿La CLAVE coincide con la del Excel?
- [ ] ¿La CLAVE se insertó en la celda correcta (después de "CLAVE: " en misma celda)?
- [ ] ¿La FECHA es la que viene en el documento fuente?
- [ ] ¿El DESARROLLO incluye TODO el contenido del archivo fuente (sin omitir nada)?
- [ ] ¿DOCUMENTOS DE REFERENCIA y DEFINICIONES están completos (generados si no existían)?
- [ ] ¿El nombre del archivo sigue el formato CLAVE_NOMBRE.docx?
- [ ] ¿No se modificó nada no autorizado del archivo base?
- [ ] ¿0 ocurrencias de "PROCEDIMIENTO EN BLANCO" en doc.xml, header2.xml y core.xml?
- [ ] ¿0 dataBindings residuales en todo el ZIP?
- [ ] ¿0 placeholders residuales en todo el ZIP?
- [ ] ¿Las imágenes y tablas del documento fuente se conservan en el documento final?
