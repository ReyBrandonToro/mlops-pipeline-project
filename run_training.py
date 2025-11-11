"""
Script simplificado para ejecutar el entrenamiento del modelo
sin dependencias de streamlit
"""

import sys
sys.path.insert(0, 'c:\\Proyecto')

# Importar el trainer
try:
    from mlops_pipeline.src.model_training_evaluation import ModelTrainer
except ImportError:
    from mlops_pipeline.src import model_training_evaluation
    ModelTrainer = model_training_evaluation.ModelTrainer

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 INICIANDO PIPELINE DE ENTRENAMIENTO")
    print("=" * 70)
    
    # Crear instancia del trainer
    trainer = ModelTrainer()
    
    # Ejecutar pipeline completo
    try:
        trainer.run_pipeline()
        print("\n" + "=" * 70)
        print("✅ PIPELINE COMPLETADO EXITOSAMENTE")
        print("=" * 70)
        print("\nModelos generados:")
        print("  📦 best_model.joblib")
        print("  📦 preprocessor.joblib")
    except Exception as e:
        print("\n" + "=" * 70)
        print(f"❌ ERROR: {str(e)}")
        print("=" * 70)
        import traceback
        traceback.print_exc()
