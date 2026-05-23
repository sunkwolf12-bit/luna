# PRD — Sistema de Inteligencia y Control de Cobranza (SICC)

> **Versión:** 1.0 · **Fecha:** 2026-05-22 · **Autor:** Claudio · **Reemplaza:** `PRD_SICC_2026.md` de Luna (incompleto)
> **Estado:** propuesta para aprobación · **Stakeholders:** Fer (sponsor), Elena (data owner), Óscar (consumer crítico), Luna (ejecutora operativa)

---

## 1 · Resumen ejecutivo

SICC es un **dashboard web de cobranza mensual** para Mutualidad Proteg-rt. Reemplaza el Excel artesanal que Elena mantiene cada mes con datos de la cobranza histórica. Vive en el VPS lunita como aplicación web propia (`sicc.protegrt.com`).

**El producto se centra en la presentación visual** — gráficas, KPIs y comparativas inter-anuales son el corazón. La pieza de fondo es la persistencia en una base de datos consultable; la captura mensual la opera **Luna** (agente Claude Code de Elena) en V1, y en V2 se elimina con un conector automático a la API de Legacy.

El producto **no es** ni un sistema contable, ni un ETL contra Legacy, ni una plataforma de comisiones, ni el "sistema nuevo" de Proteg-rt. Es **un visualizador de cifras de cobranza** con narrativa de tendencia y trazabilidad histórica.

**Volumen real:** poco — 7 conceptos × 12 meses × N años + Top5 (5 entradas × 7 categorías × 12 meses). En filas: ~5K por año. La inversión técnica va al **apartado visual y de comparativa**, no al backend.

---

## 2 · Problema que resuelve

### 2.1 Estado actual

Cada mes, Elena recibe un PPTX (`REPORTE COBRANZA <MES> <AÑO>.pptx`) con 10 slides que contienen capturas de pantalla del Excel maestro de cobranza. Manualmente ella:

1. Lee los slides uno por uno.
2. Captura las cifras a un Excel (`ESTADISTICA_2026_DROPDOWN_BELLO.xlsx` y variantes), con un formato de 9 hojas: 1 concentrado + 8 detalles (uno por categoría con Top5 por mes).
3. Cuando alguien pregunta cómo va un mes, abre el Excel y lo navega.
4. Para la junta mensual con Óscar, prepara comparativas anuales improvisadas.

### 2.2 Dolores reales

- **Captura manual** de números desde imágenes → propensa a errores tipográficos.
- **Drift entre archivos**: hay versiones `_VFINAL`, `_v2`, `_v3`, `_BELLO`, `_NUEVA`, `_CARGADO`. Nadie sabe cuál es la verdad.
- **Sin trazabilidad**: si alguien duda de un número, no hay registro de cuándo se cargó, de qué fuente, ni quién lo capturó.
- **Comparativa anual costosa**: Elena tarda horas en armar la comparativa con datos de años anteriores. Los xlsx anteriores tienen estructura distinta.
- **El Excel actual dejó de funcionar** porque se conectaba a Legacy y el schema de Legacy cambió en `empleados`. Elena no se ha atrevido a reconectarlo.
- **Contexto político**: la junta mensual con Óscar es un evento de exposición. Una hoja Excel se siente amateur; Óscar ha cuestionado la forma del entregable antes. Elena necesita un producto que **se vea profesional sin que ella tenga que hacer trabajo de diseño**.

### 2.3 Por qué ahora

Junta con Óscar el **5 de junio de 2026**. Elena pidió a Luna armar un xlsx "bonito digno de la junta". Luna entregó variantes pero el formato xlsx sigue siendo limitante. Fer decidió mover el entregable de Excel a web app: misma información, presentación profesional, datos persistentes, y un flujo operativo que escala más allá de la junta de junio.

---

## 3 · Usuarios y casos de uso

### 3.1 Personas

