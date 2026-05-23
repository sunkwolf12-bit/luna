# PRODUCT REQUIREMENT DOCUMENT (PRD)
## Sistema de Inteligencia y Control de Cobranza (SICC) — Proteg-rt Mutualidad

**Fecha de Creación:** 2026-05-22  
**Autor:** Luna 🌙  
**Estado:** PROPUESTA / DETALLE MAESTRO  
**Objetivo:** Transicionar el control de cobranza quincenal/mensual e indicadores de juntas del desorden en Excel a un sistema web dinámico, confiable, persistido en base de datos PostgreSQL, accesible en VPS y con la robustez requerida para auditorías.

---

## 1. Introducción y Objetivos de Negocio
Elena Rivas (Gerente de Cobranza de Proteg-rt Mutualidad) requiere presentar mensualmente informes ejecutivos de KPI's (Total Cobranza, Recuperada, Efectiva, Cancelaciones, Vencida, Adelantada, Proyecciones) y los respectivos rankings "Top 5" por desempeño. 

El modelo operativo actual basado en hojas de Excel dispersas y parches de fórmulas propicia errores por cálculo no transparente, rotura de referencias y pérdida de control sobre los cierres históricos.

El **SICC** tiene como fin:
1. **Centralizar**: Almacenar toda la información operativa del negocio en base de datos segura y auditable.
2. **Consolidar**: Integrar en un solo motor la cobranza histórica mes con mes (Enero-Diciembre).
3. **Dashboard Automatizado**: Generar vistas interactivas tipo dashboard que reaccionen sin latencia y muestren gráficas de tendencias exactas.
4. **Desacoplar la Presentación de los Datos**: Mantener los números duros protegidos en el backend (PostgreSQL) y el diseño gráfico en el navegador.

---

## 2. Arquitectura Tecnológica Propuesta
Se propone una pila robusta, ligera, sin costes de licenciamiento y con alto rendimiento en el VPS actual:
- **Base de Datos (Capa de Persistencia)**: PostgreSQL 16+.
- **Backend (API de Servicios)**: Python (FastAPI / SQLAlchemy) — por su extrema rapidez, tipado estático integrado, y facilidad para exportaciones a formato físico si Óscar o Dirección lo solicitan.
- **Frontend (Interfaz de Usuario)**: HTML5 interactivo, CSS3 moderno (Tailwind CSS) y JavaScript Vanilla (sin frameworks pesados tipo React para evitar sobrecarga del navegador de la oficina).

---

## 3. Modelo de Datos de PostgreSQL (Detallado)

### 3.1. Tabla: `conceptos_cobranza`
Almacena los montos globales agrupados por mes y por concepto.

```sql
CREATE TABLE conceptos_cobranza (
    id SERIAL PRIMARY KEY,
    mes VARCHAR(20) NOT NULL, -- 'ENERO', 'FEBRERO', etc.
    anio INT DEFAULT 2026,
    cobranza_corriente NUMERIC(15, 2) NOT NULL DEFAULT 0.00,
    cancelaciones NUMERIC(15, 2) NOT NULL DEFAULT 0.00,
    cobranza_vencida NUMERIC(15, 2) NOT NULL DEFAULT 0.00,
    cobranza_efectiva NUMERIC(15, 2) NOT NULL DEFAULT 0.00,
    cobranza_recuperada NUMERIC(15, 2) NOT NULL DEFAULT 0.00,
    cobranza_total_general NUMERIC(15, 2) NOT NULL DEFAULT 0.00, -- Calculado: efectiva + recuperada
    cobranza_adelantada NUMERIC(15, 2) NOT NULL DEFAULT 0.00,
    proyeccion_siguiente_mes NUMERIC(15, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_mes_anio UNIQUE (mes, anio)
);
```

### 3.2. Tabla: `top5_cobranza`
Almacena los registros detallados de los rankings.

