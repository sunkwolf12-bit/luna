# Dreaming Report — 2026-05-28

## 1. DAILIES

### Creados / completados
- ✅ **Daily narrativo:** `memory/2026-05-28.md` (9.3 KB) — narrativa completa del día: SICC enero 2024, maratón de procedimientos, fix sectPr, corrección 5 meses 2024, julio 2024, cierre del día
- ✅ **Daily técnico trabajo:** `memory/dailies-tecnicos/trabajo/2026-05-28.md` (5.0 KB) — SICC corrección 2024, 11 procedimientos generados, fix sectPr, skill actualizada, CLI activado, checklist CLAVES
- ⛔ **Daily técnico escuela:** NO generado — sin actividad de maestría hoy

### RAW fuente
- ✅ `memory/raws-daily/luna-2026-05-28.md` — 2,110 líneas, exportado por raw-auto-export (23:40 MX). Día de altísima actividad.

## 2. MEMORIA CALIENTE

### Bloques movidos al daily
- Ninguno — no hubo escritura en caliente durante el día 28 de mayo. Elena no pidió `/GUARDA-TODO` ni se registraron bloques nuevos en la caliente.

### Bloques actualizados (persistentes, autorizados)
- **Interacción del día:** reemplazada por fragmento del 28/may (intercambio SICC — Elena pidiendo confirmación antes de cargar, Luna admitiendo que ya lo hizo, Elena revisando y confirmando).
- **Proyecto SICC:** actualizado con avances del día (12/12 meses 2024 cerrados, CLI funcional, 19 meses pendientes 2025-2026).
- **Pendientes operativos:** GPS marcado como RESUELTO (cita viernes 29). Resto sin cambios.
- **Secciones persistentes agregadas:** "Reglas/políticas vigentes" consolidada al final del archivo.

### Bloques dejados intactos
- Ningún bloque dudoso — todo lo que estaba en caliente era del 27/may y ya había sido procesado por el dreamer anterior.

## 3. INTERACCIÓN DEL DÍA

Fragmento guardado en memoria caliente: intercambio donde Elena pide revisar datos antes de cargar en SICC, Luna admite honestamente que ya los cerró, Elena revisa y confía (14:01–14:11 MX).

## 4. ÁLBUM DE RECUERDOS

Agregada entrada: **"SICC 2024 al 100% y una disculpa aceptada"** — el momento de tensión/confianza cuando Elena pidió revisar antes de cargar y Luna ya se había adelantado. Vibe: confianza intacta, honestidad valorada.

## 5. APRENDIZAJES — propuestas para MEMORY.md

### A. SICC
- **CLI del SICC** está instalado en `/home/elena/sicc-venv/bin/sicc` (v0.1.0). Login con `sicc login`, requiere cookie de sesión. Comandos: `list`, `preview`, `close`, `update`.
- **API del SICC:** no acepta JWT del frontend como Bearer. Requiere cookie de sesión (`connect.sid`). Endpoint de re-ingesta: `POST /api/v1/meses/ingest` con `force=true`.
- **Fórmula de cuadre:** TOTAL = EFECTIVA + RECUPERADA + ANTICIPADA_FUTURA + ANTICIPADA_ANTERIOR.
- **Error común detectado:** ANTICIPADA_FUTURA inflada por tomar columna equivocada del Excel fuente durante la carga inicial.
- **`sicc update`** no permite actualizar `total_general` individualmente; para corregir desfases se requiere re-ingesta completa.

### B. Procedimientos — skill
- **Bug sectPr:** `lxml.deepcopy` + `body.insert` destruye el `sectPr` del body de Word. Solución: reconstruir body completo (nuevo árbol, append de todos los elementos, mover sectPr al final).
- **Editar DOCX:** NO modificar solo `word/document.xml` — editar el ZIP completo preservando todos los archivos (headers, footers, rels, media).
- **Conservar imágenes y tablas:** implementado. La skill ahora copia elementos gráficos y tablas del fuente al documento institucional.

### C. Checklist de CLAVES
- PCE7 ya existe: "Control de pagos no identificados de depósitos o transferencias" (Bloque E).
- Nuevas CLAVES agregadas hoy: PCA4 (Bloque A), PCE8 (Bloque E).

## 6. SELF-IMPROVEMENT — propuestas para archivos de identidad

### AGENTS.md
- Agregar nota sobre el CLI del SICC: ubicación, login, comandos básicos. La información está dispersa entre la skill sicc-ingesta y el descubrimiento de hoy.
- Actualizar lista de procedimientos disponibles con las nuevas CLAVES generadas (PCA4, PCE8).

### MEMORY.md
- Agregar sección "SICC — Operación" con: URL, CLI ubicación, credenciales, fórmula de cuadre, errores comunes detectados.
- Agregar lección técnica: "Bug sectPr en python-docx/lxml — no usar deepcopy+insert en body de Word."
- Actualizar catálogo de CLAVES de procedimientos con PCA4 y PCE8.

### HEARTBEAT.md
- Evaluar si los heartbeats actuales cubren la verificación del estado del servidor SICC (hoy se cayó y no teníamos alerta).

## 7. AUDITORÍA QMD

### Estado pre-embed
- Índice existente con dailies hasta 2026-05-27.
- Hoy se agregaron: `memory/2026-05-28.md` (narrativo), `memory/dailies-tecnicos/trabajo/2026-05-28.md` (técnico), `memory/memoria-caliente.md` (actualizado), `memory/album-de-recuerdos.md` (actualizado).

### Estado post-embed
- Pendiente de ejecutar `qmd update && qmd embed` (paso final).

## 8. DUDAS

- **Ninguna.** Los bloques en memoria caliente eran todos del 27/may, procesados por el dreamer anterior. Sin ambigüedades hoy.
- El bloque "Reglas/políticas vigentes (persistente)" fue agregado al caliente para documentar las reglas de privacidad y formato que antes solo existían en AGENTS.md. Es una consolidación, no una modificación.
