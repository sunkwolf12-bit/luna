# Estadística Mensual de Cobranza 📊

Habilidad especializada para la extracción, procesamiento y consolidación de datos de cobranza provenientes de reportes mensuales (PPTX) hacia el archivo de estadística anual en Excel de Proteg-rt.

## 📋 Metodología General

### 1. Extracción de Datos
- **Fuente:** Presentaciones de PowerPoint (PPTX) mensuales proporcionadas por Elena.
- **Acción:** Identificar y extraer el **Total Mensual ($)** y los montos individuales para generar el **Top 5** de cada categoría/pestaña del Excel.

### 2. Criterios de Clasificación para Top 5

Dependiendo de la pestaña/apartado, el criterio para agrupar y determinar los 5 mejores varía:

| Pestaña / Apartado | Criterio de Agrupación (Top 5) | Nota Operativa |
| :--- | :--- | :--- |
| **Cobranza Corriente** | Vendedor (Número o Nombre) | |
| **Cancelaciones** | Vendedor (Número o Nombre) | |
| **Cobranza Vencida / Atrasada** | Ubicación_T / Ruta | |
| **Cobranza Efectiva** | **COBRADO** (Persona que cobró) | Aplicar Regla de Consolidación Bancaria |
| **Cobranza Recuperada** | **COBRADO** (Persona que cobró) | Aplicar Regla de Consolidación Bancaria |
| **Cobranza Adelantada F.** | **COBRADO** (Persona que cobró) | Aplicar Regla de Consolidación Bancaria |
| **Cobranza Total / Pagada** | **COBRADO** (Persona que cobró) | Aplicar Regla de Consolidación Bancaria |

### 3. Regla de Consolidación Bancaria (Importante)
Para los apartados basados en **COBRADO**, todos los registros de pagos no realizados en efectivo deben consolidarse en un solo concepto:
- **Etiquetas en fuente:** "TRANSFER_DEPOSITO", "DEPOSITO", "TRANSFERENCIA" (incluyendo variaciones de mayúsculas/minúsculas).
- **Etiqueta en Excel:** Debe mostrarse exactamente como **"TRANSFER. / DEPTOS."**
- **Acción:** Sumar todos estos montos para que compitan como una sola entidad dentro del Top 5.

### 4. Cálculos y Porcentajes
- **Total Mensual:** Sumar la columna de montos del apartado completo **sin filtrar por STATUS** (queremos el universo total del reporte).
- **Cálculo de %:** `(Monto individual del Top 5 / Total Mensual del apartado) * 100`.

## 🛠️ Flujo de Trabajo para el Asistente

1. **Recibir insumo:** Abrir y procesar la presentación PPTX del mes solicitado.
2. **Procesar cada diapositiva:**
   - Extraer el título exacto para asegurar que corresponde al apartado.
   - Extraer leyenda y montos (incluyendo desglose de "Otros" si es necesario para completar el Top 5).
3. **Aplicar filtros y agrupaciones:** Según la tabla del punto 2 y la regla de consolidación del punto 3.
4. **Validación cruzada:** Asegurar que la suma de los componentes coincida con el total reportado en la diapositiva.
5. **Carga en Excel:**
   - Localizar el archivo maestro (ej. `ESTADISTICA_PARA_JUNTA_MENSUAL_2024_...`).
   - Insertar datos en las columnas correspondientes al mes trabajado.
6. **Entrega:** Reportar a Elena los totales cargados y los integrantes del Top 5 para validación rápida.

## ⚠️ Restricciones
- **Honestidad Brutal:** Si un monto en el PPTX no es legible o parece incoherente, no adivinar. Pedir aclaración a Elena.
- **Privacidad:** No persistir nombres completos de clientes ni folios en archivos de memoria larga; solo nombres de vendedores/cobradores y montos totales.
