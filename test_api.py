"""
Script de prueba de la API de detección de fraude.
Ejecuta varios casos de prueba para verificar el funcionamiento de la API.
"""

import requests
import json
from datetime import datetime

# Configuración
API_URL = "http://localhost:8000"

def print_separator():
    print("\n" + "="*70)

def test_health_check():
    """Prueba el endpoint de health check."""
    print_separator()
    print("🔍 TEST 1: Health Check")
    print_separator()
    
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_root():
    """Prueba el endpoint raíz."""
    print_separator()
    print("🔍 TEST 2: Endpoint Raíz")
    print_separator()
    
    try:
        response = requests.get(API_URL)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_predict_normal_transaction():
    """Prueba predicción de una transacción normal."""
    print_separator()
    print("🔍 TEST 3: Transacción Normal")
    print_separator()
    
    transaction = {
        "amount": 250.50,
        "merchant_category": "retail",
        "customer_age": 35,
        "customer_location": "urban",
        "device_type": "mobile",
        "previous_transactions": 15
    }
    
    print(f"Transacción: {json.dumps(transaction, indent=2)}")
    
    try:
        response = requests.post(f"{API_URL}/predict", json=transaction)
        print(f"\nStatus Code: {response.status_code}")
        result = response.json()
        print(f"Resultado: {json.dumps(result, indent=2)}")
        
        print(f"\n📊 Interpretación:")
        print(f"  - ¿Es fraude? {'SÍ' if result['is_fraud'] == 1 else 'NO'}")
        print(f"  - Probabilidad: {result['fraud_probability']*100:.2f}%")
        print(f"  - Nivel de riesgo: {result['risk_level']}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_predict_suspicious_transaction():
    """Prueba predicción de una transacción sospechosa."""
    print_separator()
    print("🔍 TEST 4: Transacción Sospechosa")
    print_separator()
    
    transaction = {
        "amount": 5000,
        "merchant_category": "online",
        "customer_age": 22,
        "customer_location": "rural",
        "device_type": "desktop",
        "previous_transactions": 2
    }
    
    print(f"Transacción: {json.dumps(transaction, indent=2)}")
    
    try:
        response = requests.post(f"{API_URL}/predict", json=transaction)
        print(f"\nStatus Code: {response.status_code}")
        result = response.json()
        print(f"Resultado: {json.dumps(result, indent=2)}")
        
        print(f"\n📊 Interpretación:")
        print(f"  - ¿Es fraude? {'SÍ ⚠️' if result['is_fraud'] == 1 else 'NO ✅'}")
        print(f"  - Probabilidad: {result['fraud_probability']*100:.2f}%")
        print(f"  - Nivel de riesgo: {result['risk_level']}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_predict_batch():
    """Prueba predicción por lotes."""
    print_separator()
    print("🔍 TEST 5: Predicción por Lotes (3 transacciones)")
    print_separator()
    
    batch = {
        "transactions": [
            {
                "amount": 100,
                "merchant_category": "grocery",
                "customer_age": 45,
                "customer_location": "urban",
                "device_type": "mobile",
                "previous_transactions": 50
            },
            {
                "amount": 1500,
                "merchant_category": "electronics",
                "customer_age": 28,
                "customer_location": "suburban",
                "device_type": "tablet",
                "previous_transactions": 10
            },
            {
                "amount": 8000,
                "merchant_category": "jewelry",
                "customer_age": 19,
                "customer_location": "rural",
                "device_type": "desktop",
                "previous_transactions": 1
            }
        ]
    }
    
    print(f"Número de transacciones: {len(batch['transactions'])}")
    
    try:
        response = requests.post(f"{API_URL}/predict/batch", json=batch)
        print(f"\nStatus Code: {response.status_code}")
        result = response.json()
        
        print(f"\n📊 Resumen:")
        print(f"  - Total transacciones: {result['total_transactions']}")
        print(f"  - Fraudes detectados: {result['fraud_detected']}")
        print(f"  - Tiempo de procesamiento: {result['processing_time_ms']:.2f} ms")
        
        print(f"\n📋 Detalle de predicciones:")
        for pred in result['predictions']:
            status = "⚠️ FRAUDE" if pred['is_fraud'] == 1 else "✅ Normal"
            print(f"  [{pred['index']}] {status} - Prob: {pred['fraud_probability']*100:.2f}% - Riesgo: {pred['risk_level']}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_model_info():
    """Prueba el endpoint de información del modelo."""
    print_separator()
    print("🔍 TEST 6: Información del Modelo")
    print_separator()
    
    try:
        response = requests.get(f"{API_URL}/model/info")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def run_all_tests():
    """Ejecuta todos los tests."""
    print("\n" + "="*70)
    print("🚀 INICIANDO PRUEBAS DE LA API DE DETECCIÓN DE FRAUDE")
    print("="*70)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API URL: {API_URL}")
    
    tests = [
        ("Health Check", test_health_check),
        ("Endpoint Raíz", test_root),
        ("Transacción Normal", test_predict_normal_transaction),
        ("Transacción Sospechosa", test_predict_suspicious_transaction),
        ("Predicción por Lotes", test_predict_batch),
        ("Información del Modelo", test_model_info)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error en test '{name}': {str(e)}")
            results.append((name, False))
    
    # Resumen final
    print_separator()
    print("📊 RESUMEN DE PRUEBAS")
    print_separator()
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status} - {name}")
    
    print_separator()
    print(f"Resultado: {passed}/{total} tests pasaron ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
    else:
        print(f"⚠️  {total - passed} test(s) fallaron")
    
    print_separator()

if __name__ == "__main__":
    print("\n⏳ Esperando 2 segundos para asegurar que la API esté lista...")
    import time
    time.sleep(2)
    
    run_all_tests()
    
    print("\n💡 TIP: Puedes ver la documentación interactiva en:")
    print(f"   📚 Swagger UI: {API_URL}/docs")
    print(f"   📖 ReDoc: {API_URL}/redoc")
    print()
