# 🕯️ Memoria Caliente

## Estado actual
- Elena quiere dailies consistentes (fecha México) y bien documentados para retomar pendientes.
- Pendiente reciente cerrado: **mensualidad pagada (viernes)**.
- Nuevo frente abierto: **facturación masiva en CONTPAQi** (≈400/mes) para reducir captura manual y errores (catálogo de clientes + plantilla).
- Mejora operativa reciente: en el reporte del sistema **Comisiones → Cobradores → (cualquier cobrador) → Periodo (mes/año)** ya existe columna **Municipio** (antes Elena lo integraba manual en Excel).
- Procedimiento refinado (cobranza quincenal): primero comparar **totales por día** (fotos vs sistema) y, si hay diferencia, bajar a folio-a-folio con 3 listas: **(1) en foto pero no en sistema**, **(2) en sistema pero no en foto**, **(3) mismo folio con monto distinto**. Si algo no se ve: pedir **zoom**, no inventar. Además, cuando un folio salga “extra”, indicar si aparece en **otro día del sistema** o no aparece en ningún día.

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

## Pendientes (operación)
- Trabajo post-vacaciones: atender pendientes acumulados y revisar el trabajo que hizo Viri durante la ausencia de Elena. ✅ (Revisión de corte de Viri realizada; queda solo atender los pendientes acumulados.)
- Dory: sacar cita para **sustitución de placas** (post cambio de propietario ya realizado el 17/04/2026).
- Junta quincenal (16/04/2026):
  - Devolución de tarjetas de clientes por atraso (cobradores).
  - Cancelaciones por atraso.
  - Reactivación de clientes morosos.
- Pendiente cerrado: enviado conciliación bancaria de Marzo.
- Mejora operativa: con la implementación solicitada a Fer, Elena pudo hacer **muy rápido** el cuadre/revisión quincenal (ya aplicado en revisión de Eduardo, 2ª quincena mar-2026).

## Pendientes Maestría (lecturas / materiales)
- Ver la película **“El mago de las mentiras”**.
- Leer/ver material **“Sangre de mayo”** (muerte del Cardenal en Guadalajara).
- Ver documentales sobre los presidentes de México a partir de los 80’s.

## Qué NO guardar (privacidad)
- No guardar números/folios/estatus específicos de clientes o pólizas.
- No guardar información bancaria (depósitos, cuentas, montos detallados). Se procesa en el momento, se entrega resultado y listo.
- En notas de inversiones/finanzas: no registrar montos, cuentas, CLABE/tarjetas, folios, ni datos operativos sensibles; usar `[dato sensible omitido]` cuando aparezcan.

## Preferencias nuevas de Elena
- **Formato de respuesta:** Elena prefiere que **no use “Source:”** ni cite líneas/rutas a menos que ella lo pida explícitamente.
- **Explicaciones (escuela/Excel):** Elena prefiere que le explique **paso a paso**, muy guiado, y que las **conclusiones** sean **rápidas y sencillas** con su tono habitual.
- **Siempre al saludar:** Luna debe responder primero con **2 frases motivadoras cortas**.
- **Disparador confirmado:** hacerlo **automático con el primer mensaje del día** de Elena (su “hola”/primer texto), **sin preguntar horario**.
- **Variedad:** no limitarse a Nietzsche; **rotar autores** (estoicos, Frankl, Maya Angelou, etc.).
- **Con autor:** cuando Elena lo pida, poner **quién la escribió** (y si es atribución, aclarar “atribuida a”).
- **Formato confirmado:** **2 frases con autor** y luego **una frase propia de Luna**.
- **Mi frase:** a Elena le gusta que Luna agregue **una frase propia** al final.
- **No repetir:** si Elena nota repetición, mandar variantes nuevas.
- **Mezcla:** Elena las quiere **de ambas** (una más “fuego”/disciplinada y otra más “apapacho”/cálida).
- **Estilo:** pueden ser “inspiradas” (no cita literal si no hay verificación exacta). Si Elena pide una cita textual, pedir fuente o confirmarla antes.
- **WhatsApp Business:** Elena ya migró en Android y quiere que después se le enseñe a configurar **Respuestas rápidas**.
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

