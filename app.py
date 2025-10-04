import streamlit as st
import pandas as pd
from parameters import obtener_coordenadas, velocidad_realista, calcular_radio_impacto
from damage import generar_puntos_circulo
from mapa import mostrar_mapa

st.title("Visualizador de Meteoritos 2D ☄️")

# ======================
# Lista de meteoritos
# ======================
datos_base = pd.read_csv("datos_base.csv")
datos_limpios = pd.read_csv("datos_limpios.csv")

# Combinar datos solo para poder acceder a tamaño y velocidad
meteoritos = pd.concat([datos_base, datos_limpios], axis=1)
opciones = meteoritos['id'].astype(str).tolist()
meteorito_seleccionado = st.sidebar.selectbox("Selecciona un meteorito", opciones)

mete = meteoritos[meteoritos['id'].astype(str) == meteorito_seleccionado].iloc[0]

# Datos predeterminados del meteorito seleccionado
tamano = (mete['estimated_diameter.kilometers.estimated_diameter_min'] + mete['estimated_diameter.kilometers.estimated_diameter_max']) / 2 * 1000  # km a m
densidad = 3000  # kg/m³ estándar
velocidad_kms = mete['relative_velocity.kilometers_per_second']

# ======================
# Entradas del usuario
# ======================
lugar = st.sidebar.text_input("Nombre de la ciudad")
lat_manual = st.sidebar.slider("Latitud manual", float(-80), float(80), 19.44, step=0.0001)
lon_manual = st.sidebar.slider("Longitud manual", float(-180), float(180), -99.1, step=0.0001)

# Ahora tus sliders usan los valores del meteorito seleccionado como default
tamano = st.sidebar.slider("Tamaño del meteorito (m)", 0.1, 500, float(tamano))
densidad = st.sidebar.slider("Densidad (kg/m³)", 1000, 8000, float(densidad))

# Coordenadas
lat, lon = obtener_coordenadas(lugar, lat_manual, lon_manual)

# Velocidad realista según tamaño
velocidad_kms = velocidad_realista(tamano) if st.sidebar.checkbox("Calcular velocidad realista") else float(velocidad_kms)

# Calcular radio de impacto
radio_km = calcular_radio_impacto(tamano, densidad, velocidad_kms)

# Generar puntos de impacto (centro y radio)
df = generar_puntos_circulo(lat, lon, radio_km)

# Mostrar info
st.write(f"Tamaño: {tamano:.1f} m")
st.write(f"Densidad: {densidad} kg/m³")
st.write(f"Velocidad de impacto: {velocidad_kms:.2f} km/s")
st.write(f"Radio estimado de impacto: {radio_km:.2f} km")
st.write(f"Coordenadas: {lat:.4f}, {lon:.4f}")

# Mostrar mapa
mostrar_mapa(df, lat, lon, radio_km)
