# 🎨 Instrucciones para Ejecutar el Frontend Visual

## 📋 Descripción

Este documento describe cómo ejecutar el **Sistema de Detección de Fraude Financiero** con su interfaz visual desarrollada en **Streamlit**.

---

## 🚀 Pasos para Ejecutar

### 1️⃣ Ejecutar la API (Terminal 1)

Primero, debes iniciar el servidor FastAPI que proporciona las predicciones del modelo:

```bash
# Activar entorno virtual
.\mlops_pipeline-venv\Scripts\activate

# Ejecutar API
python -m mlops_pipeline.src.model_deploy
```

**Salida Esperada:**
```
INFO:     Started server process [...]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

✅ **Verificación:** Abre http://localhost:8000/health en tu navegador - debe mostrar `{"status": "healthy"}`

---

### 2️⃣ Ejecutar el Frontend (Terminal 2)

En una **nueva terminal**, ejecuta la aplicación Streamlit:

```bash
# Activar entorno virtual (si no está activo)
.\mlops_pipeline-venv\Scripts\activate

# Ejecutar frontend de Streamlit
streamlit run mlops_pipeline\src\app_frontend.py
```

**Salida Esperada:**
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

✅ **Verificación:** Tu navegador debería abrirse automáticamente en http://localhost:8501

---

## 🖥️ Uso de la Interfaz

### Panel de Información del Modelo

En la parte superior verás:
- **Mejor Modelo:** LogisticRegression
- **ROC-AUC Score:** 0.5776
- **Recall (Sensibilidad):** 65.79%
- **Accuracy:** 51.20%

### Visualizaciones

- **Matriz de Confusión:** Muestra cómo el modelo clasifica las transacciones
- **Curvas ROC:** Comparación del rendimiento de los 3 modelos entrenados

### Formulario de Predicción

**Campos del Formulario:**

1. **💰 Monto de la Transacción ($):** Cantidad de dinero (0.0 - 1,000,000.0)
   - Ejemplo: 250.50

2. **🏪 Categoría del Comerciante:** Tipo de negocio
   - Opciones: retail, online, grocery, electronics, jewelry, restaurant, other
   - Ejemplo: retail

3. **👤 Edad del Cliente:** Edad de quien realiza la transacción (18 - 100)
   - Ejemplo: 35

4. **📍 Ubicación del Cliente:** Zona geográfica
   - Opciones: urban, suburban, rural
   - Ejemplo: urban

5. **📱 Tipo de Dispositivo:** Dispositivo usado
   - Opciones: mobile, desktop, tablet
   - Ejemplo: mobile

6. **📊 Transacciones Previas:** Historial del cliente (0 - 1000)
   - Ejemplo: 15

### Interpretación de Resultados

Después de presionar **"🔍 Analizar Transacción"**, verás:

#### ✅ Transacción Legítima
```
✅ Transacción Legítima
Probabilidad de Fraude: 15.34%
Nivel de Riesgo: Low
```

#### 🚨 Transacción Fraudulenta
```
🚨 ¡ALERTA: TRANSACCIÓN FRAUDULENTA!
Probabilidad de Fraude: 87.45%
Nivel de Riesgo: High

