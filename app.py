import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Visualizador de Meteoros ☄️", layout="centered")
st.title("☄️ Visualizador de Impacto Meteorítico")
st.write("Simula el lugar donde caería un meteoro y la zona de daño proporcional al tamaño 🌍")

# -------------------------
# Entradas del usuario
# -------------------------
st.sidebar.header("⚙️ Parámetros del impacto")

lat = st.sidebar.number_input("Latitud del impacto", value=19.4326, step=0.01, format="%.4f")
lon = st.sidebar.number_input("Longitud del impacto", value=-99.1332, step=0.01, format="%.4f")
tamano = st.sidebar.slider("Tamaño del meteoro (m)", 10, 500, 100)

# -------------------------
# Cálculo de radio de impacto
# -------------------------
# Cada 10 m = 1 km de radio aproximado
radio_km = tamano * 0.1

# Número de puntos para simular el círculo
n_puntos = 500
angles = np.random.rand(n_puntos) * 2 * np.pi
r = np.random.rand(n_puntos) ** 0.5 * (radio_km / 111)  # 1° aprox = 111 km
latitudes = lat + r * np.cos(angles)
longitudes = lon + r * np.sin(angles)

# Crear dataframe para el mapa (círculo de impacto)
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
# Mostrar mapa con círculo de impacto
# -------------------------
st.map(df, zoom=6)

st.caption("Simulador de meteoro con zona de daño proporcional al tamaño 🌠")
