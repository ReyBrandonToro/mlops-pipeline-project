"""
Módulo de entrenamiento y evaluación de modelos.
Define la clase ModelTrainer que orquesta todo el pipeline de ML.
"""

import pandas as pd
import numpy as np
import joblib
import xgboost as xgb
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report, 
    roc_auc_score, 
    f1_score, 
    confusion_matrix, 
    roc_curve,
    precision_recall_curve,
    accuracy_score,
    precision_score,
    recall_score
)
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import seaborn as sns

try:
    from mlops_pipeline.src.cargar_datos import DataLoader
    from mlops_pipeline.src.data_validation import DataValidator
    from mlops_pipeline.src.ft_engineering import FeatureEngineer
    from mlops_pipeline.src import config
except ImportError:
    from .cargar_datos import DataLoader
    from .data_validation import DataValidator
    from .ft_engineering import FeatureEngineer
    from . import config


class ModelTrainer:
    """
    Clase orquestadora del pipeline completo de Machine Learning.
    Integra carga, validación, preprocesamiento, entrenamiento y evaluación.
    """
    
    def __init__(self, random_state=None):
        """
        Inicializa el ModelTrainer.
        
        Args:
            random_state (int, optional): Semilla para reproducibilidad.
        """
        self.random_state = random_state if random_state is not None else config.RANDOM_STATE
        self.loader = DataLoader()
        self.validator = DataValidator()
        self.engineer = FeatureEngineer(random_state=self.random_state)
        self.best_model = None
        self.best_model_name = None
        self.best_auc = 0.0
        self.results = {}
    
    def build_models(self):
        """
        Construye el diccionario de modelos a entrenar.
        
        Returns:
            dict: Diccionario con nombre y objeto de modelo.
        """
        models = {
            'LogisticRegression': LogisticRegression(
                random_state=self.random_state, 
                max_iter=1000,
                class_weight='balanced'
            ),
            'RandomForest': RandomForestClassifier(
                random_state=self.random_state,
                n_estimators=100,
                max_depth=10,
                class_weight='balanced'
            ),
            'XGBoost': xgb.XGBClassifier(
                random_state=self.random_state,
                use_label_encoder=False,
                eval_metric='logloss',
                scale_pos_weight=10  # Ajustar según el desbalanceo
            )
        }
        return models
    
    def summarize_classification(self, model_name, y_test, y_pred, y_prob):
        """
        Resume y muestra las métricas de clasificación.
        
        Args:
            model_name (str): Nombre del modelo.
            y_test (array): Valores reales.
            y_pred (array): Predicciones.
            y_prob (array): Probabilidades de la clase positiva.
        """
        print("\n" + "="*60)
        print(f"MÉTRICAS DE EVALUACIÓN - {model_name}")
        print("="*60)
        
        # Métricas principales
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_prob)
        
        print("\n📊 MÉTRICAS GENERALES:")
        print(f"  • Accuracy:  {accuracy:.4f}")
        print(f"  • Precision: {precision:.4f}")
        print(f"  • Recall:    {recall:.4f}")
        print(f"  • F1-Score:  {f1:.4f}")
        print(f"  • ROC-AUC:   {roc_auc:.4f}")
        
        print("\n📋 REPORTE DE CLASIFICACIÓN:")
        print(classification_report(y_test, y_pred, target_names=['No Fraude', 'Fraude']))
        
        # Almacenar resultados
        self.results[model_name] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'roc_auc': roc_auc,
            'y_pred': y_pred,
            'y_prob': y_prob
        }
        
        # Matriz de confusión
        self._plot_confusion_matrix(y_test, y_pred, model_name)
        
        return roc_auc
    
    def _plot_confusion_matrix(self, y_test, y_pred, model_name):
        """
        Genera y muestra la matriz de confusión.
        
        Args:
            y_test (array): Valores reales.
            y_pred (array): Predicciones.
            model_name (str): Nombre del modelo.
        """
        cm = confusion_matrix(y_test, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(
            cm, 
            annot=True, 
            fmt='d', 
            cmap='Blues',
            xticklabels=['No Fraude', 'Fraude'],
            yticklabels=['No Fraude', 'Fraude']
        )
        plt.title(f'Matriz de Confusión - {model_name}')
        plt.ylabel('Real')
        plt.xlabel('Predicción')
        plt.tight_layout()
        plt.savefig(f'confusion_matrix_{model_name.lower().replace(" ", "_")}.png', dpi=300)
        plt.show()
        
        print(f"\n  ✓ Matriz de confusión guardada como: confusion_matrix_{model_name.lower().replace(' ', '_')}.png")
    
    def plot_roc_curves(self, y_test):
        """
        Genera curvas ROC comparativas para todos los modelos.
        
        Args:
            y_test (array): Valores reales del conjunto de test.
        """
        plt.figure(figsize=(10, 8))
        
        for model_name, metrics in self.results.items():
            fpr, tpr, _ = roc_curve(y_test, metrics['y_prob'])
            auc = metrics['roc_auc']
            plt.plot(fpr, tpr, label=f'{model_name} (AUC = {auc:.4f})', linewidth=2)
        
        plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate', fontsize=12)
        plt.ylabel('True Positive Rate', fontsize=12)
        plt.title('Curvas ROC - Comparación de Modelos', fontsize=14)
        plt.legend(loc='lower right', fontsize=10)
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig('roc_curves_comparison.png', dpi=300)
        plt.show()
        
        print("\n✓ Curvas ROC guardadas como: roc_curves_comparison.png")
    
    def train_and_evaluate(self, X_train, X_test, y_train, y_test):
        """
        Entrena y evalúa múltiples modelos.
        
        Args:
            X_train (array): Features de entrenamiento.
            X_test (array): Features de test.
            y_train (array): Target de entrenamiento.
            y_test (array): Target de test.
        """
        print("\n" + "="*60)
        print("ENTRENAMIENTO Y EVALUACIÓN DE MODELOS")
        print("="*60)
        
        # Manejo del desbalanceo con SMOTE (Oversampling)
        print("\n[1/3] Detectando desbalanceo en la variable objetivo...")
        fraud_counts = pd.Series(y_train).value_counts()
        fraud_pct = pd.Series(y_train).value_counts(normalize=True) * 100
        
        print(f"  Distribución original:")
        print(f"    • Clase 0 (No Fraude): {fraud_counts.get(0, 0):,} ({fraud_pct.get(0, 0):.2f}%)")
        print(f"    • Clase 1 (Fraude):    {fraud_counts.get(1, 0):,} ({fraud_pct.get(1, 0):.2f}%)")
        
        # Verificar si hay desbalanceo significativo
        if len(fraud_counts) == 2:
            ratio = fraud_counts.max() / fraud_counts.min()
            print(f"    • Ratio de desbalanceo: 1:{ratio:.1f}")
            
            if ratio > 2:  # Si el ratio es mayor a 2:1, aplicar SMOTE
                print(f"\n  ⚠️ Desbalanceo detectado (ratio > 2:1)")
                print(f"  🔄 Aplicando SMOTE (Oversampling) para balancear clases...")
                
                smote = SMOTE(random_state=self.random_state)
                X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
                
                balanced_counts = pd.Series(y_train_res).value_counts()
                balanced_pct = pd.Series(y_train_res).value_counts(normalize=True) * 100
                
                print(f"  ✅ Datos balanceados con SMOTE:")
                print(f"    • Clase 0 (No Fraude): {balanced_counts.get(0, 0):,} ({balanced_pct.get(0, 0):.2f}%)")
                print(f"    • Clase 1 (Fraude):    {balanced_counts.get(1, 0):,} ({balanced_pct.get(1, 0):.2f}%)")
                print(f"    • Shape resultante: {X_train_res.shape}")
            else:
                print(f"\n  ✓ No se requiere balanceo (ratio aceptable)")
                X_train_res, y_train_res = X_train, y_train
        else:
            print(f"\n  ⚠️ Advertencia: Solo se detectó una clase en los datos")
            X_train_res, y_train_res = X_train, y_train
        
        # Construir modelos
        print("\n[2/3] Entrenando modelos...")
        models = self.build_models()
        
        for i, (name, model) in enumerate(models.items(), 1):
            print(f"\n{'='*60}")
            print(f"[{i}/{len(models)}] Entrenando: {name}")
            print(f"{'='*60}")
            
            # Entrenar
            model.fit(X_train_res, y_train_res)
            print(f"  ✓ Modelo entrenado")
            
            # Predecir
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1]
            
            # Evaluar
            auc = self.summarize_classification(name, y_test, y_pred, y_prob)
            
            # Actualizar mejor modelo
            if auc > self.best_auc:
                self.best_auc = auc
                self.best_model = model
                self.best_model_name = name
        
        # Comparación final
        print("\n[3/3] Generando comparación de modelos...")
        self.plot_roc_curves(y_test)
        
        print("\n" + "="*60)
        print("SELECCIÓN DEL MEJOR MODELO")
        print("="*60)
        print(f"\n🏆 Mejor modelo: {self.best_model_name}")
        print(f"   ROC-AUC: {self.best_auc:.4f}")
        
        # Tabla comparativa
        print("\n📊 TABLA COMPARATIVA DE MODELOS:")
        comparison_df = pd.DataFrame(self.results).T[['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']]
        print(comparison_df.to_string())
        
        # Guardar el mejor modelo
        joblib.dump(self.best_model, config.MODEL_PATH)
        print(f"\n✓ Mejor modelo guardado en: {config.MODEL_PATH}")
    
    def run_pipeline(self):
        """
        Ejecuta el pipeline completo de extremo a extremo (E2E).
        """
        print("\n" + "="*80)
        print(" "*20 + "PIPELINE MLOps - DETECCIÓN DE FRAUDE")
        print("="*80)
        
        # Paso 1: Cargar datos
        print("\n[PASO 1/4] CARGANDO DATOS...")
        df = self.loader.load_data()
        
        if df.empty:
            print("✗ Error: No se pudieron cargar los datos. Pipeline abortado.")
            return
        
        # Paso 2: Validar datos
        print("\n[PASO 2/4] VALIDANDO DATOS...")
        if not self.validator.validate_data(df):
            print("✗ Error: Los datos no pasaron la validación. Pipeline abortado.")
            return
        
        # Paso 3: Ingeniería de características
        print("\n[PASO 3/4] APLICANDO INGENIERÍA DE CARACTERÍSTICAS...")
        X_train, X_test, y_train, y_test = self.engineer.process(df)
        
        # Paso 4: Entrenar y evaluar modelos
        print("\n[PASO 4/4] ENTRENANDO Y EVALUANDO MODELOS...")
        self.train_and_evaluate(X_train, X_test, y_train, y_test)
        
        print("\n" + "="*80)
        print(" "*25 + "✅ PIPELINE COMPLETADO CON ÉXITO")
        print("="*80)


if __name__ == "__main__":
    """
    Punto de entrada principal para ejecutar el pipeline completo.
    Uso: python -m mlops_pipeline.src.model_training_evaluation
    """
    import sys
    import io
    
    # Configurar salida UTF-8 para emojis en Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("\n" + "="*80)
    print("    Iniciando Pipeline MLOps de Detección de Fraude")
    print("="*80 + "\n")
    
    trainer = ModelTrainer()
    trainer.run_pipeline()
    
    print("\n" + "="*80)
    print("    Pipeline finalizado exitosamente")
    print("="*80 + "\n")
