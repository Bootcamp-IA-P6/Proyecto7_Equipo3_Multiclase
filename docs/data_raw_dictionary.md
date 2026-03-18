# Diccionario de Variables — NHANES UI Women

**Dataset:** `nhanes_ui_women.csv`  
**Filas:** 9.074 | **Columnas:** 27  
**Fuente:** NHANES 2017–March 2020 + 2021–2023  
**Población:** Mujeres ≥20 años con datos de incontinencia urinaria

> Cada variable se presenta con su **nombre descriptivo** (usado en el dataset de trabajo) y su **código CDC original** (NHANES). Los valores y porcentajes de missings se obtienen directamente de los datos.

---

## Variables de Identificación

| Variable | Código CDC | Tipo | Descripción | Valores | Missings |
|---|---|---|---|---|---|
| `id_participante` | `SEQN` | float64 | ID único del participante en NHANES | Numérico | 0% |
| `ciclo_nhanes` | `CYCLE` | str | Ciclo de recolección de datos | `2017-March2020`, `2021-2023` | 0% |
| `peso_encuesta` | `WTMEC2YR` | float64 | Peso estadístico de muestra compleja. Permite extrapolar resultados a la población general de EE.UU. | Continuo (>0) | 52.4% |

---

## Variables Demográficas

| Variable | Código CDC | Tipo | Descripción | Valores | Missings |
|---|---|---|---|---|---|
| `edad_anios` | `RIDAGEYR` | float64 | Edad en años cumplidos en el momento de la entrevista | 20–80 (80+ agrupados en 80) | 0% |
| `etnia` | `RIDRETH1` | float64 | Grupo étnico/racial de la participante | 1=Mexican American, 2=Other Hispanic, 3=Non-Hispanic White, 4=Non-Hispanic Black, 5=Other | 0% |
| `pais_nacimiento` | `DMDBORN4` | float64 | País de nacimiento de la participante | 1=EE.UU., 2=Otro país | 0.1% |

**Códigos CDC de missings:**

| Código | Significado | Variable |
|---|---|---|
| 77 | Refused | `pais_nacimiento` |
| 99 | Don't know | `pais_nacimiento` |

---

## Variable Antropométrica

| Variable | Código CDC | Tipo | Descripción | Valores | Missings |
|---|---|---|---|---|---|
| `imc` | `BMXBMI` | float64 | Índice de Masa Corporal medido en la exploración física (kg/m²) | Continuo | 16.0% |

---

## Condiciones Clínicas

| Variable | Código CDC | Tipo | Descripción | Valores | Missings |
|---|---|---|---|---|---|
| `dx_hipertension` | `BPQ020` | float64 | ¿Le ha dicho algún médico que tiene hipertensión? | 1=Sí, 2=No | 0% |
| `medicacion_hta_cicloP` | `BPQ050A` | float64 | ¿Está tomando actualmente medicación recetada para la hipertensión? (ciclo 2017–2020) | 1=Sí, 2=No | 81.3% |
| `medicacion_hta_cicloL` | `BPQ150` | float64 | ¿Está tomando actualmente medicación recetada para la hipertensión? (ciclo 2021–2023) | 1=Sí, 2=No | 82.4% |
| `dx_diabetes` | `DIQ010` | float64 | ¿Le ha dicho algún médico que tiene diabetes? | 1=Sí, 2=No, 3=Borderline | 0% |
| `dx_cancer` | `MCQ220` | float64 | ¿Le ha dicho algún médico que tiene o ha tenido cáncer? | 1=Sí, 2=No | 0% |
| `dx_artritis` | `MCQ160A` | float64 | ¿Le ha dicho algún médico que tiene artritis? | 1=Sí, 2=No | 0% |

**Códigos CDC de missings:**

| Código | Significado | Variables |
|---|---|---|
| 7 | Refused | `dx_cancer` |
| 9 | Don't know | `dx_hipertension`, `medicacion_hta_cicloL`, `dx_diabetes`, `dx_artritis`, `dx_cancer` |

---

## Estilo de Vida

| Variable | Código CDC | Tipo | Descripción | Valores | Missings |
|---|---|---|---|---|---|
| `fumadora_alguna_vez` | `SMQ020` | float64 | ¿Ha fumado al menos 100 cigarrillos a lo largo de su vida? | 1=Sí, 2=No | 0.1% |
| `actividad_fisica_vigorosa` | `PAQ650` | float64 | ¿Realiza actividades físicas vigorosas durante su tiempo libre? | 1=Sí, 2=No | 47.6% |

**Códigos CDC de missings:**

| Código | Significado | Variable |
|---|---|---|
| 7 | Refused | `fumadora_alguna_vez` |
| 9 | Don't know | `fumadora_alguna_vez` |

---

## Socioeconómica

| Variable | Código CDC | Tipo | Descripción | Valores | Missings |
|---|---|---|---|---|---|
| `nivel_pobreza_familiar` | `INDFMMPC` | float64 | Nivel de pobreza familiar categorizado a partir del ratio ingreso/umbral de pobreza federal | 1=0–130%, 2=130–350%, 3=>350% | 10.0% |

**Códigos CDC de missings:**

| Código | Significado | Variable |
|---|---|---|
| 7 | Refused | `nivel_pobreza_familiar` |
| 9 | Don't know | `nivel_pobreza_familiar` |

---

## Síntomas de Incontinencia Urinaria

