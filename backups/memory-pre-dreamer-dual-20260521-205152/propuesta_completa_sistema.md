# Propuesta Completa de Optimización de Sistema - Elena (Proteg-rt)
Fecha: 2026-02-26

## 1. Unificación Bancaria (Fusión de Archivos)
- **Concepto:** Integrar Depósitos Diarios + Facturación de Bancos + Conciliación Bancaria.
- **Objetivo:** Eliminar la duplicidad de trabajo en Excels separados. El sistema debe conciliar automáticamente el estado de cuenta contra los registros internos.

## 2. Reglas de Comisiones para Cobradores
El sistema debe bloquear comisiones automáticamente en estos casos:
- Pagos por transferencia o depósito anticipado (con/sin pronto pago).
- Pagos directos en oficina antes de la gestión del cobrador.
- Folios de solo "Entrega de Póliza" (sin dinero).
- Coberturas "AMPLIAS" (no generan comisión).
- **Endosos ($125):** Pago fijo de $50 por entrega, fuera del total de cobranza.

## 3. Control de Tiempos de Entrega
- **KPI:** Entrega al cliente en 3-5 días hábiles.
- **Campos:** "Fecha entrega a cobrador" y "Fecha entrega al cliente".
- **Alertas:** El sistema debe avisar si se excede el plazo para asegurar calidad en el servicio.

## 4. Gastos, Descuentos y Terceros
- **Gasolina:** Cargar reportes de gasolinera (vía Violeta) para cálculo automático del 50% de aportación.
- **Reembolsos:** Validación de facturas de gasolina en efectivo (reembolso 50%).
- **Préstamos:** Descuento quincenal automático por préstamos de moto.

## 5. Gestión de Vendedores (Atrasos)
- **Notificaciones:** Avisos automáticos de atrasos por Telegram/WhatsApp.
- **Candados:** Bloqueo de nuevas cuentas si exceden el 10% de ventas o tienen demasiada morosidad.
- **Seguimiento:** Bitácora con fechas de notificación, respuesta del vendedor y compromiso de pago.
