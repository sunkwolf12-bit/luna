# Catalogo de actores — snapshot SICC

> **SNAPSHOT** del 2026-05-23 contra la tabla `actores` de la DB SICC en
> lunita (15 vendedores activos + 9 cobradores puros / entidades virtuales).
> La fuente real es el backend; preferir `sicc actores list` (T2.6) sobre
> este archivo cuando haya conectividad. Este snapshot ayuda en caso de
> perdida de red para preparar el JSON candidato.

## Vendedores activos (codigo `V\d+`)

| Codigo | Nombre corto | Nombre completo |
|---|---|---|
| V1 | Coco | Maria del Socorro Villarreal Villarreal |
| V4 | Oscar Lopez | Oscar Lopez Villarreal |
| V6 | Gaby | Gabriela Edith Lopez Villarreal |
| V14 | Carmen | Carmen Falcon Tizcareno |
| V16 | Antonio Esparza | Lic. Antonio Esparza |
| V23 | Fernando Lopez | Fernando Lopez Villarreal |
| V27 | Santiago | Santiago Haro Ruvalcaba |
| V38 | Laura | Laura Liliana Alvarado Perez |
| V39 | Jose Asuncion | Jose Asuncion Cuevas Huerta |
| V55 | Giovanni | Giovanni Francisco Limon Orozco |
| V56 | Saul Manriquez | Saul Manriquez Valenzuela |
| V60 | Jose Luis Torres | Jose Luis Torres Ruiz |
| V84 | Leonel | Leonel Anzaldo Fernandez |
| V113 | Enrique Pulido | Enrique Pulido Naranjo |
| V114 | Jesus Perez | Jesus Perez Olivares |

## Cobradores puros (sin codigo, nombre canonico)

| Nombre canonico | Nombre completo |
|---|---|
| EDGAR | Edgar Eduardo Gonzalez Perez |
| EDUARDO | Eduardo Gonzalez |
| Erika | Erika Viridiana Vital Pardo |
| FRANCISCO | Francisco Javier Murguia |
| Fidel | Fidel Rangel Gaytan |
| JORGE | Jorge Alberto Jauregui Ruiz |
| Lizeth | Lizeth Hernandez Alvarado |

## Entidades virtuales (tambien `cobrador_puro` en DB)

| Nombre canonico | Significado |
|---|---|
| OFICINA | Pagos cobrados en ubicacion fisica Oficina. |
| TRANSFER. / DEPTOS. | Canal de pago consolidado: transferencia o deposito bancario. Receptor por defecto de la regla de consolidacion bancaria. |

## Reglas de uso

1. **V5 NO se usa.** Codigo historico erroneo (ADR-004). Si una imagen
   trae `V5`, asumir typo (probable `V55` o `V56`) y pedir confirmacion
   a Elena.
2. Vendedores tienen `codigo` (`V\d+`); cobradores puros NO. Pasar
   `actor_codigo` para vendedores y `actor_nombre` para cobradores puros.
3. Si el Top5 trae un actor que no esta en esta lista, NO inventar.
   Preguntar a Elena: alta nueva, typo o lo dejamos como esta.
4. Snapshot puede quedar desactualizado entre cargas masivas. Si Elena
   reporta "fulano debe estar y no aparece", correr
   `sicc actores list --activo` (T2.6) para refrescar.

## Vendedores inactivos / historicos

Hay 72 vendedores historicos inactivos y 4 cobradores puros inactivos en
la DB (seed F1). No deben aparecer en Top5 nuevos; si aparecen,
investigar antes de cargar (probable reactivacion silenciosa o seed
incompleto).
