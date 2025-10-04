# mapa.py
import streamlit as st
import pydeck as pdk

def mostrar_mapa(df, lat, lon, radio_km):
    """
    Muestra un mapa 2D simple con Pydeck.
    """
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_color=[255, 0, 0, 160],
        get_radius=radio_km * 1000,  # metros
        pickable=True
    )

    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=6,
        pitch=0
    )

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="road"
    )

    st.pydeck_chart(r)
