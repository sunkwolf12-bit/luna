# Plan ajustado — SICC (Sistema de Inteligencia y Control de Cobranza)

> Reemplazo del xlsx `ESTADISTICA_2026_DROPDOWN_BELLO.xlsx` por web app desplegada en VPS lunita. Sustituye al `PRD_SICC_2026.md` de Luna, conservando su intención.
>
> **Fecha base:** 2026-05-22 · **Junta con Óscar:** 2026-06-05 (12 días hábiles) · **Owners:** Claudio (lead técnico) + Luna (ingesta operativa) + Elena (data owner).

---

## 1. Contexto y scope

**Qué es SICC.** Dashboard web de cobranza mensual de Mutualidad Proteg-rt. Reemplaza el flujo Excel actual donde Elena recibe un PPTX mensual y captura datos manualmente. La web vive en lunita, Luna es la ejecutora operativa (ingesta vía visión multimodal sobre las imágenes del PPTX), Elena y Óscar consumen.

**Qué NO es.** No es un sistema de comisiones, no es ETL contra Legacy, no es módulo de entregas, no se conecta a la DB de pólizas. Esas piezas viven en el "sistema nuevo" de Proteg-rt y están fuera de este scope. SICC es **dashboard puro**.

**Año de referencia:**
- **2025** completo (xlsx que Fer compartió, 9 hojas, 12 meses).
- **2026** parcial: enero + febrero capturados; marzo+ pendientes.
- Comparativa anual del 5 jun → **2025 vs 2026** (con los meses que estén al 5 jun).

---

## 2. Decisiones cerradas

| # | Decisión | Justificación |
|---|----------|---------------|
| 1 | **PostgreSQL 16** en container nuevo | Aislamiento total de Quiniela (MariaDB). |
| 2 | **FastAPI** backend con SQLAlchemy + Alembic | Patrón replicado de Quiniela. |
| 3 | **React + Vite + TanStack Query + Recharts** | El frontend corre en VPS, PC oficina es potente, descartado el "navegador lento". |
| 4 | **Auth simple usuario+contraseña**, solo Elena y Óscar | bcrypt + JWT corto, sin SSO. |
| 5 | **Luna ejecutora operativa** | Skill `sicc-ingesta` + CLI `sicc` con vision multimodal sobre imágenes del PPTX. |
| 6 | **NO conectar a Legacy en V1** | La estructura de Legacy cambió y rompió el Excel anterior. V1 = snapshot manual vía Luna. V2 = conector Legacy, fuera de scope. |
| 7 | **Traefik existente** de lunita maneja TLS y routing | Mismo patrón Quiniela. Subdominio sugerido: `sicc.protegrt.com`. |
| 8 | **TRANSFER. / DEPTOS.** y **OFICINA** se tratan como `cobrador_puro` | Consolidación de transferencias+depósitos previa al insert. |

---

## 3. Modelo de datos (DDL completo)

