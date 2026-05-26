# SKILL.md — Skill para Procedimientos

## Objetivo
Crear documentos de procedimientos operativos para Proteg-rt usando como plantilla el documento de referencia PCC2 (`PCC2_PROCEDIMIENTO_TRATAMIENTO_DE_TARJETAS_DE_COBRO.docx`).

---

## REGLA DE ORO (del mensaje de Elena 26/may/2026)
**El nombre del procedimiento en el ENCABEZADO y en el CUERPO del documento debe coincidir EXACTAMENTE al 100%.**

---

## Archivos de referencia

| Archivo | Uso |
|---------|-----|
| `PCC2_PROCEDIMIENTO_TRATAMIENTO_DE_TARJETAS_DE_COBRO---1200a82e-0cde-4aa3-a31f-adf88b19d90d.docx` | Plantilla de formato para TODOS los procedimientos nuevos. Usar este como base para copiar encabezados y estructura. |
| Carpeta: `workspaces/instructivos/` | Carpeta donde guardar los procedimientos generados. |

---

## Formato del documento (estructura fija)

### ENCABEZADOS (3 headers)

**header1.xml** — Primera línea: `PROTEG-RT MUTUALIDAD`
**header2.xml** — Tabla con:
- Primera fila: `FIRMA` | `DIRECCIÓN` | `DEPT. ADMINISTRATIVO` | `DEPT. COBRANZA` | `DEPT. VENTAS` | `DEPT. JURÍDICO`
- Segunda fila: campos editables en celdas
- Tercera fila: `PROCEDIMIENTO [NOMBRE]` | `FECHA: DD/MM/AAAA` | `CLAVE: PAx` | `REVISIÓN: 00` | `DEPARTAMENTO: Cobranza`

**header3.xml** — Logo/corporativo (mantener igual que PCC2)

### CUERPO (body)

Estructura obligatoria por orden:
1. **1. Objetivo** — Texto del objetivo del procedimiento
2. **2. Alcance** — A quién aplica
3. **3. Responsables** — Lista con • (bullets)
4. **4. Definiciones** — Lista con • (bullets)
5. **5.- DESARROLLO** — Subtítulo en negrita
6. **5. Procedimiento** — Subtítulo en negrita
7. **5.1** hasta **5.6** — Pasos numerados en negrita con descripción
8. **REGLAS DE CONTROL:** — Lista numerada
9. **SLA / TIEMPOS:** — Lista con •
10. **RESGUARDO:** — Lista con • (ruta de archivo)

---

## Datos variables por procedimiento

| Campo | Valor |
|-------|-------|
| CLAVE | PAC1, PAC2, PAC3... (incrementar) |
| FECHA | Fecha actual de creación: 26/05/2026 |
| DEPARTAMENTO | Cobranza (salvo que sea de otro dept) |
| REVISIÓN | 00 (siempre al inicio) |
| TÍTULO | Nombre del procedimiento (mismo en encabezado y cuerpo) |

---

## PASOS PARA CREAR UN PROCEDIMIENTO

### Paso 1 — Abrir documento referencia
Usar `zipfile` para leer el PCC2 y copiar sus headers:
```python
with zipfile.ZipFile(ref_path, 'r') as z:
    xml_map = {name: z.read(name) for name in z.namelist()}
```
Copiar header1.xml, header2.xml, header3.xml al nuevo documento.

### Paso 2 — Modificar header2.xml
Cambiar SOLO estos textos (mantener estructura de tabla):
- `TRATAMIENTO DE TARJETAS DE COBRO` → Nombre nuevo del procedimiento
- `PCC2` → CLAVE del nuevo procedimiento (ej: `PAC3`)
- `31/08/2025` → `26/05/2026` (fecha actual)
- `REVISION: 00` → dejar como 00

### Paso 3 — Crear document.xml del nuevo procedimiento
Copiar la estructura del `<w:body>` del PCC2 y modificar:
1. Cambiar el título del cuerpo (`TRATAMIENTO DE TARJETAS DE COBRO`) por el nombre nuevo (DEBE coincidir exactamente con el encabezado)
2. Escribir el contenido específico de cada sección (Objetivo, Alcance, etc.)

