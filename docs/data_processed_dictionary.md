# Diccionario de Variables — NHANES UI Women (Dataset Procesado)

**Dataset:** `nhanes_clean.csv`  
**Filas:** 9.074 | **Columnas:** 24  
**Origen:** `nhanes_ui_women.csv` tras ETL completo (`00_eda_etl.ipynb`)  
**Población:** Mujeres ≥20 años con datos de incontinencia urinaria

> Dataset sin valores nulos. Listo para ingesta directa en el pipeline de modelado.  
> Para el dataset original con códigos CDC, consultar `data_dictionary_raw.md`.  
> Para el detalle de cada transformación, consultar `etl_report.md`.

---

## Variables Continuas

| Variable | Tipo | Descripción | Min | Max | Media | Mediana |
|---|---|---|---|---|---|---|
| `edad_anios` | float64 | Edad en años cumplidos | 20 | 80 | 51.8 | 53.0 |
| `imc` | float64 | Índice de Masa Corporal (kg/m²) | 11.1 | 92.3 | 30.3 | 29.2 |
| `nivel_pobreza_familiar` | float64 | Ratio ingreso familiar / umbral de pobreza federal | 1.0 | 3.0 | 2.2 | 2.4 |

---

## Variables Clínicas Binarias

Recodificadas de escala NHANES (1=Sí / 2=No) a convención ML (1=Sí / 0=No).

| Variable | Tipo | Descripción | N=0 | N=1 |
|---|---|---|---|---|
| `dx_hipertension` | float64 | Hipertensión diagnosticada por médico | 5.660 (62.4%) | 3.414 (37.6%) |
| `dx_diabetes` | float64 | Diabetes diagnosticada por médico | 7.861 (86.6%) | 1.213 (13.4%) |
| `dx_cancer` | float64 | Cáncer diagnosticado por médico | 7.877 (86.8%) | 1.197 (13.2%) |
| `dx_artritis` | float64 | Artritis diagnosticada por médico | 5.885 (64.9%) | 3.189 (35.1%) |
| `fumadora_alguna_vez` | float64 | Ha fumado al menos 100 cigarrillos en su vida | 5.985 (66.0%) | 3.089 (34.0%) |

---

## Variables de Estilo de Vida

Recodificada de escala NHANES (1=Sí / 2=No) a convención ML (1=Sí / 0=No) antes de la imputación KNN.

| Variable | Tipo | Descripción | N=0 | N=1 |
|---|---|---|---|---|
| `actividad_fisica_vigorosa` | int64 | Realiza actividad física vigorosa en su tiempo libre | 8.006 (88.2%) | 1.068 (11.8%) |

---

## Variables de Síntomas de UI — Ordinales

Variables de escala ordinal conservadas como enteros tras imputación KNN y redondeo al rango válido.

| Variable | Tipo | Descripción | Valores |
|---|---|---|---|
| `ui_frecuencia` | int64 | Frecuencia de pérdida de orina en los últimos 12 meses | 1=Nunca · 2=<1/mes · 3=Pocas veces al mes · 4=Pocas veces a la semana · 5=Todos los días |
| `ui_cantidad` | int64 | Cantidad de orina perdida habitualmente | 1=Gotas · 2=Chorro pequeño · 3=Más |
| `ui_molestia_percibida` | int64 | Molestia percibida por la pérdida de orina | 1=Nada · 2=Poca · 3=Moderada · 4=Mucha |
| `ui_impacto_actividades` | int64 | Impacto de la pérdida de orina en actividades cotidianas | 1=Nada · 2=Poca · 3=Moderada · 4=Mucha |

---

## Variables de Síntomas de UI — Binarias

Recodificadas de escala NHANES (1=Sí / 2=No) a convención ML (1=Sí / 0=No).

| Variable | Tipo | Descripción | N=0 | N=1 |
|---|---|---|---|---|
| `ui_esfuerzo_presente` | int64 | Pierde orina al toser, reír, estornudar o hacer esfuerzo físico | 5.334 (58.8%) | 3.740 (41.2%) |
| `ui_urgencia_presente` | int64 | Pierde orina con urgencia antes de llegar al baño | 6.092 (67.1%) | 2.982 (32.9%) |
| `ui_otro_tipo_presente` | int64 | Pierde orina por otro motivo distinto al esfuerzo o la urgencia | 8.205 (90.4%) | 869 (9.6%) |

---

## Variables de Etnia — One-Hot Encoding

Generadas a partir de `etnia` (NHANES `RIDRETH1`). Codificación: 1=pertenece / 0=no pertenece.  
Categoría de referencia implícita: `etnia_asiatica` (no aparece en el dataset).

| Variable | Tipo | Descripción | N=1 | % |
|---|---|---|---|---|
| `etnia_blanca` | int64 | Non-Hispanic White | 4.140 | 45.6% |
| `etnia_negra` | int64 | Non-Hispanic Black | 1.862 | 20.5% |
| `etnia_otra` | int64 | Otra etnia / sin clasificar | 1.313 | 14.5% |
| `etnia_hisp_otra` | int64 | Other Hispanic | 942 | 10.4% |
| `etnia_hisp_mex` | int64 | Mexican American | 817 | 9.0% |

> Cada participante tiene exactamente un 1 y cuatro 0 entre estas columnas.

---

## Variables de País de Nacimiento — One-Hot Encoding

Generadas a partir de `pais_nacimiento` (NHANES `DMDBORN4`). Codificación: 1=pertenece / 0=no pertenece.  
Categoría de referencia implícita: `pais_otro` (no aparece en el dataset).

| Variable | Tipo | Descripción | N=1 | % |
|---|---|---|---|---|
| `pais_usa` | int64 | Nacida en EE.UU. | 6.796 | 74.9% |
| `pais_mexico` | int64 | Nacida en México | 2.278 | 25.1% |

> Cada participante tiene exactamente un 1 y un 0 entre estas columnas.

---

## Variable Objetivo

| Variable | Tipo | Descripción | Missings |
|---|---|---|---|
| `target_tipo_ui` | str | Tipo de incontinencia urinaria | 0 |

### Distribución

| Clase | Descripción clínica | N | % |
|---|---|---|---|
| `none` | Sin incontinencia | 4.857 | 53.5% |
| `mixed` | UI mixta — esfuerzo y urgencia presentes | 1.642 | 18.1% |
| `stress` | UI de esfuerzo — solo esfuerzo presente | 1.586 | 17.5% |
| `urge` | UI de urgencia — solo urgencia presente (incluye 57 casos `other` fusionados) | 989 | 10.9% |

Ratio de desbalanceo `none:urge` = **4.9:1**.

---

*Última actualización: 18 de Marzo de 2026*
