import streamlit as st
import pydeck as pdk

def mostrar_mapa(df, lat, lon, radio_km, tipodano):
    radio_km *= 50

    if tipodano == "Impacto y crater":
        capa_negra = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[0, 0, 0, 255], 
            get_radius=radio_km,
            pickable=False
        )
        capa_rojo = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[255, 0, 0, 160],  
            get_radius=radio_km*12.5,
            pickable=False
        )
        layers = [capa_negra, capa_rojo]
        
    elif tipodano == "Bola de fuego": 
        capa_rojo = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[255, 0, 0, 160],
            get_radius=radio_km*100,
            pickable=False
        )
        capa_naranja = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[255, 40, 40, 120],
            get_radius=radio_km * 500,
            pickable=False
        )

        capa_amarillo = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[255, 90, 54, 80],
            get_radius=radio_km * 750,
            pickable=False
        )
        layers = [capa_rojo, capa_naranja, capa_amarillo]

    elif tipodano == "Sonido":
        capa_negra = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[16, 16, 148, 180],
            get_radius=radio_km * 750,
            pickable=False
        )
        capa_rojo = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[36, 36, 169, 80],  
            get_radius=radio_km * 750,
            pickable=False
        )
        capa_naranja = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[62, 62, 194, 80],  
            get_radius=radio_km * 750,
            pickable=False
        )
        capa_amarillo = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[111, 111, 209, 80],  
            get_radius=radio_km * 750,
            pickable=False
        )
        layers = [capa_negra, capa_rojo, capa_naranja, capa_amarillo]

    elif tipodano == "Terremotos":
        capa_negra = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[151, 31, 22, 180],
            get_radius=radio_km * 750,
            pickable=False
        )
        capa_rojo = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[209, 21, 7, 80],  
            get_radius=radio_km * 750,
            pickable=False
        )
        capa_naranja = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[225, 58, 45, 80],  
            get_radius=radio_km * 750,
            pickable=False
        )
        capa_amarillo = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[221, 124, 117, 80],  
            get_radius=radio_km * 750,
            pickable=False
        )
        layers = [capa_negra, capa_rojo, capa_naranja, capa_amarillo]

    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=6,
        pitch=0
    )

    deck = pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        map_style="light"
    )

    st.pydeck_chart(deck)
