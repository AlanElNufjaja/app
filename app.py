import streamlit as st
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim

# Configuración de la página
st.set_page_config(page_title="Visualizador de Meteoros ☄️", layout="centered")
st.title("☄️ Visualizador de Impacto Meteorítico")
st.write("Simula el lugar donde caería un meteoro y la zona de daño proporcional al tamaño 🌍")

# -------------------------
# Entradas del usuario
# -------------------------
st.sidebar.header("⚙️ Parámetros del impacto")

# Input principal: lugar
lugar = st.sidebar.text_input("🌎 Ingresa el lugar del impacto (ej. México, Tokyo):", "")

# Input secundario: lat/lon manual
manual_lat = st.sidebar.number_input("Latitud del impacto (manual, solo si falla el lugar)", value=0.0, step=0.01, format="%.4f")
manual_lon = st.sidebar.number_input("Longitud del impacto (manual, solo si falla el lugar)", value=0.0, step=0.01, format="%.4f")

# Tamaño del meteoro
tamano = st.sidebar.slider("Tamaño del meteoro (m)", 10, 500, 100)

# -------------------------
# Intentar geolocalizar
# -------------------------
geolocator = Nominatim(user_agent="meteor_app")
lat, lon = None, None

if lugar:
    try:
        location = geolocator.geocode(lugar)
        if location:
            lat, lon = location.latitude, location.longitude
        else:
            st.warning("No se encontró el lugar. Usa las coordenadas manuales.")
    except:
        st.warning("Error al conectar con geopy. Usa las coordenadas manuales.")

# Si no hay coordenadas válidas, usar las manuales
if lat is None or lon is None:
    if manual_lat != 0.0 or manual_lon != 0.0:
        lat, lon = manual_lat, manual_lon
    else:
        # fallback por defecto
        st.info("Usando ubicación por defecto: Ciudad de México.")
        lat, lon = 19.4326, -99.1332

# -------------------------
# Calcular radio de impacto
# -------------------------
radio_km = tamano * 0.1  # cada 10 m = 1 km aprox

# -------------------------
# Generar puntos para círculo de daño
# -------------------------
n_puntos = 500
angles = np.random.rand(n_puntos) * 2 * np.pi
r = np.random.rand(n_puntos) ** 0.5 * (radio_km / 111)  # 1° ~ 111 km
latitudes = lat + r * np.cos(angles)
longitudes = lon + r * np.sin(angles)

df = pd.DataFrame({
    "lat": latitudes,
    "lon": longitudes
})

# -------------------------
# Mostrar información
# -------------------------
st.success("Impacto estimado 🌍")
st.write(f"**Tamaño del meteoro:** {tamano} m")
st.write(f"**Radio estimado de impacto:** {radio_km:.1f} km")
st.write(f"**Coordenadas:** {lat:.4f}, {lon:.4f}")

# -------------------------
# Mostrar mapa
# -------------------------
st.map(df, zoom=6)

st.caption("Simulador de meteoro con zona de daño proporcional al tamaño 🌠")
