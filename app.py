import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from geopy.geocoders import Nominatim

# ---------- Configuración ----------
st.set_page_config(layout="wide")
st.title("Visualizador de Meteoritos 2D ☄️")

# Límites de coordenadas
LAT_MIN, LAT_MAX = -90.0, 90.0
LON_MIN, LON_MAX = -180.0, 180.0

# ---------- Inputs del usuario ----------
lugar = st.sidebar.text_input("Nombre de la ciudad")

lat_manual = st.sidebar.number_input(
    "Latitud manual", value=19.4326, min_value=LAT_MIN, max_value=LAT_MAX
)
lon_manual = st.sidebar.number_input(
    "Longitud manual", value=-99.1332, min_value=LON_MIN, max_value=LON_MAX
)
tamano = st.sidebar.slider("Tamaño del meteorito (m)", 10, 500, 100)

# ---------- Funciones ----------

def obtener_coordenadas(nombre_ciudad, lat_manual=0.0, lon_manual=0.0):
    """
    Convierte un nombre de ciudad a lat/lon usando Geopy.
    Si falla o está vacío, usa lat/lon manual.
    """
    lat, lon = lat_manual, lon_manual

    if nombre_ciudad.strip() != "":
        try:
            geolocator = Nominatim(user_agent="meteoro_app")
            location = geolocator.geocode(nombre_ciudad, timeout=5)
            if location:
                lat, lon = location.latitude, location.longitude
        except:
            pass  # fallback a lat/lon manual

    # Limitar coordenadas a rangos válidos
    lat = max(LAT_MIN, min(LAT_MAX, lat))
    lon = max(LON_MIN, min(LON_MAX, lon))
    return lat, lon


def calcular_radio(tamano_metro):
    """
    Calcula radio estimado de impacto en km según tamaño del meteorito.
    """
    return tamano_metro * 0.1


def generar_puntos_circulo(lat, lon, radio_km, n_puntos=500):
    """
    Genera puntos en círculo alrededor de lat/lon con radio_km
    """
    angles = np.linspace(0, 2*np.pi, n_puntos)
    lats = lat + (radio_km/111) * np.cos(angles)
    lons = lon + (radio_km/(111*np.cos(np.radians(lat)))) * np.sin(angles)
    return pd.DataFrame({'lat': lats, 'lon': lons})


def mostrar_mapa(df, lat, lon, radio_km):
    """
    Muestra el mapa 2D con Pydeck sin necesidad de token Mapbox
    """
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_color=[255,0,0,200],
        get_radius=radio_km*1000  # en metros
    )

    view_state = pdk.ViewState(latitude=lat, longitude=lon, zoom=4, pitch=0)

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="open-street-map"  # estilo libre sin token
    )

    st.pydeck_chart(deck)


# ---------- Lógica principal ----------
lat, lon = obtener_coordenadas(lugar, lat_manual, lon_manual)
radio_km = calcular_radio(tamano)
df = generar_puntos_circulo(lat, lon, radio_km, n_puntos=500)

st.write(f"Coordenadas finales: {lat:.4f}, {lon:.4f}")
st.write(f"Tamaño meteorito: {tamano} m")
st.write(f"Radio estimado de impacto: {radio_km:.1f} km")

mostrar_mapa(df, lat, lon, radio_km)