### Paso 4 — Crear sectPr con headerReference
El `<w:sectPr>` debe incluir:
```xml
<w:headerReference w:type="even" r:id="rId9"/>
<w:headerReference w:type="default" r:id="rId10"/>
<w:footerReference w:type="default" r:id="rId11"/>
<w:headerReference w:type="first" r:id="rId12"/>
```
Sin esto, los encabezados NO aparecen.

### Paso 5 — Guardar y verificar
Guardar como `.docx` en `workspaces/instructivos/PACx.docx`.

**Validaciones obligatorias antes de entregar:**
1. El nombre en encabezado = nombre en cuerpo (100% match)
2. Todos los headers (header1, header2, header3) están vinculados
3. La fecha muestra `DD/MM/2026` (año completo, no truncado)
4. El documento abre sin errores en Word

---

## Ejemplo: PAC3 (Aplicación de Saldos a Favor)

| Campo | Valor |
|-------|-------|
| CLAVE | PAC3 |
| FECHA | 26/05/2026 |
| TÍTULO | APLICACIÓN DE SALDOS A FAVOR |
| Ubicación | `workspaces/instructivos/PAC3.docx` |

### Contenido del cuerpo para PAC3:
- **1. Objetivo:** Establecer el proceso para identificar, validar y aplicar saldos a favor de clientes a sus próximas aportaciones, evitando pagos duplicados y garantizando el uso correcto de los recursos del cliente.
- **2. Alcance:** Aplica a todo el personal de Cobranza, Ventas y Administrativo que gestione saldos a favor provenientes de cancelaciones, ajustes, endosos o pagos en exceso.
- **3. Responsables:** Asistente de Cobranza, Vendedor, Cobrador, Gerencia de Cobranza.
- **4. Definiciones:** Saldo a favor, Aplicación de saldo, Cancelación, Endoso.
- **5.1 IDENTIFICACIÓN:** Revisar en CRM PROTEG-RT, identificar si existe saldo por pago en exceso/cancelación/endoso/ajuste. Si es mayor a $500, documentar y notificar a Gerencia.
- **5.2 VALIDACIÓN:** Verificar origen del saldo, confirmar que no exista proceso de devolución en curso. No aplicar sin evidencia y autorización si excede $500.
- **5.3 AUTORIZACIÓN:** Si saldo > $500, requerir autorización escrita de Gerencia. Documentar: fecha, monto, origen, cliente, vendedor/cobrador, decisión.
- **5.4 APLICACIÓN EN SISTEMA:** Aplicar saldo a favor a próxima aportación en CRM PROTEG-RT. Registrar: fecha, monto aplicado, остаток pendiente (si hay). No inventar datos.
- **5.5 NOTIFICACIÓN AL CLIENTE:** Comunicar al cliente la aplicación (monto y fecha). Si solicita devolución en efectivo, escalar a Gerencia.
- **5.6 CONFIRMACIÓN Y CIERRE:** Actualizar registro, archivar evidencia. Si queda остаток pendiente, informar nueva fecha de vencimiento.
- **REGLAS DE CONTROL:** 5 reglas sobre verificación, autorización, devolución, registro y liberación de saldos.
- **SLA/TIEMPOS:** Mismo día para identificación/validación; 24h para autorización; 48h para aplicación.
- **RESGUARDO:** `D:\COBRANZA\COBRANZA\COBRANZA (COBRADORES) 2026\SaldosAFavor`

---

## Checklist de verificación

- [ ] CLAVE actualizada en header2.xml
- [ ] FECHA correcta (DD/MM/2026) en header2.xml
- [ ] TÍTULO en header2.xml = TÍTULO en body (100% match)
- [ ] Todos los headers vinculados en sectPr
- [ ] Contenido completo en todas las secciones
- [ ] Documento guarda sin errores de XML
- [ ] Documento abre en Word/LibreOffice sin warnings