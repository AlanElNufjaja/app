import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from geopy.geocoders import Nominatim

# -------------------------------------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------------------------------------
st.set_page_config(layout="wide")
st.title("☄️ Visualizador de Impacto Meteorítico")
st.subheader("Simulación interactiva de escenarios de impacto 2025")

# -------------------------------------------------------------
# TOKEN DE MAPBOX (NECESARIO PARA MOSTRAR EL MAPA)
# -------------------------------------------------------------
# 🔥 Puedes usar este para pruebas, pero se recomienda usar el tuyo:
pdk.settings.mapbox_api_key = "pk.eyJ1IjoiZXhhbXBsZXVzZXIiLCJhIjoiY2xvbmU0MWtzMDJ2YzQwcGpxY2N2NG52byJ9.F_mV9rMIrR9kDk8Gz7y6lg"

# -------------------------------------------------------------
# SIDEBAR: PARÁMETROS DEL ESCENARIO
# -------------------------------------------------------------
st.sidebar.header("⚙️ Parámetros del Impacto")

# Lugar del impacto
lugar = st.sidebar.text_input("🌍 Lugar del impacto (ej. 'México', 'Tokyo', 'Cairo')", "México")

# Obtener coordenadas con geopy
geolocator = Nominatim(user_agent="impact_simulator")
try:
    location = geolocator.geocode(lugar)
    if location:
        lat, lon = location.latitude, location.longitude
    else:
        st.warning("No se encontró el lugar, usando ubicación por defecto: Ciudad de México 🇲🇽.")
        lat, lon = 19.4326, -99.1332
except Exception as e:
    st.warning("Error al conectar con el servicio de geolocalización. Usando ubicación por defecto.")
    lat, lon = 19.4326, -99.1332

# Tamaño del asteroide
tamano_ast = st.sidebar.slider("Tamaño del asteroide (m)", 10, 500, 50, step=10)

# Estrategia de mitigación
opcion_mitigacion = st.sidebar.selectbox(
    "Estrategia de mitigación",
    ("Impacto Directo (Peor Caso)", "Desviación Parcial", "Mitigación Exitosa")
)

# -------------------------------------------------------------
# CÁLCULO DEL IMPACTO
# -------------------------------------------------------------
if opcion_mitigacion == "Impacto Directo (Peor Caso)":
    factor_riesgo = 1.0
elif opcion_mitigacion == "Desviación Parcial":
    factor_riesgo = 0.5
else:
    factor_riesgo = 0.0

# Relación empírica: radio (km) = (tamaño ^ 1.2) * 0.03 * factor
radio_km = (tamano_ast ** 1.2) * 0.03 * factor_riesgo
radio_m = radio_km * 1000

# -------------------------------------------------------------
# DATOS PARA VISUALIZAR
# -------------------------------------------------------------
if factor_riesgo > 0:
    n_puntos = 600
    angles = np.random.rand(n_puntos) * 2 * np.pi
    r = np.random.rand(n_puntos) ** 0.5 * (radio_km / 111)  # 1° ~ 111 km
    latitudes = lat + r * np.cos(angles)
    longitudes = lon + r * np.sin(angles)

    datos_impacto = pd.DataFrame({
        "lat": latitudes,
        "lon": longitudes,
        "riesgo": np.clip(1 - (r / (radio_km / 111)), 0, 1)
    })
else:
    datos_impacto = pd.DataFrame(columns=["lat", "lon", "riesgo"])

# -------------------------------------------------------------
# RESULTADOS
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
st.header("🌎 Mapa del impacto")

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

    view_state = pdk.ViewState(latitude=lat, longitude=lon, zoom=5, pitch=45)

    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state=view_state,
        layers=[layer_puntos, layer_circulo],
        tooltip={"text": "Nivel de riesgo: {riesgo:.2f}"},
    ))
else:
    st.info("🌍 No hay impacto que mostrar (asteroide desviado exitosamente).")

# -------------------------------------------------------------
# PIE DE PÁGINA
# -------------------------------------------------------------
st.markdown("---")
st.caption("Proyecto Impactor-2025 • Simulación educativa del riesgo por impacto meteorítico 🌠")
