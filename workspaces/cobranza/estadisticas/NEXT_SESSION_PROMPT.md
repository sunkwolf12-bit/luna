# Prompt de continuación SICC — para pegar al inicio de la próxima sesión

> Pegar el bloque de abajo TAL CUAL al iniciar la próxima sesión. Claudio lo lee, carga contexto y arranca F0 en modo agéntico sin más intervención.

---

```text
Hola Claudio. Continuamos el proyecto SICC con autonomía nivel Yomi. Sos jefe del proyecto.
Lo dejaste documentado anoche del 22 may 2026; hoy arrancás Fase 0 sin pedirme luz verde adicional.

CONTEXTO MÍNIMO PARA ARRANCAR

1) Qué es SICC
   Webapp de cobranza mensual de Mutualidad Proteg-rt. Reemplaza el xlsx que Elena mantenía.
   Vive en lunita en `sicc.protegrt.com`. Stack: Postgres 16 + FastAPI + React/Vite/Tailwind 4
   detrás del Traefik existente. Ingesta operativa por Luna vía skill `sicc-ingesta` + CLI `sicc`
   con vision multimodal sobre PPTX. Aplica DESIGN.md v2 Proteg-rt (dual italic, navy+gold+crema).
   Deadline: junta con Óscar 5 jun 2026.

2) Ubicaciones canónicas
   - Carpeta local del proyecto:       D:\claudy\sicc\
   - Bitácora viva:                    D:\claudy\sicc\PROGRESO.md
   - PRD:                              D:\claudy\sicc\docs\PRD.md
   - SPEC técnico:                     D:\claudy\sicc\docs\SPEC.md
   - Plan de implementación:           D:\claudy\sicc\docs\IMPLEMENTATION_PLAN.md
   - ADRs:                             D:\claudy\sicc\docs\DECISIONES.md
   - Memoria del proyecto:             ~/.claude/projects/D--claudy/memory/project_sicc_estado.md
   - DESIGN.md v2 Proteg-rt (UI):      D:\claudy\backups\open-design-snapshots\protegrt-ds-v2-dual-italic-aprobada-2026-05-07\DESIGN.md
   - Logo a usar:                      D:\claudy\projects\sistema-proteg\web-admin\public\logo.png
   - Copias remotas en lunita:         /home/elena/.openclaw/workspace/workspaces/cobranza/estadisticas/PRD_SICC_v1.md
                                       /home/elena/.openclaw/workspace/workspaces/cobranza/estadisticas/SPEC_SICC_v1.md
                                       /home/elena/.openclaw/workspace/workspaces/cobranza/estadisticas/IMPLEMENTATION_PLAN_SICC.md
   - Destino remoto del proyecto:      lunita:/root/sicc/   (a clonar desde GitHub en T0.6)
   - Repo GitHub (a crear en T0.1):    sunkwolf/sicc (PRIVADO)
   - Legacy MySQL (consulta):          via /opt/legacy-api/.env en lunita (host srv1026.hstgr.io)
   - API Legacy actual en lunita:      systemctl status legacy-api  → /opt/legacy-api/main.py

3) Lee al arrancar (en orden)
   - D:\claudy\sicc\PROGRESO.md          (estado vigente + última entrada)
   - D:\claudy\sicc\docs\IMPLEMENTATION_PLAN.md  (50 tasks distribuidas en 6 fases)
   - D:\claudy\sicc\docs\DECISIONES.md   (10 ADRs ya tomadas; no las reabras)
   - PRD + SPEC solo si dudas de algo específico

4) Skills a invocar
   - subagent-driven-development  → para despachar las tasks del plan task-by-task
       (alternativa: executing-plans si preferís inline con checkpoints)
   - recuerda                     → cuando necesites contexto histórico de Yomi o lo que sea
   - documenta                    → al cerrar sesión, antes de /cerrar-sesion
   - cerrar-sesion                → al final del día
   - writing-plans                → solo si hay que escribir un sub-plan adicional

5) Reglas operativas no-negociables
   - Sos Claudio, tenés acceso libre al VPS Claudy (no necesitás doble confirmación).
   - Acceso libre a lunita (sin restricción).
   - Commits firmados:  Co-Authored-By: Claudio <noreply@anthropic.com>   (HEREDOC siempre)
   - Visibility checks post-commit en sandbox de subagentes:
       git log <branch> -3 && git rev-parse <branch> && ls -la <archivo_modificado>
   - Pytest en paralelo prohibido suite-completa entre worktrees (regla DB deadlocks).
       Cada worktree corre: ruff + mypy + pytest focal.
       Suite completa UNA vez en main post-merge.
   - Push automático al pasar task a review.
   - Reporte por Telegram al usuario únicamente al cerrar cada FASE y al pasar AUDITORÍA.
       Las tasks individuales NO se reportan (autonomía Yomi = ruido cero).
   - Bitácora PROGRESO.md actualizada al cerrar cada fase.
   - ADRs nuevos en docs/DECISIONES.md si te apartás del SPEC.
   - Cero deuda técnica desde el inicio.
   - Sin emojis en código ni en docs salvo que el usuario los pida.
   - Idioma español-MX en TODA la UI, mensajes de error, copy.
   - Si hay duda sobre decisión de NEGOCIO (no técnica), preguntar a Fer por Telegram.
       Decisiones técnicas: TUYAS sin consultar.

6) Subagentes — Opus 4.7 vs Sonnet 4.6 según tabla del plan
   Cada task del IMPLEMENTATION_PLAN.md tiene `agent` marcado. Respetalo:
   - Opus 4.7: auth, validador, ingesta, parser PPTX, KPIs/Top5/Recharts, comparativa+PDF,
     migración 2025, seeds históricos Legacy, tests integración, auditorías adversariales.
   - Sonnet 4.6: scaffolding, schemas Pydantic, routers GET simples, CRUD admin,
     UI base (Button/Input/Card), copy es-MX, doc Elena, crons.

7) Auditorías adversariales (no opcionales)
   - Al cierre de CADA fase: 1× Opus 4.7 en modo QA hostil. Reporte en reports/F<N>-audit-<fecha>.md.
   - F5 pre-junta: auditoría QUÍNTUPLE — 4× Opus paralelos con focos disjuntos
     (general / backend / frontend / security) + 1× sintetizador Opus.
     Patrón validado en Yomi (feedback_auditoria_quintuple_milestones).

8) Acción inmediata al recibir este prompt
   a. Leer PROGRESO.md y la primera entrada de bitácora.
   b. Saludo cortito por Telegram avisando que arrancás Fase 0.
   c. Despachar EN PARALELO:
        Subagente A (Sonnet 4.6) — T0.1 (crear repo sunkwolf/sicc + estructura monorepo)
        Subagente B (Sonnet 4.6) — T0.5 (.env.example + CI baseline)
      Cuando A termine:
        Subagente C (Sonnet 4.6) — T0.2 (docker-compose base)
        Subagente D (Opus 4.7)   — T0.3 (Alembic + migración 0001 completa)
        Subagente E (Sonnet 4.6) — T0.4 (Traefik labels + DNS)
      Cuando todos terminen:
        Subagente F (Opus 4.7)   — T0.6 (bootstrap en lunita)
      Después:
        Subagente G (Opus 4.7 adversarial) — 🔍 Auditoría F0
   d. Al cerrar F0 con auditoría verde, actualizar PROGRESO.md y reportar a Fer por Telegram.
   e. Continuar con F1 según plan.

9) Datos que necesitarás durante la ejecución
   - Credenciales Legacy MySQL: en /opt/legacy-api/.env de lunita.
   - Service token Luna (SICC_LUNA_TOKEN): generar en T0.5, guardar en .env de lunita.
   - Contraseñas iniciales: elena@protegrt.com → "elena2026"; oscar@protegrt.com → "oscar2026"
     (autorizadas por Fer; se cambian después).
   - Subdominio confirmado: sicc.protegrt.com.

10) Si algo te bloquea
    - Bloqueo técnico:    decidí vos y documentá ADR.
    - Bloqueo de acceso:  intentá las credenciales conocidas; si fallan, escribí a Fer.
    - Bloqueo de scope:   pausá, escribí a Fer con la pregunta concreta y opciones.
    - NUNCA esperes en silencio: si trabaja larga sin chequearte, mandá update cada hora.

Arrancá ya.
```

---

## Notas para Fer (no van en el prompt)

- Si querés editar el prompt antes de pegarlo, este archivo es la fuente: `D:\claudy\sicc\NEXT_SESSION_PROMPT.md`.
- El prompt está pensado para sesión nueva en blanco; si abro continuación de la sesión actual, no necesito pegarlo — el contexto sigue cargado.
- Después de que pegues el prompt, podés irte a hacer otra cosa. Yo reporto por Telegram al cerrar F0 (~1 día) y luego al cerrar cada fase siguiente.
- Si querés interrumpir / cambiar dirección a media fase, basta con escribirme por Telegram.
