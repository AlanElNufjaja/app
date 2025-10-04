import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim

st.set_page_config(page_title="Visualizador de Meteoros ☄️", layout="centered")

st.title("☄️ Visualizador de Impacto Meteorítico")
st.write("Simula el lugar donde caería un meteoro y su radio de impacto 🌍")

# Entrada del usuario
lugar = st.text_input("🌎 Ingresa el lugar del impacto:", "México")
tamano = st.slider("Tamaño del meteoro (m)", 10, 500, 100)

# Geolocalización
geolocator = Nominatim(user_agent="meteor_app")
try:
    location = geolocator.geocode(lugar)
    if location:
        lat, lon = location.latitude, location.longitude
    else:
        st.warning("No se encontró el lugar. Usando Ciudad de México.")
        lat, lon = 19.4326, -99.1332
except:
    st.warning("Error al conectar con geopy. Usando Ciudad de México.")
    lat, lon = 19.4326, -99.1332

# Calcular radio (km) de impacto según tamaño
radio_km = tamano * 0.1  # simplificado: cada 10 m = 1 km de daño aprox

# Crear dataframe con el punto de impacto
df = pd.DataFrame({
    "lat": [lat],
    "lon": [lon]
})

# Mostrar información
st.success(f"Impacto estimado en **{lugar}** 🌍")
st.write(f"**Tamaño del meteoro:** {tamano} m")
st.write(f"**Radio estimado de impacto:** {radio_km:.1f} km")
st.write(f"**Coordenadas:** {lat:.4f}, {lon:.4f}")

# Mostrar mapa
st.map(df, zoom=6)

st.caption("Simulador básico — meteoro versión chill 😎")
