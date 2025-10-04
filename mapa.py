# globo.py
import streamlit as st
import pydeck as pdk
import pandas as pd

def mostrar_mapa(df, lat, lon, radio_km):
    """
    Muestra un mapa 2D interactivo con Pydeck y OpenStreetMap.
    df: DataFrame con columnas 'lat' y 'lon'
    lat, lon: coordenadas del impacto
    radio_km: radio del impacto en km
    """

    # Capa del punto de impacto
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_color=[255, 50, 50, 180],
        get_radius=radio_km * 1000,  # Conversión km → metros
        pickable=True,
    )

    # Estado de vista (sin inclinación)
    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=6,
        pitch=0,  # 0 = vista completamente 2D
        bearing=0,
    )

    # Renderizado del mapa
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",  # Mapa OSM
        tooltip={"text": "Impacto meteorito\nLat: {lat}\nLon: {lon}"}
    )

    st.pydeck_chart(r)


# Ejemplo de uso
if __name__ == "__main__":
    st.title("🌎 Mapa de Impactos de Meteoritos")

    lat = st.sidebar.slider("Latitud manual", -90, 90, 19)
    lon = st.sidebar.slider("Longitud manual", -180, 180, -99)
    tamano = st.sidebar.slider("Tamaño del meteorito (m)", 10, 500, 100)

    df = pd.DataFrame([{"lat": lat, "lon": lon}])

    mostrar_mapa(df, lat, lon, tamano / 1000)  # tamaño convertido a km
