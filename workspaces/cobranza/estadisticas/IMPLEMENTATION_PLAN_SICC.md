# SICC — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) o `executing-plans` para implementar este plan task-by-task. Steps usan checkbox (`- [ ]`) para tracking.
>
> **Orquestador y jefe del proyecto:** Claudio. Tareas se delegan a subagentes Opus 4.7 o Sonnet 4.6 según el campo `agent` de cada task. Auditorías adversariales al final de cada fase NO son negociables.

**Goal:** Construir SICC (dashboard web de cobranza de Proteg-rt) desplegado en lunita y listo para la junta con Óscar del 5 jun 2026.

**Architecture:** Postgres 16 + FastAPI + React/Vite/Tailwind 4 en docker compose detrás del Traefik existente de lunita, ingesta operada por Luna via skill `sicc-ingesta` con vision multimodal sobre PPTX. Aplica DESIGN.md v2 Proteg-rt (dual italic, navy+gold+crema). PRD/SPEC v1 en `docs/PRD.md` y `docs/SPEC.md`.

**Tech Stack:** Python 3.12 + FastAPI + SQLAlchemy 2 + Alembic + Pydantic v2 + asyncpg + bcrypt + python-jose + python-pptx (en CLI) · TypeScript + React 18 + Vite 5 + Tailwind 4 + TanStack Query v5 + Recharts 2 + lucide-react + react-to-print · Docker Compose · Traefik v3 · Postgres 16 · pgvector NO requerido (sin embeddings).

