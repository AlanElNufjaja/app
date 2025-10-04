import streamlit as st
from parameters import obtener_coordenadas, calcular_radio

st.title("Visualizador de Meteoritos 2D ☄️")

# Límites
LAT_MIN, LAT_MAX = -90.0, 90.0
LON_MIN, LON_MAX = -180.0, 180.0

# Inputs del usuario con límites
lugar = st.sidebar.text_input("Nombre de la ciudad")
lat_manual = st.sidebar.number_input("Latitud manual", value=19.4326, min_value=LAT_MIN, max_value=LAT_MAX)
lon_manual = st.sidebar.number_input("Longitud manual", value=-99.1332, min_value=LON_MIN, max_value=LON_MAX)
tamano = st.sidebar.slider("Tamaño del meteorito (m)", 10, 500, 100)

# Obtener coordenadas usando Geopy + fallback a lat/lon manual
lat, lon = obtener_coordenadas(lugar, lat_manual, lon_manual)

# Calcular radio de impacto
radio_km = calcular_radio(tamano)

st.write(f"Coordenadas finales: {lat:.4f}, {lon:.4f}")
st.write(f"Radio de impacto estimado: {radio_km:.1f} km")
