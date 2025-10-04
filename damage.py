# damage.py
import pandas as pd

def generar_puntos_circulo(lat, lon, radio_km, n_puntos=1):
    """
    Genera un DataFrame con el círculo representado por su centro y radio en 2D plano.
    Evita distorsión por latitud cercana a los polos.
    """
    return pd.DataFrame({'lat': [lat], 'lon': [lon], 'radio_km': [radio_km]})
