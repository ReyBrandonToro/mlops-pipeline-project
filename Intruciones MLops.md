PROYECTO FINAL - MACHINE LEARNING
Docente: Juan Sebastián Parra Sánchez

Fecha de entrega: 10 de noviembre de 2025, 23:59

Contexto del proyecto y rol del estudiante:
Para este ejercicio vas a buscar una base de datos de tu interés con el fin de generar un modelo supervisado predictivo. Debes generar una comprensión del negocio y cada estudiante tendrá una base de datos diferente.

La empresa opera bajo un esquema estructurado de proyectos, en el cual cada iniciativa debe seguir una arquitectura de carpetas estrictamente definida. Esta estructura no puede ser modificada, ya que los procesos de despliegue a producción están automatizados a través de pipelines de validación en Jenkins. Cualquier alteración en la organización de carpetas podría generar retrasos significativos en el paso a producción.

Como primer paso, se te solicita crear un repositorio público en GitHub que contenga el desarrollo del proyecto y compartirlo al usuario juanseparracourses. El enlace a este repositorio será el entregable final que compartirás al concluir el proyecto.

Entregable final:
Repositorio en GitHub

El repositorio debe tener esta estructura de carpetas y tres ramas: developer, certification, master.

text
mlops_pipeline/
└── src/
    ├── Cargar_datos.ipynb
    ├── comprension_eda.ipynb
    ├── ft_engineering.py
    ├── model_training_evaluation.py
    ├── model_deploy.py
    └── model_monitoring.py
Base_de_datos.csv
requirements.txt
.gitignore
setup.bat
readme.md
PUNTO 1 (Se entrega el 29.10.2025)
Generar la estructura de carpetas tal y como se indicó para la entrega. Esta estructura debe estar en el repositorio creado anteriormente y no debe cambiarse.

Clona tu repositorio

Genera un archivo de requirements.txt

Configura un entorno virtual.

Cargar_datos.ipynb: Este notebook no se utiliza normalmente en el proceso de creación de un modelo dado que nuestra data deberá estar en el DWH o Database de la empresa como resultado de un proceso diferente que materialice nuestra información en una tabla. Sin embargo, para este caso, se utiliza un dataset no productivo de ejemplo en .csv.

Comprensión_eda.ipynb: Análisis experimental y exploratorio de datos. En este notebook se debe realizar el análisis exploratorio de la base de datos, teniendo en cuenta:

Exploración inicial de datos
Descripción general de los datos. Caracterización de los datos: categóricos, numéricos, ordinales, nominales, dicotómicos, politómicos. Revisión de nulos.

Unificar la forma como se representan los valores Nulos.

Eliminación de variables irrelevantes.

Convertir los datos en su tipo correcto (numéricos, categóricos, booleanos, fechas, etc) y corrección de los datos si es necesario, para cada columna tenga un tipo de dato uniforme.

Exploración de datos y descripción (EDA)
Análisis univariable. Se recomienda hacer un describe() una vez se hayan ajustado los tipos de datos. Se recomienda para las variables numéricas: histograma para distribución, boxplot, tablas pivote. Para las variables categóricas: countplot, tablas pivote, value_counts() Descripción estadística (dependiendo del tipo de dato): por ejemplo para los numéricos: tendencia Central (media, mediana, moda, max, min, etc), medidas de dispersión (Rango, IQR, cuartiles, varianza, desviación estándar, skewness y kurtosis). Tipo de distribución (gaussiana, uniforme, logarítmica, etc.)

Análisis bivariable. Se recomienda generar gráficos y tablas con respecto a la variable objetivo y comentar.

Análisis multivariable. Revisar relaciones entre variables. Se puede incluir un pairplot(), tablas cruzadas, matriz de correlación, gráficos de dispersión entre variables numéricas, gráficos utilizando el parámetro hue para las variables categóricas. El análisis debe contener: compresión detallada de las características y el esquema de datos. Muchos comentarios, interpretaciones, análisis de lo que se encuentra, analice los datos para crear las reglas de validación de los datos que serán usadas en otra etapa del proyecto. Identificar las transformaciones que tal vez se puedan aplicar. Identificar atributos adicionales (derivados, calculados) que pueden ser útiles.

PARA LA ENTREGA FINAL (10.11.2025)
Detalle de avance recomendado 1
Realizar el proceso de ingeniería de características.

Empezar a entrenar los primeros modelos.

Realizar la evaluación de los modelos supervisados, seleccionando el de mejor performance.

ft_engineering.py: Crea la primera componente de nuestro flujo de creación de modelos operativos, del cual se generan los features y se retorna el dataset con el cuál se entrenarán los modelos. Incluye el resultado de: resultan los conjuntos de datos de entrenamiento y evaluación. Se solicita crear pipelines como los siguientes.

model_training_evaluation.py: Se entrenan y evalúan diferentes modelos. De este debe resultar el objeto del modelo seleccionado como el mejor (model performance, consistency, scalability)

Se deben utilizar funciones como: summarize_classification y build_model para procesos que se hagan de forma repetida.

Utilizar gráficos comparativos para los modelos principales. Tabla resumen con el apartado de evaluación.

Detalle de avance recomendado 2
Realizar procesos de monitoreo y detección de data drift.

Desarrollar una aplicación en streamlit.

Generar el archivo REAMDE.md para tu ejercicio, documentando el caso de negocio y los principales hallazgos y proceso

model_monitoring.py: Crea el trabajo de monitoreo que trae en una tabla los datos junto con los pronósticos entregados y los utiliza, con una periodicidad definida, para muestrear y obtener métricas que permitan detectar cambios en la población que puedan afectar el desempeño del modelo. Medida del Datadrift.

Algunos elementos:

Muestreo periódico de los datos para análisis estadístico. Cálculo de métricas de data drift, como:

Kolmogorov-Smirnov (KS test)

Population Stability Index (PSI)

Jensen-Shannon divergence

Chi-cuadrado para variables categóricas

Aplicación en Streamlit
Visualización de métricas

Gráficos de comparación entre distribución histórica vs actual.

Tablas con métricas de drift por variable.

Indicadores visuales de alerta (semáforo, barras de riesgo).

Análisis temporal

Evolución del drift a lo largo del tiempo.

Detección de tendencias o cambios abruptos.

Recomendaciones

Mensajes automáticos si se supera un umbral crítico.

Sugerencias de retraining o revisión de variables.

Generación de alertas si se detectan desviaciones significativas que puedan comprometer la precisión del modelo.

Detalle de avance (para el trabajo final)
Disponibilizar mediante una API el modelo creado.

Crear una imagen que contenga las librerías y el código para una app.

model_deploy.py: Se toma el mejor modelo desplegado y una imagen que contenga las librerías y el código para una app que permita disponibilizar dicho objeto y despliega el modelo en un endpoint que puede utilizarse para predicciones (por batch).

Este script es el núcleo del despliegue. Sus responsabilidades incluyen:

Carga del modelo entrenado (por ejemplo, desde un archivo .pkl o .joblib)

Definición de la lógica de predicción: recibe datos, aplica transformaciones necesarias y retorna resultados.

Exposición del modelo como servicio: usando frameworks como FastAPI o Flask, se define un endpoint /predict que acepta datos en formato JSON o CSV y retorna predicciones.

Soporte para predicción por lotes: permite enviar múltiples registros en una sola solicitud.

Imagen Docker
Se construye una imagen que contiene:

El código fuente.

Las dependencias necesarias (requirements.txt)

El servidor de aplicación (por ejemplo, Uvicorn si se usa FastAPI)

Archivos de configuración (Dockerfile, .dockerignore)