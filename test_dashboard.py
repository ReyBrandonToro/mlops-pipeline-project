"""
Script de prueba para verificar todas las funcionalidades del dashboard.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import joblib

project_root = Path.cwd()
sys.path.insert(0, str(project_root))

print('═══════════════════════════════════════════════════════════')
print('🧪 PRUEBA DE FUNCIONES DEL DASHBOARD')
print('═══════════════════════════════════════════════════════════')
print()

# Prueba 1: Cargar datos
print('📊 1. Probando carga de datos...')
try:
    from mlops_pipeline.src import cargar_datos
    loader = cargar_datos.DataLoader()
    df = loader.load_data()
    if not df.empty:
        print(f'   ✅ Dataset cargado: {len(df):,} registros')
        print(f'   ✅ Columnas: {len(df.columns)}')
        fraud_count = df['isFraud'].sum()
        print(f'   ✅ Fraudes: {fraud_count:,}')
    else:
        print('   ❌ Dataset vacío')
        df = None
except Exception as e:
    print(f'   ❌ Error: {e}')
    df = None
print()

# Prueba 2: Validación
print('✅ 2. Probando validación de datos...')
if df is not None:
    try:
        from mlops_pipeline.src import data_validation
        validator = data_validation.DataValidator(df)
        resultados = validator.validar_todo()
        passed = sum(1 for r in resultados.values() if r['passed'])
        print(f'   ✅ Validaciones pasadas: {passed}/{len(resultados)}')
    except Exception as e:
        print(f'   ❌ Error: {e}')
else:
    print('   ⚠️ Saltando prueba (datos no cargados)')
print()

# Prueba 3: Modelo
print('🤖 3. Probando carga del modelo...')
modelo = None
preprocessor = None
try:
    modelo = joblib.load('best_model.joblib')
    preprocessor = joblib.load('preprocessor.joblib')
    print(f'   ✅ Modelo cargado: {type(modelo).__name__}')
    print(f'   ✅ Preprocessor cargado')
except Exception as e:
    print(f'   ❌ Error: {e}')
print()

# Prueba 4: Predicción
print('🎯 4. Probando predicción...')
if modelo is not None and preprocessor is not None:
    try:
        datos_test = pd.DataFrame({
            'TransactionAmount': [500.0],
            'oldbalanceOrg': [10000.0],
            'newbalanceOrig': [9500.0],
            'oldbalanceDest': [5000.0],
            'newbalanceDest': [5500.0],
            'TransactionHour': [14],
            'AccountAge': [365],
            'TransactionAmountLog': [np.log1p(500.0)],
            'type': ['PAYMENT']
        })
        
        datos_proc = preprocessor.transform(datos_test)
        pred = modelo.predict(datos_proc)[0]
        prob = modelo.predict_proba(datos_proc)[0]
        
        print(f'   ✅ Predicción: {"FRAUDE" if pred == 1 else "LEGÍTIMO"}')
        print(f'   ✅ Probabilidad fraude: {prob[1]:.1%}')
        print(f'   ✅ Nivel de riesgo: {"🔴 ALTO" if prob[1] > 0.7 else "🟡 MEDIO" if prob[1] > 0.3 else "🟢 BAJO"}')
    except Exception as e:
        print(f'   ❌ Error: {e}')
else:
    print('   ⚠️ Saltando prueba (modelo no cargado)')
print()

print('═══════════════════════════════════════════════════════════')
print('✅ PRUEBAS COMPLETADAS')
print('═══════════════════════════════════════════════════════════')
