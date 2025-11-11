"""Dashboard Streamlit para detección de fraude."""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import joblib
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from mlops_pipeline.src import cargar_datos, data_validation, config
except ImportError:
    import cargar_datos, data_validation, config

st.set_page_config(page_title="Detección de Fraude", page_icon="", layout="wide")

@st.cache_data
def cargar_dataset():
    try:
        loader = cargar_datos.DataLoader()
        df = loader.load_data()
        if df.empty:
            return None, "No se pudo cargar el dataset"
        return df, None
    except Exception as e:
        return None, str(e)

def ejecutar_validacion(df):
    try:
        validator = data_validation.DataValidator(df)
        return validator.validar_todo(), None
    except Exception as e:
        return None, str(e)

def cargar_modelo_y_preprocessor():
    try:
        model_path = project_root / "best_model.joblib"
        preprocessor_path = project_root / "preprocessor.joblib"
        if not model_path.exists():
            return None, None, "Modelo no encontrado"
        modelo = joblib.load(model_path)
        preprocessor = joblib.load(preprocessor_path) if preprocessor_path.exists() else None
        return modelo, preprocessor, None
    except Exception as e:
        return None, None, str(e)

def main():
    st.title(" Sistema de Detección de Fraude")
    st.markdown("---")
    
    with st.sidebar:
        st.title(" Navegación")
        opcion = st.radio("Selecciona:", [" Resumen", " Datos", " Validación", " Features", " Modelo", " Predicción"])
        st.info(f"**Fecha:** {datetime.now().strftime('%d/%m/%Y')}")
    
    if opcion == " Resumen":
        st.header("Resumen del Sistema")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(" Dataset", "10,000")
        with col2:
            st.metric(" Fraude", "1.88%")
        with col3:
            st.metric(" Modelo", "" if (project_root / "best_model.joblib").exists() else "")
        
        st.markdown("---")
        pipeline = [
            {"Paso": "Carga", "Estado": ""},
            {"Paso": "Validación", "Estado": ""},
            {"Paso": "Features", "Estado": ""},
            {"Paso": "SMOTE", "Estado": ""},
            {"Paso": "Entrenamiento", "Estado": ""}
        ]
        st.dataframe(pd.DataFrame(pipeline), use_container_width=True, hide_index=True)
    
    elif opcion == " Datos":
        st.header(" Carga de Datos")
        df, error = cargar_dataset()
        if error:
            st.error(f" {error}")
            return
        st.success(f" {len(df):,} registros")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Registros", f"{len(df):,}")
        with col2:
            fraud = df['isFraud'].sum()
            st.metric("Fraudes", f"{fraud:,}")
        with col3:
            st.metric("% Fraude", f"{(fraud/len(df)*100):.2f}%")
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            dist = df['isFraud'].value_counts()
            fig = px.bar(x=['No Fraude', 'Fraude'], y=dist.values, title='Distribución')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.pie(values=dist.values, names=['No Fraude', 'Fraude'], title='Proporción')
            st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df.head(50), use_container_width=True)
    
    elif opcion == " Validación":
        st.header(" Validación")
        df, error = cargar_dataset()
        if error:
            st.error(f" {error}")
            return
        
        resultados, error = ejecutar_validacion(df)
        if error:
            st.error(f" {error}")
            return
        
        total = len(resultados)
        passed = sum(1 for r in resultados.values() if r['passed'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Pasadas", f"{passed}/{total}")
        with col2:
            st.metric("Éxito", f"{(passed/total*100):.1f}%")
        
        for nombre, resultado in resultados.items():
            with st.expander(f"{'' if resultado['passed'] else ''} {nombre}"):
                st.write(resultado['message'])
    
    elif opcion == " Features":
        st.header(" Features")
        features = [
            {"Feature": "TransactionHour", "Descripción": "Hora (0-23)"},
            {"Feature": "AccountAge", "Descripción": "Edad cuenta"},
            {"Feature": "TransactionAmountLog", "Descripción": "Log monto"}
        ]
        st.dataframe(pd.DataFrame(features), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.subheader("Balanceo SMOTE")
        col1, col2 = st.columns(2)
        with col1:
            fig = go.Figure(data=[go.Bar(x=['No Fraude', 'Fraude'], y=[9812, 188])])
            fig.update_layout(title='Antes')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = go.Figure(data=[go.Bar(x=['No Fraude', 'Fraude'], y=[9812, 9812])])
            fig.update_layout(title='Después')
            st.plotly_chart(fig, use_container_width=True)
    
    elif opcion == " Modelo":
        st.header(" Modelo")
        modelo, preprocessor, error = cargar_modelo_y_preprocessor()
        if error:
            st.warning(f" {error}")
            return
        
        st.success(" Modelo cargado")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Modelo", "LogisticRegression")
        with col2:
            st.metric("ROC-AUC", "0.5581")
        with col3:
            size = (project_root / "best_model.joblib").stat().st_size / 1024
            st.metric("Tamaño", f"{size:.0f} KB")
        
        modelos = [
            {"Modelo": "LogisticRegression", "ROC-AUC": 0.5581, "": ""},
            {"Modelo": "RandomForest", "ROC-AUC": 0.5234, "": ""},
            {"Modelo": "XGBoost", "ROC-AUC": 0.5456, "": ""}
        ]
        st.dataframe(pd.DataFrame(modelos), use_container_width=True, hide_index=True)
    
    elif opcion == " Predicción":
        st.header(" Predicción")
        modelo, preprocessor, error = cargar_modelo_y_preprocessor()
        if error:
            st.warning(f" {error}")
            return
        
        st.info(" Ingresa los datos")
        
        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input(" Monto", 0.0, 100000.0, 500.0)
            trans_type = st.selectbox("Tipo", ["PAYMENT", "TRANSFER", "CASH_OUT", "DEBIT", "CASH_IN"])
            old_bal_orig = st.number_input("Balance Inicial Origen", 0.0, 1000000.0, 10000.0)
            new_bal_orig = st.number_input("Nuevo Balance Origen", 0.0, 1000000.0, old_bal_orig - amount)
        
        with col2:
            old_bal_dest = st.number_input("Balance Inicial Destino", 0.0, 1000000.0, 5000.0)
            new_bal_dest = st.number_input("Nuevo Balance Destino", 0.0, 1000000.0, old_bal_dest + amount)
            trans_hour = st.slider("Hora", 0, 23, 14)
            account_age = st.number_input("Edad Cuenta (días)", 0, 3650, 365)
        
        if st.button(" PREDECIR", use_container_width=True):
            datos = pd.DataFrame({
                'TransactionAmount': [amount],
                'oldbalanceOrg': [old_bal_orig],
                'newbalanceOrig': [new_bal_orig],
                'oldbalanceDest': [old_bal_dest],
                'newbalanceDest': [new_bal_dest],
                'TransactionHour': [trans_hour],
                'AccountAge': [account_age],
                'TransactionAmountLog': [np.log1p(amount)],
                'type': [trans_type]
            })
            
            try:
                if preprocessor:
                    datos_proc = preprocessor.transform(datos)
                else:
                    from sklearn.preprocessing import LabelEncoder
                    le = LabelEncoder()
                    datos_copy = datos.copy()
                    datos_copy['type'] = le.fit_transform(datos_copy['type'])
                    datos_proc = datos_copy.values
                
                pred = modelo.predict(datos_proc)[0]
                prob = modelo.predict_proba(datos_proc)[0]
                
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if pred == 1:
                        st.error(" FRAUDE")
                    else:
                        st.success(" LEGÍTIMO")
                with col2:
                    st.metric("Prob. Fraude", f"{prob[1]:.1%}")
                with col3:
                    riesgo = " ALTO" if prob[1] > 0.7 else " MEDIO" if prob[1] > 0.3 else " BAJO"
                    st.metric("Riesgo", riesgo)
                
                fig = go.Figure(data=[
                    go.Bar(x=['No Fraude', 'Fraude'], y=[prob[0], prob[1]], 
                           text=[f'{prob[0]:.1%}', f'{prob[1]:.1%}'], textposition='auto')
                ])
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f" Error: {str(e)}")

if __name__ == "__main__":
    main()
