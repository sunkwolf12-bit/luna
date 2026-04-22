# Dreaming Report — 2026-04-21

## 1. DAILY
- Se tomó como día a consolidar **2026-04-21 (MX)**.
- Motivo operativo:
  - existe RAW del día: `memory/raws-daily/luna-2026-04-21.md`
  - existe symlink esperado: `memory/raws-daily/2026-04-21.md`
  - no existe RAW de `2026-04-22`, así que no había materia prima para cerrar ese día.
- El daily `memory/2026-04-21.md` **ya existía** y estaba bastante completo.
- Se **completó** con contexto faltante:
  - auditoría del workspace/memoria/QMD que Elena pidió por la tarde
  - respaldo dreamer del trabajo grande del día: auditoría + unificación del procedimiento de revisión mensual de tarjetas
  - pendiente de mover el RTF fuera de raíz para respetar la estructura del workspace

## 2. MEMORIA CALIENTE
- **Bloques movidos:** ninguno.
  - No detecté bloques transitorios del 21/abr claramente separados del contenido persistente.
  - `memoria-caliente.md` estaba compuesto principalmente por estado actual, reglas, preferencias, pendientes persistentes, plantillas y automatización nocturna.
- **Qué dejé intacto:**
  - Estado actual
  - Reglas/políticas vigentes
  - Disciplina de memoria
  - Qué sí guardar / qué no guardar
  - Preferencias nuevas de Elena
  - Plantillas oficiales
  - Pendientes operativos y de maestría
  - Inversiones y finanzas familiares
  - Automatización nocturna
- **Acción hecha en memoria caliente:**
  - se actualizó/reemplazó la sección **`## Interacción del día (textual)`** con el fragmento más significativo del 21/abr
- **Duda operativa:** no limpié nada de memoria caliente porque no encontré bloques transitorios con frontera segura para “mover sin destruir”

## 3. INTERACCIÓN DEL DÍA
- Se guardó en `memory/memoria-caliente.md` este fragmento textual:

> Elena: ME PUEDES AYUDAR A AUDITAR ESTE PROCEDIMIENTO, QUE ES DE REVISION DE TARJETAS MENSUAL A LOS COBRADORES.
>
> Elena: TE EXPLICO BREVEMENTE EN QUE CONSISTE LA ACTIVIDAD:
>
> Elena: se realiza una revision para supervisar todas las tarjetas que tiene asignado un cobrador, todaaaaaaas.
> para eso se les agenda con anticipación, para que ellos puedan reunir o organizar toda la cobranza que tienen asignada, desde tarjetas hasta las pólizas con sus tarjetas para pago inicial.
>
> Luna: Sí, te lo audito. El procedimiento está bien encaminado (objetivo/alcance/responsables/frecuencia), pero hoy tiene huecos que en operación se vuelven “pleito” o se presta a que cada quien lo haga distinto. Aquí van los puntos concretos.
>
> Luna: Perfecto, con eso ya se entiende “cómo pasa en la vida real”. Aquí va la auditoría aterrizada y qué le falta al documento para que cualquiera lo ejecute igual (y para que el cobrador no te salga con cuentos).
>
> Luna: Listo. Te dejo un procedimiento completo, rígido y ejecutable, escrito en formato “de manual”, para que cualquier persona lo haga igual (sin interpretaciones).

## 4. APRENDIZAJES
- **Propuesta para MEMORY.md**
  - En revisión mensual de tarjetas a cobradores:
    - **Baseline oficial** = Excel proporcionado por Gerencia de Cobranza (origen Pagos_V3 / Proteg-rt)
    - **SIGA** = consulta de apoyo para validar/aclarar, pero no sustituye el baseline
    - El revisor/asistente nocturna **solo registra**; **no corrige en sistema**
    - Catálogo útil de dictamen: **OK / REVISAR / FALTANTE / NO CORRESPONDE**
  - En higiene del workspace:
    - si se genera un entregable de trabajo (como un RTF/procedimiento), debe vivir en `workspaces/` y no en raíz
  - En automatización nocturna:
    - si falta `scripts/export_raws.py`, el fallback válido es `scripts/batch_export_raws.sh` + symlink `memory/raws-daily/YYYY-MM-DD.md`

## 5. SELF-IMPROVEMENT
- **Propuestas para archivos de identidad/config (NO aplicadas):**
  - **AGENTS.md / MEMORY.md**
    - dejar explícita la regla del flujo dual para revisión de tarjetas:
      - Excel oficial de Gerencia = base que manda
      - SIGA = consulta de apoyo
  - **MEMORY.md**
    - agregar la convención del dictamen rígido para tarjetas: OK / REVISAR / FALTANTE / NO CORRESPONDE
  - **MEMORY.md o TOOLS.md**
    - documentar que el cron de RAW depende hoy del fallback `batch_export_raws.sh` porque `scripts/export_raws.py` no existe
  - **MEMORY.md**
    - registrar que Elena pidió respuestas sin `Source:` salvo que lo solicite explícitamente (ya aparece en caliente; podría promoverse a memoria larga si se confirma como regla estable)

## 6. AUDITORÍA QMD
- **Antes del update**
  - Docs indexados: **97**
  - Vectores embebidos: **212**
  - Updated: **10h ago**
  - Health: funcional, sin GPU, colección `workspace` activa
- **Comando ejecutado**
  - `cd /home/elena/.openclaw/workspace && /home/elena/.local/bin/qmd update && /home/elena/.local/bin/qmd embed && /home/elena/.local/bin/qmd status`
- **Resultado de update/embed**
  - Collections updated: **1**
  - Indexed: **0 new, 2 updated, 95 unchanged, 0 removed**
  - Cleaned up orphaned hashes: **2**
  - Embedded: **8 chunks from 2 documents**
- **Después del update**
  - Docs indexados: **97**
  - Vectores embebidos: **220**
  - Updated: **10s ago** al momento de la verificación
  - Health: **OK**, proceso terminó con código **0**
  - Nota: sigue en **CPU** (sin GPU), por eso puede ir lento

## 7. DUDAS
- **Fecha operativa / corrida:** el evento llegó con hora actual `2026-04-22 05:55 MX`, pero el RAW disponible y el contexto de la automatización apuntan al cierre de **2026-04-21**. Por seguridad consolidé **21/abr** y no inventé daily/RAW de 22/abr.
- **Memoria caliente:** no quedó claro qué bloques, si alguno, fueron escritos en caliente específicamente el 21/abr como bloques transitorios separados de las secciones persistentes. Preferí no mover nada para respetar la regla de “mover, no destruir”.
