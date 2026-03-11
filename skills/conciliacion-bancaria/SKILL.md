---
name: conciliacion-bancaria
description: |
  Procedimientos completos para conciliación bancaria en Proteg-rt: (1) Ingresos - comparar depósitos del banco con facturas emitidas y depósitos identificados, (2) Egresos - conciliar retiros del banco con facturas de proveedores, (3) Caja Chica - identificar facturas menores a $2,320 pagadas en efectivo. Usar cuando Elena solicite hacer conciliación bancaria mensual.
---

# Conciliación Bancaria - Proteg-rt

## Archivos Requeridos

| Para qué sirve | Archivo |
|----------------|---------|
| Ingresos | Estado de cuenta bancario (PDF) |
| Ingresos | Excel de movimientos del mes |
| Ingresos | Facturas que Nosotros emitimos (PDF SAT) - las que Proteg-rt emite a clientes |
| Ingresos | Depósitos identificados (Excel con 3 hojas) |
| Egresos | Excel de movimientos del mes |
| Egresos | Facturas que nos EMITEN (PDF SAT) - las que los proveedores nos emiten |
| Caja Chica | Facturas que nos EMITEN (PDF SAT) |

---

## Proceso 1: Conciliación de INGRESOS

### Pasos

1. **Del Excel de movimientos:** Extraer total de depósitos del banco

2. **Del Excel de depósitos identificados (3 hojas):** 
   - Sumar todos los depósitos de las 3 hojas (DEPOSITO1, DEPOSITO2, DEPOSITO3)
   - Columnas: FOLIO, CONTRATANTE, MONTO, FACTURA, FECHA FACTURA

3. **Calcular depósitos NO identificados:**
   - No identificados = Total banco - Depósitos identificados

4. **Del PDF de facturas emitidas (SAT):**
   - Buscar facturas donde RFC Emisor = PMU180521MD8
   - Excluir nóminas
   - Sumar total de facturas

5. **Comparar:**
   - Depósitos identificados vs Facturas emitidas
   - Mostrar diferencia

### Fórmulas
- Total Banco = Depósitos identificados + No identificados
- Diferencia = Depósitos identificados - Facturas emitidas

---

## Proceso 2: Conciliación de EGRESOS

### Pasos

1. **Comparar hojas del Excel:**
   - Hoja "CONCENTRADO GRAL." vs Hoja del mes (ENERO/FEBRERO)
   - Comparar: # Movimiento, Monto

2. **Identificar diferencias:**
   - Movimientos que solo están en Concentrado
   - Movimientos que solo están en la hoja del mes
   - Diferencias en montos

3. **Identificar facturas pendientes:**
   - Revisar columna #FACTURA
   - Marcar las que digan "PENDIENTE"

4. **Buscar facturas en SAT:**
   - Comparar egresos pendientes con PDF de facturas de proveedores
   - Verificar si ya fueron emitidas

### Totales a verificar
- Total Concentrado = Total Hoja del mes
- Diferencia debe ser $0.00

---

## Proceso 3: Caja Chica

### Criterios
- Factura menor o igual a $2,320 ($2,000 + IVA)
- **NO** aparece en los egresos del banco (ya pagada por transferencia)
- **Excluir:** Hospital Felman y J. Maurilio García Vargas

### Pasos

1. Extraer todas las facturas del PDF del SAT (facturas de proveedores)
2. Filtrar las menores o iguales a $2,320
3. Excluir las que ya están en egresos del banco (comparar por monto exacto)
4. Excluir Hospital Felman y J. Maurilio García Vargas
5. Generar archivo Excel con: Fecha, Proveedor, Monto
6. Enviar archivo a Elena por Telegram

---

## RFC de la Empresa
- RFC: PMU180521MD8
- Razón Social: PROTEG-RT MUTUALIDAD

## Proveedores Comunes (para egresos)

| RFC | Nombre |
|-----|--------|
| GIE9802034T2 | GRUAS IBARRA EXXEL |
| GAVJ510124IP6 | J. MAURILIO GARCIA VARGAS |
| HFE9608302X9 | HOSPITAL FELMAN |
| ABS841019IK9 | START BANREGIO |
| TFS011012M18 | TOYOTA FINANCIAL SERVICES |
