# SKILL.md — Skill para Procedimientos

## Objetivo
Crear documentos de procedimientos operativos para Proteg-rt usando como plantilla el documento de referencia PCC2 (`PCC2_PROCEDIMIENTO_TRATAMIENTO_DE_TARJETAS_DE_COBRO.docx`).

---

## REGLA CRÍTICA — Códigos oficiales del archivo Excel (26/may/2026)

**El archivo oficial de códigos es:**
`CHECK_LIST_ACTIVIDADES_GERENTE_COBRANZA_2025.xlsx` (hoja "ACTIVIDADES TOTALES")

**Los códigos de procedimientos VIENEN SIEMPRE de este archivo. NO inventar códigos tipo PAC1, PAC2, PAC3, PAC4.**

### Flujo obligatorio:
1. **Consultar la lista oficial** (abajo) antes de crear cualquier procedimiento.
2. Si el procedimiento que necesitas **ya existe** → usar su CLAVE y NOMBRE oficial.
3. Si el procedimiento **NO existe** → preguntar a Elena si autoriza uno nuevo, esperar respuesta, y solo después crearlo con la clave que ella indique.

### Lista oficial de códigos (hoja "ACTIVIDADES TOTALES"):

| BLOQUE | CLAVE | NOMBRE DEL PROCEDIMIENTO |
|--------|-------|--------------------------|
| A | PCA1 | RECEPCION Y APLICACIÓN DE PAGOS DIARIOS EN SIGA, COBRANZA DEL DIA |
| A | PCA2 | APLICACIÓN DE PAGOS EN CRM "PROTEG-RT" |
| A | PCA3 | APLICACIÓN DE SALDOS A FAVOR EN CRM "PROTEG-RT" |
| B | PCB1 | ASIGNACION, ENTREGA Y ARCHIVO DIARIO DE POLIZAS Y ENDOSOS |
| B | PCB2 | RECOLECCION Y NOTIFICACION DE ENTREGA DE POLIZAS Y ENDOSOS |
| B | PCB3 | PROCEDIMIENTO DE CONTROL, SUPERVISION DE RECIBOS |
| B | PCB4 | CANCELACION DE POLIZAS |
| B | PCB5 | PARA LA CANCELACIÓN DE RECIBOS DE PAGO Y AVISOS DE VISITA |
| B | PCB6 | ATENCION GRUAS / ATENCION SINIESTROS |
| C | PCC1 | ASIGNACION DE TARJETAS A COBRADORES Y VENDEDORES |
| C | PCC2 | PROCEDIMIENTO PARA EL TRATAMIENTO DE TARJETAS DE COBRO |
| C | PCC3 (antes PC8) | DEVOLUCION DE TARJETAS DE COBRO POR ATRASO (PC8) |
| C | PCC4 | ASIGNACIÓN DE COBRANZA QUINCENAL (COBRADORES) |
| C | PCC5 | REGISTRO DE GASTOS ANUAL DE MOTOCICLETAS DE COBRADORES |
| C | PCC6 | REVISION MENSUAL DE TARJETAS ASIGNADAS A COBRADORES |
| D | PCD1 | PROCEDIMIENTO DE SEGUIMIENTO A COBRANZA ATRASADA |
| E | PCE1 | CAPTURA Y ACTUALIZACION DE DEPOSITOS / TRANSFERENCIAS DIARIOS |
| E | PCE2 | PARA LA GENERACION DEL FORMATO DE DISPERSION DE NOMINA |
| E | PCE3 | ELABORACION DE LACONCILIACION BANCARIA |
| E | PCE4 | FACTURACIÓN MENSUAL DE INGRESOS BANCARIOS EN EFECTIVO (RFC GENERICO) |
| E | PCE5 | FACTURACION DE CAJA CHICA |
| E | PCE6 | PARA LA FACTURACIÓN DE PAGOS DE IMPUESTOS |
| F | PCF1 | PARA LA REALIZACION DEL REPORTE DE COMISIONES QUINCENALES DE VENDEDORES |
| F | PCF2 | PARA REPORTE Y PAGO DE COMISIONES QUINCENALES A COBRADORES |
| F | PCF3 | PARA LA GENERACION DE REPORTE MENSUAL DE COBRANZA |

---

## REGLA DE ORO (del mensaje de Elena 26/may/2026)
**El nombre del procedimiento en el ENCABEZADO y en el CUERPO del documento debe coincidir EXACTAMENTE al 100%.**

---

## Flujo para determinar la CLAVE correcta