**Repo:** `sunkwolf/sicc` (privado, a crear en Fase 0).
**Carpeta local:** `D:\claudy\sicc\`.
**Carpeta remota:** `/root/sicc/` en lunita.

---

## Mapa de archivos

**Backend (`backend/`):**
- Create: `pyproject.toml`, `Dockerfile`, `.env.example`, `README.md`
- Create: `alembic.ini`, `alembic/env.py`, `alembic/versions/0001_initial.py`
- Create: `app/main.py`, `app/config.py`, `app/deps.py`
- Create: `app/models/{actor,mes,concepto,top5,total,proyeccion,usuario,log}.py`
- Create: `app/schemas/{actor,mes,ingesta,auth,tendencia}.py`
- Create: `app/routers/{auth,meses,tendencia,actores,ingesta,admin,health}.py`
- Create: `app/services/{validador,consolidador,ingesta,auth,migracion}.py`
- Create: `app/seeds.py`
- Create: `tests/{test_validador,test_consolidador,test_auth,test_ingesta,test_meses}.py`
- Create: `scripts/{migrar_2025.py,seed_actores_historicos.py,reset_password.py}`

**Frontend (`frontend/`):**
- Create: `package.json`, `Dockerfile`, `vite.config.ts`, `tailwind.config.ts`, `tsconfig.json`, `nginx.conf`
- Create: `src/main.tsx`, `src/App.tsx`, `src/styles/globals.css`
- Create: `src/lib/{api,format,auth}.ts`
- Create: `src/hooks/{useAuth,useMes,useTendencia,useActores}.ts`
- Create: `src/components/{AuthGuard,MesSelector,KpiCard,ConcentradoTable,Top5Tabs,Top5Table,TendenciaChart,ComparativaAnual,ActorBadge,MesStatusBadge,IngestaLogList,PdfExportButton,Sparkline}.tsx`
- Create: `src/components/ui/{Button,Input,Card,Badge,Alert,Eyebrow,PullQuote}.tsx` (DESIGN.md v2)
- Create: `src/routes/{login,dashboard,comparativa,admin/meses,admin/logs,admin/actores}.tsx`
- Create: `public/logo.png` (copiar de `D:\claudy\projects\sistema-proteg\web-admin\public\logo.png`)
- Create: `tests/playwright/{login,dashboard,comparativa}.spec.ts`

**Skill + CLI (`skill/`, `cli/`):**
- Create: `skill/sicc-ingesta/SKILL.md`
- Create: `skill/sicc-ingesta/references/{reglas-de-negocio,catalogo-actores,formato-pptx}.md`
- Create: `skill/sicc-ingesta/scripts/{extract_pptx.py,consolidar.py}`
- Create: `cli/pyproject.toml`, `cli/sicc/{__init__,cli,client,parsers/pptx,parsers/image,parsers/xlsx}.py`

**Root:**
- Create: `docker-compose.yml`, `.env.example`, `README.md`, `.gitignore`, `.github/workflows/ci.yml`

---

## Convenciones globales

1. **Datetime tz-aware**: `Mapped[datetime] = mapped_column(DateTime(timezone=True))` + `datetime.now(UTC)`. Nunca `datetime.utcnow()`.
2. **UUIDs**: PKs como `SERIAL` (autoincremental) salvo casos justificados. Para logs `BIGSERIAL`.
3. **Montos**: `NUMERIC(14,2)` en DB; `Decimal` en Pydantic; serializa como `string` en JSON.
4. **Naming convention en constraints**: `name="<descriptor_corto>"`. SQLAlchemy auto-prefija con `ck_/uq_/fk_`.
5. **Commits firmados como Claudio**: trailer `Co-Authored-By: Claudio <noreply@anthropic.com>`. Pasar mensajes vía HEREDOC.
6. **Visibility checks post-commit** (sandbox isolation): `git log main -3 && git rev-parse main && ls -la <archivo>` antes de declarar done.
7. **Pytest concurrencia**: cada subagente corre `ruff + mypy + pytest <test_focal>`. Suite completa UNA vez en main post-merge (regla [[feedback_pytest_concurrencia_db]]).
8. **Branch por task**: `task/T<fase>.<num>-<descriptor-corto>`. PR a `main` al cerrar la task.
9. **Push automático al pasar a review** ([[feedback_push_antes_de_review]]).
10. **DESIGN.md v2** es la única referencia visual. Importar tokens en `globals.css`. Cualquier desvío requiere ADR en `docs/DECISIONES.md`.
11. **Auth de servicio (Luna)**: header `X-Service-Token` con `SICC_LUNA_TOKEN`. Backend valida en middleware.
12. **Idioma español-MX en toda UI y mensajes de error.** Sin i18n.
13. **Sin telemetría externa.** Sin analytics. Sin Sentry en V1.

---

## Resumen de fases y waves

| Fase | Tasks | Días | Paralelizable | Bloquea |
|------|-------|------|---------------|---------|
| **F0 — Setup** | T0.1–T0.6 + 🔍 | 1 | T0.1→T0.2→(T0.3‖T0.4‖T0.5)→T0.6 | F1 |
| **F1 — Backend** | T1.1–T1.10 + 🔍 | 2-3 | Ver tabla F1 | F2 |
| **F2 — Migración + Skill + CLI** | T2.1–T2.8 + 🔍 | 2-3 | Ver tabla F2 | F3 |
| **F3 — Frontend** | T3.1–T3.13 + 🔍 | 3 | Ver tabla F3 | F4 |
| **F4 — Ingesta 2026 + pulido** | T4.1–T4.6 + 🔍 | 1-2 | Mixto | F5 |
| **F5 — Pre-junta** | T5.1–T5.5 + 🔍 QUÍNTUPLE | 1 | Mayoría seriales | Junta |
| **Junta** | — | 5 jun | — | — |

---

# FASE 0 — Setup (1 día)

**Tabla de paralelización F0:**

| Task | Agent | Depende de | Paralelizable con |
|------|-------|------------|-------------------|
| T0.1 Crear repo + estructura | Sonnet | — | — |
| T0.2 docker-compose base | Sonnet | T0.1 | — |
| T0.3 Alembic + migración 0001 | **Opus** | T0.2 | T0.4, T0.5 |
| T0.4 Traefik labels + DNS | Sonnet | T0.2 | T0.3, T0.5 |
| T0.5 .env.example + CI baseline | Sonnet | T0.1 | T0.3, T0.4 |
| T0.6 Bootstrap en lunita | **Opus** | T0.3, T0.4, T0.5 | — |
| 🔍 F0 Audit | **Opus adversarial** | T0.6 | — |

### T0.1 — Crear repo `sunkwolf/sicc` + estructura monorepo  · agent: **Sonnet 4.6**

**Files:** crea `D:\claudy\sicc\` con la estructura del §Mapa de archivos. Solo crea carpetas + archivos `__init__.py`/placeholders donde aplique. NO código de backend/frontend todavía.

- [ ] **Step 1:** `gh repo create sunkwolf/sicc --private --source=D:\claudy\sicc --remote=origin --description "SICC — Dashboard de cobranza Proteg-rt"`
- [ ] **Step 2:** crear estructura completa de carpetas (backend/, frontend/, skill/, cli/, scripts/, docs/ ya existe, reports/ ya existe).
- [ ] **Step 3:** crear `.gitignore` root con `**/__pycache__/`, `*.pyc`, `node_modules/`, `dist/`, `.env`, `.venv/`, `*.sqlite3`.
- [ ] **Step 4:** `git add -A && git commit -m "feat: initial monorepo structure"`. Firmar como Claudio.
- [ ] **Step 5:** `git push -u origin main`.
- [ ] **Step 6 (visibility check):** `git log --oneline -1` debe mostrar el commit. `gh repo view sunkwolf/sicc` debe mostrar el repo.

### T0.2 — docker-compose base  · agent: **Sonnet 4.6**

**Files:** Create `docker-compose.yml`, `backend/Dockerfile` (placeholder), `frontend/Dockerfile` (placeholder).

- [ ] **Step 1:** crear `docker-compose.yml` con servicios `sicc-db` (postgres:16-alpine), `sicc-backend` (build context backend/), `sicc-frontend` (build context frontend/), redes `sicc-net` (internal) y `traefik` (external), volumen `sicc_db_data`. Labels Traefik para `sicc.protegrt.com` (host) y `Host && PathPrefix(/api)` para backend.
- [ ] **Step 2:** crear `backend/Dockerfile` base: `FROM python:3.12-slim`, COPY pyproject.toml + uv sync, COPY app/, `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]`.
- [ ] **Step 3:** crear `frontend/Dockerfile`: multi-stage con `node:20-alpine` para build (`npm run build`) y `nginx:alpine` para servir `dist/`. Incluye `nginx.conf` con fallback a `index.html` para SPA routing.
- [ ] **Step 4:** `docker compose config` valida sintaxis.
- [ ] **Step 5:** commit + push.

### T0.3 — Alembic + migración 0001 (schema completo)  · agent: **Opus 4.7**

**Files:** Create `backend/pyproject.toml`, `backend/alembic.ini`, `backend/alembic/env.py`, `backend/alembic/versions/20260523_0001_initial.py`.

Toda la DDL del SPEC §2.1 va en esta migración: ENUMs (`tipo_actor`, `concepto_concentrado`, `categoria_top5`, `concepto_proyeccion`, `status_mes`, `rol_usuario`), tablas (`actores`, `usuarios`, `meses`, `conceptos_mensuales`, `totales_mensuales`, `top5`, `proyecciones`, `ingesta_logs`), índices, triggers `tr_set_actualizado_en`. La vista materializada `mv_tendencia_anual` va en migration **0002** separada (T1.6) — no acá.

- [ ] **Step 1:** crear `pyproject.toml` con deps base: `fastapi`, `uvicorn[standard]`, `sqlalchemy[asyncio]>=2.0`, `alembic>=1.13`, `asyncpg`, `psycopg[binary]`, `pydantic>=2`, `pydantic-settings`, `python-jose[cryptography]`, `passlib[bcrypt]`, `python-multipart`, `httpx`, `pytest`, `pytest-asyncio`, `ruff`, `mypy`.
- [ ] **Step 2:** `cd backend && uv init . && uv sync && uv run alembic init alembic` (o equivalente con pip).
- [ ] **Step 3:** configurar `alembic/env.py` con `SICC_DB_URL` desde env, async engine, naming convention estándar SQLAlchemy.
- [ ] **Step 4:** escribir migración 0001 con TODA la DDL del SPEC §2.1. Usar `op.execute()` para ENUMs y triggers; `op.create_table()` para tablas; `op.create_index()` para índices. Tests: ejecutar `alembic upgrade head` contra Postgres local (docker compose up sicc-db) y verificar:
  ```sql
  \dt    -- 8 tablas
  \dT    -- 6 enums
  \d actores  -- columnas correctas
  ```
- [ ] **Step 5:** test pytest mínimo en `tests/test_migration.py`:
  ```python
  import pytest
  from sqlalchemy import text
  @pytest.mark.asyncio
  async def test_migration_creates_all_tables(db_session):
      result = await db_session.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public'"))
      tables = {r[0] for r in result.all()}
      assert {'actores','usuarios','meses','conceptos_mensuales','totales_mensuales','top5','proyecciones','ingesta_logs'} <= tables
  ```
- [ ] **Step 6:** `alembic downgrade base && alembic upgrade head` reproducible. Commit + push.
- [ ] **Step 7 (visibility check):** `docker compose exec sicc-db psql -U sicc -d sicc -c "\dt"` muestra las 8 tablas.

### T0.4 — Traefik labels + DNS `sicc.protegrt.com`  · agent: **Sonnet 4.6**

**Files:** Modify `docker-compose.yml` (labels), crear `docs/INFRA.md`.

- [ ] **Step 1:** completar labels Traefik en `docker-compose.yml`:
  ```yaml
  labels:
    - traefik.enable=true
    - traefik.http.routers.sicc-api.rule=Host(`sicc.protegrt.com`) && PathPrefix(`/api`)
    - traefik.http.routers.sicc-api.tls=true
    - traefik.http.routers.sicc-api.tls.certresolver=le
    - traefik.http.services.sicc-api.loadbalancer.server.port=8001
    - traefik.http.routers.sicc-web.rule=Host(`sicc.protegrt.com`)
    - traefik.http.routers.sicc-web.tls=true
    - traefik.http.routers.sicc-web.tls.certresolver=le
    - traefik.http.services.sicc-web.loadbalancer.server.port=80
  ```
- [ ] **Step 2:** DNS — agregar A record `sicc.protegrt.com → IP de lunita`. Documentar en `docs/INFRA.md` quién lo configura (Fer, o el panel del DNS provider). Si no hay panel, el subagente reporta y se pasa a Claudio para coordinar con Fer.
- [ ] **Step 3:** verificar con `dig sicc.protegrt.com` que resuelve a la IP correcta.

### T0.5 — `.env.example` + CI baseline  · agent: **Sonnet 4.6**

**Files:** Create `.env.example`, `.github/workflows/ci.yml`.

- [ ] **Step 1:** `.env.example` con todas las variables del SPEC §1.4 (POSTGRES_*, SICC_DB_URL, SICC_JWT_SECRET, SICC_LUNA_TOKEN, SICC_CORS_ORIGINS, SICC_ENV, VITE_API_BASE) con valores placeholder y comentarios.
- [ ] **Step 2:** `.github/workflows/ci.yml` corre en push/PR a main: matrix de backend (ruff check, mypy, pytest) y frontend (`npm ci && npm run build && npm test`). Postgres como service.
- [ ] **Step 3:** push y verificar que CI corre verde sobre el estado inicial vacío.

### T0.6 — Bootstrap en lunita  · agent: **Opus 4.7**

**Files:** ninguno nuevo. Despliegue.

- [ ] **Step 1 (SSH a lunita):** `ssh lunita "mkdir -p /root/sicc && cd /root/sicc && git clone git@github.com:sunkwolf/sicc.git ."` (o con `gh repo clone`).
- [ ] **Step 2:** crear `/root/sicc/.env` con secrets reales (generados con `openssl rand -base64 32` para passwords y tokens).
- [ ] **Step 3:** `docker compose pull && docker compose build && docker compose up -d sicc-db`.
- [ ] **Step 4:** `docker compose exec sicc-backend alembic upgrade head` (después de levantar backend con `docker compose up -d sicc-backend`, aunque el código aún es esqueleto).
- [ ] **Step 5:** verificar `curl -k https://sicc.protegrt.com/api/v1/health` devuelve 200 (incluso si solo es placeholder).
- [ ] **Step 6 (reporte por Telegram):** "Fase 0 bootstrap completado. Backend en /api/v1/health responde 200. Listo para F1."

### 🔍 AUDITORÍA F0 ADVERSARIAL  · agent: **Opus 4.7 (modo adversarial)**

**Briefing del auditor:**
> Tu rol es **QA hostil**. Tu objetivo es romper el setup de F0. NO felicitar, NO matizar. Encontrar problemas. Si no hay, decirlo explícito ("sin hallazgos") con evidencia.

- [ ] **Step 1:** Verificar que repo `sunkwolf/sicc` es **privado**, no público.
- [ ] **Step 2:** `docker compose config` parsea sin errores, NO hay puertos expuestos públicos accidentales (sicc-db jamás debe exponer 5432 al host ni a internet).
- [ ] **Step 3:** Verificar Alembic ejecuta `upgrade head` y `downgrade base` sin errores residuales. Postgres queda limpio entre runs.
- [ ] **Step 4:** Confirmar que la migración 0001 crea TODOS los CHECK constraints, índices, y triggers definidos en SPEC §2.1. Comparar `\d <tabla>` vs SPEC línea por línea.
- [ ] **Step 5:** `.env` NO está en el repo. `.gitignore` cubre `.env`. `git log --all -- .env` debe estar vacío.
- [ ] **Step 6:** TLS funcionando: `curl https://sicc.protegrt.com/api/v1/health` resuelve con cert válido de Let's Encrypt (no self-signed).
- [ ] **Step 7:** Reporta hallazgos en `reports/F0-audit-<fecha>.md`. Severidad por hallazgo: critical/high/medium/low. Si critical → arreglar antes de pasar a F1.