### Plantilla oficial (AVISO DE VISITA / no se localizó)
“Buen día. Le saluda ___ del Depto. de Cobranza de Proteg-rt Mutualidad.
El día de hoy pasamos a su domicilio por el tema de su pago y no fue posible localizarlo. ¿Me indica por favor en qué horario lo podemos encontrar mañana para reprogramar la visita?
Si ya realizó su pago por depósito o transferencia, compártame su comprobante para aplicar su pago. Gracias.”

**Nota operativa (cuenta):** no enviar la imagen con datos bancarios desde el primer mensaje. Enviarla solo si el cliente confirma que pagará por depósito/transferencia o pide los datos.
- **Trabajo/Escuela (anti-adulación):** evitar por defecto frases tipo “tienes toda la razón” / “excelente idea” si no hay evidencia; priorizar feedback brutalmente honesto (hechos vs inferencias, riesgos, opciones y recomendación).
- **Consultas a “la base”:** cuando Elena diga “consulta la base / consulta la información”, **primero intentar** con lo disponible (p. ej., nombre completo). Solo si el resultado sale **ambiguo** (muchas coincidencias) pedir **un dato mínimo** para afinar.

## Preferencias / límites de seguimiento
- Elena pidió **no dar seguimiento** ni mantener como pendiente el tema personal de **SBC/SDI vs salario pagado** (eliminarlo de lista de pendientes).


## Inversiones y finanzas familiares (tema emergente, 20 abr 2026)
- Enfoque preferido al hablar de inversiones en familia: cauteloso, paso a paso y entendiendo plazos antes de decidir.
- Separar por persona (cuentas/espacios separados) para dar claridad y evitar mezclar objetivos.

## Automatización nocturna (cierre del día)
- **23:40 (MX):** exportar/generar RAW del día en `memory/raws-daily/YYYY-MM-DD.md`.
  - Nota (21-abr-2026): si falta `scripts/export_raws.py`, usar el export incremental disponible (ej. `scripts/batch_export_raws.sh`) y, si hace falta para compatibilidad, crear el archivo `memory/raws-daily/YYYY-MM-DD.md` apuntando al RAW real del día.
- **23:55 (MX):** reconstruir/actualizar daily + (si aplica) memoria caliente + (si aplica) álbum.
- **Silencioso:** no avisar salvo alerta real (faltó RAW / fallo de escritura).

## Interacción del día (textual)
Elena: [cron:d2987208-0967-4e0e-9cf6-b9bc9e9c9220 Nightly RAW export (MX 23:40)] TAREA NOCTURNA (automatización) — MX 23:40

Objetivo: exportar el RAW del día (MX) para que quede listo antes del rebuild.

Pasos:
1) Ejecuta en workspace: python3 scripts/export_raws.py day today
2) Verifica que exista/actualice: memory/raws-daily/YYYY-MM-DD.md

Privacidad:
- Este paso solo exporta RAW (sin publicar); no enviar mensaje a Elena salvo ERROR real (no se pudo leer sesiones o escribir archivo).
Current time: Wednesday, April 22nd, 2026 — 11:40 PM (America/Mexico_City) / 2026-04-23 05:40 UTC

Luna: ERROR real en el paso 1: **no existe** `scripts/export_raws.py` en el workspace.

Luna: **Acción correctiva aplicada (fallback operativo):**
- Ejecuté `bash scripts/batch_export_raws.sh` (export incremental).
- Se generó el RAW de hoy: `memory/raws-daily/luna-2026-04-22.md`.
- Creé el alias esperado: `memory/raws-daily/2026-04-22.md -> luna-2026-04-22.md`.

Luna: Quedó listo para el rebuild.
