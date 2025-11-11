"""
Módulo de monitoreo del modelo con Streamlit.
Dashboard interactivo para detectar data drift en producción.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ks_2samp, chi2_contingency
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from mlops_pipeline.src import config
except ImportError:
    try:
        from . import config
    except ImportError:
        import config


# ==================== CONFIGURACIÓN DE LA PÁGINA ====================

st.set_page_config(
    page_title="Dashboard de Monitoreo - Detección de Fraude",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ESTILOS PERSONALIZADOS ====================

st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .alert-danger {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .alert-success {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)


# ==================== FUNCIONES AUXILIARES ====================

@st.cache_data
def load_baseline_data():
    """
    Carga los datos históricos (baseline) para comparación.
    """
    try:
        df = pd.read_csv(config.DATA_PATH)
        # Eliminar columnas irrelevantes
        df = df.drop(columns=config.IRRELEVANT_COLS, errors='ignore')
        return df
    except FileNotFoundError:
        st.error(f"❌ Error: No se encontró el archivo baseline en '{config.DATA_PATH}'")
        return None
    except Exception as e:
        st.error(f"❌ Error al cargar datos baseline: {str(e)}")
        return None


def calculate_drift_metrics(baseline_df, current_df):
    """
    Calcula métricas de drift para todas las variables.
    """
    drift_results = {
        'numerical': {},
        'categorical': {}
    }
    
    # Drift en variables numéricas (Test de Kolmogorov-Smirnov)
    for col in config.NUMERICAL_COLS:
        if col in baseline_df.columns and col in current_df.columns:
            ks_stat, p_value = ks_2samp(baseline_df[col], current_df[col])
            drift_results['numerical'][col] = {
                'statistic': ks_stat,
                'p_value': p_value,
                'drift_detected': p_value < config.KS_THRESHOLD
            }
    
    # Drift en variables categóricas (Test de Chi-cuadrado)
    for col in config.CATEGORICAL_COLS:
        if col in baseline_df.columns and col in current_df.columns:
            baseline_counts = baseline_df[col].value_counts()
            current_counts = current_df[col].value_counts()
            
            # Crear tabla de contingencia
            all_categories = set(baseline_counts.index) | set(current_counts.index)
            contingency_table = pd.DataFrame({
                'Baseline': [baseline_counts.get(cat, 0) for cat in all_categories],
                'Current': [current_counts.get(cat, 0) for cat in all_categories]
            }, index=list(all_categories))
            
            try:
                chi2_stat, p_value, _, _ = chi2_contingency(contingency_table.T)
                drift_results['categorical'][col] = {
                    'statistic': chi2_stat,
                    'p_value': p_value,
                    'drift_detected': p_value < config.CHI2_THRESHOLD,
                    'contingency_table': contingency_table
                }
            except Exception as e:
                st.warning(f"⚠️ No se pudo calcular Chi-cuadrado para '{col}': {str(e)}")
    
    return drift_results


def plot_distribution_comparison(baseline_df, current_df, column, plot_type='kde'):
    """
    Genera gráfico comparativo de distribuciones.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if plot_type == 'kde':
        # KDE Plot
        baseline_df[column].plot(kind='kde', ax=ax, label='Histórico (Baseline)', 
                                 color='blue', linewidth=2, alpha=0.7)
        current_df[column].plot(kind='kde', ax=ax, label='Actual (Producción)', 
                                color='red', linewidth=2, alpha=0.7)
    else:
        # Histogram
        ax.hist(baseline_df[column], bins=50, alpha=0.5, label='Histórico', 
                color='blue', density=True)
        ax.hist(current_df[column], bins=50, alpha=0.5, label='Actual', 
                color='red', density=True)
    
    ax.set_title(f'Comparación de Distribuciones - {column}', fontsize=14, fontweight='bold')
    ax.set_xlabel(column, fontsize=12)
    ax.set_ylabel('Densidad', fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    
    return fig


def save_drift_history(drift_results, drift_count, total_variables):
    """
    Guarda el historial de drift para análisis temporal.
    """
    history_file = "drift_history.json"
    
    # Crear entrada de historial
    history_entry = {
        'timestamp': datetime.now().isoformat(),
        'drift_count': drift_count,
        'total_variables': total_variables,
        'drift_percentage': (drift_count / total_variables * 100) if total_variables > 0 else 0,
        'variables_with_drift': []
    }
    
    # Agregar variables con drift
    for var, result in drift_results['numerical'].items():
        if result['drift_detected']:
            history_entry['variables_with_drift'].append({
                'variable': var,
                'type': 'numerical',
                'p_value': result['p_value'],
                'statistic': result['statistic']
            })
    
    for var, result in drift_results['categorical'].items():
        if result['drift_detected']:
            history_entry['variables_with_drift'].append({
                'variable': var,
                'type': 'categorical',
                'p_value': result['p_value'],
                'statistic': result['statistic']
            })
    
    # Cargar historial existente
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r') as f:
                history = json.load(f)
        except:
            history = []
    else:
        history = []
    
    # Agregar nueva entrada
    history.append(history_entry)
    
    # Mantener solo últimos 100 registros
    history = history[-100:]
    
    # Guardar historial actualizado
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)
    
    return history


