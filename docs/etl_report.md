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

Este paso se ejecuta **antes** del KNNImputer para garantizar que la imputación opera sobre la escala cor

---

## Paso 9 — Pipeline de Preprocesamiento y Persistencia

Tras la limpieza inicial, se han aplicado las siguientes transformaciones críticas para preparar los datos para el modelado:

### 9.1. Estandarización de Variables (Scalers)
Se ha aplicado `StandardScaler` a las variables continuas (`edad_anios`, `imc` y `economic_status`). Esto asegura que el modelo no se vea sesgado por la magnitud de las variables y que todas contribuyan equitativamente al aprendizaje.

### 9.2. Cambio de Nomenclatura Profesional
La variable original de nivel de pobreza se ha renombrado a **`economic_status`**. Esta decisión mejora la interpretabilidad técnica y alinea el dataset con estándares internacionales de informes de salud.

### 9.3. Balanceo de Clases (SMOTE)
Debido al desequilibrio en la variable objetivo, se implementó la técnica **SMOTE (Synthetic Minority Over-sampling Technique)**.
* **Justificación:** Prevenir el sesgo del modelo hacia la clase mayoritaria y mejorar el *Recall* en el diagnóstico de tipos de incontinencia minoritarios.
* **Resultado:** Distribución equilibrada al 25% por clase.

### 9.4. Persistencia (Serialization)
Para garantizar que el modelo en producción (Streamlit) use los mismos parámetros de transformación, se ha guardado el escalador en:
* `models/pipeline.pkl`