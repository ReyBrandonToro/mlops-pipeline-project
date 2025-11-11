"""
Módulo de despliegue del modelo con FastAPI.
Crea una API REST para servir predicciones del modelo de detección de fraude.
"""

import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List, Optional
import uvicorn
from datetime import datetime

try:
    from mlops_pipeline.src import config
except ImportError:
    from . import config


# ==================== MODELOS PYDANTIC ====================

class Transaction(BaseModel):
    """Modelo de datos para una transacción individual."""
    amount: float = Field(..., description="Monto de la transacción", ge=0)
    merchant_category: str = Field(..., description="Categoría del comerciante")
    customer_age: int = Field(..., description="Edad del cliente", ge=18, le=100)
    customer_location: str = Field(..., description="Ubicación del cliente")
    device_type: str = Field(..., description="Tipo de dispositivo usado")
    previous_transactions: int = Field(..., description="Número de transacciones previas", ge=0)
    
    class Config:
        schema_extra = {
            "example": {
                "amount": 250.50,
                "merchant_category": "retail",
                "customer_age": 35,
                "customer_location": "urban",
                "device_type": "mobile",
                "previous_transactions": 15
            }
        }


class TransactionBatch(BaseModel):
    """Modelo para predicciones por lotes."""
    transactions: List[Transaction]


class PredictionResponse(BaseModel):
    """Modelo de respuesta para una predicción."""
    index: int
    is_fraud: int
    fraud_probability: float
    risk_level: str
    timestamp: str


class BatchPredictionResponse(BaseModel):
    """Modelo de respuesta para predicciones por lotes."""
    predictions: List[PredictionResponse]
    total_transactions: int
    fraud_detected: int
    processing_time_ms: float


class HealthResponse(BaseModel):
    """Modelo de respuesta para el health check."""
    status: str
    model_loaded: bool
    preprocessor_loaded: bool
    api_version: str
    timestamp: str


# ==================== INICIALIZACIÓN DE LA API ====================

