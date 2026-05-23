# SPEC — Sistema de Inteligencia y Control de Cobranza (SICC)

> **Versión:** 1.0 · **Fecha:** 2026-05-22 · **Autor:** Claudio · **Complementa:** PRD v1.0
> **Estado:** propuesta para aprobación · **Stack target:** Postgres 16 · FastAPI · React + Vite + Tailwind 4 · Traefik v3

---

## 1 · Arquitectura

### 1.1 Diagrama

```
                          Internet
                              │
                              ▼
                ┌─────────────────────────────┐
                │ Traefik v3 (lunita, existing) │
                │ sicc.protegrt.com → TLS LE    │
                └────────────┬─────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │ /api/*       │ /            │
              ▼              ▼              │
     ┌──────────────┐ ┌──────────────┐      │
     │ sicc-backend │ │ sicc-frontend│      │
     │ FastAPI      │ │ nginx:alpine │      │
     │ uvicorn      │ │ serves React │      │
     │ port:8001    │ │  build       │      │
     └──────┬───────┘ └──────────────┘      │
            │                               │
            ▼                               │
     ┌──────────────┐                       │
     │ sicc-db      │                       │
     │ postgres:16  │                       │
     │ volume:      │                       │
     │  sicc_db_data│                       │
     └──────────────┘                       │
                                            │
                                            │ (skill ingesta vive aquí)
                                            ▼
                              ┌──────────────────────┐
                              │ /home/elena/         │
                              │ skills/sicc-ingesta/ │
                              │ + ~/.local/bin/sicc  │
                              │ (Luna ejecuta)        │
                              └──────────────────────┘
```

### 1.2 Componentes

| Componente | Tech | Puerto | Responsable |
|-----------|------|--------|-------------|
| `sicc-db` | postgres:16-alpine | 5432 (interno) | Persistencia |
| `sicc-backend` | FastAPI + uvicorn + SQLAlchemy + Alembic + Pydantic v2 | 8001 (interno) | API REST, validaciones, auth, ingesta |
| `sicc-frontend` | nginx:alpine sirviendo build estático Vite | 80 (interno) | UI React |
| Traefik | v3.6.13 (existente en lunita) | 80/443 (público) | TLS, routing |
| Skill `sicc-ingesta` | Markdown bajo `/home/elena/.openclaw/workspace/skills/` | n/a | Operación de Luna |
| CLI `sicc` | Python click, instalable como `pipx install sicc-cli` o symlink | n/a | Cliente HTTP de la skill |

### 1.3 Red y red docker

- Red docker dedicada: `sicc-net`.
- `sicc-db` solo expone 5432 dentro de `sicc-net`. Backend conecta por nombre de servicio.
- `sicc-backend` y `sicc-frontend` conectados a `sicc-net` y a `traefik` (red existente).
- Traefik labels en backend y frontend para routing automático.

### 1.4 Variables de entorno

```env
# Postgres
POSTGRES_USER=sicc
POSTGRES_PASSWORD=<openssl rand -base64 32>
POSTGRES_DB=sicc

# Backend
SICC_DB_URL=postgresql+psycopg://sicc:<pass>@sicc-db:5432/sicc
SICC_JWT_SECRET=<openssl rand -base64 64>
SICC_JWT_EXPIRE_HOURS=24
SICC_LUNA_TOKEN=<openssl rand -base64 32>
SICC_CORS_ORIGINS=https://sicc.protegrt.com
SICC_ENV=production

# Frontend (build-time)
VITE_API_BASE=/api/v1
```

---

## 2 · Modelo de datos

### 2.1 DDL completo

