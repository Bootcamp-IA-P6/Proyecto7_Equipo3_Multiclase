# Clasificación Multiclase de Incontinencia Urinaria Femenina

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://www.python.org/)
[![Dataset](https://img.shields.io/badge/Dataset-NHANES%202017--2023-green)](https://www.cdc.gov/nchs/nhanes/)
[![License](https://img.shields.io/badge/License-Académico-lightgrey)]()
[![Estado](https://img.shields.io/badge/Estado-Finalizado-brightgreen)]()
[![ML](https://img.shields.io/badge/ML-XGBoost%20%7C%20RF%20%7C%20LightGBM-orange)]()
[![Streamlit](https://img.shields.io/badge/App-Streamlit-ff4b4b?logo=streamlit)](https://streamlit.io/)
[![uv](https://img.shields.io/badge/uv-Package%20Manager-blueviolet)](https://docs.astral.sh/uv/)

Proyecto de Machine Learning para clasificación multiclase del tipo de incontinencia urinaria en mujeres adultas, desarrollado a partir del dataset NHANES (CDC, 2017–2023).

> **Aviso:** Esta herramienta es de uso académico e informativo. No sustituye el diagnóstico médico profesional.

---

## El problema

La incontinencia urinaria (UI) afecta a **1 de cada 3 mujeres adultas** a nivel mundial, pero figura entre los trastornos de salud más subdiagnosticados en medicina primaria. Este proyecto propone una aplicación web que funciona como un checklist de síntomas inteligente: la usuaria selecciona sus síntomas, el modelo predice el tipo de incontinencia más probable y orienta hacia el tipo de intervención adecuado.

**El objetivo no es sustituir al médico**, sino reducir la barrera de entrada y que la mujer llegue a la consulta con información clara.

---

## Objetivo del proyecto

Desarrollar un modelo de clasificación multiclase capaz de predecir el tipo de incontinencia urinaria a partir de variables demográficas, clínicas y de síntomas autorreportados, utilizando un **ensemble de votación suave (soft voting)** que combina XGBoost, Random Forest y LightGBM, ponderado por F1-macro en validación cruzada.

---

## Dataset

**Fuente:** [NHANES (National Health and Nutrition Examination Survey)](https://www.cdc.gov/nchs/nhanes/) — CDC, ciclos 2017–2023.

| Característica             | Valor                 |
| --------------------------- | --------------------- |
| Registros                   | 9.074 mujeres adultas |
| Variables originales        | 27                    |
| Variables tras ETL          | 24                    |
| Valores nulos tras limpieza | 0                     |

### Clases del target (`target_tipo_ui`)

| Clase      | Descripción                                  | N     | Proporción |
| ---------- | --------------------------------------------- | ----- | ----------- |
| `none`   | Sin incontinencia                             | 4.857 | 53,5 %      |
| `mixed`  | Incontinencia mixta (esfuerzo + urgencia)     | 1.642 | 18,1 %      |
| `stress` | Incontinencia de esfuerzo                     | 1.586 | 17,5 %      |
| `urge`   | Incontinencia de urgencia (incluye `other`) | 989   | 10,9 %      |

> La clase original `other` (n=57) fue fusionada con `urge` por criterio clínico. Ver [docs/etl_report.md](docs/etl_report.md) para más detalles.

---

## Arquitectura del modelo

```
┌─────────────┐   ┌─────────────────┐   ┌─────────────┐
│  XGBoost    │   │  Random Forest  │   │  LightGBM   │
│  Classifier │   │  Classifier     │   │  Classifier  │
└──────┬──────┘   └────────┬────────┘   └──────┬──────┘
       │                   │                    │
       └───────────┬───────┘────────────────────┘
                   │
        ┌──────────▼──────────┐
        │  Soft Voting        │
        │  (pesos por F1-macro│
        │   en CV)            │
        └──────────┬──────────┘
                   │
            ┌──────▼──────┐
            │ Predicción  │
            │ final       │
            └─────────────┘
```

- Cada modelo individual se entrena con **SMOTE** dentro de un `ImbPipeline` para manejar el desbalanceo de clases.
- Los hiperparámetros se optimizan con **Optuna** + validación cruzada estratificada (`StratifiedKFold`, k=5).
- El ensemble final utiliza `VotingClassifier(voting='soft')` con pesos proporcionales al **F1-macro** de cada modelo en CV.

---

## Estructura del repositorio

```
Proyecto7_Equipo3_Multiclase/
├── app/                          # Paquete de la app Streamlit
│   ├── ___init___.py
│   └── styles.css                # Estilos CSS personalizados
├── assets/                       # Gráficos generados (EDA, matrices de confusión, etc.)
├── data/
│   ├── raw/                      # Dataset original (nhanes_ui_women.csv)
│   └── processed/                # Datos limpios y splits train/test
├── docs/
│   ├── data_raw_dictionary.md    # Diccionario de variables originales
│   ├── data_processed_dictionary.md  # Diccionario de variables procesadas
│   └── etl_report.md            # Reporte de decisiones ETL
├── models/                       # Modelos serializados (.pkl)
│   ├── pipeline.pkl              # Pipeline de preprocesamiento
│   ├── cv_config.pkl             # Configuración de validación cruzada
│   └── random_forest.pkl         # Modelo Random Forest
├── notebooks/
│   ├── 00_eda_etl.ipynb          # Exploración de datos y ETL
│   ├── 01_pipeline.ipynb         # Pipeline de preprocesamiento
│   ├── 02_random_forest.ipynb    # Entrenamiento Random Forest
│   ├── 03_lightgbm.ipynb         # Entrenamiento LightGBM
│   ├── 04_xgboost.ipynb          # Entrenamiento XGBoost
│   ├── 05_ensemble.ipynb         # Ensemble (Soft Voting)
│   └── modeling/                 # Notebooks individuales del equipo
├── src/
│   └── db.py                     # Integración con Supabase
├── app.py                        # Punto de entrada de la app Streamlit
├── pyproject.toml                # Dependencias y configuración del proyecto
├── uv.lock                       # Lockfile de dependencias
└── README.md
```

---

## Instalación

### Requisitos previos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (gestor de paquetes)

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/Bootcamp-IA-P6/Proyecto7_Equipo3_Multiclase.git
cd Proyecto7_Equipo3_Multiclase

# 2. Crear el entorno virtual e instalar dependencias
uv sync

# 3. Activar el entorno virtual
source .venv/bin/activate
```

### Variables de entorno

Crear un archivo `.env` en la raíz del proyecto con las credenciales de Supabase:

```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-clave-anon
```

---

## Uso

### Ejecutar la app

```bash
uv run streamlit run app.py
```

### Ejecutar los notebooks

```bash
uv run jupyter notebook
```

---

## Tech Stack

| Categoría           | Tecnologías                                  |
| -------------------- | -------------------------------------------- |
| Lenguaje             | Python 3.11+                                 |
| ML                   | scikit-learn, XGBoost, LightGBM, SMOTE       |
| Optimización         | Optuna                                       |
| App                  | Streamlit                                    |
| Base de datos        | Supabase                                     |
| Gestión de paquetes  | uv                                           |
| Notebooks            | Jupyter                                      |

---

## Equipo

| Nombre   | Rol           |
| -------- | ------------- |
| Isa      | Scrum Master  |
| Iris     | Product Owner |
| Maryori  | Data analyst  |
| Gabriela | Data analyst  |
| Camila   | Data analyst  |

*Proyecto desarrollado en el bootcamp de IA de [Factoria F5](https://factoriaf5.org/).*
