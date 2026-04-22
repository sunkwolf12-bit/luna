# Nota Técnica para el Módulo de Cobranza (Luna 🌙 para su compañera IA)

**OBJETIVO PRINCIPAL:** Desarrollar un módulo integral que permita **prescindir por completo del sistema SIGA**, centralizando toda la inteligencia de datos y reglas de negocio en esta nueva plataforma.

Para el diseño del nuevo módulo de cobranza de Proteg-rt, se deben considerar los siguientes requerimientos críticos basados en la operación real de Elena:

1. **Migración e Integración de Datos (Reemplazo de SIGA):**
    * El sistema debe absorber toda la base de datos de clientes y cobranza que actualmente reside en SIGA (SaaS/CRM externo).
    * Debe incluir la captura y almacenamiento de documentos que SIGA maneja actualmente y que el Legacy no tiene: **INE, Tarjetas de Circulación y Datos Fiscales**.
    * El objetivo es eliminar el sobreproceso de consultar un sistema externo pagado anualmente.
    * Debe incluir la validación de Cédulas Fiscales y reglas de facturación automáticas.

2. **Conciliación Multifuente:** El sistema debe cruzar automáticamente datos de tres fuentes:
    * **Facturación (CONTPAQ):** Facturas vigentes del mes.
    * **Control Interno (Efectivo):** Detalle individual de cobros recibidos físicamente que aún no entran al banco.
    * **Bancos:** Depósitos individuales y depósitos globales.

3. **Identificación de Depósitos Globales:** El sistema debe ser capaz de "desglosar" un depósito bancario único (ej. $95,000) asociándolo a múltiples facturas individuales del reporte de efectivo para evitar duplicidades o falsos pendientes.

4. **Algoritmo de Cruce Flexible:**
    * Separación de folios múltiples en una sola celda (ej. "47772/47773").
    * Búsqueda por **Monto Exacto + Folio** como prioridad.
    * Búsqueda por **Monto Exacto + Nombre de Cliente** como respaldo cuando el folio no coincida.

5. **Gestión de Excepciones:** Marcar automáticamente:
    * Diferencias de centavos (ajustes).
    * Ingresos que no generan factura (ej. Venta de fondos de inversión).
    * Cobros sin factura detectada (posibles facturas de meses anteriores).

6. **Visualización Prioritaria:** El reporte final debe destacar las **Facturas Pendientes REALES**, ordenadas por antigüedad y con el Folio de Cliente visible para rápida localización.
