# Diccionario de Variables — NHANES UI Women

Dataset: `nhanes_ui_women_descriptivo`
Fuente: CDC NHANES, ciclos 2017–marzo 2020 y 2021–2023
Muestra: 9,074 mujeres adultas (edad ≥ 20 años)

---

## Variables de Identificación

| Variable | Tipo | Descripción |
|---|---|---|
| `SEQN` | int | ID único del participante (CDC) |
| `cycle` | str | Ciclo NHANES (2017-2020 / 2021-2023) |
| `WTMEC2YR` | float | Peso estadístico de muestra compleja — permite generalización poblacional |

## Variables Demográficas

| Variable | Tipo | Descripción | Valores |
|---|---|---|---|
| `RIDAGEYR` | int | Edad en años cumplidos | ≥ 20 |
| `RIDRETH3` | cat | Etnia/raza | 1=Mexican American, 2=Other Hispanic, 3=Non-Hispanic White, 4=Non-Hispanic Black, 6=Non-Hispanic Asian, 7=Other |
| `DMDBORN4` | cat | País de nacimiento | 1=EE.UU., 2=Otro |

## Variable Antropométrica

| Variable | Tipo | Descripción |
|---|---|---|
| `BMXBMI` | float | Índice de Masa Corporal (kg/m²) |

## Condiciones Clínicas

| Variable | Tipo | Descripción | Valores |
|---|---|---|---|
| `DIQ010` | cat | Diabetes diagnosticada por médico | 1=Sí, 2=No, 3=Borderline |
| `BPQ020` | cat | Hipertensión diagnosticada por médico | 1=Sí, 2=No |
| `BPQ040A` | cat | Toma medicación para hipertensión | 1=Sí, 2=No |

## Estilo de Vida

| Variable | Tipo | Descripción | Valores |
|---|---|---|---|
| `SMQ020` | cat | Ha fumado al menos 100 cigarrillos en su vida | 1=Sí, 2=No |
| `PAQ605` | cat | Actividad física vigorosa en el trabajo | 1=Sí, 2=No |

## Socioeconómica

| Variable | Tipo | Descripción |
|---|---|---|
| `INDFMMPC` | cat | Nivel de pobreza familiar (ratio income/poverty) categorizado |

## Síntomas de Incontinencia Urinaria

| Variable | Tipo | Descripción | Valores |
|---|---|---|---|
| `KIQ005` | cat | ¿Ha perdido orina en las últimas 12 meses? | 1=Sí, 2=No |
| `KIQ010` | cat | Frecuencia de pérdida de orina | 1=Raramente, 2=Algunos días, 3=La mayoría de los días, 4=Todos los días |
| `KIQ042` | cat | Cantidad de orina perdida normalmente | 1=Gotas, 2=Chorro pequeño, 3=Más |
| `KIQ044` | cat | Pérdida de orina al toser, reír, estornudar o hacer esfuerzo físico | 1=Sí, 2=No |
| `KIQ046` | cat | Pérdida de orina con deseo urgente de orinar antes de llegar al baño | 1=Sí, 2=No |

## Impacto Subjetivo

| Variable | Tipo | Descripción | Valores |
|---|---|---|---|
| `KIQ480` | cat | Molestia percibida por la pérdida de orina | 0=Nada, 1=Poca, 2=Moderada, 3=Mucha |
| `KIQ052` | cat | Impacto en actividades diarias | 0=Nada, 1=Poca, 2=Moderada, 3=Mucha |

---

## Variable Objetivo (Target)

| Variable | Tipo | Descripción |
|---|---|---|
| `UI_class` | cat | Clase de incontinencia urinaria (construida en ETL) |

### Valores de UI_class

| Valor | N | % | Criterio de asignación |
|---|---|---|---|
| `ninguna` | 4,857 | 53.5% | KIQ005 = No |
| `mixta` | 1,642 | 18.1% | KIQ044=Sí y KIQ046=Sí |
| `esfuerzo` | 1,586 | 17.5% | KIQ044=Sí y KIQ046=No |
| `urgencia` | 932 | 10.3% | KIQ046=Sí y KIQ044=No (incluye los 57 casos de clase 'otro') |

> La clase `otro` (57 casos, 0.6%) fue fusionada con `urgencia` por criterio clínico en la fase de ETL.

---

*Última actualización: Marzo 2026*