| Persona | Rol | Frecuencia de uso | Lo que necesita |
|---------|-----|-------------------|-----------------|
| **Elena** | Encargada de cobranza, data owner | Diaria/semanal | Consultar el mes actual, ver tendencia, validar que Luna cargó correctamente. |
| **Óscar** | Stakeholder ejecutivo | Mensual + ad-hoc | Llegar a la junta mensual con números claros. Consultar puntualmente desde su celular cuando le pasa algo por la cabeza. |
| **Luna** | Agente operadora (Claude Code de Elena, vive en lunita) | Por evento (1× al mes + correcciones) | Recibir PPTX/captura → ingerir a la DB → reportar a Elena. Responder consultas conversacionales ("Luna, ¿cómo va junio?"). |
| **Fer** | Sponsor técnico | Esporádica | Administración, ver logs, agregar usuarios. |
| **Claudio** | Lead técnico (yo) | Por evento | Mantenimiento, debugging, evolución. |

### 3.2 Casos de uso

**CU-1 — Consulta mensual de Elena.**
Elena abre `sicc.protegrt.com`, hace login, ve el dashboard con el mes vigente. Si necesita otro mes, lo selecciona. Cifras claras, Top5 visibles, tendencia respecto al mes anterior y al mismo mes del año anterior. Tiempo total: <30 segundos.

**CU-2 — Carga mensual por Luna.**
Elena recibe el PPTX del cierre del mes. Lo reenvía a Luna por chat. Luna:
1. Extrae imágenes de cada slide.
2. Lee cada imagen con vision multimodal.
3. Consolida `TRANSFER+DEPOSITO → TRANSFER. / DEPTOS.`.
4. Genera JSON candidato.
5. `sicc preview` → muestra a Elena el diff visual.
6. Elena confirma → `sicc commit` → datos persistidos.
Tiempo total: 3-5 minutos por mes.

**CU-3 — Corrección puntual.**
Elena nota que la cifra de Cancelaciones de febrero está mal. Le dice a Luna: *"corrige cancelaciones de febrero, debe ser $174,435, no $127,110"*. Luna ejecuta `sicc update --mes 2 --anio 2026 --concepto cancelaciones --monto 174435 --razon "<lo que Elena dijo>"`. El cambio queda registrado en `ingesta_logs`.

**CU-4 — Junta mensual con Óscar.**
Día de junta. Óscar abre la vista `/comparativa` desde su laptop o celular. Ve la comparativa anual del año actual vs el anterior con gráfica de tendencia. Exporta PDF para anexar al acta. Elena navega los detalles si surge una pregunta.

**CU-5 — Consulta conversacional con Luna.**
Elena por chat: *"Luna, ¿quién fue el #1 de Cobranza Vencida en marzo?"*. Luna ejecuta `sicc show --anio 2026 --mes 3 --categoria vencida` y responde en lenguaje natural.

**CU-6 — Cierre formal del mes.**
Cuando Elena ya validó los datos de un mes, marca el mes como `cerrado`. Una vez cerrado, ningún cambio puede entrar sin un override explícito con razón documentada.

---

## 4 · Alcance

### 4.1 Dentro de scope

