# map.py
import streamlit as st
import pydeck as pdk

pdk.settings.mapbox_api_key = "pk.eyJ1IjoiYWxhbmVsbnVmamFqYSIsImEiOiJjbWdjbjgwdmgwNXN0Mmtwdnh1c2lpcXI4In0.WacI81toXyjM10MlG4GIsw"

def mostrar_mapa(df, lat, lon, radio_km):
    """
    Muestra un mapa 2D interactivo con Pydeck.
    df: DataFrame con lat/lon de los puntos de impacto
    lat, lon: coordenadas del impacto
    radio_km: radio del impacto para escala de color
    """
    # Capa tipo ScatterplotLayer
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_color=[255, 0, 0, 160],  # rojo semitransparente
        get_radius=radio_km * 1000,  # radio en metros
        pickable=True
    )

    # Vista inicial centrada en el impacto
    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=6,
        pitch=0
    )

    # Crear Deck
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/light-v9"
    )

    st.pydeck_chart(r)
