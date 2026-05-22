# PROCEDIMIENTO DETALLADO PARA CONCILIACIÓN BANCARIA DE INGRESOS

## Objetivo
Conciliar los depósitos del banco con las facturas emitidas (ingresos) para verificar que todo cuadre y detectar diferencias.

---

## 📁 Archivos Necesarios

| Archivo | Fuente | Contenido |
|---------|--------|-----------|
| Movimientos Banco | Banca en Línea | Todos los depósitos y retiros del mes |
| Depósitos Banco | Viri y Nelly | Folios, clientes, facturas, montos |
| Facturas SAT | Portal SAT | Facturas timbradas en el mes |

---

## 🔄 Flujo de Datos

```
BANCO (Estado de Cuenta)
    ↓
    ├── Depósitos identificados (con folio de cliente) → Van a Viri+Nelly
    ├── Depósitos NO identificados (sin folio)        → "Sin cliente"
    └── Asociados Varios (RFC genérico XAXX)          → Pagos en efectivo
```

---

## 📊 Tipos de Depósitos

### 1. Depósitos Identificados
- Tienen **folio de asociado**
- Tienen **nombre de cliente**
- Están en el archivo de "Depósito Banco" (Viri+Nelly)
- Se les emite **factura con RFC del cliente**

### 2. Depósitos NO Identificados
- **NO tienen folio de asociado**
- No se sabe qué cliente realizó el pago
- No están en el archivo de Depósitos
- Ejemplo: "$7,748.00" sin cliente

### 3. Asociados Varios (RFC Genérico)
- Tienen **RFC genérico** = `XAXX010101000`
- Son pagos en efectivo sin cliente específico
- Se factura con nombre "ASOCIADOS VARIOS"
- La suma debe ser: `Total Banco - Depósitos identificados - No identificados`

---

## 📝 PASOS DETALLADOS

### Paso 1: OBTENER ARCHIVOS

**1.1 Estado de Cuenta (Banco)**
- Entrar a Banca en Línea BBVA
- Descargar estado de cuenta del mes
- Guardar como Excel

**1.2 Facturas del SAT**
- Entrar al portal SAT (sat.gob.mx)
- Descargar "Facturas Emitidas" del mes
- Guardar como PDF

**1.3 Archivo de Depósitos**
- Obtener de Viri y Nelly el archivo Excel
- Tiene 3 hojas: DEPOSITO1, DEPOSITO2, DEPOSITO3

---

### Paso 2: EXTRAER DATOS DEL BANCO

**2.1 Abrir archivo de Movimientos Banco**
- Hoja: "FEBRERO" (o mes correspondiente)

**2.2 Identificar columnas:**
- Columna A: # Movimiento
- Columna B: FECHA
- Columna C: BANCO
- Columna D: CLIENTE
- Columna G: DEPOSITOS
- Columna J: FOLIO ASOCIADO

**2.3 Sumar:**
- **Total Depósitos** = SUMA(columna DEPOSITOS)
- **Depósitos identificados** = Los que tienen FOLIO ASOCIADO
- **Sin folio** = Los que NO tienen FOLIO ASOCIADO

**2.4 Filtro en Excel:**
- Filtrar por "FOLIO ASOCIADO" vacío → Depósitos NO identificados
- Filtrar por "CLIENTE" = "ASOCIADOS VARIOS" → RFC genérico

---

### Paso 3: EXTRAER DATOS DE DEPÓSITOS (Viri + Nelly)

**3.1 Abrir archivo "Depósitos Banco"**

**3.2 Tiene 3 hojas:**
- DEPOSITO1
- DEPOSITO2
- DEPOSITO3

**3.3 Cada hoja tiene columnas:**
- Columna A: FOLIO
- Columna B: CONTRATANTE
- Columna C: MONTO
- Columna D: FACTURA
- Columna E: FECHA FACTURA

**3.4 Sumar:**
- Total Depósitos = SUMA de las 3 hojas (columna MONTO)

---

### Paso 4: EXTRAER FACTURAS DEL SAT

**4.1 Abrir PDF de facturas emitidas**

**4.2 Filtrar por tipo:**
- Buscar: "Efecto del Comprobante: Ingreso"
- **EXCLUIR:** "Efecto del Comprobante: Nómina" (son egresos)

**4.3 Sumar:**
- Total Facturas de Ingreso = suma de todos los "Total: $XXX"

---

### Paso 5: COMPARAR Y CONCILIAR

**5.1 Comparación 1: Desglose del Banco**

| Concepto | Fórmula | Ejemplo ($) |
|----------|---------|-------------|
| Total Banco | = SUMA(Depósitos) | 888,105.86 |
| Menos: Depósitos identificados | = Del archivo de Viri+Nelly | 285,658.74 |
| Menos: Depósitos NO identificados | = Sin folio | 7,748.00 |
| **= Asociados Varios** | = Resto | **594,699.12** |

**Fórmula:**
```
Asociados Varios = Total Banco - Depósitos identificados - NO identificados
```

**5.2 Comparación 2: Ingresos Reales**

| Concepto | Monto |
|----------|-------|
| Facturas de Ingreso (SAT) | 286,842.58 |
| Depósitos identificados | 285,658.74 |
| **Diferencia** | **1,183.84** |

La diferencia debe ser mínima (menos de $2,000).

---

## ✅ RESULTADO ESPERADO

```
Total Banco = $888,105.86
    ├── Depósitos identificados = $285,658.74
    ├── NO identificados = $7,748.00
    └── Asociados Varios = $594,699.12

Facturas Ingreso = $286,842.58
    └── Diferencia con depósitos identificados = $1,183.84 (mínima)
```

---

## ⚠️ Notas Importantes

1. **Nóminas = EGRESOS**, no ingresos. No incluir en conciliación de ingresos.
2. **RFC genérico = XAXX010101000** = "ASOCIADOS VARIOS"
3. Viri captura: Folio de Asociado, # Aportación, # Recibo
4. Nelly captura: # Factura y Fecha de Factura (solo ingresos)
5. Diferencia aceptable: menos de $2,000 (puede ser redondeo)

---

## 🚀 Para Automatizar (Fer y Claudy)

Este procedimiento se puede automatizar:
1. Importar archivos automáticamente
2. Filtrar por tipo de comprobante
3. Sumar columnas automáticante
4. Generar reporte de diferencias

---

*Documento creado: 9 de marzo de 2026*
*Para uso: Febrero 2026 y meses siguientes*
*Para automatizar en el nuevo sistema*
