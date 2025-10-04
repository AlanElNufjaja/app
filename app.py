# app.py
import streamlit as st
from parameters import obtener_coordenadas, calcular_radio
from damage import generar_puntos_circulo
from mapa import mostrar_mapa

st.title("Visualizador de Meteoritos 2D ☄️")

# Parámetros del usuario
lugar = st.sidebar.text_input("Nombre de la ciudad")
lat_manual = st.sidebar.slider("Latitud manual", -80, 80, 1)
lon_manual = st.sidebar.slider("Longitud manual", -180, 180, 1)
tamano = st.sidebar.slider("Tamaño del meteorito (m)", 10, 10000, 1)

# Obtener coordenadas
lat, lon = obtener_coordenadas(lugar, lat_manual, lon_manual)

# Calcular radio y generar puntos de impacto
radio_km = calcular_radio(tamano)
df = generar_puntos_circulo(lat, lon, radio_km, n_puntos=300)

# Mostrar info
st.write(f"Tamaño del meteorito: {tamano} m")
st.write(f"Radio estimado de impacto: {radio_km:.1f} km")
st.write(f"Coordenadas: {lat:.4f}, {lon:.4f}")

# Mostrar mapa 2D
mostrar_mapa(df, lat, lon, radio_km)
