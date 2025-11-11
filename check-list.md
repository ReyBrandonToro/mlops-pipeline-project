¿Existe un archivo requirements.txt con las dependencias necesarias?

¿Se configuró un entorno virtual (venv, conda, etc.) y está documentado su uso?

Análisis de datos (0.7). Por cada ítem faltante se descuentan 0.2 hasta llegar a 0.0.
¿Se presenta una descripción general del dataset?

¿Se identifican y clasifican correctamente los tipos de variables (categóricas, numéricas, ordinales, etc.)?

¿Se revisan los valores nulos?

¿Se unifica la representación de los valores nulos?

¿Se eliminan variables irrelevantes?

¿Se convierten los datos a sus tipos correctos?

¿Se corrigen inconsistencias en los datos?

¿Se ejecuta describe() después de ajustar los tipos de datos?

¿Se incluyen histogramas y boxplots para variables numéricas?

¿Se usan countplot, value_counts() y tablas pivote para variables categóricas?

¿Se describen medidas estadísticas: media, mediana, moda, rango, IQR, varianza, desviación estándar, skewness, kurtosis?

¿Se identifica el tipo de distribución de las variables?

¿Se analizan relaciones entre variables y la variable objetivo?

¿Se incluyen gráficos y tablas relevantes?

¿Se revisan relaciones entre múltiples variables?

¿Se incluyen pairplots, matrices de correlación, gráficos de dispersión y uso de hue?

¿Se identifican reglas de validación de datos?

¿Se sugieren atributos derivados o calculados?

Ingeniería de Características (ft_engineering.py) (0.5). Por cada ítem faltante se descuentan 0.2 hasta llegar a 0.0.
¿El script genera correctamente los features a partir del dataset base?

¿Se documenta claramente el flujo de transformación de datos?

¿Se crean pipelines para procesamiento (e.g., Pipeline de sklearn)?

¿Se separan correctamente los conjuntos de entrenamiento y evaluación?

¿Se retorna un dataset limpio y listo para modelado?

¿Se incluyen transformaciones como escalado, codificación, imputación, etc.?

¿Se documentan las decisiones tomadas en la ingeniería de características?

Entrenamiento y Evaluación de Modelos (model_training_evaluation.py). (1.0) Por cada ítem faltante se descuentan 0.25 hasta llegar a 0.0.
¿Se entrenan múltiples modelos supervisados (e.g., RandomForest, XGBoost, LogisticRegression)?

¿Se utiliza una función build_model() para estructurar el entrenamiento repetible?

¿Se aplican técnicas de validación (e.g., cross-validation, train/test split)?

¿Se guarda el objeto del modelo seleccionado?

¿Se utiliza la función summarize_classification() para resumir métricas?

¿Se comparan modelos con métricas como accuracy, precision, recall, F1-score, ROC-AUC?

¿Se presentan gráficos comparativos (e.g., curvas ROC, matriz de confusión)?

¿Se justifica la selección del modelo final (performance, consistencia, escalabilidad)?

Data monitoring. (1.0) Por cada ítem faltante se descuentan 0.25 hasta llegar a 0.0.
¿Se calcula un test para medida del Drift?

¿Se implementa una interfaz funcional en Streamlit?

¿Se muestran gráficos comparativos entre distribución histórica vs actual?

¿Se incluyen indicadores visuales de alerta (semáforo, barras de riesgo)?

¿Se activan alertas si se detectan desviaciones significativas?

Despliegue. (1.0) Por cada ítem faltante se descuentan 0.25 hasta llegar a 0.0.
¿Se utiliza un framework adecuado (FastAPI, Flask)?

¿Se define el endpoint /predict para recibir datos?

¿Se acepta entrada en formato JSON y/o CSV?

¿Se soporta predicción por lotes (múltiples registros)?

¿Se retorna la predicción en formato estructurado (JSON, lista, etc.)?

¿Se incluye un Dockerfile funcional con instrucciones claras?