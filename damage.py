import numpy as np
import pandas as pd

def generar_puntos_circulo(lat, lon, radio_km, n_puntos=200):
    """
    Genera un círculo 2D en torno a un punto (lat, lon).
    No usa fórmulas geográficas, es una aproximación visual.
    Ideal para mapas planos con Pydeck o Folium.
    """
    # Radio relativo pequeño para evitar distorsiones visuales
    escala = radio_km / 100.0  

    angulos = np.linspace(0, 2 * np.pi, n_puntos)
    lats = lat + escala * np.cos(angulos)
    lons = lon + escala * np.sin(angulos)

    return pd.DataFrame({'lat': lats, 'lon': lons})