| Variable | Código CDC | Tipo | Descripción | Valores | Missings |
|---|---|---|---|---|---|
| `ui_frecuencia` | `KIQ005` | float64 | ¿Con qué frecuencia ha perdido orina involuntariamente en los últimos 12 meses? | 1=Nunca, 2=Menos de 1 vez al mes, 3=Unas pocas veces al mes, 4=Unas pocas veces a la semana, 5=Todos los días | 24.0% |
| `ui_cantidad` | `KIQ010` | float64 | ¿Qué cantidad de orina pierde habitualmente? | 1=Gotas, 2=Chorro pequeño, 3=Más | 60.9% |
| `ui_esfuerzo_presente` | `KIQ042` | float64 | ¿Pierde orina al toser, reír, estornudar o hacer esfuerzo físico? | 1=Sí, 2=No | 24.1% |
| `ui_esfuerzo_frecuencia` | `KIQ430` | float64 | ¿Con qué frecuencia pierde orina al esfuerzo? *(subpregunta condicional de `ui_esfuerzo_presente`)* | 1=Raramente, 2=Algunos días, 3=La mayoría de días, 4=Todos los días | 80.9% |
| `ui_urgencia_presente` | `KIQ044` | float64 | ¿Pierde orina con un deseo urgente de orinar antes de llegar al baño? | 1=Sí, 2=No | 24.1% |
| `ui_urgencia_frecuencia` | `KIQ450` | float64 | ¿Con qué frecuencia pierde orina con urgencia? *(subpregunta condicional de `ui_urgencia_presente`)* | 1=Raramente, 2=Algunos días, 3=La mayoría de días, 4=Todos los días | 85.1% |
| `ui_otro_tipo_presente` | `KIQ046` | float64 | ¿Pierde orina por algún otro motivo distinto al esfuerzo o la urgencia? | 1=Sí, 2=No | 55.3% |

**Códigos CDC de missings:**

| Código | Significado | Variables |
|---|---|---|
| 7 | Refused | `ui_frecuencia`, `ui_cantidad`, `ui_esfuerzo_presente`, `ui_esfuerzo_frecuencia`, `ui_urgencia_presente`, `ui_otro_tipo_presente` |
| 9 | Don't know | `ui_frecuencia`, `ui_cantidad`, `ui_esfuerzo_presente`, `ui_urgencia_presente`, `ui_urgencia_frecuencia`, `ui_otro_tipo_presente` |

---

## Impacto Subjetivo

| Variable | Código CDC | Tipo | Descripción | Valores | Missings |
|---|---|---|---|---|---|
| `ui_molestia_percibida` | `KIQ050` | float64 | ¿Cuánta molestia le causa la pérdida de orina en su vida diaria? | 1=Nada, 2=Poca, 3=Moderada, 4=Mucha, 5=Muchísima | 73.9% |
| `ui_impacto_actividades` | `KIQ052` | float64 | ¿En qué medida la pérdida de orina limita sus actividades cotidianas? | 1=Nada, 2=Poca, 3=Moderada, 4=Mucha, 5=Muchísima | 53.6% |

**Códigos CDC de missings:**

| Código | Significado | Variable |
|---|---|---|
| 7 | Refused | `ui_impacto_actividades` |
| 9 | Don't know | `ui_impacto_actividades` |

---

## Variables Objetivo (Target)

| Variable | Código CDC | Tipo | Descripción | Valores | Missings |
|---|---|---|---|---|---|
| `target_tiene_ui` | `UI_binary` | int64 | Incontinencia urinaria presente (construida en el proyecto) | 0=No, 1=Sí | 0% |
| `target_tipo_ui` | `UI_class` | str | Tipo de incontinencia urinaria (construida en el proyecto) | `none`, `stress`, `mixed`, `urge`, `other` | 0% |

### Distribución de `target_tipo_ui`

| Valor | N | % | Criterio de asignación |
|---|---|---|---|
| `none` | 4.857 | 53.5% | `ui_frecuencia` = 1 (nunca) |
| `mixed` | 1.642 | 18.1% | `ui_esfuerzo_presente`=Sí y `ui_urgencia_presente`=Sí |
| `stress` | 1.586 | 17.5% | `ui_esfuerzo_presente`=Sí y `ui_urgencia_presente`=No |
| `urge` | 932 | 10.3% | `ui_urgencia_presente`=Sí y `ui_esfuerzo_presente`=No |
| `other` | 57 | 0.6% | UI presente sin criterio claro de tipo |

---

## Resumen global de códigos CDC de missings

| Código | Significado | Variables afectadas |
|---|---|---|
| 7 | Refused | `dx_cancer`, `fumadora_alguna_vez`, `nivel_pobreza_familiar`, `ui_frecuencia`, `ui_cantidad`, `ui_esfuerzo_presente`, `ui_esfuerzo_frecuencia`, `ui_urgencia_presente`, `ui_otro_tipo_presente`, `ui_impacto_actividades` |
| 9 | Don't know | `dx_hipertension`, `medicacion_hta_cicloL`, `dx_diabetes`, `dx_artritis`, `dx_cancer`, `fumadora_alguna_vez`, `nivel_pobreza_familiar`, `ui_frecuencia`, `ui_cantidad`, `ui_esfuerzo_presente`, `ui_urgencia_presente`, `ui_urgencia_frecuencia`, `ui_otro_tipo_presente`, `ui_impacto_actividades` |
| 77 | Refused (numérico) | `pais_nacimiento` |
| 99 | Don't know (numérico) | `pais_nacimiento` |

---

*Última actualización: 18 de Marzo de 2026*
