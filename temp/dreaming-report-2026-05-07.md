# Dreaming Report — 2026-05-07 (MX)

## 1. DAILY
- Daily del día **ya existía**: `memory/2026-05-07.md`.
- Se **completó** agregando:
  - bloque literal movido desde memoria caliente bajo `## Voz en caliente — sin hora MX`
  - bloque `## Respaldo dreamer — pipeline RAW nocturno`
- El daily ya traía contexto del incidente operativo del día y quedó reforzado con:
  - prohibición de mencionar “cancelación” a clientes
  - uso exclusivo de mensajes oficiales
  - desajuste detectado en el pipeline de export de RAW

## 2. MEMORIA CALIENTE
- Bloques movidos al daily:
  - incidente del **2026-05-07** sobre la prohibición de amenazas/intimidación y uso exclusivo de mensajes oficiales
- Bloques dejados intactos:
  - `Estado actual`
  - `Reglas/políticas vigentes`
  - `Disciplina de memoria`
  - `Qué SÍ guardar en dailies`
  - pendientes operativos persistentes
  - pendientes de maestría
  - `Qué NO guardar`
  - preferencias de Elena
  - plantillas oficiales de mensajes
  - límites de seguimiento
  - inversiones y finanzas familiares
  - automatización nocturna
- Limpieza aplicada:
  - se retiró de memoria caliente el bloque transitorio de hoy **solo después** de preservarlo literal en el daily
- Duda operativa:
  - el bloque estaba dentro de `## Pendientes (operación)` aunque en realidad funcionaba como incidente del día; se movió por fecha explícita, pero se deja constancia aquí

## 3. INTERACCIÓN DEL DÍA
- Se guardó en `memory/memoria-caliente.md` bajo `## Interacción del día (textual)` el único fragmento textual recuperable del día en RAWs:
  - instrucción automática de export nocturno RAW
  - respuesta de Luna reportando error real del script faltante y uso del exportador alterno
- Salvedad:
  - **no se encontró conversación humana Elena↔Luna del día** en los RAWs disponibles; no se inventó ninguna

## 4. APRENDIZAJES
- Propuesta para `MEMORY.md`:
  - **Pipeline RAW actual:** el setup real genera `memory/raws-daily/luna-YYYY-MM-DD.md`, no `memory/raws-daily/YYYY-MM-DD.md`; cualquier cron/verificación debe alinearse para evitar falsos errores.
  - **Incidencias operativas de Cobranza:** cuando Dirección prohíba una práctica por riesgo reputacional o de queja, documentar siempre: qué conducta queda prohibida, canal oficial permitido, sanción, responsables y seguimiento de acuses, sin datos sensibles.

## 5. SELF-IMPROVEMENT
- Propuestas para archivos de identidad/configuración (**NO aplicadas**):
  - `AGENTS.md` o `MEMORY.md`: aclarar explícitamente el nombre real del RAW diario vigente (`luna-YYYY-MM-DD.md`) para que los automatismos no fallen por expectativa de nombre.
  - `HEARTBEAT.md` o documentación de automatización: registrar que, si cambia el script de export, también debe actualizarse la instrucción del cron nocturno.
  - `MEMORY.md`: agregar mini regla de documentación de incidencias institucionales en Cobranza (conducta prohibida / mensaje oficial / seguimiento / evidencia).

## 6. AUDITORÍA QMD
- Estado **antes** de update:
  - documentos indexados: **121**
  - vectores embebidos: **295**
  - última actualización: **1d ago**
  - tamaño índice: **4.5 MB**
  - health general: índice sano; CPU only; sin GPU
- Ejecución:
  - `qmd update` → **1 new, 1 updated, 120 unchanged, 0 removed**
  - limpieza: **1 orphaned content hash**
  - `qmd embed` → **6 chunks from 2 documents**
- Estado **después**:
  - documentos indexados: **122**
  - vectores embebidos: **301**
  - última actualización: **9s ago** al momento de la verificación
  - tamaño índice: **4.6 MB**
- Resultado:
  - auditoría QMD **OK**

## 7. DUDAS
- No hubo duda fuerte sobre bloques persistentes vs transitorios aparte del incidente fechado dentro de `Pendientes (operación)`; se movió por llevar fecha explícita del día.
- Faltó el RAW con el nombre esperado por el cron (`memory/raws-daily/2026-05-07.md`).
  - Sí existió `memory/raws-daily/luna-2026-05-07.md` y alcanzó para cerrar.
  - Esto se reporta como **error de pipeline/documentación**, no como pérdida total de RAW.
