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
- **Mensaje oficial de Cobranza Vencida a vendedores:**
  "Hola __, buena tarde.

Al auditar tu cartera, identifico cobranza vencida por $ 6,423
Por favor confírmame:

1. Estatus de los pagos pendientes, y
2. Fecha compromiso para que queden liquidados.

Quedo atenta por si necesitas apoyo para la gestión.

Saludos,
Elena Rivas
Gerencia de Cobranza"
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

### Proyecto 7: Facturación masiva (CONTPAQi) + catálogo de clientes
- Volumen: ~400 facturas/mes.
- Patrón: todas **PUE**, concepto/clave de servicio fija ("001"); cambian cliente, monto y forma de pago.
- Objetivo: reducir captura manual y errores usando (a) **catálogo maestro** de clientes y (b) **plantilla** (Excel) para facturación repetitiva; evaluar si la versión permite **importación/carga masiva** y, si no, implementar flujo de duplicado/captura mínima.
- Datos sensibles: el catálogo no se debe circular por chat en texto; idealmente se mantiene en PC/carpeta interna. Fer tiene una lista base (no fiscal completa) que sirve para arrancar; los datos fiscales se completan con CSF cuando toque.
- Pendiente: definir método de resguardo/respaldos (USB/OneDrive cuando haya acceso) y checklist de campos CFDI 4.0 para evitar errores.

### Proyecto 8: Reporte de cobranza por cobrador con Municipio (mejora de sistema)
- Dolor: Elena integraba **Municipio** manualmente en Excel para supervisar cobranza por zonas.
- Implementación: Fer modificó el sistema para que el reporte **Comisiones → Cobradores → (cualquier cobrador) → Periodo (mes/año)** ya incluya la columna **Municipio**.
- Fuente del dato: el municipio ya existe guardado en la ficha/domicilio del cliente (no se calcula por CP).

### Herramienta: consultas a “la base de datos” (skill + API en VPS)
- Si Elena pide “consultar la base de datos”, usar la skill **db-consultas** (solo lectura) del asistente de Óscar, que pega a la API REST en este VPS.
- Base URL: `http://165.22.129.133:8000` · Docs: `/docs`.
- Autenticación: header `X-API-Key` (la llave ya está en el servidor/skill; no compartirla por chat).
- Nota: hay endpoints de **guardias** (ej. `/api/v1/guardias/hoy`, `/api/v1/guardias/semana`).


---

## Estructura del workspace — dónde vive cada cosa (agregado 21 abr 2026)

### Raíz (solo identidad y configuración)
- `AGENTS.md`, `SOUL.md`, `USER.md`, `IDENTITY.md`, `HEARTBEAT.md`, `TOOLS.md` — quién soy
- `MEMORY.md`, `BOOTSTRAP.md`, `PREFERENCES.md`, `SELF_IMPROVEMENT.md`, `LESSONS.md` — memoria larga + preferencias
- `CONOCIMIENTO-NEGOCIO.md` — contexto de negocio de Elena

### `memory/` — memoria operativa
- `YYYY-MM-DD.md` — dailies, uno por día
- `memoria-caliente.md` — voz primaria del momento (la mueve el dreamer al daily cada noche)
- `album-de-recuerdos.md` — momentos que importan atesorar
- `dailies-raw/` — raws por día generados por el cron (no editar a mano)
- `<tema>.md` — conocimientos permanentes por tema (ej. `estilo_elena.md`)

### `skills/<nombre>/` — habilidades
Cada skill en su propio subdir con `SKILL.md` + `references/` + `scripts/` si aplican.

### `workspaces/<tema>/` — trabajo real de Elena
**Todo archivo de trabajo (xlsx, csv, docx, pdf, scripts de negocio) va aquí, NUNCA en raíz ni en memory/.**
Subdirs actuales: `conciliacion-bancaria/`, `caja-chica/`, `ensayos-elena/`, `instructivos/`, `adjuntos/`.
Si surge un tema nuevo → crear subdir nuevo `workspaces/<tema-nuevo>/`.

### `temp/` — temporales
- `dreaming-report-YYYY-MM-DD.md` — reportes del dreamer
- Drafts, archivos transitorios
- Nada crítico aquí — si importa, muévelo a `memory/` o `workspaces/`.

### `scripts/` — infra (NO tocar desde conversación)
Scripts del pipeline de memoria: `mx_clock.py`, `jsonl_to_raw.py`, `batch_export_raws.sh`.

## Reglas duras de orden

1. **Antes de crear un archivo nuevo**, preguntarme: ¿de qué tipo es? → consultar la tabla de arriba.
2. **Raíz es sagrada** — solo los archivos listados. Si tengo impulso de crear algo en raíz, casi siempre va en `workspaces/` o `memory/`.
3. **Trabajo con fechas específicas** → dailies en `memory/YYYY-MM-DD.md`, no archivos sueltos con fecha en raíz.
4. **Drafts y cosas transitorias** → `temp/`. Si se vuelven permanentes, moverlos a `memory/` o `workspaces/`.
5. **Si dudo dónde va algo**, preguntar a Elena antes de crear.
