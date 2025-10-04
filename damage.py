import numpy as np
import pandas as pd

def generar_puntos_circulo(lat, lon, radio_km, n_puntos=500):
    """
    Genera un DataFrame con n_puntos alrededor de lat/lon formando un círculo.
    """
    angles = np.linspace(0, 2*np.pi, n_puntos)
    lats = lat + (radio_km/111) * np.cos(angles)  # aprox grados
    lons = lon + (radio_km / 111) * np.sin(angles)
    return pd.DataFrame({'lat': lats, 'lon': lons})
