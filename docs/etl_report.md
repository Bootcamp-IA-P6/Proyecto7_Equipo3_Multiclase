# Reporte de Decisiones ETL — NHANES UI Women

**Notebook:** `00_eda_etl.ipynb` — Sección 8  
**Input:** `nhanes_ui_women.csv` (9.074 filas × 27 columnas)  
**Output:** `nhanes_clean.csv` (9.074 filas × 24 columnas)  
**Fecha:** Marzo 2026

---

## Resumen de transformaciones

| Métrica | Antes | Después |
|---|---|---|
| Filas | 9.074 | 9.074 |
| Columnas | 27 | 24 |
| Valores nulos | >6.000 | **0** |
| Clases en target | 5 (`other` incluida) | **4** |
| Códigos CDC sentinel | Presentes | Eliminados (→ NaN) |
| Variables binarias | Escala 1/2 (NHANES) | Recodificadas 0/1 |
| Etnia | Variable numérica única | OHE — 5 columnas dummy |
| País de nacimiento | Variable numérica única | OHE — 2 columnas dummy |

---

## Paso 1 — Reemplazo de códigos CDC sentinel (Sección 2.3)

Los códigos 7, 9, 77 y 99 son valores centinela del CDC que representan "Refused" y "Don't know". No son datos reales y deben tratarse como missings antes de cualquier análisis.

```python
CDC_MISS = [7, 9, 77, 99]
for col in df.select_dtypes(include='number').columns:
    df[col] = df[col].replace(CDC_MISS, np.nan)
```

**Resultado:** 26 combinaciones variable-código identificadas y corregidas en el dataset.

---

## Paso 2 — Fusión de clase `other` → `urge` (Sección 8.3)

Los 57 casos con `target_tipo_ui = 'other'` fueron reasignados a `'urge'`.

**Justificación clínica:** La incontinencia de tipo "otro" que no responde a los criterios de esfuerzo ni mixta comparte mecanismo fisiopatológico con la urgencia. Con n=57 (0.6% del total), la clase no tiene masa suficiente para generalizar en un modelo multiclase.

```python
df_etl.loc[df_etl['target_tipo_ui'] == 'other', 'target_tipo_ui'] = 'urge'
```

| Clase | N antes | N después |
|---|---|---|
| `none` | 4.857 | 4.857 |
| `mixed` | 1.642 | 1.642 |
| `stress` | 1.586 | 1.586 |
| `urge` | 932 | **989** (+57) |
| `other` | 57 | — (fusionada) |

---

## Paso 3 — Eliminación de columnas (Sección 8.4)

| Variable eliminada | Razón |
|---|---|
| `id_participante` | Identificador único — no predictivo |
| `ciclo_nhanes` | Una sola categoría en el dataset — no aporta información |
| `peso_encuesta` | Peso de diseño muestral (52% missing) — no tiene rol predictivo clínico |
| `medicacion_hta_cicloP` | 82% missing + alta colinealidad con `dx_hipertension` |
| `medicacion_hta_cicloL` | 81% missing + alta colinealidad con `dx_hipertension` |
| `ui_esfuerzo_frecuencia` | 81% missing — subpregunta condicional (MNAR estructural): solo se responde si `ui_esfuerzo_presente = Sí` |
| `ui_urgencia_frecuencia` | 85% missing — subpregunta condicional (MNAR estructural): solo se responde si `ui_urgencia_presente = Sí` |
| `target_tiene_ui` | Derivada directamente del target multiclase → **data leakage** |

---

## Paso 4 — Recodificación de variables binarias 1/2 → 0/1 (Sección 8.5)

NHANES codifica las respuestas binarias como 1=Sí / 2=No. Se recodifican al estándar ML (1=Sí / 0=No) usando `.map({1: 1, 2: 0})`.

Este paso se ejecuta **antes** del KNNImputer para garantizar que la imputación opera sobre la escala correcta (0/1) y el redondeo posterior produce valores válidos.

```python
binary_cols = [
    'dx_hipertension', 'dx_diabetes', 'dx_cancer', 'dx_artritis',
    'fumadora_alguna_vez', 'actividad_fisica_vigorosa',
    'ui_esfuerzo_presente', 'ui_urgencia_presente', 'ui_otro_tipo_presente',
]
for col in binary_cols:
    if col in df_etl.columns:
        df_etl[col] = df_etl[col].map({1: 1, 2: 0})
```

---

## Paso 5 — Imputación simple por moda y mediana (Sección 8.6)