```sql
CREATE TYPE tipo_seccion_top5 AS ENUM ('CORRIENTE', 'CANCEL', 'VENCIDA', 'EFECTIVA', 'RECUPERADA', 'TOTAL_GRAL');

CREATE TABLE top5_cobranza (
    id SERIAL PRIMARY KEY,
    mes VARCHAR(20) NOT NULL,
    anio INT DEFAULT 2026,
    seccion tipo_seccion_top5 NOT NULL,
    lugar INT NOT NULL, -- 1, 2, 3, 4, 5
    vendedor_cobrador VARCHAR(100) NOT NULL, -- Nombre o Código (V1, JORGE, EDGAR, etc.)
    monto NUMERIC(15, 2) NOT NULL,
    porcentaje_participacion NUMERIC(5, 4), -- Guardado como decimal (ej. 0.2215 para 22.15%)
    CONSTRAINT unique_lugar_seccion_mes UNIQUE (mes, anio, seccion, lugar)
);
```

---

## 4. Requerimientos de Pantallas e Interfaz de Usuario (UI/UX)

### 4.1. Dashboard Principal
- **Selector de Mes (Dropdown)**: Ubicado en la barra superior. Al cambiar el mes, las tarjetas y tablas deben actualizarse de forma instantánea usando AJAX/Fetch a la API.
- **Sección de Tarjetas de Resumen (Métricas Clave)**:
  - **Tarjeta 1**: Cobranza Total General (Efectiva + Recuperada)
  - **Tarjeta 2**: Cobranza Recuperada (Monto y % de participación)
  - **Tarjeta 3**: Cobranza Efectiva (Monto y % de participación)
  - **Tarjeta 4**: Cancelaciones (Monto y % de participación)
  - **Tarjeta 5**: Cobranza Vencida (Monto y % de participación)
  - **Tarjeta 6**: Cobranza Adelantada
- **Sección del Concentrado General (Tabla)**: 
  - Columnas: `Concepto | Total ($) | % Participación | Estatus`
  - Debe mostrar las sumas y las variaciones porcentuales de forma visual.
- **Sección de Rankings (Top 5)**:
  - 4 tarjetas o tablas una al lado de la otra (estructura responsiva):
    1. **Corriente** (Vendedores que más cobranza generada tienen)
    2. **Cancelaciones** (Quién tiene más pólizas canceladas)
    3. **Vencida** (Vendedores/Cobradores con más atraso)
    4. **Efectiva** (Quién recolectó más dinero real)
  - Cada fila debe incluir: `Lugar | Vendedor/Cobrador | Monto ($)`
- **Sección de Tendencias (Gráfica de Líneas)**:
  - Gráfica interactiva anual que cargue los datos de todos los meses de la base de datos para mostrar la evolución del año completo.

---

## 5. Reglas de Negocio a Implementar
- **Cálculo de Porcentajes**: 
  - La base (100%) para la distribución mensual es el **Total General de Cobranza (Efectiva + Recuperada)**.
  - Los % de Efectiva, Recuperada, Vencida y Cancelaciones se calculan sobre esa base.
- **Endosos de $125**: Quedan explícitamente **excluidos** de estas tablas generales, ya que se controlan mediante un reporte de pago fijo mensual de $50 pesos por póliza entregada.
- **Exclusión de Coberturas Amplias**: El sistema no debe acumular montos asociados a pólizas "Amplias" en el reporte mensual de Elena.

---

## 6. Fases de Desarrollo Planificadas

| Fase | Título | Entregable | Tiempo Estimado |
|---|---|---|---|
| **Fase 1** | Solución A (Inmediata) | Archivo HTML interactivo local e independiente con datos ENERO-ABRIL listos para la junta. | **Inmediato (Hoy)** |
| **Fase 2** | Backend & DB Setup | Scripts de PostgreSQL, configuración de FastAPI y migración de datos históricos. | **2-3 días** |
| **Fase 3** | Frontend API Link | Conexión del diseño HTML dinámico a los endpoints del servidor web VPS. | **2 días** |
| **Fase 4** | Seguridad y Cierre | Auditoría de accesos privados, HTTPS, copias de respaldo y entrega final. | **1 día** |

---

## 7. Preguntas y Decisiones Pendientes para Elena
Para que esto quede perfecto 1000%, confírmame lo siguiente:
1. **¿Qué gestor de Base de Datos prefieres que instalemos en tu VPS?** Yo te recomiendo **PostgreSQL** por su robustez, pero si Fer ya tiene MySQL listo por su lado de SIGA, podemos usar MySQL sin problemas para alinearnos.
2. **¿Quién tendrá acceso a la plataforma web?** ¿Solo tú desde tu navegador privado en la oficina, o quieres que Óscar y otros vendedores tengan usuarios específicos (con permisos limitados de solo lectura)?
