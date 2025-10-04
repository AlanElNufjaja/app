# app.py
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from geopy.geocoders import Nominatim

# --------------------------
# Configuración
# --------------------------
st.set_page_config(page_title="Visualizador de Meteoritos 3D", layout="wide")
st.title("Visualizador de Meteoritos 3D ☄️")

# --------------------------
# Parámetros de usuario
# --------------------------
lugar = st.sidebar.text_input("Nombre de la ciudad (opcional)")
lat_manual = st.sidebar.slider("Latitud manual", -90, 90, 19)
lon_manual = st.sidebar.slider("Longitud manual", -180, 180, -99)
tamano = st.sidebar.slider("Tamaño del meteorito (m)", 10, 500, 100)

# --------------------------
# Funciones
# --------------------------
LAT_MIN, LAT_MAX = -90.0, 90.0
LON_MIN, LON_MAX = -180.0, 180.0

def obtener_coordenadas(nombre_ciudad, lat_manual, lon_manual):
    # Limitar manual
    lat_manual = max(LAT_MIN, min(LAT_MAX, lat_manual))
    lon_manual = max(LON_MIN, min(LON_MAX, lon_manual))
    lat, lon = lat_manual, lon_manual

    if nombre_ciudad.strip() != "":
        try:
            geolocator = Nominatim(user_agent="meteoro_app")
            location = geolocator.geocode(nombre_ciudad, timeout=5)
            if location:
                lat, lon = location.latitude, location.longitude
        except:
            pass

    # Aplicar límites
    lat = max(LAT_MIN, min(LAT_MAX, lat))
    lon = max(LON_MIN, min(LON_MAX, lon))
    return lat, lon

def calcular_radio(tamano_metro):
    return tamano_metro * 0.1  # km

def generar_puntos_circulo(lat, lon, radio_km, n_puntos=200):
    angles = np.linspace(0, 2*np.pi, n_puntos)
    lats = lat + (radio_km/111) * np.cos(angles)
    lons = lon + (radio_km/111) * np.sin(angles)
    return pd.DataFrame({'lat': lats, 'lon': lons})

# --------------------------
# Cálculos
# --------------------------
lat, lon = obtener_coordenadas(lugar, lat_manual, lon_manual)
radio_km = calcular_radio(tamano)
df = generar_puntos_circulo(lat, lon, radio_km, n_puntos=300)

st.write(f"Tamaño: {tamano} m")
st.write(f"Radio estimado: {radio_km:.1f} km")
st.write(f"Coordenadas: {lat:.4f}, {lon:.4f}")

# --------------------------
# Mostrar mapa 3D Pydeck
# --------------------------
MAPBOX_TOKEN = "pk.eyJ1IjoiYWxhbmVsbnVmamFqYSIsImEiOiJjbWdjbjgwdmgwNXN0Mmtwdnh1c2lpcXI4In0.WacI81toXyjM10MlG4GIsw"  # <-- Poner tu token válido
pdk.settings.mapbox_api_key = MAPBOX_TOKEN

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position=["lon", "lat"],
    get_color=[255, 0, 0, 180],
    get_radius=radio_km * 1000,
    pickable=True
)

view_state = pdk.ViewState(
    latitude=lat,
    longitude=lon,
    zoom=6,
    pitch=50,  # inclinación para efecto 3D
    bearing=0
)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/satellite-streets-v12"
)

st.pydeck_chart(r)
