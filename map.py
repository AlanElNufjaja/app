# map.py
import streamlit as st

def mostrar_mapa(df, zoom=6):
    """
    Muestra el mapa con los puntos de impacto utilizando st.map().
    """
    st.map(df, zoom=zoom)