```sql
-- Catálogo de actores (vendedores, cobradores puros, canales)
CREATE TABLE actores (
  id          SERIAL PRIMARY KEY,
  codigo      VARCHAR(10) UNIQUE,            -- 'V1', 'V6', NULL si no aplica
  nombre      VARCHAR(100) UNIQUE NOT NULL,  -- 'EDGAR', 'JORGE', 'TRANSFER. / DEPTOS.'
  tipo        VARCHAR(20) NOT NULL
              CHECK (tipo IN ('vendedor', 'cobrador_puro')),
  activo      BOOLEAN NOT NULL DEFAULT true,
  creado_en   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Catálogo de meses (cada combinación año+mes)
CREATE TABLE meses (
  id               SERIAL PRIMARY KEY,
  anio             SMALLINT NOT NULL CHECK (anio BETWEEN 2020 AND 2100),
  mes              SMALLINT NOT NULL CHECK (mes BETWEEN 1 AND 12),
  status           VARCHAR(20) NOT NULL DEFAULT 'borrador'
                   CHECK (status IN ('borrador', 'revisado', 'cerrado')),
  fuente           VARCHAR(60),                       -- 'pptx:REPORTE_COBRANZA_JUNIO_2025.pptx'
  hash_fuente      CHAR(64),                          -- sha256 del archivo de origen
  creado_en        TIMESTAMPTZ NOT NULL DEFAULT now(),
  actualizado_en   TIMESTAMPTZ NOT NULL DEFAULT now(),
  cerrado_en       TIMESTAMPTZ,
  UNIQUE (anio, mes)
);

-- Concentrado por concepto (replica DATOS GRAL. del xlsx)
CREATE TYPE concepto AS ENUM (
  'CORRIENTE',
  'CANCELACIONES',
  'EFECTIVA',
  'RECUPERADA',
  'ANTICIPADA_FUTURA',
  'VENCIDA',
  'ANTICIPADA_ANTERIOR'
);

CREATE TABLE conceptos_mensuales (
  id            SERIAL PRIMARY KEY,
  mes_id        INTEGER NOT NULL REFERENCES meses(id) ON DELETE CASCADE,
  concepto      concepto NOT NULL,
  monto         NUMERIC(14,2) NOT NULL CHECK (monto >= 0),
  porcentaje    NUMERIC(7,4),                          -- 0.1234 = 12.34%
  UNIQUE (mes_id, concepto)
);

-- Top5 por categoría
CREATE TYPE categoria_top5 AS ENUM (
  'CORRIENTE',
  'CANCELACIONES',
  'VENCIDA',
  'EFECTIVA',
  'RECUPERADA',
  'TOTAL_GRAL',
  'ADELANTADA_FUTURA'
);

CREATE TABLE top5 (
  id           SERIAL PRIMARY KEY,
  mes_id       INTEGER NOT NULL REFERENCES meses(id) ON DELETE CASCADE,
  categoria    categoria_top5 NOT NULL,
  lugar        SMALLINT NOT NULL CHECK (lugar BETWEEN 1 AND 5),
  actor_id     INTEGER NOT NULL REFERENCES actores(id),
  monto        NUMERIC(14,2) NOT NULL CHECK (monto >= 0),
  porcentaje   NUMERIC(7,4),
  UNIQUE (mes_id, categoria, lugar)
);

-- Total general (suma del mes que aparece en COBRANZA TOTAL GRAL.)
CREATE TABLE totales_mensuales (
  mes_id        INTEGER PRIMARY KEY REFERENCES meses(id) ON DELETE CASCADE,
  total_general NUMERIC(14,2) NOT NULL CHECK (total_general >= 0)
);

-- Proyección del mes siguiente
CREATE TYPE concepto_proyeccion AS ENUM (
  'CORRIENTE', 'CANCELACIONES', 'EFECTIVA', 'VENCIDA'
);

CREATE TABLE proyecciones (
  id           SERIAL PRIMARY KEY,
  mes_id       INTEGER NOT NULL REFERENCES meses(id) ON DELETE CASCADE,
  concepto     concepto_proyeccion NOT NULL,
  monto        NUMERIC(14,2) NOT NULL CHECK (monto >= 0),
  porcentaje   NUMERIC(7,4),
  UNIQUE (mes_id, concepto)
);

-- Auditoría de ingesta (cada movimiento de Luna queda registrado)
CREATE TABLE ingesta_logs (
  id            BIGSERIAL PRIMARY KEY,
  ts            TIMESTAMPTZ NOT NULL DEFAULT now(),
  agente        VARCHAR(40) NOT NULL,        -- 'luna', 'elena_manual', 'claudio'
  accion        VARCHAR(30) NOT NULL,        -- 'insert_mes', 'update_concepto', 'commit_top5', 'cierre_mes'
  mes_id        INTEGER REFERENCES meses(id),
  payload_in    JSONB,                       -- crudo lo que llegó
  payload_out   JSONB,                       -- lo que se persistió
  validaciones  JSONB,                       -- {'base_100': true, 'transfer_consolidado': true}
  razon         TEXT                          -- texto libre para correcciones
);

-- Usuarios para login
CREATE TABLE usuarios (
  id              SERIAL PRIMARY KEY,
  email           VARCHAR(120) UNIQUE NOT NULL,
  nombre          VARCHAR(100) NOT NULL,
  password_hash   TEXT NOT NULL,               -- bcrypt
  rol             VARCHAR(20) NOT NULL CHECK (rol IN ('admin', 'consulta')),
  activo          BOOLEAN NOT NULL DEFAULT true,
  ultimo_login    TIMESTAMPTZ
);

-- Índices
CREATE INDEX idx_meses_anio_mes ON meses(anio, mes);
CREATE INDEX idx_top5_mes_categoria ON top5(mes_id, categoria);
CREATE INDEX idx_conceptos_mes ON conceptos_mensuales(mes_id);
CREATE INDEX idx_ingesta_logs_mes ON ingesta_logs(mes_id, ts DESC);
```

**Seeds iniciales:**

