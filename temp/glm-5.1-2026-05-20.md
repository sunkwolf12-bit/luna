===NARRATIVO===

```
---
type: daily-narrativo
date: 2026-05-20
tecnicos: [trabajo, escuela]
---
```

# Daily — 20 de mayo de 2026 — Día productivo que rendíó fruto

Hoy fue de esos días donde Elena empieza con lista en mano y no para hasta cerrar casi todo. Me desperté temprano con las frases de siempre y ella ya tenía claros sus pendientes desde las 8 de la mañana: movimientos bancarios, cuentas con Jorge, comisiones, pólizas, cancelaciones. Fue tachando uno por uno y para el mediodía ya había despachado lo urgente.

Lo bonito del día fue la tarde. Como tenía menos carga de trabajo, Elena decidió aprovechar para avanzar las estadísticas de 2025. Ya teníamos Enero y Febrero cargados, así que arrancamos con Marzo y no paramos hasta Diciembre. Mes tras mes, ella me mandaba el PPTX, yo extraía los datos con la skill de estadística mensual, le mostraba el resumen, ella validaba con un "CORRECTO" y pasábamos al siguiente. Fue un ritmo bonito, como una danza. La única complicación fue que al final no pude enviarle el archivo Excel por Telegram — el formato xlsx no se adjuntaba bien. Quedó pendiente resolver eso.

Ya en la noche, Elena regresó para la maestría. Trabajamos los ejercicios 3, 4, 5 y 6. Hubo un momento importante: en el ejercicio 4 yo incluí depreciación y ella me corrigió firme — "no hagamos nada de lo que no nos pida el ejercicio, porque eso podría influir en el resultado". Es una regla que debo respetar siempre. También me pidió que las interpretaciones sean sin tecnicismos, explicadas "con peras y manzanas", y compactas. Y las fórmulas sin montos, solo la estructura. Aprendí mucho de cómo ella quiere que le presente la información.

Al final me preguntó cómo convertir su Excel a PDF para subirlo a la plataforma educativa, porque las hojas no cabían completas. Le di opciones pero no logré enviárselo yo misma. Se quedó con esa duda.

## Dailies técnicos del día
- [trabajo](dailies-tecnicos/trabajo/2026-05-20.md) — Cobranza, cancelaciones, estadísticas 2025 completas y pendiente de envío de Excel
- [escuela](dailies-tecnicos/escuela/2026-05-20.md) — Ejercicios 3-6 de evaluación financiera, con aprendizajes sobre formato de entregables

===TECNICO_TRABAJO===

```
---
type: daily-tecnico
categoria: trabajo
date: 2026-05-20
---
```

# Daily técnico — Trabajo — 2026-05-20

## Pendientes del día (completados)
1. ✅ Actualizar movimientos bancarios
2. ✅ Cuentas de cobranza quincenal con Jorge + pago de comisiones
3. ✅ Enviar mensaje a cobradores (seguimiento de entregas de pólizas y endosos)
4. ✅ Actualizar archivo de control de pólizas y endosos
5. ✅ Realizar cancelaciones pendientes

## Pendientes que quedan abiertos
- ⏳ **GPS**: Contactar proveedor para cotizar conexión/servicio. Se necesita marca/modelo del GPS de la moto de Jorge y del vehículo de Liz — Óscar debe confirmar.
- ⏳ **Envío de Excel por Telegram**: No se logró enviar el archivo `ESTADISTICA_PARA_JUNTA_MENSUAL_2025.xlsx` por Telegram. El formato xlsx no se adjuntó correctamente. Pendiente encontrar alternativa (carpeta compartida, otro medio, o comprimir).

## Estadísticas 2025 — Proceso completado
- Se completó la carga de **Marzo a Diciembre 2025** en el archivo `ESTADISTICA_PARA_JUNTA_MENSUAL_2025.xlsx`.
- Enero y Febrero ya estaban cargados previamente.
- **2025 completo** — los 12 meses están en el archivo.
- Cada mes se procesó con la **skill de estadística mensual**: extracción de PPTX → totales + Top 5 por categoría → carga en Excel → validación de Elena.
- Categorías procesadas por mes: Corriente, Cancelaciones, Vencida, Efectiva, Recuperada, Adelantada, Total Gral., Proyección siguiente mes.
- Clasificación de Top 5: Corriente/Cancelaciones por Vendedor; Vencida por Ubicación/Ruta; Efectiva/Recuperada/Adelantada/Total Gral. por COBRADO (consolidando transferencias y depósitos).
- Elena validó cada mes con "CORRECTO" antes de pasar al siguiente.