1. Recibir el nombre o descripción del procedimiento a crear.
2. Buscar en la **Lista oficial de códigos** (sección anterior).
3. **Si existe** → Usar el CLAVE y NOMBRE oficial que aparece en el archivo Excel.
4. **Si NO existe** → Preguntar a Elena si autoriza crear uno nuevo; esperar su respuesta con el código a usar. No avanzar sin esa autorización.

**Nunca crear códigos nuevos como PAC1, PAC2, PAC4, etc.** — siempre verificar primero en el Excel. Los códigos oficiales tienen el formato `PXn` donde X es la letra del bloque (A–F) y n es el número consecutivo dentro de ese bloque.

---

## Archivos de referencia

| Archivo | Uso |
|---------|-----|
| `PCC2_PROCEDIMIENTO_TRATAMIENTO_DE_TARJETAS_DE_COBRO---1200a82e-0cde-4aa3-a31f-adf88b19d90d.docx` | Plantilla de formato para TODOS los procedimientos nuevos. Usar este como base para copiar encabezados y estructura. |
| `CHECK_LIST_ACTIVIDADES_GERENTE_COBRANZA_2025.xlsx` (hoja "ACTIVIDADES TOTALES") | Fuente oficial de códigos (PCA1–PCF3). Consultar SIEMPRE antes de crear un procedimiento. |
| Carpeta: `workspaces/instructivos/` | Carpeta donde guardar los procedimientos generados. |

---

## Estructura del documento de referencia (PCC2)

### Los 3 headers (NO modificar — copiar tal cual de PCC2):

- **header1.xml**: Logo grande con "PROTEG-RT MUTUALIDAD A.C." (imagen embebida). **Copiar exacto, no cambiar.**
- **header2.xml**: Contiene UNA tabla con:
  - **Fila de departamentos** (arriba): FIRMA DIRECCIÓN | DEPT.ADMINISTRATIVO | DEPT.VENTAS | DEPT.COBRANZA | DEPT.JURÍDICO — estos textos están **embebidos como parte de imágenes/dibujos**, no como texto editable. **NO intentar cambiar estos textos — copiar la tabla completa como está.**
  - **Fila PROCEDIMIENTO** (abajo): `PROCEDIMIENTO [TÍTULO]` | `FECHA: DD/MM/AAAA` | `CLAVE: PCXn` | `REVISIÓN: 00` | `DEPARTAMENTO: Cobranza`
  - **Imagen del escudo** (al final del header): imagen embedded (image2.png) — **copiar exacta**
- **header3.xml**: Logo secundario (imagen embebida). **Copiar exacto, no cambiar.**

### Cuerpo del documento (body) — contenido del procedimiento

El PCC2 tiene en su body el procedimiento "TRATAMIENTO DE TARJETAS DE COBRO". **Este contenido del body es específico de cada procedimiento y DEBE SER REEMPLAZADO COMPLETAMENTE al crear uno nuevo.**

Estructura obligatoria del cuerpo:
1. **1. Objetivo**
2. **2. Alcance**
3. **3. Responsables** (lista con •)
4. **4. Definiciones** (lista con •)
5. **5.- DESARROLLO**
6. **5. Procedimiento**
7. **5.1** hasta **5.N** (pasos numerados)
8. **REGLAS DE CONTROL:** (lista numerada 1-5)
9. **SLA / TIEMPOS:** (lista con •)
10. **RESGUARDO:** (ruta de archivo)

---

## Datos variables por procedimiento

| Campo | Valor |
|-------|-------|
| CLAVE | Del archivo Excel (ej: PCA2, PCE1, PCC3). **Nunca inventar.** |
| FECHA | Fecha actual de creación: 26/05/2026 |
| DEPARTAMENTO | Cobranza (salvo que sea de otro dept) |
| REVISIÓN | 00 (siempre al inicio) |
| TÍTULO | Nombre oficial del procedimiento en el Excel (mismo en encabezado y cuerpo) |

---

## PASO A PASO — CORREGIDO (26/may/2026)

### Paso 1 — Copiar PCC2 como base

```python
import zipfile, shutil, os
from lxml import etree
from docx import Document

ref_path = "/home/elena/.openclaw/media/inbound/PCC2_PROCEDIMIENTO_TRATAMIENTO_DE_TARJETAS_DE_COBRO---1200a82e-0cde-4aa3-a31f-adf88b19d90d.docx"
out_path = "/home/elena/.openclaw/workspace/workspaces/instructivos/[CLAVE].docx"
tmp_path = out_path + ".tmp"

shutil.copy(ref_path, out_path)

# Leer TODOS los archivos del PCC2
with zipfile.ZipFile(ref_path, 'r') as z:
    all_files = {name: z.read(name) for name in z.namelist()}
```

