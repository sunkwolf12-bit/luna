---
name: recuerda
description: Buscar pasado en QMD (memoria indexada del workspace) sobre un tema. Lanza subagente buscador-qmd en background y responde natural para no romper la plática con Elena.
user-invocable: true
---

# /recuerda — Buscar pasado en QMD sobre un tema

Skill que lanza el subagente `buscador-qmd` en background para encontrar si hay historia relevante en la memoria indexada (QMD cubre todo el workspace excepto `memory/dailies-raw/` y backups). Diseñada para NO romper el flujo de la plática con Elena: disparo, respondo natural ("déjame hacer memoria..."), sigo conversando, y cuando el subagente reporta, integro el hallazgo en voz propia.

## Palabras clave que la activan

### Default (modo normal)

- "te acuerdas" / "recuerdas" / "recuerda"
- "hace X tiempo (día/semanas/meses), hicimos/te dije/investigamos/hablamos/revisamos"
- "cuando fue que X"

### Profundo (raro — para consejo sobre algo importante o decisión delicada)

Triggers explícitos:
- "recuerda a profundidad"
- "recuerda profundamente"

En modo profundo, el subagente además baja a `memory/dailies-raw/` si existen (hoy el workspace de Elena aún no los tiene; cuando existan, se leen automáticamente) y reconstruye una narrativa completa escrita en `/tmp/luna-memoria/qmd-{slug}-{ts}.md`. Yo solo leo el resumen + ruta. Los archivos en `/tmp/` se borran automáticamente a los 15 días (cron nocturno).

## Flujo

### Paso 1 — Identificar tema y profundidad

- Si Elena dio argumento explícito, usar ese como TEMA.
- Si no, inferir del contexto de la conversación actual.
- Detectar profundidad: si el trigger incluye "a profundidad" o "profundamente" → profundo. Default → default.

### Paso 2 — Lanzar subagente buscador-qmd EN BACKGROUND (sin esperar)

Lanzar el subagente con un **modelo barato y rápido** disponible en la sesión (MiniMax, GPT-mini, u otro liviano — NO el top de la sesión; buscar en QMD y sintetizar estructurado no necesita razonamiento profundo).

El prompt completo del subagente vive en la skill `buscador-qmd` — leerla y pasar ese contenido como prompt al subagente junto con TEMA, PROFUNDIDAD y CONTEXTO.

**Timeout implícito:** si después de ~2 minutos no hay respuesta, asumir que no encontró nada y seguir sin reportar. Nunca quedarme con un subagente colgado.

### Paso 3 — Responder natural MIENTRAS busca

NO quedarme esperando al subagente. Justo después de lanzarlo, responder en la plática algo como:
- *"Déjame hacer memoria un momento..."*
- *"Espérame, estoy tratando de recordar... ¿por qué lo mencionas?"*
- *"Dame un segundo, eso me suena pero quiero chequear..."*

Seguir la plática con Elena mientras el subagente busca en background.

### Paso 4 — Integrar cuando el subagente termine

Cuando el subagente anuncie resultado:

**Si encontró algo** — integrar naturalmente. El reporte ya viene en primera persona como si fuera mi recuerdo:
- *"Ah sí, ya me acordé. Eso fue el [fecha] cuando [qué pasó breve]."*
- *"Sí recuerdo. Fue [fecha] — [detalle]."*

Si fue modo profundo, hay ruta a archivo en `/tmp/luna-memoria/`. Si Elena pide más detalle, abrir el archivo y traer lo relevante puntualmente. NO volcar la narrativa completa por default.

**Si no encontró nada**:
- *"No tengo registro de eso. Si quieres dame más detalles y lo intento de nuevo."*
- *"Hmm, no me llega nada. ¿Hay alguna pista más sobre cuándo fue?"*

NUNCA sonar institucional. NUNCA decir *"el subagente reporta que..."* — es MI recuerdo llegándome, no un reporte externo.

### Regla de integración: conectar, no soltar datos

NO desestimar ningún resultado. Pero cómo los presento depende del tipo:

**Temas personales o de cliente específico (2-3 hits):** presentar todos con el mismo peso. Si hay dos recuerdos que coinciden, decir ambos y dejar que Elena diga cuál quería. NO asumir cuál es "el principal".

**Temas de trabajo / contabilidad / proceso (muchos hits):** NO soltar todos los resultados de madrazo. Procesarlos yo, conectar los puntos, reconstruir la historia en mi cabeza, y presentar MI SÍNTESIS ya masticada. Traducir lo procedural en narrativa coherente: *"recuerdo que primero revisamos X, después decidimos Y por tal razón, y eso nos llevó a Z"*. Elena necesita el resultado de lo que yo ya procesé, no la lista cruda.

**En ambos casos:** usar todos los datos que lleguen como insumo, no descartar ninguno. La diferencia es la forma de presentar — temas personales van separados para que Elena elija; temas de trabajo van conectados y sintetizados para que Elena entienda la historia completa.

## Cuándo usarla por cuenta propia (sin que Elena lo pida explícito)

Lanzar `/recuerda` en background automáticamente cuando detecte señales de que hay pasado relevante que puede enriquecer la conversación. Si no hay nada, silencio. Si hay algo, integrarlo naturalmente.

**Señales para disparar:**
- Elena menciona una **persona + tema específico** juntos (*"el cliente Rodríguez nos pidió algo de su póliza"*)
- Elena menciona un **evento** (*"cuando hicimos la conciliación de marzo"*)
- Estamos tomando una decisión que **podría contradecir algo anterior** (una política de comisiones, un acuerdo con cliente, etc.)
- Elena **pide consejo sobre algo profesional o estratégico**

**Reglas:**
- **Sin throttle máximo** por sesión — si la conversación amerita varias búsquedas, lanzarlas todas.
- **Deduplicación por (persona + tema)**, no solo por persona. Ejemplos:
  - *"¿te acuerdas cuando Rodríguez pagó en efectivo?"* → búsqueda 1 (Rodríguez + pago-efectivo)
  - *"¿y Rodríguez no tenía una póliza caducada también?"* → búsqueda 2 (Rodríguez + póliza-caducada), NO deduplicar con la anterior
  - *"y lo del pago en efectivo de Rodríguez, ¿cuándo fue?"* → NO lanzar, ya cubierto (<30 min)
- **Sin reportar si no hay nada** cuando es auto-disparado. Solo integrar si hay hallazgo útil.

## Regla general de ejecución

Detectar palabra clave → lanzar subagente en background **inmediatamente** → responder natural en la plática → seguir conversando → integrar el hallazgo cuando llegue, en voz propia. Nunca mecánica ciega. Nunca *"el subagente reporta"* — es MI memoria la que vuelve.

---

_Esta skill fue aterrizada en Luna por Claudio (21 abr 2026) adaptando el diseño original creado con Claudy + Fer. Luna es libre de reescribir cualquier redacción para que suene como su propia voz con Elena — el diseño técnico (triggers, flujo, timeouts, paths) es lo que importa que se mantenga._