---

# FASE 1 — Backend (2-3 días)

**Tabla de paralelización F1:**

| Task | Agent | Depende de | Paralelizable con |
|------|-------|------------|-------------------|
| T1.1 Models SQLAlchemy | **Opus** | F0 | — |
| T1.2 Schemas Pydantic | Sonnet | T1.1 | — |
| T1.3 Auth (login, JWT, bcrypt) | **Opus** | T1.2 | T1.5, T1.7 |
| T1.4 Validador + tests | **Opus** | T1.2 | T1.5, T1.7 |
| T1.5 Router meses (GET) | Sonnet | T1.2 | T1.3, T1.4, T1.7 |
| T1.6 Router tendencia + MV | **Opus** | T1.5 | T1.7 |
| T1.7 Router actores | Sonnet | T1.2 | T1.3, T1.4, T1.5 |
| T1.8 Router ingesta | **Opus** | T1.4 | — |
| T1.9 Router admin | Sonnet | T1.8 | — |
| T1.10 Tests integración | **Opus** | T1.8, T1.9 | — |
| 🔍 F1 Audit | **Opus adversarial** | T1.10 | — |

### T1.1 — Models SQLAlchemy  · agent: **Opus 4.7**

**Files:** Create `backend/app/models/{__init__,actor,mes,concepto,top5,total,proyeccion,usuario,log}.py`, `backend/app/db.py`.

- [ ] **Step 1:** `app/db.py` con `Base = declarative_base()`, `async_engine`, `AsyncSession`, dependency `get_db`. Naming convention SQLAlchemy estándar.
- [ ] **Step 2:** Un módulo por modelo, mapeando 1:1 al schema de migración 0001. Usar `Mapped[T]` style (SQLAlchemy 2). Enums como `Enum(<EnumPython>)` con `name=` explícito. FKs con `ondelete` correctos (CASCADE para meses → conceptos/top5, SET NULL para logs.mes_id).
- [ ] **Step 3:** `tests/test_models.py` — crear instancias en sesión, commit, query, verifica que los enums y constraints se respetan.
- [ ] **Step 4:** Run `pytest tests/test_models.py -v`. Expected: PASS.
- [ ] **Step 5:** commit + push + visibility checks.

### T1.2 — Schemas Pydantic v2  · agent: **Sonnet 4.6**

**Files:** Create `backend/app/schemas/{__init__,actor,mes,ingesta,auth,tendencia,common}.py`.

- [ ] **Step 1:** `common.py` con `MontoDecimal = Annotated[Decimal, BeforeValidator(...), PlainSerializer(...)]` que serializa a string. Reutilizable en todos los schemas.
- [ ] **Step 2:** Schemas por dominio. Contratos del SPEC §3:
  - `ActorOut`, `ActorCreate`, `ActorUpdate`
  - `MesOut`, `MesDetalleOut` (con concentrado + top5 + total + proyección anidados)
  - `IngestaCandidatoIn` (matchea SPEC §4.3 JSON candidato)
  - `IngestaPreviewOut`, `IngestaCommitOut`
  - `LoginIn`, `JwtOut`, `UsuarioOut`
  - `TendenciaSerieOut`, `TendenciaResponseOut`
- [ ] **Step 3:** `tests/test_schemas.py` — round-trip JSON ↔ schema para cada uno. Validación de Decimal como string.
- [ ] **Step 4:** commit + push.

### T1.3 — Auth (login + JWT + bcrypt)  · agent: **Opus 4.7**

**Files:** Create `backend/app/services/auth.py`, `backend/app/routers/auth.py`, `backend/app/deps.py`.

- [ ] **Step 1:** `services/auth.py` con `hash_password(plain) → str`, `verify_password(plain, hash) → bool`, `create_jwt(usuario_id, email, rol) → str`, `decode_jwt(token) → dict`. Cost factor bcrypt = 12.
- [ ] **Step 2:** `routers/auth.py` con `POST /api/v1/auth/login` y `POST /api/v1/auth/refresh`. Login devuelve JWT en cookie `httpOnly + Secure + SameSite=Strict` + JSON con `usuario`.
- [ ] **Step 3:** `deps.py` con `get_current_usuario(request, db)` que extrae JWT de cookie, valida, devuelve `Usuario` o lanza 401. Y `require_admin(usuario)` que valida rol.
- [ ] **Step 4:** Middleware de service token: si request lleva `X-Service-Token` válido, bypass de JWT y marca `request.state.is_service=True` con identidad `luna`.
- [ ] **Step 5:** rate limit in-memory en `/auth/login`: 5 intentos/IP/15min → bloqueo 1h. Bare-bones counter en dict (suficiente para 2 usuarios).
- [ ] **Step 6:** Tests:
  - `test_login_ok`: password correcta → 200 + cookie + JWT válido
  - `test_login_password_invalida`: 401
  - `test_login_email_inexistente`: 401
  - `test_jwt_expirado`: 401
  - `test_jwt_invalido`: 401
  - `test_service_token_ok`: bypass funciona
  - `test_service_token_invalido`: 401
  - `test_rate_limit`: 6 intentos seguidos → 429
- [ ] **Step 7:** commit + push.

### T1.4 — Validador + tests  · agent: **Opus 4.7**

**Files:** Create `backend/app/services/validador.py`, `backend/app/services/consolidador.py`, `tests/test_validador.py`, `tests/test_consolidador.py`.

Implementa las 10 validaciones del SPEC §4.5. Cada regla = una función pura testeable.

- [ ] **Step 1:** `consolidador.py` con `consolidar_actores_top5(top5: list[dict]) → list[dict]` que normaliza `DEPOSITO|TRANSFER|TRANSFERENCIA|TRANSFER_DEPOSITO → "TRANSFER. / DEPTOS."` antes de validar.
- [ ] **Step 2:** `validador.py` con `validar_ingesta(candidato: IngestaCandidatoIn, db) → ValidacionResult`. `ValidacionResult` = lista de `{regla, ok, detalles}`. Reglas:
  1. `cuadre_efectiva_recuperada_vs_total`: `|EFECTIVA + RECUPERADA - TOTAL_GENERAL| ≤ 0.01`
  2. `etiquetas_consolidadas`: ningún Top5 menciona `DEPOSITO|TRANSFER|TRANSFERENCIA` suelto
  3. `top5_porcentaje_no_excede`: suma de % ≤ 100% por categoría
  4. `top5_tamano`: 5 entradas o marca incompleto
  5. `mes_no_cerrado_sin_force`: status≠cerrado o `force=true`
  6. `hash_unico_o_force`: dedup
  7. `montos_sanidad`: ningún monto > 10M (warn)
  8. `actores_conocidos`: todos resueltos en DB o `alta_automatica=true`
  9. `rango_mes_anio`: 1≤mes≤12, 2020≤anio≤2100
  10. `lugares_top5_validos`: lugar ∈ [1,5], sin duplicados
- [ ] **Step 3:** Tests por cada regla — 10+ casos cada una (happy path, edge case, error path):
  ```python
  def test_cuadre_pasa_con_centavos_de_tolerancia(): ...
  def test_cuadre_falla_con_diferencia_significativa(): ...
  def test_consolidador_normaliza_DEPOSITO(): ...
  def test_consolidador_normaliza_TRANSFER_DEPOSITO(): ...
  def test_consolidador_no_toca_TRANSFER_DEPTOS_ya_consolidado(): ...
  ```
- [ ] **Step 4:** Coverage mínimo 90% del módulo `validador.py`. `pytest --cov=app.services.validador`.
- [ ] **Step 5:** commit + push.

### T1.5 — Router meses (GET)  · agent: **Sonnet 4.6**

**Files:** Create `backend/app/routers/meses.py`, `tests/test_meses.py`.

- [ ] **Step 1:** Endpoints SPEC §3.2:
  - `GET /api/v1/meses` → lista de meses cargados (sin detalles)
  - `GET /api/v1/meses/{anio}/{mes}` → detalle completo (concentrado + top5 + total + proyección)
- [ ] **Step 2:** Queries SQL con joins eager (`selectinload`) para evitar N+1.
- [ ] **Step 3:** Tests con fixture de mes seedeado:
  - `test_listar_meses_vacio`
  - `test_listar_meses_con_data`
  - `test_detalle_mes_inexistente_404`
  - `test_detalle_mes_completo` (verifica shape de la respuesta)
- [ ] **Step 4:** commit + push.

### T1.6 — Router tendencia + vista materializada  · agent: **Opus 4.7**

**Files:** Create `backend/app/routers/tendencia.py`, `tests/test_tendencia.py`, migración nueva `0002_mv_tendencia.py`.