```sql
-- ───────────────────────────────────────────────────────
-- ENUMs
-- ───────────────────────────────────────────────────────

CREATE TYPE tipo_actor AS ENUM ('vendedor', 'cobrador_puro');

CREATE TYPE concepto_concentrado AS ENUM (
  'CORRIENTE',
  'CANCELACIONES',
  'EFECTIVA',
  'RECUPERADA',
  'ANTICIPADA_FUTURA',
  'VENCIDA',
  'ANTICIPADA_ANTERIOR'
);

CREATE TYPE categoria_top5 AS ENUM (
  'CORRIENTE',
  'CANCELACIONES',
  'VENCIDA',
  'EFECTIVA',
  'RECUPERADA',
  'TOTAL_GRAL',
  'ADELANTADA_FUTURA'
);

CREATE TYPE concepto_proyeccion AS ENUM (
  'CORRIENTE', 'CANCELACIONES', 'EFECTIVA', 'VENCIDA'
);

CREATE TYPE status_mes AS ENUM ('borrador', 'revisado', 'cerrado');

CREATE TYPE rol_usuario AS ENUM ('admin', 'consulta');

-- ───────────────────────────────────────────────────────
-- Catálogos
-- ───────────────────────────────────────────────────────

CREATE TABLE actores (
  id                  SERIAL PRIMARY KEY,
  codigo              VARCHAR(10) UNIQUE,
  nombre              VARCHAR(100) UNIQUE NOT NULL,
  nombre_completo     VARCHAR(255),
  tipo                tipo_actor NOT NULL,
  id_empleado_legacy  INTEGER UNIQUE,
  activo              BOOLEAN NOT NULL DEFAULT true,
  notas               TEXT,
  creado_en           TIMESTAMPTZ NOT NULL DEFAULT now(),
  actualizado_en      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_actores_activo ON actores(activo) WHERE activo;
CREATE INDEX idx_actores_tipo ON actores(tipo);

CREATE TABLE usuarios (
  id              SERIAL PRIMARY KEY,
  email           VARCHAR(120) UNIQUE NOT NULL,
  nombre          VARCHAR(100) NOT NULL,
  password_hash   TEXT NOT NULL,
  rol             rol_usuario NOT NULL,
  activo          BOOLEAN NOT NULL DEFAULT true,
  ultimo_login    TIMESTAMPTZ,
  creado_en       TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ───────────────────────────────────────────────────────
-- Datos mensuales
-- ───────────────────────────────────────────────────────

CREATE TABLE meses (
  id              SERIAL PRIMARY KEY,
  anio            SMALLINT NOT NULL CHECK (anio BETWEEN 2020 AND 2100),
  mes             SMALLINT NOT NULL CHECK (mes BETWEEN 1 AND 12),
  status          status_mes NOT NULL DEFAULT 'borrador',
  fuente          VARCHAR(80),
  hash_fuente     CHAR(64),
  notas           TEXT,
  creado_en       TIMESTAMPTZ NOT NULL DEFAULT now(),
  actualizado_en  TIMESTAMPTZ NOT NULL DEFAULT now(),
  cerrado_en      TIMESTAMPTZ,
  cerrado_por     INTEGER REFERENCES usuarios(id),
  UNIQUE (anio, mes)
);

CREATE INDEX idx_meses_anio_mes ON meses(anio DESC, mes DESC);
CREATE INDEX idx_meses_status ON meses(status);

CREATE TABLE conceptos_mensuales (
  id            SERIAL PRIMARY KEY,
  mes_id        INTEGER NOT NULL REFERENCES meses(id) ON DELETE CASCADE,
  concepto      concepto_concentrado NOT NULL,
  monto         NUMERIC(14,2) NOT NULL CHECK (monto >= 0),
  porcentaje    NUMERIC(7,4),
  UNIQUE (mes_id, concepto)
);

CREATE INDEX idx_conceptos_mes ON conceptos_mensuales(mes_id);

CREATE TABLE totales_mensuales (
  mes_id          INTEGER PRIMARY KEY REFERENCES meses(id) ON DELETE CASCADE,
  total_general   NUMERIC(14,2) NOT NULL CHECK (total_general >= 0)
);

CREATE TABLE top5 (
  id           SERIAL PRIMARY KEY,
  mes_id       INTEGER NOT NULL REFERENCES meses(id) ON DELETE CASCADE,
  categoria    categoria_top5 NOT NULL,
  lugar        SMALLINT NOT NULL CHECK (lugar BETWEEN 1 AND 5),
  actor_id     INTEGER NOT NULL REFERENCES actores(id) ON DELETE RESTRICT,
  monto        NUMERIC(14,2) NOT NULL CHECK (monto >= 0),
  porcentaje   NUMERIC(7,4),
  UNIQUE (mes_id, categoria, lugar)
);

CREATE INDEX idx_top5_mes_categoria ON top5(mes_id, categoria);
CREATE INDEX idx_top5_actor ON top5(actor_id);

CREATE TABLE proyecciones (
  id         SERIAL PRIMARY KEY,
  mes_id     INTEGER NOT NULL REFERENCES meses(id) ON DELETE CASCADE,
  concepto   concepto_proyeccion NOT NULL,
  monto      NUMERIC(14,2) NOT NULL CHECK (monto >= 0),
  porcentaje NUMERIC(7,4),
  UNIQUE (mes_id, concepto)
);

-- ───────────────────────────────────────────────────────
-- Auditoría
-- ───────────────────────────────────────────────────────

CREATE TABLE ingesta_logs (
  id            BIGSERIAL PRIMARY KEY,
  ts            TIMESTAMPTZ NOT NULL DEFAULT now(),
  agente        VARCHAR(40) NOT NULL,
  accion        VARCHAR(40) NOT NULL,
  mes_id        INTEGER REFERENCES meses(id) ON DELETE SET NULL,
  payload_in    JSONB,
  payload_out   JSONB,
  validaciones  JSONB,
  razon         TEXT,
  ip_origen     INET,
  user_agent    TEXT
);

CREATE INDEX idx_ingesta_logs_mes ON ingesta_logs(mes_id, ts DESC);
CREATE INDEX idx_ingesta_logs_agente ON ingesta_logs(agente, ts DESC);

-- ───────────────────────────────────────────────────────
-- Triggers de auditoría
-- ───────────────────────────────────────────────────────

CREATE OR REPLACE FUNCTION tr_set_actualizado_en()
RETURNS TRIGGER AS $$
BEGIN
  NEW.actualizado_en = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_meses_actualizado_en
  BEFORE UPDATE ON meses
  FOR EACH ROW EXECUTE FUNCTION tr_set_actualizado_en();

CREATE TRIGGER trg_actores_actualizado_en
  BEFORE UPDATE ON actores
  FOR EACH ROW EXECUTE FUNCTION tr_set_actualizado_en();
```

### 2.2 Vistas materializadas (performance)

```sql
-- Tendencia anual para gráficas (refresh nocturno)
CREATE MATERIALIZED VIEW mv_tendencia_anual AS
SELECT
  m.anio, m.mes,
  cm.concepto,
  cm.monto,
  cm.porcentaje
FROM meses m
JOIN conceptos_mensuales cm ON cm.mes_id = m.id
WHERE m.status IN ('revisado', 'cerrado');

CREATE UNIQUE INDEX idx_mv_tendencia_unique
  ON mv_tendencia_anual(anio, mes, concepto);

-- Refresh:
-- REFRESH MATERIALIZED VIEW CONCURRENTLY mv_tendencia_anual;
```

### 2.3 Seeds iniciales y catálogo histórico

