pip install geopy
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from geopy.geocoders import Nominatim

# -------------------------------------------------------------
# CONFIGURACIÓN BÁSICA
# -------------------------------------------------------------
st.set_page_config(layout="wide")
st.title("☄️ Visualizador de Impacto Meteorítico")
st.subheader("Simulación interactiva de escenarios de impacto 2025")

# -------------------------------------------------------------
# SIDEBAR: PARÁMETROS DEL ESCENARIO
# -------------------------------------------------------------
st.sidebar.header("⚙️ Parámetros del Impacto")

# 1️⃣ Lugar del impacto
lugar = st.sidebar.text_input("Lugar del impacto (ej. 'México', 'Tokyo', 'Cairo')", "México")

geolocator = Nominatim(user_agent="impact_simulator")
location = geolocator.geocode(lugar)

if location:
    lat, lon = location.latitude, location.longitude
else:
    st.warning("No se pudo encontrar ese lugar. Se usará una ubicación por defecto (0,0).")
    lat, lon = 0, 0

# 2️⃣ Tamaño del asteroide
tamano_ast = st.sidebar.slider("Tamaño del asteroide (m)", 10, 500, 50, step=10)

# 3️⃣ Tipo de mitigación
opcion_mitigacion = st.sidebar.selectbox(
    "Estrategia de mitigación",
    ("Impacto Directo (Peor Caso)", "Desviación Parcial", "Mitigación Exitosa")
)

# -------------------------------------------------------------
# CÁLCULOS DEL IMPACTO
# -------------------------------------------------------------
# Radio de daño aumenta con el tamaño del asteroide (no lineal)
if opcion_mitigacion == "Impacto Directo (Peor Caso)":
    factor_riesgo = 1.0
elif opcion_mitigacion == "Desviación Parcial":
    factor_riesgo = 0.5
else:
    factor_riesgo = 0.0

# Relación empírica (no real pero lógica): radio en km = (diámetro ^ 1.2) * 0.03
radio_km = (tamano_ast ** 1.2) * 0.03 * factor_riesgo
radio_m = radio_km * 1000

# -------------------------------------------------------------
# DATOS DE VISUALIZACIÓN
# -------------------------------------------------------------
n_puntos = 600
angles = np.random.rand(n_puntos) * 2 * np.pi
r = np.random.rand(n_puntos) ** 0.5 * (radio_km / 111)
latitudes = lat + r * np.cos(angles)
longitudes = lon + r * np.sin(angles)

datos_impacto = pd.DataFrame({
    "lat": latitudes,
    "lon": longitudes,
    "riesgo": np.clip(1 - (r / (radio_km / 111)), 0, 1)
})

# -------------------------------------------------------------
# MENSAJE DE ESCENARIO
# -------------------------------------------------------------
if factor_riesgo == 0:
    st.success(f"✅ Mitigación exitosa: el asteroide de {tamano_ast} m fue desviado. No hay daño.")
else:
    color = "🔴" if factor_riesgo == 1 else "🟠"
    st.markdown(f"{color} **Simulación de impacto en {lugar}:**")
    st.markdown(f"- Tamaño del asteroide: **{tamano_ast} m**")
    st.markdown(f"- Radio estimado de daño: **{radio_km:.1f} km**")
    st.markdown(f"- Coordenadas: ({lat:.3f}, {lon:.3f})")

# -------------------------------------------------------------
# MAPA DE IMPACTO (PYDECK)
# -------------------------------------------------------------
if factor_riesgo > 0:
    layer_puntos = pdk.Layer(
        "ScatterplotLayer",
        data=datos_impacto,
        get_position="[lon, lat]",
        get_radius=200,
        get_fill_color="[255 * riesgo, 100, 0, 180]",
        pickable=True,
    )

    layer_circulo = pdk.Layer(
        "ScatterplotLayer",
        data=pd.DataFrame({"lon": [lon], "lat": [lat]}),
        get_position="[lon, lat]",
        get_radius=radio_m,
        get_fill_color="[255, 0, 0, 50]",
    )

    view_state = pdk.ViewState(latitude=lat, longitude=lon, zoom=6, pitch=45)

    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state=view_state,
        layers=[layer_puntos, layer_circulo],
        tooltip={"text": "Nivel de riesgo: {riesgo:.2f}"},
    ))
else:
    st.info("🌍 No hay impacto que mostrar en el mapa. El asteroide fue desviado exitosamente.")

# -------------------------------------------------------------
# PIE DE PÁGINA
# -------------------------------------------------------------
st.markdown("---")
st.caption("Proyecto Impactor-2025 • Simulación educativa del riesgo por impacto meteorítico 🌠")
