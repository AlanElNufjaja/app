# parameters.py
from geopy.geocoders import Nominatim

# Limites
LAT_MIN, LAT_MAX = -90.0, 90.0
LON_MIN, LON_MAX = -180.0, 180.0

def obtener_coordenadas(nombre_ciudad, lat_manual=0.0, lon_manual=0.0):
    """
    Convierte un nombre de ciudad a lat/lon usando Geopy.
    Si falla o está vacío, usa lat/lon manual y ajusta a límites válidos.
    """
    if nombre_ciudad.strip() == "":
        return limitar_coordenadas(lat_manual, lon_manual)

    try:
        geolocator = Nominatim(user_agent="meteoro_app")
        location = geolocator.geocode(nombre_ciudad, timeout=10)
        if location:
            return limitar_coordenadas(location.latitude, location.longitude)
        else:
            return limitar_coordenadas(lat_manual, lon_manual)
    except:
        return limitar_coordenadas(lat_manual, lon_manual)


def limitar_coordenadas(lat, lon):
    """
    Ajusta latitud y longitud a los límites válidos.
    """
    lat = max(LAT_MIN, min(LAT_MAX, lat))
    lon = max(LON_MIN, min(LON_MAX, lon))
    return lat, lon


def calcular_radio(tamano_metro):
    """
    Calcula un radio estimado de impacto en km según tamaño del meteorito.
    """
    radio_km = tamano_metro * 0.1
    return radio_km