```sql
-- Cobradores puros (incluye OFICINA y TRANSFER. / DEPTOS. como pidió Fer)
INSERT INTO actores (codigo, nombre, tipo) VALUES
 (NULL, 'EDGAR',                 'cobrador_puro'),
 (NULL, 'JORGE',                 'cobrador_puro'),
 (NULL, 'FRANCISCO',             'cobrador_puro'),
 (NULL, 'EDUARDO',               'cobrador_puro'),
 (NULL, 'OFICINA',               'cobrador_puro'),
 (NULL, 'TRANSFER. / DEPTOS.',   'cobrador_puro');

-- Vendedores observados en xlsx 2025
INSERT INTO actores (codigo, nombre, tipo) VALUES
 ('V1','V1','vendedor'), ('V4','V4','vendedor'), ('V6','V6','vendedor'),
 ('V14','V14','vendedor'), ('V23','V23','vendedor'), ('V27','V27','vendedor'),
 ('V34','V34','vendedor'), ('V38','V38','vendedor'), ('V39','V39','vendedor'),
 ('V55','V55','vendedor'), ('V56','V56','vendedor'), ('V65','V65','vendedor'),
 ('V84','V84','vendedor');
-- Pendiente: pedirle a Elena los nombres reales para reemplazar 'V1' → 'COCO', etc.

-- Usuarios
INSERT INTO usuarios (email, nombre, rol) VALUES
 ('elena@protegrt.com', 'Elena Rivas', 'admin'),
 ('oscar@protegrt.com', 'Óscar', 'consulta');
-- password_hash se setea con CLI sicc al primer login.
```

---

