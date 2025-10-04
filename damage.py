# damage.py
import pandas as pd

def generar_puntos_circulo(lat, lon, radio_km, n_puntos=200):
    """
    Genera un DataFrame representando un círculo 2D.
    En esta versión, simplemente devuelve el centro y el radio.
    lat/lon se usan como coordenadas planas.
    """
    # Un solo punto: el centro del círculo
    lats = [lat]
    lons = [lon]
    return pd.DataFrame({'lat': lats, 'lon': lons, 'radio_km': [radio_km]})
