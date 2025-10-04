# app.py
import streamlit as st
import pandas as pd
from parameters import obtener_coordenadas, calcular_radio_impacto
from damage import generar_puntos_circulo

st.set_page_config(page_title="Simulador de Meteoritos", layout="wide")

st.title("💥 Simulador de Impacto de Meteoritos")

# -----------------------------
# Entradas del usuario
# -----------------------------
lugar = st.sidebar.text_input("Nombre de la ciudad")

lat_manual = st.sidebar.slider("Latitud manual", -90.0, 90.0, 19.4326)
lon_manual = st.sidebar.slider("Longitud manual", -180.0, 180.0, -99.1332)

tamano = st.sidebar.slider("Tamaño del meteorito (m)", 0.1, 500.0, 100.0)
densidad = st.sidebar.slider("Densidad (kg/m³)", 1000.0, 8000.0, 2000.0)
velocidad = st.sidebar.slider("Velocidad (km/s)", 5.0, 72.0, 20.0)  # velocidad típica de meteoritos

# -----------------------------
# Obtener coordenadas
# -----------------------------
lat, lon = obtener_coordenadas(lugar, lat_manual, lon_manual)
st.write(f"Coordenadas: {lat:.4f}, {lon:.4f}")

# -----------------------------
# Calcular radio de impacto
# -----------------------------
radio_km = calcular_radio_impacto(tamano, densidad, velocidad)
st.write(f"Radio estimado de destrucción: {radio_km:.2f} km")

# -----------------------------
# Generar círculo de impacto
# -----------------------------
df_circulo = generar_puntos_circulo(lat, lon, radio_km)
st.write("Datos del círculo de impacto:")
st.dataframe(df_circulo)

# -----------------------------
# Mapa con DeckGL
# -----------------------------
import pydeck as pdk

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_circulo,
    get_position='[lon, lat]',
    get_color='[255, 0, 0, 160]',
    get_radius='radio_km*1000',
    pickable=True
)

view_state = pdk.ViewState(
    latitude=lat,
    longitude=lon,
    zoom=6,
    pitch=0
)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/light-v11"
)

st.pydeck_chart(r)
