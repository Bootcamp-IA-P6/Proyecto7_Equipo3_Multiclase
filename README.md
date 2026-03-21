# Clasificación Multiclase de Incontinencia Urinaria Femenina

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://www.python.org/)
[![Dataset](https://img.shields.io/badge/Dataset-NHANES%202017--2023-green)](https://www.cdc.gov/nchs/nhanes/)
[![License](https://img.shields.io/badge/License-Académico-lightgrey)]()
[![Estado](https://img.shields.io/badge/Estado-En%20desarrollo-yellow)]()

Proyecto de Machine Learning para clasificación multiclase del tipo de incontinencia urinaria en mujeres adultas, desarrollado a partir del dataset NHANES (CDC, 2017–2023).

> ⚠️ **Aviso:** Esta herramienta es de uso académico e informativo. No sustituye el diagnóstico médico profesional.

---

## 🎯 El problema

La incontinencia urinaria (UI) afecta a **1 de cada 3 mujeres adultas** a nivel mundial, pero figura entre los trastornos de salud más subdiagnosticados en medicina primaria. Este proyecto propone una aplicación web que funciona como un checklist de síntomas inteligente: la usuaria selecciona sus síntomas, el modelo predice el tipo de incontinencia más probable y orienta hacia el tipo de intervención adecuado.

**El objetivo no es sustituir al médico**, sino reducir la barrera de entrada y que la mujer llegue a la consulta con información clara.

---

## 🛠️ Stack Técnico
* **Lenguaje:** Python 3.11+
* **Bibliotecas Clave:** Pandas, Scikit-Learn, Imbalanced-learn (SMOTE).
* **Modelo:** Clasificación Multiclase (XGBoost / Random Forest).
* **Despliegue:** Streamlit (enfocado a la experiencia de usuario de la paciente).

---

## 🚀 Instalación y Uso

Este proyecto utiliza **uv** para una gestión de dependencias ultrarrápida.

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/nombre-del-repo.git](https://github.com/tu-usuario/nombre-del-repo.git)
   cd nombre-del-repo
2. **Crar entorno y sincronizar dependencias:** 
   uv sync
3. **Ejecutar la aplicación (Streamlit)**
   uv run streamlit run src/app.py   

---

## 🧠 Metodología y Calidad del Dato
Para asegurar la fiabilidad de la herramienta, el equipo ha implementado:
1. **Validación Cruzada Robusta:** Integrando el sobremuestreo (SMOTE) dentro del pipeline para evitar el sobreajuste.
2. **Imputación Avanzada:** Uso de KNNImputer para tratar datos faltantes del NHANES sin perder correlaciones clínicas.
3. **Enfoque en Usuario:** Interfaz simplificada que traduce términos médicos a lenguaje cotidiano.