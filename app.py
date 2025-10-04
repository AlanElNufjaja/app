# app.py
import streamlit as st
from parameters import obtener_coordenadas, calcular_radio
from damage import generar_puntos_circulo
from mapa
import mostrar_mapa

st.set_page_config(page_title="Visualizador de Meteoritos 3D ☄️", layout="centered")
st.title("☄️ Visualizador de Impacto de Meteoritos 3D")
st.write("Simula el lugar donde caería un meteorito y la zona de daño proporcional al tamaño 🌍")

# -------------------------
# Entradas del usuario
# -------------------------
st.sidebar.header("⚙️ Parámetros del impacto")

lugar = st.sidebar.text_input("🌎 Nombre del lugar (opcional):", "")
manual_lat = st.sidebar.number_input("Latitud manual (opcional)", value=0.0, step=0.01)
manual_lon = st.sidebar.number_input("Longitud manual (opcional)", value=0.0, step=0.01)
tamano = st.sidebar.slider("Tamaño del meteoro (m)", 10, 500, 100)

# -------------------------
# Obtener coordenadas
# -------------------------
lat, lon = obtener_coordenadas(lugar, manual_lat, manual_lon)

# -------------------------
# Calcular radio y generar puntos de impacto
# -------------------------
radio_km = calcular_radio(tamano)
df = generar_puntos_circulo(lat, lon, radio_km, n_puntos=500)

# -------------------------
# Mostrar información del impacto
# -------------------------
st.success("Impacto estimado 🌍")
st.write(f"**Tamaño del meteoro:** {tamano} m")
st.write(f"**Radio estimado de impacto:** {radio_km:.1f} km")
st.write(f"**Coordenadas:** {lat:.4f}, {lon:.4f}")

# -------------------------
# Mostrar mapa 3D con Pydeck
# -------------------------
mostrar_mapa(df, lat, lon, radio_km)
st.caption("Simulador de meteoro con zona de daño 3D proporcional al tamaño 🌠")
