# app.py
import streamlit as st
from parameters import obtener_coordenadas, calcular_radio
from damage import generar_puntos_circulo
from map import mostrar_mapa

st.set_page_config(page_title="Visualizador de Meteoritos ☄️", layout="centered")
st.title("☄️ Visualizador de Impacto de Meteoritos")
st.write("Simula el lugar donde caería un meteorito y la zona de daño proporcional al tamaño 🌍")

# Entradas
st.sidebar.header("⚙️ Parámetros del impacto")
lugar = st.sidebar.text_input("🌎 Nombre del lugar (opcional):", "")
manual_lat = st.sidebar.number_input("Latitud manual (opcional)", value=0.0, step=0.01)
manual_lon = st.sidebar.number_input("Longitud manual (opcional)", value=0.0, step=0.01)
tamano = st.sidebar.slider("Tamaño del meteoro (m)", 10, 500, 100)

# Obtener coordenadas y calcular radio
lat, lon = obtener_coordenadas(lugar, manual_lat, manual_lon)
radio_km = calcular_radio(tamano)

# Generar puntos de impacto
df = generar_puntos_circulo(lat, lon, radio_km)

# Mostrar información
st.success("Impacto estimado 🌍")
st.write(f"**Tamaño del meteoro:** {tamano} m")
st.write(f"**Radio estimado de impacto:** {radio_km:.1f} km")
st.write(f"**Coordenadas:** {lat:.4f}, {lon:.4f}")

# Mostrar mapa
mostrar_mapa(df)
st.caption("Simulador de meteoro con zona de daño proporcional al tamaño 🌠")
