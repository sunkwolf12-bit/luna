---
name: db-consultas
description: "Consultas de solo lectura a datos de Proteg-rt via API REST. Busqueda de clientes, polizas, pagos, renovaciones, vendedores, siniestros, asignacion de cobranza. SOLO LECTURA."
user-invocable: true
---

# DB Consultas - Datos de Proteg-rt (SOLO LECTURA)

Skill para consultar informacion de clientes, polizas, pagos, renovaciones, vendedores, siniestros y asignacion de cobranza en Proteg-rt **a traves de la API REST**.

---

## REGLA ABSOLUTA: SOLO LECTURA

> **Esta skill es exclusivamente de consulta.** No hay endpoints de escritura. No los habra.
> Los datos provienen de una replica sincronizada periodicamente desde produccion.

---

## API REST - Proteg-rt Consultas API

**URL Base:** `http://localhost:8000`
**Autenticacion:** Header `X-API-Key`
**API Key de Oscar:** `1fxWFNyQOwOY9jeKTBvmhM-s4vLHtcx6HG0rs_YkbyI`
**Desplegada en:** VPS de Luna (localhost) - servicio systemd `legacy-api`
**Repo:** `sunkwolf/legacy-api` (GitHub)
**Docs interactivos:** `http://localhost:8000/docs` (Swagger UI)

### API Keys y Roles

| Usuario | Rol | Acceso |
|---|---|---|
| Fernando | `admin` | Todo sin restriccion |
| Oscar | `admin` | Todo sin restriccion |
| Gaby | `gerente_ventas` | Todo de sus clientes, resumen limitado de otros |
| (futuro) | `vendedor` | Solo sus propios datos |

### Logica de acceso por rol: dueno vs ajeno

El rol `gerente_ventas` tiene acceso diferenciado segun si el cliente/poliza pertenece a su cartera:

**Cliente propio (id_vendedor = su ID):**
- Pagos completos: montos, recibos, cobrador, metodo de pago, total cobrado
- Asignacion de cobranza: tarjeta completa + historial de movimientos
- Siniestros: detalle completo (descripcion, ubicacion, proveedor grua)

**Cliente de otro vendedor:**
- Pagos: solo `numero_pago`, `fecha_limite`, `status` + campo `al_corriente` (sin montos, sin recibos, sin cobrador)
- Asignacion: solo cobrador actual + status de tarjeta (sin historial de movimientos)
- Siniestros: solo conteo, IDs, fechas y status (sin descripcion, ubicacion ni detalle de gruas)

### Como consumir la API

Para hacer consultas, usar curl con el header X-API-Key:

```bash
curl -s -H "X-API-Key: 1fxWFNyQOwOY9jeKTBvmhM-s4vLHtcx6HG0rs_YkbyI" "http://localhost:8000/api/v1/clientes/buscar?q=Lopez"
```

### Endpoints disponibles

| Metodo | Endpoint | Descripcion |
|---|---|---|
| GET | `/api/v1/sync` | Fecha de ultima sincronizacion de la BD |
| GET | `/api/v1/clientes/buscar?q=Lopez&limit=20` | Buscar clientes por nombre, apellido, telefono o correo |
| GET | `/api/v1/clientes/{id_cliente}/polizas` | Todas las polizas de un cliente |
| GET | `/api/v1/polizas/{folio}` | Detalle completo de una poliza (cliente + vehiculo + vendedor) |
| GET | `/api/v1/polizas/{folio}/pagos` | Situacion de pagos con resumen (filtrado por rol) |
| GET | `/api/v1/polizas/{folio}/siniestros` | Siniestros y servicios de grua (filtrado por rol) |
| GET | `/api/v1/polizas/{folio}/asignacion` | Cobrador asignado + tarjeta + historial movimientos (filtrado por rol) |
| GET | `/api/v1/polizas/buscar/placas?q=ABC123` | Buscar polizas por placas |
| GET | `/api/v1/polizas/buscar/serie?q=3N1CB` | Buscar polizas por numero de serie |
| GET | `/api/v1/reportes/por-vencer?dias=30` | Polizas por vencer (con estado RENOVADA / SIN RENOVAR) |
| GET | `/api/v1/reportes/morosos?limit=50` | Polizas con pagos vencidos |
| GET | `/api/v1/reportes/vendedores` | Resumen de todos los vendedores (solo gerente/admin) |
| GET | `/api/v1/reportes/ventas?mes=3&anio=2026` | Ventas por periodo |
| GET | `/api/v1/reportes/renovables?dias=90` | Polizas expiradas sin renovacion |
| GET | `/api/v1/reportes/multipoliza?minimo=3` | Clientes con multiples polizas activas |
| GET | `/api/v1/vendedor/{id_empleado}` | Detalle y polizas de un vendedor |

