# app.py
import streamlit as st
import pandas as pd
from parameters import obtener_coordenadas, calcular_radio
from damage import generar_puntos_circulo
from map.py import mostrar_mapa  # aquí usa map.py renombrado si quieres

st.title("Visualizador de Impacto de Meteoritos 2D ☄️")

# Entradas del usuario
lugar = st.sidebar.text_input("Nombre del lugar (opcional)")
manual_lat = st.sidebar.number_input("Latitud manual", value=0.0)
manual_lon = st.sidebar.number_input("Longitud manual", value=0.0)
tamano = st.sidebar.slider("Tamaño del meteoro (m)", 10, 500, 100)

# Coordenadas
lat, lon = obtener_coordenadas(lugar, manual_lat, manual_lon)

# Radio y puntos
radio_km = calcular_radio(tamano)
df = generar_puntos_circulo(lat, lon, radio_km, n_puntos=500)

# Mostrar info
st.write(f"Tamaño: {tamano} m")
st.write(f"Radio estimado: {radio_km:.1f} km")
st.write(f"Coordenadas: {lat:.4f}, {lon:.4f}")

# Mostrar mapa 2D
mostrar_mapa(df, lat, lon, radio_km)