**Estrategia de actores:**
1. **Seed inicial mínimo** (ver SQL abajo): solo los 4 cobradores puros reales activos + 2 entidades virtuales (OFICINA, TRANSFER./DEPTOS.) + 15 vendedores activos.
2. **Pre-seed histórico** ejecutado ANTES de migrar el xlsx 2025: script `scripts/seed_actores_historicos.py` consulta la tabla `empleados` de Legacy (vía `lunita:/opt/legacy-api/`) y trae **TODOS** los empleados con `es_vendedor=1 OR es_cobrador=1`, sin filtrar `activo`. Los inactivos entran a `actores` con `activo=false` y su `id_empleado_legacy` mapeado.
3. **Alta automática durante ingesta:** si un Top5 histórico menciona un actor que no está en el catálogo (no encontró match en Legacy o nunca existió como empleado), se da de alta con `activo=false` y queda en `ingesta_logs` para revisión.

**Semántica del flag `activo`:**
- `true` → aparece en dropdowns de UI y sugerencias de Top5 nuevo.
- `false` → NO aparece en dropdowns, PERO sigue siendo visible y consultable en cualquier mes histórico donde aparezca. Si data nueva lo menciona, la skill alerta y propone reactivar.



```sql
-- Cobradores puros reales (con link a Legacy)
INSERT INTO actores (codigo, nombre, nombre_completo, tipo, id_empleado_legacy) VALUES
 (NULL, 'EDGAR',     'Edgar Eduardo Gonzalez Perez',  'cobrador_puro', 94),
 (NULL, 'JORGE',     'Jorge Alberto Jauregui Ruiz',   'cobrador_puro', 92),
 (NULL, 'FRANCISCO', 'Francisco Javier Murguia',      'cobrador_puro', 93),
 (NULL, 'EDUARDO',   'Eduardo Gonzalez',              'cobrador_puro', 95);

-- Entidades virtuales (sin link a Legacy)
INSERT INTO actores (codigo, nombre, nombre_completo, tipo, id_empleado_legacy, notas) VALUES
 (NULL, 'OFICINA',             'Pagos cobrados en ubicación física Oficina',    'cobrador_puro', NULL, 'Ubicación. V5 fue código erróneo histórico, no se usa.'),
 (NULL, 'TRANSFER. / DEPTOS.', 'Pagos por transferencia o depósito bancario', 'cobrador_puro', NULL, 'Canal de pago lógico. Agrupa TRANSFER_DEPOSITO+TRANSFERENCIA+DEPOSITO.');

-- Vendedores activos (todos cobran también)
INSERT INTO actores (codigo, nombre, nombre_completo, tipo, id_empleado_legacy) VALUES
 ('V1',   'Coco',             'Maria del Socorro Villarreal Villarreal', 'vendedor', 1),
 ('V4',   'Oscar Lopez',      'Oscar Lopez Villarreal',                  'vendedor', 4),
 ('V6',   'Gaby',             'Gabriela Edith Lopez Villarreal',         'vendedor', 6),
 ('V14',  'Carmen',           'Carmen Falcon Tizcareño',                 'vendedor', 14),
 ('V16',  'Antonio Esparza',  'Lic. Antonio Esparza',                    'vendedor', 16),
 ('V23',  'Fernando Lopez',   'Fernando Lopez Villarreal',               'vendedor', 23),
 ('V27',  'Santiago',         'Santiago Haro Ruvalcaba',                 'vendedor', 27),
 ('V38',  'Laura',            'Laura Liliana Alvarado Perez',            'vendedor', 38),
 ('V39',  'Jose Asuncion',    'Jose Asuncion Cuevas Huerta',             'vendedor', 39),
 ('V55',  'Giovanni',         'Giovanni Francisco Limon Orozco',         'vendedor', 55),
 ('V56',  'Saul Manriquez',   'Saul Manriquez Valenzuela',               'vendedor', 56),
 ('V60',  'Jose Luis Torres', 'Jose Luis Torres Ruiz',                   'vendedor', 60),
 ('V84',  'Leonel',           'Leonel Anzaldo Fernandez',                'vendedor', 84),
 ('V113', 'Enrique Pulido',   'Enrique Pulido Naranjo',                  'vendedor', 113),
 ('V114', 'Jesus Perez',      'Jesus Perez Olivares',                    'vendedor', 114);

-- Usuarios iniciales (password_hash generado con bcrypt al primer setup)
INSERT INTO usuarios (email, nombre, rol, password_hash) VALUES
 ('elena@protegrt.com', 'Elena Rivas',     'admin',    crypt('elena2026', gen_salt('bf'))),
 ('oscar@protegrt.com', 'Oscar Lopez',     'consulta', crypt('oscar2026', gen_salt('bf')));
```

---

## 3 · API REST

### 3.1 Convenciones

- Base: `/api/v1`.
- Auth user: `Authorization: Bearer <jwt>`.
- Auth service (Luna): `X-Service-Token: <SICC_LUNA_TOKEN>` (no JWT, no expira).
- Encoding: `application/json` con UTF-8.
- Cifras numéricas: enteros para montos en centavos NO; usamos `NUMERIC(14,2)` en DB y `Decimal` en Pydantic. JSON serializa como string `"1553183.00"` para no perder precisión.
- Fechas: ISO 8601 con TZ explícita (`2026-05-22T18:30:00-06:00`).
- Errores: `{"error": {"code": "...", "message": "...", "details": {...}}}` con HTTP code apropiado.

### 3.2 Endpoints

#### Auth

```
POST /api/v1/auth/login
  Body: {"email": "...", "password": "..."}
  Resp: {"jwt": "...", "expira_en": "ISO8601", "usuario": {...}}
  401 si credenciales inválidas.

POST /api/v1/auth/refresh
  Header: Authorization: Bearer <jwt_actual>
  Resp: {"jwt": "...", "expira_en": "..."}
```

#### Meses

