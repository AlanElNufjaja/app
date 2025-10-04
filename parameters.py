# parameters.py
from geopy.geocoders import Nominatim

# Límites válidos del mapa
LAT_MIN, LAT_MAX = -90.0, 90.0
LON_MIN, LON_MAX = -180.0, 180.0

def obtener_coordenadas(nombre_ciudad, lat_manual=19.4326, lon_manual=-99.1332):
    """
    Devuelve coordenadas (lat, lon) de una ciudad.
    Si no se encuentra o el campo está vacío, usa los valores manuales.
    """
    lat_manual = max(LAT_MIN, min(LAT_MAX, lat_manual))
    lon_manual = max(LON_MIN, min(LON_MAX, lon_manual))
    lat, lon = lat_manual, lon_manual  # valores por defecto

    if nombre_ciudad.strip():
        try:
            geolocator = Nominatim(user_agent="meteoro_app")
            location = geolocator.geocode(nombre_ciudad, timeout=5)
            if location:
                lat, lon = location.latitude, location.longitude
        except Exception:
            pass  # si falla geopy, se quedan los valores manuales

    # Asegurar que no se salga de los límites del mapa
    lat = max(LAT_MIN, min(LAT_MAX, lat))
    lon = max(LON_MIN, min(LON_MAX, lon))
    return lat, lon


def calcular_radio(tamano_metro):
    """
    Calcula un radio visual para el impacto (no geográfico, solo para el mapa 2D).
    """
    # En vez de convertir metros a km reales, solo lo escalamos visualmente
    radio_visual = tamano_metro / 50.0  # ajusta este divisor si se ve muy grande o chico
    return radio_visual
