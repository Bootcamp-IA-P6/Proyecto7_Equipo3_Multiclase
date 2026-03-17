# Decisiones de ETL e Imputación de NHANES

Basado en los resultados del Análisis Exploratorio de Datos (EDA), se han tomado las siguientes decisiones documentadas para la construcción del Pipeline de Datos (nhanes_clean.csv):

## 1. Tratamiento de Códigos Especiales (CDC)

- **Problema:** El CDC codifica valores perdidos o rechazos con `7`, `9`, `77`, `99`.
- **Decisión:** Transformar todos estos códigos explícitos a verdaderos `NaN` aritméticos antes de cualquier imputación para evitar que el modelo asuma falsamente frecuencias altísimas (e.g., 99 en `ui_frecuencia`).

## 2. Variables Numéricas y Categóricas (Atrición Aleatoria MCAR / MAR)

Para variables demográficas o clínicas con pocos valores faltantes (<20%) asumimos atrición debido al diseño de la encuesta:

- **Numéricas (e.g., `imc`, `edad_anios`):** Imputación por la **Mediana**. (Minimiza el impacto de los severos outliers de obesidad detectados en el boxplot).
- **Categóricas / Booleanas (e.g., `etnia`, `dx_diabetes`):** Imputación por la **Moda** (el valor más frecuente).

## 3. Manejo de Variables Sintomatológicas de Incontinencia (Patrón MNAR)

**Problema:** Variables como `ui_frecuencia`, `ui_cantidad`, o `ui_molestia_percibida` tienen más del 40% de nulos. Estos nulos ocurren específicamente en pacientes de clase `none` del target a las que no se les formularon estas preguntas.

**Decisión:** Estas variables causan Fuga de Información ("Data Leakage"). Eliminar completamente este bloque de columnas para el modelado, ya que el objetivo es **predecir** la afección basándonos en historial demográfico/clínico, no documentar la severidad del síntoma.

## 4. Fusión de Clases (Limpieza del Target)

- Siguiendo requerimientos médicos, la clase `other` (57 escasos registros) se va a mapear (fusionar) de forma directa dentro de la categoría `urge` (urgencia).