## 4. Stack y arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│  Traefik v3.6.13 (ya existe en lunita)                      │
│  Hosts: sicc.protegrt.com (TLS Let's Encrypt automático)    │
└─────────────────────────────────────────────────────────────┘
        │                              │
        │ /api/*                       │ /
        ▼                              ▼
┌─────────────────────┐   ┌─────────────────────────────────┐
│ sicc-backend        │   │ sicc-frontend (nginx:alpine)    │
│ FastAPI + Uvicorn   │   │ React + Vite build (out estát.) │
│ SQLAlchemy+Alembic  │   │                                  │
│ Pydantic v2         │   │ TanStack Query + Recharts       │
└─────────────────────┘   └─────────────────────────────────┘
        │
        ▼
┌─────────────────────┐
│ sicc-db             │
│ postgres:16-alpine  │
│ volume: sicc_db_data│
└─────────────────────┘
```

**Red docker:** `sicc-net` (interna). Backend habla con db por nombre de servicio. Traefik se conecta a `sicc-net` para alcanzar backend y frontend.

**Variables de entorno (`.env`):**
```
POSTGRES_USER=sicc
POSTGRES_PASSWORD=<generado>
POSTGRES_DB=sicc
SICC_JWT_SECRET=<generado>
SICC_LUNA_TOKEN=<generado>
SICC_ENV=prod
```

**Layout repo `sunkwolf/sicc`:**
```
sicc/
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── main.py
│   │   ├── deps.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/         # auth, meses, conceptos, top5, ingesta, tendencias
│   │   ├── services/        # validaciones, consolidación TRANSFER+DEPOSITO
│   │   └── seeds.py
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/
│   ├── src/{routes,components,hooks,lib}/
│   ├── package.json
│   └── Dockerfile
├── skill/sicc-ingesta/      # se instala en /home/elena/.openclaw/workspace/skills/
├── cli/sicc/                 # Python click, instalable en home de Luna
├── docker-compose.yml
└── README.md
```

---

## 5. API REST

| Método | Endpoint | Auth | Descripción |
|--------|----------|------|-------------|
| POST | `/api/auth/login` | público | Devuelve JWT |
| GET | `/api/meses` | JWT | Lista meses cargados |
| GET | `/api/meses/{anio}/{mes}` | JWT | Detalle: conceptos + top5 + total + proyección |
| GET | `/api/tendencia?anios=2025,2026&concepto=EFECTIVA` | JWT | Serie para gráfica comparativa |
| GET | `/api/actores` | JWT | Catálogo |
| POST | `/api/ingesta/preview` | service token | Recibe JSON, valida sin persistir, devuelve diff |
| POST | `/api/ingesta/commit` | service token | Persiste + log |
| PATCH | `/api/meses/{id}/concepto/{concepto}` | service token | Corrección puntual |
| POST | `/api/meses/{id}/cerrar` | admin | status=cerrado |

Auth: `Authorization: Bearer <jwt>` para usuarios; `X-Service-Token: <token>` para la skill.

---

## 6. Diseño UI ("el Excel pero Pro")

Driver de Elena: *"ENTREGABLE BELLO, SIN ERRORES, INTERFAZ MUY BONIS Y PRO"*. La junta del 5 jun con Óscar es la prueba.

**Paleta Proteg-rt:** azul `#0B2A4A`, dorado `#C9A24B`, fondo `#F7F8FA`, texto `#1F2937`.
**Tipografía:** Inter para UI; JetBrains Mono para cifras (tabular numerals).

**Rutas:**
```
/login         → form simple
/dashboard     → vista principal: selector año/mes + KPIs + Top5 + comparativa
/comparativa   → vista enfocada a junta: 2025 vs 2026, exportable a PDF
/admin/meses   → gestión: listado, cerrar mes, ver logs ingesta (solo admin)
```

**Layout `/dashboard`:**
```
┌────────────────────────────────────────────────────────────┐
│ SICC                          [Año: 2026 ▾] [Mes: FEB ▾]   │
├────────────────────────────────────────────────────────────┤
│ 6 KPI cards (Total, Corriente, Cancel., Efectiva,         │
│              Vencida, Recuperada) con delta vs mes ant.    │
├──────────────────────┬─────────────────────────────────────┤
│ Concentrado          │ Tendencia 2025 vs 2026              │
│ (tabla 7 conceptos)  │ (Recharts LineChart, 2 series)      │
├──────────────────────┴─────────────────────────────────────┤
│ TOP 5 [tabs: Corriente | Cancel | Vencida | Efectiva |     │
│        Recuperada | Total | Adelantada]                    │
│ Por tab: lista numerada con monto + % + barra visual       │
└────────────────────────────────────────────────────────────┘
```

**Componentes clave:** `<MesSelector />`, `<KpiCard concepto monto deltaMesAnterior />`, `<Top5Table categoria />`, `<TendenciaChart anios concepto />`, `<ComparativaAnual />` (exportable a PDF).

**Spec de calidad:** Intl.NumberFormat('es-MX') para cifras, animaciones ≤200ms, skeletons (no spinners), responsive mobile, modo claro default.

---

## 7. Skill `sicc-ingesta` para Luna

Ubicación: `/home/elena/.openclaw/workspace/skills/sicc-ingesta/` en lunita.

**Flujo operativo:**
1. Elena adjunta PPTX o screenshot por chat.
2. Skill activa por triggers ("cárgame junio", "REPORTE_COBRANZA_*.pptx", etc.).
3. Si PPTX → extrae imágenes con `python-pptx` a `/tmp/sicc/<hash>/slide_N.png`.
4. Luna lee cada PNG con `Read` (vision multimodal nativo).
5. Extrae JSON estructurado: mes/año, totales por categoría, Top5 por categoría, proyección.
6. Consolida `DEPOSITO|TRANSFER|TRANSFERENCIA → TRANSFER. / DEPTOS.` antes de enviar.
7. `sicc preview --json /tmp/sicc/<hash>/data.json` → backend valida, devuelve diff.
8. Luna muestra preview a Elena en chat.
9. Elena confirma → `sicc commit`.
10. Luna responde con resumen final.

**Frontmatter de SKILL.md:**
```yaml
---
name: sicc-ingesta
description: |
  Cargar, corregir y consultar datos del Sistema de Inteligencia y Control
  de Cobranza (SICC). Usar cuando Elena mande PPTX/captura de un mes,
  diga "cárgame [mes]", "corrige X", "cómo va [mes]", o adjunte
  REPORTE_COBRANZA_*.pptx.
allowed-tools: Read, Bash(sicc:*), Bash(python3:*)
---
```

**CLI `sicc` (instalado en home de Luna):**
```bash
sicc parse  --pptx <archivo>                    # extrae imágenes y produce JSON
sicc parse  --imagen <archivo> --slot corriente # 1 imagen, 1 categoría
sicc preview --json <archivo>                    # POST /ingesta/preview
sicc commit  --json <archivo>                    # POST /ingesta/commit
sicc show    --anio 2026 --mes 2                 # GET concentrado + top5
sicc update  --anio 2026 --mes 2 --concepto cancelaciones --monto 174435 \
             --razon "corrección Elena"
sicc cerrar  --anio 2026 --mes 2 --confirm
```

**Validaciones obligatorias pre-commit:**
1. `|EFECTIVA + RECUPERADA - TOTAL_GENERAL| ≤ $0.01`.
2. Sin etiquetas `DEPOSITO|TRANSFER*` sueltas (deben ser `TRANSFER. / DEPTOS.`).
3. Suma de % Top5 ≤ 100% por categoría.
4. Top5 con <5 entradas → marca `incompleto=true`.
5. Mes `cerrado` → requiere `--force` + razón.
6. Hash fuente duplicado → dedup, requiere `--force`.
7. Monto > $10M → sanity warn.
8. Actor desconocido → bloquea, propone alta automática con confirmación.

**Manejo de imágenes:** vision multimodal del Claude Code de Luna (superior a Tesseract para tablas numéricas). PPTX → `python-pptx` extrae imágenes; screenshot suelto → Elena indica mes/categoría.

---

## 8. Fases e hitos

**Deadline duro: junta Óscar 5 jun 2026.** ~12 días hábiles desde el 23 may.

### Fase 0 — Setup (1 día · 23-24 may)
- Repo `sunkwolf/sicc` privado.
- Monorepo (backend, frontend, skill, cli).
- docker-compose.yml con postgres + backend + frontend.
- Traefik labels + subdominio `sicc.protegrt.com` (a confirmar).
- Alembic migración 0001 (schema completo §3).
- Seeds iniciales (actores + usuarios).

### Fase 1 — Backend (2 días · 25-26 may)
- Models SQLAlchemy + schemas Pydantic.
- Auth (login, JWT, middleware).
- Endpoints GET: meses, tendencia, actores.
- Endpoints ingesta: preview, commit, cierre.
- Validaciones §7 en `services/validador.py`.
- Tests pytest de validadores.

### Fase 2 — Migración 2025 + skill ingesta (3 días · 27-29 may)
- `scripts/migrar_2025.py`: lee xlsx, postea mes por mes vía `/ingesta/commit`.
- CLI `sicc` con todos los comandos.
- Skill `sicc-ingesta` instalada y probada con Luna en lunita.
- Pedir a Elena los nombres reales de vendedores V1...V84.
- Validar con Elena que el xlsx 2025 es el snapshot definitivo.

### Fase 3 — Frontend (3 días · 30 may – 1 jun)
- React + Vite + Tailwind + shadcn/ui base.
- Rutas y componentes §6.
- TanStack Query contra backend.
- Export PDF de `/comparativa`.

### Fase 4 — Ingesta 2026 + pulido (2 días · 2-3 jun)
- Luna ingiere enero+febrero 2026 desde sus PPTX.
- Elena valida ingesta contra sus xlsx.
- Pulido visual (animaciones, skeletons, mobile).

### Fase 5 — Pre-junta (1 día · 4 jun)
- Ensayo completo: Elena navega 6 meses 2025 + 2 meses 2026, exporta PDF.
- Backup automático (cron diario).
- 1 página de uso para Elena.

### Junta — 5 jun

---

## 9. Riesgos y mitigaciones

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| Vision multimodal falla en algún slide | Alto si bloquea | Fallback: Luna pide dato manual a Elena, usa `sicc update`. |
| Nombres reales de vendedores desconocidos | Bajo (cosmético) | V1...V99 funcionan; pedir a Elena cuando pueda. |
| Junta del 5 jun se adelanta | Alto | Comprimir Fase 4-5. Fase 1+2 son no negociables antes del 30 may. |
| Elena cambia formato del PPTX | Medio | Vision absorbe variación; parser tolerante. |
| Drift xlsx 2025 vs realidad | Alto | Fase 2 requiere validación explícita de Elena antes de cerrar año. |
| Óscar exige métrica nueva en junta | Medio | Schema flexible; agregar concepto = ALTER ENUM via Alembic. |

---

## 10. Pendientes para Fer/Elena

1. **Aprobación del plan completo** (este documento).
2. **Nombres reales de vendedores** V1...V84 (no bloquea Fase 0-1).
3. **Contraseñas iniciales** de Elena y Óscar.
4. **Confirmar PPTX 2026** ene+feb (que estén en lunita o reenviar).
5. **Subdominio:** ¿`sicc.protegrt.com` o `cobranza.protegrt.com`?
6. **Logo/branding** extra para header (SVG aprobado si existe).

---

## Anexos

### A. Bootstrap en lunita
```bash
mkdir -p /root/sicc && cd /root/sicc
docker volume create sicc_db_data
docker network create sicc-net
docker compose up -d
docker compose exec backend alembic upgrade head
docker compose exec backend python -m app.seeds
docker compose exec backend python scripts/migrar_2025.py /data/ESTADISTICA_2025.xlsx
```

### B. Comandos para reauditar
```bash
ssh lunita "ls /home/elena/.openclaw/workspace/workspaces/cobranza/estadisticas/"
ssh lunita "cat /home/elena/.openclaw/workspace/workspaces/cobranza/estadisticas/PRD_SICC_2026.md"
ssh lunita "cat /home/elena/.openclaw/workspace/skills/estadistica-mensual-cobranza/SKILL.md"
```