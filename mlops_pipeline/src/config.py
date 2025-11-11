"""
Archivo de configuración central del proyecto MLOps.
Contiene todas las constantes y parámetros del pipeline.
"""

# ==================== RUTAS DE ARCHIVOS ====================
DATA_PATH = "financial_fraud_dataset.csv"
MODEL_PATH = "best_model.joblib"
PREPROCESSOR_PATH = "preprocessor.joblib"

# ==================== VARIABLES DEL DATASET ====================
TARGET_VARIABLE = "is_fraud"
IRRELEVANT_COLS = ["transaction_id", "timestamp", "customer_id"]

# Columnas numéricas (basadas en el dataset real)
NUMERICAL_COLS = ["amount", "customer_age", "previous_transactions"]

# Columnas categóricas
CATEGORICAL_COLS = ["merchant_category", "customer_location", "device_type"]

# Valores permitidos para las columnas categóricas (se determinarán dinámicamente)
ALLOWED_TYPES = []  # No aplicable para este dataset

# ==================== PARÁMETROS DE MODELADO ====================
TEST_SIZE = 0.2
RANDOM_STATE = 42

# ==================== UMBRALES DE MONITOREO ====================
KS_THRESHOLD = 0.05  # Umbral para el test Kolmogorov-Smirnov
CHI2_THRESHOLD = 0.05  # Umbral para el test Chi-cuadrado

# ==================== CONFIGURACIÓN DE API ====================
API_TITLE = "API de Detección de Fraude Financiero"
API_VERSION = "1.0"
API_PORT = 8000
