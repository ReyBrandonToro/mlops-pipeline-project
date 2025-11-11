# 📚 Ejemplos de Uso

Esta carpeta contiene scripts de ejemplo que demuestran cómo usar el proyecto MLOps de Detección de Fraude.

## 🚀 Inicio Rápido

### 1. Asegúrate de tener el entorno activado

```bash
# Windows
mlops_pipeline-venv\Scripts\activate

# Linux/Mac
source mlops_pipeline-venv/bin/activate
```

### 2. Asegúrate de tener la API corriendo (para ejemplos de API)

```bash
python main.py
# Selecciona la opción 5 (Iniciar API REST)
```

## 📋 Ejemplos Disponibles

### 1. `api_usage_example.py` - Uso de la API REST

Demuestra cómo hacer requests a la API de predicción.

**Qué hace:**
- ✅ Verifica el estado de la API (`/health`)
- ✅ Realiza predicciones individuales (`/predict`)
- ✅ Realiza predicciones por lote (`/predict/batch`)
- ✅ Muestra ejemplos de transacciones normales y sospechosas

**Ejecutar:**
```bash
cd examples
python api_usage_example.py
```

**Ejemplo de código:**
```python
import requests

# Predicción individual
transaction = {
    "amount": 9000.60,
    "oldbalanceOrg": 170136.0,
    "newbalanceOrg": 161136.0,
    "type": "TRANSFER"
}

response = requests.post(
    "http://localhost:8000/predict",
    json=transaction
)

result = response.json()
print(f"Es fraude: {result['is_fraud']}")
print(f"Probabilidad: {result['fraud_probability']:.2%}")
```

---

### 2. `pipeline_usage_example.py` - Uso Programático del Pipeline

Muestra cómo usar las clases del pipeline directamente en tu código.

**Qué hace:**
- ✅ Ejemplo de carga de datos con `DataLoader`
- ✅ Ejemplo de validación con `DataValidator`
- ✅ Ejemplo de ingeniería de características con `FeatureEngineer`
- ✅ Ejemplo de entrenamiento completo con `ModelTrainer`
- ✅ Ejemplo de pipeline personalizado paso a paso

**Ejecutar:**
```bash
cd examples
python pipeline_usage_example.py
```

**Ejemplo de código:**
```python
from mlops_pipeline.src.cargar_datos import DataLoader
from mlops_pipeline.src.data_validation import DataValidator
from mlops_pipeline.src.ft_engineering import FeatureEngineer

# Cargar datos
loader = DataLoader()
df = loader.load_data()

# Validar
validator = DataValidator()
is_valid = validator.validate_data(df)

# Procesar
engineer = FeatureEngineer()
X_train, X_test, y_train, y_test = engineer.process(df)
```

---

## 🔧 Casos de Uso Comunes

### Integrar la API en tu Aplicación

```python
import requests

class FraudDetectionClient:
    def __init__(self, api_url="http://localhost:8000"):
        self.api_url = api_url
    
    def check_transaction(self, amount, old_balance, new_balance, tx_type):
        transaction = {
            "amount": amount,
            "oldbalanceOrg": old_balance,
            "newbalanceOrg": new_balance,
            "type": tx_type
        }
        
        response = requests.post(
            f"{self.api_url}/predict",
            json=transaction
        )
        
        return response.json()

# Uso
client = FraudDetectionClient()
result = client.check_transaction(
    amount=5000.0,
    old_balance=10000.0,
    new_balance=5000.0,
    tx_type="TRANSFER"
)

if result['is_fraud'] == 1:
    print("⚠️ ALERTA: Transacción sospechosa detectada!")
```

### Entrenar tu Propio Modelo Personalizado

```python
from mlops_pipeline.src.cargar_datos import DataLoader
from mlops_pipeline.src.data_validation import DataValidator
from mlops_pipeline.src.ft_engineering import FeatureEngineer
from sklearn.ensemble import GradientBoostingClassifier
import joblib

# Preparar datos
loader = DataLoader()
df = loader.load_data()

validator = DataValidator()
validator.validate_data(df)

engineer = FeatureEngineer()
X_train, X_test, y_train, y_test = engineer.process(df)

# Entrenar modelo personalizado
model = GradientBoostingClassifier(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=5
)

model.fit(X_train, y_train)

# Guardar
joblib.dump(model, "my_custom_model.joblib")
```

