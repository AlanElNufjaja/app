# parameters.py
from geopy.geocoders import Nominatim

# Límites
LAT_MIN, LAT_MAX = -90.0, 90.0
LON_MIN, LON_MAX = -180.0, 180.0

def obtener_coordenadas(nombre_ciudad, lat_manual=19.4326, lon_manual=-99.1332):
    """
    Convierte un nombre de ciudad a lat/lon usando Geopy.
    Si falla o está vacío, usa lat/lon manual y ajusta a límites válidos.
    """
    lat_manual = max(LAT_MIN, min(LAT_MAX, lat_manual))
    lon_manual = max(LON_MIN, min(LON_MAX, lon_manual))
    lat, lon = lat_manual, lon_manual

    if nombre_ciudad.strip() != "":
        try:
            geolocator = Nominatim(user_agent="meteoro_app")
            location = geolocator.geocode(nombre_ciudad, timeout=5)
            if location:
                lat, lon = location.latitude, location.longitude
        except:
            pass

    lat = max(LAT_MIN, min(LAT_MAX, lat))
    lon = max(LON_MIN, min(LON_MAX, lon))
    return lat, lon

def calcular_radio(tamano_metro):
    """Calcula un radio aproximado de impacto en km"""
    return tamano_metro * 0.1