### Paso 2 — Modificar SOLO la tabla de PROCEDIMIENTO en header2.xml

**NO modificar la fila de departamentos (FIRMA, DIRECCIÓN, etc.) — esos textos están embebidos en imágenes y deben quedar como están.**

Cambiar en header2.xml (solo estos tres elementos):
1. Título del procedimiento en la primera celda de la tabla PROCEDIMIENTO
2. La fecha (nota: la fecha está partida en dos runs XML: `: 31/08/202` + `5`)
3. La CLAVE (PCC2 → nueva CLAVE)

```python
h2 = all_files['word/header2.xml'].decode('utf-8')

# 1. Cambiar título del procedimiento
h2 = h2.replace('TRATAMIENTO DE TARJETAS DE COBRO', 'NOMBRE DEL NUEVO PROCEDIMIENTO')

# 2. Cambiar CLAVE
import re
h2 = re.sub(r'>PCC2<', '>PCE7<', h2)

# 3. Cambiar fecha (partida en dos runs)
# El patrón XML es: ": 31/08/202</w:t></w:r><w:r ...><w:t>5</w:t>"
h2 = h2.replace(': 31/08/202</w:t></w:r><w:r w:rsidR="00BF75E2"><w:t>5</w:t>',
                ': 26/05/2026</w:t>')
```

### Paso 3 — Reemplazar COMPLETAMENTE el body del document.xml

**ERROR COMÚN: No basta con cambiar solo el título. Hay que reemplazar TODO el contenido del cuerpo.**

```python
from docx.oxml.ns import qn

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NEW_TITLE = "NOMBRE DEL NUEVO PROCEDIMIENTO"

def make_para(text, bold=False):
    """Crear un párrafo con texto"""
    para = etree.Element(qn('w:p'))
    pPr = etree.SubElement(para, qn('w:pPr'))
    jc = etree.SubElement(pPr, qn('w:jc'))
    jc.set(qn('w:val'), 'both')
    if text:
        run = etree.SubElement(para, qn('w:r'))
        rPr = etree.SubElement(run, qn('w:rPr'))
        if bold:
            etree.SubElement(rPr, qn('w:b'))
            sz = etree.SubElement(rPr, qn('w:sz'))
            sz.set(qn('w:val'), '22')
            szCs = etree.SubElement(rPr, qn('w:szCs'))
            szCs.set(qn('w:val'), '22')
        t = etree.SubElement(run, qn('w:t'))
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        t.text = text
    return para

def make_body():
    """Construir el cuerpo completo del procedimiento"""
    body = etree.Element(qn('w:body'))
    
    # 1. Objetivo
    body.append(make_para("1. Objetivo", bold=True))
    body.append(make_para("[Texto del objetivo del nuevo procedimiento]"))
    body.append(make_para(""))
    
    # 2. Alcance
    body.append(make_para("2. Alcance", bold=True))
    body.append(make_para("[A quién aplica]"))
    body.append(make_para(""))
    
    # 3. Responsables
    body.append(make_para("3. Responsables", bold=True))
    body.append(make_para("• [Responsable 1]"))
    body.append(make_para("• [Responsable 2]"))
    body.append(make_para(""))
    
    # 4. Definiciones
    body.append(make_para("4. Definiciones", bold=True))
    body.append(make_para("• [Definición 1]"))
    body.append(make_para("• [Definición 2]"))
    body.append(make_para(""))
    
    # 5.- DESARROLLO
    body.append(make_para("5.- DESARROLLO", bold=True))
    body.append(make_para("5. Procedimiento", bold=True))
    
    # 5.1
    body.append(make_para("5.1 [NOMBRE DEL PASO]", bold=True))
    body.append(make_para("[Descripción del paso 1]"))
    body.append(make_para(""))
    
    # 5.2
    body.append(make_para("5.2 [NOMBRE DEL PASO]", bold=True))
    body.append(make_para("[Descripción del paso 2]"))
    body.append(make_para(""))
    
    # ... más pasos según sea necesario ...
    
    # REGLAS DE CONTROL
    body.append(make_para("REGLAS DE CONTROL:", bold=True))
    body.append(make_para("1) [Regla 1]"))
    body.append(make_para("2) [Regla 2]"))
    body.append(make_para("3) [Regla 3]"))
    body.append(make_para("4) [Regla 4]"))
    body.append(make_para("5) [Regla 5]"))
    body.append(make_para(""))
    
    # SLA / TIEMPOS
    body.append(make_para("SLA / TIEMPOS:", bold=True))
    body.append(make_para("• [Tiempo 1]"))
    body.append(make_para("• [Tiempo 2]"))
    body.append(make_para(""))
    
    # RESGUARDO
    body.append(make_para("RESGUARDO:", bold=True))
    body.append(make_para("• [Ruta de archivo o sistema]"))
    
    return body

# Obtener el document.xml base y reemplazar el body
base_doc = etree.fromstring(all_files['word/document.xml'])
body_el = base_doc.find(qn('w:body'))

# Quitar todos los hijos del body EXCEPTO el último (sectPr)
children = list(body_el)
for child in children[:-1]:
    body_el.remove(child)

# Guardar el sectPr (último elemento) para re-insertarlo
sect_pr = children[-1]

# Insertar el nuevo contenido del cuerpo
new_body = make_body()
for child in list(new_body):
    body_el.append(child)

# Re-insertar sectPr al final
body_el.append(sect_pr)

# Guardar el document.xml modificado
all_files['word/header2.xml'] = h2.encode('utf-8')
all_files['word/document.xml'] = etree.tostring(
    base_doc,
    xml_declaration=True,
    encoding='UTF-8',
    standalone=True
)
```

