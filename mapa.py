# globo.py
import streamlit as st
import pydeck as pdk

# Tu token de Mapbox
pdk.settings.mapbox_api_key = "sk.eyJ1IjoiYWxhbmVsbnVmamFqYSIsImEiOiJjbWdjbmgyMXkxZ2xrMmpvY3o1enE4OXJzIn0.XSl3O7XF_-TuM7dLncF4hQ"

def mostrar_mapa(df, lat, lon, radio_km):
    """
    Muestra un mapa 2D interactivo con Pydeck.
    df: DataFrame con lat/lon de los puntos de impacto
    lat, lon: coordenadas del impacto
    radio_km: radio del impacto para escala de color
    """
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_color=[255, 0, 0, 160],
        get_radius=radio_km * 1000,  # radio en metros
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
