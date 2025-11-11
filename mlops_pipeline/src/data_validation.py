"""
Módulo de validación de datos.
Define la clase DataValidator que valida esquema, tipos, nulos y reglas de negocio.
"""

import pandas as pd
try:
    from mlops_pipeline.src import config
except ImportError:
    from . import config


class DataValidator:
    """
    Clase responsable de validar la calidad e integridad de los datos.
    Implementa validaciones de esquema, tipos, nulos y reglas de negocio.
    """
    
    def __init__(self):
        """Inicializa el validador con las configuraciones del proyecto."""
        self.numerical_cols = config.NUMERICAL_COLS
        self.categorical_cols = config.CATEGORICAL_COLS
        self.expected_cols = self.numerical_cols + self.categorical_cols + [config.TARGET_VARIABLE]
        self.allowed_types = config.ALLOWED_TYPES
        self.target_variable = config.TARGET_VARIABLE
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """
        Ejecuta todas las validaciones sobre el DataFrame.
        
        Args:
            df (pd.DataFrame): DataFrame a validar.
            
        Returns:
            bool: True si todas las validaciones pasan, False en caso contrario.
        """
        print("\n" + "="*60)
        print("INICIANDO VALIDACIÓN DE DATOS")
        print("="*60)
        
        try:
            self.validate_schema(df)
            self.validate_types(df)
            self.validate_nulls(df)
            self.validate_business_rules(df)
            
            print("\n" + "="*60)
            print("✓ VALIDACIÓN EXITOSA - Todos los checks pasaron")
            print("="*60 + "\n")
            return True
            
        except (ValueError, TypeError) as e:
            print("\n" + "="*60)
            print(f"✗ VALIDACIÓN FALLIDA: {str(e)}")
            print("="*60 + "\n")
            return False
    
    def validate_schema(self, df: pd.DataFrame):
        """
        Valida que las columnas esperadas existan en el DataFrame.
        
        Args:
            df (pd.DataFrame): DataFrame a validar.
            
        Raises:
            ValueError: Si faltan columnas esperadas.
        """
        print("\n[1/4] Validando esquema (columnas esperadas)...")
        missing_cols = [col for col in self.expected_cols if col not in df.columns]
        
        if missing_cols:
            raise ValueError(f"Faltan columnas en el DataFrame: {missing_cols}")
        
        print(f"  ✓ Todas las columnas esperadas están presentes: {self.expected_cols}")
    
    def validate_types(self, df: pd.DataFrame):
        """
        Valida los tipos de datos de las columnas.
        
        Args:
            df (pd.DataFrame): DataFrame a validar.
            
        Raises:
            TypeError: Si alguna columna no tiene el tipo esperado.
        """
        print("\n[2/4] Validando tipos de datos...")
        
        # Validar columnas numéricas
        for col in self.numerical_cols:
            if col in df.columns:
                if not pd.api.types.is_numeric_dtype(df[col]):
                    raise TypeError(f"Columna '{col}' debe ser numérica, pero es {df[col].dtype}")
        
        print(f"  ✓ Columnas numéricas validadas: {self.numerical_cols}")
        
        # Validar columnas categóricas
        for col in self.categorical_cols:
            if col in df.columns:
                if not (pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_categorical_dtype(df[col])):
                    raise TypeError(f"Columna '{col}' debe ser categórica/object, pero es {df[col].dtype}")
        
        print(f"  ✓ Columnas categóricas validadas: {self.categorical_cols}")
    
    def validate_nulls(self, df: pd.DataFrame):
        """
        Valida que no haya valores nulos en el DataFrame.
        
        Args:
            df (pd.DataFrame): DataFrame a validar.
            
        Raises:
            ValueError: Si se encuentran valores nulos.
        """
        print("\n[3/4] Validando valores nulos...")
        
        null_counts = df.isnull().sum()
        total_nulls = null_counts.sum()
        
        if total_nulls > 0:
            print(f"  Valores nulos encontrados por columna:")
            for col, count in null_counts[null_counts > 0].items():
                print(f"    - {col}: {count} nulos")
            raise ValueError(f"Se encontraron {total_nulls} valores nulos en el DataFrame.")
        
        print(f"  ✓ No se encontraron valores nulos")
    
    def validate_business_rules(self, df: pd.DataFrame):
        """
        Valida reglas de negocio específicas identificadas en el EDA.
        
        Args:
            df (pd.DataFrame): DataFrame a validar.
            
        Raises:
            ValueError: Si alguna regla de negocio no se cumple.
        """
        print("\n[4/4] Validando reglas de negocio...")
        
        # Regla 1: 'amount' no puede ser negativo
        if 'amount' in df.columns:
            negative_amounts = (df['amount'] < 0).sum()
            if negative_amounts > 0:
                raise ValueError(f"Se encontraron {negative_amounts} valores negativos en 'amount'.")
            print(f"  ✓ Regla 1: 'amount' >= 0 (todas las transacciones son válidas)")
        
        # Regla 2: 'customer_age' debe estar en un rango válido (18-100)
        if 'customer_age' in df.columns:
            invalid_age = ((df['customer_age'] < 18) | (df['customer_age'] > 100)).sum()
            if invalid_age > 0:
                raise ValueError(f"Se encontraron {invalid_age} edades inválidas (fuera del rango 18-100).")
            print(f"  ✓ Regla 2: 'customer_age' está en rango válido (18-100)")
        
        # Regla 3: Variable objetivo debe ser binaria (0 o 1)
        if self.target_variable in df.columns:
            unique_targets = df[self.target_variable].unique()
            if not all(val in [0, 1] for val in unique_targets):
                raise ValueError(
                    f"Variable objetivo '{self.target_variable}' debe ser binaria (0 o 1), "
                    f"pero contiene: {unique_targets}"
                )
            print(f"  ✓ Regla 3: '{self.target_variable}' es binaria (0, 1)")
        
        # Regla 4: previous_transactions no puede ser negativo
        if 'previous_transactions' in df.columns:
            negative_trans = (df['previous_transactions'] < 0).sum()
            if negative_trans > 0:
                raise ValueError(f"Se encontraron {negative_trans} valores negativos en 'previous_transactions'.")
            print(f"  ✓ Regla 4: 'previous_transactions' >= 0")



if __name__ == "__main__":
    # Prueba del módulo
    from mlops_pipeline.src.cargar_datos import DataLoader
    
    print("Cargando datos para prueba de validación...")
    loader = DataLoader()
    df = loader.load_data()
    
    if not df.empty:
        validator = DataValidator()
        resultado = validator.validate_data(df)
        
        if resultado:
            print("\n✅ El dataset pasó todas las validaciones!")
        else:
            print("\n❌ El dataset NO pasó las validaciones.")
