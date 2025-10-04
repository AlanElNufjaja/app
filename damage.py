import numpy as np
import pandas as pd

def generar_puntos_circulo(lat, lon, radio_km, n_puntos=200):
    """
    Genera puntos distribuidos en un círculo 2D alrededor de (lat, lon).
    No usa trigonometría compleja, pero sí un radio proporcional para mapa plano.
    """
    # Escala simple: 1 grado ≈ 111 km (no exacto, pero suficiente para mapa 2D)
    escala = radio_km / 111.0

    # Generar ángulos desde 0 hasta 360 grados
    angulos = np.linspace(0, 2 * np.pi, n_puntos)

    # Generar puntos en el borde del "círculo"
    lats = lat + escala * np.cos(angulos)
    lons = lon + escala * np.sin(angulos)

    return pd.DataFrame({'lat': lats, 'lon': lons})
