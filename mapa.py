# mapa.py
import streamlit as st
import folium
from streamlit_folium import st_folium

# Token de Google Maps (opcional, necesario si quieres tiles de Google)
GOOGLE_MAPS_API_KEY = "TU_API_KEY_DE_GOOGLE"

def mostrar_mapa(df, lat, lon, radio_km):
    """
    Muestra un mapa 2D interactivo con Folium y Google Maps.
    df: DataFrame con lat/lon de los puntos de impacto
    lat, lon: coordenadas del impacto
    radio_km: radio del impacto para escala de círculo
    """
    # Crear mapa centrado en el punto de impacto
    m = folium.Map(location=[lat, lon], zoom_start=6, tiles=None)

    # Agregar tile de Google Maps (roadmap)
    folium.TileLayer(
        tiles=f"https://maps.googleapis.com/maps/api/js?key={GOOGLE_MAPS_API_KEY}&callback=initMap",
        attr="Google",
        name="Google Maps",
        control=False
    ).add_to(m)

    # Agregar los puntos de impacto como un círculo
    for _, row in df.iterrows():
        folium.Circle(
            location=[row['lat'], row['lon']],
            radius=radio_km * 1000,  # en metros
            color="red",
            fill=True,
            fill_opacity=0.5
        ).add_to(m)

    # Mostrar el mapa en Streamlit
    st_folium(m, width=700, height=500)
