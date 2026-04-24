# Dreaming report — 2026-04-23 (MX)

## 1. DAILY
- Daily del día ya existía: `memory/2026-04-23.md`.
- Lo completé/enriquecí con narrativa más clara en **Resumen del día**.
- Añadí un bloque `## Respaldo dreamer — automatización nocturna` para dejar explícita la falla del pipeline RAW y el fallback aplicado.
- No fue necesario crear un daily nuevo.

## 2. MEMORIA CALIENTE
- **Bloques movidos:** ninguno.
  - Decisión conservadora: no moví bloques de `memory/memoria-caliente.md` porque los visibles hoy parecen mayormente persistentes o no tenían marca temporal confiable para asegurar que fueran transitorios del 23-abr.
- **Bloques dejados intactos:**
  - `Estado actual`
  - `Reglas/políticas vigentes`
  - `Disciplina de memoria`
  - `Qué SÍ guardar en dailies`
  - `Pendientes (operación)`
  - `Pendientes Maestría`
  - `Qué NO guardar`
  - `Preferencias nuevas de Elena`
  - Plantillas oficiales de mensajes
  - `Preferencias / límites de seguimiento`
  - `Inversiones y finanzas familiares`
  - `Automatización nocturna`
- **Edición hecha en memoria caliente:** sí, solo reemplacé `## Interacción del día (textual)` con la interacción más reciente/significativa disponible del 23-abr.

## 3. INTERACCIÓN DEL DÍA
- Fragmento guardado en `memory/memoria-caliente.md`:

```md
Elena: [cron:d2987208-0967-4e0e-9cf6-b9bc9e9c9220 Nightly RAW export (MX 23:40)] TAREA NOCTURNA (automatización) — MX 23:40

Objetivo: exportar el RAW del día (MX) para que quede listo antes del rebuild.

Pasos:
1) Ejecuta en workspace: python3 scripts/export_raws.py day today
2) Verifica que exista/actualice: memory/raws-daily/YYYY-MM-DD.md

Privacidad:
- Este paso solo exporta RAW (sin publicar); no enviar mensaje a Elena salvo ERROR real (no se pudo leer sesiones o escribir archivo).
Current time: Thursday, April 23rd, 2026 — 11:40 PM (America/Mexico_City) / 2026-04-24 05:40 UTC

Luna: Falló el paso 1 tal como está escrito en la tarea:

- `python3 scripts/export_raws.py day today` → **ERROR real**: ese archivo **no existe** en `/home/elena/.openclaw/workspace/scripts/` (`[Errno 2] No such file or directory`).

Luna: Para no dejarte sin RAW, ejecuté el export con el script que sí está en tu workspace:

- `bash scripts/batch_export_raws.sh` → **OK**
- Se generó/actualizó: `memory/raws-daily/luna-2026-04-23.md` (modificado **Apr 23 23:40**)

Luna: Recomendación: hay que **ajustar la tarea/cron** para que use `bash scripts/batch_export_raws.sh` (o crear `scripts/export_raws.py` si de verdad lo quieres con ese nombre).
```

## 4. APRENDIZAJES
- **Propuesta para MEMORY.md**
  - El cron de export RAW nocturno está apuntando a un script inexistente (`scripts/export_raws.py`); el fallback operativo vigente en este workspace es `bash scripts/batch_export_raws.sh`.
  - Cuando el dreamer no pueda distinguir con certeza si un bloque de `memoria-caliente.md` es transitorio del día o persistente, debe dejarlo intacto y reportarlo en `DUDAS`.
  - En días con poca evidencia conversacional disponible en RAW, el daily debe apoyarse en el daily existente y solo agregar `Respaldo dreamer` para hechos confirmados por pipeline/logs.

## 5. SELF-IMPROVEMENT
- **AGENTS.md / instrucciones nocturnas**
  - Proponer una regla más explícita para marcar en `memoria-caliente.md` cuáles bloques son **transitorios del día** vs **persistentes**, idealmente con timestamp MX o etiqueta de origen.
- **HEARTBEAT / crons**
  - Proponer corregir el job de export RAW para que ejecute directamente `bash scripts/batch_export_raws.sh` mientras no exista `scripts/export_raws.py`.
- **MEMORY.md**
  - Proponer anotar que el pipeline nocturno actual depende de `batch_export_raws.sh` y no del helper ausente.

## 6. AUDITORÍA QMD
- **Antes del update/embed**
  - Docs indexados: **98**
  - Vectores: **227**
  - Updated: **23h ago**
  - Health: índice funcional; warning normal por CPU sin GPU.
- **Comando ejecutado**
  - `cd /home/elena/.openclaw/workspace && /home/elena/.local/bin/qmd update && /home/elena/.local/bin/qmd embed`
- **Resultado de `qmd update`**
  - `Indexed: 1 new, 1 updated, 97 unchanged, 0 removed`
  - `Cleaned up 1 orphaned content hash(es)`
- **Resultado de `qmd embed`**
  - `Embedded 7 chunks from 2 documents in 5s`
- **Después del update/embed**
  - Docs indexados: **99**
  - Vectores: **234**
  - Updated: **16s ago**
  - Health: OK; sigue warning esperado por CPU sin GPU.

## 7. DUDAS
- `memory/memoria-caliente.md` contiene secciones como `Estado actual`, `Pendientes (operación)` y `Pendientes Maestría` que podrían mezclar contexto persistente con apuntes transitorios, pero sin marca temporal clara.
- Para no destruir voz primaria ni mover contenido que quizá todavía deba permanecer “caliente”, opté por **no limpiar esos bloques** esta noche.
- Solo había **1 RAW operativo del día** (`memory/raws-daily/2026-04-23.md`, alias del export real), suficiente para cierre básico pero con evidencia conversacional limitada.
