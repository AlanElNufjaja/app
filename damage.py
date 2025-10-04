import pandas as pd

def generar_puntos_circulo(lat, lon, radio_km, n_puntos=1):
    """
    Genera un DataFrame con el círculo representado por su centro y radio en 2D plano.
    """
    return pd.DataFrame({'lat': [lat], 'lon': [lon], 'radio_km': [radio_km]})

def calcular_radio_impacto(tamano_m, densidad, velocidadkms, k=0.05):
    """
    Calcula un radio estimado de destrucción en km según parámetros del meteorito:
    - tamano_m: diámetro en metros
    - densidad: kg/m³
    - velocidad: m/s
    """
    velocidad = velocidadkms*1000
    radio = k * (tamano_m**(1/3)) * (densidad**(1/3)) * (velocidad**(2/3))
    return radio
