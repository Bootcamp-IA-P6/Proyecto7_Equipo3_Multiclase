# Reporte Ejecutivo: Solución de Inteligencia de Datos para la Salud Femenina
**Proyecto VII - Clasificación Multiclase de Incontinencia Urinaria (UI)**
**Equipo 3 | Scrum Master: Isabel Rodriguez Amor**

## 1. Introducción y Propósito
Este reporte detalla el desarrollo de una herramienta de triaje digital diseñada para abordar el subdiagnóstico de la Incontinencia Urinaria femenina. Utilizando datos del **CDC (NHANES 2017-2023)**, el equipo ha construido un ecosistema que transforma síntomas reportados por la usuaria en clasificaciones clínicas precisas, eliminando las barreras del tabú y facilitando el acceso a un diagnóstico temprano e informado.

---

## 2. Metodología de Trabajo y Excelencia Operativa
Como equipo, hemos gestionado este proyecto bajo el marco **Agile/SCRUM**, priorizando la trazabilidad y el rigor técnico en cada fase:

### 2.1. Gestión del Ciclo de Vida del Software (SDLC)
* **Gobernanza del Repositorio:** Uso de flujo de trabajo basado en ramas (`feature-branching`). Integración mediante **Peer Review** obligatorio, asegurando que cada línea de código cumpla con los estándares del equipo antes de su fusión en la rama de desarrollo.
* **Gestión de Entornos:** Implementación de **`uv`** como gestor de paquetes de última generación, garantizando un entorno 100% reproducible y libre de conflictos de dependencias.
* **Sincronización Ágil:** Uso de GitHub Projects para la gestión del backlog y sesiones Daily para la resolución proactiva de bloqueos.

### 2.2. Ingeniería de Datos y Calidad Clínica
* **Tratamiento de Datos:** Procesamiento de más de 9,000 registros con eliminación de valores centinela e imputación inteligente mediante **KNNImputer**, preservando la estructura de correlación médica original.
* **Estandarización:** Aplicación de `StandardScaler` y codificación avanzada para asegurar que el modelo interprete correctamente tanto variables físicas (IMC, Edad) como factores socioeconómicos.

---

## 3. Resolución de Desafíos Técnicos (Hito del Sprint)
El mayor reto del proyecto fue la detección de un **overfitting masivo del 53.46%** en las fases iniciales de modelado. 

**Nuestra Respuesta Estratégica:**
El equipo rediseñó el Pipeline técnico para integrar el balanceo de clases (**SMOTE**) y la **Validación Cruzada (CV)** de forma dinámica. Al encapsular estas transformaciones dentro del Pipeline, eliminamos la fuga de datos (*data leakage*), garantizando un modelo con capacidad de generalización real y honestidad en sus predicciones.

---

## 4. Arquitectura de la Solución Final
Se ha optado por una arquitectura de **Ensemble (Votación Suave)** que combina las fortalezas de tres algoritmos de alto rendimiento:
1.  **XGBoost:** Para capturar patrones no lineales en los síntomas.
2.  **Random Forest:** Para reducir la varianza y aportar estabilidad al diagnóstico.
3.  **LightGBM:** Para optimizar la velocidad de respuesta en la interfaz de usuario.

---

## 5. Resultados e Impacto Social
* **Producto Final:** Aplicación web en **Streamlit** diseñada con un enfoque centrado en la usuaria, permitiendo un triaje privado y seguro.
* **Estado de las Métricas:** El sistema se encuentra actualmente en su fase final de consolidación. Tras la refactorización del pipeline para corregir el sobreajuste, los modelos están siendo sometidos a pruebas de estrés para asegurar que el *Recall* (sensibilidad) en la detección de tipos de incontinencia críticos cumpla con los estándares de fiabilidad clínica establecidos por el equipo.
* **Visión de Futuro:** Esta herramienta representa el primer paso hacia una plataforma de salud femenina integral, escalable a otras patologías subdiagnosticadas.

---
*Documento generado para la entrega final del Proyecto VII - Marzo 2026.*