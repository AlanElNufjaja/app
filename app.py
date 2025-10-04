import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static

print ("Autistaldo tungtung sahur")

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

# Calcular radio de impacto proporcional al tamaño (ejemplo simple)
radio_km = tamano * 0.1  # cada 10 m = 1 km de radio de daño
radio_m = radio_km * 1000

# Mostrar información
st.success(f"Impacto estimado en **{lugar}** 🌍")
st.write(f"**Tamaño del meteoro:** {tamano} m")
st.write(f"**Radio estimado de impacto:** {radio_km:.1f} km")
st.write(f"**Coordenadas:** {lat:.4f}, {lon:.4f}")

# Crear mapa centrado en la ubicación
m = folium.Map(location=[lat, lon], zoom_start=6)

# Agregar marcador del impacto
folium.Marker([lat, lon], tooltip="Punto de impacto").add_to(m)

# Agregar círculo de daño proporcional al tamaño
folium.Circle(
    location=[lat, lon],
    radius=radio_m,  # en metros
    color="red",
    fill=True,
    fill_opacity=0.3,
    popup=f"Zona de daño aprox: {radio_km:.1f} km"
).add_to(m)

# Mostrar mapa en Streamlit
folium_static(m)

st.caption("Simulador de meteoro básico con daño proporcional al tamaño 🌠")