### Paso 4 — Escribir el archivo final

```python
with zipfile.ZipFile(tmp_path, 'w', zipfile.ZIP_DEFLATED) as zout:
    for fname, content in all_files.items():
        zout.writestr(fname, content)

os.replace(tmp_path, out_path)
```

### Paso 5 — Verificar

```python
from docx import Document
doc = Document(out_path)
print(f"Párrafos: {len(doc.paragraphs)}")
# Verificar que el contenido sea el correcto (no el de PCC2)
```

---

## Validaciones obligatorias ANTES de entregar

- [ ] La CLAVE en header2.xml es la correcta (ej: PCE7)
- [ ] La FECHA muestra 26/05/2026 (año completo, no truncado)
- [ ] El TÍTULO en header2.xml = TÍTULO en body (100% match)
- [ ] Los headers (header1, header2, header3) están vinculados en sectPr
- [ ] El CUERPO contiene el procedimiento NUEVO (no el de PCC2)
- [ ] El documento abre sin errores en Word/LibreOffice

---

## Ejemplo rápido: crear PCE7 (CONTROL DE PAGOS NO IDENTIFICADOS)

```python
# Datos
NEW_TITLE = "CONTROL DE PAGOS NO IDENTIFICADOS"
NEW_KEY = "PCE7"
NEW_DATE = "26/05/2026"

# Copiar base (Paso 1)
shutil.copy(ref_path, out_path)

# Leer archivos (Paso 1, continuación)
with zipfile.ZipFile(ref_path, 'r') as z:
    all_files = {name: z.read(name) for name in z.namelist()}

# Modificar header2.xml (Paso 2)
h2 = all_files['word/header2.xml'].decode('utf-8')
h2 = h2.replace('TRATAMIENTO DE TARJETAS DE COBRO', NEW_TITLE)
h2 = re.sub(r'>PCC2<', f'>{NEW_KEY}<', h2)
h2 = h2.replace(': 31/08/202</w:t></w:r><w:r w:rsidR="00BF75E2"><w:t>5</w:t>',
                ': 26/05/2026</w:t>')

# Reemplazar body COMPLETAMENTE (Paso 3)
# ... usar make_body() con el contenido específico de PCE7 ...

# Escribir (Paso 4)
with zipfile.ZipFile(tmp_path, 'w', zipfile.ZIP_DEFLATED) as zout:
    for fname, content in all_files.items():
        zout.writestr(fname, content)
os.replace(tmp_path, out_path)

# Verificar (Paso 5)
doc = Document(out_path)
assert len(doc.paragraphs) > 50, "Body parece vacío"
```

---

## Checklist de verificación final

- [ ] CLAVE correcta en header2.xml
- [ ] FECHA 26/05/2026 completa
- [ ] TÍTULO igual en encabezado y cuerpo (100%)
- [ ] Headers vinculados (header1, header2, header3)
- [ ] Body completo con contenido del nuevo procedimiento (NO copiar PCC2)
- [ ] Archivo abre sin errores
- [ ] Guardado en `workspaces/instructivos/[CLAVE].docx`
