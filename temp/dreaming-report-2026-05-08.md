# Dreaming Report — 2026-05-08 (MX)

## 1. DAILY
- Se **completó/reescribió** `memory/2026-05-08.md` para dejarlo narrativo y escaneable.
- Se documentó que el día tuvo una sola actividad relevante: **la exportación RAW nocturna**.
- Se dejó claro en el daily:
  - que el script pedido por el cron **no existe** (`scripts/export_raws.py`)
  - que el fallback **sí funcionó** (`bash scripts/batch_export_raws.sh`)
  - que el RAW del día **sí existe** como `memory/raws-daily/luna-2026-05-08.md`
  - que el problema real es **desalineación del pipeline** (nombre esperado vs nombre generado)
- No se añadieron datos sensibles.

## 2. MEMORIA CALIENTE
- **Bloques movidos al daily:** ninguno.
  - No detecté bloques transitorios nuevos del 2026-05-08 para mover desde `memory/memoria-caliente.md`.
- **Bloques dejados intactos:**
  - `Estado actual`
  - `Reglas/políticas vigentes`
  - `Disciplina de memoria`
  - `Qué SÍ guardar en dailies`
  - `Pendientes (operación)`
  - `Pendientes Maestría`
  - `Qué NO guardar`
  - `Preferencias nuevas de Elena`
  - `Preferencias / límites de seguimiento`
  - `Inversiones y finanzas familiares`
  - `Automatización nocturna`
  - plantillas oficiales de mensajes a clientes
- **Acción aplicada:** se actualizó `## Interacción del día (textual)` para reemplazar la anterior por la del 2026-05-08.
- **Limpieza de transitorios:** no fue necesaria.
- **Duda operativa menor:** el bloque `Automatización nocturna` ya menciona que el export genera `luna-YYYY-MM-DD.md`; eso confirma que es persistente y se dejó intacto.

## 3. INTERACCIÓN DEL DÍA
- Fragmento guardado en `memory/memoria-caliente.md`:

```md
Elena:
[cron:d2987208-0967-4e0e-9cf6-b9bc9e9c9220 Nightly RAW export (MX 23:40)] TAREA NOCTURNA (automatización) — MX 23:40

Objetivo: exportar el RAW del día (MX) para que quede listo antes del rebuild.

Pasos:
1) Ejecuta en workspace: python3 scripts/export_raws.py day today
2) Verifica que exista/actualice: memory/raws-daily/YYYY-MM-DD.md

Privacidad:
- Este paso solo exporta RAW (sin publicar); no enviar mensaje a Elena salvo ERROR real (no se pudo leer sesiones o escribir archivo).

Luna:
ERROR real en la tarea nocturna:

- Falló el paso 1 porque **no existe** el script: `scripts/export_raws.py`
  (`[Errno 2] No such file or directory`).

Para no dejar el día sin RAW, corrí el **fallback operativo**:
- `bash scripts/batch_export_raws.sh` ✅

Resultado:
- Sí se generó/actualizó el RAW del día en:
  `memory/raws-daily/luna-2026-05-08.md` ✅

Nota: el nombre que queda en este workspace es `luna-YYYY-MM-DD.md` (no `YYYY-MM-DD.md`), por eso no aparece el archivo con el nombre “esperado” del paso 2.
```

## 4. APRENDIZAJES
- **Propuesta para MEMORY.md**
  - `Pipeline de RAW nocturno:` en este workspace, el exportador vigente genera archivos con patrón `memory/raws-daily/luna-YYYY-MM-DD.md`; cualquier automatización o verificación debe contemplar ese nombre real para evitar falsos errores.
  - `Criterio operativo de resiliencia:` si el script documentado por un cron no existe, usar el exportador vigente del workspace y registrar el error exacto; no asumir que la ausencia del script significa ausencia de RAW.

## 5. SELF-IMPROVEMENT
- **Propuesta para AGENTS.md o TOOLS.md**
  - Documentar explícitamente el **nombre real de salida** del export RAW nocturno para evitar confusión futura.
- **Propuesta para HEARTBEAT/automatizaciones**
  - Ajustar el cron de 23:40 para que:
    - o bien use `bash scripts/batch_export_raws.sh` como comando principal
    - o bien valide ambos nombres posibles (`YYYY-MM-DD.md` y `luna-YYYY-MM-DD.md`)
- **Propuesta para MEMORY.md / infraestructura**
  - Registrar como regla técnica que el dreamer **no debe regenerar RAWs**; solo auditar lo que dejó el export anterior y reportar fallas de pipeline.

## 6. AUDITORÍA QMD
- **Antes del update/embed**
  - Docs indexados: **122 files indexed**
  - Vectores: **301 embedded**
  - Última actualización: **23h ago**
  - Health: índice funcional, sin GPU, ejecutando en CPU
- **Acción ejecutada**
  - `cd /home/elena/.openclaw/workspace && /home/elena/.local/bin/qmd update && /home/elena/.local/bin/qmd embed`
- **Resultado de `qmd update`**
  - `Indexed: 1 new, 1 updated, 121 unchanged, 0 removed`
  - `Cleaned up 1 orphaned content hash(es)`
- **Resultado de `qmd embed`**
  - `Embedded 6 chunks from 2 documents in 4s`
- **Después del update/embed**
  - Docs indexados: **123 files indexed**
  - Vectores: **307 embedded**
  - Última actualización: **10s ago**
  - Health: correcto; sin errores

## 7. DUDAS
- No hubo dudas de clasificación suficientemente fuertes como para dejar bloques sin tocar.
- Único punto a revisar después: decidir si la discrepancia `YYYY-MM-DD.md` vs `luna-YYYY-MM-DD.md` se corrige en el cron o en el exportador.
