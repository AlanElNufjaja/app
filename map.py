# map.py
import streamlit as st
import pydeck as pdk

def mostrar_mapa(df, lat, lon, radio_km):
    """
    Muestra un mapa 3D con Pydeck mostrando la zona de impacto.
    
    df: DataFrame con lat/lon de los puntos
    lat, lon: centro del impacto
    radio_km: radio del impacto en km (para la altura del cráter)
    """
    # Creamos una nueva columna de altura según el radio
    df['elevation'] = radio_km * 1000  # altura proporcional al radio

    # Capa 3D tipo HexagonLayer
    layer = pdk.Layer(
        "HexagonLayer",
        data=df,
        get_position=["lon", "lat"],
        auto_highlight=True,
        radius=5000,  # radio de los hexágonos en metros
        elevation_scale=50,  # escala de altura
        pickable=True,
        elevation_range=[0, 1000],
        extruded=True,
    )

    # Vista inicial centrada en el impacto
    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=6,
        pitch=45,
        bearing=0
    )

    # Crear el deck
    r = pdk.Deck(layers=[layer], initial_view_state=view_state, map_style='mapbox://styles/mapbox/light-v9')

    # Mostrar en Streamlit
    st.pydeck_chart(r)

