---
name: revision-cobranza-quincenal
description: "Revisión y conciliación de cobranza quincenal con cobradores (Proteg-rt). Cargar esta skill cuando Elena diga frases como: 'vamos a hacer revision de cobranza quincenal', 'revisión de cobranza quincenal', 'cuadrar cobranza quincenal', 'comparar relación vs sistema', o cuando envíe Excel del sistema + fotos/relación del cobrador. Pasos: filtrar ENTREGADO, excluir pagos de $125 (endosos), sacar totales por día, comparar por día, identificar folios que explican diferencias, clasificar en desfases de fecha vs diferencias reales (transferencias reflejadas después/pagos adelantados/folios faltantes) y entregar resumen final para explicar a cobrador/Control. Regla: si un folio/monto no se ve claro en foto, detenerse y preguntar a Elena." 
---

# Revisión de cobranza quincenal (Proteg-rt)

## Objetivo
Cuadrar la cobranza de una quincena comparando:
- **Sistema (Excel)**: registros **ENTREGADO**
- **Relación del cobrador**: fotos/relación por día (folios y montos)

El cierre correcto separa:
1) **Desfases de fecha** (sí está en ambos, solo en distinto día)
2) **Diferencias reales** (falta en sistema en el corte, o se refleja después)

## Reglas no negociables
- **Excluir pagos de $125** del total (endosos) al comparar.
- Si un folio o monto **no se ve claro** en una foto, **detenerse y preguntar a Elena** antes de concluir.
- No “inventar” folios, montos, ni lecturas dudosas.

## Entradas mínimas
1) Excel del sistema del cobrador (típicamente hoja **Cobranza**).
2) Relación del cobrador (fotos claras por día o una lista de folios/montos).
3) Confirmación de Elena si hay:
   - Transferencias reflejadas días después
   - Pagos adelantados
   - Correcciones ya hechas en sistema

## Flujo (paso a paso)

### Paso 1) Preparar “Sistema” (Excel)
1. Filtrar solo **ENTREGADO**.
2. **Excluir $125**.
3. Calcular:
   - **Total sistema (ENTREGADO, sin $125)**
   - **Totales por día**

**Automatización (opcional):** ejecutar `scripts/resumen_sistema.py` para sacar totales por día y folios por fecha.

### Paso 2) Preparar “Relación del cobrador”
1. Por cada día, obtener el **total del día**.
2. Si la relación incluye $125, **restarlos** para que coincida con el criterio del sistema.
3. Guardar también (si se puede) los **folios por día**.

> Si la relación viene en fotos y no se leen folios/montos con claridad: pedir a Elena una foto más nítida o confirmación puntual.

### Paso 3) Comparación base por día
Construir tabla:
- **Día | Relación sin $125 | Sistema sin $125 | Diferencia (Relación – Sistema)**

Interpretación:
- Diferencia = 0 → OK
- Diferencia ≠ 0 → bajar a detalle (Paso 4)

### Paso 4) Bajar a detalle SOLO en los días con diferencia
Para cada día con diferencia:
1. Listar folios del sistema de ese día (con monto) y folios de la relación de ese día.
2. Detectar qué folio(s) explican la diferencia y clasificar en:

#### Caso A) Desfase de fecha (cuadra, no es faltante)
Se identifica cuando:
- Un día sale **+X** y otro día sale **-X** (mismo monto)
- Y el/los folio(s) existen en ambos, solo cambiados de fecha

**Acción:** documentar como “desfase de fecha” con:
- folio, monto, día en relación, día en sistema

#### Caso B) Diferencia real
Ejemplos típicos:
- Transferencia reportada en la relación un día, pero **reflejada en sistema días después**
- Pago adelantado que aparece en relación pero **no aparece en sistema**
- Folio que no está en el Excel (ni en días cercanos)

**Acción:** documentar como “diferencia real” con motivo.

#### Caso C) Ajuste/corrección ya realizada
Si Elena confirma que un folio ya fue capturado o corregido en sistema:
- Cambiar estatus a “corregido” y no contarlo como diferencia real.

### Paso 5) Cierre matemático (validación final)
1. Sumar **diferencias reales**.
2. Validar consistencia:

**Total relación (sin $125) − Diferencias reales = Total sistema (ENTREGADO, sin $125)**

Si no cuadra:
- Revisar que $125 estén excluidos en ambos
- Revisar si hay más transferencias reflejadas posterior al corte
- Pedir confirmación de folios dudosos

### Paso 6) Entregable para revisar con el cobrador / Control
Entregar 2 listas:

**A) Desfases de fecha (sí está en ambos):**
- Folio | Monto | Día relación | Día sistema | Nota

**B) Diferencias reales:**
- Folio | Monto | Día relación | Cuándo se reflejó (si aplica) | Motivo

Y un mini-resumen:
- Total relación (sin $125)
- Total sistema (sin $125)
- Total diferencia real

## Plantilla
- `references/plantilla_diferencias.csv`: formato para capturar folios/montos y motivos.

## Script incluido (opcional)
### `scripts/resumen_sistema.py`
Genera:
- Totales por día (ENTREGADO)
- Folios por día
- Lista de pagos $125 detectados (para exclusión)

Uso (ejemplo):
```bash
python3 skills/revision-cobranza-quincenal/scripts/resumen_sistema.py \
  --excel /ruta/al/archivo.xlsx \
  --sheet Cobranza \
  --header-row 4 \
  --entregado-col "ENTREGADO EN OFICINA" \
  --entregado-value "ENTREGADO" \
  --exclude-125
```
