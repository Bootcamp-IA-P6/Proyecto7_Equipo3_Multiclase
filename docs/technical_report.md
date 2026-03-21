# Reporte de Decisiones Técnicas - Fase ETL y Pipeline

## 1. Decisiones de Limpieza (ETL)
* **Variable Objetivo:** Se fusionó la clase `other` con `urge` (n=57) debido a la similitud clínica y la falta de masa crítica para el entrenamiento multiclase.
* **Imputación:** Se utilizó **KNNImputer** tras la recodificación binaria para completar los valores faltantes manteniendo la estructura de correlación del dataset.
* **Encoding:** Se aplicó **One-Hot Encoding** a las variables nominales (`etnia`, `pais_nacimiento`) para permitir su procesamiento por modelos lineales y de boosting.

## 2. Decisiones del Pipeline (Preprocesamiento)
* **Escalado:** Uso de `StandardScaler` para normalizar las variables continuas: `edad_anios`, `imc` y `economic_status`.
* **Optimización de SMOTE (Prevención de Overfitting):** Tras detectar un desajuste del 53.46% entre Train (0.99) y Test (0.46), se decidió integrar el **SMOTE dentro del Pipeline** con Validación Cruzada (CV). Esto asegura que el balanceo se aplique solo en el set de entrenamiento de cada fold, eliminando la fuga de datos (*data leakage*).
* **Estandarización:** Se renombró la variable socioeconómica a **`economic_status`** para asegurar coherencia técnica y rigor profesional en el reporte final.