def load_drift_history():
    """
    Carga el historial de drift.
    """
    history_file = "drift_history.json"
    
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r') as f:
                return json.load(f)
        except:
            return []
    return []


def plot_drift_evolution(history):
    """
    Grafica la evolución del drift a lo largo del tiempo.
    """
    if not history or len(history) < 2:
        return None
    
    df_history = pd.DataFrame(history)
    df_history['timestamp'] = pd.to_datetime(df_history['timestamp'])
    df_history = df_history.sort_values('timestamp')
    
    fig = go.Figure()
    
    # Línea de evolución del porcentaje de drift
    fig.add_trace(go.Scatter(
        x=df_history['timestamp'],
        y=df_history['drift_percentage'],
        mode='lines+markers',
        name='% Drift',
        line=dict(color='red', width=2),
        marker=dict(size=8)
    ))
    
    # Línea de umbral crítico (ejemplo: 20%)
    fig.add_hline(y=20, line_dash="dash", line_color="orange", 
                  annotation_text="Umbral de Alerta (20%)")
    
    fig.update_layout(
        title='Evolución del Data Drift en el Tiempo',
        xaxis_title='Fecha',
        yaxis_title='Porcentaje de Variables con Drift (%)',
        hovermode='x unified',
        height=400
    )
    
    return fig


def analyze_drift_trends(history):
    """
    Analiza tendencias en el historial de drift.
    """
    if not history or len(history) < 3:
        return {
            'trend': 'Datos insuficientes',
            'severity': 'info',
            'message': 'Se requieren al menos 3 mediciones para análisis de tendencias.'
        }
    
    df_history = pd.DataFrame(history)
    recent_drift = df_history.tail(3)['drift_percentage'].mean()
    older_drift = df_history.head(max(1, len(df_history) - 3))['drift_percentage'].mean()
    
    trend_change = recent_drift - older_drift
    
    if trend_change > 10:
        return {
            'trend': 'Aumento Abrupto',
            'severity': 'danger',
            'message': f'⚠️ **ALERTA CRÍTICA**: El drift ha aumentado {trend_change:.1f}% en las últimas mediciones. Se recomienda re-entrenamiento inmediato.'
        }
    elif trend_change > 5:
        return {
            'trend': 'Tendencia Creciente',
            'severity': 'warning',
            'message': f'⚠️ **ADVERTENCIA**: El drift está aumentando ({trend_change:.1f}%). Monitorear de cerca y preparar re-entrenamiento.'
        }
    elif trend_change < -10:
        return {
            'trend': 'Mejora Significativa',
            'severity': 'success',
            'message': f'✅ **POSITIVO**: El drift ha disminuido {abs(trend_change):.1f}%. El modelo está mejorando su estabilidad.'
        }
    elif abs(trend_change) < 2:
        return {
            'trend': 'Estable',
            'severity': 'info',
            'message': '✓ El drift se mantiene estable sin cambios significativos.'
        }
    else:
        return {
            'trend': 'Fluctuación Normal',
            'severity': 'info',
            'message': f'Variación de {trend_change:.1f}% está dentro de rangos normales.'
        }


