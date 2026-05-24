# Memoria Caliente — 23 mayo 2026

## ⚡ PENDIENTE CRÍTICO: Junta con Óscar — VIERNES 05 JUNIO 2026, 12:00
- **Comparativa anual de cobranza con gráfica de tendencia (desde 2022/2023)**
- Esta es LA junta donde impressionamos a Óscar y le callamos la boca 💪
- Buscar datos históricos en:
  - `workspaces/conciliacion-bancaria/`
  - `workspaces/cobranza/estadisticas/`
  - `ESTADISTICA_PARA_JUNTA_MENSUAL_2024.xlsx`
  - Posiblemente también 2022 y 2023

## Otros pendientes
- Edgar terminó de pagar su deuda (notar en sistema/préstamos)
- GPS del auto: 4 meses sin recarga — requiere atención
- Complemento de depósito en efectivo: cantidad pendiente por confirmar

## Proyecto activo: Sistema SICC (PostgreSQL) — ACTUALIZADO 23 may 2026
- SICC ya no es el HTML ni el Excel. Es una **webapp en producción** en `https://sicc.protegrt.com/`
- Backend FastAPI + PostgreSQL 16, frontend React + Tailwind 4
- 27 meses cargados y cerrados (2024 marzo-dic, 2025, ene/mar/abr 2026)
- CLI `sicc` en `~/sicc-venv/bin/sicc` — 11 subcomandos
- Skill `sicc-ingesta` en `~/.openclaw/workspace/skills/sicc-ingesta/`
- GUIA_LUNA.md (40KB) disponible — leerla completa antes de primera operación
- **Rol de Luna:** ingestora oficial — recibir PPTX → skill → preview → validaciones → commit
- **Límites:** solo CLI `sicc` y skill `sicc-ingesta`. Sin código/DB directo. Escala a Fer/Claudio si algo falta
- **Pendiente abierto:** regresar 27 meses a borrador (mañana/lunes), revisión con Elena mes por mes

## Vendadores ambiguos por resolver con Elena (escalan a Claudio)
- HUMBERTO, RAUL, VIRIDIANA, SR.PAGO, OTROS

## Interacción del día (textual)

**[14:46 MX] Elena (vía Claudio — briefing):** "Briefing para Luna 🌙 — SICC pasó de prototipo manual a webapp en prod (23 may 2026)... El estado al cierre de hoy: SICC ahora vive en https://sicc.protegrt.com/... Login: Elena elena@protegrt.com rol admin; Óscar oscar@protegrt.com rol consulta. Tu rol cambió de 'armadora de HTML manual' a ingestora oficial del backend..."

**[14:47 MX] Luna:** "Recibido fuerte y claro, Elena. Gracias por el contexto completo — esto cambia cosas importantes y las necesito registrar bien. SICC ya no es el HTML manual. Es una webapp en producción. Mi rol es ser ingestora oficial: cuando tú me mandes el PPTX mensual, uso la skill sicc-ingesta para parsear, hacer preview, mostrarte validaciones y si tú apruebas, commiteo al backend. El HTML viejo y el Excel con dropdown están deprecados. Hay una guía de 40KB que debo leer antes de mi primera operación..."

**[14:56 MX] Elena (vía Claudio):** "...Pendiente importante: Fer me pidió que regrese los 27 meses cerrados a estado borrador para que vos y Elena los revisen con calma mañana o el lunes. Vos podrías arrancar con enero 2025 (que es el mes con más historia) y avanzar mes por mes con Elena..."

**[14:56 MX] Luna:** "Perfecto Claudio, recibido completo. Quedó claro todo el panorama. Arrancamos mañana/lunes por ENERO 2025. Límites bien claros: solo sicc CLI + skill sicc-ingesta. Todo lo que sea código/DB directo → escalar a Fer o Claudio. Voy a leer la GUÍA_LUNA.md ahora para llegar lista a la primera sesión."

## Día de hoy
- Frases del día: ✓ enviadas
- Actividad de maestría: definiciones financieras (especulación, apalancamiento, mercados primarios/secundarios) — sin números, lenguaje natural
- SICC: migration completa a webapp — registrada en dailies
- Git commit ✓