- [ ] **Step 1:** Migración `0002_add_mv_tendencia.py` con SPEC §2.2 (CREATE MATERIALIZED VIEW + index unique).
- [ ] **Step 2:** `GET /api/v1/tendencia?anios=2025,2026&concepto=EFECTIVA` consulta `mv_tendencia_anual`, devuelve estructura SPEC §3.2.
- [ ] **Step 3:** Validar params (anios comma-separated, concepto enum, max 5 años para no abusar).
- [ ] **Step 4:** Test que crea 2 meses de 2 años distintos, verifica que tendencia devuelve ambas series con shape correcto.
- [ ] **Step 5:** commit + push.

### T1.7 — Router actores  · agent: **Sonnet 4.6**

**Files:** Create `backend/app/routers/actores.py`, `tests/test_actores.py`.

- [ ] **Step 1:** Endpoints:
  - `GET /api/v1/actores?activo=true` (default sin filtro)
  - `POST /api/v1/actores` (admin) — alta
  - `PATCH /api/v1/actores/{id}` (admin) — edición
- [ ] **Step 2:** Validaciones: codigo `^V\d+$` o NULL; nombre único; tipo en enum; id_empleado_legacy único cuando no NULL.
- [ ] **Step 3:** Tests: alta OK, alta duplicada (409), patch toggle activo, listar con filtro.
- [ ] **Step 4:** commit + push.

### T1.8 — Router ingesta (preview + commit + patch)  · agent: **Opus 4.7**

**Files:** Create `backend/app/routers/ingesta.py`, `backend/app/services/ingesta.py`, `tests/test_ingesta.py`.

- [ ] **Step 1:** `services/ingesta.py` con:
  - `preview(candidato) → IngestaPreviewOut` — invoca validador, NO persiste, calcula `diff` (nuevo vs cambios).
  - `commit(candidato) → IngestaCommitOut` — re-valida + inserta/UPSERT + escribe `ingesta_logs`.
  - `patch_concepto(mes_id, concepto, monto, razon)` — UPDATE puntual + re-valida cuadre + log.
- [ ] **Step 2:** Endpoints SPEC §3.2 con `X-Service-Token` auth. `POST /ingesta/preview`, `POST /ingesta/commit`, `PATCH /meses/{id}/concepto/{concepto}`.
- [ ] **Step 3:** Manejo de `force=true` en commit (override de validaciones soft: hash dedup, mes cerrado).
- [ ] **Step 4:** Tests:
  - `test_preview_valido_no_persiste`
  - `test_commit_inserta_y_loguea`
  - `test_commit_dedup_hash`
  - `test_commit_force_override_mes_cerrado`
  - `test_patch_concepto_actualiza_y_revalida_cuadre`
  - `test_patch_concepto_rompe_cuadre_rechazado`
  - `test_alta_automatica_actor_desconocido`
- [ ] **Step 5:** commit + push.

### T1.9 — Router admin (logs + cerrar mes + reset password)  · agent: **Sonnet 4.6**

**Files:** Create `backend/app/routers/admin.py`, `backend/app/services/admin.py`, `tests/test_admin.py`, `backend/scripts/reset_password.py`.

- [ ] **Step 1:** Endpoints:
  - `GET /api/v1/admin/logs?mes_id=X&limit=50` (admin)
  - `POST /api/v1/meses/{id}/cerrar` (admin) → status='cerrado', cerrado_en=now, cerrado_por=usuario
- [ ] **Step 2:** Script standalone `scripts/reset_password.py --email --nueva` para bootstrap inicial.
- [ ] **Step 3:** Tests: listar logs filtrado por mes, cerrar mes feliz, cerrar mes ya cerrado (409).
- [ ] **Step 4:** commit + push.

### T1.10 — Tests de integración  · agent: **Opus 4.7**

**Files:** Create `tests/integration/{test_flujo_completo_ingesta,test_auth_full,test_consulta_completa}.py`.

- [ ] **Step 1:** `test_flujo_completo_ingesta`: con service token, POST /preview → POST /commit → GET /meses/{anio}/{mes} → verifica todo el shape devuelto match al JSON candidato original.
- [ ] **Step 2:** `test_auth_full`: login → cookie set → call protected endpoint → 200 → logout (deletar cookie) → call protegido → 401.
- [ ] **Step 3:** `test_consulta_completa`: precargar 6 meses, GET /meses → 6 elementos, GET tendencia → 2 series correctas.
- [ ] **Step 4:** commit + push.

### 🔍 AUDITORÍA F1 ADVERSARIAL  · agent: **Opus 4.7 adversarial**

**Briefing:**
> QA hostil contra el backend completo. Buscar bugs de auth, race conditions en ingesta, validaciones bypaseables, errores de tipo Decimal/float, SQL injection, missing CASCADE en deletes.

- [ ] **Step 1:** Intentar bypass de auth: JWT sin firma, JWT firmado con secret distinto, cookie tampered, service token con rol distinto.
- [ ] **Step 2:** Race condition: 2 commits concurrentes del mismo mes/año. Debería UNIQUE constraint atrapar.
- [ ] **Step 3:** Decimal precisions: cargar mes con monto `123.456789` y verificar que se trunca/round a 2 decimales sin perder en el JSON respuesta.
- [ ] **Step 4:** SQL injection en query params (`?concepto=EFECTIVA' OR 1=1--`). Debería 422 por enum mismatch.
- [ ] **Step 5:** Cascade: DELETE de un mes → todos los `top5/conceptos/proyecciones/totales` deben caer. Verificar.
- [ ] **Step 6:** Coverage real: `pytest --cov=app --cov-report=html` debe estar ≥80% global, ≥90% en `validador.py`.
- [ ] **Step 7:** Reporte en `reports/F1-audit-<fecha>.md`. Cualquier critical bloquea F2.

---

# FASE 2 — Migración + Skill + CLI (2-3 días)

**Tabla de paralelización F2:**

| Task | Agent | Depende de | Paralelizable con |
|------|-------|------------|-------------------|
| T2.1 Seeds (actores activos + históricos) | **Opus** | F1 | T2.4 inicio, T2.7 inicio |
| T2.2 Script migración 2025 | **Opus** | T2.1 | T2.4, T2.7 |
| T2.3 Reporte HTML validación | Sonnet | T2.2 | T2.4, T2.7 |
| T2.4 CLI sicc (parse + preview + commit) | **Opus** | F1 | T2.1, T2.7 |
| T2.5 CLI parser PPTX | **Opus** | T2.4 | T2.6, T2.7 |
| T2.6 CLI comandos auxiliares (show/update/cerrar) | Sonnet | T2.4 | T2.5, T2.7 |
| T2.7 Skill sicc-ingesta | **Opus** | T2.4 | T2.1, T2.2, T2.5 |
| T2.8 Dry run con Elena | manual (Claudio) | T2.3, T2.7 | — |
| 🔍 F2 Audit | **Opus adversarial** | T2.8 | — |

### T2.1 — Seeds (actores activos + históricos desde Legacy)  · agent: **Opus 4.7**

**Files:** Create `backend/app/seeds.py`, `backend/scripts/seed_actores_historicos.py`.

- [ ] **Step 1:** `seeds.py` ejecuta los INSERTs del SPEC §2.3 (4 cobradores puros, 2 virtuales OFICINA/TRANSFER., 15 vendedores activos, 2 usuarios). Idempotente con `ON CONFLICT DO NOTHING`.
- [ ] **Step 2:** `seed_actores_historicos.py` se conecta a Legacy MySQL Hostinger (credentials desde `LEGACY_DB_HOST/USER/PASS/NAME` env vars, mismas que `/opt/legacy-api/.env` en lunita) con `mysql.connector`, query `SELECT id_empleado, nombre, nombre_completo, nombre_clave, es_vendedor, es_cobrador, activo FROM empleados WHERE es_vendedor=1 OR es_cobrador=1`, inserta cualquier no-existente en `actores` con `activo=row.activo`, `id_empleado_legacy=row.id_empleado`. Idempotente.
- [ ] **Step 3:** Manejo del caso V5: si encuentra `codigo='V5'` en Legacy, NO lo inserta (es código erróneo histórico según ADR-004).
- [ ] **Step 4:** Tests: con DB vacía, ejecutar seeds.py → 21 actores; ejecutar otra vez → sigue siendo 21 (idempotente).
- [ ] **Step 5:** commit + push.

### T2.2 — Script migración 2025  · agent: **Opus 4.7**

**Files:** Create `backend/scripts/migrar_2025.py`.

Lee `ESTADISTICA_2025.xlsx`, construye JSON candidato por cada uno de los 12 meses, postea a `/api/v1/ingesta/commit` con `X-Service-Token` y `force_fuente=True`.

