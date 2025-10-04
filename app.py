import streamlit as st
import pandas as pd
from parameters import obtener_coordenadas
from damage import generar_puntos_circulo
from mapa import mostrar_mapa

st.title("Visualizador de Meteoritos 2D ☄️")

# Entrada del usuario
lugar = st.sidebar.text_input("Nombre de la ciudad")
lat_manual = st.sidebar.slider("Latitud manual", -90, 90, 90)
lon_manual = st.sidebar.slider("Longitud manual", -180, 180, 90)
tamano = st.sidebar.slider("Tamaño del meteorito (m)", 10, 500, 100)

# Obtener coordenadas
lat, lon = obtener_coordenadas(lugar, lat_manual, lon_manual)

# Radio y puntos de impacto
radio_km = tamano / 10  # ejemplo simple: más grande, más radio
df = generar_puntos_circulo(lat, lon, radio_km, n_puntos=500)

# Mostrar info
st.write(f"Tamaño: {tamano} m")
st.write(f"Radio estimado: {radio_km:.1f} km")
st.write(f"Coordenadas: {lat:.4f}, {lon:.4f}")

# Mostrar mapa
mostrar_mapa(df, lat, lon, radio_km)
