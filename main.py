"""
Script principal para ejecutar el pipeline completo de MLOps.
Proporciona un menú interactivo para las diferentes operaciones.
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def print_banner():
    """Imprime el banner del proyecto."""
    banner = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║        🚀 MLOps Pipeline - Detección de Fraude Financiero     ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_menu():
    """Imprime el menú de opciones."""
    menu = """
┌────────────────────────────────────────────────────────────────┐
│  OPCIONES DISPONIBLES:                                         │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  1. 📊 Ejecutar Pipeline Completo (E2E)                       │
│     └─ Carga → Validación → Features → Entrenamiento          │
│                                                                │
│  2. 🔍 Solo Validar Datos                                     │
│     └─ Verifica calidad e integridad del dataset              │
│                                                                │
│  3. 🛠️  Solo Ingeniería de Características                    │
│     └─ Crea features y preprocesa datos                       │
│                                                                │
│  4. 🤖 Solo Entrenar Modelos                                  │
│     └─ Entrena y compara múltiples modelos                    │
│                                                                │
│  5. 🌐 Iniciar API REST                                       │
│     └─ FastAPI en http://localhost:8000                       │
│                                                                │
│  6. 📈 Abrir Dashboard de Monitoreo                           │
│     └─ Streamlit para detección de drift                      │
│                                                                │
│  7. 📓 Abrir Notebook de EDA                                  │
│     └─ Jupyter Lab con análisis exploratorio                  │
│                                                                │
│  8. ℹ️  Ver Información del Proyecto                          │
│                                                                │
│  0. ❌ Salir                                                   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
    """
    print(menu)


def run_full_pipeline():
    """Ejecuta el pipeline completo E2E."""
    print("\n" + "="*60)
    print("  EJECUTANDO PIPELINE COMPLETO")
    print("="*60 + "\n")
    
    try:
        from mlops_pipeline.src.model_training_evaluation import ModelTrainer
        
        trainer = ModelTrainer()
        trainer.run_pipeline()
        
        print("\n✅ Pipeline completado exitosamente!")
        print(f"   - Modelo guardado: best_model.joblib")
        print(f"   - Preprocesador guardado: preprocessor.joblib")
        
    except Exception as e:
        print(f"\n❌ Error al ejecutar el pipeline: {str(e)}")
        import traceback
        traceback.print_exc()


def validate_data_only():
    """Solo valida los datos."""
    print("\n" + "="*60)
    print("  VALIDANDO DATOS")
    print("="*60 + "\n")
    
    try:
        from mlops_pipeline.src.cargar_datos import DataLoader
        from mlops_pipeline.src.data_validation import DataValidator
        
        loader = DataLoader()
        df = loader.load_data()
        
        if not df.empty:
            validator = DataValidator()
            if validator.validate_data(df):
                print("\n✅ Validación completada - Datos correctos!")
            else:
                print("\n❌ Validación fallida - Revisa los errores anteriores")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def feature_engineering_only():
    """Solo ejecuta ingeniería de características."""
    print("\n" + "="*60)
    print("  INGENIERÍA DE CARACTERÍSTICAS")
    print("="*60 + "\n")
    
    try:
        from mlops_pipeline.src.cargar_datos import DataLoader
        from mlops_pipeline.src.data_validation import DataValidator
        from mlops_pipeline.src.ft_engineering import FeatureEngineer
        
        loader = DataLoader()
        df = loader.load_data()
        
        if not df.empty:
            validator = DataValidator()
            if validator.validate_data(df):
                engineer = FeatureEngineer()
                X_train, X_test, y_train, y_test = engineer.process(df)
                
                print(f"\n✅ Procesamiento completado!")
                print(f"   - Shape X_train: {X_train.shape}")
                print(f"   - Shape X_test: {X_test.shape}")
                print(f"   - Preprocesador guardado: preprocessor.joblib")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def train_models_only():
    """Solo entrena modelos (asume que ya existen datos preprocesados)."""
    print("\n" + "="*60)
    print("  ENTRENANDO MODELOS")
    print("="*60 + "\n")
    
    print("⚠️  Esta opción requiere ejecutar primero la opción 3")
    print("   (Ingeniería de Características) o el pipeline completo.\n")
    
    response = input("¿Deseas ejecutar el pipeline completo? (s/n): ")
    if response.lower() == 's':
        run_full_pipeline()


def start_api():
    """Inicia la API REST."""
    print("\n" + "="*60)
    print("  INICIANDO API REST")
    print("="*60 + "\n")
    
    print("📡 La API se iniciará en: http://localhost:8000")
    print("📚 Documentación: http://localhost:8000/docs")
    print("\n⚠️  Presiona Ctrl+C para detener el servidor\n")
    
    import time
    time.sleep(2)
    
    try:
        import uvicorn
        from mlops_pipeline.src.model_deploy import app
        
        uvicorn.run(
            "mlops_pipeline.src.model_deploy:app",
            host="0.0.0.0",
            port=8000,
            reload=True
        )
    except KeyboardInterrupt:
        print("\n\n✅ API detenida correctamente")
    except Exception as e:
        print(f"\n❌ Error al iniciar API: {str(e)}")


def start_monitoring_dashboard():
    """Inicia el dashboard de monitoreo."""
    print("\n" + "="*60)
    print("  INICIANDO DASHBOARD DE MONITOREO")
    print("="*60 + "\n")
    
    print("📊 El dashboard se abrirá en tu navegador")
    print("⚠️  Presiona Ctrl+C para detener el dashboard\n")
    
    import time
    import subprocess
    time.sleep(2)
    
    try:
        subprocess.run([
            "streamlit", "run",
            "mlops_pipeline/src/model_monitoring.py"
        ])
    except KeyboardInterrupt:
        print("\n\n✅ Dashboard detenido correctamente")
    except Exception as e:
        print(f"\n❌ Error al iniciar dashboard: {str(e)}")


def open_jupyter_notebook():
    """Abre el notebook de EDA en Jupyter Lab."""
    print("\n" + "="*60)
    print("  ABRIENDO NOTEBOOK DE EDA")
    print("="*60 + "\n")
    
    print("📓 Se abrirá Jupyter Lab en tu navegador")
    print("⚠️  Presiona Ctrl+C para detener Jupyter\n")
    
    import time
    import subprocess
    time.sleep(2)
    
    try:
        subprocess.run([
            "jupyter", "lab",
            "mlops_pipeline/src/comprension_eda.ipynb"
        ])
    except KeyboardInterrupt:
        print("\n\n✅ Jupyter Lab detenido correctamente")
    except Exception as e:
        print(f"\n❌ Error al abrir Jupyter: {str(e)}")


def show_project_info():
    """Muestra información del proyecto."""
    info = """