```
GET /api/v1/meses
  Resp: [{"id": 1, "anio": 2025, "mes": 1, "status": "cerrado"}, ...]

GET /api/v1/meses/{anio}/{mes}
  Resp: {
    "mes": {"id": 1, "anio": 2025, "mes": 1, "status": "cerrado", "fuente": "..."},
    "concentrado": [{"concepto": "CORRIENTE", "monto": "2242449.00", "porcentaje": "1.0000"}, ...],
    "total_general": "2002535.00",
    "top5": {
      "CORRIENTE": [{"lugar": 1, "actor": {"id": 12, "codigo": "V38", "nombre": "Laura"}, "monto": "837402.00", "porcentaje": "0.3734"}, ...],
      "EFECTIVA": [...]
    },
    "proyeccion": [{"concepto": "CORRIENTE", "monto": "1227299.00", "porcentaje": "1.0000"}, ...]
  }

POST /api/v1/meses/{id}/cerrar
  Auth: admin
  Resp: {"id": 1, "status": "cerrado", "cerrado_en": "ISO8601"}
```

#### Tendencia

```
GET /api/v1/tendencia?anios=2025,2026&concepto=EFECTIVA
  Resp: {
    "series": [
      {"anio": 2025, "datos": [{"mes": 1, "monto": "1826933.00"}, ..., {"mes": 12, "monto": "1040437.00"}]},
      {"anio": 2026, "datos": [{"mes": 1, "monto": "..."}, {"mes": 2, "monto": "..."}]}
    ]
  }
```

#### Actores

```
GET /api/v1/actores?activo=true
  Resp: [{"id": 1, "codigo": "V1", "nombre": "Coco", "tipo": "vendedor", ...}, ...]

POST /api/v1/actores            (admin)
PATCH /api/v1/actores/{id}      (admin)
```

#### Ingesta (service token)

```
POST /api/v1/ingesta/preview
  Header: X-Service-Token
  Body: <JSON candidato — schema en §4.3>
  Resp: {
    "valida": true|false,
    "validaciones": [
      {"regla": "cuadre_efectiva_recuperada_vs_total", "ok": true},
      {"regla": "etiquetas_consolidadas", "ok": true},
      {"regla": "actores_conocidos", "ok": false, "desconocidos": ["V999"]}
    ],
    "diff": {
      "nuevo": ["mes 2026-06"],
      "cambios": []
    },
    "errores": [...]
  }

POST /api/v1/ingesta/commit
  Header: X-Service-Token
  Body: <mismo JSON candidato>
  Resp: {"mes_id": 13, "creado": true, "log_id": 42}
  409 si hash duplicado y no se pasa --force.

PATCH /api/v1/meses/{id}/concepto/{concepto}
  Header: X-Service-Token
  Body: {"monto": "174435.00", "razon": "Corrección Elena ..."}
  Resp: {"ok": true, "log_id": 43}
```

#### Logs de auditoría

```
GET /api/v1/admin/logs?mes_id=1&limit=50
  Auth: admin
  Resp: [{"id": 1, "ts": "...", "agente": "luna", "accion": "commit_mes", ...}, ...]
```

#### Health

```
GET /api/v1/health
  Resp: {"ok": true, "db": "ok", "version": "1.0.0"}
```

---

## 4 · Skill `sicc-ingesta` y CLI `sicc`

### 4.1 Estructura de la skill

```
/home/elena/.openclaw/workspace/skills/sicc-ingesta/
├── SKILL.md
├── references/
│   ├── reglas-de-negocio.md       # extracto de estadistica-mensual-cobranza
│   ├── catalogo-actores.md         # codigos V# + nombres
│   └── formato-pptx.md             # estructura esperada de slides
└── scripts/
    ├── extract_pptx.py             # python-pptx → imágenes a /tmp/sicc/<hash>/
    └── consolidar.py               # TRANSFER+DEPOSITO → TRANSFER. / DEPTOS.
```

### 4.2 Frontmatter de SKILL.md

```yaml
---
name: sicc-ingesta
description: |
  Cargar, corregir y consultar datos del Sistema de Inteligencia y Control
  de Cobranza (SICC) en sicc.protegrt.com. Activar cuando Elena adjunte
  REPORTE_COBRANZA_*.pptx, captura de pantalla del Excel de cobranza, o
  diga "cárgame [mes]", "corrige [X] de [mes]", "cómo va [mes]", "muéstrame
  Top5 de [categoría] en [mes]".
allowed-tools: Read, Bash(sicc:*), Bash(python3:*)
---
```

### 4.3 JSON candidato (contrato entre skill y backend)

