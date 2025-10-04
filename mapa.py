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
    Funciona en Streamlit.
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
    img_array = np.asarray(img).astype(float)/255

    # Convertir RGB a un solo valor para surfacecolor (promedio de canales)
    surfacecolor = img_array.mean(axis=2)

    # Crear figura
    fig = go.Figure()

    fig.add_trace(go.Surface(
        x=x, y=y, z=z,
        surfacecolor=surfacecolor,
        colorscale='Earth'