- Captura, almacenamiento y consulta de cifras mensuales de cobranza para los 7 conceptos del concentrado (Corriente, Cancelaciones, Efectiva, Recuperada, Anticipada Futura, Vencida, Anticipada Anterior).
- Top5 mensual por cada una de las 7 categorías del reporte (Corriente, Cancelaciones, Vencida, Efectiva, Recuperada, Total General, Adelantada Futura).
- Total general del mes (combo de Efectiva + Recuperada + ajustes).
- Proyección del siguiente mes en 4 conceptos (Corriente, Cancelaciones, Efectiva, Vencida).
- Catálogo unificado de actores (vendedores con código V#, cobradores puros, OFICINA y TRANSFER./DEPTOS. como entidades virtuales).
- Comparativa anual (año actual vs años anteriores cargados) con gráfica de tendencia.
- Auditoría completa de cada movimiento (quién, cuándo, qué, desde qué fuente).
- Skill operativa para Luna (`sicc-ingesta`) + CLI auxiliar (`sicc`).
- Migración del histórico 2025 completo desde el xlsx que Elena ya tiene.

### 4.2 Fuera de scope (explícito)

- **Conexión live a Legacy en V1.** En V1, los datos vienen del snapshot mensual (PPTX/captura) ingerido por Luna. **V2 incorpora el conector automático** (ver §11 roadmap).
- **Comisiones, reglas de bloqueo de pago, módulo de entregas, KPI de tiempo de entrega.** Eso es del "sistema nuevo" de Proteg-rt, no del SICC.
- **Migración histórica 2022, 2023, 2024.** Solo se cargará si Elena tiene los archivos a la mano. No bloquea el lanzamiento.
- **Alertas/notificaciones push a vendedores morosos.** Spec separado si se quiere después.
- **Multi-empresa / multi-sucursal.** Una sola entidad (Proteg-rt).
- **App nativa móvil.** Web responsive cubre el caso móvil.

---

## 5 · Requisitos funcionales

### RF-1 — Autenticación
- Login por email + contraseña.
- 2 usuarios iniciales: Elena (rol `admin`), Óscar (rol `consulta`).
- Sin SSO, sin SMS, sin 2FA en V1.
- JWT con expiración 24h, refresh manual con re-login.

### RF-2 — Vista dashboard mensual (CORAZÓN VISUAL)
- Selector año + mes (sincronizados, animados en transición).
- **6 KPI cards prominentes**: Total General, Corriente, Cancelaciones, Efectiva, Vencida, Recuperada. Cada una con:
  - Monto principal grande en JetBrains Mono tabular-nums (Saira para acento ocasional).
  - Delta vs mes anterior (% + flecha + color verde/rojo).
  - Delta vs mismo mes del año anterior (cuando exista; tooltip o segunda línea).
  - Micro-sparkline de los últimos 6 meses al pie de cada card (línea de 1px navy-700 sobre crema, sin grid).
- **Gráfica de tendencia hero**: línea principal del año seleccionado + serie shadow del año anterior, métrica seleccionable (default Efectiva). Recharts con animación de entrada, tooltips elegantes, leyenda inline.
- Tabla "Concentrado" con los 7 conceptos del DATOS GRAL. (monto + %), tipográficamente refinada (no genérica).
- **Sección "Top 5"** con tabs por categoría (7 tabs). Cada Top5:
  - Lista numerada con número grande Saira italic accent.
  - Barra visual proporcional (gradient navy o gold-soft según posición).
  - Avatar / iniciales del actor (cuando es persona) o ícono lucide (cuando es OFICINA / TRANSFER./DEPTOS.).
  - Hover muestra tooltip con `nombre_completo` y stats del año.

### RF-3 — Vista comparativa (junta) — APARTADO ESTRELLA PARA ÓSCAR
- Vista enfocada para la junta mensual. Diseñada para verse impecable en 3 segundos.
- **Header narrativo:** "Cobranza Proteg-rt · año actual vs año anterior · cierre [mes]" en display Saira CAPS.
- **Big number hero:** total general del año actual con `.gold-foil` aplicado al monto.
- **Gráfica grande de tendencia** con todas las series anuales cargadas (multi-line, eje X = meses, leyenda años). Recharts con animaciones progresivas (stagger por serie).
- **Tabla comparativa por concepto:** año actual vs año anterior side-by-side con delta % iluminado.
- **Mini-cards de Top1/Top3** por categoría del año, con foto/inicial del actor.
- **Botón "Exportar a PDF"** → genera PDF con marca Proteg-rt listo para imprimir/anexar al acta. PDF respeta el design system completo (paleta, tipografía, layout). El PDF debe verse tan profesional como un report de Banorte/IXE.

### RF-4 — Vista admin (solo Elena/Fer)
- Listado de meses cargados con status (`borrador`, `revisado`, `cerrado`).
- Botón "Cerrar mes" (requiere confirmación).
- Visualización de `ingesta_logs` por mes (quién hizo qué, cuándo).
- Gestión de actores (alta/edición de vendedores y cobradores).

### RF-5 — Ingesta por Luna
- Endpoint `POST /api/ingesta/preview` recibe JSON, valida, devuelve diff sin persistir.
- Endpoint `POST /api/ingesta/commit` persiste el JSON validado y registra en `ingesta_logs`.
- Endpoint `PATCH /api/meses/{id}/concepto/{concepto}` para correcciones puntuales.
- Validaciones obligatorias (cuadre Efectiva+Recuperada vs Total, sin etiquetas sueltas, sin actores desconocidos, dedup por hash de fuente, etc.).
- Logging completo con payload de entrada, salida y resultado de validaciones.

### RF-6 — Catálogo de actores
- Tabla `actores` con vendedores (código V#), cobradores puros, OFICINA, TRANSFER./DEPTOS.
- Cada actor con link opcional a `id_empleado` de Legacy para trazabilidad.
- Alta/edición desde vista admin.
- Alta automática propuesta por la skill cuando aparece un actor desconocido (requiere confirmación humana).

### RF-7 — Consulta histórica
- Cualquier mes cargado es accesible desde la UI sin restricción.
- Mes cerrado se muestra con badge "CERRADO" y no admite edición sin override.

### RF-8 — Backup automático
- Snapshot diario de la DB a `/srv/backups/sicc/` con retención 30 días (igual que Quiniela).

---

## 6 · Requisitos no funcionales

| Req | Spec |
|-----|------|
| **Rendimiento** | Dashboard inicial <1.5s en LAN, <2.5s en celular vía 4G. |
| **Disponibilidad** | Best-effort. Sin SLA formal. Backup diario protege contra pérdida. |
| **Seguridad** | TLS Let's Encrypt vía Traefik, contraseñas bcrypt, JWT con expiración, service token para Luna rotable. |
| **Privacidad** | Sin telemetría externa. Sin analytics de terceros. Logs solo locales. |
| **Compatibilidad** | Chrome/Edge/Safari últimas 2 versiones, iOS Safari 16+, Android Chrome. |
| **Idioma** | Español MX exclusivamente. Sin i18n en V1 (estructura preparada para futuro). |
| **Accesibilidad** | WCAG AA mínimo (contraste, focus visible, semántica). |
| **Responsive** | Funcional en mobile (375px+), tablet, desktop. Layout adapta. |
| **Estética** | Aplica DESIGN.md v2 de Proteg-rt aprobado el 7 may 2026 (paleta navy/gold/crema, tipografía Saira + Montserrat + JetBrains Mono, radius 0px editorial). |

---

## 7 · Criterios de éxito

### 7.1 Criterios de lanzamiento (5 jun 2026)

- [ ] Elena puede entrar desde su PC y celular, hacer login, navegar 6+ meses 2025 + meses 2026 disponibles.
- [ ] Óscar puede entrar desde su laptop, navegar a `/comparativa`, exportar PDF.
- [ ] Los 12 meses de 2025 están cargados y marcados como `cerrado`.
- [ ] Al menos los meses 2026 que Elena ya tiene capturados están en SICC.
- [ ] La skill `sicc-ingesta` está instalada en lunita y Luna sabe usarla (validado en un dry run con Elena).
- [ ] Backups diarios funcionando.

### 7.2 Métricas operativas post-lanzamiento (mes 1 post-junta)

- Tiempo de captura mensual por Luna: <10 minutos por mes (vs ~horas que tomaba Elena).
- Errores de captura detectados por Elena: 0 idealmente, <2 aceptable.
- Disponibilidad: >99% mensual.
- Latencia p95 del dashboard: <2s.

### 7.3 Métrica blanda (la importante)

Después de la junta del 5 jun, Elena reporta a Fer que **NO** sintió presión negativa por el formato del entregable. La conversación de la junta se centra en los números, no en cómo se presentaron.

---

## 8 · Decisiones de producto registradas

| # | Decisión | Por qué |
|---|----------|---------|
| 1 | Web app, no Excel mejorado | Trazabilidad + presentación profesional + ingesta automatizable. |
| 2 | Hosteado en lunita, no en Claudy | Aislamiento: cobranza no debe compartir infra con desarrollo. |
| 3 | Postgres propio (no MariaDB de Quiniela) | Aislamiento aplicación-por-aplicación. |
| 4 | Luna ejecutora, no captura humana | Elena ya delegó esta tarea a Luna. SICC formaliza el patrón. |
| 5 | Snapshot mensual, no live Legacy | Legacy es inestable; el flujo PPTX funciona. V2 evaluará conector. |
| 6 | React, no JS vanilla | El frontend corre en VPS, no hay restricción de navegador. |
| 7 | Auth simple email+password | 2 usuarios, sin necesidad de SSO ni 2FA en V1. |
| 8 | OFICINA y TRANSFER./DEPTOS. como cobradores puros virtuales | OFICINA es ubicación (V5 fue código erróneo histórico); TRANSFER./DEPTOS. es canal lógico. Pero deben competir en Top5 como si fueran actores. |
| 9 | Aplica DESIGN.md de Proteg-rt v2 | Sistema visual aprobado el 7 may 2026, dual italic, paleta navy+gold+crema. |

---

## 9 · Riesgos de producto

| Riesgo | Impacto | Plan |
|--------|---------|------|
| Junta del 5 jun se adelanta | Alto | Comprimir Fases 4-5; Fases 1-2 son no negociables antes del 30 may. |
| Elena cambia el formato del PPTX | Medio | Vision multimodal absorbe variación; parser tolerante. |
| Óscar exige métrica nueva en junta | Medio | Schema flexible; agregar concepto es ALTER ENUM con Alembic. |
| Vision multimodal falla en un slide | Medio | Fallback: Luna pide dato manual a Elena → `sicc update`. |
| Elena no adopta el flujo Luna | Alto si pasa | Diseño operativo de Fase 2: validación end-to-end con Elena en dry run, no entrega "ciega". |
| Datos históricos 2025 inconsistentes | Alto | Fase 2 requiere validación explícita de Elena antes de cerrar el año en DB. |

---

## 11 · Roadmap V2 y futuro

### V2 — Conector automático a Legacy API

Cuando la estructura de la tabla `empleados` de Legacy se estabilice y el equipo agregue endpoints al microservicio `legacy-api` (ubicado en `lunita:/opt/legacy-api/`), SICC pivotea a ingesta automática:

### Endpoint sugerido a agregar en `legacy-api`

```
GET /api/v1/reportes/cobranza-mensual?anio=2026&mes=6
  Auth: X-API-Key con rol admin
  Resp: <mismo JSON candidato definido en SPEC §4.3>
```

Ese endpoint hace los SELECTs contra `pagos`, `polizas`, `empleados`, consolida (incluyendo la lógica TRANSFER. / DEPTOS.), y devuelve el JSON listo para `POST /api/v1/ingesta/commit` de SICC.

### Cron de SICC en V2

```cron
0 7 1 * *  # día 1 de cada mes 07:00
  curl -H "X-API-Key: $LEGACY_KEY" \
       "https://legacy.protegrt.com/api/v1/reportes/cobranza-mensual?anio=$Y&mes=$M" \
    | curl -X POST -H "X-Service-Token: $SICC_LUNA_TOKEN" \
           -H "Content-Type: application/json" --data-binary @- \
           "https://sicc.protegrt.com/api/v1/ingesta/commit"
```

Luna sigue siendo responsable de **correcciones operativas y consultas conversacionales**, pero ya no de la carga periódica.

### Por qué no V1

- Estructura de Legacy aún inestable (cambió `empleados` recientemente).
- Validar primero que la lógica de consolidación (TRANSFER. / DEPTOS., Top5 por sección con criterio dual VENDEDOR/COBRADO) funciona contra data real ingerida manualmente.
- Una vez que SICC viva con data validada por 1-2 meses, agregar el endpoint a `legacy-api` es trabajo pequeño (~1 día).

### Otros candidatos V2+ (no comprometidos)

- Vista por actor (ficha individual: "Top de Edgar en 2025-2026").
- Drill-down de un mes a sus pagos individuales (requiere conector Legacy live).
- Exportación a Excel del dashboard (paradójico pero útil para conciliación externa).
- Modo oscuro.

---

## 12 · Próximos pasos

1. Aprobación del PRD por Fer.
2. Aprobación del SPEC técnico complementario (documento separado).
3. Arranque Fase 0 (setup repo + infraestructura) al recibir luz verde.
4. Confirmación de Elena de:
   - Contraseña inicial (o aceptar `elena2026` temporal).
   - Si tiene PPTX 2026 enero+febrero o hay que pedirlos a Luna.
5. Confirmación de Óscar de:
   - Contraseña inicial (o aceptar `oscar2026` temporal).
6. Decisión sobre subdominio definitivo (`sicc.protegrt.com` recomendado).
