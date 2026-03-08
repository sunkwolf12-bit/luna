# Conocimiento de Negocio — Proteg-rt
_Recopilado por Luna 🌙 trabajando con Elena_
_Última actualización: 25 de febrero de 2026_

Este documento centraliza las reglas de negocio, excepciones y procesos que Elena maneja de forma cotidiana y que deben ser considerados para el desarrollo del nuevo sistema.

## 1. Cobranza y Facturación
*   **Volumen:** Se procesan entre 500 y 600 facturas mensuales.
*   **Conciliación Bancaria:** Se requiere cruzar CONTPAQ, Control de Efectivo y Estados de Cuenta Bancarios.
*   **Depósitos Globales:** Existen depósitos acumulados (ej. "Asociados Varios" por $95,000 aprox.) que representan la suma de múltiples pagos individuales detallados en el archivo de Efectivo.
*   **Folios Múltiples:** En el banco, los folios pueden capturarse agrupados (ej. "47772/47773"), lo que requiere lógica de separación para el cruce.
*   **Identificación por Monto:** Si el folio no coincide, se utiliza el **Monto Exacto + Razón Social** como criterio de respaldo.
*   **Venta de Fondos:** Los movimientos con concepto "VTA. FONDOS DE INV." en bancos son internos y **no deben facturarse**.

## 2. Clientes y Pólizas
*   **Sustitución de SIGA:** El nuevo sistema debe almacenar INE, Tarjetas de Circulación y Datos Fiscales que actualmente solo residen en SIGA.
*   **Relación Factura-Póliza:** El Folio de Factura en CONTPAQ está vinculado directamente al Folio de Cliente/Póliza en el sistema Legacy.

## 3. Procesos Diarios y Herramientas
*   **Herramientas Actuales:** CONTPAQ (Facturación), SIGA (CRM Externo), Excel (Bancos y Efectivo), Legacy (Interno).
*   **Corte de Caja:** Elena realiza cortes de caja diarios que deben reflejar tanto el flujo de efectivo físico como los depósitos bancarios.

## 4. Datos Fiscales (Reglas SAT)
*   **RFC Genérico:** Se utiliza cuando el cliente no proporciona datos fiscales.
*   **Parámetros por Defecto:** Régimen 616 (Sin obligaciones fiscales) y Uso CFDI S01 (Sin efectos fiscales).
*   **IVA:** El servicio principal de la mutualidad **no causa IVA**.

## 5. Excepciones y Casos Especiales
*   **Pagos en Efectivo no Depositados:** Existen pagos registrados en el "Control de Efectivo" que pueden tardar días en aparecer en el Banco (ej. "Depósito 3" pendiente de traslado físico).
*   **Pagos de Meses Anteriores:** Si un folio en el banco no aparece en el reporte de facturas del mes actual, probablemente sea una factura de un periodo anterior.
*   **Diferencias de Monto:** Se permiten pequeñas variaciones (centavos) entre lo facturado y lo cobrado por redondeos o ajustes.
