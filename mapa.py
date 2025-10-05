import streamlit as st
import pydeck as pdk

def mostrar_mapa(df, lat, lon, radio_km, tipodano):
    radio_km *= 50

    if tipodano == "Impacto y crater":
        capa_negra = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[0, 0, 0, 150], 
            get_radius=radio_km,
            pickable=False,
            get_line_color=[0, 0, 0, 255],  
            get_line_width=1
        )
        capa_rojo = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[255, 0, 0, 100],  
            get_radius=radio_km*35,
            pickable=False,
            get_line_color=[255, 0, 0, 255],  
            get_line_width=1
        )
        layers = [capa_negra, capa_rojo]
        
    elif tipodano == "Bola de fuego": 
        capa_negra = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[255, 0, 0, 240], 
            get_radius=radio_km*50,
            pickable=False,
            get_line_color=[0, 0, 0, 255],  
            get_line_width=1
        )
        capa_rojo = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[255, 0, 0, 1000],
            get_radius=radio_km*250,
            pickable=False,
            get_line_color=[255, 0, 0, 255],  
            get_line_width=1
        )
        capa_naranja = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[255, 165, 0, 80],
            get_radius=radio_km * 250,
            pickable=False,
            get_line_color=[255, 165, 0, 255],  
            get_line_width=1
        )

        capa_amarillo = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[255, 255, 0, 80],
            get_radius=radio_km * 500,
            pickable=False,
            get_line_color=[255, 255, 0, 255],  
            get_line_width=1
        )
        layers = [capa_negra, capa_rojo, capa_naranja, capa_amarillo]

    elif tipodano == "Sonido":
        capa_negra = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[0, 0, 255, 50],  
            get_radius=radio_km * 750,
            pickable=False,
            get_line_color=[0, 0, 0, 255],  
            get_line_width=1
        )
        capa_rojo = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[0, 0, 200, 50],  
            get_radius=radio_km * 600,
            pickable=False,
            get_line_color=[0, 0, 200, 255],  
            get_line_width=1
        )
        capa_naranja = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[0, 128, 255, 50],  
            get_radius=radio_km * 450,
            pickable=False,
            get_line_color=[0, 128, 255, 255],  
            get_line_width=1
        )
        capa_amarillo = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[128, 255, 255, 50],  
            get_radius=radio_km * 300,
            pickable=False,
            get_line_color=[128, 255, 255, 255],  
            get_line_width=1
        )
        layers = [capa_negra, capa_rojo, capa_naranja, capa_amarillo]

    elif tipodano == "Terremotos":
        capa_negra = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[139, 0, 0, 50],
            get_radius=radio_km * 750,
            pickable=False,
            get_line_color=[139, 0, 0, 255],  
            get_line_width=1
        )
        capa_rojo = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[255, 0, 0, 50],  
            get_radius=radio_km * 600,
            pickable=False,
            get_line_color=[255, 0, 0, 255],  
            get_line_width=1
        )
        capa_naranja = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[255, 165, 0, 50],  
            get_radius=radio_km * 450,
            pickable=False,
            get_line_color=[255, 165, 0, 255],  
            get_line_width=1
        )
        capa_amarillo = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color=[255, 255, 0, 50],  
            get_radius=radio_km * 300,
            pickable=False,
            get_line_color=[255, 255, 0, 255],  
            get_line_width=1
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