```json
{
  "mes": 6,
  "anio": 2025,
  "fuente": "pptx:REPORTE_COBRANZA_JUNIO_2025.pptx",
  "hash_fuente": "abc123def456...",
  "concentrado": [
    {"concepto": "CORRIENTE",           "monto": "1553183.00", "porcentaje": "1.0000"},
    {"concepto": "CANCELACIONES",       "monto": "169955.00",  "porcentaje": "0.1094"},
    {"concepto": "EFECTIVA",            "monto": "1030490.00", "porcentaje": "0.6634"},
    {"concepto": "RECUPERADA",          "monto": "79437.00",   "porcentaje": "0.0511"},
    {"concepto": "ANTICIPADA_FUTURA",   "monto": "19073.00",   "porcentaje": "0.0123"},
    {"concepto": "VENCIDA",             "monto": "194393.00",  "porcentaje": "0.1252"},
    {"concepto": "ANTICIPADA_ANTERIOR", "monto": "0.00",       "porcentaje": "0.0000"}
  ],
  "total_general": "1184720.00",
  "top5": {
    "CORRIENTE": [
      {"lugar": 1, "actor_codigo": "V6",  "actor_nombre": null, "monto": "338235.00", "porcentaje": "0.2178"},
      {"lugar": 2, "actor_codigo": "V1",  "actor_nombre": null, "monto": "247834.00", "porcentaje": "0.1596"},
      {"lugar": 3, "actor_codigo": "V39", "actor_nombre": null, "monto": "200807.00", "porcentaje": "0.1293"},
      {"lugar": 4, "actor_codigo": "V38", "actor_nombre": null, "monto": "167328.00", "porcentaje": "0.1077"},
      {"lugar": 5, "actor_codigo": "V56", "actor_nombre": null, "monto": "150000.00", "porcentaje": "0.0966"}
    ],
    "EFECTIVA": [
      {"lugar": 1, "actor_codigo": null, "actor_nombre": "FRANCISCO", "monto": "154335.00", "porcentaje": "0.1498"},
      ...
    ]
  },
  "proyeccion": [
    {"concepto": "CORRIENTE",     "monto": "1103443.00", "porcentaje": "1.0000"},
    {"concepto": "CANCELACIONES", "monto": "110344.00",  "porcentaje": "0.1000"},
    {"concepto": "EFECTIVA",      "monto": "827583.00",  "porcentaje": "0.7500"},
    {"concepto": "VENCIDA",       "monto": "165517.00",  "porcentaje": "0.1500"}
  ]
}
```

**Resolución de actor:** el backend resuelve `actor_codigo` (preferido) o `actor_nombre` (fallback) contra `actores`. Si no encuentra y no se pasa `--alta-automatica`, rechaza.

### 4.4 Comandos CLI

```bash
# Parse de PPTX → JSON
sicc parse --pptx /path/REPORTE_COBRANZA_JUNIO_2025.pptx \
           --out /tmp/sicc/<hash>/data.json

# Parse de imagen suelta (cuando Elena manda screenshot único)
sicc parse --imagen /path/captura.png \
           --slot corriente \
           --mes 6 --anio 2025 \
           --out /tmp/sicc/<hash>/data.json

# Preview (no persiste, devuelve diff + validaciones)
sicc preview --json /tmp/sicc/<hash>/data.json

# Commit (persiste, requiere preview verde)
sicc commit --json /tmp/sicc/<hash>/data.json

# Corrección puntual
sicc update --anio 2026 --mes 2 \
            --concepto cancelaciones --monto 174435.00 \
            --razon "Corrección Elena: monto del PPTX mal leído"

# Consulta para Luna en chat
sicc show --anio 2026 --mes 2 [--categoria corriente] [--formato markdown|json]

# Cerrar mes (admin)
sicc cerrar --anio 2026 --mes 2 --confirm

# Listar meses cargados
sicc meses [--anio 2025]
```

Implementación: Python 3.10+ con `click`, `httpx`, `python-pptx`, `pydantic`, `rich` para output. Distribución: `pipx install` desde el repo, o symlink directo a `~/.local/bin/sicc`.

### 4.5 Validaciones obligatorias (backend, no CLI)

| # | Regla | Comportamiento |
|---|-------|----------------|
| 1 | Cuadre `EFECTIVA + RECUPERADA ≈ TOTAL_GENERAL` ±$0.01 | Rechaza si no cuadra. |
| 2 | Sin etiquetas `DEPOSITO\|TRANSFER\|TRANSFERENCIA` sueltas | Rechaza, exige `TRANSFER. / DEPTOS.` consolidado. |
| 3 | Suma de % Top5 ≤ 100% por categoría | Rechaza. |
| 4 | Top5 con <5 entradas | Advierte, no bloquea. Marca `incompleto=true` en log. |
| 5 | Mes con `status='cerrado'` | Rechaza salvo `force=true` + razón obligatoria. |
| 6 | `hash_fuente` ya existe | Rechaza con 409 salvo `force=true`. |
| 7 | Monto > $10,000,000 | Advierte, no bloquea. |
| 8 | Actor desconocido (sin código y sin nombre conocido) | Rechaza salvo `alta_automatica=true` + confirmación de Elena. |
| 9 | Mes/año fuera de rango (mes 1-12, año 2020-2100) | Rechaza con 400. |
| 10 | `lugar` Top5 fuera de [1,5] o duplicado | Rechaza con 400. |

---

## 5 · Frontend

### 5.1 Stack

- React 18 + TypeScript
- Vite 5 (build estático, `output: 'static'`)
- Tailwind 4 con `@theme` (tokens del DESIGN.md v2 importados)
- shadcn/ui base + componentes custom según DESIGN.md
- TanStack Query v5 para data fetching/caching
- Recharts 2 para gráficas
- lucide-react para iconos (DESIGN.md §6)
- `next/font` no aplica (no Next.js); fonts vía Google Fonts directo o self-host

### 5.2 Rutas

```
/login                       → form simple
/                            → redirect a /dashboard
/dashboard                   → vista principal (selector mes + KPIs + Top5 + tendencia)
/comparativa                 → vista junta (PDF export)
/admin/meses                 → gestión (solo admin)
/admin/logs                  → audit log (solo admin)
/admin/actores               → catálogo (solo admin)
```

### 5.3 Componentes principales

| Componente | Responsabilidad |
|-----------|-----------------|
| `<AuthGuard />` | Wrap de rutas privadas, verifica JWT |
| `<MesSelector />` | Dos `<Select>` sincronizados año + mes |
| `<KpiCard concepto monto delta />` | Tarjeta KPI con delta colorizado |
| `<ConcentradoTable />` | Tabla 7 conceptos con monto + % |
| `<TendenciaChart anios concepto />` | LineChart Recharts, multi-serie |
| `<Top5Tabs />` | Tabs por categoría con `<Top5Table />` dentro |
| `<Top5Table categoria />` | Lista lugar+actor+monto+% con barra visual |
| `<ComparativaAnual />` | Vista grande para junta, exportable |
| `<PdfExportButton vista />` | Genera PDF con `react-to-print` o jsPDF |
| `<MesStatusBadge status />` | Badge: borrador/revisado/cerrado |
| `<ActorBadge actor />` | Chip con codigo + nombre + tooltip nombre_completo |
| `<IngestaLogList />` | Lista de logs (admin) |

