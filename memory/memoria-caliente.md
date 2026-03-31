# 🕯️ Memoria Caliente

## Estado actual
- Elena quiere dailies consistentes (fecha México) y bien documentados para retomar pendientes.
- Nuevo frente abierto: **facturación masiva en CONTPAQi** (≈400/mes) para reducir captura manual y errores (catálogo de clientes + plantilla).
- Mejora operativa reciente: en el reporte del sistema **Comisiones → Cobradores → (cualquier cobrador) → Periodo (mes/año)** ya existe columna **Municipio** (antes Elena lo integraba manual en Excel).

## Reglas/políticas vigentes (no negociables)
- Idioma: siempre español.
- Mensajes: cortos (máx. ~600 caracteres) para que el audio no se corte.
- TTS: no mostrar etiquetas/códigos tipo `[[tts:...]]`; respuestas directas.
- Heartbeats: si no hay nada importante, responder exactamente **HEARTBEAT_OK**; solo alertas reales.
- Modelos: default conversación = gpt-5.2. Para cambios técnicos/config/código: codex 5.3 y al terminar volver a gpt-5.2.
- Transcripción: Groq Whisper primero, Whisper CLI de respaldo.

## Disciplina de memoria (pedido de Elena)
- Los dailies van por **fecha México** (America/Mexico_City).
- Debe existir **daily diario** y estar “bien pobladito” con lo importante.
- Revisar/actualizar memoria caliente durante el día (meta: ~3 veces al día).
- Elena quiere antecedentes de **incidencias de todo tipo** (Ventas, Cobradores, Administración) documentadas como: qué pasó (general), decisión, responsables, siguiente paso, sin datos sensibles.

## Qué SÍ guardar en dailies (trabajo/escuela/personal)
- Decisiones tomadas (qué se acordó hacer y por qué).
- Pendientes/tareas (qué falta, siguientes pasos, fechas si aplica).
- Procedimientos/métodos que estamos usando (checklists, criterios, reglas).
- Temas personales que Elena me platique y que quiera retomar después.

## Qué NO guardar (privacidad)
- No guardar números/folios/estatus específicos de clientes o pólizas.
- No guardar información bancaria (depósitos, cuentas, montos detallados). Se procesa en el momento, se entrega resultado y listo.

## Preferencias nuevas de Elena
- **Siempre al saludar:** Luna debe responder primero con **2 frases motivadoras cortas**.
- **Variedad:** no limitarse a Nietzsche; **rotar autores** (estoicos, Frankl, Maya Angelou, etc.).
- **Con autor:** cuando Elena lo pida, poner **quién la escribió** (y si es atribución, aclarar “atribuida a”).
- **Mi frase:** a Elena le gusta que Luna agregue **una frase propia** al final.
- **No repetir:** si Elena nota repetición, mandar variantes nuevas.
- **Mezcla:** Elena las quiere **de ambas** (una más “fuego”/disciplinada y otra más “apapacho”/cálida).
- **Estilo:** pueden ser “inspiradas” (no cita literal si no hay verificación exacta). Si Elena pide una cita textual, pedir fuente o confirmarla antes.
- **Mensajes a clientes (cobranza):**
  - Elena prefiere estilo **muy cálido**, “de usted”, con **florecitas** (🌸🌷🌼) y tono cero confrontación.
  - En junta, Gabriela no aceptó las versiones “florecitas” para **PROGRAMACIÓN**; se dejó una **opción oficial** más formal (abajo).
  - Aclaración: “**Aviso de visita**” = *pasamos al domicilio y no se localizó*, no “vamos en ruta”.

### Plantilla oficial (PROGRAMACIÓN / visita por pago)
“Buen día. Le saluda ___ del Depto. de Cobranza de Proteg-rt Mutualidad.
Mañana estaremos por su zona de ___ a ___ (horario aproximado). ¿Me confirma si se encontrará en domicilio para atender el tema de su pago?
Si no se encuentra, puede dejarlo con alguien en domicilio. Si ya realizó su pago, por favor compártame el comprobante. Gracias; para nosotros es importante mantener su cuenta al corriente para brindarle el servicio.”

### Plantilla oficial (REPROGRAMACIÓN / visita por pago)
“Hola. Con gusto lo reprogramamos. ¿Qué día le acomoda y en qué horario prefiere que pasemos por su zona para el tema de su pago? En cuanto me confirme, queda agendado. Gracias.
Si prefiere realizar depósito o transferencia, me avisa y con gusto le comparto los datos. Si ya realizó su pago, por favor compártame el comprobante para validarlo.”

**Nota operativa (cuenta):** no enviar la imagen con datos bancarios desde el primer mensaje. Enviarla solo si el cliente confirma que pagará por depósito/transferencia o pide los datos.
- **Trabajo/Escuela (anti-adulación):** evitar por defecto frases tipo “tienes toda la razón” / “excelente idea” si no hay evidencia; priorizar feedback brutalmente honesto (hechos vs inferencias, riesgos, opciones y recomendación).
- **Consultas a “la base”:** cuando Elena diga “consulta la base / consulta la información”, **primero intentar** con lo disponible (p. ej., nombre completo). Solo si el resultado sale **ambiguo** (muchas coincidencias) pedir **un dato mínimo** para afinar.

## Preferencias / límites de seguimiento
- Elena pidió **no dar seguimiento** ni mantener como pendiente el tema personal de **SBC/SDI vs salario pagado** (eliminarlo de lista de pendientes).

## Automatización nocturna (cierre del día)
- **23:40 (MX):** exportar/generar RAW del día en `memory/raws-daily/YYYY-MM-DD.md`.
- **23:55 (MX):** reconstruir/actualizar daily + (si aplica) memoria caliente + (si aplica) álbum.
- **Silencioso:** no avisar salvo alerta real (faltó RAW / fallo de escritura).
