# parameters.py
import requests

def obtener_coordenadas(lugar):
    """
    Obtiene las coordenadas geográficas de un lugar utilizando la NASA Meteorite Landings API.
    Si no se encuentra el lugar, devuelve coordenadas predeterminadas.
    """
    url = f"https://data.nasa.gov/api/3/action/datastore_search_sql?sql=SELECT%20*%20FROM%20meteorite_landings%20WHERE%20name%20LIKE%20'{lugar}%'"
    response = requests.get(url)
    data = response.json()
    
    if data['result']['records']:
        record = data['result']['records'][0]
        lat, lon = float(record['reclat']), float(record['reclong'])
        return lat, lon
    else:
        # Coordenadas predeterminadas si no se encuentra el lugar
        return 19.4326, -99.1332

def calcular_radio(tamano):
    """
    Calcula el radio de impacto en kilómetros según el tamaño del meteorito.
    """
    return tamano * 0.1  # Ejemplo: cada 10 metros de tamaño = 1 km de radio
