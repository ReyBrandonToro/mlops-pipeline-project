"""
Módulo para carga de datos del dataset de fraude financiero.
Define la clase DataLoader que se encarga de cargar y limpiar inicialmente los datos.
"""

import pandas as pd
try:
    from mlops_pipeline.src import config
except ImportError:
    from . import config


class DataLoader:
    """
    Clase responsable de cargar el dataset y realizar la limpieza inicial.
    """
    
    def __init__(self):
        """Inicializa el DataLoader con las configuraciones del archivo config.py"""
        self.data_path = config.DATA_PATH
        self.irrelevant_cols = config.IRRELEVANT_COLS
    
    def load_data(self) -> pd.DataFrame:
        """
        Carga los datos desde el archivo CSV y elimina columnas irrelevantes.
        
        Returns:
            pd.DataFrame: DataFrame con los datos cargados y limpiados.
        """
        try:
            print(f"Cargando datos desde: {self.data_path}")
            df = pd.read_csv(self.data_path)
            print(f"✓ Datos cargados exitosamente. Shape: {df.shape}")
            
            # Eliminar columnas irrelevantes
            df = df.drop(columns=self.irrelevant_cols, errors='ignore')
            print(f"✓ Columnas irrelevantes eliminadas: {self.irrelevant_cols}")
            print(f"✓ Shape final: {df.shape}")
            
            return df
            
        except FileNotFoundError:
            print(f"✗ Error: No se encontró el archivo en {self.data_path}")
            print("  Asegúrate de que el archivo 'financial_fraud_dataset.csv' esté en la raíz del proyecto.")
            return pd.DataFrame()
        
        except Exception as e:
            print(f"✗ Error inesperado al cargar datos: {str(e)}")
            return pd.DataFrame()


if __name__ == "__main__":
    # Prueba del módulo
    loader = DataLoader()
    df = loader.load_data()
    
    if not df.empty:
        print("\n" + "="*50)
        print("RESUMEN DE LOS DATOS CARGADOS")
        print("="*50)
        print(f"\nPrimeras 5 filas:")
        print(df.head())
        print(f"\nInformación del DataFrame:")
        print(df.info())