Para variables con menos del 5% de missings se usa la estrategia más simple, adecuada cuando los missings son escasos y sin patrón claro.

| Variable | Missings | Estrategia |
|---|---|---|
| `pais_nacimiento` | <0.1% | Moda |
| `dx_hipertension` | <0.1% (tras CDC codes) | Moda |
| `dx_diabetes` | <0.1% (tras CDC codes) | Moda |
| `dx_cancer` | <0.1% (tras CDC codes) | Moda |
| `dx_artritis` | <0.1% (tras CDC codes) | Moda |
| `fumadora_alguna_vez` | <0.1% | Moda |
| `edad_anios` | ~1% (92 casos, CDC code 77) | Mediana — distribución asimétrica |

---

## Paso 6 — Imputación KNN para variables MAR (Sección 8.7)

Para variables con patrón MAR (los missings dependen de otras variables observables) se usa `KNNImputer(n_neighbors=5)`. Busca los 5 vecinos más cercanos en el espacio de todas las variables y usa sus valores para estimar el missing, respetando las correlaciones del dataset.

```python
from sklearn.impute import KNNImputer
imputer = KNNImputer(n_neighbors=5)
df_etl[knn_vars] = imputer.fit_transform(df_etl[knn_vars])
```

| Variable | % Missing | Tipo de missing |
|---|---|---|
| `imc` | 16% | MAR — más missings en participantes jóvenes y clase `none` |
| `nivel_pobreza_familiar` | 10% | MNAR leve — non-response correlaciona con nivel real de ingresos |
| `actividad_fisica_vigorosa` | 48% | MAR — más missings en personas mayores y clase `none` |
| `ui_frecuencia` | 24% | MAR estructural — solo se pregunta a mujeres con UI positiva |
| `ui_cantidad` | 61% | MAR estructural — solo se pregunta a mujeres con UI positiva |
| `ui_esfuerzo_presente` | 24% | MAR estructural — solo se pregunta a mujeres con UI positiva |
| `ui_urgencia_presente` | 24% | MAR estructural — solo se pregunta a mujeres con UI positiva |
| `ui_otro_tipo_presente` | 55% | MAR estructural — solo se pregunta a mujeres con UI positiva |
| `ui_molestia_percibida` | 74% | MAR estructural — solo se pregunta a mujeres con UI positiva |
| `ui_impacto_actividades` | 54% | MAR estructural — solo se pregunta a mujeres con UI positiva |

---

## Paso 7 — Redondeo y clampeo post-KNN (Sección 8.8)

El KNNImputer opera con promedios ponderados, produciendo valores continuos para variables que deben ser enteras. Se aplica `.round().clip(min, max).astype(int)` a cada variable según su rango válido.

| Variable | Rango válido |
|---|---|
| `actividad_fisica_vigorosa` | [0, 1] |
| `ui_frecuencia` | [1, 6] |
| `ui_cantidad` | [1, 3] |
| `ui_esfuerzo_presente` | [0, 1] |
| `ui_urgencia_presente` | [0, 1] |
| `ui_otro_tipo_presente` | [0, 1] |
| `ui_molestia_percibida` | [0, 4] |
| `ui_impacto_actividades` | [0, 4] |

---

## Paso 8 — One-Hot Encoding de variables nominales (Sección 8.9)

Las variables `etnia` y `pais_nacimiento` son nominales (sin orden intrínseco) y se transforman con `pd.get_dummies`.

### Etnia

```python
etnia_map = {1:'hisp_mex', 2:'hisp_otra', 3:'blanca', 4:'negra', 6:'asiatica', 7:'otra'}
etnia_dummies = pd.get_dummies(df_etl['etnia_lbl'], prefix='etnia', drop_first=False, dtype=int)
```

Columnas generadas: `etnia_hisp_mex`, `etnia_hisp_otra`, `etnia_blanca`, `etnia_negra`, `etnia_otra`.  
Categoría de referencia implícita: `etnia_asiatica`.

### País de nacimiento

```python
pais_map = {1:'usa', 2:'mexico', 3:'otro'}
pais_dummies = pd.get_dummies(df_etl['pais_lbl'], prefix='pais', drop_first=False, dtype=int)
```

Columnas generadas: `pais_usa`, `pais_mexico`.  
Categoría de referencia implícita: `pais_otro`.

### Nivel de pobreza familiar

Variable numérica continua (ratio ingreso/umbral de pobreza). No requiere encoding — se conserva tal cual.

---

*Reporte generado desde `00_eda_etl.ipynb` — 18 de Marzo de 2026*
