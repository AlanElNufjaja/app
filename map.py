# map.py
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from PIL import Image
import requests
from io import BytesIO

def mostrar_mapa(df, lat, lon, radio_km):
    """
    Globo 3D con textura de la Tierra y punto de impacto.
    """
    # Crear esfera
    theta = np.linspace(0, 2*np.pi, 200)
    phi = np.linspace(0, np.pi, 100)
    theta, phi = np.meshgrid(theta, phi)
    r = 1
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)

    # Cargar imagen de la Tierra
    url = "https://eoimages.gsfc.nasa.gov/images/imagerecords/57000/57730/land_ocean_ice_2048.jpg"
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert("RGB")
    img = img.resize((theta.shape[1], phi.shape[0]))
    img_array = np.asarray(img) / 255  # normalizar

    # Crear figura con textura
    fig = go.Figure()

    # Asignar los canales RGB a surfacecolor
    fig.add_trace(go.Surface(
        x=x, y=y, z=z,
        surfacecolor=np.zeros_like(z),
        colorscale=[[0, 'white'], [1, 'white']],  # placeholder, no afecta porque usamos cmin/cmax y cauto
        showscale=False,
        opacity=1,
        lighting=dict(ambient=1),
        hoverinfo='skip',
        colorsrc=img_array  # esto aplica la textura
    ))

    # Coordenadas del impacto
    lat_rad = np.radians(90 - lat)
    lon_rad = np.radians(lon)
    x_impact = r * np.sin(lat_rad) * np.cos(lon_rad)
    y_impact = r * np.sin(lat_rad) * np.sin(lon_rad)
    z_impact = r * np.cos(lat_rad)

    # Punto de impacto
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
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(fig)
