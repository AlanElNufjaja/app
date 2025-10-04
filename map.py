# map.py
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

def mostrar_mapa(df, lat, lon, radio_km):
    """
    Muestra un globo terráqueo 3D con los puntos de impacto.
    """
    # Crear esfera (globo)
    theta = np.linspace(0, 2*np.pi, 100)
    phi = np.linspace(0, np.pi, 50)
    theta, phi = np.meshgrid(theta, phi)
    r = 1
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)

    # Crear figura
    fig = go.Figure()

    # Superficie del globo
    fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale='Blues', opacity=0.7, showscale=False))

    # Convertir lat/lon a coordenadas 3D sobre la esfera
    lat_rad = np.radians(90 - lat)
    lon_rad = np.radians(lon)
    x_impact = r * np.sin(lat_rad) * np.cos(lon_rad)
    y_impact = r * np.sin(lat_rad) * np.sin(lon_rad)
    z_impact = r * np.cos(lat_rad)

    # Añadir punto de impacto
    fig.add_trace(go.Scatter3d(
        x=[x_impact],
        y=[y_impact],
        z=[z_impact],
        mode='markers',
        marker=dict(size=5 + radio_km/10, color='red'),
        name='Impacto'
    ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(fig)
