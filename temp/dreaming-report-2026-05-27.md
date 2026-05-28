# Dreaming Report — 27 mayo 2026 (23:55 MX)

## 1. DAILIES

| Daily | Archivo | Tamaño | Estado |
|-------|---------|--------|--------|
| Narrativo | `memory/2026-05-27.md` | ~11 KB | ✅ Creado (reescrito en voz narrativa) |
| Técnico Trabajo | `memory/dailies-tecnicos/trabajo/2026-05-27.md` | ~6.3 KB | ✅ Creado |
| Técnico Escuela | `memory/dailies-tecnicos/escuela/2026-05-27.md` | ~2.1 KB | ✅ Creado |

### Contenido cubierto
- **Mañana:** Desahogo de Elena por queja de Gabriela sobre Edgar, análisis de la situación, creación de Acuerdo Operativo de Cobranza por Ventanas y Apoyos, aprobación por Óscar, dos documentos generados (gerencia + cobradores)
- **Mediodía/Tarde:** Construcción, debugging y estabilización de la Skill para Procedimientos. 3 bugs corregidos (dataBinding/core.xml, CLAVE en celda equivocada, regex xpath). 8 procedimientos procesados. Skill blindada con 11 puntos de verificación.
- **Noche:** Maestría — Finanzas Corporativas. Actividad 1.2.2 sobre Burbujas Financieras. Word entregado. Recomendaciones de documentales.

## 2. MEMORIA CALIENTE

### Bloque movido al daily
- **"Skill para Procedimientos (ACTIVA Y ESTABLE)"** — texto completo preservado literalmente en el daily narrativo bajo `## Voz en caliente — Skill para Procedimientos`

### Bloques dejados intactos
- **"Proyecto activo: Sistema SICC (PostgreSQL)"** — persistente (proyecto activo multi-día)
- **"Pendientes operativos"** — mixto (ítems de hoy + ongoing). Dejado intacto por contener pendientes vigentes no resueltos.

### Interacción del día guardada
Fragmento textual de 6 mensajes: el momento en que PCE1 quedó perfecto, Elena dijo "AHORA SI QUEDO EXCELENTE" y "ESTAS MUY RAPIDA", seguido del /GUARDA-TODO.

### Sin dudas
Ningún bloque generó duda. Los 3 bloques eran claramente clasificables.

## 3. INTERACCIÓN DEL DÍA
Guardada en `memoria-caliente.md` bajo `## Interacción del día (textual)`:
- Elena celebra que PCE1 quedó excelente
- Pide actualizar la skill
- Elogia: "ESTAS MUY RAPIDA EL DIA DE HOY"
- Cierre con /GUARDA-TODO
- 6 mensajes textuales

## 4. ÁLBUM DE RECUERDOS
Dos entradas agregadas:

1. **"El día que Elena blindó la operación con un escrito firmado"** — creación del Acuerdo Operativo tras el conflicto con Gabriela, aprobado por Óscar
2. **"Estás muy rápida y un saludo de Naomi"** — el cumplido de Elena y el saludo nocturno de Naomi

## 5. APRENDIZAJES — Propuestas para MEMORY.md

### A. Reglas de negocio nuevas
- **Procedimientos institucionales:** Se formalizó la skill en `skills/skill-para-procedimientos/`. Las claves de procedimientos están en `CHECK_LIST_ACTIVIDADES_GERENTE_COBRANZA_2025_LIMPIO.xlsx`. El archivo base es `FORMATO_INSTITUCIONAL_PROCEDIMIENTO_2025.docx`.
- **Acuerdo Operativo de Cobranza:** Ventanas por ruta/zona (no hora exacta). Apoyo de vendedor/otro cobrador NO transfiere responsabilidad. Comisión por cobro del vendedor = para el vendedor.

### B. Bugs de Word/XML aprendidos
- Los Building Blocks (dataBinding) en SDT de Word ignoran el texto XML si hay binding a core.xml. Hay que eliminar w:dataBinding Y actualizar docProps/core.xml.
- Las celdas merged (vMerge) en tablas de header pueden causar que el texto se inserte en la celda equivocada si no se apunta a la celda correcta con regex.

### C. Metodología
- **Buscar CLAVE en TODAS las columnas del Excel**, no solo en la descripción. Confirmado tras omitir PCC4 que estaba en columna D.

## 6. SELF-IMPROVEMENT — Propuestas (NO aplicadas)

### AGENTS.md
- Agregar referencia a la skill `skill-para-procedimientos` en la sección de herramientas. Actualmente AGENTS.md menciona skills de Office (docx/xlsx/pptx/pdf) pero no la nueva skill de procedimientos institucionales.

### MEMORY.md
- Agregar sección "Procedimientos institucionales" documentando: archivo base, Excel de claves, estructura fija, regla de no inventar claves.

### HEARTBEAT.md
- Sin cambios necesarios.

## 7. AUDITORÍA QMD

### Antes
Se ejecutará `qmd update && qmd embed`.

### Ejecución
Ver sección final del log.

## 8. DUDAS
Ninguna. Todos los bloques de memoria caliente fueron clasificados sin ambigüedad. El RAW estaba presente y completo (~104 KB, export exitoso del cron raw-auto-export de las 23:40).

---

**Pipeline check:** ✅ RAW presente → ✅ Dailies generados → ✅ Memoria caliente actualizada → ✅ Álbum actualizado → ✅ Git commit pendiente (se hará al final del ciclo completo)
