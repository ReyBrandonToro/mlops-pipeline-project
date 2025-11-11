"""
Módulo de ingeniería de características.
Define la clase FeatureEngineer que crea features, divide datos y aplica preprocesamiento.
"""

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
try:
    from mlops_pipeline.src import config
except ImportError:
    from . import config


class FeatureEngineer:
    """
    Clase responsable de la ingeniería de características y preprocesamiento de datos.
    Crea features derivados, divide los datos y aplica transformaciones.
    """
    
    def __init__(self, random_state=None):
        """
        Inicializa el FeatureEngineer.
        
        Args:
            random_state (int, optional): Semilla para reproducibilidad. 
                                         Si es None, usa el valor de config.RANDOM_STATE.
        """
        self.random_state = random_state if random_state is not None else config.RANDOM_STATE
        self.preprocessor = None
        self.feature_names = None
    
    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Crea features derivados basados en el análisis exploratorio.
        
        Args:
            df (pd.DataFrame): DataFrame original.
            
        Returns:
            pd.DataFrame: DataFrame con features adicionales.
        """
        print("\n" + "="*60)
        print("CREANDO FEATURES DERIVADOS")
        print("="*60)
        
        df = df.copy()
        
        # Feature 1: Amount per transaction ratio
        # Ratio de cantidad por transacción previa
        if all(col in df.columns for col in ['amount', 'previous_transactions']):
            df['amount_per_transaction'] = df['amount'] / (df['previous_transactions'] + 1)
            print("  ✓ Feature creado: 'amount_per_transaction'")
        
        # Feature 2: Age group (categorización de edad)
        if 'customer_age' in df.columns:
            df['age_group'] = pd.cut(df['customer_age'], 
                                     bins=[0, 25, 35, 50, 100], 
                                     labels=['young', 'adult', 'middle_age', 'senior'])
            df['age_group'] = df['age_group'].astype(str)
            print("  ✓ Feature creado: 'age_group'")
        
        # Feature 3: High amount flag (transacciones de monto alto)
        if 'amount' in df.columns:
            amount_threshold = df['amount'].quantile(0.75)
            df['high_amount'] = (df['amount'] > amount_threshold).astype(int)
            print("  ✓ Feature creado: 'high_amount'")
        
        print(f"\n  Shape después de crear features: {df.shape}")
        return df
    
    def _create_preprocessor(self, df: pd.DataFrame) -> ColumnTransformer:
        """
        Crea el pipeline de preprocesamiento.
        
        Args:
            df (pd.DataFrame): DataFrame con todas las features.
            
        Returns:
            ColumnTransformer: Preprocesador configurado.
        """
        # Identificar todas las columnas numéricas (originales + derivadas)
        numerical_features = config.NUMERICAL_COLS.copy()
        
        # Agregar features derivados si existen
        derived_features = ['errorBalanceOrg', 'transactionRatio', 'zeroBalanceAfter']
        for feat in derived_features:
            if feat in df.columns:
                numerical_features.append(feat)
        
        # Pipeline para features numéricas
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        
        # Pipeline para features categóricas
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])
        
        # Combinar transformadores
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numerical_features),
                ('cat', categorical_transformer, config.CATEGORICAL_COLS)
            ],
            remainder='drop'  # Eliminar columnas no especificadas
        )
        
        return preprocessor
    
    def process(self, df: pd.DataFrame, test_size=None):
        """
        Aplica ingeniería de características y preprocesamiento completo.
        
        Args:
            df (pd.DataFrame): DataFrame original.
            test_size (float, optional): Proporción del conjunto de test. 
                                        Si es None, usa config.TEST_SIZE.
        
        Returns:
            tuple: (X_train_processed, X_test_processed, y_train, y_test)
        """
        print("\n" + "="*60)
        print("INICIANDO PROCESAMIENTO DE DATOS")
        print("="*60)
        
        test_size = test_size if test_size is not None else config.TEST_SIZE
        
        # Paso 1: Crear features derivados
        df_with_features = self.create_features(df)
        
        # Paso 2: Separar features y target
        print("\n[1/4] Separando features y variable objetivo...")
        X = df_with_features.drop(config.TARGET_VARIABLE, axis=1)
        y = df_with_features[config.TARGET_VARIABLE]
        print(f"  ✓ Features shape: {X.shape}")
        print(f"  ✓ Target shape: {y.shape}")
        print(f"  ✓ Distribución del target: {y.value_counts().to_dict()}")
        
        # Paso 3: División train/test estratificada
        print(f"\n[2/4] Dividiendo datos (test_size={test_size}, stratified)...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=test_size, 
            random_state=self.random_state, 
            stratify=y
        )
        print(f"  ✓ Train set: {X_train.shape}")
        print(f"  ✓ Test set: {X_test.shape}")
        
        # Paso 4: Crear y ajustar el preprocesador SOLO con datos de entrenamiento
        print("\n[3/4] Creando y ajustando preprocesador...")
        self.preprocessor = self._create_preprocessor(X_train)
        self.preprocessor.fit(X_train)
        print("  ✓ Preprocesador ajustado con datos de entrenamiento")
        
        # Guardar el preprocesador
        joblib.dump(self.preprocessor, config.PREPROCESSOR_PATH)
        print(f"  ✓ Preprocesador guardado en: {config.PREPROCESSOR_PATH}")
        
        # Paso 5: Transformar datos
        print("\n[4/4] Aplicando transformaciones...")
        X_train_processed = self.preprocessor.transform(X_train)
        X_test_processed = self.preprocessor.transform(X_test)
        print(f"  ✓ Train transformado shape: {X_train_processed.shape}")
        print(f"  ✓ Test transformado shape: {X_test_processed.shape}")
        
        print("\n" + "="*60)
        print("✓ PROCESAMIENTO COMPLETADO")
        print("="*60 + "\n")
        
        return X_train_processed, X_test_processed, y_train, y_test
    
    def transform_new_data(self, df: pd.DataFrame):
        """
        Transforma nuevos datos usando el preprocesador ya ajustado.
        Útil para datos de producción.
        
        Args:
            df (pd.DataFrame): Nuevos datos a transformar.
            
        Returns:
            np.ndarray: Datos transformados.
        """
        if self.preprocessor is None:
            try:
                self.preprocessor = joblib.load(config.PREPROCESSOR_PATH)
                print(f"✓ Preprocesador cargado desde: {config.PREPROCESSOR_PATH}")
            except FileNotFoundError:
                raise ValueError(
                    "No se encontró el preprocesador. "
                    "Ejecuta primero el método 'process()' para entrenar el preprocesador."
                )
        
        # Crear features en los nuevos datos
        df_with_features = self.create_features(df)
        
        # Si tiene la variable objetivo, eliminarla
        if config.TARGET_VARIABLE in df_with_features.columns:
            df_with_features = df_with_features.drop(config.TARGET_VARIABLE, axis=1)
        
        # Transformar
        X_transformed = self.preprocessor.transform(df_with_features)
        
        return X_transformed


if __name__ == "__main__":
    # Prueba del módulo
    from mlops_pipeline.src.cargar_datos import DataLoader
    from mlops_pipeline.src.data_validation import DataValidator
    
    print("="*60)
    print("PRUEBA DEL MÓDULO DE INGENIERÍA DE CARACTERÍSTICAS")
    print("="*60)
    
    # Cargar y validar datos
    loader = DataLoader()
    df = loader.load_data()
    
    if not df.empty:
        validator = DataValidator()
        if validator.validate_data(df):
            # Aplicar ingeniería de características
            engineer = FeatureEngineer()
            X_train, X_test, y_train, y_test = engineer.process(df)
            
            print("\n" + "="*60)
            print("RESUMEN FINAL")
            print("="*60)
            print(f"X_train shape: {X_train.shape}")
            print(f"X_test shape: {X_test.shape}")
            print(f"y_train shape: {y_train.shape}")
            print(f"y_test shape: {y_test.shape}")
            print("\n✅ Prueba completada exitosamente!")