### Campos renombrados para claridad

La API devuelve nombres de campo corregidos respecto a la BD Legacy:
- `tipo` -> `modelo_comercial` (nombre comercial del vehiculo: "TSURU", "SPARK")
- `modelo` -> `anio_vehiculo` (ano del vehiculo: "2003", "2015")
- `tipo_vehiculo` -> `clase_vehiculo` (categoria: AUTOMOVIL, PICKUP, MOTOCICLETA)

### Pendientes de implementar en la API

- [ ] **Endpoint de contrato preparatorio** - Servir imagen del contrato desde protegrt-files. Filtrado por rol.

---

## Que puedo preguntarte? - Guia para el usuario

Cuando el usuario no sepa que buscar o como pedirlo, mostrarle esta lista como referencia.

### Busquedas de clientes
- "Busca al cliente Juan Perez"
- "Tenemos un cliente con telefono 3312345678?"
- "Quien tiene el correo juanperez@gmail.com?"

### Informacion de polizas
- "Que polizas tiene el cliente Maria Lopez?"
- "Dame los datos completos del folio 22848"
- "Que carro tiene asegurado el folio 20148?"
- "Busca las polizas con placas JKG8288"
- "Tenemos alguna poliza con serie 3N1CB51D?"

### Pagos y cobranza
- "Como va de pagos el folio 22848?"
- "Cuanto debe el cliente Godines?"
- "Ya pago su mensualidad el folio 20148?"
- "Quien tiene asignada la cuenta del folio 22848?"
- "Dame el historial de la tarjeta del folio 22848"

### Renovaciones
- "Ya se renovo la poliza 20148?"
- "Que polizas se vencen esta semana?"
- "Cuales de mis polizas que vencen en 30 dias ya fueron renovadas?"
- "Dame las polizas vencidas que no se renovaron"

### Morosos y riesgos
- "Que polizas estan morosas?"
- "Quienes deben mas dinero?"
- "Este cliente tiene problemas de pago o fraude?"

### Vendedores y ventas
- "Cuantas polizas activas tiene cada vendedor?"
- "Cuantas ventas hubo en marzo?"
- "Quien vendio mas este mes?"
- "Dame el detalle de las polizas de Santiago"

### Siniestros
- "El folio 20148 ha tenido siniestros?"
- "Cuantas gruas le quedan a esta poliza?"

### Clientes especiales
- "Que clientes tienen mas de 3 polizas activas?"

> **Nota:** Toda la informacion proviene de una replica de la base de datos que se sincroniza periodicamente.
> En cada respuesta se muestra la fecha de la ultima sincronizacion para que sepas que tan recientes son los datos.

---

## Consultas frecuentes y como resolverlas

### "Ya se renovo la poliza X?"
Endpoint: `/api/v1/reportes/por-vencer?dias=30` - incluye campo de estado de renovacion.

### "Cuanto debe el cliente X?"
Buscar al cliente -> listar polizas -> para cada una, consultar `/pagos` -> el resumen incluye `vencidos` y `total_cobrado`.

### "Quien es el vendedor que mas vende?"
Endpoint: `/api/v1/reportes/ventas?mes=3&anio=2026` o `/api/v1/reportes/vendedores` para acumulado.

### "Dame los clientes de [vendedor] que estan por vencer"
Endpoint: `/api/v1/vendedor/{id_empleado}` muestra sus polizas ordenadas por vencimiento.

### "Este cliente es confiable para AMPLIA SELECT?"
Consultar el detalle de la poliza. Los campos `has_payment_issues` y `has_fraud_observation` deben ser 0.

### "Cuantas gruas le quedan a esta poliza?"
Campo `servicios_grua_disponibles` en el detalle de la poliza.

