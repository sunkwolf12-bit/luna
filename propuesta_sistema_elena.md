# Propuesta de Optimización: Módulo de Gestión de Cobranza Quincenal

**Objetivo:** Automatizar el cuadre de cuentas de cobradores y la gestión de comisiones para eliminar revisiones manuales y errores de captura.

## 0. Unificación de Procesos Bancarios (Fusión de Archivos)
Antes de las comisiones, es vital integrar el flujo de dinero para evitar duplicidad de trabajo:
- **Fusión de Archivos:** Integrar en un solo módulo el registro de **Depósitos Diarios**, la **Facturación de Bancos** (lo que hace Nelly) y la **Conciliación Bancaria**.
- **Conciliación Automática:** El sistema debe cruzar automáticamente el estado de cuenta bancario contra los depósitos registrados internamente para detectar diferencias de inmediato.

## 1. Reglas de Negocio para Cálculo de Comisiones
El sistema debe filtrar automáticamente qué folios NO generan comisión para el cobrador:
- **Pagos sin gestión de campo:** Pagos realizados por transferencia, depósito o directamente en oficina antes de la labor del cobrador.
- **Entregas de Póliza:** Folios donde solo se entrega el documento pero no hay ingreso de dinero real.
- **Coberturas "AMPLIAS":** Por política de la empresa, estos pagos no generan comisión de cobranza.
- **Endosos:** Pagos por montos de $125. Estos tienen un pago fijo por entrega de $50 pesos y no deben sumarse al total de cobranza general.

## 2. Control de Tiempos de Entrega (Servicio al Cliente)
Para garantizar que los documentos lleguen a tiempo, el sistema debe validar que las pólizas y endosos se entreguen en un plazo de **3 a 5 días hábiles**:
- **Fecha de Salida:** Registro de cuándo se le entrega el documento al cobrador.
- **Fecha de Entrega Real:** Registro de cuándo el cliente recibe el documento.
- El sistema debe alertar si se excede este plazo para mantener la calidad en la atención.

## 3. Automatización de Descuentos y Reembolsos
Integrar los siguientes rubros que actualmente se calculan de forma manual o externa:
- **Consumo de Gasolina:** Integrar el reporte quincenal de la gasolinera (actualmente enviado por Violeta) para que el sistema calcule automáticamente el 50% de aportación de la empresa.
- **Reembolsos de Gasolina en Efectivo:** Espacio para capturar facturas a nombre de la empresa y aplicar el 50% de reembolso.
- **Préstamos de Moto:** Aplicar el descuento quincenal programado a cada cobrador.

## 3. Optimización del Proceso de Revisión (Cuadre)
- **Carga de Datos:** Permitir la carga de fotos o reportes de los concentrados manuales de los cobradores para comparar contra el sistema.
- **Detección de Discrepancias:** El sistema debe señalar automáticamente diferencias en montos (ej. Edgar reporta $700 pero sistema marca $749) o folios inexistentes.

## 4. Gestión de Vendedores (Aviso de Atrasos)
- **Notificaciones Automáticas:** Envío programado de mensajes por Telegram/WhatsApp a vendedores con su lista de cobranza atrasada.
- **Límites de Asignación:** Bloqueo automático de nuevas asignaciones a vendedores que excedan su límite de cobranza atrasada o el 10% de sus ventas mensuales.
- **Bitácora de Seguimiento:** Registro de fecha de notificación, retroalimentación del vendedor y fecha compromiso de pago del cliente.