### 5.4 Diseño visual

Aplica **DESIGN.md v2** de Proteg-rt (snapshot `D:\claudy\backups\open-design-snapshots\protegrt-ds-v2-dual-italic-aprobada-2026-05-07\`):

- **Paleta:** `--navy-800` brand, `--gold` acento (max 2x/pantalla), `--cream` background, `--red` solo para deltas negativos extremos.
- **Tipografía:** Saira Condensed 800 vertical para headers display; Montserrat 400/600 para body; JetBrains Mono `tabular-nums` para CIFRAS.
- **Italic accent** `.t-italic-display` reservado para el total del mes en hero del dashboard (1 momento/pantalla).
- **`.gold-foil`** reservado para el total general del año en `/comparativa` (1 momento/pantalla).
- **Radius:** 0px default (cards, secciones). 4px solo en inputs/botones.
- **Sombras:** none default. Solo en dropdowns/modales (`--shadow-1`).
- **Border-block-start** con `--gold` para feature-cards (regla decorativa superior).
- **Mobile responsive** con breakpoints 375/640/1024/1280.
- **`prefers-reduced-motion`** soportado.

---

## 6 · Estructura del repo

```
sicc/
├── backend/
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   │       └── 0001_initial.py
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── deps.py
│   │   ├── config.py
│   │   ├── models/
│   │   │   ├── actor.py
│   │   │   ├── mes.py
│   │   │   ├── concepto.py
│   │   │   ├── top5.py
│   │   │   ├── usuario.py
│   │   │   └── log.py
│   │   ├── schemas/
│   │   │   └── (Pydantic v2 mirrors)
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── meses.py
│   │   │   ├── tendencia.py
│   │   │   ├── actores.py
│   │   │   ├── ingesta.py
│   │   │   └── admin.py
│   │   ├── services/
│   │   │   ├── validador.py
│   │   │   ├── consolidador.py
│   │   │   ├── ingesta.py
│   │   │   └── auth.py
│   │   └── seeds.py
│   ├── tests/
│   │   ├── test_validador.py
│   │   ├── test_ingesta.py
│   │   └── test_auth.py
│   ├── pyproject.toml
│   ├── Dockerfile
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── routes/
│   │   ├── components/
│   │   ├── hooks/
│   │   │   ├── useMes.ts
│   │   │   ├── useTendencia.ts
│   │   │   └── useAuth.ts
│   │   ├── lib/
│   │   │   ├── api.ts
│   │   │   └── format.ts
│   │   └── styles/
│   │       └── globals.css       # importa tokens de DESIGN.md
│   ├── public/
│   │   └── logo.png              # copiado de sistema-proteg/web-admin
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── Dockerfile
├── skill/
│   └── sicc-ingesta/
│       ├── SKILL.md
│       ├── references/
│       └── scripts/
├── cli/
│   ├── pyproject.toml
│   └── sicc/
│       ├── __init__.py
│       ├── cli.py
│       ├── parsers/
│       │   ├── pptx.py
│       │   └── image.py
│       └── client.py
├── scripts/
│   ├── migrar_2025.py             # ingesta del xlsx que Fer compartió
│   └── seed_actores.py            # alta inicial del catálogo
├── docker-compose.yml
├── .env.example
├── README.md
└── PRD.md → symlink al doc de producto
```

---

## 7 · Auth y seguridad

### 7.1 Modelo

- **Usuarios humanos (Elena, Óscar, Fer):** login con email+password → JWT.
- **Servicio (Luna):** `X-Service-Token` con valor de `SICC_LUNA_TOKEN`, no expira, rotable cambiando el env y reiniciando backend.
- **Roles:**
  - `admin` (Elena, Fer): todo, incluyendo cerrar mes, ver logs, gestionar actores.
  - `consulta` (Óscar): solo lectura del dashboard y comparativa.

### 7.2 JWT

```
HS256
Claims: {sub, email, rol, exp}
Expira: 24h
Refresh: re-login (sin refresh tokens en V1)
```

Algoritmo HS256 con secret rotable. JWT no se almacena en localStorage (vulnerable a XSS) — se guarda en cookie `httpOnly + Secure + SameSite=Strict`.

### 7.3 Password hashing

bcrypt con cost factor 12. Reset de contraseña en V1 es manual via CLI:

```bash
sicc admin reset-password --email elena@protegrt.com --nueva <nueva>
```

### 7.4 CORS

Backend acepta solo `https://sicc.protegrt.com` (single origin). En dev, `http://localhost:5173`.

### 7.5 Rate limiting

`/auth/login`: 5 intentos por IP / 15 minutos antes de bloquear 1h. Sin Redis dedicado: counter in-memory por proceso (suficiente para 2 usuarios).

---

## 8 · Deploy y operación

### 8.1 docker-compose.yml (esquema)

```yaml
services:
  sicc-db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - sicc_db_data:/var/lib/postgresql/data
    networks: [sicc-net]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

  sicc-backend:
    build: ./backend
    restart: unless-stopped
    environment:
      SICC_DB_URL: postgresql+psycopg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@sicc-db:5432/${POSTGRES_DB}
      SICC_JWT_SECRET: ${SICC_JWT_SECRET}
      SICC_LUNA_TOKEN: ${SICC_LUNA_TOKEN}
      SICC_CORS_ORIGINS: ${SICC_CORS_ORIGINS}
    depends_on:
      sicc-db: {condition: service_healthy}
    networks: [sicc-net, traefik]
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.sicc-api.rule=Host(`sicc.protegrt.com`) && PathPrefix(`/api`)"
      - "traefik.http.routers.sicc-api.tls.certresolver=le"

  sicc-frontend:
    build: ./frontend
    restart: unless-stopped
    networks: [sicc-net, traefik]
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.sicc-web.rule=Host(`sicc.protegrt.com`)"
      - "traefik.http.routers.sicc-web.tls.certresolver=le"

volumes:
  sicc_db_data:

networks:
  sicc-net:
    internal: true
  traefik:
    external: true
```

### 8.2 Bootstrap

```bash
cd /root/sicc
cp .env.example .env && nano .env   # llenar secrets
docker compose pull
docker compose build
docker compose up -d
docker compose exec sicc-backend alembic upgrade head
docker compose exec sicc-backend python -m app.seeds
# Migrar 2025
docker cp /home/elena/.openclaw/workspace/workspaces/cobranza/estadisticas/ESTADISTICA_2025.xlsx \
  sicc-backend:/tmp/ESTADISTICA_2025.xlsx
docker compose exec sicc-backend python scripts/migrar_2025.py /tmp/ESTADISTICA_2025.xlsx
```

### 8.3 Backup

Cron en lunita (host, no en container):

```cron
0 3 * * * docker compose -f /root/sicc/docker-compose.yml exec -T sicc-db \
  pg_dump -U sicc sicc | gzip > /srv/backups/sicc/sicc-$(date +\%Y\%m\%d).sql.gz \
  && find /srv/backups/sicc/ -name 'sicc-*.sql.gz' -mtime +30 -delete
```

### 8.4 Logs

- Backend: `docker compose logs sicc-backend -f` (uvicorn + app logs).
- DB: `docker compose logs sicc-db`.
- Audit log de aplicación: tabla `ingesta_logs` (no archivo).
- Skill/CLI: logs locales en `/home/elena/.local/share/sicc/cli.log`.

### 8.5 Refresh de vista materializada

Cron en lunita (host):

```cron
0 4 * * * docker compose -f /root/sicc/docker-compose.yml exec -T sicc-db \
  psql -U sicc -d sicc -c "REFRESH MATERIALIZED VIEW CONCURRENTLY mv_tendencia_anual"
```

---

## 9 · Testing

### 9.1 Backend (pytest)

- `test_validador.py`: 10+ casos por cada regla del §4.5.
- `test_ingesta.py`: flujo preview → commit, dedup por hash, alta de actor desconocido.
- `test_auth.py`: login OK, login KO, JWT inválido, rol insuficiente.
- Fixtures con SQLite en memoria + Alembic upgrade.

### 9.2 Frontend (vitest + playwright)

- Unit: format helpers (Intl.NumberFormat es-MX), hook tests con mock API.
- E2E (playwright): login, navegar mes, exportar PDF. 3-5 escenarios críticos.

### 9.3 Migración 2025

Antes de cerrar Fase 2, generar reporte de validación cruzada xlsx ↔ DB y entregarlo a Elena para visto bueno antes de marcar los 12 meses como `cerrado`.

---

## 10 · Migración de datos 2025

### 10.1 Fuente

`/home/elena/.openclaw/workspace/workspaces/cobranza/estadisticas/ESTADISTICA_2025.xlsx` (39 KB, compartido por Fer 22 may 2026).

Estructura: 9 hojas (`DATOS GRAL.`, `COBRANZA CORRIENTE`, `CANCELACIONES`, `COBRANZA VENCIDA`, `COBRANZA EFECTIVA`, `COBRANZA RECUPERADA`, `COBRANZA TOTAL GRAL.`, `COBRANZA ADELANTADA F.`, `PROYECCION SIG. MES`).

### 10.2 Script

```python
# scripts/migrar_2025.py
# Usa openpyxl para leer cada hoja
# Construye un JSON candidato por mes
# POSTea a /api/v1/ingesta/commit con X-Service-Token y --force-fuente
# (porque la "fuente" oficial es el xlsx, no un PPTX)
```

### 10.3 Validación post-migración

- Cuadre de cada mes (Efectiva+Recuperada ≈ Total).
- Que los 12 meses de 2025 estén en `meses` con status inicialmente `revisado`.
- Que cada hoja Top5 tenga 5 entradas por categoría (febrero y otros pueden tener filas vacías; lo verifica el script).
- Reporte HTML con discrepancias detectadas para que Elena valide manualmente.

### 10.4 Cierre del año

Una vez que Elena visa el reporte, los 12 meses se marcan `cerrado` con `cerrado_por = elena.id`.

---

## 11 · Decisiones técnicas registradas

| # | Decisión | Alternativas consideradas | Por qué |
|---|----------|---------------------------|---------|
| 1 | Postgres 16 (no MariaDB Quiniela) | Reusar MariaDB existente | Aislamiento; el bug de Quiniela no debe poder tocar cobranza. |
| 2 | psycopg3 + SQLAlchemy 2 | asyncpg + raw SQL | Mantenibilidad sobre micro-perf (2 usuarios). |
| 3 | Pydantic v2 | dataclasses + marshmallow | Validación nativa con FastAPI, mejor DX. |
| 4 | Alembic | atlasgo, manual | Estándar del ecosistema SQLAlchemy. |
| 5 | NUMERIC(14,2) para montos | INT centavos, FLOAT | Cobranza es contable; precisión decimal es no-negociable. |
| 6 | JWT en cookie httpOnly | LocalStorage | XSS hardening, OWASP recomendación. |
| 7 | Service token plano para Luna | OAuth2 client credentials | Simplicidad; 1 cliente, sin necesidad de scopes. |
| 8 | TanStack Query | Redux Toolkit Query, SWR | API más ergonómica, mejor cache invalidation. |
| 9 | Recharts | Chart.js, Visx, D3 directo | Suficiente para line+bar, componibilidad con React. |
| 10 | nginx:alpine para frontend | sirvir desde FastAPI | Separación, cache headers nativos, menor superficie. |
| 11 | Vistas materializadas para tendencia | View regular, query directo | Volume bajo pero queries cross-año pueden multiplicar lookups; mv preview-rápido. |
| 12 | Skill markdown + CLI (no solo CLI) | Solo CLI, solo prompt en SKILL | Skill da semántica (cuándo); CLI da determinismo (cómo). Patrón estándar de Luna. |
| 13 | Vision multimodal para imágenes (no Tesseract) | Tesseract + post-procesamiento | Tablas numéricas con separadores son mejor manejadas por modelo multimodal. |
| 14 | Single year en `mv_tendencia_anual` no requerido | Sharding por año, partitioning | Volume <10K filas. YAGNI. |
| 15 | Backup `pg_dump` (no PITR ni replicación) | WAL streaming, replicación lógica | Daily snapshot es suficiente para 2 usuarios; PITR es over-engineering. |

---

## 12 · Anexos

### A. Mapeo de columnas xlsx → DB (para `migrar_2025.py`)

| Hoja xlsx | Columna xlsx | Tabla DB | Campo |
|-----------|--------------|----------|-------|
| `DATOS GRAL.` | `MES` (A) | `meses` | `mes` (parsed) |
| `DATOS GRAL.` | `CORRIENTE` (B) | `conceptos_mensuales` | `monto` con `concepto='CORRIENTE'` |
| `DATOS GRAL.` | `%` (C) | `conceptos_mensuales` | `porcentaje` |
| `DATOS GRAL.` | `CANCELACIONES` (D) | `conceptos_mensuales` | `monto` con `concepto='CANCELACIONES'` |
| ... | ... | ... | ... |
| `COBRANZA CORRIENTE` | `VENDEDOR 1` (C) + `TOTAL` (D) + `%` (E) | `top5` | `categoria='CORRIENTE'`, `lugar=1` |
| ... | (V5-9, V10-14, V15-19) | ... | `lugar=2..5` |

### B. Comandos para reauditar este SPEC

```bash
ssh lunita "ls /home/elena/.openclaw/workspace/workspaces/cobranza/estadisticas/"
ssh lunita "cat /home/elena/.openclaw/workspace/skills/estadistica-mensual-cobranza/SKILL.md"
ssh lunita "grep -E 'empleados|SELECT' /opt/legacy-api/main.py"
```

### C. Referencias

- DESIGN.md v2 Proteg-rt: `D:\claudy\backups\open-design-snapshots\protegrt-ds-v2-dual-italic-aprobada-2026-05-07\DESIGN.md`
- PRD complementario: `D:\claudy\sicc-prd.md`
- xlsx 2025 (snapshot de fuente): `/home/elena/.openclaw/workspace/workspaces/cobranza/estadisticas/` (a copiar)
- API de Legacy (consulta): `/opt/legacy-api/main.py` en lunita

### D. V2 — Endpoint a agregar en `legacy-api`

Diseño del endpoint que sustituirá la ingesta vía Luna cuando Legacy estabilice:

```python
# /opt/legacy-api/main.py — agregar en V2

@app.get("/api/v1/reportes/cobranza-mensual")
async def cobranza_mensual(
    anio: int = Query(..., ge=2020, le=2100),
    mes: int = Query(..., ge=1, le=12),
    user: dict = Depends(get_current_user),
):
    """Snapshot de cobranza para SICC. Equivalente al PPTX que Elena recibe."""
    if user["rol"] != "admin":
        raise HTTPException(403, "Solo admin")

    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)

        # 1. Concentrado: SUMs por concepto desde tabla `pagos` JOIN `polizas`
        cur.execute("""
            SELECT
              SUM(CASE WHEN status_pago='Corriente'   THEN monto END) AS corriente,
              SUM(CASE WHEN status_pago='Cancelado'   THEN monto END) AS cancelaciones,
              SUM(CASE WHEN status_pago='Efectiva'    THEN monto END) AS efectiva,
              SUM(CASE WHEN status_pago='Recuperada'  THEN monto END) AS recuperada,
              SUM(CASE WHEN status_pago='Anticipada'  THEN monto END) AS anticipada_futura,
              SUM(CASE WHEN status_pago='Vencida'     THEN monto END) AS vencida,
              SUM(CASE WHEN status_pago='AnticipadaAnt' THEN monto END) AS anticipada_anterior
            FROM pagos
            WHERE YEAR(fecha_pago)=%s AND MONTH(fecha_pago)=%s
        """, (anio, mes))
        concentrado = cur.fetchone()

        # 2. Top5 por categoría (consolidando TRANSFER+DEPOSITO)
        # ... (queries específicas por categoría con criterio dual vendedor/cobrado)

        return {
          "mes": mes, "anio": anio,
          "fuente": f"legacy-api:cobranza-mensual:{anio}-{mes:02d}",
          "hash_fuente": <sha256 del payload>,
          "concentrado": [...],
          "total_general": ...,
          "top5": {...},
          "proyeccion": [...]
        }
    finally:
        conn.close()
```

Trabajo estimado en V2: ~1 día una vez que las queries contra Legacy estén validadas (lo que requiere que la estructura de `empleados` esté estabilizada).
