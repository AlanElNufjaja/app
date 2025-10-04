# mapa.py
import streamlit as st
import pydeck as pdk

pdk.settings.mapbox_api_key = "pk.eyJ1IjoiYWxhbmVsbnVmamFqYSIsImEiOiJjbWdjbmIycnUwNXMxMmxwc2Exemo5NTg2In0.VBBKq9TBBoNS4DFkw8JRuw"

def mostrar_mapa(df, lat, lon, radio_km):
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
        pitch=45,      # efecto 3D visual
        bearing=0
    )

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/satellite-streets-v12"
    )

    st.pydeck_chart(r)
