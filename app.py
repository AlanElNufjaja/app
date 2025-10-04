import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# ---------------------------------------------
# CONFIGURACIÓN BÁSICA
# ---------------------------------------------
st.set_page_config(layout="wide")
st.title("🛡 Visualizador de Riesgo: Proyecto Impactor-2025")
st.subheader("Herramienta de Decisión para Mitigación de Asteroides")

# ---------------------------------------------
# CONTROLES LATERALES
# ---------------------------------------------
st.sidebar.header("Parámetros del Escenario de Impacto")

# Coordenadas del punto de impacto (modificables por el usuario)
lat = st.sidebar.number_input("Latitud del impacto", value=38.9, step=0.1, format="%.4f")
lon = st.sidebar.number_input("Longitud del impacto", value=-77.0, step=0.1, format="%.4f")

# Estrategia de mitigación
opcion_mitigacion = st.sidebar.selectbox(
    "Seleccione Estrategia de Mitigación:",
    ('Impacto Directo (Peor Caso)', 'Desviación Parcial', 'Mitigación Exitosa')
)

# Tamaño estimado del asteroide
tamano_ast = st.sidebar.slider(
    'Tamaño Estimado del Asteroide (metros):',
    min_value=10.0, max_value=300.0, value=50.0, step=10.0
)

# ---------------------------------------------
# MODELO SIMPLE DE IMPACTO
# ---------------------------------------------
# Radio de daño estimado (km) según tamaño y mitigación
if opcion_mitigacion == 'Impacto Directo (Peor Caso)':
    factor_riesgo = 1.0
elif opcion_mitigacion == 'Desviación Parcial':
    factor_riesgo = 0.5
else:
    factor_riesgo = 0.0  # mitigado

# Relación empírica (ficticia pero razonable): radio de daño ~ tamaño ^ 1.3
radio_km = (tamano_ast ** 1.3) * 0.02 * factor_riesgo
radio_m = radio_km * 1000

# ---------------------------------------------
# GENERAR DATOS DE IMPACTO VISUAL
# ---------------------------------------------
# Simular puntos dentro del área de daño
n_puntos = 500
angles = np.random.rand(n_puntos) * 2 * np.pi
r = np.random.rand(n_puntos) ** 0.5 * (radio_km / 111)  # conversión a grados aprox
latitudes = lat + r * np.cos(angles)
longitudes = lon + r * np.sin(angles)

datos_impacto = pd.DataFrame({
    'lat': latitudes,
    'lon': longitudes,
    'riesgo': np.clip(1 - (r / (radio_km / 111)), 0, 1)
})

# ---------------------------------------------
# MENSAJE SEGÚN RESULTADO
# ---------------------------------------------
if opcion_mitigacion == 'Impacto Directo (Peor Caso)':
    st.error(f"🔴 ALERTA: Impacto confirmado. El asteroide de {tamano_ast} m genera un radio de daño estimado de {radio_km:.2f} km.")
elif opcion_mitigacion == 'Mitigación Exitosa':
    st.success(f"✅ ÉXITO: El asteroide de {tamano_ast} m fue desviado. Sin daño reportado.")
else:
    st.warning(f"🟠 IMPACTO PARCIAL: Zona afectada estimada de {radio_km:.2f} km.")

# ---------------------------------------------
# MAPA INTERACTIVO (PYDECK)
# ---------------------------------------------
st.header("🌎 Mapa de Consecuencias del Impacto")

layer_puntos = pdk.Layer(
    'ScatterplotLayer',
    data=datos_impacto,
    get_position='[lon, lat]',
    get_radius=200,  # tamaño de punto
    get_fill_color='[255 * riesgo, 80, 0, 160]',
    pickable=True
)

# Círculo principal del impacto
layer_circulo = pdk.Layer(
    "ScatterplotLayer",
    data=pd.DataFrame({'lon': [lon], 'lat': [lat]}),
    get_position='[lon, lat]',
    get_radius=radio_m,
    get_fill_color='[255, 0, 0, 50]',
)

view_state = pdk.ViewState(latitude=lat, longitude=lon, zoom=6, pitch=45)

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/dark-v10',
    initial_view_state=view_state,
    layers=[layer_puntos, layer_circulo],
    tooltip={"text": "Riesgo: {riesgo}"}
))

# ---------------------------------------------
# INFORME FINAL
# ---------------------------------------------
st.markdown(f"""
**Análisis del Escenario:**
- Coordenadas: ({lat:.3f}, {lon:.3f})  
- Tamaño estimado: **{tamano_ast} m**  
- Estrategia: **{opcion_mitigacion}**  
- Radio de daño: **{radio_km:.2f} km**  
""")