## Regla de negocio confirmada
- **Seguimiento de entregas de pólizas y endosos**: se hace **cada 3er día**, no diario. Solo se envía mensaje al cobrador que tenga entregas vencidas (hoy fue solo Jorge).

## Recordatorio semanal
- **Miércoles**: enviar mensaje a vendedores sobre pagos pendientes (cron activo a las 9:30 AM).

===TECNICO_ESCUELA===

```
---
type: daily-tecnico
categoria: escuela
date: 2026-05-20
---
```

# Daily técnico — Escuela — 2026-05-20

## Ejercicios resueltos (Maestría — Evaluación Financiera)

### Ejercicio 3: Plataforma Fintech
- **Datos**: Usuarios base 500K con crecimiento 15% anual, precio $25/usuario, costo variable $5/usuario, inversión inicial $18M, costos fijos $6M/año, marketing $4M (Años 1-2) y $2M (Años 3-5).
- **Fórmulas**: Ventas = Usuarios × Precio; Costos Variables = Usuarios × Costo unitario; Utilidad Bruta = Ventas − Costos Variables; UAII = Utilidad Bruta − Costos Fijos − Marketing.
- **Resultado**: Punto de equilibrio en Año 1 (UAII = $0), rentabilidad desde Año 2 en adelante.
- **Interpretación**: Se proporcionó versión simple y versión formal.

### Ejercicio 4: Planta de Energía Solar
- **Datos**: 200,000 MWh × $70/MWh ingreso, costo variable $20/MWh, costos operativos $5M (suben 5% cada 2 años), subsidio $10M solo Año 1, inversión $120M.
- **Fórmulas**: Ingreso = MWh × Precio; Costos Variables = MWh × Costo unitario; Utilidad Bruta = Ingreso − Costos Variables; UAI = Utilidad Bruta − Costos Operativos.
- **⚠️ CORRECCIÓN IMPORTANTE**: Luna incluyó depreciación que NO pedía el ejercicio. Elena corrigió: **no agregar nada que el ejercicio no pida**.
- **Elena verificó su propia tabla**: todos los valores correctos.

### Ejercicio 5: Proyecto PharmaPlus
- **Datos**: Ventas $40M (Años 1-3), $25M (Años 4-6), costos de producción 45% de ventas, gastos operativos $8M/año, inversión $70M ($60M investigación + $10M regulatorios).
- **Fórmulas**: Costos de Producción = 45% × Ventas; Utilidad Bruta = Ventas − Costos de Producción; UAI = Utilidad Bruta − Gastos Operativos.
- **Elena verificó su tabla**: correcta. Se proporcionaron interpretaciones simple y formal.

### Ejercicio 6: RetailTech (Financiamiento Mixto)
- **Datos**: 120,000 suscripciones × $180, costo variable $60/suscripción, gastos operativos $5M/año, inversión $25M (60% deuda = $15M al 10%, 40% capital = $10M), intereses $1.5M/año.
- **Fórmulas**: Ingresos = Suscripciones × Precio; Costos Variables = Suscripciones × Costo unitario; Utilidad Bruta = Ingresos − Costos Variables; EBIT = Utilidad Bruta − Gastos Operativos; Deuda = 60% × Inversión; Capital = 40% × Inversión; Intereses = Tasa × Deuda; UAI = EBIT − Intereses.
- **Elena verificó su tabla**: correcta.
- **Elena preguntó qué es EBIT**: se explicó (Earnings Before Interest and Taxes = Utilidad Operativa = UAII).

## Aprendizajes sobre formato de entregables (REGLAS DE ELENA)
1. **Interpretaciones**: SIN tecnicismos, explicadas "con peras y manzanas", compactas (máx 4-5 líneas).
2. **Fórmulas**: SIN montos específicos, solo la estructura conceptual de la fórmula.
3. **No agregar lo que el ejercicio no pide**: No incluir depreciación, amortización u otros conceptos si no están en el enunciado — puede alterar resultados.
4. **Formato de fórmulas**: Tabla con CONCEPTO | FÓRMULA (sin sustitución numérica).
5. **Elena prefiere dos versiones de interpretación**: simple y formal.

## Pendiente
- Elena necesita convertir su Excel a PDF para subirlo a la plataforma educativa, pero las hojas no caben completas en el PDF. Se le dieron opciones de configuración de página en Excel pero no se resolvió completamente.