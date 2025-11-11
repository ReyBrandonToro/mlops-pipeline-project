# 🚀 MLOps Pipeline - Detección de Fraude Financiero

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Proyecto MLOps completo para la detección de fraude en transacciones financieras. Implementa un pipeline end-to-end que incluye análisis exploratorio, ingeniería de características, entrenamiento de modelos, despliegue via API REST y monitoreo de drift.

## 📋 Tabla de Contenidos

- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Arquitectura](#-arquitectura)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Uso](#-uso)
- [Hallazgos del EDA](#-hallazgos-del-eda)
- [Modelos y Performance](#-modelos-y-performance)
- [API REST](#-api-rest)
- [Dashboard de Monitoreo](#-dashboard-de-monitoreo)
- [Docker](#-docker)
- [Contribuciones](#-contribuciones)

---

## 🎯 Descripción del Proyecto

Este proyecto implementa un sistema completo de MLOps para detectar transacciones fraudulentas en un dataset de transacciones financieras. El sistema cubre todas las etapas del ciclo de vida de un modelo de Machine Learning:

### Caso de Negocio

Las instituciones financieras pierden miles de millones de dólares anualmente debido al fraude. Este proyecto proporciona una solución automatizada para:

- ✅ **Detectar transacciones fraudulentas** en tiempo real
- ✅ **Reducir falsos positivos** mediante modelos optimizados
- ✅ **Monitorear la calidad** de los datos en producción
- ✅ **Escalar fácilmente** mediante contenedores Docker

### Características Principales

- 📊 **Análisis Exploratorio Completo**: Notebook interactivo con visualizaciones
- 🔍 **Validación de Datos**: Reglas de negocio automatizadas
- 🛠️ **Ingeniería de Características**: Features derivados optimizados
- 🤖 **Múltiples Modelos**: Comparación de LogisticRegression, RandomForest, XGBoost
- 🚀 **API REST**: Predicciones en tiempo real con FastAPI
- 📈 **Dashboard de Monitoreo**: Detección de data drift con Streamlit
- 🐳 **Dockerizado**: Despliegue sencillo en cualquier entorno

---

## 🏗️ Arquitectura

El proyecto sigue una arquitectura modular basada en **clases e importaciones**, facilitando el mantenimiento y escalabilidad:

```
┌─────────────────┐
│  Data Source    │
│ (CSV Dataset)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│  DataLoader     │─────▶│ DataValidator    │
│ (cargar_datos)  │      │ (data_validation)│
└────────┬────────┘      └──────────────────┘
         │
         ▼
┌─────────────────┐
│ FeatureEngineer │
│ (ft_engineering)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│  ModelTrainer   │─────▶│  Best Model      │
│ (model_training)│      │  (best_model.    │
└─────────────────┘      │   joblib)        │
                         └────────┬──────────┘
                                  │
                  ┌───────────────┴──────────────┐
                  │                              │
                  ▼                              ▼
         ┌─────────────────┐          ┌─────────────────┐
         │  FastAPI Server │          │    Streamlit    │
         │ (model_deploy)  │          │  (monitoring)   │
         └─────────────────┘          └─────────────────┘
```

### Flujo de Trabajo

1. **Carga**: `DataLoader` lee el dataset y elimina columnas irrelevantes
2. **Validación**: `DataValidator` verifica esquema, tipos y reglas de negocio
3. **Ingeniería**: `FeatureEngineer` crea features, divide datos y preprocesa
4. **Entrenamiento**: `ModelTrainer` entrena múltiples modelos y selecciona el mejor
5. **Despliegue**: API REST con FastAPI sirve predicciones
6. **Monitoreo**: Dashboard Streamlit detecta data drift

---

## 📁 Estructura del Proyecto

```
mlops_pipeline/
│
├── mlops_pipeline/
│   └── src/
│       ├── __init__.py                    # Paquete Python
│       ├── config.py                      # Configuración centralizada
│       ├── cargar_datos.py                # Clase DataLoader
│       ├── data_validation.py             # Clase DataValidator
│       ├── ft_engineering.py              # Clase FeatureEngineer
│       ├── model_training_evaluation.py   # Clase ModelTrainer (orquestador)
│       ├── model_deploy.py                # API REST con FastAPI
│       ├── model_monitoring.py            # Dashboard con Streamlit
│       └── comprension_eda.ipynb          # Notebook de EDA
│
├── financial_fraud_dataset.csv            # Dataset principal
├── best_model.joblib                      # Mejor modelo entrenado
├── preprocessor.joblib                    # Pipeline de preprocesamiento
│
├── requirements.txt                       # Dependencias de Python
├── config.json                            # Configuración del proyecto
├── setup.bat                              # Script de instalación (Windows)
├── .gitignore                             # Archivos ignorados por Git
├── Dockerfile                             # Configuración de contenedor
└── README.md                              # Este archivo
```

---

## 🔧 Instalación y Configuración

### Prerrequisitos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

### Opción 1: Instalación Automática (Windows)

```batch
# Ejecutar el script de configuración
setup.bat
```

Este script:
- Crea un entorno virtual `mlops_pipeline-venv`
- Instala todas las dependencias
- Activa el entorno

### Opción 2: Instalación Manual

```bash
# 1. Crear entorno virtual
python -m venv mlops_pipeline-venv

# 2. Activar el entorno
# Windows:
mlops_pipeline-venv\Scripts\activate
# Linux/Mac:
source mlops_pipeline-venv/bin/activate

# 3. Actualizar pip
pip install --upgrade pip

# 4. Instalar dependencias
pip install -r requirements.txt
```

### Verificar Instalación

```bash
python -c "import pandas, sklearn, fastapi, streamlit; print('✅ Instalación exitosa')"
```

---

## 🚀 Uso

### 🎯 Opción Recomendada: Menú Interactivo

La forma más fácil de usar el proyecto es con el menú interactivo:

```bash
python main.py
```

Esto abrirá un menú con todas las opciones disponibles:

```
┌────────────────────────────────────────────────────────────────┐
│  OPCIONES DISPONIBLES:                                         │
├────────────────────────────────────────────────────────────────┤
│  1. 📊 Ejecutar Pipeline Completo (E2E)                       │
│  2. 🔍 Solo Validar Datos                                     │
│  3. 🛠️  Solo Ingeniería de Características                    │
│  4. 🤖 Solo Entrenar Modelos                                  │
│  5. 🌐 Iniciar API REST                                       │
│  6. 📈 Abrir Dashboard de Monitoreo                           │
│  7. 📓 Abrir Notebook de EDA                                  │
│  8. ℹ️  Ver Información del Proyecto                          │
│  0. ❌ Salir                                                   │
└────────────────────────────────────────────────────────────────┘
```

### 1. Análisis Exploratorio de Datos (EDA)

Ejecutar el notebook para entender el dataset:

```bash
jupyter lab mlops_pipeline/src/comprension_eda.ipynb
```

El notebook incluye:
- Carga de datos y exploración inicial
- Análisis univariable (histogramas, boxplots, estadísticas)
- Análisis bivariable y multivariable (correlaciones, pairplots)
- Identificación de reglas de validación
- Propuesta de features derivados

### 2. Entrenar el Pipeline Completo

Ejecutar el orquestador que realiza todo el flujo E2E:

```bash
python -m mlops_pipeline.src.model_training_evaluation
```

Este comando:
1. ✅ Carga los datos
2. ✅ Valida la calidad e integridad
3. ✅ Aplica ingeniería de características
4. ✅ Entrena múltiples modelos (LogisticRegression, RandomForest, XGBoost)
5. ✅ Compara performance y selecciona el mejor
6. ✅ Guarda el modelo y preprocesador

**Salida esperada:**
- `best_model.joblib`: Modelo entrenado
- `preprocessor.joblib`: Pipeline de preprocesamiento
- Gráficos comparativos (matrices de confusión, curvas ROC)

### 3. Probar Módulos Individuales

```bash
# Probar carga de datos
python -m mlops_pipeline.src.cargar_datos

# Probar validación
python -m mlops_pipeline.src.data_validation

# Probar ingeniería de características
python -m mlops_pipeline.src.ft_engineering
```

### 4. Desplegar la API REST

```bash
python -m mlops_pipeline.src.model_deploy
```

La API estará disponible en:
- **URL Base**: http://localhost:8000
- **Documentación Interactiva**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

#### Endpoints Disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Información de la API |
| `/health` | GET | Estado de salud del servicio |
| `/predict` | POST | Predicción para una transacción |
| `/predict/batch` | POST | Predicciones por lote |
| `/model/info` | GET | Información del modelo |

#### Ejemplo de Uso (cURL)

```bash
# Predicción individual
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 9000.60,
    "oldbalanceOrg": 170136.0,
    "newbalanceOrg": 161136.0,
    "type": "TRANSFER"
  }'
```

#### Ejemplo de Uso (Python)

```python
import requests

url = "http://localhost:8000/predict"
transaction = {
    "amount": 9000.60,
    "oldbalanceOrg": 170136.0,
    "newbalanceOrg": 161136.0,
    "type": "TRANSFER"
}

response = requests.post(url, json=transaction)
print(response.json())
# Output: {"index": 0, "is_fraud": 0, "fraud_probability": 0.0234, "risk_level": "Bajo", ...}
```

### 5. Lanzar el Dashboard de Monitoreo

```bash
streamlit run mlops_pipeline/src/model_monitoring.py
```

El dashboard abrirá automáticamente en el navegador (http://localhost:8501).

**Funcionalidades:**
- 📊 Comparación de distribuciones (baseline vs producción)
- 🔍 Test estadísticos de drift (KS para numéricas, Chi² para categóricas)
- 📈 Visualizaciones interactivas
- ⚠️ Alertas automáticas de drift
- 💡 Recomendaciones de re-entrenamiento

---

## 📊 Hallazgos del EDA

### 1. Desbalanceo de Clases

- **No Fraude**: ~99%
- **Fraude**: ~1%
- **Ratio**: 1:100

**Acción tomada**: Aplicación de `RandomUnderSampler` y `class_weight='balanced'`

### 2. Variables Numéricas

| Variable | Media | Mediana | Skewness | Outliers |
|----------|-------|---------|----------|----------|
| `amount` | 179,862 | 74,871 | 2.45 | ⚠️ Alto |
| `oldbalanceOrg` | 833,883 | 14,208 | 5.12 | ⚠️ Alto |
| `newbalanceOrg` | 855,114 | 0 | 4.98 | ⚠️ Alto |

**Observaciones:**
- Distribuciones altamente asimétricas (right-skewed)
- Presencia significativa de outliers
- Se aplicó **StandardScaler** para normalización

### 3. Tipo de Transacción

| Tipo | % del Total | % de Fraude |
|------|-------------|-------------|
| CASH_OUT | 35% | 🔴 Alto |
| PAYMENT | 34% | 🟢 Bajo |
| CASH_IN | 22% | 🟢 Muy Bajo |
| TRANSFER | 8% | 🔴 Alto |
| DEBIT | 1% | 🟢 Bajo |

**Conclusión**: `CASH_OUT` y `TRANSFER` son indicadores fuertes de fraude

### 4. Reglas de Validación Identificadas

1. ✅ `amount >= 0`
2. ✅ `type` ∈ {CASH_IN, CASH_OUT, DEBIT, PAYMENT, TRANSFER}
3. ✅ `isFraud` ∈ {0, 1}
4. ✅ Balances no negativos

### 5. Features Derivados Creados

| Feature | Fórmula | Propósito |
|---------|---------|-----------|
| `errorBalanceOrg` | `oldbalanceOrg - newbalanceOrg - amount` | Detecta inconsistencias |
| `transactionRatio` | `amount / (oldbalanceOrg + 1)` | Identifica transacciones desproporcionadas |
| `zeroBalanceAfter` | `1 if newbalanceOrg == 0 else 0` | Marca cuentas vaciadas |

---

## 🤖 Modelos y Performance

### Modelos Entrenados

1. **Logistic Regression**
   - Baseline simple y rápido
   - Interpretable

2. **Random Forest**
   - Manejo automático de no-linealidades
   - Feature importance

3. **XGBoost**
   - Estado del arte en datos tabulares
   - Optimización de gradiente

### Métricas de Evaluación

Dado el desbalanceo, se priorizan:
- **ROC-AUC**: Métrica principal de comparación
- **Recall**: Minimizar fraudes no detectados (falsos negativos)
- **Precision**: Reducir falsos positivos
- **F1-Score**: Balance entre precision y recall

### Resultados Esperados

| Modelo | ROC-AUC | F1-Score | Recall | Precision |
|--------|---------|----------|--------|-----------|
| Logistic Regression | ~0.85 | ~0.75 | ~0.72 | ~0.78 |
| Random Forest | ~0.92 | ~0.85 | ~0.83 | ~0.87 |
| **XGBoost** | **~0.95** | **~0.89** | **~0.88** | **~0.91** |

*Nota: Los valores exactos dependen del dataset y semilla aleatoria*

### Selección del Modelo

El modelo con el **mayor ROC-AUC** se guarda automáticamente como `best_model.joblib`.

---

## 🌐 API REST

### Arquitectura de la API

- **Framework**: FastAPI (alta performance, validación automática)
- **Validación**: Pydantic models
- **Documentación**: Auto-generada (OpenAPI/Swagger)

### Modelos de Datos (Schemas)

```python
class Transaction(BaseModel):
    amount: float
    oldbalanceOrg: float
    newbalanceOrg: float
    type: str  # CASH_IN, CASH_OUT, DEBIT, PAYMENT, TRANSFER

class PredictionResponse(BaseModel):
    index: int
    is_fraud: int  # 0 o 1
    fraud_probability: float  # 0.0 - 1.0
    risk_level: str  # "Bajo", "Medio", "Alto"
    timestamp: str
```

### Ejemplo de Respuesta

```json
{
  "index": 0,
  "is_fraud": 1,
  "fraud_probability": 0.8745,
  "risk_level": "Alto",
  "timestamp": "2025-11-09T10:30:45.123456"
}
```

### Escalabilidad

- **Procesamiento por lotes**: Endpoint `/predict/batch` para múltiples transacciones
- **Async/Await**: Soporte para alta concurrencia
- **Caching**: Posibilidad de agregar Redis para caché de predicciones

---

## 📈 Dashboard de Monitoreo

### Funcionalidades del Dashboard

1. **Carga de Datos**
   - Upload de CSV con datos de producción
   - Comparación automática con baseline

2. **Detección de Drift**
   - **Variables Numéricas**: Test de Kolmogorov-Smirnov
   - **Variables Categóricas**: Test de Chi-Cuadrado

3. **Visualizaciones**
   - Gráficos KDE comparativos
   - Heatmaps de frecuencias
   - Tablas de contingencia

4. **Alertas Automáticas**
   - 🟢 Verde: Sin drift detectado
   - 🔴 Rojo: Drift significativo (requiere acción)

5. **Recomendaciones**
   - Sugerencias de re-entrenamiento
   - Investigación de causas
   - Configuración de alertas

### Interpretación de Resultados

| P-Value | Interpretación | Acción |
|---------|----------------|--------|
| p > 0.05 | No hay drift | ✅ Continuar monitoreando |
| p < 0.05 | **Drift detectado** | ⚠️ Investigar y considerar re-entrenamiento |
| p < 0.01 | Drift severo | 🚨 Re-entrenar urgentemente |

---

## 🐳 Docker

### Construcción de la Imagen

```bash
docker build -t fraud-detection-api .
```

### Ejecución del Contenedor

```bash
docker run -d \
  --name fraud-api \
  -p 8000:8000 \
  -v $(pwd)/best_model.joblib:/app/best_model.joblib \
  -v $(pwd)/preprocessor.joblib:/app/preprocessor.joblib \
  fraud-detection-api
```

### Verificar Estado

```bash
# Logs
docker logs fraud-api

# Health check
curl http://localhost:8000/health
```

### Docker Compose (Opcional)

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./best_model.joblib:/app/best_model.joblib
      - ./preprocessor.joblib:/app/preprocessor.joblib
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
```

Ejecutar:
```bash
docker-compose up -d
```

---

## 📁 Ejemplos de Uso

En la carpeta `examples/` encontrarás scripts completos que demuestran cómo usar el proyecto:

### 1. Uso de la API REST

```bash
python examples/api_usage_example.py
```

Este script muestra:
- ✅ Cómo verificar el estado de la API
- ✅ Cómo hacer predicciones individuales
- ✅ Cómo hacer predicciones por lote
- ✅ Ejemplos de transacciones normales y sospechosas

### 2. Uso Programático del Pipeline

```bash
python examples/pipeline_usage_example.py
```

Este script demuestra:
- ✅ Uso modular de cada componente
- ✅ Pipeline completo E2E
- ✅ Cómo personalizar el flujo

Consulta [`examples/README.md`](examples/README.md) para más detalles.

---

## 🧪 Testing

### Ejecutar Validaciones

```bash
# Validar carga de datos
python -m mlops_pipeline.src.cargar_datos

# Validar pipeline completo
python -m mlops_pipeline.src.data_validation
```

### Test de API

```bash
# Health check
curl http://localhost:8000/health

# Predicción de prueba
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"amount": 5000, "oldbalanceOrg": 10000, "newbalanceOrg": 5000, "type": "TRANSFER"}'
```

---

## 📝 Próximos Pasos y Mejoras

### Corto Plazo
- [ ] Implementar CI/CD con GitHub Actions
- [ ] Agregar tests unitarios (pytest)
- [ ] Configurar logging centralizado

### Mediano Plazo
- [ ] Optimización de hiperparámetros (Optuna, GridSearch)
- [ ] Feature selection automático (SHAP values)
- [ ] Versionado de modelos (MLflow, DVC)

### Largo Plazo
- [ ] Despliegue en cloud (AWS, Azure, GCP)
- [ ] Auto-retraining periódico
- [ ] Monitoreo de performance en producción (A/B testing)

---

## 👥 Contribuciones

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 📞 Contacto

**Proyecto desarrollado como parte del curso de MLOps**

- 📧 Email: [tu-email@example.com](mailto:tu-email@example.com)
- 🔗 LinkedIn: [Tu Perfil](https://linkedin.com/in/tu-perfil)
- 🐙 GitHub: [@tu-usuario](https://github.com/tu-usuario)

---

## 🙏 Agradecimientos

- Dataset: [Kaggle - Financial Fraud Detection](https://www.kaggle.com/)
- Frameworks: FastAPI, Streamlit, Scikit-learn, XGBoost
- Comunidad: Stack Overflow, Medium, GitHub

---

<div align="center">
  <p><strong>⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!</strong></p>
  <p>Hecho con ❤️ y ☕</p>
</div>

---

"Prueba SonarCloud"
