# damage.py
import numpy as np
import pandas as pd

def generar_puntos_circulo(lat, lon, radio_km, n_puntos=200):
    """
    Genera un DataFrame con puntos alrededor de lat/lon formando un círculo 2D.
    Aquí lat/lon se usan como coordenadas planas en km.
    """
    angles = np.linspace(0, 2*np.pi, n_puntos)
    lats = lat + radio_km * np.cos(angles)   # desplazamiento en X
    lons = lon + radio_km * np.sin(angles)   # desplazamiento en Y
    return pd.DataFrame({'lat': lats, 'lon': lons})