- [ ] **Step 1:** Cargar xlsx con `openpyxl`. Parsear hoja `DATOS GRAL.` (12 filas × 14 cols): mes (col A) + 7 conceptos con monto y % (cols B-O).
- [ ] **Step 2:** Para cada hoja Top5 (CORRIENTE, CANCELACIONES, VENCIDA, EFECTIVA, RECUPERADA, TOTAL_GRAL., ADELANTADA F.), parsear `MES | TOTAL MENSUAL | VENDEDOR1 | TOTAL1 | %1 | ... | VENDEDOR5 | TOTAL5 | %5`. Skip filas vacías o duplicadas (vimos `DICIEMBRE | DICIEMBRE`).
- [ ] **Step 3:** Parsear `PROYECCION SIG. MES` (12×4).
- [ ] **Step 4:** Resolver actores: por código `V\d+` o por nombre (`EDGAR`, `JORGE`, etc.). Si `DEPOSITO`/`TRANSFER` aparece, consolidar a `TRANSFER. / DEPTOS.`.
- [ ] **Step 5:** Por cada mes: construir JSON candidato, POST a `/api/v1/ingesta/commit`. Si error, loggear y continuar al siguiente.
- [ ] **Step 6:** Al final, generar resumen: meses cargados / fallados / actores nuevos creados.
- [ ] **Step 7:** Test E2E: `pytest tests/test_migracion_2025.py` que corre el script contra DB local con seeds + xlsx fixture pequeño (mes enero) y verifica que GET /meses/2025/1 devuelve la data correcta.
- [ ] **Step 8:** commit + push.

### T2.3 — Reporte HTML de validación post-migración  · agent: **Sonnet 4.6**

**Files:** Create `backend/scripts/reporte_validacion.py`.

- [ ] **Step 1:** Script que toma año (default 2025), recorre los 12 meses, compara DB vs xlsx fuente, y genera HTML con:
  - Tabla resumen: monto total por concepto por mes, ✅/❌ por mes.
  - Detalle de discrepancias (montos que no coinciden centavo a centavo).
  - Top5 por categoría: verifica que las 5 entradas estén y los actores resuelvan.
- [ ] **Step 2:** Output a `reports/validacion-migracion-2025-<fecha>.html`. Diseño básico con tabla + colorización ✅/❌.
- [ ] **Step 3:** commit + push.

### T2.4 — CLI `sicc` core (parse + preview + commit)  · agent: **Opus 4.7**

**Files:** Create `cli/pyproject.toml`, `cli/sicc/__init__.py`, `cli/sicc/cli.py`, `cli/sicc/client.py`, `cli/sicc/config.py`.

- [ ] **Step 1:** `pyproject.toml` con entry point `sicc = sicc.cli:main`. Deps: `click>=8`, `httpx`, `pydantic`, `rich`, `python-pptx`, `openpyxl`, `pillow`.
- [ ] **Step 2:** `config.py`: lee `~/.config/sicc/config.toml` con `api_base` (default `https://sicc.protegrt.com/api/v1`) y `service_token` (desde env `SICC_LUNA_TOKEN`).
- [ ] **Step 3:** `client.py` con `SiccClient` (httpx.Client) que hace POST a `/ingesta/preview`, `/ingesta/commit`, GET a `/meses/...`, etc. Manejo de errores HTTP con mensajes legibles.
- [ ] **Step 4:** `cli.py` con `click.group()` y subcomandos `parse`, `preview`, `commit`. `parse` lee archivo (pptx/xlsx/imagen) y produce JSON candidato a stdout o `--out`. `preview` POST a backend con `--json`. `commit` idem `--json`.
- [ ] **Step 5:** Salida bonita con `rich`: tabla de validaciones del preview, diff coloreado, confirmación interactiva para commit.
- [ ] **Step 6:** Tests CLI con `click.testing.CliRunner`. Mockear `SiccClient`. Verificar: `sicc parse --imagen test.png` produce JSON válido; `sicc preview --json X.json` muestra tabla.
- [ ] **Step 7:** commit + push.

### T2.5 — CLI parser PPTX  · agent: **Opus 4.7**

**Files:** Create `cli/sicc/parsers/pptx.py`, `cli/sicc/parsers/image.py`, `cli/sicc/parsers/xlsx.py`.

- [ ] **Step 1:** `pptx.py`: con `python-pptx`, abre PPTX. Para cada slide, extrae:
  - Título (placeholder 0) → identifica categoría (`Cobranza Corriente` → CORRIENTE).
  - Text box con `TOTAL $X` → extrae monto.
  - Picture (shape_type=13) → guarda a `/tmp/sicc/<hash>/slide_N.png` con `shape.image.blob`.
  Devuelve dict con totales por categoría + paths de imágenes para que Luna las lea con vision.
- [ ] **Step 2:** `image.py`: si Elena manda screenshot suelto, parser pasa el path tal cual al output. Luna lo lee con `Read` multimodal.
- [ ] **Step 3:** `xlsx.py`: parser del xlsx 2025 reusable (lo mismo que T2.2 pero como módulo importable). Para uso futuro si Elena manda xlsx puntuales.
- [ ] **Step 4:** Tests: PPTX fixture (REPORTE_COBRANZA_JUNIO_2025.pptx) → output esperado con totales correctos y paths de imágenes existentes.
- [ ] **Step 5:** commit + push.

### T2.6 — CLI comandos auxiliares (show, update, cerrar, meses)  · agent: **Sonnet 4.6**

**Files:** Modify `cli/sicc/cli.py`.

- [ ] **Step 1:** `sicc show --anio Y --mes M [--categoria X] [--formato markdown|json]` — GET al backend, formatea con `rich` o markdown.
- [ ] **Step 2:** `sicc update --anio Y --mes M --concepto X --monto N --razon T` — PATCH al backend.
- [ ] **Step 3:** `sicc cerrar --anio Y --mes M --confirm` — POST al backend.
- [ ] **Step 4:** `sicc meses [--anio Y]` — GET lista.
- [ ] **Step 5:** Tests para cada comando.
- [ ] **Step 6:** commit + push.

### T2.7 — Skill `sicc-ingesta`  · agent: **Opus 4.7**

**Files:** Create `skill/sicc-ingesta/SKILL.md`, `skill/sicc-ingesta/references/{reglas-de-negocio,catalogo-actores,formato-pptx}.md`, `skill/sicc-ingesta/scripts/{extract_pptx.py,consolidar.py}`.

- [ ] **Step 1:** `SKILL.md` con frontmatter SPEC §4.2 + cuerpo. Cuerpo describe el flujo paso a paso para Luna:
  1. Identificar trigger (Elena adjuntó PPTX o dijo "cárgame...")
  2. Ejecutar `sicc parse --pptx <path>` → obtiene JSON + paths de imágenes
  3. Por cada imagen, hacer `Read <path>` y extraer Top5 visualmente
  4. Construir el JSON final con Top5 completos
  5. `sicc preview --json /tmp/sicc/.../data.json` → mostrar a Elena
  6. Esperar confirmación
  7. `sicc commit --json ...`
  8. Responder a Elena con resumen
- [ ] **Step 2:** `references/reglas-de-negocio.md` — extracto de las reglas relevantes del SKILL viejo `estadistica-mensual-cobranza/SKILL.md` (base 100%, exclusiones, regla TRANSFER./DEPTOS., criterio dual VENDEDOR/COBRADO por categoría).
- [ ] **Step 3:** `references/catalogo-actores.md` — V1..V114 con sus nombres reales (mantener sincronizado con DB).
- [ ] **Step 4:** `references/formato-pptx.md` — descripción de los 10 slides esperados, qué slot corresponde a qué categoría.
- [ ] **Step 5:** Deploy de la skill a `/home/elena/.openclaw/workspace/skills/sicc-ingesta/` en lunita.
- [ ] **Step 6:** commit + push.

### T2.8 — Dry run con Elena  · operativo (Claudio)

- [ ] **Step 1:** Claudio coordina con Elena para que Luna ingiera 1 mes 2026 conocido (enero o febrero) end-to-end.
- [ ] **Step 2:** Elena valida visualmente el resultado en la web.
- [ ] **Step 3:** Si algo falla, abre task de fix antes de audit.
- [ ] **Step 4:** Report por Telegram a Fer del resultado del dry run.

### 🔍 AUDITORÍA F2 ADVERSARIAL  · agent: **Opus 4.7 adversarial**

- [ ] **Step 1:** Reportar y reproducir el resultado de `migrar_2025.py` end-to-end. ¿12 meses cargados? ¿Cuántos actores nuevos creados? ¿Errores silenciados?
- [ ] **Step 2:** Validar cuadre por mes manualmente para 3 meses sample. Comparar montos DB vs xlsx fuente al centavo.
- [ ] **Step 3:** Probar consolidación: cargar un PPTX falso con `DEPOSITO` y `TRANSFERENCIA` separados, verificar que consolidar.py los une como `TRANSFER. / DEPTOS.` antes de validar.
- [ ] **Step 4:** Skill `sicc-ingesta` se carga limpia en Claude Code de Luna sin syntax errors en frontmatter.
- [ ] **Step 5:** CLI: `sicc --help` muestra todos los subcomandos. Tab completion funciona si está instalado.
- [ ] **Step 6:** Reporte `reports/F2-audit-<fecha>.md`.