---

## 📊 Ejemplos de Transacciones

### Transacción Normal (Bajo Riesgo)

```json
{
    "amount": 500.00,
    "oldbalanceOrg": 10000.00,
    "newbalanceOrg": 9500.00,
    "type": "PAYMENT"
}
```

### Transacción Sospechosa (Alto Riesgo)

```json
{
    "amount": 250000.00,
    "oldbalanceOrg": 300000.00,
    "newbalanceOrg": 0.00,
    "type": "TRANSFER"
}
```

### Transacción de Riesgo Medio

```json
{
    "amount": 50000.00,
    "oldbalanceOrg": 100000.00,
    "newbalanceOrg": 50000.00,
    "type": "CASH_OUT"
}
```

---

## 🧪 Testing de la API

### Con cURL (Línea de Comandos)

```bash
# Health check
curl http://localhost:8000/health

# Predicción individual
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 5000.0,
    "oldbalanceOrg": 20000.0,
    "newbalanceOrg": 15000.0,
    "type": "TRANSFER"
  }'
```

### Con Postman

1. Importa la colección desde la documentación interactiva
2. Visita: http://localhost:8000/docs
3. Usa el botón "Download OpenAPI Spec"

---

## 💡 Tips y Mejores Prácticas

### 1. Manejo de Errores en Producción

```python
import requests
from requests.exceptions import RequestException

def safe_predict(transaction):
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json=transaction,
            timeout=5  # Timeout de 5 segundos
        )
        response.raise_for_status()
        return response.json()
        
    except RequestException as e:
        print(f"Error en la predicción: {e}")
        return None
```

### 2. Batch Processing para Alto Volumen

```python
def process_large_dataset(transactions, batch_size=100):
    results = []
    
    for i in range(0, len(transactions), batch_size):
        batch = transactions[i:i+batch_size]
        
        response = requests.post(
            "http://localhost:8000/predict/batch",
            json={"transactions": batch}
        )
        
        if response.status_code == 200:
            results.extend(response.json()['predictions'])
    
    return results
```

### 3. Logging y Monitoreo

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def predict_with_logging(transaction):
    logger.info(f"Procesando transacción: {transaction}")
    
    response = requests.post(
        "http://localhost:8000/predict",
        json=transaction
    )
    
    result = response.json()
    
    if result['is_fraud'] == 1:
        logger.warning(f"FRAUDE DETECTADO: {transaction}")
    
    return result
```

---

## 🆘 Solución de Problemas

### Error: "Connection refused"

**Problema:** La API no está corriendo.

**Solución:**
```bash
python main.py
# Selecciona la opción 5
```

### Error: "Model not loaded"

**Problema:** No se han entrenado los modelos.

**Solución:**
```bash
python main.py
# Selecciona la opción 1 (Pipeline completo)
```

### Error: "Invalid transaction type"

**Problema:** El tipo de transacción no es válido.

**Solución:** Usa solo estos tipos:
- `CASH_IN`
- `CASH_OUT`
- `DEBIT`
- `PAYMENT`
- `TRANSFER`

---

## 📖 Más Recursos

- 📚 Documentación completa: `../README.md`
- 🔗 API Docs interactiva: http://localhost:8000/docs
- 📊 EDA Notebook: `../mlops_pipeline/src/comprension_eda.ipynb`
- 🐳 Deployment: `../Dockerfile`

---

## 🤝 Contribuir

¿Tienes más ejemplos útiles? ¡Compártelos!

1. Crea un nuevo archivo en esta carpeta
2. Documéntalo adecuadamente
3. Actualiza este README

---

<div align="center">
  <p><strong>💡 ¿Necesitas ayuda? Revisa el README principal o abre un issue.</strong></p>
</div>
