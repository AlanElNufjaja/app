import streamlit as st
from parameters import obtener_coordenadas, velocidad_realista, calcular_radio_impacto
from damage import generar_puntos_circulo
from mapa import mostrar_mapa

st.title("Visualizador de Meteoritos 2D ☄️")

# Entradas del usuario
lugar = st.sidebar.text_input("Nombre de la ciudad")
lat_manual = st.sidebar.slider("Latitud manual", float(-80), float(80), 19)
lon_manual = st.sidebar.slider("Longitud manual", -180, 180, -99)
tamano = st.sidebar.slider("Tamaño del meteorito (m)", float(0.1), float(500), 100)
densidad = st.sidebar.slider("Densidad (kg/m³)", (float(1000), float(8000), 2000)

# Coordenadas
lat, lon = obtener_coordenadas(lugar, lat_manual, lon_manual)

# Velocidad realista según tamaño
velocidad_kms = velocidad_realista(tamano)

# Calcular radio de impacto
radio_km = calcular_radio_impacto(tamano, densidad, velocidad_kms)

# Generar puntos de impacto (centro y radio)
df = generar_puntos_circulo(lat, lon, radio_km)

# Mostrar info
st.write(f"Tamaño: {tamano} m")
st.write(f"Densidad: {densidad} kg/m³")
st.write(f"Velocidad de impacto: {velocidad_kms} km/s")
st.write(f"Radio estimado de impacto: {radio_km:.2f} km")
st.write(f"Coordenadas: {lat:.4f}, {lon:.4f}")

# Mostrar mapa
mostrar_mapa(df, lat, lon, radio_km)
