# damage.py
import numpy as np
import pandas as pd

def generar_puntos_circulo(lat, lon, radio_km, n_puntos=500):
    """
    Genera un DataFrame con puntos dentro de un círculo para simular la zona de daño del impacto.
    """
    angles = np.random.rand(n_puntos) * 2 * np.pi
    r = np.random.rand(n_puntos) ** 0.5 * (radio_km / 111)  # 1° ≈ 111 km
    latitudes = lat + r * np.cos(angles)
    longitudes = lon + r * np.sin(angles)
    
    df = pd.DataFrame({
        "lat": latitudes,
        "lon": longitudes
    })
    
    return df