### "Historial de un vehiculo?"
Buscar por placas o serie. La cadena de renovaciones muestra todas las polizas del vehiculo.

### "Quien tiene la tarjeta de cobranza del folio X?"
Endpoint: `/api/v1/polizas/{folio}/asignacion` - muestra cobrador actual + historial de movimientos.

---

## Logica de Negocio - Lo que necesitas saber

### La empresa

**Mutualidad Proteg-rt** ("Protegerte") - seguros vehiculares en Tonala, Jalisco. Negocio familiar:
- **Oscar Lopez** - Director general
- **Gabriela (Gaby)** - Gerente de ventas (id_empleado: 6)
- **Fernando (Fer)** - Encargado de sistemas (id_empleado: 23)
- **Elena** - Gerente de cobranza

### Status de polizas

| Status | Significado |
|---|---|
| **Activa** | Vigente, al corriente en pagos |
| **Morosa** | Vigente pero con pagos atrasados |
| **Expirada** | Vencio su periodo de vigencia |
| **Cancelada** | Cancelada antes de vencer |
| **Pendiente** | Creada pero no completamente procesada |
| **Previgencia** | Renovacion que aun no entra en vigor |

### Renovaciones
- Se crea una nueva poliza con `renewal_folio` apuntando al folio anterior.
- **Previgencia** = renovacion capturada que arranca cuando vence la anterior.

### Pagos
- Cada poliza tiene N pagos segun `forma_pago` (mensual, trimestral, semestral, contado).
- Un pago es **vencido** si `fecha_limite < hoy` y status no es PAGADO/APLICADO/CANCELADO.

### Coberturas (menor a mayor proteccion)
1. RC BASICA -> RC PLUS -> RC PRO -> RC INTERMEDIA -> RC PREMIUM
2. RC TON 3 A 5 / RC TON 6 A 10 (camiones por tonelaje)
3. AMPLIA -> AMPLIA SELECT (requiere elegibilidad) -> PLATINO -> PLATINO +
4. PLATAFORMA (Uber/DiDi)

### Elegibilidad AMPLIA SELECT
- `has_payment_issues` = 0 (sin problemas de pago)
- `has_fraud_observation` = 0 (sin fraude)

### Campos de BD que confunden

| Columna en BD | Lo que REALMENTE es | Ejemplo |
|---|---|---|
| `tipo` | Modelo comercial del vehiculo | "TSURU", "SPARK" |
| `modelo` | Ano del vehiculo | "2003", "2015" |
| `tipo_vehiculo` | Clase/categoria | "PICKUP", "AUTOMOVIL" |
| `entrega` | Quien entrega la poliza fisica | "Vendedor", "Cobrador" |

> La API ya renombra estos campos para evitar confusion.

---

## Restricciones por Rol

### Admin (Fer, Oscar)
- Sin restriccion. Todo visible.

### Gerente ventas (Gaby, id_empleado: 6)
- Todo de sus clientes. Resumen limitado de otros (ver seccion "dueno vs ajeno").
- Acceso a reportes globales de vendedores y ventas.

### Vendedor (futuro)
- Solo sus propios clientes y polizas (`id_vendedor` = su ID).
- Sin acceso a resumenes globales.
- **Contratos:** Solo de polizas a <=30 dias de vencer - protege cartera de la empresa.

### Cobradores (futuro)
- Solo pagos de polizas asignadas a ellos.

---

## Recursos

| Recurso | Ubicacion | Descripcion |
|---|---|---|
| SKILL.md | `skills/db-consultas/SKILL.md` | Este archivo |
| API REST | `sunkwolf/legacy-api` (GitHub) | Microservicio FastAPI en VPS Luna |
| Swagger UI | `http://localhost:8000/docs` | Documentacion interactiva |
| Script local | `scripts/buscar_cliente.py` | Respaldo: consultas directas a MySQL si la API cae |

---

## Notas importantes

1. **Los datos tienen un delay** respecto a produccion. La API incluye la fecha de sync en cada respuesta.
2. **`folio` es el identificador principal** - es lo que todos usan para referirse a una poliza.
3. **La API es temporal** - se apaga cuando Legacy migre al Sistema Nuevo (PostgreSQL).
4. **Script local como respaldo:** Si la API no responde, `scripts/buscar_cliente.py` conecta directo a Hostinger.