╔════════════════════════════════════════════════════════════════╗
║  📋 INFORMACIÓN DEL PROYECTO                                   ║
╚════════════════════════════════════════════════════════════════╝

📦 Proyecto: MLOps Pipeline - Detección de Fraude
🎯 Objetivo: Detectar transacciones fraudulentas en tiempo real
🏗️  Arquitectura: Pipeline modular basado en clases

📂 Estructura:
   ├── mlops_pipeline/src/
   │   ├── config.py                      (Configuración)
   │   ├── cargar_datos.py                (DataLoader)
   │   ├── data_validation.py             (DataValidator)
   │   ├── ft_engineering.py              (FeatureEngineer)
   │   ├── model_training_evaluation.py   (ModelTrainer)
   │   ├── model_deploy.py                (API REST)
   │   ├── model_monitoring.py            (Dashboard)
   │   └── comprension_eda.ipynb          (EDA Notebook)
   │
   ├── financial_fraud_dataset.csv        (Dataset)
   ├── best_model.joblib                  (Modelo entrenado)
   ├── preprocessor.joblib                (Preprocesador)
   └── requirements.txt                   (Dependencias)

🤖 Modelos Implementados:
   • Logistic Regression
   • Random Forest
   • XGBoost (mejor performance esperada)

📊 Features Derivados:
   • errorBalanceOrg
   • transactionRatio
   • zeroBalanceAfter

🔧 Tecnologías:
   • Python 3.10+
   • Scikit-learn, XGBoost
   • FastAPI (API REST)
   • Streamlit (Dashboard)
   • Docker (Contenedores)

📖 Documentación completa en: README.md

    """
    print(info)


def main():
    """Función principal del menú interactivo."""
    while True:
        print_banner()
        print_menu()
        
        try:
            option = input("Selecciona una opción [0-8]: ").strip()
            
            if option == '1':
                run_full_pipeline()
            elif option == '2':
                validate_data_only()
            elif option == '3':
                feature_engineering_only()
            elif option == '4':
                train_models_only()
            elif option == '5':
                start_api()
            elif option == '6':
                start_monitoring_dashboard()
            elif option == '7':
                open_jupyter_notebook()
            elif option == '8':
                show_project_info()
            elif option == '0':
                print("\n👋 ¡Hasta pronto!\n")
                break
            else:
                print("\n❌ Opción inválida. Por favor, selecciona una opción válida.\n")
            
            if option != '0':
                input("\n\n📌 Presiona Enter para volver al menú principal...")
                print("\n" * 2)
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta pronto!\n")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {str(e)}\n")
            input("\n📌 Presiona Enter para continuar...")


if __name__ == "__main__":
    main()