def generate_detailed_recommendations(drift_results, drift_count, total_variables, trend_analysis):
    """
    Genera recomendaciones detalladas basadas en el análisis de drift.
    """
    recommendations = []
    critical_variables = []
    
    # Identificar variables críticas (p-value muy bajo)
    for var, result in drift_results['numerical'].items():
        if result['drift_detected'] and result['p_value'] < 0.01:
            critical_variables.append({'variable': var, 'p_value': result['p_value'], 'type': 'numérica'})
    
    for var, result in drift_results['categorical'].items():
        if result['drift_detected'] and result['p_value'] < 0.01:
            critical_variables.append({'variable': var, 'p_value': result['p_value'], 'type': 'categórica'})
    
    # Prioridad de recomendaciones
    drift_percentage = (drift_count / total_variables * 100) if total_variables > 0 else 0
    
    if drift_percentage > 50:
        recommendations.append({
            'priority': '🔴 CRÍTICA',
            'action': 'Re-entrenamiento Inmediato',
            'description': f'Más del 50% de las variables ({drift_count}/{total_variables}) muestran drift. El modelo está comprometido.',
            'steps': [
                '1. Detener predicciones en producción si es posible',
                '2. Recolectar datos actualizados',
                '3. Re-entrenar el modelo con datos recientes',
                '4. Validar performance antes de re-desplegar'
            ]
        })
    elif drift_percentage > 30:
        recommendations.append({
            'priority': '🟠 ALTA',
            'action': 'Planificar Re-entrenamiento',
            'description': f'{drift_count}/{total_variables} variables con drift. Acción requerida pronto.',
            'steps': [
                '1. Programar re-entrenamiento en las próximas 48-72 horas',
                '2. Investigar causas del drift',
                '3. Actualizar pipeline de datos si es necesario',
                '4. Aumentar frecuencia de monitoreo'
            ]
        })
    elif drift_percentage > 10:
        recommendations.append({
            'priority': '🟡 MEDIA',
            'action': 'Monitoreo Intensivo',
            'description': f'{drift_count}/{total_variables} variables con drift. Monitorear de cerca.',
            'steps': [
                '1. Aumentar frecuencia de monitoreo a diario',
                '2. Analizar patrones de drift',
                '3. Preparar datos para posible re-entrenamiento',
                '4. Documentar observaciones'
            ]
        })
    
    if critical_variables:
        recommendations.append({
            'priority': '⚠️ ATENCIÓN',
            'action': 'Variables Críticas Detectadas',
            'description': f'{len(critical_variables)} variable(s) con drift severo (p-value < 0.01)',
            'steps': [
                f'Variables afectadas: {", ".join([v["variable"] for v in critical_variables])}',
                'Investigar cambios en la fuente de datos',
                'Verificar procesos de ETL',
                'Validar calidad de datos de entrada'
            ]
        })
    
    # Recomendaciones basadas en tendencia
    if trend_analysis['severity'] == 'danger':
        recommendations.append({
            'priority': '🔴 URGENTE',
            'action': 'Tendencia Crítica Detectada',
            'description': trend_analysis['message'],
            'steps': [
                'El drift está acelerándose',
                'Revisar cambios recientes en datos de producción',
                'Considerar rollback a versión anterior del modelo',
                'Activar plan de contingencia'
            ]
        })
    
    return recommendations, critical_variables


# ==================== INTERFAZ PRINCIPAL ====================