app = FastAPI(
    title=config.API_TITLE,
    version=config.API_VERSION,
    description="API para detección de fraude en transacciones financieras usando Machine Learning",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Variables globales para el modelo y preprocesador
model = None
preprocessor = None


@app.on_event("startup")
async def load_model_and_preprocessor():
    """
    Carga el modelo y el preprocesador al iniciar la aplicación.
    """
    global model, preprocessor
    
    try:
        print("🔄 Cargando modelo y preprocesador...")
        
        # Cargar preprocesador
        preprocessor = joblib.load(config.PREPROCESSOR_PATH)
        print(f"✓ Preprocesador cargado desde: {config.PREPROCESSOR_PATH}")
        
        # Cargar modelo
        model = joblib.load(config.MODEL_PATH)
        print(f"✓ Modelo cargado desde: {config.MODEL_PATH}")
        
        print("✅ API lista para servir predicciones")
        
    except FileNotFoundError as e:
        print(f"❌ Error: No se encontraron los archivos del modelo o preprocesador")
        print(f"   Asegúrate de entrenar el modelo primero ejecutando model_training_evaluation.py")
        print(f"   Detalle: {str(e)}")
    except Exception as e:
        print(f"❌ Error inesperado al cargar modelo: {str(e)}")


# ==================== ENDPOINTS ====================

@app.get("/", response_model=dict)
async def root():
    """
    Endpoint raíz - Información básica de la API.
    """
    return {
        "message": "API de Detección de Fraude Financiero",
        "version": config.API_VERSION,
        "endpoints": {
            "health": "/health",
            "predict_single": "/predict",
            "predict_batch": "/predict/batch",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Endpoint de health check - Verifica el estado de la API.
    """
    return HealthResponse(
        status="healthy" if (model is not None and preprocessor is not None) else "unhealthy",
        model_loaded=model is not None,
        preprocessor_loaded=preprocessor is not None,
        api_version=config.API_VERSION,
        timestamp=datetime.now().isoformat()
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict_single(transaction: Transaction):
    """
    Predice si una transacción individual es fraudulenta.
    
    Args:
        transaction: Objeto Transaction con los datos de la transacción.
    
    Returns:
        PredictionResponse: Predicción y probabilidad de fraude.
    """
    if model is None or preprocessor is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo no disponible. El servicio no está listo."
        )
    
    try:
        start_time = datetime.now()
        
        # Convertir a DataFrame
        df = pd.DataFrame([transaction.dict()])
        
        # Crear features derivados (igual que en ft_engineering.py)
        df['amount_per_transaction'] = df['amount'] / (df['previous_transactions'] + 1)
        df['age_group'] = pd.cut(df['customer_age'], 
                                 bins=[0, 25, 35, 50, 100], 
                                 labels=['young', 'adult', 'middle_age', 'senior'])
        df['age_group'] = df['age_group'].astype(str)
        amount_threshold = df['amount'].quantile(0.75)
        df['high_amount'] = (df['amount'] > amount_threshold).astype(int)
        
        # Preprocesar
        X_processed = preprocessor.transform(df)
        
        # Predecir
        prediction = int(model.predict(X_processed)[0])
        probability = float(model.predict_proba(X_processed)[0, 1])
        
        # Determinar nivel de riesgo
        if probability < 0.3:
            risk_level = "Bajo"
        elif probability < 0.7:
            risk_level = "Medio"
        else:
            risk_level = "Alto"
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return PredictionResponse(
            index=0,
            is_fraud=prediction,
            fraud_probability=round(probability, 4),
            risk_level=risk_level,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar la predicción: {str(e)}"
        )


@app.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(batch: TransactionBatch):
    """
    Predice fraude para múltiples transacciones en lote.
    
    Args:
        batch: TransactionBatch con lista de transacciones.
    
    Returns:
        BatchPredictionResponse: Lista de predicciones.
    """
    if model is None or preprocessor is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo no disponible. El servicio no está listo."
        )
    
    try:
        start_time = datetime.now()
        
        # Convertir a DataFrame
        df = pd.DataFrame([t.dict() for t in batch.transactions])
        
        # Crear features derivados
        df['amount_per_transaction'] = df['amount'] / (df['previous_transactions'] + 1)
        df['age_group'] = pd.cut(df['customer_age'], 
                                 bins=[0, 25, 35, 50, 100], 
                                 labels=['young', 'adult', 'middle_age', 'senior'])
        df['age_group'] = df['age_group'].astype(str)
        amount_threshold = df['amount'].quantile(0.75)
        df['high_amount'] = (df['amount'] > amount_threshold).astype(int)
        
        # Preprocesar
        X_processed = preprocessor.transform(df)
        
        # Predecir
        predictions = model.predict(X_processed)
        probabilities = model.predict_proba(X_processed)[:, 1]
        
        # Formatear respuestas
        results = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            if prob < 0.3:
                risk_level = "Bajo"
            elif prob < 0.7:
                risk_level = "Medio"
            else:
                risk_level = "Alto"
            
            results.append(
                PredictionResponse(
                    index=i,
                    is_fraud=int(pred),
                    fraud_probability=round(float(prob), 4),
                    risk_level=risk_level,
                    timestamp=datetime.now().isoformat()
                )
            )
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        fraud_count = sum(predictions)
        
        return BatchPredictionResponse(
            predictions=results,
            total_transactions=len(batch.transactions),
            fraud_detected=int(fraud_count),
            processing_time_ms=round(processing_time, 2)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar predicciones por lote: {str(e)}"
        )


@app.get("/model/info")
async def model_info():
    """
    Retorna información sobre el modelo cargado.
    """
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo no disponible"
        )
    
    return {
        "model_type": type(model).__name__,
        "model_path": config.MODEL_PATH,
        "preprocessor_path": config.PREPROCESSOR_PATH,
        "features": {
            "numerical": config.NUMERICAL_COLS,
            "categorical": config.CATEGORICAL_COLS
        }
    }


# ==================== MAIN ====================

if __name__ == "__main__":
    """
    Ejecutar la API directamente.
    Uso: python -m mlops_pipeline.src.model_deploy
    """
    print("="*60)
    print("  Iniciando API de Detección de Fraude")
    print("="*60)
    print(f"\n📡 Servidor: http://localhost:{config.API_PORT}")
    print(f"📚 Documentación: http://localhost:{config.API_PORT}/docs")
    print(f"📖 ReDoc: http://localhost:{config.API_PORT}/redoc\n")
    
    uvicorn.run(
        "mlops_pipeline.src.model_deploy:app",
        host="0.0.0.0",
        port=config.API_PORT,
        reload=True,
        log_level="info"
    )
