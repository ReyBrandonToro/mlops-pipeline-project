"""
Ejemplo de uso de la API REST para predicciones de fraude.
Este script muestra cómo hacer requests a la API desde Python.
"""

import requests
import json
from typing import List, Dict


# Configuración de la API
API_URL = "http://localhost:8000"


def check_api_health() -> bool:
    """
    Verifica si la API está disponible.
    
    Returns:
        bool: True si la API está activa, False en caso contrario.
    """
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ API Status:", data.get("status"))
            print(f"   - Modelo cargado: {data.get('model_loaded')}")
            print(f"   - Preprocesador cargado: {data.get('preprocessor_loaded')}")
            return True
        else:
            print(f"❌ API no disponible. Status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar a la API. ¿Está el servidor corriendo?")
        print("   Ejecuta: python main.py y selecciona la opción 5")
        return False


def predict_single_transaction(transaction: Dict) -> Dict:
    """
    Realiza una predicción para una transacción individual.
    
    Args:
        transaction: Diccionario con los datos de la transacción.
        
    Returns:
        Dict: Respuesta de la API con la predicción.
    """
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=transaction,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error en la predicción: {response.status_code}")
            print(f"   Detalle: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def predict_batch_transactions(transactions: List[Dict]) -> Dict:
    """
    Realiza predicciones para múltiples transacciones.
    
    Args:
        transactions: Lista de diccionarios con transacciones.
        
    Returns:
        Dict: Respuesta de la API con las predicciones.
    """
    try:
        payload = {"transactions": transactions}
        response = requests.post(
            f"{API_URL}/predict/batch",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error en predicción por lote: {response.status_code}")
            print(f"   Detalle: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def print_prediction_result(result: Dict, transaction: Dict):
    """Imprime el resultado de la predicción de forma legible."""
    if result:
        print("\n" + "="*60)
        print("  RESULTADO DE LA PREDICCIÓN")
        print("="*60)
        print(f"\n📋 Transacción:")
        print(f"   Monto: ${transaction['amount']:,.2f}")
        print(f"   Balance Anterior: ${transaction['oldbalanceOrg']:,.2f}")
        print(f"   Balance Nuevo: ${transaction['newbalanceOrg']:,.2f}")
        print(f"   Tipo: {transaction['type']}")
        
        print(f"\n🔍 Predicción:")
        print(f"   Es Fraude: {'❌ SÍ' if result['is_fraud'] == 1 else '✅ NO'}")
        print(f"   Probabilidad: {result['fraud_probability']:.2%}")
        print(f"   Nivel de Riesgo: {result['risk_level']}")
        print(f"   Timestamp: {result['timestamp']}")
        print("="*60 + "\n")


def main():
    """Función principal con ejemplos de uso."""
    
    print("\n" + "🚀"*30)
    print("  EJEMPLOS DE USO - API DE DETECCIÓN DE FRAUDE")
    print("🚀"*30 + "\n")
    
    # 1. Verificar que la API esté activa
    print("[1/3] Verificando estado de la API...")
    if not check_api_health():
        return
    
    print("\n" + "-"*60 + "\n")
    
    # 2. Ejemplo de predicción individual - Transacción Normal
    print("[2/3] Ejemplo: Predicción Individual (Transacción Normal)")
    
    transaction_normal = {
        "amount": 1500.50,
        "oldbalanceOrg": 50000.00,
        "newbalanceOrg": 48500.00,
        "type": "PAYMENT"
    }
    
    result = predict_single_transaction(transaction_normal)
    print_prediction_result(result, transaction_normal)
    
    # 3. Ejemplo de predicción individual - Transacción Sospechosa
    print("[3/3] Ejemplo: Predicción Individual (Transacción Sospechosa)")
    
    transaction_suspicious = {
        "amount": 250000.00,
        "oldbalanceOrg": 300000.00,
        "newbalanceOrg": 0.00,
        "type": "TRANSFER"
    }
    
    result = predict_single_transaction(transaction_suspicious)
    print_prediction_result(result, transaction_suspicious)
    
    # 4. Ejemplo de predicción por lote
    print("\n" + "-"*60 + "\n")
    print("[EXTRA] Ejemplo: Predicción por Lote (3 transacciones)")
    
    batch_transactions = [
        {
            "amount": 5000.00,
            "oldbalanceOrg": 20000.00,
            "newbalanceOrg": 15000.00,
            "type": "CASH_OUT"
        },
        {
            "amount": 500.00,
            "oldbalanceOrg": 10000.00,
            "newbalanceOrg": 9500.00,
            "type": "PAYMENT"
        },
        {
            "amount": 100000.00,
            "oldbalanceOrg": 150000.00,
            "newbalanceOrg": 0.00,
            "type": "TRANSFER"
        }
    ]
    
    batch_result = predict_batch_transactions(batch_transactions)
    
    if batch_result:
        print("\n" + "="*60)
        print("  RESULTADOS DE PREDICCIÓN POR LOTE")
        print("="*60)
        print(f"\n📊 Total de transacciones: {batch_result['total_transactions']}")
        print(f"🚨 Fraudes detectados: {batch_result['fraud_detected']}")
        print(f"⏱️  Tiempo de procesamiento: {batch_result['processing_time_ms']:.2f} ms")
        
        print("\n📋 Detalle de predicciones:")
        for pred in batch_result['predictions']:
            status = "🔴 FRAUDE" if pred['is_fraud'] == 1 else "🟢 LEGÍTIMO"
            print(f"\n   Transacción {pred['index'] + 1}: {status}")
            print(f"      Probabilidad: {pred['fraud_probability']:.2%}")
            print(f"      Riesgo: {pred['risk_level']}")
        
        print("\n" + "="*60 + "\n")
    
    # Resumen final
    print("\n" + "✅"*30)
    print("\nEjemplos completados exitosamente!")
    print("\n💡 TIP: Puedes usar estos ejemplos para integrar la API en tu aplicación")
    print("   - FastAPI Docs: http://localhost:8000/docs")
    print("   - ReDoc: http://localhost:8000/redoc")
    print("\n" + "✅"*30 + "\n")


if __name__ == "__main__":
    main()
