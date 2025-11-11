# ⚡ Guía Rápida - MLOps Pipeline

Esta es una guía de inicio rápido para poner el proyecto en marcha en **5 minutos**.

---

## 📋 Pre-requisitos

- [x] Python 3.10 o superior instalado
- [x] Git instalado (opcional)
- [x] Conexión a internet (para descargar dependencias)

---

## 🚀 Paso 1: Descargar el Proyecto

Si tienes Git:
```bash
git clone https://github.com/ReyBrandonToro/mlops-pipeline-project.git
cd mlops-pipeline-project
```

Si descargaste el ZIP:
```bash
cd c:\Proyecto
# O la ruta donde descomprimiste el proyecto
```

---

## 🔧 Paso 2: Configurar el Entorno

### Windows:
```batch
setup.bat
```

### Linux/Mac:
```bash
python -m venv mlops_pipeline-venv
source mlops_pipeline-venv/bin/activate
pip install -r requirements.txt
```

⏱️ **Tiempo estimado**: 2-3 minutos

---

## 🎯 Paso 3: Ejecutar el Menú Principal

```bash
python main.py
```

Verás un menú interactivo. **Selecciona la opción 1** para ejecutar el pipeline completo.

⏱️ **Tiempo estimado**: 2-5 minutos (dependiendo de tu hardware)

---

## ✅ ¡Listo! Ahora puedes:

### 🌐 Iniciar la API REST (Opción 5 del menú)

```bash
python main.py
# Selecciona: 5
```

La API estará en: http://localhost:8000/docs

### 📊 Ver el Dashboard de Monitoreo (Opción 6 del menú)

```bash
python main.py
# Selecciona: 6
```

### 🧪 Probar la API con un Ejemplo

```bash
python examples/api_usage_example.py
```

---

## 📝 Comandos Más Usados

```bash
# 1. Entrenar el modelo
python -m mlops_pipeline.src.model_training_evaluation

# 2. Iniciar API
python -m mlops_pipeline.src.model_deploy

# 3. Dashboard de monitoreo
streamlit run mlops_pipeline/src/model_monitoring.py

# 4. Notebook de EDA
jupyter lab mlops_pipeline/src/comprension_eda.ipynb
```

---

## 🐳 Opción con Docker

Si prefieres usar Docker:

```bash
# 1. Construir imagen
docker build -t fraud-detection-api .

# 2. Ejecutar contenedor
docker run -d -p 8000:8000 \
  -v ${PWD}/best_model.joblib:/app/best_model.joblib \
  -v ${PWD}/preprocessor.joblib:/app/preprocessor.joblib \
  fraud-detection-api

# O con Docker Compose
docker-compose up -d
```

---

## 🆘 Problemas Comunes

### ❌ "Dataset no encontrado"
**Solución**: Asegúrate de que `financial_fraud_dataset.csv` esté en la raíz del proyecto.

### ❌ "Modelo no encontrado"
**Solución**: Ejecuta primero el pipeline completo (opción 1 del menú o `python -m mlops_pipeline.src.model_training_evaluation`)

### ❌ "Port 8000 already in use"
**Solución**: Cambia el puerto en `mlops_pipeline/src/config.py` (`API_PORT = 8001`)

### ❌ "Module not found"
**Solución**: Asegúrate de estar en el directorio raíz del proyecto y con el entorno virtual activado.

---

## 📚 Más Ayuda

- **README Completo**: [`README.md`](README.md)
- **Ejemplos**: [`examples/README.md`](examples/README.md)
- **Comandos Útiles**: [`COMMANDS.txt`](COMMANDS.txt)
- **Documentación API**: http://localhost:8000/docs (cuando la API esté corriendo)

---

## 🎓 Próximos Pasos

1. ✅ Explora el notebook de EDA: `comprension_eda.ipynb`
2. ✅ Prueba la API con diferentes transacciones
3. ✅ Sube datos nuevos al dashboard de monitoreo
4. ✅ Personaliza los modelos y parámetros
5. ✅ Despliega en producción con Docker

---

<div align="center">
  <p><strong>🎉 ¡Felicidades! Ya tienes tu pipeline MLOps funcionando.</strong></p>
  <p>Si tienes dudas, revisa la documentación o abre un issue.</p>
</div>
