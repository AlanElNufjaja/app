import streamlit as st
import pandas as pd
import numpy as np

# TÍTULO Y OBJETIVO CLAVE
st.set_page_config(layout="wide") # Opcional: usa todo el ancho de la pantalla
st.title("🛡 Visualizador de Riesgo: Proyecto Impactor-2025")
st.subheader("Herramienta de Decisión para Mitigación de Asteroides")

# SIMULACIÓN DE DATOS (REEMPLAZA ESTO CON LA DATA REAL DE NASA/USGS)
# En un sprint, usamos datos falsos para construir la interfaz.
datos_impacto = pd.DataFrame({
    'lat': np.random.randn(1000) * 1 + 38.9, # Latitudes cerca de una ciudad
    'lon': np.random.randn(1000) * 1 + -77.0, # Longitudes
    'riesgo': np.random.rand(1000)
})

# ----------------------------------------------------
# 2. SECCIÓN DE CONTROLES (PARA EL DECISOR)
# ----------------------------------------------------
st.sidebar.header("Parámetros del Escenario de Impacto")

# Control interactivo: Asumiendo que Impactor-2025 podría ser desviado
opcion_mitigacion = st.sidebar.selectbox(
    "Seleccione Estrategia de Mitigación:",
    ('Impacto Directo (Peor Caso)', 'Desviación Parcial', 'Mitigación Exitosa')
)

# Control interactivo: Slider para el tamaño del asteroide
tamano_ast = st.sidebar.slider(
    'Tamaño Estimado del Asteroide (metros):',
    min_value=10.0, max_value=100.0, value=30.0, step=5.0
)

# ----------------------------------------------------
# 3. SECCIÓN DE VISUALIZACIÓN DE RESULTADOS
# ----------------------------------------------------

# Muestra el resultado de la mitigación
if opcion_mitigacion == 'Impacto Directo (Peor Caso)':
    st.error(f"🔴 ALERTA: Confirmado Impacto. Evaluación de consecuencias para un objeto de {tamano_ast}m.")
elif opcion_mitigacion == 'Mitigación Exitosa':
    st.success(f"✅ ÉXITO: El asteroide de {tamano_ast}m ha sido desviado. Riesgo nulo.")
else:
    st.warning("🟠 EVALUANDO: Impacto parcial. Modelando zona de riesgo residual.")


st.header("Mapa de Consecuencias (Datos USGS Integrados)")

# Visualización interactiva del mapa (usando la data simulada)
st.map(datos_impacto) 

st.markdown(f"*Análisis:* El modelo actual considera un tamaño de *{tamano_ast} metros* y la estrategia de *{opcion_mitigacion}*.")
