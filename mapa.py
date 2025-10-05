# mapa.py
import streamlit as st
import pydeck as pdk

def mostrar_mapa(df, lat, lon, radio_km):
    """
    Muestra un mapa 2D interactivo con Pydeck con zonas de impacto coloreadas:
    rojo = impacto directo, naranja = cráter, amarillo = contaminación.
    """
    radio_km *=50
    # Capas para cada zona
    capa_negra = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_color=[0, 0, 0, 255],  # rojo
        get_radius=radio_km,
        pickable=False
    )
    capa_rojo = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_color=[255, 0, 0, 160],  # rojo
        get_radius=radio_km*12.5,
        pickable=False
    )

    capa_naranja = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_color=[255, 165, 0, 120],  # naranja
        get_radius=radio_km * 1000,
        pickable=False
    )

    capa_amarillo = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_color=[255, 255, 0, 80],  # amarillo
        get_radius=radio_km * 3 * 250,
        pickable=False
    )

    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=6,
        pitch=0
    )

    deck = pdk.Deck(
        layers=[capa_amarillo, capa_naranja, capa_rojo, capa_negra],
        initial_view_state=view_state,
        map_style="light"
    )

    st.pydeck_chart(deck)
