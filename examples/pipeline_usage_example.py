"""
Ejemplo de uso del pipeline de forma programática.
Muestra cómo usar las clases del pipeline sin el menú interactivo.
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mlops_pipeline.src.cargar_datos import DataLoader
from mlops_pipeline.src.data_validation import DataValidator
from mlops_pipeline.src.ft_engineering import FeatureEngineer
from mlops_pipeline.src.model_training_evaluation import ModelTrainer


def example_data_loading():
    """Ejemplo 1: Carga de datos."""
    print("\n" + "="*60)
    print("EJEMPLO 1: CARGA DE DATOS")
    print("="*60 + "\n")
    
    # Instanciar el DataLoader
    loader = DataLoader()
    
    # Cargar datos
    df = loader.load_data()
    
    if not df.empty:
        print("\n✅ Datos cargados correctamente")
        print(f"\nInformación del DataFrame:")
        print(f"  - Filas: {df.shape[0]:,}")
        print(f"  - Columnas: {df.shape[1]}")
        print(f"  - Columnas disponibles: {list(df.columns)}")
        
        # Ver primeras filas
        print(f"\n📊 Primeras 3 filas:")
        print(df.head(3))
        
        return df
    else:
        print("❌ Error al cargar datos")
        return None


def example_data_validation(df):
    """Ejemplo 2: Validación de datos."""
    print("\n" + "="*60)
    print("EJEMPLO 2: VALIDACIÓN DE DATOS")
    print("="*60 + "\n")
    
    # Instanciar el validador
    validator = DataValidator()
    
    # Validar datos
    is_valid = validator.validate_data(df)
    
    if is_valid:
        print("\n✅ Los datos pasaron todas las validaciones")
        return True
    else:
        print("\n❌ Los datos NO pasaron las validaciones")
        return False


def example_feature_engineering(df):
    """Ejemplo 3: Ingeniería de características."""
    print("\n" + "="*60)
    print("EJEMPLO 3: INGENIERÍA DE CARACTERÍSTICAS")
    print("="*60 + "\n")
    
    # Instanciar el FeatureEngineer
    engineer = FeatureEngineer(random_state=42)
    
    # Procesar datos
    X_train, X_test, y_train, y_test = engineer.process(df)
    
    print("\n✅ Datos procesados correctamente")
    print(f"\nFormas de los conjuntos:")
    print(f"  - X_train: {X_train.shape}")
    print(f"  - X_test: {X_test.shape}")
    print(f"  - y_train: {y_train.shape}")
    print(f"  - y_test: {y_test.shape}")
    
    print(f"\nDistribución del target en entrenamiento:")
    print(f"  - No Fraude (0): {(y_train == 0).sum():,}")
    print(f"  - Fraude (1): {(y_train == 1).sum():,}")
    
    return X_train, X_test, y_train, y_test


def example_model_training():
    """Ejemplo 4: Entrenamiento completo del pipeline."""
    print("\n" + "="*60)
    print("EJEMPLO 4: ENTRENAMIENTO COMPLETO")
    print("="*60 + "\n")
    
    # Instanciar el ModelTrainer (orquestador)
    trainer = ModelTrainer(random_state=42)
    
    # Ejecutar pipeline completo
    print("🚀 Ejecutando pipeline E2E...")
    print("   Esto incluye:")
    print("   1. Carga de datos")
    print("   2. Validación")
    print("   3. Ingeniería de características")
    print("   4. Entrenamiento de modelos")
    print("   5. Evaluación y selección del mejor")
    print("\n" + "-"*60 + "\n")
    
    trainer.run_pipeline()
    
    print("\n✅ Pipeline completado")
    print(f"\nMejor modelo seleccionado: {trainer.best_model_name}")
    print(f"ROC-AUC Score: {trainer.best_auc:.4f}")
    
    # Mostrar comparación de modelos
    if trainer.results:
        print("\n📊 Comparación de Modelos:")
        for model_name, metrics in trainer.results.items():
            print(f"\n   {model_name}:")
            print(f"      - ROC-AUC: {metrics['roc_auc']:.4f}")
            print(f"      - F1-Score: {metrics['f1_score']:.4f}")
            print(f"      - Precision: {metrics['precision']:.4f}")
            print(f"      - Recall: {metrics['recall']:.4f}")


def example_custom_pipeline():
    """Ejemplo 5: Pipeline personalizado (paso a paso)."""
    print("\n" + "="*60)
    print("EJEMPLO 5: PIPELINE PERSONALIZADO")
    print("="*60 + "\n")
    
    # Paso 1: Cargar datos
    df = example_data_loading()
    if df is None:
        return
    
    # Paso 2: Validar datos
    if not example_data_validation(df):
        return
    
    # Paso 3: Ingeniería de características
    X_train, X_test, y_train, y_test = example_feature_engineering(df)
    
    # Paso 4: Podrías entrenar un modelo personalizado aquí
    print("\n" + "="*60)
    print("💡 TIP: Aquí podrías entrenar tu propio modelo personalizado")
    print("="*60)
    print("\nEjemplo:")
    print("   from sklearn.ensemble import GradientBoostingClassifier")
    print("   model = GradientBoostingClassifier()")
    print("   model.fit(X_train, y_train)")
    print("   predictions = model.predict(X_test)")


def main():
    """Función principal que ejecuta todos los ejemplos."""
    
    print("\n" + "🎓"*30)
    print("  EJEMPLOS DE USO DEL PIPELINE MLOps")
    print("🎓"*30 + "\n")
    
    print("\nEste script muestra diferentes formas de usar el pipeline:")
    print("  1. Uso modular (paso a paso)")
    print("  2. Uso completo (end-to-end)")
    print("  3. Personalización del pipeline")
    
    print("\n" + "-"*60)
    
    # Menú de ejemplos
    print("\nSelecciona qué ejemplo ejecutar:")
    print("  1 - Solo carga de datos")
    print("  2 - Carga + Validación")
    print("  3 - Carga + Validación + Feature Engineering")
    print("  4 - Pipeline completo (entrenar modelos)")
    print("  5 - Pipeline personalizado (todos los pasos)")
    print("  0 - Salir")
    
    try:
        option = input("\nOpción: ").strip()
        
        if option == '1':
            example_data_loading()
            
        elif option == '2':
            df = example_data_loading()
            if df is not None:
                example_data_validation(df)
                
        elif option == '3':
            df = example_data_loading()
            if df is not None and example_data_validation(df):
                example_feature_engineering(df)
                
        elif option == '4':
            example_model_training()
            
        elif option == '5':
            example_custom_pipeline()
            
        elif option == '0':
            print("\n👋 ¡Hasta pronto!\n")
            return
            
        else:
            print("\n❌ Opción inválida")
        
        print("\n" + "✅"*30)
        print("\n¡Ejemplo completado exitosamente!")
        print("\n💡 Revisa el código en 'examples/pipeline_usage_example.py'")
        print("   para ver cómo se implementa cada función.")
        print("\n" + "✅"*30 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n👋 Ejecución interrumpida por el usuario\n")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