def main():
    """
    Función principal del dashboard.
    """
    # Encabezado
    st.markdown('<p class="main-header">📊 Dashboard de Monitoreo de Data Drift</p>', 
                unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/artificial-intelligence.png", width=80)
        st.title("⚙️ Configuración")
        st.markdown("---")
        
        st.subheader("Umbrales de Detección")
        ks_threshold = st.slider(
            "Umbral KS (variables numéricas)", 
            min_value=0.01, 
            max_value=0.10, 
            value=config.KS_THRESHOLD, 
            step=0.01,
            help="Nivel de significancia para el test de Kolmogorov-Smirnov"
        )
        
        chi2_threshold = st.slider(
            "Umbral Chi² (variables categóricas)", 
            min_value=0.01, 
            max_value=0.10, 
            value=config.CHI2_THRESHOLD, 
            step=0.01,
            help="Nivel de significancia para el test de Chi-cuadrado"
        )
        
        st.markdown("---")
        st.info("💡 **Tip:** Valores p menores al umbral indican drift significativo")
    
    # Cargar datos baseline
    st.header("1️⃣ Datos de Referencia (Baseline)")
    baseline_df = load_baseline_data()
    
    if baseline_df is None:
        st.stop()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Registros", f"{len(baseline_df):,}")
    with col2:
        st.metric("Variables Numéricas", len(config.NUMERICAL_COLS))
    with col3:
        st.metric("Variables Categóricas", len(config.CATEGORICAL_COLS))
    
    with st.expander("🔍 Ver muestra de datos baseline"):
        st.dataframe(baseline_df.head(100))
    
    st.markdown("---")
    
    # Cargar datos actuales
    st.header("2️⃣ Datos de Producción (Actuales)")
    uploaded_file = st.file_uploader(
        "📁 Sube un archivo CSV con los datos de producción",
        type="csv",
        help="El archivo debe tener las mismas columnas que el dataset de entrenamiento"
    )
    
    if uploaded_file is not None:
        try:
            current_df = pd.read_csv(uploaded_file)
            current_df = current_df.drop(columns=config.IRRELEVANT_COLS, errors='ignore')
            
            st.success(f"✅ Datos cargados exitosamente: {len(current_df):,} registros")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Registros Actuales", f"{len(current_df):,}")
            with col2:
                fraud_rate = (current_df['isFraud'].sum() / len(current_df)) * 100 if 'isFraud' in current_df.columns else 0
                st.metric("Tasa de Fraude", f"{fraud_rate:.2f}%")
            with col3:
                st.metric("Período", datetime.now().strftime("%Y-%m-%d"))
            
            with st.expander("🔍 Ver muestra de datos actuales"):
                st.dataframe(current_df.head(100))
            
            st.markdown("---")
            
            # ==================== ANÁLISIS DE DRIFT ====================
            
            st.header("3️⃣ Análisis de Data Drift")
            
            # Calcular drift
            with st.spinner("🔄 Calculando métricas de drift..."):
                drift_results = calculate_drift_metrics(baseline_df, current_df)
            
            # Resumen de drift
            total_variables = len(config.NUMERICAL_COLS) + len(config.CATEGORICAL_COLS)
            drift_count = sum(1 for v in drift_results['numerical'].values() if v['drift_detected'])
            drift_count += sum(1 for v in drift_results['categorical'].values() if v['drift_detected'])
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Variables Analizadas", total_variables)
            with col2:
                st.metric("Con Drift Detectado", drift_count, delta=f"{(drift_count/total_variables)*100:.1f}%")
            with col3:
                st.metric("Sin Drift", total_variables - drift_count)
            with col4:
                status = "🔴 ALERTA" if drift_count > 0 else "🟢 ESTABLE"
                st.metric("Estado General", status)
            
            st.markdown("---")
            
            # ==================== ANÁLISIS TEMPORAL ====================
            
            st.header("🕒 Análisis Temporal del Drift")
            
            # Guardar historial actual
            history = save_drift_history(drift_results, drift_count, total_variables)
            
            if len(history) >= 2:
                st.success(f"📊 Se tienen {len(history)} mediciones en el historial")
                
                # Gráfico de evolución
                fig_evolution = plot_drift_evolution(history)
                if fig_evolution:
                    st.plotly_chart(fig_evolution, use_container_width=True)
                
                # Análisis de tendencias
                trend_analysis = analyze_drift_trends(history)
                
                if trend_analysis['severity'] == 'danger':
                    st.error(f"**{trend_analysis['trend']}**\n\n{trend_analysis['message']}")
                elif trend_analysis['severity'] == 'warning':
                    st.warning(f"**{trend_analysis['trend']}**\n\n{trend_analysis['message']}")
                elif trend_analysis['severity'] == 'success':
                    st.success(f"**{trend_analysis['trend']}**\n\n{trend_analysis['message']}")
                else:
                    st.info(f"**{trend_analysis['trend']}**\n\n{trend_analysis['message']}")
                
                # Tabla de historial
                with st.expander("📋 Ver historial completo de mediciones"):
                    df_history = pd.DataFrame(history)
                    df_history['timestamp'] = pd.to_datetime(df_history['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
                    df_history = df_history[['timestamp', 'drift_count', 'total_variables', 'drift_percentage']]
                    df_history.columns = ['Fecha/Hora', 'Variables con Drift', 'Total Variables', 'Porcentaje Drift (%)']
                    st.dataframe(df_history.sort_values('Fecha/Hora', ascending=False), use_container_width=True)
            else:
                st.info("📊 Se requieren al menos 2 mediciones para el análisis temporal. Este es el primer registro.")
            
            st.markdown("---")
            
            # ==================== RECOMENDACIONES DETALLADAS ====================
            
            st.header("4️⃣ Recomendaciones y Plan de Acción")
            
            # Generar recomendaciones
            recommendations, critical_vars = generate_detailed_recommendations(
                drift_results, drift_count, total_variables, 
                trend_analysis if len(history) >= 2 else {'severity': 'info', 'trend': 'N/A', 'message': 'Primer análisis'}
            )
            
            if recommendations:
                st.subheader("📋 Plan de Acción Recomendado")
                
                for i, rec in enumerate(recommendations, 1):
                    with st.expander(f"{rec['priority']} - {rec['action']}", expanded=(i == 1)):
                        st.markdown(f"**Descripción:** {rec['description']}")
                        st.markdown("**Pasos a seguir:**")
                        for step in rec['steps']:
                            st.markdown(f"- {step}")
            
            # Tabla de métricas de drift por variable
            st.subheader("📊 Tabla Resumen de Métricas de Drift")
            
            drift_summary = []
            
            for var, result in drift_results['numerical'].items():
                drift_summary.append({
                    'Variable': var,
                    'Tipo': 'Numérica',
                    'Test': 'Kolmogorov-Smirnov',
                    'Estadístico': f"{result['statistic']:.4f}",
                    'P-Value': f"{result['p_value']:.4f}",
                    'Drift Detectado': '🔴 Sí' if result['drift_detected'] else '🟢 No',
                    'Severidad': 'Alta' if result['p_value'] < 0.01 else ('Media' if result['p_value'] < 0.05 else 'Baja')
                })
            
            for var, result in drift_results['categorical'].items():
                drift_summary.append({
                    'Variable': var,
                    'Tipo': 'Categórica',
                    'Test': 'Chi-Cuadrado',
                    'Estadístico': f"{result['statistic']:.4f}",
                    'P-Value': f"{result['p_value']:.4f}",
                    'Drift Detectado': '🔴 Sí' if result['drift_detected'] else '🟢 No',
                    'Severidad': 'Alta' if result['p_value'] < 0.01 else ('Media' if result['p_value'] < 0.05 else 'Baja')
                })
            
            df_summary = pd.DataFrame(drift_summary)
            st.dataframe(df_summary, use_container_width=True)
            
            # Indicadores visuales tipo semáforo
            st.subheader("🚦 Indicadores de Salud del Modelo")
            
            col1, col2, col3, col4 = st.columns(4)
            
            drift_pct = (drift_count / total_variables * 100) if total_variables > 0 else 0
            
            with col1:
                if drift_pct == 0:
                    st.success("🟢 **EXCELENTE**\n\nSin drift detectado")
                elif drift_pct < 20:
                    st.info("🟡 **BUENO**\n\nDrift mínimo")
                elif drift_pct < 50:
                    st.warning("🟠 **PRECAUCIÓN**\n\nDrift moderado")
                else:
                    st.error("🔴 **CRÍTICO**\n\nDrift severo")
            
            with col2:
                if len(critical_vars) == 0:
                    st.success("🟢 **ESTABLE**\n\nNo hay variables críticas")
                elif len(critical_vars) <= 2:
                    st.warning(f"🟡 **ATENCIÓN**\n\n{len(critical_vars)} var. críticas")
                else:
                    st.error(f"🔴 **ALERTA**\n\n{len(critical_vars)} var. críticas")
            
            with col3:
                if len(history) >= 2:
                    trend_analysis = analyze_drift_trends(history)
                    if trend_analysis['severity'] == 'danger':
                        st.error(f"🔴 **URGENTE**\n\n{trend_analysis['trend']}")
                    elif trend_analysis['severity'] == 'warning':
                        st.warning(f"🟡 **CUIDADO**\n\n{trend_analysis['trend']}")
                    else:
                        st.success(f"🟢 **NORMAL**\n\n{trend_analysis['trend']}")
                else:
                    st.info("⚪ **N/A**\n\nPrimer análisis")
            
            with col4:
                # Calidad general
                quality_score = 100 - drift_pct
                if quality_score >= 80:
                    st.success(f"🟢 **{quality_score:.0f}%**\n\nCalidad Alta")
                elif quality_score >= 50:
                    st.warning(f"🟡 **{quality_score:.0f}%**\n\nCalidad Media")
                else:
                    st.error(f"🔴 **{quality_score:.0f}%**\n\nCalidad Baja")
            
            st.markdown("---")
            
            # Alertas automáticas
            st.subheader("🚨 Sistema de Alertas Automáticas")
            
            alerts_triggered = []
            
            # Alerta 1: Drift severo
            if drift_pct > 50:
                alerts_triggered.append({
                    'tipo': 'CRÍTICO',
                    'mensaje': f'Drift severo detectado en {drift_count} de {total_variables} variables ({drift_pct:.1f}%)',
                    'accion': 'RE-ENTRENAMIENTO INMEDIATO REQUERIDO'
                })
            
            # Alerta 2: Variables críticas
            if critical_vars:
                alerts_triggered.append({
                    'tipo': 'ALTA PRIORIDAD',
                    'mensaje': f'{len(critical_vars)} variable(s) con drift crítico (p-value < 0.01)',
                    'accion': 'INVESTIGAR Y VALIDAR DATOS DE ENTRADA'
                })
            
            # Alerta 3: Tendencia peligrosa
            if len(history) >= 3:
                trend_analysis = analyze_drift_trends(history)
                if trend_analysis['severity'] == 'danger':
                    alerts_triggered.append({
                        'tipo': 'URGENTE',
                        'mensaje': 'Tendencia de drift en aumento acelerado',
                        'accion': 'ACTIVAR PLAN DE CONTINGENCIA'
                    })
            
            if alerts_triggered:
                for alert in alerts_triggered:
                    st.error(f"""
                    **🚨 ALERTA {alert['tipo']}**
                    
                    **Detalle:** {alert['mensaje']}
                    
                    **Acción Requerida:** {alert['accion']}
                    """)
            else:
                st.success("✅ No hay alertas críticas en este momento. El sistema está operando normalmente.")
            
            st.markdown("---")
            
            # ==================== DRIFT EN VARIABLES NUMÉRICAS ====================
            
            st.subheader("📈 Drift en Variables Numéricas (Test de Kolmogorov-Smirnov)")
            
            for col in config.NUMERICAL_COLS:
                if col in drift_results['numerical']:
                    result = drift_results['numerical'][col]
                    
                    # Header de la variable
                    if result['drift_detected']:
                        st.markdown(f"""
                        <div class="alert-danger">
                            <h4>🔴 {col} - DRIFT DETECTADO</h4>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="alert-success">
                            <h4>🟢 {col} - ESTABLE</h4>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Métricas
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Estadístico KS", f"{result['statistic']:.4f}")
                    with col2:
                        st.metric("P-Value", f"{result['p_value']:.4f}")
                    with col3:
                        drift_status = "Sí ⚠️" if result['drift_detected'] else "No ✓"
                        st.metric("Drift", drift_status)
                    
                    # Gráfico comparativo
                    fig = plot_distribution_comparison(baseline_df, current_df, col, plot_type='kde')
                    st.pyplot(fig)
                    plt.close()
                    
                    # Estadísticas comparativas
                    with st.expander(f"📊 Estadísticas detalladas de {col}"):
                        stats_df = pd.DataFrame({
                            'Métrica': ['Media', 'Mediana', 'Desv. Estándar', 'Mín', 'Máx'],
                            'Baseline': [
                                baseline_df[col].mean(),
                                baseline_df[col].median(),
                                baseline_df[col].std(),
                                baseline_df[col].min(),
                                baseline_df[col].max()
                            ],
                            'Actual': [
                                current_df[col].mean(),
                                current_df[col].median(),
                                current_df[col].std(),
                                current_df[col].min(),
                                current_df[col].max()
                            ]
                        })
                        stats_df['Diferencia %'] = ((stats_df['Actual'] - stats_df['Baseline']) / stats_df['Baseline'] * 100).round(2)
                        st.dataframe(stats_df)
                    
                    st.markdown("---")
            
            # ==================== DRIFT EN VARIABLES CATEGÓRICAS ====================
            
            st.subheader("📊 Drift en Variables Categóricas (Test de Chi-Cuadrado)")
            
            for col in config.CATEGORICAL_COLS:
                if col in drift_results['categorical']:
                    result = drift_results['categorical'][col]
                    
                    # Header de la variable
                    if result['drift_detected']:
                        st.markdown(f"""
                        <div class="alert-danger">
                            <h4>🔴 {col} - DRIFT DETECTADO</h4>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="alert-success">
                            <h4>🟢 {col} - ESTABLE</h4>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Métricas
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Estadístico χ²", f"{result['statistic']:.4f}")
                    with col2:
                        st.metric("P-Value", f"{result['p_value']:.4f}")
                    with col3:
                        drift_status = "Sí ⚠️" if result['drift_detected'] else "No ✓"
                        st.metric("Drift", drift_status)
                    
                    # Tabla de contingencia
                    st.write("**Tabla de Frecuencias:**")
                    contingency_pct = result['contingency_table'].copy()
                    contingency_pct['Baseline %'] = (contingency_pct['Baseline'] / contingency_pct['Baseline'].sum() * 100).round(2)
                    contingency_pct['Current %'] = (contingency_pct['Current'] / contingency_pct['Current'].sum() * 100).round(2)
                    st.dataframe(contingency_pct)
                    
                    # Gráfico de barras comparativo
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        name='Baseline',
                        x=result['contingency_table'].index,
                        y=result['contingency_table']['Baseline'],
                        marker_color='blue'
                    ))
                    fig.add_trace(go.Bar(
                        name='Actual',
                        x=result['contingency_table'].index,
                        y=result['contingency_table']['Current'],
                        marker_color='red'
                    ))
                    fig.update_layout(
                        title=f'Comparación de Distribución - {col}',
                        xaxis_title=col,
                        yaxis_title='Frecuencia',
                        barmode='group',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("---")
            
            st.markdown("---")
            
            # Footer con resumen ejecutivo
            st.header("📄 Resumen Ejecutivo")
            
            executive_summary = f"""
            ### Fecha de Análisis: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            
            **Estado del Sistema:** {"🔴 CRÍTICO" if drift_pct > 50 else "🟡 ATENCIÓN" if drift_pct > 20 else "🟢 ESTABLE"}
            
            **Métricas Clave:**
            - Variables Analizadas: {total_variables}
            - Variables con Drift: {drift_count} ({drift_pct:.1f}%)
            - Variables Críticas (p < 0.01): {len(critical_vars)}
            - Calidad del Modelo: {100 - drift_pct:.0f}%
            
            **Acción Inmediata Recomendada:**
            """
            
            if drift_pct > 50:
                executive_summary += "\n🔴 **RE-ENTRENAR EL MODELO INMEDIATAMENTE** - El modelo está comprometido y no debe usarse en producción."
            elif drift_pct > 30:
                executive_summary += "\n🟠 **PLANIFICAR RE-ENTRENAMIENTO EN 48-72 HORAS** - El drift es significativo."
            elif drift_pct > 10:
                executive_summary += "\n🟡 **AUMENTAR FRECUENCIA DE MONITOREO** - Drift moderado detectado."
            else:
                executive_summary += "\n🟢 **CONTINUAR OPERACIÓN NORMAL** - El modelo está funcionando correctamente."
            
            st.markdown(executive_summary)
        
        except Exception as e:
            st.error(f"❌ Error al procesar el archivo: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            st.stop()
    
    else:
        st.info("👆 Por favor, sube un archivo CSV con los datos de producción para comenzar el análisis.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p>🔬 Dashboard de Monitoreo MLOps | Detección de Fraude Financiero</p>
        <p>Desarrollado con Streamlit 🎈</p>
    </div>
    """, unsafe_allow_html=True)


# ==================== EJECUCIÓN ====================

if __name__ == "__main__":
    main()
