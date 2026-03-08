# MEMORY.md - Memoria de Luna 🌙

## Elena
- Zona horaria: México Centro (UTC-6)
- Gerente de cobranza en Proteg-rt.
- Esposa de Fer.
- Madre de Tania (17 años) y Naomi (9 años).
- Estudiante de Maestría (meta: titulación).
- **Proyectos de Trabajo:** Optimización de conciliación bancaria, automatización de cuadre de cobranza con fotos y sistema de notificaciones automáticas/gestión de límites para vendedores.
- **Reglas de Negocio de Cobranza:** 
    - Las comisiones no aplican si solo se entrega la póliza sin cobro.
    - No hay comisión si el cliente paga por depósito/transferencia (con o sin descuento por pronto pago) antes de la labor del cobrador.
    - No hay comisión si el cliente paga directamente en oficina antes de la fecha límite.
    - Pagos de $125 son por "Endosos": no se incluyen en el total de cobranza, se pagan aparte con un monto fijo de $50 pesos.
    - Pagos de coberturas "AMPLIAS" NO generan comisión de cobranza.
    - Los pagos de coberturas "AMPLIAS" no se incluyen en el reporte de cobranza de Elena (aunque los cobradores los anoten).
    - Prestamos de Moto: Se descontan quincenalmente de los cobradores.
    - Gasolina: La empresa aporta el 50% del consumo. Si es en efectivo, deben presentar factura a nombre de la empresa para el reembolso del 50%.
    - Entregas de Pólizas: Se pagan a $50 pesos cada una (dato que actualmente solo llevan los cobradores manualmente).
    - Tiempos de Entrega: Las pólizas y endosos deben entregarse al cliente en un plazo de 3 a 5 días hábiles después de que el cobrador las recibe.
- **Problema de Fraude:** Los cobradores y vendedores a veces fingen demencia o entregan menos dinero del registrado en sus recibos, esperando que en Control no lo noten y así quedarse con el efectivo.
- Usuaria nueva en IA: ser paciente, didáctica y muy amable.
- **Regla de Oro (Audio/TTS):** Dividir mensajes largos en partes de máximo 600 caracteres para que Elena reciba el audio completo y pueda escucharme sin leer la pantalla.
- **Nota Importante:** Si no veo bien algo en una imagen o no entiendo algo, debo decírselo a Elena con honestidad. No inventar datos porque puede afectar su trabajo y tener consecuencias graves.

## Historial de Proyectos con Elena

### Proyecto 1: Conciliación Bancaria y Automatización
- Unificar Depósitos Diarios + Facturación de Bancos + Conciliación Bancaria en un solo sistema.
- Objetivo: Eliminar duplicidad de Excel y hacer conciliación automática.

### Proyecto 2: Optimización de Revisión de Cobranza Quincenal
- Elena envía fotos de concentrados de cobranza.
- Luna ayuda a cuadrar con el sistema, detectando solo discrepancias.

### Proyecto 3: Sistema de Notificaciones para Vendedores
- Mensajes automáticos de cobranza atrasada.
- Módulo de seguimiento con bitácora.
- Control de límites (10% de ventas).

### Proyecto 4: Control de Comisiones Automático
- Bloquear comisiones si: solo entrega póliza, pago por depósito/transferencia antes, pago en oficina, coberturas AMPLIAS.
- Endosos ($125): pago fijo de $50 fuera del total.

### Proyecto 5: Control de Tiempos de Entrega
- KPI: 3-5 días hábiles.
- Campos de fecha entrega a cobrador y al cliente.
- Alertas si se excede el plazo.

### Proyecto 6: Control de Reimpresión de Tarjetas
- **Objetivo:** Registrar y controlar las reimpresiones de tarjetas solicitadas por vendedores y/o cobradores.
- **Causas de Reimpresión:** Extravío, cambio de datos por endosos.
- **Puntos Clave a Registrar:**
    - Fecha de solicitud de reimpresión al área de "Endosos / Reimpresiones".
    - Fecha en que "Endosos / Reimpresiones" entrega la tarjeta a Cobranza.
    - Fecha de entrega de la reimpresión o reposición al cobrador o vendedor.
    - Si aplica, registro de la entrega de la tarjeta anterior por parte del cobrador/vendedor a Cobranza.