---

# FASE 3 — Frontend (3 días)

**Tabla de paralelización F3:**

| Task | Agent | Depende de | Paralelizable con |
|------|-------|------------|-------------------|
| T3.1 Vite + Tailwind + tokens DESIGN | Sonnet | F2 | T3.2 |
| T3.2 Auth flow + AuthGuard | **Opus** | F1 | T3.1, T3.3 |
| T3.3 Componentes ui/ (Button, Input, Card, Badge, Alert) | Sonnet | T3.1 | T3.2 |
| T3.4 MesSelector + KpiCard + Sparkline | **Opus** | T3.3 | T3.5, T3.6 |
| T3.5 Top5Tabs + Top5Table | **Opus** | T3.3 | T3.4, T3.6 |
| T3.6 TendenciaChart (Recharts) | **Opus** | T3.3 | T3.4, T3.5 |
| T3.7 ConcentradoTable | Sonnet | T3.3 | T3.4, T3.5, T3.6 |
| T3.8 Vista /dashboard | **Opus** | T3.4, T3.5, T3.6, T3.7 | — |
| T3.9 Vista /comparativa + PDF export | **Opus** | T3.8 | — |
| T3.10 Vistas /admin/* | Sonnet | T3.8 | T3.9 |
| T3.11 Layout global + Footer institucional | Sonnet | T3.3 | T3.4-T3.10 |
| T3.12 Mobile responsive + a11y | Sonnet | T3.11 | — |
| T3.13 Tests playwright | **Opus** | T3.12 | — |
| 🔍 F3 Audit | **Opus adversarial** | T3.13 | — |

### T3.1 — Vite + Tailwind 4 + tokens DESIGN.md  · agent: **Sonnet 4.6**

**Files:** Create `frontend/package.json`, `frontend/vite.config.ts`, `frontend/tailwind.config.ts`, `frontend/tsconfig.json`, `frontend/index.html`, `frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/src/styles/globals.css`.

- [ ] **Step 1:** `npm create vite@latest frontend -- --template react-ts`. Mover archivos a `frontend/`.
- [ ] **Step 2:** Instalar Tailwind 4: `npm install -D tailwindcss@next @tailwindcss/vite`. Configurar `vite.config.ts` con plugin Tailwind 4. `tailwind.config.ts` con paths.
- [ ] **Step 3:** `globals.css` con `@theme` que importa TODOS los tokens del DESIGN.md v2 §2-§4: colores (navy 50-900, gold soft/main/deep, red soft/main, cream, neutral 100/300/500/900, success), font families, font sizes (xs..display), espaciado, radii, borders, shadows. Usar `oklch()` donde DESIGN.md lo especifica.
- [ ] **Step 4:** Font loading: link tags a Google Fonts para Saira Condensed (800, 900 italic), Montserrat (400/500/600), Poppins Black Italic (900), JetBrains Mono (400/500) en `index.html` con `display=swap`.
- [ ] **Step 5:** Variable CSS `--font-display`, `--font-display-italic`, `--font-italic`, `--font-body`, `--font-mono` en `globals.css`. Utility class `.t-italic-display` y `.gold-foil` del DESIGN.md §3.4 y §3.5.
- [ ] **Step 6:** Smoke test: `npm run dev`, abrir localhost:5173, verificar que el body usa Montserrat y los headings Saira Condensed 800 CAPS.
- [ ] **Step 7:** commit + push.

### T3.2 — Auth flow + cookie httpOnly + AuthGuard  · agent: **Opus 4.7**

**Files:** Create `frontend/src/lib/api.ts`, `frontend/src/lib/auth.ts`, `frontend/src/hooks/useAuth.ts`, `frontend/src/components/AuthGuard.tsx`, `frontend/src/routes/login.tsx`.

- [ ] **Step 1:** `api.ts`: fetch wrapper que mete `credentials: 'include'` por default. Base URL desde `VITE_API_BASE`.
- [ ] **Step 2:** `auth.ts`: `login(email, password)` POST a `/auth/login` (cookie se setea sola), `logout()` borra cookie via endpoint, `getCurrentUser()` GET `/auth/me` (a agregar al backend si no existe).
- [ ] **Step 3:** `useAuth.ts`: TanStack Query hook que mantiene estado del usuario. Invalida en login/logout.
- [ ] **Step 4:** `AuthGuard.tsx`: wrapper de rutas privadas. Si no autenticado, redirect a `/login` con `from=<ruta>` query param.
- [ ] **Step 5:** `routes/login.tsx`: form con email + password aplicando DESIGN.md (Input + Button primary). Submit → `login()` → redirect a `from` o `/dashboard`.
- [ ] **Step 6:** Tests vitest del hook + componente Login.
- [ ] **Step 7:** commit + push.

### T3.3 — Componentes ui/ base  · agent: **Sonnet 4.6**

**Files:** Create `frontend/src/components/ui/{Button,Input,Card,Badge,Alert,Eyebrow,PullQuote}.tsx`.

Aplicar exactamente las specs del DESIGN.md §5.

- [ ] **Step 1:** `Button` con variantes `primary | secondary | gold | ghost | destructive | link` y sizes `sm | md | lg`. Hover/focus/disabled states.
- [ ] **Step 2:** `Input` con label + helper + error states del DESIGN.md §5.6.
- [ ] **Step 3:** `Card` con variantes `editorial | feature | hero` (DESIGN.md §5.3). Feature con `border-block-start: 4px solid var(--gold)`.
- [ ] **Step 4:** `Badge` con `default | gold | red | outline` (DESIGN.md §5.4).
- [ ] **Step 5:** `Alert` con `info | warn | urgent | success` y `border-inline-start` colorizado (DESIGN.md §5.5).
- [ ] **Step 6:** `Eyebrow` 11px Montserrat 600 CAPS gold-deep (DESIGN.md §5.7).
- [ ] **Step 7:** `PullQuote` Poppins Black Italic 900 con regla gold lateral (DESIGN.md §5.8).
- [ ] **Step 8:** Storybook o página `/dev/showcase` interna que renderiza todos los componentes para validación visual.
- [ ] **Step 9:** commit + push.

### T3.4 — MesSelector + KpiCard + Sparkline  · agent: **Opus 4.7**

**Files:** Create `frontend/src/components/{MesSelector,KpiCard,Sparkline}.tsx`, `frontend/src/hooks/{useMes,useTendencia}.ts`.

- [ ] **Step 1:** `MesSelector`: dos `<Select>` (año, mes) con animación de transición al cambiar. Sincronizados (cambio de año reset mes si no existe).
- [ ] **Step 2:** `KpiCard` props: `concepto, monto, deltaMesAnterior, deltaAnioAnterior, sparklineData`. Render:
  - Eyebrow CAPS con concepto.
  - Monto en mono tabular-nums 36-44px.
  - Delta 1: % + flecha + color verde/rojo.
  - Delta 2: tooltip con vs año anterior.
  - Sparkline 1px navy-700 al pie.
- [ ] **Step 3:** `Sparkline` SVG inline (no Recharts para 6 puntos). Path generated de los `monto` últimos 6 meses.
- [ ] **Step 4:** Tests visuales en showcase + unit tests de cálculo de delta.
- [ ] **Step 5:** commit + push.

### T3.5 — Top5Tabs + Top5Table  · agent: **Opus 4.7**

**Files:** Create `frontend/src/components/{Top5Tabs,Top5Table,ActorBadge}.tsx`.

- [ ] **Step 1:** `Top5Tabs` con 7 tabs (Corriente | Cancelaciones | Vencida | Efectiva | Recuperada | Total Gral | Adelantada). State del activo.
- [ ] **Step 2:** `Top5Table` recibe `entries` (lista de 5). Cada entrada:
  - Número de lugar en Saira 900 italic 32px (`.t-italic-display`).
  - `ActorBadge` con código/nombre del actor + tooltip nombre_completo.
  - Monto en mono.
  - % en mono small.
  - Barra visual proporcional con `<div>` background `gradient(navy-700 → navy-800)` para lugar 1, decay hacia navy-500 para lugar 5. `width: <%>%`.
- [ ] **Step 3:** `ActorBadge` para personas (V1, V6, EDGAR, etc.) muestra iniciales en círculo navy. Para OFICINA / TRANSFER. / DEPTOS. muestra icono lucide (`Building2`, `ArrowLeftRight`).
- [ ] **Step 4:** Tests visuales + unit.
- [ ] **Step 5:** commit + push.

### T3.6 — TendenciaChart (Recharts)  · agent: **Opus 4.7**

**Files:** Create `frontend/src/components/TendenciaChart.tsx`.

- [ ] **Step 1:** Props: `anios: number[]`, `concepto: string`. Hook interno `useTendencia(anios, concepto)` que llama `/api/v1/tendencia`.
- [ ] **Step 2:** Recharts `<LineChart>` con `<XAxis dataKey="mes" tickFormatter={(m)=>monthShort(m)}>`, `<YAxis tickFormatter={(v)=>formatMontoCompact(v)}>`, `<CartesianGrid stroke=neutral-300 strokeDasharray="3 3">`. Una `<Line>` por año (año actual = navy-800 solid, año anterior = navy-400 dashed).
- [ ] **Step 3:** Tooltip custom con DESIGN.md aesthetic (card editorial blanca con number en mono).
- [ ] **Step 4:** Animación de entrada `animationBegin=0 animationDuration=600 animationEasing="ease-out"`. Stagger entre series.
- [ ] **Step 5:** Soporte `prefers-reduced-motion` para deshabilitar animaciones.
- [ ] **Step 6:** Tests visuales + unit (mock data).
- [ ] **Step 7:** commit + push.

### T3.7 — ConcentradoTable  · agent: **Sonnet 4.6**

**Files:** Create `frontend/src/components/ConcentradoTable.tsx`.

- [ ] **Step 1:** Tabla con 7 filas (uno por concepto del DATOS GRAL.). Columnas: Concepto, Monto, %.
- [ ] **Step 2:** Headers en eyebrow CAPS gold-deep. Cifras en mono tabular-nums. Total row al final destacado en navy-800 cream.
- [ ] **Step 3:** commit + push.

### T3.8 — Vista `/dashboard`  · agent: **Opus 4.7**

**Files:** Create `frontend/src/routes/dashboard.tsx`.

- [ ] **Step 1:** Layout completo SPEC §6 RF-2:
  - Header con `MesSelector` flotando a la derecha.
  - Grid 6 KPI cards.
  - Grid 2 columnas: `ConcentradoTable` izquierda, `TendenciaChart` derecha.
  - Sección `Top5Tabs`.
- [ ] **Step 2:** Estado: mes/año desde URL (`?anio=2026&mes=2`) o defaults al mes vigente más reciente.
- [ ] **Step 3:** Tests playwright: navegar, cambiar mes, verificar que TODOS los componentes recargan con nueva data.
- [ ] **Step 4:** commit + push.

### T3.9 — Vista `/comparativa` + PDF export  · agent: **Opus 4.7**

**Files:** Create `frontend/src/routes/comparativa.tsx`, `frontend/src/components/{ComparativaAnual,PdfExportButton}.tsx`.

- [ ] **Step 1:** Header narrativo: "Cobranza Proteg-rt · año actual vs año anterior · cierre [mes]" en display Saira CAPS.
- [ ] **Step 2:** Big number hero: total general año actual con `.gold-foil` aplicado. Big number año anterior debajo en `navy-400`.
- [ ] **Step 3:** Gráfica grande tendencia con `<TendenciaChart anios={[year-1, year]} />`.
- [ ] **Step 4:** Tabla comparativa por concepto: 7 filas, columnas Concepto | Año actual | Año anterior | Δ %. Δ con color y flecha.
- [ ] **Step 5:** Sección mini-cards Top1/Top3 por categoría con avatars.
- [ ] **Step 6:** `PdfExportButton` usa `react-to-print` o `html2pdf.js`. Genera PDF con marca Proteg-rt en header, footer institucional.
- [ ] **Step 7:** Tests playwright: navegar a `/comparativa`, click export PDF, verificar download.
- [ ] **Step 8:** commit + push.

### T3.10 — Vistas `/admin/*`  · agent: **Sonnet 4.6**

**Files:** Create `frontend/src/routes/admin/{meses,logs,actores}.tsx`.

- [ ] **Step 1:** `/admin/meses`: tabla de meses con status, botón "Cerrar mes" con confirmación modal.
- [ ] **Step 2:** `/admin/logs`: tabla de `ingesta_logs` con filtros por mes y agente. Detalles expandibles.
- [ ] **Step 3:** `/admin/actores`: CRUD básico de catálogo. Formulario para crear/editar.
- [ ] **Step 4:** Todos con `AuthGuard` que requiere rol admin.
- [ ] **Step 5:** commit + push.

### T3.11 — Layout global + Footer institucional  · agent: **Sonnet 4.6**

**Files:** Create `frontend/src/components/{Layout,Header,Footer}.tsx`.

- [ ] **Step 1:** `Layout` wrap principal de rutas. Header sticky con logo + nav + usuario menu.
- [ ] **Step 2:** `Header`: logo a la izquierda (importado de `/public/logo.png`), nav (`/dashboard`, `/comparativa`, `/admin` si admin), avatar usuario a la derecha con dropdown (logout).
- [ ] **Step 3:** `Footer`: layout institucional del DESIGN.md §5.9. Wordmark slot, slogan oficial "Porque nuestro principal objetivo es Protegerte.", regla horizontal, © 2026.
- [ ] **Step 4:** commit + push.

### T3.12 — Mobile responsive + a11y  · agent: **Sonnet 4.6**

**Files:** Modify todos los componentes que necesiten breakpoints.

- [ ] **Step 1:** Breakpoints Tailwind: sm 640 / md 768 / lg 1024 / xl 1280. Mobile-first.
- [ ] **Step 2:** Grid 6 KPI cards → 2 cols en mobile, 3 en tablet, 6 en desktop.
- [ ] **Step 3:** TendenciaChart con `<ResponsiveContainer>`.
- [ ] **Step 4:** Top5Tabs scrollable horizontal en mobile.
- [ ] **Step 5:** a11y: focus visible en todo, aria-labels, semántica correcta (`<main>`, `<nav>`, `<footer>`), `lang="es-MX"`. Verificar con axe DevTools.
- [ ] **Step 6:** commit + push.

### T3.13 — Tests playwright golden path  · agent: **Opus 4.7**

**Files:** Create `frontend/tests/playwright/{login,dashboard,comparativa,admin}.spec.ts`.

- [ ] **Step 1:** Setup playwright config con base URL local + auth state shared.
- [ ] **Step 2:** `login.spec.ts`: login KO + login OK + persist session.
- [ ] **Step 3:** `dashboard.spec.ts`: navegar 2026/1, verificar todas las secciones cargan, cambiar a 2025/12, verificar refetch.
- [ ] **Step 4:** `comparativa.spec.ts`: navegar, verificar gráfica + tabla + cards, export PDF.
- [ ] **Step 5:** `admin.spec.ts`: ver lista de meses, ver logs.
- [ ] **Step 6:** Smoke total <60s.
- [ ] **Step 7:** commit + push.

### 🔍 AUDITORÍA F3 ADVERSARIAL  · agent: **Opus 4.7 adversarial**

- [ ] **Step 1:** Aplicación visual real: levantar `npm run build && npm run preview`, abrir en Chrome + iOS Safari, capturar screenshots de cada vista. Compararlas contra el DESIGN.md y reportar TODO desvío (colores, tipografía, spacing).
- [ ] **Step 2:** Color contrast: medir TODO texto con DevTools. ≥4.5:1 body, ≥3:1 headings.
- [ ] **Step 3:** Performance: Lighthouse mobile en `/dashboard`. Performance ≥85, Accessibility ≥95.
- [ ] **Step 4:** Bundle size: `dist/` total <500KB gzipped.
- [ ] **Step 5:** XSS: intentar inyectar `<script>alert(1)</script>` en nombres de actor. React debería escapar.
- [ ] **Step 6:** Mobile: probar layout en iPhone 13 mini (375px), iPad (768px). Sin scroll horizontal.
- [ ] **Step 7:** Reporte `reports/F3-audit-<fecha>.md`. Critical bloquea F4.

---

# FASE 4 — Ingesta 2026 + pulido (1-2 días)

**Tabla de paralelización F4:**

| Task | Agent | Depende de | Paralelizable con |
|------|-------|------------|-------------------|
| T4.1 Conseguir PPTX 2026 ene+feb | manual | — | T4.4, T4.5 |
| T4.2 Luna ingiere ene+feb 2026 | operativo (Luna+Claudio) | T4.1 | T4.4, T4.5 |
| T4.3 Elena valida ingesta | operativo (Elena+Claudio) | T4.2 | T4.4, T4.5 |
| T4.4 Pulir animaciones | **Opus** | F3 | T4.1-T4.3, T4.5 |
| T4.5 Copy + formato es-MX | Sonnet | F3 | T4.1-T4.3, T4.4 |
| T4.6 Fixes bugs | **Opus** | T4.3 | — |
| 🔍 F4 Audit | **Opus adversarial** | T4.6 | — |

### T4.1-T4.3 — Operativo (ingesta 2026)

- [ ] **T4.1:** Claudio confirma con Fer/Elena que los PPTX 2026 enero+febrero están en lunita o se reenvían a Luna por Telegram.
- [ ] **T4.2:** Luna ejecuta `sicc parse --pptx ... && sicc preview && sicc commit` para ambos meses.
- [ ] **T4.3:** Elena entra a la web, valida que los números coinciden con sus xlsx 2026, marca los meses como `revisado` o `cerrado` desde `/admin/meses`.

### T4.4 — Pulir animaciones + micro-interactions  · agent: **Opus 4.7**

- [ ] **Step 1:** Skeleton loaders en todos los datafetching (no spinners).
- [ ] **Step 2:** Fade-in al cambio de mes (200ms).
- [ ] **Step 3:** Stagger en TendenciaChart al primer mount (60ms por serie).
- [ ] **Step 4:** Hover states en cards: leve `translateY(-2px)` + border-color change.
- [ ] **Step 5:** Respeta `prefers-reduced-motion`.
- [ ] **Step 6:** commit + push.

### T4.5 — Copy + formato es-MX  · agent: **Sonnet 4.6**

- [ ] **Step 1:** Revisar TODO copy en español MX. Sin "vos", sin "vale" europeo. Consistencia "tú/tu".
- [ ] **Step 2:** Cifras con `Intl.NumberFormat('es-MX', {style:'currency', currency:'MXN'})`.
- [ ] **Step 3:** Fechas con `Intl.DateTimeFormat('es-MX', {dateStyle:'long'})`.
- [ ] **Step 4:** commit + push.

### T4.6 — Fixes bugs reportados  · agent: **Opus 4.7**

- [ ] Bucket de tasks dinámicas según hallazgos de T4.3 y T4.4. Cada bug = 1 task hijo con fix + test de regresión.

### 🔍 AUDITORÍA F4 ADVERSARIAL  · agent: **Opus 4.7 adversarial**

- [ ] **Step 1:** Re-validar visualmente las 3 vistas principales.
- [ ] **Step 2:** Comparar números DB vs xlsx 2026 que Elena tiene (al centavo).
- [ ] **Step 3:** Probar flujo Luna otra vez con un mes ya cargado: dedup debe rechazar con 409.
- [ ] **Step 4:** Reporte `reports/F4-audit-<fecha>.md`.

---

# FASE 5 — Pre-junta (1 día)

**Tabla de paralelización F5:**

| Task | Agent | Depende de | Paralelizable con |
|------|-------|------------|-------------------|
| T5.1 Backup cron + retention | Sonnet | F4 | T5.2, T5.3 |
| T5.2 Refresh MV cron | Sonnet | F4 | T5.1, T5.3 |
| T5.3 Doc Elena (1 página) | Sonnet | F4 | T5.1, T5.2 |
| T5.4 Ensayo completo | operativo | T5.1, T5.2, T5.3 | — |
| T5.5 Smoke test celular+laptop | operativo | T5.4 | — |
| 🔍 F5 QUÍNTUPLE | **4×Opus adversarial + 1 sintetizador** | T5.5 | — |

### T5.1 — Backup cron + retention  · agent: **Sonnet 4.6**

- [ ] **Step 1:** Crontab del host lunita con el script de SPEC §8.3. Test manual primero.
- [ ] **Step 2:** Restore drill: bajar la DB, restaurar el último backup, verificar que la web sigue funcionando.
- [ ] **Step 3:** Documentar el restore drill en `docs/RUNBOOK.md`.

### T5.2 — Refresh MV cron  · agent: **Sonnet 4.6**

- [ ] **Step 1:** Crontab del SPEC §8.5.
- [ ] **Step 2:** Verificar que `mv_tendencia_anual` se refresca limpio (CONCURRENTLY no bloquea reads).

### T5.3 — Documentación Elena (1 página)  · agent: **Sonnet 4.6**

**Files:** Create `docs/MANUAL_ELENA.md`.

- [ ] **Step 1:** 1 página en español MX claro. Secciones:
  - Cómo entrar (URL + credenciales)
  - Cómo navegar al mes que necesitas
  - Qué hacer si un dato está mal (mandar mensaje a Luna)
  - Cómo cerrar un mes
  - A quién preguntar si algo no funciona (Claudio vía Fer)
- [ ] **Step 2:** Imprimir-friendly en PDF.

### T5.4-T5.5 — Operativo

- [ ] **T5.4:** Claudio + Elena hacen ensayo: login, navegar 2025 + 2026 cargado, abrir comparativa, exportar PDF, validar que se ve impecable.
- [ ] **T5.5:** Elena desde su celular + Óscar desde su laptop (con preview): logueo + dashboard + comparativa. Sin glitches visuales.

### 🔍 AUDITORÍA QUÍNTUPLE PRE-JUNTA  · agents: **4× Opus 4.7 adversarial + 1× sintetizador Opus 4.7**

Aplica regla [[feedback_auditoria_quintuple_milestones]]. 4 auditores paralelos con foco disjunto + 1 sintetizador. Disparados en paralelo en un solo turno.

**Auditor 1 — General/Funcional:**
- Smoke test E2E completo. Cargar 2025 + 2026 disponibles. Validar shape de TODOS los endpoints. Reportar críticos vs nice-to-have.

**Auditor 2 — Backend/Datos:**
- Cuadre matemático mes a mes. Foreign keys. Cascades. Constraints. Performance de queries hot path con `EXPLAIN ANALYZE`.

**Auditor 3 — Frontend/UX:**
- Cumplimiento DESIGN.md v2. Contrast. Mobile. Performance Lighthouse. Bundle. Accessibility con axe.

**Auditor 4 — Security:**
- Auth bypass attempts. JWT manipulation. SQL injection. XSS. Service token rotation works. Rate limit funciona. TLS valid.

**Sintetizador:**
- Lee los 4 reportes. Deduplica hallazgos. Prioriza por severidad. Produce 1 reporte final `reports/F5-quintuple-audit-<fecha>.md` con:
  - 🔴 Critical (bloqueantes para junta): lista numerada con fix-plan.
  - 🟠 High (deseables antes de junta): si tiempo permite.
  - 🟡 Medium/Low: post-junta backlog.
- Si hay critical, dispatch sub-tasks de fix y re-auditar antes del 4 jun.

---

# JUNTA — 5 jun 2026

**Día del evento.** Claudio en standby por Telegram para cualquier issue de último minuto. Backup completo pre-junta en `/srv/backups/sicc/pre-junta-2026-06-05.sql.gz`.

---

## Self-review check

Revisé el plan contra el SPEC y PRD:

- ✅ Auth (login + JWT cookie + service token + roles): T1.3
- ✅ CRUD meses (ingesta + lectura + cierre): T1.5, T1.8, T1.9
- ✅ Validador 10 reglas: T1.4
- ✅ Tendencia + MV: T1.6
- ✅ Catálogo actores + pre-seed Legacy: T1.7, T2.1
- ✅ Migración 2025 + reporte validación: T2.2, T2.3
- ✅ Skill + CLI con vision: T2.4, T2.5, T2.6, T2.7
- ✅ UI dashboard + comparativa + admin: T3.4-T3.10
- ✅ DESIGN.md v2 aplicado: T3.1, T3.3 + todos los componentes
- ✅ Mobile + a11y: T3.12
- ✅ PDF export: T3.9
- ✅ Backup + MV refresh + RUNBOOK: T5.1, T5.2, T5.3
- ✅ Audits adversariales cada fase + quíntuple pre-junta

Sin gaps. Sin placeholders en steps que tienen código. Convenciones globales fijadas.

---

## Notas para el orquestador (yo, Claudio)

- **Despacho de subagentes**: cada task se delega a un subagente en su propia worktree (regla [[feedback_pytest_concurrencia_db]] para pytest). Dispatch en paralelo cuando la tabla de paralelización lo permite.
- **Visibility checks**: SIEMPRE después de commit en sandbox (regla [[feedback_agente_sandbox_visibility]]).
- **Branch + push automático** al pasar task a review (regla [[feedback_push_antes_de_review]]).
- **Reporte a Fer por Telegram** al cerrar cada fase y al pasar auditoría. Nunca al cerrar tasks individuales (ruido innecesario; Fer dijo autonomía).
- **Bitácora `PROGRESO.md`** actualizada al cerrar cada fase + al pasar audit.
- **ADRs `docs/DECISIONES.md`**: cualquier decisión técnica que se aparte del SPEC va aquí antes de implementarla.
- **Calibración de tiempo**: mi percepción va 25-40x más rápida que el reloj real (regla [[feedback_calibracion_estimaciones_tiempo]]). No prometo deadlines absolutos, solo orden de fases.