⚠️ Acciones Recomendadas:
- Bloquear la transacción inmediatamente
- Notificar al cliente
- Revisar actividad reciente de la cuenta
- Considerar congelamiento temporal de la cuenta
```

---

## 💡 Ejemplos de Transacciones

### Transacción Normal
```json
{
  "amount": 250.50,
  "merchant_category": "retail",
  "customer_age": 35,
  "customer_location": "urban",
  "device_type": "mobile",
  "previous_transactions": 15
}
```

### Transacción Sospechosa
```json
{
  "amount": 5000.00,
  "merchant_category": "jewelry",
  "customer_age": 22,
  "customer_location": "rural",
  "device_type": "desktop",
  "previous_transactions": 2
}
```

### Transacción de Alto Riesgo
```json
{
  "amount": 8500.00,
  "merchant_category": "electronics",
  "customer_age": 19,
  "customer_location": "rural",
  "device_type": "tablet",
  "previous_transactions": 0
}
```

---

## 📊 Sidebar (Barra Lateral)

### Estado de la API
- ✅ **Conectado:** Muestra información del modelo en formato JSON
- ❌ **Desconectado:** Indica que la API no está disponible

### Instrucciones Rápidas
Comandos para ejecutar ambos componentes del sistema

### Enlaces Útiles
- [Documentación API](http://localhost:8000/docs) - Swagger UI interactivo
- [ReDoc](http://localhost:8000/redoc) - Documentación alternativa
- [Health Check](http://localhost:8000/health) - Estado de la API

---

## ⚠️ Resolución de Problemas

### Problema: API Desconectada

**Síntoma:** El frontend muestra "❌ API Desconectada"

**Solución:**
1. Verifica que la API esté corriendo en el Terminal 1
2. Visita http://localhost:8000/health en el navegador
3. Si no responde, reinicia la API:
   ```bash
   python -m mlops_pipeline.src.model_deploy
   ```

### Problema: Streamlit no se instala

**Síntoma:** Error al ejecutar `streamlit run`

**Solución:**
```bash
# Reinstalar Streamlit
pip install streamlit --no-deps
pip install pydeck toml altair
```

### Problema: Imágenes no aparecen

**Síntoma:** Las visualizaciones no se muestran

**Solución:**
Verifica que existan los archivos:
- `c:\Proyecto\confusion_matrix_logisticregression.png`
- `c:\Proyecto\roc_curves_comparison.png`

Si faltan, ejecuta nuevamente el entrenamiento:
```bash
python run_training.py
```

### Problema: Error de conexión

**Síntoma:** "Connection refused" o "Error en la predicción"

**Solución:**
1. Confirma que la API esté corriendo en `http://localhost:8000`
2. Presiona el botón **"🔄 Actualizar Estado"** en el frontend
3. Verifica el firewall de Windows no esté bloqueando el puerto 8000

---

## 🎯 Características Destacadas

### 🔄 Actualización en Tiempo Real
- Estado de la API se actualiza con el botón "🔄 Actualizar Estado"
- Los resultados se muestran inmediatamente después del análisis

### 📊 Visualización de Métricas
- Métricas del modelo actualizadas (ROC-AUC, Recall, Accuracy)
- Gráficas de rendimiento (Matriz de Confusión y Curvas ROC)

### 🎨 Interfaz Intuitiva
- Diseño claro con colores según el nivel de riesgo
- Formulario fácil de usar con valores por defecto
- Resultados detallados con recomendaciones

### 📱 Responsive
- Se adapta a diferentes tamaños de pantalla
- Layout en columnas para mejor visualización

---

## 🔗 Arquitectura del Sistema

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│  Streamlit      │         │   FastAPI        │         │  Modelo ML      │
│  Frontend       │ ─HTTP─→ │   API            │ ────→   │  (LogReg)       │
│  (Puerto 8501)  │         │   (Puerto 8000)  │         │  best_model.pkl │
└─────────────────┘         └──────────────────┘         └─────────────────┘
      ↑                              ↑
      │                              │
   Usuario                      Preprocessor
   Interacción                  + Features
```

---

## 📚 Más Información

- **Documentación Completa:** `EJECUCION_COMPLETA.md`
- **Detalles de Ejecución:** `EJECUCION_EXITOSA.md`
- **Resumen Visual:** `RESUMEN_VISUAL.txt`
- **Guía Rápida:** `QUICKSTART.md`

---

## ✅ Checklist de Verificación

Antes de usar el sistema, confirma que:

- [ ] El entorno virtual está activado
- [ ] La API está corriendo en http://localhost:8000
- [ ] El frontend está corriendo en http://localhost:8501
- [ ] El navegador abrió automáticamente la aplicación
- [ ] El estado de la API muestra "✅ API Conectada"
- [ ] Las visualizaciones aparecen correctamente

---

## 🎓 Notas Adicionales

### Rendimiento del Modelo

- **ROC-AUC de 0.5776** indica un modelo mejor que el azar (0.5)
- **Recall de 65.79%** significa que detecta 2 de cada 3 fraudes
- **Accuracy de 51.20%** es razonable considerando el desbalance de clases

### Dataset Desbalanceado

El dataset tiene:
- **No Fraude:** 98.1% (9,813 transacciones)
- **Fraude:** 1.9% (187 transacciones)

Se aplicó **RandomUnderSampler** para balancear las clases durante el entrenamiento.

### Próximos Pasos

1. **Mejorar el modelo:** Probar técnicas adicionales de balanceo (SMOTE)
2. **Más features:** Crear variables derivadas más sofisticadas
3. **Monitoreo:** Implementar seguimiento de predicciones en producción
4. **A/B Testing:** Comparar versiones del modelo en producción

---

**Desarrollado con ❤️ para el curso de MLOps**

🛡️ Sistema de Detección de Fraude Financiero | MLOps Pipeline v1.0
